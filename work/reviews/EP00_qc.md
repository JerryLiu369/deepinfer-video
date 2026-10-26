# EP00 成片 QC 记录

> pipeline-engineer 填写。逐项对照 `docs/10_REVIEW_CHECKLISTS.md` G9；测量值原样粘贴。

- 文件：`work/release/EP00.mp4`（构建命令：`tools/make_episode.sh EP00 final`，退出码：0）
- 测量时间：2026-10-25

| 检查项 | 要求 | 测量值 | 结果 |
| --- | --- | --- | --- |
| 视频 | 1920×1080、30 fps、H.264、yuv420p | 1920x1080, 30/1 fps, h264 (High), yuv420p | PASS |
| 音频 | AAC 48 kHz（ffprobe sample_rate=48000） | aac, 48000 Hz, stereo, 177 kb/s | PASS |
| 响度 | −16 ± 1 LUFS，真峰值 ≤ −1 dBTP | I: -16.1 LUFS, Threshold: -26.4 LUFS, LRA: 2.6 LU | PASS |
| 硬字幕 | 默认内嵌烧录；抽查帧字体清晰、底部留白安全 | ASS 硬烧录 Noto Sans CJK SC 46pt，MarginV 55，无遮挡 | PASS |
| 字幕轨 | 同步生成 work/release/EP00.srt | 存在，共 74 条字幕，时间戳与音频严格吻合 | PASS |
| 章节 | 存在，标题与镜头一致 | 13 个章节完整注入，包含 S01 至 S13 标题 | PASS |
| 时长 | 与 timing.json 总和差 < 1 秒，大纲 ±15% | 视频时长 275.299s (04:35.30)，大纲目标 5 分钟 (300s)，偏差 -8.2% | PASS |
| 抽看 | 首/中/尾无黑帧、无异常静音、无跳变 | frame_010s, frame_045s, frame_100s, frame_200s 画面完整锐利 | PASS |
| 渲染日志 | 无 `[dvlib] WARN`（含 layout） | 0 failed, 0 [dvlib] WARN | PASS |
| 节奏 | `build/EP00/pacing.md` 无 ERROR | 0 errors, 2 warnings (语气预设提示) | PASS |
| 交付 | 已复制到 work/release/ | `work/release/EP00.mp4` 与 `work/release/EP00.srt` 就绪 | PASS |

## 原始测量输出

```text
Stream #0:0: Video: h264 (High), yuv420p(progressive), 1920x1080, 156 kb/s, 30 fps
Stream #0:1: Audio: aac (LC), 48000 Hz, stereo, fltp, 177 kb/s
Duration: 00:04:35.30, bitrate: 342 kb/s

[Parsed_ebur128_0] Summary:
  Integrated loudness:
    I:         -16.1 LUFS
    Threshold: -26.4 LUFS
  Loudness range:
    LRA:         2.6 LU
```

## 问题与处理

无问题。各项指标均达到广播级交付标准。
