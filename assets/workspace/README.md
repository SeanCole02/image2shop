# Workspace

This workspace is split into:

- `specs/` for process, page specs, and design tokens
- `design-assets/` for raw and reference design files
- `theme/` for deployable Shopify Liquid output

Shared storefront structure belongs in `specs/theme-system.md`.
Persistent shared memory belongs in `THEME_MEMORY.md`.

After initialization:

- put shared colors, typography, spacing, and related tokens in `specs/tokens/theme-tokens.json`
- if you have a brand-guidelines PDF, put it in `design-assets/raw/` and extract tokens from it first
- use a lowercase hyphenated page slug like `homepage` or `product-detail`
- put page mockups in `design-assets/mockups/<page-slug>/desktop/` and `design-assets/mockups/<page-slug>/mobile/`
- put the page's user goal, primary CTA, UX success criteria, and final UX review in `specs/pages/<page-slug>.md`
- record whether the page uses the shared header/navigation and footer, or intentionally excludes them, in `specs/pages/<page-slug>.md`
- record cross-page structure in `specs/theme-system.md`
- record reusable component decisions in `THEME_MEMORY.md`
- review generated pages against their primary user task and CTA, not only against the source mockup
- keep copy concise and avoid unnecessary cards, wrappers, and container nesting

Rules:

- do not place planning docs in `theme/`
- do not place deployable theme code in `specs/`
- do not place raw source mockups directly in `theme/assets/`
