# compound

## Purpose

Append a structured learning entry to `docs/learnings.md` in the project repo.

## Inputs

- Stage (explore/shape/develop/review/release/other).
- Title.
- Context links (PR, issue, docs paths).
- Summary and what changed.
- Root cause, fix, prevention.
- Verification evidence (required if code-touching).

## Outputs

- Updated `docs/learnings.md` (append-only).

## Steps

1. Open the project repo `docs/learnings.md`.
2. Add a new entry under the matching stage heading.
3. Include required fields and verification evidence if code-touching.
4. Keep history append-only.

## Verification

- Entry includes date, stage, summary, root cause, fix, prevention, verification, and links.

## Go/No-Go

- GO if entry is complete and appended under correct stage.
- NO-GO if required fields are missing.

## Usage

- Codex: `/prompts:compound`
- Claude: `/compound`
