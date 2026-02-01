---
name: create-json-prd
description: Convert PRD to JSON PRD for tooling.
---

# Create JSON PRD

## Inputs
- PRD doc
- Optional: breadboard, spike plan, deepen plan

## Outputs
- `.agents/tasks/prd-<slug>.json` per `docs/AGENTS.md` in target repo.

## Steps
1. Read PRD; extract project, branch name, description, user stories.
2. For each story: id (US-001), title, description, acceptanceCriteria[], priority int.
3. Add optional fields if helpful: `passes` (false), `notes` (empty).
4. Validate against `docs/templates/json-prd.schema.json`; fix gaps or NO-GO.

## Verification
- JSON validates against schema.
- All PRD acceptance criteria captured.
