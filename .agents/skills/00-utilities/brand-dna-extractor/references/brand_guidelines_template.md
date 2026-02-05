# Overview

- Run summary:
  - Sites analysed: {{site_count}}
  - Pages visited: {{pages_visited_total}}
  - Blend mode: {{blend_mode}}
  - Output style: {{output_style}}
- High-level direction (3–6 bullets):
  - {{composite_summary_bullets}}

# Composite Brand DNA

## Visual

### Colours
- Primary: {{primary_hex}} (usage: {{primary_usage}})
- Secondary: {{secondary_hex}} (usage: {{secondary_usage}})
- Accent: {{accent_hex}} (usage: {{accent_usage}})
- Background: {{background_hex}}
- Text: {{text_hex}}
- Notes:
  - {{colour_notes}}

### Typography
- Body: {{body_font}}
- Headings: {{heading_font}}
- Weights: {{weights_summary}}
- Scale and hierarchy:
  - {{type_hierarchy_notes}}

### Imagery
- Medium: {{imagery_medium}}
- Treatment:
  - {{imagery_treatment_bullets}}

### Iconography
- Style: {{icon_style_summary}}

### Motion / Interaction
- Style: {{motion_style_summary}}
- Notes:
  - {{motion_notes}}

## UI and Components

- Density: {{ui_density}}
- Corner radius: {{radius_notes}}
- Elevation: {{elevation_notes}}
- Components (top patterns):
  - {{component_inventory_bullets}}

## Voice & Personality

### Voice traits
- {{voice_traits_bullets}}

### Microcopy patterns
- {{microcopy_patterns_bullets}}

### Do / Don’t
**Do**
- {{do_bullets}}

**Don’t**
- {{dont_bullets}}

# Composite Design Tokens

Provide design tokens in human-readable form (these must match `design_tokens.json`):

- Spacing scale: {{spacing_scale}}
- Radius scale: {{radius_scale}}
- Shadow tokens: {{shadow_tokens}}
- Border tokens: {{border_tokens}}
- Grid/layout rhythm: {{layout_rhythm}}

# Composite Voice & Copy

- Summary:
  - {{copy_summary}}
- Example rewrites (paraphrased, not lifted):
  - {{rewrite_examples}}

# Composite Prompt Pack

## Brand style prompt
{{composite_prompt_pack.brand_style_prompt}}

## Visual direction prompt
{{composite_prompt_pack.visual_direction_prompt}}

## UI direction prompt
{{composite_prompt_pack.ui_direction_prompt}}

## Copywriting prompt
{{composite_prompt_pack.copywriting_prompt}}

## Negative prompt / Avoid
{{composite_prompt_pack.negative_prompt}}

## Token set
{{composite_prompt_pack.token_set}}

# Provenance Map

Explain “what came from where”, including weights and evidence anchors:

- {{provenance_bullets}}

# Conflicts & Resolutions

## Conflicts
- {{conflicts_bullets}}

## Resolutions
- {{resolutions_bullets}}

# Per-site Appendices

For each site, include:
- Site summary + confidence overview
- Per-site Brand DNA (condensed)
- Per-site prompt pack (optional summary, avoid dumping long prompts if output_style=concise)
- Limitations

{{per_site_appendices}}

# Limitations

- Global limitations:
  - {{global_limitations_bullets}}
- Per-site limitations:
  - {{per_site_limitations_bullets}}
