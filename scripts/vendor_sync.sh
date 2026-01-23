#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
vendors_file="${root_dir}/.agents/vendors.json"

if [ ! -f "${vendors_file}" ]; then
  echo "Missing .agents/vendors.json"
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required to parse vendors.json"
  exit 1
fi

errors=0

while IFS=$'\t' read -r vendor src dst; do
  [ -z "${vendor}" ] && continue

  src_path="${root_dir}/inspiration/${vendor}/${src}"
  dst_path="${root_dir}/.agents/${dst}"

  if [ ! -e "${src_path}" ]; then
    echo "Missing source: ${src_path}"
    errors=1
    continue
  fi

  mkdir -p "$(dirname "${dst_path}")"

  if [ -e "${dst_path}" ] && [ ! -L "${dst_path}" ]; then
    echo "Refusing to overwrite non-symlink: ${dst_path}"
    echo "Move or remove the local fork, or update vendors.json to point elsewhere."
    errors=1
    continue
  fi

  if [ -L "${dst_path}" ]; then
    rm "${dst_path}"
  fi

  ln -s "${src_path}" "${dst_path}"
  echo "Linked ${dst_path} -> ${src_path}"
done < <(
  python3 - "${vendors_file}" <<'PY'
import json
import sys

path = sys.argv[1]
with open(path, 'r', encoding='utf-8') as fh:
    data = json.load(fh)

for vendor, cfg in data.items():
    for item in cfg.get("sync", []):
        src = item.get("src")
        dst = item.get("dst")
        if not src or not dst:
            continue
        print(f"{vendor}\t{src}\t{dst}")
PY
)

if [ "${errors}" -ne 0 ]; then
  exit 1
fi

echo "Vendor sync complete."
