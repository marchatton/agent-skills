# Templates Cheatsheet

Quick reference for commands, skills, and hooks in this repo.

## Commands

Workflow commands use `wf-*` prefix. Utility commands use `c-*` prefix.

| Command | Purpose | Invocation (Codex) | Invocation (Claude) |
|---------|---------|-------------------|---------------------|
| **wf-explore** | Product strategy, opportunity briefs, experiments | `/prompts:wf-explore` | `/wf-explore` |
| **wf-shape** | PRDs, specs, architecture sketches | `/prompts:wf-shape` | `/wf-shape` |
| **wf-plan** | Transform ideas into structured plans | `/prompts:wf-plan` | `/wf-plan` |
| **wf-work** | Execute work plans with quality checks | `/prompts:wf-work` | `/wf-work` |
| **wf-review** | Multi-agent code review, finding synthesis | `/prompts:wf-review` | `/wf-review` |
| **wf-release** | Release checklist, deploy verification | `/prompts:wf-release` | `/wf-release` |
| **wf-compound** | Capture solved problems as docs | `/prompts:wf-compound` | `/wf-compound` |
| **c-handoff** | Package session state for next agent | `/prompts:c-handoff` | `/c-handoff` |
| **c-pickup** | Rehydrate context when starting work | `/prompts:c-pickup` | `/c-pickup` |
| **c-landpr** | Land PRs with rebase, gate, merge | `/prompts:c-landpr <pr>` | `/c-landpr <pr>` |

## Skills

Skills grouped by workflow category. Invoke with `skill: <name>` in prompts.

### work/
| Skill | Purpose |
|-------|---------|
| frontend-design | Distinctive, production-grade UI with high design quality |

### review/
| Skill | Purpose |
|-------|---------|
| agent-native-architecture | Build apps where agents are first-class citizens |

### compound/
| Skill | Purpose |
|-------|---------|
| compound-docs | Capture solved problems as categorized docs with YAML frontmatter |

### utilities/
| Skill | Purpose |
|-------|---------|
| agent-browser | Browser automation via Vercel's agent-browser CLI |
| create-agent-skills | Expert guidance for creating Claude Code skills |
| every-style-editor | Review/edit copy against Every style guide |
| file-todos | File-based todo tracking in todos/ directory |
| gemini-imagegen | Image generation/editing with Gemini API |
| markdown-converter | Convert documents to Markdown via markitdown |
| nano-banana-pro | Image generation/editing with Nano Banana Pro (Gemini) |
| openai-image-gen | Batch image generation via OpenAI Images API |
| oracle | Bundle prompt+files for second-model review |
| skill-creator | Official skill creator from Anthropic spec |
| video-transcript-downloader | Download videos, audio, subtitles, transcripts |

## Hooks

Git hooks in `hooks/git/`. Ship as templates - edit to enable.

| Hook | Purpose |
|------|---------|
| pre-commit.sample | Run lint/format if package.json exists |
| pre-push.sample | Run typecheck/test if package.json exists |

## Scripts

| Script | Purpose |
|--------|---------|
| `install_codex_prompts.sh` | Copy commands to ~/.codex/prompts/ |
| `install_claude_commands.sh` | Copy commands to .claude/commands/ |
| `install_git_hooks.sh` | Install hook templates to .git/hooks/ |
| `committer` | Scoped git commit helper (stages only listed paths) |
| `verify.sh` | Verify repo structure and print smoke test steps |

## Artifact Paths (for target repos)

| Artifact | Path | Created by |
|----------|------|------------|
| Plans | `docs/plans/<type>-<slug>.md` | wf-plan |
| Todos | `docs/todos/{id}-{status}-{priority}-{desc}.md` | wf-review |
| Solutions | `docs/solutions/<category>/<slug>.md` | wf-compound |

## Quick Verification

```bash
./scripts/verify.sh
```
