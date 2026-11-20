#!/usr/bin/env python3
"""Which Seating static site builder. Run from the repo root.

  python3 _build/build.py            # noindex on every page (INDEXABLE is false)
  python3 _build/build.py --launch   # indexable pages, Cloudflare beacon

Paths are always root-relative. Canonicals always use https://whichseating.com/.
The single index flag is INDEXABLE in _build/config.py.
"""
import os, sys, json, html, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAUNCH = config.INDEXABLE or "--launch" in sys.argv
BASE = config.BASE_URL
BRAND = config.BRAND
E = html.escape
VENUES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "venues.json"), encoding="utf-8"))
PAGES = []

LEAGUE_ORDER = ["nfl", "mlb", "nba", "nhl", "college-football"]
LEAGUE_NAME = {
    "nfl": "NFL", "mlb": "MLB", "nba": "NBA", "nhl": "NHL", "college-football": "College football",
}
SPORT = {
    "nfl": "football", "college-football": "football", "mlb": "baseball", "nba": "basketball", "nhl": "hockey",
}
READ = {
    "football": "On a football seating chart, the closest straight on view of the whole field is the lowest seating level near midfield. The lowest seats in an end zone are close to one end of the field and far from the other. Upper levels sit higher and farther from the field.",
    "baseball": "On a baseball seating chart, seats in the lowest level directly behind home plate face the pitcher and the full field. Seats down the first base line or the third base line look across the diamond. Upper levels are farther from home plate. Outfield seats face back toward the infield.",
    "basketball": "On a basketball seating chart, the lowest seats at midcourt are the closest straight on view of the whole floor. The lowest seats behind a basket look at the near hoop from the baseline. Upper levels are higher.",
    "hockey": "On a hockey seating chart, the lowest seats at center ice are the closest straight on view of the whole rink. The lowest seats behind a goal look at the near net from the end. Upper levels are higher.",
}
SURFACE = {"football": "Field", "baseball": "Diamond", "basketball": "Court", "hockey": "Rink"}
STATE_CODE = {
    "Alabama": "al", "Arizona": "az", "Arkansas": "ar", "California": "ca", "Colorado": "co",
    "District of Columbia": "dc", "Florida": "fl", "Georgia": "ga", "Illinois": "il", "Indiana": "in",
    "Louisiana": "la", "Maryland": "md", "Massachusetts": "ma", "Michigan": "mi", "Minnesota": "mn",
    "Missouri": "mo", "Nebraska": "ne", "Nevada": "nv", "New Jersey": "nj", "New York": "ny",
    "North Carolina": "nc", "Ohio": "oh", "Oklahoma": "ok", "Oregon": "or", "Pennsylvania": "pa",
    "South Carolina": "sc", "Tennessee": "tn", "Texas": "tx", "Utah": "ut", "Washington": "wa",
    "Wisconsin": "wi",
}
LOGO = '<svg width="34" height="34" viewBox="0 0 64 64" aria-hidden="true" focusable="false"><rect width="64" height="64" rx="14" fill="#16382c"/><rect x="8" y="42" width="48" height="8" rx="2" fill="#e4a04a"/><rect x="12" y="16" width="10" height="18" rx="2" fill="#f6f3ec"/><rect x="27" y="16" width="10" height="18" rx="2" fill="#f6f3ec"/><rect x="42" y="16" width="10" height="18" rx="2" fill="#f6f3ec"/></svg>'
NAV = [("/", "Home"), ("/venues/", "Venues"), ("/leagues/", "Leagues"), ("/states/", "States"), ("/guides/how-to-choose-a-seat/", "How to choose")]
FOOT = [("About", "/about/"), ("Sources and methods", "/methodology/"), ("Editorial policy", "/editorial-policy/"),
        ("Image policy", "/image-policy/"), ("Terms of use", "/terms/"), ("Privacy", "/privacy/"),
        ("Disclaimer", "/disclaimer/"), ("Advertising disclosure", "/ad-disclosure/"),
        ("Copyright and DMCA", "/copyright/"), ("Contact", "/contact/")]

def url(path):
    if path in ("/", ""): return BASE
    return BASE + path.lstrip("/")

def slug(name):
    s = name.replace("&", " and ").replace(".com", "-com").replace(".", "").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def place(v):
    if v["state"] == "District of Columbia": return "Washington, D.C."
    return v["city"] + ", " + v["state"]

def city_slug(v): return slug(v["city"]) + "-" + STATE_CODE[v["state"]]
def state_slug(v): return slug(v["state"])
def leagues_of(v):
    out = []
    for t in v["teams"]:
        if t["league"] not in out: out.append(t["league"])
    return out
def sports_of(v):
    out = []
    for lg in leagues_of(v):
        s = SPORT[lg]
        if s not in out: out.append(s)
    return out
def roof_key(v):
    return {"Open-air": "open", "Open": "open", "Retractable": "retractable", "Dome": "dome",
            "Skylight": "skylight", "Fixed": "fixed", "Indoor": "indoor"}.get(v["roof_label"], "unknown")
def official(v):
    for s in v["sources"]:
        if s["role"] == "official": return s
    return None
def team_names(v): return [t["name"] for t in v["teams"]]
def team_list(v):
    names = team_names(v)
    if len(names) == 1: return names[0]
    if len(names) == 2: return names[0] + " and " + names[1]
    return ", ".join(names[:-1]) + ", and " + names[-1]
def cap_list(v):
    return "; ".join(c["label"].replace(" listed", "") + " " + c["value"] for c in v["capacities"])
def pick_desc(where, vs):
    names = ", ".join(v["name"] for v in vs)
    full = "Which seats to pick in %s: %s." % (where, names)
    if len(full) <= 155:
        return full
    return "Which seats to pick in %s. %d venue guides on this page." % (where, len(vs))

def venue_title(name):
    """Unique title under 60 characters. Shorten only when the full name does not fit."""
    title = "Best Seats at %s" % name
    if len(title) < 60:
        return title
    if " at " in name:
        short = name.rsplit(" at ", 1)[1]
        alt = "Best Seats at %s" % short
        if short and len(alt) < 60:
            return alt
    raise SystemExit("title %d %s" % (len(title), name))

def clip(d, n=155):
    d = re.sub(r"\s+", " ", d).strip()
    if len(d) <= n: return d
    cut = d[: n - 1]
    i = cut.rfind(" ")
    if i > 90: cut = cut[:i]
    out = cut.rstrip(".,;:") + "."
    if len(out) > n: out = out[: n - 1].rstrip(".,;:") + "."
    return out

def write(path, content):
    if "\u2013" in content or "\u2014" in content:
        raise SystemExit("dash in " + path)
    fp = os.path.join(ROOT, "404.html" if path == "404.html" else path.strip("/"))
    if path.endswith("/") or path == "/":
        fp = os.path.join(ROOT if path == "/" else os.path.join(ROOT, path.strip("/")), "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(content)

def ld(obj):
    raw = json.dumps(obj, ensure_ascii=False).replace("<", "\\u003c")
    return '<script type="application/ld+json">' + raw + "</script>"

def crumbs_html(crumbs):
    if not crumbs: return ""
    bits = []
    for i, (p, n) in enumerate(crumbs):
        if i < len(crumbs) - 1: bits.append('<li><a href="%s">%s</a></li>' % (p, E(n)))
        else: bits.append('<li aria-current="page">%s</li>' % E(n))
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(bits) + "</ol></nav>"

# AdSense low-value-content fix (20 Nov 2026): paths listed in _build/thin-noindex.txt
# get noindex,follow and stay out of the sitemap until they have real unique substance.
_THIN_NOINDEX = set()
try:
    import os as _os
    with open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "thin-noindex.txt"), encoding="utf-8") as _fh:
        _THIN_NOINDEX = {l.strip().strip("/") for l in _fh if l.strip() and not l.startswith("#")}
except FileNotFoundError:
    pass


def _is_thin(path):
    return str(path).strip("/") in _THIN_NOINDEX


def page(path, title, desc, body, crumbs=None, extra_ld=None, legal=False, index=True, mod=None):
    if _is_thin(path):
        index = False
    if len(title) >= 60: raise SystemExit("title %d %s" % (len(title), path))
    desc = clip(desc)
    if len(desc) > 155: raise SystemExit("desc %d %s" % (len(desc), path))
    canon = url(path if path != "404.html" else "404.html")
    noindex = (not LAUNCH) or (not index)
    if index: PAGES.append((path if path != "404.html" else "404.html", mod or config.MODIFIED))
    blocks = []
    if path == "/":
        blocks.append({"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": BASE,
                       "publisher": {"@type": "Organization", "name": BRAND, "url": BASE, "logo": url("/logo.png")}})
        blocks.append({"@context": "https://schema.org", "@type": "Organization", "name": BRAND, "url": BASE,
                       "logo": url("/logo.png")})
    if crumbs:
        blocks.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (p, n) in enumerate(crumbs)]})
    if extra_ld: blocks.extend(extra_ld)
    ldh = "".join(ld(b) for b in blocks)
    og_type = "article" if any(b.get("@type") == "Article" for b in blocks) else "website"
    og_image = url("/og.png")
    for b in blocks:
        if b.get("@type") == "Article" and b.get("image"):
            og_image = b["image"]
            break
    nav = "".join('<a href="%s"%s>%s</a>' % (p, ' aria-current="page"' if p == path else "", n) for p, n in NAV)
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    flag = "<!-- robots: noindex while INDEXABLE is false in _build/config.py -->" if not LAUNCH else "<!-- robots: indexable (INDEXABLE or --launch) -->"
    beacon = ("<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{\"token\": \"%s\"}'></script><!-- End Cloudflare Web Analytics -->" % config.CF_BEACON_TOKEN) if LAUNCH else "<!-- cf-beacon: added when INDEXABLE is true -->"
    # GA4 loads from consent.js only after Accept. The inline id is read by that file.
    ga = ('<script>window.WHICH_GA4_ID=%s;</script><script src="/assets/consent.js?v=1" defer></script>' % json.dumps(config.GA4_ID)) if LAUNCH else "<!-- ga4 loader is added by build.py --launch -->"
    # AdSense account meta + head script (no ad units). Verification / readiness only.
    adsense = (
        '<meta name="google-adsense-account" content="%s">'
        '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=%s" crossorigin="anonymous"></script>'
        % (config.ADSENSE_PUB, config.ADSENSE_PUB)
    ) if LAUNCH else "<!-- adsense: added when INDEXABLE is true -->"
    foot_items = list(FOOT)
    if LAUNCH:
        foot_items.append(("Cookie settings", "/privacy/#analytics"))
    foot_bits = []
    for n, p in foot_items:
        if n == "Cookie settings":
            foot_bits.append('<a href="%s" id="cookie-settings">%s</a>' % (p, n))
        else:
            foot_bits.append('<a href="%s">%s</a>' % (p, n))
    foot = " | ".join(foot_bits)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{canon}">
<meta name="robots" content="{robots}">
{flag}
{adsense}
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{og_image}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/style.css?v=3">{ldh}
</head><body><a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap"><a class="brand" href="/">{LOGO}<span>{BRAND}</span></a><nav class="main" aria-label="Main">{nav}</nav></div></header>
<main id="main" class="wrap">{crumbs_html(crumbs)}{body}<!-- ad-slot: below-content (reserved; no ad code) --></main>
<footer class="site"><div class="wrap"><p class="fbrand"><strong>{BRAND}</strong> tells you which seats to pick at major US stadiums and arenas, and which to skip. Facts come from public lists and official pages. Section numbers are printed only when a source prints them. Layouts change, so check the venue's current chart before you buy.</p>
<p class="flinks">{foot}</p>
</div></footer>
<script src="/assets/site.js?v=1" defer></script>{ga}{beacon}
</body></html>'''

def article(headline, path, about=None, mod=None, published=None, image=None):
    data = {"@context": "https://schema.org", "@type": "Article", "headline": headline,
            "datePublished": published or mod or config.PUBLISHED,
            "dateModified": mod or config.MODIFIED,
            "author": {"@type": "Organization", "name": BRAND, "url": BASE},
            "publisher": {"@type": "Organization", "name": BRAND, "url": BASE, "logo": {"@type": "ImageObject", "url": url("/logo.png")}},
            "image": url(image or "/og.png"), "mainEntityOfPage": url(path)}
    if about: data["about"] = {"@type": "Place", "name": about}
    return data

HERO_IMG = "/assets/images/empty-stadium-dusk.png"

def hero_photo(alt):
    """One realistic news-photo thumbnail, AI-labelled, linking the image policy."""
    return (
        '<figure class="hero-photo">'
        '<img src="%s" width="1280" height="720" loading="eager" '
        'alt="%s">'
        '<figcaption>AI-generated image. <a href="/image-policy/">Image policy</a>.</figcaption>'
        '</figure>'
    ) % (HERO_IMG, E(alt))

def next_reads(items, heading="Keep reading"):
    """3-4 closely related next-read links with thumbnails (engagement rule)."""
    bits = ['<aside class="next-reads" aria-label="%s"><h2>%s</h2><ul class="next-reads-list">' % (E(heading), E(heading))]
    for href, title, blurb in items:
        bits.append(
            '<li><a href="%s"><img src="%s" width="320" height="180" loading="lazy" alt="">'
            '<span class="nr-text"><strong>%s</strong><span class="nr-blurb">%s</span></span></a></li>'
            % (href, HERO_IMG, E(title), E(blurb))
        )
    bits.append("</ul></aside>")
    return "".join(bits)

def compare_box(heading, intro, links):
    """Compare / check-another box for lookup guides (engagement rule)."""
    lis = "".join('<li><a href="%s">%s</a></li>' % (href, E(label)) for href, label in links)
    return (
        '<aside class="compare" aria-label="%s">'
        '<h2>%s</h2><p>%s</p><ul>%s</ul></aside>'
    ) % (E(heading), E(heading), intro, lis)

def faq_ld(pairs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}

def faq_html(pairs):
    bits = ['<section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">Frequently asked questions</h2>']
    for q, a in pairs:
        bits.append("<details><summary>%s</summary><p>%s</p></details>" % (E(q), E(a)))
    bits.append("</section>")
    return "".join(bits)

def sources_html(sources, extra="", retrieved=None):
    bits = ['<section class="sources" aria-labelledby="src-h"><h2 id="src-h">Sources</h2><ul>']
    for s in sources:
        bits.append('<li><a href="%s" rel="nofollow noopener" target="_blank">%s</a> (%s)</li>' % (E(s["url"]), E(s["title"]), E(s["publisher"])))
    bits.append("</ul>")
    tail = (extra + " ") if extra else ""
    bits.append('<p class="note">Retrieved %s. %sWhich Seating is not affiliated with any team, league, or venue. See <a href="/methodology/">how we build these pages</a> and our <a href="/editorial-policy/">editorial policy</a>.</p>' % (retrieved or config.VERIFIED, tail))
    bits.append("</section>")
    return "".join(bits)

def bowl(sport):
    label = SURFACE.get(sport, "Field")
    return '''<figure class="bowl"><figcaption><strong>Generic bowl.</strong> This is our drawing, not the venue seating chart, and it has no section numbers. The lowest band is closest to the %s. The upper band is farther away. <a href="/image-policy/">Image policy</a>.</figcaption>
<svg viewBox="0 0 320 150" role="img"><title>Generic seating bowl</title>
<rect x="40" y="28" width="240" height="94" rx="46" fill="#e7f3ee" stroke="#16382c" stroke-width="2"/>
<rect x="78" y="52" width="164" height="52" rx="26" fill="#fff3df" stroke="#9a5b00" stroke-width="2"/>
<rect x="118" y="68" width="84" height="26" rx="6" fill="#16382c"/>
<text x="160" y="85" text-anchor="middle" fill="#f6f3ec" font-size="11" font-family="system-ui,sans-serif">%s</text>
<text x="160" y="48" text-anchor="middle" fill="#9a5b00" font-size="11" font-family="system-ui,sans-serif">Lowest level</text>
<text x="160" y="24" text-anchor="middle" fill="#0f6e56" font-size="11" font-family="system-ui,sans-serif">Upper level</text>
</svg></figure>''' % (E(label.lower()), E(label))

def sun_text(v):
    key = roof_key(v)
    label = v["roof_label"] or "not stated"
    if key == "open":
        return "The source list classifies the roof as %s. The sources on this page do not publish a shade chart by section, so this page does not name sunny or shaded sections." % label
    if key == "retractable":
        return "The source list classifies the roof as retractable. Sun and weather depend on whether the roof is open for that event. The sources do not name shaded sections."
    if key == "dome":
        return "The source list classifies the roof as a dome. Sun and rain are not seating factors while the roof is closed, which is how a dome is normally used."
    if key == "skylight":
        return "The source list classifies the roof as a skylight, a fixed roof rather than open stands. The sources do not say which sections get more light, so this page does not name them."
    if key == "fixed":
        return "The source list classifies the roof as fixed, a roof that does not open. Sun and rain are not seating factors the way they are at an open air park."
    if key == "indoor":
        return "This building is an indoor arena on the league arena list. The sources do not publish a shade chart by section, so this page does not name sunny seats."
    return "The stadium list we used does not state a roof type, so this page does not make a sun or shade claim."

def best_text(v):
    reads = " ".join(READ[s] for s in sports_of(v))
    off = official(v)
    lead = "Start with the official page linked in the sources." if off else "We did not confirm an official seating page on this check, so start with the list source and the venue's own current chart."
    return lead + " " + reads + " This is our method for reading a chart. It is not a list of section numbers from the venue."

def skip_text(v):
    base = "Skip any seat the official page or the ticket marks as limited view, obstructed view, or partial view. The text sources checked for this page did not publish a numbered list of obstructed sections, so none is printed here."
    if any("upper deck" in n.lower() for n in v["notes"]):
        base += " A sourced note on this page covers a closed upper deck. Read that note before you buy."
    return base

def access_text(v):
    return "The sources checked for this page do not publish accessible section numbers at %s. Use the venue accessibility office, and the accessible path on the official page when one is linked below, before you buy." % v["name"]

def value_text(v):
    return "No value ranking of sections is published in the sources, and this page does not list prices, because prices change by opponent. On a normal chart, upper levels are farther from the playing surface than the lowest level."

def who_text(v):
    leagues = ", ".join(LEAGUE_NAME[lg] for lg in leagues_of(v))
    return "Home teams on the source list: %s. League: %s." % (team_list(v), leagues)

def pairs_for(v):
    return [
        ("What are the best seats at %s?" % v["name"], best_text(v)),
        ("Does sun or shade matter at %s?" % v["name"], sun_text(v)),
        ("Which sections should I skip at %s?" % v["name"], skip_text(v)),
        ("Where is accessible seating at %s?" % v["name"], access_text(v)),
        ("Who plays at %s?" % v["name"], who_text(v)),
    ]

def by_league(lg):
    return sorted([v for v in VENUES if lg in leagues_of(v)], key=lambda v: v["name"].casefold())

def siblings(v, n=3):
    lg = leagues_of(v)[0]
    group = by_league(lg)
    i = next(k for k, x in enumerate(group) if x["slug"] == v["slug"])
    out = []
    for step in range(1, len(group)):
        out.append(group[(i + step) % len(group)])
        if len(out) == n: break
    return out

def venue_page(v):
    path = "/venues/%s/" % v["slug"]
    lg = leagues_of(v)[0]
    crumbs = [("/", "Home"), ("/venues/", "Venues"), ("/leagues/%s/" % lg, LEAGUE_NAME[lg]), (path, v["name"])]
    pairs = pairs_for(v)
    chips = "".join('<span class="chip">%s</span>' % E(x) for x in [LEAGUE_NAME[x] for x in leagues_of(v)] + [v["roof_label"] or "Roof not stated", place(v)])
    quick = "<ul>" + "".join("<li><strong>%s</strong> %s</li>" % (lab, E(txt)) for lab, txt in [
        ("Best view.", best_text(v)), ("Sun and roof.", sun_text(v)), ("Skip.", skip_text(v)),
        ("Accessible seating.", access_text(v)), ("Value.", value_text(v))]) + "</ul>"
    rows = [("Place", place(v)), ("Home teams", team_list(v)), ("Opened", v["opened"] or "Not stated"),
            ("Roof on the source list", v["roof_label"] or "Not stated")]
    for c in v["capacities"]:
        rows.append((c["label"], c["value"]))
    if v.get("surface"): rows.append(("Surface listed", v["surface"]))
    if v.get("center_field"): rows.append(("Center field distance listed", v["center_field"]))
    if v.get("ballpark_type"): rows.append(("Ballpark type listed", v["ballpark_type"]))
    table = "".join("<tr><th scope=\"row\">%s</th><td>%s</td></tr>" % (E(a), E(b)) for a, b in rows)
    notes = ""
    if v["notes"]:
        notes = "<h2>Sourced notes</h2>" + "".join("<p>%s</p>" % E(n) for n in v["notes"])
    sib = siblings(v)
    links = []
    for lgx in leagues_of(v):
        links.append('<a href="/leagues/%s/">%s venues</a>' % (lgx, LEAGUE_NAME[lgx]))
    links.append('<a href="/states/%s/">%s</a>' % (state_slug(v), v["state"]))
    links.append('<a href="/cities/%s/">%s</a>' % (city_slug(v), v["city"]))
    for s in sib:
        links.append('<a href="/venues/%s/">%s</a>' % (s["slug"], s["name"]))
    if "nfl" in leagues_of(v):
        links.append('<a href="/guides/nfl-stadiums-with-a-roof/">Which NFL stadiums have a roof</a>')
    if "mlb" in leagues_of(v):
        links.append('<a href="/guides/mlb-ballparks-with-a-retractable-roof/">Which MLB ballparks have a retractable roof</a>')
    links += ['<a href="/guides/how-to-choose-a-seat/">How to choose a seat</a>',
              '<a href="/guides/shade-and-sun/">Shade and sun</a>',
              '<a href="/guides/sections-to-skip/">Sections to skip</a>',
              '<a href="/guides/accessible-seating/">Accessible seating</a>']
    where = "the Bronx, New York" if v["city"] == "Bronx" else place(v)
    intro = "%s in %s is listed as home to %s. %s. Roof on the source list: %s." % (
        v["name"], where, team_list(v), cap_list(v), v["roof_label"] or "not stated")
    body = '''<article class="prose wide"><h1>Which seats are best at %s?</h1>
<p class="byline">By %s. Last verified %s.</p>
<p class="chips">%s</p>
<div class="answer"><p><strong>Quick answer</strong></p>%s</div>
<p>%s</p>
%s
<h2>How to read the chart</h2>
<div class="method"><p>%s</p></div>
%s
<h2>%s at a glance</h2>
<div class="tablewrap"><table class="stats"><tbody>%s</tbody></table></div>
<p class="note">Figures are copied from the source list linked below, retrieved %s. If a cell was missing, it is marked not stated.</p>
<h2>What we left out</h2>
<div class="leftout"><ul>
<li>Numbered "best" sections. Not printed in the sources we checked.</li>
<li>A shade map by section.</li>
<li>A numbered obstructed view list, unless a note above states one.</li>
<li>Accessible section numbers.</li>
<li>Prices and fees. They change by event.</li>
</ul></div>
<h2>More on this building</h2><p>%s</p>
%s
%s
</article>''' % (E(v["name"]), BRAND, config.VERIFIED, chips, quick, E(intro), bowl(sports_of(v)[0]),
                 E(best_text(v)), notes, E(v["name"]), table, config.VERIFIED,
                 " · ".join(links), faq_html(pairs), sources_html(v["sources"]))
    title = venue_title(v["name"])
    where = "the Bronx, New York" if v["city"] == "Bronx" else place(v)
    full = "Which seats to pick at %s in %s. Capacity, roof, and how to read the chart. No invented section numbers." % (v["name"], where)
    short = "Seat guide for %s. Capacity, roof, and how to read the chart. No invented section numbers." % v["name"]
    desc = full if len(full) <= 155 else short
    if len(desc) > 155: raise SystemExit("desc " + v["name"])
    html_out = page(path, title, desc, body, crumbs, [article("Which seats are best at %s?" % v["name"], path, v["name"]), faq_ld(pairs)])
    write(path, html_out)

def card(v):
    roof = v["roof_label"] or "Roof not stated"
    return '<li class="card"><h3><a href="/venues/%s/">%s</a></h3><p>%s. %s. %s. Opened %s.</p></li>' % (
        v["slug"], E(v["name"]), E(team_list(v)), E(place(v)), E(roof), E(v["opened"] or "not stated"))

RELATED = ('<p>Related: <a href="/guides/how-to-choose-a-seat/">How to choose a seat</a>'
           ' · <a href="/guides/shade-and-sun/">Shade and sun</a>'
           ' · <a href="/guides/sections-to-skip/">Sections to skip</a>'
           ' · <a href="/guides/accessible-seating/">Accessible seating</a>'
           ' · <a href="/guides/club-seats/">What club seats include</a></p>')

def hub_page(path, title, desc, h1, intro, items, crumbs, pairs):
    # Venue pages carry the external list sources. Hubs link back to those pages and to the guides.
    body = '<article class="prose wide"><h1>%s</h1><p class="byline">By %s. Last verified %s.</p><p>%s</p><ul class="cards">%s</ul>%s%s<p>Each venue page lists the public list and the official page we checked. <a href="/methodology/">Sources and methods</a>.</p></article>' % (
        E(h1), BRAND, config.VERIFIED, intro, "".join(card(v) for v in items), RELATED, faq_html(pairs))
    write(path, page(path, title, desc, body, crumbs, [article(h1, path), faq_ld(pairs)]))

def build_hubs():
    # leagues index
    bits = []
    for lg in LEAGUE_ORDER:
        vs = by_league(lg)
        bits.append('<li class="card"><h2><a href="/leagues/%s/">%s</a></h2><p>%d venues. %s</p></li>' % (
            lg, LEAGUE_NAME[lg], len(vs), E(", ".join(v["name"] for v in vs[:4])) + ("." if len(vs) <= 4 else "...")))
    intro = "League hubs group every venue in this guide. A shared arena can appear under both the NBA and the NHL."
    pairs = [("Which league list should I use?",
              "Open the league for the game you are attending. A shared arena can appear under both the NBA and the NHL.")]
    body = '<article class="prose wide"><h1>Venues by league</h1><p>%s</p><ul class="cards">%s</ul>%s%s</article>' % (intro, "".join(bits), RELATED, faq_html(pairs))
    write("/leagues/", page("/leagues/", "Venues by League | Which Seating",
                            "Which seats to pick at NFL, MLB, NBA, NHL, and college football venues, grouped by league.",
                            body, [("/", "Home"), ("/leagues/", "Leagues")], [article("Venues by league", "/leagues/"), faq_ld(pairs)]))
    for lg in LEAGUE_ORDER:
        vs = by_league(lg)
        path = "/leagues/%s/" % lg
        h1 = "Best seats at %s venues" % LEAGUE_NAME[lg]
        pairs = [("Which %s venues does Which Seating cover?" % LEAGUE_NAME[lg],
                  "This page lists every %s venue in the guide. Open a venue for capacity, roof, and how to read the chart. Section numbers are on the venue page only when a source prints them." % LEAGUE_NAME[lg]),
                 ("How should I choose a seat at an %s building?" % LEAGUE_NAME[lg] if LEAGUE_NAME[lg][0] in "AEIOU" else "How should I choose a seat at a %s building?" % LEAGUE_NAME[lg],
                  READ[SPORT[lg]] + " Then open the venue page and the official page linked there.")]
        # fix grammar by hand in the question: "an NFL" is wrong. Use a simple question.
        pairs[1] = ("How do I choose seats for %s?" % LEAGUE_NAME[lg], pairs[1][1])
        intro = "There are %d %s venues in this guide. Facts on each page are tied to the sources at the bottom of that page." % (len(vs), LEAGUE_NAME[lg])
        if lg == "nfl":
            intro += ' See every stadium grouped by roof: <a href="/guides/nfl-stadiums-with-a-roof/">Which NFL stadiums have a roof</a>.'
        if lg == "mlb":
            intro += ' See every ballpark grouped by roof: <a href="/guides/mlb-ballparks-with-a-retractable-roof/">Which MLB ballparks have a retractable roof</a>.'
        hub_page(path, "%s Seat Guides | Which Seating" % LEAGUE_NAME[lg],
                 "Which seats to pick at %s venues. Capacity and roof come from the public list." % LEAGUE_NAME[lg],
                 h1, intro,
                 vs, [("/", "Home"), ("/leagues/", "Leagues"), (path, LEAGUE_NAME[lg])], pairs)
    # states
    states = {}
    cities = {}
    for v in VENUES:
        states.setdefault(v["state"], []).append(v)
        cities.setdefault((v["city"], v["state"]), []).append(v)
    pairs = [("Which state should I open?",
              "Open the state where the venue sits. Each state page links the stadium and arena guides there.")]
    body = '<article class="prose wide"><h1>Venues by state</h1><p>Pick a state to see every stadium and arena we cover there.</p><ul class="cols">'
    for st in sorted(states):
        body += '<li><a href="/states/%s/">%s</a> (%d)</li>' % (slug(st), E(st), len(states[st]))
    body += "</ul>%s%s</article>" % (RELATED, faq_html(pairs))
    write("/states/", page("/states/", "Venues by State | Which Seating",
                           "Which seats to pick at US stadiums and arenas, grouped by state.",
                           body, [("/", "Home"), ("/states/", "States")], [article("Venues by state", "/states/"), faq_ld(pairs)]))
    for st, vs in states.items():
        vs = sorted(vs, key=lambda v: v["name"].casefold())
        path = "/states/%s/" % slug(st)
        h1 = "Stadiums and arenas in %s" % st
        pairs = [("Which venues in %s have a seat guide?" % st,
                  "This page lists %d venues in %s. Open one for the seat guide." % (len(vs), st))]
        hub_page(path, "Best Seats in %s | Which Seating" % st,
                 pick_desc(st, vs),
                 h1, "%s has %d venues in this guide." % (st, len(vs)),
                 vs, [("/", "Home"), ("/states/", "States"), (path, st)], pairs)
    pairs = [("Which city page should I open?",
              "Open the city named on the source list for that venue. A shared metro area can be split across more than one city page. The state page brings them back together.")]
    body = '<article class="prose wide"><h1>Venues by city</h1><p>Cities follow the place named on the source list. Shared metro areas can be split across more than one city page. The state page brings them back together.</p><ul class="cols">'
    for (city, st), vs in sorted(cities.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        body += '<li><a href="/cities/%s/">%s, %s</a> (%d)</li>' % (slug(city) + "-" + STATE_CODE[st], E(city), E(st), len(vs))
    body += "</ul>%s%s</article>" % (RELATED, faq_html(pairs))
    write("/cities/", page("/cities/", "Venues by City | Which Seating",
                           "Which seats to pick, grouped by the city named on the source list.",
                           body, [("/", "Home"), ("/cities/", "Cities")], [article("Venues by city", "/cities/"), faq_ld(pairs)]))
    for (city, st), vs in cities.items():
        vs = sorted(vs, key=lambda v: v["name"].casefold())
        path = "/cities/%s/" % (slug(city) + "-" + STATE_CODE[st])
        label = city if st != "District of Columbia" else "Washington, D.C."
        where = "%s, %s" % (city, st)
        h1 = "Stadiums and arenas in %s" % where
        names = ", ".join(v["name"] for v in vs)
        pairs = [("Which venues in %s have a seat guide?" % where,
                  "This page covers %s." % names)]
        hub_page(path, "Best Seats in %s | Which Seating" % label,
                 pick_desc(where, vs),
                 h1, '<a href="/states/%s/">All %s venues</a>. This city page covers %d.' % (slug(st), E(st), len(vs)),
                 vs, [("/", "Home"), ("/cities/", "Cities"), (path, city)], pairs)

def venues_index():
    bits = []
    for lg in LEAGUE_ORDER:
        vs = by_league(lg)
        bits.append("<h2>%s</h2><ul class=\"cols\">" % LEAGUE_NAME[lg])
        for v in vs:
            bits.append('<li><a href="/venues/%s/">%s</a></li>' % (v["slug"], E(v["name"])))
        bits.append("</ul>")
    pairs = [("Which venue should I open?",
              "Open the stadium or arena where you have tickets. Each page covers capacity, roof, and how to read the chart. Section numbers are printed only when a source prints them.")]
    body = '<article class="prose wide"><h1>All venues</h1><p>%d stadium and arena guides. Pick one, or use the <a href="/leagues/">leagues</a>, <a href="/states/">states</a>, and <a href="/cities/">cities</a>.</p>%s%s%s</article>' % (
        len(VENUES), "".join(bits), RELATED, faq_html(pairs))
    write("/venues/", page("/venues/", "All Stadium and Arena Seat Guides",
                           "Which seats to pick at every NFL, MLB, NBA, NHL, and college venue in this guide.",
                           body, [("/", "Home"), ("/venues/", "Venues")], [article("All venues", "/venues/"), faq_ld(pairs)]))

def picker_html():
    bits = ['<form id="picker-form" class="picker" action="/venues/" method="get">',
            '<label for="venue-picker">Pick a venue</label>',
            '<select id="venue-picker"><option value="">Choose a stadium or arena</option>']
    for lg in LEAGUE_ORDER:
        bits.append('<optgroup label="%s">' % E(LEAGUE_NAME[lg]))
        seen = set()
        for v in by_league(lg):
            if v["slug"] in seen: continue
            seen.add(v["slug"])
            bits.append('<option value="/venues/%s/">%s</option>' % (v["slug"], E(v["name"])))
        bits.append("</optgroup>")
    bits.append('</select><button class="btn" type="submit">Open the guide</button></form>')
    bits.append('<p class="note">Without JavaScript, the button opens the full <a href="/venues/">venue list</a>.</p>')
    return "".join(bits)

def home():
    cards = []
    for lg in LEAGUE_ORDER:
        vs = by_league(lg)
        links = ", ".join('<a href="/venues/%s/">%s</a>' % (v["slug"], E(v["name"])) for v in vs[:6])
        cards.append('<li class="card"><h3><a href="/leagues/%s/">%s</a></h3><p>%s</p><p><a href="/leagues/%s/">All %d</a></p></li>' % (
            lg, LEAGUE_NAME[lg], links, lg, len(vs)))
    body = '''<section class="hero"><h1>Which seats should you pick?</h1>
<p class="answer">Seat guides for %d major US stadiums and arenas. Each page answers one question: which seats are the best at that building, and which should you skip? We use public stadium lists and the venue's own page when we could open one. If a section number is not in those sources, it is not on the page.</p>
%s
<p class="btnrow"><a class="btn" href="/venues/">Browse every venue</a> <a class="btn alt" href="/guides/how-to-choose-a-seat/">How to choose a seat</a></p>
</section>
<h2>Venues by league</h2><ul class="cards">%s</ul>
<h2>Guides</h2><ul class="cols">
<li><a href="/guides/how-to-choose-a-seat/">How to choose a seat</a></li>
<li><a href="/guides/shade-and-sun/">Shade and sun</a></li>
<li><a href="/guides/sections-to-skip/">Sections to skip</a></li>
<li><a href="/guides/accessible-seating/">Accessible seating</a></li>
<li><a href="/guides/club-seats/">What club seats include</a></li>
<li><a href="/guides/nfl-stadiums-with-a-roof/">Which NFL stadiums have a roof</a></li>
<li><a href="/guides/mlb-ballparks-with-a-retractable-roof/">Which MLB ballparks have a retractable roof</a></li>
<li><a href="/states/">Browse by state</a></li>
<li><a href="/cities/">Browse by city</a></li>
</ul>
<h2>How a page is built</h2>
<p>We copy capacity, roof, year opened, and home teams from a public list, and we link the official page when a check on %s got a response. We do not invent section numbers, shade maps, or obstructed view lists. <a href="/methodology/">Sources and methods</a>.</p>''' % (
        len(VENUES), picker_html(), "".join(cards), config.VERIFIED)
    pairs = [
        ("Which seats should I pick?",
         "Open the venue you are attending. The page tells you how to read that chart, and which seats to skip when the ticket says limited view, obstructed view, or partial view. Section numbers appear only when a source prints them."),
        ("Which venues does this guide cover?",
         "This guide covers %d major US stadiums and arenas in the NFL, MLB, NBA, NHL, and college football. A building used by two teams has one page." % len(VENUES)),
    ]
    body += faq_html(pairs)
    desc = "Which seats to pick at major US stadiums and arenas, and which to skip. Sourced guides for NFL, MLB, NBA, NHL, and college."
    write("/", page("/", "Which Seating: Best Seats at US Stadiums and Arenas", desc, body, extra_ld=[
        article("Which seats should you pick?", "/"), faq_ld(pairs)]))

def guide(path, title, h1, desc, body_html, pairs, sources, mod=None, published=None,
          verified=None, image=None, sources_retrieved=None):
    # mod is dateModified / sitemap lastmod. published is datePublished (defaults
    # to mod, then to the launch PUBLISHED). verified is the byline date.
    # sources_retrieved overrides the Sources "Retrieved" line when this page
    # checked different primary pages than the global venue list date.
    crumbs = [("/", "Home"), (path, h1)]
    ver = verified or config.VERIFIED
    crumbs_hub = '<p class="hubline">Guides hub: <a href="/guides/how-to-choose-a-seat/">How to choose a seat</a> · <a href="/leagues/">Leagues</a> · <a href="/venues/">Venues</a></p>'
    art = article(h1, path, mod=mod, published=published, image=image)
    src = sources_html(sources, retrieved=sources_retrieved)
    body = '<article class="prose"><h1>%s</h1><p class="byline">By %s. Last verified %s.</p>%s%s%s%s</article>' % (
        E(h1), BRAND, ver, body_html, faq_html(pairs), src, crumbs_hub)
    write(path, page(path, title, desc, body, crumbs, [art, faq_ld(pairs)], mod=mod))

def guides():
    lists = [
        {"title": "List of current NFL stadiums", "url": "https://en.wikipedia.org/wiki/List_of_current_NFL_stadiums", "publisher": "Wikipedia", "role": "list"},
        {"title": "List of current Major League Baseball stadiums", "url": "https://en.wikipedia.org/wiki/List_of_current_Major_League_Baseball_stadiums", "publisher": "Wikipedia", "role": "list"},
        {"title": "List of NBA arenas", "url": "https://en.wikipedia.org/wiki/List_of_NBA_arenas", "publisher": "Wikipedia", "role": "list"},
        {"title": "List of National Hockey League arenas", "url": "https://en.wikipedia.org/wiki/List_of_National_Hockey_League_arenas", "publisher": "Wikipedia", "role": "list"},
        {"title": "List of NCAA Division I FBS football stadiums", "url": "https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_FBS_football_stadiums", "publisher": "Wikipedia", "role": "list"},
        {"title": "MLB.com ballpark guide directory", "url": "https://www.mlb.com/fans/ballpark-guides/mlb", "publisher": "MLB.com", "role": "official"},
    ]
    vlink = lambda name: '<a href="/venues/%s/">%s</a>' % (slug(name), name)
    g1 = '''<p class="answer">Read the venue page, then the official page it links, then the ticket. Use the lowest level near the middle of the playing surface for a straight on view. Skip any seat marked limited view. Do not trust a section number that Which Seating did not copy from a source.</p>
<h2>Steps</h2>
<ol>
<li>Open the venue in this guide. Start with a league: <a href="/leagues/nfl/">NFL</a>, <a href="/leagues/mlb/">MLB</a>, <a href="/leagues/nba/">NBA</a>, <a href="/leagues/nhl/">NHL</a>, or <a href="/leagues/college-football/">college football</a>.</li>
<li>Read the roof line. A dome, a fixed roof, or an indoor arena changes the sun question. A retractable roof depends on the event. <a href="/guides/shade-and-sun/">Shade and sun</a>.</li>
<li>Use the official page linked on the venue for the real section map. Our bowl drawing is generic.</li>
<li>On the ticket, reject limited view, obstructed view, and partial view unless you mean to buy that seat. <a href="/guides/sections-to-skip/">Sections to skip</a>.</li>
<li>For step free seats and companion seats, use the venue accessibility office. <a href="/guides/accessible-seating/">Accessible seating</a>.</li>
<li>If the ticket names a club, read what that club includes before you treat it as a better view. <a href="/guides/club-seats/">What club seats include</a>.</li>
</ol>
<h2>Examples</h2>
<ul>
<li>%s, an open air NFL stadium.</li>
<li>%s, a retractable NFL roof.</li>
<li>%s, a dome.</li>
<li>%s, a baseball park with an official MLB.com ballpark page.</li>
<li>%s, an indoor arena shared by two teams.</li>
</ul>''' % (vlink("Lambeau Field"), vlink("AT&T Stadium"), vlink("Caesars Superdome"), vlink("Yankee Stadium"), vlink("Madison Square Garden"))
    p1 = [("What is the safest way to pick a section?",
           "Use the venue's own chart and the words on the ticket. Which Seating will not give you a section number the venue did not publish in our sources."),
          ("Do you rank sections by price?",
           "No. Prices change by opponent and by day. We do not publish a value ranking.")]
    guide("/guides/how-to-choose-a-seat/", "How to Choose a Stadium Seat", "How to choose a seat",
          "How to pick a stadium or arena seat using the official chart, the roof, and the ticket.",
          g1, p1, lists)
    g2 = '''<p class="answer">Sun depends on the roof class in the source list. We do not publish a shade map by section, because the lists we use do not print one.</p>
<h2>Roof classes in this guide</h2>
<ul>
<li><strong>Open air.</strong> Sun and weather reach the seats. Example: %s. We still do not name a sunny section.</li>
<li><strong>Retractable.</strong> Sun depends on whether the roof is open that day. Examples: %s and %s.</li>
<li><strong>Dome.</strong> The roof stays closed in normal use, so sun is not a seating factor. Example: %s.</li>
<li><strong>Skylight.</strong> A fixed roof, not open stands. The list does not say which sections get more light. Example: %s.</li>
<li><strong>Fixed.</strong> A baseball roof that does not open. Example: %s.</li>
<li><strong>Indoor arena.</strong> Sun is not the way to pick a seat. Example: %s.</li>
<li><strong>Not stated.</strong> The college list we used has no roof column. Example: %s. We do not guess.</li>
</ul>
<p>See every NFL stadium grouped by roof: <a href="/guides/nfl-stadiums-with-a-roof/">Which NFL stadiums have a roof</a>. See every MLB ballpark grouped by roof: <a href="/guides/mlb-ballparks-with-a-retractable-roof/">Which MLB ballparks have a retractable roof</a>.</p>''' % (vlink("Lambeau Field"), vlink("AT&T Stadium"), vlink("Chase Field"), vlink("Ford Field"),
        vlink("SoFi Stadium"), vlink("Tropicana Field"), vlink("Madison Square Garden"), vlink("Michigan Stadium"))
    p2 = [("Do you publish a sunny section for each park?",
           "No. A shade map by section was not in the sources, so naming one would be a guess."),
          ("What if the roof can open?",
           "Treat a retractable roof as open air when it is open, and as a closed building when it is shut. The list does not say which sections are shaded either way.")]
    guide("/guides/shade-and-sun/", "Stadium Shade and Sun", "Shade and sun",
          "How roof type changes sun and shade at a stadium, without invented section numbers.",
          g2, p2, lists)
    g3 = '''<p class="answer">Skip a seat when the chart or the ticket says limited view, obstructed view, or partial view. We do not keep a second list of bad section numbers.</p>
<h2>The one sourced closure in this guide</h2>
<p>At %s, the Wikipedia MLB list gives a capacity of 25,000 and cites a 2019 USA Today report that the Rays closed the upper deck. Do not assume an upper deck seat there is on sale. Check the current Rays ballpark page.</p>
<h2>What we will not do</h2>
<p>Fan sites publish long lists of sections to avoid. We do not copy those lists. If the venue has not printed the number, it is not here. Report a venue page that does publish an obstructed list and we will add it with a citation. <a href="/contact/">Contact</a>.</p>''' % vlink("Tropicana Field")
    p3 = [("Which section numbers should I avoid?",
           "Only numbers the venue or the ticket marks as limited, obstructed, or partial view. This guide does not invent a blacklist."),
          ("Is the Tropicana Field upper deck open?",
           "A 2019 report cited on the Wikipedia MLB list said the Rays closed the upper deck. Confirm the current chart before you buy.")]
    guide("/guides/sections-to-skip/", "Stadium Sections to Skip", "Sections to skip",
          "Skip limited view and obstructed seats. We do not invent a list of bad section numbers.",
          g3, p3, lists + [{"title": "Tampa Bay Rays reduce seating capacity at Tropicana Field",
                           "url": "https://www.usatoday.com/story/sports/mlb/rays/2019/01/04/rays-tropicana-field-close-upper-deck-reduce-capacity/2481217002/",
                           "publisher": "USA Today", "role": "extra"}])
    mid_reads_access = next_reads([
        ("/guides/how-to-choose-a-seat/", "How to choose a seat", "The chart, the roof, and the ticket, in that order."),
        ("/guides/club-seats/", "What club seats include", "Lounge access, covered seats, and in seat service, only where venues publish them."),
        ("/guides/sections-to-skip/", "Sections to skip", "Limited view, obstructed view, and the one sourced upper deck closure."),
    ], heading="Related guides")
    end_reads_access = next_reads([
        ("/guides/shade-and-sun/", "Shade and sun", "How roof class changes the sun question."),
        ("/guides/nfl-stadiums-with-a-roof/", "Which NFL stadiums have a roof", "Dome, retractable, skylight, or open air."),
        ("/leagues/mlb/", "MLB venues", "Every ballpark page on this site."),
        ("/venues/", "All venues", "Browse every stadium and arena guide."),
    ], heading="More to read")
    compare_access = compare_box(
        "Check another venue",
        "Accessible inventory is sold per event. Open the venue page on this site, then the official accessibility page it points to.",
        [("/venues/lambeau-field/", "Lambeau Field"),
         ("/venues/yankee-stadium/", "Yankee Stadium"),
         ("/venues/angel-stadium/", "Angel Stadium"),
         ("/venues/loandepot-park/", "LoanDepot Park"),
         ("/venues/madison-square-garden/", "Madison Square Garden")])
    g4 = '''%s
<p class="answer">Accessible seats are a separate inventory from the standard section map. Buy the wheelchair or companion ticket the venue sells for that event, and confirm the path from your gate. This guide cites only section lists that the venue itself publishes in plain text.</p>
<h2>What every fan should ask before buying</h2>
<ul>
<li>Which ticket type you need: wheelchair space, companion seat, aisle transfer seat, or semi ambulatory seat.</li>
<li>Whether the path from the gate on your ticket is step free to that section.</li>
<li>How many companion seats you can buy next to the accessible space.</li>
<li>Whether the venue relocates season tickets game by game when accessible inventory is still open.</li>
</ul>
%s
<h2>What official ADA pages publish today</h2>
<p>These facts come from the venue pages linked in Sources, checked %s. Layouts change, so re check the live page before you buy.</p>
<h3>%s</h3>
<p>The Packers guests with disabilities page says you must obtain wheelchair and companion tickets before entering if you will watch from a wheelchair or scooter. Season ticket holders can trade non accessible tickets for wheelchair and companion seats game by game when inventory remains, with a stated limit of one wheelchair and one companion seat per swap. Wheelchair and companion season seats are sold to people whose disability requires that seating, with a stated limit of four tickets (one wheelchair and up to three companions). The page does not print a public list of accessible section numbers.</p>
<h3>%s</h3>
<p>The Yankees Guide for Guests with Disabilities says wheelchair accessible and designated aisle transfer seats are sold at various price points and locations. The same page lists electrical outlets for recharging mobility equipment at wheelchair accessible seating areas in sections 021B, 029, 104 through 106, 109, 111, 114A, 116, 118 through 121B, 124, 127A, 130, 132 through 134, 211, 225, 226, 305, 306, 309, 310, 313 through 315, 317 through 320A, 320C through 323, 325 through 327, 330, 331, 333 and 334, plus bleacher sections 203 and 235 through 237. It also states there are 16 public elevators. For current seat locations, the page directs guests to Disabled Services rather than a printable chart of every open wheelchair row.</p>
<h3>%s</h3>
<p>The Angels accessible seating page says more than 500 wheelchair, semi ambulatory, and companion tickets are available. It lists accessible seating on the Terrace Level in sections 201 through 213 and 221 through 233, the Left Field Pavilion in sections 257 through 260, and the Right Field Pavilion in sections 241 through 249. It also lists accessible seats in premium club areas including the Lexus Diamond Club (sections 114 through 122) and Club Level sections 322 and 330, and notes that seating in those premium areas offers in seat food and beverage service. A buyer of an accessible seat may purchase up to three additional contiguous companion seats in the same row when they remain available.</p>
<h3>%s</h3>
<p>The Marlins disability access guide says wheelchair accessible and semi ambulatory seats with operable armrests sit on all ballpark levels, and one companion or escort may accompany a guest with a disability in the designated areas. The same guide lists electrical outlets at wheelchair accessible seating on the Promenade Level (sections 1, 9 through 20, 28, 30 through 31, 35 and 39), Legends Level (sections 205, 211, 220 and 223), and Vista Level (sections 309 through 311, 317, 319, 320 and 322). Wheelchair transport is offered from an entrance to a seating section and back.</p>
<h3>%s</h3>
<p>The Madison Square Garden site states that the arena provides wheelchair seats, designated aisle transfer seats, and companion seats, plus accessible restrooms and assisted listening devices. It does not publish a plain text list of accessible section numbers on the pages we opened; it points guests to Accessibility Services for event specific inventory.</p>
%s
<h2>How this ties to picking any seat</h2>
<p>Accessible inventory is not a substitute for reading the chart. If you also care about sun, roof, or a limited view label, use <a href="/guides/how-to-choose-a-seat/">How to choose a seat</a>, <a href="/guides/shade-and-sun/">Shade and sun</a>, and <a href="/guides/sections-to-skip/">Sections to skip</a> alongside the venue accessibility office.</p>
%s''' % (
        hero_photo("Empty stadium seating bowl at dusk with lights on along the aisles"),
        mid_reads_access, config.VERIFIED_TODAY,
        vlink("Lambeau Field"), vlink("Yankee Stadium"), vlink("Angel Stadium"),
        vlink("LoanDepot Park"), vlink("Madison Square Garden"),
        compare_access, end_reads_access)
    p4 = [("Which section is accessible?",
           "Only sections the venue lists for accessible inventory. Yankee Stadium, Angel Stadium, and LoanDepot Park publish section lists on their ADA pages linked in Sources. Lambeau Field and Madison Square Garden direct you to their accessibility offices instead of a public section list."),
          ("Can a companion sit with me?",
           "Yes when the venue sells companion seats. The Angels page allows up to three contiguous companions with an accessible seat when available. The Marlins guide allows one companion or escort in designated areas. Lambeau Field states limits on wheelchair and companion pairs. Confirm the pair on the ticket for your event."),
          ("Do accessible seats appear on the normal map?",
           "Often not until you ask for accessible inventory. Treat the ADA page and the ticket office path as the source, not a generic seating diagram."),
          ("What if my ticketed seat does not work for my disability?",
           "Several venues describe a relocation process through guest services when a ticketed seat cannot accommodate a disability. Ask at the venue; this guide does not invent a relocation rule.")]
    access_sources = [
        {"title": "Packers Services for Guests with Disabilities", "url": "https://www.packers.com/tickets/guests-with-disabilities", "publisher": "Green Bay Packers", "role": "official"},
        {"title": "Yankee Stadium Guide For Guests With Disabilities", "url": "https://www.mlb.com/yankees/ballpark/information/disabled-services", "publisher": "MLB.com / New York Yankees", "role": "official"},
        {"title": "Accessible Seating | Los Angeles Angels", "url": "https://www.mlb.com/angels/tickets/accessible-seating", "publisher": "MLB.com / Los Angeles Angels", "role": "official"},
        {"title": "Accessibility Guide | Los Angeles Angels", "url": "https://www.mlb.com/angels/ballpark/accessibility-guide", "publisher": "MLB.com / Los Angeles Angels", "role": "official"},
        {"title": "Access Guide for Guests With Disabilities | Miami Marlins", "url": "https://www.mlb.com/marlins/ballpark/disability-access-guide", "publisher": "MLB.com / Miami Marlins", "role": "official"},
        {"title": "Madison Square Garden", "url": "https://www.msg.com/madison-square-garden", "publisher": "Madison Square Garden", "role": "official"},
    ]
    guide("/guides/accessible-seating/", "Accessible Stadium Seating: What Venues Publish",
          "Accessible seating: what venues publish",
          "Accessible stadium seats from official ADA pages: wheelchair, companion, and aisle transfer facts without guessing.",
          g4, p4, access_sources, mod=config.TODAY, published=config.PUBLISHED,
          verified=config.VERIFIED_TODAY, image=HERO_IMG, sources_retrieved=config.VERIFIED_TODAY)

    def roof_groups(lg):
        groups = {}
        for v in by_league(lg):
            groups.setdefault(v["roof_label"], []).append(v)
        return groups

    def roof_list_html(vs):
        return "<ul>" + "".join(
            "<li>%s, home to %s, in %s.</li>" % (vlink(v["name"]), E(team_list(v)), E(place(v))) for v in vs
        ) + "</ul>"

    nfl_roof = roof_groups("nfl")
    nfl_order = [("Dome", "Dome (closed in normal use)"),
                 ("Retractable", "Retractable roof (open or closed by game day)"),
                 ("Skylight", "Skylight roof (a fixed roof, not open stands)"),
                 ("Open-air", "Open air (no roof over the seats)")]
    nfl_sections = "".join(
        "<h2>%s: %d stadium%s</h2>%s" % (label, len(nfl_roof.get(key, [])), "" if len(nfl_roof.get(key, [])) == 1 else "s", roof_list_html(nfl_roof.get(key, [])))
        for key, label in nfl_order if nfl_roof.get(key)
    )
    g5 = '''<p class="answer">The Wikipedia list of current NFL stadiums classifies all %d stadiums by roof. %d are open air, %d have a retractable roof, %d have a fixed skylight roof, and %d are a dome. The roof class is the first fact worth checking before you weigh sun, wind, or rain for a section.</p>
%s
<h2>Why the roof class matters for your seat</h2>
<p>A dome, or a retractable roof that stays closed for the game, removes sun and weather from the seating decision. A skylight roof still lets in daylight through a fixed structure, but it is not open to the sky the way a true open air bowl is. At an open air stadium, sun and wind are back on the table, and which side of the field gets the afternoon sun depends on the building's orientation, a detail this stadium list does not publish. See <a href="/guides/shade-and-sun/">Shade and sun</a> for how this site reads that question per venue, and the stadium's own page, linked from each venue guide below, for any shade chart it publishes.</p>
<p>Open the <a href="/leagues/nfl/">NFL venues</a> hub for every stadium page, or use <a href="/guides/how-to-choose-a-seat/">How to choose a seat</a> for the general method.</p>''' % (
        len(by_league("nfl")), len(nfl_roof.get("Open-air", [])), len(nfl_roof.get("Retractable", [])),
        len(nfl_roof.get("Skylight", [])), len(nfl_roof.get("Dome", [])), nfl_sections)
    p5 = [("Which NFL stadiums have a dome?",
           "On the current Wikipedia stadium list: %s." % ", ".join(v["name"] for v in nfl_roof.get("Dome", []))),
          ("Which NFL stadiums have a retractable roof?",
           "On the current Wikipedia stadium list: %s." % ", ".join(v["name"] for v in nfl_roof.get("Retractable", []))),
          ("Which NFL stadiums are open air with no roof?",
           "%d of the 30 stadiums on the list have no roof: %s." % (len(nfl_roof.get("Open-air", [])), ", ".join(v["name"] for v in nfl_roof.get("Open-air", [])))),
          ("Does a retractable roof mean the stadium is always closed?",
           "No. A retractable roof can be open or closed for a given game. The source list does not say how often each team opens it, so this page does not guess.")]
    guide("/guides/nfl-stadiums-with-a-roof/", "Which NFL Stadiums Have a Roof?", "Which NFL stadiums have a roof?",
          "Every NFL stadium grouped by roof type: dome, retractable, skylight, or open air, with the home team and city.",
          g5, p5, [lists[0]], mod="2026-11-18")

    mlb_roof = roof_groups("mlb")
    mlb_order = [("Retractable", "Retractable roof (open or closed by game day)"),
                 ("Fixed", "Fixed roof (does not open)"),
                 ("Open", "Open air (no roof over the seats)")]
    mlb_sections = "".join(
        "<h2>%s: %d ballpark%s</h2>%s" % (label, len(mlb_roof.get(key, [])), "" if len(mlb_roof.get(key, [])) == 1 else "s", roof_list_html(mlb_roof.get(key, [])))
        for key, label in mlb_order if mlb_roof.get(key)
    )
    g6 = '''<p class="answer">The Wikipedia list of current MLB stadiums classifies all %d ballparks by roof. %d have a retractable roof, %d is a fixed roof that does not open, and %d are open air. Checking this before the shade question matters more in baseball than in most sports, because a day game can run three hours or longer under the sun.</p>
%s
<h2>The one fixed roof: %s</h2>
<p>%s is the single MLB park on this list with a fixed, non opening roof, so sun is not a seating factor there the way it is at an open air park. A 2019 report cited on the same Wikipedia list said the team closed the ballpark's upper deck and reduced capacity; the <a href="/guides/sections-to-skip/">Sections to skip</a> guide carries that note and its source. Confirm the current chart before you buy.</p>
<h2>Why roof class matters for your seat</h2>
<p>At a retractable roof park, sun exposure depends on whether the roof is open for that game, which this list does not record game by game. At an open air park, sun and wind reach every seat, and which side of the field gets the afternoon sun depends on the park's orientation, a detail these sources do not publish. See <a href="/guides/shade-and-sun/">Shade and sun</a> for our general method, and open the park's own page, linked from each venue guide below, for a shade chart if the team publishes one.</p>
<p>Open the <a href="/leagues/mlb/">MLB venues</a> hub for every ballpark page, or use <a href="/guides/how-to-choose-a-seat/">How to choose a seat</a> for the general method.</p>''' % (
        len(by_league("mlb")), len(mlb_roof.get("Retractable", [])), len(mlb_roof.get("Fixed", [])),
        len(mlb_roof.get("Open", [])), mlb_sections,
        E(mlb_roof["Fixed"][0]["name"]) if mlb_roof.get("Fixed") else "none",
        E(mlb_roof["Fixed"][0]["name"]) if mlb_roof.get("Fixed") else "No park on this list carries that label")
    p6 = [("Which MLB ballparks have a retractable roof?",
           "On the current Wikipedia stadium list: %s." % ", ".join(v["name"] for v in mlb_roof.get("Retractable", []))),
          ("Which MLB ballpark has a fixed roof that does not open?",
           "%s, on the current Wikipedia stadium list." % ", ".join(v["name"] for v in mlb_roof.get("Fixed", []))),
          ("Which MLB ballparks are open air with no roof?",
           "%d of the %d parks on the list have no roof, including %s and %s." % (
               len(mlb_roof.get("Open", [])), len(by_league("mlb")),
               mlb_roof["Open"][0]["name"] if mlb_roof.get("Open") else "none",
               mlb_roof["Open"][1]["name"] if len(mlb_roof.get("Open", [])) > 1 else "others on the list")),
          ("Is the Tropicana Field upper deck open?",
           "A 2019 report cited on the Wikipedia MLB list said the team closed the upper deck. Confirm the current chart before you buy.")]
    guide("/guides/mlb-ballparks-with-a-retractable-roof/", "Which MLB Ballparks Have a Retractable Roof?",
          "Which MLB ballparks have a retractable roof?",
          "Every MLB ballpark grouped by roof type: retractable, fixed, or open air, with the home team and city.",
          g6, p6, [lists[1], lists[5], {"title": "Tampa Bay Rays reduce seating capacity at Tropicana Field",
                            "url": "https://www.usatoday.com/story/sports/mlb/rays/2019/01/04/rays-tropicana-field-close-upper-deck-reduce-capacity/2481217002/",
                            "publisher": "USA Today", "role": "extra"}], mod="2026-11-18")

    mid_reads_club = next_reads([
        ("/guides/how-to-choose-a-seat/", "How to choose a seat", "Roof, chart, and ticket labels before you spend on a club."),
        ("/guides/shade-and-sun/", "Shade and sun", "Open air vs retractable vs dome, without invented shade maps."),
        ("/guides/nfl-stadiums-with-a-roof/", "Which NFL stadiums have a roof", "Roof class for every NFL stadium on our list."),
    ], heading="Related guides")
    end_reads_club = next_reads([
        ("/guides/mlb-ballparks-with-a-retractable-roof/", "MLB retractable roofs", "Which ballparks can close the roof on game day."),
        ("/guides/accessible-seating/", "Accessible seating", "What ADA pages publish about wheelchair and companion seats."),
        ("/guides/sections-to-skip/", "Sections to skip", "Limited view and obstructed labels to reject on the ticket."),
        ("/leagues/nfl/", "NFL venues", "Every NFL stadium guide on this site."),
    ], heading="More to read")
    compare_club = compare_box(
        "Check another seat question",
        "Club amenities are venue specific. Pair this page with a venue guide, a roof guide, or the accessible seating page.",
        [("/venues/lucas-oil-stadium/", "Lucas Oil Stadium"),
         ("/venues/empower-field-at-mile-high/", "Empower Field at Mile High"),
         ("/venues/soldier-field/", "Soldier Field"),
         ("/venues/loandepot-park/", "LoanDepot Park"),
         ("/venues/angel-stadium/", "Angel Stadium"),
         ("/guides/shade-and-sun/", "Shade and sun")])
    g7 = '''%s
<p class="answer">Club seats are a premium ticket tier. What you get is whatever that venue prints for that club: lounge access, padded seats, private entrances, and sometimes included food or in seat service. This page compares only official club pages we opened on %s. It does not publish prices, and it does not invent a package for a stadium we did not check.</p>
<h2>What "club seats" usually means on official pages</h2>
<p>Across the NFL and MLB club pages below, three promises show up again and again:</p>
<ul>
<li><strong>Lounge access.</strong> A climate controlled or private club space behind or beside the seats, often open before kickoff or first pitch and for a stated window after the game.</li>
<li><strong>Better seat hardware.</strong> Wider or padded seats, sometimes with extra leg room, in a named club section.</li>
<li><strong>Separate entry.</strong> VIP or private entrances that skip the general gate line.</li>
</ul>
<p>Food and drink are not one rule. Some clubs include food and selected drinks. Others sell specialty food inside the lounge. Always read the amenity list for the exact club name on your ticket.</p>
%s
<h2>NFL examples from team club pages</h2>
<h3>%s (Indianapolis Colts)</h3>
<p>The Colts club seats page describes the KennMar East Club and Ascension St. Vincent West Club. It lists padded seats with extra leg room between the 25 yard lines, VIP entrances for premium ticket holders, club lounges with live music and complimentary samplings, and a concierge desk in each lounge. Lounge sampling is described as available from gate open until kickoff while supplies last. The page does not claim a full all inclusive meal plan for every club seat.</p>
<h3>%s (Denver Broncos)</h3>
<p>The Broncos United Globe Club page lists club level access three hours before kickoff and up to one hour after the game, exclusive premium entrances, extra wide 22 inch padded seats, and high end food and beverage with named action stations, pizza ovens, and full service bars. West Club sections 300 through 315 and East Club sections 331 through 346 are named on that page.</p>
<h3>%s (Chicago Bears)</h3>
<p>The Bears United Club page places club seats on the east side of Soldier Field on the 200 and 300 levels and lists climate controlled indoor lounge access for club seat ticket holders. It says the lounge opens two hours before kickoff and stays open about five hours after the game starts. Amenities named on the page include private entrances and restrooms, specialty food, 12 full service bars, 21 inch wide cushioned seats, a private team store, and more than 140 indoor TVs. The page also lists the United Club section numbers on those two levels.</p>
<h2>MLB examples from team premium pages</h2>
<h3>%s (Miami Marlins)</h3>
<p>The Marlins PNC Club page lists valet parking, a private entrance, all inclusive food and beverage including house wine, beer, and soft drinks, a private lounge, large cushioned seats, and in seat service. It states the club is available to Marlins Members.</p>
<h3>%s (Los Angeles Angels)</h3>
<p>The Angels Don Julio Club page places seats behind home plate on the Terrace Level, with executive style seating and countertops, exclusive lounge access, food and non alcoholic beverages included, and preferred parking options. It does not describe in seat delivery on that page.</p>
%s
<h2>Are club seats "worth it"?</h2>
<p>Which Seating does not publish prices or a value score. Worth depends on which printed amenity you actually need:</p>
<ol>
<li><strong>Watching the play.</strong> A club seat still has to face the field well. Use <a href="/guides/how-to-choose-a-seat/">How to choose a seat</a> and the venue chart. A lounge does not fix a bad angle.</li>
<li><strong>Weather.</strong> An indoor lounge helps at an open air stadium when you can leave your seat. It does not change the roof over the seat itself. Check <a href="/guides/nfl-stadiums-with-a-roof/">Which NFL stadiums have a roof</a> and <a href="/guides/mlb-ballparks-with-a-retractable-roof/">Which MLB ballparks have a retractable roof</a> first.</li>
<li><strong>Food included vs for purchase.</strong> The Marlins PNC Club and Angels Don Julio Club pages describe included food. The Colts club page emphasizes lounge samplings and specialty menus. The Broncos page highlights action stations and bars. Match the ticket name to the amenity list.</li>
<li><strong>In seat service.</strong> The Marlins PNC Club page names in seat service. The Angels accessible seating page notes in seat service in some premium accessible areas. Do not assume every club seat includes runners.</li>
<li><strong>Access time.</strong> Broncos and Bears pages state lounge open windows before and after the game. If early entry matters, verify the hours on the club page for that season.</li>
</ol>
<p>If the official page does not list lounge access, covered seating, or in seat service for the product on your ticket, this site will not invent them. Open the venue page on Which Seating, then the official premium link in its sources.</p>
%s''' % (
        hero_photo("Empty stadium seating bowl at dusk with lights on along the aisles"),
        config.VERIFIED_TODAY, mid_reads_club,
        vlink("Lucas Oil Stadium"), vlink("Empower Field at Mile High"), vlink("Soldier Field"),
        vlink("LoanDepot Park"), vlink("Angel Stadium"),
        compare_club, end_reads_club)
    p7 = [("What do club seats include?",
           "Whatever that venue lists for the named club: often lounge access, padded seats, and a private entrance. Food may be included or sold separately. Read the club page for the ticket name you hold."),
          ("Do club seats come with in seat service?",
           "Only when the venue says so. The Marlins PNC Club page names in seat service. Other club pages we checked emphasize lounges and bars instead. Do not assume runners at every club seat."),
          ("Are club seats covered from sun and rain?",
           "Not automatically. A climate controlled lounge is not the same as a roof over your seat. Check the stadium roof class and the club page before you buy."),
          ("Are club seats worth the upgrade?",
           "This site does not publish prices or a value score. Decide from the printed amenities: lounge hours, included food, seat width, private entry, and whether the view matches what you want to watch.")]
    club_sources = [
        {"title": "Colts Premium Seating | Club Seating", "url": "https://www.colts.com/tickets/premium-seating/club-seats/", "publisher": "Indianapolis Colts", "role": "official"},
        {"title": "United Globe Club", "url": "https://www.denverbroncos.com/tickets/premiumseating/unitedclublevel", "publisher": "Denver Broncos", "role": "official"},
        {"title": "United Club | Chicago Bears", "url": "https://www.chicagobears.com/game-day/united-club", "publisher": "Chicago Bears", "role": "official"},
        {"title": "PNC Club | Miami Marlins", "url": "https://www.mlb.com/marlins/tickets/premium/the-club", "publisher": "MLB.com / Miami Marlins", "role": "official"},
        {"title": "Don Julio Club | Los Angeles Angels", "url": "https://www.mlb.com/angels/tickets/premium/don-julio-club", "publisher": "MLB.com / Los Angeles Angels", "role": "official"},
    ]
    guide("/guides/club-seats/", "What Do NFL and MLB Club Seats Include?",
          "What do NFL and MLB club seats include?",
          "What club seats include at NFL and MLB venues: lounge access, covered comfort, and in seat service, only where venues say so.",
          g7, p7, club_sources, mod=config.TODAY, published=config.TODAY,
          verified=config.VERIFIED_TODAY, image=HERO_IMG, sources_retrieved=config.VERIFIED_TODAY)

def legal_wrap(path, title, h1, desc, inner, mod=None, published=None):
    crumbs = [("/", "Home"), (path, h1)]
    body = '<article class="prose"><h1>%s</h1>%s<p class="legal-line">%s</p></article>' % (E(h1), inner, config.LEGAL_LINE)
    write(path, page(path, title, desc, body, crumbs,
                     [article(h1, path, mod=mod, published=published)], legal=True, mod=mod))

def static_pages():
    legal_wrap("/editorial-policy/", "Editorial Policy | Which Seating", "Editorial policy",
               "Editorial policy for Which Seating: sourcing, bylines, and corrections.",
               '''<p>Last updated %s. This policy governs Which Seating (whichseating.com), a trade name of Joshua Israel Ventures LLC.</p>
<h2>What we publish</h2>
<p>Evergreen seat guides. Each venue page answers which seats to pick at that building and which to skip. We do not publish scores, rumors, or ticket prices.</p>
<h2>Sourcing</h2>
<p>A factual claim needs a source on the page. We prefer the venue's own page and public league or stadium lists. If a detail is not in those sources, we leave it out. We do not invent section numbers, shade maps, or obstructed view lists.</p>
<h2>Byline</h2>
<p>The byline on a guide is Which Seating, the site. It is not a personal byline. The author in our Article markup is the organization Which Seating.</p>
<h2>Dates</h2>
<p>datePublished is the first publication date of the page and is not taken from the build clock. dateModified changes only when the page's facts change. The "last verified" line is the date we last checked the sources.</p>
<h2>Independence</h2>
<p>No team, league, venue, or ticket seller pays for a listing or for a change to a page. We do not display team logos. Names are plain text so you can tell the buildings apart.</p>
<h2>Corrections</h2>
<p>If a venue publishes a section fact we missed, or a fact on a page is wrong, email <a href="mailto:%s">%s</a> with the page address and the source. We correct verified mistakes.</p>''' % (config.VERIFIED, config.CONTACT_EMAIL, config.CONTACT_EMAIL))
    # editorial policy contains the email. It is a legal page. Good.
    # But "Joshua" appears in the legal line which is added by legal_wrap, and also "Joshua Israel Ventures LLC" in the first paragraph. Good.
    body = '''<p>Which Seating is an independent guide to seats at major US stadiums and arenas. Ticket maps show every section. We answer a smaller question: where to start, and what to skip, using facts we can cite.</p>
<h2>What we cover</h2>
<p>%d venues across the NFL, MLB, NBA, NHL, and major college football stadiums. A building shared by two teams has one page.</p>
<h2>How we work</h2>
<p>Every venue page starts from a public list and, when we could open one, the venue's own page. We write the reading method ourselves and we label it as a method. See <a href="/methodology/">sources and methods</a> and the <a href="/editorial-policy/">editorial policy</a>.</p>
<h2>Independence</h2>
<p>Which Seating is not affiliated with any team, league, venue, or ticket seller. It is the stadium companion to <a href="https://whichcabin.com/">Which Cabin</a>.</p>
<p>See a mistake after a renovation? <a href="/contact/">Write to us</a>.</p>''' % len(VENUES)
    write("/about/", page("/about/", "About Which Seating",
                          "What Which Seating is and how the seat guides are checked.",
                          '<article class="prose"><h1>About Which Seating</h1>%s</article>' % body,
                          [("/", "Home"), ("/about/", "About Which Seating")], [article("About Which Seating", "/about/")]))
    meth = '''<h2>Lists</h2>
<p>Capacity, year opened, roof, surface, and home team come from these public lists, retrieved %s:</p>
<ul>
<li><a href="https://en.wikipedia.org/wiki/List_of_current_NFL_stadiums" rel="nofollow noopener">List of current NFL stadiums</a></li>
<li><a href="https://en.wikipedia.org/wiki/List_of_current_Major_League_Baseball_stadiums" rel="nofollow noopener">List of current Major League Baseball stadiums</a></li>
<li><a href="https://en.wikipedia.org/wiki/List_of_NBA_arenas" rel="nofollow noopener">List of NBA arenas</a></li>
<li><a href="https://en.wikipedia.org/wiki/List_of_National_Hockey_League_arenas" rel="nofollow noopener">List of National Hockey League arenas</a></li>
<li><a href="https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_FBS_football_stadiums" rel="nofollow noopener">List of NCAA Division I FBS football stadiums</a></li>
</ul>
<p>MLB parks also link the team's ballpark page on MLB.com and the <a href="https://www.mlb.com/fans/ballpark-guides/mlb" rel="nofollow noopener">MLB.com ballpark guide directory</a>. NBA arenas also cite the <a href="https://www.nba.com/news/all-30-nba-arenas-by-team" rel="nofollow noopener">NBA.com arena list</a> updated 28 Oct 2026. Official venue URLs were kept only when a request on %s returned a page.</p>
<h2>The reading method</h2>
<p>The "how to read the chart" paragraph is ours. It describes where a straight on view sits on a normal chart for that sport. It is not a section list. The generic bowl drawing is ours too. It is not a copy of any venue map.</p>
<h2>What we leave out</h2>
<p>Section numbers, shade maps, obstructed lists, accessible section numbers, and prices, unless a source on that page states them. College roof type is left out because the FBS list has no roof column. Canadian stadiums are left out of this US guide. Rogers Centre is the MLB park we skipped for that reason.</p>
<h2>Names</h2>
<p>We use the name on the list. Where an official page uses a 2026 name, we follow that page and say so. Reliant Stadium, Highmark Stadium, and the Utah Mammoth are examples, and each page cites the page we opened.</p>
<h2>Updates</h2>
<p><a href="/contact/">Report an error</a> and we will re-check the source. We change the verified date when we do.</p>''' % (config.VERIFIED, config.VERIFIED)
    write("/methodology/", page("/methodology/", "Sources and Methods | Which Seating",
                                "Where Which Seating's stadium facts come from, and what we refuse to guess.",
                                '<article class="prose"><h1>Sources and methods</h1>%s</article>' % meth,
                                [("/", "Home"), ("/methodology/", "Sources and methods")],
                                [article("Sources and methods", "/methodology/")]))
    img = '''<p>Last updated %s.</p>
<h2>Diagrams</h2>
<p>The bowl drawing on a venue page is an original diagram. It is not a copy of a seating chart, a broadcast graphic, or a team map. The caption on that drawing links to this page.</p>
<h2>Photos</h2>
<p>Guide articles may use one realistic news style thumbnail. The caption says AI-generated image and links to this policy. Those images do not depict a real person, a readable logo, or a copied seat chart. The site logo and the default social card are simple seat drawings we made for the site.</p>
<h2>AI-generated images</h2>
<p>AI-generated illustrations are labelled in the caption as "AI-generated image" and link here. They are not photographs of a specific branded stadium event.</p>
<h2>Questions</h2>
<p>If you believe an image uses your work, see our <a href="/copyright/">copyright policy</a> or <a href="/contact/">contact us</a>.</p>''' % config.VERIFIED_TODAY
    write("/image-policy/", page("/image-policy/", "Image Policy | Which Seating",
                                 "How Which Seating handles diagrams, photos, and team marks.",
                                 '<article class="prose"><h1>Image policy</h1>%s</article>' % img,
                                 [("/", "Home"), ("/image-policy/", "Image policy")],
                                 [article("Image policy", "/image-policy/", mod=config.TODAY, published=config.PUBLISHED)],
                                 mod=config.TODAY))
    legal_wrap("/terms/", "Terms of Use | Which Seating", "Terms of use",
               "Terms of use for Which Seating (whichseating.com).",
               '''<p>Last updated %s. These terms govern your use of whichseating.com ("Which Seating", "we", "us"). Which Seating is a trade name of Joshua Israel Ventures LLC, a Florida limited liability company. By using the site you agree to these terms.</p>
<h2>Information only</h2>
<p>Which Seating provides general information to help you choose a seat. It is not ticketing, accessibility, medical, or professional advice. Seating charts, roofs, and accessible inventory are set by each venue and can change. Always check the venue's current chart and the ticket before you buy.</p>
<h2>Accuracy</h2>
<p>We work to keep information accurate and cite our sources, but we make no warranty that any information is complete, current, or error free.</p>
<h2>Acceptable use</h2>
<p>You may view and share links to our pages for personal, non-commercial use. You may not scrape the site in bulk, republish our original text or compilations without permission, misuse the contact address, or try to disrupt the site.</p>
<h2>Intellectual property</h2>
<p>Original text, design, diagrams, and data compilations on this site belong to Joshua Israel Ventures LLC. Team, league, and venue names and trademarks belong to their owners and are used only to identify the buildings. Their use does not imply affiliation or endorsement.</p>
<h2>Third party links</h2>
<p>We link to league sites, venue sites, Wikipedia, and other sources. We are not responsible for their content. The site is hosted on GitHub Pages.</p>
<h2>Disclaimer of warranties and limitation of liability</h2>
<p>The site is provided "as is" and "as available". To the fullest extent permitted by law, Joshua Israel Ventures LLC disclaims all warranties, express or implied, and will not be liable for any indirect, incidental, special, consequential, or punitive damages, or any loss arising from your use of the site or any ticket. Our total liability for any claim relating to the site is limited to US$100.</p>
<h2>Indemnity</h2>
<p>You agree to indemnify Joshua Israel Ventures LLC against claims arising from your misuse of the site or your breach of these terms.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of the State of Florida, United States, without regard to conflict of law rules. Any dispute will be resolved in the state or federal courts located in Florida, and you consent to their jurisdiction.</p>
<h2>Changes</h2>
<p>We may update these terms. The date above shows the latest version. Questions: use our <a href="/contact/">contact page</a>.</p>''' % config.VERIFIED)
    legal_wrap("/privacy/", "Privacy Policy | Which Seating", "Privacy policy",
               "Privacy policy for Which Seating (whichseating.com).",
               '''<p>Last updated %s. This policy explains how Which Seating (whichseating.com), a trade name of Joshua Israel Ventures LLC, a Florida limited liability company, handles information.</p>
<h2 id="analytics">Analytics</h2>
<p>The public site measures visits with Cloudflare Web Analytics and Google Analytics 4 (GA4). The preview build loads neither tool.</p>
<p>Cloudflare Web Analytics is the beacon at static.cloudflareinsights.com. It counts page views. It does not use cookies or local storage and does not track you across sites. It records aggregated information such as the page visited, referrer, browser, and country.</p>
<p>Google Analytics 4 loads only after you accept the cookie banner. Until you choose, Consent Mode v2 defaults are denied for analytics storage, ad storage, ad user data, and ad personalization, and the Google tag is not requested. If you accept, the site loads gtag.js for the measurement ID in the build config, and Google may set analytics cookies. If you decline, the tag stays unloaded. The Cookie settings link in the footer opens that choice again. While the measurement ID is blank, accepting does not send data to Google.</p>
<h2>Contact</h2>
<p>If you email us, we use your address and message only to reply, and we keep them only as long as needed. The address is on the <a href="/contact/">contact page</a>.</p>
<h2 id="advertising">Advertising</h2>
<p>Which Seating uses Google AdSense. Pages include the AdSense account meta tag and the AdSense script for publisher account %s. The site does not place ad units on pages yet, so you should not see display ads from this site today. When ad units go live, third party vendors including Google may use cookies to serve ads based on your prior visits to this and other websites. You can opt out of personalised advertising at <a href="https://www.google.com/settings/ads" rel="nofollow noopener" target="_blank">Google Ads Settings</a> and <a href="https://www.aboutads.info/choices/" rel="nofollow noopener" target="_blank">aboutads.info/choices</a>. Where the law requires it (for example in the EEA, the UK, and Switzerland), we will ask for consent through a certified consent management platform before any advertising cookies are set. Authorized sellers are listed in <a href="/ads.txt">ads.txt</a>. See also our <a href="/ad-disclosure/">advertising disclosure</a>.</p>
<h2>Google advertising cookies and your choices</h2><p>Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads based on your visit to this site and/or other sites on the Internet. You may opt out of personalized advertising by visiting <a href="https://adssettings.google.com/" rel="nofollow noopener">Google Ads Settings</a>. Alternatively, you can opt out of a third-party vendor's use of cookies for personalized advertising at <a href="https://www.aboutads.info/choices/" rel="nofollow noopener">aboutads.info/choices</a>. For more information, see <a href="https://policies.google.com/technologies/partner-sites" rel="nofollow noopener">how Google uses information from sites or apps that use its services</a>.</p>
<h2>Cookies</h2>
<p>Which Seating's own pages do not set cookies. Cloudflare Web Analytics does not use cookies. Google Analytics 4 may set cookies only after you accept. When ads are shown, Google and other vendors may set advertising cookies subject to the consent rules above. You can decline analytics, change that choice from Cookie settings, or block cookies in your browser. The guides work without them.</p>
<h2>Hosting</h2>
<p>The site is hosted on GitHub Pages, which may log IP addresses for security and operations.</p>
<h2>Your rights</h2>
<p>You can ask us to access, correct, or delete personal information we hold about you via the <a href="/contact/">contact page</a>. Residents of some US states and other countries may have additional rights, which we will honour.</p>
<h2>Children</h2>
<p>The site is for a general audience and is not directed to children under 13. We do not knowingly collect personal information from children.</p>
<h2>Changes</h2>
<p>We will post any changes here with a new date.</p>''' % (config.VERIFIED_TODAY, config.ADSENSE_PUB),
               mod=config.TODAY, published=config.PUBLISHED)
    legal_wrap("/disclaimer/", "Disclaimer | Which Seating", "Disclaimer",
               "Disclaimer for Which Seating (whichseating.com).",
               '''<p>Last updated %s.</p>
<h2>Not affiliated with any team or venue</h2>
<p>Which Seating is an independent site. It is not affiliated with, endorsed by, or sponsored by any team, league, venue, or ticket seller. All names and trademarks belong to their owners and are used only to identify the buildings.</p>
<h2>Charts change</h2>
<p>Seating charts, roofs, and accessible inventory can change. Our pages reflect the sources on the date shown. The venue's current chart and the ticket always take priority. We do not sell tickets.</p>
<h2>No professional advice</h2>
<p>Seat notes are general information to help you plan. They are not accessibility, medical, or legal advice. Descriptions of views are our reading method, labeled as such, plus the facts we cite.</p>
<h2>Accuracy and corrections</h2>
<p>We cite our sources and leave out what we cannot verify, but errors can happen. Please <a href="/contact/">report errors</a> and we will correct verified mistakes.</p>
<h2>Limitation of liability</h2>
<p>To the extent permitted by law, Joshua Israel Ventures LLC is not liable for any loss arising from reliance on this site. See our <a href="/terms/">terms of use</a>.</p>''' % config.VERIFIED)
    legal_wrap("/ad-disclosure/", "Advertising Disclosure | Which Seating", "Advertising disclosure",
               "Advertising disclosure for Which Seating and Google AdSense readiness.",
               '''<p>Last updated %s. Which Seating is free to use and contains no affiliate links today. The site is configured for Google AdSense (publisher %s): every page carries the AdSense account meta tag and the AdSense script, and <a href="/ads.txt">ads.txt</a> authorizes google.com for that publisher id. No ad units are placed on pages yet, so display ads should not appear until units are added after approval.</p>
<p>When ads appear they will be separate from our guides and labeled. Advertisers will have no influence over which seats we describe. If we add affiliate links later, we may earn a commission at no extra cost to you, and we will label those links.</p>
<h2>Editorial independence</h2>
<p>No team, league, venue, or ticket seller pays for coverage or for a change to a page. Questions: use our <a href="/contact/">contact page</a>.</p>''' % (config.VERIFIED_TODAY, config.ADSENSE_PUB),
               mod=config.TODAY, published=config.PUBLISHED)
    legal_wrap("/copyright/", "Copyright and DMCA Policy | Which Seating", "Copyright and DMCA policy",
               "Copyright and DMCA policy for Which Seating (whichseating.com).",
               '''<p>Last updated %s. Original text, design, diagrams, and data compilations on Which Seating are owned by Joshua Israel Ventures LLC. Facts are cited to their sources. The site uses no team logos and no venue photos. See our <a href="/image-policy/">image policy</a>.</p>
<h2>Reporting infringement</h2>
<p>If you believe material on this site infringes your copyright, email <a href="mailto:%s">%s</a> with: (1) your name and contact details; (2) a description of the copyrighted work; (3) the URL of the material on our site; (4) a statement that you have a good faith belief the use is not authorised by the owner, its agent, or the law; (5) a statement, under penalty of perjury, that the information is accurate and you are the owner or authorised to act for the owner; and (6) your physical or electronic signature. We will review notices promptly and remove or disable material where appropriate.</p>
<h2>Counter notice</h2>
<p>If material you provided was removed and you believe this was a mistake, you may send a counter notice to the same address with the details required by 17 U.S.C. section 512(g).</p>
<h2>Repeat infringers</h2>
<p>We will act against repeat infringement where appropriate.</p>''' % (config.VERIFIED, config.CONTACT_EMAIL, config.CONTACT_EMAIL))
    legal_wrap("/contact/", "Contact Which Seating", "Contact",
               "Contact Which Seating with corrections or venue requests.",
               '''<p>Questions, corrections after a renovation, or a venue you want us to cover next? Email <a href="mailto:%s">%s</a>.</p>
<h2>Corrections</h2>
<p>Include the page address, what looks wrong, and a link to the venue page or list that shows it. We update the verified date when we re-check the source.</p>
<p class="note">We read mail sent to that address. See our <a href="/privacy/">privacy policy</a>.</p>''' % (config.CONTACT_EMAIL, config.CONTACT_EMAIL))
    write("404.html", page("404.html", "Page not found | Which Seating", "Page not found.",
                           '<h1>Page not found</h1><p>That page is missing. Try the <a href="/venues/">venue guides</a> or <a href="/guides/how-to-choose-a-seat/">how to choose a seat</a>.</p>',
                           index=False))

def finish():
    # drop 404 if it was appended (it is not, index=False)
    locs = []
    for path, mod in PAGES:
        loc = url(path)
        locs.append((loc, mod))
    locs = sorted(set(locs))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, mod in locs:
        sm.append("<url><loc>%s</loc><lastmod>%s</lastmod></url>" % (loc, mod))
    sm.append("</urlset>\n")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(sm))
    bots = ["*", "Googlebot", "Bingbot", "Mediapartners-Google", "OAI-SearchBot", "ChatGPT-User", "GPTBot",
            "PerplexityBot", "Perplexity-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
            "Google-Extended", "Applebot", "Applebot-Extended", "DuckAssistBot", "Amazonbot", "CCBot", "Bytespider"]
    robots = []
    for b in bots:
        robots.append("User-agent: %s\nAllow: /\n" % b)
    robots.append("Sitemap: %ssitemap.xml\n" % BASE)
    open(os.path.join(ROOT, "robots.txt"), "w").write("\n".join(robots))
    lines = ["# Which Seating", "",
             "> Which Seating (whichseating.com) tells readers which seats to pick at major US stadiums and arenas, and which to skip. Facts come from public lists and official pages. Section numbers appear only when a source prints them. Checked %s." % config.VERIFIED,
             "", "Independent. Not affiliated with any team, league, or venue.", "", "## Guides"]
    for title, path in [("How to choose a seat", "/guides/how-to-choose-a-seat/"),
                        ("Shade and sun", "/guides/shade-and-sun/"),
                        ("Sections to skip", "/guides/sections-to-skip/"),
                        ("Accessible seating", "/guides/accessible-seating/"),
                        ("What club seats include", "/guides/club-seats/"),
                        ("Which NFL stadiums have a roof", "/guides/nfl-stadiums-with-a-roof/"),
                        ("Which MLB ballparks have a retractable roof", "/guides/mlb-ballparks-with-a-retractable-roof/"),
                        ("Sources and methods", "/methodology/"),
                        ("Editorial policy", "/editorial-policy/")]:
        lines.append("- [%s](%s)" % (title, url(path)))
    lines += ["", "## Venues"]
    for v in sorted(VENUES, key=lambda v: v["name"]):
        lines.append("- [%s](%s) (%s): %s" % (v["name"], url("/venues/%s/" % v["slug"]), team_list(v), cap_list(v)))
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    ads = """# whichseating.com ads.txt
google.com, %s, DIRECT, f08c47fec0942fa0
""" % config.ADSENSE_PUB_TXT
    open(os.path.join(ROOT, "ads.txt"), "w").write(ads)
    open(os.path.join(ROOT, "CNAME"), "w").write("whichseating.com\n")
    open(os.path.join(ROOT, config.INDEXNOW_KEY + ".txt"), "w").write(config.INDEXNOW_KEY)
    print(len(VENUES), "venues;", len(PAGES), "indexable URLs;", "LAUNCH" if LAUNCH else "NOINDEX")

def main():
    for v in VENUES:
        venue_page(v)
    venues_index()
    build_hubs()
    guides()
    static_pages()
    home()
    finish()

if __name__ == "__main__":
    main()
