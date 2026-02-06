"""
parallel_search_extract.py

Minimal CLI wrapper around Parallel Search (beta) and Extract (beta).

Requirements:
  pip install httpx

Env:
  PARALLEL_API_KEY
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

import httpx

API_BASE = "https://api.parallel.ai"
BETA_HEADER_VALUE = "search-extract-2025-10-10"

def require_key() -> str:
    key = os.environ.get("PARALLEL_API_KEY", "").strip()
    if not key:
        print("Missing PARALLEL_API_KEY env var.", file=sys.stderr)
        raise SystemExit(2)
    return key

def client() -> httpx.Client:
    key = require_key()
    return httpx.Client(
        base_url=API_BASE,
        headers={
            "Content-Type": "application/json",
            "x-api-key": key,
            "parallel-beta": BETA_HEADER_VALUE,
        },
        timeout=60.0,
    )

def post_json(c: httpx.Client, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    r = c.post(path, json=payload)
    try:
        data = r.json()
    except Exception:
        data = {"raw_text": r.text}
    if r.status_code >= 400:
        raise RuntimeError(f"{path} failed ({r.status_code}): {data}")
    return data

def do_search(objective: Optional[str], search_queries: Optional[List[str]], mode: str, max_results: int) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"mode": mode, "max_results": max_results}
    if objective:
        payload["objective"] = objective
    if search_queries:
        payload["search_queries"] = search_queries
    if not payload.get("objective") and not payload.get("search_queries"):
        raise ValueError("Provide objective or search_queries.")
    with client() as c:
        return post_json(c, "/v1beta/search", payload)

def do_extract(urls: List[str], objective: Optional[str], excerpts: bool, full_content: bool, fetch_policy: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"urls": urls, "excerpts": excerpts, "full_content": full_content}
    if objective:
        payload["objective"] = objective
    if fetch_policy:
        payload["fetch_policy"] = fetch_policy
    with client() as c:
        return post_json(c, "/v1beta/extract", payload)

def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search")
    s.add_argument("--objective", default=None)
    s.add_argument("--query", action="append", dest="search_queries", default=None)
    s.add_argument("--mode", default="agentic", choices=["one-shot", "agentic", "fast"])
    s.add_argument("--max-results", type=int, default=10)

    e = sub.add_parser("extract")
    e.add_argument("--urls", nargs="+", required=True)
    e.add_argument("--objective", default=None)
    e.add_argument("--excerpts", action="store_true", default=True)
    e.add_argument("--no-excerpts", action="store_false", dest="excerpts")
    e.add_argument("--full-content", action="store_true", default=False)

    se = sub.add_parser("search-then-extract")
    se.add_argument("--objective", required=True)
    se.add_argument("--mode", default="agentic", choices=["one-shot", "agentic", "fast"])
    se.add_argument("--max-results", type=int, default=5)
    se.add_argument("--extract-objective", default=None)
    se.add_argument("--excerpts", action="store_true", default=True)
    se.add_argument("--no-excerpts", action="store_false", dest="excerpts")
    se.add_argument("--full-content", action="store_true", default=False)

    args = ap.parse_args()

    try:
        if args.cmd == "search":
            out = do_search(args.objective, args.search_queries, args.mode, args.max_results)
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 0

        if args.cmd == "extract":
            out = do_extract(args.urls, args.objective, args.excerpts, args.full_content)
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 0

        if args.cmd == "search-then-extract":
            search_out = do_search(args.objective, None, args.mode, args.max_results)
            urls = [r.get("url") for r in search_out.get("results", []) if isinstance(r, dict) and r.get("url")]
            extract_out = do_extract(urls, args.extract_objective, args.excerpts, args.full_content)
            combined = {"run_metadata": {"objective": args.objective, "mode": args.mode, "max_results": args.max_results},
                        "search": search_out, "extract": extract_out}
            print(json.dumps(combined, indent=2, ensure_ascii=False))
            return 0

        return 1

    except Exception as ex:
        print(str(ex), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
