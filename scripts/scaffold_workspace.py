#!/usr/bin/env python3
"""
Scaffold a Framer-to-Shopify workspace.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

PAGE_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_page_slug(value: str) -> str:
    if not PAGE_SLUG_RE.fullmatch(value):
        raise argparse.ArgumentTypeError(
            "page slug must use lowercase letters, digits, and hyphens only"
        )
    return value


def copy_tree(template_root: Path, target_root: Path, force: bool) -> tuple[list[Path], list[Path]]:
    written: list[Path] = []
    skipped: list[Path] = []

    for source in sorted(template_root.rglob("*")):
        relative = source.relative_to(template_root)
        destination = target_root / relative
        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and not force:
            skipped.append(destination)
            continue
        shutil.copyfile(source, destination)
        written.append(destination)

    return written, skipped


def ensure_page_scaffold(skill_root: Path, target_root: Path, page_slug: str, force: bool) -> tuple[list[Path], list[Path]]:
    written: list[Path] = []
    skipped: list[Path] = []

    page_spec = target_root / "specs" / "pages" / f"{page_slug}.md"
    page_spec.parent.mkdir(parents=True, exist_ok=True)
    page_template = skill_root / "assets" / "templates" / "page-intake-template.md"
    if page_spec.exists() and not force:
        skipped.append(page_spec)
    else:
        shutil.copyfile(page_template, page_spec)
        written.append(page_spec)

    notes_file = target_root / "design-assets" / "mockups" / page_slug / "notes.md"
    notes_file.parent.mkdir(parents=True, exist_ok=True)
    notes_template = skill_root / "assets" / "templates" / "mockup-notes.md"
    if notes_file.exists() and not force:
        skipped.append(notes_file)
    else:
        shutil.copyfile(notes_template, notes_file)
        written.append(notes_file)

    for folder in ("desktop", "mobile"):
        mockup_dir = target_root / "design-assets" / "mockups" / page_slug / folder
        mockup_dir.mkdir(parents=True, exist_ok=True)

    return written, skipped


def ensure_workspace_script(skill_root: Path, target_root: Path, relative_path: str, force: bool) -> tuple[list[Path], list[Path]]:
    written: list[Path] = []
    skipped: list[Path] = []

    source = skill_root / relative_path
    destination = target_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists() and not force:
        skipped.append(destination)
    else:
        shutil.copyfile(source, destination)
        written.append(destination)

    return written, skipped


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a Framer-to-Shopify workspace.")
    parser.add_argument("target_dir", help="Target directory for the workspace.")
    parser.add_argument(
        "--page-slug",
        type=validate_page_slug,
        help="Optional page slug to scaffold.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    template_root = skill_root / "assets" / "workspace"
    target_root = Path(args.target_dir).resolve()
    target_root.mkdir(parents=True, exist_ok=True)

    written, skipped = copy_tree(template_root, target_root, args.force)

    token_target = target_root / "specs" / "tokens" / "theme-tokens.json"
    token_template = skill_root / "assets" / "templates" / "theme-tokens.json"
    token_target.parent.mkdir(parents=True, exist_ok=True)
    if token_target.exists() and not args.force:
        skipped.append(token_target)
    else:
        shutil.copyfile(token_template, token_target)
        written.append(token_target)

    script_written, script_skipped = ensure_workspace_script(
        skill_root,
        target_root,
        "scripts/validate_page_spec.py",
        args.force,
    )
    written.extend(script_written)
    skipped.extend(script_skipped)

    if args.page_slug:
        page_written, page_skipped = ensure_page_scaffold(skill_root, target_root, args.page_slug, args.force)
        written.extend(page_written)
        skipped.extend(page_skipped)

    print(f"[OK] Scaffolded workspace in {target_root}")
    print(f"[OK] Wrote {len(written)} file(s)")
    if skipped:
        print(f"[INFO] Skipped {len(skipped)} existing file(s)")
    if args.page_slug:
        print(f"[OK] Prepared page slug: {args.page_slug}")
    print("[NEXT] Put shared colors and theme tokens in specs/tokens/theme-tokens.json")
    print("[NEXT] If you have a brand-guidelines PDF, put it in design-assets/raw/ and extract tokens from it before styling pages")
    print("[NEXT] Put shared navigation, footer, routes, and template structure in specs/theme-system.md")
    print("[NEXT] Put reusable component decisions in THEME_MEMORY.md")
    if args.page_slug:
        print(f"[NEXT] Put desktop mockups in design-assets/mockups/{args.page_slug}/desktop/")
        print(f"[NEXT] Put mobile mockups in design-assets/mockups/{args.page_slug}/mobile/")
        print(f"[NEXT] Fill out the matching page spec in specs/pages/{args.page_slug}.md after the mockups are in place")
    else:
        print("[NEXT] Choose a lowercase hyphenated page slug such as homepage or product-detail")
        print("[NEXT] Then put desktop and mobile mockups in design-assets/mockups/<page-slug>/desktop/ and mobile/")
        print("[NEXT] Fill out the matching page spec in specs/pages/<page-slug>.md after the mockups are in place")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
