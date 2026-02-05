## Worked example (minimal, hypothetical)

This example is invented. It shows structure, not real scraped data.

### Inputs

```json
{
  "urls": ["https://example-a.com", "https://example-b.com"],
  "blend_mode": "harmonise",
  "output_style": "standard"
}
```

### Per-site extracted_signals (snippets)

```json
{
  "per_site": [
    {
      "site_id": "site_a",
      "root_url": "https://example-a.com",
      "extracted_signals": {
        "colours": {
          "primary": {"hex": "#0B5FFF", "confidence": 0.85},
          "secondary": {"hex": "#111827", "confidence": 0.72},
          "accent": {"hex": "#22C55E", "confidence": 0.66},
          "background": {"hex": "#FFFFFF", "confidence": 0.9},
          "text": {"hex": "#0F172A", "confidence": 0.8}
        },
        "typography": {"body_font": "Inter", "heading_font": "Inter", "notes": ["tight H1", "8px spacing rhythm"]},
        "voice": {"traits": ["direct", "optimistic", "product-led"], "cta_style": ["Start free", "See pricing"]}
      },
      "evidence_map": {
        "colours.primary": [{"source_url": "https://example-a.com", "selector": ".btn-primary", "excerpt": "Start free"}]
      }
    },
    {
      "site_id": "site_b",
      "root_url": "https://example-b.com",
      "extracted_signals": {
        "colours": {
          "primary": {"hex": "#111827", "confidence": 0.8},
          "secondary": {"hex": "#F59E0B", "confidence": 0.7},
          "accent": {"hex": "#EC4899", "confidence": 0.62},
          "background": {"hex": "#0B0F19", "confidence": 0.75},
          "text": {"hex": "#F8FAFC", "confidence": 0.78}
        },
        "typography": {"body_font": "Söhne (or similar grotesk)", "heading_font": "Söhne", "notes": ["airy spacing", "high contrast dark mode"]},
        "voice": {"traits": ["premium", "editorial", "confident"], "cta_style": ["Request a demo"]}
      },
      "evidence_map": {
        "voice.traits": [{"source_url": "https://example-b.com/about", "excerpt": "Built for teams who care about craft"}]
      }
    }
  ]
}
```

### Per-site prompt_pack (snippets)

```json
{
  "per_site_prompt_packs": [
    {
      "site_id": "site_a",
      "prompt_pack": {
        "brand_style_prompt": "Product-led, direct, optimistic. Use clean layouts and a bright primary blue. Evidence: [site_a:home:colours.primary].",
        "visual_direction_prompt": "Bright, modern SaaS photography, natural light, minimal backgrounds...",
        "ui_direction_prompt": "Landing page with clear H1, strong primary CTA, 8px spacing rhythm...",
        "copywriting_prompt": "Short sentences, action verbs, minimal jargon...",
        "negative_prompt": "Avoid overly formal tone, avoid heavy gradients...",
        "token_set": {"colour": ["primary blue", "white background"], "voice": ["direct", "optimistic"]}
      }
    }
  ]
}
```

### Blended composite snippet (harmonise)

```json
{
  "composite_tokens": {
    "tokens": {
      "colours": {"primary": "#0B5FFF", "accent": "#F59E0B", "background": "#FFFFFF", "text": "#0F172A"},
      "typography": {"body": "Inter (or similar modern sans)", "headings": "Inter", "notes": ["retain editorial confidence via copy, not type conflicts"]},
      "voice": {"traits": ["direct", "confident", "craft-aware"], "cta_style": ["Start free", "Request a demo (enterprise)"]}
    },
    "provenance": [
      {"signal": "colours.primary", "from": "site_a", "weight": 0.5, "evidence": ["[site_a:home:colours.primary]"]},
      {"signal": "colours.accent", "from": "site_b", "weight": 0.5, "evidence": ["[site_b:pricing:colours.secondary]"]}
    ]
  }
}
```
