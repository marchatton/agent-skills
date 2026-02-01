# Release
This folder holds the global release history across projects.

## When releasing
- Update `docs/06-release/CHANGELOG.md` with a short entry linking to the dossier + PR(s).
- Include any rollout/rollback notes if the change is risky (migrations, auth, payments, etc).

## After shipping
- Smoke test the critical paths you touched.
- Record incidents/postmortems under `docs/06-release/postmortems/` when needed.

## Helpers (if available)
Prefer existing release skills/commands in the repo over inventing a bespoke checklist.
