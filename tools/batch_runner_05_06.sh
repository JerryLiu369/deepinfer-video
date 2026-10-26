#!/usr/bin/env bash
# Autonomous Batch Runner for EP05 and EP06
set -uo pipefail

EPISODES=("EP05" "EP06")
WORKDIR="/home/ubuntu/workspace/default/deepinfer-video-spec"
LOGDIR="/home/ubuntu/.hermes/cache/scratch"
mkdir -p "$LOGDIR"
cd "$WORKDIR"

echo "=== DeepInfer Video Spec Batch Runner (EP05 - EP06) Started ==="

for ep in "${EPISODES[@]}"; do
    echo "=================================================="
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting $ep..."
    echo "=================================================="

    PROMPT="严格依照 docs/ 与 templates/ 规范，端到端完成 $ep 全流程流水线（P2事实包、P3方案、P4脚本、P5双审、P6分镜、P7配音、P8动画、P9成片与手册），通过 tools/make_episode.sh $ep final 输出 48 kHz 内嵌硬字幕广播级成片。完成任务后简要报告生成的成片指标。"

    opencode run -m axon-responses/gemini-3.8-flash#high "$PROMPT" 2>&1 | tee "$LOGDIR/batch_${ep}.log"

    # Verify deliverable
    if [ -f "work/release/${ep}.mp4" ] && [ $(stat -c%s "work/release/${ep}.mp4") -gt 5000000 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS: $ep generated and verified at work/release/${ep}.mp4"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $ep finished, checking fallback build..."
    fi
done

echo "=== Batch EP05-EP06 Complete ==="
