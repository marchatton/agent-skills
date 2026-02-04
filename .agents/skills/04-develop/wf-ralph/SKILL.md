---
name: wf-ralph
description: This skill should only be used when the user uses the word workflow and asks to run the Ralph workflow loop (dev/review/research/e2e) with verification and periodic handoff/pickup checkpoints to avoid context rot.
---

# wf-ralph

## Purpose

Run iterative Ralph loops without letting context rot. Use checkpoints (handoff → new thread → pickup) to keep each block crisp.

## Inputs (free text)

Parse from user text; ask if missing.

Required:
- PRD path (prd.md + prd.json). Ask if unsure.
- Mode: `dev | code-review | research | e2e`
- Iteration count (default 5)

Defaults:
- Quick checks: verify skill (skip in research mode)
- Review after loop: `wf-review` in **light-plus** mode
- Checkpointing: every **3** iterations (recommended)

Optional args:
- `checkpoint_every: <n>` (0 disables)
- `review_mode: light | light-plus | heavy`
- `handoff_dir: <path>` (default `.ralph/handoffs/` or dossier `/handoffs/` if provided)
- `AGENT_CMD` override

## Outputs

- `.ralph/` state + logs
- Updated prd.json (passes true per story)
- Handoff notes at each checkpoint (file path printed)
- Optional dossier log (if repo conventions require)

## The key rule (context management)

For long loops:
- After every checkpoint: **handoff → start new thread → pickup → continue**
- Do not drag a 50-turn debug thread through 10 iterations.

## Steps

0) Confirm params
- Ask for: PRD path, mode, iteration count if missing.
- Ask for checkpointing only if user pushes back. Otherwise default:
  - `checkpoint_every = 3` (non-research)
  - `checkpoint_every = 5` (research)

1) Pickup (recommended, esp in new thread)
- Invoke `pickup` at the start of the loop block.
- If a previous checkpoint handoff note exists, read it first.

2) Baseline verification
- If mode != research: run verify skill once before iteration 1.
- Record whether baseline is clean.

3) Loop
For i in 1..N:

A) Run one Ralph iteration
- Run `ralph build 1`

B) Run quick checks
- If mode == research: skip checks (ship an artefact, not code)
- Else:
  - run verify skill (or your configured quick checks)
  - fix failures before next iteration

C) Mark story pass rules
- Mark story pass only when checks are green + acceptance criteria met.

D) Optional e2e diagnostics
- If mode == e2e or UI story: run `test-browser` diagnostics and capture evidence.

E) Checkpoint decision (Option 3 behaviour)
Trigger a checkpoint when:
- `checkpoint_every > 0` and `i % checkpoint_every == 0`, OR
- two consecutive iterations failed verification, OR
- a major direction change happened (new approach, refactor spike, etc)

When checkpoint triggers:
1. Write a handoff note (see “Checkpoint routine”)
2. Stop and ask user to start a new thread:
   - user runs `/new`
   - then invoke `pickup` in the new thread and point it at the handoff note path
3. Continue the loop in the new thread (starting at next iteration)

4) After the loop: review once (no review inside loop)
- Create a handoff note for the review boundary.
- Recommend a new thread for review:
  - `/new` then `pickup` then run `wf-review` with `review_mode` (default light-plus)

5) If review finds issues
- Only run a follow-up Ralph loop if user requests.
- If requested: start from a clean thread using pickup.

## Checkpoint routine (handoff + bash)

Goal: create a durable “resume point” file.

1) Decide where to store handoff notes
- If dossier path provided: `<dossier>/handoffs/`
- Else: `.ralph/handoffs/`

2) Capture machine state quickly (bash)
Run a quick snapshot (adjust paths as needed):

```bash
set -euo pipefail

ITER="${ITER:-<iter>}"
TS="$(date +%Y-%m-%d-%H%M)"
HANDOFF_DIR="${HANDOFF_DIR:-.ralph/handoffs}"
mkdir -p "$HANDOFF_DIR"
OUT="$HANDOFF_DIR/ralph-handoff-iter${ITER}-${TS}.md"

{
  echo "# Ralph handoff (iter ${ITER}) - ${TS}"
  echo
  echo "## Repo"
  git status -sb || true
  echo
  echo "## Recent commits"
  git log -5 --oneline || true
  echo
  echo "## Diff stat"
  git diff --stat || true
  echo
  echo "## PR (optional)"
  gh pr status 2>/dev/null || true
  echo
  echo "## tmux (optional)"
  tmux list-sessions 2>/dev/null || true
  echo
  echo "## .ralph (optional)"
  ls -la .ralph 2>/dev/null || true
} > "$OUT"

echo "Wrote: $OUT"
```

3) Write the human handoff checklist
- Invoke `handoff` skill and append its bullet list into the same `$OUT` file.
- Include:
  - what’s done vs pending
  - what failed and how to reproduce
  - what to run first next thread (verify, specific test, etc)

4) Start new thread + pickup
- user runs `/new`
- first message should include the handoff note path, e.g.:
  - “pickup and continue wf-ralph from handoff: .ralph/handoffs/ralph-handoff-iter3-YYYY-MM-DD-HHMM.md”

## Verification

- verify skill run in non-research modes (baseline + per iteration or at least per checkpoint block)
- wf-review run once after loop (unless user explicitly skips)

## Go/No-Go

- GO if checks green, acceptance criteria met, and review (if run) is GO.
- NO-GO if any required verification fails.
