"""Builds the INTERNAL fertilizer.pro page (behind Cloudflare Access, Direct Hedge staff only).
Same page as the public one (pubgen.py) plus the licensed Argus / ICIS / Profercy benchmark table.
Writes out/site/index.html. Never publish this output anywhere public."""
import json, os, html, subprocess, sys
from datetime import datetime
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
subprocess.run([sys.executable, os.path.join(HERE, "pubgen.py")], check=True)
page = open(os.path.join(OUT, "public.html")).read()
e = html.escape
b = json.load(open(os.path.join(OUT, "benchmarks.json")))["rows"] if os.path.exists(os.path.join(OUT, "benchmarks.json")) else []
def f(v, d): return "—" if v is None else f"{v:,.{d}f}"
def unit(u): return (u or "").replace("USD/metric tonne", "$/t").replace("USD/short ton", "$/st")
def dt(s):
    try: return datetime.strptime(s[:10], "%Y-%m-%d").strftime("%-d %b")
    except Exception: return e(s or "")
rows = "".join(f'<tr><td class="l">{e(r["benchmark"])}</td><td class="l">{e(r.get("publisher",""))}</td><td class="l mu">{e(r.get("basis",""))}</td>'
               f'<td>{f(r.get("low"),0)}</td><td>{f(r.get("high"),0)}</td><td>{f(r.get("mid"),1)}</td><td class="mu">{e(unit(r.get("unit")))}</td><td>{dt(r.get("assessment_date",""))}</td></tr>' for r in b)
card = ('<div class="card" style="margin-top:16px"><h3>Publisher benchmarks — Argus, ICIS, Profercy</h3>'
        '<table><thead><tr><th>Benchmark</th><th>Publisher</th><th>Basis</th><th>Low</th><th>High</th><th>Mid</th><th>Unit</th><th>Assessed</th></tr></thead>'
        f'<tbody>{rows or "<tr><td class=\"l mu\" colspan=\"8\">No assessments yet</td></tr>"}</tbody></table>'
        '<p class="sub">Latest assessment from each publisher. Licensed data: for Direct Hedge staff only, do not forward.</p></div>')
anchor = '<div class="grid" style="margin-top:16px"><div class="card"><h3>Daily NOLA urea index</h3>'
assert anchor in page, "anchor missing"
page = page.replace(anchor, card + anchor, 1)
page = page.replace("<title>DH Fertilizer Terminal</title>", '<title>fertilizer.pro · DH Fertilizer Terminal</title><meta name="robots" content="noindex,nofollow">')
page = page.replace("For Direct Hedge internal use. Not investment advice.", "Direct Hedge internal. Contains licensed Argus, ICIS and Profercy prices: staff only, do not forward. Not investment advice.")
os.makedirs(os.path.join(OUT, "site"), exist_ok=True)
open(os.path.join(OUT, "site", "index.html"), "w").write(page)
print("site page", len(page), "bytes;", len(b), "benchmark rows")
