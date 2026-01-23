---
name: post-release-verify
description: Use when verifying post-release behavior and monitoring signals.
---

# Post-Release Verify

## Inputs

- Release checklist.
- Monitoring dashboards.
- Rollback plan.

## Outputs

- `docs/release/<slug>/post-release.md`.

## Steps

1. Run post-release checks and smoke tests.
2. Review monitors and error rates.
3. Record incidents or follow-ups.

## Verification

- Post-release doc includes checks run, monitor status, and follow-ups.
