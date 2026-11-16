#!/bin/bash
# Ping IndexNow with every sitemap URL, or the URLs given.
# Refuses to run while pages are still noindex. Use only after whichseating.com is live.
set -e
cd "$(dirname "$0")"
if grep -q 'content="noindex' index.html; then
  echo "Refusing IndexNow: pages are still noindex. Set INDEXABLE in _build/config.py, rebuild, and deploy first."
  exit 1
fi
KEY=438ec3fb524a086ccf75531cb3688282
if [ $# -gt 0 ]; then URLS=$(printf '"%s",' "$@"); else URLS=$(grep -o '<loc>[^<]*' sitemap.xml | sed 's/<loc>//' | sed 's/.*/"&"/' | paste -sd, -); fi
curl -s -o /dev/null -w "IndexNow HTTP %{http_code}\n" -H "Content-Type: application/json; charset=utf-8" https://api.indexnow.org/indexnow \
  -d "{\"host\":\"whichseating.com\",\"key\":\"$KEY\",\"keyLocation\":\"https://whichseating.com/$KEY.txt\",\"urlList\":[${URLS%,}]}"
