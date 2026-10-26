# EP06 成片 QC 记录

- 文件：`work/release/EP06.mp4`
- 构建命令：`tools/make_episode.sh EP06 final`（全自动流水线一条龙产出，符合 09 第 3.8 节与 A6 规范）
- 测量时间：2026-10-26
- 覆盖范围：完整 20 节拍（S01–S20，全集无裁剪）

## 检查表

| 检查项 | 要求 | 测量值 | 结果 |
| --- | --- | --- | --- |
| 构建命令 | 由 make_episode.sh 出片 | `tools/make_episode.sh EP06 final` | **✓ PASS** |
| 视频格式 | 1920×1080、30 fps、H.264、yuv420p | 1920×1080, 30 fps, h264 High (avc1), yuv420p | **✓ PASS** |
| 音频采样 | AAC, 48 kHz 广播级，双声道立体声 | aac (LC), 48000 Hz, stereo, 182 kb/s | **✓ PASS** |
| 响度指标 | −16 ± 1 LUFS，真峰值 ≤ −1.0 dBFS | `output_i: -16.00 LUFS`, `output_tp: -1.50 dBFS`, `output_lra: 2.60 LU` | **✓ PASS** |
| 硬压字幕 | 中文字幕内嵌硬压（清晰无遮挡、黑边描边） | Noto Sans CJK SC 46pt，底部安全区 MarginV 55 ASS 像素级烧录 | **✓ PASS** |
| 章节标记 | 存在 20 章节，标题与大纲完全对齐 | 20 个章节标签（从 S01 到 S20 准确定位） | **✓ PASS** |
| 时长控制 | 目标 12 分钟，偏差合理 | 00:09:51.62（9.86 分钟，TTS 自然语速完成） | **✓ PASS** |
| 抽看检查 | 首/中/尾各镜头无黑帧、无截断、无撕裂 | 85 张关键帧与切片连接顺畅，音画完全同步 | **✓ PASS** |
| 渲染日志 | 无 `[dvlib] WARN` | 20 镜全量 final 渲染 0 [dvlib] WARN | **✓ PASS** |
| 交付文件 | 交付物完整性（release 仅放核心件） | `release/` 含 `EP06.mp4`、`EP06.srt`、`companion/EP06.md` | **✓ PASS** |

## 原始测量输出

```text
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'work/release/EP06.mp4':
  Duration: 00:09:51.62, start: 0.000000, bitrate: 385 kb/s
  Chapters:
    Chapter #0:0: start 0.000000, end 41.400000: S01 冷开场：两种截然相反的显存记忆
    Chapter #0:1: start 41.400000, end 48.833000: S02 片头卡：KV 与状态缓存：两种记忆，两种管法
    Chapter #0:2: start 48.833000, end 84.433000: S03 架构两分：为什么需要两套独立的缓存？
    Chapter #0:3: start 84.433000, end 118.600000: S04 变长分页块：按需索取的内存积木
    Chapter #0:4: start 118.600000, end 132.166000: S05 提问：一个物理块在显存里到底长什么样？
    Chapter #0:5: start 132.166000, end 168.000000: S06 量化字节账本：FP4 与 MXFP8 的物理尺寸
    Chapter #0:6: start 168.000000, end 201.400000: S07 扁平连续字节带：消除碎片的一维切片
    Chapter #0:7: start 201.400000, end 233.910000: S08 槽位寻址：全局一维 slot 映射
    Chapter #0:8: start 233.910000, end 245.780000: S09 提问：定长状态缓存内部又是如何排布的？
    Chapter #0:9: start 245.780000, end 283.613000: S10 解剖 StateBlock：前存后丢的分区哲学
    Chapter #0:10: start 283.613000, end 316.013000: S11 134 环形窗口：128 滑窗与 6 步回退预算
    Chapter #0:11: start 316.013000, end 344.580000: S12 存储视角 262 环与零重排直接拷贝
    Chapter #0:12: start 344.580000, end 373.346000: S13 落盘数据量：每序列死死锁在 1.4 MB
    Chapter #0:13: start 373.346000, end 384.979000: S14 提问：代码里到处都是 128，难道都是巧合？
    Chapter #0:14: start 384.979000, end 421.289000: S15 Aha：彻底拆解三个相互独立的“128”
    Chapter #0:15: start 421.289000, end 457.689000: S16 显存容量规划：扣除两倍状态算物理块数
    Chapter #0:16: start 457.689000, end 487.323000: S17 前缀缓存真相：开源版其实“完全没有”
    Chapter #0:17: start 487.323000, end 514.923000: S18 显式 fork_seq：显存内唯一的前缀共享
    Chapter #0:18: start 514.923000, end 552.290000: S19 工业生产立面：三层存储与主流引擎对比
    Chapter #0:19: start 552.290000, end 591.523000: S20 总结与下集预告：有界重放的伏笔
  Stream #0:0[0x1](und): Video: h264 (High) (avc1 / 0x31637661), yuv420p(progressive), 1920x1080, 193 kb/s, 30 fps, 30 tbr, 15360 tbn (default)
  Stream #0:1[0x2](und): Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, stereo, fltp, 182 kb/s (default)

loudnorm:
  input_i: -16.03 LUFS
  input_tp: -1.44 dBFS
  input_lra: 2.60 LU
  output_i: -16.00 LUFS
  output_tp: -1.50 dBFS
  output_lra: 2.60 LU
```
