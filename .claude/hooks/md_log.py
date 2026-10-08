#!/usr/bin/env python3
"""Mirror a Claude Code session into a markdown file for reading in Obsidian.

Port of the pi `md-log` extension from github.com/amosblomqvist/learn.
Logs user prompts, assistant prose, and AskUserQuestion Q&A; omits other tools.
Also gates AskUserQuestion: denied unless visible text precedes it since the learner last spoke.

  md_log.py link <file.md> [--open]   link this session (CLAUDE_CODE_SESSION_ID) to a file
  md_log.py unlink                    stop logging this session
  md_log.py hook                      hook entry point (Stop / PreToolUse / PostToolUse), JSON on stdin
"""

import json
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
STATE_DIR = PROJECT / ".claude" / "md-log"
ASK = "AskUserQuestion"


def state_path(session_id):
    return STATE_DIR / f"{session_id}.json"


def load_state(session_id):
    p = state_path(session_id)
    if not p.exists():
        return None
    return json.loads(p.read_text())


def save_state(session_id, state):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_path(session_id).write_text(json.dumps(state))


def append(state, text):
    f = Path(state["file"])
    current = f.read_text() if f.exists() else ""
    prefix = "\n" if current.strip() else ""
    with f.open("a") as fh:
        fh.write(prefix + text + "\n")


def callout(kind, title, body_lines):
    lines = [f"> [!{kind}] {title}"]
    lines += [">" if not l else f"> {l}" for l in body_lines]
    return "\n".join(lines)


def question_blocks(tool_input):
    out = []
    for q in tool_input.get("questions", []):
        body = q.get("question", "").split("\n")
        opts = q.get("options", [])
        if opts:
            body.append("")
            for i, o in enumerate(opts, 1):
                body.append(f"{i}. {o.get('label', '')}")
                if o.get("description"):
                    body.append(f"    {o['description']}")
        if q.get("multiSelect"):
            body += ["", "*(select all that apply)*"]
        out.append(callout("question", q.get("header") or "Question", body))
    return out


def answer_block(result):
    if not isinstance(result, dict) or "answers" not in result:
        return callout("warning", "Answer", ["(no answer — skipped or cancelled)"])
    annotations = result.get("annotations") or {}
    body = []
    for q, a in result["answers"].items():
        body.append(f"**{a}**")
        note = (annotations.get(q) or {}).get("notes")
        if note:
            body.append(f"Note: {note}")
    return callout("example", "YOUR ANSWER", body or ["(no answer)"])


NOISE = re.compile(r"<(system-reminder|local-command-stdout|local-command-caveat)>[\s\S]*?</\1>")


def user_text(content):
    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        if any(b.get("type") == "tool_result" for b in content):
            return None
        text = "\n".join(b.get("text", "") for b in content if b.get("type") == "text")
    else:
        return None
    text = NOISE.sub("", text).strip()
    m = re.search(r"<command-name>/?([^<]+)</command-name>", text)
    if m:
        name = m.group(1).strip()
        if name == "md-log":
            return None
        args = re.search(r"<command-args>([\s\S]*?)</command-args>", text)
        args = args.group(1).strip() if args else ""
        return f"> [!note] /{name} {args}".rstrip()
    if not text or text.startswith("[Request interrupted"):
        return None
    return f"> [!quote] YOU\n\n{text}"


def render_entry(entry, state):
    """Markdown blocks for one transcript entry."""
    if entry.get("isSidechain") or entry.get("isMeta"):
        return []
    msg = entry.get("message") or {}
    content = msg.get("content")
    if entry.get("type") == "user":
        if isinstance(content, list):
            out = []
            for b in content:
                if b.get("type") == "tool_result" and b.get("tool_use_id") in state["asks"]:
                    tid = b["tool_use_id"]
                    if tid not in state["answered"]:
                        state["answered"].append(tid)
                        out.append(answer_block(entry.get("toolUseResult")))
            if out:
                return out
        block = user_text(content)
        return [block] if block else []
    if entry.get("type") == "assistant" and isinstance(content, list):
        out = []
        for b in content:
            if b.get("type") == "text" and b.get("text", "").strip():
                out.append(f"> [!abstract] CLAUDE\n\n{b['text'].strip()}")
            elif b.get("type") == "tool_use" and b.get("name") == ASK:
                if b["id"] not in state["asks"]:
                    state["asks"].append(b["id"])
                    out += question_blocks(b.get("input") or {})
        return out
    return []


def read_entries(transcript):
    entries = []
    with open(transcript) as fh:
        for line in fh:
            if not line.endswith("\n"):
                break
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                entries.append({})
    return entries


def sync(state, transcript):
    """Log transcript entries past state['offset']."""
    entries = read_entries(transcript)
    blocks = []
    for e in entries[state["offset"]:]:
        blocks += render_entry(e, state)
    state["offset"] = len(entries)
    for b in blocks:
        append(state, b)


def turn_finished(entries):
    for e in reversed(entries):
        if e.get("type") in ("user", "assistant") and not e.get("isSidechain"):
            c = (e.get("message") or {}).get("content")
            return e["type"] == "assistant" and isinstance(c, list) and not any(b.get("type") == "tool_use" for b in c)
    return False


def wait_for(transcript, pred, timeout=2.0):
    # The transcript can lag the hook by a moment; poll briefly so ordering stays right.
    deadline = time.time() + timeout
    while time.time() < deadline:
        if pred(read_entries(transcript)):
            return True
        time.sleep(0.05)
    return False


MIN_VISIBLE_CHARS = 120

SILENT_ASK_REASON = (
    "Blocked: the learner sees only your visible text, and you have written none since their last "
    "answer or message. Anything in your reasoning never reached them. First write, as visible text: "
    "the grade and explanation for their last answer (if any), a reply to anything they asked, and "
    "every definition, setup, or number this question relies on. Then ask again."
)


def visible_text_since_learner(entries):
    """Chars of visible assistant text since the learner last spoke (a prompt or an AskUserQuestion answer)."""
    chars = 0
    for e in reversed(entries):
        if e.get("isSidechain") or e.get("isMeta"):
            continue
        c = (e.get("message") or {}).get("content")
        if e.get("type") == "assistant" and isinstance(c, list):
            chars += sum(len(b.get("text", "").strip()) for b in c if b.get("type") == "text")
        elif e.get("type") == "user":
            if isinstance(c, str):
                break
            if isinstance(c, list):
                if any(b.get("type") == "text" for b in c):
                    break
                if any(b.get("type") == "tool_result" and is_ask_result(entries, b.get("tool_use_id")) for b in c):
                    break
    return chars


def is_ask_result(entries, tool_use_id):
    for e in entries:
        c = (e.get("message") or {}).get("content")
        if isinstance(c, list):
            for b in c:
                if b.get("type") == "tool_use" and b.get("id") == tool_use_id:
                    return b.get("name") == ASK
    return False


def hook():
    data = json.load(sys.stdin)
    event = data.get("hook_event_name")
    is_ask = data.get("tool_name") == ASK
    transcript = data.get("transcript_path")
    tool_use_id = data.get("tool_use_id")
    have_transcript = bool(transcript) and os.path.exists(transcript)

    # The pending tool_use isn't in the transcript yet when PreToolUse fires, so read back from the end.
    if event == "PreToolUse" and is_ask and have_transcript:
        silent = lambda es: visible_text_since_learner(es) < MIN_VISIBLE_CHARS
        if silent(read_entries(transcript)) and not wait_for(transcript, lambda es: not silent(es), timeout=1.0):
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": SILENT_ASK_REASON,
            }}))
            return

    session_id = data.get("session_id")
    state = load_state(session_id) if session_id else None
    if not state or not have_transcript:
        return

    if event == "PreToolUse" and is_ask:
        sync(state, transcript)
        if tool_use_id not in state["asks"]:
            state["asks"].append(tool_use_id)
            for b in question_blocks(data.get("tool_input") or {}):
                append(state, b)
    elif event == "PostToolUse" and is_ask:
        if tool_use_id not in state["answered"]:
            state["answered"].append(tool_use_id)
            append(state, answer_block(data.get("tool_response")))
    elif event == "Stop":
        wait_for(transcript, turn_finished)
        sync(state, transcript)
    save_state(session_id, state)


def link(target, open_it):
    session_id = os.environ.get("CLAUDE_CODE_SESSION_ID")
    if not session_id:
        sys.exit("CLAUDE_CODE_SESSION_ID is not set; run this from inside Claude Code.")
    p = Path(target)
    if p.suffix != ".md":
        p = p.with_name(p.name + ".md")
    if not p.is_absolute():
        p = PROJECT / (p if len(p.parts) > 1 else Path("lessons") / p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.touch()
    prev = load_state(session_id)
    save_state(session_id, {"file": str(p), "offset": 0, "asks": [], "answered": []})
    if prev and prev["file"] != str(p):
        print(f"Relinked from {prev['file']}")
    print(f"Linked this session to {p}\nThe full session is backfilled at the end of this turn.")
    uri = "obsidian://open?path=" + urllib.parse.quote(str(p))
    print(f"Obsidian: {uri}")
    if open_it:
        os.system(f"open '{uri}'")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "hook"
    if cmd == "hook":
        try:
            hook()
        except Exception as e:  # a logging failure must never block the session
            print(f"md-log: {e}", file=sys.stderr)
    elif cmd == "link" and len(sys.argv) > 2:
        link(sys.argv[2], "--open" in sys.argv[3:])
    elif cmd == "unlink":
        sid = os.environ.get("CLAUDE_CODE_SESSION_ID", "")
        state_path(sid).unlink(missing_ok=True)
        print("md-log: stopped logging this session.")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
