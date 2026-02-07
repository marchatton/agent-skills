---
name: create-json-prd
description: "Generate a Product Requirements Document (PRD) as JSON for Ralph by converting an existing PRD markdown file. Triggers on: create a prd, write prd for, plan this feature, requirements for, spec out."
---

# PRD Generator (JSON Only)

Create a structured JSON PRD that Ralph can execute deterministically. This PRD is the **single source of truth** for stories, gates, and status.

This skill **ingests PRD markdown** written via `$create-prd` (for example `prd.md` / `prd-overall.md` / `prds/<slice_id>_<slug>/prd.md`) and produces the matching PRD JSON.

**Important:** Do NOT implement anything. Only generate JSON.

## Inputs

Required:
- A PRD markdown file path (one of):
  - `prd.md` (single-PRD dossier)
  - `prd-overall.md` (multi-PRD dossier overall/spine)
  - `prds/<slice_id>_<slug>/prd.md` (multi-PRD dossier slice)
  - (Optional legacy naming) `prd-<slug>.md` if a dossier uses that pattern

Optional (for "no information loss"):
- Shaping inputs in the same dossier (if present): `brief.md`, `breadboard-pack.md`, `spike-investigation.md`, `risk-register.md`

If the user only provides a feature description (no PRD markdown), **NO-GO**: ask them to create `prd.md` via `$create-prd` first.

## Outputs

- Save the PRD JSON **alongside the PRD markdown** with the matching basename (per `docs/04-projects/AGENTS.md`):
  - `prd.md` -> `prd.json`
  - `prd-overall.md` -> `prd-overall.json`
  - `prd-<slug>.md` -> `prd-<slug>.json`
  - `prds/<slice_id>_<slug>/prd.md` -> `prds/<slice_id>_<slug>/prd.json`

If the prompt provides an explicit output path, save to that path instead.

## The Job

1. Read the PRD markdown and extract all details needed for a deterministic PRD JSON.
2. If required information is missing, invoke `$ask-questions-if-underspecified` and ask clarifying questions (see below).
3. **Always ask about quality gates** (commands that must pass).
4. Generate a **detailed** PRD JSON that follows the structure below and save it to the output path.

## Step 1: Clarifying Questions (When Needed)

Only ask questions when the PRD markdown is missing required inputs for the JSON shape. If you need to ask questions, use `$ask-questions-if-underspecified` and follow its workflow.

Ask **5-10** clarifying questions (with lettered options), in batches of up to 5 at a time (ask 5, wait for answers, then ask the next batch if needed). Focus on:

- **Problem/Goal:** What problem does this solve?
- **Core Functionality:** What are the key actions?
- **Scope/Boundaries:** What should it NOT do?
- **Success Criteria:** How do we know it's done?
- **Stack + Environment:** frameworks, hosting, runtime, database, auth approach
- **UI + Routes:** key screens, navigation, route map, layout constraints
- **Data Model + Import Format:** entities, relationships, external data shape
- **Rules/Calculations:** business logic, progression rules, edge cases
- **Quality Gates:** tests, lint, typecheck, build/dev verification (REQUIRED)

Always ask explicitly:
- **Is this a new project or an existing codebase?**

### Format Questions Like This

```
1. What quality commands must pass for each story?
   A. pnpm test
   B. pnpm run lint
   C. pnpm run typecheck
   D. Other: [specify]

2. What UI screens/routes are required?
   A. Minimal (1-2 pages)
   B. Basic app shell (dashboard + detail pages)
   C. Full routing map (list all routes)
   D. Other: [specify]

Note: All example questions and options are illustrative only. Do not copy them verbatim into the PRD JSON unless the user explicitly chooses them.
```

## Step 2: JSON Structure (Required)

Output a JSON file with this shape (include detailed top-level fields so the PRD is fully self-contained):

```json
{
  "version": 1,
  "project": "Feature Name",
  "overview": "Short problem + solution summary",
  "goals": [
    "Goal 1",
    "Goal 2"
  ],
  "nonGoals": [
    "Explicitly out of scope items"
  ],
  "successMetrics": [
    "How success is measured"
  ],
  "openQuestions": [
    "Remaining unknowns"
  ],
  "stack": {
    "framework": "TanStack Start",
    "hosting": "Cloudflare",
    "database": "D1",
    "auth": "describe approach"
  },
  "routes": [
    { "path": "/", "name": "Home", "purpose": "..." }
  ],
  "uiNotes": [
    "Layout or component requirements"
  ],
  "dataModel": [
    { "entity": "Workout", "fields": ["id", "userId", "date", "notes"] }
  ],
  "importFormat": {
    "description": "Expected JSON shape",
    "example": { "programName": "..." }
  },
  "rules": [
    "Key business rules / calculations"
  ],
  "qualityGates": ["pnpm test"],
  "stories": [
    {
      "id": "US-001",
      "title": "Short story title",
      "status": "open",
      "dependsOn": [],
      "description": "As a [user], I want [feature] so that [benefit].",
      "acceptanceCriteria": [
        "Specific verifiable criterion",
        "Example: a valid input behaves as expected",
        "Negative case: invalid input returns a safe error"
      ]
    }
  ]
}
```

### Story + JSON Rules

- **IDs**: Sequential (`US-001`, `US-002`, ...)
- **Status**: Always `"open"` for new stories
- **DependsOn**: Use IDs only; empty array if none
- **Quality Gates**: Only at the top-level `qualityGates`
- **Acceptance Criteria**: Verifiable, specific, testable
- **Every story must include**: at least 1 example + 1 negative case
- **UI stories**: include explicit routes, components, and UI states
- **New projects**: include initial setup stories (scaffold, env/config, local dev, deploy basics, **package installs**)
- **Dependencies**: any new package/library introduced must be called out with install commands in acceptance criteria (for example `pnpm add <pkg>`), plus any required config or scripts.
- **Ordering**: if this is a new project, the **first story must be setup** (scaffold + installs + scripts + env/config). Migrations or data model work come after setup.

## No Information Loss (Critical)

Do not drop details from the PRD markdown when producing PRD JSON.

- Map PRD content into the required keys above where it fits.
- If the PRD includes additional sections (for example functional requirements, failure states/UX, verification plan, metrics/logging, rollback/disable path, risks/dependencies, links/sources), preserve them by adding **additional top-level keys** as needed. Ralph ignores unknown keys; the only hard requirements are `qualityGates[]` and `stories[]`.

## Output Requirements

- Save JSON to the chosen output path.
- The JSON file must contain **only** JSON (no Markdown PRD, no commentary).

After saving, tell the user:
`PRD JSON saved to <path>. Close this chat and run \`ralph build\`.`

## Verification

- JSON parses.
- JSON contains required keys: `version`, `project`, `overview`, `qualityGates`, `stories`.
- All PRD user stories + acceptance criteria are captured (no loss).
- Each story has:
  - `status: "open"`
  - `dependsOn: []` (or IDs)
  - acceptance criteria including at least 1 example + 1 negative case.
