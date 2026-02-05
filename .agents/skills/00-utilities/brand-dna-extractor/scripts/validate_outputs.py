#!/usr/bin/env python3
"""
Validate artefacts produced by brand-dna-extractor.

Checks:
- Required output files exist
- brand_guidelines.md contains required headings (in order)
- prompt_library.json and design_tokens.json contain required top-level keys
- design_tokens.json contains evidence_map with category coverage per site
- Evidence excerpts do not exceed quote limit
- (Best-effort) flags when meaningful pages are too low

Usage:
  python scripts/validate_outputs.py --outdir ./out --quote-limit 20 --min-pages 3
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple


REQUIRED_MD_HEADINGS = [
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

REQUIRED_PROMPT_LIBRARY_KEYS = [
    "run_metadata",
    "per_site_prompt_packs",
    "composite_prompt_pack",
    "provenance_map",
]

REQUIRED_DESIGN_TOKENS_KEYS = [
    "run_metadata",
    "per_site_tokens",
    "composite_tokens",
    "conflicts",
    "resolutions",
]

SIGNAL_CATEGORIES = [
    "colours",
    "typography",
    "tokens",
    "components",
    "imagery",
    "iconography",
    "motion",
    "voice",
    "personality",
]


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _word_count(text: str) -> int:
    # Count words in a way that behaves okay for short excerpts.
    return len([w for w in re.split(r"\s+", text.strip()) if w])


def _assert(cond: bool, msg: str, errors: List[str]) -> None:
    if not cond:
        errors.append(msg)


def validate_md_headings(md_text: str, errors: List[str]) -> None:
    # Accept both "# Heading" and "## Heading" etc.
    heading_positions: Dict[str, int] = {}
    lines = md_text.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^\s{0,3}#{1,6}\s+(.*)\s*$", line)
        if m:
            title = m.group(1).strip()
            if title in REQUIRED_MD_HEADINGS and title not in heading_positions:
                heading_positions[title] = i

    for h in REQUIRED_MD_HEADINGS:
        _assert(h in heading_positions, f"brand_guidelines.md missing heading: '{h}'", errors)

    # Order check (only if all exist)
    if all(h in heading_positions for h in REQUIRED_MD_HEADINGS):
        positions = [heading_positions[h] for h in REQUIRED_MD_HEADINGS]
        _assert(
            positions == sorted(positions),
            "brand_guidelines.md headings are present but not in the required order",
            errors,
        )


def validate_prompt_library(data: Dict[str, Any], errors: List[str]) -> None:
    for k in REQUIRED_PROMPT_LIBRARY_KEYS:
        _assert(k in data, f"prompt_library.json missing top-level key: '{k}'", errors)

    # Best-effort: validate prompt pack shape
    def check_pack(pack: Any, path: str) -> None:
        if not isinstance(pack, dict):
            errors.append(f"{path} should be an object")
            return
        for key in [
            "brand_style_prompt",
            "visual_direction_prompt",
            "ui_direction_prompt",
            "copywriting_prompt",
            "negative_prompt",
            "token_set",
        ]:
            _assert(key in pack, f"{path} missing key: '{key}'", errors)

    if "composite_prompt_pack" in data:
        check_pack(data["composite_prompt_pack"], "composite_prompt_pack")

    if isinstance(data.get("per_site_prompt_packs"), list):
        for i, item in enumerate(data["per_site_prompt_packs"]):
            if not isinstance(item, dict):
                errors.append(f"per_site_prompt_packs[{i}] should be an object")
                continue
            _assert("site_id" in item, f"per_site_prompt_packs[{i}] missing 'site_id'", errors)
            _assert("root_url" in item, f"per_site_prompt_packs[{i}] missing 'root_url'", errors)
            if "prompt_pack" in item:
                check_pack(item["prompt_pack"], f"per_site_prompt_packs[{i}].prompt_pack")
            else:
                errors.append(f"per_site_prompt_packs[{i}] missing 'prompt_pack'")


def validate_design_tokens(
    data: Dict[str, Any],
    quote_limit_words: int,
    min_pages: int,
    errors: List[str],
) -> None:
    for k in REQUIRED_DESIGN_TOKENS_KEYS:
        _assert(k in data, f"design_tokens.json missing top-level key: '{k}'", errors)

    per_site = data.get("per_site_tokens")
    if not isinstance(per_site, list):
        errors.append("design_tokens.json 'per_site_tokens' should be an array")
        return

    for i, site in enumerate(per_site):
        if not isinstance(site, dict):
            errors.append(f"per_site_tokens[{i}] should be an object")
            continue

        site_id = site.get("site_id", f"index_{i}")

        # Evidence map must exist
        ev_map = site.get("evidence_map")
        _assert(isinstance(ev_map, dict), f"per_site_tokens[{i}] missing or invalid evidence_map", errors)
        if not isinstance(ev_map, dict):
            continue

        # Category coverage: require at least one evidence key per category
        keys = list(ev_map.keys())
        for cat in SIGNAL_CATEGORIES:
            has_cat = any(k == cat or k.startswith(cat + ".") for k in keys)
            _assert(has_cat, f"site '{site_id}' evidence_map has no entries for category '{cat}'", errors)

        # Quote limit
        for ev_key, ev_list in ev_map.items():
            if not isinstance(ev_list, list):
                errors.append(f"evidence_map['{ev_key}'] should be a list")
                continue
            for j, ev in enumerate(ev_list):
                if not isinstance(ev, dict):
                    errors.append(f"evidence_map['{ev_key}'][{j}] should be an object")
                    continue
                excerpt = ev.get("excerpt")
                if isinstance(excerpt, str) and excerpt.strip():
                    wc = _word_count(excerpt)
                    _assert(
                        wc <= quote_limit_words,
                        f"excerpt too long ({wc} words) at site '{site_id}' evidence_map['{ev_key}'][{j}]",
                        errors,
                    )

        # Best-effort: low page count flagging
        meaningful_pages = site.get("meaningful_pages_count")
        if isinstance(meaningful_pages, int) and meaningful_pages < min_pages:
            # Must either set needs_human_review or mention limitation
            needs_review = bool(site.get("needs_human_review"))
            limitations = site.get("limitations") or []
            mentions = any("page" in str(l).lower() and "few" in str(l).lower() for l in limitations)
            _assert(
                needs_review or mentions,
                f"site '{site_id}' has meaningful_pages_count={meaningful_pages} (<{min_pages}) but lacks clear flagging",
                errors,
            )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True, help="Directory containing output artefacts")
    ap.add_argument("--quote-limit", type=int, default=20)
    ap.add_argument("--min-pages", type=int, default=3)
    args = ap.parse_args()

    outdir = Path(args.outdir)
    errors: List[str] = []

    md_path = outdir / "brand_guidelines.md"
    pl_path = outdir / "prompt_library.json"
    dt_path = outdir / "design_tokens.json"

    _assert(md_path.exists(), "Missing brand_guidelines.md", errors)
    _assert(pl_path.exists(), "Missing prompt_library.json", errors)
    _assert(dt_path.exists(), "Missing design_tokens.json", errors)

    if md_path.exists():
        validate_md_headings(md_path.read_text(encoding="utf-8"), errors)

    if pl_path.exists():
        try:
            validate_prompt_library(_load_json(pl_path), errors)
        except Exception as e:
            errors.append(f"prompt_library.json is not valid JSON: {e}")

    if dt_path.exists():
        try:
            validate_design_tokens(_load_json(dt_path), args.quote_limit, args.min_pages, errors)
        except Exception as e:
            errors.append(f"design_tokens.json is not valid JSON: {e}")

    if errors:
        print("❌ Validation failed:")
        for e in errors:
            print("-", e)
        return 1

    print("✅ Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
