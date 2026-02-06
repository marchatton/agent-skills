# Hooks (templates)

Hooks under `.agents/hooks/` are canonical templates.

Git hooks:
- Source (tracked): `.agents/hooks/git/*`
- Install: run `scripts/install_git_hooks.sh` (sets `core.hooksPath`)
- Repo config: `scripts/git-hooks.config.sh` (sourced by hooks)
