#!/usr/bin/env python3
"""Renders the game's clay SVGs into the site's WebP images (assets/art/).

The game repository is the single source of the art: tools/*_gen.py write art/source/**.svg there. This script strips
the rig pivots (the magenta dots the game removes on import), renders each SVG with macOS QuickLook (qlmanage) and
encodes it with cwebp. QuickLook always paints a white page, so sprites are rendered twice, on black and on white,
and the alpha is recovered from the difference (difference matting). Run it only when the game art changes; the WebP
files are committed.

    python3 -m venv .venv && .venv/bin/pip install pillow numpy
    .venv/bin/python scripts/art.py                   # game repo at ../blades-of-ages, or AOB_GAME_REPO
    .venv/bin/python scripts/art.py --only apep       # a single image

Needs macOS (qlmanage), cwebp (brew install webp), Pillow and numpy.
"""
import argparse, os, pathlib, re, shutil, subprocess, sys, tempfile
import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
GAME = pathlib.Path(os.environ.get("AOB_GAME_REPO", ROOT.parent / "blades-of-ages"))
SRC = GAME / "art" / "source"
OUT = ROOT / "assets" / "art"

# (output name, source svg under art/source, longest side in px, kind)
# kind "sprite" keeps alpha; "tile" is a seamless ground texture (opaque).
IMAGES = [
    # Hero playground (canvas sprites)
    ("hero-kaya", "heroes/hero_kaya.svg", 256, "sprite"),
    ("tas-domuz", "gobeklitepe/tas_domuz.svg", 160, "sprite"),
    ("akrep-ruhu", "gobeklitepe/akrep_ruhu.svg", 160, "sprite"),
    ("tilki-golgesi", "gobeklitepe/tilki_golgesi.svg", 160, "sprite"),
    ("gold-coin", "ortak/gold_coin.svg", 64, "sprite"),
    ("dikili-tas", "gobeklitepe/dikili_tas.svg", 160, "sprite"),
    # Era I
    ("akbaba-ana", "gobeklitepe/akbaba_ana.svg", 480, "sprite"),
    ("humbaba", "sumer/humbaba.svg", 480, "sprite"),
    ("kil-golem", "sumer/kil_golem.svg", 240, "sprite"),
    ("zigurat", "sumer/structure_sumer_ziggurat.svg", 400, "sprite"),
    ("teras", "gobeklitepe/structure_gobeklitepe_terrace.svg", 400, "sprite"),
    # Era II
    ("apep", "misir/apep.svg", 480, "sprite"),
    ("mumya", "misir/mumya.svg", 240, "sprite"),
    ("sfenks-bekcisi", "misir/sfenks_bekcisi.svg", 320, "sprite"),
    ("medusa", "yunan/medusa.svg", 480, "sprite"),
    ("iskelet-hoplit", "yunan/iskelet_hoplit.svg", 240, "sprite"),
    ("tapinak", "yunan/structure_yunan_temple.svg", 400, "sprite"),
    ("illuyanka", "hitit/illuyanka.svg", 480, "sprite"),
    ("kaya-devi", "hitit/kaya_devi.svg", 240, "sprite"),
    # Era III
    ("fenrir", "iskandinav/fenrir.svg", 480, "sprite"),
    ("draugr", "iskandinav/draugr.svg", 240, "sprite"),
    ("buz-kurdu", "iskandinav/buz_kurdu.svg", 240, "sprite"),
    # Ground tiles
    ("ground-gobeklitepe", "gobeklitepe/gobeklitepe_ground_0.svg", 256, "tile"),
    ("ground-sumer", "sumer/sumer_ground_0.svg", 256, "tile"),
    ("ground-misir", "misir/misir_ground_0.svg", 256, "tile"),
    ("ground-yunan", "yunan/yunan_ground_0.svg", 256, "tile"),
    ("ground-hitit", "hitit/hitit_ground_0.svg", 256, "tile"),
    ("ground-iskandinav", "iskandinav/iskandinav_ground_0.svg", 256, "tile"),
] + [(f"hero-{h}", f"heroes/hero_{h}.svg", 240, "sprite") for h in (
    "nefertari", "muwatalli", "antiope", "sigrun", "tomoe", "tomris", "itzel", "jin")] + [
    # Realm pages: the rest of each live realm's enemies (240) and elites (320)
    (rel.split("/")[1].removesuffix(".svg").replace("_", "-"), rel, size, "sprite") for rel, size in (
        ("gobeklitepe/totem_tasiyici.svg", 320),
        ("sumer/kanatli_cin.svg", 240), ("sumer/akrep_adam.svg", 240), ("sumer/gok_bogasi.svg", 320),
        ("misir/skarabe.svg", 240), ("misir/cakal_muhafiz.svg", 240),
        ("yunan/satir_okcu.svg", 240), ("yunan/harpi.svg", 240), ("yunan/kiklop.svg", 320),
        ("hitit/firtina_ruhu.svg", 240), ("hitit/dag_kecisi_suvari.svg", 240), ("hitit/ullikummi.svg", 320),
        ("iskandinav/kuzgun_surusu.svg", 240), ("iskandinav/buz_devi.svg", 320),
    )]

PIVOTS = re.compile(r'<g id="pivots">.*?</g>', re.S)


def quicklook(svg: str, name: str, size: int, tmp: pathlib.Path) -> np.ndarray:
    src = tmp / name
    src.write_text(svg, encoding="utf-8")
    subprocess.run(["qlmanage", "-t", "-s", str(size), "-o", str(tmp), str(src)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    png = tmp / (name + ".png")
    if not png.exists():
        sys.exit(f"qlmanage did not render {name}")
    return np.asarray(Image.open(png).convert("RGB"), dtype=np.float32)


def matte(on_black: np.ndarray, on_white: np.ndarray) -> Image.Image:
    """alpha = 1 - (white - black); colour = black / alpha (premultiplied over black)."""
    alpha = 1.0 - (on_white - on_black).mean(axis=2) / 255.0
    alpha = np.clip(alpha, 0.0, 1.0)
    safe = np.maximum(alpha, 1e-3)[..., None]
    rgb = np.clip(on_black / safe, 0, 255)
    rgba = np.dstack([rgb, alpha * 255.0]).round().astype(np.uint8)
    rgba[alpha < 1 / 255] = 0
    return Image.fromarray(rgba, "RGBA")


def with_background(svg: str, colour: str) -> str:
    rect = f'<rect x="-100000" y="-100000" width="200000" height="200000" fill="{colour}"/>'
    return re.sub(r"(<svg\b[^>]*>)", r"\1" + rect, svg, count=1)


def render(src: pathlib.Path, size: int, kind: str, dest: pathlib.Path, tmp: pathlib.Path) -> None:
    svg = PIVOTS.sub("", src.read_text(encoding="utf-8"))
    png = tmp / (src.stem + ".final.png")
    if kind == "sprite":
        black = quicklook(with_background(svg, "#000"), src.stem + ".b.svg", size, tmp)
        white = quicklook(with_background(svg, "#fff"), src.stem + ".w.svg", size, tmp)
        matte(black, white).save(png)
        args = ["-alpha_q", "90", "-exact"]
    else:
        Image.fromarray(quicklook(svg, src.stem + ".svg", size, tmp).astype(np.uint8)).save(png)
        args = ["-noalpha"]
    subprocess.run(["cwebp", "-quiet", "-q", "82", "-m", "6", *args, str(png), "-o", str(dest)], check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    a = ap.parse_args()
    if not SRC.is_dir():
        sys.exit(f"Game art not found: {SRC} (set AOB_GAME_REPO)")
    for tool in ("qlmanage", "cwebp"):
        if not shutil.which(tool):
            sys.exit(f"{tool} is required")
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        tmp = pathlib.Path(t)
        for name, rel, size, kind in IMAGES:
            if a.only and a.only != name:
                continue
            dest = OUT / f"{name}.webp"
            render(SRC / rel, size, kind, dest, tmp)
            print(f"{dest.relative_to(ROOT)}  {dest.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
