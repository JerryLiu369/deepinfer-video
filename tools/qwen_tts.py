#!/usr/bin/env python3
"""Qwen-Audio-3.1-TTS-Plus synthesizer (Alibaba Cloud Bailian / DashScope) for the DeepInfer video pipeline.

Used two ways:
  - as a module by tools/tts.py (backend "qwen", the recommended backend);
  - as a CLI for one-off tests:
      python tools/qwen_tts.py --text "你好" --out /tmp/t.wav [--speaker n|q] [--voice ID] [--instruction "..."]

Configuration comes from the environment, with deepinfer-video/.env loaded first
(existing environment variables win). Keys: DASHSCOPE_API_KEY (required), DASHSCOPE_ENDPOINT,
DASHSCOPE_MODEL, DASHSCOPE_PROXY (unset or empty = direct connection), DASHSCOPE_IPV4_ONLY
(default 1: resolve hosts to IPv4 only, for IP-whitelisted endpoints). Voices and tone
instructions default to tools/voices.yaml. Output: whatever the service returns for format=wav, sample_rate=24000;
tools/tts.py re-encodes it to 24 kHz mono s16 before use.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent

DEFAULT_ENDPOINT = "https://llm-8lerj76ycab56lsy.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer"
DEFAULT_MODEL = "qwen-audio-3.1-tts-plus"
FALLBACK_VOICES = {"n": "longanhuan_v3.1", "q": "longanlingxin_v3.1"}
FALLBACK_TONES = {"n": "沉稳、清晰、富有逻辑的科技讲解口吻", "q": "好奇、探究、求真的提问口吻"}
RETRY_STATUS = {429, 500, 502, 503, 504}


def load_env(paths: list[Path] | None = None) -> None:
    """Minimal .env reader: KEY=VALUE lines, '#' comments, optional quotes. Never overrides os.environ."""
    for p in paths or [ROOT / ".env", Path.cwd() / ".env"]:
        if not p.is_file():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip().removeprefix("export ").strip(), v.strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
                v = v[1:-1]
            os.environ.setdefault(k, v)


def voice_config() -> dict:
    """The qwen section of tools/voices.yaml, or built-in fallbacks."""
    cfg = {}
    try:
        import yaml
        cfg = (yaml.safe_load((TOOLS / "voices.yaml").read_text(encoding="utf-8")) or {}).get("qwen", {})
    except (ImportError, OSError):
        pass
    return {"voices": {**FALLBACK_VOICES, **(cfg.get("voices") or {})},
            "tones": {**FALLBACK_TONES, **(cfg.get("tones") or {})}}


def settings() -> dict:
    load_env()
    proxy = os.environ.get("DASHSCOPE_PROXY", "")
    return {
        "api_key": os.environ.get("DASHSCOPE_API_KEY", ""),
        "endpoint": os.environ.get("DASHSCOPE_ENDPOINT") or DEFAULT_ENDPOINT,
        "proxy": proxy.strip(),
        "model": os.environ.get("DASHSCOPE_MODEL") or DEFAULT_MODEL,
        "ipv4_only": os.environ.get("DASHSCOPE_IPV4_ONLY", "1").strip().lower() not in {"0", "false", "no"},
    }


_ipv4_installed = False


def _force_ipv4() -> None:
    """Make unspecified-family DNS lookups return IPv4 only (process-wide, installed once).

    The workspace endpoint whitelists the caller's IPv4 address; if the host also has IPv6,
    a dual-stack machine may connect over IPv6 and get rejected.
    """
    global _ipv4_installed
    if _ipv4_installed:
        return
    orig = socket.getaddrinfo

    def v4(host, port, family=0, *args, **kw):
        return orig(host, port, socket.AF_INET if family == 0 else family, *args, **kw)

    socket.getaddrinfo = v4
    _ipv4_installed = True


def _opener(proxy: str):
    # An explicit empty ProxyHandler disables env proxies so DASHSCOPE_PROXY="" really means direct.
    handler = urllib.request.ProxyHandler({"http": proxy, "https": proxy} if proxy else {})
    return urllib.request.build_opener(handler)


def synthesize(text: str, out_path: Path, speaker: str = "n", voice: str | None = None,
               instruction: str | None = None, retries: int = 4, timeout: float = 60) -> None:
    s = settings()
    if not s["api_key"]:
        raise ValueError("DASHSCOPE_API_KEY is not set (put it in deepinfer-video/.env)")
    if s["ipv4_only"]:
        _force_ipv4()
    vc = voice_config()
    voice = voice or vc["voices"]["q" if speaker == "q" else "n"]
    instruction = instruction or vc["tones"]["q" if speaker == "q" else "n"]
    payload = {"model": s["model"], "input": {"text": text, "voice": voice, "format": "wav",
                                              "sample_rate": 24000, "instruction": instruction}}
    req = urllib.request.Request(s["endpoint"], data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                                 headers={"Authorization": f"Bearer {s['api_key']}",
                                          "Content-Type": "application/json"}, method="POST")
    api = _opener(s["proxy"])
    for attempt in range(retries):
        try:
            with api.open(req, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            url = (data.get("output") or {}).get("audio", {}).get("url")
            if not url:
                raise RuntimeError(f"no audio URL in response: {json.dumps(data, ensure_ascii=False)[:300]}")
            # The audio URL is a signed object-storage link; fetch it with default (env) proxy settings.
            with urllib.request.urlopen(url, timeout=timeout) as r:
                audio = r.read()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(audio)
            return
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:300]
            if e.code not in RETRY_STATUS or attempt == retries - 1:
                raise RuntimeError(f"TTS API error {e.code}: {body}") from None
            print(f"  qwen retry {attempt + 1}: HTTP {e.code}", file=sys.stderr)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if attempt == retries - 1:
                raise RuntimeError(f"TTS request failed (proxy {s['proxy'] or 'none'}): {e}") from None
            print(f"  qwen retry {attempt + 1}: {e}", file=sys.stderr)
        time.sleep(2 * (attempt + 1))


def main():
    ap = argparse.ArgumentParser(description="Qwen-Audio-3.1-TTS-Plus CLI")
    ap.add_argument("--text-file", help="file containing the text to speak")
    ap.add_argument("--text", help="text to speak")
    ap.add_argument("--out", required=True, help="output wav path")
    ap.add_argument("--speaker", default="n", choices=["n", "q"], help="n = narrator, q = questioner")
    ap.add_argument("--voice", default=None, help="voice ID (default from tools/voices.yaml)")
    ap.add_argument("--instruction", default=None, help="tone instruction (default from tools/voices.yaml)")
    a = ap.parse_args()
    if a.text_file:
        text = Path(a.text_file).read_text(encoding="utf-8").strip()
    elif a.text:
        text = a.text.strip()
    else:
        sys.exit("Error: --text or --text-file is required")
    synthesize(text, Path(a.out), speaker=a.speaker, voice=a.voice, instruction=a.instruction)
    print(f"Synthesized: {a.out}")


if __name__ == "__main__":
    main()
