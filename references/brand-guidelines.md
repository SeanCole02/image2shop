# Brand Guidelines

Use a brand-guidelines document to populate shared theme tokens before page work drifts.

Preferred source location in scaffolded workspaces:

- `design-assets/raw/brand-guidelines.pdf`
- or another brand-guidelines file under `design-assets/raw/`

Use `scripts/extract_brand_guidelines.py` to:

- extract text from a PDF through `pdftotext`
- fall back to OCR for image-heavy or scanned PDFs when the text extraction is weak
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

Extraction modes:

- `--mode auto` tries native PDF text first, then switches to OCR when needed
- `--mode text` forces native PDF text extraction
- `--mode ocr` forces OCR
