---
name: wf-develop
description: This skill should only be used when the user uses the word workflow and asks to develop or implement changes with a verification-first loop and clean handoff/pickup boundaries.
---

# wf-develop

## Purpose

Implement changes with a verification-first loop, keeping context clean between workflow steps.

Prefer plan-driven work (wf-plan output) but allow PRD-driven work.

## Inputs

Preferred:
- Plan path (e.g. `docs/04-projects/.../plan.md`)

Fallback:
- PRD path + acceptance criteria

Also:
- Target repo + branch
- Known risks/deps

## Outputs

- Code changes
- Dev log artefact saved per repo conventions (summary + verification evidence + GO/NO-GO)

## Steps

0) (Recommended) Pickup if starting fresh thread / resuming
- Invoke `pickup` skill if:
  - new chat/thread, or
  - user says “resume / pick up”, or
  - repo/branch uncertain

1) Confirm work input
- If both plan and PRD exist: treat **plan** as canonical.
- If neither provided: ask once for plan/PRD path (or accept “current branch + describe goal”).

2) Baseline verification (before touching code)
- Run verify skill and record result.
- If verify fails before changes:
  - call out as pre-existing failure
  - ask whether to fix baseline first (recommended) or continue

3) Implement in smallest verifiable increments
Loop:
- pick the next smallest slice that proves progress toward an acceptance criterion
- implement minimal change
- run verify skill (or targeted check then verify)
- record evidence (what ran, result, any screenshots/logs)

4) Write dev log
Include:
- what changed
- verification evidence
- any follow-ups / risks
- GO/NO-GO

5) Context boundary (recommended)
If switching workflows next (review/release/ralph) or stopping:
- invoke `handoff`
- recommend new thread for the next workflow: `/new` then `pickup` with the handoff note path

6) Compound (optional but recommended)
If a non-trivial issue was solved or a gotcha discovered:
- suggest invoking `compound-docs`

## Verification

- Verify skill run at least once after changes.

## Go/No-Go

- GO if verify is green and acceptance criteria met.
- NO-GO if verify fails or behaviour cannot be demonstrated.
