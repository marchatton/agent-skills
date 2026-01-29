---
name: use-ai-sdk
description: AI SDK guidance. Use for Vercel AI SDK APIs (generateText, streamText, ToolLoopAgent, tools), providers, streaming, tool calling, structured output, or troubleshooting.
---

# AI SDK

## Prefer local docs (ai@6.0.34+)

- Search docs: `rg "query" node_modules/ai/docs`
- Search source: `rg "query" node_modules/ai/src`
- List docs: `rg --files -g "node_modules/ai/docs/**/*.mdx"`
- List source: `rg --files -g "node_modules/ai/src/**/*.ts"`

## Provider packages (ai@6.0.34+)

- Search provider docs: `rg "query" node_modules/@ai-sdk/<provider>/docs`
- Search provider source: `rg "query" node_modules/@ai-sdk/<provider>/src`
- Use provider docs for `providerOptions` details.

## Remote docs fallback

- Search: `https://ai-sdk.dev/api/search-docs?q=<query>`
- Fetch `.md` links from results for plain-text docs.

## References

- Common errors: `references/common-errors.md`
- AI Gateway: `references/ai-gateway.md`

## Verify

- Confirm AI SDK version and doc source (local vs remote).
- If code touched: run `pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm build`, `pnpm verify`; report GO or NO-GO with evidence.
