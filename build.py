#!/usr/bin/env python3
"""Builds the Blades of Ages site into the repository root and checks it.

    python3 build.py            # build + checks (exit 1 on an error)

Sources: data/facts.json (facts, numbers), data/site.json (settings), content/i18n/<lang>.json (all text).
Legal and help pages: src/<page>.<lang>.html (body fragments; {{CONTACT}} and {{page:<id>}} are filled in).
Outputs: index.html, <lang>/index.html, the pages in PAGES, 404.html, robots.txt, sitemap.xml, llms.txt.
The pages are static and host-independent: no server headers are assumed (CSP and referrer via <meta>), internal
links are root-relative, canonical/hreflang/OG URLs are absolute.
"""
import html, json, os, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
GAME = pathlib.Path(os.environ.get("AOB_GAME_REPO", ROOT.parent / "blades-of-ages"))
FACTS = json.loads((ROOT / "data/facts.json").read_text(encoding="utf-8"))
SITE = json.loads((ROOT / "data/site.json").read_text(encoding="utf-8"))
BASE = SITE["baseUrl"]

# code: (path prefix, html lang, hreflang, og:locale, published, latin script)
LANGS = {
    "tr": ("/", "tr", "tr", "tr_TR", True, True),
    "en": ("/en/", "en", "en", "en_US", True, True),
    "ja": ("/ja/", "ja", "ja", "ja_JP", False, False),
    "ko": ("/ko/", "ko", "ko", "ko_KR", False, False),
    "zh-Hant": ("/zh-hant/", "zh-Hant", "zh-Hant", "zh_TW", False, False),
    "de": ("/de/", "de", "de", "de_DE", False, True),
    "fr": ("/fr/", "fr", "fr", "fr_FR", False, True),
}
PUBLISHED = [c for c, v in LANGS.items() if v[4]]
X_DEFAULT = "en"
CSP = ("default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; "
       "connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'")
ROMAN = ["I", "II", "III", "IV", "V"]
SRC = ROOT / "src"

# page id: {lang: path under the language prefix}; "*" is every other language. A document page exists in a language
# only when src/<page>.<lang>.html does (kvkk is Turkish law, so it is Turkish only).
PAGES = {
    "home": {"*": ""},
    "privacy": {"tr": "gizlilik/", "*": "privacy/"},
    "kvkk": {"tr": "kvkk/"},
    "terms": {"tr": "kosullar/", "*": "terms/"},
    "delete": {"tr": "hesap-silme/", "*": "delete-account/"},
    "support": {"tr": "destek/", "*": "support/"},
}
DOCS = [p for p in PAGES if p != "home"]
FOOTER_DOCS = ["support", "privacy", "kvkk", "terms", "delete"]

errors: list[str] = []
warnings: list[str] = []


def load_i18n(lang: str) -> dict:
    return json.loads((ROOT / "content/i18n" / f"{lang}.json").read_text(encoding="utf-8"))


def esc(s: str) -> str:
    return html.escape(s, quote=True)


class T:
    """Text lookup with {placeholder} filling from facts. A missing key is a build error."""

    def __init__(self, lang: str):
        self.lang, self.d = lang, load_i18n(lang)
        names = [self.d[f"langnames.{c}"] for c in FACTS["appLanguages"]]
        self.vars = dict(FACTS["counts"], holder=SITE["copyrightHolder"],
                         appLanguages=", ".join(names))

    def __call__(self, key: str) -> str:
        if key not in self.d:
            errors.append(f"[{self.lang}] missing text key: {key}")
            return key
        return self.d[key].format(**self.vars)

    def h(self, key: str) -> str:
        return esc(self(key))


def url(lang: str, page: str = "home") -> str:
    slugs = PAGES[page]
    return LANGS[lang][0] + slugs.get(lang, slugs.get("*", ""))


def page_langs(page: str) -> list[str]:
    """Published languages this page exists in."""
    if page == "home":
        return PUBLISHED
    return [c for c in PUBLISHED if (SRC / f"{page}.{c}.html").exists()]


# ---------------------------------------------------------------- page parts

def mark_svg(cls: str = "mark") -> str:
    """The brand mark: six outward-facing blades around a gem (the app icon's ring). Decorative."""
    return f'<svg class="{cls}" viewBox="0 0 64 64" aria-hidden="true" focusable="false"><use href="/assets/mark.svg#m"/></svg>'


def head(t: T, title: str, desc: str, page: str, jsonld: dict | None, extra: str = "") -> str:
    lang = t.lang
    code = LANGS[lang]
    langs = page_langs(page)
    alts = ""
    if len(langs) > 1:
        alts = "".join(f'<link rel="alternate" hreflang="{LANGS[c][2]}" href="{BASE}{url(c, page)}">' for c in langs)
        alts += f'<link rel="alternate" hreflang="x-default" href="{BASE}{url(X_DEFAULT if X_DEFAULT in langs else langs[0], page)}">'
    fonts = ""
    if code[5]:
        fonts = ('<link rel="preload" href="/assets/fonts/baloo2-800-latin.woff2" as="font" type="font/woff2" crossorigin>'
                 '<link rel="preload" href="/assets/fonts/nunito-600-latin.woff2" as="font" type="font/woff2" crossorigin>')
    ld = ""
    if jsonld:
        ld = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False, separators=(",", ":")) + "</script>"
    og_locale_alts = "".join(f'<meta property="og:locale:alternate" content="{LANGS[c][3]}">' for c in langs if c != lang)
    return f"""<!doctype html>
<html lang="{code[1]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}{url(lang, page)}">
{alts}
<meta name="theme-color" content="#CDEBFF">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/icon-180.png">
{fonts}
<link rel="stylesheet" href="/assets/site.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{t.h('brand')}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{BASE}{url(lang, page)}">
<meta property="og:image" content="{BASE}/assets/icon-512.png">
<meta property="og:locale" content="{code[3]}">{og_locale_alts}
<meta name="twitter:card" content="summary">
{extra}{ld}
<script src="/assets/site.js" defer></script>
</head>"""


def header(t: T, page: str = "home") -> str:
    home = "" if page == "home" else url(t.lang)
    links = "".join(f'<li><a href="{home}#{a}">{t.h(k)}</a></li>' for a, k in (
        ("how", "nav.play"), ("journey", "nav.journey"), ("heroes", "nav.heroes"), ("fair", "nav.fair"), ("faq", "nav.faq")))
    langs = page_langs(page)
    others = "".join(f'<li><a href="{url(c, page if c in langs else "home")}" hreflang="{LANGS[c][2]}" lang="{LANGS[c][1]}">{esc(load_i18n(c)["lang.name"])}</a></li>'
                     for c in PUBLISHED if c != t.lang)
    return f"""<a class="skip" href="#main">{t.h('skip')}</a>
<header class="top">
  <a class="logo" href="{url(t.lang)}">{mark_svg()}<span>{t.h('brand')}</span></a>
  <nav aria-label="{t.h('nav.label')}"><ul class="nav">{links}</ul></nav>
  <details class="langs"><summary aria-label="{t.h('lang.label')}">{esc(LANGS[t.lang][2].upper())}</summary><ul>{others}</ul></details>
</header>"""


def soon_badge(t: T, cls: str = "") -> str:
    return f'<span class="soon {cls}">{mark_svg("mark mini")}{t.h("cta.soon")}</span>'


def hero(t: T) -> str:
    return f"""<section class="hero" id="top" aria-labelledby="hero-title">
  <div class="arena" data-arena>
    <canvas class="arena-canvas" aria-hidden="true"></canvas>
    <div class="arena-poster" aria-hidden="true">
      <div class="ring">{''.join('<i></i>' for _ in range(6))}</div>
      <img src="/assets/art/hero-kaya.webp" width="256" height="256" alt="" fetchpriority="high">
    </div>
    <p class="gold-pill" aria-hidden="true"><img src="/assets/art/gold-coin.webp" width="64" height="64" alt=""><b data-gold>0</b><span>{t.h('hero.gold')}</span></p>
    <button class="btn btn-ghost arena-exit" type="button" data-exit hidden>{t.h('hero.exit')}</button>
    <p class="sr-only">{t.h('hero.canvas')}</p>
  </div>
  <div class="hero-card">
    <p class="eyebrow">{t.h('hero.eyebrow')}</p>
    <h1 id="hero-title">{t.h('hero.title')}</h1>
    <p class="lead">{t.h('hero.lead')}</p>
    <div class="actions">
      <button class="btn btn-go" type="button" data-try hidden>{t.h('hero.try')}</button>
      {soon_badge(t)}
    </div>
    <p class="hint" data-hint data-pointer="{t.h('hero.hint.pointer')}" data-touch="{t.h('hero.hint.touch')}"></p>
  </div>
</section>"""


def how(t: T) -> str:
    cards = ""
    for k, cls in (("move", "wide"), ("stand", "tight"), ("parry", "parry")):
        cards += f"""<li class="card how-card">
  <div class="orbit orbit-{cls}" aria-hidden="true"><span class="core"></span>{''.join('<i></i>' for _ in range(6))}{'<b class="orb"></b>' if cls == 'parry' else ''}</div>
  <h3>{t.h(f'how.{k}.title')}</h3><p>{t.h(f'how.{k}.text')}</p></li>"""
    return f"""<section class="band" id="how" aria-labelledby="how-title">
  <h2 id="how-title">{t.h('how.title')}</h2><p class="section-lead">{t.h('how.lead')}</p>
  <ul class="grid3">{cards}</ul>
</section>"""


def era(t: T, i: int, e: dict) -> str:
    eid = e["id"]
    realms = "".join(f"<li>{t.h('realm.' + r)}</li>" for r in e["realms"])
    head_html = f"""<header class="era-head"><span class="era-num" aria-hidden="true">{ROMAN[i]}</span>
  <div><h3>{t.h(f'era.{eid}.name')}</h3><p class="period">{t.h(f'era.{eid}.period')}</p></div></header>"""
    if not e["revealed"]:
        return f"""<article class="era era-erased" aria-labelledby="{eid}-t">
  {head_html.replace('<h3>', f'<h3 id="{eid}-t">')}
  <p class="erased-note">{t.h('journey.erased')}</p>
  <div class="era-meta"><div><h4>{t.h('journey.realms')}</h4><ul class="chips chips-faded">{realms}</ul></div></div>
</article>"""
    bosses = "".join(f"<li>{t.h('boss.' + b)}</li>" for b in e["bosses"])
    figs = "".join(
        f'<img class="fig fig-{a["role"]}" src="/assets/art/{a["img"]}.webp" width="{a["w"]}" height="{a["w"]}" alt="" loading="lazy" decoding="async">'
        for a in e["art"])
    return f"""<article class="era ground-{e['ground']}" aria-labelledby="{eid}-t">
  <div class="era-stage" aria-hidden="true">{figs}</div>
  <div class="era-body card">
    {head_html.replace('<h3>', f'<h3 id="{eid}-t">')}
    <p>{t.h(f'era.{eid}.blurb')}</p>
    <div class="era-meta">
      <div><h4>{t.h('journey.realms')}</h4><ul class="chips">{realms}</ul></div>
      <div><h4>{t.h('journey.bosses')}</h4><ul class="chips chips-boss">{bosses}</ul></div>
      <div><h4>{t.h('journey.guardian')}</h4><p class="guardian">{t.h('boss.' + e['guardian'])}</p></div>
    </div>
  </div>
</article>"""


def journey(t: T) -> str:
    eras = "".join(era(t, i, e) for i, e in enumerate(FACTS["eras"]))
    return f"""<section class="journey" id="journey" aria-labelledby="journey-title">
  <div class="band"><h2 id="journey-title">{t.h('journey.title')}</h2><p class="section-lead">{t.h('journey.lead')}</p></div>
  <div class="eras">{eras}</div>
</section>"""


def heroes(t: T) -> str:
    cards = "".join(
        f'<li class="card hero-chip"><img src="/assets/art/hero-{h}.webp" width="{256 if h == "kaya" else 240}" height="{256 if h == "kaya" else 240}" alt="" loading="lazy" decoding="async"><span>{t.h("hero." + h)}</span></li>'
        for h in FACTS["heroShowcase"])
    return f"""<section class="band" id="heroes" aria-labelledby="heroes-title">
  <h2 id="heroes-title">{t.h('heroes.title')}</h2><p class="section-lead">{t.h('heroes.lead')}</p>
  <ul class="hero-strip">{cards}</ul>
</section>"""


def fair(t: T) -> str:
    cards = "".join(f'<li class="card fair-card fair-{k}"><svg class="fair-icon" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><use href="/assets/mark.svg#i-{k}"/></svg><h3>{t.h(f"fair.{k}.title")}</h3><p>{t.h(f"fair.{k}.text")}</p></li>'
                    for k in ("ads", "myth", "gore"))
    return f"""<section class="band" id="fair" aria-labelledby="fair-title">
  <h2 id="fair-title">{t.h('fair.title')}</h2>
  <ul class="grid3">{cards}</ul>
</section>"""


def faq(t: T) -> str:
    items = "".join(f'<details class="card qa"><summary><h3>{t.h(f"faq.{k}.q")}</h3></summary><p>{t.h(f"faq.{k}.a")}</p></details>'
                    for k in ("when", "devices", "price", "langs", "myth"))
    return f"""<section class="band narrow" id="faq" aria-labelledby="faq-title">
  <h2 id="faq-title">{t.h('faq.title')}</h2>{items}
</section>"""


def footer(t: T) -> str:
    langs = " · ".join(f'<a href="{url(c)}" hreflang="{LANGS[c][2]}" lang="{LANGS[c][1]}">{esc(load_i18n(c)["lang.name"])}</a>' for c in PUBLISHED)
    docs = "".join(f'<li><a href="{url(t.lang, d)}">{t.h("doc." + d)}</a></li>' for d in FOOTER_DOCS if t.lang in page_langs(d))
    return f"""<footer class="foot">
  <div class="foot-brand">{mark_svg()}<div><b>{t.h('brand')}</b><span>{t.h('brand.alt')}</span></div></div>
  {soon_badge(t, 'soon-dark')}
  <nav aria-label="{t.h('footer.docs')}"><ul class="foot-docs">{docs}</ul></nav>
  <p>{t.h('footer.dev')} · <a href="mailto:{esc(SITE['contact'])}">{t.h('footer.contact')}</a> · {langs}</p>
  <p class="fine">© {SITE['copyrightYear']} {esc(SITE['copyrightHolder'])}. {esc(SITE['trademarkLine'])}</p>
</footer>"""


def jsonld_home(t: T) -> dict:
    page = f"{BASE}{url(t.lang)}"
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": t("brand"),
         "inLanguage": LANGS[t.lang][2], "publisher": {"@id": f"{BASE}/#developer"}},
        {"@type": "Person", "@id": f"{BASE}/#developer", "name": SITE["copyrightHolder"], "url": SITE["developerUrl"]},
        {"@type": ["VideoGame", "MobileApplication"], "@id": f"{BASE}/#game", "name": t("brand"),
         "alternateName": t("brand.alt"), "description": t("hero.lead"), "url": page,
         "image": f"{BASE}/assets/icon-512.png", "operatingSystem": "iOS", "applicationCategory": "GameApplication",
         "gamePlatform": FACTS["platforms"], "inLanguage": FACTS["appLanguages"],
         "author": {"@id": f"{BASE}/#developer"}},
        {"@type": "WebPage", "@id": f"{page}#webpage", "url": page, "name": t("meta.home.title"),
         "description": t("meta.home.desc"), "inLanguage": LANGS[t.lang][2],
         "isPartOf": {"@id": f"{BASE}/#website"}, "about": {"@id": f"{BASE}/#game"}},
    ]}


def build_home(lang: str) -> str:
    t = T(lang)
    extra = '<script src="/assets/arena.js" defer></script>'
    body = "".join([header(t), '<main id="main">', hero(t), how(t), journey(t), heroes(t), fair(t), faq(t), "</main>", footer(t)])
    return head(t, t("meta.home.title"), t("meta.home.desc"), "home", jsonld_home(t), extra) + f"\n<body>\n{body}\n</body>\n</html>\n"


def doc_body(page: str, lang: str) -> str:
    """The page's hand-written body fragment with its placeholders filled; an unknown placeholder is a build error."""
    text = (SRC / f"{page}.{lang}.html").read_text(encoding="utf-8").replace("{{CONTACT}}", esc(SITE["contact"]))

    def link(m: re.Match) -> str:
        target = m.group(1)
        if target not in PAGES or lang not in page_langs(target):
            errors.append(f"src/{page}.{lang}.html: no page {target} in {lang}")
            return "#"
        return url(lang, target)

    text = re.sub(r"\{\{page:([a-z]+)\}\}", link, text)
    for left in re.findall(r"\{\{[^}]*\}\}", text):
        errors.append(f"src/{page}.{lang}.html: unknown placeholder {left}")
    return text


def build_doc(page: str, lang: str) -> str:
    t = T(lang)
    body = doc_body(page, lang)
    h1 = re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S).group(1)).strip()
    title = f"{h1} · {t('brand')}"
    page_url = f"{BASE}{url(lang, page)}"
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": f"{page_url}#webpage", "url": page_url, "name": title,
         "description": t(f"meta.{page}.desc"), "inLanguage": LANGS[lang][2],
         "isPartOf": {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": t("brand")},
         "about": {"@id": f"{BASE}/#game"}},
    ]}
    main = f'<main id="main" class="doc"><div class="doc-card card">{body}</div></main>'
    return (head(t, title, t(f"meta.{page}.desc"), page, jsonld)
            + f"\n<body>\n{header(t, page)}{main}{footer(t)}\n</body>\n</html>\n")


def build_404() -> str:
    t = T("tr")
    e = T("en")
    body = f"""<main id="main" class="lost">{mark_svg('mark big')}
  <h1>{t.h('404.title')}</h1><p>{t.h('404.text')}</p><p><a class="btn btn-go" href="/">{t.h('404.home')}</a></p>
  <p lang="en">{e.h('404.text')} <a href="/en/">{e.h('404.home')}</a></p></main>"""
    return head(t, t("meta.404.title"), t("404.text"), "home", None).replace(
        f'<link rel="canonical" href="{BASE}/">', '<meta name="robots" content="noindex">') + f"\n<body>\n{body}\n</body>\n</html>\n"


def llms_txt() -> str:
    t, c = T("en"), FACTS["counts"]
    eras = "\n".join(f"- {t('era.' + e['id'] + '.name')} ({t('era.' + e['id'] + '.period')}): "
                     + ", ".join(t('realm.' + r) for r in e["realms"]) for e in FACTS["eras"])
    pages = "\n".join(f"- [{load_i18n(l)['lang.name']}]({BASE}{url(l)})" for l in PUBLISHED)
    pages += "\n" + "\n".join(f"- [{t('doc.' + d)}]({BASE}{url('en', d)})" for d in FOOTER_DOCS if "en" in page_langs(d))
    return f"""# {t('brand')}

> {t('hero.lead')}

Status: not yet released (coming soon to the App Store). Platforms: {', '.join(FACTS['platforms'])}.
Turkish name: {t('brand.alt')}. Developer: {SITE['copyrightHolder']} ({SITE['developerUrl']}).

## Facts
- Ages: {c['eras']}; mythological realms: {c['realms']}; maps: {c['maps']} ({c['mapsPerRealm']} per realm); heroes: {c['heroes']}
- Controls: one thumb. Walking widens the blades' orbit; standing still draws them in and spins them faster.
- Monetization: free to download, optional in-app purchases, no forced ads; rewarded ads only by choice.
- Game languages: {t.vars['appLanguages']}

## Ages and realms
{eras}

## Pages
{pages}
"""


# ---------------------------------------------------------------- checks

def visible_text(doc: str) -> str:
    body = doc.split("<body>", 1)[1]
    body = re.sub(r"<script.*?</script>", " ", body, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(body))


def check_page(path: str, doc: str) -> None:
    if doc.count("<h1") != 1:
        errors.append(f"{path}: needs exactly one <h1>")
    for img in re.findall(r"<img\b[^>]*>", doc):
        if ' alt="' not in img or " width=" not in img or " height=" not in img:
            errors.append(f"{path}: <img> without alt/width/height: {img[:80]}")
    for href in re.findall(r'(?:href|src)="(/[^"#?]*)', doc):
        target = ROOT / href.lstrip("/")
        if href.endswith("/"):
            target = target / "index.html"
        if not target.exists():
            errors.append(f"{path}: broken internal link {href}")
    if 'style="' in doc:
        errors.append(f"{path}: inline style attribute (blocked by the CSP)")
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S)
    if m:
        data = json.loads(m.group(1))
        text = visible_text(doc)
        for node in data["@graph"]:
            for key in ("name", "alternateName", "description"):
                if key in node and node[key] not in text and node["@type"] != "WebPage":
                    errors.append(f"{path}: JSON-LD {key} is not visible on the page: {node[key][:60]}")
    if re.search(r"\b(first|only|best|ilk|tek|en iyi)\b", re.sub(r"<[^>]+>", " ", doc.split("<title>")[1].split("</title>")[0]), re.I):
        errors.append(f"{path}: superlative in <title>")


def check_i18n() -> None:
    ref = set(load_i18n("tr"))
    for lang in PUBLISHED:
        keys = set(load_i18n(lang))
        for k in sorted(ref - keys):
            errors.append(f"[{lang}] missing key {k}")
        for k in sorted(keys - ref):
            warnings.append(f"[{lang}] extra key {k}")


def check_game() -> None:
    """Facts and names must match the game repository (skipped with a warning when it is not checked out)."""
    data = GAME / "data"
    if not data.is_dir():
        warnings.append(f"game repo not found at {GAME}; facts not cross-checked")
        return
    load = lambda n: json.loads((data / n).read_text(encoding="utf-8"))
    eras, realms = load("eras.json")["eras"], load("realms.json")["realms"]
    bosses = {b["id"]: b for b in load("bosses.json")["bosses"]}
    heroes = {h["id"]: h for h in load("heroes.json")["heroes"]}
    en = json.loads((data / "l10n/en.json").read_text(encoding="utf-8"))
    c = FACTS["counts"]
    actual = {"eras": len(eras), "realms": len(realms), "heroes": len(heroes),
              "maps": max(r["maps"][1] for r in realms), "mapsPerRealm": load("balance.json")["mapsPerRealm"]}
    for k, v in actual.items():
        if c[k] != v:
            errors.append(f"facts.counts.{k} = {c[k]}, game says {v}")
    tr, enj = load_i18n("tr"), load_i18n("en")
    era_by_id = {e["id"]: e for e in eras}
    realm_by_id = {r["id"]: r for r in realms}
    for e in FACTS["eras"]:
        if era_by_id[e["id"]]["realms"] != e["realms"]:
            errors.append(f"{e['id']}: realms differ from the game")
        for k in ("name", "period"):
            pairs = [(tr, era_by_id[e["id"]][k]), (enj, en[f"content.eras.{e['id']}.{k}"])]
            for d, want in pairs:
                if d[f"era.{e['id']}.{k}"] != want:
                    errors.append(f"era.{e['id']}.{k} differs from the game: {want}")
        for r in e["realms"]:
            for d, want in ((tr, realm_by_id[r]["name"]), (enj, en[f"content.realms.{r}.name"])):
                if d[f"realm.{r}"] != want:
                    errors.append(f"realm.{r} differs from the game: {want}")
        for b in e["bosses"] + [e["guardian"]]:
            for d, want in ((tr, bosses[b]["name"]), (enj, en[f"content.bosses.{b}.name"])):
                if d[f"boss.{b}"] != want:
                    errors.append(f"boss.{b} differs from the game: {want}")
    for h in FACTS["heroShowcase"]:
        if h not in heroes:
            errors.append(f"heroShowcase: unknown hero {h}")


# ---------------------------------------------------------------- main

def write(rel: str, text: str) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def main() -> int:
    check_i18n()
    check_game()
    pages, entries = {}, []
    for page in PAGES:
        for lang in page_langs(page):
            rel = url(lang, page).lstrip("/") + "index.html"
            pages[rel] = build_home(lang) if page == "home" else build_doc(page, lang)
            entries.append((page, lang))
    pages["404.html"] = build_404()
    for rel, doc in pages.items():
        write(rel, doc)
    for rel, doc in pages.items():
        check_page(rel, doc)

    def sitemap_entry(page: str, lang: str) -> str:
        langs = page_langs(page)
        alts = ""
        if len(langs) > 1:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{LANGS[a][2]}" href="{BASE}{url(a, page)}"/>' for a in langs)
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{url(X_DEFAULT if X_DEFAULT in langs else langs[0], page)}"/>'
        return f"<url><loc>{BASE}{url(lang, page)}</loc>{alts}</url>"

    urls = "\n".join(sitemap_entry(p, l) for p, l in entries)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          f'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{urls}\n</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    write("llms.txt", llms_txt())
    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("ERROR:", e)
    print(f"built {len(pages)} pages ({', '.join(PUBLISHED)}); {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
