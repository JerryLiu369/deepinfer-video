#!/usr/bin/env python3
"""Compare voiced timing with the script's design: per-shot length vs target, speaking rate per tone,
pause share, questioner density, episode total vs target. Writes build/EPxx/pacing.md.

Run after tts.py (make_episode.sh does). Exit 1 if any ERROR; WARNs go to the G7 review.
Rules: docs/03_NARRATION_STYLE.md sections 6 and 12.4, docs/10_REVIEW_CHECKLISTS.md G7.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from statistics import mean

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parse_script import spoken_len  # noqa: E402

SHOT_DEV = 0.30      # per-shot length vs target_s
EP_DEV = 0.15        # episode length vs target_min
TONE_DEV = 0.20      # a tone's rate vs the default narrator rate
CPS_DEV = 0.10       # default narrator rate vs voices.yaml cps (recalibrate when exceeded)
CARD_MAX_S = 8.0     # title / section cards
Q_EVERY = 6          # at least one Q line per this many shots


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("--work", default="work")
    a = ap.parse_args(argv)
    build = Path(a.work) / "build" / a.episode
    shots = json.loads((build / "shots.json").read_text(encoding="utf-8"))
    tm = json.loads((build / "timing.json").read_text(encoding="utf-8"))
    cfg = yaml.safe_load((Path(__file__).resolve().parent / "voices.yaml").read_text(encoding="utf-8"))
    backend = tm.get("backend", cfg.get("backend", "qwen"))
    cps_cfg = float((cfg.get(backend) or {}).get("cps") or 0)

    rows, errs, warns, by_tone = [], [], [], {}
    q_shots = []
    for k, s in enumerate(shots["shots"]):
        t = tm["shots"].get(s["id"])
        if not t:
            errs.append(f"ERROR {s['id']}: not voiced"); continue
        dur = float(t["duration"])
        chars = sum(spoken_len(c["spoken"]) for c in s["chunks"] if c["speaker"] == "n")
        speech = sum(c["end"] - c["start"] for c in t["chunks"] if c["speaker"] == "n")
        talk = sum(c["end"] - c["start"] for c in t["chunks"])
        cps = chars / speech if speech else 0.0
        tone = s.get("tone") or "n"
        if cps:
            by_tone.setdefault(tone, []).append(cps)
        nq = sum(1 for c in t["chunks"] if c["speaker"] == "q")
        if nq:
            q_shots.append(k)
        tgt = float(s.get("target_s") or 0)
        dev = (dur - tgt) / tgt if tgt else 0.0
        pause = 1 - talk / dur if dur else 0.0
        rows.append((s["id"], s["title"][:16], tone, tgt, dur, dev, cps, pause, nq))
        if tgt and abs(dev) > SHOT_DEV:
            warns.append(f"WARN  {s['id']}: {dur:.0f}s vs target {tgt:.0f}s ({dev:+.0%}); back to P4 if it stays")
        if tone == "card" and dur > CARD_MAX_S:
            warns.append(f"WARN  {s['id']}: card runs {dur:.0f}s (> {CARD_MAX_S:.0f}s)")
        if pause > 0.25:
            warns.append(f"WARN  {s['id']}: {pause:.0%} of the shot is silence")

    base = mean(by_tone.get("n", [0])) if by_tone.get("n") else 0.0
    if base and cps_cfg and abs(base - cps_cfg) / cps_cfg > CPS_DEV:
        warns.append(f"WARN  measured narrator rate {base:.2f} cps vs voices.yaml {backend}.cps {cps_cfg}; "
                     f"recalibrate (decisions.md) so estimates stop drifting")
    for tone, vals in sorted(by_tone.items()):
        if tone != "n" and base and abs(mean(vals) - base) / base > TONE_DEV:
            warns.append(f"WARN  tone '{tone}' reads at {mean(vals):.2f} cps vs narrator {base:.2f} "
                         f"({mean(vals) / base - 1:+.0%}); soften its instruction in voices.yaml")

    n = len(shots["shots"])
    need_q = max(1, n // Q_EVERY)
    if len(q_shots) < need_q:
        warns.append(f"WARN  {len(q_shots)} shot(s) with a Q line in {n} shots; plan about one every 3-5 shots "
                     f"(at least {need_q})")
    gaps = [b - a - 1 for a, b in zip([-1] + q_shots, q_shots + [n])]
    if q_shots and max(gaps) > 8:
        warns.append(f"WARN  {max(gaps)} shots in a row without a Q line")

    total = sum(r[4] for r in rows) / 60
    tgt_min = float(shots.get("target_min") or 0)
    if tgt_min and abs(total - tgt_min) / tgt_min > 0.35:
        warns.append(f"WARN episode {total:.1f} min vs target {tgt_min:.0f} min ({total / tgt_min - 1:+.0%})")

    out = [f"# {a.episode} 节奏报告（{backend}）", "",
           f"总时长 {total:.2f} 分钟；目标 {tgt_min:.0f} 分钟；解说实测 {base:.2f} 字/秒（voices.yaml {cps_cfg}）；"
           f"含 Q 的镜头 {len(q_shots)}/{n}", "",
           "| 镜头 | 标题 | tone | 目标 s | 实际 s | 偏差 | 字/秒 | 静音 | Q |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    out += [f"| {i} | {ti} | {to} | {tg:.0f} | {du:.1f} | {dv:+.0%} | {c:.2f} | {p:.0%} | {q} |"
            for i, ti, to, tg, du, dv, c, p, q in rows]
    out += ["", "## 各语气语速", ""] + [f"- `{k}`: {mean(v):.2f} 字/秒（{len(v)} 镜）" for k, v in sorted(by_tone.items())]
    out += ["", "## 问题", ""] + [f"- {x}" for x in errs + warns] + ([] if errs or warns else ["- 无"])
    (build / "pacing.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    for x in errs + warns:
        print(x)
    print(f"{a.episode}: {total:.2f} min, narrator {base:.2f} cps, Q in {len(q_shots)}/{n} shots, "
          f"{len(errs)} errors, {len(warns)} warnings -> {build / 'pacing.md'}")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
