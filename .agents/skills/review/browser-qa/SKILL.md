---
name: browser-qa
description: Use when running browser QA checks for user flows and visual regressions.
---

# Browser QA

## Inputs

- Target URL or environment.
- Critical user flows.
- Known risks or regressions.

## Outputs

- Browser QA notes.
- Screenshots or recordings (optional).

## Steps

1. List critical flows and expected outcomes.
2. Run checks with `utilities/agent-browser` via `test-browser`.
3. Record issues, steps, and evidence.

## Verification

- QA notes include tested flows, outcomes, and issues.
