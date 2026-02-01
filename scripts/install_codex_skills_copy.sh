#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./scripts/install_codex_skills_copy.sh
#   CODEX_HOME=/custom/path ./scripts/install_codex_skills_copy.sh

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="${root_dir}/.agents/skills"

if [ ! -d "${source_dir}" ]; then
  echo "Missing source skills directory: ${source_dir}"
  exit 1
fi

codex_home="${CODEX_HOME:-$HOME/.codex}"
dest_dir="${codex_home}/skills"

if [ -L "${dest_dir}" ]; then
  echo "Refusing to copy into symlinked destination: ${dest_dir}"
  exit 1
fi

mkdir -p "${dest_dir}"

echo "Copying skills to ${dest_dir}"

if command -v rsync >/dev/null 2>&1; then
  rsync -aL "${source_dir}/" "${dest_dir}/"
else
  cp -RL "${source_dir}/" "${dest_dir}/"
fi

echo "Copy complete."
echo "If needed, set CODEX_HOME to target a different Codex home."
echo "Note: This copy does not delete stale skills; remove them manually if needed."
