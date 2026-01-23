---
name: resolve-pr-feedback
description: Use when addressing PR feedback and re-verifying changes.
---

# Resolve PR Feedback

## Inputs

- PR comments and requested changes.
- Target repo and branch.
- Acceptance criteria.

## Outputs

- Updated code changes.
- Reply notes for reviewers.

## Steps

1. Group comments by theme and risk.
2. Apply fixes with clear commits.
3. Re-run verification and summarize changes.

## Verification

- If code touched: `pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm build`, `pnpm verify`.
- GO if ladder green; NO-GO otherwise.
