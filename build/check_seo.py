"""Check the local-search parts of the BUILT site: python build/check_seo.py  (exit 0 = good)

Reads site/ as it will be served, not the sources. Checks: one canonical per indexable page and it
is the page's own public address; en, es and x-default alternates on both sides; the business
facts on the home page parse as JSON and repeat only what the site already prints; sitemap lists
exactly the indexable pages; robots.txt points at the sitemap; print-only pages stay noindex and
out of the sitemap; titles are unique.
"""
import json, pathlib, re, sys
import xml.etree.ElementTree as ET

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build  # noqa: E402

SITE = build.SITE
bad = []


def need(ok, msg):
    if not ok:
        bad.append(msg)


def head(html):
    return html.split("</head>", 1)[0]


letters = {k for k in build.PAGES
           if "layout: letter" in (build.ROOT / "en" / (k + ".html")).read_text(encoding="utf-8").split("\n---\n", 1)[0]}
titles = {}
privacy_text = (SITE / "privacy.html").read_text(encoding="utf-8")

for lang in ("en", "es"):
    for key, files in build.PAGES.items():
        rel = ("" if lang == "en" else "es/") + files[0 if lang == "en" else 1]
        html = (SITE / rel).read_text(encoding="utf-8")
        h = head(html)
        t = re.search(r"<title>(.*?)</title>", h).group(1)
        need(t not in titles, f"{rel}: title repeats {titles.get(t)}")
        titles[t] = rel
        need(len(re.findall(r'<meta name="description"', h)) == 1, f"{rel}: description count")
        need(not re.search(r"\{\{[A-Z_:a-z]+\}\}", html), f"{rel}: unrendered token")
        if key in letters:
            need('content="noindex"' in h, f"{rel}: print page must be noindex")
            need('rel="canonical"' not in h, f"{rel}: print page must not have a canonical")
            continue
        can = re.findall(r'<link rel="canonical" href="([^"]+)">', h)
        need(can == [build.url(lang, key)], f"{rel}: canonical {can}")
        for l2 in ("en", "es"):
            need(f'hreflang="{l2}" href="{build.url(l2, key)}"' in h, f"{rel}: missing hreflang {l2}")
        need(f'hreflang="x-default" href="{build.url("en", key)}"' in h, f"{rel}: missing x-default")
        lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        if key == "home":
            need(len(lds) == 1 and lds[0] in h, f"{rel}: expected one JSON-LD block in <head>")
            d = json.loads(lds[0].replace("<\\/", "</"))
            need(d["telephone"] == build.CONTACT["phone_dial"], f"{rel}: phone")
            need(d["email"] == build.CONTACT["email"], f"{rel}: email")
            need(build.CONTACT["phone_shown"].replace(" ", " ") in html or build.CONTACT["phone_shown"] in html,
                 f"{rel}: phone in schema is not printed on the page")
            a = d["address"]
            printed = f'{a["addressLocality"]}, {a["addressRegion"]} {a["postalCode"]}'
            need(printed in privacy_text, f"{rel}: schema address not printed on the privacy page: {printed}")
            need(d["url"] == build.url(lang, "home"), f"{rel}: schema url")
        else:
            need(not lds, f"{rel}: JSON-LD only belongs on the home page")

# the towns named in the schema must be named on the Map page
map_text = (SITE / "map.html").read_text(encoding="utf-8")
for town in ("Wilkes-Barre", "Scranton", "Hazleton"):
    need(town in map_text, f"map.html does not name {town}, but the schema does")

ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
root = ET.parse(SITE / "sitemap.xml").getroot()
locs = [u.find("s:loc", ns).text for u in root.findall("s:url", ns)]
want = [build.url(l, k) for l in ("en", "es") for k in build.PAGES if k not in letters]
need(sorted(locs) == sorted(want), f"sitemap locs differ: {sorted(set(locs) ^ set(want))}")
for u in root.findall("s:url", ns):
    need(len(u.findall("x:link", ns)) == 3, f"sitemap: {u.find('s:loc', ns).text} needs 3 alternates")
robots = (SITE / "robots.txt").read_text(encoding="utf-8")
need(f"Sitemap: {build.BASE}sitemap.xml" in robots and "Disallow: /\n" not in robots, "robots.txt")

if bad:
    print("FAIL")
    for b in bad:
        print(" -", b)
    sys.exit(1)
print(f"OK: {len(titles)} pages, {len(locs)} sitemap urls, robots.txt points at the sitemap")
