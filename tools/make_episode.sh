#!/usr/bin/env bash
# One episode through the whole build: parse -> lint -> tts -> render -> assemble -> keyframes.
# Usage: tools/make_episode.sh EP07 [preview|draft|final] [--animatic]
set -euo pipefail
EP=${1:?episode id, e.g. EP07}
Q=${2:-preview}
EXTRA=${3:-}
WORK=${DV_WORK:-work}
T=$(cd "$(dirname "$0")" && pwd)
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
$PY "$T/parse_script.py" "$EP" --work "$WORK"
$PY "$T/lint_script.py" "$EP" --work "$WORK"
$PY "$T/tts.py" "$EP" --work "$WORK"
$PY "$T/pacing_report.py" "$EP" --work "$WORK" || true
$PY "$T/render.py" "$EP" --work "$WORK" --quality "$Q" $EXTRA
$PY "$T/assemble.py" "$EP" --work "$WORK" --quality "$Q"
$PY "$T/keyframes.py" "$EP" --work "$WORK"
if [ "$Q" = final ]; then
  mkdir -p "$WORK/release"
  cp "$WORK/build/$EP/$EP.mp4" "$WORK/build/$EP/$EP.srt" "$WORK/release/"
  echo "released: $WORK/release/$EP.mp4"
fi
echo "done: $WORK/build/$EP/$EP.mp4"
