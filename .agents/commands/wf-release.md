# wf-release

## Purpose

Ship changes with a release checklist, changelog, and post-release verification.

## Inputs

- Approved PRD and acceptance criteria.
- Release scope and rollout constraints.
- Monitoring and rollback requirements.

## Outputs

- `docs/release/<slug>/release.md`
- `docs/release/<slug>/changelog.md`
- Optional: `docs/release/<slug>/post-release.md`
- Optional: appended entry in `docs/learnings.md` via `compound`

## Steps

1. Define the work slug and gather release context.
2. Run skill `release-checklist` and capture rollout, rollback, monitors.
3. Draft changelog via `changelog-draft`.
4. Run `pnpm verify` in the target repo.
5. If non-trivial, run `compound` to append learnings.
6. Write GO/NO-GO decision with verification evidence.

## Verification

- `pnpm verify`

## Go/No-Go

- GO if verify is green, rollback plan exists, and monitors listed.
- NO-GO otherwise.

## Usage

- Codex: `/prompts:wf-release <slug>`
- Claude: `/wf-release <slug>`
