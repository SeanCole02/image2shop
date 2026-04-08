---
name: image2shop
description: Turn Framer pages, screenshots, and static storefront mockups into a structured Shopify Liquid workflow and implementation plan. Use when Codex needs to scaffold a Framer-to-Shopify workspace, organize specs/design-assets/theme folders, create page intake files and mockup paths, extract design tokens, ask clarifying questions for ambiguous UI behavior, or rebuild a design into Shopify templates, sections, snippets, and theme settings.
---

# Image2Shop

## Overview

Convert image-based storefront designs into maintainable Shopify Liquid workspaces and implementation plans.
Treat Framer files and exported mockups as design inputs, not deployable code.

## Core Rules

- Ask clarifying questions whenever anything is even mildly ambiguous.
- Pair each clarification question with one or two suggested implementation paths.
- Keep `specs/`, `design-assets/`, and `theme/` separate.
- Define shared theme structure before treating pages as isolated conversions.
- Identify likely reusable components as soon as they appear in a design.
- Record shared decisions and reusable-component status in `THEME_MEMORY.md`.
- Promote candidates once they meet the shared-component rules in `THEME_MEMORY.md`.
- Keep raw or reference mockups out of `theme/assets/` until they are intentionally prepared as production assets.
- Do not begin theme implementation for a page until its intake file, mockup references, and unresolved questions are recorded.
- After workspace initialization, tell the user exactly where to put colors, page slugs, and mockups, and explain why each location exists.
- If the user has a brand-guidelines PDF, tell them to place it in `design-assets/raw/` and extract tokens from it before page styling begins.
- Let the extractor add extra brand-specific token fields when the brand document defines roles beyond the base token schema.
- Review generated themes for human-focused UX based on the page's actual job, not only visual parity.
- Check that hierarchy, CTA placement, scannability, trust cues, and interaction friction support the page's feature and user intent.
- Run `python scripts/validate_page_spec.py specs/pages/<page-slug>.md --stage pre-implement` before implementation starts.
- Run `python scripts/validate_page_spec.py specs/pages/<page-slug>.md --stage pre-complete` before treating a page as complete.

## Quick Start

- Run `python scripts/scaffold_workspace.py <target-dir>` to scaffold or normalize a workspace.
- Run `python scripts/extract_brand_guidelines.py <source> --tokens <theme-tokens-path>` when the user provides a brand-guidelines PDF or text document.
- Run `python scripts/validate_page_spec.py specs/pages/<page-slug>.md --stage <pre-implement|pre-complete>` to enforce intake and UX-review gates.
- Run `python scripts/update_installed_skill.py` when the user asks to update the installed skill.
- Add `--page-slug <slug>` to scaffold a page at the same time.
- Read `references/repo-structure.md` for folder conventions.
- Read `references/theme-system.md` for shared theme planning.
- Read `references/theme-memory.md` for persistent theme-memory usage.
- Read `references/intake-workflow.md` for the page handoff process.
- Read `references/framer-to-shopify.md` for the design-to-theme mapping rules.

## Workflow

1. Create or verify the workspace structure.
2. Define the shared theme system in `specs/theme-system.md`.
3. Initialize or update `THEME_MEMORY.md`.
4. Tell the user where to put shared colors in `specs/tokens/theme-tokens.json`.
5. If available, extract brand-guidelines data into the token file before styling pages.
6. Let the extractor populate `colors_additional` and `typography_additional` when the brand document defines named roles outside the default token schema.
7. Tell the user how to choose a page slug and where its mockups should go.
8. Create the page spec and mockup folders.
9. Ask questions and record unknowns before implementation.
10. Mark likely reusable sections, snippets, cards, and patterns immediately.
11. Lock design tokens only when the design values are clear.
12. Map design regions into templates, sections, blocks, snippets, settings, and app blocks.
13. Run `python scripts/validate_page_spec.py specs/pages/<page-slug>.md --stage pre-implement`.
14. Link the page back to shared navigation, footer, templates, and reusable section inventory.
15. Implement the approved output in `theme/`.
16. Review visual parity, responsive behavior, merchant editability, and whether the UI/UX serves the page's primary human goal.
17. Record `UX review notes` and `UX review result` in the page spec, using `pass`, `needs-rework`, or `fail` for the result.
18. Run `python scripts/validate_page_spec.py specs/pages/<page-slug>.md --stage pre-complete`.

## Bundled Resources

- Use `scripts/scaffold_workspace.py` for deterministic workspace setup.
- Use `scripts/extract_brand_guidelines.py` to merge brand-guidelines data into theme tokens.
- Use `scripts/validate_page_spec.py` to enforce page-spec and UX-review gates.
- Use `scripts/update_installed_skill.py` to update an installed copy in place.
- Use `assets/workspace/` for scaffolded repo files.
- Use `assets/templates/theme-system-template.md` for the shared theme plan.
- Use `assets/templates/theme-memory-template.md` for persistent theme memory.
- Use `assets/templates/page-intake-template.md` for a page spec.
- Use `assets/templates/theme-tokens.json` for starting tokens.

## Reference Files

- `references/repo-structure.md`
- `references/brand-guidelines.md`
- `references/theme-system.md`
- `references/theme-memory.md`
- `references/intake-workflow.md`
- `references/framer-to-shopify.md`
