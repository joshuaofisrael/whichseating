#!/usr/bin/env python3
"""Build _build/venues.json from cited list rows. Retrieved 16 Nov 2026.
Run from the repo root: python3 _build/gen_data.py
"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venues.json")

W_NFL = ("List of current NFL stadiums", "https://en.wikipedia.org/wiki/List_of_current_NFL_stadiums", "Wikipedia")
W_MLB = ("List of current Major League Baseball stadiums", "https://en.wikipedia.org/wiki/List_of_current_Major_League_Baseball_stadiums", "Wikipedia")
W_NBA = ("List of NBA arenas", "https://en.wikipedia.org/wiki/List_of_NBA_arenas", "Wikipedia")
W_NHL = ("List of National Hockey League arenas", "https://en.wikipedia.org/wiki/List_of_National_Hockey_League_arenas", "Wikipedia")
W_NCAA = ("List of NCAA Division I FBS football stadiums", "https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_FBS_football_stadiums", "Wikipedia")
MLB_DIR = ("MLB.com ballpark guide directory", "https://www.mlb.com/fans/ballpark-guides/mlb", "MLB.com")
NBA_NEWS = ("All 30 NBA team arenas", "https://www.nba.com/news/all-30-nba-arenas-by-team", "NBA.com")

ABBR = {
 "AL":"Alabama","AR":"Arkansas","AZ":"Arizona","CA":"California","CO":"Colorado","DC":"District of Columbia",
 "FL":"Florida","GA":"Georgia","IL":"Illinois","IN":"Indiana","LA":"Louisiana","MA":"Massachusetts",
 "MD":"Maryland","MI":"Michigan","MN":"Minnesota","MO":"Missouri","NC":"North Carolina","NE":"Nebraska",
 "NJ":"New Jersey","NV":"Nevada","NY":"New York","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania",
 "SC":"South Carolina","TN":"Tennessee","TX":"Texas","UT":"Utah","WA":"Washington","WI":"Wisconsin",
}

def slug(name):
    s = name.replace("&", " and ").replace(".com", "-com").replace(".", "").replace("'", "")
    s = s.replace("\u2013", "-").replace("\u2014", "-")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s

def src(triple, role):
    title, url, publisher = triple
    return {"title": title, "url": url, "publisher": publisher, "role": role}

VENUES = []

def add(name, loc, opened, roof_label, teams, capacities, surface="", notes=None, official=None, extra_sources=None, ballpark_type="", center="", lists=None):
    if loc in ("Washington, D.C.", "Washington, DC"):
        city, state = "Washington", "District of Columbia"
    else:
        city, state = [x.strip() for x in loc.rsplit(",", 1)]
    rec = {
        "name": name,
        "slug": slug(name),
        "city": city,
        "state": state,
        "opened": opened,
        "roof_label": roof_label,
        "teams": [{"league": lg, "name": tn} for lg, tn in teams],
        "capacities": [{"label": lab, "value": val} for lab, val in capacities],
        "surface": surface,
        "ballpark_type": ballpark_type,
        "center_field": center,
        "notes": notes or [],
        "sources": [src(t, "list") for t in (lists or [])],
    }
    if official:
        rec["sources"].append(src(official, "official"))
    for t in extra_sources or []:
        rec["sources"].append(src(t, "extra"))
    for n in rec["notes"]:
        if "\u2013" in n or "\u2014" in n or re.search(r"\bsections?\s+\d+", n, re.I):
            raise SystemExit("bad note on " + name)
    VENUES.append(rec)

def nfl(name, teams, loc, cap, roof, opened, surface, official=None, notes=None, extra=None):
    add(name, loc, opened, roof, [("nfl", t) for t in teams], [("Listed capacity", cap)],
        surface=surface, notes=notes, official=official, extra_sources=extra, lists=[W_NFL])

def mlb(name, team, loc, cap, opened, surface, center, btype, roof, slug_key, notes=None, extra=None):
    official = (team + " ballpark page on MLB.com", "https://www.mlb.com/%s/ballpark" % slug_key, "MLB.com")
    add(name, loc, opened, roof, [("mlb", team)], [("Listed capacity", cap)],
        surface=surface, center=center, ballpark_type=btype, notes=notes,
        official=official, extra_sources=[MLB_DIR] + (extra or []), lists=[W_MLB])

def arena(name, loc, opened, teams, capacities, official=None, notes=None, extra=None, lists=None):
    add(name, loc, opened, "Indoor", teams, capacities, notes=notes, official=official,
        extra_sources=extra, lists=lists or [])

# --- NFL. Capacity, roof, surface, opened, and city from the Wikipedia NFL list. ---
nfl("Acrisure Stadium", ["Pittsburgh Steelers"], "Pittsburgh, Pennsylvania", "68,984", "Open-air", "2001", "Bermuda grass")
nfl("Allegiant Stadium", ["Las Vegas Raiders"], "Paradise, Nevada", "66,000", "Skylight", "2020", "Bermuda grass")
nfl("Arrowhead Stadium", ["Kansas City Chiefs"], "Kansas City, Missouri", "73,426", "Open-air", "1972", "Bermuda grass",
    official=("Chiefs stadium page", "https://www.chiefs.com/stadium/", "Kansas City Chiefs"),
    notes=["The Wikipedia NFL list says the Chiefs sold naming rights for the field to GEHA from 2021 to 2026, then returned the stadium name to Arrowhead Stadium."])
nfl("AT&T Stadium", ["Dallas Cowboys"], "Arlington, Texas", "80,000", "Retractable", "2009", "Artificial",
    official=("Cowboys stadium page", "https://www.dallascowboys.com/stadium/", "Dallas Cowboys"))
nfl("Bank of America Stadium", ["Carolina Panthers"], "Charlotte, North Carolina", "75,037", "Open-air", "1996", "FieldTurf")
nfl("Caesars Superdome", ["New Orleans Saints"], "New Orleans, Louisiana", "73,208", "Dome", "1975", "Artificial",
    official=("Saints stadium page", "https://www.neworleanssaints.com/stadium/", "New Orleans Saints"))
nfl("Empower Field at Mile High", ["Denver Broncos"], "Denver, Colorado", "76,125", "Open-air", "2001", "Kentucky bluegrass",
    official=("Empower Field at Mile High", "https://www.empowerfieldatmilehigh.com/", "Empower Field at Mile High"))
nfl("EverBank Stadium", ["Jacksonville Jaguars"], "Jacksonville, Florida", "69,132", "Open-air", "1995", "Bermuda grass",
    official=("Jaguars stadium page", "https://www.jaguars.com/stadium/", "Jacksonville Jaguars"))
nfl("Ford Field", ["Detroit Lions"], "Detroit, Michigan", "65,000", "Dome", "2002", "FieldTurf",
    official=("Lions stadium page", "https://www.detroitlions.com/stadium/", "Detroit Lions"))
nfl("Gillette Stadium", ["New England Patriots"], "Foxborough, Massachusetts", "66,829", "Open-air", "2002", "FieldTurf")
nfl("Hard Rock Stadium", ["Miami Dolphins"], "Miami Gardens, Florida", "65,326", "Open-air", "1987", "Bermuda grass")
nfl("Highmark Stadium", ["Buffalo Bills"], "Orchard Park, New York", "60,108", "Open-air", "2026", "Kentucky bluegrass",
    official=("Bills stadium page", "https://www.buffalobills.com/stadium/", "Buffalo Bills"),
    extra=[("Highmark Stadium", "https://en.wikipedia.org/wiki/Highmark_Stadium", "Wikipedia")],
    notes=["The Wikipedia NFL list calls this the newest NFL stadium and the smallest listed capacity in the league, at 60,108, and gives the opened year as 2026.",
           "The Highmark Stadium Wikipedia article describes the figure as 60,108 seats plus 2,892 standing room places, which it totals as 63,000."])
nfl("Huntington Bank Field", ["Cleveland Browns"], "Cleveland, Ohio", "67,895", "Open-air", "1999", "Kentucky bluegrass")
nfl("Lambeau Field", ["Green Bay Packers"], "Green Bay, Wisconsin", "81,441", "Open-air", "1957", "Hybrid grass",
    official=("Packers Lambeau Field page", "https://www.packers.com/lambeau-field/", "Green Bay Packers"),
    notes=["The Wikipedia NFL list calls Lambeau Field the oldest continuously operating NFL stadium, with the Packers as tenant since it opened in 1957."])
nfl("Levi's Stadium", ["San Francisco 49ers"], "Santa Clara, California", "68,500", "Open-air", "2014", "Bermuda grass")
nfl("Lincoln Financial Field", ["Philadelphia Eagles"], "Philadelphia, Pennsylvania", "69,596", "Open-air", "2003", "GrassMaster")
nfl("Lucas Oil Stadium", ["Indianapolis Colts"], "Indianapolis, Indiana", "67,000", "Retractable", "2008", "Artificial")
nfl("Lumen Field", ["Seattle Seahawks"], "Seattle, Washington", "69,000", "Open-air", "2002", "FieldTurf")
nfl("M&T Bank Stadium", ["Baltimore Ravens"], "Baltimore, Maryland", "71,008", "Open-air", "1998", "Bermuda and ryegrass",
    official=("Ravens stadium page", "https://www.baltimoreravens.com/stadium/", "Baltimore Ravens"))
nfl("Mercedes-Benz Stadium", ["Atlanta Falcons"], "Atlanta, Georgia", "71,000", "Retractable", "2017", "FieldTurf",
    official=("Falcons stadium page", "https://www.atlantafalcons.com/stadium/", "Atlanta Falcons"))
nfl("MetLife Stadium", ["New York Giants", "New York Jets"], "East Rutherford, New Jersey", "82,500", "Open-air", "2010", "FieldTurf",
    notes=["The Wikipedia NFL list says MetLife Stadium has the highest listed seating capacity in the league, at 82,500. The Giants and the Jets share it."])
nfl("Nissan Stadium", ["Tennessee Titans"], "Nashville, Tennessee", "69,143", "Open-air", "1999", "Artificial",
    official=("Titans stadium page", "https://www.tennesseetitans.com/stadium/", "Tennessee Titans"),
    notes=["The same Wikipedia page lists a new Titans stadium as under construction in Nashville, with an opening year of 2027. This guide is about the stadium in use now."])
nfl("Northwest Stadium", ["Washington Commanders"], "Landover, Maryland", "64,000", "Open-air", "1997", "Bermuda grass",
    official=("Northwest Stadium", "https://northweststadium.com/", "Northwest Stadium"))
nfl("Paycor Stadium", ["Cincinnati Bengals"], "Cincinnati, Ohio", "65,515", "Open-air", "2000", "Artificial",
    official=("Bengals stadium page", "https://www.bengals.com/stadium/", "Cincinnati Bengals"))
nfl("Raymond James Stadium", ["Tampa Bay Buccaneers"], "Tampa, Florida", "65,890", "Open-air", "1998", "Bermuda grass",
    official=("Buccaneers stadium page", "https://www.buccaneers.com/stadium/", "Tampa Bay Buccaneers"))
nfl("Reliant Stadium", ["Houston Texans"], "Houston, Texas", "72,220", "Retractable", "2002", "Artificial",
    official=("Texans stadium page", "https://www.houstontexans.com/stadium/", "Houston Texans"),
    notes=["The Texans official stadium page calls the building Reliant Stadium, previously NRG Stadium, and says the Reliant name returned in August 2026. The Wikipedia NFL list uses Reliant Stadium and a retractable roof."])
nfl("SoFi Stadium", ["Los Angeles Rams", "Los Angeles Chargers"], "Inglewood, California", "70,000", "Skylight", "2020", "Artificial",
    official=("SoFi Stadium", "https://www.sofistadium.com/", "SoFi Stadium"),
    extra=[("Chargers SoFi Stadium page", "https://www.chargers.com/sofi-stadium/", "Los Angeles Chargers")],
    notes=["The Rams and the Chargers share SoFi Stadium. The Wikipedia NFL list classifies the roof as a skylight."])
nfl("Soldier Field", ["Chicago Bears"], "Chicago, Illinois", "62,500", "Open-air", "1924", "Bermuda grass",
    official=("Bears stadium page", "https://stadium.chicagobears.com/", "Chicago Bears"),
    notes=["The Wikipedia NFL list says Soldier Field opened in 1924. A note on that page says the playing field and seating bowl were renovated in 2003."])
nfl("State Farm Stadium", ["Arizona Cardinals"], "Glendale, Arizona", "63,400", "Retractable", "2006", "Bermuda grass",
    official=("Cardinals stadium page", "https://www.azcardinals.com/stadium/", "Arizona Cardinals"))
nfl("U.S. Bank Stadium", ["Minnesota Vikings"], "Minneapolis, Minnesota", "66,655", "Skylight", "2016", "Artificial",
    official=("Vikings stadium page", "https://www.vikings.com/stadium/", "Minnesota Vikings"))

# --- MLB. US parks only. Rogers Centre in Toronto is outside this US guide. ---
MLB = [
("American Family Field","Milwaukee Brewers","Milwaukee, Wisconsin","41,900","2001","Grass","400 feet","Retro-modern","Retractable","brewers"),
("Angel Stadium","Los Angeles Angels","Anaheim, California","45,517","1966","Grass","396 feet","Modern and retro-modern","Open","angels"),
("Busch Stadium","St. Louis Cardinals","St. Louis, Missouri","44,383","2006","Grass","400 feet","Retro-classic","Open","cardinals"),
("Chase Field","Arizona Diamondbacks","Phoenix, Arizona","48,330","1998","Artificial turf","407 feet","Retro-modern","Retractable","dbacks"),
("Citi Field","New York Mets","Queens, New York","41,922","2009","Grass","408 feet","Retro-classic","Open","mets"),
("Citizens Bank Park","Philadelphia Phillies","Philadelphia, Pennsylvania","42,901","2004","Grass","401 feet","Retro-classic","Open","phillies"),
("Comerica Park","Detroit Tigers","Detroit, Michigan","41,083","2000","Grass","412 feet","Retro-classic","Open","tigers"),
("Coors Field","Colorado Rockies","Denver, Colorado","46,897","1995","Grass","415 feet","Retro-classic","Open","rockies"),
("Daikin Park","Houston Astros","Houston, Texas","41,168","2000","Grass","409 feet","Retro-modern","Retractable","astros"),
("Dodger Stadium","Los Angeles Dodgers","Los Angeles, California","56,000","1962","Grass","395 feet","Modern","Open","dodgers"),
("Fenway Park","Boston Red Sox","Boston, Massachusetts","37,755","1912","Grass","390 feet","Jewel box","Open","redsox"),
("Globe Life Field","Texas Rangers","Arlington, Texas","40,300","2020","Artificial turf","407 feet","Retro-modern","Retractable","rangers"),
("Great American Ball Park","Cincinnati Reds","Cincinnati, Ohio","43,500","2003","Grass","404 feet","Retro-modern","Open","reds"),
("Kauffman Stadium","Kansas City Royals","Kansas City, Missouri","37,903","1973","Grass","410 feet","Modern and retro-modern","Open","royals"),
("LoanDepot Park","Miami Marlins","Miami, Florida","36,742","2012","Artificial turf","407 feet","Contemporary","Retractable","marlins"),
("Nationals Park","Washington Nationals","Washington, D.C.","41,373","2008","Grass","402 feet","Retro-modern","Open","nationals"),
("Oracle Park","San Francisco Giants","San Francisco, California","41,331","2000","Grass","391 feet","Retro-classic","Open","giants"),
("Oriole Park at Camden Yards","Baltimore Orioles","Baltimore, Maryland","42,455","1992","Grass","410 feet","Retro-classic","Open","orioles"),
("Petco Park","San Diego Padres","San Diego, California","39,860","2004","Grass","396 feet","Retro-modern","Open","padres"),
("PNC Park","Pittsburgh Pirates","Pittsburgh, Pennsylvania","38,747","2001","Grass","399 feet","Retro-classic","Open","pirates"),
("Progressive Field","Cleveland Guardians","Cleveland, Ohio","34,820","1994","Grass","410 feet","Retro-modern","Open","guardians"),
("Rate Field","Chicago White Sox","Chicago, Illinois","40,615","1991","Grass","400 feet","Modern and retro-classic","Open","whitesox"),
("Sutter Health Park","Athletics","West Sacramento, California","13,416","2000","Grass","403 feet","Retro-modern","Open","athletics"),
("T-Mobile Park","Seattle Mariners","Seattle, Washington","47,929","1999","Grass","401 feet","Retro-modern","Retractable","mariners"),
("Target Field","Minnesota Twins","Minneapolis, Minnesota","38,544","2010","Grass","404 feet","Retro-modern","Open","twins"),
("Tropicana Field","Tampa Bay Rays","St. Petersburg, Florida","25,000","1990","Artificial turf","404 feet","Modern","Fixed","rays"),
("Truist Park","Atlanta Braves","Cumberland, Georgia","41,084","2017","Grass","400 feet","Retro-modern","Open","braves"),
("Wrigley Field","Chicago Cubs","Chicago, Illinois","41,649","1914","Grass","400 feet","Jewel box","Open","cubs"),
("Yankee Stadium","New York Yankees","Bronx, New York","46,537","2009","Grass","408 feet","Retro-classic","Open","yankees"),
]
MLB_NOTES = {
 "Dodger Stadium": ["The Wikipedia MLB list introduction says the Dodgers sold naming rights for the field to Uniqlo and kept the stadium name Dodger Stadium."],
 "Sutter Health Park": ["The Wikipedia MLB list says Sutter Health Park is a temporary home for the Athletics until a new stadium in Las Vegas is completed in 2028. The listed capacity, 13,416, is far smaller than a typical MLB park."],
 "Tropicana Field": ["The list gives a fixed roof and a listed capacity of 25,000. The citation on that row is a January 2019 USA Today report that the Rays closed the upper deck to shrink the bowl. The list also notes that the building opened in 1990 and the Rays have played there since 1998. Treat the upper deck as closed unless the current official page says it is open."],
}
MLB_EXTRA = {
 "Tropicana Field": [("Tampa Bay Rays reduce seating capacity at Tropicana Field", "https://www.usatoday.com/story/sports/mlb/rays/2019/01/04/rays-tropicana-field-close-upper-deck-reduce-capacity/2481217002/", "USA Today")],
}
for row in MLB:
    name, team, loc, cap, opened, surface, center, btype, roof, key = row
    mlb(name, team, loc, cap, opened, surface, center, btype, roof, key, notes=MLB_NOTES.get(name), extra=MLB_EXTRA.get(name))

# --- NBA arenas in the US, plus hockey tenants where the NHL list names the same building. ---
# capacities: (label, value). lists assigned below.
NBA = [
("American Airlines Center","Dallas, Texas","2001","Dallas Mavericks","19,200"),
("Ball Arena","Denver, Colorado","1999","Denver Nuggets","19,520"),
("Barclays Center","Brooklyn, New York","2012","Brooklyn Nets","17,732"),
("Capital One Arena","Washington, D.C.","1997","Washington Wizards","20,333"),
("Chase Center","San Francisco, California","2019","Golden State Warriors","18,064"),
("Crypto.com Arena","Los Angeles, California","1999","Los Angeles Lakers","18,997"),
("Delta Center","Salt Lake City, Utah","1991","Utah Jazz","18,306"),
("FedExForum","Memphis, Tennessee","2004","Memphis Grizzlies","17,794"),
("Fiserv Forum","Milwaukee, Wisconsin","2018","Milwaukee Bucks","17,341"),
("Frost Bank Center","San Antonio, Texas","2002","San Antonio Spurs","18,354"),
("Gainbridge Fieldhouse","Indianapolis, Indiana","1999","Indiana Pacers","17,923"),
("Golden 1 Center","Sacramento, California","2016","Sacramento Kings","17,611"),
("Intuit Dome","Inglewood, California","2024","Los Angeles Clippers","18,000"),
("Kaseya Center","Miami, Florida","1999","Miami Heat","19,600"),
("Kia Center","Orlando, Florida","2010","Orlando Magic","18,846"),
("Little Caesars Arena","Detroit, Michigan","2017","Detroit Pistons","20,332"),
("Madison Square Garden","New York City, New York","1968","New York Knicks","19,812"),
("Moda Center","Portland, Oregon","1995","Portland Trail Blazers","19,411"),
("Mortgage Matchup Center","Phoenix, Arizona","1992","Phoenix Suns","17,071"),
("Paycom Center","Oklahoma City, Oklahoma","2002","Oklahoma City Thunder","18,203"),
("Rocket Arena","Cleveland, Ohio","1994","Cleveland Cavaliers","19,432"),
("Smoothie King Center","New Orleans, Louisiana","1999","New Orleans Pelicans","16,867"),
("Spectrum Center","Charlotte, North Carolina","2005","Charlotte Hornets","19,077"),
("State Farm Arena","Atlanta, Georgia","1999","Atlanta Hawks","17,044"),
("Target Center","Minneapolis, Minnesota","1990","Minnesota Timberwolves","18,024"),
("TD Garden","Boston, Massachusetts","1995","Boston Celtics","18,624"),
("Toyota Center","Houston, Texas","2003","Houston Rockets","18,055"),
("United Center","Chicago, Illinois","1994","Chicago Bulls","20,917"),
("Xfinity Mobile Arena","Philadelphia, Pennsylvania","1996","Philadelphia 76ers","20,007"),
]
HOCKEY = {
 "American Airlines Center": ("Dallas Stars","18,532"),
 "Ball Arena": ("Colorado Avalanche","17,809"),
 "Capital One Arena": ("Washington Capitals","18,573"),
 "Crypto.com Arena": ("Los Angeles Kings","18,230"),
 "Delta Center": ("Utah Mammoth","16,020"),
 "Little Caesars Arena": ("Detroit Red Wings","19,515"),
 "Madison Square Garden": ("New York Rangers","18,006"),
 "TD Garden": ("Boston Bruins","17,565"),
 "United Center": ("Chicago Blackhawks","19,717"),
 "Xfinity Mobile Arena": ("Philadelphia Flyers","19,538"),
}
ARENA_OFFICIAL = {
 "American Airlines Center": ("American Airlines Center", "https://www.americanairlinescenter.com/", "American Airlines Center"),
 "Ball Arena": ("Ball Arena", "https://www.ballarena.com/", "Ball Arena"),
 "Barclays Center": ("Barclays Center", "https://www.barclayscenter.com/", "Barclays Center"),
 "Capital One Arena": ("Capital One Arena", "https://www.capitalonearena.com/", "Capital One Arena"),
 "Chase Center": ("Chase Center", "https://www.chasecenter.com/", "Chase Center"),
 "Crypto.com Arena": ("Crypto.com Arena", "https://www.cryptoarena.com/", "Crypto.com Arena"),
 "Fiserv Forum": ("Fiserv Forum", "https://www.fiservforum.com/", "Fiserv Forum"),
 "Gainbridge Fieldhouse": ("Gainbridge Fieldhouse", "https://www.gainbridgefieldhouse.com/", "Gainbridge Fieldhouse"),
 "Intuit Dome": ("Intuit Dome", "https://www.intuitdome.com/", "Intuit Dome"),
 "Kaseya Center": ("Kaseya Center", "https://www.kaseyacenter.com/", "Kaseya Center"),
 "Madison Square Garden": ("Madison Square Garden", "https://www.msg.com/madison-square-garden", "Madison Square Garden"),
 "State Farm Arena": ("State Farm Arena", "https://www.statefarmarena.com/", "State Farm Arena"),
 "TD Garden": ("TD Garden", "https://www.tdgarden.com/", "TD Garden"),
 "Xfinity Mobile Arena": ("Xfinity Mobile Arena", "https://www.xfinitymobilearena.com/", "Xfinity Mobile Arena"),
}
ARENA_NOTES = {
 "Madison Square Garden": ["The NBA arena list locates Madison Square Garden in New York, New York. This page files the city as New York City.",
     "The NBA arena list says the building opened in 1968 and was renovated from 2010 to 2013, with a new bowl and concourses inside the original structure."],
 "Paycom Center": ["The NBA arena list gives an opened year of 2002 and a first NBA season of 2005 to 2006."],
 "Delta Center": ["The NHL arena list names the hockey tenant as the Utah Mammoth. The official team site uses that name. The list gives 2024 to 2025 as the first NHL season there."],
}
ARENA_EXTRA = {
 "Delta Center": [("Official Utah Mammoth website", "https://www.nhl.com/utah/", "NHL.com")],
}
for name, loc, opened, team, cap in NBA:
    teams = [("nba", team)]
    caps = [("Basketball capacity listed", cap)]
    lists = [W_NBA]
    extra = [NBA_NEWS]
    if name in HOCKEY:
        ht, hc = HOCKEY[name]
        teams.append(("nhl", ht))
        caps.append(("Hockey capacity listed", hc))
        lists.append(W_NHL)
    extra = extra + ARENA_EXTRA.get(name, [])
    arena(name, loc, opened, teams, caps, official=ARENA_OFFICIAL.get(name), notes=ARENA_NOTES.get(name), extra=extra, lists=lists)

# NHL-only US arenas (not already covered as an NBA building). Canadian arenas are omitted.
NHL_ONLY = [
("Amerant Bank Arena","Sunrise, Florida","1998","Florida Panthers","19,250", None),
("Benchmark International Arena","Tampa, Florida","1996","Tampa Bay Lightning","19,092",
    ("Lightning arena page", "https://www.nhl.com/lightning/arena/", "Tampa Bay Lightning")),
("Bridgestone Arena","Nashville, Tennessee","1996","Nashville Predators","17,159",
    ("Bridgestone Arena", "https://www.bridgestonearena.com/", "Bridgestone Arena")),
("Climate Pledge Arena","Seattle, Washington","2021","Seattle Kraken","17,151",
    ("Climate Pledge Arena", "https://climatepledgearena.com/", "Climate Pledge Arena")),
("Enterprise Center","St. Louis, Missouri","1994","St. Louis Blues","18,096", None),
("Grand Casino Arena","Saint Paul, Minnesota","2000","Minnesota Wild","17,954",
    ("Wild game day page", "https://www.nhl.com/wild/arena/game-day", "Minnesota Wild")),
("Honda Center","Anaheim, California","1993","Anaheim Ducks","17,174", None),
("KeyBank Center","Buffalo, New York","1996","Buffalo Sabres","19,070",
    ("KeyBank Center", "https://www.keybankcenter.com/", "KeyBank Center")),
("Lenovo Center","Raleigh, North Carolina","1999","Carolina Hurricanes","18,547", None),
("Nationwide Arena","Columbus, Ohio","2000","Columbus Blue Jackets","18,144",
    ("Nationwide Arena", "https://www.nationwidearena.com/", "Nationwide Arena")),
("PPG Paints Arena","Pittsburgh, Pennsylvania","2010","Pittsburgh Penguins","18,387",
    ("PPG Paints Arena", "https://www.ppgpaintsarena.com/", "PPG Paints Arena")),
("Prudential Center","Newark, New Jersey","2007","New Jersey Devils","16,514",
    ("Prudential Center", "https://www.prucenter.com/", "Prudential Center")),
("SAP Center","San Jose, California","1993","San Jose Sharks","17,435",
    ("SAP Center", "https://www.sapcenter.com/", "SAP Center")),
("T-Mobile Arena","Paradise, Nevada","2016","Vegas Golden Knights","17,367",
    ("T-Mobile Arena", "https://www.t-mobilearena.com/", "T-Mobile Arena")),
("UBS Arena","Elmont, New York","2021","New York Islanders","17,255",
    ("UBS Arena", "https://ubsarena.com/", "UBS Arena")),
]
NHL_NOTES = {
 "Benchmark International Arena": ["A Benchmark International page about the arena says the premium club level is called the Benchmark International Club Level and describes an all inclusive space called The Mark. That page does not publish section numbers."],
 "Climate Pledge Arena": ["The Wikipedia NHL arena list says Climate Pledge Arena opened in 2021 and reuses the original roof of the Seattle Center Coliseum from 1962 after a reconstruction."],
 "Grand Casino Arena": ["The Wild game day page uses the name Grand Casino Arena. It mentions a few section numbers only to locate team stores. Those numbers are not a seating recommendation, so they are not repeated here."],
}
NHL_EXTRA = {
 "Benchmark International Arena": [("Benchmark International arena page", "https://www.benchmarkintl.com/arena/", "Benchmark International")],
}
for name, loc, opened, team, cap, official in NHL_ONLY:
    arena(name, loc, opened, [("nhl", team)], [("Hockey capacity listed", cap)],
          official=official, notes=NHL_NOTES.get(name), extra=NHL_EXTRA.get(name), lists=[W_NHL])

# --- Major college stadiums. Capacity and opened year from the Wikipedia FBS list. Roof is not in that table, so it is omitted. ---
COLLEGE = [
("Michigan Stadium","Ann Arbor","MI","Michigan","107,601","1927"),
("Beaver Stadium","University Park","PA","Penn State","106,572","1959"),
("Ohio Stadium","Columbus","OH","Ohio State","102,780","1922"),
("Tiger Stadium","Baton Rouge","LA","LSU","102,321","1924"),
("Neyland Stadium","Knoxville","TN","Tennessee","101,915","1921"),
("Darrell K Royal-Texas Memorial Stadium","Austin","TX","Texas","100,119","1924"),
("Saban Field at Bryant-Denny Stadium","Tuscaloosa","AL","Alabama","100,077","1929"),
("Sanford Stadium","Athens","GA","Georgia","93,033","1929"),
("Rose Bowl Stadium","Pasadena","CA","UCLA","89,702","1921"),
("Steve Spurrier-Florida Field at Ben Hill Griffin Stadium","Gainesville","FL","Florida","88,548","1930"),
("Pat Dye Field at Jordan-Hare Stadium","Auburn","AL","Auburn","88,043","1939"),
("Memorial Stadium, Tom Osborne Field","Lincoln","NE","Nebraska","85,458","1923"),
("Frank Howard Field at Clemson Memorial Stadium","Clemson","SC","Clemson","81,500","1942"),
("Gaylord Family Oklahoma Memorial Stadium","Norman","OK","Oklahoma","80,126","1923"),
("Notre Dame Stadium","Notre Dame","IN","Notre Dame","77,622","1930"),
]
for name, city, st, team, cap, opened in COLLEGE:
    # Names on the Wikipedia list use an en dash in a few titles. We store an ASCII hyphen.
    add(name.replace("\u2013", "-"), "%s, %s" % (city, ABBR[st]), opened, "",
        [("college-football", team)], [("Listed capacity", cap)], lists=[W_NCAA])

slugs = [v["slug"] for v in VENUES]
if len(slugs) != len(set(slugs)):
    from collections import Counter
    raise SystemExit("duplicate slugs " + str([k for k,c in Counter(slugs).items() if c>1]))
if len(VENUES) < 60:
    raise SystemExit("need 60 venues, have %d" % len(VENUES))
json.dump(VENUES, open(OUT, "w"), indent=2, ensure_ascii=False)
print(len(VENUES), "venues ->", OUT)
