# Image2Shop

Image2Shop is an open-source Codex skill for turning Framer pages, screenshots, and storefront mockups into a coherent Shopify Liquid theme workflow.

Use it when you want to:

- turn page mockups into Shopify theme work
- keep pages connected inside one theme system
- identify reusable components early
- preserve shared decisions across pages
- review generated pages against human goals, not only design fidelity

## Installation

Install this skill through Codex with `$skill-installer`.

Example:

- `Use $skill-installer to install the skill from https://github.com/SeanCole02/image2shop.`

After installation, restart Codex so the new skill is discovered.

## Updating

For non-technical users, the best update path is to ask Codex to use `$image2shop` to update the installed skill in place.

Ask Codex:

- `Use $image2shop to update the installed skill to the latest version and tell me when to restart Codex.`

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
4. If you have a brand-guidelines PDF, put it in `design-assets/raw/` and ask Codex to extract shared tokens from it.
5. Add your Framer exports or screenshots to:
   - `design-assets/mockups/<page-slug>/desktop/`
   - `design-assets/mockups/<page-slug>/mobile/`
6. Ask Codex to update:
   - `specs/theme-system.md`
   - `THEME_MEMORY.md`
   - `specs/pages/<page-slug>.md`
7. Ask Codex to map the design into Shopify templates, sections, snippets, and settings.
8. Ask Codex to implement the approved output under `theme/`.
9. Ask Codex to review the generated page for human-focused UX based on that page's purpose, CTA, and user task.

## After Initialization

After the workspace is created, the next inputs should go here:

- shared colors and design tokens:
  put them in `specs/tokens/theme-tokens.json`
  because they should stay consistent across the whole theme
- extra brand-specific color or type roles discovered from guidelines:
  let Codex add them in `specs/tokens/theme-tokens.json` under `colors_additional` and `typography_additional`
  because those values often exist in a brand document even when the base token schema does not include them yet
- page slug:
  use a lowercase hyphenated name like `homepage` or `product-detail`
  because the slug names the page spec and the mockup folders
- page goal and UX review fields:
  put the page's primary user task, primary CTA, UX success criteria, `Header/navigation decision`, `Footer decision`, `UX review notes`, `Copy discipline review`, `Layout discipline review`, and `UX review result` in `specs/pages/<page-slug>.md`
  because implementation and final review are now gated against those fields
- desktop and mobile mockups:
  put them in `design-assets/mockups/<page-slug>/desktop/` and `design-assets/mockups/<page-slug>/mobile/`
  because the page spec and implementation should point to those exact files
- shared storefront structure:
  put it in `specs/theme-system.md`
  because navigation, footer, routes, and template families should be decided across pages
- reusable component decisions:
  put them in `THEME_MEMORY.md`
  because repeated cards, snippets, and layouts should be tracked before pages drift apart
- brand-guidelines PDF:
  put it in `design-assets/raw/`
  because shared colors, fonts, and other brand rules should update theme tokens before page styling starts

## What Codex Creates

The scaffolded workspace has three main areas:

- `specs/` for theme planning, page specs, and tokens
- `design-assets/` for raw and reference design files
- `theme/` for deployable Shopify Liquid output

It also creates:

- `specs/theme-system.md` for shared storefront structure
- `THEME_MEMORY.md` for shared decisions and reusable components
- `design-assets/raw/` for original brand and design-source files

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

To extract tokens from a brand-guidelines document:

```bash
python scripts/extract_brand_guidelines.py design-assets/raw/brand-guidelines.pdf --tokens specs/tokens/theme-tokens.json
```

The extractor defaults to `--mode auto`, which tries native PDF text first and falls back to OCR for scanned or image-heavy PDFs. It updates the standard `colors` and `typography` sections first, then records any extra named brand roles in `colors_additional` and `typography_additional`.

To validate a page spec before implementation:

```bash
python scripts/validate_page_spec.py specs/pages/homepage.md --stage pre-implement
```

To validate that UX review has been recorded before treating a page as complete:

```bash
python scripts/validate_page_spec.py specs/pages/homepage.md --stage pre-complete
```

Use `pass`, `needs-rework`, or `fail` for `UX review result`.

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
