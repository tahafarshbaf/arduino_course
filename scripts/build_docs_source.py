"""Assembles the docs/ folder mkdocs builds from, out of the repo's real
source files (README.md, Lectures/) without duplicating them in git.

Run this before `mkdocs build` / `mkdocs serve` / `mkdocs gh-deploy`.
"""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

if DOCS.exists():
    shutil.rmtree(DOCS)
DOCS.mkdir()

shutil.copyfile(ROOT / "README.md", DOCS / "index.md")
shutil.copytree(ROOT / "Lectures", DOCS / "Lectures")
shutil.copytree(ROOT / "Pre-Course", DOCS / "Pre-Course")
shutil.copyfile(ROOT / "LICENSE", DOCS / "LICENSE")

print(f"docs/ assembled at {DOCS}")
