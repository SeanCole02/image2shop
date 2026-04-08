# Brand Guidelines

Use a brand-guidelines document to populate shared theme tokens before page work drifts.

Preferred source location in scaffolded workspaces:

- `design-assets/raw/brand-guidelines.pdf`
- or another brand-guidelines file under `design-assets/raw/`

Use `scripts/extract_brand_guidelines.py` to:

- extract text from a PDF through `pdftotext`
- find labeled brand colors
- collect a fallback color palette
- find heading/body font names when labeled
- detect a base font size when present
- merge the extracted values into `specs/tokens/theme-tokens.json`
- add extra named color roles under `colors_additional`
- add extra named type roles under `typography_additional`

After extraction:

- review the merged tokens
- rename or add fields when the brand doc defines roles outside the default schema
- keep the extracted source record in the `brand_guidelines` section of the token file
