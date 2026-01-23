#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
vendors_dir="${root_dir}/inspiration"

# Managed vendor repos:
# - agent-scripts: https://github.com/steipete/agent-scripts.git
# - compound-engineering-plugin: https://github.com/EveryInc/compound-engineering-plugin
vendors=(
  "agent-scripts|https://github.com/steipete/agent-scripts.git"
  "compound-engineering-plugin|https://github.com/EveryInc/compound-engineering-plugin"
)

mkdir -p "${vendors_dir}"

for entry in "${vendors[@]}"; do
  name="${entry%%|*}"
  repo="${entry#*|}"
  target="${vendors_dir}/${name}"

  if [ ! -d "${target}/.git" ]; then
    echo "Cloning ${name}..."
    git clone "${repo}" "${target}"
  else
    echo "Updating ${name}..."
    git -C "${target}" pull --ff-only
  fi

done

echo "Vendor update complete."
