# EPxx 成片 QC 记录

> pipeline-engineer 填写。逐项对照 `docs/10_REVIEW_CHECKLISTS.md` G9；测量值原样粘贴（只贴关键行）。命令见 `docs/09_PRODUCTION_PIPELINE.md` 第 5 节。

- 文件：work/release/EPxx.mp4（构建命令：`tools/make_episode.sh EPxx final`，退出码：_）
- 测量时间：

| 检查项 | 要求 | 测量值 | 结果 |
| --- | --- | --- | --- |
| 视频 | 1920×1080、30 fps、H.264、yuv420p | | |
| 音频 | AAC 48 kHz（ffprobe `sample_rate=48000`） | | |
| 响度 | −16 ± 1 LUFS，真峰值 ≤ −1 dBTP | | |
| 字幕轨 | 存在；抽查 10 条误差 < 0.3 秒 | | |
| 章节 | 存在，标题正确 | | |
| 时长 | 与 timing.json 总和差 < 1 秒 | | |
| 抽看 | 首/中/尾各 30 秒无黑帧、无异常静音、无跳变 | | |
| 渲染日志 | 无 `[dvlib] WARN`（含 layout） | | |
| 节奏 | `build/EPxx/pacing.md` 无 ERROR；时长对 02 大纲目标 ±15% | | |
| 交付 | 已复制到 work/release/；目录里只有 EPxx.mp4、EPxx.srt、companion/EPxx.md | | |
| 人类检查点 | 试点：H3 由委托人本人确认（原话 + 时间），代理不能代填 | | |

## 原始测量输出

```text
（ffprobe / loudnorm 输出关键行）
```

## 问题与处理
