---
name: oracle
description: Use when running Oracle CLI workflows; wraps the latest Oracle CLI with Node 22+ checks.
---

# Oracle Wrapper

## Inputs

- Oracle CLI arguments.
- Target repo context.

## Outputs

- Oracle CLI output.

## Steps

1. Ensure Node 22+ is available.
2. Run `scripts/oracle.sh <args>`.
3. If pnpm is unavailable, fallback to `npx -y @steipete/oracle@latest <args>`.

## Verification

- Oracle command completes without errors.
