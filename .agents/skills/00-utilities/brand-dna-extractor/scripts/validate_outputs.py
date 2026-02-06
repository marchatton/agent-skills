"""
validate_outputs.py

Baseline validator for the three required artefacts.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

REQUIRED_HEADINGS = [
    "Overview",
    "Composite Brand DNA",
    "Composite Design Tokens",
    "Composite Voice & Copy",
    "Composite Prompt Pack",
    "Provenance Map",
    "Conflicts & Resolutions",
    "Per-site Appendices",
    "Limitations",
]

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_md_headings(md: str) -> List[str]:
    headings = []
    for line in md.splitlines():
        line = line.strip()
        if line.startswith("#"):
            text = line.lstrip("#").strip()
            if text:
                headings.append(text)
    return headings

def assert_required_headings(md_path: str) -> None:
    md = load_text(md_path)
    headings = extract_md_headings(md)
    missing = [h for h in REQUIRED_HEADINGS if h not in headings]
    if missing:
        raise AssertionError(f"Missing required headings: {missing}")

    idx = {h: headings.index(h) for h in REQUIRED_HEADINGS}
    for a, b in zip(REQUIRED_HEADINGS, REQUIRED_HEADINGS[1:]):
        if idx[a] > idx[b]:
            raise AssertionError(f"Heading order wrong: '{a}' appears after '{b}'")

def assert_top_keys(obj: Any, required_keys: List[str], path: str) -> None:
    if not isinstance(obj, dict):
        raise AssertionError(f"{path} must be a JSON object at top level.")
    missing = [k for k in required_keys if k not in obj]
    if missing:
        raise AssertionError(f"Missing keys in {path}: {missing}")

def count_words(s: str) -> int:
    return len([w for w in re.split(r"\s+", s.strip()) if w])

def walk(obj: Any) -> List[Any]:
    out = []
    if isinstance(obj, dict):
        out.append(obj)
        for v in obj.values():
            out.extend(walk(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(walk(v))
    return out

def enforce_quote_limit_in_design_tokens(tokens: Dict[str, Any], quote_limit_words: int) -> List[str]:
    errors: List[str] = []
    nodes = walk(tokens)
    for node in nodes:
        if not isinstance(node, dict):
            continue
        if node.get("type") == "excerpt" and isinstance(node.get("excerpt"), str):
            wc = count_words(node["excerpt"])
            if wc > quote_limit_words:
                errors.append(f"Excerpt exceeds quote_limit_words ({wc} > {quote_limit_words}): {node.get('page_url')}")
    return errors

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--quote-limit", type=int, default=20)
    args = ap.parse_args()

    out_dir = args.dir
    bg = os.path.join(out_dir, "brand_guidelines.md")
    pl = os.path.join(out_dir, "prompt_library.json")
    dt = os.path.join(out_dir, "design_tokens.json")

    for p in (bg, pl, dt):
        if not os.path.exists(p):
            print(f"Missing required output file: {p}", file=sys.stderr)
            return 2

    assert_required_headings(bg)

    prompt_lib = load_json(pl)
    assert_top_keys(prompt_lib, ["run_metadata", "per_site_prompt_packs", "composite_prompt_pack", "provenance_map"], pl)

    tokens = load_json(dt)
    assert_top_keys(tokens, ["run_metadata", "per_site_tokens", "composite_tokens", "conflicts", "resolutions"], dt)

    quote_errors = enforce_quote_limit_in_design_tokens(tokens, args.quote_limit)
    if quote_errors:
        for e in quote_errors:
            print(e, file=sys.stderr)
        return 3

    print("OK: outputs pass baseline validation.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
