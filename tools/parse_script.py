#!/usr/bin/env python3
"""Parse work/scripts/EPxx.md (format: docs/05_FORMATS.md section 4) into build/EPxx/shots.json."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

TOOLS = Path(__file__).resolve().parent
SHOT_RE = re.compile(r"^##\s+(S\d{2,3})\s*(.*)$")
META_RE = re.compile(r"<!--\s*shot:\s*(.*?)\s*-->")
EP_RE = re.compile(r"<!--\s*episode:\s*(.*?)\s*-->")
SECTION_RE = re.compile(r"^\*\*(画面|屏幕字|旁白|备注)\*\*\s*[：:]\s*(.*)$")
INLINE_RE = re.compile(r"\{([^{}|]+)\|([^{}]+)\}")
MARK_RE = re.compile(r"(\[#[A-Za-z0-9_]+\]|\[pause:[0-9.]+\])")
SENT_RE = re.compile(r"(?<=[。！？；!?])")
SPEAKER_RE = re.compile(r"^(Q|N)\s*[：:]\s*")

def _cps() -> float:
    """Speaking rate for duration estimates: $DV_CPS, else the active backend's cps in voices.yaml."""
    if os.environ.get("DV_CPS"):
        return float(os.environ["DV_CPS"])
    p = TOOLS / "voices.yaml"
    if yaml is not None and p.exists():
        cfg = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        backend = os.environ.get("DV_TTS_BACKEND") or cfg.get("backend") or "qwen"
        cps = (cfg.get(backend) or {}).get("cps")
        if cps:
            return float(cps)
    return 3.8


CPS = _cps()       # spoken chars per second as counted by spoken_len(); calibrate in P0
GAP_S = 0.12       # silence between chunks
LEAD_S = 0.35      # silence before first chunk
TAIL_S = 0.6       # silence after last chunk


def load_lexicon(path: Path | None = None) -> list[tuple[re.Pattern, str]]:
    path = path or TOOLS / "lexicon.yaml"
    if not path.exists() or yaml is None:
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    items = sorted(data.items(), key=lambda kv: -len(str(kv[0])))
    out = []
    for k, v in items:
        k = str(k)
        pat = re.escape(k)
        if re.match(r"[A-Za-z0-9]", k[0]):
            pat = r"(?<![A-Za-z0-9_])" + pat
        if re.match(r"[A-Za-z0-9]", k[-1]):
            pat = pat + r"(?![A-Za-z0-9_])"
        out.append((re.compile(pat), str(v)))
    return out


def to_written_spoken(text: str, lexicon) -> tuple[str, str]:
    """Resolve {written|spoken} markup, then apply the lexicon only outside inline markup."""
    pieces_w, pieces_s, protected = [], [], []
    pos = 0
    for m in INLINE_RE.finditer(text):
        pieces_w.append(text[pos:m.start()]); pieces_s.append(text[pos:m.start()])
        pieces_w.append(m.group(1)); pieces_s.append(f"\x00{len(protected)}\x00")
        protected.append(m.group(2))
        pos = m.end()
    pieces_w.append(text[pos:]); pieces_s.append(text[pos:])
    written = "".join(pieces_w)
    spoken = "".join(pieces_s)
    for pat, rep in lexicon:
        spoken = pat.sub(rep, spoken)
    spoken = re.sub(r"\x00(\d+)\x00", lambda m: protected[int(m.group(1))], spoken)
    return written, spoken


def spoken_len(s: str) -> float:
    cjk = len(re.findall(r"[\u4e00-\u9fff]", s))
    words = re.findall(r"[A-Za-z]+", s)
    digits = re.findall(r"\d+", s)
    return cjk + sum(max(1.0, len(w) * 0.45) for w in words) + sum(len(d) * 0.9 for d in digits)


def chunk_narration(lines: list[str], lexicon) -> list[dict]:
    chunks, pending_cues, pending_pause = [], [], 0.0
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        speaker = "n"
        m = SPEAKER_RE.match(line)
        if m:
            speaker = m.group(1).lower()
            line = line[m.end():]
        for part in MARK_RE.split(line):
            if not part:
                continue
            if part.startswith("[#"):
                pending_cues.append(part[2:-1]); continue
            if part.startswith("[pause:"):
                pending_pause += float(part[7:-1]); continue
            for sent in SENT_RE.split(part):
                if not sent.strip():
                    continue
                w, s = to_written_spoken(sent.strip(), lexicon)
                chunks.append({"speaker": speaker, "written": w, "spoken": s,
                               "cues_before": pending_cues, "pause_before": pending_pause})
                pending_cues, pending_pause = [], 0.0
    if pending_cues or pending_pause:
        chunks.append({"speaker": "n", "written": "", "spoken": "", "cues_before": pending_cues,
                       "pause_before": pending_pause})
    return chunks


def estimate(chunks: list[dict]) -> tuple[float, dict]:
    t, cues = LEAD_S, {}
    for i, c in enumerate(chunks):
        if i:
            t += GAP_S
        t += c["pause_before"]
        for name in c["cues_before"]:
            cues[name] = round(t, 3)
        t += spoken_len(c["spoken"]) / CPS
    return round(t + TAIL_S, 2), cues


def parse_meta(s: str) -> dict:
    out = {}
    for item in s.split("|"):
        if ":" in item:
            k, v = item.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def parse_script(path: Path, lexicon=None) -> dict:
    lexicon = load_lexicon() if lexicon is None else lexicon
    text = path.read_text(encoding="utf-8")
    ep = path.stem
    ep_meta, title = {}, ""
    shots, cur, section = [], None, None
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        m = EP_RE.search(line)
        if m and cur is None:
            ep_meta = parse_meta(m.group(1)); continue
        m = SHOT_RE.match(line)
        if m:
            cur = {"sid": m.group(1), "title": m.group(2).strip(), "line": lineno, "meta": {},
                   "visual": [], "screen_text": [], "narration": [], "notes": []}
            shots.append(cur); section = None
            continue
        if cur is None:
            continue
        m = META_RE.search(line)
        if m and not cur["meta"]:
            cur["meta"] = parse_meta(m.group(1)); continue
        m = SECTION_RE.match(line)
        if m:
            section = {"画面": "visual", "屏幕字": "screen_text", "旁白": "narration", "备注": "notes"}[m.group(1)]
            if m.group(2).strip():
                cur[section].append(m.group(2).strip())
            continue
        if line.startswith("---"):
            section = None; continue
        if section:
            if section == "screen_text":
                s = line.strip()
                if s.startswith("- "):
                    cur[section].append(s[2:].strip())
            elif line.strip() or section == "narration":
                cur[section].append(line.rstrip())

    out_shots = []
    for s in shots:
        meta = s["meta"]
        sid = meta.get("shot", s["sid"])
        chunks = chunk_narration(s["narration"], lexicon)
        est_s, est_cues = estimate(chunks)
        facts = [f.strip() for f in meta.get("facts", "").split(",") if f.strip() and f.strip() != "-"]
        out_shots.append({
            "id": f"{ep}-{sid}", "sid": sid, "title": s["title"], "line": s["line"],
            "target_s": float(meta.get("target_s", 0) or 0), "facts": facts,
            "badge": meta.get("badge", "").upper(), "scope": meta.get("scope", ""),
            "scene": meta.get("scene", f"{ep}_{sid}"), "type": meta.get("type", "anim"),
            "tone": meta.get("tone", ""),
            "visual": "\n".join(s["visual"]).strip(), "screen_text": s["screen_text"],
            "notes": "\n".join(s["notes"]).strip(),
            "narration_written": "".join(c["written"] for c in chunks),
            "chunks": chunks, "est_s": est_s, "est_cues": est_cues,
        })
    return {"episode": ep, "title": title, "target_min": float(ep_meta.get("target_min", 0) or 0),
            "meta": ep_meta, "shots": out_shots}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("episode", help="e.g. EP07")
    ap.add_argument("--work", default="work")
    a = ap.parse_args(argv)
    work = Path(a.work)
    src = work / "scripts" / f"{a.episode}.md"
    if not src.exists():
        sys.exit(f"missing {src}")
    data = parse_script(src)
    out = work / "build" / a.episode / "shots.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(s["est_s"] for s in data["shots"])
    print(f"{a.episode}: {len(data['shots'])} shots, est {total/60:.1f} min -> {out}")


if __name__ == "__main__":
    main()
