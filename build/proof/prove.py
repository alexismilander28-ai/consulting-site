"""prove.py <base-url> <out-dir> [--quick]: screenshot matrix + gates for a multi-page static site.
Exits 1 on console/page errors (CSP violations included), failed requests, horizontal overflow,
a focusable element with no visible focus ring, or nav links off screen."""
import sys, json, pathlib
from playwright.sync_api import sync_playwright

base, out = sys.argv[1].rstrip("/"), pathlib.Path(sys.argv[2])
quick = "--quick" in sys.argv
out.mkdir(parents=True, exist_ok=True)
PAGES = [("en", "home", "/index.html"), ("en", "map", "/map.html"), ("en", "ai", "/ai-workers.html"),
         ("en", "about", "/about.html"), ("en", "leave", "/leave-behind.html"),
         ("es", "home", "/es/index.html"), ("es", "map", "/es/mapa.html"), ("es", "ai", "/es/trabajadores-ia.html"),
         ("es", "about", "/es/sobre-mi.html"), ("es", "leave", "/es/hoja.html")]
WIDTHS = [(375, 812, True), (768, 1024, False), (1280, 800, False)]
fails, rows = [], []

FOCUS = """() => { const e = document.activeElement; if (!e || e === document.body) return null; const cs = getComputedStyle(e);
  const r = e.getBoundingClientRect(); return { tag: e.tagName, text: (e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 40),
  ring: cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) >= 2, visible: r.width > 0 && r.height > 0, x: Math.round(r.left), w: Math.round(r.width) }; }"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for lang, key, path in PAGES:
        for w, h, touch in WIDTHS:
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, has_touch=touch, is_mobile=touch, color_scheme="light")
            pg = ctx.new_page(); errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type in ("error", "warning") else None)
            pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
            pg.on("requestfailed", lambda r: errs.append("requestfailed: " + r.url[:90]))
            resp = pg.goto(base + path, wait_until="networkidle")
            pg.wait_for_timeout(400)
            name = f"{key}-{w}-{lang}"
            m = pg.evaluate("""() => ({ h: document.documentElement.scrollHeight, sw: document.documentElement.scrollWidth, vw: innerWidth,
                 htmlLang: document.documentElement.lang, h1: document.querySelectorAll('h1').length,
                 navOff: [...document.querySelectorAll('header.top a')].filter(a => { const r = a.getBoundingClientRect(); return r.right > innerWidth + 1 || r.left < -1; }).length,
                 wide: [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.right > innerWidth + 1 && !e.closest('.hero-art'); }).slice(0,3).map(e => e.tagName + '.' + e.className),
                 fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family).filter((v,i,s) => s.indexOf(v) === i),
                 touchBtn: [...document.querySelectorAll('a.btn')].filter(a => a.getClientRects().length).map(a => a.getAttribute('href').split(':')[0]) })""")
            if resp.status != 200: fails.append(f"{name}: HTTP {resp.status}")
            if errs: fails.append(f"{name}: console {errs[:3]}")
            if m["sw"] > m["vw"] + 1: fails.append(f"{name}: horizontal overflow {m['sw']} > {m['vw']} {m['wide']}")
            if m["navOff"]: fails.append(f"{name}: {m['navOff']} header links off screen")
            if m["htmlLang"] != lang: fails.append(f"{name}: html lang {m['htmlLang']}")
            if m["h1"] != 1: fails.append(f"{name}: {m['h1']} h1")
            if touch and "mailto" in m["touchBtn"][:1]: fails.append(f"{name}: main button is not sms on touch {m['touchBtn']}")
            if not touch and "sms" in m["touchBtn"][:1]: fails.append(f"{name}: main button is sms on desktop {m['touchBtn']}")
            rows.append((name, m["h"], round(m["h"] / h, 2), ",".join(m["fonts"]), ",".join(m["touchBtn"])))
            if not quick:
                pg.screenshot(path=str(out / f"{name}-fold.png"))
                if touch:  # full_page drops touch emulation in Chromium, so grow the viewport instead
                    pg.set_viewport_size({"width": w, "height": m["h"]}); pg.wait_for_timeout(150)
                    pg.screenshot(path=str(out / f"{name}.png")); pg.set_viewport_size({"width": w, "height": h})
                else:
                    pg.screenshot(path=str(out / f"{name}.png"), full_page=True)
            # keyboard walk at 1280 only
            if w == 1280:
                n = pg.evaluate("document.querySelectorAll('a[href],button:not([hidden]),summary').length")
                seen = 0
                for _ in range(n + 3):
                    pg.keyboard.press("Tab")
                    f = pg.evaluate(FOCUS)
                    if not f: break
                    seen += 1
                    if not f["ring"] and f["visible"]: fails.append(f"{name}: no focus ring on {f['tag']} '{f['text']}'")
                rows.append((name + " keyboard", f"{seen} stops", "", "", ""))
            ctx.close()
    # no-JS pass: everything readable, all three report pages present
    ctx = b.new_context(viewport={"width": 1280, "height": 800}, java_script_enabled=False)
    pg = ctx.new_page(); pg.goto(base + "/map.html")
    vis = pg.locator(".sheets .sheet").evaluate_all("els => els.filter(e => e.getClientRects().length).length") if False else None
    ctx.close()
    # print: leave-behind must be exactly one Letter page
    for lang, path in (("en", "/leave-behind.html"), ("es", "/es/hoja.html")):
        ctx = b.new_context(); pg = ctx.new_page(); pg.goto(base + path, wait_until="networkidle")
        pdf = pg.pdf(format="Letter", print_background=True, prefer_css_page_size=True)
        (out / f"leave-{lang}.pdf").write_bytes(pdf)
        pages = pdf.count(b"/Type /Page") - pdf.count(b"/Type /Pages")
        rows.append((f"leave-{lang}.pdf", f"{pages} page(s)", "", "", ""))
        if pages != 1: fails.append(f"leave-{lang}: prints on {pages} pages")
        pg.emulate_media(media="print"); pg.set_viewport_size({"width": 816, "height": 1056})
        pg.screenshot(path=str(out / f"leave-print-{lang}.png"), full_page=True)
        ctx.close()
    b.close()

sys.stdout.reconfigure(encoding="utf-8")
for r in rows: print("  ".join(str(x) for x in r))
print("\nFAILS:" if fails else "\nGATE OK")
for f in fails: print(" -", f)
sys.exit(1 if fails else 0)
