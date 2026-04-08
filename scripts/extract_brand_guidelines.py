#!/usr/bin/env python3
"""
Extract brand-guidelines data from a PDF or text file and merge it into theme tokens.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
ROLE_PATTERNS = {
    "brand_primary": re.compile(r"(?:primary|brand primary|main color)[^#\n]{0,80}(#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b)", re.I),
    "brand_secondary": re.compile(r"(?:secondary|brand secondary)[^#\n]{0,80}(#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b)", re.I),
    "accent": re.compile(r"(?:accent|highlight)[^#\n]{0,80}(#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b)", re.I),
    "text_primary": re.compile(r"(?:text|copy|body text)[^#\n]{0,80}(#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b)", re.I),
    "surface_primary": re.compile(r"(?:background|surface|canvas)[^#\n]{0,80}(#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b)", re.I),
    "border_default": re.compile(r"(?:border|stroke|divider)[^#\n]{0,80}(#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b)", re.I),
    "success": re.compile(r"(?:success)[^#\n]{0,80}(#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b)", re.I),
    "warning": re.compile(r"(?:warning|caution)[^#\n]{0,80}(#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b)", re.I),
    "error": re.compile(r"(?:error|danger)[^#\n]{0,80}(#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b)", re.I),
}
KNOWN_COLOR_ROLE_SYNONYMS = {
    "brand_primary": {"primary", "brand primary", "main color", "primary color"},
    "brand_secondary": {"secondary", "brand secondary", "secondary color"},
    "accent": {"accent", "highlight", "accent color"},
    "text_primary": {"text", "body text", "copy", "primary text"},
    "surface_primary": {"background", "surface", "canvas", "page background"},
    "border_default": {"border", "stroke", "divider"},
    "success": {"success"},
    "warning": {"warning", "caution"},
    "error": {"error", "danger"},
}
FONT_LABELS = {
    "font_heading": ("heading", "headline", "display", "title"),
    "font_body": ("body", "paragraph", "copy", "text"),
}
FONT_CANDIDATE_RE = re.compile(r"\b([A-Z][A-Za-z0-9&'./+-]*(?: [A-Z][A-Za-z0-9&'./+-]*){0,3})\b")
LINE_WITH_HEX_RE = re.compile(r"^(?P<label>[^#\n]{1,120}?)\s+(?P<hex>#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b)")
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")
PX_RE = re.compile(r"\b(\d{1,3})\s*px\b", re.I)
PT_RE = re.compile(r"\b(\d{1,3}(?:\.\d+)?)\s*pt\b", re.I)
OCR_LANGUAGES = ["en"]
AUTO_TEXT_SCORE_THRESHOLD = 6


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract brand-guidelines data from a PDF or text file and update theme tokens."
    )
    parser.add_argument("source", help="Path to a brand-guidelines PDF or text file.")
    parser.add_argument(
        "--tokens",
        default="specs/tokens/theme-tokens.json",
        help="Path to the theme tokens file to update.",
    )
    parser.add_argument(
        "--mode",
        choices=("auto", "text", "ocr"),
        default="auto",
        help="Extraction mode. `auto` tries text first, then OCR if needed.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the merged tokens instead of writing them.")
    return parser.parse_args()


def normalize_hex(value: str) -> str:
    value = value.upper()
    if len(value) == 4:
        return "#" + "".join(ch * 2 for ch in value[1:])
    return value


def slugify_token_key(value: str) -> str:
    normalized = NON_ALNUM_RE.sub("_", value.lower()).strip("_")
    return normalized[:48] or "unnamed"


def text_backend_available() -> bool:
    return bool(shutil.which("pdftotext"))


def ocr_backend_available() -> bool:
    return bool(shutil.which("pdftoppm")) and bool(importlib.util.find_spec("easyocr"))


def read_text_source(source: Path) -> dict[str, Any]:
    suffix = source.suffix.lower()
    if suffix in {".txt", ".md"}:
        return {
            "text": source.read_text(encoding="utf-8"),
            "method": "text-file",
            "candidate_scores": {},
            "fallback_used": False,
        }
    raise SystemExit("[ERROR] Supported text source types are .txt and .md")


def read_pdf_text(source: Path) -> str:
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise RuntimeError("pdftotext is not available in PATH")

    with tempfile.TemporaryDirectory() as temp_dir:
        output = Path(temp_dir) / "guidelines.txt"
        cmd = [pdftotext, "-layout", "-enc", "UTF-8", str(source), str(output)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            stderr = result.stderr.strip() or result.stdout.strip() or "unknown pdftotext error"
            raise RuntimeError(f"Failed to extract text from PDF: {stderr}")
        return output.read_text(encoding="utf-8", errors="replace")


def render_pdf_pages(source: Path, temp_dir: Path) -> list[Path]:
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        raise RuntimeError("pdftoppm is not available in PATH")

    prefix = temp_dir / "page"
    cmd = [pdftoppm, "-png", "-r", "200", str(source), str(prefix)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip() or "unknown pdftoppm error"
        raise RuntimeError(f"Failed to rasterize PDF for OCR: {stderr}")
    return sorted(temp_dir.glob("page-*.png"))


def read_pdf_ocr(source: Path) -> str:
    try:
        import easyocr  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("easyocr is not installed") from exc

    with tempfile.TemporaryDirectory() as temp_dir:
        image_paths = render_pdf_pages(source, Path(temp_dir))
        if not image_paths:
            raise RuntimeError("No PDF pages were rendered for OCR")

        reader = easyocr.Reader(OCR_LANGUAGES, gpu=False)
        lines: list[str] = []
        for image_path in image_paths:
            page_lines = reader.readtext(str(image_path), detail=0, paragraph=True)
            lines.extend(item.strip() for item in page_lines if item and item.strip())
        return "\n".join(lines)


def score_extracted_text(text: str) -> int:
    stripped = text.strip()
    if not stripped:
        return 0

    lines = [line for line in text.splitlines() if line.strip()]
    score = 0
    score += min(len(stripped) // 250, 6)
    score += min(len(lines) // 12, 3)
    score += min(len(HEX_RE.findall(text)), 4)
    score += min(len(labeled_color_matches(text)), 4)
    score += min(len(extract_fonts(text)), 2)
    if extract_base_font_size(text):
        score += 1
    return score


def read_pdf_source(source: Path, mode: str) -> dict[str, Any]:
    text_result: dict[str, Any] | None = None
    ocr_result: dict[str, Any] | None = None
    warnings: list[str] = []
    text_error: str | None = None
    ocr_error: str | None = None

    if mode in {"auto", "text"}:
        if not text_backend_available():
            if mode == "text":
                raise SystemExit("[ERROR] pdftotext is not available in PATH")
            warnings.append("pdftotext is not available; skipping native PDF text extraction")
        else:
            try:
                text = read_pdf_text(source)
            except RuntimeError as exc:
                text_error = str(exc)
                if mode == "text":
                    raise SystemExit(f"[ERROR] {exc}")
                warnings.append(f"Native PDF text extraction failed: {exc}")
            else:
                text_result = {
                    "text": text,
                    "method": "pdftotext",
                    "score": score_extracted_text(text),
                }

    if mode in {"auto", "ocr"}:
        if not ocr_backend_available():
            if mode == "ocr":
                raise SystemExit("[ERROR] OCR mode requires pdftoppm and easyocr")
            ocr_error = "OCR backend is not available"
            warnings.append("OCR backend is not available; OCR fallback cannot run")
        else:
            try:
                ocr_text = read_pdf_ocr(source)
            except RuntimeError as exc:
                ocr_error = str(exc)
                if mode == "ocr":
                    raise SystemExit(f"[ERROR] {exc}")
                warnings.append(f"OCR extraction failed: {exc}")
            else:
                ocr_result = {
                    "text": ocr_text,
                    "method": "ocr",
                    "score": score_extracted_text(ocr_text),
                }

    if mode == "text":
        if not text_result:
            raise SystemExit("[ERROR] PDF text extraction is not available")
        return {
            "text": text_result["text"],
            "method": text_result["method"],
            "candidate_scores": {"text": text_result["score"]},
            "fallback_used": False,
            "warnings": warnings,
        }

    if mode == "ocr":
        if not ocr_result:
            raise SystemExit("[ERROR] OCR extraction is not available")
        return {
            "text": ocr_result["text"],
            "method": ocr_result["method"],
            "candidate_scores": {"ocr": ocr_result["score"]},
            "fallback_used": False,
            "warnings": warnings,
        }

    candidate_scores: dict[str, int] = {}
    if text_result:
        candidate_scores["text"] = text_result["score"]
    if ocr_result:
        candidate_scores["ocr"] = ocr_result["score"]

    if text_result and text_result["score"] >= AUTO_TEXT_SCORE_THRESHOLD:
        return {
            "text": text_result["text"],
            "method": text_result["method"],
            "candidate_scores": candidate_scores,
            "fallback_used": False,
            "warnings": warnings,
        }

    if ocr_result and (not text_result or ocr_result["score"] > text_result["score"]):
        return {
            "text": ocr_result["text"],
            "method": ocr_result["method"],
            "candidate_scores": candidate_scores,
            "fallback_used": bool(text_result),
            "warnings": warnings,
        }

    if text_result:
        if text_result["score"] < AUTO_TEXT_SCORE_THRESHOLD:
            if ocr_error:
                warnings.append(
                    f"Using weak native PDF text extraction because OCR fallback did not succeed: {ocr_error}"
                )
            else:
                warnings.append(
                    "Using weak native PDF text extraction because OCR fallback was not available"
                )
        return {
            "text": text_result["text"],
            "method": text_result["method"],
            "candidate_scores": candidate_scores,
            "fallback_used": False,
            "warnings": warnings,
        }

    error_parts = [item for item in (text_error, ocr_error) if item]
    if error_parts:
        raise SystemExit("[ERROR] No usable extraction backend is available for this PDF: " + " | ".join(error_parts))
    raise SystemExit("[ERROR] No usable extraction backend is available for this PDF")


def read_source_text(source: Path, mode: str) -> dict[str, Any]:
    suffix = source.suffix.lower()
    if suffix in {".txt", ".md"}:
        return read_text_source(source)
    if suffix == ".pdf":
        return read_pdf_source(source, mode)
    raise SystemExit("[ERROR] Supported source types are .pdf, .txt, and .md")


def labeled_color_matches(text: str) -> dict[str, str]:
    matches: dict[str, str] = {}
    for key, pattern in ROLE_PATTERNS.items():
        match = pattern.search(text)
        if match:
            matches[key] = normalize_hex(match.group(1))
    return matches


def additional_color_matches(text: str, assigned_colors: dict[str, str]) -> dict[str, str]:
    assigned_values = set(assigned_colors.values())
    extras: dict[str, str] = {}

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = LINE_WITH_HEX_RE.search(line)
        if not match:
            continue

        color = normalize_hex(match.group("hex"))
        if color in assigned_values:
            continue

        label = match.group("label")
        label = re.sub(r"\s+", " ", label.replace(":", " ").replace("/", " ")).strip(" -")
        label_key = slugify_token_key(label)
        if not label_key:
            continue

        if any(label_key == slugify_token_key(name) for values in KNOWN_COLOR_ROLE_SYNONYMS.values() for name in values):
            continue

        extra_key = f"custom_{label_key}"
        extras.setdefault(extra_key, color)

    return extras


def most_common_colors(text: str, limit: int = 12) -> list[str]:
    counter = Counter(normalize_hex(item) for item in HEX_RE.findall(text))
    return [color for color, _ in counter.most_common(limit)]


def extract_font_from_lines(lines: list[str], labels: tuple[str, ...]) -> str | None:
    for line in lines:
        lowered = line.lower()
        if not any(label in lowered for label in labels):
            continue
        if not any(keyword in lowered for keyword in ("font", "typeface", "typography", "type style", "type-style", "type")):
            continue
        cleaned_line = re.sub(
            r"\b(heading|headline|display|title|body|paragraph|copy|text|font|fonts|type|typeface|typography)\b",
            " ",
            line,
            flags=re.I,
        )
        candidates = [
            item for item in FONT_CANDIDATE_RE.findall(cleaned_line)
            if item.lower() not in {"font", "fonts", "type", "typeface", "primary", "secondary", "body", "heading", "headline"}
        ]
        if candidates:
            return candidates[-1]
    return None


def extract_fonts(text: str) -> dict[str, str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    result: dict[str, str] = {}
    for key, labels in FONT_LABELS.items():
        font = extract_font_from_lines(lines, labels)
        if font:
            result[key] = font
    return result


def extract_additional_fonts(text: str, assigned_fonts: dict[str, str]) -> dict[str, str]:
    known_values = set(assigned_fonts.values())
    extras: dict[str, str] = {}
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in lines:
        if ":" not in line:
            continue
        label, remainder = (part.strip() for part in line.split(":", 1))
        lowered = label.lower()
        if "font" not in lowered and "type" not in lowered:
            continue

        candidates = [
            item for item in FONT_CANDIDATE_RE.findall(remainder)
            if item.lower() not in {"font", "fonts", "type", "typeface", "primary", "secondary", "body", "heading", "headline"}
        ]
        if not candidates:
            continue

        value = candidates[-1]
        if value in known_values:
            continue

        cleaned_label = re.sub(r"\b(font|fonts|type|typeface|typography)\b", "", label, flags=re.I).strip()
        key = f"custom_{slugify_token_key(cleaned_label)}"
        extras.setdefault(key, value)

    return extras


def extract_base_font_size(text: str) -> int | None:
    for line in text.splitlines():
        lowered = line.lower()
        if "base" in lowered and "font" in lowered:
            px = PX_RE.search(line)
            if px:
                return int(px.group(1))
            pt = PT_RE.search(line)
            if pt:
                return round(float(pt.group(1)) * 96 / 72)
    return None


def load_tokens(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"meta": {"name": "theme-tokens", "version": "0.1.0"}}


def ensure_sections(tokens: dict) -> None:
    tokens.setdefault("meta", {})
    tokens.setdefault("colors", {})
    tokens.setdefault("colors_additional", {})
    tokens.setdefault("typography", {})
    tokens.setdefault("typography_additional", {})
    tokens.setdefault("brand_guidelines", {})


def merge_extracted_data(tokens: dict, source: Path, text: str, extraction: dict[str, Any]) -> dict:
    ensure_sections(tokens)
    colors = labeled_color_matches(text)
    color_extras = additional_color_matches(text, colors)
    palette = most_common_colors(text)
    fonts = extract_fonts(text)
    font_extras = extract_additional_fonts(text, fonts)
    base_font_size = extract_base_font_size(text)

    for key, value in colors.items():
        tokens["colors"][key] = value
    if palette:
        tokens["colors"]["extracted_palette"] = palette
    for key, value in color_extras.items():
        tokens["colors_additional"][key] = value

    for key, value in fonts.items():
        tokens["typography"][key] = value
    if fonts:
        tokens["typography"]["extracted_families"] = sorted(set(fonts.values()))
    for key, value in font_extras.items():
        tokens["typography_additional"][key] = value
    if base_font_size:
        tokens["typography"]["base_font_size_px"] = base_font_size

    guidelines = tokens["brand_guidelines"]
    guidelines["source_file"] = str(source)
    guidelines["source_type"] = source.suffix.lower().lstrip(".")
    guidelines["extracted_at_utc"] = datetime.now(timezone.utc).isoformat()
    guidelines["extraction_method"] = extraction["method"]
    guidelines["candidate_scores"] = extraction.get("candidate_scores", {})
    guidelines["ocr_fallback_used"] = extraction.get("fallback_used", False)
    guidelines["extraction_warnings"] = extraction.get("warnings", [])
    guidelines["colors_found"] = len(palette)
    guidelines["fonts_found"] = len(tokens["typography"].get("extracted_families", []))
    guidelines["additional_color_fields"] = sorted(color_extras.keys())
    guidelines["additional_typography_fields"] = sorted(font_extras.keys())
    guidelines["notes"] = [
        "Review extracted values before treating them as final.",
        "Add or rename token fields when the brand document defines roles not covered by the default schema.",
    ]
    return {
        "tokens": tokens,
        "palette": palette,
        "fonts": tokens["typography"].get("extracted_families", []),
        "applied_color_roles": sorted(colors.keys()),
        "additional_color_roles": sorted(color_extras.keys()),
        "additional_font_roles": sorted(font_extras.keys()),
        "base_font_size_px": base_font_size,
    }


def main() -> int:
    args = parse_args()
    source = Path(args.source).expanduser().resolve()
    tokens_path = Path(args.tokens).expanduser().resolve()

    if not source.exists():
        raise SystemExit(f"[ERROR] Source file not found: {source}")

    extraction = read_source_text(source, args.mode)
    tokens = load_tokens(tokens_path)
    result = merge_extracted_data(tokens, source, extraction["text"], extraction)

    if args.dry_run:
        print(json.dumps(result["tokens"], indent=2))
    else:
        tokens_path.parent.mkdir(parents=True, exist_ok=True)
        tokens_path.write_text(json.dumps(result["tokens"], indent=2) + "\n", encoding="utf-8")
        print(f"[OK] Updated tokens at {tokens_path}")

    print(f"[OK] Extraction method: {extraction['method']}")
    if extraction.get("candidate_scores"):
        formatted_scores = ", ".join(f"{key}={value}" for key, value in extraction["candidate_scores"].items())
        print(f"[INFO] Extraction scores: {formatted_scores}")
    if extraction.get("fallback_used"):
        print("[INFO] OCR fallback was used")
    for warning in extraction.get("warnings", []):
        print(f"[WARN] {warning}")
    print(f"[OK] Extracted {len(result['palette'])} color(s)")
    if result["applied_color_roles"]:
        print(f"[OK] Applied labeled color roles: {', '.join(result['applied_color_roles'])}")
    if result["additional_color_roles"]:
        print(f"[OK] Added custom color fields: {', '.join(result['additional_color_roles'])}")
    if result["fonts"]:
        print(f"[OK] Extracted fonts: {', '.join(result['fonts'])}")
    if result["additional_font_roles"]:
        print(f"[OK] Added custom typography fields: {', '.join(result['additional_font_roles'])}")
    if result["base_font_size_px"]:
        print(f"[OK] Extracted base font size: {result['base_font_size_px']}px")
    print("[INFO] Review extracted values before treating them as final")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
