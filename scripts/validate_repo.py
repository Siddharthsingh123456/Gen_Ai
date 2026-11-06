"""Lightweight repository checks for Python files and Jupyter notebooks.

Run from the repository root:
    python scripts/validate_repo.py
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "node_modules",
    "build",
    "dist",
}


def iter_source_files(suffix: str):
    for path in ROOT.rglob(f"*{suffix}"):
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        yield path


def check_python() -> list[str]:
    errors = []
    for path in iter_source_files(".py"):
        try:
            source = path.read_text(encoding="utf-8-sig")
            ast.parse(source, filename=str(path))
        except (OSError, UnicodeError, SyntaxError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    return errors


def check_notebooks() -> list[str]:
    errors = []
    for path in iter_source_files(".ipynb"):
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(notebook, dict):
                raise ValueError("notebook root must be a JSON object")
            if "cells" not in notebook or not isinstance(notebook["cells"], list):
                raise ValueError("missing valid 'cells' array")
            if "nbformat" not in notebook:
                raise ValueError("missing 'nbformat' field")
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    return errors


def main() -> int:
    errors = check_python() + check_notebooks()
    if errors:
        print(f"Validation failed: {len(errors)} issue(s)")
        for error in errors:
            print(f" - {error}")
        return 1

    python_count = sum(1 for _ in iter_source_files(".py"))
    notebook_count = sum(1 for _ in iter_source_files(".ipynb"))
    print("Repository validation passed.")
    print(f"Python files checked: {python_count}")
    print(f"Jupyter notebooks checked: {notebook_count}")
    print("Note: syntax/JSON validation does not execute projects or verify dependencies.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
