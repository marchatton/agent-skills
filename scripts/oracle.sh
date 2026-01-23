#!/usr/bin/env bash
set -euo pipefail

node_version=""
if command -v node >/dev/null 2>&1; then
  node_version="$(node -v)"
fi

if [ -n "${node_version}" ]; then
  node_major="${node_version#v}"
  node_major="${node_major%%.*}"
  if [ "${node_major}" -lt 22 ]; then
    echo "Warning: Node 22+ required. Current: ${node_version}" 1>&2
  fi
else
  echo "Warning: Node 22+ required. Node not found." 1>&2
fi

if command -v pnpm >/dev/null 2>&1; then
  pnpm dlx @steipete/oracle@latest "$@"
else
  npx -y @steipete/oracle@latest "$@"
fi
