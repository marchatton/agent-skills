---
name: wf-shape
description: This skill should only be used when the user uses the word workflow and asks to shape a project from messy inputs into a de-risked, de-scoped shaped packet (brief, breadboard, risks, spikes) ready for wf-plan, with handoff/pickup boundaries to avoid context rot.
---

# wf-shape

## Purpose

Turn messy inputs into a shaped packet that is ready for commit-ready planning (wf-plan).

Optimise for:
- de-scope (draw the perimeter)
- risks understood (rabbit holes surfaced + treated)
- concrete artefacts (brief + breadboard + spikes)

## Inputs

- Raw notes, feature idea, bug report, links
- Constraints + appetite/timebox
- Any existing artefacts (designs, metrics, incidents)

## Outputs (dossier)

Create/update a dossier folder:
- `docs/04-projects/<lane>/<id>_<slug>/`

Files:
- `brief.md` (1–2 pager)
- `breadboard-pack.md`
- `risk-register.md`
- `spike-investigation.md` (optional; single file)

## Steps

0) Pickup (recommended if resuming / new thread)
- Invoke `pickup` if repo/dossier context is not fresh.

1) Start a dossier
- Choose `id_<slug>` (prefer `0001_<short>`).
- Choose a lane under `docs/04-projects/`.
- Create dossier + stub files.

2) Write the 1–2 pager brief
- Write `brief.md`.
- Hard requirements:
  - goals + non-goals
  - in-scope/out-of-scope perimeter
  - top risks + unknowns
  - open questions
  - GO/NO-GO placeholder

3) Breadboard
- Invoke breadboarding skill.
- Save as `breadboard-pack.md` (places/affordances/connections + parts list + rabbit holes + fit check).

4) Risk register
- Write `risk-register.md`.
- For every top risk choose: Cut / Patch / Spike / Out-of-bounds.

5) Spike investigation (only for Spike items)
- Invoke spike-investigation skill for each Spike.
- Record results in `spike-investigation.md`.

6) Oracle pass (mandatory per spike)
- After each spike section, invoke `oracle` skill.
- Append oracle notes and apply cuts/patches if needed.

7) Synthesis + perimeter lock
- Update `brief.md` to reflect the final perimeter, cuts, and risk treatments.
- Ensure breadboard is buildable as parts.

8) Shaping decision
- GO only if biggest risks are proved, cut, or out-of-bounds.

9) Handoff to wf-plan (recommended boundary)
- Invoke `handoff` and include:
  - dossier path
  - perimeter (in/out)
  - biggest risks + spike outcomes
  - what wf-plan must decide next
- Recommend starting wf-plan in a fresh thread:
  - `/new` then `pickup` then run wf-plan with the dossier path

## Verification

- brief has perimeter + testable outcomes
- risk register has a mitigation for each top risk
- spikes (if any) include oracle notes

## Go/No-Go

- GO if a stranger can explain what will be built and what won’t from brief + breadboard.
- NO-GO if core mechanics are still foggy.
