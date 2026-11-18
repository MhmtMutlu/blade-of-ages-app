#!/usr/bin/env python3
"""Cuts the game's fonts (Baloo 2, Nunito; SIL OFL) into Latin and Latin Extended WOFF2 subsets for the site.

Needs fontTools + brotli (not a dependency of build.py; run only when the fonts change):
    python3 -m venv .venv && .venv/bin/pip install fonttools brotli
    .venv/bin/python scripts/subset-fonts.py

Source: the game repository's Assets/_Project/Art/Fonts (../blades-of-ages or AOB_GAME_REPO).
Output: assets/fonts/<face>-<subset>.woff2 and the OFL licences. CJK pages use system fonts (no web font).
The unicode ranges must match the @font-face blocks in assets/site.css.
"""
import os, pathlib, shutil
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
GAME = pathlib.Path(os.environ.get("AOB_GAME_REPO", ROOT.parent / "blades-of-ages"))
SRC = GAME / "game" / "Assets" / "_Project" / "Art" / "Fonts"
OUT = ROOT / "assets" / "fonts"

RANGES = {
    "latin": "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,"
             "U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD",
    "latinext": "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,"
                "U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF",
}
FACES = {"baloo2-800": "Baloo2-ExtraBold.ttf", "nunito-600": "Nunito-SemiBold.ttf", "nunito-800": "Nunito-ExtraBold.ttf"}


def unicodes(spec: str) -> list[int]:
    cps = []
    for part in spec.split(","):
        part = part.strip()[2:]
        lo, _, hi = part.partition("-")
        cps.extend(range(int(lo, 16), int(hi or lo, 16) + 1))
    return cps


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for face, file in FACES.items():
        for name, spec in RANGES.items():
            font = TTFont(SRC / file)
            opts = subset.Options()
            opts.flavor = "woff2"
            opts.layout_features = ["*"]
            sub = subset.Subsetter(opts)
            sub.populate(unicodes=unicodes(spec))
            sub.subset(font)
            dest = OUT / f"{face}-{name}.woff2"
            font.flavor = "woff2"
            font.save(dest)
            print(f"{dest.relative_to(ROOT)}  {dest.stat().st_size // 1024} KB")
    for lic in ("OFL-Baloo2.txt", "OFL-Nunito.txt"):
        shutil.copy(SRC / lic, OUT / lic)


if __name__ == "__main__":
    main()
