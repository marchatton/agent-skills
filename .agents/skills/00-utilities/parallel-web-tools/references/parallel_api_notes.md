# Parallel API notes (beta)

Endpoints:
- POST /v1beta/search
- POST /v1beta/extract

Base URL:
- https://api.parallel.ai

Headers:
- x-api-key: <your key>
- parallel-beta: search-extract-2025-10-10

Search:
- Provide objective and/or search_queries
- mode: one-shot | agentic | fast

Extract:
- Provide urls list
- objective optional (recommended)
- excerpts true for compressed snippets
- full_content true for full markdown

Treat Search/Extract as beta and record request ids and warnings when available.
