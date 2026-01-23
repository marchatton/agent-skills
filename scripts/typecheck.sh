#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

required_files=(
  "AGENTS.md"
  ".agents/AGENTS.md"
  "docs/templates/prd.md"
  "docs/templates/breadboard.md"
  "docs/templates/spike-plan.md"
  "docs/templates/pack.md"
  "docs/templates/release-checklist.md"
  "docs/templates/json-prd.schema.json"
  "docs/templates/learnings.md"
  "docs/templates/learning-entry.md"
  "docs/guides/oracle.md"
  "docs/guides/ralph.md"
  ".agents/commands/wf-explore.md"
  ".agents/commands/wf-shape.md"
  ".agents/commands/wf-develop.md"
  ".agents/commands/wf-review.md"
  ".agents/commands/wf-release.md"
  ".agents/commands/wf-ralph.md"
  ".agents/commands/verify.md"
  ".agents/commands/compound.md"
  ".agents/commands/oracle.md"
  ".agents/hooks/README.md"
  ".agents/ralph/config.sh"
  ".agents/vendors.json"
  "scripts/vendor_update.sh"
  "scripts/vendor_sync.sh"
  "scripts/agents_refresh.sh"
  "scripts/generate_cheatsheet.ts"
  "scripts/verify_repo.sh"
  "scripts/oracle.sh"
  ".agents/skills/explore/opportunity-solution-tree/SKILL.md"
  ".agents/skills/explore/customer-segmentation/SKILL.md"
  ".agents/skills/explore/positioning/SKILL.md"
  ".agents/skills/explore/roadmap/SKILL.md"
  ".agents/skills/explore/pricing-packaging/SKILL.md"
  ".agents/skills/shape/create-prd/SKILL.md"
  ".agents/skills/shape/breadboard/SKILL.md"
  ".agents/skills/shape/spike-plan/SKILL.md"
  ".agents/skills/shape/deepen-plan/SKILL.md"
  ".agents/skills/shape/prd-review/SKILL.md"
  ".agents/skills/shape/create-json-prd/SKILL.md"
  ".agents/skills/develop/work-execute/SKILL.md"
  ".agents/skills/develop/reproduce-bug/SKILL.md"
  ".agents/skills/develop/report-bug/SKILL.md"
  ".agents/skills/develop/resolve-todos/SKILL.md"
  ".agents/skills/develop/resolve-pr-feedback/SKILL.md"
  ".agents/skills/review/pr-review/SKILL.md"
  ".agents/skills/review/agent-native-architecture/SKILL.md"
  ".agents/skills/review/browser-qa/SKILL.md"
  ".agents/skills/release/release-checklist/SKILL.md"
  ".agents/skills/release/changelog-draft/SKILL.md"
  ".agents/skills/release/post-release-verify/SKILL.md"
  ".agents/skills/compound/compound-docs/SKILL.md"
  ".agents/skills/utilities/oracle/SKILL.md"
  ".agents/skills/utilities/create-cli/SKILL.md"
  ".agents/skills/utilities/docs-list/SKILL.md"
  ".agents/skills/utilities/trash/SKILL.md"
  ".agents/skills/utilities/ask-questions-if-underspecified/SKILL.md"
  "hooks/git/pre-commit"
  "hooks/git/pre-push"
  "hooks/git/prepare-commit-msg"
  "hooks/git/commit-msg"
  "hooks/git/post-merge"
  "scripts/install_git_hooks.sh"
  "scripts/install_codex_skills_copy.sh"
  "cheatsheet.md"
)

missing=()
for file in "${required_files[@]}"; do
  if [ ! -f "${root_dir}/${file}" ]; then
    missing+=("${file}")
  fi
done

if [ "${#missing[@]}" -gt 0 ]; then
  printf "Typecheck failed. Missing required files:\n"
  printf "- %s\n" "${missing[@]}"
  exit 1
fi

echo "Typecheck OK."
