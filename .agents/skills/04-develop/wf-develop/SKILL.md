---
name: wf-develop
description: This skill should only be used when the user uses the word workflow and asks to develop or implement changes with a verification-first loop and clean handoff/pickup boundaries.
---

# wf-develop

## Purpose

Implement changes with a verification-first loop, keeping context clean between workflow steps.

`prd.json` (single-PRD dossier or slice PRD).
`plan.md` may exist for higher-risk work, but it’s optional.

Prefer plan-driven work when plan.md exists, but allow PRD-driven work (especially with PRD JSON: `prd.json`).

## Inputs

Preferred:
- Dossier path (contains one or more`prd.json` ) - implement one `prd.json` at a time.
- Or explicit PRD JSON path (`prd.json` / `prds/<slice_id>_<slug>/prd.json`)

Optional:
- `plan.md` path (only when created by wf-plan)

Also:
- Target repo + branch
- Known risks/deps

## Outputs

- Code changes
- Verification evidence (what ran, result, screenshots/logs when relevant)
- Update the relevant PRD JSON story `passes` and `notes` to reflect reality (`prd.json` or a slice `prds/.../prd.json`)
- Dev log artefact saved per repo conventions (summary + verification evidence + GO/NO-GO) (optional but nice)

## Steps

0) (Recommended) Pickup if starting fresh thread / resuming
- Invoke `pickup` skill if:
  - new chat/thread, or
  - user says “resume / pick up”, or
  - repo/branch uncertain

1) Confirm work input
- If PRD JSON missing (`prd.json`): check if `prd.md` exists. If yes, run `create-json-prd` first (NO-GO if schema invalid). If not, ask user to create `prd.md`.
- If `plan.md` exists: use it in conjunction with `prd.json` to guide development.
- If no plan.md: proceed from the `prd.json` directly (this is normal for small work).

2) Baseline verification (before touching code)
- Run verify skill and record result.
- If verify fails before changes:
  - call out as pre-existing failure
  - ask whether to fix baseline first (recommended) or continue

3) Implement in smallest verifiable increments
Loop:
- pick the next smallest slice that proves progress toward an acceptance criterion
- implement minimal change
- run targeted check then verify skill
- record evidence (what ran, result, any screenshots/logs)
- update the relevant PRD JSON:
  - set `passes=true` for stories fully meeting criteria
  - use `notes` for partials, tradeoffs, follow-ups

4) Light review loop (default)
Before opening a PR / handing off:
- do a quick diff scan for naming, tests, and obvious failure modes
- rerun verify
- only escalate to wf-review when risk/size warrants it

5) Write dev log (optional)
Include:
- what changed
- verification evidence
- any follow-ups / risks
- GO/NO-GO

6) Context boundary (recommended)
If switching workflows next (review/release/ralph) or stopping:
- invoke `handoff`
- recommend new thread for the next workflow: `/new` then `pickup` with the handoff note path

7) Compound (optional but recommended)
If a non-trivial issue was solved or a gotcha discovered:
- suggest invoking `compound-docs` skills

## Verification

- Verify skill run at least once after changes.
- PRD JSON updated to reflect what passes (`prd.json` or slice `prds/.../prd.json`).

## Go/No-Go

- GO if verify is green and acceptance criteria met (per the PRD JSON).
- NO-GO if verify fails or behaviour cannot be demonstrated.
