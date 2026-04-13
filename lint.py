"""Structural lint checks for the wiki — no LLM involvement."""

import re
from difflib import SequenceMatcher
from pathlib import Path

import click
import frontmatter

from wikimind.utils import (
    CONCEPTS_DIR,
    OUTPUT_DIR,
    SUMMARIES_DIR,
    WIKI_DIR,
    WIKI_INDEX,
    load_manifest,
    slugify,
)

WIKILINK_RE = re.compile(r"\[\[(.+?)]]")
DUPLICATE_THRESHOLD = 0.85
LINT_REPORT_PATH = OUTPUT_DIR / "lint_report.md"


# ── Data gathering ──────────────────────────────────────────────────────

def _load_article(path: Path) -> tuple[dict, str]:
    """Return (metadata, body) for a wiki article."""
    try:
        post = frontmatter.loads(path.read_text())
        return dict(post.metadata), post.content
    except Exception:
        return {}, path.read_text()


def _gather_articles(directory: Path) -> list[tuple[Path, dict, str]]:
    if not directory.exists():
        return []
    out = []
    for md in sorted(directory.glob("*.md")):
        meta, body = _load_article(md)
        out.append((md, meta, body))
    return out


def _source_refs(meta: dict) -> list[str]:
    """Normalize source_refs / sources / source frontmatter into a list."""
    raw = meta.get("source_refs") or meta.get("sources") or meta.get("source")
    if raw is None:
        return []
    if isinstance(raw, list):
        return [str(r) for r in raw]
    return [str(raw)]


# ── Checks ──────────────────────────────────────────────────────────────

def _check_broken_backlinks(
    all_articles: list[tuple[Path, dict, str]],
    valid_slugs: set[str],
) -> list[tuple[str, str]]:
    """Return list of (source_file, broken_target) pairs."""
    broken: list[tuple[str, str]] = []
    for path, _, body in all_articles:
        for match in WIKILINK_RE.finditer(body):
            target_slug = slugify(match.group(1))
            if target_slug and target_slug not in valid_slugs:
                broken.append((str(path.relative_to(WIKI_DIR)), match.group(1)))
    return broken


def _check_orphan_articles(
    concepts: list[tuple[Path, dict, str]],
    all_articles: list[tuple[Path, dict, str]],
) -> list[str]:
    """Concept articles with zero incoming [[links]] from other wiki files."""
    orphans: list[str] = []
    for path, _, _ in concepts:
        slug = path.stem
        incoming = 0
        for other_path, _, body in all_articles:
            if other_path == path:
                continue
            for match in WIKILINK_RE.finditer(body):
                if slugify(match.group(1)) == slug:
                    incoming += 1
                    break
        if incoming == 0:
            orphans.append(str(path.relative_to(WIKI_DIR)))
    return orphans


def _check_missing_summaries(
    manifest: dict,
    summaries: list[tuple[Path, dict, str]],
) -> list[tuple[str, str]]:
    """Compiled manifest entries with no summary file referencing them.

    A summary references a source if its frontmatter (source / source_refs /
    sources / original_source) contains the raw filename or its original path.
    """
    # Build the set of reference strings used across all summaries
    referenced: set[str] = set()
    for _, meta, _ in summaries:
        for key in ("source", "source_refs", "sources", "original_source"):
            val = meta.get(key)
            if val is None:
                continue
            if isinstance(val, list):
                for v in val:
                    referenced.add(str(v))
            else:
                referenced.add(str(val))

    missing: list[tuple[str, str]] = []
    for raw_name, entry in manifest.items():
        if not entry.get("compiled"):
            continue
        original = entry.get("original_source", "")
        # Match if any referenced value contains the raw filename or original path
        matched = any(
            raw_name in ref or (original and original in ref) or ref in original
            for ref in referenced
        )
        if not matched:
            missing.append((raw_name, original))
    return missing


def _check_stale_articles(
    all_articles: list[tuple[Path, dict, str]],
    manifest: dict,
) -> list[tuple[str, str]]:
    """Articles whose source_refs point to raw files currently marked uncompiled.

    A raw file is marked compiled=false by ingest.py whenever its content hash
    changes on re-ingestion — so an article referencing it is stale.
    """
    stale: list[tuple[str, str]] = []
    for path, meta, _ in all_articles:
        for ref in _source_refs(meta):
            # Match against manifest by raw name or original_source substring
            for raw_name, entry in manifest.items():
                original = entry.get("original_source", "")
                is_match = (
                    raw_name == ref
                    or raw_name in ref
                    or (original and (original == ref or original in ref or ref in original))
                )
                if is_match and not entry.get("compiled", True):
                    stale.append(
                        (str(path.relative_to(WIKI_DIR)), f"raw/{raw_name}")
                    )
                    break
    return stale


def _check_duplicate_concepts(
    concepts: list[tuple[Path, dict, str]],
) -> list[tuple[str, str, float]]:
    """Pairs of concept articles whose titles are >= DUPLICATE_THRESHOLD similar."""
    titles: list[tuple[str, str]] = []  # (rel_path, title)
    for path, meta, _ in concepts:
        title = str(meta.get("title") or path.stem).strip()
        titles.append((str(path.relative_to(WIKI_DIR)), title))

    dupes: list[tuple[str, str, float]] = []
    for i in range(len(titles)):
        for j in range(i + 1, len(titles)):
            a_path, a_title = titles[i]
            b_path, b_title = titles[j]
            ratio = SequenceMatcher(None, a_title.lower(), b_title.lower()).ratio()
            if ratio >= DUPLICATE_THRESHOLD:
                dupes.append((a_path, b_path, ratio))
    return dupes


# ── Report rendering ───────────────────────────────────────────────────

def _format_report(
    broken: list[tuple[str, str]],
    orphans: list[str],
    missing_summaries: list[tuple[str, str]],
    stale: list[tuple[str, str]],
    duplicates: list[tuple[str, str, float]],
    markdown: bool = False,
) -> str:
    """Render the lint report as either terminal text or markdown."""
    h1 = "# " if markdown else ""
    h2 = "## " if markdown else ""
    bullet = "- " if markdown else "  - "

    out: list[str] = []
    out.append(f"{h1}wikimind lint report")
    if not markdown:
        out.append("=" * 40)
    out.append("")

    sections = [
        ("Broken backlinks", broken,
         lambda x: f"{bullet}[[{x[1]}]] in {x[0]}"),
        ("Orphan articles (no incoming links)", orphans,
         lambda x: f"{bullet}{x}"),
        ("Missing summaries (compiled source, no summary)", missing_summaries,
         lambda x: f"{bullet}raw/{x[0]}  <- {x[1]}"),
        ("Stale articles (source re-ingested)", stale,
         lambda x: f"{bullet}{x[0]}  (ref: {x[1]})"),
        ("Duplicate concepts (fuzzy title match ≥ 0.85)", duplicates,
         lambda x: f"{bullet}{x[0]}  ↔  {x[1]}  (similarity: {x[2]:.2f})"),
    ]

    total_issues = 0
    for label, items, fmt in sections:
        out.append(f"{h2}{label} ({len(items)})")
        if items:
            total_issues += len(items)
            for item in items:
                out.append(fmt(item))
        else:
            out.append(f"{bullet}none" if markdown else "  none")
        out.append("")

    if total_issues == 0:
        out.append("All checks passed.")
    else:
        out.append(f"Total issues: {total_issues}")
    out.append("")
    return "\n".join(out)


# ── Entry point ────────────────────────────────────────────────────────

def run_lint(write_output: bool = False) -> None:
    """Run all structural lint checks and print a report."""
    concepts = _gather_articles(CONCEPTS_DIR)
    summaries = _gather_articles(SUMMARIES_DIR)
    all_articles = concepts + summaries
    # Include _index.md and any other top-level wiki files in the scan
    if WIKI_DIR.exists():
        for extra in sorted(WIKI_DIR.glob("*.md")):
            if extra == WIKI_INDEX:
                continue
            meta, body = _load_article(extra)
            all_articles.append((extra, meta, body))

    manifest = load_manifest()

    # Valid backlink targets: any article file anywhere under wiki/
    valid_slugs = {p.stem for p, _, _ in all_articles}

    broken = _check_broken_backlinks(all_articles, valid_slugs)
    orphans = _check_orphan_articles(concepts, all_articles)
    missing = _check_missing_summaries(manifest, summaries)
    stale = _check_stale_articles(all_articles, manifest)
    duplicates = _check_duplicate_concepts(concepts)

    report = _format_report(broken, orphans, missing, stale, duplicates, markdown=False)
    click.echo(report)

    if write_output:
        md_report = _format_report(broken, orphans, missing, stale, duplicates, markdown=True)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        LINT_REPORT_PATH.write_text(md_report)
        click.echo(f"Report written to {LINT_REPORT_PATH.relative_to(WIKI_DIR.parent)}")
