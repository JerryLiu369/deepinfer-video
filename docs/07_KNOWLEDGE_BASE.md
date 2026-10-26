# 07 知识库：已有材料怎么用

上一轮项目（写一本书《读懂 DeepInfer》）已经做了大量调研。这个视频项目**不从零开始**，但也**不照单全收**。

## 1. 位置与内容

默认路径 `../deepinfer-book/research`（相对本 Spec 根目录），可用环境变量 `DV_KB` 改。

| 路径 | 内容 | 可信度 | 用法 |
| --- | --- | --- | --- |
| `sources/DeepInfer` | 源码克隆 @ `9bd9cf2`（2026-10-21），含 `doc/inference_deployment_qa.md`、README | 一手 | A 级证据唯一来源 |
| `sources/vllm`、`sources/sglang`、`sources/deepseek-recipe` | 对照组源码（版本见 `versions.md`） | 一手 | EP05–EP12 的对比 |
| `versions.md` | 四个仓库与 6 个 vendor 子模块的 commit | 一手记录 | 版本基线 |
| `notes/R01–R18` | 18 份结构化研究笔记，每条带 `路径:行号` 与等级 | **线索**（质量较高，但由模型写成） | P2 的起点；入账前必须复核 |
| `open_questions.md` | 6 个已查明的争议点 | 线索 | 直接参考结论，入账前复核 |
| `chapters/`、`deepinfer_book.pdf` | 书稿 | **低**（已知有错） | 只当"讲法参考"，不当证据 |
| `figures/` | 书的 mermaid 图 | 低 | 不复用 |

源码目录约 1.2 GB，**不要复制**到视频项目里，只读引用。

## 2. 笔记索引（按集）

| 笔记 | 主题 | 主要服务的集 |
| --- | --- | --- |
| R01 | 一手资料清单、官方原话、知乎与 QA 的关系 | EP00、EP02、EP11 |
| R02a | 注意力与 KV：MLA/MQA、每层类型、890 B/token 推导、SWA 状态 | EP03、EP06 |
| R02b | 层结构：encoder/decoder（`n_prefill_layer`）、YOCO 共享 KV、Engram | EP03、EP07 |
| R02c | 参数分解（763.2B 中 196.9B 是 Engram 表）、MTP/DSpark 草稿、视觉、拓扑 | EP03、EP09 |
| R03 | 仓库地图、代码量、vLLM 派生文件清单 | EP04 |
| R04 | 请求生命周期、进程模型、RPC、ZOS 的执行顺序 | EP04、EP05 |
| R05 | 调度：ZOS 细节、`gather_input_ids_zos`、分块 | EP05 |
| R06 | KV 与状态缓存：三个 128、`StateBlock`、无自动前缀缓存 | EP06 |
| R07 | SWA 有界重放、YOCO 截断、等价性测试 | EP07 |
| R08 | 并行：DP 投票与陪跑步、MoE 六段流水、EPLB | EP08 |
| R09 | 投机解码：吞吐曲线、DFlash 块并行、两份实现 | EP09 |
| R10 | 内核与双硬件：5 个库、TileLang 镜像、Mega MoE | EP10 |
| R11 | 批不变、确定性采样、结构化输出、评测 | EP10 |
| R12 | 未开源部分：插槽、负载均衡、3FS、recipe | EP02、EP11 |
| R13 | vLLM 现状（V1、async scheduling、"6%"的出处） | EP05、EP12 |
| R14 | SGLang 现状（Day-0 方案、UnifiedRadixCache、overlap 调度） | EP05、EP06、EP09、EP12 |
| R15 | 血统分析：骨架来自 vLLM v0.2.x，删/裁/换三类 | EP04、EP12 |
| R16 | 性能数据口径：Pareto 图是换算值、EP64 vs EP8、口径八问 | EP08、EP12 |
| R17 | 社区反应：PR 分布、行业定调、单机实测 | EP00、EP12、EP13 |
| R18 | 上手：构建链、环境变量优先级、硬件门槛 | EP04、EP13 |

每份笔记的第 1 节"三个最重要的发现"是最快的入口。

## 3. 书稿里已知的错误（反面教材）

抽查书稿第 8 章与对应笔记 R07、源码对照后发现，书稿把笔记里谨慎的结论"写顺了"，出现了以下错误。它们说明了为什么**书稿不能当证据**，也是 viewer 和 tech-reviewer 要警惕的典型错误：

| 书稿说法 | 问题 | 正确情况 |
| --- | --- | --- |
| "140 = 128 + 2×6" | 编造算式 | 代码只要求 KEEP_TOKENS ≥ 128 + 6 = 134；140 是 README 给 V4.1 的设置，比下限多 6，代码没有任何地方解释 140 的构成（R07 #2） |
| "默认取 140" | 混淆默认值 | 代码默认 `TRUNCATION_MODE=off`、`KEEP_TOKENS=0`（`environ.py:188-194`）；140 是 README 推荐值 |
| "以微秒级的时间代价补齐 SWA" | 无证据的数字 | 没有任何来源给出这个耗时 |
| "后 20 层算力直降 98.6%" | 漏了第 20 层 | 第 20 层仍要对全长 L 做 attn_norm 与共享 KV 投影（`decoder_layer.py:137-141`，R07 #13），所以 decoder 半边并非整体省 98.6%；文档原话是"nearly halving total prefill computation" |
| "yoco_equiv.py 证明截断不损伤输出" | 误读测试 | 它验证的是 mask 与 compact 两种截断实现彼此一致；`keep_tokens=0` 时只验证 harness 自身确定性（`yoco_equiv.py:536`、`796-797`，R07 #21）。仓库里没有"截断 vs 不截断"的数值对比 |
| "暴力截断""不可思议的常数开销""全书最具震撼力" | 文风 | 违反旁白规范的禁用词 |
| 核心论点里的"极致" | 文风 | 同上 |

**全书其他章节未逐一核对**，应假定有同类问题。

## 4. 易错陷阱清单

fact-checker 建账、tech-reviewer 审稿时逐条对照。括号里是笔记出处，入账前复核。

### 开源边界

1. 负载均衡器、KV 存储（3FS）、P/D 传输、Entrypoint、弹性伸缩：**只在文档里**。仓库里只有"插槽"（`EngineType`、空虚函数、`should_copy_state()` 恒为 `False`）（R12 #1）。
2. 开源版**没有**自动前缀缓存：`BlockManager` 只是空闲链表 + 引用计数；`fork_seq` 是唯一的前缀共享原语（R06 #3）。
3. 文档里的 prefill 二次代价模型 `compute_quota_limit` **不在**代码里；`flops_estimator.hpp` 的二次项只用于 MFU 统计（R05 #3）。
4. "命中长度由谁决定"不在本仓库：代码只提供接收端（`cached_hit_tokens`、`swa_valid_start`）（R07 #17）。

### 数字口径

5. "每 GPU 小时 38 美元"是 DeepSeek 自己说的生产整体收入（谷时定价）；"38.96 美元"是 vLLM 团队在 GB300 NVL72 + AgentX 负载下按 DeepSeek 谷时价格换算的估算毛收入。不能比。
6. "vLLM 在 DeepInfer 的 6% 以内"出自 vLLM 官方 X 推文（不是博客），条件是 GB200、decode、131K、nextn=3、batch 8–256，**没有公布 vLLM 侧 GPU 数与拓扑**；对比对象是 DeepInfer 公布的曲线（R13 #3）。
7. README 的 decode Pareto 图是"实测步频 × (1 + nextn × 假设接受率 75%)"的换算值，不是端到端实测（`plot_pareto.py`、`benchmark.py`，R16 #1）。
8. DSpark 的 +4–7% 指每卡约 60 并发的生产工作点，EP64/DP64；并发 16 时 −1.5%。
9. 模型参数：以 HF `config.json` 推算为准（R02c 给出 763.2B 总参数），媒体报道的 552B 等数字是 D 级，不用。
10. EPLB 的 `moe_lb` 有两套口径、两份文档数字不同（`open_questions.md` Q01）。
11. 有界重放的实测 TTFT 降幅（25–45%，vLLM/GB200，C 级）不是 50%；"减半"是文档对计算量的说法（R07 #3）。

### 名字与概念

12. "encoder/decoder 层"是文档术语；代码里是 `n_prefill_layer` 之前/之后、`yoco consumer`（R02b）。CED 在代码里不出现。
13. 三个"128"：块大小（128 个压缩前 token）、落盘粒度 `KVSTORE_GRAIN`、128 **字节**对齐（R06 #1）。
14. 134 与 140 是两个对象：134 = 128 + 6 是存储与命中口径；140 是保留行数的设置（R07 #2）。6 = nextn + 1，nextn 默认 5（`environ.py:129-132`）。
15. "3 层 MTP"与"每步猜 5 个"是两个独立超参（R02c #2）。
16. 开源代码里没有张量并行：没有 TP group，只有 DP/CP/EP（R04 #1）；文档说生产也不用 TP 和 CP，但代码支持 CP。
17. ZOS 只把 decode 步的后处理推迟一步；prefill 步仍同步（R05 #1）。
18. 异步/零开销调度不是 DeepInfer 首创，文档明说参考 SGLang 和 NanoFlow。
19. 结构化输出的后端是上游 xgrammar；DeepInfer 自研的是调度与搬运（R11 #3）。

### 运行与测试

20. 没有人跑过 DeepInfer；仓库没有 CI 产物，测试"存在"不等于"通过"。
21. 示例默认单机 8 卡 EP8；文档的最小高效部署单元是 64 卡 prefill + 64 卡 decode（R18 #3）。

## 5. 外部来源可信度

| 来源 | 处理 |
| --- | --- |
| DeepInfer 源码、README、`doc/` | 首选（A/B） |
| DeepSeek 官方知乎、官方 X、HF 模型卡、技术报告 | 首选（B） |
| vLLM、SGLang 官方仓库、文档、官方博客、官方推文 | 可用（B/C），注意时效，以本地克隆代码核对 |
| 新闻媒体（Bloomberg、The Decoder 等） | 只作背景（D） |
| AlphaSignal、各类"XX 详解"、聚合站、`deepinfer.net`（不是官方站） | 只作线索（D），必须追到原始出处 |
| Reddit、Hacker News、知乎回答 | 只用于 EP12/EP13 的"社区怎么看"（D） |
