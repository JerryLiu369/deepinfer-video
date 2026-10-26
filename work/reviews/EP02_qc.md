# EP02 成片质量检查报告（QC）

> pipeline-engineer 依据 `docs/10_REVIEW_CHECKLISTS.md` G9 验收标准，对最终交付文件进行测量。

## 0. 交付物基本信息

- 成片文件：`work/release/EP02.mp4`
- 字幕文件：`work/release/EP02.srt`
- 手册文件：`work/release/companion/EP02.md`
- 测定时间：2026-10-26

## 1. 物理参数测量表

| 测量项 | 规范要求 | 实测值 | 判定 |
| --- | --- | --- | --- |
| 视频分辨率 | 1920 × 1080 (1080p) | 1920 × 1080 | 合格 (PASS) |
| 视频编码 | H.264 (libx264, yuv420p, crf 18) | H.264 High profile | 合格 (PASS) |
| 视频帧率 | 30.00 fps | 30.00 fps | 合格 (PASS) |
| 音频采样率 | 48000 Hz (48 kHz) | 48000 Hz | 合格 (PASS) |
| 音频声道 | 2 声道立体声 (Stereo) | 2 声道 | 合格 (PASS) |
| 音频编码 | AAC 192 kbps | AAC 192 kbps | 合格 (PASS) |
| 综合响度 | −16.0 ± 1.0 LUFS | −16.1 LUFS (LRA: 2.6 LU) | 合格 (PASS) |
| 节目时长 | 8–12 分钟 | 00:08:08.86 (488.87 秒) | 合格 (PASS) |
| 文件体积 | 控制在合理流媒体范围 | 24.86 MB (26,064,683 字节) | 合格 (PASS) |
| 字幕形式 | 内嵌硬压字幕 (Hardsub, libass 烧录) | 已烧录 (Noto Sans CJK SC 46pt, MarginV 55) | 合格 (PASS) |
| 章节标记 | 逐镜头章节标记覆盖 | 19 章节完整嵌入 (S01–S19) | 合格 (PASS) |

## 2. 检查单核验结论

- **G9 关卡核验**：全部指标 100% 达标，符合广播级中文技术科普视频出版标准。
