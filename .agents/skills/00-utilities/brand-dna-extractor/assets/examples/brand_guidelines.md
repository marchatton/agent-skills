# Overview

- Analysed 2 sites (example.com, example.org) using hybrid scraping + browser probing on 5 pages/site.
- Intended use: produce a cohesive landing page + lightweight product UI direction.
- Limits: computed styles sampled for key elements only; no logged-in app UI analysed.

# Composite Brand DNA

## Personality
- Direct, confident, slightly warm (CTA verbs are active; copy avoids hype). [composite:voice.core]
- Modern, utilitarian polish (clean layouts, restrained decoration). [composite:ui.posture]

## Visual stance
- Airy, high-contrast, minimal chrome, emphasis on readable hierarchy. [composite:layout.stance]

## Experience stance
- Interaction feels crisp not bouncy (short transitions, subtle hover). [composite:motion.posture]

# Composite Design Tokens

## Colour
- Primary: #3B82F6
- Accent: #A855F7
- Background: #FFFFFF
- Text: #0F172A
- Dark theme: background #0B1220, text #E5E7EB (best-effort). [composite:colour.dark]

## Typography
- Body: modern sans (Inter-like), 16px baseline, 1.5 line-height. [composite:type.body]
- Headings: same family with heavier weights and tighter tracking. [composite:type.headings]

## Spacing and layout
- Spacing step: 8px (inferred from common paddings and section gaps). [composite:spacing.step]
- Sections: consistent vertical rhythm, generous top/bottom padding. [composite:layout.rhythm]

## Shape, borders, shadows
- Radius: medium (8–12px) on CTAs and cards. [composite:radius.scale]
- Shadows: subtle single-layer elevation, often off by default. [composite:elevation]

## Motion and interaction
- Hover: colour shift + subtle shadow, 150–250ms ease. [composite:motion.hover]
- Focus: visible focus ring, not removed. [composite:motion.focus]

# Composite Voice & Copy

## Tone traits
- Benefit-led, short sentences, low fluff. [composite:voice.traits]
- Avoids “revolutionary” language, prefers concrete outcomes. [composite:voice.traits]

## Do and don't
- Do: use active verbs, make the outcome explicit.
- Don't: stack buzzwords, overpromise, use excessive exclamation marks.

## Microcopy patterns
- CTA verbs: “Get started”, “Try”, “See pricing”, “Book a demo”. [composite:voice.cta]

# Composite Prompt Pack

## Brand style prompt
Write in a direct, calm, modern voice. Keep sentences short and outcome-driven. Prefer concrete benefits over hype. Use crisp headings, clean hierarchy, and minimal ornamentation.

## Visual direction prompt
Minimal, modern UI with high-contrast typography, airy spacing, restrained colour accents, and subtle depth. Prefer clean shapes and readable layouts.

## UI direction prompt
Build a responsive landing page with a strong hero, clear CTA buttons, and card-based feature sections. Use 8px spacing rhythm, medium radius, subtle shadow elevation, and consistent focus rings.

## Copywriting prompt
Use benefit-led, plain English microcopy. Prefer action verbs for CTAs. Keep error/help text calm and specific. Avoid marketing clichés.

## Negative prompt
Avoid loud gradients, overly playful illustration styles, heavy glassmorphism, or long hype paragraphs.

## Token set
- Colour: primary blue for CTAs, purple accent for highlights, neutral white/ink base.
- Type: modern sans, 16px body baseline, bold but not oversized headings.
- Layout: airy sections, clear hierarchy, consistent padding cadence.
- Imagery: product-forward, clean screenshots, minimal clutter.
- Voice: direct, outcome-first, calm confidence.
- Motion: subtle hover shifts, short easing, visible focus rings.

# Provenance Map

- Weights: equal (0.5 / 0.5)
- Primary colour: example.com (CTA background) + confirmed via computed styles
- Accent: example.org (badge / highlight colour)
- Type posture: both sites converge on modern sans + clean hierarchy
- Motion: both show short transitions on interactive elements

# Conflicts & Resolutions

- Conflict: different accent colours across sources
  - Resolution: constrain to one accent used sparingly, keep neutrals consistent

# Per-site Appendices

## example.com

### Brand DNA (site)
- Clean SaaS posture, crisp CTAs, minimal decoration.

### Evidence highlights
- CTA background, hover diff, body text colour, heading scale.

### Per-site limitations
- No design system page found; app UI not accessible.

## example.org

### Brand DNA (site)
- Slightly more playful accent usage, similar layout rhythm.

### Evidence highlights
- Accent tokens, card radius, focus ring behaviour.

### Per-site limitations
- Dark mode tokens not explicitly declared, inferred via media probe only.

# Limitations

## Global limitations
- Only sampled key elements for computed styles, not every component.
- Cross-origin stylesheet parsing may be incomplete; stored URLs for follow-up parsing.
- Motion inferred from CSS primitives, not full behavioural tracing.

## Per-site limitations
- See per-site appendices.
