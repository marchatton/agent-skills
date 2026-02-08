#!/usr/bin/env python3
"""
validate_inputs.py

Normalise an inputs JSON payload for the demo-runbook skill.
Apply defaults and insert TODO placeholders instead of failing.

Usage:
  python scripts/validate_inputs.py < inputs.json > normalised.json

Or:
  python scripts/validate_inputs.py path/to/inputs.json > normalised.json
"""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from typing import Any, Dict, List

TODO = "[TODO]"

DEFAULTS: Dict[str, Any] = {
    "poc_name": TODO,
    "tagline": TODO,
    "audience": TODO,
    "segment": {
        "organisation": TODO,
        "buyer": TODO,
        "end_user": TODO,
    },
    "job_to_be_done": TODO,
    "starting_feelings": "rushed, uncertain, too many tabs, risk-averse",
    "desired_feelings": "confidence, clarity, speed, fewer guesses",
    "scenario": TODO,
    "success_outcome": TODO,
    "business_success_outcome": "[TODO: $ impact or growth/adoption metric + timeframe]",
    "geography": "US",
    "special_feature": {
        "name": "X",
        "what_it_does": TODO,
        "why_it_matters": TODO,
        "citation": "",
        "evidence_note": "Evidence is preliminary.",
    },
    "caveats": [
        "Done with synthetic customer data, including made-up packs.",
        "Segmentation and positioning were not a focus.",
        "This is not production ready.",
        "Goal was to create a mini Orbital Copilot PoC with special feature X (citation optional, otherwise evidence is preliminary).",
        "Focus is only on the US.",
    ],
    "competitors": [],
    "competitor_patterns": [
        "Some competitors optimise for speed and breadth, accepting more variance in grounding.",
        "Some competitors optimise for deterministic workflows, accepting less flexibility.",
        "Some competitors optimise for deep provenance, accepting more complexity and sometimes more latency.",
    ],
    "our_approach_summary": TODO,
    "tradeoffs": [TODO],
    "tech_stack": {
        "frontend": TODO,
        "backend": TODO,
        "llm_provider_and_models": TODO,
        "orchestration": TODO,
        "vector_search_or_db": TODO,
        "storage": TODO,
        "auth_security": TODO,
        "observability": TODO,
        "evals_tooling": TODO,
        "hosting": TODO,
    },
    "architecture": {
        "chosen_option": "RAG + light tool use",
        "options_considered": [
            {
                "name": "Prompt-only",
                "pros": ["Fast to build", "Few moving parts"],
                "cons": ["Weaker grounding", "Harder to keep reliable at scale"],
            },
            {
                "name": "RAG + light tool use",
                "pros": ["Better grounding", "Provenance and safer outputs"],
                "cons": ["More moving parts", "Needs tuning and monitoring"],
            },
        ],
        "rag_details": {
            "what_is_retrieved": TODO,
            "chunking": TODO,
            "retrieval_strategy": TODO,
            "grounding_behaviour": "Cite sources when available, say unknown when not grounded, ask clarifying questions when ambiguous.",
        },
        "citations_policy": "Cite when the answer depends on retrieved context, never fabricate citations, say unknown when not grounded.",
        "evals": {
            "offline_set": TODO,
            "regression": "Run on every prompt, retrieval, or model change.",
            "what_good_means": "Correct when grounded, clarifies when needed, refuses when not grounded, citations match sources.",
        },
        "observability": {
            "tracing": "Capture per-request traces including prompt version, retrieval stats, latency, and cost.",
            "failure_modes": "Log refusals, low-confidence outputs, retrieval misses, user corrections, and escalation triggers.",
        },
        "security_privacy_notes": "Separate secrets from prompts, redact logs, least privilege access, clear data boundaries.",
        "tradeoffs": [TODO],
        "rationale": TODO,
    },
    "app_links": [
        {"label": "Home", "url": TODO, "note": "Entry point"},
        {"label": "Copilot", "url": TODO, "note": "Core query and answer"},
        {"label": "Feature X", "url": TODO, "note": "Wow moment"},
    ],
    "runbook_links": [],
    "known_limitations": [
        "Coverage gaps due to synthetic data and limited corpus.",
        "Potential hallucinations if retrieval is weak or prompts are underspecified.",
        "Latency and cost not optimised in this PoC.",
    ],
    "next_steps": [
        "Replace synthetic data with real sources and access control.",
        "Expand eval set and add regression gates.",
        "Harden observability, redaction, and reliability.",
        "Decide what to productionise based on user value and risk.",
    ],
}

def deep_merge(dst: Dict[str, Any], src: Dict[str, Any]) -> Dict[str, Any]:
    for k, v in src.items():
        if k in dst and isinstance(dst[k], dict) and isinstance(v, dict):
            deep_merge(dst[k], v)
        else:
            dst[k] = v
    return dst

def normalise(payload: Dict[str, Any]) -> Dict[str, Any]:
    out = deepcopy(DEFAULTS)
    deep_merge(out, payload)

    seg = out.get("segment")
    if not isinstance(seg, dict):
        seg = deepcopy(DEFAULTS["segment"])
        out["segment"] = seg

    # Back-compat: older inputs used `persona` for the end user.
    persona = out.pop("persona", None)
    if isinstance(persona, str) and persona.strip():
        if seg.get("end_user") in (None, "", TODO):
            seg["end_user"] = persona.strip()

    bso = out.get("business_success_outcome")
    if not isinstance(bso, str) or not bso.strip():
        out["business_success_outcome"] = DEFAULTS["business_success_outcome"]

    sf = out.get("special_feature", {})
    if not isinstance(sf, dict):
        sf = deepcopy(DEFAULTS["special_feature"])
        out["special_feature"] = sf

    citation = (sf.get("citation") or "").strip()
    if citation:
        sf["evidence_note"] = "Citation provided."
    else:
        sf["evidence_note"] = "Evidence is preliminary."

    geo = (out.get("geography") or "").strip()
    out["geography"] = geo if geo else "US"

    caveats = out.get("caveats")
    if not isinstance(caveats, list):
        caveats = deepcopy(DEFAULTS["caveats"])
        out["caveats"] = caveats

    links = out.get("app_links")
    if not isinstance(links, list) or not links:
        out["app_links"] = deepcopy(DEFAULTS["app_links"])
    else:
        norm_links: List[Dict[str, Any]] = []
        for item in links:
            if isinstance(item, dict):
                norm_links.append({
                    "label": item.get("label") or "TODO link label",
                    "url": item.get("url") or TODO,
                    "note": item.get("note") or "",
                })
            else:
                norm_links.append({"label": "TODO link label", "url": TODO, "note": ""})
        out["app_links"] = norm_links

    return out

def read_input() -> Dict[str, Any]:
    if len(sys.argv) > 1:
        path = sys.argv[1]
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    return json.loads(raw)

def main() -> int:
    try:
        payload = read_input()
        if not isinstance(payload, dict):
            raise ValueError("Input JSON must be an object at the top level.")
        out = normalise(payload)
        sys.stdout.write(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
        return 0
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
