# Framer to Shopify

Treat Framer as the visual specification.

Do not attempt to preserve Framer as runtime code. Rebuild the design as native Shopify theme primitives.

Before page implementation, decide which parts belong to the shared theme system and which parts are page-specific.
When repeated structure appears, mark it immediately in `THEME_MEMORY.md` as either a candidate or an approved shared component.

Map each design region to one of:

- template
- section
- block
- snippet
- app block
- theme setting
- metafield or metaobject source

Also decide whether each repeated region is:

- page-only
- reusable candidate
- approved shared section
- approved shared snippet

Implementation order:

1. template composition
2. high-level sections
3. repeated snippets
4. CSS architecture
5. JavaScript only where necessary
6. schema settings for merchant control

Token extraction priorities:

- colors
- typography
- spacing
- radius
- shadows
- container widths
- motion values when the design makes them explicit

Implementation guidance:

- prefer progressive enhancement
- simplify decorative Framer interactions when they are not worth the Shopify complexity cost
- preserve app compatibility
- use Shopify objects for products, collections, cart, and customer data instead of static HTML

QA checklist:

- consistency with the shared theme system
- consistency with `THEME_MEMORY.md`
- visual parity against the mockup
- desktop and mobile behavior
- empty states
- overflow handling
- section setting behavior
- app block rendering
- performance impact of media and motion
