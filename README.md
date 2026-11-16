# Which Seating (whichseating.com)

Which seats to pick at major US stadiums and arenas, and which to skip. Static site for GitHub Pages (branch `main`, folder `/`, custom domain `whichseating.com`).

v1 is a preview. Every page has `<meta name="robots" content="noindex, follow">` until the domain is live.

## Build

```bash
python3 _build/gen_data.py    # refresh _build/venues.json from the cited rows
python3 _build/build.py       # preview: noindex, root-relative paths, CNAME
python3 _build/check.py
python3 _build/legal_gate.py check
```

Launch, after whichseating.com resolves:

```bash
# Flip the single index flag in _build/config.py (INDEXABLE = True), then:
python3 _build/build.py --launch
python3 _build/check.py --launch
python3 _build/legal_gate.py check
./indexnow.sh
```

`INDEXABLE` in `_build/config.py` is the only switch for the noindex tag. `--launch` overrides it for one run and also adds the Cloudflare beacon. Paths stay root-relative in both modes. Canonicals, the sitemap, robots, and llms.txt always use `https://whichseating.com/`. `datePublished` is `2026-11-16` and is not the build clock.

## What v1 contains

118 venue pages (30 NFL stadiums, 29 US MLB parks, 29 NBA arenas, 15 more NHL-only arenas, 15 major college stadiums), plus league, state, and city hubs, four guides, and the legal pages. A venue shared by two teams is one page.

Facts are the capacity, roof, year, surface, and home teams on the public lists linked from each page, plus an official URL when a check on 16 Nov 2026 got a response. Section numbers are not invented. If a source did not print a number, the page says so.

## Pages

GitHub Pages workflow: `.github/workflows/pages.yml` (deploys the site root on push to `main`). `CNAME` is `whichseating.com`. Until DNS points here, the github.io project URL will not serve these root-relative paths, and GitHub will try to send visitors to the custom domain.

## Not done until the domain is live

Buy whichseating.com, point DNS at GitHub Pages, set `INDEXABLE = True`, rebuild, confirm the certificate, submit the sitemap, run `./indexnow.sh`. The beacon token matches the shared JI Ventures Analytics token; a Cloudflare site entry for this hostname still has to be added before views record. Ads.txt is a placeholder with no seller id. The site shows no ads.
