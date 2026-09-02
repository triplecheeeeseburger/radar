# Dan's Radar

Weekly curated signal feed (AI, frontier models, web dev, browsers, cybersec, agentic workflows), published at **radar.danberte.com**. Static site, zero backend, design matched to danberte.com.

## How it works

1. **Ingest** — Paste links (X threads, articles) into a Cowork chat with Claude, anytime.
2. **Curate** — Claude pulls the content (via your Chrome extension for X, since X blocks server-side fetches; or you paste the thread text), then writes a "why it matters" blurb, scores it, tags topics, and cross-links overlapping threads.
3. **Publish** — Claude updates `data/links.json` and commits via the GitHub API; Actions rebuilds and deploys Pages automatically. `week` is always the Monday of the week the signal is ADDED, regardless of when the underlying story happened — a signal curated today belongs on today's page, not retroactively filed under whichever week the news broke. **On Mondays specifically: before filing anything, check TODAY'S ACTUAL DATE (not the last key in `data.weeks`) against what build.py's live current-week logic would compute.** If today is Monday, the current week may have already rolled over to a new Monday with zero entries yet — signals curated that day belong in the brand-new week, not the one that just closed. Getting this wrong misfiles fresh signals into an already-archived week and corrupts that week's TL;DR. This happened 2026-08-31 and was caught and fixed after the fact — see RADAR-DEVLOG.md v1.9. Never again: always verify today's date first.
4. **Archive** — Weeks run Monday–Sunday; cut Monday AM. Every week gets a permanent page under `/archive/`; `index.html` always shows the current week.

## Scoring rubric (0–10) — strategic lens

Ranking and the executive summary are read through an **Opera Neon product-strategy lens**. Signals are weighted by what they mean for agentic workflows, agentic browsers, and the larger ecosystem — with direct threats or benefits to Opera Neon ranking highest, because those inform strategic decisions inside the product.

- **Opera Neon impact** — direct threat or benefit: competitor moves, platform plays that erode/strengthen Neon's position, house wins (0–4)
- **Agentic workflows & agentic browsing impact** — changes to how agents drive the web (0–3)
- **Ecosystem shift & durability** — payment rails, protocols, model access, developer behavior (0–3)

Overlapping threads are cross-referenced ("↔ overlaps") and their scores weighed relative to each other within the week.

## Published-text style (applies to TL;DR and blurbs)

- **Factual and compressed.** A reader should be up to speed from one glance. No flamboyance, no editorializing, no scene-setting openers.
- **Never announce the objective.** The strategic lens governs scoring and ordering only; published text never mentions that ranking serves Opera Neon strategy, and never contains internal product-strategy language ("house win", "worth evaluating as a play"). The site is public.
- **TL;DR** opens with one succinct, high-level conclusion sentence about the week — measured, not tabloid. Never claim an unverifiable superlative ("the most X yet"); hedge instead ("more consequential than usual", "a quieter week for X"). After the conclusion, 2-4 more sentences covering only the week's main threads at a high level — not a walk through every signal. Target well under 100 words even as signal counts grow past 10+ per week. (Reworked 2026-08-29 per Dan's call: the old one-paragraph-per-signal convention, ~120-150 words, got too long as weeks grew past 10 signals. See RADAR-DEVLOG.md v1.8.)
- **Blurbs** stay in normal editorial prose (not STE) but are half the length of the original convention — roughly 25–35 words, one to two sentences. State the facts, then the implication if there's room, worded neutrally (e.g. "differentiation shifts to…", "a pattern other vendors are likely to copy"). Decided via an in-chat style test on 2026-08-03; see devlog v1.4.
- **Dan's take** (optional, per entry) is personal commentary, kept separate from the blurb and visually labeled as opinion. Unlike the TL;DR/blurb, it may reference Opera Neon or product strategy directly — the neutrality rule above applies only to the factual summary, not to Dan's own stated opinion.
- **No em dashes.** Never use — (em dash) anywhere in published text (TL;DR, blurbs, titles). Use a comma, colon, period, or restructure the sentence instead. Removed from week 2026-08-31's TL;DR and permanently banned 2026-09-01 per Dan's call.
- **Bold hook words in the TL;DR only.** Mark a few (rare, not every sentence) key 1-2 word hooks per TL;DR using markdown `**word**` syntax — build.py renders these as `<strong>` in HTML; the Markdown export renders them natively since it's already markdown. Never applied to blurbs or titles. One to two words per bolded span, sparingly. Added 2026-09-01.

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
  "week": "2026-07-10",            // Monday of the week it was ADDED/published (not the event date) — always the current week at curation time, so it shows on the front page, not buried in the archive
  "topics": ["ai", "browsers"],
  "score": 8.4,                     // null while pending
  "status": "curated",              // or "pending"
  "blurb": "Why it matters: …",
  "take": "Dan's personal commentary — optional, may mention Neon/strategy directly",
  "related": ["other-entry-id"]
}
```
