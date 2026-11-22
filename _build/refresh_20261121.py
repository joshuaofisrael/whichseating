# Sourced copy for the 21 Nov 2026 Which Seating run.
# Facts were read off the linked venue and school pages on 21 Nov 2026.
# This module does not invent section lists, prices, or rankings.

import os
import config

V = config.VERIFIED_21
D = config.RUN_21
HERO = "/assets/images/empty-stadium-dusk.png"
ALT = "Empty stadium seating bowl at dusk with lights on along the aisles"

UC_CHARTS = "https://www.unitedcenter.com/venue/seating-charts/"
UC_BOOK = "https://www.unitedcenter.com/assets/1/7/clubseatinghandbook.pdf"
BARC_AZ = "https://www.barclayscenter.com/plan-your-visit/a-z-guide"
BARC_CHARTS = "https://www.barclayscenter.com/seating-charts"
PRU_AZ = "https://www.prucenter.com/a-z-guide"
PRU_SEAT = "https://www.prucenter.com/seating"
TM_INFO = "https://www.t-mobilearena.com/arena-information"
TM_AZ = "https://www.t-mobilearena.com/arena-info/a-z-guide"
MICH_MAP = "https://mgoblue.com/sports/2026/4/14/michigan-stadium-2026-football-preferred-seat-contribution-map"
MICH_STU = "https://mgoblue.com/sports/2017/6/16/tickets-students-football"
FBS = "https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_FBS_football_stadiums"
CRYPTO_AZ = "https://www.cryptoarena.com/a-z-guide"
CRYPTO_VITAL = "https://www.cryptoarena.com/arena-info/vital-stats"
NBA_LIST = "https://en.wikipedia.org/wiki/List_of_NBA_arenas"
NHL_LIST = "https://en.wikipedia.org/wiki/List_of_National_Hockey_League_arenas"


def a(href, label):
    return '<a href="%s" rel="nofollow noopener" target="_blank">%s</a>' % (href, label)


def _clean(name, text):
    if "\u2013" in text or "\u2014" in text or "%" in text:
        raise SystemExit("bad character in " + name)


def _photo(hero_photo, note):
    return hero_photo(ALT) + '<p class="note">%s</p>' % note


def _src(items):
    bits = ['<section class="sources" aria-labelledby="src-h"><h2 id="src-h">Sources checked for this update</h2><ul>']
    for title, url, pub in items:
        bits.append('<li><a href="%s" rel="nofollow noopener" target="_blank">%s</a> (%s)</li>' % (url, title, pub))
    bits.append("</ul>")
    bits.append('<p class="note">Retrieved %s. Which Seating is not affiliated with any team, league, or venue.</p></section>' % V)
    return "".join(bits)


def venues(next_reads, compare_box, hero_photo):
    out = {
        "united-center": _united(next_reads, compare_box, hero_photo),
        "barclays-center": _barclays(next_reads, compare_box, hero_photo),
        "prudential-center": _prudential(next_reads, compare_box, hero_photo),
        "t-mobile-arena": _tmobile(next_reads, compare_box, hero_photo),
    }
    for slug, block in out.items():
        for key in ("html", "end", "quick", "leftout", "desc", "title", "photo"):
            _clean(slug + " " + key, block[key])
        if len(block["title"]) >= 60:
            raise SystemExit("title %d %s" % (len(block["title"]), slug))
        if len(block["desc"]) > 155:
            raise SystemExit("desc %d %s" % (len(block["desc"]), slug))
        for q, ans in block["pairs"]:
            _clean(slug + " faq", q + ans)
    return out


def _pack(html, end, quick, pairs, sources, leftout, desc, title, photo):
    return {
        "html": html, "end": end, "quick": quick, "pairs": pairs, "sources": sources,
        "leftout": leftout, "desc": desc, "title": title, "photo": photo,
        "image": HERO, "verified": V, "mod": D,
    }


def _united(nr, cb, hero):
    mid = nr([
        ("/guides/how-to-choose-a-seat/", "How to choose a seat", "Read the chart name before you read the section."),
        ("/guides/sections-to-skip/", "Sections to skip", "An obstructed label is a ticket fact, not a guess."),
        ("/guides/club-seats/", "What club seats include", "The 200 level here is the club, with a lounge attached."),
        ("/leagues/nba/", "NBA venues", "How other arenas separate a game chart from a concert chart."),
    ], heading="Related guides")
    end = nr([
        ("/venues/barclays-center/", "Barclays Center", "A general admission floor there is standing room, with no seat."),
        ("/venues/prudential-center/", "Prudential Center", "The arena publishes an end stage map and a center stage map."),
        ("/venues/t-mobile-arena/", "T-Mobile Arena", "End stage and center stage are printed as different capacities."),
        ("/guides/shade-and-sun/", "Shade and sun", "This building is indoor. Sun is not the seating question."),
    ], heading="Check another arena")
    compare = cb(
        "Check another arena's own charts",
        'Same question, different paperwork. <a href="/venues/barclays-center/">Barclays</a> says a GA floor ticket is not a seat. <a href="/venues/prudential-center/">Prudential</a> names an end stage map and a center stage map. <a href="/venues/t-mobile-arena/">T-Mobile Arena</a> prints a capacity range for each.',
        [("/venues/barclays-center/", "Barclays Center"),
         ("/venues/prudential-center/", "Prudential Center"),
         ("/venues/t-mobile-arena/", "T-Mobile Arena"),
         ("/leagues/nhl/", "NHL venues")],
    )
    html = f'''<h2>Five charts, and two of them are concerts</h2>
<p>The generic bowl above is only a method. On {V} the <a href="{UC_CHARTS}">United Center seating charts page</a> names five separate layouts, and it says they reflect the general layout and may vary by event. The accurate chart, the page says, is the one on that event's page.</p>
<div class="tablewrap"><table class="stats">
<thead><tr><th scope="col">Name on the arena page</th><th scope="col">What the title tells you</th></tr></thead>
<tbody>
<tr><th scope="row">Chicago Blackhawks seating chart</th><td>A hockey layout</td></tr>
<tr><th scope="row">Chicago Bulls seating chart</th><td>A basketball layout</td></tr>
<tr><th scope="row">Concert with floor seating</th><td>A concert layout that still has seats on the floor</td></tr>
<tr><th scope="row">Concert with general admission floor</th><td>A concert layout whose floor is general admission</td></tr>
<tr><th scope="row">Premium seating chart</th><td>The premium layout, separate from both concert files</td></tr>
</tbody></table></div>
<p>The page does not print section numbers in the text. The pictures are the charts. A Bulls ticket and a concert ticket are not the same file, and the two concert files are not the same as each other. "Floor" on one show can be a reserved seat. On the other it is general admission. Open the chart that matches the event name before you decide the 100 level is "close."</p>
{mid}
<h2>What the club handbook still says about a blocked view</h2>
<p>Club seats are the 200 level. The <a href="{UC_BOOK}">club seating handbook</a> still hosted on the arena's site calls them Club Seat (200 level) tickets, and it says guests with 100 or 300 level tickets are on the other bowls. It also says the handbook's concert maps of the 200 level cover several stage shapes. Then it gets specific, and old.</p>
<p>The same PDF cites the City of Chicago Clean Indoor Act of 2005 when it talks about smoking. Treat the section ranges below as the handbook's general assumption for club seats, not as a promise about tonight. The seating charts page, opened the same day, does not repeat these numbers in text.</p>
<ul>
<li>For a 180 degree stage, the handbook says club sections 220 to 232 are assumed to have an obstructed view.</li>
<li>For a 270 degree stage, it says club sections 221 to 231 are assumed to have an obstructed view.</li>
<li>Obstructed seats, it says, are determined by the performer, event by event. Members in those seats are moved to the next available 200 or 300 level location.</li>
<li>For a smaller theatre setup, which the handbook describes as generally 3,000 to 10,000 guests, it says there will be club seats with obstructed views beyond the ones normally restricted, and that draping, lighting, and sound decide which ones.</li>
</ul>
<p>That is a club rule. It is not a map of sections 101 to 122, and it does not say the 300 level is a bad view of a Bulls game. A game chart and a concert chart answer different questions. <a href="/guides/sections-to-skip/">Sections to skip</a> is where an obstructed label on a ticket fits. <a href="/guides/club-seats/">What club seats include</a> is the amenity question, which this handbook answers with a lounge, in seat service, and a 200 level ticket.</p>
{compare}
<h2>Basketball, hockey, and the roof</h2>
<p>The building is indoor on the arena list, so sun is not how you pick a seat. The lowest bowl is the 100 level, the club is the 200, and the upper bowl is the 300. For a Bulls game, the closest straight on view of the whole floor is still the lowest seats near midcourt, and the lowest seats behind a basket look at one hoop. That method is ours. The arena's own contribution is the separate chart files, plus the club handbook's concert assumptions. Home teams on the list: Chicago Bulls and Chicago Blackhawks. More of the indoor arenas are on the <a href="/leagues/nba/">NBA hub</a> and the <a href="/leagues/nhl/">NHL hub</a>.</p>'''
    quick = (
        "<ul>"
        "<li><strong>Two concert files.</strong> The arena publishes \"Concert with floor seating\" and \"Concert with general admission floor\" as different charts. A Bulls chart and a Blackhawks chart are different again.</li>"
        "<li><strong>Club is the 200 level.</strong> The club handbook still on the site assumes sections 220 to 232 are obstructed for a 180 degree stage, and sections 221 to 231 for a 270 degree stage. The PDF cites a 2005 smoking ordinance, so treat the ranges as the handbook's assumption.</li>"
        "<li><strong>Charts vary.</strong> The seating page says the event page is the accurate chart. The text of that page does not list section numbers.</li>"
        "<li><strong>Indoor.</strong> Sun is not the seating factor. The list classifies the roof as indoor.</li>"
        "</ul>"
    )
    pairs = [
        ("What are the best seats at the United Center?",
         "The arena does not rank them. It publishes five charts: Blackhawks, Bulls, a concert with floor seating, a concert with a general admission floor, and a premium chart. The event page is the accurate one, and the charts may vary."),
        ("Does a United Center concert put seats on the floor?",
         "Sometimes. The arena's seating page has one chart called Concert with floor seating and another called Concert with general admission floor. Read the title of the chart on your event."),
        ("Which United Center club seats are obstructed at a concert?",
         "The club handbook still posted by the arena assumes club sections 220 to 232 are obstructed for a 180 degree stage and sections 221 to 231 for a 270 degree stage. The handbook cites a 2005 city ordinance, and the current charts page does not repeat those numbers in text. The performer decides obstructed seats event by event."),
        ("Does sun matter at the United Center?",
         "No. The source list classifies the building as indoor."),
        ("Who plays at the United Center?",
         "Home teams on the source list: Chicago Bulls and Chicago Blackhawks. Leagues: NBA and NHL."),
    ]
    sources = [
        {"title": "Seating Charts", "url": UC_CHARTS, "publisher": "United Center", "role": "official"},
        {"title": "Club seating handbook", "url": UC_BOOK, "publisher": "United Center", "role": "official"},
    ]
    leftout = '''<h2>What we left out</h2>
<div class="leftout"><ul>
<li>A ranking of the 100 level against the 300 level for a concert. The charts are images. The text does not score them.</li>
<li>Section numbers for a Bulls or Blackhawks game. They are not in the text we opened.</li>
<li>A claim that the handbook's 220 to 232 range is tonight's map. The PDF is older than the charts page, and the charts page says layouts vary.</li>
<li>Prices, fees, and parking.</li>
</ul></div>'''
    desc = "United Center publishes two concert charts, reserved floor and general admission floor, plus a club handbook that flags some 200 level seats."
    title = "United Center: Floor Chart or GA Floor"
    photo = _photo(hero, "This photo is a generic bowl at dusk. It is not the United Center, and it is not one of the five charts named below.")
    return _pack(html, end, quick, pairs, sources, leftout, desc, title, photo)


def _barclays(nr, cb, hero):
    mid = nr([
        ("/venues/united-center/", "United Center", "Two concert chart names: reserved floor, or a general admission floor."),
        ("/guides/how-to-choose-a-seat/", "How to choose a seat", "A standing floor and a reserved bowl are different products."),
        ("/guides/club-seats/", "What club seats include", "This arena says some clubs may open for concerts, and does not name them."),
        ("/guides/accessible-seating/", "Accessible seating", "Guest services for a wheelchair escort sits on the main concourse and the upper pavilion."),
    ], heading="Related guides")
    end = nr([
        ("/venues/prudential-center/", "Prudential Center", "End stage and center stage are separate maps on the arena site."),
        ("/venues/t-mobile-arena/", "T-Mobile Arena", "A GA floor there is also standing room, with a wristband."),
        ("/leagues/nba/", "NBA venues", "Every NBA arena page on this site."),
        ("/guides/sections-to-skip/", "Sections to skip", "A limited view note on the ticket still governs."),
    ], heading="Check another building")
    compare = cb(
        "Check another floor",
        'Barclays tells you the GA floor has no seats. United Center splits that idea into two chart files. Prudential names the stage shape instead.',
        [("/venues/united-center/", "United Center"),
         ("/venues/prudential-center/", "Prudential Center"),
         ("/venues/t-mobile-arena/", "T-Mobile Arena"),
         ("/guides/how-to-choose-a-seat/", "How to choose a seat")],
    )
    html = f'''<h2>A GA floor ticket is not a seat</h2>
<p>On {V} the <a href="{BARC_AZ}">Barclays Center A to Z guide</a> says the general admission area on the floor is standing room only and there are no seats. Guests with a GA floor ticket enter at the Atlantic Entrance, get a wristband after they are inside, and are sent to aisles that reach the floor. The guide asks people who want to arrive early to line up no earlier than 9:00 AM, and it says doors open at the same time for everyone. That is a standing product. It is not "row 1 of the floor." If your ticket is a numbered seat, you are not in that paragraph.</p>
<p>The same guide lists five levels: event level, main concourse at street level, Barclays suite level A, suite level B, and the upper pavilion. Suite level guests are pointed at the VIP entrances. Not every concert uses every club. Under club access for concerts, the guide says certain clubs may be open during concerts or as part of a concert package, and it tells you to ask guest services. It does not name the clubs. A club name on a ticket is an amenity question for <a href="/guides/club-seats/">what club seats include</a>, and this page will not invent the lounge.</p>
{mid}
<h2>The rows that get a drink brought to the seat</h2>
<p>In seat beverage service is printed as a location list, not as a view ranking. The A to Z guide puts it in sections 7, 8 and 9, rows 1 to 10, and in sections 23, 24 and 25, rows 1 to 10. You order from a QR code on the armrest, and alcohol still needs a photo ID at delivery. Those six sections are where the arena runs that service. The guide does not say they are the best view of a stage, a court, or a concert screen.</p>
<p>Seat width is a separate printed fact. Seats vary, the guide says, from about 17 inches to about 22 inches. That is the hardware range. It is not a map of which sections are the wide ones.</p>
{compare}
<h2>The concert chart is its own file</h2>
<p>The <a href="{BARC_CHARTS}">seating charts page</a> says charts may vary by event, and that the accurate chart is the one on the event page. The files it offers by name are Concerts and Entertainment, Brooklyn Nets, and New York Liberty. A Nets ticket and a concert ticket are different downloads. The text around those links does not number the sections behind a stage. If the ticket says limited view or obstructed view, that label is the fact. See <a href="/guides/sections-to-skip/">sections to skip</a>.</p>
<p>The building is indoor on the arena list, so shade is not the way to choose. Home team on the list: Brooklyn Nets. Guest services centers, for a question the chart does not answer, are on the main concourse across from section 12 and section 112, and on the upper pavilion behind section 212. The <a href="/leagues/nba/">NBA hub</a> collects the other indoor arenas.</p>'''
    quick = (
        "<ul>"
        "<li><strong>GA floor.</strong> The A to Z guide says it is standing room only, with no seats, a wristband, and entry at the Atlantic Entrance.</li>"
        "<li><strong>Five levels.</strong> Event level, main concourse, two suite levels, and the upper pavilion.</li>"
        "<li><strong>In seat drinks.</strong> Sections 7, 8 and 9, and sections 23, 24 and 25, rows 1 to 10. That is a service zone, not a view ranking.</li>"
        "<li><strong>Concert chart.</strong> The seating page publishes a Concerts and Entertainment file, separate from the Nets and Liberty files, and says charts vary by event.</li>"
        "</ul>"
    )
    pairs = [
        ("What are the best seats at Barclays Center?",
         "The arena does not rank them. It separates a Concerts and Entertainment chart from the Nets and Liberty charts, and it says the event page is the accurate one because charts vary."),
        ("Is the Barclays Center floor a seat?",
         "Not when the ticket says GA floor. The A to Z guide says that area is standing room only, with no seats. You enter at the Atlantic Entrance and get a wristband."),
        ("Which Barclays sections have in seat service?",
         "The A to Z guide lists sections 7, 8 and 9, rows 1 to 10, and sections 23, 24 and 25, rows 1 to 10. It describes drink delivery, not a better view."),
        ("Do Barclays clubs open for concerts?",
         "The guide says certain clubs may be open during concerts or as part of a concert package. It does not name which clubs. Ask guest services for that show."),
        ("Who plays at Barclays Center?",
         "Home team on the source list: Brooklyn Nets. League: NBA. The seating page also publishes a New York Liberty chart."),
    ]
    sources = [
        {"title": "A to Z guide", "url": BARC_AZ, "publisher": "Barclays Center", "role": "official"},
        {"title": "Seating charts", "url": BARC_CHARTS, "publisher": "Barclays Center", "role": "official"},
    ]
    leftout = '''<h2>What we left out</h2>
<div class="leftout"><ul>
<li>A ranked list of lower bowl sections for a concert. The charts page does not print one in text.</li>
<li>Which clubs open on a given concert night. The guide says some may, and stops there.</li>
<li>A shade map. The building is indoor on the source list.</li>
<li>Prices and fees.</li>
</ul></div>'''
    desc = "Barclays Center says a GA floor ticket is standing room with no seat, and it publishes a separate concerts chart."
    title = "Barclays: The GA Floor Has No Seats"
    photo = _photo(hero, "This photo is a generic bowl at dusk. It is not Barclays Center, and it is not the concerts chart.")
    return _pack(html, end, quick, pairs, sources, leftout, desc, title, photo)


def _prudential(nr, cb, hero):
    mid = nr([
        ("/venues/t-mobile-arena/", "T-Mobile Arena", "The arena prints a capacity range for end stage and another for center stage."),
        ("/venues/united-center/", "United Center", "Reserved floor and general admission floor are different chart files."),
        ("/guides/how-to-choose-a-seat/", "How to choose a seat", "Pick the map that matches the event, then read the ticket."),
        ("/guides/sections-to-skip/", "Sections to skip", "A warm up aisle is not a concert seat."),
    ], heading="Related guides")
    end = nr([
        ("/venues/barclays-center/", "Barclays Center", "Five levels, and a GA floor with no seats."),
        ("/leagues/nhl/", "NHL venues", "Every hockey arena page on this site."),
        ("/guides/shade-and-sun/", "Shade and sun", "Indoor means the roof is not the seating question."),
        ("/guides/club-seats/", "What club seats include", "The Lofts, Studio Suites, and M Lounge are named products, not a view score."),
    ], heading="More to read")
    compare = cb(
        "Check another stage shape",
        "Prudential publishes the two concert maps by name. T-Mobile Arena publishes the two capacities. United Center publishes the two floor types.",
        [("/venues/t-mobile-arena/", "T-Mobile Arena"),
         ("/venues/united-center/", "United Center"),
         ("/venues/barclays-center/", "Barclays Center"),
         ("/leagues/nhl/", "NHL venues")],
    )
    html = f'''<h2>The arena names the stage shape on the map</h2>
<p>On {V} the <a href="{PRU_SEAT}">Prudential Center seating page</a> does not offer one arena map. It offers separate maps, and two of the names are the concert question: End Stage Seating and Center Stage Seating. The same page also lists Devils Seating, Basketball Seating, Luxury Suites, The Lofts, Studio Suites, and M Lounge by BMW. An end stage concert and a center stage concert are different files. A Devils game is a third file. The page says you can look up a Devils seat view. It does not say the Devils view tool works for a concert.</p>
<p>The <a href="{PRU_AZ}">A to Z guide</a> says the same thing in one sentence under seating information: for concerts and events with floor seating, the seating chart varies. It adds a small reading rule that does travel from event to event. If you sit in a section and face the floor, seat number 1 is on your right. The number of seats in a row, and the number of rows, varies by event. Most main concourse sections have rows of 20 to 24 seats. Upper concourse sections have 9 to 14 rows. Those are typical counts, and the guide says the event can break them.</p>
<div class="tablewrap"><table class="stats">
<thead><tr><th scope="col">Map name on the seating page</th><th scope="col">Use it for</th></tr></thead>
<tbody>
<tr><th scope="row">End Stage Seating</th><td>A concert with the stage at one end</td></tr>
<tr><th scope="row">Center Stage Seating</th><td>A concert with the stage in the middle</td></tr>
<tr><th scope="row">Devils Seating</th><td>New Jersey Devils hockey</td></tr>
<tr><th scope="row">Basketball Seating</th><td>Basketball, including Seton Hall on the arena's own description</td></tr>
<tr><th scope="row">Luxury Suites, The Lofts, Studio Suites, M Lounge by BMW</th><td>Named premium products, each with its own map link</td></tr>
</tbody></table></div>
{mid}
<h2>The lower level rule is a Devils warm up rule</h2>
<p>The A to Z guide describes a warm up policy for Devils regular season games. Doors to the end of warm ups, about 20 minutes before puck drop, ticket holders may watch from their own seat. Someone whose ticket is not in the lower level, which the guide defines as sections 1 to 22, may stand in rows 1 to 6 of sections 2, 3, 4, 12, 13, or 14 if that seat is empty. They have to leave when warm ups end. That paragraph is about hockey warm ups. It is not a concert seating recommendation, and it is not permission to move at a show.</p>
<p>The house scoreboard is a concert fact, and it cuts the other way. The guide says the Prudential Center scoreboard is generally not used during concerts. It is used for concert announcements. Other screens are brought by the tour. Buying a seat because it faces the hockey scoreboard does not tell you where the tour's screens will sit.</p>
{compare}
<h2>Levels the guide actually names</h2>
<p>The A to Z guide never prints a neat "five levels" list. It names the bowls in passing: main concourse, suite level 1, suite level 2, and the New Jersey Lottery Upper Concourse. Family restrooms and first aid are pinned to sections on those levels, including section 9 and section 114 for guest services. Doors generally open about 60 to 90 minutes before the event, and the guide says the event page can override that. The building is indoor on our list. Home team on the list: New Jersey Devils. The <a href="/leagues/nhl/">NHL hub</a> is the parent page. <a href="/guides/how-to-choose-a-seat/">How to choose a seat</a> is the order of operations: pick the map whose name matches the ticket, then read the row.</p>'''
    quick = (
        "<ul>"
        "<li><strong>Two concert maps.</strong> The seating page publishes End Stage Seating and Center Stage Seating as separate files, plus Devils and basketball maps.</li>"
        "<li><strong>Floor charts vary.</strong> The A to Z guide says so. Seat 1 is on the right when you face the floor. Main concourse rows are often 20 to 24 seats. The upper concourse often has 9 to 14 rows.</li>"
        "<li><strong>Warm ups are hockey.</strong> Sections 1 to 22 are the lower level in a Devils warm up rule. It is not a concert instruction.</li>"
        "<li><strong>Concert screens.</strong> The house scoreboard is generally not used for the show. The tour brings other screens.</li>"
        "</ul>"
    )
    pairs = [
        ("What are the best seats at Prudential Center?",
         "The arena does not rank them. It publishes separate maps for an end stage concert, a center stage concert, Devils hockey, and basketball. The A to Z guide says concert floor charts vary by event."),
        ("How do I tell an end stage seat from a center stage seat?",
         "Open the map with that name. End Stage Seating and Center Stage Seating are different links on the arena's seating page."),
        ("How many seats are in a Prudential Center row?",
         "It varies by event. The A to Z guide says most main concourse sections have rows of 20 to 24 seats, and upper concourse sections have 9 to 14 rows."),
        ("Can I stand in the lower level during warm ups?",
         "At Devils regular season games, the guide allows empty rows 1 to 6 of sections 2, 3, 4, 12, 13, or 14 until warm ups end, if your ticket is not already in sections 1 to 22. That rule is not a concert rule."),
        ("Who plays at Prudential Center?",
         "Home team on the source list: New Jersey Devils. League: NHL. The arena also publishes a basketball map and says Seton Hall plays there."),
    ]
    sources = [
        {"title": "A to Z guide", "url": PRU_AZ, "publisher": "Prudential Center", "role": "official"},
        {"title": "Seating maps", "url": PRU_SEAT, "publisher": "Prudential Center", "role": "official"},
    ]
    leftout = '''<h2>What we left out</h2>
<div class="leftout"><ul>
<li>Which sections sit behind an end stage. The map is an image. The text names the file and does not list the sections.</li>
<li>A dollar figure for The Lofts, the suites, or M Lounge.</li>
<li>A shade map. The building is indoor on the source list.</li>
<li>The warm up aisle as a recommended concert seat. The guide limits that paragraph to Devils warm ups.</li>
</ul></div>'''
    desc = "Prudential Center publishes separate end stage and center stage maps, and says concert floor charts vary."
    title = "Prudential: End Stage or Center Stage"
    photo = _photo(hero, "This photo is a generic bowl at dusk. It is not Prudential Center, and it is not the end stage map.")
    return _pack(html, end, quick, pairs, sources, leftout, desc, title, photo)


def _tmobile(nr, cb, hero):
    mid = nr([
        ("/venues/prudential-center/", "Prudential Center", "End stage and center stage are named maps, without a capacity pair."),
        ("/venues/barclays-center/", "Barclays Center", "Another arena where the GA floor has no seats."),
        ("/guides/how-to-choose-a-seat/", "How to choose a seat", "Capacity tells you the bowl changed. The event chart tells you where."),
        ("/leagues/nhl/", "NHL venues", "The hockey number on the arena page and the number on our list do not match."),
    ], heading="Related guides")
    end = nr([
        ("/venues/united-center/", "United Center", "Reserved floor versus a general admission floor."),
        ("/guides/club-seats/", "What club seats include", "Club here means the two center sections, plus named lounges."),
        ("/guides/shade-and-sun/", "Shade and sun", "Indoor arena. Sun is not the question."),
        ("/guides/sections-to-skip/", "Sections to skip", "A smaller end stage capacity is not, by itself, a list of bad sections."),
    ], heading="More to read")
    compare = cb(
        "Check another arena's concert split",
        "T-Mobile Arena prints two concert capacities. Prudential prints two concert map names. United Center prints two floor types. None of the three prints a ranked section list in the text.",
        [("/venues/prudential-center/", "Prudential Center"),
         ("/venues/united-center/", "United Center"),
         ("/venues/barclays-center/", "Barclays Center"),
         ("/leagues/nba/", "NBA venues")],
    )
    html = f'''<h2>End stage and center stage are different capacities</h2>
<p>On {V} T-Mobile Arena's own pages print the concert split as headcount, not as a section ranking. The <a href="{TM_INFO}">arena info page</a> and the <a href="{TM_AZ}">A to Z guide</a> agree on the concert ranges and disagree on basketball. Both were opened the same day. We are printing both basketball figures because picking one would be a guess.</p>
<div class="tablewrap"><table class="stats">
<thead><tr><th scope="col">Setup</th><th scope="col">Arena info page</th><th scope="col">A to Z guide</th></tr></thead>
<tbody>
<tr><th scope="row">End stage concert</th><td>12,000 to 18,000</td><td>12,000 to 18,000</td></tr>
<tr><th scope="row">Center stage concert</th><td>19,500 to 20,000</td><td>19,500 to 20,000</td></tr>
<tr><th scope="row">Hockey</th><td>17,500</td><td>17,500</td></tr>
<tr><th scope="row">Basketball</th><td>18,000</td><td>19,000</td></tr>
<tr><th scope="row">Boxing or UFC</th><td>20,000</td><td>20,000</td></tr>
</tbody></table></div>
<p>An end stage show is the smaller number. A center stage show is the larger one. The pages do not name the sections that make up the difference. A lower capacity is not, by itself, a list of seats to skip. The event chart is. The Wikipedia hockey figure on the table further down this page is 17,367. The arena's own pages say 17,500. Both stay cited. The info page also says the building seats up to 20,000 and that it opened to the public on 6 April 2016, which matches the 2016 opening year on our list.</p>
{mid}
<h2>Seven levels, and a loge aimed at the far end of the stage</h2>
<p>The A to Z guide lists seven levels and then warns that not all of them open for every event: event level on the ground, mezzanine, main concourse, City National Bank suite level, Allegiant Flight Deck, upper concourse, and the tower level with Hyde Lounge on the 7th level.</p>
<p>The loge boxes are the closest the guide comes to a concert view sentence. It says they fit four to six guests and "will be perfectly situated in one end of the lower level at the opposite end of the stage for viewing concerts." That is the arena describing its loge product: the end of the lower bowl facing the stage, not a side seat and not the floor. The same paragraph adds drink service, a TV for every two seats, and a private lounge. It does not say every lower level seat has that view.</p>
<p>Club seat memberships are a different product. The guide says they are a limited number of in bowl seats in the two center sections, with access to Ghost Lounge and the Bud Light Lounge. "Center sections" is the arena's phrase. It does not print the section numbers, and it does not say those two sections face an end stage the way the loge does.</p>
{compare}
<h2>The floor ticket with no chair</h2>
<p>General admission on the floor is standing room only. The A to Z guide says there are no seats. After you enter you get a wristband and you are directed to aisles that reach the floor. People who want to line up early are asked to start no earlier than 4 p.m. Doors for concerts generally open 60 minutes before the event, and the guide says that can vary. Seats that do exist run about 18 to 22 inches wide.</p>
<p>The arena info page describes the building as being in Las Vegas. The NHL list we used files the city as Paradise. The page you are on keeps Paradise because that is the list's place name. The arena's own wording is Las Vegas. Home team on the list: Vegas Golden Knights. The <a href="/leagues/nhl/">NHL hub</a> is the parent. <a href="/guides/how-to-choose-a-seat/">How to choose a seat</a> still applies after you know which capacity you bought: end stage, center stage, or a floor with no seat.</p>'''
    quick = (
        "<ul>"
        "<li><strong>End stage.</strong> Both official pages print 12,000 to 18,000 for an end stage concert.</li>"
        "<li><strong>Center stage.</strong> Both print 19,500 to 20,000. They do not list which sections make up the gap.</li>"
        "<li><strong>Loge.</strong> The A to Z guide places loge boxes at one end of the lower level, opposite the stage, for concerts. Club seats are the two center sections. Neither sentence numbers the sections.</li>"
        "<li><strong>GA floor.</strong> Standing room only, no seats, wristband. Basketball capacity is 18,000 on the info page and 19,000 on the A to Z guide.</li>"
        "</ul>"
    )
    pairs = [
        ("What are the best seats at T-Mobile Arena?",
         "The arena does not rank sections. It prints 12,000 to 18,000 for an end stage concert and 19,500 to 20,000 for a center stage concert, and it says loge boxes sit at the end of the lower level opposite the stage."),
        ("How many people fit at a T-Mobile Arena concert?",
         "End stage concerts are listed at 12,000 to 18,000. Center stage concerts are listed at 19,500 to 20,000. The info page and the A to Z guide agree on those two ranges."),
        ("Is the T-Mobile Arena floor a seat?",
         "Not on a GA floor ticket. The A to Z guide says the floor is standing room only, with no seats, and that you receive a wristband inside."),
        ("Why do the basketball numbers disagree?",
         "The arena info page says 18,000 for basketball. The A to Z guide says 19,000. Hockey is 17,500 on both, while the Wikipedia list used on this site says 17,367. We print the conflict instead of choosing."),
        ("Who plays at T-Mobile Arena?",
         "Home team on the source list: Vegas Golden Knights. League: NHL."),
    ]
    sources = [
        {"title": "Arena info", "url": TM_INFO, "publisher": "T-Mobile Arena", "role": "official"},
        {"title": "A to Z guide", "url": TM_AZ, "publisher": "T-Mobile Arena", "role": "official"},
    ]
    leftout = '''<h2>What we left out</h2>
<div class="leftout"><ul>
<li>The section numbers that close when the show is an end stage. The capacity gap is printed. The section list is not.</li>
<li>A single basketball capacity. The arena's two pages disagree, so both numbers stay.</li>
<li>A shade map. The building is indoor.</li>
<li>Prices, and any claim that the loge sentence describes every lower level seat.</li>
</ul></div>'''
    desc = "T-Mobile Arena lists end stage concerts at 12,000 to 18,000 and center stage concerts at 19,500 to 20,000."
    title = "T-Mobile Arena: End Stage or Center"
    photo = _photo(hero, "This photo is a generic bowl at dusk. It is not T-Mobile Arena, and it is not a capacity chart.")
    return _pack(html, end, quick, pairs, sources, leftout, desc, title, photo)


def leagues(next_reads, compare_box, hero_photo):
    out = {
        "nba": _nba(next_reads, compare_box, hero_photo),
        "college-football": _college(next_reads, compare_box, hero_photo),
    }
    for slug, pack in out.items():
        for key in ("extra", "intro", "desc", "h1", "title"):
            _clean(slug + " " + key, pack[key])
        if len(pack["title"]) >= 60:
            raise SystemExit("title %d %s" % (len(pack["title"]), slug))
        if len(pack["desc"]) > 155:
            raise SystemExit("desc %d %s" % (len(pack["desc"]), slug))
        for q, ans in pack["pairs"]:
            _clean(slug + " faq", q + ans)
    return out


def _nba(nr, cb, hero):
    mid = nr([
        ("/venues/t-mobile-arena/", "T-Mobile Arena", "End stage and center stage, printed as two capacities."),
        ("/venues/prudential-center/", "Prudential Center", "End stage and center stage, printed as two maps."),
        ("/venues/united-center/", "United Center", "Reserved floor and a general admission floor."),
        ("/venues/barclays-center/", "Barclays Center", "A GA floor ticket is standing room, with no seat."),
    ], heading="Four arenas, four kinds of paperwork")
    end = nr([
        ("/guides/how-to-choose-a-seat/", "How to choose a seat", "Midcourt, baseline, then the words on the ticket."),
        ("/guides/club-seats/", "What club seats include", "A club name is an amenity list, not a view."),
        ("/guides/sections-to-skip/", "Sections to skip", "Limited view and obstructed view, when the ticket says so."),
        ("/leagues/nhl/", "NHL venues", "Many of these buildings are on the hockey list too."),
    ], heading="Keep reading")
    compare = cb(
        "Check a building, not the league average",
        "The league page cannot tell you the row. These four publish the concert difference in their own words.",
        [("/venues/t-mobile-arena/", "T-Mobile Arena"),
         ("/venues/prudential-center/", "Prudential Center"),
         ("/venues/united-center/", "United Center"),
         ("/venues/barclays-center/", "Barclays Center")],
    )
    photo = _photo(hero, "This photo is a generic bowl at dusk. It is not an NBA arena, and it is not a seating chart.")
    extra = f'''{photo}
<h2>A game chart and a concert chart are not the same file</h2>
<p>All 29 buildings on this list are indoor, so sun is not how you pick an NBA seat. The basketball method is still the old one: the lowest seats at midcourt are the closest straight on view of the whole floor, and the lowest seats behind a basket look at the near hoop. That is a way to read a game chart. It is a bad way to read a concert, because several of these arenas publish a different document for a show. Checked {V}.</p>
<div class="tablewrap"><table class="stats">
<thead><tr><th scope="col">Arena</th><th scope="col">What its own page separates</th></tr></thead>
<tbody>
<tr><th scope="row"><a href="/venues/t-mobile-arena/">T-Mobile Arena</a></th><td>End stage concerts 12,000 to 18,000. Center stage concerts 19,500 to 20,000. The info page and the A to Z guide agree. They do not list the sections in the gap.</td></tr>
<tr><th scope="row"><a href="/venues/prudential-center/">Prudential Center</a></th><td>A map titled End Stage Seating and a map titled Center Stage Seating. The A to Z guide says concert floor charts vary.</td></tr>
<tr><th scope="row"><a href="/venues/united-center/">United Center</a></th><td>A chart called Concert with floor seating and a chart called Concert with general admission floor, plus separate Bulls and Blackhawks files.</td></tr>
<tr><th scope="row"><a href="/venues/barclays-center/">Barclays Center</a></th><td>A Concerts and Entertainment chart, separate from the Nets chart. A GA floor ticket is standing room with no seats.</td></tr>
</tbody></table></div>
<p>None of those four pages ranks "the best section in the league." They tell you the paperwork changed. Open the building. <a href="/guides/how-to-choose-a-seat/">How to choose a seat</a> is the order. <a href="/guides/sections-to-skip/">Sections to skip</a> is the ticket label.</p>
{mid}
<h2>When the arena's own pages disagree on capacity</h2>
<p>Crypto.com Arena is the caution against copying one number. On {V} the <a href="{CRYPTO_AZ}">A to Z guide</a> says basketball capacity is 19,079, hockey is 18,118, and concerts and other special events near 20,000 depending on the setup. The <a href="{CRYPTO_VITAL}">vital stats page</a> says 18,997 for the Lakers, 18,145 for the Kings, and 19,395 for concerts, and that two thirds of the seating is in the lower level. The <a href="{NBA_LIST}">Wikipedia NBA arena list</a> figure on our venue page is 18,997 for basketball, which matches vital stats and not the A to Z guide. The <a href="{NHL_LIST}">NHL list</a> figure we carry for the Kings is 18,230, which matches neither official page. The <a href="/venues/crypto-com-arena/">Crypto.com Arena page</a> keeps the list figures in the table. This paragraph is here so a concert capacity and a game capacity are not treated as one fact.</p>
<p>The same A to Z guide is useful for the floor question even without a cleaned up capacity. It says a GA floor ticket is standing room only, with no seats, entered as "GA FLR" at the Kobe Bryant entrance, and that some shows use a different setup. Levels it names: event level for floor and GA tickets, main concourse for 100 and 200 level tickets, three suite levels, and an upper concourse for 300 level tickets. That stack is this building's stack. It is not the United Center's 100, 200, and 300, and it is not Barclays' upper pavilion.</p>
{compare}
<p>Madison Square Garden's concert seat map, opened the same day, says stage setup and seat configuration varies by event. The <a href="/venues/madison-square-garden/">Garden page</a> is the one to open for Knicks and Rangers. A shared building can sit on this list and on the <a href="/leagues/nhl/">NHL list</a>. Use the team on the ticket, then the chart with that event's name.</p>
''' + end + _src([
        ("Arena info", TM_INFO, "T-Mobile Arena"),
        ("A to Z guide", TM_AZ, "T-Mobile Arena"),
        ("Seating maps", PRU_SEAT, "Prudential Center"),
        ("A to Z guide", PRU_AZ, "Prudential Center"),
        ("Seating charts", UC_CHARTS, "United Center"),
        ("A to Z guide", BARC_AZ, "Barclays Center"),
        ("Seating charts", BARC_CHARTS, "Barclays Center"),
        ("A to Z guide", CRYPTO_AZ, "Crypto.com Arena"),
        ("Vital stats", CRYPTO_VITAL, "Crypto.com Arena"),
        ("Madison Square Garden concert seat map", "https://www.msg.com/madison-square-garden/seating/msg-concerts", "Madison Square Garden"),
    ])
    intro = "There are 29 NBA venues in this guide. A concert in the same building often uses a different chart from the game. The notes under this paragraph were checked %s." % V
    pairs = [
        ("Which NBA seats face the whole floor?",
         "On a game chart, the lowest seats at midcourt are the closest straight on view of the whole floor. The lowest seats behind a basket look at the near hoop. A concert in the same building can use a different chart."),
        ("Do NBA arenas publish a separate concert map?",
         "Several do. T-Mobile Arena prints an end stage capacity and a center stage capacity. Prudential Center publishes an end stage map and a center stage map. United Center publishes a reserved floor concert chart and a general admission floor concert chart. Barclays Center publishes a concerts chart and says a GA floor ticket is not a seat."),
        ("Why do some capacity numbers disagree?",
         "Crypto.com Arena's A to Z guide says basketball capacity is 19,079 and concerts near 20,000. Its vital stats page says 18,997 for the Lakers and 19,395 for concerts. The Wikipedia figure on our venue table matches 18,997. We keep both official numbers."),
        ("Does the sun matter at an NBA arena?",
         "No. Every arena on this list is indoor, so sun is not the seating factor."),
    ]
    return {
        "h1": "Which seats face the floor at an NBA arena?",
        "title": "NBA Arenas: Bowl, Floor, or Upper?",
        "desc": "NBA arenas are indoor. A concert in the same building uses another chart: end stage, center stage, or a floor with no seats.",
        "intro": intro,
        "extra": extra,
        "pairs": pairs,
        "verified": V,
        "mod": D,
    }


def _college(nr, cb, hero):
    mid = nr([
        ("/venues/michigan-stadium/", "Michigan Stadium", "The one school page in this hub with a 2026 row key."),
        ("/venues/ohio-stadium/", "Ohio Stadium", "A different building. Michigan's row numbers are not its row numbers."),
        ("/venues/beaver-stadium/", "Beaver Stadium", "Open the stadium page. This hub does not copy a Michigan section onto it."),
        ("/guides/shade-and-sun/", "Shade and sun", "The FBS list has no roof column, so this page does not assign shade."),
    ], heading="Open a stadium, not a template")
    end = nr([
        ("/guides/how-to-choose-a-seat/", "How to choose a seat", "Lowest seats near midfield, then the end zone tradeoff."),
        ("/guides/nfl-stadiums-with-a-roof/", "Which NFL stadiums have a roof", "The NFL list has a roof column. The college list does not."),
        ("/leagues/nfl/", "NFL venues", "Pro football bowls, with roof types attached."),
        ("/venues/rose-bowl-stadium/", "Rose Bowl Stadium", "Another open question the FBS list does not answer with a roof."),
    ], heading="Keep reading")
    compare = cb(
        "Check another stadium",
        "Michigan publishes the row bands below. The other 14 stadiums on this page do not, in a source we opened today. Use the stadium's own page.",
        [("/venues/michigan-stadium/", "Michigan Stadium"),
         ("/venues/ohio-stadium/", "Ohio Stadium"),
         ("/venues/neyland-stadium/", "Neyland Stadium"),
         ("/venues/rose-bowl-stadium/", "Rose Bowl Stadium")],
    )
    photo = _photo(hero, "This photo is a generic bowl at dusk. It is not Michigan Stadium, and it is not a seat map.")
    extra = f'''{photo}
<h2>The college list still has no roof column</h2>
<p>On {V} the <a href="{FBS}">list of NCAA Division I FBS football stadiums</a> still has no roof column. The columns on the page are stadium, city, state, team, conference, capacity, record, built, expanded, and surface. Shade is not something this hub can assign from that list. The <a href="/guides/nfl-stadiums-with-a-roof/">NFL roof guide</a> can group pro stadiums because the NFL list prints a roof. This page cannot. <a href="/guides/shade-and-sun/">Shade and sun</a> says the same thing one stadium at a time: when the source does not name a sunny section, we do not invent one.</p>
<h2>Michigan is the stadium that prints a row key</h2>
<p>The <a href="{MICH_MAP}">Michigan athletics 2026 preferred seat map</a> organizes Michigan Stadium into three row bands. Lower is rows A through 30. Middle is rows 31 through 60. Upper is row 61 and above. The same page names the horizontal zones the school uses, including Victors, Valiant, Maize, Blue, and End Zone, and it shows suites on the east and west sides. Contribution amounts are on that map. This page does not repeat them. A price is not a view.</p>
<div class="tablewrap"><table class="stats">
<thead><tr><th scope="col">Band on the 2026 Michigan map</th><th scope="col">Rows</th></tr></thead>
<tbody>
<tr><th scope="row">Lower</th><td>A through 30</td></tr>
<tr><th scope="row">Middle</th><td>31 through 60</td></tr>
<tr><th scope="row">Upper</th><td>61 and above</td></tr>
</tbody></table></div>
<p>End zone is its own zone on that map, not a nickname for "bad seats." The lowest end zone seats are close to one goal line and far from the other. The lowest sideline seats are the straight on view of the whole field. That tradeoff is the football method on <a href="/guides/how-to-choose-a-seat/">how to choose a seat</a>. Michigan's map is the school saying the bowl is cut both ways: height in three bands, and location in named zones.</p>
{mid}
<h2>Students are a published block, not a rumor</h2>
<p>The <a href="{MICH_STU}">2026 Michigan student football ticket policy</a> says the student section begins at the aisle break in section 25 and extends through section 34 if needed. Seats inside that block are assigned by priority points from the prior season. The highest totals sit in the lowest rows. Incoming students, who have no points yet, sit in the upper rows. Points reset each season. The policy says incoming students cannot be seated with returning students. That is one school's student block. It is not the student section at <a href="/venues/ohio-stadium/">Ohio Stadium</a>, <a href="/venues/beaver-stadium/">Beaver Stadium</a>, or <a href="/venues/neyland-stadium/">Neyland Stadium</a>.</p>
{compare}
<p>The other stadiums in the directory below still deserve their own pages. A Michigan row number copied onto another building would be a fiction. Open the stadium you are attending. Roof, when a school prints it, belongs on that page after we have read it. Until then the directory keeps the honest label from the list: roof not stated.</p>
''' + end + _src([
        ("List of NCAA Division I FBS football stadiums", FBS, "Wikipedia"),
        ("Michigan Stadium 2026 preferred seat map", MICH_MAP, "University of Michigan Athletics"),
        ("2026 student football ticket policies", MICH_STU, "University of Michigan Athletics"),
    ])
    intro = "There are 15 college football stadiums in this guide. The FBS list has no roof column, so this page does not assign shade. Michigan's 2026 map is the row key we could check on %s." % V
    pairs = [
        ("Which college football seats are in the shade?",
         "This page does not name them. On 21 Nov 2026 the FBS stadium list still had no roof column. The columns are stadium, city, state, team, conference, capacity, record, built, expanded, and surface."),
        ("What do lower, middle, and upper mean at Michigan Stadium?",
         "On Michigan's 2026 preferred seat map, lower is rows A through 30, middle is rows 31 through 60, and upper is row 61 and above. End zone is a named zone on the same map."),
        ("Where do Michigan students sit?",
         "The 2026 student ticket policy says the student section starts at the aisle break in section 25 and can run through section 34. Higher priority points sit in lower rows. Incoming students start in the upper rows."),
        ("Can I use the Michigan map at another stadium?",
         "No. Ohio Stadium, Beaver Stadium, Neyland, and the Rose Bowl are different buildings. Open that stadium's page. A Michigan row number is not theirs."),
    ]
    return {
        "h1": "Where should you sit for a college football game?",
        "title": "College Seats: Sideline or End Zone?",
        "desc": "The FBS list has no roof column. Michigan's 2026 map names lower, middle, and upper rows, plus a student section.",
        "intro": intro,
        "extra": extra,
        "pairs": pairs,
        "verified": V,
        "mod": D,
    }


CONCERT_IMG = "/assets/images/arena-concert-lower-bowl.png"
MSG_CONCERT = "https://www.msg.com/madison-square-garden/seating/msg-concerts"
MSG_SUITE = "https://www.msg.com/madison-square-garden/luxury-suites/suites/infosys-suite-level"
MSG_TOUR = "https://www.msg.com/msg-english-follow-along-tour-guide"


def write_concert(guide, hero_photo, next_reads, compare_box, root):
    """Emit the arena concert guide only when its thumbnail is in the tree."""
    img_path = os.path.join(root, CONCERT_IMG.lstrip("/"))
    if not os.path.isfile(img_path):
        print("IMAGE NEEDED: realistic news photo of an arena lower bowl, natural light, no logos, no readable text, no faces. File: assets/images/arena-concert-lower-bowl.png")
        return False
    _emit_concert(guide, hero_photo, next_reads, compare_box)
    return True


def _emit_concert(guide, hero_photo, nr, cb):
    mid = nr([
        ("/venues/madison-square-garden/", "Madison Square Garden", "Nine named maps, and a concert page that says the setup varies."),
        ("/venues/crypto-com-arena/", "Crypto.com Arena", "A GA floor has no seats. The upper concourse is the 300 level."),
        ("/venues/t-mobile-arena/", "T-Mobile Arena", "End stage and center stage are two different capacities."),
        ("/venues/prudential-center/", "Prudential Center", "The arena publishes both maps by name."),
    ], heading="Open the building")
    end = nr([
        ("/guides/how-to-choose-a-seat/", "How to choose a seat", "The chart name first, then the words on the ticket."),
        ("/guides/sections-to-skip/", "Sections to skip", "A limited view label is a ticket fact."),
        ("/venues/united-center/", "United Center", "Reserved floor and a general admission floor are different files."),
        ("/leagues/nba/", "NBA venues", "Most of these arenas are on the basketball list too."),
    ], heading="Keep reading")
    compare = cb(
        "Check another arena",
        'The three buildings below do not share a vocabulary. <a href="/venues/madison-square-garden/">MSG</a> names bands and says the setup varies. <a href="/venues/crypto-com-arena/">Crypto.com Arena</a> says the floor ticket can be standing room. <a href="/venues/t-mobile-arena/">T-Mobile Arena</a> prints two concert capacities.',
        [("/venues/madison-square-garden/", "Madison Square Garden"),
         ("/venues/crypto-com-arena/", "Crypto.com Arena"),
         ("/venues/t-mobile-arena/", "T-Mobile Arena"),
         ("/venues/prudential-center/", "Prudential Center"),
         ("/venues/barclays-center/", "Barclays Center")],
    )
    body = f'''{hero_photo("Arena lower bowl in daylight, empty seats facing a bare stage end, no logos and no readable signs", CONCERT_IMG)}
<p class="note">The photo is a generic lower bowl. It is not Madison Square Garden, Crypto.com Arena, or T-Mobile Arena, and it is not a seating chart. <a href="/image-policy/">Image policy</a>.</p>
<p class="answer">Madison Square Garden, Crypto.com Arena, and T-Mobile Arena do not publish a ranking of floor, lower bowl, upper level, and a side seat. They publish different paperwork, and the paperwork does not use the same words. MSG groups the floor with the 100s and the 200s, then lists the 300s with the bridge and the 400s on their own, and it says the stage setup varies by event. Crypto.com Arena says a general admission floor ticket has no seat, and it stacks a 300 level above three suite levels. T-Mobile Arena prints a smaller capacity for an end stage concert than for a center stage concert, and it places loge boxes at the end of the lower bowl opposite the stage. Checked {V}.</p>
<h2>End stage and center stage are not one chart with two nicknames</h2>
<p>Start with the building that prints the split as a headcount. On {V} both the <a href="{TM_INFO}">T-Mobile Arena info page</a> and the <a href="{TM_AZ}">A to Z guide</a> list end stage concerts at 12,000 to 18,000 and center stage concerts at 19,500 to 20,000. Hockey is 17,500 on both pages. Basketball is 18,000 on the info page and 19,000 on the A to Z guide, so this guide does not pick a basketball number. The concert ranges match. The pages do not name the sections that account for the gap between an end stage show and a center stage show. A smaller end stage number means the bowl on sale is smaller. It is not, by itself, a list of seats to avoid.</p>
<p>Madison Square Garden does not use those two phrases on its concert seat map. The <a href="{MSG_CONCERT}">concerts page</a> says stage setup and seat configuration varies by event. The same page carries nine named maps: NY Knicks, NY Rangers, Concerts, College Basketball, Professional Bull Riding, WWE, Tennis, Boxing, and UFC. Concerts is one file among those nine. It is not split on that page into an end stage file and a center stage file. If you need the two names printed as two maps, that is <a href="/venues/prudential-center/">Prudential Center</a>, whose seating page titles them End Stage Seating and Center Stage Seating. <a href="/venues/united-center/">United Center</a> splits the floor instead: one chart with floor seating, one chart with a general admission floor.</p>
{mid}
<h2>Floor: sometimes a chair, sometimes a wristband</h2>
<p>Crypto.com Arena's <a href="{CRYPTO_AZ}">A to Z guide</a> is blunt about one product. The general admission area on the floor is standing room only and there are no seats. The ticket reads "GA FLR." You enter at the Kobe Bryant entrance, you get a wristband, and the guide says some shows use a different setup. Read the event page before you assume the floor is a chair.</p>
<p>T-Mobile Arena's A to Z guide says the same kind of thing in its own words. The general admission floor is standing room only, there are no seats, you get a wristband inside, and early arrivals are asked to line up no earlier than 4 p.m. Concert doors generally open 60 minutes before the event. That is a standing ticket. A reserved seat in the bowl is a different purchase.</p>
<p>MSG's concert page does not say whether the floor is seated or standing. What it does say, in the filter on that page, is that Floor, 100s, and 200s are one group. Suites are separate. The 400s are separate. The 300s are grouped with the Hyundai Bridge. Because the page also says the configuration varies by event, a floor section on one show can be a seat and on the next show a different shape entirely. The filter names the bands. It does not freeze them.</p>
<h2>Lower bowl and upper level, in each building's own stack</h2>
<p>Crypto.com Arena lists six levels: event level for floor and GA tickets, main concourse for 100 and 200 level tickets, suite levels A, B, and C, and an upper concourse for 300 level tickets. The <a href="{CRYPTO_VITAL}">vital stats page</a> says two thirds of the seating is in the lower level, counts 2,515 premier seats, and lists concert capacity at 19,395. The A to Z guide says concerts near 20,000 depending on setup, basketball at 19,079, and hockey at 18,118. Vital stats say 18,997 for the Lakers and 18,145 for the Kings. Both pages were open on {V}. The lower level is where most of the chairs are, on the vital stats page. The 300 level is the upper concourse, above three suite levels, which is a taller climb than a building with one suite ring. That is this arena's stack. It is not a template for the other two.</p>
<p>At the Garden, the concert filters are the public stack: floor with the 100s and 200s, then suites, then 400s, then 300s with the Hyundai Bridge. The <a href="{MSG_SUITE}">Infosys suite page</a> places that suite product in the upper bowl, just below bridge level, and it says the location is stage facing for concerts. The page's own line is "some of the best stage-facing sight lines." That is MSG describing the Infosys suites, which hold 12 to 21 people. The same page also lists an event level suite at ice or court level for 8 to 13 people, and a suite it calls an extension of the lower bowl for 12 to 24 people. Three products, three heights. The tour script, opened the same day, names the walk in a different sponsor vocabulary: level 5 is the arena floor, level 6 is the Kalshi Concourse, level 7 is Lexus Suites, and level 10 is the Hyundai Bridge. The suite page still says Infosys. The tour script says Kalshi. Both strings are on msg.com. This guide does not decide which sponsor name is current beyond what each page prints.</p>
<p>The tour script also says that removing visible support beams gives fans a perfectly unobstructed view from every single seat in the arena. That sentence is about the roof, forty-eight cables to a tension ring, not about a concert stage. The concert page still says the setup varies by event. A building with no pillars can still put a stage in front of some seats. The <a href="/venues/madison-square-garden/">Garden page</a> on this site is the Knicks and Rangers guide. This one is the concert reading.</p>
{compare}
<h2>There is no published side stage band</h2>
<p>The words side stage do not appear on the MSG concert page, the Crypto.com Arena A to Z guide, or the T-Mobile Arena pages opened for this check. The closest official sentences point the other way. T-Mobile's loge boxes, the A to Z guide says, sit at one end of the lower level at the opposite end of the stage for viewing concerts, four to six guests, with a screen for every two seats. That is the far end, facing the stage, not a seat beside it. Club memberships are the two center sections, and the guide does not print their numbers. MSG's filter refuses the side split by putting the floor, the 100s, and the 200s in a single button. If a ticket says limited view or obstructed view, that label is the fact. <a href="/guides/sections-to-skip/">Sections to skip</a> is where that label belongs.</p>
<p>Barclays is the nearby caution on the floor, already written up on its <a href="/venues/barclays-center/">own page</a>: a GA floor ticket there is standing room with no seat, and the concerts chart is a separate file from the Nets chart. Use it when the question is Brooklyn. Use this page when the question is how to read the three buildings people compare first.</p>
{end}'''
    _clean("concert body", body)
    title = "Arena Concerts: Floor or the Bowl?"
    desc = "Floor, lower bowl, or upper level at an arena concert: what MSG, Crypto.com Arena, and T-Mobile Arena actually print."
    h1 = "Which arena concert seat faces the stage?"
    if len(title) >= 60:
        raise SystemExit("concert title %d" % len(title))
    if len(desc) > 155:
        raise SystemExit("concert desc %d" % len(desc))
    pairs = [
        ("Is the floor the best seat at an arena concert?",
         "Not as a rule, and sometimes it is not a seat. Crypto.com Arena and T-Mobile Arena both say a general admission floor ticket is standing room with no seats. MSG groups the floor with the 100s and 200s and says the stage setup varies by event."),
        ("What is the difference between an end stage and a center stage?",
         "At T-Mobile Arena the printed capacities differ: 12,000 to 18,000 for an end stage concert and 19,500 to 20,000 for a center stage concert. MSG's concert page does not use those two names. It says the configuration varies and publishes one map called Concerts. Prudential Center publishes both names as separate maps."),
        ("Where is the upper level?",
         "At Crypto.com Arena the upper concourse is the 300 level, above three suite levels. At MSG the concert filters list the 300s with the Hyundai Bridge and the 400s on their own. At T-Mobile Arena the upper concourse is one of seven levels, and not every level opens for every event."),
        ("Which seats are beside the stage?",
         "The three official pages checked on 21 Nov 2026 do not label a side stage band. T-Mobile Arena describes loge boxes at the opposite end of the stage. A limited view note on the ticket is the fact to trust."),
    ]
    for q, ans in pairs:
        _clean("concert faq", q + ans)
    sources = [
        {"title": "Concert seating chart", "url": MSG_CONCERT, "publisher": "Madison Square Garden", "role": "official"},
        {"title": "Infosys Suite Level", "url": MSG_SUITE, "publisher": "Madison Square Garden", "role": "official"},
        {"title": "All Access Tour guide", "url": MSG_TOUR, "publisher": "Madison Square Garden", "role": "official"},
        {"title": "A to Z guide", "url": CRYPTO_AZ, "publisher": "Crypto.com Arena", "role": "official"},
        {"title": "Vital stats", "url": CRYPTO_VITAL, "publisher": "Crypto.com Arena", "role": "official"},
        {"title": "Arena info", "url": TM_INFO, "publisher": "T-Mobile Arena", "role": "official"},
        {"title": "A to Z guide", "url": TM_AZ, "publisher": "T-Mobile Arena", "role": "official"},
        {"title": "Seating maps", "url": PRU_SEAT, "publisher": "Prudential Center", "role": "official"},
    ]
    guide("/guides/arena-concert-seating/", title, h1, desc, body, pairs, sources,
          mod=D, published=D, verified=V, image=CONCERT_IMG, sources_retrieved=V)
