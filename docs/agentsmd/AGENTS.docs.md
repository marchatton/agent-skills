# Docs hub

## Purpose
Single place for workflow artefacts + docs outputs.

## Folder structure
- We follow a PARA-inspired technique for knowledge management. Under /docs we have:
  - Projects:
    - `04-projects/`: lanes include experiments-prototypes, features, fixes, refactors and migrations
  - Areas: 
    - `00-strategy/`:  up-to-date product-strategy, roadmap and large initiatives
    - `03-architecture/`: up-to-date system and data architecture 
    - `05-reviews-audits/`: periodic reviews, audits, and systems compliance 
    - `06-release/`: global `CHANGELOG.md` and postmortems etc
    - `96-engineering-tutor-learnings` a collection of learnings from `engineering-tutor` skill. 
    - `97-throwaway/`: local-only scratch space (NOT synced to GitHub)
    - `98-tmp/`: scratch space. Synced to GitHub. Avoid .gitignore for files in this folder, instead move them to `97-throwaway/` if they are not needed anymore.
      - `/oracle/`: oracle `--render` bundles for non-dossier work
      - `/handoffs/`: handoff notes for non-dossier or cross-dossier work
  - Resources:
    - `01-insights/`: reports, summaries and raw transcripts covering customers, competitors, capabilities (internal) and tech-market trends.
    - `08-example-data/` contains worked examples with synthetic yet realistic data.
    - `02-guidelines/`: brand ui guidelines and design system guidelines.
  - Archive: 
    - `99-archive/` mirrors the live structure for closed work + old context

## Guidelines
- Keep docs append-only where that’s the existing convention (e.g. `CHANGELOG.md`, `LEARNINGS.md`).
- Knowledge management for projects (`04-projects/`): 
  - Inside a lane (e.g. `docs/04-projects/02-features/`), create a dossier folder. e.g. `docs/04-projects/02-features/0007_bulk-invite-members/`
  - Folder name is: 0001_<slug>/
    - `0001` is lane-local (features count separately from fixes, etc)
    - `<slug>` is kebab-case
    - Every work item has a slug for easy `@slug` tagging in PRDs and discussions.
  - All change types require PRD markdown + JSON (even if tiny). Naming depends on whether the dossier has 1 PRD or multiple PRDs:
    - Single-PRD dossier: `prd.md` + `prd.json`
    - Multi-PRD dossier: `prd-overall.md` + `prd-overall.json` plus slice PRDs under `prds/<slice_id>_<slug>/prd.md` + `prd.json`
  - Reviews for a project live inside its dossier (e.g. `reviews/`).

## Storing oracle bundles and handoff notes
- Oracle bundles (`oracle --render`) are committed under:
  - Dossier work: `<dossier>/tmp-oracle/` (inside `docs/04-projects/...`)
  - Non-dossier work: `docs/98-tmp/oracle/`
- Handoff notes (`handoff` skill) are committed under:
  - Dossier work: `<dossier>/tmp-handoffs/` (inside `docs/04-projects/...`)
  - Non-dossier or cross-dossier: `docs/98-tmp/handoffs/`
- Filenames:
  - Oracle bundles: `oracle-bundle_<slug>.md` (or `oracle-bundle_<id>_<slug>.md` inside dossiers)
  - Handoff notes: `handoff_YYYY-MM-DD_HH-MM-SS_<slug>.md`
- Store local-only scratch in root `throwaway/` (gitignored; not synced to GitHub)
- Store other random tmp files in root `tmp/` folder (synced to GitHub)
- When working on a project, follow the conventions outlined in `docs/04-projects/AGENTS.md`

## Archiving rule
- Completed work and old context is manually moved into `docs/99-archive/` which mirrors the live structure.

## Cross-cutting concerns
- Log ADRs by appending to `docs/03-architecture/DECISIONS.md`.
- Synthesis: use `compound` to consolidate learnings.
