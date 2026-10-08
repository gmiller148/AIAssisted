# AIAssisted

A learning workspace based on [amosblomqvist/learn](https://github.com/amosblomqvist/learn) (his "How I Use AI to Learn Things" system). It runs under two harnesses from the same repo:

- **Claude Code**: config in `.claude/` (skills, agents, hooks, render tools).
- **Pi** ([earendil-works/pi](https://github.com/earendil-works/pi)): config in `.pi/` (skills, agents, extensions). Differs from upstream: `quiz.ts` and `ask-user-question.ts` wrap long option labels instead of truncating them.

Core pieces: a `teach` skill (orient → probe → plan → teach), a `visualize` skill that delegates to `svg-maker` / `mermaid-maker` subagents, a `researcher` subagent that verifies claims, and `md-log`, which mirrors a session into a markdown lesson file (written for Obsidian).

## Instructions for an agent setting this up

Do the shared steps, then the section for the harness your user wants. Check each step before running it; skip what is already installed. macOS is assumed; the Chrome path in `.claude/tools/render.mjs` is macOS-specific.

### Shared

1. Node 20+ and git. Google Chrome installed at `/Applications/Google Chrome.app` (used to render diagrams).
2. Create the folders the tools write into: `mkdir -p lessons viz`.
3. Install the diagram renderers: `cd .claude/tools && npm install` (puppeteer and mermaid-cli, ~400 MB).

### Claude Code

Nothing else to install. Open Claude Code in the repo root; `.claude/settings.json` wires the `md-log` hooks (they call `python3`, so Python 3 must be on PATH). The `teach`, `visualize` and `md-log` skills and the three agents load automatically.

### Pi

1. Install Pi: `npm i -g @earendil-works/pi-coding-agent`.
2. Install subagents (needs `tmux`): `pi install git:github.com/amosblomqvist/pi-interactive-subagents`.
3. Install the visual tools' dependencies: `cd .pi/extensions/visual-tools && npm install`.
4. Optional global extensions from [amosblomqvist/pi-config](https://github.com/amosblomqvist/pi-config). Copy individual folders into `~/.pi/agent/extensions/` and run `npm install` inside any that has a `package.json`; do not clone over an existing `~/.pi/agent`. Used here: `bash-guard/`, `web-fetch/`, `custom-header.ts`. Do **not** also copy his `ask-user-question.ts`: this repo bundles its own, and two copies break popup locking. `web-search/` needs a Google search API key; without it the `researcher` agent has no `web_search`.
5. The user must authenticate themselves: run `pi`, then `/login` (or set a provider API key such as `ANTHROPIC_API_KEY`). Do not ask for or handle their keys.
6. Run Pi from the repo root inside tmux so subagents can open panes: `tmux new -A -s pi 'pi'`. Use `/reload` after changing extensions.

Known issues:
- Some models (seen with Kimi via OpenRouter) emit malformed tool calls with their reasoning text inside the arguments, which breaks `ask_user_question`. Switch models with `/model` if popups never appear.
- `.pi/agents/researcher.md` lists a `safe_bash` tool; confirm your subagent implementation provides it or edit the `tools:` line.

### Not in this repo

`lessons/` (the user's notes), `reference/` (the source video transcript), `.obsidian/`, and session logs are git-ignored. `CLAUDE.md` mentions `reference/`; it is optional.
