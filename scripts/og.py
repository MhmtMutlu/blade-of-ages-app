#!/usr/bin/env python3
"""Draws the share cards (Open Graph, 1200×630) into assets/og/: one for the home page per language and one per live
realm per language. Everything comes from the site's own data (facts, game.json, i18n) and art (assets/art), in the
game's daylight clay look. Run it after the text or the art changes; the JPEGs are committed.

    .venv/bin/python scripts/og.py
    .venv/bin/python scripts/og.py --only en      # one language

Needs Pillow and the game's TTF fonts (../blades-of-ages/game/Assets/_Project/Art/Fonts or AOB_FONTS). Languages
outside the Latin script use the system's CJK fonts (macOS Hiragino Sans, Apple SD Gothic Neo, Heiti TC).
"""
import argparse, json, math, os, pathlib, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = pathlib.Path(os.environ.get("AOB_FONTS", ROOT.parent / "blades-of-ages/game/Assets/_Project/Art/Fonts"))
ART = ROOT / "assets/art"
OUT = ROOT / "assets/og"
W, H = 1200, 630
TEXT, MUTED, ACCENT, ACCENT_DEEP, AMBER = "#1F3B47", "#5D7A83", "#12A684", "#0B7A61", "#C98A12"
SKY, MINT = (205, 235, 255), (230, 246, 241)
# (file, collection index) per face; macOS system fonts, since the game's Baloo 2 and Nunito are Latin only.
CJK = {
    "ja": {"head": ("/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc", 0), "body": ("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 0)},
    "ko": {"head": ("/System/Library/Fonts/AppleSDGothicNeo.ttc", 16), "body": ("/System/Library/Fonts/AppleSDGothicNeo.ttc", 6)},
    "zh-Hant": {"head": ("/System/Library/Fonts/STHeiti Medium.ttc", 0), "body": ("/System/Library/Fonts/STHeiti Medium.ttc", 0)},
}
ROMAN = ["I", "II", "III", "IV", "V"]

FACTS = json.loads((ROOT / "data/facts.json").read_text(encoding="utf-8"))
GAME = json.loads((ROOT / "data/game.json").read_text(encoding="utf-8"))
REALMS = {r["id"]: r for r in GAME["realms"]}


def font(lang: str, face: str, size: int) -> ImageFont.FreeTypeFont:
    """lang None = the game's Latin fonts (brand names are Latin in every language)."""
    if lang in CJK:
        path, index = CJK[lang][face]
        return ImageFont.truetype(path, round(size * 0.86), index=index)
    return ImageFont.truetype(str(FONTS / {"head": "Baloo2-ExtraBold.ttf", "body": "Nunito-ExtraBold.ttf"}[face]), size)


def bold(lang: str) -> dict:
    """Heiti TC has no heavy weight: thicken its headings with a same-colour stroke."""
    return {"stroke_width": 1, "stroke_fill": TEXT} if lang == "zh-Hant" else {}


def wrap(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, width: int) -> list[str]:
    """Greedy word wrap; CJK text (no spaces) wraps by character."""
    units = text.split(" ") if " " in text else list(text)
    sep = " " if " " in text else ""
    lines, line = [], ""
    for u in units:
        trial = f"{line}{sep}{u}" if line else u
        if draw.textlength(trial, font=f) <= width:
            line = trial
        else:
            lines.append(line)
            line = u
    return lines + [line]


def sky() -> Image.Image:
    img = Image.new("RGB", (W, H))
    px = ImageDraw.Draw(img)
    for y in range(H):
        k = y / (H - 1)
        px.line([(0, y), (W, y)], fill=tuple(round(a + (b - a) * k) for a, b in zip(SKY, MINT)))
    return img


def tiled(name: str, size: tuple[int, int], tile: int = 256) -> Image.Image:
    src = Image.open(ART / f"ground-{name}.webp").convert("RGB").resize((tile, tile))
    out = Image.new("RGB", size)
    for x in range(0, size[0], tile):
        for y in range(0, size[1], tile):
            out.paste(src, (x, y))
    return out


def rounded_mask(size: tuple[int, int], r: int) -> Image.Image:
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=255)
    return m


def card(img: Image.Image, box: tuple[int, int, int, int], r: int = 36) -> None:
    """A white clay card with the game's two-step soft shadow."""
    x0, y0, x1, y1 = box
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([x0, y0 + 14, x1, y1 + 14], r, fill=(31, 59, 71, 46))
    img.paste(shadow.filter(ImageFilter.GaussianBlur(18)), (0, 0), shadow.filter(ImageFilter.GaussianBlur(18)))
    ImageDraw.Draw(img).rounded_rectangle(box, r, fill="#FFFFFF")


def sprite(img: Image.Image, name: str, width: int, center: tuple[int, int], shadow: bool = True) -> None:
    s = Image.open(ART / f"{name}.webp").convert("RGBA")
    s = s.resize((width, round(s.height * width / s.width)), Image.LANCZOS)
    x, y = center[0] - s.width // 2, center[1] - s.height // 2
    if shadow:
        a = s.getchannel("A").point(lambda v: v * 0.16)
        sh = Image.new("RGBA", s.size, (31, 59, 71, 0))
        sh.putalpha(a)
        img.paste(sh, (x, y + 12), sh)
    img.paste(s, (x, y), s)


def blades(img: Image.Image, center: tuple[int, int], radius: int, length: int) -> None:
    """Six outward-facing blades around the hero, as in the game's orbit."""
    d = ImageDraw.Draw(img)
    cx, cy = center
    for k in range(6):
        a = math.radians(k * 60 - 90 + 15)
        ux, uy = math.cos(a), math.sin(a)
        px, py = -uy, ux
        base = (cx + ux * radius, cy + uy * radius)
        tip = (cx + ux * (radius + length), cy + uy * (radius + length))
        w = length * 0.16
        poly = [(base[0] + px * w, base[1] + py * w), (tip[0] + px * w * .9 - ux * w, tip[1] + py * w * .9 - uy * w), tip,
                (tip[0] - px * w * .9 - ux * w, tip[1] - py * w * .9 - uy * w), (base[0] - px * w, base[1] - py * w)]
        d.polygon(poly, fill="#F4F8FF", outline="#9DBAD4", width=3)


def pill(img: Image.Image, xy: tuple[int, int], text: str, f, fg: str, bg: str) -> int:
    d = ImageDraw.Draw(img)
    w = round(d.textlength(text, font=f)) + 36
    h = f.size + 22
    d.rounded_rectangle([xy[0], xy[1], xy[0] + w, xy[1] + h], h // 2, fill=bg)
    d.text((xy[0] + 18, xy[1] + h / 2), text, font=f, fill=fg, anchor="lm")
    return w


def home_card(lang: str, t: dict) -> Image.Image:
    img = sky()
    panel = tiled("gobeklitepe", (620, 630)).convert("RGBA")
    panel.putalpha(rounded_mask(panel.size, 0))
    img.paste(panel, (580, 0))
    ImageDraw.Draw(img).rectangle([580, 0, 600, 630], fill=MINT)
    img = img.convert("RGBA")
    centre = (900, 330)
    for name, w, pos in (("tas-domuz", 120, (690, 470)), ("akrep-ruhu", 112, (1110, 150)), ("tilki-golgesi", 108, (1100, 520))):
        sprite(img, name, w, pos)
    blades(img, centre, 92, 70)
    sprite(img, "hero-kaya", 170, (centre[0], centre[1] - 6))
    card(img, (48, 60, 640, 570))
    d = ImageDraw.Draw(img)
    icon = Image.open(ROOT / "assets/icon-180.png").convert("RGBA").resize((92, 92), Image.LANCZOS)
    icon.putalpha(rounded_mask(icon.size, 22))
    img.paste(icon, (88, 100), icon)
    short, sub = t["brand"].split(": ", 1)  # the one name as a lockup, as in the site header
    d.text((200, 146), f"{short}:", font=font(None, "head", 54), fill=TEXT, anchor="ls")
    d.text((202, 184), sub, font=font(None, "body", 24), fill=MUTED, anchor="ls")
    y = 230
    size = 60
    while True:  # shrink the title until it fits in two lines
        title_font = font(lang, "head", size)
        lines = wrap(d, t["hero.title"], title_font, 510)
        if len(lines) <= 2 or size <= 40:
            break
        size -= 4
    for line in lines:
        d.text((88, y), line, font=title_font, fill=TEXT, **bold(lang))
        y += round(size * 1.17)
    y += 14
    body = font(lang, "body", 24)
    for line in wrap(d, t["og.counts"].format(**FACTS["counts"]), body, 510):
        d.text((88, y), line, font=body, fill=MUTED)
        y += 32
    pill(img, (88, max(470, y + 14)), t["cta.soon"], font(lang, "body", 26), "#FFFFFF", ACCENT)
    return img.convert("RGB")


def realm_card(lang: str, t: dict, rid: str) -> Image.Image:
    r = REALMS[rid]
    gt = GAME["text"][lang]
    img = tiled(rid, (W, H)).convert("RGBA")
    veil = Image.new("RGBA", (W, H), (205, 235, 255, 0))
    vd = ImageDraw.Draw(veil)
    for y in range(H):
        vd.line([(0, y), (W, y)], fill=(205, 235, 255, round(150 * (1 - y / H))))
    img.alpha_composite(veil)
    sprite(img, r["enemies"][0].replace("_", "-") if rid != "misir" or r["enemies"][0] != "skarabe_surusu" else "skarabe", 150, (760, 520))
    sprite(img, r["boss"].replace("_", "-"), 430, (950, 300))
    card(img, (48, 70, 620, 560))
    d = ImageDraw.Draw(img)
    i = next(n for n, e in enumerate(FACTS["eras"]) if e["id"] == r["era"])
    era = gt[f"eras.{r['era']}.name"]
    pill(img, (88, 108), f"{ROMAN[i]} · {era}", font(lang, "body", 22), ACCENT_DEEP, "#E3F6EF")
    y = 176
    h1 = t["realm.h1"].format(realm=gt[f"realms.{rid}.name"], mapName=gt[f"realms.{rid}.mapName"])
    size = 56
    while True:
        hf = font(lang, "head", size)
        h1_lines = wrap(d, h1, hf, 490)
        if len(h1_lines) <= 2 or size <= 40:
            break
        size -= 4
    for line in h1_lines:
        d.text((88, y), line, font=hf, fill=TEXT, **bold(lang))
        y += round(size * 1.14)
    y += 10
    sub = t["og.realm"].format(boss=gt[f"bosses.{r['boss']}.name"], first=r["maps"][0], last=r["maps"][1])
    bf = font(lang, "body", 25)
    for line in wrap(d, sub, bf, 490):
        d.text((88, y), line, font=bf, fill=MUTED)
        y += 34
    icon = Image.open(ROOT / "assets/icon-180.png").convert("RGBA").resize((56, 56), Image.LANCZOS)
    icon.putalpha(rounded_mask(icon.size, 14))
    img.paste(icon, (88, 476), icon)
    short, sub = t["brand"].split(": ", 1)
    d.text((158, 500), f"{short}:", font=font(None, "head", 34), fill=TEXT, anchor="ls")
    d.text((159, 526), sub, font=font(None, "body", 20), fill=MUTED, anchor="ls")
    return img.convert("RGB")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    a = ap.parse_args()
    if not FONTS.is_dir():
        sys.exit(f"fonts not found: {FONTS} (set AOB_FONTS)")
    OUT.mkdir(parents=True, exist_ok=True)
    langs = [p.stem for p in sorted((ROOT / "content/i18n").glob("*.json"))]
    for lang in langs:
        if a.only and a.only != lang:
            continue
        t = json.loads((ROOT / "content/i18n" / f"{lang}.json").read_text(encoding="utf-8"))
        jobs = [(f"og-{lang}.jpg", lambda: home_card(lang, t))]
        jobs += [(f"og-{rid}-{lang}.jpg", lambda rid=rid: realm_card(lang, t, rid)) for rid in FACTS["realmsLive"]]
        for name, make in jobs:
            make().save(OUT / name, "JPEG", quality=84, optimize=True, progressive=True)
            print(f"assets/og/{name}  {(OUT / name).stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
