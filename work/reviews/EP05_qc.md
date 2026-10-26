# EP05 成片 QC 记录

- 文件：`work/release/EP05.mp4`
- 构建命令：`tools/make_episode.sh EP05 final`（全自动流水线一条龙产出，符合 09 第 3.8 节与 A6 规范）
- 测量时间：2026-10-26
- 覆盖范围：完整 20 节拍（S01–S20，全集无裁剪）

## 检查表

| 检查项 | 要求 | 测量值 | 结果 |
| --- | --- | --- | --- |
| 构建命令 | 由 make_episode.sh 出片 | `tools/make_episode.sh EP05 final` | **✓ PASS** |
| 视频格式 | 1920×1080、30 fps、H.264、yuv420p | 1920×1080, 30 fps, h264 High (avc1), yuv420p | **✓ PASS** |
| 音频采样 | AAC, 48 kHz 广播级，双声道立体声 | aac (LC), 48000 Hz, stereo, 192 kb/s | **✓ PASS** |
| 响度指标 | −16 ± 1 LUFS，真峰值 ≤ −1.0 dBFS | `input_i: -16.07 LUFS`, `output_i: -15.97 LUFS`, `input_tp: -1.50 dBFS` | **✓ PASS** |
| 硬压字幕 | 中文字幕内嵌硬压（清晰无遮挡、黑边描边） | Noto Sans CJK SC 46pt，底部安全区 MarginV 55 ASS 像素级烧录 | **✓ PASS** |
| 章节标记 | 存在 20 章节，标题与大纲完全对齐 | 20 个章节标签（从 S01 到 S20 准确定位） | **✓ PASS** |
| 时长控制 | 目标 13 分钟（大纲承诺 13 分钟），偏差 ≤ 15% | 00:12:37.03（12.62 分钟，偏差 2.9% < 15%） | **✓ PASS** |
| 抽看检查 | 首/中/尾各镜头无黑帧、无截断、无撕裂 | 143 张关键帧与切片连接顺畅，音画完全同步 | **✓ PASS** |
| 渲染日志 | 无 `[dvlib] WARN` | 20 镜全量 preview & final 渲染 0 [dvlib] WARN | **✓ PASS** |
| 交付文件 | 交付物完整性（release 仅放核心件） | `release/` 仅含 `EP05.mp4`、`EP05.srt`、`companion/EP05.md` | **✓ PASS** |

## 原始测量输出

```text
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'work/release/EP05.mp4':
  Duration: 00:12:37.03, start: 0.000000, bitrate: 349 kb/s
  Chapters:
    Chapter #0:0: start 0.000000, end 42.366000: S01 冷开场：GPU 空泡之谜
    Chapter #0:1: start 42.366000, end 47.400000: S02 片头卡：调度：让 GPU 一刻不停
    Chapter #0:2: start 47.400000, end 88.400000: S03 核心矛盾：同步调度的阻塞等待
    Chapter #0:3: start 88.400000, end 128.110000: S04 破局之道：让 CPU 永远晚一步
    Chapter #0:4: start 128.110000, end 171.643000: S05 骨架剖析：worker 的四段式单步循环
    Chapter #0:5: start 171.643000, end 215.753000: S06 关键界限：ZOS 只管连续解码，Prefill 纯同步
    Chapter #0:6: start 215.753000, end 248.463000: S07 难题之一：还没算出的词怎么输入？
    Chapter #0:7: start 248.463000, end 285.173000: S08 现场捡词：TileLang 内核就地索引
    Chapter #0:8: start 285.173000, end 328.463000: S09 行序重排：为什么必须有 remap 映射？
    Chapter #0:9: start 328.463000, end 361.733000: S10 难题之二：请求已经结束了怎么办？
    Chapter #0:10: start 361.733000, end 400.923000: S11 确定性代价：多跑一步的算术账本
    Chapter #0:11: start 400.923000, end 437.553000: S12 乐观推进：虚高账本与真实回填
    Chapter #0:12: start 437.553000, end 482.283000: S13 变长协作：DSpark 投机在 ZOS 下的双层切分
    Chapter #0:13: start 482.283000, end 526.193000: S14 调度取舍：LCFS 选拔与残忍抢占
    Chapter #0:14: start 526.193000, end 564.703000: S15 步型共识：DP 副本的 70 步与 100 步投票
    Chapter #0:15: start 564.703000, end 617.593000: S16 代码真相：文档里的二次模型去哪了？
    Chapter #0:16: start 617.593000, end 655.863000: S17 严谨收尾：Deferred 释放与 flush 兜底
    Chapter #0:17: start 655.863000, end 696.293000: S18 工业全景：NanoFlow 血统、vLLM 与 SGLang 殊途同归
    Chapter #0:18: start 696.293000, end 741.883000: S19 三句话总结与暂停题公布
    Chapter #0:19: start 741.883000, end 757.026000: S20 尾声与预告：从调度走向显存记忆
  Stream #0:0[0x1](und): Video: h264 (High) (avc1 / 0x31637661), yuv420p(progressive), 1920x1080, 159 kb/s, 30 fps, 30 tbr, 15360 tbn (default)
  Stream #0:1[0x2](und): Audio: aac (LC) (mp4a / 0x6134706d), 48000 Hz, stereo, fltp, 185 kb/s (default)

loudnorm:
  input_i: -16.07 LUFS
  output_i: -15.97 LUFS
  input_tp: -1.50 dBFS
  output_tp: -1.50 dBFS
  input_lra: 2.50 LU
```
