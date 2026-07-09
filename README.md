# Dan's Radar

Weekly curated signal feed (AI, frontier models, web dev, browsers, cybersec, agentic workflows), published at **radar.danberte.com**. Static site, zero backend, design matched to danberte.com.

## How it works

1. **Ingest** — Paste links (X threads, articles) into a Cowork chat with Claude, anytime.
2. **Curate** — Claude pulls the content (via your Chrome extension for X, since X blocks server-side fetches; or you paste the thread text), then writes a "why it matters" blurb, scores it, tags topics, and cross-links overlapping threads.
3. **Publish** — Claude updates `data/links.json`, runs `python3 build.py`, and pushes to GitHub. Pages redeploys in ~1 min.
4. **Archive** — Weeks cut Friday PM. Every week gets a permanent page under `/archive/`; `index.html` always shows the current week.

## Scoring rubric (0–10)

- Relevance to our space (0–4)
- Novelty vs. what we've already shared (0–3)
- Likely impact / durability (0–3)

Overlapping threads are cross-referenced ("↔ overlaps") and their scores weighed relative to each other within the week.

## Files

- `data/links.json` — single source of truth (site config + all entries)
- `build.py` — stdlib-only generator: `index.html`, `archive/index.html`, `archive/<week>.html`
- `CNAME` — custom domain for GitHub Pages

## Content-first rule for X entries

The **title is a summary of what the tweet/thread actually says** (its core claim or finding) — never "Thread by @handle". The blurb adds the "why it matters" layer. The author appears only in the small meta line (`X · @handle · day`). Claude paraphrases rather than quoting at length.

## Entry schema

```json
{
  "id": "2026-07-05-omoore-thread",
  "url": "https://x.com/...",
  "title": "…", "author": "@handle", "source": "X",
  "added": "2026-07-09", "posted": "2026-07-05",
  "week": "2026-07-10",            // Friday cut date of its week
  "topics": ["ai", "browsers"],
  "score": 8.4,                     // null while pending
  "status": "curated",              // or "pending"
  "blurb": "Why it matters: …",
  "related": ["other-entry-id"]
}
```

Sample entries (marked `"sample": true`, rendered with a SAMPLE pill) demo the design — delete them before first real publish.
