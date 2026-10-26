#!/usr/bin/env python3
"""Render every shot of an episode with Manim into build/EPxx/renders/<shot>.mp4.

Shots whose scene class is missing from work/scenes/EPxx.py (or with --animatic)
are rendered with manim_lib/autocard.py so the episode can always be assembled.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "manim_lib"
QUALITY = {
    "preview": ["-ql"],                                         # 854x480 15fps
    "draft": ["-r", "1280,720", "--frame_rate", "30"],
    "final": ["-r", "1920,1080", "--frame_rate", "30"],
}


def classes_in(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return set(re.findall(r"^class\s+(\w+)\s*\(", path.read_text(encoding="utf-8"), re.M))


def render_one(shot, a, work: Path, scene_file: Path, have: set[str]):
    build = work / "build" / a.episode
    cls = shot["scene"]
    use_auto = a.animatic or cls == "auto" or cls not in have
    file, klass = (LIB / "autocard.py", "AutoCard") if use_auto else (scene_file, cls)
    out = build / "renders" / f"{shot['id']}.mp4"
    log = build / "logs" / f"render_{shot['id']}.log"
    stamp = build / "renders" / f"{shot['id']}.key"
    import hashlib
    timing_file = build / "timing.json"
    t_hash = hashlib.sha256(timing_file.read_bytes()).hexdigest() if timing_file.exists() else ""
    f_hash = hashlib.sha256(file.read_bytes()).hexdigest() if file.exists() else ""
    key = json.dumps([f_hash, t_hash, a.quality, klass])

    if out.exists() and stamp.exists() and log.exists() and stamp.read_text() == key:
        warn = [l for l in log.read_text(encoding="utf-8").splitlines() if "[dvlib] WARN" in l]
        return shot["id"], True, ("autocard" if use_auto else klass) + ("; " + "; ".join(warn) if warn else "")

    media = build / "manim" / shot["id"]
    env = dict(os.environ, DV_WORK=str(work.resolve()), DV_SHOT=shot["id"], PYTHONPATH=str(LIB))
    cmd = [sys.executable, "-m", "manim", "render", str(file), klass, *QUALITY[a.quality],
           "--media_dir", str(media), "-o", shot["id"], "--disable_caching", "--progress_bar", "none"]
    p = subprocess.run(cmd, env=env, capture_output=True, text=True)
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(p.stdout + "\n" + p.stderr, encoding="utf-8")
    if p.returncode != 0:
        return shot["id"], False, f"manim failed, see {log}"
    vids = sorted(media.rglob(f"{shot['id']}.mp4"), key=lambda q: q.stat().st_mtime)
    if not vids:
        return shot["id"], False, f"no output mp4, see {log}"
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(vids[-1], out)
    stamp.write_text(key)
    warn = [l for l in (p.stdout + p.stderr).splitlines() if "[dvlib] WARN" in l]
    return shot["id"], True, ("autocard" if use_auto else klass) + ("; " + "; ".join(warn) if warn else "")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("episode")
    ap.add_argument("--work", default="work")
    ap.add_argument("--quality", default="preview", choices=list(QUALITY))
    ap.add_argument("--shots", help="comma list, e.g. S01,S04")
    ap.add_argument("--animatic", action="store_true", help="render every shot as an AutoCard")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 2)
    ap.add_argument("--allow-warn", action="store_true", help="let a final render pass with [dvlib] WARN")
    a = ap.parse_args(argv)
    work = Path(a.work)
    shots = json.loads((work / "build" / a.episode / "shots.json").read_text(encoding="utf-8"))["shots"]
    if a.shots:
        keep = {s if s.startswith("EP") else f"{a.episode}-{s}" for s in a.shots.split(",")}
        shots = [s for s in shots if s["id"] in keep]
    scene_file = work / "scenes" / f"{a.episode}.py"
    have = classes_in(scene_file)
    failed = warned = 0
    with ThreadPoolExecutor(a.jobs) as ex:
        for sid, ok, msg in ex.map(lambda s: render_one(s, a, work, scene_file, have), shots):
            print(f"{'OK  ' if ok else 'FAIL'} {sid}: {msg}")
            failed += not ok
            warned += msg.count("[dvlib] WARN")
    print(f"{a.episode}: {len(shots)} shots, {failed} failed, {warned} [dvlib] WARN")
    # G8: a final render with open warnings (late cues, layout) is not releasable.
    if a.quality == "final" and warned and not a.allow_warn:
        sys.exit(f"{warned} [dvlib] WARN in a final render; fix them or pass --allow-warn and log why in decisions.md")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
