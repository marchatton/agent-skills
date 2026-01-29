#!/usr/bin/env bash
set -euo pipefail

# Scaffold a target repo using canonical templates from this repo.
# Usage: scripts/onboard_repo.sh /path/to/target-repo

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${1:-}"

if [[ -z "$TARGET_DIR" ]]; then
  echo "Usage: scripts/onboard_repo.sh /path/to/target-repo" >&2
  exit 1
fi

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Target repo not found: $TARGET_DIR" >&2
  exit 1
fi

TEMPLATES_DIR="$ROOT_DIR/docs/agentsmd"
STRUCTURE_DOC="$TEMPLATES_DIR/REPO-STRUCTURE.md"

if [[ ! -f "$STRUCTURE_DOC" ]]; then
  echo "Missing structure doc: $STRUCTURE_DOC" >&2
  exit 1
fi

# Create docs structure from the fenced block in REPO-STRUCTURE.md.
# Assumes the block starts with "docs/" and ends at the closing fence.
DOC_BLOCK=$(awk '
  $0 ~ /^```/ {in_block = !in_block; next}
  in_block && $0 ~ /^docs\// {print}
  in_block && printed {print}
' "$STRUCTURE_DOC")

if [[ -z "$DOC_BLOCK" ]]; then
  echo "No docs/ tree found in $STRUCTURE_DOC" >&2
  exit 1
fi

# Build directories and placeholder files.
while IFS= read -r line; do
  # Strip leading spaces.
  path="${line##+([[:space:]])}"
  # Skip empty lines.
  [[ -z "$path" ]] && continue
  # Skip fence artifacts or comments.
  [[ "$path" == "```"* ]] && continue

  # Determine if line is a directory (ends with /) or file.
  if [[ "$path" == */ ]]; then
    mkdir -p "$TARGET_DIR/$path"
  else
    mkdir -p "$(dirname "$TARGET_DIR/$path")"
    if [[ ! -f "$TARGET_DIR/$path" ]]; then
      : > "$TARGET_DIR/$path"
    fi
  fi
  printed=1

  # Stop when we leave docs/ block.
  if [[ $path != docs/* ]]; then
    break
  fi

done <<< "$DOC_BLOCK"

# Copy AGENTS templates into target repo.
cp -f "$TEMPLATES_DIR/AGENTS.root.md" "$TARGET_DIR/AGENTS.md"
cp -f "$TEMPLATES_DIR/AGENTS.apps-web.md" "$TARGET_DIR/apps/web/AGENTS.md"
cp -f "$TEMPLATES_DIR/AGENTS.guidelines.md" "$TARGET_DIR/docs/02-guidelines/AGENTS.md"
cp -f "$TEMPLATES_DIR/AGENTS.architecture.md" "$TARGET_DIR/docs/03-architecture/AGENTS.md"
cp -f "$TEMPLATES_DIR/AGENTS.delivery.md" "$TARGET_DIR/docs/06-delivery/AGENTS.md"

# Copy templates for docs content (if present in this repo).
if [[ -f "$ROOT_DIR/docs/templates/learnings.md" ]]; then
  cp -f "$ROOT_DIR/docs/templates/learnings.md" "$TARGET_DIR/docs/LEARNINGS.md"
fi

echo "Onboarding scaffold complete: $TARGET_DIR"
