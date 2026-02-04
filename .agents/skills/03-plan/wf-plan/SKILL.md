---
name: wf-plan
description: This skill should only be used when the user uses the word workflow and asks to create a commit-ready, deep project plan from a shaped packet (brief, breadboard, risks, spikes) before development starts, with handoff/pickup boundaries to avoid context rot.
---

# wf-plan

## Purpose

Turn a shaped packet (wf-shape dossier) into a commit-ready plan without re-litigating the shape.

Never implement production code. Only research and write the plan.

## Inputs

Dossier folder path containing:
- `brief.md`
- `breadboard-pack.md`
- `risk-register.md`
- `spike-investigation.md` (if present)

## Outputs

Inside the same dossier:
- `plan.md`

## Steps

0) Pickup (recommended if new thread)
- Invoke `pickup` if repo/branch state is not fresh.

1) Ingest shaped packet (no idea refinement loop)
- Read brief → breadboard → risk register → spikes.
- If perimeter or top risks are missing: route back to wf-shape.

2) Create plan skeleton
- Create `plan.md` with:
  - scope (in/out)
  - key flows + key logic
  - acceptance criteria + verification plan
  - sequencing/phases + stop points
  - rollout/rollback + observability
  - dependencies + risks

3) Local research (always)
- Find similar patterns in repo.
- Pull institutional learnings (docs/solutions, docs/LEARNINGS.md).
- Record concrete file paths.

4) External research (conditional)
- Always external for: security/auth, payments, privacy, external APIs, migrations.
- Otherwise only if local context is thin.

5) Spec hardening (gap pass)
- Edge cases, failure modes, concurrency, performance, data integrity, security threats.
- Update acceptance criteria + verification.

6) Plan review passes
- Simplicity, risk, ops/release, data integrity, security/privacy, UX/product.
- Final mandatory pass: invoke `oracle` on the whole plan and integrate findings (or mark out-of-bounds).

7) Commit gate
- GO only if:
  - AC measurable
  - verification per AC
  - sequencing explicit
  - rollout/rollback explicit
  - no P1 unknowns remain

8) Handoff to build (recommended boundary)
- Invoke `handoff` and include:
  - plan path + summary of phases
  - how to verify
  - rollout notes
  - biggest remaining risks
- Recommend build in a fresh thread:
  - `/new` then `pickup` then run wf-develop or wf-ralph

## Verification

- plan includes acceptance criteria + verification + rollout/rollback
- oracle pass integrated

## Go/No-Go

- GO if the plan can be built without re-discovering the shape.
- NO-GO if it depends on “we’ll figure it out during implementation”.
