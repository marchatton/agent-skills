---
name: pickup
description: This skill should be used when preparing a pickup checklist when starting a task, rehydrating context from the latest handoff note if available.
---

# /pickup

Purpose: rehydrate context quickly when you start work.

## Read a handoff note first (preferred)

- If the user provides a handoff note path, read that file first.
- Else, attempt to locate the most recent handoff note under repo root:
  - If the work is tied to a dossier: `<dossier>/tmp-handoffs/handoff_*.md`
  - Otherwise (or if unsure): `docs/04-projects/**/tmp-handoffs/handoff_*.md`
  - Also check cross-dossier handoffs: `docs/98-tmp/handoffs/handoff_*.md`
- If no handoff note exists, continue with the standard pickup steps.

## Pickup steps

1) Read AGENTS.MD pointer + relevant docs (run `pnpm run docs:list` if present).
2) Repo state: `git status -sb`; check for local commits; confirm current branch/PR.
3) CI/PR: `gh pr view <num> --comments --files` (or derive PR from branch) and note failing checks.
4) tmux/processes: list sessions and attach if needed:
   - `tmux list-sessions`
   - If sessions exist: `tmux attach -t codex-shell` or `tmux capture-pane -p -J -t codex-shell:0.0 -S -200`
5) Tests/checks: note what last ran (from handoff notes/CI) and what you will run first.
6) Plan next 2–3 actions as bullets and execute.

## Output format

- Concise bullet summary.
- Include copy/paste tmux attach/capture commands when live sessions are present.

## Notes

- Prefer starting new threads between workflows: run `handoff`, start a new thread, then run `pickup`.
- If the handoff note contradicts the current repo state, trust the repo state and call out the mismatch.
