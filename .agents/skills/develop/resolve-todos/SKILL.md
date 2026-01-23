---
name: resolve-todos
description: Use when resolving TODOs and cleanup items with verification.
---

# Resolve Todos

## Inputs

- TODO list or files.
- Target repo and branch.
- Acceptance criteria for cleanup.

## Outputs

- Resolved TODOs.
- Updated notes or dev-log.

## Steps

1. Triage TODOs by risk and scope.
2. Resolve in small batches.
3. Verify after each batch.

## Verification

- If code touched: `pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm build`, `pnpm verify`.
- GO if ladder green; NO-GO otherwise.
