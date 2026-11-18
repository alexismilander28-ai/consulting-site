"""comply.py <site-dir>: compliance grep + Spanish-page language check on the BUILT files."""
import re, sys, html, pathlib
site = pathlib.Path(sys.argv[1]); sys.stdout.reconfigure(encoding="utf-8")
fails = []

def visible(path):
    t = path.read_text(encoding="utf-8")
    t = re.sub(r"data:image/[a-z+]+;base64,[A-Za-z0-9+/=]+", "data:X", t)
    raw = t
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S)
    attrs = re.findall(r'(?:alt|aria-label|content|title|data-say)="([^"]*)"', body)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    title = re.findall(r"<title>(.*?)</title>", body)
    nodes = [html.unescape(x).strip() for x in re.split(r"<[^>]+>", body)]
    return raw, [n for n in nodes + attrs + title if n]

RULES = [
    ("price / currency", r"[$€£]\s?\d|\d\s?(dollars|USD|dólares)\b|\b(cheap|cheapest|barato|free quote|cotización gratis)\b"),
    ("guarantee words", r"\b(guarantee\w*|garant\w*|risk-free|sin riesgo|money back)\b"),
    ("result claims", r"\b(more jobs|más trabajos|never miss|nunca pierda|ROI|\d+\s?%|fewer no-shows|save (money|time)|ahorr\w+|boost|increase your|aumente)\b"),
    ("fix it / AI team", r"\bfix(es)? it\b|\bAI team\b|equipo de IA|AI employees|empleados de IA|that fix\b|lo arregl\w+"),
    ("fake proof", r"\b(testimonial\w*|testimonio\w*|trusted by|clients say|5[- ]star|five[- ]star|reseñas de clientes|as seen in|case stud\w+|our clients|nuestros clientes)\b"),
    ("banned names", r"\b(BERO|MCP|Multiservice|credit|crédito|dispute|disputa|Bureau|Front Desk)\b"),
    ("price word", r"\b(price\w*|pricing|precio\w*)\b"),
    ("attorney / LLC / PO box", r"\b(attorney\w*|LLC|L\.L\.C\.|P\.?\s?O\.?\s?Box|apartado postal)\b"),
    ("no-access claim", r"\bno access\b|needs no access|no necesita acceso|sin acceso a sus cuentas"),
    ("made-up wording", r"made-up|made up|inventad\w*"),
    ("old email", r"alexis\.milander28|gmail"),
    ("SMS promise", r"\bSMS\b|automated texts?\b|texts? back|texted back|mensaje de texto autom\w+|contesta\w* con un mensaje de texto|contestadas por mensaje"),
    ("we / our team", r"\b(our team|we deliver|nuestro equipo)\b"),
    ("placeholders", r"\[(?!DEMO\])[A-Z ]{3,}\]|TODO|lorem|\{\{"),
    ("slop words", r"\b(seamless|effortless|unlock|elevate|streamline|empower|leverage|transform\w*|cutting-edge|tailored|solutions|soluciones|de vanguardia|potenci\w+)\b"),
    ("dash joiners", r"[—–]"),
    ("straight quotes in text", r"\w'\w|\"\w"),
]
RAW_RULES = [
    ("external url", r"https?://(?!fonts\.googleapis\.com|fonts\.gstatic\.com|www\.w3\.org/2000/svg)[^\s\"')]+"),
    ("img not data:", r"<img(?![^>]*src=\"data:)[^>]*>"),
    ("iframe / script src / storage / cookie", r"<iframe|<script[^>]+src=|localStorage|sessionStorage|document\.cookie|<form|<video|<audio"),
    ("inline event handler", r"\son(click|load|error)="),
]
pages = sorted(site.rglob("*.html"))
en_nodes = set()
for p in pages:
    raw, nodes = visible(p)
    rel = p.relative_to(site).as_posix()
    if not rel.startswith("es/"): en_nodes |= set(nodes)
    text = "\n".join(nodes)
    for name, rx in RULES:
        for m in re.finditer(rx, text, flags=re.I if name not in ("banned names", "placeholders") else 0):
            ctx = text[max(0, m.start()-30):m.end()+30].replace("\n", " | ")
            fails.append(f"{rel}: {name}: ...{ctx}...")
    for name, rx in RAW_RULES:
        for m in re.finditer(rx, raw):
            fails.append(f"{rel}: {name}: {m.group(0)[:90]}")
    # required disclosures
    W_EN = "working demo built around a sample shop; I run it live on a call"
    W_ES = "demostración que funciona, armada alrededor de un negocio de muestra; la pongo a funcionar en vivo en una llamada"
    need = {"index.html": [W_EN, "None runs for a customer yet", "AI Supervisor", "I train them"],
            "ai-workers.html": [W_EN, "None is running for a customer yet", "not offered yet", "AI Supervisor", "email only", "automated", "Sample"],
            "see-it-work.html": [W_EN, "None of this runs for a customer yet", "This is an automated message", "Sample numbers, not results"],
            "receptionist.html": ["The phone receptionist is not offered yet", W_EN, "automated", "Sample"],
            "privacy.html": ["CMRI Consulting", "sole proprietor", "No cookies"],
            "map.html": ["sample", "not results", "written permission", "read-only"],
            "about.html": ["sole proprietor", "read-only"],
            "leave-behind.html": [W_EN, "AI Supervisor"],
            "es/index.html": [W_ES, "Ninguno funciona todavía para un cliente", "Supervisor de IA", "Yo la entreno"],
            "es/trabajadores-ia.html": [W_ES, "Ninguno funciona todavía para un cliente", "todavía no se ofrece", "Supervisor de IA", "solo correos", "automático", "Muestra"],
            "es/vealo-funcionar.html": [W_ES, "Nada de esto funciona todavía para un cliente", "Este es un mensaje automático", "Números de muestra, no son resultados"],
            "es/recepcionista.html": ["La recepcionista por teléfono todavía no se ofrece", W_ES, "automático", "Muestra"],
            "es/privacidad.html": ["CMRI Consulting", "propietario único", "Sin cookies"],
            "es/mapa.html": ["de muestra", "No son resultados", "permiso por escrito", "solo para leer"],
            "es/sobre-mi.html": ["propietario único", "solo para leer"],
            "es/hoja.html": [W_ES, "Supervisor de IA"]}
    for s in need.get(rel, []):
        if s not in text: fails.append(f"{rel}: missing disclosure '{s}'")

ALLOW = re.compile(r"^(Carlos Milander|CMRI Consulting|English|Español|STOP|Sample HVAC Co\.?|Dana.*|dana@example\.com|light dark|#1A1815|Wilkes-Barre.*|[\W\d_]+|.*@cmriconsulting\.com|\(?\d[\d\s()\-:.apm]*|C|data:X|width=device-width, initial-scale=1|light|no-referrer|#F6F3EC|telephone=no|noindex|Scranton|Hazleton|Allentown)$")
ENGLISH = re.compile(r"\b(the|and|your|with|you|shop|call|quote|sample|page|free|test|report|made-up|workers|about)\b", re.I)
for p in pages:
    rel = p.relative_to(site).as_posix()
    if not rel.startswith("es/"): continue
    _, nodes = visible(p)
    for n in nodes:
        if ALLOW.match(n): continue
        if n in en_nodes: fails.append(f"{rel}: same string as the English page: '{n[:70]}'")
        elif ENGLISH.search(n) and not re.search(r"Sample HVAC|English", n): fails.append(f"{rel}: English word in: '{n[:80]}'")

print(f"{len(pages)} pages checked")
print("COMPLIANCE OK" if not fails else "HITS:")
for f in fails: print(" -", f)
sys.exit(1 if fails else 0)
