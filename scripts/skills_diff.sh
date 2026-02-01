#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
vendors_file="${root_dir}/.agents/vendors.json"

usage() {
  cat <<'USAGE'
Usage:
  scripts/skills_diff.sh --list
  scripts/skills_diff.sh --all
  scripts/skills_diff.sh <skill-name>

Notes:
- Diffs local skills against inspiration sources from .agents/vendors.json.
- Directories use recursive diff; files use unified diff.
USAGE
}

list_entries() {
  python3 - "${vendors_file}" <<'PY'
import json
import sys
from pathlib import Path

path = sys.argv[1]
with open(path, 'r', encoding='utf-8') as fh:
    data = json.load(fh)

entries = []
for vendor, cfg in data.items():
    for item in cfg.get("sync", []):
        src = item.get("src")
        dst = item.get("dst")
        if not src or not dst:
            continue
        if not dst.startswith("skills/"):
            continue
        dst_path = Path(dst)
        if dst_path.name == "SKILL.md":
            name = dst_path.parent.name
        else:
            name = dst_path.name
        entries.append((name, vendor, src, dst))

for name, vendor, src, dst in entries:
    print(f"{name}\t{vendor}\t{src}\t{dst}")
PY
}

mode="all"
skill=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --all)
      mode="all"
      ;;
    --list)
      mode="list"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [ -n "${skill}" ]; then
        usage
        exit 1
      fi
      skill="$1"
      mode="one"
      ;;
  esac
  shift
done

if [ "${mode}" = "list" ]; then
  list_entries | cut -f1 | sort -u
  exit 0
fi

found=0

while IFS=$'\t' read -r name vendor src dst; do
  if [ "${mode}" = "one" ] && [ "${name}" != "${skill}" ]; then
    continue
  fi
  found=1
  src_path="${root_dir}/inspiration/${vendor}/${src}"
  dst_path="${root_dir}/.agents/${dst}"

  if [ ! -e "${src_path}" ]; then
    echo "Missing source: ${src_path}" >&2
    continue
  fi
  if [ ! -e "${dst_path}" ]; then
    echo "Missing local: ${dst_path}" >&2
    continue
  fi

  echo "==> ${name}"
  if [ "$(basename "${dst_path}")" = "SKILL.md" ]; then
    diff -u "${src_path}" "${dst_path}" || true
  else
    diff -ru -x .DS_Store "${src_path}" "${dst_path}" || true
  fi

done < <(list_entries)

if [ "${mode}" = "one" ] && [ "${found}" -eq 0 ]; then
  echo "Skill not found: ${skill}" >&2
  exit 1
fi
