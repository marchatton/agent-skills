# AGENTS.md Skill/Command Analysis

Analysis of which skills and commands should be explicitly referenced in AGENTS.md files vs trusting the skill matcher.

---

## Structure Recommendations

### Key Insight
- **Docs = knowledge taxonomy** (strategy, architecture, etc.)
- **AGENTS.md = process/workflow guidance**
- Keep docs structure stable; add phase-specific AGENTS.md as overlays

### Recommended AGENTS.md Set

| File | Phase | Purpose |
|------|-------|---------|
| `/AGENTS.md` | — | Identity, globals, invariants |
| `/docs/AGENTS.md` | Router | Phase → folder map, wf-* commands index |
| `/docs/00-strategy/AGENTS.md` | Explore | Segmentation, positioning, roadmap outputs |
| `/docs/01-insights/AGENTS.md` | Explore | Customer/competitor/tech inputs |
| `/docs/02-guidelines/AGENTS.md` | — | Brand, a11y, product principles |
| `/docs/03-architecture/AGENTS.md` | — | Boundaries, state, ADRs (cross-cutting) |
| `/docs/05-prds/AGENTS.md` | Shape | PRD creation/review, experiments |
| `/docs/06-delivery/AGENTS.md` | Develop + Review | Execution, bugs, PR feedback |
| `/docs/09-release/AGENTS.md` | Release | Changelog, checklist, post-release |
| `/apps/web/AGENTS.md` | — | App-specific stack |

### Cross-Cutting Concerns

| Concern | Owner |
|---------|-------|
| Boundaries/errors | `03-architecture/AGENTS.md` |
| Commands/workflows | `docs/AGENTS.md` (router) |
| Bug handling | `06-delivery/AGENTS.md` |
| Review | Part of delivery (add `07-review/` later if it grows) |

### Phase Router (`/docs/AGENTS.md`)

Single file that maps phases to folders + commands:

```md
# Docs Router

Phases
- Explore: 00-strategy/, 01-insights/ → `wf-explore`
- Shape: 04-experiments/, 05-prds/ → `wf-shape`
- Develop: apps/, packages/ → `wf-develop`
- Review: (cross-cutting) → `wf-review`
- Release: 09-release/ → `wf-release`

Cross-cutting commands: see 06-delivery/AGENTS.md
```

### Why Not Restructure Docs?

- Same doc often spans multiple phases
- Restructuring causes path churn
- Phase alignment via AGENTS.md is sufficient

---

## Decision Framework

Reference in AGENTS.md only when:
- Local convention matters
- Multiple tools exist (pick a default)
- Extra setup needed
- Safety concern
- Repeated failure mode observed

Trust the matcher when:
- Task is standard
- No repo-specific nuance
- Any reasonable approach acceptable

---

## Skills

| Skill | Reference? | File | Trigger |
|-------|------------|------|---------|
| `ask-questions-if-underspecified` | **Yes** | guidelines | If task lacks inputs/acceptance criteria, run before coding |
| `agent-browser` | **Yes** | review | If validation requires real browser interaction |
| `oracle` | **Yes** | root | If stuck on architecture or trade-offs, escalate |
| `trash` | **Yes** | boundaries | If deleting/moving many files (never hard-delete) |
| `docs-list` | **Yes** | root | If you need "where is the doc for X?" |
| `create-agent-skills` | **Yes** | architecture | If adding/modifying skills, match repo conventions |
| `skill-creator` | **Yes** | architecture | If you need a new skill definition |
| `openai-image-gen` | **Yes** | apps-web | Default for generated UI/marketing images |
| `report-bug` | **Yes** | errors | When reporting an issue, capture required fields |
| `reproduce-bug` | **Yes** | errors | When investigating a bug, capture steps + env first |
| `resolve-pr-feedback` | **Yes** | review | When addressing review comments, track changes |
| `use-ai-sdk` | **Yes** | architecture | If integrating AI features, follow repo SDK patterns |
| `agent-native-architecture` | **Yes** | architecture | If designing agent-native components |
| `browser-qa` | **Yes** | review | If you must verify behavior end-to-end in browser |
| `pr-review` | **Yes** | review | Before requesting review/merge |
| `create-json-prd` | **Yes** | guidelines | If you need structured spec for automation |
| `create-prd` | **Yes** | guidelines | If scope unclear or multi-stakeholder |
| `deepen-plan` | **Yes** | guidelines | If the plan feels hand-wavy |
| `prd-review` | **Yes** | review | Before committing to a PRD |
| `changelog-draft` | **Yes** | delivery | When preparing a release |
| `post-release-verify` | **Yes** | delivery | After shipping (checklist) |
| `release-checklist` | **Yes** | delivery | Before cutting a release |
| `compound-docs` | **Yes** | commands | If merging/synthesizing multiple docs |
| `create-cli` | No | — | Standard scaffolding |
| `multi-agent-routing` | No | — | Matcher sufficient |
| `every-style-editor` | No | — | Any approach acceptable |
| `file-todos` | No | — | Standard utility |
| `frontend-design` | No | — | Standard utility |
| `gemini-imagegen` | No | — | Use default (`openai-image-gen`) instead |
| `markdown-converter` | No | — | Standard utility |
| `nano-banana-pro` | No | — | Use default instead |
| `video-transcript-downloader` | No | — | Niche; matcher sufficient |
| `resolve-todos` | No | — | Generic; matcher sufficient |
| `work-execute` | No | — | Internal helper; matcher OK |
| `agentation` | No | — | Matcher sufficient |
| `breadboard` | No | — | Any approach acceptable |
| `spike-plan` | No | — | Any approach acceptable |
| `customer-segmentation` | No | — | Product method; any approach OK |
| `opportunity-solution-tree` | No | — | Product method; any approach OK |
| `positioning` | No | — | Product method; any approach OK |
| `pricing-packaging` | No | — | Product method; any approach OK |
| `roadmap` | No | — | Product method; any approach OK |

---

## Commands

| Command | Reference? | File | Trigger |
|---------|------------|------|---------|
| `agent-native-audit` | **Yes** | architecture | Before large agent-native changes |
| `changelog` | **Yes** | delivery | When you need release notes |
| `compound` | **Yes** | commands | To synthesize many inputs into one output |
| `create-agent-skill` | **Yes** | architecture | When adding a new skill |
| `deepen-plan` | **Yes** | guidelines | If implementation risk is high |
| `generate-command` | **Yes** | architecture | When adding a new command |
| `handoff` | **Yes** | delivery | When transferring work between agents/people |
| `heal-skill` | **Yes** | architecture | If a skill is failing/flaky |
| `landpr` | **Yes** | delivery | When ready to merge (repo's merge procedure) |
| `oracle` | **Yes** | root | If blocked on key decisions |
| `pickup` | **Yes** | delivery | When resuming an existing thread/task |
| `plan-review` | **Yes** | review | Before starting large work |
| `report-bug` | **Yes** | errors | To file an issue |
| `reproduce-bug` | **Yes** | errors | To investigate a bug |
| `resolve-parallel` | **Yes** | commands | If executing multiple independent fixes in parallel |
| `resolve-pr-parallel` | **Yes** | commands | If addressing many PR comments across areas |
| `resolve-todo-parallel` | **Yes** | commands | If cleaning up many TODOs safely |
| `test-browser` | **Yes** | review | If behavior depends on real browser execution |
| `triage` | **Yes** | errors | When an issue report arrives |
| `verify` | **Yes** | delivery | Before declaring done/shipped |
| `wf-develop` | **Yes** | commands | For end-to-end implementation workflow |
| `wf-explore` | **Yes** | commands | For discovery work |
| `wf-ralph` | **Yes** | commands | If task calls for 'ralph' workflow |
| `wf-release` | **Yes** | commands | For release workflow |
| `wf-review` | **Yes** | commands | For review workflow |
| `wf-shape` | **Yes** | commands | For shaping/spec workflow |

---

## Summary by AGENTS.md File (Phase-Aligned)

### /AGENTS.md (root)
- `oracle` — If blocked on key decisions
- `docs-list` — If you need "where is the doc for X?"

### /docs/AGENTS.md (router)
- `wf-explore` — Discovery work
- `wf-shape` — Shaping/spec workflow
- `wf-develop` — End-to-end implementation workflow
- `wf-review` — Review workflow
- `wf-release` — Release workflow
- `wf-ralph` — Ralph workflow
- `compound` — Synthesize many inputs into one output
- `compound-docs` — Merge/synthesize multiple docs

### /docs/00-strategy/AGENTS.md (Explore)
- Phase outputs: segmentation, positioning, roadmap
- No specific skills needed (product methods; matcher OK)

### /docs/01-insights/AGENTS.md (Explore inputs)
- Customer/competitor/tech research
- No specific skills needed

### /docs/02-guidelines/AGENTS.md
- `ask-questions-if-underspecified` — If task lacks inputs
- Brand, a11y, product principles

### /docs/03-architecture/AGENTS.md
- `trash` — If deleting/moving many files (never hard-delete)
- `create-agent-skills` / `skill-creator` — Adding/modifying skills
- `use-ai-sdk` — AI feature integration
- `agent-native-architecture` — Agent-native component design
- `agent-native-audit` — Before large agent-native changes
- `create-agent-skill` / `generate-command` — Scaffolding
- `heal-skill` — Repair/update failing skills

### /docs/05-prds/AGENTS.md (Shape)
- `create-prd` / `create-json-prd` — Spec creation
- `deepen-plan` — If plan feels hand-wavy
- `prd-review` — Before committing to PRD

### /docs/06-delivery/AGENTS.md (Develop + Review)
- `report-bug` — To file an issue
- `reproduce-bug` — To investigate a bug
- `triage` — When an issue report arrives
- `resolve-pr-feedback` — Address review comments
- `pr-review` — Before requesting review/merge
- `plan-review` — Before starting large work
- `agent-browser` / `browser-qa` / `test-browser` — Browser validation
- `resolve-parallel` — Execute multiple independent fixes
- `resolve-pr-parallel` — Address many PR comments
- `resolve-todo-parallel` — Clean up many TODOs
- `landpr` — Merge procedure
- `verify` — Before declaring done
- `handoff` — Transfer work
- `pickup` — Resume existing thread/task

### /docs/09-release/AGENTS.md (Release)
- `changelog` / `changelog-draft` — Release notes
- `release-checklist` — Before cutting a release
- `post-release-verify` — After shipping

### /apps/web/AGENTS.md
- `openai-image-gen` — Default for generated assets
- Stack-specific patterns (React, Next.js)

---

## Trust the Matcher (No Reference Needed)

These are standard utilities or product methods where any reasonable approach is acceptable:

**Skills:** `create-cli`, `multi-agent-routing`, `every-style-editor`, `file-todos`, `frontend-design`, `gemini-imagegen`, `markdown-converter`, `nano-banana-pro`, `video-transcript-downloader`, `resolve-todos`, `work-execute`, `agentation`, `breadboard`, `spike-plan`, `customer-segmentation`, `opportunity-solution-tree`, `positioning`, `pricing-packaging`, `roadmap`

---

## Next Steps

1. Create phase-aligned AGENTS.md templates in `docs/agentsmd2/`:
   - `AGENTS.root.md` — identity + globals
   - `AGENTS.router.md` — phase → folder map (for `/docs/AGENTS.md`)
   - `AGENTS.strategy.md` — explore outputs (for `/docs/00-strategy/`)
   - `AGENTS.insights.md` — explore inputs (for `/docs/01-insights/`)
   - `AGENTS.guidelines.md` — brand/a11y (for `/docs/02-guidelines/`)
   - `AGENTS.architecture.md` — boundaries/ADRs (for `/docs/03-architecture/`)
   - `AGENTS.prds.md` — shaping (for `/docs/05-prds/`)
   - `AGENTS.delivery.md` — develop + review (for `/docs/06-delivery/`)
   - `AGENTS.release.md` — release (for `/docs/09-release/`)
   - `AGENTS.apps-web.md` — web app stack (for `/apps/web/`)

2. Keep each file single-concern and token-efficient
3. Keep triggers to one line each
4. Avoid duplicating triggers across files
5. Review periodically for staleness

## Files to Remove from agentsmd2 (consolidated)

These standalone files should be merged into phase-aligned files:
- `AGENTS.boundaries.md` → merge into `AGENTS.architecture.md`
- `AGENTS.errors.md` → merge into `AGENTS.delivery.md`
- `AGENTS.commands.md` → merge into `AGENTS.router.md`
- `AGENTS.react.md` → merge into `AGENTS.apps-web.md`
- `AGENTS.review.md` → merge into `AGENTS.delivery.md`
