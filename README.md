# Image2Shop

Image2Shop is an open-source Codex skill for turning Framer pages, screenshots, and storefront mockups into a coherent Shopify Liquid theme workflow.

Use it when you want to:

- turn page mockups into Shopify theme work
- keep pages connected inside one theme system
- identify reusable components early
- preserve shared decisions across pages

## Get Started

1. Clone this repo.
2. Pick or create a target workspace for your Shopify theme work.
3. Scaffold the workspace:

```bash
python scripts/scaffold_workspace.py <target-dir>
```

4. If you already know your first page slug, scaffold that too:

```bash
python scripts/scaffold_workspace.py <target-dir> --page-slug homepage
```

5. Put your Framer exports or screenshots into:
   - `design-assets/mockups/<page-slug>/desktop/`
   - `design-assets/mockups/<page-slug>/mobile/`
6. Define the shared storefront in `specs/theme-system.md`.
7. Record reusable component decisions in `THEME_MEMORY.md`.
8. Fill out `specs/pages/<page-slug>.md`.
9. Build the approved Shopify output under `theme/`.

## What Gets Generated

The scaffolded workspace has three main areas:

- `specs/` for theme planning, page specs, and tokens
- `design-assets/` for raw and reference design files
- `theme/` for deployable Shopify Liquid output

It also creates:

- `specs/theme-system.md` for shared storefront structure
- `THEME_MEMORY.md` for reusable-component memory

## Typical Workflow

1. Define navigation, footer, routes, template families, and shared sections in `specs/theme-system.md`.
2. Add reusable component candidates to `THEME_MEMORY.md`.
3. Create or update the page spec for the current page.
4. Ask clarifying questions before implementation if anything is ambiguous.
5. Promote components when they are clearly global or reused across pages.
6. Implement the resulting Liquid sections, snippets, templates, and settings.

## Reusable Component Rules

`THEME_MEMORY.md` tracks:

- approved shared sections
- approved shared snippets
- section candidates
- snippet candidates
- card candidates
- layout-pattern candidates

Promote a candidate:

- immediately if it is clearly global
- after reuse on 2 or more pages with materially matching structure and behavior

Keep it as a candidate if reuse is likely but scope or behavior is still unclear.

## Repository Layout

- `SKILL.md` is the root skill definition
- `agents/openai.yaml` contains skill UI metadata
- `references/` contains workflow guidance
- `scripts/scaffold_workspace.py` scaffolds a working repo
- `assets/templates/` contains reusable templates
- `assets/workspace/` contains starter workspace files

## License

This repository is licensed under `GPL-3.0-or-later`.

See [LICENSE](./LICENSE) and [NOTICE](./NOTICE).
