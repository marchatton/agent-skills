# Ralph Guide

## Requirements

- Ralph CLI installed and on PATH.
- `.agents/tasks/prd-<slug>.json` exists.

## State and Outputs

- `.ralph/` stores state and logs.
- JSON PRD lives at `.agents/tasks/prd-<slug>.json`.

## Loop

- Ask for iteration count (default 10).
- Run `ralph build 1` N times.
- After iterations, run `verify` and report GO/NO-GO.
