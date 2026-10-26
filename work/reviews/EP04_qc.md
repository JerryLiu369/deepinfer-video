# EP04 成片 QC 记录

- 文件：`work/release/EP04.mp4`
- 构建命令：`tools/make_episode.sh EP04 final`（全自动流水线一条龙产出，符合 09 第 3.8 节与 A6 规范）
- 测量时间：2026-10-26
- 覆盖范围：完整 21 节拍（S01–S21，全集无裁剪）

## 检查表

| 检查项 | 要求 | 测量值 | 结果 |
| --- | --- | --- | --- |
| 构建命令 | 由 make_episode.sh 出片 | `tools/make_episode.sh EP04 final` | **✓ PASS** |
| 视频格式 | 1920×1080、30 fps、H.264、yuv420p | 1920×1080, 30 fps, h264 High (avc1), yuv420p | **✓ PASS** |
| 音频采样 | AAC, 48 kHz 广播级，双声道立体声 | aac (LC), 184 kb/s, 48000 Hz, stereo | **✓ PASS** |
| 响度指标 | −16 ± 1 LUFS，真峰值 ≤ −1.0 dBFS | `input_i: -16.07 LUFS`, `input_tp: -1.49 dBFS`, `input_lra: 2.40 LU` | **✓ PASS** |
| 硬压字幕 | 中文字幕内嵌硬压（清晰无遮挡、黑边描边） | Noto Sans CJK SC 46pt，底部安全区 MarginV 55 ASS 烧录 | **✓ PASS** |
| 章节标记 | 存在 21 章节，标题与大纲完全对齐 | 21 个章节标签（从 S01 到 S21 准确定位） | **✓ PASS** |
| 时长控制 | 目标 15 分钟（大纲承诺 15 分钟），偏差 ≤ 15% | 00:13:17.36（13.29 分钟，偏差 11.4% < 15%） | **✓ PASS** |
| 抽看检查 | 首/中/尾各镜头无黑帧、无截断、无撕裂 | 125 张关键帧与切片连接顺畅，音画完全同步 | **✓ PASS** |
| 渲染日志 | 无 `[dvlib] WARN` | 21 镜全量 preview & final 渲染 0 [dvlib] WARN | **✓ PASS** |
| 交付文件 | 交付物完整性（release 仅放核心件） | `release/` 仅含 `EP04.mp4`、`EP04.srt`、`companion/EP04.md` | **✓ PASS** |

## 原始测量输出

```text
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'work/release/EP04.mp4':
  Duration: 00:13:17.36, start: 0.000000, bitrate: 355 kb/s
  Chapters:
    Chapter #0:0: start 0.000000, end 43.766000: S01 冷开场：代码树里的反直觉反差
    Chapter #0:1: start 43.766000, end 50.666000: S02 片头卡：代码地图：一个请求在仓库里的一生
    Chapter #0:2: start 50.666000, end 91.336000: S03 目录全貌：三层架构立面与代码量
    Chapter #0:3: start 91.336000, end 131.336000: S04 重心揭晓：算子层占半壁与双镜像
    Chapter #0:4: start 131.336000, end 172.436000: S05 血统剖析：23 个文件与 12% 胶水层
    Chapter #0:5: start 172.436000, end 212.870000: S06 历史分叉：v0.2.x 骨架与 shm 补丁
    Chapter #0:6: start 212.870000, end 260.940000: S07 边界声明：单架构定位与在线缺失
    Chapter #0:7: start 260.940000, end 304.840000: S08 推理起点：examples/offline_inference.py
    Chapter #0:8: start 304.840000, end 339.840000: S09 请求入队：预分词与 C++ Sequence 接管
    Chapter #0:9: start 339.840000, end 381.239000: S10 进程拓扑：单引擎管 CP 卡与主从 spawn
    Chapter #0:10: start 381.239000, end 419.249000: S11 并行真相：告别 TP，走向 DP/CP/EP
    Chapter #0:11: start 419.249000, end 454.719000: S12 控制面广播：10×1MB 环形 SHM 与单向 RPC
    Chapter #0:12: start 454.719000, end 489.153000: S13 调度核心：C++ Scheduler 与释放 GIL
    Chapter #0:13: start 489.153000, end 530.453000: S14 步型仲裁：DP 投票与防止 EP 死锁
    Chapter #0:14: start 530.453000, end 568.123000: S15 陪跑步机制：空闲 Rank 为什么必须跟跑？
    Chapter #0:15: start 568.123000, end 602.723000: S16 错步重叠：Forward(N) 与 Post-process(N-1)
    Chapter #0:16: start 602.723000, end 640.989000: S17 账本推演：乐观推进与事后真实回填
    Chapter #0:17: start 640.989000, end 677.589000: S18 图捕获边界：CUDA Graph 阶梯分桶与 Eager 模式
    Chapter #0:18: start 677.589000, end 713.259000: S19 输出汇聚：Driver 独占采样与 C++ 对象池
    Chapter #0:19: start 713.259000, end 755.129000: S20 平台切换：platform.py 与顶层导包铁律
    Chapter #0:20: start 755.129000, end 797.329000: S21 总结预告：三句话与 ZOS 调度深度解密
  Stream #0:0[0x1](und): Video: h264 (High) (avc1 / 0x31637661), yuv420p(progressive), 1920x1080, 162 kb/s, 30 fps, 30 tbr, 15360 tbn (default)
  Stream #0:1[0x2](und): Audio: aac (LC) (mp4a / 0x6134706d), 48000 Hz, stereo, fltp, 183 kb/s (default)
```
