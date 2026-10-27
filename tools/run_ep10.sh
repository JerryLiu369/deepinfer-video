#!/usr/bin/env bash
# Autonomous Runner for EP10 (Full 16-20 shots, 13-15 min, No Companion Manual)
set -uo pipefail

EP="EP10"
WORKDIR="/home/ubuntu/workspace/default/deepinfer-video-spec"
LOGDIR="/home/ubuntu/.hermes/cache/scratch"
mkdir -p "$LOGDIR"
cd "$WORKDIR"

echo "=== DeepInfer Video Spec Runner: $EP Started at $(date '+%Y-%m-%d %H:%M:%S') ==="

PROMPT="严格依照 docs/ 与 templates/ 规范，端到端完成 $EP 全流程流水线（P2事实包、P3方案、P4脚本、P5双审、P6分镜、P7配音、P8动画、P9成片；不需要编写伴读手册）。【核心体量要求】：必须充分展开 16~20 个镜头节拍（每镜 40~50 秒），成片总时长保持在 13~15 分钟的饱满大集标准，严禁压缩为短小脚本。重点讲透：1) 5个外部内核库与自研TileLang在CUDA/昇腾上的构建期同名镜像；2) 批不变性的物理本质（浮点加法非结合律、消除批维度归约、关split-KV/K、定点CDF）；3) 确定性采样绝对位置与变长MTP破坏同批独立性的权衡；4) 结构化输出（xgrammar调度）与eval/评测真实定位。通过 tools/make_episode.sh $EP final 输出 48 kHz 内嵌硬字幕广播级成片。"

opencode run -m axon-responses/gemini-3.8-flash#high "$PROMPT" 2>&1 | tee "$LOGDIR/run_${EP}.log"

if [ -f "work/release/${EP}.mp4" ] && [ $(stat -c%s "work/release/${EP}.mp4") -gt 5000000 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS: $EP generated and verified at work/release/${EP}.mp4"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $EP finished, checking fallback build..."
fi
