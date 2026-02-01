#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
vendors_file="${root_dir}/.agents/vendors.json"

usage() {
  cat <<'USAGE'
Usage:
  scripts/skills_copy.sh --all [--force]
  scripts/skills_copy.sh <skill-name> [--force]

Notes:
- Copies skill content from inspiration sources into .agents/skills.
- Does not delete extra local files; use --force to overwrite matching files.
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

force=0
mode=""
skill=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --all)
      mode="all"
      ;;
    --force)
      force=1
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

if [ -z "${mode}" ]; then
  usage
  exit 1
fi

copied=0

while IFS=$'\t' read -r name vendor src dst; do
  if [ "${mode}" = "one" ] && [ "${name}" != "${skill}" ]; then
    continue
  fi
  src_path="${root_dir}/inspiration/${vendor}/${src}"
  dst_path="${root_dir}/.agents/${dst}"

  if [ ! -e "${src_path}" ]; then
    echo "Missing source: ${src_path}" >&2
    continue
  fi

  if [ -e "${dst_path}" ] && [ "${force}" -eq 0 ]; then
    echo "Skip ${name}: ${dst_path} exists (use --force to overwrite)."
    continue
  fi

  if [ "$(basename "${dst_path}")" = "SKILL.md" ]; then
    mkdir -p "$(dirname "${dst_path}")"
    cp "${src_path}" "${dst_path}"
  else
    mkdir -p "$(dirname "${dst_path}")"
    if [ -d "${dst_path}" ]; then
      cp -R "${src_path}/." "${dst_path}/"
    else
      cp -R "${src_path}" "${dst_path}"
    fi
  fi

  copied=$((copied + 1))
  echo "Copied ${name}"

done < <(list_entries)

if [ "${mode}" = "one" ] && [ "${copied}" -eq 0 ]; then
  echo "Skill not found: ${skill}" >&2
  exit 1
fi
