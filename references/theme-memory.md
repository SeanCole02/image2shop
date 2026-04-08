# Theme Memory

Use `THEME_MEMORY.md` to persist decisions that should survive across page work.

Record at least:

- approved reusable sections
- approved reusable snippets
- reusable section candidates
- reusable snippet candidates
- reusable card candidates
- reusable layout-pattern candidates
- shared navigation and footer decisions
- template family decisions
- cross-page linking rules
- app integration assumptions
- repeated unresolved questions

Update it when:

- a new repeated pattern appears
- a page introduces a reusable card or media treatment
- a shared section is promoted from page-only to global
- a repeated layout pattern appears across templates
- a navigation or route decision changes

Do not keep this knowledge only inside page specs.

Promotion rules:

- promote immediately if the component is obviously global, such as header, footer, or a canonical product card
- promote after reuse on 2 or more pages when the structure and behavior are materially the same
- keep it as a candidate when visual similarity exists but data source, behavior, or merchant controls are still unsettled
