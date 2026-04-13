"""Click-based CLI entry point for wikimind."""

import re

import click

from wikimind.ingest import run_ingest
from wikimind.index import run_index
from wikimind.search import run_search
from wikimind.lint import run_lint
from wikimind.utils import (
    CONCEPTS_DIR,
    SUMMARIES_DIR,
    WIKI_DIR,
    load_manifest,
    slugify,
)


@click.group()
def cli():
    """wikimind — a personal wiki builder powered by LLMs."""


@cli.command()
@click.argument("sources", nargs=-1, required=True, type=click.Path(exists=True))
def ingest(sources: tuple[str, ...]):
    """Ingest one or more source files or directories into raw/."""
    run_ingest(sources)


@cli.command()
def status():
    """Show the current state of the wiki."""
    manifest = load_manifest()

    # ── Sources ─────────────────────────────────────────────────────
    total_sources = len(manifest)
    uncompiled = [name for name, e in manifest.items() if not e.get("compiled")]
    stale = [name for name, e in manifest.items()
             if e.get("compiled") and not e.get("compiled_hash_matches", True)]

    # ── Wiki articles & summaries ───────────────────────────────────
    concept_files = sorted(CONCEPTS_DIR.glob("*.md")) if CONCEPTS_DIR.exists() else []
    summary_files = sorted(SUMMARIES_DIR.glob("*.md")) if SUMMARIES_DIR.exists() else []

    # ── Orphan detection ────────────────────────────────────────────
    # Collect all concept slugs (stems) that have articles
    concept_slugs = {f.stem for f in concept_files}

    # Scan every .md under wiki/ for [[wikilinks]] and find unresolved ones
    link_re = re.compile(r"\[\[(.+?)]]")
    orphans: dict[str, list[str]] = {}  # missing_slug -> list of files referencing it
    for md in WIKI_DIR.rglob("*.md"):
        text = md.read_text()
        for match in link_re.finditer(text):
            target = slugify(match.group(1))
            if target and target not in concept_slugs:
                orphans.setdefault(target, []).append(
                    str(md.relative_to(WIKI_DIR))
                )

    # ── Stale detection ─────────────────────────────────────────────
    # Sources that were re-ingested (hash changed) since last compile:
    # these are the ones marked compiled=False that previously had compiled=True,
    # but more practically, any source with compiled=false is either new or stale.
    # We report uncompiled sources and let the user decide.
    stale_sources = [
        (name, e["original_source"])
        for name, e in manifest.items()
        if not e.get("compiled")
    ]

    # ── Render report ───────────────────────────────────────────────
    click.echo("wikimind status")
    click.echo("=" * 40)

    click.echo(f"\n  Sources ingested:    {total_sources}")
    click.echo(f"  Awaiting compile:    {len(uncompiled)}")
    click.echo(f"  Wiki articles:       {len(concept_files)}")
    click.echo(f"  Summaries:           {len(summary_files)}")

    if stale_sources:
        click.echo(f"\n  Stale / uncompiled sources ({len(stale_sources)}):")
        for raw_name, orig in stale_sources:
            click.echo(f"    - raw/{raw_name}  <- {orig}")

    if orphans:
        click.echo(f"\n  Orphan links ({len(orphans)}):")
        for slug, refs in sorted(orphans.items()):
            ref_list = ", ".join(refs)
            click.echo(f"    - [[{slug}]]  referenced in: {ref_list}")

    if not stale_sources and not orphans:
        click.echo("\n  No issues found.")

    click.echo()


@cli.command()
def index():
    """Rebuild the wiki index."""
    run_index()


@cli.command()
@click.argument("query", required=False)
@click.option("--top-k", default=5, show_default=True, help="Number of results.")
@click.option("--serve", is_flag=True, help="Start the web UI instead of a one-shot search.")
@click.option("--port", default=8080, show_default=True, help="Port for --serve.")
def search(query: str | None, top_k: int, serve: bool, port: int):
    """Search the wiki using BM25."""
    if serve:
        run_search(None, top_k=top_k, serve=True, port=port)
        return
    if not query:
        raise click.UsageError("QUERY is required unless --serve is passed.")
    run_search(query, top_k=top_k, serve=False, port=port)


@cli.command()
@click.option("--output", "output", is_flag=True,
              help="Also write report to output/lint_report.md.")
def lint(output: bool):
    """Run structural lint checks on the wiki."""
    run_lint(write_output=output)


if __name__ == "__main__":
    cli()
