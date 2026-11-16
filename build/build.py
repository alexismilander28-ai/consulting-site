"""Build the Carlos Milander site: python build/build.py

Writes self-contained pages into site/ (English) and site/es/ (Spanish). Every page carries its
own CSS, JS and the photo inline, because the host policy allows nothing else
(default-src 'none'; img-src data:; script-src 'unsafe-inline'). Do not edit site/*.html by hand.
"""
import base64, pathlib, re, sys, urllib.parse

# ---------------------------------------------------------------------------------------------
# CONTACT DETAILS: the ONE place to change them. The phone is a Google number and the Gmail is
# temporary. Change the values here, run this script, and every page and both languages follow.
# ---------------------------------------------------------------------------------------------
CONTACT = {
    "phone_shown": "(570) 392-9271",          # as printed on the page
    "phone_dial": "+15703929271",             # as dialed and texted
    "email": "alexis.milander28@gmail.com",   # temporary; "Alexis is my middle name" note on About
}
# The ready-written request the main button opens (a text on a phone, an email on a computer).
REQUEST = {
    "en": {"subject": "Free missed-call test",
           "body": "Hi Carlos. I would like the free missed-call test. My business phone number or website is: "},
    "es": {"subject": "Prueba gratuita de llamadas perdidas",
           "body": "Hola, Carlos. Quiero la prueba gratuita de llamadas perdidas. El teléfono o la página web de mi negocio es: "},
}
HELLO = {
    "en": {"subject": "Question for Carlos", "body": "Hi Carlos. "},
    "es": {"subject": "Pregunta para Carlos", "body": "Hola, Carlos. "},
}
# ---------------------------------------------------------------------------------------------

ROOT = pathlib.Path(__file__).resolve().parent
SITE = ROOT.parent / "site"

# page key -> (English file, Spanish file)
PAGES = {
    "home":  ("index.html", "index.html"),
    "map":   ("map.html", "mapa.html"),
    "ai":    ("ai-workers.html", "trabajadores-ia.html"),
    "about": ("about.html", "sobre-mi.html"),
    "leave": ("leave-behind.html", "hoja.html"),
}
NAV = ["map", "ai", "about"]

LANG = {
    "en": {
        "skip": "Skip to content", "nav_label": "Main",
        "map": "The Map", "ai": "AI workers", "about": "About",
        "other": "Español", "other_lang": "es", "other_label": "Español: this page in Spanish",
        "tel_label": "Call (570) 392-9271",
        "foot1": "© 2026 Carlos Milander. Wilkes-Barre area, Pennsylvania.",
        "foot2": "No cookies. No analytics. Fonts load from Google, which can see your IP address.",
        "foot_leave": "A one-page summary to print",
    },
    "es": {
        "skip": "Ir al contenido", "nav_label": "Principal",
        "map": "El Mapa", "ai": "Trabajadores de IA", "about": "Sobre mí",
        "other": "English", "other_lang": "en", "other_label": "English: esta página en inglés",
        "tel_label": "Llamar al (570) 392-9271",
        "foot1": "© 2026 Carlos Milander. Área de Wilkes-Barre, Pensilvania.",
        "foot2": "Sin cookies. Sin analítica. Las fuentes se cargan desde Google, que puede ver su dirección IP.",
        "foot_leave": "Un resumen de una página para imprimir",
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
    r, h = REQUEST[lang], HELLO[lang]
    photo = "data:image/webp;base64," + base64.b64encode((ROOT / "assets" / "headshot.webp").read_bytes()).decode()
    t = {
        "PHONE": c["phone_shown"].replace(" ", " "),
        "TEL": "tel:" + c["phone_dial"],
        "EMAIL": c["email"],
        "SMS": "sms:" + c["phone_dial"],
        # "?&body=" is the form both iOS and Android accept
        "SMS_TEST": "sms:" + c["phone_dial"] + "?&amp;body=" + q(r["body"]),
        "MAIL_TEST": "mailto:" + c["email"] + "?subject=" + q(r["subject"]) + "&amp;body=" + q(r["body"]),
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
        "<!-- Carlos Milander. BUILT FILE: do not edit by hand.",
        "     Phone and email live in ONE place: build/build.py, the CONTACT block at the top.",
        "     Change them there and run: python build/build.py -->",
        f'<html lang="{lang}">', "<head>", '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{meta['title']}</title>",
        f'<meta name="description" content="{meta["description"]}">',
        '<meta name="color-scheme" content="light">', '<meta name="referrer" content="no-referrer">',
        '<meta name="theme-color" content="#F6F3EC">', '<meta name="format-detection" content="telephone=no">',
    ]
    if meta.get("layout") == "letter":
        out.append('<meta name="robots" content="noindex">')
    out += [
        f'<link rel="alternate" hreflang="{other}" href="{other_href}">',
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
            f'<a class="name" href="{toks["HREF:home"]}"{home_cur}>Carlos Milander</a>',
            f'<nav aria-label="{L["nav_label"]}"><ul>', *nav, "</ul></nav>",
            f'<a class="tel" href="{toks["TEL"]}" aria-label="{L["tel_label"]}">{toks["PHONE"]}</a>',
            "</div></header>",
            '<main id="main">', body, "</main>",
            '<footer class="foot"><div class="wrap">',
            f'<p>{L["foot1"]} <a href="{toks["HREF:leave"]}">{L["foot_leave"]}</a></p>', f'<p>{L["foot2"]}</p>',
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
    sys.stdout.reconfigure(encoding="utf-8")
    for name, size in written:
        print(f"{size/1024:7.1f} KB  {name}")


if __name__ == "__main__":
    main()
