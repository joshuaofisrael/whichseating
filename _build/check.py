#!/usr/bin/env python3
"""Site QA. Usage: python3 _build/check.py [--launch]

Preview (default): every page has noindex, no beacon.
Launch: beacon present, noindex only on 404.html.
Also checks canonicals, one h1, JSON-LD, legal line, dashes, descriptions,
root-relative links, sitemap, robots, ads.txt, CNAME, and unsourced section numbers.
"""
import glob, os, re, sys, json, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = [f for f in glob.glob(ROOT + "/**/*.html", recursive=True) if "/_build/" not in f]
home = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
LAUNCH = "noindex" not in home
if "--launch" in sys.argv and not LAUNCH:
    print("flag says launch but homepage is noindex"); sys.exit(1)
LEGAL = {"terms", "privacy", "disclaimer", "copyright", "ad-disclosure", "editorial-policy", "contact"}
bad = 0
titles = {}
def fail(msg):
    global bad
    print(msg); bad += 1
linked = {}
for f in files:
    h = open(f, encoding="utf-8").read()
    rel = os.path.relpath(f, ROOT)
    top = rel.split("/")[0]
    vis = re.sub(r"<script.*?</script>", "", h, flags=re.S)
    vis = re.sub(r"<style.*?</style>", "", vis, flags=re.S)
    if "\u2013" in h or "\u2014" in h: fail("dash " + rel)
    if "github.io" in h: fail("github.io " + rel)
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: json.loads(m)
        except Exception as e: fail("JSONLD %s %s" % (rel, e))
    if top not in LEGAL and rel != "404.html" and re.search(r"Joshua|Israel Ventures|©", vis):
        fail("LLC " + rel)
    if top in LEGAL and "is a trade name of Joshua Israel Ventures LLC" not in h:
        fail("nolegalline " + rel)
    if not re.search(r'<link rel="canonical" href="https://whichseating.com/', h):
        fail("canonical " + rel)
    if h.count("<h1") != 1: fail("h1 %s %d" % (rel, h.count("<h1")))
    dm = re.search(r'<meta name="description" content="(.*?)"', h)
    if not dm: fail("nodesc " + rel)
    elif len(html.unescape(dm.group(1))) > 155: fail("desc %d %s" % (len(html.unescape(dm.group(1))), rel))
    if LAUNCH:
        if rel != "404.html" and "noindex" in h: fail("noindex " + rel)
        if "static.cloudflareinsights.com/beacon.min.js" not in h: fail("nobeacon " + rel)
    elif "noindex" not in h:
        fail("preview-missing-noindex " + rel)
    if rel.startswith("venues/") and rel.count("/") >= 2:
        if 'class="sources"' not in h or not re.search(r'href="https?://', h[h.find('class="sources"'):]):
            fail("nosource " + rel)
        if re.search(r"\bsections?\s+\d+", vis, re.I): fail("section-number " + rel)
        if '"datePublished": "2026-11-16"' not in h: fail("datePublished " + rel)
    if "FAQPage" in h:
        data = [json.loads(m) for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)]
        nq = 0
        for d in data:
            if d.get("@type") == "FAQPage": nq = len(d.get("mainEntity") or [])
        nd = len(re.findall(r"<details>", h[h.find('class="faq"'):])) if 'class="faq"' in h else 0
        if nq != nd or nq == 0: fail("faq %s schema %d details %d" % (rel, nq, nd))
    t = re.search(r"<title>(.*?)</title>", h).group(1)
    t = html.unescape(t)
    titles.setdefault(t, []).append(rel)
    if len(t) > 70: print("longtitle", len(t), t)
    for l in re.findall(r'(?:href|src)="(/[^"#?]*)', h):
        p = os.path.join(ROOT, l.lstrip("/"))
        if not (os.path.isfile(p) or os.path.isfile(os.path.join(p, "index.html"))):
            fail("broken %s %s" % (rel, l))
        linked.setdefault(l, []).append(rel)
venue_hrefs = []
for f in files:
    rel = os.path.relpath(f, ROOT)
    if rel.startswith("venues/") and rel.endswith("index.html") and rel.count("/") == 2:
        venue_hrefs.append("/" + rel[: -len("index.html")])
if len(venue_hrefs) < 60: fail("venue count %d" % len(venue_hrefs))
for href in venue_hrefs:
    users = [r for r in linked.get(href, []) if not r.endswith(href.strip("/") + "/index.html") and r != href]
    # a venue is linked from other pages if the href appears outside its own file
    outsiders = [r for r in linked.get(href, []) if os.path.normpath(r) != os.path.normpath(href.strip("/") + "/index.html")]
    if not outsiders: fail("unlinked " + href)
for t, fs in titles.items():
    if len(fs) > 1: fail("duptitle %s %s" % (t, fs))
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
if any("github.io" in x for x in locs): fail("sitemap github.io")
if any("404" in x for x in locs): fail("404 in sitemap")
expected = []
for f in files:
    rel = os.path.relpath(f, ROOT)
    if rel == "404.html": continue
    if rel == "index.html": expected.append("https://whichseating.com/")
    else: expected.append("https://whichseating.com/" + rel[: -len("index.html")])
if sorted(locs) != sorted(expected):
    fail("sitemap mismatch %d locs %d pages" % (len(locs), len(expected)))
robots = open(os.path.join(ROOT, "robots.txt"), encoding="utf-8").read()
for bot in ["Googlebot", "Bingbot", "GPTBot", "ClaudeBot", "PerplexityBot", "OAI-SearchBot", "CCBot", "Google-Extended", "Applebot-Extended", "Bytespider"]:
    if bot not in robots: fail("robots missing " + bot)
if "Sitemap: https://whichseating.com/sitemap.xml" not in robots: fail("robots sitemap")
llms = open(os.path.join(ROOT, "llms.txt"), encoding="utf-8").read()
for href in venue_hrefs:
    if "https://whichseating.com" + href not in llms: fail("llms missing " + href)
ads = open(os.path.join(ROOT, "ads.txt"), encoding="utf-8").read()
if "Placeholder" not in ads: fail("ads.txt")
cname = open(os.path.join(ROOT, "CNAME"), encoding="utf-8").read().strip()
if cname != "whichseating.com": fail("CNAME " + cname)
print("files", len(files), "venues", len(venue_hrefs), "launch" if LAUNCH else "noindex", "issues", bad)
sys.exit(1 if bad else 0)
