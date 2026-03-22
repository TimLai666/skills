#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


EXCLUDED_DIR_NAMES = {"output", ".git"}


def is_excluded_directory(path: Path) -> bool:
    name = path.name
    return name in EXCLUDED_DIR_NAMES or name.startswith(".")


def create_zip_with_top_level(folder: Path, zip_path: Path) -> None:
    with ZipFile(zip_path, mode="w", compression=ZIP_DEFLATED) as archive:
        for current_dir, dir_names, file_names in os.walk(folder):
            current_path = Path(current_dir)
            relative_dir = current_path.relative_to(folder)

            if not dir_names and not file_names:
                if str(relative_dir) != ".":
                    archive.writestr(f"{relative_dir.as_posix()}/", "")

            for file_name in file_names:
                file_path = current_path / file_name
                archive_name = file_path.relative_to(folder).as_posix()
                archive.write(file_path, archive_name)


def run() -> int:
    root = Path.cwd()
    output_dir = root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    failure_count = 0
    skipped_count = 0

    child_directories = sorted((path for path in root.iterdir() if path.is_dir()), key=lambda p: p.name.lower())

    for child_dir in child_directories:
        if is_excluded_directory(child_dir):
            skipped_count += 1
            print(f"SKIP {child_dir.name}: excluded")
            continue

        destination_zip = output_dir / f"{child_dir.name}.zip"

        try:
            if destination_zip.exists():
                destination_zip.unlink()

            create_zip_with_top_level(child_dir, destination_zip)
            success_count += 1
            print(f"OK   {child_dir.name} -> {destination_zip.relative_to(root)}")
        except Exception as exc:  # pragma: no cover
            failure_count += 1
            print(f"FAIL {child_dir.name}: {exc}")

    print(
        "Summary: "
        f"success={success_count}, "
        f"failure={failure_count}, "
        f"skipped={skipped_count}"
    )

    return 1 if failure_count else 0


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
