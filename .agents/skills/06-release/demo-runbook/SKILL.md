---
name: demo-runbook
description: This skill should be used when a user needs a demo package that starts with a live demo (not slides) and produces both a demo script and a navigable single-file HTML runbook, including caveats, respectful competitive comparison, and LLM architecture details (RAG, evals, observability).
---

# Demo Runbook

Create a demo package that is demo-first, user-empathy-led, and technically credible. Produce two deliverables every time: a demo script and a single-file HTML runbook.

## When to use this skill

Use this skill when asked to create or refresh a demo (often a PoC demo) that:
- Starts with an end-to-end live demo before explaining why, what, and how
- Includes a competitive landscape comparison using April Dunford’s respectful approach framing
- Includes technical architecture details, especially LLM patterns (RAG, evals, observability)
- Produces both a talk track and a navigable runbook page

Example triggering requests:
- “Help me create a PoC demo runbook and script for a live demo.”
- “Make a demo-first talk track, then cover why/what/how and architecture.”
- “Create a single HTML runbook with links, diagrams, and sections for tech stack.”
- “Write a respectful competitive comparison and explain our approach.”

## Outputs

Always produce both:
1) **Demo script** as markdown (talk track + what to click + timings)
2) **Single-file HTML runbook** (visual-first with custom CSS, navigable sections, Mermaid diagrams (flowchart + sequence), in-app hyperlinks, back-to-home navigation)

HTML runbook must:
- Be single-file HTML (no build step required) with custom CSS styling (cards/callouts/layout), not a plain document.
- Include Mermaid diagrams (at least one flowchart and one sequence diagram).
- Include navigation between sections (hash router is fine) and “Back to Home” affordances.
- Include an app links section with real links or TODO placeholders.

When returning outputs, format as:
- `=== demo-script.md ===` then the markdown
- `=== demo-runbook.html ===` then the full HTML

## Input schema

Accept inputs in either bullet form or JSON. If any field is missing, insert a clear TODO placeholder rather than asking questions.

Minimum inputs to request are not required. Proceed with placeholders.

### Core narrative
- `poc_name`: Name of the PoC
- `tagline`: One-line value statement
- `audience`: Who is watching (and expected technical depth)
- `segment`:
  - `organisation`: The organisation context (industry, size, geography, constraints)
  - `buyer`: Who buys / signs (budget owner, success metric, risk posture)
  - `end_user`: Who uses it day-to-day (workflow, pain, what “better” feels like)
- `job_to_be_done`: What the user is trying to do
- `starting_feelings`: How they feel at the start (rushed, uncertain, risk-averse, too many tabs)
- `desired_feelings`: How the product changes that (confidence, clarity, speed, fewer guesses)
- `scenario`: The demo scenario in plain English
- `success_outcome`: What “done” looks like for the user
- `business_success_outcome`: What success looks like for the business (be specific: $ impact or growth/adoption metric + timeframe)

### Special feature X
- `special_feature`:
  - `name`: Feature X name
  - `what_it_does`: Plain English
  - `why_it_matters`: User value
  - `citation`: Optional link or text reference
  - `evidence_note`: If citation missing, set to “Evidence is preliminary.”

### Scope and caveats
- `geography`: Default `US`
- `caveats`: Default list must include:
  - Synthetic customer data including made up packs
  - Segmentation and positioning were not a focus
  - Not production ready
  - Goal was mini Orbital Copilot PoC with special feature X (citation optional, otherwise evidence preliminary)
  - US only

### Competitive landscape
- `competitors`: Optional list of competitor names
- `competitor_patterns`: Optional list describing market approaches (use when competitor names are unknown)
- `our_approach_summary`: How the PoC approach differs and why
- `tradeoffs`: Explicit trade-offs accepted

### Tech stack
- `tech_stack`:
  - `frontend`
  - `backend`
  - `llm_provider_and_models`
  - `orchestration`
  - `vector_search_or_db`
  - `storage`
  - `auth_security`
  - `observability`
  - `evals_tooling`
  - `hosting`

### Architecture and choices
- `architecture`:
  - `chosen_option`: e.g. “RAG + light tool use”
  - `options_considered`: At least 2 options with pros/cons
  - `rag_details`: chunking, retrieval, filters, grounding approach
  - `citations_policy`: when to cite, when to say unknown
  - `evals`: offline set, regression, quality metrics and what “good” means
  - `observability`: traces, prompt/versioning, cost/latency, failure modes
  - `security_privacy_notes`: even for synthetic data, log redaction and separation of secrets

### Demo links
- `app_links`: List of `{label, url, note}` for in-app pages to click during demo
- `runbook_links`: Optional external links to supporting docs (PRD, repo, design, etc.)

### Risks and next steps
- `known_limitations`: hallucination risks, coverage gaps, latency/cost concerns, reliability risks
- `next_steps`: what to productionise, what to validate, what to expand

## Workflow

Follow this workflow in order.

### Step 1: Normalise inputs and apply defaults
- Apply default caveats and geography (US).
- If `special_feature.citation` is missing, set `special_feature.evidence_note` to “Evidence is preliminary.”
- If competitors are missing, use `competitor_patterns` or generate neutral market patterns with TODO markers.
- If tech stack fields are missing, insert TODO placeholders.
- If app links are missing, create 3 placeholder links with TODO URLs.

Optional: Run `scripts/validate_inputs.py` to normalise a JSON input payload and produce a filled structure.

### Step 2: Build the demo-first narrative backbone
- Lead with an end-to-end happy path.
- Make the segment (organisation, buyer, end-user), job, and feelings explicit in the first minute.
- Call out the emotional shift, from uncertainty to confidence, as part of the story.
- Include one edge case showing safe behaviour (clarify, refuse, uncertainty).
- Tie the story to the business success outcome (what changes, and how you will measure it).

### Step 3: Add caveats early and repeat at the end
- Place caveats immediately after the first sentence or within the first 10 seconds.
- Repeat a short caveats recap in the closing.

### Step 4: Add why, what, how
- Explain why after the demo has landed.
- Define what is in scope and out of scope.
- Explain how at two levels:
  - Product level, what components do
  - Technical level, architecture and LLM specifics

### Step 5: Add competitive landscape section
- Compare approaches, priorities, and trade-offs.
- Avoid dunking on competitors.
- Frame differences as “different constraints” and “optimising for X”.

Use `references/competitive-template.md`.

### Step 6: Add technical architecture section
- Include RAG, grounding, citations policy.
- Include evals plan and what “good” means.
- Include observability plan and what gets logged.
- Include at least two architecture options considered and why the PoC choice was made.

Use `references/architecture-template.md`.

### Step 7: Generate deliverables
- Generate `demo-script.md` using `references/demo-script-template.md`.
- Generate `demo-runbook.html` by copying `assets/runbook-template.html` and filling placeholders:
  - PoC name, tagline, narrative, caveats
  - Segment (organisation, buyer, end-user) and business success outcome
  - App links
  - Tech stack and architecture content
  - Competitive section content
  - Mermaid diagrams (flowchart and sequence diagram) and custom CSS styling (keep it visual, not a plain document)

### Step 8: Quality check before returning
Confirm:
- Demo starts before any explanation.
- Segment (organisation, buyer, end-user), job and feelings are explicit.
- Caveats appear early and at the end.
- Competitive section is respectful and trade-off based.
- Architecture includes RAG, evals, observability and options considered.
- Geography is US only.
- Business success outcome is specific and measurable (not vibes).
- Outputs are British English, crisp, no production promises.

## Bundled resources

Load as needed:
- `references/demo-script-template.md` for the script structure
- `references/competitive-template.md` for respectful comparison framing
- `references/architecture-template.md` for the LLM architecture talk track
- `assets/runbook-template.html` for a navigable, visual-first runbook shell
- `scripts/validate_inputs.py` for deterministic input normalisation (optional)
