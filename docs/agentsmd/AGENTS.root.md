# AGENTS.md

## Tooling
- Package manager: pnpm (workspaces).

## Canonical and local agents files and instructions (skills, commands, hooks etc)
- For codex, use .agents and Agents.md
- For other agentic tools, respective skills and files etc will be symlinked using `iannuttal/dotagents. Don’t fork instructions per agentic tool (e.g. Claude, Amp).
- `AGENTS.md` is the source of truth. Any other agent-specific files are symlinks — don’t fork instructions per tool.
- Canonical skills/commands/hooks live in `marchatton/templates` (synced into this repo via symlinks). If a skill/command seems missing or wrong, fix it there.

## Principles
- Keep changes small and focused (one concern per PR).
- Prefer the simplest thing that meets the requirement (avoid enterprise edge-case soup).
- Prefer TypeScript for new code unless the repo already uses something else.

## Error handling + safety (high level)
- Validate external inputs at boundaries (Zod) and return safe user-facing errors.
- Don’t leak internal errors/details to clients.
- Unexpected issues: fail loudly (log/throw). Only surface user-facing errors when needed.

## Compatibility
- Local/unreleased workspace changes: optimise for speed; compatibility usually not required.
- Anything already released: ask before making breaking changes.

## Verification
- Don’t guess commands. Use `docs/verify.md` (if present) and the relevant package `package.json` scripts.
- Use `agent-browser` skill 

## Skills usage
Core skills to frequently use:
- `ask-questions-if-underspecified` when unclear.
- `oracle` for deep research.
- When you invoke a skill, print echo: `:: the <skill name> skill must FLOW ::`
