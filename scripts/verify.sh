#!/usr/bin/env bash
# Verify templates repo structure and compliance
# Run from repo root: ./scripts/verify.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT"

errors=0
warnings=0

pass() { echo "  ✓ $1"; }
fail() { echo "  ✗ $1"; ((errors++)) || true; }
warn() { echo "  ⚠ $1"; ((warnings++)) || true; }

echo "=== Templates Repo Verification ==="
echo ""

# 1. Required directory structure
echo "## Directory Structure"
for dir in skills/explore skills/shape skills/work skills/review skills/release skills/compound skills/utilities commands hooks/git scripts; do
  if [ -d "$dir" ]; then
    pass "$dir/"
  else
    fail "$dir/ missing"
  fi
done
echo ""

# 2. Each skill folder has SKILL.md
echo "## Skills"
skill_count=0
for skill_dir in skills/*/*/; do
  [ -d "$skill_dir" ] || continue
  skill_name=$(basename "$skill_dir")
  if [ -f "$skill_dir/SKILL.md" ]; then
    # Extract only the first YAML frontmatter block (between first and second ---)
    frontmatter=$(awk 'NR==1 && /^---$/{start=1; next} start && /^---$/{exit} start{print}' "$skill_dir/SKILL.md" || true)
    has_name=$(echo "$frontmatter" | grep -c '^name:' || true)
    has_desc=$(echo "$frontmatter" | grep -c '^description:' || true)
    # Check for extra fields (not name, description, or empty/whitespace lines)
    extra_fields=$(echo "$frontmatter" | grep -v '^name:' | grep -v '^description:' | grep -v '^[[:space:]]*$' | head -1 || true)
    
    if [ "$has_name" -ge 1 ] && [ "$has_desc" -ge 1 ]; then
      if [ -n "$extra_fields" ]; then
        warn "$skill_name: extra frontmatter field detected: $extra_fields"
      else
        pass "$skill_name"
      fi
    else
      fail "$skill_name: missing name or description in frontmatter"
    fi
    ((skill_count++)) || true
  else
    fail "$skill_name: missing SKILL.md"
  fi
done
echo "  Total skills: $skill_count"
echo ""

# 3. Baseline command set
echo "## Commands"
baseline_commands="wf-explore wf-shape wf-plan wf-work wf-review wf-release wf-compound c-handoff c-pickup c-landpr"
for cmd in $baseline_commands; do
  if [ -f "commands/${cmd}.md" ]; then
    pass "$cmd.md"
  else
    fail "$cmd.md missing"
  fi
done
cmd_count=$(ls -1 commands/*.md 2>/dev/null | wc -l | tr -d ' ')
echo "  Total commands: $cmd_count"
echo ""

# 4. Cheatsheet exists and has required sections
echo "## Cheatsheet"
if [ -f "cheatsheet.md" ]; then
  pass "cheatsheet.md exists"
  for section in "## Commands" "## Skills" "## Hooks"; do
    if grep -q "$section" cheatsheet.md; then
      pass "Has $section section"
    else
      fail "Missing $section section"
    fi
  done
else
  fail "cheatsheet.md missing"
fi
echo ""

# 5. Install scripts
echo "## Install Scripts"
for script in install_codex_prompts.sh install_claude_commands.sh install_git_hooks.sh; do
  if [ -f "scripts/$script" ] && [ -x "scripts/$script" ]; then
    pass "$script (executable)"
  elif [ -f "scripts/$script" ]; then
    warn "$script exists but not executable"
  else
    fail "$script missing"
  fi
done
echo ""

# 6. Hooks
echo "## Hooks"
for hook in pre-commit.sample pre-push.sample; do
  if [ -f "hooks/git/$hook" ]; then
    pass "$hook"
  else
    warn "$hook missing (optional)"
  fi
done
echo ""

# Summary
echo "=== Summary ==="
if [ $errors -eq 0 ]; then
  echo "✓ All checks passed ($warnings warnings)"
  echo ""
  echo "=== Manual Smoke Test Steps ==="
  echo ""
  echo "1. Install commands:"
  echo "   ./scripts/install_codex_prompts.sh"
  echo "   ./scripts/install_claude_commands.sh  # in target repo"
  echo "   ./scripts/install_git_hooks.sh        # in target repo"
  echo ""
  echo "2. Test wf-plan in Codex:"
  echo "   /prompts:wf-plan 'Add user authentication'"
  echo "   → Confirm plan file created in docs/plans/"
  echo ""
  echo "3. Test review artefact flow:"
  echo "   → Create plan → run review lane → check todos/"
  echo ""
  exit 0
else
  echo "✗ $errors error(s), $warnings warning(s)"
  exit 1
fi
