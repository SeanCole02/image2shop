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

## Quick Start

- Run `python scripts/scaffold_workspace.py <target-dir>` to scaffold or normalize a workspace.
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
4. Create the page spec and mockup folders.
5. Ask questions and record unknowns before implementation.
6. Mark likely reusable sections, snippets, cards, and patterns immediately.
7. Lock design tokens only when the design values are clear.
8. Map design regions into templates, sections, blocks, snippets, settings, and app blocks.
9. Link the page back to shared navigation, footer, templates, and reusable section inventory.
10. Implement the approved output in `theme/`.
11. Review visual parity, responsive behavior, and merchant editability.

## Bundled Resources

- Use `scripts/scaffold_workspace.py` for deterministic workspace setup.
- Use `assets/workspace/` for scaffolded repo files.
- Use `assets/templates/theme-system-template.md` for the shared theme plan.
- Use `assets/templates/theme-memory-template.md` for persistent theme memory.
- Use `assets/templates/page-intake-template.md` for a page spec.
- Use `assets/templates/theme-tokens.json` for starting tokens.

## Reference Files

- `references/repo-structure.md`
- `references/theme-system.md`
- `references/theme-memory.md`
- `references/intake-workflow.md`
- `references/framer-to-shopify.md`
