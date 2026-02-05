#!/usr/bin/env python3
"""
Optional helper: blend per-site tokens into composite tokens.

This is a pragmatic baseline, not a full brand strategist.
Use it to generate a first pass for `design_tokens.json`:
- Choose a foundation site (blend_mode dependent)
- Select colours per role via weighted medoid in Lab colour space
- Merge voice traits via weighted voting
- Detect a small set of obvious conflicts (eg low contrast)

Input:
- A JSON file shaped like design_tokens.json (preferred), containing per_site_tokens[*].tokens
  or a brand_dna_run-like file containing per_site[*].extracted_signals / tokens.

Output:
- JSON to stdout with:
  - composite_tokens
  - conflicts
  - resolutions

Usage:
  python scripts/blend_signals.py --input design_tokens.json --blend-mode harmonise
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


ROLES = ["primary", "secondary", "accent", "background", "text"]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def hex_to_rgb01(hex_str: str) -> Tuple[float, float, float]:
    h = hex_str.strip().lstrip("#")
    if len(h) == 3:
        h = "".join([c * 2 for c in h])
    r = int(h[0:2], 16) / 255.0
    g = int(h[2:4], 16) / 255.0
    b = int(h[4:6], 16) / 255.0
    return r, g, b


def srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rgb_to_xyz(r: float, g: float, b: float) -> Tuple[float, float, float]:
    # sRGB D65
    rl, gl, bl = srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b)
    x = rl * 0.4124 + gl * 0.3576 + bl * 0.1805
    y = rl * 0.2126 + gl * 0.7152 + bl * 0.0722
    z = rl * 0.0193 + gl * 0.1192 + bl * 0.9505
    return x, y, z


def f_lab(t: float) -> float:
    delta = 6 / 29
    return t ** (1 / 3) if t > delta ** 3 else (t / (3 * delta ** 2)) + (4 / 29)


def xyz_to_lab(x: float, y: float, z: float) -> Tuple[float, float, float]:
    # Reference white D65
    xn, yn, zn = 0.95047, 1.00000, 1.08883
    fx, fy, fz = f_lab(x / xn), f_lab(y / yn), f_lab(z / zn)
    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)
    return L, a, b


def hex_to_lab(hex_str: str) -> Tuple[float, float, float]:
    r, g, b = hex_to_rgb01(hex_str)
    x, y, z = rgb_to_xyz(r, g, b)
    return xyz_to_lab(x, y, z)


def lab_distance(c1: Tuple[float, float, float], c2: Tuple[float, float, float]) -> float:
    return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2)


def relative_luminance(hex_str: str) -> float:
    r, g, b = hex_to_rgb01(hex_str)
    rl, gl, bl = srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b)
    return 0.2126 * rl + 0.7152 * gl + 0.0722 * bl


def contrast_ratio(hex1: str, hex2: str) -> float:
    l1 = relative_luminance(hex1)
    l2 = relative_luminance(hex2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def normalise_weights(items: List[Dict[str, Any]]) -> List[float]:
    ws: List[float] = []
    for it in items:
        w = it.get("weight")
        ws.append(float(w) if isinstance(w, (int, float)) else 1.0)
    s = sum(ws)
    if s <= 0:
        return [1.0 / len(ws)] * len(ws)
    return [w / s for w in ws]


def pick_foundation(items: List[Dict[str, Any]], weights: List[float], blend_mode: str) -> int:
    if not items:
        return 0
    if blend_mode == "dominant_source":
        return max(range(len(items)), key=lambda i: weights[i])
    # fallback: weight * confidence if present
    def score(i: int) -> float:
        conf = items[i].get("confidence")
        c = float(conf) if isinstance(conf, (int, float)) else 0.75
        return weights[i] * c
    return max(range(len(items)), key=score)


def extract_site_tokens(site_obj: Dict[str, Any]) -> Dict[str, Any]:
    # Support design_tokens.json style: site_obj.tokens
    if isinstance(site_obj.get("tokens"), dict):
        return site_obj["tokens"]
    # Support brand_dna_run-like: extracted_signals or tokens
    if isinstance(site_obj.get("extracted_signals"), dict):
        # If present, treat tokens as extracted_signals.tokens else map
        ex = site_obj["extracted_signals"]
        if isinstance(ex.get("tokens"), dict):
            return ex["tokens"]
        # fallback: return a shallow projection
        return ex
    return {}


def get_colour_hex(colour_value: Any) -> Optional[str]:
    # Accept "#rrggbb", or {"hex":"#..."}
    if isinstance(colour_value, str) and colour_value.strip().startswith("#"):
        return colour_value.strip()
    if isinstance(colour_value, dict):
        h = colour_value.get("hex")
        if isinstance(h, str) and h.strip().startswith("#"):
            return h.strip()
    return None


def blend_colours(
    sites: List[Dict[str, Any]],
    weights: List[float],
    foundation_idx: int,
    blend_mode: str,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    # Returns (composite_colours, conflicts, resolutions)
    # Baseline: pick per-role medoid (existing site colour), no averaging.
    candidates: Dict[str, List[Tuple[int, str, Tuple[float, float, float]]]] = {r: [] for r in ROLES}
    for i, site in enumerate(sites):
        tokens = extract_site_tokens(site)
        colours = tokens.get("colours") or tokens.get("colors") or {}
        if not isinstance(colours, dict):
            continue
        for role in ROLES:
            hx = get_colour_hex(colours.get(role))
            if hx:
                try:
                    candidates[role].append((i, hx, hex_to_lab(hx)))
                except Exception:
                    continue

    composite: Dict[str, Any] = {}
    provenance: List[Dict[str, Any]] = []
    conflicts: List[Dict[str, Any]] = []
    resolutions: List[Dict[str, Any]] = []

    for role in ROLES:
        cands = candidates.get(role, [])
        if not cands:
            # Fallback: skip
            continue

        if blend_mode == "dominant_source":
            # Prefer foundation site if it has the role
            f = [c for c in cands if c[0] == foundation_idx]
            chosen = f[0] if f else cands[0]
        else:
            # Weighted medoid
            best = None
            best_score = float("inf")
            for (i, hx_i, lab_i) in cands:
                score = 0.0
                for (j, hx_j, lab_j) in cands:
                    d = lab_distance(lab_i, lab_j)
                    score += weights[j] * d
                if score < best_score:
                    best_score = score
                    best = (i, hx_i, lab_i)
            chosen = best if best else cands[0]

        chosen_i, chosen_hex, _ = chosen
        composite[role] = chosen_hex
        provenance.append({"signal": f"colours.{role}", "from": sites[chosen_i].get("site_id", str(chosen_i)), "weight": weights[chosen_i]})

    # Simple conflict: contrast ratio of text/background
    bg = composite.get("background")
    tx = composite.get("text")
    if isinstance(bg, str) and isinstance(tx, str):
        try:
            cr = contrast_ratio(bg, tx)
            if cr < 4.5:
                conflicts.append({
                    "type": "contrast_low",
                    "description": f"Text/background contrast ratio is {cr:.2f} (< 4.5).",
                    "affected_signals": ["colours.background", "colours.text"],
                    "sources": [p["from"] for p in provenance if p["signal"] in ["colours.background", "colours.text"]],
                })
                # Resolution: attempt swap text/background from foundation if available
                resolutions.append({
                    "decision": "Keep selected colours but flag for manual adjustment (WCAG contrast).",
                    "rationale": "Automated blend produced low contrast; manual tweak needed for accessibility.",
                    "chosen_sources": [p["from"] for p in provenance],
                    "blend_mode": blend_mode,
                })
        except Exception:
            pass

    return {"roles": composite, "provenance": provenance}, conflicts, resolutions


def blend_voice_traits(sites: List[Dict[str, Any]], weights: List[float]) -> Dict[str, Any]:
    # Weighted vote on traits from tokens.voice.traits or tokens.personality.traits
    scores: Dict[str, float] = {}

    for i, site in enumerate(sites):
        tokens = extract_site_tokens(site)
        voice = tokens.get("voice") or {}
        pers = tokens.get("personality") or {}
        traits = []
        if isinstance(voice, dict) and isinstance(voice.get("traits"), list):
            traits.extend([str(t).strip() for t in voice["traits"] if str(t).strip()])
        if isinstance(pers, dict) and isinstance(pers.get("traits"), list):
            traits.extend([str(t).strip() for t in pers["traits"] if str(t).strip()])
        # Deduplicate within site
        traits = list(dict.fromkeys([t.lower() for t in traits]))

        for t in traits:
            scores[t] = scores.get(t, 0.0) + weights[i]

    # Top traits
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    top = [t for t, _ in ranked[:7]]
    return {"traits": top, "trait_scores": scores}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to JSON input (design_tokens.json or brand_dna_run-like)")
    ap.add_argument("--blend-mode", default=None, choices=["harmonise", "bold_hybrid", "dominant_source", "theme_collage"])
    args = ap.parse_args()

    data = load_json(Path(args.input))

    # Extract per-site list
    sites: List[Dict[str, Any]] = []
    if isinstance(data.get("per_site_tokens"), list):
        sites = data["per_site_tokens"]
    elif isinstance(data.get("per_site"), list):
        sites = data["per_site"]
    else:
        raise SystemExit("Input JSON does not contain per_site_tokens or per_site")

    weights = normalise_weights(sites)

    blend_mode = args.blend_mode
    if blend_mode is None:
        # Try read from run_metadata if present
        rm = data.get("run_metadata") or {}
        blend_mode = rm.get("blend_mode") or "harmonise"

    foundation_idx = pick_foundation(sites, weights, blend_mode)

    colours_out, conflicts, resolutions = blend_colours(sites, weights, foundation_idx, blend_mode)
    voice_out = blend_voice_traits(sites, weights)

    composite = {
        "tokens": {
            "colours": colours_out["roles"],
            "voice": {"traits": voice_out["traits"]},
        },
        "provenance": colours_out["provenance"],
        "confidence": 0.7,
        "needs_human_review": True if conflicts else False,
    }

    out = {
        "composite_tokens": composite,
        "conflicts": conflicts,
        "resolutions": resolutions,
    }

    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
