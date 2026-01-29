# AGENTS.md Skill/Command Analysis

Analysis of which skills and commands should be explicitly referenced in AGENTS.md files vs trusting the skill matcher.

---

## Structure Recommendations

### Key Insight
- **Docs = knowledge taxonomy** (strategy, architecture, etc.)
- **AGENTS.md = process/workflow guidance**
- Keep docs structure stable; add phase-specific AGENTS overlays

### Recommended AGENTS.md Set

| File | Phase | Purpose |
|------|-------|---------|
| `/AGENTS.md` | — | Identity, globals, invariants |
| `/docs/AGENTS.md` | Router | Phase → folder map, wf-* commands index |
| `/docs/02-guidelines/AGENTS.md` | — | Brand, a11y, product principles |
| `/docs/03-architecture/AGENTS.md` | — | Boundaries, security, env, cross-cutting |
| `/docs/06-delivery/AGENTS.md` | Develop + Review | Execution, verify, PR hygiene |
| `/docs/09-release/AGENTS.md` | Release | Checklist, changelog, post-release |
| `/apps/web/AGENTS.md` | — | App-specific stack |

### Cross-Cutting Concerns

| Concern | Owner |
|---------|-------|
| Boundaries/errors/env | `03-architecture/AGENTS.md` |
| Commands/workflows | `docs/AGENTS.md` (router) |
| Review + bug handling | `06-delivery/AGENTS.md` |

### Phase Router (`/docs/AGENTS.md`)

```md
# Docs Router

Phases
- Explore → `wf-explore`
- Shape → `wf-shape`
- Develop → `wf-develop`
- Review → `wf-review`
- Release → `wf-release`
- Ralph → `wf-ralph`

Cross-cutting: `verify`, `compound`
```

### Why Not Restructure Docs?

- Same doc spans multiple phases
- Path churn is high
- Phase alignment via AGENTS is enough

---

## Decision Framework

Reference in AGENTS.md only when:
- Local convention matters
- Multiple tools exist (pick default)
- Extra setup needed
- Safety concern
- Repeated failure mode seen

Trust the matcher when:
- Task is standard
- No repo nuance
- Any reasonable approach ok

---

## Skills

| Skill | Reference? | File | Trigger |
|-------|------------|------|---------|
| `ask-questions-if-underspecified` | **Yes** | root | If task underspecified, run before work |
| `oracle` | **Yes** | root | If blocked on key decision |
| `browser-qa` | **Yes** | delivery/review | If real browser validation needed |
| `use-ai-sdk` | **Yes** (conditional) | architecture | If AI SDK is in repo |
| `agent-native-architecture` | **Yes** (conditional) | architecture | If designing agent-native pieces |
| `pr-review` | **Yes** (conditional) | delivery/review | Before requesting review/merge |
| `report-bug` | **Yes** (conditional) | delivery | When filing issues |
| `reproduce-bug` | **Yes** (conditional) | delivery | When investigating bugs |
| `resolve-pr-feedback` | **Yes** (conditional) | delivery | When addressing review comments |
| `release-checklist` | **Yes** (conditional) | release | Before cutting release |
| `changelog-draft` | **Yes** (conditional) | release | When drafting release notes |
| `post-release-verify` | **Yes** (conditional) | release | After shipping |
| `compound-docs` | **Yes** (optional) | router | If learnings doc is standard |
| `docs-list` | No | — | Matcher ok |
| `trash` | No | — | Matcher ok |
| `multi-agent-routing` | No | — | Matcher ok |
| Explore/Shape skills (opportunity-solution-tree, segmentation, positioning, roadmap, breadboard, spike-plan, deepen-plan, create-prd, create-json-prd, prd-review) | No | — | Use via wf-* commands |
| Dev utilities (work-execute, resolve-todos, create-cli) | No | — | Matcher ok |
| Misc utilities (frontend-design, markdown-converter, nano-banana-pro, gemini-imagegen, video-transcript-downloader) | No | — | Matcher ok |

---

## Commands

| Command | Reference? | File | Trigger |
|---------|------------|------|---------|
| `wf-explore` | **Yes** | router | Discovery workflow |
| `wf-shape` | **Yes** | router | Spec workflow |
| `wf-develop` | **Yes** | router | Implementation workflow |
| `wf-review` | **Yes** | router | Review workflow |
| `wf-release` | **Yes** | router | Release workflow |
| `wf-ralph` | **Yes** | router | Ralph workflow |
| `verify` | **Yes** | delivery | Before declaring done |
| `compound` | **Yes** (optional) | router | Synthesize learnings |
| `oracle` | **Yes** | root | If blocked |
| `agent-native-audit` | **Yes** (conditional) | architecture | For agent-native audits |
| Other commands from plugins (triage, handoff, pickup, landpr, plan-review, resolve-* parallel, test-browser, generate-command, heal-skill, create-agent-skill) | No | — | Not present in `.agents/` here; don’t reference unless synced |

---

## Summary by AGENTS.md File

### /AGENTS.md
- `ask-questions-if-underspecified`
- `oracle`

### /docs/AGENTS.md (router)
- `wf-explore`, `wf-shape`, `wf-develop`, `wf-review`, `wf-release`, `wf-ralph`
- `verify`
- `compound` (optional)

### /docs/02-guidelines/AGENTS.md
- Brand/a11y only; no skills

### /docs/03-architecture/AGENTS.md
- `agent-native-audit` (conditional)
- `use-ai-sdk` (conditional)
- `agent-native-architecture` (conditional)

### /docs/06-delivery/AGENTS.md
- `verify`
- `browser-qa` (conditional)
- `pr-review`, `report-bug`, `reproduce-bug`, `resolve-pr-feedback` (conditional)

### /docs/09-release/AGENTS.md
- `release-checklist`
- `changelog-draft`
- `post-release-verify`

### /apps/web/AGENTS.md
- Web stack + server-first rules
- Optional: `browser-qa` if UI QA is standard

---

## Trust the Matcher (No Reference Needed)

Standard utilities or product methods where any reasonable approach is ok:

`docs-list`, `trash`, `multi-agent-routing`, `create-cli`, `work-execute`, `resolve-todos`, explore/shape methods (opportunity-solution-tree, segmentation, positioning, roadmap, breadboard, spike-plan, deepen-plan, create-prd, create-json-prd, prd-review)

---

## Notes / Risks

- `oracle` exists as both command + skill. Prefer command in AGENTS.
- `browser-qa` relies on `test-browser` + `utilities/agent-browser`; not synced into `.agents/` yet per vendors config. Don’t reference unless synced.
- Hooks are examples only; no AGENTS refs.
