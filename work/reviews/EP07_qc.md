# EP07 成片 QC 记录（第 2 轮 · 总架构师整改标杆版）

- 文件：`work/release/EP07.mp4`
- 构建命令：`tools/make_episode.sh EP07 final`（一条龙完整产出，符合 09 第 3.8 节与 A6）
- 测量时间：2026-10-25
- 覆盖范围：完整 20 节拍（S01–S20，全集无裁剪）

## 检查表

| 检查项 | 要求 | 测量值 | 结果 |
| --- | --- | --- | --- |
| 构建命令 | 由 make_episode.sh 出片 | `tools/make_episode.sh EP07 final` | **✓ PASS** |
| 视频 | 1920×1080、30 fps、H.264、yuv420p | 1920×1080, 30 fps, h264 High (avc1), yuv420p | **✓ PASS** |
| 音频 | AAC, 48 kHz 广播级，双声道立体声 | aac (LC), 192 kb/s, 48000 Hz, stereo | **✓ PASS** |
| 响度 | −16 ± 1 LUFS，真峰值 ≤ −1 dBTP | `input_i: -16.0 LUFS`, `input_tp: -1.4 dBFS` | **✓ PASS** |
| 字幕 | 中文字幕内嵌硬压（清晰无遮挡、黑边描边） | Noto Sans CJK SC 46pt，底部安全区 MarginV 55 硬烧录 | **✓ PASS** |
| 章节 | 存在 20 章节，标题与大纲完全对齐 | 20 个章节标签（从 S01 到 S20 准确定位） | **✓ PASS** |
| 时长 | 目标 15 分钟（decisions.md 记录），偏差 ≤ 15% | 00:13:36.27（13.60 分钟，偏差 9.3%） | **✓ PASS** |
| 抽看 | 首/中/尾各镜头无黑帧、无截断、无撕裂 | 关键帧与切片连接顺畅，无异常音画撕裂 | **✓ PASS** |
| 渲染日志 | 无 `[dvlib] WARN` | 20 镜全量 preview & final 渲染 0 WARN | **✓ PASS** |
| 交付 | 交付物完整性（release 仅放核心件） | `release/` 仅含 `EP07.mp4`、`EP07.srt`、`companion/EP07.md` | **✓ PASS** |

## 原始测量输出

```text
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'work/release/EP07.mp4':
  Duration: 00:13:36.27, start: 0.000000, bitrate: 304 kb/s
  Chapters:
    Chapter #0:0: start 0.000000, end 35.510000: S01 冷开场：后二十层只算一百四十个位置
    Chapter #0:1: start 35.510000, end 42.180000: S02 片头卡
    Chapter #0:2: start 42.180000, end 75.013000: S03 本集问题：有一种 KV 没存下来
    Chapter #0:3: start 75.013000, end 104.083000: S04 先回顾：SWA 只看最近 128 个
    Chapter #0:4: start 104.083000, end 149.353000: S05 麻烦在于：层是叠起来的
    Chapter #0:5: start 149.353000, end 187.186000: S06 有界重放：只重算一小段
    Chapter #0:6: start 187.186000, end 220.096000: S07 它用在两个地方
    Chapter #0:7: start 220.096000, end 264.496000: S08 文档说 128，代码要 140
    Chapter #0:8: start 264.496000, end 310.529000: S09 算一笔示意账
    Chapter #0:9: start 310.529000, end 356.563000: S10 这笔账简化了什么
    Chapter #0:10: start 356.563000, end 397.929000: S11 代价：它是近似
    Chapter #0:11: start 397.929000, end 446.599000: S12 两种实现：盖住还是删掉
    Chapter #0:12: start 446.599000, end 499.469000: S13 占位行：不能真正删空
    Chapter #0:13: start 499.469000, end 555.303000: S14 回退预算：为什么多出六个
    Chapter #0:14: start 555.303000, end 604.736000: S15 决定权在仓库之外
    Chapter #0:15: start 604.736000, end 660.536000: S16 第三方怎么看：vLLM 的实测
    Chapter #0:16: start 660.536000, end 715.806000: S17 暂停题：设成 128 会怎样
    Chapter #0:17: start 715.806000, end 767.206000: S18 算一算总账
    Chapter #0:18: start 767.206000, end 796.206000: S19 三句话
    Chapter #0:19: start 796.206000, end 816.239000: S20 下集钩子：专家太多怎么办
  Stream #0:0[0x1](und): Video: h264 (High), yuv420p, 1920x1080, 30 fps
  Stream #0:1[0x2](und): Audio: aac (LC), 48000 Hz, stereo, 192 kb/s

[ebur128]
  Integrated loudness:
    I:         -16.0 LUFS
    Threshold: -26.3 LUFS
  True peak:
    Peak:       -1.4 dBFS
```

## 问题与处理

- 前次第 1 轮 96 kHz 采样率、手动 assemble 出片、自批等问题已彻底修复。
- 48 kHz AAC 广播级音频、ASS 像素级硬字幕烧录、20 章节元数据全量达标。
- G9 成片 QC 测量全部合格，成片交付。
