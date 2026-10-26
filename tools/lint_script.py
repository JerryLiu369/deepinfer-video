#!/usr/bin/env python3
"""Lint an episode script against the fact ledger and the narration rules.

Exit 1 if any ERROR. Rules: docs/03_NARRATION_STYLE.md, docs/06_FACT_PROTOCOL.md.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parse_script import parse_script  # noqa: E402

FORBIDDEN = ["赋能", "助力", "全方位", "多维度", "深度融合", "极致", "颠覆", "革命性", "里程碑", "底层逻辑",
             "抓手", "闭环", "打通", "生态位", "降本增效", "值得注意的是", "不难看出", "综上所述", "众所周知",
             "毋庸置疑", "扮演着", "起到了", "具有重要意义", "黑科技", "炸裂", "吊打", "遥遥领先", "不可思议",
             "暴力", "腰斩", "震撼", "彻底理解", "彻底搞懂", "彻底明白", "一文读懂"]
GRADE_ORDER = "ABCDE"
OK_STATUS = {"verified", "verified_with_caveat"}
WEAK_STATUS = {"unverifiable"}


def load_facts(work: Path) -> dict:
    facts = {}
    for p in sorted((work / "facts").glob("*.yaml")):
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        for f in data.get("facts", []) or []:
            if f.get("id") in facts:
                print(f"ERROR facts: duplicate id {f['id']} in {p.name}")
            facts[f["id"]] = {**f, "_file": p.name}
    return facts


def tone_presets() -> set:
    p = Path(__file__).resolve().parent / "voices.yaml"
    if not p.exists():
        return set()
    cfg = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return set(((cfg.get("qwen") or {}).get("tones") or {}).keys())


def outline_minutes(episode: str) -> float:
    """Episode length promised in docs/02_EPISODE_OUTLINE.md, e.g. '## EP07 ...（18 分钟）'."""
    p = Path(__file__).resolve().parent.parent / "docs" / "02_EPISODE_OUTLINE.md"
    if not p.exists():
        return 0.0
    m = re.search(rf"^## {episode}\b.*?（(\d+(?:\.\d+)?) 分钟）", p.read_text(encoding="utf-8"), re.M)
    return float(m.group(1)) if m else 0.0


def scene_cues(scene_file: Path) -> dict:
    if not scene_file.exists():
        return {}
    src = scene_file.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"^class\s+(\w+)\s*\(", src, re.M):
        start = m.end()
        nxt = re.search(r"^class\s+\w+\s*\(", src[start:], re.M)
        body = src[start:start + nxt.start()] if nxt else src[start:]
        out[m.group(1)] = set(re.findall(r"""until\(\s*["']([A-Za-z0-9_]+)["']""", body))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("episode")
    ap.add_argument("--work", default="work")
    a = ap.parse_args(argv)
    work = Path(a.work)
    data = parse_script(work / "scripts" / f"{a.episode}.md")
    facts = load_facts(work)
    cues_by_class = scene_cues(work / "scenes" / f"{a.episode}.py")
    tones = tone_presets()
    errors, warns, ascii_terms = [], [], set()

    def E(shot, msg): errors.append(f"ERROR {shot['id']} (L{shot['line']}): {msg}")
    def W(shot, msg): warns.append(f"WARN  {shot['id']} (L{shot['line']}): {msg}")

    seen = set()
    for s in data["shots"]:
        if s["id"] in seen:
            E(s, "duplicate shot id")
        seen.add(s["id"])
        if not s["chunks"] or not s["narration_written"].strip():
            if s["type"] != "silent":
                E(s, "no narration (use type: silent for intentional silence)")
        if not s["target_s"]:
            W(s, "missing target_s")
        elif s["est_s"] and abs(s["est_s"] - s["target_s"]) / s["target_s"] > 0.3:
            W(s, f"estimated {s['est_s']:.0f}s vs target {s['target_s']:.0f}s")
        if s["scope"] not in {"oss", "doc", "mixed", "general"}:
            E(s, f"scope must be oss|doc|mixed|general, got '{s['scope']}'")
        tone = s.get("tone", "")
        if tone == "card" and s["target_s"] and s["target_s"] > 8:
            W(s, f"card shot target_s {s['target_s']:.0f} (> 8s); a title card is read, not explained")
        if tone and tone not in tones:
            E(s, f"tone '{tone}' is not a preset in tools/voices.yaml: {sorted(tones - {'q'})}")
        elif tone == "q":
            E(s, "tone 'q' is reserved for Q lines; pick a narrator preset")

        written = s["narration_written"]
        has_number = bool(re.search(r"\d", written + "".join(s["screen_text"])))
        if has_number and not s["facts"]:
            E(s, "narration/screen text has numbers but cites no fact")
        grades = []
        for fid in s["facts"]:
            f = facts.get(fid)
            if not f:
                E(s, f"fact {fid} not in work/facts/*.yaml"); continue
            st = f.get("status", "")
            if st in WEAK_STATUS:
                W(s, f"fact {fid} is 'unverifiable': narration must say it is unconfirmed")
            elif st not in OK_STATUS:
                E(s, f"fact {fid} status '{st}' is not usable (needs verified / verified_with_caveat)")
            g = str(f.get("grade", "")).upper()
            if g == "D":
                W(s, f"fact {fid} is grade D: only as '有说法认为…', never as fact")
            if g:
                grades.append(g)
        if s["facts"] and s["badge"] not in GRADE_ORDER:
            E(s, "shot cites facts but has no badge: A|B|C|D|E")
        if grades and s["badge"] in GRADE_ORDER:
            weakest = max(grades, key=GRADE_ORDER.index)
            if GRADE_ORDER.index(s["badge"]) < GRADE_ORDER.index(weakest):
                W(s, f"badge {s['badge']} is stronger than weakest cited fact grade {weakest}")

        for word in FORBIDDEN:
            if word in written or any(word in t for t in s["screen_text"]):
                E(s, f"forbidden word '{word}'")
        for sent in re.split(r"[。！？；!?]", written):
            n = len(sent.strip())
            if n > 60:
                E(s, f"sentence {n} chars (>60): {sent[:24]}…")
            elif n > 42:
                W(s, f"sentence {n} chars (>42): {sent[:24]}…")
        for c in s["chunks"]:
            for tok in re.findall(r"[A-Za-z][A-Za-z0-9.+\-]*", c["spoken"]):
                if len(tok) >= 2 and tok.isupper() or re.search(r"\d", tok):
                    ascii_terms.add(tok)
            if re.search(r"\d,\d{3}", c["spoken"]):
                W(s, f"digit group with comma will be read badly, use {{written|spoken}}: {c['written'][:30]}")
        for line in s["screen_text"]:
            if len(line) > 20:
                W(s, f"screen text line {len(line)} chars (>20): {line}")
        if len(s["screen_text"]) > 4:
            W(s, "more than 4 screen-text lines")

        cls = s["scene"]
        if cls in cues_by_class:
            missing = cues_by_class[cls] - set(s["est_cues"])
            if missing:
                E(s, f"scene {cls} waits for cues not in narration: {sorted(missing)}")

    q_shots = [k for k, s in enumerate(data["shots"]) if any(c["speaker"] == "q" for c in s["chunks"])]
    need_q = max(1, len(data["shots"]) // 6)
    if len(q_shots) < need_q:
        warns.append(f"WARN  only {len(q_shots)} shot(s) with a Q line in {len(data['shots'])} shots; "
                     f"plan one every 3-5 shots (docs/03 section 6)")

    total = sum(s["est_s"] for s in data["shots"]) / 60
    promised = outline_minutes(a.episode)
    if promised and data["target_min"] and abs(data["target_min"] - promised) / promised > 0.25:
        msg = f"target_min {data['target_min']:.0f} differs from the outline's {promised:.0f} min (docs/02)"
        warns.append(f"WARN  {a.episode}: {msg}")
    for line in errors + warns:
        print(line)
    if ascii_terms:
        print("INFO  uppercase/digit tokens TTS will read as-is (add to tools/lexicon.yaml if wrong): "
              + ", ".join(sorted(ascii_terms)))
    tgt = data["target_min"]
    if tgt and abs(total - tgt) / tgt > 0.2:
        print(f"WARN  episode estimated {total:.1f} min vs target {tgt:.0f} min")
    print(f"{a.episode}: {len(data['shots'])} shots, est {total:.1f} min, {len(errors)} errors, {len(warns)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
