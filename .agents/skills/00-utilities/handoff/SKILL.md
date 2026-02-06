---
name: handoff
description: This skill should be used when preparing a handoff checklist for agents and persisting it as a handoff note that can be picked up in a fresh thread.
---

# /handoff

Purpose: package the current state so the next agent (or future you) can resume quickly.

## Persist the handoff note (always)

- Determine repo root.
  - Prefer: `git rev-parse --show-toplevel`
  - Fallback: current working directory
- Use a git-tracked handoff area so it can be reused later (including via automations):
  - If the work is tied to a dossier under `docs/04-projects/.../<dossier>/`: write to `<dossier>/tmp-handoffs/`.
  - Otherwise (non-dossier or cross-dossier): write to `docs/98-tmp/handoffs/`.
- Create the folder if missing.
- Generate filename using the handoff time:
  - `handoff_YYYY-MM-DD_HH-MM-SS_<3-5 words>.md`
  - Choose 3–5 words that describe the work or topic.
  - Prefer lowercase kebab-case for the words (avoid spaces and special characters).
- Write the handoff checklist content into that markdown file.
- Echo the saved file path at the top of the handoff output.

## Handoff checklist content (write in this order)

1) Scope/status: what you were doing, what’s done, what’s pending, and any blockers.
2) Working tree: `git status -sb` summary and whether there are local commits not pushed.
3) Branch/PR: current branch, relevant PR number/URL, CI status if known.
4) Running processes: list tmux sessions/panes and how to attach:
   - Example: `tmux attach -t codex-shell` or `tmux capture-pane -p -J -t codex-shell:0.0 -S -200`
   - Note dev servers, tests, debuggers, background scripts.
5) Tests/checks: which commands were run, results, and what still needs to run.
6) Next steps: ordered bullets the next agent should do first.
7) Risks/gotchas: any flaky tests, credentials, feature flags, or brittle areas.

## Output format

- Start with: “Saved handoff: <path>”
- Then a concise bullet list (copy/paste friendly).
- Include copy/paste tmux commands for any live sessions.

## Notes

- Prefer writing the note even if the session continues. A fresh thread can be started at any time without losing state.
- If file write is not possible, print the handoff checklist in chat and ask the user to save it into the git-tracked handoff area.
