#!/usr/bin/env python3
"""Extract review stills for each shot (at every cue, mid-shot and end) plus contact sheets.

Output: build/EPxx/keyframes/<shot>_<tag>.png, sheet_NN.png and index.md
(the art-director agent reviews these instead of watching the video).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def vid_dur(p: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                          "default=nw=1:nk=1", str(p)], capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def grab(video: Path, t: float, out: Path):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(t, 0):.3f}", "-i", str(video),
                    "-frames:v", "1", str(out)], check=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("episode")
    ap.add_argument("--work", default="work")
    a = ap.parse_args(argv)
    build = Path(a.work) / "build" / a.episode
    shots = json.loads((build / "shots.json").read_text(encoding="utf-8"))["shots"]
    tpath = build / "timing.json"
    timing = json.loads(tpath.read_text(encoding="utf-8"))["shots"] if tpath.exists() else {}
    kdir = build / "keyframes"
    if kdir.exists():
        shutil.rmtree(kdir)
    seq = kdir / "seq"; seq.mkdir(parents=True)
    index, k = [f"# {a.episode} keyframes\n", "| # | 文件 | 镜头 | 时刻 | 此刻旁白 |", "|---|---|---|---|---|"], 0
    for s in shots:
        vid = build / "renders" / f"{s['id']}.mp4"
        if not vid.exists():
            continue
        tm = timing.get(s["id"], {"duration": s["est_s"], "cues": s["est_cues"], "chunks": []})
        dur = min(tm["duration"], vid_dur(vid))
        points = [(f"cue-{c}", t + 0.6) for c, t in tm["cues"].items()] + [("mid", dur / 2), ("end", dur - 0.15)]
        for tag, t in sorted(points, key=lambda p: p[1]):
            k += 1
            out = kdir / f"{s['id']}_{tag}.png"
            grab(vid, min(t, dur - 0.1), out)
            shutil.copy2(out, seq / f"{k:04d}.png")
            said = next((c["text"] for c in tm.get("chunks", []) if c["start"] <= t <= c["end"] + 0.12), "")
            index.append(f"| {k} | {out.name} | {s['sid']} {s['title']} | {t:.1f}s | {said} |")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(seq / "%04d.png"),
                    "-vf", "scale=480:-1,tile=4x3:padding=6:color=0x30363D", str(kdir / "sheet_%02d.png")],
                   check=True)
    shutil.rmtree(seq)
    (kdir / "index.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"{a.episode}: {k} keyframes -> {kdir}")


if __name__ == "__main__":
    main()
