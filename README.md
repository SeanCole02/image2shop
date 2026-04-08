# Image2Shop

Image2Shop is an open-source Codex skill for turning Framer pages, screenshots, and storefront mockups into a coherent Shopify Liquid theme workflow.

Use it when you want to:

- turn page mockups into Shopify theme work
- keep pages connected inside one theme system
- identify reusable components early
- preserve shared decisions across pages

## Installation

Install this skill through Codex with `$skill-installer`.

Example:

- `Use $skill-installer to install the skill from https://github.com/SeanCole02/image2shop.`

After installation, restart Codex so the new skill is discovered.

## Updating

For non-technical users, the best update path is to ask Codex to use `$image2shop` to update the installed skill in place.

Ask Codex:

- `Use $image2shop to update the installed skill to the latest version and tell me when to restart Codex.`

Why this flow:

- it avoids manual filesystem work
- it avoids uninstalling the existing skill first
- it keeps the update flow inside the skill itself

If you want to run the updater directly:

```bash
python scripts/update_installed_skill.py
```

After the update, restart Codex.

## Use With Codex

The normal way to use this repo is to ask Codex to use `$image2shop`.

Examples:

- `Use $image2shop to initialize a Shopify theme workspace in <target-dir>.`
- `Use $image2shop to initialize a workspace in <target-dir> and scaffold the page slug homepage.`
- `Use $image2shop to review these Framer mockups, update specs/theme-system.md and THEME_MEMORY.md, and scaffold the next page.`

## First Workflow

1. Make the skill available to Codex.
2. Restart Codex if you just installed the skill.
3. Ask Codex to use `$image2shop` to initialize your workspace.
4. Add your Framer exports or screenshots to:
   - `design-assets/mockups/<page-slug>/desktop/`
   - `design-assets/mockups/<page-slug>/mobile/`
5. Ask Codex to update:
   - `specs/theme-system.md`
   - `THEME_MEMORY.md`
   - `specs/pages/<page-slug>.md`
6. Ask Codex to map the design into Shopify templates, sections, snippets, and settings.
7. Ask Codex to implement the approved output under `theme/`.

## After Initialization

After the workspace is created, the next inputs should go here:

- shared colors and design tokens:
  put them in `specs/tokens/theme-tokens.json`
  because they should stay consistent across the whole theme
- page slug:
  use a lowercase hyphenated name like `homepage` or `product-detail`
  because the slug names the page spec and the mockup folders
- desktop and mobile mockups:
  put them in `design-assets/mockups/<page-slug>/desktop/` and `design-assets/mockups/<page-slug>/mobile/`
  because the page spec and implementation should point to those exact files
- shared storefront structure:
  put it in `specs/theme-system.md`
  because navigation, footer, routes, and template families should be decided across pages
- reusable component decisions:
  put them in `THEME_MEMORY.md`
  because repeated cards, snippets, and layouts should be tracked before pages drift apart

## What Codex Creates

The scaffolded workspace has three main areas:

- `specs/` for theme planning, page specs, and tokens
- `design-assets/` for raw and reference design files
- `theme/` for deployable Shopify Liquid output

It also creates:

- `specs/theme-system.md` for shared storefront structure
- `THEME_MEMORY.md` for shared decisions and reusable components

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

## Manual Fallback

If you want to initialize a workspace directly instead of asking Codex, use:

```bash
python scripts/scaffold_workspace.py <target-dir>
```

To scaffold the first page at the same time:

```bash
python scripts/scaffold_workspace.py <target-dir> --page-slug homepage
```

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
