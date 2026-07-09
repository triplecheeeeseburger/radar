#!/usr/bin/env python3
"""Dan's Radar — static site builder.

Reads data/links.json, writes:
  index.html            current (latest) week, ranked
  archive/index.html    list of all past weeks
  archive/<week>.html   snapshot per past week

Design system mirrors danberte.com (Libre Baskerville + DM Sans,
hairline rules, item-row lists). No dependencies beyond stdlib.
"""
import json, html, datetime, pathlib, collections

ROOT = pathlib.Path(__file__).parent
DATA = json.loads((ROOT / "data" / "links.json").read_text())
SITE = DATA["site"]

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --black: #0d0d0d; --gray: #6b6b6b; --mid: #999; --rule: #e0e0e0; --bg-subtle: #f6f5f2;
  --serif: 'Libre Baskerville', Georgia, serif; --sans: 'DM Sans', system-ui, sans-serif;
  --mono: 'SF Mono','Fira Code','Courier New',monospace;
}
html { scroll-behavior: smooth; }
body { background: #fff; color: var(--black); font-family: var(--sans); font-size: 15px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
nav { position: fixed; top: 0; left: 0; right: 0; z-index: 100; display: flex; align-items: center; justify-content: space-between; padding: 16px 52px; background: rgba(255,255,255,0.95); backdrop-filter: blur(16px); border-bottom: 1px solid var(--rule); }
.nav-name { font-family: var(--serif); font-size: 15px; letter-spacing: 0.01em; text-decoration: none; color: var(--black); }
nav ul { list-style: none; display: flex; gap: 28px; }
nav ul a { font-size: 11px; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; text-decoration: none; color: var(--gray); transition: color 0.18s; }
nav ul a:hover { color: var(--black); }
main { max-width: 900px; margin: 0 auto; padding: 0 48px; }
section { padding: 64px 0; border-bottom: 1px solid var(--rule); }
section:last-child { border-bottom: none; }
.section-label { font-size: 10px; font-weight: 500; letter-spacing: 0.16em; text-transform: uppercase; color: var(--mid); margin-bottom: 36px; }
.masthead { padding-top: 140px; }
.hero-name { font-family: var(--serif); font-size: clamp(34px, 4.6vw, 52px); font-weight: 700; line-height: 1.05; letter-spacing: -0.025em; margin-bottom: 10px; animation: fadeUp 0.6s ease both; }
.hero-title { font-family: var(--serif); font-style: italic; font-size: 15px; color: var(--gray); line-height: 1.6; max-width: 640px; animation: fadeUp 0.6s 0.09s ease both; }
.week-label { font-size: 11px; font-weight: 500; letter-spacing: 0.16em; text-transform: uppercase; color: var(--black); animation: fadeUp 0.6s ease both; }
.tldr-label { font-size: 10px; font-weight: 500; letter-spacing: 0.16em; text-transform: uppercase; color: var(--mid); margin-top: 40px; animation: fadeUp 0.6s 0.09s ease both; }
.tldr { font-family: var(--serif); font-size: 14.5px; line-height: 1.85; color: #2d2d2d; max-width: 720px; margin-top: 14px; animation: fadeUp 0.6s 0.15s ease both; }
.item-list { display: flex; flex-direction: column; }
.entry { display: grid; grid-template-columns: 34px 1fr auto; align-items: baseline; gap: 18px; padding: 17px 0; border-bottom: 1px solid var(--rule); text-decoration: none; color: inherit; transition: opacity 0.16s; }
.entry:first-child { border-top: 1px solid var(--rule); }
.entry:hover { opacity: 0.45; }
.rank { font-family: var(--mono); font-size: 12px; color: var(--mid); }
.entry-title { font-family: var(--serif); font-size: 15px; line-height: 1.5; }
.entry-blurb { display: block; font-size: 12.5px; color: var(--gray); font-style: italic; margin-top: 5px; line-height: 1.65; font-family: var(--sans); }
.entry-topics { display: block; margin-top: 7px; }
.topic-pill { display: inline-block; font-size: 9.5px; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: var(--gray); border: 1px solid var(--rule); border-radius: 3px; padding: 2px 7px; margin-right: 5px; background: #fafafa; }
.topic-pill.sample { color: #b06000; border-color: #e1dcc4; background: #fdf6ea; }
.entry-meta { text-align: right; white-space: nowrap; }
.entry-meta .src { display: block; font-size: 11px; color: var(--mid); }
.score { display: block; font-family: var(--mono); font-size: 13px; color: var(--black); margin-top: 4px; }
.score.pending { color: var(--mid); }
.related-note { display: block; font-size: 11px; color: var(--mid); margin-top: 5px; }
.week-row { display: grid; grid-template-columns: 1fr auto; align-items: baseline; gap: 20px; padding: 14px 0; border-bottom: 1px solid var(--rule); text-decoration: none; color: inherit; transition: opacity 0.16s; }
.week-row:first-child { border-top: 1px solid var(--rule); }
.week-row:hover { opacity: 0.45; }
.week-title { font-family: var(--serif); font-size: 14px; }
.week-note { display: block; font-size: 11.5px; color: var(--gray); font-style: italic; margin-top: 2px; }
.week-meta { font-size: 11px; color: var(--mid); white-space: nowrap; }
footer { text-align: center; padding: 36px 40px; font-size: 11px; color: var(--mid); letter-spacing: 0.04em; }
footer a { color: inherit; }
@keyframes fadeUp { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
@media (max-width: 640px) {
  nav { padding: 14px 20px; } nav ul { gap: 16px; } main { padding: 0 22px; }
  .entry { grid-template-columns: 26px 1fr; }
  .entry-meta { grid-column: 2; text-align: left; margin-top: 4px; }
  .entry-meta .src, .score { display: inline; margin-right: 10px; }
}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
         '<link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400'
         '&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap" rel="stylesheet" />')

def esc(s): return html.escape(str(s), quote=True)

def fmt_week(week_iso):
    d = datetime.date.fromisoformat(week_iso)
    return "Week ending " + d.strftime("%B %-d, %Y")

def weekday(date_iso):
    return datetime.date.fromisoformat(date_iso).strftime("%a")

def page(title, body, depth=0):
    pre = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(SITE['subtitle'])}" />
{FONTS}
<style>{CSS}</style>
</head>
<body>
<nav>
  <a class="nav-name" href="{pre}index.html">{esc(SITE['title'])}</a>
  <ul>
    <li><a href="{pre}index.html">This Week</a></li>
    <li><a href="{pre}archive/index.html">Archive</a></li>
    <li><a href="https://danberte.com">danberte.com</a></li>
  </ul>
</nav>
<main>
{body}
</main>
<footer>© {datetime.date.today().year} {esc(SITE['author'])} &nbsp;·&nbsp; curated weekly &nbsp;·&nbsp; <a href="https://danberte.com">danberte.com</a></footer>
</body>
</html>"""

def render_entry(e, rank, all_by_id):
    topics = "".join(f'<span class="topic-pill">{esc(t)}</span>' for t in e.get("topics", []))
    if e.get("sample"):
        topics += '<span class="topic-pill sample">sample</span>'
    rel = ""
    rel_ids = [r for r in e.get("related", []) if r in all_by_id]
    if rel_ids:
        names = " · ".join(esc(all_by_id[r]["title"][:60]) for r in rel_ids)
        rel = f'<span class="related-note">↔ overlaps: {names}</span>'
    if e.get("score") is None:
        score = '<span class="score pending">—</span>'
    else:
        score = f'<span class="score">{e["score"]:.1f}</span>'
    posted = e.get("posted") or e.get("added")
    return f"""<a class="entry" href="{esc(e['url'])}" target="_blank" rel="noopener">
  <span class="rank">{rank:02d}</span>
  <span>
    <span class="entry-title">{esc(e['title'])}</span>
    <span class="entry-blurb">{esc(e['blurb'])}</span>
    <span class="entry-topics">{topics}</span>{rel}
  </span>
  <span class="entry-meta">
    <span class="src">{esc(e['source'])} · {esc(e['author'])} · {weekday(posted)}</span>
    {score}
  </span>
</a>"""

def render_week_body(week_iso, entries, all_by_id, is_current):
    entries = sorted(entries, key=lambda e: (e.get("score") is None, -(e.get("score") or 0)))
    rows = "\n".join(render_entry(e, i + 1, all_by_id) for i, e in enumerate(entries))
    label = "This Week" if is_current else "Archived Week"
    tldr = DATA.get("weeks", {}).get(week_iso, {}).get("tldr", "")
    tldr_html = (f'\n  <p class="tldr-label">Executive summary</p>'
                 f'\n  <p class="tldr">{esc(tldr)}</p>') if tldr else ""
    return f"""<section class="masthead">
  <p class="week-label">{esc(label)} — {esc(fmt_week(week_iso))} · {len(entries)} signals</p>{tldr_html}
</section>
<section>
  <p class="section-label">Ranked by weight — score reflects relevance, novelty and likely impact</p>
  <div class="item-list">
{rows}
  </div>
</section>"""

def main():
    entries = DATA["entries"]
    all_by_id = {e["id"]: e for e in entries}
    weeks = collections.defaultdict(list)
    for e in entries:
        weeks[e["week"]].append(e)
    ordered = sorted(weeks.keys(), reverse=True)
    current = ordered[0]

    (ROOT / "archive").mkdir(exist_ok=True)

    # current week -> index.html
    (ROOT / "index.html").write_text(page(
        f"{SITE['title']} — {fmt_week(current)}",
        render_week_body(current, weeks[current], all_by_id, True), depth=0))

    # every week (incl. current) also gets a permanent archive page
    for wk in ordered:
        (ROOT / "archive" / f"{wk}.html").write_text(page(
            f"{SITE['title']} — {fmt_week(wk)}",
            render_week_body(wk, weeks[wk], all_by_id, wk == current), depth=1))

    # archive index
    rows = []
    for wk in ordered:
        es = weeks[wk]
        top = max(es, key=lambda e: e.get("score") or 0)
        note = f'<span class="week-note">Top signal: {esc(top["title"][:80])}</span>' if top.get("score") else ""
        cur = " · current" if wk == current else ""
        rows.append(f"""<a class="week-row" href="{wk}.html">
  <span class="week-title">{esc(fmt_week(wk))}{note}</span>
  <span class="week-meta">{len(es)} signals{cur}</span>
</a>""")
    body = f"""<section class="masthead">
  <h1 class="hero-name">Archive</h1>
  <p class="hero-title">Every week of {esc(SITE['title'])}, preserved for later reference.</p>
</section>
<section>
  <p class="section-label">Weekly editions</p>
  <div class="item-list">
{chr(10).join(rows)}
  </div>
</section>"""
    (ROOT / "archive" / "index.html").write_text(page(f"{SITE['title']} — Archive", body, depth=1))
    print(f"Built: index.html, archive/index.html, {len(ordered)} week page(s). Current week: {current}")

if __name__ == "__main__":
    main()
