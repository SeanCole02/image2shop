# Intake Workflow

Use this workflow for each page before implementation.

Before using it, make sure `specs/theme-system.md` exists and defines the shared storefront structure.
Make sure `THEME_MEMORY.md` exists and captures current reusable-component decisions.

Required inputs:

- a page slug
- a page spec at `specs/pages/<page-slug>.md`
- desktop and mobile mockups under `design-assets/mockups/<page-slug>/`
- a Framer link or equivalent source reference
- known app constraints

Steps:

1. Define the page slug.
2. Create `design-assets/mockups/<page-slug>/desktop/` and `design-assets/mockups/<page-slug>/mobile/`.
3. Add Framer screenshots or exported page images to those folders.
4. Create `specs/pages/<page-slug>.md` from the intake template.
5. Link the exact mockup paths in the page spec.
6. Record unknowns and ask clarifying questions before implementation.
7. Mark likely reusable components and add them to `THEME_MEMORY.md`.
8. Link the page to shared navigation, footer, templates, and reusable sections from `specs/theme-system.md`.
9. Record `Header/navigation decision` and `Footer decision` as `shared` or `intentional-exception`.
10. Decide what is static, merchant-editable, or Shopify-data-driven.
11. Record the page's primary user task, primary CTA, and what a successful UX should feel like for that page.
12. Run `python scripts/validate_page_spec.py specs/pages/<page-slug>.md --stage pre-implement`.
13. Only then begin implementation in `theme/`.

Minimum completion standard:

- page purpose
- primary user task and CTA
- UX success criteria for that page
- header/navigation and footer decisions
- Shopify page type
- desktop and mobile references
- editable versus fixed content decisions
- data source decisions
- app constraints
- known unknowns
- suggested implementation path

Completion gate:

- fill in `UX review notes`
- fill in `Copy discipline review`
- fill in `Layout discipline review`
- fill in `UX review result`
- run `python scripts/validate_page_spec.py specs/pages/<page-slug>.md --stage pre-complete`
