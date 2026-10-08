---
name: md-log
description: Link this session to a markdown file so it's mirrored for reading in Obsidian. `/md-log <file>` to link, `/md-log off` to stop.
argument-hint: "<file.md> | off"
disable-model-invocation: true
---

If the argument is `off`, run:

```bash
python3 .claude/hooks/md_log.py unlink
```

Otherwise run:

```bash
python3 .claude/hooks/md_log.py link "$ARGUMENTS" --open
```

Reply with one line: the linked file path. Nothing else.
