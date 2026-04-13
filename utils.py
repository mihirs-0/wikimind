"""Shared helpers and path constants."""

import json
from pathlib import Path
import re
import unicodedata

# ── Path constants (all relative to project root) ──────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DIR = PROJECT_ROOT / "raw"
WIKI_DIR = PROJECT_ROOT / "wiki"
OUTPUT_DIR = PROJECT_ROOT / "output"

CONCEPTS_DIR = WIKI_DIR / "concepts"
SUMMARIES_DIR = WIKI_DIR / "summaries"
QUERIES_DIR = WIKI_DIR / "queries"
WIKI_INDEX = WIKI_DIR / "_index.md"
MANIFEST_PATH = RAW_DIR / "_manifest.json"

SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf", ".html"}


def slugify(text: str) -> str:
    """Convert text to a filesystem-safe slug."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text


def title_from_filename(path: Path) -> str:
    """Derive a human-readable title from a filename."""
    return path.stem.replace("-", " ").replace("_", " ").title()


def load_manifest() -> dict:
    """Load raw/_manifest.json, returning {} if it doesn't exist."""
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text())
    return {}


def save_manifest(manifest: dict) -> None:
    """Write manifest dict to raw/_manifest.json."""
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse YAML-style frontmatter from markdown text.

    Returns (metadata_dict, body) where body is everything after the
    closing '---' delimiter. If no frontmatter is found, returns
    an empty dict and the original text.
    """
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not match:
        return {}, text

    meta = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()

    return meta, match.group(2)
