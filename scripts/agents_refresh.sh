#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

steps=(
  "vendor_update|${root_dir}/scripts/vendor_update.sh"
  "vendor_sync|${root_dir}/scripts/vendor_sync.sh"
  "npx_skills_refresh|${root_dir}/scripts/npx_skills_refresh.sh"
  "generate_cheatsheet|${root_dir}/scripts/generate_cheatsheet.ts"
  "verify_repo|${root_dir}/scripts/verify_repo.sh"
)

statuses=()
failed=0

for entry in "${steps[@]}"; do
  name="${entry%%|*}"
  cmd="${entry#*|}"

  echo "==> ${name}"

  if [ "${name}" = "generate_cheatsheet" ]; then
    if node --experimental-strip-types -e "" >/dev/null 2>&1; then
      if node --experimental-strip-types "${cmd}"; then
        statuses+=("${name}: OK")
      else
        statuses+=("${name}: FAIL")
        failed=1
        break
      fi
    else
      echo "Node does not support --experimental-strip-types. Upgrade Node or install a TS runner."
      statuses+=("${name}: FAIL")
      failed=1
      break
    fi
  else
    if "${cmd}"; then
      statuses+=("${name}: OK")
    else
      statuses+=("${name}: FAIL")
      failed=1
      break
    fi
  fi

done

echo "Summary:"
for status in "${statuses[@]}"; do
  echo "- ${status}"
done

if [ "${failed}" -ne 0 ]; then
  exit 1
fi

echo "Agents refresh complete."
