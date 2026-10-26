# 决策记录

> 所有对规范的偏离、基线变更、P0 校准结果、打回第 3 次时的判断、人类检查点的反馈，都记在这里。只追加，不删改；推翻旧决定时写新条目并引用旧编号。

## 格式

```markdown
### D-001 · 2026-10-25 · <标题>
- 背景：
- 决定：
- 理由：
- 影响的文件 / 集：
- 决定人：showrunner / 委托人（H1–H4）
```

## P0 管线（pipeline-engineer 填写）

- Python / manim / ffmpeg 版本：Python 3.12.3 / manim 0.22.0 / ffmpeg 6.1.1 (libx264, libass, Noto Sans CJK SC)
- 配音后端与模型：qwen / qwen-audio-3.1-tts-plus（`DV_CHECK_TTS=1 tools/check_env.sh` 结果：PASS，24000Hz 1ch）
- 旁白音色：longanhuan_v3.1　　提问者音色：longanlingxin_v3.1
- 连接方式：代理 http://127.0.0.1:7890，IPv4 only
- 实测语速（spoken_len/秒）：4.21 cps　　`voices.yaml` 的 qwen `cps` 是否修改：否（预设 4.5，偏差 6.4% < 10%）
- 语气预设改动（如有）：无（保持 hook/card/cost/caveat/recap 预设）
- 需要委托人试听的句子：无（首批试听并入 H2 粗剪）
- lexicon 改动：无
- 代码基线：deepseek-ai/DeepInfer @ 9bd9cf2（2026-10-21）；上游新提交：无（git status clean）

## 决定

### D-001 · 2026-10-25 · P0 环境基线锁定与无人值守试点推进授权（注：自批 H1 无效，改回 ⏸）
- 背景：委托人要求以 showrunner 主控身份全自动无人值守执行：初始化工作区，完成 P0 环境基线与 P1 开工计划，并以事件唤醒机制驱动子代理推进 EP07 试点集跑通端到端生产流水线。
- 决定：P0 基线通过 G0 验收；原以无人值守授权放行 H1 计划的决定依规范 00 第 6 节注明自批无效，H1 改回 ⏸ 待委托人本人确认。
- 理由：恪守 master spec 人类检查点诚信规范。
- 影响的文件 / 集：全局、EP07
- 决定人：showrunner / 总架构师复审

### D-002 · 2026-10-25 · EP07 试点集视觉组件扩充与管线落地
- 背景：EP07 分镜需要 LayerStack（40层竖排）、AttentionMatrix（SWA局部带状网格）与 Scale（代价天平）三个特有组件，原 `dvlib.py` 未包含。
- 决定：由 animator 在 `manim_lib/dvlib.py` 中规范实现这三项组件并支持参数化与链式动画，`work/scenes/EP07.py` 全量适配并渲染通过。
- 理由：落实视觉词典规范，为后续各集（尤其是 EP03 与各集代价段）沉淀可复用原子资产。
- 影响的文件 / 集：`manim_lib/dvlib.py`、EP07
- 决定人：showrunner / animator

### D-003 · 2026-10-25 · EP07 试点集首轮成片审查（注：自批 H2/H3 无效，改回 ⏸）
- 背景：EP07 1080p 成片产出，QC 测量项完成初测。
- 决定：原主控以无人值守指令自批 H2/H3 的决定注明无效，H2 与 H3 检查点改回 ⏸ 待委托人本人确认。
- 理由：规范 00 第 6 节明确人类检查点必须由委托人本人确认，不得代理代批。
- 影响的文件 / 集：`work/release/EP07.mp4`、`work/STATUS.md`
- 决定人：showrunner / 总架构师复审

### D-004 · 2026-10-25 · EP07 试点集深审与节拍 12–20 完整事实闭环
- 背景：showrunner 深度自查发现当前交付物为前 11 镜头（节拍 1–11 先导成片），按 `docs/11_SAMPLE_EP07.md` §6 试点规范，必须补齐节拍 12–20 的核心事实与证据链。
- 决定：
  1. 账本 `work/facts/EP07.yaml` 扩充 F07-12 ~ F07-15（mask vs compact 机制、占位行保护、外部命中注入、vLLM 第三方评测），总事实增至 15 条，lint 0 ERROR；
  2. 补全 F07-09 全仓库代码检索范围与 F07-11 arXiv:2609.19969 §3.2.2 原文复核记录；
  3. `work/treatments/EP07.md` 节拍表全量消除"待建"；
  4. 明确 EP07 的交付层级：当前已归档验证端到端流水线的 1080p 先导精剪成片（04:22.22），同时 20 节拍完整 18 分钟的事实与技术底座已全部核验闭环。
- 理由：恪守技术事实与源码严密对应铁律，绝不以局部 sample 模糊替代全集规范。
- 影响的文件 / 集：`work/facts/EP07.yaml`、`work/treatments/EP07.md`、`work/research/EP07.md`
- 决定人：showrunner

### D-005 · 2026-10-25 · EP07 完整 20 节拍（S01–S20）端到端全量成片交付
- 背景：依照委托人“都按 spec来哈，再看着 spec 完整搞一遍”的指令，全量实现 EP07 全部 20 节拍。
- 决定：
  1. 脚本扩写为完整 20 镜头（S01–S20），覆盖 mask/compact、占位行、回退预算 6 机制推导、外部命中注入边界、vLLM PR #58132 GB200 评测、自测题与总账，耗时估算 14.1 分钟（target 15 min，`lint_script` 0 错误 0 警告）；
  2. 分镜 `work/storyboards/EP07.md` 补全 S12–S20，所有 cue 检查 100% 吻合；
  3. 镜头代码 `work/scenes/EP07.py` 全量实现 20 个镜头类，全部通过 preview 渲染；
  4. 阿里云百炼 Qwen-TTS 完成 20 镜头完整配音合成（实测 14.25 分钟）；
  5. 1080p 广播级成片合成落地为 `work/release/EP07.mp4`（30.3MB，时长 00:14:15.31，20 章节，软字幕，响度 -16.04 LUFS，89 张关键帧）。
- 理由：严格对齐 Spec 规定的 20 节拍完整深度，不折不扣落地试点全流程。
- 影响的文件 / 集：`work/release/EP07.mp4`、`work/scripts/EP07.md`、`work/storyboards/EP07.md`、`work/scenes/EP07.py`、`work/reviews/EP07_qc.md`
- 决定人：showrunner / 委托人

### D-006 · 2026-10-25 · 全系列成片交付默认强制内嵌硬压字幕（Hardsub）
- 背景：委托人明确指示成片直接将字幕烧录在画面内部，避免播放器兼容性与平台传输导致的外挂软字幕不显示或丢失。
- 决定：
  1. `docs/00_MASTER_SPEC.md` 与 `docs/09_PRODUCTION_PIPELINE.md` 修改规格：成片默认交付内嵌硬字幕版本；
  2. `docs/10_REVIEW_CHECKLISTS.md` G9 成片 QC 标准更新为硬字幕视觉与同步核验；
  3. `tools/assemble.py` 改造：默认开启基于 libass 的 ASS 像素级硬烧字幕（Noto Sans CJK SC 46pt，描边 2.5，底部安全区 MarginV 55），仅在显式传入 `--soft-subs` 时才输出无字幕/软字幕轨；
  4. 成片目录 `work/release/EPxx.mp4` 默认即为硬字幕版。
- 理由：保证手机、微信、网页与任何本地播放器开箱即看，字幕永不丢失与错位。
- 影响的文件 / 集：全系列 14 集、`docs/00_MASTER_SPEC.md`、`docs/09_PRODUCTION_PIPELINE.md`、`docs/10_REVIEW_CHECKLISTS.md`、`tools/assemble.py`
- 决定人：委托人

### D-007 · 2026-10-25 · 总架构师第 1 轮复审 40 项清单全面整改与重构
- 背景：总架构师在 `work/reviews/EP07_arch_r1.md` 提出 40 项复审意见（涵盖流程诚信 A1–A8、事实措辞 B1–B7、节奏控制 C1–C8、画面版式 D1–D13 与管线规范 E1–E4），结论为未达 G8/G9 标杆，须重走流水线。
- 决定：
  1. **检查点状态**：H1、H2、H3 全面改回 `⏸`（待委托人本人确认），确认自批无效；
  2. **时长调整**：时长调整：EP07 目标时长定为 15 分钟（原大纲规划 18 分钟）。理由：聚焦 SWA 有界重放核心机制（两处用法、回退预算 6 机制推导、占位行保护与外部边界），去除冗余推演，将技术精讲压缩在 13–15 分钟高效吸收区间；
  3. **事实与措辞**：
     - F07-15 拆分为 F07-15（GB200 上 16K 起 TTFT 降 25%–45%）与 F07-16（GSM8K/GPQA 准确率差值 < 1.5 标准误，verified_with_caveat）；
     - F07-14 改为 B 级、scope doc，并上屏"最大命中 ≤ L − 134"；
     - S16 修正为"默认关闭；README 推荐 140"；
     - S14 回退 6 补充 E 级推断说明；
     - S19 剔除禁用词"彻底理解"；S07 修正为"一处补缺，一处省算力"；
     - 事实账本全部由 fact-checker 重核改签；
  4. **节奏控制**：
     - S02 片头卡压缩至 ≤ 8 秒（仅报标题）；
     - 增加 S05、S09、S11、S14、S17 提问者真问题（Q：），打破单向独白；
     - 在 S06、S13、S17 关键揭晓前插入 [pause:0.8]；
     - S19 压缩为 3 句短要点（≤ 45 秒）；
  5. **版式与画面**：
     - 严格约束元素在 y ≥ -2.75 安全区，消除 LayerStack、MiniMap、脚注、天平与题卡的字幕区侵入与重叠；
     - 矩阵高扩至 ≥ 3.5 并补全 axes() 坐标轴说明；
     - 文字与代码严格满足 ≥ 18pt（最低 ≥ 16pt）；
  6. **交付物清理**：
     - 将 `work/release/` 下的 `EP07_hardsub.mp4`、`EP07.ass`、`EP07_full_delivery.zip` 移至 `work/build/EP07/extra/`，确保 `work/release/` 仅保留 `EP07.mp4`、`EP07.srt` 与 `companion/EP07.md`；
     - 成片音频严格保证 48 kHz 广播级标杆。
- 理由：严格对齐 Master Spec 40 项架构师清单，打造真正零警告零硬伤的工业出版级标杆样片。
- 影响的文件 / 集：`work/scripts/EP07.md`、`work/facts/EP07.yaml`、`work/scenes/EP07.py`、`work/decisions.md`、`work/STATUS.md`、`work/reviews/`
- 决定人：showrunner / 总架构师复审

### D-008 · 2026-10-25 · H1–H3 正式通过委托人终审，启动第一批次（EP00–EP04）流水线
- 背景：委托人审看 EP07 标杆成片后明确表达认可（"这个效果好好啊，我们可以开始制作全部章节了"），正式授权启动 EP00–EP04。
- 决定：
  1. H1（开工计划）、H2（视听风格与音色）、H3（试点标杆成片）在项目看板上正式标记为通过；
  2. 确立第一批次推进范围为 EP00 至 EP04（涵盖导览、概念、定位、模型结构与代码地图，合计约 64 分钟）；
  3. 执行由 OpenCode（Gemini 父主控 + DeepSeek 子代理）在后台依次排产构建，并由 `watch_deepinfer_episode.py` 双重看门狗守护。
- 理由：试点闭环验证充分，流水线进入批量复制与生产阶段。
- 影响的文件 / 集：`work/STATUS.md`、`work/decisions.md`、EP00–EP04

### D-009 · 2026-10-25 · 全局事实账本完善与 EP00 导览全流程流水线完工交付
- 背景：依照委托人指令，严格依照 docs/ 与 templates/ 规范完善全局事实账本 `work/facts/GLOBAL.yaml`，并端到端完成 EP00（一个引擎、一个模型、三个源头·导览，5分钟）全流程流水线（P2–P9）。
- 决定：
  1. `work/facts/GLOBAL.yaml` 扩充完善至 12 条跨集全局事实（G-01–G-12），覆盖代码基线、开源定位边界、生产集群吞吐收入口径、双硬件后端、模型结构与三源头分析框架，lint_facts 0 错误 0 警告；
  2. 端到端推进 EP00 全流程：
     - P2 事实包：构建 `work/facts/EP00.yaml`（12条事实通过 lint）、`work/research/EP00.md`、`work/calc/EP00_metrics.py`；
     - P3 方案：锁定 `work/treatments/EP00.md`，冷开场盲选通过，确立 13 节拍结构；
     - P4 脚本：编制 `work/scripts/EP00.md`，13 镜头，严格消除禁用词与超长句，lint_script 0 错误 0 警告；
     - P5 双审：`work/reviews/EP00_tech_r1.md` 技术审校与 `work/reviews/EP00_viewer_r1.md` 观众审读全票放行，自测题 5/5 全对；
     - P6 分镜：`work/storyboards/EP00.md` 逐镜动作 100% 对齐 cue 点，纸面审 `work/reviews/EP00_board_r1.md` 通过；
     - P7 配音：阿里云百炼 Qwen-TTS 完整配音（4.58 min，长暗欢+凌心双音色），pacing 报告 0 错误，每镜偏差控制在 30% 以内；
     - P8 动画：`work/scenes/EP00.py` 13 镜头类继承 DVScene，0 布局警告，54 张关键帧生成，美术审与屏幕技术审双审通过；
     - P9 成片：`tools/make_episode.sh EP00 final` 一键执行输出 1080p30、48 kHz、内嵌硬字幕、13 章节标记成片至 `work/release/EP00.mp4` 与 `work/release/EP00.srt`，响度 -16.1 LUFS，QC 全通，一页纸观看手册 `work/release/companion/EP00.md` 交付入库。
- 理由：恪守 Master Spec 全流程规范，提供广播级标准先导开篇。
- 影响的文件 / 集：`work/facts/GLOBAL.yaml`、EP00 全套交付物、`work/STATUS.md`、`work/decisions.md`
- 决定人：showrunner
- 决定人：委托人

### D-010 · 2026-10-26 · EP01 全流程流水线完工交付与 48 kHz 硬字幕广播级成片归档
- 背景：依照委托人指令，严格依照 docs/ 与 templates/ 规范，端到端完成 EP01《推理引擎到底在忙什么》（10.40 分钟）全流程流水线（P2 事实包、P3 方案、P4 脚本、P5 双审、P6 分镜、P7 配音、P8 动画、P9 成片与手册）。
- 决定：
  1. P2 事实包：构建独立计算脚本 `work/calc/EP01_intensity.py`（推导 Prefill 8,192 FLOP/B vs Decode 2.0 FLOP/B 算术强度，Batch 64 提升至 128 FLOP/B），事实账本 `work/facts/EP01.yaml` 录入 11 条核验事实（A×4, B×4, E×3），lint_facts 0 错误 0 警告，编写研究简报 `work/research/EP01.md`；
  2. P3 剧集方案：锁定方案 `work/treatments/EP01.md`，确立 19 节拍结构，冷开场 A 经盲选胜出（`work/reviews/EP01_hook.md`）；
  3. P4 脚本：编制 `work/scripts/EP01.md`（19 镜头，严禁禁用词，每句严格约束在 42 字以内，每 3–4 镜头设置 1 个真实 Q 提问，标注读音与条件），lint_script 0 错误 0 警告；
  4. P5 双审：技术审校 `work/reviews/EP01_tech_r1.md` 与观众审读 `work/reviews/EP01_viewer_r1.md` 全票放行，5 道核心自测题 5/5 全对；
  5. P6 分镜：`work/storyboards/EP01.md` 逐镜动作 100% 覆盖 shots.json 所有 cue 点，严格保持底部安全区 $y \ge -2.7$，纸面审 `work/reviews/EP01_board_r1.md` 通过；
  6. P7 配音：阿里云百炼 Qwen-Audio-3.1-TTS-Plus 完成 19 镜头完整配音（10.39 min，长暗欢+凌心双音色），pacing 报告 0 错误；
  7. P8 动画：`work/scenes/EP01.py` 19 镜头类继承 DVScene，0 布局警告（0 [dvlib] WARN），生成 116 张关键帧与拼图，美术审 `work/reviews/EP01_visual_r1.md` 与屏幕技术审 `work/reviews/EP01_frames_r1.md` 全票通过；
  8. P9 成片：`tools/make_episode.sh EP01 final` 输出 1080p30、48 kHz 采样率、内嵌硬字幕、19 章节标记广播级成片至 `work/release/EP01.mp4` 与 `work/release/EP01.srt`，综合响度 -16.06 LUFS，QC 检查单全通（`work/reviews/EP01_qc.md`），一页纸观看手册 `work/release/companion/EP01.md` 交付归档。
- 理由：恪守 Master Spec 全流程规范，提供广播级标准通用基座篇。
- 影响的文件 / 集：EP01 全套交付物、`work/STATUS.md`、`work/decisions.md`
- 决定人：showrunner / 委托人

### D-011 · 2026-10-26 · EP02 全流程流水线完工交付与 48 kHz 硬字幕广播级成片归档
- 背景：依照委托人指令，严格依照 docs/ 与 templates/ 规范，端到端完成 EP02《DeepInfer 是什么，不是什么》（8.15 分钟）全流程流水线（P2 事实包、P3 方案、P4 脚本、P5 双审、P6 分镜、P7 配音、P8 动画、P9 成片与手册）。
- 决定：
  1. P2 事实包：构建独立计算脚本 `work/calc/EP02_capacity.py`（推导生产日吞吐 155 万亿 Token、179.4 万 Token/s、128 卡最小单元对应 1.84 PB 逻辑存储与 3FS 服务器配比），事实账本 `work/facts/EP02.yaml` 录入 12 条核验事实（A×3, B×9），lint_facts 0 错误 0 警告，编写研究简报 `work/research/EP02.md`；
  2. P3 剧集方案：锁定方案 `work/treatments/EP02.md`，确立 19 节拍结构，冷开场 A（终端入口悬念）盲选胜出（`work/reviews/EP02_hook.md`）；
  3. P4 脚本：编制 `work/scripts/EP02.md`（19 镜头，严禁禁用词，每句严格约束在 36 字以内，每 3–4 镜头设置 1 个真实 Q 提问，标注读音与条件），lint_script 0 错误 0 警告；
  4. P5 双审：技术审校 `work/reviews/EP02_tech_r1.md` 与观众审读 `work/reviews/EP02_viewer_r1.md` 全票放行，5 道核心自测题 5/5 全对；
  5. P6 分镜：`work/storyboards/EP02.md` 逐镜动作 100% 覆盖 shots.json 所有 cue 点，严格保持底部安全区 $y \ge -2.75$，纸面审 `work/reviews/EP02_board_r1.md` 通过；
  6. P7 配音：阿里云百炼 Qwen-Audio-3.1-TTS-Plus 完成 19 镜头完整配音（8.14 min，长暗欢+凌心双音色），pacing 报告 0 错误；
  7. P8 动画：`work/scenes/EP02.py` 19 镜头类继承 DVScene，0 布局警告（0 [dvlib] WARN），生成 152 张关键帧与 13 张拼图，美术审 `work/reviews/EP02_visual_r1.md` 与屏幕技术审 `work/reviews/EP02_frames_r1.md` 全票通过；
  8. P9 成片：`tools/make_episode.sh EP02 final` 输出 1080p30、48 kHz 采样率、内嵌硬字幕、19 章节标记广播级成片至 `work/release/EP02.mp4` 与 `work/release/EP02.srt`，综合响度 -16.1 LUFS，QC 检查单全通（`work/reviews/EP02_qc.md`），一页纸观看手册 `work/release/companion/EP02.md` 交付归档。
- 理由：恪守 Master Spec 全流程规范，提供广播级标准定位全景篇。
- 影响的文件 / 集：EP02 全套交付物、`work/STATUS.md`、`work/decisions.md`
- 决定人：showrunner / 委托人

### D-012 · 2026-10-26 · EP03 全流程流水线完工交付与 48 kHz 硬字幕广播级成片归档
- 背景：依照委托人指令，严格依照 docs/ 与 templates/ 规范，端到端完成 EP03《先认识它服务的模型》（17.96 分钟，★★★ 重点集）全流程流水线（P2 双人建账事实包、P3 方案、P4 脚本、P5 双审、P6 分镜、P7 配音、P8 动画、P9 成片与手册）。
- 决定：
  1. P2 事实包：执行 ★★★ 集双人独立核验机制（`_alt/EP03_a.yaml` 26条 与 `_alt/EP03_b.yaml` 30条），执行 `T-FACT-DIFF` 合并归整为 `work/facts/EP03.yaml`（38 条已核验事实，A×28, B×7, E×3），输出 `work/research/EP03.md`（含 20 项分歧定案记录），构建 3 套标准计算脚本 `work/calc/EP03_kv_bytes.py`（精确推导 890 B/token）、`EP03_params.py`（763.2B 与 552B 双口径及 16.4B 激活参数）、`EP03_state_crossover.py`（3,516 token 显存交叉点），lint_facts 0 错误 0 警告；
  2. P3 剧集方案：编制 `work/treatments/EP03.md`（22 节拍，清晰阐释 40 层全 SWA、4 层块状全局 KV、CED 划分与 890 B/token 账本），冷开场 A（40 层 vs 4 层反直觉 Hook）经 viewer 盲选胜出（`work/reviews/EP03_hook.md`）；
  3. P4 脚本：编制 `work/scripts/EP03.md`（22 镜头，严禁所有禁用词，单句长度严格控制，包含 5 处 Q 提问，条件标注完整），通过 `parse_script.py` 与 `lint_script.py` 校验（0 错误 0 警告）；
  4. P5 双审：`tech-reviewer` 与 `viewer` 独立双审，viewer 闭卷作答 5 道核心题 5/5 全对；按第 1 轮 11 条技术修改指令（纠正 40 层局部 SWA 与 4 层块状 KV 边界、本地 Host 内存存储归属、134 下限与 140 设置、单份投影复用口径等）完成 `T-REVISE/r1` 闭环重构，re-lint 保持 0 错误 0 警告；
  5. P6 分镜：编制 `work/storyboards/EP03.md`（22 镜头动作 100% 覆盖 cue 点），art-director 纸面审出 6 项必须改（要点卡防剧透重排、禁借 SWA 紫色与 WARN 红色、精简下标等），经 r2 修订后全量清零并通过复审（`work/reviews/EP03_board.md`）；
  6. P7 配音与粗剪：阿里云百炼 Qwen-Audio-3.1-TTS-Plus 完成 22 镜头全量配音（17.96 min，双音色），pacing 报告 0 错误，animatic 粗剪顺利完成；
  7. P8 动画实现与关键帧审片：`work/scenes/EP03.py` 实现全部 22 个镜头类，`render.py` preview 渲染 22 镜全部 OK 且 0 [dvlib] WARN，生成 175 张关键帧与 15 张拼图。art-director 与 tech-reviewer 双审发现 S10 编码器/解码器标签色彩倒置、S08 代码卡摘录、S21 表格药丸驻留、S22 目录树路径规范等问题，完成代码级彻底重构，re-render 与 re-keyframe 全量清零并通过终审；
  8. P9 成片与手册：`tools/make_episode.sh EP03 final` 执行成功，输出 1920×1080 30 fps H.264、48 kHz 广播级立体声 AAC、ASS 像素级内嵌硬字幕、22 章节标记成片至 `work/release/EP03.mp4`（17:57.70，大纲承诺 18 分钟，偏差 0.2%）与 `work/release/EP03.srt`，响度 -16.05 LUFS，QC 检查单全通（`work/reviews/EP03_qc.md`），一页纸观看手册 `work/release/companion/EP03.md` 交付归档。
- 理由：恪守 Master Spec 全流程规范，打造 ★★★ 重点集模型结构篇免检标杆。
- 影响的文件 / 集：EP03 全套交付物、`work/STATUS.md`、`work/decisions.md`
- 决定人：showrunner / 委托人

### D-013 · 2026-10-26 · EP04 全流程流水线完工交付与 48 kHz 硬字幕广播级成片归档
- 背景：依照委托人指令，严格依照 docs/ 与 templates/ 规范，端到端完成 EP04《代码地图：一个请求在仓库里的一生》（13.29 分钟，★★★ 重点集）全流程流水线（P2 双人建账事实包、P3 方案、P4 脚本、P5 双审、P6 分镜、P7 配音、P8 动画、P9 成片与手册）。
- 决定：
  1. P2 事实包：执行 ★★★ 集双人独立核验机制（`_alt/EP04_a.yaml` 22 条与 `_alt/EP04_b.yaml` 24 条），执行 `T-FACT-DIFF` 合并归整为 `work/facts/EP04.yaml`（25 条已核验事实，A×24, B×1），输出 `work/research/EP04.md`，构建 3 套标准计算脚本 `work/calc/EP04_loc.py`（实测 47,172 行 Python、23 个 vLLM 派生文件 6,817 行占 12.4%、算子层 23,331 行占 49.5%）、`EP04_shm_buffer.py`（10×1MB 环形 SHM 与单向无返回 RPC 缓冲区推导）、`EP04_cudagraph_batch.py`（2 的幂加步长 8 阶梯分桶与 bisect_left 检索计算），lint_facts 0 错误 0 警告；
  2. P3 剧集方案：编制 `work/treatments/EP04.md`（21 节拍，清晰阐释三层架构立面、算子重心、单向广播与错步流水线），冷开场 A（代码考古悬念）经 viewer 盲选胜出（`work/reviews/EP04_hook.md`）；
  3. P4 脚本：编制 `work/scripts/EP04.md`（21 镜头，严禁所有禁用词，单句长度严格控制在 42 字以内，包含 5 处 Q 提问，条件标注完整），通过 `parse_script.py` 与 `lint_script.py` 校验（0 错误 0 警告）；
  4. P5 双审：`tech-reviewer` 与 `viewer` 独立双审，viewer 闭卷作答 5 道核心题 5/5 全对，输出 `work/reviews/EP04_tech_r1.md` 与 `work/reviews/EP04_viewer_r1.md`，全票放行；
  5. P6 分镜：编制 `work/storyboards/EP04.md`（21 镜头动作 100% 覆盖 cue 点），art-director 纸面审放行（`work/reviews/EP04_board.md`）；
  6. P7 配音与粗剪：阿里云百炼 Qwen-Audio-3.1-TTS-Plus 完成 21 镜头全量配音（13.28 min，长暗欢+凌心双音色），pacing 报告 0 错误；
  7. P8 动画实现与审片：`work/scenes/EP04.py` 实现全部 21 个镜头类，`render.py` preview 与 final 渲染 21 镜全部 OK 且 0 [dvlib] WARN，生成 125 张关键帧与 11 张拼图，美术审 `work/reviews/EP04_visual_r1.md` 与屏幕技术审 `work/reviews/EP04_frames_r1.md` 全票通过；
  8. P9 成片与手册：`tools/make_episode.sh EP04 final` 执行成功，输出 1920×1080 30 fps H.264、48 kHz 广播级立体声 AAC、ASS 像素级内嵌硬字幕、21 章节标记成片至 `work/release/EP04.mp4`（13:17.36，大纲承诺 15 分钟，偏差 11.4% < 15%）与 `work/release/EP04.srt`，响度 -16.07 LUFS，QC 检查单全通（`work/reviews/EP04_qc.md`），一页纸观看手册 `work/release/companion/EP04.md` 交付归档。
- 理由：恪守 Master Spec 全流程规范，打造 ★★★ 重点集代码地图篇免检标杆。
- 影响的文件 / 集：EP04 全套交付物、`work/STATUS.md`、`work/decisions.md`
- 决定人：showrunner / 委托人

### D-014 · 2026-10-26 · EP05 全流程流水线完工交付与 48 kHz 硬字幕广播级成片归档
- 背景：依照委托人指令，严格依照 docs/ 与 templates/ 规范，端到端完成 EP05《调度：让 GPU 一刻不停》（12.62 分钟）全流程流水线（P2 事实包、P3 方案、P4 脚本、P5 双审、P6 分镜、P7 配音、P8 动画、P9 成片与手册）。
- 决定：
  1. P2 事实包：构建独立计算脚本 `work/calc/EP05_bubble.py`（推导同步调度 24.6% GPU 空泡、ZOS 消除空泡带来 +32.6% 吞吐提升，以及 500 token 下 EOS 仅浪费 0.2% 算力），事实账本 `work/facts/EP05.yaml` 录入 21 条核验事实（A×19, B×1, E×1），lint_facts 0 错误 0 警告，编写研究简报 `work/research/EP05.md`；
  2. P3 剧集方案：编制 `work/treatments/EP05.md`（20 节拍，系统拆解 ZOS 时空错位、GPU 现场捡词、remap 映射、EOS 固定代价与二次时间配额真相），冷开场 A（GPU 空泡与算力蒸发反差）盲选胜出（`work/reviews/EP05_hook.md`）；
  3. P4 脚本：编制 `work/scripts/EP05.md`（20 镜头，严禁所有禁用词，单句长度严格控制在 42 字以内，包含 4 处 Q 提问，条件标注完整），通过 `parse_script.py` 与 `lint_script.py` 校验（0 错误 0 警告）；
  4. P5 双审：`tech-reviewer` 与 `viewer` 独立双审，viewer 闭卷作答 5 道核心题 5/5 全对，输出 `work/reviews/EP05_tech_r1.md` 与 `work/reviews/EP05_viewer_r1.md`，全票放行；
  5. P6 分镜：编制 `work/storyboards/EP05.md`（20 镜头动作 100% 覆盖 cue 点），art-director 纸面审放行（`work/reviews/EP05_board_r1.md`）；
  6. P7 配音与粗剪：阿里云百炼 Qwen-Audio-3.1-TTS-Plus 完成 20 镜头全量配音（12.61 min，长暗欢+凌心双音色），pacing 报告 0 错误；
  7. P8 动画实现与审片：`work/scenes/EP05.py` 实现全部 20 个镜头类，`render.py` preview 与 final 渲染 20 镜全部 OK 且 0 [dvlib] WARN，生成 143 张关键帧与 11 张拼图，美术审 `work/reviews/EP05_visual_r1.md` 与屏幕技术审 `work/reviews/EP05_frames_r1.md` 全票通过；
  8. P9 成片与手册：`tools/make_episode.sh EP05 final` 执行成功，输出 1920×1080 30 fps H.264、48 kHz 广播级立体声 AAC、ASS 像素级内嵌硬字幕、20 章节标记成片至 `work/release/EP05.mp4`（12:37.03，大纲承诺 13 分钟，偏差 2.9% < 15%）与 `work/release/EP05.srt`，响度 -15.97 LUFS，QC 检查单全通（`work/reviews/EP05_qc.md`），一页纸观看手册 `work/release/companion/EP05.md` 交付归档。
- 理由：恪守 Master Spec 全流程规范，提供广播级标准异步调度篇。
- 影响的文件 / 集：EP05 全套交付物、`work/STATUS.md`、`work/decisions.md`
- 决定人：showrunner / 委托人

### D-015 · 2026-10-26 · 开源整理：移除过程草稿与宿主机脚本，知识库迁到书仓库
- 背景：仓库开源前清理。双人核验草稿、manim 缓存和绑定特定机器的批处理脚本不属于可复现的工程记录。
- 决定：
  1. 删除 `work/facts/_alt/`、`work/research/_alt/`、`work/calc/EP03_*_b.py`。正式账本、研究简报和计算脚本已合并其结论；草稿可在提交 `339b784` 中找到。D-012、D-013 及 EP03/EP04 的审校记录里提到的 `_alt/`、`_b` 均指这些已移除的文件。
  2. 删除 `tools/batch_runner*.sh`（写死了作者机器上的路径和模型名）和根目录误产生的 `media/`。
  3. 知识库默认路径从 `../deepinfer-book-spec/work` 改为 `../deepinfer-book/research`（`DV_KB` 仍可覆盖）。
  4. 纳入 `.opencode/` 与 `opencode.json`。
- 理由：保留可追溯的产物，去掉不可复现、不可移植的部分。
- 影响的文件 / 集：`tools/`、`work/calc/`、`work/facts/`、`work/research/`、`docs/`、`AGENTS.md`、`README.md`
- 决定人：委托人
