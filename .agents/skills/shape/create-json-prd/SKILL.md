---
name: create-json-prd
description: Use when converting a PRD into the canonical JSON PRD for tooling; requires a PRD and may include breadboard/spike/plan inputs.
---

# Create JSON PRD

## Inputs

- Required: `docs/05-prds/<slug>.md`.
- Optional: breadboard, spike plan, deepen plan.

## Outputs

- `.agents/tasks/prd-<slug>.json`.
- Optional: `docs/05-prds/<slug>.json`.

## Steps

1. Parse PRD goals, scope, acceptance criteria.
2. Incorporate optional breadboard/spike/plan details.
3. Populate JSON PRD schema and save.

## Verification

- JSON PRD includes project, branchName, description, and userStories.
