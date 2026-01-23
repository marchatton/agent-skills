# wf-explore

## Purpose

Define the opportunity and next experiment before shaping.

## Inputs

- Problem context and target users.
- Current metrics or qualitative signals.
- Constraints and known risks.

## Outputs

- `docs/explore/<slug>/opportunity-solution-tree.md`
- Optional: `docs/explore/<slug>/customer-segmentation.md`
- Optional: `docs/explore/<slug>/positioning.md`
- Optional: `docs/explore/<slug>/roadmap.md`

## Steps

1. Define the work slug and create the output folder in the project repo.
2. Run skill `opportunity-solution-tree` to capture problems, opportunities, and experiments.
3. Add optional segmentation/positioning/roadmap docs if needed.
4. Summarize the next experiment and expected learning.

## Verification

- Target user, target metric, riskiest assumption, and next experiment are explicit.

## Go/No-Go

- GO if the opportunity is scoped and the next bet is clear.
- NO-GO if it is a list without a testable next step.

## Usage

- Codex: `/prompts:wf-explore <slug>`
- Claude: `/wf-explore <slug>`
