#!/usr/bin/env python3
"""
Validate that a page spec includes the required fields for implementation and UX review.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PAGE_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PATH_SPLIT_RE = re.compile(r"\s*[;,]\s*")
PLACEHOLDER_VALUES = {"tbd", "todo", "unknown", "pending", "?"}
REVIEW_PLACEHOLDER_VALUES = PLACEHOLDER_VALUES | {"n/a", "na", "none"}
ALLOWED_UX_REVIEW_RESULTS = {"pass", "needs-rework", "fail"}

REQUIRED_BY_STAGE = {
    "pre-implement": [
        "Page",
        "Slug",
        "Source",
        "Business goal",
        "Primary user task",
        "Primary CTA",
        "UX success criteria",
        "Shopify page type",
        "Desktop mockup paths",
        "Mobile mockup paths",
        "Shopify data sources",
        "Merchant-editable areas",
        "App constraints",
        "Unknowns",
        "Suggested implementation path",
    ],
    "pre-complete": [
        "Page",
        "Slug",
        "Source",
        "Business goal",
        "Primary user task",
        "Primary CTA",
        "UX success criteria",
        "Shopify page type",
        "Desktop mockup paths",
        "Mobile mockup paths",
        "Shopify data sources",
        "Merchant-editable areas",
        "App constraints",
        "Unknowns",
        "Suggested implementation path",
        "UX review notes",
        "UX review result",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate that a page spec is complete enough for implementation or completion."
    )
    parser.add_argument("spec_path", help="Path to specs/pages/<page-slug>.md")
    parser.add_argument(
        "--stage",
        choices=sorted(REQUIRED_BY_STAGE),
        default="pre-implement",
        help="Validation stage to enforce.",
    )
    return parser.parse_args()


def read_fields(spec_path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in spec_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not (line.startswith("`") and line.endswith("`")):
            continue
        content = line[1:-1]
        if ":" not in content:
            continue
        label, value = content.split(":", 1)
        fields[label.strip()] = value.strip()
    return fields


def workspace_root_from_spec(spec_path: Path) -> Path:
    return spec_path.parent.parent.parent


def validate_slug(fields: dict[str, str]) -> str | None:
    value = fields.get("Slug", "")
    if value and PAGE_SLUG_RE.fullmatch(value):
        return None
    return "Slug must be filled and use lowercase letters, digits, and hyphens only"


def is_placeholder(value: str) -> bool:
    return value.strip().lower() in PLACEHOLDER_VALUES


def split_path_field(value: str) -> list[str]:
    if not value.strip():
        return []
    return [item.strip() for item in PATH_SPLIT_RE.split(value.strip()) if item.strip()]


def validate_required_fields(fields: dict[str, str], stage: str) -> list[str]:
    errors: list[str] = []
    missing = [label for label in REQUIRED_BY_STAGE[stage] if not fields.get(label)]
    if missing:
        errors.append(f"Missing required fields for {stage}: " + ", ".join(missing))

    placeholders = [
        label for label in REQUIRED_BY_STAGE[stage]
        if fields.get(label) and is_placeholder(fields[label])
    ]
    if placeholders:
        errors.append(f"Placeholder values are not allowed for {stage}: " + ", ".join(placeholders))

    return errors


def validate_mockup_paths(fields: dict[str, str], spec_path: Path) -> list[str]:
    errors: list[str] = []
    workspace_root = workspace_root_from_spec(spec_path)

    for label in ("Desktop mockup paths", "Mobile mockup paths"):
        values = split_path_field(fields.get(label, ""))
        if not values:
            continue
        missing_paths: list[str] = []
        for value in values:
            candidate = Path(value).expanduser()
            if not candidate.is_absolute():
                candidate = (workspace_root / candidate).resolve()
            if not candidate.exists():
                missing_paths.append(value)
        if missing_paths:
            errors.append(f"{label} must point to existing file(s): " + ", ".join(missing_paths))

    return errors


def validate_ux_review(fields: dict[str, str], stage: str) -> list[str]:
    if stage != "pre-complete":
        return []

    errors: list[str] = []
    review_result = fields.get("UX review result", "").strip().lower()
    review_notes = fields.get("UX review notes", "").strip()

    if review_result and review_result not in ALLOWED_UX_REVIEW_RESULTS:
        errors.append(
            "UX review result must be one of: " + ", ".join(sorted(ALLOWED_UX_REVIEW_RESULTS))
        )
    if review_notes and (review_notes.strip().lower() in REVIEW_PLACEHOLDER_VALUES or len(review_notes) < 20):
        errors.append("UX review notes must describe the review outcome in a meaningful sentence")

    return errors


def main() -> int:
    args = parse_args()
    spec_path = Path(args.spec_path).expanduser().resolve()
    if not spec_path.exists():
        raise SystemExit(f"[ERROR] Page spec not found: {spec_path}")

    fields = read_fields(spec_path)
    errors: list[str] = []

    slug_error = validate_slug(fields)
    if slug_error:
        errors.append(slug_error)
    errors.extend(validate_required_fields(fields, args.stage))
    errors.extend(validate_mockup_paths(fields, spec_path))
    errors.extend(validate_ux_review(fields, args.stage))

    if errors:
        for item in errors:
            print(f"[ERROR] {item}")
        return 1

    print(f"[OK] Page spec is valid for {args.stage}: {spec_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
