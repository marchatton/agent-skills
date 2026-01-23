---
name: create-cli
description: Use when creating a new CLI project scaffold with pnpm and basic structure.
---

# Create CLI

## Inputs

- CLI name and purpose.
- Target language/runtime.
- Distribution needs.

## Outputs

- New CLI scaffold with README and entrypoint.

## Steps

1. Define CLI scope, commands, and flags.
2. Scaffold project structure and scripts.
3. Add usage examples and verification steps.

## Verification

- If code touched: `pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm build`, `pnpm verify`.
- GO if ladder green; NO-GO otherwise.
