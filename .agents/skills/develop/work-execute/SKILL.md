---
name: work-execute
description: Use when implementing planned work with a tight verify-first loop.
---

# Work Execute

## Inputs

- PRD and plan.
- Target repo and branch.
- Acceptance criteria.

## Outputs

- Code changes.
- `docs/dev/<slug>/dev-log.md`.

## Steps

1. Implement in small verified increments.
2. Keep notes for dev-log.
3. Run pnpm ladder after meaningful changes.

## Verification

- If code touched: `pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm build`, `pnpm verify`.
- GO if ladder green and criteria met; NO-GO otherwise.
