#!/usr/bin/env python3
"""Copies chosen in-game screenshots into assets/shots/ as WebP (half size, 390×844).

The screenshots come from the game's own PlayMode test runs (game/Logs/screenshots in the game repo): they are real
frames of the current build, captured in Turkish. The list below is the single place that picks them; build.py shows
a realm's shots on pages in the language they were captured in.

    .venv/bin/python scripts/shots.py
"""
import os, pathlib, subprocess, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
GAME = pathlib.Path(os.environ.get("AOB_GAME_REPO", ROOT.parent / "blades-of-ages"))
SRC = GAME / "game/Logs/screenshots"
OUT = ROOT / "assets/shots"
SIZE = (390, 844)

# output name: source file
SHOTS = {
    "gobeklitepe-1": "showcase-gobeklitepe-30s.png", "gobeklitepe-2": "showcase-gobeklitepe-48s.png",
    "sumer-1": "showcase-sumer-30s.png", "sumer-2": "showcase-humbaba-75s.png",
    "misir-1": "showcase-misir-30s.png", "misir-2": "showcase-apep-30s.png",
    "yunan-1": "yunan-walls.png", "yunan-2": "yunan-medusa-gaze.png",
    "hitit-1": "hitit-lightning.png", "hitit-2": "hitit-illuyanka-coil.png",
    "iskandinav-1": "iskandinav-ponds.png", "iskandinav-2": "iskandinav-fenrir-chain.png",
    "hero-select": "showcase-select.png", "map": "showcase-hub.png",
}


def main() -> None:
    if not SRC.is_dir():
        sys.exit(f"screenshots not found: {SRC} (set AOB_GAME_REPO)")
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / "_tmp.png"
    for name, src in SHOTS.items():
        Image.open(SRC / src).convert("RGB").resize(SIZE, Image.LANCZOS).save(tmp)
        dest = OUT / f"{name}.webp"
        subprocess.run(["cwebp", "-quiet", "-q", "78", "-m", "6", str(tmp), "-o", str(dest)], check=True)
        print(f"{dest.relative_to(ROOT)}  {dest.stat().st_size // 1024} KB")
    tmp.unlink()


if __name__ == "__main__":
    main()
