# Demo Script Template (demo-first, user feelings included)

Use this template to produce `demo-script.md`. Keep it tight. Prefer short paragraphs and bullets.

## Header
- PoC: **{{poc_name}}**
- Tagline: {{tagline}}
- Audience: {{audience}}
- Scope: **{{geography}} only**
- Segment:
  - Organisation: {{segment.organisation}}
  - Buyer: {{segment.buyer}}
  - End user: {{segment.end_user}}
- Business success outcome: {{business_success_outcome}}

## 0) Caveats upfront (say within 10 seconds)
Say this while already on the product UI:
- “Caveats upfront: synthetic customer info including made up packs, segmentation and positioning were not a focus, not production ready.”
- “Goal was a mini Orbital Copilot PoC with special feature {{special_feature.name}}.”
- “{{special_feature.evidence_note}} {{special_feature.citation_if_present}}”
- “Scope is {{geography}} only.”

## 1) User story and emotional context (20 to 30 seconds)
Make this explicit:
- Segment:
  - Organisation: {{segment.organisation}}
  - Buyer: {{segment.buyer}}
  - End user: {{segment.end_user}}
- Job to be done: {{job_to_be_done}}
- Starting feelings: {{starting_feelings}}
- Why they feel that way: information scattered, time pressure, risk of being wrong, too many tabs
- What better feels like: {{desired_feelings}}
- Business success outcome: {{business_success_outcome}}

Suggested talk track:
- “This is for {{segment.organisation}}. The buyer is {{segment.buyer}} and the end user is {{segment.end_user}}.”
- “They’re trying to {{job_to_be_done}}. They feel {{starting_feelings}} because they have to stitch info across tools and they cannot afford to be wrong.”
- “What they want is {{desired_feelings}}.”
- “And for the business, success looks like: {{business_success_outcome}}.”

## 2) Demo run (happy path first) (2 to 3 mins)
### Step 1: Start at the real entry point
- What to show: {{app_links[0].label}} (or TODO)
- What to click: {{app_links[0].url}}
- What to say: “This is where they start, not a slide.”

### Step 2: Ask the core question
- Scenario prompt: {{scenario}}
- What to say: “In the old flow this becomes searching and second guessing.”

### Step 3: Show the output and why it matters
- What to highlight: answer clarity, provenance, next steps
- What to say: “This is the moment their stress drops, because they can trust and act.”

### Step 4: Special feature X (the wow moment)
- Feature: {{special_feature.name}}
- What it does: {{special_feature.what_it_does}}
- Why it matters: {{special_feature.why_it_matters}}
- Evidence statement:
  - If citation present: “We’ve seen evidence in {{special_feature.citation}}.”
  - If missing: “Evidence is preliminary, this is a PoC signal not a production claim.”

### Step 5: Edge case and safety behaviour (30 to 45 seconds)
Demonstrate one:
- ambiguous question, missing data, conflicting sources
- show clarify, refuse, or uncertainty rather than bluffing
What to say:
- “If we cannot ground it, we say so. That is deliberate.”

## 3) Transition to why, what, how (15 seconds)
Say:
- “Now that you’ve seen it working end-to-end, here’s why we built it, what we scoped, and how it works.”

## 4) Why (30 to 60 seconds)
Cover:
- why now
- what user pain this removes
- how it changes speed and confidence

## 5) What (scope and non-goals) (30 to 60 seconds)
Include:
- In scope: {{in_scope_bullets_or_todos}}
- Out of scope: segmentation and positioning, production hardening, international
- Geography: {{geography}} only
- Data caveat reminder: synthetic packs and customers

## 6) Competitive landscape (1 to 2 mins)
Use `references/competitive-template.md`.
Ensure:
- respectful, trade-off based
- “different constraints” framing
- no dunking

## 7) Technical architecture and stack (2 to 3 mins)
Use `references/architecture-template.md`.
Include:
- tech stack list
- options considered and chosen
- RAG, evals, observability
- key trade-offs

## 8) Close (30 to 45 seconds)
Recap:
- what was shown
- user value, emotional shift
- next steps
- business success outcome (measurable)

Repeat caveats briefly:
- synthetic data, segmentation/positioning not focus, not production ready, US only, feature evidence note

## 9) Q&A prompts (optional)
Prepare answers for:
- “How do we productionise this?”
- “How do we stop hallucinations?”
- “What is the evaluation plan?”
- “What is the cost and latency profile?”
- “What competitors do differently, and why?”
