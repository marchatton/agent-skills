---
name: parallel-web-tools
description: This skill should be used when users want a Firecrawl-like capability for web discovery and clean markdown extraction using Parallel Search and Parallel Extract (including objective-led excerpts and full content).
license: Complete terms in LICENSE.txt
---

# parallel-web-tools

## Purpose

Provide a repeatable workflow to:
- discover relevant URLs with Parallel Search
- extract clean markdown from URLs (including JS-heavy pages and PDFs) with Parallel Extract
- return objective-focused excerpts or full content depending on task

## When to use

Use when asked to:
- search the web for relevant sources with an explicit objective
- extract clean markdown from one or many URLs
- do “scrape this page” but want objective-focused excerpts, not raw HTML

## What this skill is not

- Not a live browser probe for computed styles or hover/focus diffs.
- For “CSS etc”, use a browser-probe lane (agent-browser / Playwright) alongside Parallel.

## Required setup

- Set environment variable `PARALLEL_API_KEY`.
- Base URL: `https://api.parallel.ai`
- Headers:
  - `x-api-key: <key>`
  - `parallel-beta: search-extract-2025-10-10`

## Workflow

### 1) Decide search vs extract
- Use Search when URLs are unknown.
- Use Extract when URLs are known.

### 2) Search
- Provide objective and/or search_queries
- mode: one-shot | agentic | fast
- Capture url, title, publish_date (if present), excerpts

### 3) Extract
- Provide urls list
- objective optional (recommended)
- excerpts=true for objective-aligned snippets
- full_content=true for full markdown

### 4) Error handling
- Retry failures up to 2 times with backoff.
- Batch requests if rate limits appear.

## Output shape recommendation
- run_metadata
- search_results (if used)
- extract_results (if used)
- errors/warnings

Use `scripts/parallel_search_extract.py` for a ready-to-run CLI.
