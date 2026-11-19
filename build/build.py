"""Build the CMRI Consulting site: python build/build.py

Writes self-contained pages into site/ (English) and site/es/ (Spanish). Every page carries its
own CSS, JS and the photo inline, because the host policy allows nothing else
(default-src 'none'; img-src data:; script-src 'unsafe-inline'). Do not edit site/*.html by hand.
"""
import base64, json, pathlib, re, sys, urllib.parse

# ---------------------------------------------------------------------------------------------
# CONTACT DETAILS: the ONE place to change them. The phone is a Google number. The email is the
# company mailbox. Change the values here, run this script, and every page and both languages follow.
# ---------------------------------------------------------------------------------------------
CONTACT = {
    "phone_shown": "(570) 392-9271",          # as printed on the page
    "phone_dial": "+15703929271",             # as dialed and texted
    "email": "carlos@cmriconsulting.com",     # company mailbox (Google Workspace)
}
# The ready-written request the main button opens (a text on a phone, an email on a computer).
REQUEST = {
    "en": {"subject": "Free missed-call test",
           "body": "Hi Carlos. I would like the free missed-call test. My business phone number or website is: "},
    "es": {"subject": "Prueba gratuita de llamadas perdidas",
           "body": "Hola, Carlos. Quiero la prueba gratuita de llamadas perdidas. El teléfono o la página web de mi negocio es: "},
}
# The ready-written request for the live demo (See it work page).
DEMO = {
    "en": {"subject": "Live demo on a call",
           "body": "Hi Carlos. I would like to see the working demo on a call. A good time to reach me is: "},
    "es": {"subject": "Demostración en vivo por llamada",
           "body": "Hola, Carlos. Quiero ver la demostración en una llamada. Un buen horario para llamarme es: "},
}
HELLO = {
    "en": {"subject": "Question for Carlos", "body": "Hi Carlos. "},
    "es": {"subject": "Pregunta para Carlos", "body": "Hola, Carlos. "},
}
# ---------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------
# LOCAL SEARCH: the public address of the site and the business facts the search engines read.
# Every fact here is already printed on the site (phone, email, mailing address on the privacy
# page, the towns on the Map page). Do not add a fact here that the pages do not already say.
# ---------------------------------------------------------------------------------------------
BASE = "https://cmriconsulting.com/"
BUSINESS = {
    "name": "CMRI Consulting",
    "founder": "Carlos Alexis Milander",
    "street": "20 Dundee Apartments",
    "town": "Wilkes-Barre",
    "region": "PA",
    "zip": "18706",
    # the towns the Map page names; Luzerne and Lackawanna are the counties they sit in
    "areas": ["Wilkes-Barre, PA", "Scranton, PA", "Hazleton, PA",
              "Luzerne County, PA", "Lackawanna County, PA"],
    "languages": ["en", "es"],
}

ROOT = pathlib.Path(__file__).resolve().parent
SITE = ROOT.parent / "site"

# page key -> (English file, Spanish file)
PAGES = {
    "home":  ("index.html", "index.html"),
    "map":   ("map.html", "mapa.html"),
    "ai":    ("ai-workers.html", "trabajadores-ia.html"),
    "demo":  ("see-it-work.html", "vealo-funcionar.html"),
    "recep": ("receptionist.html", "recepcionista.html"),
    "about": ("about.html", "sobre-mi.html"),
    "privacy": ("privacy.html", "privacidad.html"),
    "leave": ("leave-behind.html", "hoja.html"),
}
NAV = ["map", "ai", "demo", "about"]

LANG = {
    "en": {
        "skip": "Skip to content", "nav_label": "Main",
        "map": "The Map", "ai": "AI workers", "demo": "See it work", "about": "About",
        "other": "Español", "other_lang": "es", "other_label": "Español: this page in Spanish",
        "tel_label": "Call (570) 392-9271",
        "foot1": "© 2026 CMRI Consulting. Carlos Milander, sole proprietor. Wilkes-Barre area, Pennsylvania.",
        "foot2": "No cookies. No analytics. Fonts load from Google, which can see your IP address.",
        "foot_leave": "One-page summary to print", "foot_privacy": "Privacy", "foot_recep": "The receptionist",
        "foot_label": "More pages",
    },
    "es": {
        "skip": "Ir al contenido", "nav_label": "Principal",
        "map": "El Mapa", "ai": "Trabajadores de IA", "demo": "Véalo funcionar", "about": "Sobre mí",
        "other": "English", "other_lang": "en", "other_label": "English: esta página en inglés",
        "tel_label": "Llamar al (570) 392-9271",
        "foot1": "© 2026 CMRI Consulting. Carlos Milander, propietario único. Área de Wilkes-Barre, Pensilvania.",
        "foot2": "Sin cookies. Sin analítica. Las fuentes se cargan desde Google, que puede ver su dirección IP.",
        "foot_leave": "Resumen de una página para imprimir", "foot_privacy": "Privacidad", "foot_recep": "La recepcionista",
        "foot_label": "Más páginas",
    },
}

FONTS = ("https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,600;1,400"
         "&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap")
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' "
        "height='32' fill='%23F6F3EC'/%3E%3Cpath d='M8 10h16M8 16h16M8 22h9' stroke='%231C1A17' stroke-width='2.4'/%3E%3C/svg%3E")


def q(s):
    return urllib.parse.quote(s, safe="")


def tokens(lang):
    c = CONTACT
    r, h, dm = REQUEST[lang], HELLO[lang], DEMO[lang]
    photo = "data:image/webp;base64," + base64.b64encode((ROOT / "assets" / "headshot.webp").read_bytes()).decode()
    t = {
        "PHONE": c["phone_shown"].replace(" ", " "),
        "TEL": "tel:" + c["phone_dial"],
        "EMAIL": c["email"],
        "SMS": "sms:" + c["phone_dial"],
        # "?&body=" is the form both iOS and Android accept
        "SMS_TEST": "sms:" + c["phone_dial"] + "?&amp;body=" + q(r["body"]),
        "MAIL_TEST": "mailto:" + c["email"] + "?subject=" + q(r["subject"]) + "&amp;body=" + q(r["body"]),
        "SMS_DEMO": "sms:" + c["phone_dial"] + "?&amp;body=" + q(dm["body"]),
        "MAIL_DEMO": "mailto:" + c["email"] + "?subject=" + q(dm["subject"]) + "&amp;body=" + q(dm["body"]),
        "MAILTO": "mailto:" + c["email"] + "?subject=" + q(h["subject"]) + "&amp;body=" + q(h["body"]),
        "HEADSHOT": photo,
    }
    for key, files in PAGES.items():
        t["HREF:" + key] = files[0 if lang == "en" else 1]
    return t


def render(text, lang, toks, depth=0):
    def inc(m):
        return render((ROOT / lang / ("_" + m.group(1) + ".html")).read_text(encoding="utf-8"), lang, toks, depth + 1)
    text = re.sub(r"\{\{>\s*([\w-]+)\s*\}\}", inc, text)

    def tok(m):
        k = m.group(1)
        if k not in toks:
            raise SystemExit(f"unknown token {{{{{k}}}}} in a {lang} page")
        return toks[k]
    return re.sub(r"\{\{([A-Z_]+(?::\w+)?)\}\}", tok, text)


def url(lang, key):
    """The one public address of a page. Home pages use the folder form (/ and /es/)."""
    f = PAGES[key][0 if lang == "en" else 1]
    return BASE + ("" if lang == "en" else "es/") + ("" if f == "index.html" else f)


def schema(lang, desc):
    """LocalBusiness facts for the home page, as JSON-LD (a data block; the CSP does not run it)."""
    b = BUSINESS
    data = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": BASE + "#business",
        "name": b["name"],
        "url": url(lang, "home"),
        "description": desc,
        "telephone": CONTACT["phone_dial"],
        "email": CONTACT["email"],
        "founder": {"@type": "Person", "name": b["founder"]},
        "address": {"@type": "PostalAddress", "addressLocality": b["town"],
                    "addressRegion": b["region"], "postalCode": b["zip"], "addressCountry": "US"},
        "areaServed": [{"@type": "Place", "name": a} for a in b["areas"]],
        "knowsLanguage": b["languages"],
        "inLanguage": lang,
    }
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def page(lang, key):
    src = (ROOT / lang / (key + ".html")).read_text(encoding="utf-8")
    front, body = src.split("\n---\n", 1)
    meta = dict(line.split(": ", 1) for line in front.strip().splitlines())
    L, toks = LANG[lang], tokens(lang)
    other = "es" if lang == "en" else "en"
    other_href = ("es/" if lang == "en" else "../") + PAGES[key][0 if other == "en" else 1]
    css = (ROOT / "site.css").read_text(encoding="utf-8")
    if meta.get("layout") == "letter":
        css += "\n" + (ROOT / "letter.css").read_text(encoding="utf-8")
    js = (ROOT / "site.js").read_text(encoding="utf-8")
    body = render(body, lang, toks)
    out = [
        "<!doctype html>",
        "<!-- CMRI Consulting. BUILT FILE: do not edit by hand.",
        "     Phone and email live in ONE place: build/build.py, the CONTACT block at the top.",
        "     Change them there and run: python build/build.py -->",
        f'<html lang="{lang}">', "<head>", '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{meta['title']}</title>",
        f'<meta name="description" content="{meta["description"]}">',
        '<meta name="color-scheme" content="light dark">', '<meta name="referrer" content="no-referrer">',
        '<meta name="theme-color" content="#F6F3EC" media="(prefers-color-scheme: light)">',
        '<meta name="theme-color" content="#1A1815" media="(prefers-color-scheme: dark)">', '<meta name="format-detection" content="telephone=no">',
    ]
    if meta.get("layout") == "letter":
        out.append('<meta name="robots" content="noindex">')
        out.append(f'<link rel="alternate" hreflang="{other}" href="{other_href}">')
    else:
        out += [
            f'<link rel="canonical" href="{url(lang, key)}">',
            f'<link rel="alternate" hreflang="en" href="{url("en", key)}">',
            f'<link rel="alternate" hreflang="es" href="{url("es", key)}">',
            f'<link rel="alternate" hreflang="x-default" href="{url("en", key)}">',
        ]
    if key == "home":
        out.append(schema(lang, meta["description"]))
    out += [
        f'<link rel="icon" href="{ICON}">',
        f'<link rel="stylesheet" href="{FONTS}">',
        "<script>document.documentElement.className='js'</script>",
        "<style>", css, "</style>", "</head>", "<body>",
    ]
    if meta.get("layout") == "letter":
        out.append(body)
    else:
        nav = []
        for k in NAV:
            cur = ' aria-current="page"' if k == key else ""
            nav.append(f'<li><a href="{toks["HREF:" + k]}"{cur}>{L[k]}</a></li>')
        nav.append(f'<li><a href="{other_href}" lang="{L["other_lang"]}" hreflang="{L["other_lang"]}" '
                   f'aria-label="{L["other_label"]}">{L["other"]}</a></li>')
        home_cur = ' aria-current="page"' if key == "home" else ""
        out += [
            f'<a class="skip" href="#main">{L["skip"]}</a>',
            '<header class="top"><div class="wrap">',
            f'<a class="name" href="{toks["HREF:home"]}"{home_cur}>CMRI Consulting</a>',
            f'<nav aria-label="{L["nav_label"]}"><ul>', *nav, "</ul></nav>",
            f'<a class="tel" href="{toks["TEL"]}" aria-label="{L["tel_label"]}">{toks["PHONE"]}</a>',
            "</div></header>",
            '<main id="main">', body, "</main>",
            '<footer class="foot"><div class="wrap">',
            f'<p>{L["foot1"]}</p>',
            f'<ul class="foot-links" aria-label="{L["foot_label"]}">'
            f'<li><a href="{toks["HREF:recep"]}">{L["foot_recep"]}</a></li>'
            f'<li><a href="{toks["HREF:privacy"]}">{L["foot_privacy"]}</a></li>'
            f'<li><a href="{toks["HREF:leave"]}">{L["foot_leave"]}</a></li></ul>',
            f'<p>{L["foot2"]}</p>',
            "</div></footer>",
        ]
    out += ["<script>", js, "</script>", "</body>", "</html>", ""]
    return "\n".join(out)


def main():
    written = []
    for lang in ("en", "es"):
        for key, files in PAGES.items():
            dest = SITE / ("" if lang == "en" else "es") / files[0 if lang == "en" else 1]
            dest.parent.mkdir(parents=True, exist_ok=True)
            html = page(lang, key)
            dest.write_text(html, encoding="utf-8", newline="\n")
            written.append((dest.relative_to(SITE.parent).as_posix(), len(html.encode("utf-8"))))
    # sitemap: every indexable page in both languages, each with its language pair. The letter
    # layout (leave-behind) is noindex, so it is left out.
    letters = {k for k in PAGES if "layout: letter" in (ROOT / "en" / (k + ".html")).read_text(encoding="utf-8").split("\n---\n", 1)[0]}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for lang in ("en", "es"):
        for key in PAGES:
            if key in letters:
                continue
            sm.append(f"  <url><loc>{url(lang, key)}</loc>")
            for l2 in ("en", "es"):
                sm.append(f'    <xhtml:link rel="alternate" hreflang="{l2}" href="{url(l2, key)}"/>')
            sm.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url("en", key)}"/>')
            sm.append("  </url>")
    sm += ["</urlset>", ""]
    (SITE / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8", newline="\n")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n",
                                     encoding="utf-8", newline="\n")
    written += [("site/sitemap.xml", len("\n".join(sm))), ("site/robots.txt", 0)]
    sys.stdout.reconfigure(encoding="utf-8")
    for name, size in written:
        print(f"{size/1024:7.1f} KB  {name}")


if __name__ == "__main__":
    main()
