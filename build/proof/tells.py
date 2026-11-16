"""tells.py: measure the site-wow-factor AI-tells check on a rendered page.

  python tells.py <url> --accent "#1d3f9c" [--out tells.json] [--shots DIR --name before]

Measures at 1280x800 and 375x812. Heuristic counts; every line prints the measured value.
Lines that cannot be measured by machine print NOT MEASURED (judge those from the screenshot).
"""
import argparse, json, sys, re, pathlib
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("url")
ap.add_argument("--accent", default="")
ap.add_argument("--out", default="")
ap.add_argument("--shots", default="")
ap.add_argument("--name", default="page")
a = ap.parse_args()

JS = r"""
(accentHex) => {
  const vw = innerWidth, vh = innerHeight;
  const vis = el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && el.getClientRects().length > 0; };
  const inFold = el => { const r = el.getBoundingClientRect(); return vis(el) && r.top < vh && r.bottom > 0 && r.left < vw && r.right > 0; };
  const all = [...document.body.querySelectorAll('*')].filter(vis);
  const out = {};
  const _cv = document.createElement('canvas'); _cv.width = _cv.height = 1; const _cx = _cv.getContext('2d', { willReadFrequently: true }); const _cache = {};
  const rgb = s => { if (!s) return null; if (_cache[s]) return _cache[s]; _cx.clearRect(0,0,1,1); _cx.fillStyle = '#000'; _cx.fillStyle = s; _cx.fillRect(0,0,1,1); const d = _cx.getImageData(0,0,1,1).data; const r = d[3] === 0 ? [0,0,0,0] : [Math.round(d[0]*255/d[3]), Math.round(d[1]*255/d[3]), Math.round(d[2]*255/d[3]), d[3]/255]; return (_cache[s] = r); };
  const lum = c => { const f = v => { v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4); }; return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2]); };
  const bgOf = el => { let e = el; while (e) { const c = rgb(getComputedStyle(e).backgroundColor); if (c && (c.length<4 || c[3] > 0.5)) return c; e = e.parentElement; } return [255,255,255]; };
  const contrast = el => { const cs = getComputedStyle(el); let c = rgb(cs.color); if(!c) return null; const b = bgOf(el); const l1 = lum(c), l2 = lum(b); return (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05); };
  const ownText = el => [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
  const foldText = all.filter(inFold).map(ownText).filter(Boolean).join(' \n ');
  const pageText = all.map(ownText).filter(Boolean).join(' \n ');

  // A1 raster images in the fold
  const imgs = [...document.images].filter(inFold).filter(i => !/^data:image\/svg/.test(i.currentSrc || i.src));
  out.A1 = imgs.length;
  // A2 svg illustrations in fold (bigger than an icon), and is one the largest media element
  const svgs = [...document.querySelectorAll('svg')].filter(inFold).filter(s => { const r = s.getBoundingClientRect(); return r.width > 72 && r.height > 72; });
  const area = e => { const r = e.getBoundingClientRect(); return r.width*r.height; };
  const maxSvg = Math.max(0, ...svgs.map(area)), maxImg = Math.max(0, ...imgs.map(area));
  out.A2 = { svgIllustrations: svgs.length, svgIsLargestMedia: maxSvg > 0 && maxSvg > maxImg, maxSvgArea: Math.round(maxSvg), maxImgArea: Math.round(maxImg) };
  // A3 name and place
  out.A3 = { name: /Carlos Milander/.test(foldText), place: (foldText.match(/Wilkes-Barre|Scranton|Hazleton|Allentown|Pennsylvania|Pensilvania|\bPA\b/g) || []).filter((v,i,s)=>s.indexOf(v)===i) };
  // A4 phone or email as plain text in fold
  out.A4 = { phone: /\(570\)\s?392-9271/.test(foldText), email: /@gmail\.com/.test(foldText) };
  // A5 headline one voice
  const h1 = [...document.querySelectorAll('h1,[aria-level="1"]')].filter(vis)[0];
  if (h1) { const cs = getComputedStyle(h1); const kids = [...h1.querySelectorAll('*')].filter(vis).filter(k => { const k2 = getComputedStyle(k); return k2.fontWeight !== cs.fontWeight || k2.fontStyle !== cs.fontStyle || k2.color !== cs.color; });
    out.A5 = { text: h1.innerText.slice(0,120), mixedChildren: kids.length, sizePx: parseFloat(cs.fontSize), weight: cs.fontWeight }; } else out.A5 = null;
  // A6 filled buttons in fold
  const pressables = [...document.querySelectorAll('a,button,summary,[role=button],[role=tab]')].filter(vis);
  const filled = pressables.filter(inFold).filter(p => { const cs = getComputedStyle(p); const b = rgb(cs.backgroundColor); if (!b || (b.length === 4 && b[3] < 0.5)) return false; const r = p.getBoundingClientRect(); if (r.height < 28 || !p.innerText.trim()) return false; const pb = bgOf(p.parentElement); const d = Math.abs(lum(b) - lum(pb)); return d > 0.25; });
  out.A6 = { count: filled.length, labels: filled.map(f => f.innerText.trim().slice(0,40)) };
  // A7 nav
  const nav = [...document.querySelectorAll('header nav, nav')].filter(vis)[0];
  if (nav) { const links = [...nav.querySelectorAll('a,[role=tab]')].filter(vis); let scroller = nav; let sideways = false; let e = nav; for (let i=0;i<3&&e;i++){ if (e.scrollWidth > e.clientWidth + 2) sideways = true; e = e.firstElementChild; }
    const off = links.filter(l => { const r = l.getBoundingClientRect(); return r.right > vw + 1 || r.left < -1; }).length;
    out.A7 = { links: links.length, sidewaysScroll: sideways, linksOffScreen: off, labels: links.map(l=>l.innerText.trim()) }; } else out.A7 = null;
  // A8 header toggles
  const header = document.querySelector('header');
  out.A8 = header ? [...header.querySelectorAll('button,[role=switch],input[type=checkbox]')].filter(vis).length : 0;

  // B1/B2 card groups: siblings sharing a class, each boxed (border, background or shadow) and holding text
  const boxed = el => { const cs = getComputedStyle(el); const b = rgb(cs.backgroundColor); const hasBg = b && (b.length < 4 || b[3] > 0.05) && JSON.stringify(b.slice(0,3)) !== JSON.stringify(bgOf(el.parentElement).slice(0,3)); const hasBorder = ['Top','Left'].every(s => parseFloat(cs['border'+s+'Width']) > 0 && cs['border'+s+'Style'] !== 'none'); return hasBg || hasBorder || cs.boxShadow !== 'none'; };
  const groups = [];
  for (const p of all) { const kids = [...p.children].filter(vis); if (kids.length < 2) continue; const by = {};
    for (const k of kids) { const key = k.tagName + '.' + (k.className && k.className.baseVal === undefined ? String(k.className).split(/\s+/)[0] : ''); (by[key] = by[key] || []).push(k); }
    for (const key in by) { const g = by[key]; if (g.length >= 2 && g.every(k => boxed(k) || (k.children.length === 1 && boxed(k.children[0]))) && g.every(k => k.innerText && k.innerText.trim().length > 12) && g.every(k => { const r = k.getBoundingClientRect(); return r.width > 120 && r.height > 60; })) groups.push({ key, n: g.length }); } }
  out.B1 = Math.max(0, ...groups.map(g => g.n));
  out.B2 = { gridsOf3plus: groups.filter(g => g.n >= 3).length, groups: groups.slice(0,12) };
  // B4 equal two-column grids
  let equal = 0, twoCol = 0; for (const el of all) { const cs = getComputedStyle(el); if (cs.display.includes('grid')) { const t = cs.gridTemplateColumns.split(' ').map(parseFloat).filter(n => !isNaN(n)); if (t.length === 2 && el.getBoundingClientRect().width > 500) { twoCol++; if (Math.abs(t[0]-t[1]) < 4) equal++; } } }
  out.B4 = { twoColumnGrids: twoCol, exactly5050: equal };
  // B5 centred text blocks
  out.B5 = all.filter(el => /^(P|H1|H2|H3|LI|FIGCAPTION|DIV|SPAN)$/.test(el.tagName) && ownText(el).length > 24 && getComputedStyle(el).textAlign === 'center' && !el.closest('a,button')).length;
  // B6 radii and shadows
  const radii = {}, shadows = {};
  for (const el of all) { const cs = getComputedStyle(el); const r = cs.borderTopLeftRadius; const hasBox = boxed(el) || el.tagName === 'IMG';
    if (hasBox && r && r !== '0px') { const px = parseFloat(r); const rr = el.getBoundingClientRect(); const pill = r.includes('%') || px >= Math.min(rr.width, rr.height)/2 - 1; if (!pill) radii[r] = (radii[r]||0)+1; }
    if (cs.boxShadow && cs.boxShadow !== 'none') shadows[cs.boxShadow] = (shadows[cs.boxShadow]||0)+1; }
  out.B6 = { radii, shadowCount: Object.keys(shadows).length, radiusCount: Object.keys(radii).length };
  // B7 icon tiles
  out.B7 = [...document.querySelectorAll('svg')].filter(vis).filter(s => { const p = s.parentElement; const cs = getComputedStyle(p); const r = p.getBoundingClientRect(); const b = rgb(cs.backgroundColor); return r.width <= 72 && r.height <= 72 && r.width >= 28 && Math.abs(r.width - r.height) < 6 && b && (b.length < 4 || b[3] > 0.05) && parseFloat(cs.borderTopLeftRadius) > 0 && !p.closest('a.btn,button'); }).length;

  // C1 body size + chars per line of the longest paragraphs
  const ps = [...document.querySelectorAll('main p, p')].filter(vis).filter(p => p.innerText.length > 90);
  const cpl = ps.map(p => { const cs = getComputedStyle(p); const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize)*1.5; const lines = Math.max(1, Math.round(p.getBoundingClientRect().height / lh)); return { fs: parseFloat(cs.fontSize), cpl: Math.round(p.innerText.length / lines), lines }; }).filter(x => x.lines >= 2);
  const med = arr => { const s = [...arr].sort((x,y)=>x-y); return s.length ? s[Math.floor(s.length/2)] : null; };
  out.C1 = { bodyPx: med(cpl.map(x=>x.fs)) || parseFloat(getComputedStyle(document.body).fontSize), medianCharsPerLine: med(cpl.map(x=>x.cpl)), maxCharsPerLine: Math.max(0,...cpl.map(x=>x.cpl)), paragraphs: cpl.length };
  out.C2 = out.A5 ? +(out.A5.sizePx / out.C1.bodyPx).toFixed(2) : null;
  // C3 uppercase or tracked labels
  const caps = all.filter(el => ownText(el).length > 2 && (getComputedStyle(el).textTransform === 'uppercase' || (parseFloat(getComputedStyle(el).letterSpacing) / parseFloat(getComputedStyle(el).fontSize)) >= 0.06));
  out.C3 = { count: caps.length, samples: caps.slice(0,6).map(e => ownText(e).slice(0,30)) };
  // C4 accent on non-pressables
  if (accentHex) { const t = accentHex.replace('#',''); const ac = [0,2,4].map(i => parseInt(t.substr(i,2),16)); const near = c => c && Math.abs(c[0]-ac[0]) + Math.abs(c[1]-ac[1]) + Math.abs(c[2]-ac[2]) < 40 && (c.length < 4 || c[3] > 0.5);
    const hits = all.filter(el => { const cs = getComputedStyle(el); const usesText = ownText(el).length > 0 && near(rgb(cs.color)); const usesBg = near(rgb(cs.backgroundColor)); return (usesText || usesBg) && !el.closest('a,button,summary,label,[role=tab],[role=button]'); });
    let accArea = 0; for (const el of all.filter(inFold)) { const cs = getComputedStyle(el); if (near(rgb(cs.backgroundColor))) { const r = el.getBoundingClientRect(); accArea += Math.max(0, Math.min(r.right,vw)-Math.max(r.left,0)) * Math.max(0, Math.min(r.bottom,vh)-Math.max(r.top,0)); } }
    out.C4 = { nonPressableAccent: hits.length, samples: hits.slice(0,6).map(e => e.tagName + ':' + (ownText(e) || e.className).toString().slice(0,30)), accentFillPctOfFold: +(100*accArea/(vw*vh)).toFixed(1) }; } else out.C4 = 'NOT MEASURED (no accent given)';
  // C5 gradient text, glows, gradient washes
  let clipText = 0, glow = 0, grad = 0; for (const el of all) { const cs = getComputedStyle(el); if ((cs.webkitBackgroundClip || cs.backgroundClip) === 'text') clipText++; if (/gradient/.test(cs.backgroundImage) && el.getBoundingClientRect().width > vw*0.6 && el.getBoundingClientRect().height > 200) grad++;
    const m = cs.boxShadow !== 'none' && cs.boxShadow.match(/rgba?\(([^)]+)\)\s+(-?[\d.]+)px\s+(-?[\d.]+)px\s+([\d.]+)px/); if (m) { const c = m[1].split(',').map(parseFloat); const sat = Math.max(c[0],c[1],c[2]) - Math.min(c[0],c[1],c[2]); if (parseFloat(m[4]) > 20 && sat > 60) glow++; } }
  out.C5 = { gradientText: clipText, colouredGlow: glow, gradientWash: grad };
  // C6 contrast
  const texts = all.filter(el => ownText(el).length > 1 && !el.closest('svg'));
  const cr = texts.map(el => ({ c: contrast(el), t: ownText(el).slice(0,30), fs: parseFloat(getComputedStyle(el).fontSize) })).filter(x => x.c);
  const bodyP = ps[0] ? contrast(ps[0]) : null; const low = cr.sort((x,y)=>x.c-y.c)[0];
  out.C6 = { bodyContrast: bodyP && +bodyP.toFixed(2), lowest: low && { ratio: +low.c.toFixed(2), text: low.t, px: low.fs }, below45: cr.filter(x => x.c < 4.5).length };
  // C7 straight quotes
  const sq = pageText.match(/["']/g) || []; out.C7 = { straightQuotes: sq.length, sample: (pageText.match(/.{0,18}["'].{0,18}/) || [''])[0] };
  // D1 triads
  const lists = [...document.querySelectorAll('ul,ol')].filter(vis).filter(l => !l.closest('nav,header,footer')).map(l => [...l.children].filter(vis)).filter(k => k.length === 3 && k.every(li => li.innerText.trim().length < 90));
  out.D1 = { listsOfExactlyThree: lists.length, samples: lists.slice(0,4).map(k => k.map(li => li.innerText.trim().slice(0,24)).join(' | ')) };
  // D2 local names and first person
  const names = (pageText.match(/Wilkes-Barre|Scranton|Hazleton|Allentown|HVAC|plumb\w*|plomer\w*|dental|dentista|auto(?:motriz)? repair|taller|contractor|contratista|barber\w*/gi) || []).map(s=>s.toLowerCase()).filter((v,i,s)=>s.indexOf(v)===i);
  const sent = foldText.split(/(?<=[.!?])\s+|\n/).filter(s => /(^|\s)(I|I’m|I'm|I’ll|I'll|Yo|Soy|Voy|Trabajo|Atiendo|Me comunico)\s/.test(s));
  out.D2 = { names, firstPersonSentencesInFold: sent.length };
  out.docHeight = document.documentElement.scrollHeight; out.overflowX = document.documentElement.scrollWidth > vw + 1;
  return out;
}
"""

res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in ((1280, 800), (375, 812)):
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, color_scheme="light")
        pg = ctx.new_page()
        pg.goto(a.url, wait_until="networkidle")
        pg.wait_for_timeout(600)
        res[str(w)] = pg.evaluate(JS, a.accent)
        if a.shots:
            d = pathlib.Path(a.shots); d.mkdir(parents=True, exist_ok=True)
            pg.screenshot(path=str(d / f"{a.name}-{w}-fold.png"))
            pg.screenshot(path=str(d / f"{a.name}-{w}-full.png"), full_page=True)
        ctx.close()
    b.close()

if a.out:
    pathlib.Path(a.out).write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps(res, indent=1, ensure_ascii=False))
