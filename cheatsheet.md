# Cheatsheet

## Commands
- `agent-native-audit`: Purpose not documented. (verify: See command.)
- `changelog`: Purpose not documented. (verify: See command.)
- `compound`: Append a structured learning entry to `docs/learnings.md` in the project repo. (verify: Entry includes date, stage, summary, root cause, fix, prevention, verification, and links.)
- `create-agent-skill`: Purpose not documented. (verify: See command.)
- `deepen-plan`: Purpose not documented. (verify: See command.)
- `generate-command`: Purpose not documented. (verify: See command.)
- `handoff`: Purpose not documented. (verify: See command.)
- `heal-skill`: Purpose not documented. (verify: See command.)
- `landpr`: Purpose not documented. (verify: See command.)
- `oracle`: Run the Oracle CLI as latest via the wrapper script. (verify: Oracle command completes without errors.)
- `pickup`: Purpose not documented. (verify: See command.)
- `plan-review`: Purpose not documented. (verify: See command.)
- `report-bug`: Purpose not documented. (verify: See command.)
- `reproduce-bug`: Purpose not documented. (verify: See command.)
- `resolve-parallel`: Purpose not documented. (verify: See command.)
- `resolve-pr-parallel`: Purpose not documented. (verify: See command.)
- `resolve-todo-parallel`: Purpose not documented. (verify: See command.)
- `test-browser`: Purpose not documented. (verify: See command.)
- `triage`: Purpose not documented. (verify: See command.)
- `verify`: Run the pnpm verification ladder with clear GO/NO-GO output. (verify: `pnpm lint`)
- `wf-develop`: Implement changes with a verification-first loop. (verify: `pnpm lint`)
- `wf-explore`: Define the opportunity and next experiment before shaping. (verify: Target user, target metric, riskiest assumption, and next experiment are explicit.)
- `wf-ralph`: Run a continuous coding loop with Ralph and finish with verification. (verify: `verify` (pnpm ladder))
- `wf-release`: Ship changes with a release checklist, changelog, and post-release verification. (verify: `pnpm verify`)
- `wf-review`: Review changes with explicit verification and risk checks. (verify: `pnpm verify`)
- `wf-shape`: Produce a PRD and optional supporting artefacts that are ready for implementation. (verify: Acceptance criteria are testable and mapped to verification steps.)

## Skills
### compound
- `compound-docs`: Use when appending structured learnings to a project repo's docs/learnings.md.

### develop
- `report-bug`: Use when writing a bug report with reproduction details and impact.
- `reproduce-bug`: Use when you need to reproduce a bug with clear steps and evidence.
- `resolve-pr-feedback`: Use when addressing PR feedback and re-verifying changes.
- `resolve-todos`: Use when resolving TODOs and cleanup items with verification.
- `work-execute`: Use when implementing planned work with a tight verify-first loop.

### explore
- `customer-segmentation`: Use when defining customer segments and targeting criteria during Explore.
- `opportunity-solution-tree`: Use when selecting a product opportunity and defining the next experiment; produce an opportunity-solution tree.
- `positioning`: Use when defining product positioning, differentiation, and messaging in Explore.
- `pricing-packaging`: Use when exploring pricing and packaging options for a product or feature.
- `roadmap`: Use when outlining high-level sequencing and milestones in Explore.

### release
- `changelog-draft`: Use when drafting release notes or a changelog entry for a release.
- `post-release-verify`: Use when verifying post-release behavior and monitoring signals.
- `release-checklist`: Use when preparing a release checklist with rollout, rollback, and monitoring steps.

### review
- `agent-native-architecture`: Use when reviewing architecture for agent-native workflows, risks, and verification needs.
- `browser-qa`: Use when running browser QA checks for user flows and visual regressions.
- `pr-review`: Use when reviewing a PR for correctness, risk, and verification evidence.

### shape
- `breadboard`: Use when mapping the core user/system flow for a feature or change.
- `create-json-prd`: Use when converting a PRD into the canonical JSON PRD for tooling; requires a PRD and may include breadboard/spike/plan inputs.
- `create-prd`: Use when shaping work into a PRD with acceptance criteria and verification plan.
- `deepen-plan`: Use when sequencing work, dependencies, and cut lines need a deeper plan.
- `prd-review`: Use when reviewing a PRD for clarity, scope, and verification readiness.
- `spike-plan`: Use when a timeboxed spike is needed to answer risks or unknowns.

### utilities
- `agent-browser`: Browser automation using Vercel's agent-browser CLI. Use when you need to interact with web pages, fill forms, take screenshots, or scrape data. Alternative to Playwright MCP - uses Bash commands with ref-based element selection. Triggers on "browse website", "fill form", "click button", "take screenshot", "scrape page", "web automation".
- `ask-questions-if-underspecified`: Clarify requirements before implementing. Do not use automatically, only when invoked explicitly.
- `create-agent-skills`: Expert guidance for creating, writing, and refining Claude Code Skills. Use when working with SKILL.md files, authoring new skills, improving existing skills, or understanding skill structure and best practices.
- `create-cli`: Use when creating a new CLI project scaffold with pnpm and basic structure.
- `docs-list`: Use when listing or summarizing docs files in a repo.
- `every-style-editor`: This skill should be used when reviewing or editing copy to ensure adherence to Every's style guide. It provides a systematic line-by-line review process for grammar, punctuation, mechanics, and style guide compliance.
- `file-todos`: This skill should be used when managing the file-based todo tracking system in the todos/ directory. It provides workflows for creating todos, managing status and dependencies, conducting triage, and integrating with slash commands and code review processes.
- `frontend-design`: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
- `gemini-imagegen`: This skill should be used when generating and editing images using the Gemini API (Nano Banana Pro). It applies when creating images from text prompts, editing existing images, applying style transfers, generating logos with text, creating stickers, product mockups, or any image generation/manipulation task. Supports text-to-image, image editing, multi-turn refinement, and composition from multiple reference images.
- `markdown-converter`: Convert documents and files to Markdown using markitdown. Use when converting PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx, .xls), HTML, CSV, JSON, XML, images (with EXIF/OCR), audio (with transcription), ZIP archives, YouTube URLs, or EPubs to Markdown format for LLM processing or text analysis.
- `nano-banana-pro`: Generate/edit images with Nano Banana Pro (Gemini 3 Pro Image). Use for image create/modify requests incl. edits. Supports text-to-image + image-to-image; 1K/2K/4K; use --input-image.
- `openai-image-gen`: Batch-generate images via OpenAI Images API. Random prompt sampler + `index.html` gallery.
- `oracle`: Use when running Oracle CLI workflows; wraps the latest Oracle CLI with Node 22+ checks.
- `skill-creator`: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
- `trash`: Use when safely deleting or archiving files with confirmation and notes.
- `video-transcript-downloader`: Download videos, audio, subtitles, and clean paragraph-style transcripts from YouTube and any other yt-dlp supported site. Use when asked to “download this video”, “save this clip”, “rip audio”, “get subtitles”, “get transcript”, or to troubleshoot yt-dlp/ffmpeg and formats/playlists.

## Hooks
- `hooks/git/commit-msg`
- `hooks/git/post-merge`
- `hooks/git/pre-commit`
- `hooks/git/pre-push`
- `hooks/git/prepare-commit-msg`

## Verification
- `pnpm lint`
- `pnpm typecheck`
- `pnpm test`
- `pnpm build`
- `pnpm verify`

## Key Output Paths
- `docs/explore/<slug>/opportunity-solution-tree.md`
- `docs/shape/<slug>/prd.md`
- `docs/shape/<slug>/breadboard.md`
- `docs/shape/<slug>/spike-plan.md`
- `docs/shape/<slug>/plan.md`
- `docs/shape/<slug>/prd.json`
- `.agents/tasks/prd-<slug>.json`
- `docs/dev/<slug>/dev-log.md`
- `docs/review/<slug>/review.md`
- `docs/review/<slug>/browser-qa.md`
- `docs/release/<slug>/release.md`
- `docs/release/<slug>/changelog.md`
- `docs/release/<slug>/post-release.md`
- `docs/learnings.md`
- `.ralph/`
