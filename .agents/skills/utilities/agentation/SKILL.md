---
name: agentation
description: Add Agentation visual feedback toolbar to Next.js (App Router or Pages Router). Use when installing/configuring agentation or adding dev-only <Agentation />.
---

# Agentation

## Install

- Check `package.json` for `agentation`.
- If missing, install with the active package manager (match lockfile).

## Place component

- If `app/layout.*` exists (App Router), add to root layout body after children:
```tsx
import { Agentation } from "agentation";

{process.env.NODE_ENV === "development" && <Agentation />}
```
- If `pages/_app.*` exists (Pages Router), add after `Component`:
```tsx
import { Agentation } from "agentation";

{process.env.NODE_ENV === "development" && <Agentation />}
```

## Notes

- Dev-only via `NODE_ENV` gate.
- Requires React 18.
- No extra config.

## Verify

- Run dev server; confirm toolbar appears.
- If code touched: run `pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm build`, `pnpm verify`; report GO or NO-GO with evidence.
