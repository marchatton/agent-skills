/**
 * probe_css.js
 *
 * Run inside the page context via agent-browser eval.
 * Returns a JSON object containing:
 * - stylesheet inventory
 * - best-effort CSS variables
 * - computed style snapshots for key elements
 *
 * Notes:
 * - Accessing document.styleSheets[i].cssRules can throw for cross-origin CSS.
 * - Always return stylesheet URLs so a server-side fetch/parser can complete coverage.
 */

(() => {
  const STYLE_PROPS = [
    "color",
    "background-color",
    "border-color",
    "border-radius",
    "box-shadow",
    "font-family",
    "font-size",
    "font-weight",
    "line-height",
    "letter-spacing",
    "text-transform",
    "padding",
    "margin",
    "outline-color",
    "outline-style",
    "outline-width",
    "transition-property",
    "transition-duration",
    "transition-timing-function",
    "animation-name",
    "animation-duration",
    "animation-timing-function"
  ];

  const isVisible = (el) => {
    if (!el) return false;
    const cs = getComputedStyle(el);
    return cs.display !== "none" && cs.visibility !== "hidden" && cs.opacity !== "0";
  };

  const textOf = (el) => (el?.textContent || "").trim();

  const tagPrimaryCta = () => {
    const candidates = Array.from(document.querySelectorAll("a, button"))
      .filter(isVisible)
      .filter((el) => textOf(el).length > 0);

    const byCtaText =
      candidates.find((el) =>
        /(get started|sign up|start|book a demo|request a demo|try|pricing)/i.test(textOf(el))
      ) || candidates[0];

    if (byCtaText) byCtaText.setAttribute("data-brandprobe", "primary-cta");
    return byCtaText || null;
  };

  const pick = {
    body: () => document.body,
    h1: () => document.querySelector("h1"),
    link: () => document.querySelector("a[href]"),
    input: () => document.querySelector("input, textarea, select"),
    primaryCta: () => document.querySelector('[data-brandprobe="primary-cta"]')
  };

  const styleSnapshot = (el) => {
    if (!el) return null;
    const cs = getComputedStyle(el);
    const out = {};
    for (const p of STYLE_PROPS) out[p] = cs.getPropertyValue(p).trim();
    return out;
  };

  // Tag CTA for stable hover/focus probing.
  tagPrimaryCta();

  // Stylesheet inventory.
  const stylesheets = Array.from(document.querySelectorAll('link[rel="stylesheet"]'))
    .map((l) => l.href)
    .filter(Boolean);

  const inlineCss = Array.from(document.querySelectorAll("style"))
    .map((s) => s.textContent || "")
    .filter(Boolean);

  // Best-effort CSS custom properties from readable CSSRules.
  const vars = {};
  for (const ss of Array.from(document.styleSheets)) {
    let rules;
    try {
      rules = ss.cssRules;
    } catch {
      continue;
    }
    for (const r of Array.from(rules)) {
      if (!r || !r.style) continue;
      for (const name of Array.from(r.style)) {
        if (!name.startsWith("--")) continue;
        const value = r.style.getPropertyValue(name).trim();
        (vars[name] ||= new Set()).add(value);
      }
    }
  }
  const cssVariables = Object.fromEntries(
    Object.entries(vars).map(([k, set]) => [k, Array.from(set)])
  );

  return {
    url: location.href,
    title: document.title,
    stylesheets,
    inlineCss_char_counts: inlineCss.map((s) => s.length),
    cssVariables_count: Object.keys(cssVariables).length,
    cssVariables_sample: Object.fromEntries(Object.entries(cssVariables).slice(0, 50)),
    computed: {
      body: styleSnapshot(pick.body()),
      h1: styleSnapshot(pick.h1()),
      link: styleSnapshot(pick.link()),
      primary_cta: styleSnapshot(pick.primaryCta()),
      input: styleSnapshot(pick.input())
    }
  };
})();
