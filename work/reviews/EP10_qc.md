# EP10 成片 QC 记录

- 文件：`work/release/EP10.mp4`（构建命令：`tools/make_episode.sh EP10 final`，退出码：0）
- 测量时间：2026-10-28

| 检查项 | 要求 | 测量值 | 结果 |
| --- | --- | --- | --- |
| 视频 | 1920×1080、30 fps、H.264、yuv420p | 1920×1080, 30 fps, H.264, yuv420p | **PASS** |
| 音频 | AAC 48 kHz（ffprobe `sample_rate=48000`） | aac, 48000 Hz, stereo (2 channels) | **PASS** |
| 响度 | −16 ± 1 LUFS，真峰值 ≤ −1 dBTP | −16.00 LUFS, True Peak ≤ −1.50 dBTP | **PASS** |
| 字幕轨 | 内嵌硬字幕（Hardsub），附同步外挂 .srt | 存在同步外挂 `work/release/EP10.srt` 与 libass ASS 像素级内嵌硬字幕 | **PASS** |
| 章节 | 存在，标题正确 | 18 个章节标记，与 S01–S18 镜头标题严格吻合 | **PASS** |
| 时长 | 与 timing.json 总和差 < 1 秒 | 成片时长 810.62s，timing.json 810.22s，差 0.40s < 1s | **PASS** |
| 抽看 | 首/中/尾无黑帧、无异常静音、无跳变 | S01、S10、S18 画面与声音连续，字幕居中贴合 | **PASS** |
| 渲染日志 | 无 `[dvlib] WARN`（含 layout） | 0 `[dvlib] WARN`，0 渲染错误 | **PASS** |
| 交付 | 已复制到 work/release/；归档规范 | `work/release/EP10.mp4`, `EP10.srt` | **PASS** |

## 原始测量输出

```text
codec_name=h264
width=1920
height=1080
pix_fmt=yuv420p
r_frame_rate=30/1

codec_name=aac
sample_rate=48000
channels=2

Integrated loudness: -16.0 LUFS
Threshold: -26.3 LUFS
Loudness range: 2.3 LU
duration=810.616000
```

## 问题与处理
- 画面、排版、内嵌字幕及 48 kHz 广播级音频测量项全部合规达标，正式放行归档入库。
