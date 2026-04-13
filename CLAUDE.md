# CLAUDE.md

Instructions for Claude Code when working in the wikimind project.

## Project Overview

wikimind is a personal LLM knowledge base system. Raw source documents are ingested into `raw/`, then an LLM (you, Claude Code) compiles them into a structured markdown wiki in `wiki/`. The wiki is viewed in Obsidian. **The LLM maintains the wiki — the human rarely edits it directly.**

Your job is to read raw sources, extract concepts, write dense technical articles, and keep the wiki internally consistent. The CLI tools handle infrastructure (ingestion, indexing, search, linting). You handle everything that requires reading and judgment.

## Directory Structure

```
wikimind/
├── cli.py              # Click entry point — dispatches to modules below
├── ingest.py           # Source ingestion (PDF, HTML, MD, TXT → raw/)
├── index.py            # Rebuilds wiki/_index.md from frontmatter
├── search.py           # BM25 search (CLI and Flask web UI)
├── lint.py             # Structural lint checks
├── utils.py            # Shared helpers and path constants
├── raw/                # Ingested source documents (LLM reads, CLI writes)
│   └── _manifest.json  # Tracks original_source, hash, compiled flag per raw file
├── wiki/               # The compiled wiki (LLM writes, human reads)
│   ├── _index.md       # Auto-generated master index — do NOT edit by hand
│   ├── concepts/       # Concept articles — thorough, cross-linked
│   ├── summaries/      # Per-source summaries — concise (<500 words)
│   └── queries/        # Filed query answers (from --file-back)
└── output/             # Generated reports, slides, charts
```

## How to Compile Sources

When the user asks you to **"compile"** new sources, follow this workflow exactly:

1. Run `python cli.py status` to see what's uncompiled.
2. Read each uncompiled source file in `raw/`.
3. Read `wiki/_index.md` to understand what concepts already exist.
4. For each new source:
   a. Write a summary to `wiki/summaries/<slugified-title>.md` with frontmatter: `title`, `source`, `ingested_at`, `tags`.
   b. Identify key concepts. For each concept:
      - If `wiki/concepts/<concept>.md` exists: **UPDATE** it — append new information, add the source to `source_refs`, don't duplicate existing content.
      - If it doesn't exist: **CREATE** it.
   c. Every concept article must have this frontmatter: `title`, `related_concepts` (list), `source_refs` (list), `last_updated`.
   d. Use Obsidian `[[wiki-links]]` for every cross-reference between concepts.
   e. Write in clear, dense, technical prose. No fluff. Include specific numbers, equations, findings.
5. Run `python cli.py index` to rebuild `_index.md`.
6. Run `python cli.py lint` to catch broken links and orphans.
7. Fix any issues lint reports.
8. Update `raw/_manifest.json` — set `compiled: true` for all processed sources.

## How to Answer Queries

When the user asks a question:

1. Read `wiki/_index.md` first.
2. Identify relevant articles — be selective, don't load everything.
3. Read those articles.
4. If the index doesn't surface something, use `python cli.py search "terms"` to find it.
5. Synthesize an answer with specific citations to wiki articles (e.g. "per [[attention]]...").
6. If the user says `--file-back` or "save this": write the answer to `wiki/queries/<slugified-question>.md` with frontmatter `title`, `question`, `related_concepts`, `created_at`. Then run `python cli.py index`.

## How to Lint (Deep)

When the user asks for a **"deep lint"** or **"find contradictions"**:

1. Run `python cli.py lint` for structural issues first.
2. Read clusters of related articles — use each article's `related_concepts` to find the cluster.
3. Look for:
   - Contradictory claims across articles
   - Outdated information (check `last_updated` against newer sources)
   - Concepts that should be linked but aren't
   - Gaps where a connecting concept article would help
4. Write a report to `output/deep_lint_report.md`.
5. **Ask the user which fixes to apply before making changes.**

## Article Format Convention

Every `.md` file in `wiki/` must start with YAML frontmatter fenced by `---`. Example:

```markdown
---
title: "Saddle Point Escape in Transformer Training"
related_concepts: ["gradient_noise", "plateau_duration", "marginals_before_conditionals"]
source_refs: ["raw/karpathy2026_learning_dynamics.md", "raw/ziyin2025_entropic_force.md"]
last_updated: 2026-04-13
tags: ["optimization", "training_dynamics"]
---

# Saddle Point Escape in Transformer Training

Article content with [[gradient_noise]] backlinks inline on first mention.

## Key Findings

Dense technical content...

## Open Questions

What remains unknown...
```

## Backlinks Convention

- Use `[[concept_name]]` format (Obsidian-compatible).
- The filename must match the link: `[[gradient_noise]]` → `wiki/concepts/gradient_noise.md`.
- Use `snake_case` for filenames and links.
- Always link on first mention in an article. Don't over-link (one link per concept per article is enough).

## Output Formats

When asked to produce artifacts, save them under `output/`:

- **Markdown reports** → `output/<name>.md`
- **Marp slides** → `output/<name>.md` with frontmatter `marp: true`, `theme: default`
- **Charts** → generate with matplotlib, save `.png` to `output/`, reference from `.md` files
- **Always tell the user the file path** after writing.

## CLI Reference

- `python cli.py ingest <path>...` — ingest files or directories into `raw/`
- `python cli.py status` — show wiki health overview
- `python cli.py index` — rebuild `wiki/_index.md` from frontmatter
- `python cli.py search "query" --top-k 5` — BM25 search
- `python cli.py search --serve --port 8080` — web search UI
- `python cli.py lint` — structural health checks
- `python cli.py lint --output` — also save report to `output/lint_report.md`

## Rules

1. **Never delete wiki articles without asking the user.**
2. Always run `index` after creating or modifying articles.
3. Always run `lint` after a compile pass.
4. When updating an existing article, **preserve existing content — append, don't overwrite.**
5. Keep summaries concise (under 500 words). Concept articles have no upper limit — be thorough.
6. If a source contradicts existing wiki content, flag it under an `## Open Questions` or `## Contradictions` section rather than silently overwriting.
