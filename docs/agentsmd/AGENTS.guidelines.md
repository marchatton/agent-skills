# Product + UI guidelines

## Purpose
- Keep product tone + interaction consistent.

## Brand
- Follow `brand-tone.md`, `brand-guidelines.md`, `product-principles.md` (if present).
- Don't invent a new voice or UI conventions.

## Accessibility baseline (minimum)
- Keyboard support + visible focus.
- Targets >= 24px (>= 44px on mobile).
- Inline errors with aria-live="polite"; focus first invalid on submit.
- Confirm destructive actions (or Undo).
- Honor prefers-reduced-motion (opacity/transform only).
- Never block paste, rely on color-only, or disable zoom.

If missing, search within `docs/02-guidelines/`.

## Helpers
- Use `docs-list` to locate guidance fast.
