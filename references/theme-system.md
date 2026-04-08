# Theme System

Define the shared storefront before implementing individual pages.
Pair it with `THEME_MEMORY.md`, which stores the evolving reusable-component inventory.

Record at least:

- page inventory and route map
- global header and footer behavior
- navigation structure
- shared templates
- reusable section inventory
- shared snippets and cards
- app integration points
- collection, product, cart, account, and policy page relationships
- canonical tokens and style rules

Use `specs/theme-system.md` for this plan.
Use `THEME_MEMORY.md` for evolving component and implementation memory.

Default assumptions:

- storefront pages should include shared header/navigation and footer structure
- intentional header/footer exceptions should be documented explicitly per page
- copy should stay concise, with UI carrying as much meaning as possible
- element count, card count, and nested container depth should stay restrained unless there is a clear reason not to

Questions to answer early:

- Which pages share the same header and footer?
- Which Framer sections should become reusable sections instead of page-only markup?
- Which cards, badges, buttons, and media treatments should be global snippets?
- Which pages should inherit the same collection or product template family?
- Which flows must link together cleanly, such as home -> collection -> product -> cart?

Do not treat page specs as isolated implementations once repeated structure is visible.
