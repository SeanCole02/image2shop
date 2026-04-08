# AGENTS.md

## Purpose

This repository converts Framer designs into production-ready Shopify Liquid theme code.

The default output should favor:

- visual parity with the Framer source
- clean Shopify theme architecture
- reusable sections and blocks over one-off page code
- merchant-editable settings where practical

## Operating Rules

Agents working in this repository must follow these rules:

- Ask clarifying questions whenever any requirement is even mildly ambiguous.
- Do not guess on content hierarchy, responsive behavior, animation intent, collection behavior, or product-card behavior when the design does not make it explicit.
- Provide suggestions alongside questions so the user can choose a direction quickly.
- Prefer rebuilding the design as native Shopify sections, blocks, snippets, and theme settings rather than shipping static HTML.
- Treat Framer as the design source, not the runtime target.
- Preserve Shopify compatibility with standard storefront apps unless the user explicitly asks for a headless approach.
- Keep output editable in the Shopify theme editor whenever possible.
- Keep the theme coherent across pages instead of treating each page as an isolated conversion.
- Mark reusable component candidates immediately and update `THEME_MEMORY.md`.
- Promote candidates once they are clearly global or reused across multiple pages.
- After creating the workspace, tell the user in plain language where to put shared colors, page slugs, and mockups, and explain why each belongs there.

## Design-to-Code Workflow

Agents should use this sequence unless the user asks otherwise:

1. intake the Framer design and supporting notes
2. define or update the shared theme system in `specs/theme-system.md`
3. create or update `THEME_MEMORY.md`
4. create or update a page intake file under `specs/pages/`
5. attach or reference page mockups under `design-assets/mockups/<page-slug>/`
6. ask clarification questions
7. map the design into Shopify page types and components
8. define reusable sections, snippets, and settings
9. mark reusable candidates and approved shared components in `THEME_MEMORY.md`
10. map visual tokens from the design into `specs/tokens/theme-tokens.json`
11. connect the page to shared navigation, footer, templates, and reusable components
12. implement Liquid, schema, CSS, and assets
13. verify responsive behavior and editor ergonomics
14. summarize open gaps and recommended next steps

Implementation should not begin for a page until:

- `THEME_MEMORY.md` exists
- `specs/theme-system.md` exists
- `specs/pages/<page-slug>.md` exists
- the relevant mockups exist under `design-assets/mockups/<page-slug>/`
- unresolved questions have been recorded
- any high-risk ambiguities have been asked back to the user

## Repository Conventions

- `specs/` stores process documents, intake notes, reference material, and design tokens.
- `design-assets/` stores raw and intermediate design-source files that are not yet production theme assets.
- `theme/` stores the actual Shopify theme output.
