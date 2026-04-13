"""BM25 search over wiki articles — CLI and web UI."""

import pickle
import re
from pathlib import Path
from urllib.parse import quote

import click
import frontmatter
from rank_bm25 import BM25Okapi

from wikimind.utils import WIKI_DIR

SEARCH_CACHE = WIKI_DIR / ".search_cache.pkl"
TOKEN_RE = re.compile(r"[a-z0-9]+")
SEARCH_ROOTS = ("concepts", "summaries", "queries")


# ── Tokenization & indexing ─────────────────────────────────────────────

def _tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def _iter_wiki_files() -> list[Path]:
    """All .md files under the searchable wiki subdirs."""
    files: list[Path] = []
    for sub in SEARCH_ROOTS:
        d = WIKI_DIR / sub
        if d.exists():
            files.extend(sorted(d.rglob("*.md")))
    return files


def _cache_is_stale(files: list[Path]) -> bool:
    if not SEARCH_CACHE.exists():
        return True
    cache_mtime = SEARCH_CACHE.stat().st_mtime
    return any(f.stat().st_mtime > cache_mtime for f in files)


def _build_index(files: list[Path]) -> dict:
    """Parse each file, tokenize, build BM25 model, capture display metadata."""
    tokens: list[list[str]] = []
    records: list[dict] = []
    for path in files:
        raw = path.read_text()
        try:
            post = frontmatter.loads(raw)
            body = post.content
            title = post.metadata.get("title") or path.stem.replace("-", " ").title()
        except Exception:
            body = raw
            title = path.stem.replace("-", " ").title()

        tokens.append(_tokenize(f"{title}\n{body}"))
        snippet = body.strip().replace("\n", " ")[:200]
        records.append(
            {
                "path": str(path),
                "rel_path": str(path.relative_to(WIKI_DIR)),
                "title": title,
                "snippet": snippet,
            }
        )

    bm25 = BM25Okapi(tokens)
    return {"bm25": bm25, "records": records}


def _load_or_build_index() -> dict:
    files = _iter_wiki_files()
    if not files:
        return {"bm25": None, "records": []}

    if _cache_is_stale(files):
        index = _build_index(files)
        SEARCH_CACHE.write_bytes(pickle.dumps(index))
        return index

    try:
        return pickle.loads(SEARCH_CACHE.read_bytes())
    except Exception:
        # Corrupt cache — rebuild
        index = _build_index(files)
        SEARCH_CACHE.write_bytes(pickle.dumps(index))
        return index


def _search(query: str, top_k: int) -> list[dict]:
    index = _load_or_build_index()
    if not index["records"] or index["bm25"] is None:
        return []

    tokens = _tokenize(query)
    if not tokens:
        return []

    scores = index["bm25"].get_scores(tokens)
    ranked = sorted(
        zip(scores, index["records"]), key=lambda x: x[0], reverse=True
    )
    results = []
    for score, rec in ranked[:top_k]:
        if score <= 0:
            break
        results.append({**rec, "score": float(score)})
    return results


# ── CLI output ──────────────────────────────────────────────────────────

def _print_results(query: str, results: list[dict]) -> None:
    if not results:
        click.echo(f'No matches for "{query}".')
        return

    click.echo(f'Top {len(results)} results for "{query}":\n')
    for i, r in enumerate(results, 1):
        click.echo(f"{i}. {r['title']}  [{r['rel_path']}]  (score: {r['score']:.3f})")
        click.echo(f"   {r['snippet']}\n")


# ── Web UI ──────────────────────────────────────────────────────────────

_PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>wikimind search</title>
<style>
  body { font: 16px -apple-system, system-ui, sans-serif; max-width: 760px;
         margin: 2rem auto; padding: 0 1rem; color: #222; }
  h1 { font-size: 1.4rem; margin-bottom: 1rem; }
  form { display: flex; gap: .5rem; margin-bottom: 1.5rem; }
  input[type=text] { flex: 1; padding: .55rem .7rem; font-size: 1rem;
                     border: 1px solid #bbb; border-radius: 4px; }
  button { padding: .55rem 1rem; font-size: 1rem; border: 0;
           background: #2a6df4; color: #fff; border-radius: 4px; cursor: pointer; }
  .result { border-bottom: 1px solid #eee; padding: .9rem 0; }
  .result h3 { margin: 0 0 .2rem; font-size: 1.05rem; }
  .result .meta { color: #888; font-size: .85rem; margin-bottom: .3rem; }
  .result .snippet { color: #444; }
  .empty { color: #888; font-style: italic; }
  a { color: #2a6df4; text-decoration: none; }
  a:hover { text-decoration: underline; }
</style></head>
<body>
  <h1>wikimind search</h1>
  <form method="get" action="/">
    <input type="text" name="q" value="{{ query|e }}" placeholder="Search the wiki..." autofocus>
    <button type="submit">Search</button>
  </form>
  {% if query %}
    {% if results %}
      <p class="meta">{{ results|length }} result(s) for <b>{{ query|e }}</b></p>
      {% for r in results %}
        <div class="result">
          <h3><a href="{{ r.obsidian_url }}">{{ r.title }}</a></h3>
          <div class="meta">{{ r.rel_path }} &middot; score {{ '%.3f' % r.score }}</div>
          <div class="snippet">{{ r.snippet }}</div>
        </div>
      {% endfor %}
    {% else %}
      <p class="empty">No matches.</p>
    {% endif %}
  {% endif %}
</body></html>"""


def _serve(port: int) -> None:
    from flask import Flask, render_template_string, request

    app = Flask(__name__)

    @app.route("/")
    def home():
        query = (request.args.get("q") or "").strip()
        top_k = int(request.args.get("k") or 10)
        results = _search(query, top_k) if query else []
        for r in results:
            # Obsidian URI scheme — opens the file in the user's vault
            r["obsidian_url"] = f"obsidian://open?path={quote(r['path'])}"
        return render_template_string(_PAGE, query=query, results=results)

    click.echo(f"Serving wikimind search on http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=False)


# ── Entry point ────────────────────────────────────────────────────────

def run_search(query: str | None, top_k: int = 5, serve: bool = False, port: int = 8080) -> None:
    if serve:
        _serve(port)
        return
    results = _search(query or "", top_k)
    _print_results(query or "", results)
