#!/usr/bin/env python3
"""Synthesize narration per shot and write build/EPxx/timing.json (cue times, subtitle chunks).

Backends:
  qwen     (recommended, default) Alibaba Cloud Bailian Qwen-Audio-3.1-TTS-Plus via tools/qwen_tts.py.
           Needs DASHSCOPE_API_KEY etc. in deepinfer-video/.env. Supports tone instructions.
  edge     Microsoft Edge online TTS via the edge-tts package: no key, no tone control. Fallback.
  command  any local TTS; set DV_TTS_CMD, e.g.
           'python my_tts.py --speaker {speaker} --text-file {text} --out {out}'
Voices and tone presets live in tools/voices.yaml. A shot picks a narrator tone with
"tone: <preset>" in its metadata line; Q lines always use the questioner tone.
Chunk audio is cached by content hash (backend, model, voice, tone, rate, text), so re-running
after a script edit only re-synthesizes changed sentences.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import shlex
import subprocess
import sys
import wave
from pathlib import Path

import yaml

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
from parse_script import GAP_S, LEAD_S, TAIL_S  # noqa: E402
import qwen_tts  # noqa: E402

SR = 24000
BACKENDS = ["qwen", "edge", "command"]
DEFAULT_JOBS = {"qwen": 2, "edge": 6, "command": 2}


def load_voices() -> dict:
    p = TOOLS / "voices.yaml"
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def ffmpeg_to_wav(src: Path, dst: Path):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", str(SR),
                    "-sample_fmt", "s16", str(dst)], check=True)


async def synth_edge(text: str, voice: str, rate: str, out_wav: Path):
    import edge_tts
    tmp = out_wav.with_suffix(".mp3")
    for attempt in range(4):
        try:
            await edge_tts.Communicate(text, voice, rate=rate).save(str(tmp))
            break
        except Exception as e:  # network hiccups are common
            if attempt == 3:
                raise
            print(f"  retry {attempt + 1}: {e}")
            await asyncio.sleep(2 * (attempt + 1))
    ffmpeg_to_wav(tmp, out_wav)
    tmp.unlink(missing_ok=True)


def synth_qwen(text: str, speaker: str, voice: str, instruction: str, out_wav: Path):
    raw = out_wav.with_suffix(".raw.wav")
    qwen_tts.synthesize(text, raw, speaker=speaker, voice=voice, instruction=instruction)
    ffmpeg_to_wav(raw, out_wav)  # normalize whatever the service returns to 24 kHz mono s16
    raw.unlink(missing_ok=True)


def synth_command(text: str, speaker: str, out_wav: Path):
    tmpl = os.environ.get("DV_TTS_CMD")
    if not tmpl:
        sys.exit("backend=command needs DV_TTS_CMD")
    txt = out_wav.with_suffix(".txt")
    txt.write_text(text, encoding="utf-8")
    raw = out_wav.with_suffix(".raw.wav")
    cmd = tmpl.format(text=shlex.quote(str(txt)), out=shlex.quote(str(raw)), speaker=speaker)
    subprocess.run(cmd, shell=True, check=True)
    ffmpeg_to_wav(raw, out_wav)
    raw.unlink(missing_ok=True); txt.unlink(missing_ok=True)


def wav_frames(p: Path) -> bytes:
    with wave.open(str(p), "rb") as w:
        assert w.getframerate() == SR and w.getnchannels() == 1 and w.getsampwidth() == 2, p
        return w.readframes(w.getnframes())


def silence(sec: float) -> bytes:
    return b"\x00\x00" * int(round(sec * SR))


def resolve(a) -> dict:
    """Pick backend, voices, tone table and model; fail early with a clear message."""
    qwen_tts.load_env()
    cfg = load_voices()
    backend = a.backend or os.environ.get("DV_TTS_BACKEND") or cfg.get("backend") or "qwen"
    if backend not in BACKENDS:
        sys.exit(f"unknown backend '{backend}' (choose from {BACKENDS})")
    section = cfg.get(backend) or {}
    voices = dict(section.get("voices") or {})
    if backend == "qwen":
        voices = {**qwen_tts.FALLBACK_VOICES, **voices}
    if a.voice_n:
        voices["n"] = a.voice_n
    if a.voice_q:
        voices["q"] = a.voice_q
    tones, model = {}, ""
    if backend == "qwen":
        st = qwen_tts.settings()
        if not st["api_key"]:
            sys.exit("backend qwen needs DASHSCOPE_API_KEY (deepinfer-video/.env, see .env.example); "
                     "for a no-key build use --backend edge")
        tones = qwen_tts.voice_config()["tones"]
        model = st["model"]
        if a.rate != "+0%":
            print("NOTE  --rate is ignored by the qwen backend; pace is set by the tone instruction")
    elif backend == "edge" and not voices:
        voices = {"n": "zh-CN-YunxiNeural", "q": "zh-CN-XiaoxiaoNeural"}
    return {"backend": backend, "voices": voices, "tones": tones, "model": model}


def instruction_for(r: dict, speaker: str, tone: str) -> str:
    if r["backend"] != "qwen":
        return ""
    if speaker == "q":
        return r["tones"]["q"]
    if tone and tone not in r["tones"]:
        sys.exit(f"tone '{tone}' is not defined in tools/voices.yaml (qwen.tones)")
    return r["tones"][tone or "n"]


async def run(a):
    r = resolve(a)
    work = Path(a.work)
    build = work / "build" / a.episode
    shots = json.loads((build / "shots.json").read_text(encoding="utf-8"))["shots"]
    if a.shots:
        keep = {f"{a.episode}-{s}" if not s.startswith("EP") else s for s in a.shots.split(",")}
        shots_todo = [s for s in shots if s["id"] in keep]
    else:
        shots_todo = shots
    cache = build / "audio" / "cache"
    cache.mkdir(parents=True, exist_ok=True)
    voices = r["voices"]
    sem = asyncio.Semaphore(a.jobs or DEFAULT_JOBS[r["backend"]])
    print(f"TTS backend={r['backend']} model={r['model'] or '-'} voices={voices}")

    def instr(c, s):
        return instruction_for(r, c["speaker"], s.get("tone", ""))

    def key(c, s):
        rate = a.rate if r["backend"] == "edge" else ""
        ident = f"{r['backend']}|{r['model']}|{voices.get(c['speaker'], c['speaker'])}|{instr(c, s)}|{rate}|{c['spoken']}"
        return cache / f"{hashlib.sha1(ident.encode()).hexdigest()[:16]}.wav"

    async def one(c, s):
        out = key(c, s)
        if out.exists() or not c["spoken"].strip():
            return
        async with sem:
            if r["backend"] == "edge":
                await synth_edge(c["spoken"], voices[c["speaker"]], a.rate, out)
            elif r["backend"] == "qwen":
                await asyncio.to_thread(synth_qwen, c["spoken"], c["speaker"], voices[c["speaker"]],
                                        instr(c, s), out)
            else:
                await asyncio.to_thread(synth_command, c["spoken"], c["speaker"], out)

    await asyncio.gather(*[one(c, s) for s in shots_todo for c in s["chunks"]])

    timing_path = build / "timing.json"
    timing = json.loads(timing_path.read_text(encoding="utf-8")) if timing_path.exists() else {"shots": {}}
    timing.update({"episode": a.episode, "backend": r["backend"], "model": r["model"], "voices": voices,
                   "rate": a.rate if r["backend"] == "edge" else None})
    for s in shots_todo:
        pcm, t, cues, chunks = [silence(LEAD_S)], LEAD_S, {}, []
        for i, c in enumerate(s["chunks"]):
            gap = (GAP_S if i else 0.0) + c["pause_before"]
            pcm.append(silence(gap)); t += gap
            for name in c["cues_before"]:
                cues[name] = round(t, 3)
            if not c["spoken"].strip():
                continue
            frames = wav_frames(key(c, s))
            dur = len(frames) / 2 / SR
            pcm.append(frames)
            chunks.append({"start": round(t, 3), "end": round(t + dur, 3), "text": c["written"],
                           "speaker": c["speaker"]})
            t += dur
        pcm.append(silence(TAIL_S)); t += TAIL_S
        out = build / "audio" / f"{s['id']}.wav"
        pcm_bytes = b"".join(pcm)
        if not out.exists() or out.stat().st_size != len(pcm_bytes) + 44:
            with wave.open(str(out), "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
                w.writeframes(pcm_bytes)
        entry = {"duration": round(t, 3), "cues": cues, "chunks": chunks}
        if r["backend"] == "qwen":
            entry["tone"] = s.get("tone") or "n"
        timing["shots"][s["id"]] = entry
        flag = ""
        if s["target_s"] and abs(t - s["target_s"]) / s["target_s"] > 0.3:
            flag = f"  (target {s['target_s']:.0f}s)"
        print(f"{s['id']}: {t:6.2f}s  cues={list(cues)}{flag}")
    order = [s["id"] for s in shots]
    timing["shots"] = {k: timing["shots"][k] for k in order if k in timing["shots"]}
    new_timing_text = json.dumps(timing, ensure_ascii=False, indent=1) + "\n"
    if not timing_path.exists() or timing_path.read_text(encoding="utf-8") != new_timing_text:
        timing_path.write_text(new_timing_text, encoding="utf-8")
    total = sum(v["duration"] for v in timing["shots"].values())
    print(f"{a.episode}: narration total {total/60:.2f} min -> {timing_path}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("--work", default="work")
    ap.add_argument("--shots", help="comma list, e.g. S01,S04")
    ap.add_argument("--backend", choices=BACKENDS,
                    help="default: $DV_TTS_BACKEND, else 'backend' in tools/voices.yaml (qwen)")
    ap.add_argument("--voice-n", default=os.environ.get("DV_VOICE_N"), help="narrator voice (default: voices.yaml)")
    ap.add_argument("--voice-q", default=os.environ.get("DV_VOICE_Q"), help="questioner voice (default: voices.yaml)")
    ap.add_argument("--rate", default=os.environ.get("DV_TTS_RATE", "+0%"), help="edge only, e.g. +5%%")
    ap.add_argument("--jobs", type=int, default=None, help="parallel requests (default: qwen 4, edge 6)")
    asyncio.run(run(ap.parse_args(argv)))


if __name__ == "__main__":
    main()
