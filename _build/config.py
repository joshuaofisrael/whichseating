# Which Seating build settings.
# SINGLE INDEX FLAG. False puts <meta name="robots" content="noindex, follow">
# on every page. Set this to True only after whichseating.com is live and you
# want the pages indexed. `python3 _build/build.py --launch` overrides it for one run.
INDEXABLE = False

# First publication of this version. Do not replace with the build clock.
# Bump MODIFIED only when a page's facts change. Never set datePublished from datetime.now().
PUBLISHED = "2026-11-16"
MODIFIED = "2026-11-16"
VERIFIED = "16 Nov 2026"

# First-publication / material-change date for pages added or refreshed after
# the 16 Nov 2026 launch batch. Used only by those pages' own datePublished /
# dateModified and sitemap lastmod, so older pages keep their own lastmod
# (no manufactured freshness).
TODAY = "2026-11-19"
VERIFIED_TODAY = "19 Nov 2026"

# 20 Nov 2026 SEO run. Pass these only on pages whose facts changed that day.
# Do not assign them as the global MODIFIED, or unchanged pages pick up a fake lastmod.
RUN_20 = "2026-11-20"
VERIFIED_20 = "20 Nov 2026"

# 21 Nov 2026 SEO run. Same rule: only pages whose facts changed.
RUN_21 = "2026-11-21"
VERIFIED_21 = "21 Nov 2026"

SITE = "whichseating.com"
BASE_URL = "https://whichseating.com/"
BRAND = "Which Seating"
INDEXNOW_KEY = "438ec3fb524a086ccf75531cb3688282"
# Shared JI Ventures Analytics 2 beacon. Launch build only. A Cloudflare site
# entry for whichseating.com still has to exist before the beacon records views.
CF_BEACON_TOKEN = "eac63f2b5dbc4539a2d95249baab6472"
# Google Analytics 4 measurement ID. Leave this empty until you paste a real
# measurement id (the G- value from the GA4 property).
# ./deploy.sh --launch fails the check while this is empty.
GA4_ID = "G-NLDQ2E1E8V"
# Google AdSense publisher id. Head script + meta only; no ad units yet.
# ads.txt uses the pub- form without the ca- prefix.
ADSENSE_PUB = "ca-pub-5681559774142917"
ADSENSE_PUB_TXT = "pub-5681559774142917"
CONTACT_EMAIL = "joshuaofisrael@gmail.com"
LEGAL_LINE = "© 2026 Joshua Israel Ventures LLC. All rights reserved. Which Seating is a trade name of Joshua Israel Ventures LLC, a Florida limited liability company."
