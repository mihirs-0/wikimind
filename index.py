"""Index building logic — generate _index.md from wiki contents.

Pure file parsing — no LLM calls.
"""

import re
from pathlib import Path

import click
import frontmatter

from wikimind.utils import (
    CONCEPTS_DIR,
    SUMMARIES_DIR,
    WIKI_DIR,
    WIKI_INDEX,
)


WIKILINK_RE = re.compile(r"\[\[(.+?)]]")


def _fmt_list(value) -> str:
    """Render a frontmatter field (list or scalar) as a comma-separated string."""
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


def _fmt_date(value) -> str:
    """Render a date/datetime/string field as YYYY-MM-DD."""
    if value is None:
        return ""
    s = str(value)
    # Trim ISO timestamps down to the date portion
    return s[:10]


def _load_posts(directory: Path) -> list[tuple[Path, frontmatter.Post]]:
    """Load and parse all .md files in a directory, sorted by filename."""
    if not directory.exists():
        return []
    posts = []
    for md in sorted(directory.glob("*.md")):
        try:
            post = frontmatter.loads(md.read_text())
        except Exception as exc:
            click.echo(f"  warn: could not parse {md.name}: {exc}")
            continue
        posts.append((md, post))
    return posts


def _count_backlinks() -> int:
    """Count every [[wikilink]] occurrence across all wiki .md files."""
    total = 0
    for md in WIKI_DIR.rglob("*.md"):
        if md == WIKI_INDEX:
            continue
        total += len(WIKILINK_RE.findall(md.read_text()))
    return total


def _concepts_table(posts: list[tuple[Path, frontmatter.Post]]) -> list[str]:
    lines = [
        "| Article | Related Concepts | Sources | Last Updated |",
        "|---------|-----------------|---------|--------------|",
    ]
    for path, post in posts:
        title = post.metadata.get("title") or path.stem.replace("-", " ").title()
        related = _fmt_list(post.metadata.get("related") or post.metadata.get("related_concepts"))
        sources = _fmt_list(post.metadata.get("sources"))
        updated = _fmt_date(post.metadata.get("updated") or post.metadata.get("last_updated"))
        link = f"concepts/{path.name}"
        lines.append(f"| [{title}]({link}) | {related} | {sources} | {updated} |")
    return lines


def _summaries_table(posts: list[tuple[Path, frontmatter.Post]]) -> list[str]:
    lines = [
        "| Summary | Source | Ingested |",
        "|---------|--------|----------|",
    ]
    for path, post in posts:
        title = post.metadata.get("title") or path.stem.replace("-", " ").title()
        source = post.metadata.get("source") or post.metadata.get("original_source") or ""
        ingested = _fmt_date(post.metadata.get("ingested") or post.metadata.get("ingested_at"))
        link = f"summaries/{path.name}"
        lines.append(f"| [{title}]({link}) | {source} | {ingested} |")
    return lines


def run_index() -> None:
    """Rebuild wiki/_index.md from concept + summary frontmatter."""
    concept_posts = _load_posts(CONCEPTS_DIR)
    summary_posts = _load_posts(SUMMARIES_DIR)
    backlink_count = _count_backlinks()

    lines: list[str] = ["# Wiki Index", ""]

    lines.append("## Concepts")
    lines.append("")
    if concept_posts:
        lines.extend(_concepts_table(concept_posts))
    else:
        lines.append("_No concept articles yet._")
    lines.append("")

    lines.append("## Summaries")
    lines.append("")
    if summary_posts:
        lines.extend(_summaries_table(summary_posts))
    else:
        lines.append("_No summaries yet._")
    lines.append("")

    lines.append("## Statistics")
    lines.append(f"- Total concepts: {len(concept_posts)}")
    lines.append(f"- Total summaries: {len(summary_posts)}")
    lines.append(f"- Total backlinks: {backlink_count}")
    lines.append("")

    WIKI_INDEX.parent.mkdir(parents=True, exist_ok=True)
    WIKI_INDEX.write_text("\n".join(lines))
    click.echo(
        f"Wrote {WIKI_INDEX.relative_to(WIKI_DIR.parent)} "
        f"({len(concept_posts)} concepts, {len(summary_posts)} summaries, "
        f"{backlink_count} backlinks)."
    )
