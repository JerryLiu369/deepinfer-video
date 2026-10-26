# EP03 成片 QC 记录

- 文件：`work/release/EP03.mp4`
- 构建命令：`tools/make_episode.sh EP03 final`（一条龙完整产出，符合 09 第 3.8 节与 A6）
- 测量时间：2026-10-26
- 覆盖范围：完整 22 节拍（S01–S22，全集无裁剪）

## 检查表

| 检查项 | 要求 | 测量值 | 结果 |
| --- | --- | --- | --- |
| 构建命令 | 由 make_episode.sh 出片 | `tools/make_episode.sh EP03 final` | **✓ PASS** |
| 视频 | 1920×1080、30 fps、H.264、yuv420p | 1920×1080, 30 fps, h264 High (avc1), yuv420p | **✓ PASS** |
| 音频 | AAC, 48 kHz 广播级，双声道立体声 | aac (LC), 185 kb/s, 48000 Hz, stereo | **✓ PASS** |
| 响度 | −16 ± 1 LUFS，真峰值 ≤ −1.0 dBFS | `input_i: -16.05 LUFS`, `input_tp: -1.39 dBFS`, `input_lra: 2.40 LU` | **✓ PASS** |
| 字幕 | 中文字幕内嵌硬压（清晰无遮挡、黑边描边） | Noto Sans CJK SC 46pt，底部安全区 MarginV 55 硬烧录 | **✓ PASS** |
| 章节 | 存在 22 章节，标题与大纲完全对齐 | 22 个章节标签（从 S01 到 S22 准确定位） | **✓ PASS** |
| 时长 | 目标 16–18 分钟（大纲承诺 18 分钟），偏差 ≤ 15% | 00:17:57.70（17.96 分钟，偏差 0.2%） | **✓ PASS** |
| 抽看 | 首/中/尾各镜头无黑帧、无截断、无撕裂 | 关键帧与切片连接顺畅，无异常音画撕裂 | **✓ PASS** |
| 渲染日志 | 无 `[dvlib] WARN` | 22 镜全量 preview & final 渲染 0 WARN | **✓ PASS** |
| 交付 | 交付物完整性（release 仅放核心件） | `release/` 含 `EP03.mp4`、`EP03.srt`、`companion/EP03.md` | **✓ PASS** |

## 原始测量输出

```text
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'work/release/EP03.mp4':
  Duration: 00:17:57.70, start: 0.000000, bitrate: 349 kb/s
  Chapters:
    Chapter #0:0: start 0.000000, end 41.200000: S01 冷开场：四十层与四层键值缓存
    Chapter #0:1: start 41.200000, end 49.166000: S02 片头卡：先认识它服务的模型
    Chapter #0:2: start 49.166000, end 91.566000: S03 参数口径：总容量与主干参数
    Chapter #0:3: start 91.566000, end 131.333000: S04 激活真相：全 MoE 与极端稀疏
    Chapter #0:4: start 131.333000, end 170.166000: S05 查表巨物：两层近两千亿参数
    Chapter #0:5: start 170.166000, end 211.036000: S06 查表机制：每 token 24 行
    Chapter #0:6: start 211.036000, end 253.670000: S07 残差主干：Single-Pass mHC
    Chapter #0:7: start 253.670000, end 301.539000: S08 注意力骨架：全 SWA
    Chapter #0:8: start 301.539000, end 345.773000: S09 结构密码：compress_ratios
    Chapter #0:9: start 345.773000, end 402.940000: S10 结构分水岭：CED 体系
    Chapter #0:10: start 402.940000, end 452.140000: S11 潜在注意力：MLA 拓扑
    Chapter #0:11: start 452.140000, end 515.373000: S12 块状 KV 来源：仅此 4 层
    Chapter #0:12: start 515.373000, end 565.940000: S13 稀疏索引：8 个 indexer
    Chapter #0:13: start 565.940000, end 626.610000: S14 算式揭晓：890 B/token 账本
    Chapter #0:14: start 626.610000, end 677.376000: S15 另一种记忆：SWA 状态槽
    Chapter #0:15: start 677.376000, end 739.086000: S16 状态分工：落盘区与丢弃区
    Chapter #0:16: start 739.086000, end 794.756000: S17 显存反转：状态槽与块状键值的交汇
    Chapter #0:17: start 794.756000, end 841.626000: S18 原生草稿：多词预测与非因果块
    Chapter #0:18: start 841.626000, end 894.460000: S19 动态验证：置信度头与变长预算
    Chapter #0:19: start 894.460000, end 955.860000: S20 暂停互动：解码半区为什么能被截断？
    Chapter #0:20: start 955.860000, end 1018.530000: S21 全景索引：模型特性与引擎机制对照
    Chapter #0:21: start 1018.530000, end 1077.600000: S22 总结预告：三句话与请求在代码里的一生
  Stream #0:0[0x1](und): Video: h264 (High), yuv420p, 1920x1080, 30 fps
  Stream #0:1[0x2](und): Audio: aac (LC), 48000 Hz, stereo, 185 kb/s

[Parsed_loudnorm_0] 
{
	"input_i" : "-16.05",
	"input_tp" : "-1.39",
	"input_lra" : "2.40",
	"input_thresh" : "-26.37",
	"output_i" : "-16.08",
	"output_tp" : "-1.50",
	"output_lra" : "2.40",
	"output_thresh" : "-26.40",
	"normalization_type" : "dynamic",
	"target_offset" : "0.08"
}
```

## 问题与处理

- 48 kHz AAC 广播级双声道音频完全符合标准。
- libass 像素级硬字幕烧录无重叠，MarginV 55 确保不侵入主舞台内容。
- 22 个章节元数据准确定位至毫秒级。
- G9 成片 QC 测量全部合格，成片交付。
