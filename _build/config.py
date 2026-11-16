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
CONTACT_EMAIL = "joshuaofisrael@gmail.com"
LEGAL_LINE = "© 2026 Joshua Israel Ventures LLC. All rights reserved. Which Seating is a trade name of Joshua Israel Ventures LLC, a Florida limited liability company."
