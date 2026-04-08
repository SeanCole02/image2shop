#!/usr/bin/env python3
"""
Update an installed Image2Shop skill in place.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import urllib.request
import zipfile
from pathlib import Path

DEFAULT_REPO = "SeanCole02/image2shop"
DEFAULT_REF = "main"
SKILL_NAME = "image2shop"
PRESERVE_NAMES = {".git", "__pycache__"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update an installed Image2Shop skill in place.")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="GitHub repo in owner/name form.")
    parser.add_argument("--ref", default=DEFAULT_REF, help="GitHub ref to install from.")
    parser.add_argument("--dest", help="Destination installed skill directory.")
    parser.add_argument("--source-dir", help="Local source directory to update from instead of GitHub.")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without changing files.")
    return parser.parse_args()


def require_skill_root(path: Path) -> Path:
    if not (path / "SKILL.md").exists():
        raise SystemExit(f"[ERROR] SKILL.md not found in {path}")
    return path


def download_repo(repo: str, ref: str, temp_dir: Path) -> Path:
    archive_path = temp_dir / "skill.zip"
    url = f"https://api.github.com/repos/{repo}/zipball/{ref}"
    urllib.request.urlretrieve(url, archive_path)

    extract_dir = temp_dir / "extract"
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path) as zf:
        zf.extractall(extract_dir)

    roots = [path for path in extract_dir.iterdir() if path.is_dir()]
    if len(roots) != 1:
        raise SystemExit("[ERROR] Could not determine extracted repo root.")
    return require_skill_root(roots[0])


def should_preserve(path: Path, dest_root: Path) -> bool:
    try:
        relative = path.relative_to(dest_root)
    except ValueError:
        return False
    return bool(relative.parts and relative.parts[0] in PRESERVE_NAMES)


def is_preserved_relative(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return bool(relative.parts and relative.parts[0] in PRESERVE_NAMES)


def installed_skill_dir() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    base = Path(codex_home).expanduser() if codex_home else Path.home() / ".codex"
    return base / "skills" / SKILL_NAME


def resolve_dest_root(current_root: Path, explicit_dest: str | None) -> Path:
    if explicit_dest:
        return require_skill_root(Path(explicit_dest).expanduser().resolve())

    installed_root = installed_skill_dir().resolve()
    if current_root.resolve() == installed_root and (current_root / "SKILL.md").exists():
        return current_root

    if installed_root.exists():
        return require_skill_root(installed_root)

    if (current_root / ".git").exists():
        raise SystemExit(
            "[ERROR] Installed skill copy not found. Pass --dest or run the updater from the installed skill directory."
        )

    return require_skill_root(current_root)


def schedule_self_replace(staged_path: Path, dest_path: Path) -> None:
    code = textwrap.dedent(
        """
        import os, sys, time
        staged, dest = sys.argv[1], sys.argv[2]
        for _ in range(100):
            try:
                os.replace(staged, dest)
                raise SystemExit(0)
            except PermissionError:
                time.sleep(0.1)
        raise SystemExit(1)
        """
    ).strip()
    popen_kwargs = {
        "args": [sys.executable, "-c", code, str(staged_path), str(dest_path)],
        "close_fds": True,
        "start_new_session": True,
    }
    if os.name == "nt":
        popen_kwargs["creationflags"] = (
            getattr(subprocess, "DETACHED_PROCESS", 0)
            | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        )
    subprocess.Popen(**popen_kwargs)


def sync_tree(source_root: Path, dest_root: Path, dry_run: bool) -> tuple[int, int, int, bool]:
    written = 0
    removed = 0
    skipped = 0
    self_replace_scheduled = False
    script_path = Path(__file__).resolve()
    prune = not (dest_root / ".git").exists()

    expected_files: set[Path] = set()
    expected_dirs: set[Path] = set()

    for source in sorted(source_root.rglob("*")):
        if is_preserved_relative(source, source_root):
            continue
        relative = source.relative_to(source_root)
        destination = dest_root / relative
        if source.is_dir():
            expected_dirs.add(destination)
            if dry_run:
                continue
            destination.mkdir(parents=True, exist_ok=True)
            continue

        expected_files.add(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)

        if destination.resolve() == script_path:
            if dry_run:
                skipped += 1
                continue
            staged_self = destination.with_suffix(destination.suffix + ".new")
            shutil.copy2(source, staged_self)
            schedule_self_replace(staged_self, destination)
            skipped += 1
            self_replace_scheduled = True
            continue

        if dry_run:
            written += 1
            continue

        shutil.copy2(source, destination)
        written += 1

    if prune:
        files_to_remove = [
            path for path in dest_root.rglob("*")
            if path.is_file()
            and path not in expected_files
            and path.resolve() != script_path
            and not should_preserve(path, dest_root)
        ]
        for path in sorted(files_to_remove, reverse=True):
            if dry_run:
                removed += 1
                continue
            path.unlink(missing_ok=True)
            removed += 1

        dirs_to_remove = [
            path for path in dest_root.rglob("*")
            if path.is_dir()
            and path not in expected_dirs
            and not should_preserve(path, dest_root)
        ]
        for path in sorted(dirs_to_remove, key=lambda item: len(item.parts), reverse=True):
            if dry_run:
                continue
            try:
                path.rmdir()
            except OSError:
                pass

    return written, removed, skipped, self_replace_scheduled


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parents[1]
    dest_root = resolve_dest_root(skill_root, args.dest)

    if args.source_dir:
        source_root = require_skill_root(Path(args.source_dir).expanduser().resolve())
        temp_dir_ctx = None
    else:
        temp_dir_ctx = tempfile.TemporaryDirectory()
        source_root = download_repo(args.repo, args.ref, Path(temp_dir_ctx.name))

    try:
        written, removed, skipped, self_replace_scheduled = sync_tree(source_root, dest_root, args.dry_run)
    finally:
        if temp_dir_ctx is not None:
            temp_dir_ctx.cleanup()

    print(f"[OK] Updated skill at {dest_root}")
    print(f"[OK] Wrote {written} file(s)")
    if removed:
        print(f"[OK] Removed {removed} stale file(s)")
    if skipped:
        print(f"[INFO] Skipped {skipped} file(s), including the running updater if applicable")
    if self_replace_scheduled:
        print("[INFO] Scheduled updater self-replacement after this process exits")
    if args.dry_run:
        print("[INFO] Dry run only, no files changed")
    print("Restart Codex to pick up updated skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
