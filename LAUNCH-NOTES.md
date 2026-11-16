# Which Seating launch

Committed pages stay noindex. `INDEXABLE` in `_build/config.py` stays `False`. `--launch` is the switch for one build: it drops noindex (except `404.html`), adds the Cloudflare Web Analytics beacon, and adds the GA4 consent loader. Paths stay root-relative. `CNAME` stays `whichseating.com`.

`GA4_ID` in `_build/config.py` is `""` until you paste a measurement ID. The launch check fails while it is empty, and it fails if any page is missing the Cloudflare beacon or `/assets/consent.js`.

## Exact launch command

From the repo root, after `whichseating.com` answers on HTTPS:

```bash
# One line in _build/config.py. Replace with the real measurement ID. Do not commit a fake one.
# GA4_ID = "G-XXXXXXXXXX"

./deploy.sh --launch
```

That runs, in order:

```bash
python3 _build/build.py --launch
python3 _build/check.py --launch
python3 _build/legal_gate.py check
```

Pass looks like `issues 0` and `0 HOLD_REVIEW`. Then commit the generated site and push `main`. After the live pages are indexable:

```bash
./indexnow.sh
```

`indexnow.sh` refuses to run while `index.html` is still noindex. The key file `438ec3fb524a086ccf75531cb3688282.txt` is already in the repo. Sitemap, `robots.txt`, and `llms.txt` are rewritten by the build and keep `https://whichseating.com/`.

With `GA4_ID` still empty, `./deploy.sh --launch` exits 1 and `check.py` reports `empty GA4_ID`. That is the gate. Fill the one line and run the same command again.

## What the launch HTML adds

- Cloudflare beacon on every page, including `404.html`.
- `assets/consent.js` on every page. Consent Mode v2 defaults are denied. `gtag.js` loads only after Accept. Cookie settings in the footer reopens the banner.
- Privacy page names Google Analytics 4 and Cloudflare Web Analytics.

## Preview rebuild

```bash
python3 _build/build.py
python3 _build/check.py
python3 _build/legal_gate.py check
```

Preview pages stay `noindex, follow`, with no beacon and no GA4 loader.
