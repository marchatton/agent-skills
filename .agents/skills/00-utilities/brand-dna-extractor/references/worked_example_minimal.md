# Worked example (minimal)

This file shows the expected shapes and evidence anchoring style.
Do not copy any slogans from real sites. Paraphrase.

## Evidence anchor convention

Use: `[site_id:page_id:signal_key]`

Example:
- `[acme:home:colour.primary]`
- `[acme:pricing:motion.button_hover]`

## Example per-site signals (sketch)

Site: acme
- Colour primary: #3B82F6 `[acme:home:colour.primary]`
- Typography body: Inter, 16px, 1.5 `[acme:home:type.body]`
- Radius: 10–12px on CTAs `[acme:home:radius.button]`
- Motion: 200ms ease on hover `[acme:home:motion.button_hover]`
- Voice: direct, confident, benefit-led CTAs `[acme:home:voice.cta_style]`

## Example composite resolution (sketch)

Conflict: two competing primaries (blue vs purple)
Resolution (harmonise):
- Keep blue as primary, use purple as accent only for highlights.
- Enforce neutral base for backgrounds.
Provenance:
- Primary from acme (weight 0.6)
- Accent from beta (weight 0.4)

## Example output trio (sketch)

- brand_guidelines.md uses the exact headings from the template
- prompt_library.json includes per-site and composite prompt packs
- design_tokens.json includes per-site tokens + evidence_map and composite tokens + provenance
