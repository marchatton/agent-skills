---
name: wf-review
description: This skill should only be used when the user uses the word workflow and asks to review changes (select mode: light, light-plus, heavy) with verification and context handoff/pickup to avoid context rot.
---

# wf-review

## Purpose

Review changes at the right depth, then produce a clear GO/NO-GO with evidence.

Default mode: **light-plus**.

Always run basic verification (verify skill). Treat review as provisional if verification cannot be run.

## Args (free text)

Parse mode + target from user text.

**Mode tokens (first match wins):**
- `light`
- `light-plus`
- `heavy`

Accept either:
- `wf-review light PR#123`
- `wf-review mode: heavy target: <url>`
- `wf-review <target>` (mode missing)

**Target examples:**
- PR number/URL
- branch name
- file path (doc review)
- empty = current branch

**If mode missing:** ask (default **light-plus**).
**If target missing:** ask.

## Outputs

All modes:
- Review summary + severity (P1/P2/P3)
- Verification result (verify skill) + GO/NO-GO
- Optional handoff notes (recommended)

Heavy only:
- Todo files for findings (file-todos skill)

## Mode behaviours

### light

Minimum: run native `/review` only (no extra passes). Then run verify skill.

Use when:
- Small diffs
- Low risk
- You mostly want a sanity check

### light-plus (default)

Run:
- native `/review`
- repo prompt review: `/rp-review`
- verify skill

Use when:
- Most PRs
- You want repo-specific conventions checked too

### heavy

Do **light-plus**, then do the full wf-review deep pass:
- multi-angle passes (single-agent, sequential)
- deep-dive scenarios
- synthesize + de-dupe
- create todos for **all** findings (file-todos)
- verify loop (optionally fix verify failures)
- optional `test-browser` if UI/user flow changed
- final GO/NO-GO

Use when:
- auth/payments/privacy/external APIs/migrations
- big refactors / large surface area
- repeated CI failures / flaky behaviour
- user explicitly asks for “thorough”

## Steps (all modes)

1) Determine mode + target
- If missing: ask once (mode default light-plus, target default current branch).

2) (Recommended) Pickup if starting fresh thread / resuming
- Invoke `pickup` skill if:
  - new chat/thread, or
  - user says “resume / pick up”, or
  - repo/branch uncertain

3) Gather review context
- If PR number/URL: capture title/body/files/diff via `gh pr view --json` if available.
- If branch: confirm current branch matches target (ask before switching).
- If file path: open the file and treat as doc review.

4) Run review analysis for chosen mode
- light: `/review`
- light-plus: `/review` then `/rp-review`
- heavy: do light-plus, then run the heavy checklist below

5) Run basic verification (all modes)
- Invoke verify skill in target repo.
- If verify cannot be run: mark as “unverified” and block GO unless change is docs-only.

6) Summarise + decide
- De-dupe findings.
- Label severity:
  - P1 blocks merge/release
  - P2 should fix
  - P3 nice-to-have
- Write GO/NO-GO with reasons + evidence.

7) (Recommended) Handoff at workflow boundary
- If switching workflows next (fix work, release, more Ralph): invoke `handoff`.
- If user wants clean context: recommend starting a new thread and running `pickup` there with the handoff note path.

## Heavy checklist (only when mode=heavy)

A) Review passes (single-agent, sequential; no sub-agents)
- security-sentinel
- performance-oracle
- architecture-strategist
- data-integrity-guardian
- agent-native-reviewer
- pattern-recognition-specialist
- language reviewer if relevant (kieran-*-reviewer)
- code-simplicity-reviewer
- if migrations/backfills: data-migration-expert + deployment-verification-agent

B) Deep-dive scenarios
- invalid inputs, boundaries, concurrency, scale, timeouts, resource exhaustion
- data corruption, security attacks, cascading failures

C) Todo creation (mandatory in heavy)
- Invoke `file-todos` for **all** findings.
- Store under the active dossier if present:
  - `docs/04-projects/<lane>/<id>_<slug>/todos/`
- Periodic reviews/audits can store under:
  - `docs/05-reviews-audits/<slug>/todos/`

D) Verify loop
- Run verify skill.
- If verify fails: ask “Fix failures now? (y/n)”
  - If yes: loop up to N iterations (default 10): fix top failure, run targeted check, then rerun verify
  - If no: proceed to summary with failures called out

E) Optional browser QA
- If UI/user-flow changed: run `test-browser` and record evidence.

F) Mandatory handoff
- End heavy review with `handoff`.
- Recommend a new thread for fix work: `/new` then `pickup` + read the handoff note.

## Verification

- Verify skill run (or explicitly marked unverified)
- Heavy: todo files created for all findings

## Go/No-Go

- GO if verify is green and no P1 gaps remain.
- NO-GO if verify fails, or correctness/security/rollout risks remain unresolved.
