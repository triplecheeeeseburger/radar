# Dan's Radar

Weekly curated signal feed (AI, frontier models, web dev, browsers, cybersec, agentic workflows), published at **radar.danberte.com**. Static site, zero backend, design matched to danberte.com.

## How it works

1. **Ingest** — Paste links (X threads, articles) into a Cowork chat with Claude, anytime.
2. **Curate** — Claude pulls the content (via your Chrome extension for X, since X blocks server-side fetches; or you paste the thread text), then writes a "why it matters" blurb, scores it, tags topics, and cross-links overlapping threads.
3. **Publish** — Claude updates `data/links.json` and commits via the GitHub API; Actions rebuilds and deploys Pages automatically.
4. **Archive** — Weeks cut Friday PM. Every week gets a permanent page under `/archive/`; `index.html` always shows the current week.

## Scoring rubric (0–10) — strategic lens

Ranking and the executive summary are read through an **Opera Neon product-strategy lens**. Signals are weighted by what they mean for agentic workflows, agentic browsers, and the larger ecosystem — with direct threats or benefits to Opera Neon ranking highest, because those inform strategic decisions inside the product.

- **Opera Neon impact** — direct threat or benefit: competitor moves, platform plays that erode/strengthen Neon's position, house wins (0–4)
- **Agentic workflows & agentic browsing impact** — changes to how agents drive the web (0–3)
- **Ecosystem shift & durability** — payment rails, protocols, model access, developer behavior (0–3)

Overlapping threads are cross-referenced ("↔ overlaps") and their scores weighed relative to each other within the week.

## Published-text style (applies to TL;DR and blurbs)

- **Factual and compressed.** A reader should be up to speed from one glance. No flamboyance, no editorializing, no scene-setting openers.
- **Never announce the objective.** The strategic lens governs scoring and ordering only; published text never mentions that ranking serves Opera Neon strategy, and never contains internal product-strategy language ("house win", "worth evaluating as a play"). The site is public.
- **TL;DR** = one paragraph of plain declarative sentences covering every signal, ordered roughly by rank, ending with any caution/caveat item. Target under ~120 words — written for a decision-maker in a rush; keep only what a reader needs to understand and act on each signal.
- **Blurbs** state the facts, then the implication, worded neutrally (e.g. "differentiation shifts to…", "a pattern other vendors are likely to copy").

## Files

- `data/links.json` — single source of truth (site config + all entries)
- `build.py` — stdlib-only generator: `index.html`, `archive/index.html`, `archive/<week>.html`
- `.github/workflows/build.yml` — CI: rebuilds and deploys Pages on every push
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
