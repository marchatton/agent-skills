---
name: wf-release
description: This skill should only be used when the user uses the word workflow and asks to release or ship changes with a release checklist, verification, and clean handoff/pickup boundaries.
---

# wf-release

## Purpose

Ship changes safely with a minimal release checklist, changelog/release notes, and post-release verification.

## Inputs

- Plan/PRD acceptance criteria
- Release scope + rollout constraints
- Monitoring + rollback requirements
- Target repo + branch/PR

## Outputs

- Release notes / changelog entry / post-release notes (as needed)
- GO/NO-GO decision with verification evidence
- Optional learning entry via `compound-docs`

## Steps

0) (Recommended) Pickup if starting fresh thread / resuming
- Invoke `pickup` if repo/branch/PR state is not fresh.

1) Confirm scope + rollout shape
Capture:
- what is shipping (and what is not)
- rollout strategy (flags, staged, canary)
- rollback steps (including data)
- monitors to watch

2) Pre-release verification (mandatory)
- Run verify skill.
- If verify fails: NO-GO unless user explicitly accepts risk.

3) Release artefacts
- Draft release notes / changelog entry (keep it short, user-facing)
- Note any operator actions (migrations, flags, config)

4) Post-release verification
- State what to check after deploy (smoke checks + metrics)
- If available, record evidence (screenshots/logs)

5) Compound (recommended when non-trivial)
- If anything surprising happened (flaky tests, rollout gotcha, weird failure mode): suggest `compound-docs`

6) Context boundary (recommended)
If handing off to another agent/person or switching workflows:
- invoke `handoff`
- recommend new thread for next work: `/new` then `pickup`

## Verification

- Verify skill run pre-release (required).

## Go/No-Go

- GO if verify is green, rollback plan exists, and monitors listed.
- NO-GO otherwise.
