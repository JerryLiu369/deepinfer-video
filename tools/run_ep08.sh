#!/usr/bin/env bash
# Autonomous Refactoring Runner for EP08 (18-22 shots, 15-16 min, No Companion Manual)
set -uo pipefail

EP="EP08"
WORKDIR="/home/ubuntu/workspace/default/deepinfer-video-spec"
LOGDIR="/home/ubuntu/.hermes/cache/scratch"
mkdir -p "$LOGDIR"
cd "$WORKDIR"

echo "=== DeepInfer Video Spec Runner: $EP Refactoring Started at $(date '+%Y-%m-%d %H:%M:%S') ==="

PROMPT="严格依照 docs/ 与 templates/ 规范，对 $EP 进行深度重构，端到端完成全流程流水线（P3方案、P4脚本、P5双审、P6分镜、P7配音、P8动画、P9成片；不需要编写伴读手册）。【核心体量要求】：将目前 3 分钟的雏形彻底重构成 18~22 个镜头节拍（每镜 40~50 秒），成片总时长达到 15~16 分钟的饱满大集标准。重点讲透：1) DP-Attention 与 EP-MoE 进程组解耦（开源无 TP、DP 组间不同步 batch 仅同步步型、无活 rank 陪跑机制）；2) MoE 六段流水线与 NVLink 域内 Mega MoE 单核融合；3) Wide-EP 的真实定义与悖论（从 EP8 到 EP64 权重访存削减 7.4 倍，但高并发吞吐差距收敛到 5% 的物理瓶颈）；4) EPLB 两级贪心装箱策略与 symm_mem 共享显存直读；5) Zigzag 镜像平衡 CP 与生产为什么不用 TP。通过 tools/make_episode.sh $EP final 输出 48 kHz 内嵌硬字幕广播级成片。"

opencode run -m axon-responses/gemini-3.8-flash#high "$PROMPT" 2>&1 | tee "$LOGDIR/run_${EP}.log"

if [ -f "work/release/${EP}.mp4" ] && [ $(stat -c%s "work/release/${EP}.mp4") -gt 5000000 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS: $EP generated and verified at work/release/${EP}.mp4"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $EP finished, checking fallback build..."
fi
