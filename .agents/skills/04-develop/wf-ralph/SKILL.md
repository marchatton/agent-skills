---
name: wf-ralph
description: This skill should only be used when the user uses the word workflow and asks to run the Ralph workflow loop (dev/review/research/e2e).
---

# wf-ralph

## Purpose
Continuous Ralph loop for dev, code review, e2e testing, research and more.

## Inputs
- PRD path (prd.md + prd.json) per docs/AGENTS. Ask if unsure.
- Mode: dev | code review | research | e2e.
- Iteration count (default 5).
- Quick-check commands (default: verify skill).
- Optional: browser command prefix for e2e dev/CDP port 9222.
- Optional: `AGENT_CMD` override (codex default; amp/claude/gemini ok).

## Outputs
- Updated prd.json (passes true per story).
- `.ralph/` state + logs.
- Optional: dossier log per docs/AGENTS.md.

## Steps
1. Confirm PRD path + branch. 
2. Ask for mode, iteration count, quick checks (default verify).
3. Loop `ralph build 1` for N iterations.
4. After each iteration:
   - Run quick checks (skip for research mode).
   - Fix failures before next iteration.
   - Mark story pass only when checks green + acceptance criteria met.
   - Research mode: ship the artifact (doc/decision/plan), not code.
   - If e2e mode or UI story: run `test-browser` diagnostics and capture evidence.
5. After core loop, run `wf-review` once (no review inside core loop).
6. If `wf-review` finds issues, run a follow-up Ralph loop only if requested.

## E2E diagnostics (test-browser)

Run browser smoke in dev mode via `test-browser`; keep it minimal and capture evidence.

### Optional: CDP port 9222
Only if your installed browser CLI supports `--cdp`. Use the `test-browser` flow and add `--cdp 9222` where supported.

## Verification
- Verify skill
- `wf-review` after entire rap loop is finished.

## Go/No-Go
- GO if checks green, acceptance criteria met, and (if run) wf-review is GO.
- NO-GO if any required verification fails.
