# Sourced copy for the 20 Nov 2026 Which Seating run.
# Facts below were read off the linked club and MLB.com pages on 20 Nov 2026.
# This module does not invent section lists, prices, or rankings.

import config

V = config.VERIFIED_20
D = config.RUN_20
FIELD = "/assets/images/stadium-pitch-floodlights.png"

YANKEES_SUITES = "https://www.mlb.com/yankees/tickets/premium/suites"
REDSOX_NET = "https://www.mlb.com/redsox/ballpark/netting"
REDSOX_AZ = "https://www.mlb.com/redsox/ballpark/information/guide"
FENWAY_GUIDE = "https://www.mlb.com/news/featured/fenway-park-guide-capacity-seating-chart-parking-and-more"
CUBS_RENUM = "https://www.mlb.com/cubs/ballpark/renumbering"
CUBS_GATES = "https://www.mlb.com/cubs/ballpark/information/gates"
TROP_GUIDE = "https://www.mlb.com/news/featured/tropicana-field-guide-capacity-seating-chart-parking-and-more"
USA_TROP = "https://www.usatoday.com/story/sports/mlb/rays/2019/01/04/rays-tropicana-field-close-upper-deck-reduce-capacity/2481217002/"
BREWERS_OV = "https://www.mlb.com/brewers/tickets/2025-07-30"
YANKEES_2016 = "https://www.mlb.com/news/yankee-stadium-to-receive-design-enhancements-c207026018"
YANKEES_SOCCER = "https://www.mlb.com/yankees/tickets/events/soccer/group-one"
DODGERS_2022 = "https://www.mlb.com/dodgers/tickets/postseason-ticket-opportunity"


def a(href, label):
    return '<a href="%s" rel="nofollow noopener" target="_blank">%s</a>' % (href, label)


def _clean(name, text):
    if "\u2013" in text or "\u2014" in text or "%" in text:
        raise SystemExit("bad character in " + name)


def venues(next_reads, compare_box):
    out = {
        "fenway-park": _fenway(next_reads, compare_box),
        "wrigley-field": _wrigley(next_reads, compare_box),
    }
    for slug, block in out.items():
        for key in ("html", "end", "quick", "leftout", "desc"):
            _clean(slug + " " + key, block[key])
        for q, ans in block["pairs"]:
            _clean(slug + " faq", q + ans)
    return out


def _fenway(nr, cb):
    mid = nr([
        ("/guides/best-view-of-the-field/", "See the whole field", "Home plate, the lines, and the upper deck, in the clubs' own words.", FIELD),
        ("/guides/shade-and-sun/", "Shade and sun", "Fenway is listed as open air, with a roof over the infield grandstand."),
        ("/guides/sections-to-skip/", "Sections to skip", "Netting at Fenway is a safety screen, not an obstructed label."),
        ("/venues/wrigley-field/", "Wrigley Field", "How the Cubs renumbered the upper level in 2019."),
    ], heading="Related guides")
    end = nr([
        ("/guides/how-to-choose-a-seat/", "How to choose a seat", "Chart, roof, and the words on the ticket."),
        ("/guides/club-seats/", "What club seats include", "Lounge access only where the venue prints it."),
        ("/leagues/mlb/", "MLB venues", "Every ballpark page on this site."),
        ("/guides/mlb-ballparks-with-a-retractable-roof/", "MLB roofs", "Which parks can close a roof, and which cannot."),
    ], heading="More to read")
    compare = cb(
        "Check another park",
        'Same question, different building. <a href="/venues/wrigley-field/">Wrigley</a> publishes a section key. <a href="/venues/yankee-stadium/">Yankee Stadium</a> publishes view words by club level.',
        [("/venues/wrigley-field/", "Wrigley Field"),
         ("/venues/yankee-stadium/", "Yankee Stadium"),
         ("/guides/best-view-of-the-field/", "Where to sit to see the whole field"),
         ("/guides/sections-to-skip/", "Sections to skip")],
    )
    html = '''<h2>What the Red Sox pages actually say</h2>
<p>The generic chart method above is still only a method. On %s the Red Sox and MLB.com print a handful of Fenway specific facts. Checked %s. None of them is a ranked list of every section.</p>
<p>Protective netting is the fact that changes the lower bowl. The <a href="%s">Red Sox netting page</a> says the screen runs from Field Box Section 79 to Field Box Section 9, with varying height, about 12 feet 8 inches above the field. The page tells fans in those seats to stay alert for bats and batted balls. It does not call the seats obstructed, limited, or partial view. Treat the net as a safety screen in front of a close seat. If the ticket adds an obstructed label, that is a separate fact. See <a href="/guides/sections-to-skip/">sections to skip</a>.</p>
<p>Ian Browne's <a href="%s">MLB.com Fenway guide</a>, dated 18 March 2026, is the sightline writeup the league site is willing to print. It says the park has great sightlines and puts fans on top of the action. Then it splits the bowl into products:</p>
<ul>
<li>Monster Seats, installed above the 37 foot left field wall in 2003. Before that, the guide says, home runs landed in a net or went out to Lansdowne Street.</li>
<li>Box seats in the lower bowl from foul line to foul line: a close view, which the guide ties to Fenway's small foul territory.</li>
<li>Wooden grandstand seats in the infield: a strong sightline, with a roof overhead that keeps rain off that band.</li>
<li>The Sam Deck on the roof in right field: a bar, picnic tables, and a lot of people standing.</li>
<li>Bleachers: a looser crowd, and seats near the bullpen with a view of pitchers warming up.</li>
</ul>
<p>That is five different ways to watch, written by MLB.com, not a Which Seating ranking. The grandstand roof matters for <a href="/guides/shade-and-sun/">shade and sun</a> because the stadium list still classes Fenway as open air. Open air does not mean every seat is uncovered.</p>
<h2>Distances and wall heights</h2>
<p>The <a href="%s">Red Sox A to Z guide</a> prints the dimensions in feet: 310 down the left field line, 379 in left center, 390 in center, 420 in deep center, 380 in deep right, and 302 down the right field line. The left field wall, the Green Monster, is 37 feet. The center field wall is 17 feet. The bullpen fences are 5 feet. The right field fence is 3 to 5 feet. The 390 feet to center matches the center field figure already in the table below, which came from the Wikipedia stadium list on 16 Nov 2026. The wall heights are why the Monster Seats feel like their own deck: you are looking over a 37 foot wall, not over a ordinary outfield fence.</p>
%s
<h2>Fourth level, and the one club sold only by the season</h2>
<p>The same A to Z guide describes two premium bands without calling either one the best seat in the park.</p>
<p>The Aura Pavilion Level is the entire 4th and 5th level, including Pavilion seating, Pavilion Box, and the Pavilion suites marked B and K. Pavilion and Aura Club tickets include in seat food and drink, padded seats, and what the page calls unparalleled views of the field and the Boston skyline. Pavilion seating sits along the 4th level on the first and third base lines and can use the Aura Club dining room. Aura Club seating is directly behind home plate on the 4th level, reached through that dining room. Pavilion Box tickets and the B and K suites do not get the dining room. So "4th level" on a Fenway ticket is not one product. Behind the plate and down the lines share a lounge. The box and the named suites do not.</p>
<p>The Dell Technologies Club overlooks the field and the city. Inside, the page says, it is climate controlled, with a restaurant and full service bars. Outside are padded seats with a TV in each section, and the page's own line is that they are some of the best views in baseball. The club is sold as season tickets only. That is a Red Sox claim about the view, and a hard limit on how you buy it. It is not a score we assigned.</p>
<p>Use these names when you read a ticket: Field Box and the net, lower box from line to line, infield grandstand under the roof, Monster Seats, Sam Deck, bleachers, Aura Club behind the plate, Aura Pavilion along the baselines, Dell season seats. If the ticket uses a name this page does not, open the Red Sox page again. Layouts move. <a href="/guides/how-to-choose-a-seat/">How to choose a seat</a> is the order of operations. <a href="/guides/best-view-of-the-field/">Where to sit to see the whole field</a> compares this language with Yankee Stadium and Wrigley.</p>
%s''' % (V, V, REDSOX_NET, FENWAY_GUIDE, REDSOX_AZ, mid, compare)
    # The first %s in the template above is V twice then URLs. Wait, I used %s for V, V, urls, mid, compare.
    # Count: "On %s the Red Sox" is V. Then "Checked %s." is V.
    # Then netting href %s, fenway guide href %s, A to Z href %s, mid, compare.
    # That's 2 + 3 + 2 = 7. The tuple has (V, V, REDSOX_NET, FENWAY_GUIDE, REDSOX_AZ, mid, compare). Good.
    _clean("fenway html", html)
    quick = (
        "<ul>"
        "<li><strong>Close view.</strong> MLB.com's 18 March 2026 Fenway guide calls the lower box seats from line to line a close view, and the infield grandstand a strong sightline under a roof.</li>"
        "<li><strong>Netting.</strong> The Red Sox netting page puts the screen from Field Box Section 79 to Field Box Section 9, about 12 feet 8 inches over the field. It does not call those seats obstructed.</li>"
        "<li><strong>Up high in left.</strong> Monster Seats sit above the 37 foot wall, installed in 2003. Aura Club seats are behind home plate on the 4th level. The Dell club is season tickets only.</li>"
        "<li><strong>Still open air.</strong> The stadium list says Open. The grandstand roof covers one band. It is not a dome.</li>"
        "</ul>"
    )
    pairs = [
        ("What are the best seats at Fenway Park?",
         "The Red Sox do not publish one winning section. MLB.com's Fenway guide dated 18 March 2026 calls the lower box seats from line to line a close view and the wooden infield grandstand a strong sightline under a roof. Monster Seats sit above the left field wall. Aura Club seats are directly behind home plate on the 4th level."),
        ("Does the Fenway net block the view?",
         "The Red Sox netting page says the screen runs from Field Box Section 79 to Field Box Section 9, about 12 feet 8 inches above the field, and tells fans there to watch for bats and balls. It does not use the words obstructed view."),
        ("Which Fenway seats are under a roof?",
         "The MLB.com guide says the wooden grandstand seats in the infield have a roof overhead that keeps rain off. The Dell Technologies Club is climate controlled inside, with padded seats outside. The park is still listed as open air."),
        ("What is the difference between the Aura Club and the Pavilion?",
         "Aura Club seats are directly behind home plate on the 4th level and open into the dining room. Pavilion seats run along the 4th level baselines and can use that dining room. Pavilion Box tickets and the B and K suites cannot."),
        ("Who plays at Fenway Park?",
         "Home team on the source list: Boston Red Sox. League: MLB."),
    ]
    sources = [
        {"title": "Fenway Park Netting", "url": REDSOX_NET, "publisher": "Boston Red Sox", "role": "official"},
        {"title": "Fenway Park A to Z guide", "url": REDSOX_AZ, "publisher": "Boston Red Sox", "role": "official"},
        {"title": "Fenway Park guide", "url": FENWAY_GUIDE, "publisher": "MLB.com", "role": "official"},
    ]
    leftout = '''<h2>What we left out</h2>
<div class="leftout"><ul>
<li>A ranking of every section. The pages name products and two Field Box numbers for the net. They do not score the rest.</li>
<li>A shade map by section. The grandstand roof is one sentence in the MLB.com guide, not a sun chart.</li>
<li>A numbered obstructed view list. The netting page does not use that label.</li>
<li>Accessible section numbers. Use the venue accessibility office.</li>
<li>Prices and fees. They change by event.</li>
</ul></div>'''
    desc = "Fenway seats from Red Sox pages: the netting span, Monster Seats, the grandstand roof, and the 4th level clubs."
    return {
        "html": html, "end": end, "quick": quick, "pairs": pairs, "sources": sources,
        "leftout": leftout, "desc": desc, "verified": V, "mod": D,
    }


def _wrigley(nr, cb):
    mid = nr([
        ("/guides/best-view-of-the-field/", "See the whole field", "Why the Cubs compared their old 400 level to 200 level seats elsewhere.", FIELD),
        ("/guides/how-to-choose-a-seat/", "How to choose a seat", "Read the section suffix before you pick a ramp."),
        ("/venues/fenway-park/", "Fenway Park", "Netting, the Monster, and a roof over the infield grandstand."),
        ("/guides/sections-to-skip/", "Sections to skip", "Wrigley's renumbering page does not list obstructed sections."),
    ], heading="Related guides")
    end = nr([
        ("/guides/shade-and-sun/", "Shade and sun", "Wrigley is open air. The roof question is a different page."),
        ("/guides/club-seats/", "What club seats include", "A club name on the ticket is an amenity list, not a view."),
        ("/leagues/mlb/", "MLB venues", "Every ballpark page on this site."),
        ("/venues/yankee-stadium/", "Yankee Stadium", "Field, main, and terrace, in the Yankees' own view words."),
    ], heading="More to read")
    compare = cb(
        "Check another park",
        "Wrigley tells you how the numbers changed. Fenway tells you where the net and the roof are. Yankee Stadium names the view by level.",
        [("/venues/fenway-park/", "Fenway Park"),
         ("/venues/yankee-stadium/", "Yankee Stadium"),
         ("/guides/best-view-of-the-field/", "Where to sit to see the whole field"),
         ("/guides/how-to-choose-a-seat/", "How to choose a seat")],
    )
    html = '''<h2>Read the section before you trust an old photo</h2>
<p>Wrigley tickets changed labels in 2019. The seats did not move. The <a href="%s">Cubs renumbering FAQ</a>, still up when we checked it on %s, is the page that explains the difference.</p>
<p>The old system dated to the early 1980s and used aisle, row, and seat. The Cubs say it left neighboring seats with numbers that did not run in order, and it left upper level seats looking cheaper than the view. Opening Day 2019 switched the park to section, row, and seat. Season ticket holders kept the same physical seat. Only the label changed. An old photo or forum post that cites an aisle number is describing the same chair under a retired name.</p>
<p>The FAQ's own view sentence is specific, and it is theirs, not ours: the old 400 seats are "some of the best in baseball" and "comparable to 200-level seats in other ballparks." To match that, the club renumbered. The FAQ lists three moves. The 400s are now the 300s. The 500s are now the 400s. The Budweiser Bleachers are now the 500s. The bleachers stay general admission in the regular season and become assigned seats in the postseason. That is the whole map the page is willing to print. It does not say which row inside the 300s is the good one.</p>
<p>Upper level sections carry a letter so you can find a ramp. L means left field. R means right field. The examples on the page are Section 303L and Section 431R. The same letters show up on wayfinding signs on the main concourse. Suites kept their old numbers and gained an S in front, for suite level.</p>
<p>The <a href="%s">gate page</a> still translates the old letter gates. Marquee Gate was Gate F, at Addison and Clark. Left Field Gate was Gate K, on the Waveland side. The Budweiser Bleacher Gate is at Sheffield and Waveland. If your section ends in L, you are aiming at the left field side of the park, not at a mystery ramp. The letter is a direction, not a quality grade.</p>
%s
<h2>What the renumbering does not decide</h2>
<p>The FAQ says the upper level was undervalued, and that the old 400s compare with 200 level seats elsewhere. It does not publish a shaded section, an obstructed row, or a price. Bleacher seats in the 500s are a different product from the 300s: general admission on a normal day, assigned if the Cubs are in the postseason, according to that FAQ. Confirm the current chart if you are buying a playoff ticket, because a FAQ can lag a later change. We read it on %s and it still said that.</p>
<p>For the wider question of home plate versus a high seat, use <a href="/guides/best-view-of-the-field/">where to sit to see the whole field</a>. For a limited view word on the ticket, use <a href="/guides/sections-to-skip/">sections to skip</a>. This page will not copy a fan site pole list into the gap.</p>
%s''' % (CUBS_RENUM, V, CUBS_GATES, mid, V, compare)
    _clean("wrigley html", html)
    quick = (
        "<ul>"
        "<li><strong>Labels moved in 2019. Seats did not.</strong> The Cubs switched from aisle, row, and seat to section, row, and seat. Season seats stayed put.</li>"
        "<li><strong>Upper level.</strong> The club says the old 400s, now the 300s, compare with 200 level seats at other parks. The old 500s are now the 400s.</li>"
        "<li><strong>Bleachers.</strong> Now the 500s. General admission in the regular season, assigned in the postseason, on the FAQ we checked.</li>"
        "<li><strong>L and R.</strong> Left field and right field, so you can find the ramp. The page's examples are Section 303L and Section 431R.</li>"
        "</ul>"
    )
    pairs = [
        ("How do I read a Wrigley section number?",
         "Since Opening Day 2019 the Cubs use section, row, and seat. The old aisle numbers described the same chairs. Upper level sections end in L for left field or R for right field. The club's examples are Section 303L and Section 431R."),
        ("Are Wrigley's upper seats a bad view?",
         "The Cubs' renumbering FAQ says the old 400 level is some of the best seats in baseball and comparable to 200 level seats at other parks. That level is now the 300s. The old 500s are now the 400s."),
        ("Are the Wrigley bleachers general admission?",
         "The same FAQ says the Budweiser Bleachers are now the 500s, stay general admission in the regular season, and switch to assigned seats in the postseason."),
        ("Which Wrigley sections are obstructed?",
         "The renumbering FAQ and the gate page do not publish a numbered obstructed list. Skip a seat when the ticket says limited view, obstructed view, or partial view."),
        ("Who plays at Wrigley Field?",
         "Home team on the source list: Chicago Cubs. League: MLB."),
    ]
    sources = [
        {"title": "Wrigley Field seat renumbering", "url": CUBS_RENUM, "publisher": "Chicago Cubs", "role": "official"},
        {"title": "Wrigley Field seating and gate map", "url": CUBS_GATES, "publisher": "Chicago Cubs", "role": "official"},
    ]
    leftout = '''<h2>What we left out</h2>
<div class="leftout"><ul>
<li>A row by row ranking inside the 300s. The Cubs compare the whole old 400 level with 200 level seats elsewhere. They do not pick a row.</li>
<li>A shade map by section.</li>
<li>A numbered obstructed view list. It is not on the pages we checked.</li>
<li>Accessible section numbers.</li>
<li>Prices and fees. They change by event.</li>
</ul></div>'''
    desc = "How to read a Wrigley ticket after the 2019 renumbering, from the Cubs' own seating FAQ."
    return {
        "html": html, "end": end, "quick": quick, "pairs": pairs, "sources": sources,
        "leftout": leftout, "desc": desc, "verified": V, "mod": D,
    }


def choose(hero, nr, cb, vlink):
    hero_html = hero("Empty stadium seating bowl at dusk with lights on along the aisles")
    mid = nr([
        ("/guides/best-view-of-the-field/", "See the whole field", "Intimate, expansive, and sweeping are three different Yankees sentences.", FIELD),
        ("/guides/shade-and-sun/", "Shade and sun", "Start with the roof class before you worry about a sunny section."),
        ("/guides/sections-to-skip/", "Sections to skip", "The words limited, obstructed, and partial are the list."),
        ("/venues/fenway-park/", "Fenway Park", "A worked example: net, grandstand roof, Monster, 4th level."),
    ])
    end = nr([
        ("/venues/wrigley-field/", "Wrigley Field", "L and R on the section are left field and right field."),
        ("/guides/club-seats/", "What club seats include", "A lounge does not repair a bad angle."),
        ("/guides/accessible-seating/", "Accessible seating", "Wheelchair and companion inventory is sold separately."),
        ("/leagues/", "Leagues", "NFL, MLB, NBA, NHL, and college football hubs."),
    ], heading="More to read")
    compare = cb(
        "Check another way in",
        "Pick the question you actually have. View, sun, a bad label, or a club amenity.",
        [("/guides/best-view-of-the-field/", "Where to sit to see the whole field"),
         ("/guides/shade-and-sun/", "Shade and sun"),
         ("/guides/sections-to-skip/", "Sections to skip"),
         ("/guides/club-seats/", "What club seats include"),
         ("/venues/", "All venues")],
    )
    body = '''%s
<p class="answer">Open the venue page, then the official page it links, then the ticket. Use a low seat near the middle of the playing surface when the club has not described the view in its own words. When it has, use those words. Skip any seat marked limited view. Ignore a section number that Which Seating did not copy from a source.</p>
<h2>Do this in order</h2>
<ol>
<li>Open the venue. Start from a league if you are not sure of the building: <a href="/leagues/nfl/">NFL</a>, <a href="/leagues/mlb/">MLB</a>, <a href="/leagues/nba/">NBA</a>, <a href="/leagues/nhl/">NHL</a>, or <a href="/leagues/college-football/">college football</a>.</li>
<li>Read the roof line before you ask about sun. A dome, a fixed roof, or an indoor arena takes weather off the table. A retractable roof depends on that event. <a href="/guides/shade-and-sun/">Shade and sun</a> is the longer version, including the Fenway case where an open park still has a roof over the infield grandstand.</li>
<li>Look for the club's own view language. On %s the <a href="%s">Yankees premium seating page</a> uses three different adjectives: intimate for the Legends Suite between sections 014A and 027A, expansive for the Delta SKY360 Suite on the Main Level, and sweeping for the Jim Beam Club on the Terrace Level. Those are not synonyms. <a href="/guides/best-view-of-the-field/">Where to sit to see the whole field</a> lines them up.</li>
<li>Use the official section map for numbers. Our bowl drawing is generic. At <a href="/venues/wrigley-field/">Wrigley</a> the Cubs' own FAQ is the key: since 2019, L on an upper section means left field and R means right field.</li>
<li>On the ticket, reject limited view, obstructed view, and partial view unless you mean to sit there. A safety net is not the same label. Fenway's net runs from Field Box Section 79 to Field Box Section 9 and the Red Sox page does not call it obstructed. <a href="/guides/sections-to-skip/">Sections to skip</a>.</li>
<li>For a step free seat or a companion seat, use the venue accessibility office. <a href="/guides/accessible-seating/">Accessible seating</a>.</li>
<li>If the ticket names a club, read the amenity list before you treat the club as a better view. <a href="/guides/club-seats/">What club seats include</a>.</li>
</ol>
%s
<h2>One worked baseball pass</h2>
<p>Say you are choosing among three parks and you care about seeing the field, not about a lounge.</p>
<ul>
<li>%s. The Yankees put the most intimate view of the diamond on the Legends Suite, between sections 014A and 027A, and a sweeping view on the Terrace. The Champions Suite, just past first and third, is described with food and a lounge, not with a view adjective. Read the product name.</li>
<li>%s. MLB.com's 18 March 2026 guide calls the lower boxes a close view and the infield grandstand a strong sightline under a roof. Monster Seats are above the 37 foot wall. The net in front of Field Box 79 through Field Box 9 is published as protection.</li>
<li>%s. The Cubs say their old 400 level, now the 300s, compares with 200 level seats at other parks. The letter after the section number points you to a ramp. It does not grade the seat.</li>
</ul>
<p>Other buildings in this guide still have only the chart method, because their pages did not print a view sentence we could quote on %s. Examples already on the site: %s is open air, %s has a retractable roof, %s is a dome, and %s is an indoor arena used by two teams.</p>
%s
%s''' % (
        hero_html, V, YANKEES_SUITES,
        mid,
        vlink("Yankee Stadium"), vlink("Fenway Park"), vlink("Wrigley Field"),
        V,
        vlink("Lambeau Field"), vlink("AT&T Stadium"), vlink("Caesars Superdome"), vlink("Madison Square Garden"),
        compare, end,
    )
    _clean("choose", body)
    pairs = [
        ("What is the safest way to pick a section?",
         "Use the venue's own chart and the words on the ticket. If the club has described the view, use that sentence. Which Seating will not give you a section number the venue did not publish in our sources."),
        ("Is the lowest seat always the best view of the field?",
         "It is the fallback when the club is silent. The Yankees call a Field Level suite intimate and a Terrace club sweeping. The Cubs compare an upper level with 200 level seats elsewhere. Read the page for that park."),
        ("Do you rank sections by price?",
         "No. Prices change by opponent and by day. We do not publish a value ranking."),
    ]
    sources = [
        {"title": "Yankees premium seating", "url": YANKEES_SUITES, "publisher": "New York Yankees", "role": "official"},
        {"title": "Fenway Park Netting", "url": REDSOX_NET, "publisher": "Boston Red Sox", "role": "official"},
        {"title": "Fenway Park guide", "url": FENWAY_GUIDE, "publisher": "MLB.com", "role": "official"},
        {"title": "Wrigley Field seat renumbering", "url": CUBS_RENUM, "publisher": "Chicago Cubs", "role": "official"},
        {"title": "List of current NFL stadiums", "url": "https://en.wikipedia.org/wiki/List_of_current_NFL_stadiums", "publisher": "Wikipedia", "role": "list"},
        {"title": "List of current Major League Baseball stadiums", "url": "https://en.wikipedia.org/wiki/List_of_current_Major_League_Baseball_stadiums", "publisher": "Wikipedia", "role": "list"},
    ]
    desc = "How to pick a stadium seat: the club's own view words, the roof, and the label printed on the ticket."
    return body, pairs, sources, desc


def shade_tail(nr, cb):
    mid = nr([
        ("/venues/fenway-park/", "Fenway Park", "Open air on the list, with a roof over the infield grandstand."),
        ("/guides/mlb-ballparks-with-a-retractable-roof/", "MLB roofs", "Retractable, fixed, or open, park by park."),
        ("/guides/nfl-stadiums-with-a-roof/", "NFL roofs", "Dome, retractable, skylight, or open air."),
        ("/guides/best-view-of-the-field/", "See the whole field", "A roof over your head is not the same as a blocked view.", FIELD),
    ])
    end = nr([
        ("/guides/how-to-choose-a-seat/", "How to choose a seat", "Roof first, then the chart, then the ticket."),
        ("/guides/sections-to-skip/", "Sections to skip", "The Tropicana upper deck is still the closed one to check."),
        ("/venues/tropicana-field/", "Tropicana Field", "Fixed roof, and the upper deck note."),
        ("/leagues/mlb/", "MLB venues", "Every ballpark page on this site."),
    ], heading="More to read")
    compare = cb(
        "Check a roof, then a park",
        "The class on the list is the first cut. A few parks then publish one extra sentence.",
        [("/guides/nfl-stadiums-with-a-roof/", "Which NFL stadiums have a roof"),
         ("/guides/mlb-ballparks-with-a-retractable-roof/", "Which MLB ballparks have a retractable roof"),
         ("/venues/fenway-park/", "Fenway Park"),
         ("/venues/tropicana-field/", "Tropicana Field")],
    )
    html = '''<h2>When "open" still has a roof over some seats</h2>
<p>Checked %s. The stadium list is still the roof class. Two ballpark guides add a sentence the list does not.</p>
<p>Fenway Park stays Open on the list. Ian Browne's <a href="%s">MLB.com Fenway guide</a> of 18 March 2026 says the wooden grandstand seats in the infield have a roof overhead that keeps rain off the people in that band. That is cover for one slice of an open park. It is not a shade chart, and it does not say which baseline gets the afternoon sun. The lower boxes and the bleachers are outside that sentence. Details and the Red Sox dimension list are on the <a href="/venues/fenway-park/">Fenway page</a>.</p>
<p><a href="/venues/tropicana-field/">Tropicana Field</a> is the fixed roof on the MLB list, the one that does not open. Adam Berry's <a href="%s">MLB.com Tropicana guide</a> of 9 April 2026 still treats it as a dome and lists capacity as 25,025, with the upper deck closed since 2019. The same guide says the Rays played the 2025 season at George M. Steinbrenner Field in Tampa and came back to Tropicana Field for 2026 after the repairs. Sun is still not a seating factor under that fixed roof. The upper deck is still the section group to avoid assuming is on sale. Our venue table still shows 25,000 from the Wikipedia list retrieved 16 Nov 2026. The newer guide figure is 25,025. We are not papering over the difference.</p>
<p>Neither page names a sunny section number. If a club has not printed one, this site will not invent one. <a href="/guides/how-to-choose-a-seat/">How to choose a seat</a> puts the roof step before the view step.</p>
%s
%s
%s''' % (V, FENWAY_GUIDE, TROP_GUIDE, mid, compare, end)
    _clean("shade", html)
    pairs = [
        ("Does open air mean every seat is in the sun?",
         "No. Fenway Park is Open on the stadium list. MLB.com's Fenway guide dated 18 March 2026 says the wooden infield grandstand has a roof overhead that keeps rain off those seats. That is one covered band, not a shade map of the park."),
        ("Is Tropicana Field still a fixed roof with the upper deck closed?",
         "The MLB.com Tropicana guide dated 9 April 2026 still describes the dome and says the upper deck has been closed since 2019. It lists capacity as 25,025. The Rays played 2025 at George M. Steinbrenner Field and returned to Tropicana Field for 2026."),
    ]
    sources = [
        {"title": "Fenway Park guide", "url": FENWAY_GUIDE, "publisher": "MLB.com", "role": "official"},
        {"title": "Tropicana Field guide", "url": TROP_GUIDE, "publisher": "MLB.com", "role": "official"},
    ]
    return html, pairs, sources


def skip(hero, nr, cb, vlink):
    hero_html = hero("Empty stadium seating bowl at dusk with lights on along the aisles")
    mid = nr([
        ("/venues/tropicana-field/", "Tropicana Field", "Upper deck closed since 2019, and the Rays are back in the dome for 2026."),
        ("/venues/fenway-park/", "Fenway Park", "The net from Field Box 79 to Field Box 9 is not an obstructed label."),
        ("/guides/how-to-choose-a-seat/", "How to choose a seat", "The label check sits after the roof and the chart."),
        ("/guides/best-view-of-the-field/", "See the whole field", "A clear view and a safe view are different questions.", FIELD),
    ])
    end = nr([
        ("/venues/yankee-stadium/", "Yankee Stadium", "A 2016 note about bleacher seats, and a warning for non baseball events."),
        ("/guides/shade-and-sun/", "Shade and sun", "Sun is not why you skip a seat."),
        ("/guides/accessible-seating/", "Accessible seating", "A bad label is not an accessible seat problem."),
        ("/leagues/mlb/", "MLB venues", "Every ballpark page on this site."),
    ], heading="More to read")
    compare = cb(
        "Check the park, not a blacklist",
        "These are the pages where a club has printed something you can verify. A missing name means we found no list, not a clean bill of health.",
        [("/venues/tropicana-field/", "Tropicana Field"),
         ("/venues/fenway-park/", "Fenway Park"),
         ("/venues/yankee-stadium/", "Yankee Stadium"),
         ("/venues/wrigley-field/", "Wrigley Field"),
         ("/guides/how-to-choose-a-seat/", "How to choose a seat")],
    )
    body = '''%s
<p class="answer">Skip a seat when the chart or the ticket says limited view, obstructed view, or partial view. Clubs rarely print a second list of bad section numbers. The words on that ticket are the list. A safety net, a closed deck, and a non baseball event are three other things a club sometimes prints, and they are not the same label.</p>
<h2>Read the adjective the club used</h2>
<p>Checked %s. Three club pages show the vocabulary, and none of them hands you a permanent section blacklist.</p>
<ul>
<li>The <a href="%s">Brewers' ticket page</a> for the 30 July 2025 game against the Cubs, still posted on the club site, says a limited number of tickets remained, "including Standing Room &amp; Obstructed View seats." Obstructed View is a named bucket next to standing room. The page does not give section numbers. If you are buying a Brewers seat and the listing uses those words, you already have the warning. You do not need a blog to translate it.</li>
<li>The <a href="%s">Dodgers' page</a> for their 2022 World Series ticket drawing says the seats offered could have a partial, restricted, or obstructed view, and could be anywhere in the park. That page is about 2022, not about a 2026 section map. It is useful because it shows the three adjectives the club was willing to put in one sentence. If a current Dodgers listing uses one of them, believe the listing.</li>
<li>The <a href="%s">Yankees' presale page</a> for a Liverpool and Sporting CP soccer match at Yankee Stadium says the sightlines for that event may be obstructed from baseball seating locations. A section that faces the diamond can face a soccer setup badly. Check the event, not only the section number you liked for baseball.</li>
</ul>
%s
<h2>A closed deck is not an obstructed seat</h2>
<p>At %s the question is whether the upper deck is on sale at all. The Wikipedia MLB list we used on 16 Nov 2026 gives a capacity of 25,000 and cites a <a href="%s">2019 USA Today report</a> that the Rays closed the upper deck. Adam Berry's <a href="%s">MLB.com Tropicana guide</a> of 9 April 2026 lists capacity as 25,025 and says the upper deck has been closed since 2019. The Rays spent 2025 at George M. Steinbrenner Field and returned to the dome for 2026. Do not buy an upper deck seat on the theory that the return reopened it. The 2026 guide still says closed. The venue table on our Tropicana page still shows the older 25,000 figure from Wikipedia. Both numbers are cited. Neither one puts the upper deck back on the map.</p>
<h2>Netting is a third category</h2>
<p>The <a href="%s">Red Sox netting page</a> puts protective netting from Field Box Section 79 to Field Box Section 9, about 12 feet 8 inches above the field, and says fans there should still watch for bats and balls. It never says obstructed. A seat behind that net can be a close view of the field with a screen in front of it. Skip it only if you do not want the screen, or if the ticket adds a limited view line of its own. The <a href="/venues/fenway-park/">Fenway page</a> has the rest of the sightline notes.</p>
<h2>Old removal plans go stale</h2>
<p>On 24 October 2016, MLB.com's Bryan Hoch reported a Yankees announcement that obstructed view seats in the bleachers would be removed, about 1,100 of them, as part of a larger cut of just under 2,100 seats that also included about 600 Terrace Level seats. That article is <a href="%s">here</a>. It is a 2016 plan for the 2017 season. The <a href="%s">premium seating page</a> we opened on %s describes Legends, Champions, Delta SKY360, Ford Field MVP, and Jim Beam. It does not reprint a current bleacher obstructed list, and it does not confirm the 2016 removal in those words. Use the 2016 piece as history. Use the ticket in your hand for the game you are attending.</p>
<p>Fan sites still publish long pole lists. We do not copy them. If a venue page prints a numbered obstructed list, send it through <a href="/contact/">contact</a> and we will add it with the citation. Until then the ticket adjective, the closed deck, the netting note, and the event warning are the sourced checks.</p>
%s
%s''' % (
        hero_html, V, BREWERS_OV, DODGERS_2022, YANKEES_SOCCER,
        mid, vlink("Tropicana Field"), USA_TROP, TROP_GUIDE, REDSOX_NET,
        YANKEES_2016, YANKEES_SUITES, V, compare, end,
    )
    _clean("skip", body)
    pairs = [
        ("Which section numbers should I avoid?",
         "The ones the venue or the ticket marks limited, obstructed, partial, or restricted. This guide does not keep a second blacklist. The Brewers page for 30 July 2025 names Obstructed View as inventory and does not list sections."),
        ("Is the Tropicana Field upper deck open in 2026?",
         "No, according to the MLB.com Tropicana guide dated 9 April 2026, which says the upper deck has been closed since 2019 and lists capacity as 25,025. The Rays played 2025 at George M. Steinbrenner Field and returned to Tropicana Field for 2026."),
        ("Does Fenway netting mean the seat is obstructed?",
         "The Red Sox netting page does not use that word. The screen runs from Field Box Section 79 to Field Box Section 9. An obstructed label on the ticket would be an additional fact."),
        ("Can a good baseball seat be a bad seat at another event?",
         "Yes. The Yankees' page for a soccer match at Yankee Stadium says sightlines from baseball seating locations may be obstructed for that event."),
    ]
    sources = [
        {"title": "Brewers ticket page, 30 July 2025", "url": BREWERS_OV, "publisher": "Milwaukee Brewers", "role": "official"},
        {"title": "Dodgers 2022 World Series ticket opportunity", "url": DODGERS_2022, "publisher": "Los Angeles Dodgers", "role": "official"},
        {"title": "Yankees soccer presale terms", "url": YANKEES_SOCCER, "publisher": "New York Yankees", "role": "official"},
        {"title": "Tropicana Field guide", "url": TROP_GUIDE, "publisher": "MLB.com", "role": "official"},
        {"title": "Tampa Bay Rays reduce seating capacity at Tropicana Field", "url": USA_TROP, "publisher": "USA Today", "role": "extra"},
        {"title": "Fenway Park Netting", "url": REDSOX_NET, "publisher": "Boston Red Sox", "role": "official"},
        {"title": "Yankee Stadium design enhancements, 24 Oct 2016", "url": YANKEES_2016, "publisher": "MLB.com", "role": "official"},
        {"title": "Yankees premium seating", "url": YANKEES_SUITES, "publisher": "New York Yankees", "role": "official"},
    ]
    desc = "How to spot a seat to skip: ticket labels, a closed upper deck, and netting that is not the same thing."
    return body, pairs, sources, desc


def best_view(hero, nr, cb, vlink):
    hero_html = hero("Empty stadium bowl at dusk, floodlights on, seen from field level down the pitch", FIELD)
    mid = nr([
        ("/venues/yankee-stadium/", "Yankee Stadium", "Intimate on the field, expansive on the main level, sweeping on the terrace."),
        ("/venues/fenway-park/", "Fenway Park", "Lower boxes, a grandstand roof, and seats atop the Monster."),
        ("/venues/wrigley-field/", "Wrigley Field", "The Cubs' case that an upper level can match a 200 level view."),
        ("/guides/sections-to-skip/", "Sections to skip", "A whole field view can still sit behind a net or a bad label."),
    ])
    end = nr([
        ("/guides/how-to-choose-a-seat/", "How to choose a seat", "The order: roof, club language, chart, ticket."),
        ("/guides/shade-and-sun/", "Shade and sun", "Seeing the field and sitting in the sun are separate."),
        ("/guides/mlb-ballparks-with-a-retractable-roof/", "MLB roofs", "A closed roof takes weather out of the seat decision."),
        ("/leagues/mlb/", "MLB venues", "Every ballpark page on this site."),
    ], heading="More to read")
    compare = cb(
        "Check another park's own words",
        "Three clubs described the view. The rest of the ballparks on this site have not, in a sentence we could quote on this check.",
        [("/venues/yankee-stadium/", "Yankee Stadium"),
         ("/venues/fenway-park/", "Fenway Park"),
         ("/venues/wrigley-field/", "Wrigley Field"),
         ("/guides/shade-and-sun/", "Shade and sun"),
         ("/guides/club-seats/", "What club seats include")],
    )
    body = '''%s
<p class="answer">No league page ranks the best seat for seeing the whole field. Three clubs describe the view in their own words, and the words do not match. At Yankee Stadium, Field Level is "intimate" or "prime," the Main Level is "expansive," and the Terrace is "sweeping." At Fenway, a close lower box and a high seat over the left field wall are both published as good looks at the game. At Wrigley, the Cubs say an upper level compares with 200 level seats at other parks. Pick the sentence that matches what you want to see. Checked %s.</p>
<p>The photo above is a generic empty bowl under floodlights. It is not a seating chart, and it is not Fenway, Wrigley, or Yankee Stadium. <a href="/image-policy/">Image policy</a>.</p>
<h2>What the Yankees call intimate, expansive, and sweeping</h2>
<p>The <a href="%s">Yankees premium seating page</a> is the cleanest primary comparison we found, because one page uses a different view word for each level. This is a reading of that page, not a ranking.</p>
<div class="tablewrap"><table class="stats">
<thead><tr><th scope="col">Product</th><th scope="col">Where the Yankees place it</th><th scope="col">View language on the page</th></tr></thead>
<tbody>
<tr><th scope="row">Legends Suite</th><td>Between sections 014A and 027A</td><td>Most intimate views of the diamond, "right in the action"</td></tr>
<tr><th scope="row">Champions Suite</th><td>Just beyond first and third base</td><td>No view adjective. The sentence is about food, nonalcoholic drinks, and a lounge</td></tr>
<tr><th scope="row">Ford Field MVP Club</th><td>Field Level</td><td>Prime views of the diamond, "the center of the action"</td></tr>
<tr><th scope="row">Delta SKY360 Suite</th><td>Main Level, with an outdoor patio</td><td>Expansive views of the playing field</td></tr>
<tr><th scope="row">Jim Beam Club</th><td>Terrace Level, with an outdoor terrace</td><td>Sweeping views of the playing field</td></tr>
</tbody></table></div>
<p>Intimate and prime sit low, between or near the bases. Expansive is one deck up, still behind the idea of a wide look at the field. Sweeping is the Terrace. The Champions Suite is the caution: it is past the bases, and the page sells the lounge rather than the sightline. A baseline club seat is not automatically a whole field seat. The page has to say so.</p>
<p>A separate, older sentence is worth keeping dated. On 24 October 2016 the Yankees described the MasterCard Batter's Eye Deck, on the 200 level in center field, as a clear, sweeping view of the entire stadium. Bryan Hoch reported it for <a href="%s">MLB.com</a>. The premium page we opened on %s does not repeat that deck. Treat the center field line as a 2016 description of an outfield deck looking back across the stadium, and confirm the name on a current map before you count on it.</p>
%s
<h2>Fenway: close to the field, or up on the wall</h2>
<p>The <a href="%s">MLB.com Fenway guide</a> of 18 March 2026 says the park puts fans on top of the action, then names two looks that are both about seeing the game and are not the same seat. Box seats in the lower bowl from line to line are a close view, which the guide credits to the park's small foul territory. Wooden grandstand seats in the infield are a strong sightline with a roof overhead. Monster Seats, added in 2003, sit above the 37 foot left field wall. You see the field from over the wall, which is a high outfield angle, not a seat behind the pitcher.</p>
<p>The <a href="%s">Red Sox A to Z guide</a> puts Aura Club seating directly behind home plate on the 4th level, and Aura Pavilion seating along the 4th level baselines. Both are given the same phrase, unparalleled views of the field and the skyline. The club is not claiming the baseline seats see less baseball than the seats behind the plate. It is claiming both see the field and the city. The Dell Technologies Club, season tickets only, gets the page's "best views in baseball" line for the padded seats outside a climate controlled room. That is marketing copy on an official page. We quote it. We do not extend it to a numbered section the page never prints.</p>
<p>One limit sits in front of the close seats. The <a href="%s">netting page</a> runs the screen from Field Box Section 79 to Field Box Section 9, about 12 feet 8 inches over the field. You can be in the lower bowl, seeing the whole infield, and still be looking through a net. The page does not call that an obstructed view. More on the building is on the <a href="/venues/fenway-park/">Fenway page</a>.</p>
<h2>Wrigley: the upper deck the club defends</h2>
<p>The usual advice is to sit low. The <a href="%s">Cubs renumbering FAQ</a> argues the other way about one specific band. The old 400 seats, the club writes, are some of the best in baseball and comparable to 200 level seats at other parks. Those 400s are now the 300s. The old 500s are now the 400s. The Budweiser Bleachers are now the 500s and stay general admission in the regular season. Upper sections end in L or R, left field or right field, so you can find the ramp. The page's examples are Section 303L and Section 431R.</p>
<p>So "upper deck" at Wrigley is not one view. The 300s are the band the club compares with a good 200 level seat elsewhere. The 500s are bleachers. An old photo that says "400 level" may be today's 300s. The <a href="/venues/wrigley-field/">Wrigley page</a> walks through the label change. The FAQ does not say the 300s show more of the field than a field box. It says they were mislabeled, and that the view is better than the old number suggested.</p>
%s
<h2>How to choose without a fake winner</h2>
<p>Ask which of these you want, then match a sentence above.</p>
<ol>
<li><strong>The pitcher and the infield, close.</strong> Yankees: Legends, between sections 014A and 027A, or the Ford Field MVP Club on the Field Level. Fenway: the lower boxes from line to line, knowing the net covers Field Box 79 through Field Box 9.</li>
<li><strong>A wider look from higher up.</strong> Yankees: Delta SKY360 on the Main Level is the expansive one, Jim Beam on the Terrace is the sweeping one. Wrigley: the 300s, formerly the 400s, are the upper band the Cubs defend. Fenway: Aura Club behind the plate on the 4th level, or the Monster Seats if you want left field from above the wall.</li>
<li><strong>Down the line.</strong> The Yankees locate the Champions Suite just past first and third and then talk about the lounge. Do not promote that into a whole field claim. Fenway's Pavilion seats are along the 4th level baselines and share the Aura dining room with the seats behind the plate. The view phrase is the same. The angle is not.</li>
</ol>
<p>Sun and rain are a different cut. A roof over the Fenway grandstand keeps rain off and does not, by itself, hide the field. Start with <a href="/guides/shade-and-sun/">shade and sun</a> if weather is the real question, and with <a href="/guides/club-seats/">club seats</a> if the question is the lounge. <a href="/guides/how-to-choose-a-seat/">How to choose a seat</a> is the full order. Parks with no sentence like these stay on the chart method only.</p>
%s''' % (
        hero_html, V, YANKEES_SUITES, YANKEES_2016, V, mid,
        FENWAY_GUIDE, REDSOX_AZ, REDSOX_NET, CUBS_RENUM,
        compare, end,
    )
    _clean("best", body)
    pairs = [
        ("Is behind home plate the best view of the whole field?",
         "The Yankees call the Legends Suite, between sections 014A and 027A, the most intimate view of the diamond, and they call the Terrace a sweeping view. Intimate is close. Sweeping is wide. The page does not crown one of them."),
        ("Do upper deck seats see more of the field?",
         "The Cubs say their old 400 level, now the 300s, compares with 200 level seats at other parks. That is one club defending one band. Fenway's Monster Seats are a different kind of up: they sit above the left field wall."),
        ("Does netting mean you cannot see the field?",
         "Not on the Red Sox page. The screen from Field Box Section 79 to Field Box Section 9 is a safety note. The page does not call those seats obstructed."),
        ("Which ballpark has the best whole field seats?",
         "We do not rank parks. Yankee Stadium, Fenway, and Wrigley each publish different view language, quoted on this page. A park that has not published a sentence is not scored."),
    ]
    sources = [
        {"title": "Yankees premium seating", "url": YANKEES_SUITES, "publisher": "New York Yankees", "role": "official"},
        {"title": "Yankee Stadium design enhancements, 24 Oct 2016", "url": YANKEES_2016, "publisher": "MLB.com", "role": "official"},
        {"title": "Fenway Park guide", "url": FENWAY_GUIDE, "publisher": "MLB.com", "role": "official"},
        {"title": "Fenway Park A to Z guide", "url": REDSOX_AZ, "publisher": "Boston Red Sox", "role": "official"},
        {"title": "Fenway Park Netting", "url": REDSOX_NET, "publisher": "Boston Red Sox", "role": "official"},
        {"title": "Wrigley Field seat renumbering", "url": CUBS_RENUM, "publisher": "Chicago Cubs", "role": "official"},
    ]
    desc = "Home plate, the baselines, or the upper deck: what Yankees, Red Sox, and Cubs pages say about the view."
    _clean("best desc", desc)
    return body, pairs, sources, desc
