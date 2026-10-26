#!/usr/bin/env bash
# Environment gate for P0. Prints PASS/FAIL per item; exit 1 if any FAIL.
# Usage: tools/check_env.sh [path-to-knowledge-base]
#   DV_CHECK_TTS=1 tools/check_env.sh   # also synthesize one test sentence with the active TTS backend
T=$(cd "$(dirname "$0")" && pwd)
KB=${1:-${DV_KB:-../deepinfer-book/research}}
if [ -z "${PYTHON:-}" ]; then
  if [ -x "$T/../.venv/bin/python" ]; then
    PY="$T/../.venv/bin/python"
  else
    PY=python3
  fi
else
  PY="$PYTHON"
fi
unset PYTHONPATH
fail=0
ok()  { printf 'PASS  %s\n' "$1"; }
bad() { printf 'FAIL  %s\n' "$1"; fail=1; }
warn(){ printf 'WARN  %s\n' "$1"; }

$PY -c 'import sys; assert sys.version_info >= (3,10)' && ok "python $($PY -V 2>&1)" || bad "python >= 3.10"
$PY -c 'import manim; print(manim.__version__)' >/dev/null 2>&1 && ok "manim $($PY -c 'import manim;print(manim.__version__)' 2>/dev/null)" || bad "manim import (pip install -r tools/requirements.txt)"
$PY -c 'import yaml' 2>/dev/null && ok "pyyaml" || bad "pyyaml import"

# TTS: qwen (recommended) needs .env credentials; edge is the no-key fallback.
backend=$(cd "$T" && $PY -c '
import os, yaml
cfg = yaml.safe_load(open("voices.yaml", encoding="utf-8")) or {}
print(os.environ.get("DV_TTS_BACKEND") or cfg.get("backend") or "qwen")' 2>/dev/null) || { bad "tools/voices.yaml unreadable"; backend=qwen; }
qwen_state=$(cd "$T" && $PY -c '
import qwen_tts as q
s = q.settings()
if not s["api_key"]:
    print("nokey")
else:
    print("ok  model=%s, %s, %s" % (s["model"], ("proxy " + s["proxy"]) if s["proxy"] else "direct",
                                   "IPv4 only" if s["ipv4_only"] else "IPv4/IPv6"))' 2>/dev/null)
case "$qwen_state" in
  ok*) qwen_ok=1; ok "qwen TTS configured (${qwen_state#ok  })" ;;
  *)   qwen_ok=0; warn "qwen TTS: DASHSCOPE_API_KEY not found (copy .env.example to .env)" ;;
esac
if $PY -c 'import edge_tts' 2>/dev/null; then edge_ok=1; ok "edge-tts (fallback backend)"; else edge_ok=0; warn "edge-tts not installed (fallback backend unavailable)"; fi
case "$backend" in
  qwen) [ "$qwen_ok" = 1 ] && ok "active TTS backend: qwen" || bad "active TTS backend qwen is not configured (or set DV_TTS_BACKEND=edge)" ;;
  edge) [ "$edge_ok" = 1 ] && ok "active TTS backend: edge" || bad "active TTS backend edge: pip install edge-tts" ;;
  command) [ -n "$DV_TTS_CMD" ] && ok "active TTS backend: command" || bad "backend command needs DV_TTS_CMD" ;;
  *) bad "unknown TTS backend '$backend'" ;;
esac
if [ -n "$DV_CHECK_TTS" ]; then
  tmp=$(mktemp -d)
  if [ "$backend" = qwen ]; then
    (cd "$T" && $PY qwen_tts.py --text "环境检查：配音正常。" --out "$tmp/t.wav" >/dev/null 2>"$tmp/err") \
      && ok "qwen live synthesis ($(ffprobe -v error -show_entries stream=sample_rate,channels -of csv=p=0 "$tmp/t.wav" 2>/dev/null))" \
      || bad "qwen live synthesis: $(tail -1 "$tmp/err")"
  elif [ "$backend" = edge ]; then
    $PY -c 'import asyncio, edge_tts, sys; asyncio.run(edge_tts.Communicate("环境检查。", "zh-CN-YunxiNeural").save(sys.argv[1]))' "$tmp/t.mp3" 2>"$tmp/err" \
      && ok "edge live synthesis" || bad "edge live synthesis: $(tail -1 "$tmp/err")"
  fi
  rm -rf "$tmp"
fi

command -v ffmpeg >/dev/null && ok "ffmpeg" || bad "ffmpeg on PATH"
command -v ffprobe >/dev/null && ok "ffprobe" || bad "ffprobe on PATH"
ffmpeg -hide_banner -encoders 2>/dev/null | grep -q libx264 && ok "libx264 encoder" || bad "ffmpeg built with libx264"
ffmpeg -hide_banner -filters 2>/dev/null | grep -q ' subtitles ' && ok "libass (subtitle burn-in, optional)" || warn "no libass: only soft subtitles"
fc-list 2>/dev/null | grep -q 'Noto Sans CJK SC' && ok "font Noto Sans CJK SC" || bad "font Noto Sans CJK SC (fonts-noto-cjk)"
fc-list 2>/dev/null | grep -qi 'Noto Sans Mono' && ok "font Noto Sans Mono" || warn "Noto Sans Mono missing: set DV_MONO_FONT"
if [ -d "$KB/notes" ]; then ok "knowledge base: $KB ($(ls "$KB/notes" | wc -l) notes)"; else bad "knowledge base not found at $KB (pass path or set DV_KB)"; fi
if [ -d "$KB/sources/DeepInfer/.git" ]; then
  ok "DeepInfer source @ $(git -C "$KB/sources/DeepInfer" rev-parse --short HEAD)"
else bad "DeepInfer source checkout missing at $KB/sources/DeepInfer"; fi
exit $fail
