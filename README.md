# Engineering Case Studies Hub

A curated collection of Tabitha Khadse's software engineering work, focusing on frontend development, developer tooling, healthcare workflows, AI experiments, accessibility and practical automation.

**Live site:** https://tabitha-dev.github.io/Engineering-Case-Studies-Hub/  
**Primary portfolio:** https://code.tabitha.dev/  
**Accessible, machine-readable overview:** https://tabitha-dev.github.io/Engineering-Case-Studies-Hub/portfolio.md

## What this project demonstrates

The case-study interface has searchable categories, a responsive layout, light/dark themes, and detailed project dialogs. The project cards distinguish live websites and released tools from simulated healthcare demos and experimental AI-assisted workflows.

## SEO and AI-search foundations

- Canonical page URL; meta description; Open Graph and Twitter card metadata
- Structured data: `CollectionPage`, `WebSite`, `Person`, `BreadcrumbList`, and `ItemList` of project summaries
- Static HTML summaries available without JavaScript, supporting crawlers and no-script visitors
- `sitemap.xml`, `llms.txt`, and the full `portfolio.md` text overview
- Exact TK monogram artwork shared with the primary portfolio; local SVG favicon
- `.nojekyll` keeps Markdown files and other static assets available at their actual URLs

AEO is a content and retrieval discipline, not a guaranteed ranking or inclusion in AI-generated answers. The structured descriptions avoid asserting unsupported production, compliance or performance claims.

## Accessibility considerations

The hub includes a skip link, semantic main region, descriptive page headings, keyboard-operable case cards, labeled search/filter controls, live filter-result status, descriptive dialog metadata, Escape-key closing, dialog focus containment, focus restoration and reduced-motion CSS. The cards remain visible and linked in an HTML fallback without JavaScript.

**Verification status:** These source checks are not a WCAG conformance certification. Run a full browser, zoom, color-contrast, keyboard and screen-reader audit before claiming WCAG 2.2 AA compliance.

## Source checks

Requires Python 3.11+; no third-party dependencies:

```sh
python scripts/check_site.py
```

GitHub Actions runs the same checks on source changes and pull requests through `.github/workflows/site-checks.yml`.

## Build and performance note

The existing interface uses browser-side Babel and Tailwind CDN styling. A future production-build migration could compile and minify these assets, reducing runtime work and improving dependability; this change has not been performed yet.

## Project context and verification

Medical and billing examples are educational or synthetic-data demonstrations, not operational patient systems or independent regulatory certifications. The ShipLab experiment distinguishes independent CI success from unverified native recorded QA. Refer to the main portfolio and individual public project sources for current details.

Contact: [Portfolio](https://code.tabitha.dev/) · [LinkedIn](https://www.linkedin.com/in/tabitha-dev/) · [GitHub](https://github.com/tabitha-dev) · [Book a call](https://code.tabitha.dev/code/Schedule-a-Meeting/)

Last content and SEO review: November 10, 2026.
