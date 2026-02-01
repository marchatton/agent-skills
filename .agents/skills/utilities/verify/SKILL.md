---
name: verify
description: Single verification flow; read docs/AGENTS.md; report PASS/NO-GO.
---

# Verify

## Purpose
Skill-only verification. Repo steps live in `docs/AGENTS.md`.

## When
Any change affecting behavior/build/tests/types/lint/package/UI. If blocked, return NO-GO + smallest unblock.

## Steps
1. Read `docs/AGENTS.md` verification section.
2. If a `verify` script exists, run it first.
3. Run smallest-scope scripts in doc (monorepo: narrowest package).
4. If docs missing: run lint/typecheck/test/build if present; else NO-GO.

## Browser smoke (UI only)
If UI/user-flow changed: after normal checks, use `agent-browser` skill to start app, exercise path, capture evidence.

## Output
Include a `Verification` section with commands + results.
Use `PASS:` or `NO-GO:`.
