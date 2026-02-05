---
name: docs-list
description: Run `scripts/docs-list.ts` to list `docs/` markdown + frontmatter summary/read_when. Use when auditing docs coverage.
---

# Docs List

## Quick Start

```bash
pnpm dlx tsx scripts/docs-list.ts
```

## Behavior

- Walks `docs/` (skips `archive/`, `research/`).
- Requires frontmatter `summary:`; optional `read_when:` list.
- Output `path - summary` (+ `Read when:`); errors flagged.

## Steps

1. Ensure local copy `scripts/docs-list.ts` (copy from `inspiration/agent-scripts/scripts/docs-list.ts` if missing).
2. Run from repo root.
3. Review errors for missing/stale docs.

## Outputs

- Paths + summaries for `docs/`.
- Missing/stale notes.

## Verification

- Output includes paths + summaries; errors shown.
