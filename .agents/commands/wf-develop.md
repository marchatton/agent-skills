# wf-develop

## Purpose

Implement changes with a verification-first loop.

## Inputs

- Approved PRD and acceptance criteria.
- Target repo and branch.
- Known risks and dependencies.

## Outputs

- Code changes.
- `docs/dev/<slug>/dev-log.md` (what changed + how verified + GO/NO-GO).

## Steps

1. Define the work slug and open the target repo.
2. Implement changes with tight, verifiable increments.
3. Run pnpm ladder (lint/typecheck/test/build/verify).
4. Write `docs/dev/<slug>/dev-log.md` with summary, verification, and GO/NO-GO.

## Verification

- `pnpm lint`
- `pnpm typecheck`
- `pnpm test`
- `pnpm build`
- `pnpm verify`

## Go/No-Go

- GO if ladder is green and acceptance criteria met.
- NO-GO if any command fails or behavior cannot be demonstrated.

## Usage

- Codex: `/prompts:wf-develop <slug>`
- Claude: `/wf-develop <slug>`
