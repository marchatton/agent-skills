# Verify agents.md

How to run checks

If a command below doesn’t exist, **don’t guess**. Check `package.json` scripts (repo root and the relevant package), then update this file.

## Repo-wide checks (monorepo)
Use these when you’re changing shared libs or touching multiple areas.
- Typecheck: `pnpm -r typecheck`
- Lint: `pnpm -r lint`
- Unit tests: `pnpm -r test`

Notes:
- Prefer running the smallest scope that gives confidence (single package first), then go wider if needed.
- If a package doesn’t have a script, that’s fine — don’t add scripts just to satisfy this list unless it’s a recurring pain.

## Package/app checks (scoped)

Use when you’re working in a single package/app.

Pattern:
- `pnpm -F <pkg> typecheck`
- `pnpm -F <pkg> lint`
- `pnpm -F <pkg> test`

Example (web):
- `pnpm -F web typecheck`
- `pnpm -F web lint`
- `pnpm -F web test`

## UI / browser testing
Only run these when UI behaviour changes, or a bug is browser-specific.

- Browser tests (if present): `pnpm -F web test:browser`
- Prefer using the `agent-browser` skill for verification when the result depends on real interaction.

## Smoke checks (manual, quick)
Do these when you changed UI, auth, routing, payments, or anything user-facing.

- Load the critical path you touched (happy path + one sad path)
- Keyboard: tab order, focus visible, submit works
- Forms: error messaging shows and focuses first invalid field
- Prefer reduced motion: no jarring animations

## Refactor signals (optional)
Some repos include extra scripts to catch dead code, duplication, or unsafe refactors.
If present, run them during refactors or larger clean-ups.

Examples (if present):
- `pnpm -F web scan`
- `pnpm -F web dead`
- `pnpm -F web dupes`
- `pnpm -F web refactor:check`

## If something fails
- Keep the fix small and local first.
- If the failure suggests a missing script or repeated workflow, prefer adding/updating a skill/command in `marchatton/templates` over expanding `AGENTS.md`.
