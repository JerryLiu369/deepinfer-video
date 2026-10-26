# EP03 关键帧技术核验（第 1 轮）

- 审校对象：`work/build/EP03/keyframes/` 175 张关键帧（`index.md` 逐行对应），另有 15 张 4×3 拼图 `sheet_*.png`
- 基线：DeepInfer @ `9bd9cf2`；DeepSeek-V4.1-Flash-1017 的 `config.json` / 权重索引；arXiv:2609.19969v1
- 依据：`docs/06_FACT_PROTOCOL.md` §5、§6；`docs/07_KNOWLEDGE_BASE.md` §3、§4；`work/facts/EP03.yaml`、`GLOBAL.yaml`；`work/calc/EP03_*.py`（已重跑）
- 方法说明：本模型不能读图。屏幕文字逐条取自生成这批 PNG 的 `work/scenes/EP03.py`（场景 mtime 04:52:34，早于关键帧 05:05，渲染日志无 layout 警告），并对数字密集的 10 张帧（S03/S04/S05/S13/S14/S15/S16/S17/S20/S21）做 eng OCR 抽查，数字与拉丁串逐字比对。版式、可读性、颜色观感留给 art-director。
- 数字复核：890 / 288 / 68 / 528 / 178 / 356 / 534 / 720 / 170 / 113,920 / 134 / 1,415,040 / 1.35 MiB / 1.63 MiB / 3.13 MB / 3,516 / 3,584 / 28 块 / 763.21B / 552B / 196.61B / 196.93B / 25.80% / 16.42B / 2.15% / 384 / 6 / 24×256=6,144 / 43 项 / 64 / 1 / 512 / 448 / 64 / 1280 / 2,048×8=16,384 / 512 全部与 calc 脚本及账本一致；唯一数字问题见 #15（差额取整）。
- 角标：22 个镜头的 badge 与其 facts 的最弱等级逐一比对，全部相符；scope 取值与镜头内容相符（S03/S04 的 `general` 是 r1 结论，不再提）。

## 问题表

| # | 位置（镜头号 + 原句开头 / 关键帧文件名） | 类型 | 问题 | 建议或正确内容（含证据） | 级别 |
| --- | --- | --- | --- | --- | --- |
| 1 | S10 `EP03-S10_mid.png` / `cue-source.png` 右侧区段标签 | 事实错误 | 两条标签互换：0–19 段标“解码器 (Decoder)”、20–39 段标“因果编码器 (Causal Encoder)”。同一镜头的字幕条（`cue-ced_overview.png` 起）写“Layer 0-19 编码器处理全长”，条柱配色也是 0–19 用 PREFILL、20–39 用 DECODE，标签与字幕、配色三方互相矛盾。`LayerStack` 把 layer 0 画在顶部（`manim_lib/dvlib.py:493-503`），所以视觉上方那段就是 0–19。 | 上半段标“因果编码器 (Causal Encoder)”，下半段标“解码器 (Decoder)”。证据：F03-04（`n_prefill_layer=20`，layer 20 起为 yoco consumer）、F03-05、G-06；`deepinfer/hugging_face/config.py:158-161`、`v4_modules/yoco.py:19-21`。 | 错误 |
| 2 | S08 `EP03-S08_cue-no_full.png` 代码卡“if kv_compress_ratio == 0 and…” | 代码路径 / 事实错误 | 两处错：① 路径 `deepinfer/hugging_face/config.py:104` 处是 `_win_spec` 的 docstring 行，不是这段判断；② 片段把逻辑写反了——真实 `_is_full` 在条件成立时 `return True`，卡片写成 `return False`，且用了源码里不存在的裸变量名。 | 换成 `deepinfer/worker/cache_engine.py:696-699` 原文：`return cfg.cfg.get("kv_compress_ratio", 0) == 0 and cfg.cfg.get("sink_mode", "") != "swa"`（highlight 该行）。V4.1 每层 spec 都是 `sink_mode="swa"`（`config.py:104/115/140`），所以 `_is_full` 返回 False——“无全量注意力层”成立。证据：F03-09、`cache_engine.py:464-466`、`config.py:115`。 | 错误 |
| 3 | S22 `EP03-S22_cue-code_tree.png` 目录树 | 代码路径 | 四个节点里两个在 `9bd9cf2` 不存在：`entrypoints/offline_inference.py`（`deepinfer/entrypoints/` 只有 `__init__.py`、`llm.py`）和 `scheduler/`（无 `deepinfer/scheduler/`）。被 `Indicate` 高亮的正是那条不存在的入口。画面不能靠“示意”兜底：脚注写的是“代码结构源自 … 开源仓库”。 | 改成实际结构：`examples/offline_inference.py`、`deepinfer/entrypoints/llm.py`、`deepinfer/engine/llm_engine.py`、`csrc/engine/scheduler.hpp`、`deepinfer/model_executor/`（均在 `$DV_KB/sources/DeepInfer` 核对）。高亮落在 `examples/offline_inference.py`。 | 错误 |
| 4 | S13 `EP03-S13_cue-candidate.png` 字幕条“每层挑选 top-512 压缩token” | 说过头 | 只有 8 层（4 Full + 4 Reindex）真的选 top-512；30 层 Reuse 复用上一次结果，0–1 层没有全局分支。与同帧图例“30 层 Reuse”自相矛盾。 | 改“带 Indexer 的 8 层各挑 top-512”。证据：F03-07、F03-08；`v4_modules/attn.py:292`。 | 不准确 |
| 5 | S18 `EP03-S18_cue-markov.png` / `cue-fwd_parallel.png` “5 个低秩马尔可夫头 (rank-256)” | 事实表述 | 代码里只构造一组 Markov 头权重（`markov_w1` / `markov_w2`），在 `for step_i in range(max_MTP_value)` 里对 5 个位置各调用一次；不是 5 个独立的头。 | 改“同一个 rank-256 Markov 头，按 5 个位置逐步修正”。证据：`mtp/dflash.py:165-175`（构图一次）、`:310-312`（循环内复用）；F03-32。 | 不准确 |
| 6 | S20 `EP03-S20_cue-full_l20.png` “Layer 20 全长投影 · 承担唯一一次全局写入” | 事实表述 | 块状 KV 有 4 个源层（2/8/14/20），第 20 层只是**解码器半区**唯一的源。说成“唯一一次全局写入”与本集 S12/S14 的四源层账本直接冲突。 | 改“第 20 层承担解码器侧唯一一次全长 KV 投影”。证据：F03-06、F03-35；`worker/cache_engine.py:433-461`。 | 不准确 |
| 7 | S20 全镜头标题“暂停互动：后二十层为什么能被截断？”（`cue-explain.png` 起每帧） | 范围口径 | 第 20 层不被截断：它仍对全序列做 `attn_norm` 并写出全长 KV，只是 query 侧截断；被截断的是 21–39 层。标题与同帧题卡“为何21-39层不产块状KV”矛盾。 | 标题改“第 21–39 层为什么能被截断？”。证据：F03-35、`decoder_layer.py:134-142`。 | 不准确 |
| 8 | S19 `EP03-S19_cue-waste.png` “全量验证 5 词，后两词注定被拒” | 说过头 | 置信度数值本身就是示意；拒绝是概率事件，不是必然。官方文档只说固定验证把算力浪费在“low-probability tokens”上。 | 改“后两词大概率被拒”或“低概率词仍会被验证”。证据：F03-34、`doc/inference_deployment_qa.md:243`；本帧 foot 已标“接受概率数值为示意”。 | 不准确 |
| 9 | S19 角标（全帧）“A 代码证实” | 角标 | 屏幕同时挂着“官方文档：生产使用”（B 级文档断言），角标却只标 A。按“角标取本镜最弱等级”，应为 B。 | 角标改 B；或把 F03-34 拆成 A（默认关闭/置信度头）与 B（生产变长验证）并引 B 那条。证据：`doc/inference_deployment_qa.md:243`；账本 F03-34 现为单一 A 级条目（见“账本问题” 2）。 | 不准确 |
| 10 | S04 标题“激活真相：全 MoE 与百倍稀疏”（`cue-moe_all.png` 起每帧） | 数字口径 | 两个“稀疏倍数”都不是百倍：专家 384/6 = 64×，参数 763.2B/16.42B ≈ 46×。标题是全片可见的量化标签。 | 改“数十倍稀疏”或“64 倍专家稀疏”。证据：F03-23（384/6）、F03-22（16.42/763.2）。 | 不准确 |
| 11 | S20 `cue-bound_134.png` 代码卡“assert keep_tokens >= 128 + 6” | 代码卡 | 变量名与断言行都不是原文：真实断言是 `window_size + envs.DEEPINFER_MAX_BACKTRACKING_TOKENS <= envs.DEEPINFER_YOCO_PREFILL_KEEP_TOKENS`，且只在 `TRUNCATION_MODE != "off"` 时执行；`128 + 6` 是默认值代入后的结果。卡片带等宽字体，会被当成源码。 | 贴 `deepinfer/worker/model_runner.py:107-113` 原文 3 行，caption 写“开启截断时的下限；默认 128+6=134”。证据：F03-38、`environ.py:188-194`。 | 建议 |
| 12 | S16 `EP03-S16_cue-oss_note.png` 代码卡 `'dropped': remote` | 示意措辞 | dropped 区不写长期存储，但会随 PE→CE 传完整 state（`TO_CE` 分支取 `total_bytes_inference`）；`remote` 容易被读成“远端落盘”，正好是 r1 修掉的那个误解。卡片已标“示意/非原文”，风险有限。 | 改 `'dropped': state_to_ce` 或加注“非落盘、随请求传输”。证据：`worker/cache_engine.py:780`、`:790,800`；F03-17 caveat。 | 建议 |
| 13 | S16 `cue-split_intro.png` / `cue-dropped_23.png` “dropped 区：后 20 层 SWA + 草稿 / 约 1.63 MiB” | 口径不全 | 标签只列 23 个 SWA 层（23×70,752 B = 1.55 MiB），而 1.63 MiB 必须加上 3 层 C2 压缩状态 86,016 B 才成立；观众按标签算不出这个数。 | 标签补“+ 3 层压缩状态”，或数字写 1.55 MiB。证据：`calc/EP03_state_crossover.py`、F03-16/F03-17。 | 建议 |
| 14 | S07 `EP03-S07_cue-mhc_title.png` 药丸“Single-Pass mHC (Hyper-Connections)” | 名称出处 | 代码只写 `mhc_mult: number of hyper-connection heads`，展开的是 HC，不是 m；“mHC (Hyper-Connections)”会被读成整体展开。F03-29 caveat 明确要求不给 m 编展开。 | 改“mHC（HC = hyper-connection，`hc_mult=4`）”，或去掉括号。证据：`v4_modules/mhc_modeling.py:48`；F03-29 caveat。 | 建议 |
| 15 | S03 `EP03-S03_cue-backbone.png` “差额约 211B” | 数字口径 | 分项 196.93 + 14.23 + 0.49 = 211.65B，但屏上 763.2 − 552 = 211.2B；差 0.4B 来自 552B 是 551.57B 的取整。两个数都在同一帧，观众一减就对不上。 | 写“差额约 211.6B”，并在脚注加“552B ≈ 551.57B 取整”。证据：`calc/EP03_params.py`（backbone 551.57、engram 196.93、mtp 14.23、vision 0.49）。 | 建议 |
| 16 | S15/S16/S17 状态槽单位：`cue-mb313.png` 3.13 MB vs `cue-cross_hit.png` 1.35 MiB | 单位 | S15/S17 用十进制 MB（3.13、2.8），S16 用 MiB（1.35、1.63）。3.13 MB ≠ 2.98 MiB，跨镜并看会算不平（r1 第 39 条建议未落实）。 | S16 首块标“3.13 MB（2.98 MiB）状态槽”，或全片统一一种单位。证据：`calc/EP03_state_crossover.py` 的 `state_slot_MiB_per_seq = 2.984`、`state_to_disk_MiB_per_seq = 1.349`。 | 建议 |
| 17 | S06 `EP03-S06_cue-sparse.png` 图形“Dense GEMM ✗” | 说过头 | Engram 仍有投影 GEMM（`wkv [25600,6144]`、`q/k [4,5120]`，合计 0.31B 参数）；打叉的图形会被读成整条路径没有 GEMM（字幕条已改为“无百亿规模密集GEMM”，图形没跟上）。 | 图形改“196.6B 表不做 GEMM”。证据：F03-26 conditions、F03-27 caveat。 | 建议 |
| 18 | S13 `EP03-S13_cue-indexer_overview.png` 图例“4 层 Full Indexer / 4 层 Reindex” | 名称出处 | 三个名字来自官方报告，代码里只有 `is_index_source` / `layer_index_module_map`；旁白有“在官方报告的分类里”，图例没有。 | 图例加“（报告术语）”。证据：F03-07 caveat、`config.py:71-74`。 | 建议 |

## 账本本身的问题（交 showrunner 转 fact-checker）

1. **F03-09 的 `evidence` 路径错，直接导致了 #2 的关键帧错误。** 条目列 `deepinfer/hugging_face/config.py:284`，但该行是 `_build_moe` 里的 `window_size=...`；`_is_full` 与它引的 `return cfg.cfg.get("kv_compress_ratio", 0) == 0 and …` 在 `deepinfer/worker/cache_engine.py:696-699`。应改路径，并保留 `config.py:104/115` 作为 `sink_mode="swa"` 的依据。
2. **F03-34 仍是单一 A 级，但含 B 级断言。** “官方文档描述生产使用变长验证”（`doc:243`）是 B，与代码默认关闭（A）混在一条，导致 S19 角标 A（见 #9）。建议拆 A/B 或加等级说明——r1 已提，仍未落实。
3. **F03-16 的 `screen` 与 `claim` 单位不一致。** `screen: 状态 3.13 MB / 序列`，`claim` 写 3,128,928 B（2.98 MiB）；同一个值两种单位，建议 `screen` 写“3.13 MB（2.98 MiB）”。
4. **账本没有覆盖 S22 的目录树结构。** 屏幕上出现了 4 条 `路径`，但没有任何一条事实条目为它们背书（06 要求“账本里没有的不许出现在成片里”）。建议新增一条 A 级事实，列 3–5 个真实入口路径，供 S22 与 EP04 复用；否则删掉这棵树。

## 三句话

1. 数字关基本干净：175 张帧上的派生数字与三个 calc 脚本逐一吻合，四个源层的 890 账本、状态槽 3.13 MB/2.98 MiB、交叉点 3,516/28 块都站得住。
2. 三处必须改：S10 编码器/解码器标签画反（整镜核心图自相矛盾）、S08 代码卡把 `_is_full` 逻辑写反且指到 `config.py:104`、S22 目录树两条路径在 `9bd9cf2` 不存在（含被高亮的入口）。
3. 其余是“说过头/口径不全”：S13“每层挑 top-512”、S18“5 个 Markov 头”、S20“唯一一次全局写入”、S19“注定被拒”与 A 角标；账本侧 F03-09 的路径必须同步修正，否则下一轮还会画出同一张错卡。

---

# 第 2 轮复核（r2，2026-10-26）

- 复核对象：同 r1 的 175 帧 / 190 个 PNG。全部 PNG 在 05:37 重新生成（无早于 05:35 的残留）；`work/scenes/EP03.py` mtime 05:34:16，`renders/EP03-S*.mp4` 05:34–05:37 逐镜重渲染，`EP03.mp4` 05:42 重合成——本轮结论对应的是修后画面，不是旧帧。
- 方法同 r1：不能读图；屏幕文字取自场景代码（`work/scenes/EP03.py`），对 S08/S10/S13/S18/S20/S22 做 eng OCR 复核拉丁串与数字坐标（中文 OCR 不可用，中文标签以场景代码为准）。
- 数字复核：重跑 `EP03_kv_bytes.py`、`EP03_state_crossover.py`、`EP03_params.py`，输出与 r1 列出的 890 / 288 / 68 / 528 / 178 / 356 / 28 块 / 3,516 / 3.13 MB / 1.35 MiB / 763.21B / 552B / 196.93B / 25.80% / 16.42B / 2.15% 逐项一致；本轮改动只涉及标签与路径，未动数字。

## 上轮 3 条错误

1. **S10 已清零。** `range_label(0,20)`=“因果编码器 (Causal Encoder)”、`range_label(20,40)`=“解码器 (Decoder)”（`EP03.py:627-628`）；`LayerStack` 把 0 层画在顶部，OCR 坐标 “(Causal Encoder)” y=166 位于 “(Decoder)” y=323 之上，与字幕条“Layer 0-19 编码器处理全长”和 PREFILL/DECODE 配色三方一致。
2. **S08 路径与逻辑已清零，摘录未清零。** caption 与注释行均为 `deepinfer/worker/cache_engine.py:696(-699)`，不再出现 `return False`。但卡面正文仍非源码（见 R2-1）。
3. **S22 已清零。** 三条路径在 `9bd9cf2` 真实存在（`git ls-tree -r 9bd9cf2` 命中 `examples/offline_inference.py`、`deepinfer/engine/llm_engine.py`、`csrc/engine/scheduler.hpp`，工作树干净）；OCR 从 `S22_end.png` 读回三条路径，高亮落在 `examples/offline_inference.py`。

## 问题表（r2 未清项）

| # | 位置（镜头号 + 原句开头 / 关键帧文件名） | 类型 | 问题 | 建议或正确内容（含证据） | 级别 |
| --- | --- | --- | --- | --- | --- |
| R2-1 | S08 `EP03-S08_cue-no_full.png` 代码卡正文 | 代码摘录（r1 #2 残留） | 卡面是 `def _is_full(self, module):` + `return (ratio == 0 and sink_mode != "swa")`。真实源码是 `@staticmethod def _is_full(cfg: dict \| None) -> bool:`（`:695-696`），且省略 `if cfg is None: return False`（`:697-698`）；`ratio`/`sink_mode` 是源码不存在的裸名。带 `路径:行号` 的等宽卡会被当成原文。 | 贴 `:699` 原文 `return cfg.cfg.get("kv_compress_ratio", 0) == 0 and cfg.cfg.get("sink_mode", "") != "swa"`，签名行用 `:695-696`，caption 写 `cache_engine.py:695-699`。证据：F03-09、`worker/cache_engine.py:695-699`。 | 不准确 |
| R2-2 | S04 全帧标题“激活真相：全 MoE 与百倍稀疏”（`cue-moe_all.png` 起） | 说过头（r1 #10 未修） | 两个稀疏倍数都不是百倍：专家 384/6=64×，参数 763.2/16.42≈46×。标题与同帧“384 路由专家·每步激活 6 个”“2.15%”并置，观众一算就对不上。 | 改“64 倍专家稀疏”或“数十倍稀疏”。证据：F03-23（384/6）、F03-22（16.42/763.2）。 | 不准确 |
| R2-3 | S13 `EP03-S13_cue-candidate.png` 字幕条“每层挑选 top-512 压缩token” | 范围错（r1 #4 未修） | 只有 8 层（4 Full + 4 Reindex）选 top-512；30 层 Reuse 复用、0–1 层没有全局分支。与同帧图例“30 层 Reuse / 2 层纯 SWA”自相矛盾。 | 改“带 Indexer 的 8 层各挑 top-512”；24/28/32/36 只在候选池内重选。证据：F03-07、F03-08；`v4_modules/attn.py:292`。 | 不准确 |
| R2-4 | S20 全帧标题“暂停互动：后二十层为什么能被截断？”（`cue-explain.png` 起） | 范围口径（r1 #7 未修） | 第 20 层不被截断：仍对全序列做 `attn_norm` 并写出全长 KV，只有 query 侧截断；被截的是 21–39。同帧题卡“为何21-39层不产块状KV”与标题矛盾。 | 标题改“第 21–39 层为什么能被截断？”。证据：F03-35、`decoder_layer.py:134-142`。 | 不准确 |
| R2-5 | S19 `EP03-S19_cue-waste.png` 卡片“全量验证 5 词，后两词注定被拒” | 说过头（r1 #8 未修） | 0.28/0.09 本身是示意概率；拒绝是概率事件，不是必然。官方文档只说固定验证把算力浪费在“low-probability tokens”上。 | 改“后两词大概率被拒”或“低概率词仍会被验证”。证据：F03-34、`doc/inference_deployment_qa.md:243`；本帧 foot 已标“接受概率数值为示意”。 | 不准确 |
| R2-6 | S19 全帧角标“A 代码证实” | 角标（r1 #9 未修） | 同帧挂“官方文档：生产使用”（B 级断言），按“角标取本镜最弱等级”应为 B。`shots.json` 仍 `badge=A`；F03-34 仍是单条 A（账本问题 2）。 | 角标改 B；或把 F03-34 拆成 A（默认关闭/置信度头）+ B（生产变长验证）并引 B 那条。证据：`doc:243`。 | 不准确 |
| R2-7 | S20 `cue-explain.png` 旁白“第 L/2 层已经承担了唯一一次全长投影” | 口径（屏幕已修，旁白未跟） | 屏幕已改为“产出解码半区唯一全局KV”，旁白仍无“解码器半区”限定；编码器侧 2/8/14 同样写全长块状 KV，与本集 S12/S14 的四源层账本冲突。 | 旁白加“解码器侧”。证据：F03-06、F03-35。属脚本层，改旁白需重配 S20。 | 建议 |

## 上轮 18 条状态一览

| 状态 | 条目 |
| --- | --- |
| 已修（4） | #1 S10 标签、#3 S22 目录树、#5 S18 Markov 头（现为“1 组 Markov 头 (rank-256) 自回归采样 5 步”，OCR 复核）、#6 S20 “解码半区唯一全局KV” |
| 部分（2） | #2 S08（路径+逻辑已改，摘录仍非原文 → R2-1）、#11 S20 代码卡（行号 110 已对，仍非原文且路径缺 `deepinfer/worker/`） |
| 未修（12） | #4/#7/#8/#9/#10（R2-2…R2-6 的不准确）；#12 `'dropped': remote`、#13 1.63 MiB 标签缺“+3 层压缩状态”、#14 mHC 药丸仍写“(Hyper-Connections)”、#15 仍“差额约 211B”、#16 MB/MiB 混用、#17 图形仍“Dense GEMM ✗”（字幕条已改）、#18 S13 图例仍缺“报告术语” |

## 账本本身的问题（交 showrunner 转 fact-checker）

1. **更正 r1“账本问题 1”：F03-09 本来就含正确路径。** `work/facts/EP03.yaml:191` 列了 `deepinfer/worker/cache_engine.py:696-700`，`quote` 就是 `:699`；文件 mtime 03:26，早于 r1，说明 #2 的错卡不是账本导致的。`config.py:284` 是 `window_size=(text["sliding_window"], 0)`，支撑的是“128 窗口”而非 `_is_full`。建议在 evidence 各行注明支撑哪一句，不必改路径。
2. **F03-34 仍是单条 A 级混 B 断言**（`doc:243`），直接导致 S19 角标只能是 A（R2-6）。建议拆 A/B —— r1 已提，未落实。
3. **F03-16 `screen` 与 `claim` 单位仍不一致**：`screen: 3.13 MB / 序列`、`claim: 3,128,928 B（2.98 MiB）`。建议 `screen` 写“3.13 MB（2.98 MiB）”。
4. **S22 三条路径仍无事实条目**。路径已在 `9bd9cf2` 核实（`git ls-tree`），但按 06 §1“账本里没有的不许出现在成片里”，仍需新增一条 A 级事实列这 3 条路径供 EP04 复用；否则 S22 的 A 角标没有账本支撑。

## 验收结论

- **错误清零：3/3。** S10、S22 完全清零；S08 的“路径”和“逻辑方向”两项清零，只剩代码摘录不准确（R2-1），按 r1 的分级已不构成“错误”。
- **不准确只清 2/7**（#5、#6）；剩余 5 条（R2-2…R2-6）全部是成片可见项，其中 S20 标题、S04 标题、S19 角标与同帧文字/事实直接矛盾。
- **结论：有条件通过。** 错误门已过；final 前须修 R2-1 至 R2-6（S08 代码卡贴原文、S20 标题、S04 标题、S13 字幕条、S19 卡片与角标），账本侧先拆 F03-34 才能把 S19 角标改成 B。r1 的 8 条建议（#12–#18 与 #11 的路径）不阻塞发布。
