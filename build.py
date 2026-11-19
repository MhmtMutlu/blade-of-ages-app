#!/usr/bin/env python3
"""Builds the Blade of Ages: Çağların Kılıcı site into the repository root and checks it.

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
    "ja": ("/ja/", "ja", "ja", "ja_JP", True, False),
    "ko": ("/ko/", "ko", "ko", "ko_KR", True, False),
    "zh-Hant": ("/zh-hant/", "zh-Hant", "zh-Hant", "zh_TW", True, False),
    "de": ("/de/", "de", "de", "de_DE", True, True),
    "fr": ("/fr/", "fr", "fr", "fr_FR", True, True),
}
PUBLISHED = [c for c, v in LANGS.items() if v[4]]
X_DEFAULT = "en"
CSP = ("default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; "
       "connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'")
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
GAMEDATA = json.loads((ROOT / "data/game.json").read_text(encoding="utf-8"))
REALMS = {r["id"]: r for r in GAMEDATA["realms"]}
PAGES["realms"] = {"tr": "diyarlar/", "*": "realms/"}
PAGES["press"] = {"tr": "basin/", "*": "press/"}
PAGES["heroes"] = {"tr": "kahramanlar/", "*": "heroes/"}
PAGES["story"] = {"tr": "hikaye/", "*": "story/"}
for _rid in FACTS["realmsLive"]:
    PAGES[f"realm:{_rid}"] = {"tr": f"diyarlar/{_rid}/", "*": f"realms/{FACTS['realmSlugs'][_rid]}/"}
GENERATED = {"home", "realms", "press", "heroes", "story"} | {f"realm:{r}" for r in FACTS["realmsLive"]}
# Sources for the heroes' "in myth and history" line: {hero: [{title, url}]}, language-neutral.
HERO_SOURCES = json.loads((ROOT / "content/hero-sources.json").read_text(encoding="utf-8"))
FOOTER_DOCS = ["support", "press", "privacy", "kvkk", "terms", "delete"]
SHOTS_LANG = "tr"  # the in-game screenshots (scripts/shots.py) are captured with the Turkish interface

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
                         appLanguages={"ja": "、", "zh-Hant": "、"}.get(lang, ", ").join(names))

    def __call__(self, key: str, **extra) -> str:
        if key not in self.d:
            errors.append(f"[{self.lang}] missing text key: {key}")
            return key
        return self.d[key].format(**self.vars, **extra)

    def h(self, key: str, **extra) -> str:
        return esc(self(key, **extra))


def url(lang: str, page: str = "home") -> str:
    slugs = PAGES[page]
    return LANGS[lang][0] + slugs.get(lang, slugs.get("*", ""))


def page_langs(page: str) -> list[str]:
    """Published languages this page exists in."""
    if page in GENERATED:
        return PUBLISHED
    return [c for c in PUBLISHED if (SRC / f"{page}.{c}.html").exists()]


# ---------------------------------------------------------------- page parts

def mark_svg(cls: str = "mark") -> str:
    """The brand mark: six outward-facing blades around a gem (the app icon's ring). Decorative."""
    return f'<svg class="{cls}" viewBox="0 0 64 64" aria-hidden="true" focusable="false"><use href="/assets/mark.svg#m"/></svg>'


def brand_parts(t: T) -> tuple[str, str]:
    """The one name, split for the two-line lockup: ("Blade of Ages", "Çağların Kılıcı")."""
    short, sub = t("brand").split(": ", 1)
    return short, sub


def og_image(lang: str, page: str) -> str:
    """The page's share card (scripts/og.py): a realm's own card, else the home card in the page's language."""
    name = f"og-{page.split(':', 1)[1]}-{lang}.jpg" if page.startswith("realm:") else f"og-{lang}.jpg"
    return f"/assets/og/{name}" if (ROOT / "assets/og" / name).exists() else "/assets/icon-512.png"


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
    og = og_image(lang, page)
    og_size = '\n<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">' if og.endswith(".jpg") else ""
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
<meta property="og:image" content="{BASE}{og}">{og_size}
<meta property="og:image:alt" content="{t.h('og.alt')}">
<meta property="og:locale" content="{code[3]}">{og_locale_alts}
<meta name="twitter:card" content="{'summary_large_image' if og.endswith('.jpg') else 'summary'}">
{extra}{ld}
<script src="/assets/site.js" defer></script>
</head>"""


def header(t: T, page: str = "home") -> str:
    short, sub = brand_parts(t)
    home = "" if page == "home" else url(t.lang)
    links = "".join(f'<li><a href="{home}#{a}">{t.h(k)}</a></li>' for a, k in (
        ("how", "nav.play"), ("journey", "nav.journey")))
    for target, key in (("realms", "nav.realms"), ("story", "nav.story")):
        current = ' aria-current="page"' if page == target else ""
        links += f'<li><a href="{url(t.lang, target)}"{current}>{t.h(key)}</a></li>'
    links += "".join(f'<li><a href="{home}#{a}">{t.h(k)}</a></li>' for a, k in (
        ("heroes", "nav.heroes"), ("fair", "nav.fair"), ("faq", "nav.faq")))
    langs = page_langs(page)
    others = "".join(f'<li><a href="{url(c, page if c in langs else "home")}" hreflang="{LANGS[c][2]}" lang="{LANGS[c][1]}">{esc(load_i18n(c)["lang.name"])}</a></li>'
                     for c in PUBLISHED if c != t.lang)
    return f"""<a class="skip" href="#main">{t.h('skip')}</a>
<header class="top">
  <a class="logo" href="{url(t.lang)}">{mark_svg()}<span class="logo-name"><span>{esc(short)}:</span> <span class="logo-sub">{esc(sub)}</span></span></a>
  <nav aria-label="{t.h('nav.label')}"><ul class="nav">{links}</ul></nav>
  <details class="langs"><summary aria-label="{esc(LANGS[t.lang][2].upper())} · {t.h('lang.label')}">{esc(LANGS[t.lang][2].upper())}</summary><ul>{others}</ul></details>
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
    realms = "".join(f"<li><a href=\"{url(t.lang, 'realm:' + r)}\">{t.h('realm.' + r)}</a></li>" if r in FACTS["realmsLive"]
                     else f"<li>{t.h('realm.' + r)}</li>" for r in e["realms"])
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


def hero_img(h: str, alt: str = "") -> str:
    size = 256 if h == "kaya" else 240
    return f'<img src="/assets/art/hero-{h}.webp" width="{size}" height="{size}" alt="{alt}" loading="lazy" decoding="async">'


def heroes(t: T) -> str:
    page = url(t.lang, "heroes")
    cards = "".join(f'<li><a class="card hero-chip" href="{page}#hero-{h}">{hero_img(h)}<span>{gh(t.lang, f"heroes.{h}.name")}</span></a></li>'
                    for h in GAMEDATA["heroes"])
    return f"""<section class="band" id="heroes" aria-labelledby="heroes-title">
  <h2 id="heroes-title">{t.h('heroes.title')}</h2><p class="section-lead">{t.h('heroes.lead')}</p>
  <ul class="hero-strip">{cards}</ul>
  <p class="center"><a class="btn" href="{page}">{t.h('heroes.all')}</a></p>
</section>"""


def fair(t: T) -> str:
    cards = "".join(f'<li class="card fair-card fair-{k}"><svg class="fair-icon" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><use href="/assets/mark.svg#i-{k}"/></svg><h3>{t.h(f"fair.{k}.title")}</h3><p>{t.h(f"fair.{k}.text")}</p></li>'
                    for k in ("ads", "myth", "gore"))
    return f"""<section class="band" id="fair" aria-labelledby="fair-title">
  <h2 id="fair-title">{t.h('fair.title')}</h2>
  <ul class="grid3">{cards}</ul>
</section>"""


def parents(t: T) -> str:
    """What a parent should know; every line must be true in the game today (no claim about planned features)."""
    items = "".join(f"<li>{t.h(f'parents.{k}')}</li>" for k in ("gore", "iap", "lives", "board", "apple"))
    return f"""<section class="band narrow" id="parents" aria-labelledby="parents-title">
  <div class="card museum-card"><h2 id="parents-title">{t.h('parents.title')}</h2><p>{t.h('parents.lead')}</p>
  <ul class="dots">{items}</ul><p class="fine-note">{t.h('parents.ask')}</p></div>
</section>"""


def faq(t: T) -> str:
    items = "".join(f'<details class="card qa"><summary><h3>{t.h(f"faq.{k}.q")}</h3></summary><p>{t.h(f"faq.{k}.a")}</p></details>'
                    for k in ("story", "when", "devices", "price", "langs", "myth"))
    return f"""<section class="band narrow" id="faq" aria-labelledby="faq-title">
  <h2 id="faq-title">{t.h('faq.title')}</h2>{items}
</section>"""


def footer(t: T) -> str:
    short, sub = brand_parts(t)
    langs = " · ".join(f'<a href="{url(c)}" hreflang="{LANGS[c][2]}" lang="{LANGS[c][1]}">{esc(load_i18n(c)["lang.name"])}</a>' for c in PUBLISHED)
    docs = "".join(f'<li><a href="{url(t.lang, d)}">{t.h("doc." + d)}</a></li>' for d in FOOTER_DOCS if t.lang in page_langs(d))
    return f"""<footer class="foot">
  <div class="foot-brand">{mark_svg()}<div><b>{esc(short)}:</b> <span>{esc(sub)}</span></div></div>
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
         "alternateName": brand_parts(t)[0], "description": t("hero.lead"), "url": page,
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
    body = "".join([header(t), '<main id="main">', hero(t), how(t), journey(t), heroes(t), fair(t), parents(t), faq(t), "</main>", footer(t)])
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


# ---------------------------------------------------------------- realm pages ("Mit Müzesi" in daylight)

MYTH_PATH = ROOT / "content/myth.json"
MYTH = json.loads(MYTH_PATH.read_text(encoding="utf-8")) if MYTH_PATH.exists() else {}
# Translations of the myth sections: content/myth.<lang>.json = {realm: {"myth": [...], "departures": [...]}}
for _path in sorted((ROOT / "content").glob("myth.*.json")):
    _lang = _path.name[len("myth."):-len(".json")]
    for _rid, _entry in json.loads(_path.read_text(encoding="utf-8")).items():
        if _rid in MYTH:
            MYTH[_rid][_lang] = _entry


def g(lang: str, key: str) -> str:
    """A text the game ships (data/game.json, synced from the game's l10n). Missing is a build error."""
    text = GAMEDATA["text"][lang]
    if key not in text:
        errors.append(f"[{lang}] game text missing: {key} (run scripts/sync-game.py)")
        return key
    return text[key]


def gh(lang: str, key: str) -> str:
    return esc(g(lang, key))


ART_FILE = {"skarabe_surusu": "skarabe"}  # the swarm is drawn as one beetle (game: art/source/misir/skarabe.svg)


def art(name: str) -> str:
    return ART_FILE.get(name, name).replace("_", "-")


def art_size(name: str) -> int:
    return {"boss": 480, "elite": 320}.get(name, 240)


def era_index(era_id: str) -> int:
    return next(i for i, e in enumerate(FACTS["eras"]) if e["id"] == era_id)


LIST_SEP = {"ja": "、", "zh-Hant": "、"}  # list separator; ", " elsewhere


def join_names(t: T, names: list[str]) -> str:
    sep = LIST_SEP.get(t.lang, ", ")
    return names[0] if len(names) == 1 else t("list.and", head=sep.join(names[:-1]), last=names[-1])


def crumbs(t: T, trail: list[tuple[str, str | None]]) -> tuple[str, dict]:
    """Visible breadcrumb and its BreadcrumbList; the last item is the current page (no link)."""
    items = "".join(f'<li><a href="{href}">{esc(name)}</a></li>' if href else f'<li aria-current="page">{esc(name)}</li>'
                    for name, href in trail)
    ld = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, **({"item": f"{BASE}{href}"} if href else {})}
        for i, (name, href) in enumerate(trail)]}
    return f'<nav class="crumbs" aria-label="{t.h("crumb.label")}"><ol>{items}</ol></nav>', ld


def realm_lead(t: T, rid: str) -> str:
    r, L = REALMS[rid], t.lang
    enemies = join_names(t, [g(L, f"enemies.{e}.name") for e in r["enemies"]])
    return t("realm.lead", realm=g(L, f"realms.{rid}.name"), first=r["maps"][0], last=r["maps"][1],
                                  mapName=g(L, f"realms.{rid}.mapName"), rule=g(L, f"realms.{rid}.rule"),
                                  enemies=enemies, elite=g(L, f"enemies.{r['elite']}.name"), boss=g(L, f"bosses.{r['boss']}.name"))


def foe_card(t: T, eid: str, kind: str) -> str:
    L = t.lang
    size = art_size(kind)
    badge = f'<span class="foe-badge">{t.h("realm.elite")}</span>' if kind == "elite" else ""
    return f"""<li class="card foe foe-{kind}">
  <div class="foe-fig"><img src="/assets/art/{art(eid)}.webp" width="{size}" height="{size}" alt="{gh(L, f'enemies.{eid}.name')}" loading="lazy" decoding="async"></div>
  <div class="foe-body">{badge}<h3>{gh(L, f'enemies.{eid}.name')}</h3><p class="foe-role">{gh(L, f'enemies.{eid}.role')}</p>
  <p>{gh(L, f'enemies.{eid}.behavior')}</p><p class="foe-teach"><b>{t.h('realm.teaches')}</b> {gh(L, f'enemies.{eid}.teaches')}</p></div>
</li>"""


def realm_myth(t: T, rid: str) -> str:
    entry = MYTH.get(rid)
    if not entry or t.lang not in entry:
        return ""
    paras = "".join(f"<p>{esc(p)}</p>" for p in entry[t.lang]["myth"])
    departs = "".join(f"<li>{esc(d)}</li>" for d in entry[t.lang].get("departures", []))
    departs_html = f'<h3>{t.h("realm.departures")}</h3><ul class="dots">{departs}</ul>' if departs else ""
    return f"""<section class="band narrow realm-myth" id="myth" aria-labelledby="myth-title">
  <div class="card museum-card"><p class="eyebrow">{t.h('realm.myth.eyebrow')}</p><h2 id="myth-title">{t.h('realm.myth.title')}</h2>{paras}{departs_html}
  <p class="fine-note">{t.h('realm.myth.note')}</p></div>
</section>"""


def realm_story(t: T, rid: str) -> str:
    """The game's own tale of the realm, after the museum card that tells the myth itself."""
    return f"""<section class="band narrow" id="story" aria-labelledby="story-title">
  <div class="card museum-card"><h2 id="story-title" class="h-small">{t.h('realm.story.title')}</h2><p>{t.h(f'realm.story.{rid}')}</p>
  <p><a href="{url(t.lang, 'story')}">{t.h('nav.story')}</a></p></div>
</section>"""


def build_story(lang: str) -> str:
    t, L = T(lang), lang
    page = "story"
    h1, lead = t("story.h1"), t("story.lead")
    trail = [(t("crumb.home"), url(L)), (t("nav.story"), None)]
    crumb_html, crumb_ld = crumbs(t, trail)
    revealed = [e for e in FACTS["eras"] if e.get("revealed")]
    ages = " · ".join(t(f"era.{e['id']}.name") for e in revealed)  # era names may contain "and" themselves
    parts = "".join(
        f'<section class="card museum-card" aria-labelledby="story-{k}"><h2 id="story-{k}" class="h-small">{t.h(f"story.{k}.title")}</h2>'
        f'<p>{t.h(f"story.{k}.text")}</p></section>'
        for k in ("tree", "silik", "blades", "teller"))
    parts += (f'<section class="card museum-card" aria-labelledby="story-ages"><h2 id="story-ages" class="h-small">{t.h("story.ages.title")}</h2>'
              f'<p>{esc(ages)}. {t.h("story.ages.text")}</p><p><a href="{url(L, "realms")}">{t.h("nav.realms")}</a></p></section>')
    parts += "".join(
        f'<section class="card museum-card" aria-labelledby="story-{k}"><h2 id="story-{k}" class="h-small">{t.h(f"story.{k}.title")}</h2>'
        f'<p>{t.h(f"story.{k}.text")}</p></section>'
        for k in ("unutus", "myth"))
    body = f"""<main id="main" class="band narrow story-page">
  {crumb_html}
  <h1>{esc(h1)}</h1><p class="eyebrow">{t.h('story.opening')}</p><p class="section-lead left">{esc(lead)}</p>
  {parts}
</main>"""
    page_url = f"{BASE}{url(L, page)}"
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": f"{page_url}#webpage", "url": page_url, "name": h1, "description": lead,
         "inLanguage": LANGS[L][2], "isPartOf": {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": t("brand")},
         "about": {"@id": f"{BASE}/#game"}, "breadcrumb": {"@id": f"{page_url}#breadcrumb"}},
        {**crumb_ld, "@id": f"{page_url}#breadcrumb"},
    ]}
    return head(t, t("meta.story.title"), t("meta.story.desc"), page, jsonld) + f"\n<body>\n{header(t, page)}{body}{footer(t)}\n</body>\n</html>\n"


def realm_sources(t: T, rid: str) -> str:
    sources = MYTH.get(rid, {}).get("sources", [])
    if not sources or t.lang not in MYTH[rid]:
        return ""
    items = "".join(f'<li><a href="{esc(s["url"])}" rel="noopener">{esc(s["title"])}</a> · {esc(s["publisher"])}</li>' for s in sources)
    return f"""<section class="band narrow" id="sources" aria-labelledby="sources-title">
  <h2 id="sources-title" class="h-small">{t.h('realm.sources')}</h2><ul class="sources">{items}</ul></section>"""


def realm_shots(t: T, rid: str) -> str:
    shots = sorted((ROOT / "assets/shots").glob(f"{rid}-*.webp"))
    if not shots:
        return ""
    name = g(t.lang, f"realms.{rid}.name")
    imgs = "".join(f'<li class="shot"><img src="/assets/shots/{p.name}" width="390" height="844" alt="{t.h("realm.shot.alt", realm=name, n=n + 1)}" loading="lazy" decoding="async"></li>'
                   for n, p in enumerate(shots))
    note = "" if t.lang == SHOTS_LANG else f'<p class="fine-note center">{t.h("shots.lang")}</p>'
    return f"""<section class="band" id="shots" aria-labelledby="shots-title">
  <h2 id="shots-title">{t.h('realm.shots.title')}</h2><ul class="shots">{imgs}</ul>{note}
</section>"""


def build_realm(rid: str, lang: str) -> str:
    t, r, L = T(lang), REALMS[rid], lang
    i = era_index(r["era"])
    era = FACTS["eras"][i]
    name, map_name = g(L, f"realms.{rid}.name"), g(L, f"realms.{rid}.mapName")
    h1 = t("realm.h1", realm=name, mapName=map_name)
    lead = realm_lead(t, rid)
    page = f"realm:{rid}"
    trail = [(t("crumb.home"), url(L)), (t("crumb.realms"), url(L, "realms")), (name, None)]
    crumb_html, crumb_ld = crumbs(t, trail)
    boss = r["boss"]
    facts = [
        (t("realm.fact.era"), f"{ROMAN[i]} · {t('era.' + era['id'] + '.name')}"),
        (t("realm.fact.maps"), t("realm.maps", first=r["maps"][0], last=r["maps"][1])),
        (t("realm.fact.myth"), g(L, f"realms.{rid}.mythology")),
        (t("realm.fact.rule"), g(L, f"realms.{rid}.rule")),
    ]
    facts_html = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in facts)
    foes = "".join(foe_card(t, e, "enemy") for e in r["enemies"]) + foe_card(t, r["elite"], "elite")
    phases = "".join(
        f"<tr><td><b>{gh(L, f'bosses.{boss}.phases.{n}.name')}</b><span class=\"hp\">{esc(hp)}</span></td>"
        f"<td>{gh(L, f'bosses.{boss}.phases.{n}.text')}</td><td>{gh(L, f'bosses.{boss}.phases.{n}.counter')}</td></tr>"
        for n, hp in enumerate(r["phases"]))
    rewards = "".join(f"<li>{gh(L, f'bosses.{boss}.rewards.{n}')}</li>" for n in range(r["rewards"]))
    rewards_html = f'<h3>{t.h("realm.rewards")}</h3><ul class="dots">{rewards}</ul>' if rewards else ""
    kit = [(t("realm.kit.weapon"), g(L, f"weapons.{r['weapon']}.name"), g(L, f"weapons.{r['weapon']}.behavior"))]
    kit.append((t("realm.kit.set"), g(L, f"armor-sets.{r['armorSet']}.name"),
                t("realm.kit.setbonus", two=g(L, f"armor-sets.{r['armorSet']}.bonus2"), four=g(L, f"armor-sets.{r['armorSet']}.bonus4"))))
    if r["mythPower"]:
        kit.append((t("realm.kit.power"), g(L, f"myth-powers.{r['mythPower']}.name"), g(L, f"myth-powers.{r['mythPower']}.effect")))
    kit_html = "".join(f'<li class="card kit-card"><p class="kit-kind">{esc(k)}</p><h3>{esc(n)}</h3><p>{esc(d)}</p></li>' for k, n, d in kit)
    minions = "".join(f'<img class="exhibit-minion m{n}" src="/assets/art/{art(e)}.webp" width="240" height="240" alt="" decoding="async">'
                      for n, e in enumerate(r["enemies"][:2]))
    live = FACTS["realmsLive"]
    pos = live.index(rid)
    nav = ""
    for cls, other, key in (("prev", live[pos - 1] if pos else None, "realm.prev"), ("next", live[pos + 1] if pos + 1 < len(live) else None, "realm.next")):
        if other:
            nav += f'<a class="card realm-step realm-{cls}" href="{url(L, "realm:" + other)}"><span>{t.h(key)}</span><b>{gh(L, f"realms.{other}.name")}</b></a>'
    body = f"""<main id="main" class="realm">
<header class="realm-hero ground-{rid}">
  {crumb_html}
  <div class="exhibit">
    <div class="exhibit-stage" aria-hidden="true"><img class="exhibit-boss" src="/assets/art/{art(boss)}.webp" width="480" height="480" alt="" fetchpriority="high">{minions}</div>
    <div class="card exhibit-label">
      <p class="eyebrow">{esc(ROMAN[i])} · {t.h('era.' + era['id'] + '.name')}</p>
      <h1>{esc(h1)}</h1>
      <p class="lead">{esc(lead)}</p>
      <dl class="facts">{facts_html}</dl>
    </div>
  </div>
</header>
{realm_myth(t, rid)}
{realm_story(t, rid)}
<section class="band" id="foes" aria-labelledby="foes-title">
  <h2 id="foes-title">{t.h('realm.foes.title')}</h2><p class="section-lead">{t.h('realm.foes.lead')}</p>
  <ul class="foes">{foes}</ul>
</section>
{realm_shots(t, rid)}
<section class="band" id="boss" aria-labelledby="boss-title">
  <div class="card boss-card">
    <div class="boss-fig"><img src="/assets/art/{art(boss)}.webp" width="480" height="480" alt="{gh(L, f'bosses.{boss}.name')}" loading="lazy" decoding="async"></div>
    <div class="boss-body">
      <p class="eyebrow eyebrow-boss">{t.h('realm.boss.eyebrow', map=r['maps'][1])}</p>
      <h2 id="boss-title">{gh(L, f'bosses.{boss}.name')}</h2>
      <p class="boss-lore">{gh(L, f'bosses.{boss}.lore')}</p>
    </div>
    <div class="table phases"><table>
      <caption class="sr-only">{t.h('realm.phases.caption')}</caption>
      <thead><tr><th scope="col">{t.h('realm.phase')}</th><th scope="col">{t.h('realm.phase.does')}</th><th scope="col">{t.h('realm.phase.counter')}</th></tr></thead>
      <tbody>{phases}</tbody></table></div>
    <div class="boss-foot">{rewards_html}<p class="fine-note">{t.h('realm.balance.note')}</p></div>
  </div>
</section>
<section class="band" id="kit" aria-labelledby="kit-title">
  <h2 id="kit-title">{t.h('realm.kit.title')}</h2><p class="section-lead">{t.h('realm.kit.lead')}</p>
  <ul class="grid3">{kit_html}</ul>
</section>
{realm_sources(t, rid)}
<nav class="band realm-nav" aria-label="{t.h('realm.nav')}">{nav}</nav>
</main>"""
    page_url = f"{BASE}{url(L, page)}"
    desc = t("meta.realm.desc", realm=name, first=r["maps"][0], last=r["maps"][1],
             boss=g(L, f"bosses.{boss}.name"), elite=g(L, f"enemies.{r['elite']}.name"))
    title = t("meta.realm.title", realm=name, mapName=map_name)
    about = [{"@id": f"{BASE}/#game"}]
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": f"{page_url}#webpage", "url": page_url, "name": title, "description": desc,
         "inLanguage": LANGS[L][2], "isPartOf": {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": t("brand")},
         "about": about, "breadcrumb": {"@id": f"{page_url}#breadcrumb"}},
        {**crumb_ld, "@id": f"{page_url}#breadcrumb"},
    ]}
    return head(t, title, desc, page, jsonld) + f"\n<body>\n{header(t, page)}{body}{footer(t)}\n</body>\n</html>\n"


def build_realms(lang: str) -> str:
    t, L = T(lang), lang
    page = "realms"
    trail = [(t("crumb.home"), url(L)), (t("crumb.realms"), None)]
    crumb_html, crumb_ld = crumbs(t, trail)
    cards, items = "", []
    for e_i, e in enumerate(FACTS["eras"]):
        realm_cards = ""
        for rid in e["realms"]:
            r = REALMS[rid]
            name = g(L, f"realms.{rid}.name")
            maps = t("realm.maps", first=r["maps"][0], last=r["maps"][1])
            if rid in FACTS["realmsLive"]:
                href = url(L, f"realm:{rid}")
                items.append({"@type": "ListItem", "position": len(items) + 1, "name": name, "url": f"{BASE}{href}"})
                realm_cards += f"""<li><a class="card realm-card ground-{rid}" href="{href}">
  <img src="/assets/art/{art(r['boss'])}.webp" width="480" height="480" alt="" loading="lazy" decoding="async">
  <span class="realm-card-body"><b>{esc(name)}</b><span>{gh(L, f'realms.{rid}.mapName')} · {esc(maps)}</span><span class="muted">{gh(L, f'realms.{rid}.mythology')}</span></span></a></li>"""
            else:
                realm_cards += f"""<li class="card realm-card realm-soon"><span class="realm-card-body"><b>{esc(name)}</b><span>{esc(maps)}</span><span class="muted">{t.h('realms.soon')}</span></span></li>"""
        cards += f"""<section class="era-row" aria-labelledby="row-{e['id']}"><h2 id="row-{e['id']}" class="h-small"><span class="era-num" aria-hidden="true">{ROMAN[e_i]}</span>{t.h('era.' + e['id'] + '.name')}<span class="period">{t.h('era.' + e['id'] + '.period')}</span></h2>
  <ul class="realm-grid">{realm_cards}</ul></section>"""
    h1, lead = t("realms.title"), t("realms.lead")
    body = f"""<main id="main" class="band realms-index">
  {crumb_html}
  <h1>{esc(h1)}</h1><p class="section-lead left">{esc(lead)}</p>
  {cards}
</main>"""
    page_url = f"{BASE}{url(L, page)}"
    title = t("meta.realms.title")
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": f"{page_url}#webpage", "url": page_url, "name": h1, "description": lead,
         "inLanguage": LANGS[L][2], "isPartOf": {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": t("brand")},
         "about": {"@id": f"{BASE}/#game"}, "breadcrumb": {"@id": f"{page_url}#breadcrumb"},
         "mainEntity": {"@type": "ItemList", "itemListElement": items}},
        {**crumb_ld, "@id": f"{page_url}#breadcrumb"},
    ]}
    return head(t, title, t("meta.realms.desc"), page, jsonld) + f"\n<body>\n{header(t, page)}{body}{footer(t)}\n</body>\n</html>\n"


def build_heroes(lang: str) -> str:
    t, L = T(lang), lang
    page = "heroes"
    h1, lead = t("heroes.page.title"), t("heroes.page.lead")
    trail = [(t("crumb.home"), url(L)), (h1, None)]
    crumb_html, crumb_ld = crumbs(t, trail)
    text = GAMEDATA["text"][L]
    cards, items = "", []
    for h in GAMEDATA["heroes"]:
        name = g(L, f"heroes.{h}.name")
        items.append({"@type": "ListItem", "position": len(items) + 1, "name": name, "url": f"{BASE}{url(L, page)}#hero-{h}"})
        title, style, quote = (text.get(f"heroes.{h}.{k}") for k in ("title", "playstyle", "quote"))
        details = ""
        if title:
            details += f'<p class="hero-title">{esc(title)}</p>'
        details += f'<dl class="hero-facts"><div><dt>{t.h("hero.f.homeland")}</dt><dd>{gh(L, f"heroes.{h}.realm")}</dd></div>'
        if style:
            details += f'<div><dt>{t.h("hero.f.style")}</dt><dd>{esc(style)}</dd></div>'
        details += "</dl>"
        details += f'<blockquote class="hero-quote">{esc(quote)}</blockquote>' if quote else f'<p class="fine-note">{t.h("hero.unknown")}</p>'
        sources = "".join(f' <a href="{esc(s["url"])}" rel="noopener">{esc(s["title"])}</a>' for s in HERO_SOURCES.get(h, []))
        story = (f'<div class="hero-story"><p>{t.h(f"hero.bio.{h}")}</p>'
                 f'<p class="fine-note"><b>{t.h("hero.f.myth")}:</b> {t.h(f"hero.myth.{h}")}{sources}</p></div>')
        cards += f"""<li class="card hero-card-full" id="hero-{h}">
  <div class="hero-fig">{hero_img(h, esc(name))}</div>
  <div class="hero-body"><h2 class="h-small">{esc(name)}</h2>{details}</div>
  {story}
</li>"""
    body = f"""<main id="main" class="band heroes-page">
  {crumb_html}
  <h1>{esc(h1)}</h1><p class="section-lead left">{esc(lead)}</p>
  <ul class="hero-grid">{cards}</ul>
</main>"""
    page_url = f"{BASE}{url(L, page)}"
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": f"{page_url}#webpage", "url": page_url, "name": h1, "description": lead,
         "inLanguage": LANGS[L][2], "isPartOf": {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": t("brand")},
         "about": {"@id": f"{BASE}/#game"}, "breadcrumb": {"@id": f"{page_url}#breadcrumb"},
         "mainEntity": {"@type": "ItemList", "itemListElement": items}},
        {**crumb_ld, "@id": f"{page_url}#breadcrumb"},
    ]}
    return head(t, t("meta.heroes.title"), t("meta.heroes.desc"), page, jsonld) + f"\n<body>\n{header(t, page)}{body}{footer(t)}\n</body>\n</html>\n"


def build_press(lang: str) -> str:
    t, L = T(lang), lang
    page = "press"
    trail = [(t("crumb.home"), url(L)), (t("doc.press"), None)]
    crumb_html, crumb_ld = crumbs(t, trail)
    langs = t.vars["appLanguages"]
    status = t("cta.soon") if FACTS["stage"] == "prelaunch" else t("press.status.live")
    sheet = [(t("press.f.name"), t("brand")), (t("press.f.dev"), SITE["copyrightHolder"]),
             (t("press.f.platforms"), ", ".join(FACTS["platforms"])), (t("press.f.status"), status),
             (t("press.f.price"), t("faq.price.a")), (t("press.f.langs"), langs),
             (t("press.f.content"), t("og.counts")), (t("press.f.contact"), SITE["contact"])]
    sheet_html = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in sheet)
    sheet_html = sheet_html.replace(esc(SITE["contact"]) + "</dd>", f'<a href="mailto:{esc(SITE["contact"])}">{esc(SITE["contact"])}</a></dd>')
    feats = "".join(f"<li>{t.h(f'press.feat.{k}')}</li>" for k in ("blades", "realms", "myth", "fair"))
    files = [("press/icon-1024.png", t("press.file.icon"), "PNG · 1024×1024"), ("press/mark.svg", t("press.file.mark"), "SVG"),
             (f"og/og-{L}.jpg", t("press.file.og"), "JPEG · 1200×630")]
    files_html = "".join(f'<li><a href="/assets/{f}" download>{esc(n)}</a> <span class="muted">{esc(k)}</span></li>' for f, n, k in files)
    shots = ["hero-select", "map"] + [f"{r}-1" for r in FACTS["realmsLive"]]
    shots_html = "".join(f'<li class="shot"><a href="/assets/shots/{s}.webp"><img src="/assets/shots/{s}.webp" width="390" height="844" alt="{t.h("press.shot.alt", n=i + 1)}" loading="lazy" decoding="async"></a></li>'
                         for i, s in enumerate(shots))
    note = "" if L == SHOTS_LANG else f'<p class="fine-note center">{t.h("shots.lang")}</p>'
    figs = [REALMS[r]["boss"] for r in FACTS["realmsLive"]]
    figs_html = "".join(f'<li class="card hero-chip"><a href="/assets/art/{art(b)}.webp"><img src="/assets/art/{art(b)}.webp" width="480" height="480" alt="{gh(L, f"bosses.{b}.name")}" loading="lazy" decoding="async"></a><span>{gh(L, f"bosses.{b}.name")}</span></li>' for b in figs)
    h1 = t("press.title")
    body = f"""<main id="main" class="press">
<div class="band narrow">{crumb_html}
  <h1>{esc(h1)}</h1><p class="section-lead left">{t.h('press.lead')}</p>
  <div class="card museum-card"><h2 class="h-small">{t.h('press.facts')}</h2><dl class="facts">{sheet_html}</dl></div>
  <div class="card museum-card press-about"><h2 class="h-small">{t.h('press.about')}</h2><p>{t.h('hero.lead')}</p><p>{t.h('journey.lead')}</p><ul class="dots">{feats}</ul></div>
  <div class="card museum-card"><h2 class="h-small">{t.h('press.files')}</h2><ul class="dots">{files_html}</ul><p class="fine-note">{t.h('press.usage')}</p></div>
</div>
<section class="band" aria-labelledby="press-shots"><h2 id="press-shots">{t.h('press.shots')}</h2><ul class="shots shots-wide">{shots_html}</ul>{note}</section>
<section class="band" aria-labelledby="press-art"><h2 id="press-art">{t.h('press.art')}</h2><ul class="hero-strip">{figs_html}</ul></section>
</main>"""
    page_url = f"{BASE}{url(L, page)}"
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "AboutPage", "@id": f"{page_url}#webpage", "url": page_url, "name": h1, "description": t("press.lead"),
         "inLanguage": LANGS[L][2], "isPartOf": {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": t("brand")},
         "about": {"@id": f"{BASE}/#game"}, "breadcrumb": {"@id": f"{page_url}#breadcrumb"}},
        {**crumb_ld, "@id": f"{page_url}#breadcrumb"},
    ]}
    title = f"{h1} · {t('brand')}"
    return head(t, title, t("press.lead"), page, jsonld) + f"\n<body>\n{header(t, page)}{body}{footer(t)}\n</body>\n</html>\n"


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
    pages += f"\n- [{t('realms.title')}]({BASE}{url('en', 'realms')})"
    pages += "\n" + "\n".join(
        f"- [{t('realm.h1', realm=g('en', f'realms.{r}.name'), mapName=g('en', f'realms.{r}.mapName'))}]({BASE}{url('en', 'realm:' + r)}): "
        f"boss {g('en', 'bosses.' + REALMS[r]['boss'] + '.name')}, maps {REALMS[r]['maps'][0]}–{REALMS[r]['maps'][1]}"
        for r in FACTS["realmsLive"])
    return f"""# {t('brand')}

> {t('hero.lead')}

Status: not yet released (coming soon to the App Store). Platforms: {', '.join(FACTS['platforms'])}.
Short name: {brand_parts(t)[0]}. Developer: {SITE['copyrightHolder']} ({SITE['developerUrl']}).

## Facts
- Ages: {c['eras']}; mythological realms: {c['realms']}; maps: {c['maps']} ({c['mapsPerRealm']} per realm); heroes: {c['heroes']}
- Controls: one thumb. Walking widens the blades' orbit; standing still draws them in and spins them faster.
- Monetization: free to download, optional in-app purchases, no forced ads; rewarded ads only by choice.
- Game languages: {t.vars['appLanguages']}

## Story
{t('story.llms')} More: {BASE}{url('en', 'story')}

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
                if key in node and re.sub(r"\s+", " ", node[key]) not in text and node["@type"] != "WebPage":
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
    # Every published language names eras, realms, bosses and heroes exactly as the game does.
    for lang in PUBLISHED:
        site, game = load_i18n(lang), GAMEDATA["text"][lang]
        pairs = [(f"era.{e['id']}.{k}", f"eras.{e['id']}.{k}") for e in FACTS["eras"] for k in ("name", "period")]
        pairs += [(f"realm.{r}", f"realms.{r}.name") for e in FACTS["eras"] for r in e["realms"]]
        pairs += [(f"boss.{b}", f"bosses.{b}.name") for e in FACTS["eras"] for b in e["bosses"] + [e["guardian"]]]
        pairs += [(f"hero.{h}", f"heroes.{h}.name") for h in FACTS["heroShowcase"]]
        for site_key, game_key in pairs:
            if game_key in game and site.get(site_key) != game[game_key]:
                errors.append(f"[{lang}] {site_key} = {site.get(site_key)!r}, the game says {game[game_key]!r}")
    import importlib.util
    spec = importlib.util.spec_from_file_location("sync_game", ROOT / "scripts/sync-game.py")
    sync = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sync)
    fresh = sync.snapshot(GAME)
    if fresh["realms"] != GAMEDATA["realms"] or fresh["text"] != GAMEDATA["text"]:
        errors.append("data/game.json differs from the game repo: run python3 scripts/sync-game.py")


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
            if page == "home":
                pages[rel] = build_home(lang)
            elif page == "realms":
                pages[rel] = build_realms(lang)
            elif page == "heroes":
                pages[rel] = build_heroes(lang)
            elif page == "press":
                pages[rel] = build_press(lang)
            elif page == "story":
                pages[rel] = build_story(lang)
            elif page.startswith("realm:"):
                pages[rel] = build_realm(page.split(":", 1)[1], lang)
            else:
                pages[rel] = build_doc(page, lang)
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
