# Repo Structure

Use this three-way split for Framer-to-Shopify workspaces:

- `specs/` for process docs, page specs, and design tokens
- `design-assets/` for raw, mockup, and intermediate design files
- `theme/` for deployable Shopify Liquid output

Recommended layout:

- `THEME_MEMORY.md`
- `specs/theme-system.md`
- `specs/pages/<page-slug>.md`
- `specs/process/`
- `specs/templates/`
- `specs/tokens/theme-tokens.json`
- `design-assets/raw/`
- `design-assets/mockups/<page-slug>/desktop/`
- `design-assets/mockups/<page-slug>/mobile/`
- `design-assets/mockups/<page-slug>/notes.md`
- `design-assets/processed/`
- `theme/layout/`
- `theme/templates/`
- `theme/sections/`
- `theme/snippets/`
- `theme/assets/`
- `theme/config/`
- `theme/locales/`

Rules:

- Do not place planning documents into `theme/`.
- Do not place deployable Shopify code into `specs/`.
- Do not place raw Framer exports directly into `theme/assets/`.
- Use `specs/tokens/theme-tokens.json` as the token source of truth.
- Use `specs/theme-system.md` as the shared source of truth for cross-page structure.
- Use `THEME_MEMORY.md` to persist reusable-component decisions and shared implementation memory.
