# wikimind

**LLM-compiled personal knowledge bases in plain markdown.**

> Inspired by Andrej Karpathy's post on using LLMs to build personal knowledge bases.

## Overview

Drop raw sources (PDFs, HTML, notes) into `raw/`. An LLM (Claude Code) reads them and compiles a structured wiki of concept articles and summaries into `wiki/`. You view and navigate the wiki in Obsidian, querying it through the same LLM. Query outputs can be filed back into the wiki, so the knowledge base grows as you use it.

No vector DB, no embeddings, no RAG pipeline. Just markdown files and an LLM that can read and write them. The wiki is the LLM's domain — you rarely edit it manually.

## Architecture

```
  raw sources  ──►  ingest CLI  ──►  raw/  ──►  LLM compile  ──►  wiki/  ──►  Obsidian (view)
                                                                     │
                                                                     ▼
                                                        query / lint / search
                                                                     │
                                                                     ▼
                                                          output/  ──►  (file back into wiki/)
```

| Component     | Type          | Role                                                        |
|---------------|---------------|-------------------------------------------------------------|
| **ingest**    | CLI tool      | Pulls PDFs/HTML/MD/TXT into `raw/` with a content manifest  |
| **compile**   | LLM (Claude)  | Reads `raw/`, writes concept articles and summaries to `wiki/` |
| **index**     | CLI tool      | Regenerates `wiki/_index.md` from frontmatter               |
| **search**    | CLI tool      | BM25 search (terminal or minimal web UI)                    |
| **lint**      | CLI tool      | Structural checks: broken links, orphans, stale articles    |
| **query**     | LLM (Claude)  | Answers questions using the wiki as context                 |
| **deep lint** | LLM (Claude)  | Finds contradictions and conceptual gaps across articles    |

CLI tools handle infrastructure. The LLM handles everything that requires reading and judgment.

## Quickstart

```bash
# 1. Clone
git clone <repo-url> && cd wikimind

# 2. Install
pip install -e .

# 3. Point Obsidian at the project root (or the wiki/ subdirectory)
#    File → Open vault → select this directory

# 4. Ingest your first sources
python cli.py ingest ./my_papers/

# 5. Check what's uncompiled
python cli.py status

# 6. Open Claude Code in the repo and tell it: "compile the new sources"

# 7. Rebuild the index
python cli.py index

# 8. Open Obsidian and explore the graph view
```

## CLI Reference

### `ingest`

Pull source documents into `raw/`. Supports `.md`, `.txt`, `.pdf`, `.html`. Directories are walked recursively.

```bash
python cli.py ingest paper.pdf                   # single file
python cli.py ingest ./papers/ ./notes/          # multiple directories
python cli.py ingest ~/Downloads/article.html    # HTML → markdown via trafilatura
python cli.py ingest thesis.pdf                  # PDF → markdown via pymupdf4llm
```

Re-ingesting an unchanged file is a no-op. If content changes, the raw copy is updated and the manifest's `compiled` flag is reset to `false` so you know it needs recompiling.

### `status`

Health overview: source counts, uncompiled sources, orphan links.

```bash
python cli.py status
```

### `index`

Rebuilds `wiki/_index.md` from the YAML frontmatter of every article. Pure parsing — no LLM.

```bash
python cli.py index
```

### `search`

BM25 ranking over all articles in `wiki/concepts/`, `wiki/summaries/`, `wiki/queries/`.

```bash
python cli.py search "attention mechanism" --top-k 5
python cli.py search --serve --port 8080          # web UI
```

The BM25 index is cached at `wiki/.search_cache.pkl` and rebuilt automatically when any wiki file changes.

### `lint`

Five structural checks: broken backlinks, orphan articles, missing summaries, stale articles, duplicate concepts (fuzzy title match ≥ 0.85).

```bash
python cli.py lint               # terminal report
python cli.py lint --output      # also writes output/lint_report.md
```

## The LLM Workflow

The CLI handles infrastructure. **Claude Code handles intelligence.** Open Claude Code in the repo and prompt it naturally — it reads `CLAUDE.md` and follows the project's conventions.

### Compiling sources

```
compile the new sources
compile raw/attention-paper.md into the wiki
recompile everything — I've updated the source files
```

### Querying the wiki

```
what does the wiki say about saddle point escape during training?
compare gradient noise and learning rate schedules — file this back
summarize everything related to [[attention]]
```

### Deep linting

```
find contradictions between articles in the optimization cluster
do a deep lint and save the report
which concepts are missing connector articles?
```

### Output generation

```
make Marp slides on transformer training dynamics
generate a chart of loss curves from the papers in raw/
write a one-page report on the RAG-vs-finetuning tradeoff
```

## Obsidian Setup

1. Open Obsidian → **File → Open vault** → point at either the project root or the `wiki/` subdirectory.
2. Recommended plugins:
   - **Graph view** (built-in) — visualize `[[wiki-link]]` connections
   - **Dataview** — query article frontmatter (`tags`, `source_refs`, etc.)
   - **Marp Slides** — render `output/*.md` Marp decks inline
3. The `[[snake_case]]` link convention used by wikimind is native to Obsidian — backlinks, graph view, and quick-switch all work out of the box.

## Design Philosophy

- **Plain markdown over proprietary formats.** The wiki outlives any tool.
- **No embeddings or vector DB at small scale.** An index file + LLM context is enough for hundreds of articles.
- **Incremental compilation.** Content-hash manifest means only what changed gets reprocessed.
- **The wiki is the LLM's artifact.** Humans read and query; the LLM writes.
- **Query outputs feed back into the wiki.** The knowledge base grows as it's used — a flywheel.
- **Tools stay simple.** The LLM is the intelligence layer; the CLI stays dumb.

## Limitations

- **Scale ceiling.** Around 500 articles the `_index.md` plus frontmatter exceeds a comfortable context window. Past that point, hierarchical indexing or retrieval becomes necessary.
- **No image handling yet.** Figures are lost during PDF extraction.
- **Compile quality depends on the LLM.** Ambiguous or sprawling sources can produce poorly scoped articles.
- **No automated compile pipeline.** Every compile pass requires prompting Claude Code manually.
- **No version control built in.** Use `git` on the `wiki/` directory if you care about history.

## Future Work

- Image extraction and referencing from PDFs
- Hierarchical indexing for larger wikis (topic-level indexes pointing at concept-level indexes)
- Automated compile via API (optional "Path A" mode that runs unattended)
- Richer Marp slide generation tooling
- Synthetic data generation for finetuning from the compiled wiki
- Multi-wiki support — separate knowledge bases per project

## License

MIT
