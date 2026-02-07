---
name: create-json-prd
description: Convert `prd.md` or `prd-<slug>.md` into a Ralph-compatible PRD JSON (`qualityGates[]`, `stories[]`) for deterministic loops.
---

# Create JSON PRD (Ralph)

## Inputs
- A PRD Markdown file named either:
  - `prd.md`, or
  - `prd-<slug>.md` (kebab-case)
- Optional: shaping artefacts (brief/breadboard/spikes/risks) to avoid context loss

## Outputs
- Ralph PRD JSON saved alongside the PRD markdown with the matching basename:
  - `prd.md` -> `prd.json`
  - `prd-<slug>.md` -> `prd-<slug>.json`

This JSON is intended for `ralph build` and must follow the iannuttall/ralph PRD schema (`qualityGates[]`, `stories[]`, story `status`/`dependsOn`).

## Steps
1) Resolve the input PRD Markdown

- If the user provides a file path: it must be `prd.md` or `prd-<slug>.md` (NO-GO otherwise).
- If the user provides a directory:
  - If `prd.md` exists, use it.
  - Else, find `prd-*.md`:
    - If exactly one match, use it.
    - If none or multiple matches: NO-GO and ask which PRD file to ingest.

2) Ingest the PRD Markdown

Read the PRD and extract (best-effort; leave empty arrays where genuinely missing):
- project name
- overview
- goals / non-goals / success metrics / open questions
- stack constraints (framework/hosting/db/auth, etc)
- routes + UI notes (if present)
- data model (if present)
- key rules / edge cases
- quality gates (commands that must pass)
- stories + acceptance criteria

3) Ask questions only where underspecified (minimum, must-have only)

Do NOT default to a fixed number of questions.
If details are missing/ambiguous in a way that could cause wrong JSON, ask 1–5 must-have questions and pause.

Use the `$ask-questions-if-underspecified` rubric:
- eliminate whole branches of work
- multiple-choice where possible
- provide a fast-path reply (`defaults`)

Common must-have triggers:
- `qualityGates` missing or unclear (no concrete commands)
- stories are too large for a single iteration (need splitting)
- acceptance criteria are not verifiable / missing example or negative case
- unclear environment/tooling assumptions (pnpm vs npm, build/test entrypoints)

4) Generate Ralph PRD JSON

Output JSON with this shape (plus optional fields noted below):

```json
{
  "version": 1,
  "project": "Feature Name",
  "overview": "Short problem + solution summary",
  "goals": [],
  "nonGoals": [],
  "successMetrics": [],
  "openQuestions": [],
  "stack": {},
  "routes": [],
  "uiNotes": [],
  "dataModel": [],
  "importFormat": { "description": "", "example": {} },
  "rules": [],
  "qualityGates": [],
  "stories": [
    {
      "id": "US-001",
      "title": "Short story title",
      "status": "open",
      "dependsOn": [],
      "description": "As a [user], I want [feature] so that [benefit].",
      "acceptanceCriteria": [],
      "passes": false,
      "notes": ""
    }
  ]
}
```

Rules:
- `stories[].id`: sequential (`US-001`, `US-002`, ...)
- `stories[].status`: always `"open"` for newly generated PRDs
- `stories[].dependsOn`: IDs only; default `[]`
- `qualityGates`: top-level only
- Story size: each story must be completable in a single Ralph iteration
- Every story must include:
  - at least 1 `Example:` acceptance criterion
  - at least 1 `Negative case:` acceptance criterion
- UI stories must include browser verification guidance in acceptance criteria:
  - Default tool: `$dev-browser`
  - Include what to verify and where evidence (screenshots) should go

5) Save the JSON alongside the PRD markdown (matching basename)

6) Final output to the user (in chat, not inside the JSON file)

Tell the user:
- `PRD JSON saved to <path>.`
- Suggested next step: `ralph build 1 --prd <path>`

## Verification
- JSON parses.
- `qualityGates` present (empty only if user explicitly confirmed “none”).
- `stories` is a non-empty array.
- Every story includes: `id`, `title`, `status`, `dependsOn`, `description`, `acceptanceCriteria`.
- Every story includes optional: `passes` (boolean) and `notes` (string).
- Acceptance criteria include at least one example and one negative case per story.
