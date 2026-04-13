"""Ingestion logic — pull source documents into raw/."""

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import click

from wikimind.utils import (
    RAW_DIR,
    SUPPORTED_EXTENSIONS,
    load_manifest,
    save_manifest,
    slugify,
    title_from_filename,
)


def _sha256(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()


# ── Per-format extraction ───────────────────────────────────────────────

def _extract_text(path: Path) -> str:
    """Read a supported file and return its content as markdown text."""
    ext = path.suffix.lower()
    if ext in (".md", ".txt"):
        return path.read_text()
    if ext == ".pdf":
        return _extract_pdf(path)
    if ext == ".html":
        return _extract_html(path)
    raise ValueError(f"Unsupported file type: {ext}")


def _extract_pdf(path: Path) -> str:
    import pymupdf4llm
    return pymupdf4llm.to_markdown(str(path))


def _extract_html(path: Path) -> str:
    import trafilatura
    html = path.read_text()
    result = trafilatura.extract(html, output_format="markdown", include_links=True)
    if result is None:
        raise click.ClickException(f"trafilatura could not extract content from {path}")
    return result


# ── Frontmatter wrapping ───────────────────────────────────────────────

def _wrap_with_frontmatter(body: str, source_path: Path, title: str, now: str) -> str:
    frontmatter = (
        f"---\n"
        f"title: {title}\n"
        f"source_path: {source_path}\n"
        f"ingested_at: {now}\n"
        f"---\n\n"
    )
    return frontmatter + body


# ── Core ingestion ─────────────────────────────────────────────────────

def _collect_files(sources: tuple[str, ...]) -> list[Path]:
    """Expand directories and filter to supported extensions."""
    files: list[Path] = []
    for src in sources:
        p = Path(src).resolve()
        if p.is_dir():
            for child in sorted(p.rglob("*")):
                if child.is_file() and child.suffix.lower() in SUPPORTED_EXTENSIONS:
                    files.append(child)
        elif p.is_file():
            if p.suffix.lower() not in SUPPORTED_EXTENSIONS:
                click.echo(f"  skip (unsupported): {p.name}")
                continue
            files.append(p)
        else:
            click.echo(f"  skip (not found): {src}")
    return files


def _ingest_one(path: Path, manifest: dict) -> bool:
    """Ingest a single file. Returns True if the file was written/updated."""
    now = datetime.now(timezone.utc).isoformat()
    title = title_from_filename(path)
    body = _extract_text(path)
    content_hash = _sha256(body)
    content = _wrap_with_frontmatter(body, path, title, now)

    slug = slugify(path.stem) + ".md"
    dest = RAW_DIR / slug
    source_key = str(path)

    # Check manifest for existing entry from the same source
    for raw_name, entry in manifest.items():
        if entry["original_source"] == source_key:
            if entry["sha256"] == content_hash:
                click.echo(f"  skip (unchanged): {path.name}")
                return False
            # Source changed — overwrite and mark uncompiled
            click.echo(f"  update: {path.name} -> raw/{raw_name}")
            dest = RAW_DIR / raw_name
            dest.write_text(content)
            entry["sha256"] = content_hash
            entry["ingested_at"] = now
            entry["compiled"] = False
            return True

    # Handle slug collisions for genuinely new sources
    if dest.exists() and slug in manifest:
        counter = 2
        while True:
            candidate = f"{slugify(path.stem)}-{counter}.md"
            if candidate not in manifest:
                slug = candidate
                dest = RAW_DIR / slug
                break
            counter += 1

    click.echo(f"  ingest: {path.name} -> raw/{slug}")
    dest.write_text(content)
    manifest[slug] = {
        "original_source": source_key,
        "ingested_at": now,
        "sha256": content_hash,
        "compiled": False,
    }
    return True


def run_ingest(sources: tuple[str, ...]) -> None:
    """Ingest one or more files or directories into raw/."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    files = _collect_files(sources)

    if not files:
        click.echo("No supported files found.")
        return

    click.echo(f"Found {len(files)} file(s) to process.")
    written = 0
    for f in files:
        try:
            if _ingest_one(f, manifest):
                written += 1
        except Exception as exc:
            click.echo(f"  error ({f.name}): {exc}")

    save_manifest(manifest)
    click.echo(f"Done. {written} file(s) ingested, {len(files) - written} skipped.")
