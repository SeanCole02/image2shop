# Image2Shop

Image2Shop is an open-source Codex skill for turning Framer pages, screenshots, and static storefront mockups into a structured Shopify Liquid workflow.
It gives teams a repeatable handoff from design imagery into:

- shared theme-system planning
- persistent theme memory
- page intake specs
- mockup storage
- design token capture
- Shopify theme architecture
- implementation-ready workspace scaffolding

## What It Does

Image2Shop helps Codex:

- scaffold a Framer-to-Shopify workspace
- separate `specs/`, `design-assets/`, and `theme/`
- define a coherent theme system across pages
- preserve shared decisions in `THEME_MEMORY.md`
- identify and promote reusable components early
- create page intake files and mockup folders
- ask clarifying questions before implementation
- map image-based designs into Shopify templates, sections, snippets, and settings

## Repository Layout

- `SKILL.md`: root skill definition
- `agents/openai.yaml`: UI metadata for the skill
- `references/`: workflow and mapping guidance
- `scripts/scaffold_workspace.py`: deterministic workspace scaffold script
- `assets/templates/`: reusable intake and token templates
- `assets/workspace/`: starter workspace files emitted by the scaffold script

## Quick Start

Scaffold a workspace:

```bash
python scripts/scaffold_workspace.py <target-dir>
```

Scaffold a workspace and first page:

```bash
python scripts/scaffold_workspace.py <target-dir> --page-slug homepage
```

## Generated Workspace

The scaffolded workspace is split into:

- `specs/` for process docs, page specs, and design tokens
- `design-assets/` for raw, mockup, and processed design files
- `theme/` for deployable Shopify Liquid output

The shared storefront layer lives in `specs/theme-system.md`.
Persistent cross-page decisions live in `THEME_MEMORY.md`.

`THEME_MEMORY.md` separates reusable candidates into:

- section candidates
- snippet candidates
- card candidates
- layout-pattern candidates

## Intended Workflow

1. Define the shared storefront structure in `specs/theme-system.md`.
2. Update `THEME_MEMORY.md` with reusable components and shared decisions.
3. Promote candidates when they are clearly global or reused across multiple pages.
4. Export or capture Framer page mockups.
5. Place them under `design-assets/mockups/<page-slug>/`.
6. Fill out `specs/pages/<page-slug>.md`.
7. Record unknowns and ask clarifying questions.
8. Lock tokens in `specs/tokens/theme-tokens.json`.
9. Build the approved Shopify output under `theme/`.

## License

This repository is licensed under `GPL-3.0-or-later`.

See [LICENSE](./LICENSE).
