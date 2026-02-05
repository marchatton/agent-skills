---
name: verify
description: Verify changes before done; scripts then UI smoke; output PASS/NO-GO.
---

# verify

## Purpose
Provide a single, consistent way for agents to verify changes before claiming “done”.

## When to run
Run verification for every change that alters behaviour, build outputs, tests, types, linting, packaging, CI, or UI.
If you cannot verify, return **NO-GO** with a concrete reason and the smallest unblock request.

## Procedure

### 0) Pick scope (don’t waste time)
- Prefer the smallest scope that covers what changed:
  - single package/app if changes are local
  - repo-wide only if shared libraries, configs, or multiple packages changed
- If unsure, start scoped, then widen if failures suggest shared impact.

### 1) Discover the available verification scripts (don’t guess)
1) Identify the relevant `package.json`:
- repo root for repo-wide checks
- the changed package/app directory for scoped checks

2) List scripts from the relevant `package.json`:
- Look for canonical script names first:
  - `verify`
  - `test`, `test:unit`, `test:ci`
  - `lint`
  - `typecheck`, `tsc`
  - `build`
  - `format`, `fmt`, `prettier:check`
  - `check` (sometimes bundles lint/typecheck/test)

3) If none exist, search one level up/down for where scripts live (monorepo layouts vary).
If you still cannot find scripts, return **NO-GO** and ask for expected verification steps or for a `verify` script to be added.

### 2) Run verification in this order (stop on red)
Run the best available equivalents in this order:

1) Format / basic hygiene (only if a check script exists)
- Prefer `format:check` / `prettier:check` / `fmt:check`
- Do not run auto-format as “verification” unless explicitly requested

2) Lint
- Run the repo/package lint script

3) Typecheck
- Run `typecheck` / `tsc` / equivalent

4) Tests
- Run the smallest relevant test suite:
  - `test` / `test:unit` for code changes
  - include integration/e2e only when the repo provides it and it’s relevant

5) Build
- Run `build` when:
  - you changed build outputs, bundling, env wiring, dependencies, or UI
  - or when the repo commonly relies on build as a gate

Notes:
- If the repo provides a single `verify` or `check` script, prefer it first. If it fails, fix before running anything else.
- In monorepos, use the workspace/package targeting mechanism that exists in the repo (don’t assume pnpm). If unclear, run within the package directory.

### 3) UI smoke testing (required for UI/user-flow changes)
If changes affect UI, routing, auth flows, forms, state, client behaviour, styling that could break layout, or anything user-visible, do a smoke test.

#### 3.1 Start the app
- Use the repo’s normal dev/start script for the relevant app (e.g. `dev`, `start`, `preview`).
- If there are multiple apps, start the one you changed.

If you cannot start the app due to missing env/secrets, return **NO-GO** and request the minimal env needed (or a mock mode).

#### 3.2 Smoke checklist (happy path + one sad path)
Do the minimum that proves the change works:
- Load the page/route you touched
- Exercise the changed behaviour end-to-end
- Confirm no obvious runtime errors (console/network) and the UI behaves as intended
- Do one “sad path” where relevant (invalid form submit, unauth access, empty state)

#### 3.3 Basic a11y spot-check
- Keyboard: tab order makes sense, focus is visible, primary actions reachable
- Forms: error message appears, first invalid field gets focus (or is clearly indicated)
- No colour-only signalling for errors or status
- Reduced motion: no jarring animations if the change touches motion (best-effort)

#### 3.4 Evidence
Prefer using the `agent-browser` skill for smoke testing when real interaction matters.
Capture evidence where possible:
- screenshot of the critical state, or
- short description of the steps performed + observed outcome

### 4) If something fails
- Keep the fix small and local first.
- If the failure is due to missing scripts or repeated workflow pain, recommend adding a `verify` script that bundles lint/typecheck/test/build for that scope.

## Output contract (mandatory)
Include a section named `Verification` with either:

### PASS
- `PASS:`
  - Commands run (exact)
  - Results (pass)
  - UI smoke (if applicable): steps + outcome + evidence note

### NO-GO
- `NO-GO:`
  - What blocked verification (exact)
  - What you need to proceed (smallest unblock request)
  - What you did manage to verify (if anything)
