#!/usr/bin/env python3
"""Mux each shot's render with its narration, concatenate, and write the episode deliverables.

Outputs in build/EPxx/: EPxx.mp4 (hard-burned subtitles by default + chapters, loudness-normalized),
EPxx.srt, chapters.txt. Use --soft-subs for soft subtitles track.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
import re
import subprocess
import sys
from pathlib import Path

PRESETS = {"preview": (854, 480), "draft": (1280, 720), "final": (1920, 1080)}
SUB_MAX = 20  # max CJK chars per subtitle line


def ffprobe_dur(p: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                          "default=nw=1:nk=1", str(p)], capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def split_sub(text: str) -> list[str]:
    text = text.strip().rstrip("。，；、")
    if len(text) <= SUB_MAX:
        return [text] if text else []
    parts = [p for p in re.split(r"(?<=[，、：；])", text) if p]
    out, cur = [], ""
    for p in parts:
        if cur and len(cur) + len(p) > SUB_MAX:
            out.append(cur); cur = p
        else:
            cur += p
    if cur:
        out.append(cur)
    final = []
    for o in out:  # hard-wrap pieces without punctuation
        while len(o) > SUB_MAX + 6:
            final.append(o[:SUB_MAX]); o = o[SUB_MAX:]
        final.append(o)
    return [f.rstrip("，、；") for f in final]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("episode")
    ap.add_argument("--work", default="work")
    ap.add_argument("--quality", default="preview", choices=list(PRESETS))
    ap.add_argument("--soft-subs", action="store_true", help="output soft subtitles track instead of burning into video")
    ap.add_argument("--burn-subs", action="store_true", default=True, help="kept for backwards compatibility")
    ap.add_argument("--bgm", help="optional music file, looped under narration")
    ap.add_argument("--bgm-db", type=float, default=-30.0)
    a = ap.parse_args(argv)
    work = Path(a.work)
    build = work / "build" / a.episode
    shots = json.loads((build / "shots.json").read_text(encoding="utf-8"))
    timing = json.loads((build / "timing.json").read_text(encoding="utf-8"))["shots"]
    W, H = PRESETS[a.quality]
    seg_dir = build / "segments"; seg_dir.mkdir(exist_ok=True)

    def mux_one(s):
        sid = s["id"]
        vid, aud = build / "renders" / f"{sid}.mp4", build / "audio" / f"{sid}.wav"
        if sid not in timing or not aud.exists():
            sys.exit(f"{sid}: no audio, run tools/tts.py first")
        if not vid.exists():
            sys.exit(f"{sid}: no render, run tools/render.py first")
        da, dv = timing[sid]["duration"], ffprobe_dur(vid)
        dur = max(da, dv)
        if dv > da + 0.3:
            print(f"WARN {sid}: video {dv:.2f}s longer than narration {da:.2f}s; padding audio")
        seg = seg_dir / f"{sid}.mp4"
        key = json.dumps([vid.stat().st_mtime_ns, vid.stat().st_size, aud.stat().st_mtime_ns,
                          aud.stat().st_size, W, H, round(da, 3)])
        stamp = seg.with_suffix(".key")
        if not seg.exists() or not stamp.exists() or stamp.read_text() != key:
            vf = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,"
                  f"fps=30,format=yuv420p,tpad=stop_mode=clone:stop_duration={max(0.0, da - dv) + 0.1:.3f}[v];"
                  f"[1:a]aresample=48000,apad[a]")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(vid), "-i", str(aud),
                            "-filter_complex", vf, "-map", "[v]", "-map", "[a]", "-t", f"{dur:.3f}",
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k",
                            "-ac", "2", str(seg)], check=True)
            stamp.write_text(key)

    with ThreadPoolExecutor(os.cpu_count() or 2) as pool:
        list(pool.map(mux_one, shots["shots"]))

    srt, chapters, listing, t0, n = [], [";FFMETADATA1"], [], 0.0, 1
    for s in shots["shots"]:
        sid = s["id"]
        seg = seg_dir / f"{sid}.mp4"
        dur = ffprobe_dur(seg)
        listing.append(f"file '{seg.resolve()}'")
        chapters += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(t0*1000)}", f"END={int((t0+dur)*1000)}",
                     f"title={s['sid']} {s['title']}"]
        for c in timing[sid]["chunks"]:
            lines = split_sub(c["text"])
            if not lines:
                continue
            total = sum(len(x) for x in lines)
            st = c["start"]
            for line in lines:
                en = st + (c["end"] - c["start"]) * len(line) / total
                prefix = "" if c["speaker"] == "n" else "（问）"
                srt.append(f"{n}\n{ts(t0 + st)} --> {ts(t0 + en)}\n{prefix}{line}\n")
                n += 1; st = en
        t0 += dur

    (build / "concat.txt").write_text("\n".join(listing) + "\n", encoding="utf-8")
    srt_path = build / f"{a.episode}.srt"; srt_path.write_text("\n".join(srt), encoding="utf-8")
    chap = build / "chapters.txt"; chap.write_text("\n".join(chapters) + "\n", encoding="utf-8")
    joined = build / "joined.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i",
                    str(build / "concat.txt"), "-c", "copy", str(joined)], check=True)

    burn_subs = not a.soft_subs
    ass_path = build / f"{a.episode}.ass"
    ass_header = (
        "[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: Default,Noto Sans CJK SC,46,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2.5,0,2,40,40,55,1\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )

    def srt_ts_to_ass(t):
        h, m, s_ms = t.split(":")
        s, ms = s_ms.split(",")
        return f"{int(h)}:{m}:{s}.{int(ms[:2]):02d}"

    ass_events = []
    for b in "\n".join(srt).strip().split("\n\n"):
        parts = b.strip().split("\n")
        if len(parts) >= 3 and "-->" in parts[1]:
            st_str, en_str = [x.strip() for x in parts[1].split("-->")]
            txt = "\\N".join(parts[2:])
            ass_events.append(f"Dialogue: 0,{srt_ts_to_ass(st_str)},{srt_ts_to_ass(en_str)},Default,,0,0,0,,{txt}")
    ass_path.write_text(ass_header + "\n".join(ass_events) + "\n", encoding="utf-8")

    out = build / f"{a.episode}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(joined)]
    afilter = "[0:a]loudnorm=I=-16:TP=-1.5:LRA=11[a]"
    if a.bgm:
        cmd += ["-stream_loop", "-1", "-i", a.bgm]
        afilter = (f"[1:a]volume={a.bgm_db}dB,aresample=48000[m];[0:a][m]amix=inputs=2:duration=first:"
                   f"dropout_transition=0,loudnorm=I=-16:TP=-1.5:LRA=11[a]")
    sub_idx = 2 if a.bgm else 1
    cmd += ["-i", str(srt_path), "-i", str(chap)]
    vmap = ["-map", "0:v"]
    if burn_subs:
        afilter += f";[0:v]ass={ass_path}[v]"
        vmap = ["-map", "[v]"]
    cmd += ["-filter_complex", afilter, *vmap, "-map", "[a]"]
    if not burn_subs:
        cmd += ["-map", f"{sub_idx}:s", "-c:s", "mov_text", "-metadata:s:s:0", "language=chi"]
    vcodec = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "0"] if burn_subs else ["-c:v", "copy"]
    cmd += ["-map_metadata", str(sub_idx + 1), "-map_chapters", str(sub_idx + 1),
            *vcodec,
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    joined.unlink(missing_ok=True)
    print(f"{a.episode}: {t0/60:.2f} min, {len(shots['shots'])} shots -> {out}")


if __name__ == "__main__":
    main()
