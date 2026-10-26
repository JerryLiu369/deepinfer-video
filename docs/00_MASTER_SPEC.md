# 00 主控调度指南（MASTER SPEC）

这份文件有两个读者：

- **人类**（委托人）：用它把控全局，知道每一步在干什么、哪里需要自己拍板。
- **showrunner 主代理**（Gemini 3.8 Flash）：把它当作调度程序来执行。第 4 节的流程、第 5 节的调度协议是硬性规定，不是建议。

## 0. 目标

做一部中文技术科普视频系列，让委托人看完后能做到：

1. **讲清定位**：DeepInfer 是什么、不是什么；开源了哪一半，没开源哪一半。
2. **画出结构**：一个请求从进入系统到返回，经过哪些组件，每个组件为什么存在。
3. **讲透机制**：调度（ZOS）、KV 与状态缓存、SWA 有界重放、并行与 EPLB、投机解码（DSpark）、批不变与确定性，每个都能说出"不这么做会怎样 → 怎么做 → 换来什么 → 付出什么"。
4. **追溯原因**：每个设计能追到三个源头之一——模型长什么样、系统怎么部署、生产要什么。
5. **正确对比**：和 vLLM、SGLang 的真实关系（血统、定位、取舍），以及为什么网上流传的性能数字大多不能直接比。
6. **知道怎么继续**：没有 64 张 SM100，也知道从哪读代码、做什么练习。

验收方式不是"视频做完了"，而是：委托人看完每集，能答对《观看手册》里的自测题（H3 检查点）。

## 1. 交付物

| 交付物 | 位置 | 说明 |
| --- | --- | --- |
| 14 集成片 | `work/release/EPxx.mp4` | 1080p30，H.264 + AAC，内嵌硬字幕，章节标记，响度 −16 LUFS |
| 字幕 | `work/release/EPxx.srt` | 与成片同步 |
| 观看手册 | `work/release/companion/EPxx.md` | 一页纸：三句话、关键图、代码入口、5 道自测题与答案 |
| 系列总图 | `work/release/series_map.png` | "一个请求的一生"全景，每站标出对应集号 |
| 工作区 | `work/` | 全部中间产物，可追溯 |
| 精华版（可选） | `work/release/digest.mp4` | 25–30 分钟，H4 后委托人决定是否做 |

## 2. 两个模型的分工

### 2.1 分工原则

**Gemini 管"怎么讲"，DeepSeek 管"真不真、能不能跑"。** 两边的接口只有三个：

1. **事实账本**（`work/facts/*.yaml`）：DeepSeek 写，Gemini 只读、只引用。这是技术信息进入脚本的唯一入口。
2. **分镜**（`work/storyboards/EPxx.md`）：Gemini 写，DeepSeek 照着实现动画。
3. **审校记录**（`work/reviews/`）：双方互相审，只报问题，不改对方的文件。

这样分的理由：

- Gemini 的长处是长文本统筹和视听语言编排，短处是技术细节容易"顺口编"。所以它不许自己生成技术事实。
- DeepSeek 的长处是读代码、推理、算数、写代码，短处是文案。所以它交结构化笔记和代码，不写给观众听的句子。

### 2.2 代理清单

| 代理 | 模型 | 模式 | 职责 | 主要输出 |
| --- | --- | --- | --- | --- |
| `showrunner` | Gemini | primary | 总导演兼调度：拆任务、派发、验收、仲裁冲突、维护系列一致性、更新看板 | `work/plan.md`、`STATUS.md`、`decisions.md` |
| `screenwriter` | Gemini | subagent | 编剧：剧集方案（节拍表）、脚本、观看手册 | `work/treatments/`、`work/scripts/`、`work/release/companion/` |
| `storyboarder` | Gemini | subagent | 分镜：把脚本翻译成精确的画面说明，严格使用视觉词典 | `work/storyboards/` |
| `viewer` | Gemini | subagent | 观众模拟：只读脚本（或看关键帧），列出看不懂的地方，复述要点，做自测题 | `work/reviews/EPxx_viewer_rN.md` |
| `art-director` | Gemini | subagent | 美术审片：看关键帧拼图，查可读性、一致性、信息密度 | `work/reviews/EPxx_visual_rN.md` |
| `fact-checker` | DeepSeek | subagent | 事实核验：读源码和文档，建事实账本，写计算脚本，写研究简报 | `work/facts/`、`work/calc/`、`work/research/` |
| `tech-reviewer` | DeepSeek | subagent | 技术审校：逐句核对脚本、分镜、屏幕文字与数字 | `work/reviews/EPxx_tech_rN.md` |
| `animator` | DeepSeek | subagent | 动画工程：按分镜写 Manim 镜头代码，渲染预览，自查对时 | `work/scenes/EPxx.py` |
| `pipeline-engineer` | DeepSeek | subagent | 管线工程：环境、配音、渲染、合成、修工具 bug、QC 测量 | `work/build/`、`work/release/`、`tools/` 的修复 |

代理定义在 `.opencode/agent/`，每个文件里有完整的角色提示词。showrunner 用 OpenCode 的 task 工具（或 `@代理名`）调用它们。

### 2.3 "几乎无限 token"怎么花

token 不是瓶颈，**质量和一致性**才是。多花 token 的地方：

| 做法 | 用在哪里 | 为什么 |
| --- | --- | --- |
| 双人独立核验 | ★★★ 集（EP03、EP04、EP07、EP12）的事实账本 | 两个 fact-checker 独立建账，再由第三个对比差异。错误在这几集代价最大 |
| 多版本择优 | 每集冷开场写 2 个版本；关键比喻写 2 个版本 | 开场决定能不能看下去，让 viewer 盲选 |
| 多轮审读 | 脚本最多 3 轮"技术审 + 观众审" | 一轮通常只能发现一半的问题 |
| 新上下文审读 | viewer、tech-reviewer 每轮都用新会话 | 避免"看惯了就看不出问题" |
| 计算全部写成脚本 | 所有派生数字 | 让数字可以重跑、可以审 |

不要花 token 的地方：让 showrunner 自己读大段源码或笔记（交给 fact-checker）；让子代理在报告里复述文件内容。

## 3. 知识库

上一轮"写一本书"的项目留下了大量可复用的材料，路径默认是 `../deepinfer-book/research`（环境变量 `DV_KB`）：

- `sources/`：DeepInfer、vLLM、SGLang、deepseek-recipe 的源码克隆，版本见 `versions.md`
- `notes/R01–R18`：18 份结构化研究笔记，带 `路径:行号` 证据与等级
- `chapters/`：书稿。**已知有错，不能当证据**，只能当"讲法参考"
- `open_questions.md`：已查明的 6 个争议点

详细用法、已知错误、易错陷阱见 `docs/07_KNOWLEDGE_BASE.md`。核心规则：**笔记是线索，不是结论**。笔记里的每条事实进入账本前，fact-checker 都要回到源码或文档原文复核一次。

## 4. 流程与关卡

共 11 个阶段。每个阶段有负责人、输入、输出和过关条件（关卡 G0–G10）。没过关不进下一阶段。验收清单的细项在 `docs/10_REVIEW_CHECKLISTS.md`。

```
P0 环境与基线 ─► P1 开工计划 ─►(H1)─► P2 事实包（全部集并行）
                                         │
              ┌──────────────────────────┘
              ▼   以下按集流水线推进；EP07 先走完全程当试点
   P3 剧集方案 ─► P4 脚本 ─► P5 双审（≤3 轮）─► P6 分镜 ┐
                                              └► P7 配音+粗剪 ─(H2 仅试点)┤
                                                                         ▼
                       P8 动画实现 + 审片 ─► P9 成片与 QC ─(H3 仅试点)─► 下一集
                                                                         ▼
                                                     P10 系列统合 ─(H4)─► 交付
```

### P0 环境与基线（showrunner 派 pipeline-engineer、fact-checker）

1. pipeline-engineer：按 `README.md` 装环境，跑 `tools/check_env.sh`，跑通 `examples/smoke`（EP99）。
2. pipeline-engineer：用推荐后端 qwen（Qwen-Audio-3.1-TTS-Plus，凭据在 `.env`）配 EP99。音色已由委托人定下：解说 `longanhuan_v3.1`、提问 `longanlingxin_v3.1`，语气预设见 `03_NARRATION_STYLE.md` 第 12 节，都在 `tools/voices.yaml` 里，P0 不改。要做的是：跑 `DV_CHECK_TTS=1 tools/check_env.sh` 确认凭据和网络；把读错的术语写进 `tools/lexicon.yaml`；实测语速，如果和 `voices.yaml` 里 qwen 的 `cps` 差 10% 以上就改掉。结果写进 `work/decisions.md`。（模型听不了音频时，把试听列进 H2 由人确认。）没有凭据时可以先用 `--backend edge` 跑通管线，但正式配音必须用 qwen。
3. fact-checker：确认知识库里 DeepInfer 的 commit 还是 `9bd9cf2`；`git fetch` 看上游有没有新提交。有新提交就列出改动文件，由 showrunner 决定是否换基线（默认不换，视频以固定版本为准）。
4. showrunner：建 `work/` 目录，复制 `templates/STATUS.md` 为 `work/STATUS.md`。

**G0 过关**：`check_env.sh` 全部 PASS（含 `DV_CHECK_TTS=1` 的实际合成）；`work/build/EP99/EP99.mp4` 存在，关键帧拼图正常；`decisions.md` 记录了音色、语速、代码基线。

### P1 开工计划（showrunner 自己做）

读完 `docs/` 全部文件后，写 `work/plan.md`（模板 `templates/plan.md`）：

1. 用自己的话写系列核心论点（不超过 200 字）。
2. "一个请求的一生"贯穿案例的具体设定（可以修改 `01_SERIES_BIBLE.md` 的默认设定，但要说理由）。
3. 对 `02_EPISODE_OUTLINE.md` 的调整（合并、拆分、改时长），每条带理由。
4. 你认为最难讲好的三集，以及打算怎么应对。
5. 派发计划：P2 的分组、哪些集做双人核验、试点之后的推进顺序。

**G1 过关**：`plan.md` 写完；**人类检查点 H1** 通过（委托人回复"可以"或给出修改意见）。H1 之前不派发 P2。

### P2 事实包（fact-checker，全部集并行）

每集一个任务（模板 T-FACT），产出：

- `work/facts/EPxx.yaml`：本集事实账本（格式见 `05_FORMATS.md` 第 1 节）
- `work/research/EPxx.md`：研究简报——本集最重要的 3–5 个发现、最反直觉的一点（"aha"候选）、观众最容易误解的地方、可视化素材（时序、数据、结构）、未解决问题
- `work/calc/EPxx_*.py`：所有派生数字的计算脚本（标准库 Python，可直接运行，输出与账本一致）

跨集共用的事实（版本、模型参数、部署规模）放 `work/facts/GLOBAL.yaml`，由 EP00 和 EP03 的任务负责建立，其他任务只引用、不重复建。

★★★ 集（EP03、EP04、EP07、EP12）派两个 fact-checker 独立建账（输出到 `work/facts/_alt/EPxx.yaml`），再派第三个任务（T-FACT-DIFF）对比两份账本，合并成正式版，分歧逐条写进 `work/open_questions.md`。

**G2 过关**：`python tools/lint_facts.py EPxx` 无错误；研究简报写完；`open_questions.md` 中影响本集主线的问题已解决，或已明确标为"无法确认"并写好口径。

### P3 剧集方案（screenwriter）

模板 T-TREAT。输入：系列圣经、本集大纲、事实账本、研究简报、**前面各集已锁定的方案**（保证不重复、不跳步）。输出 `work/treatments/EPxx.md`：

- 一句话梗概、核心问题、看完能说出的三句话
- 本集在"一个请求的一生"中的站点
- 节拍表：每个节拍的时间、要点、用到的事实 ID、画面意图
- 两个冷开场版本（A/B）
- aha 时刻：本集最想让观众"哦——原来如此"的那一下，用什么画面实现
- 前置概念清单：每个概念在第几集讲过；没讲过的必须本集补

showrunner 验收后，派 viewer 盲选冷开场（T-VIEW-HOOK），然后锁定方案。

**G3 过关**：方案通过 `10_REVIEW_CHECKLISTS.md` 的方案清单；前置概念全部有着落；冷开场已选定。

### P4 脚本（screenwriter）

模板 T-SCRIPT。按 `05_FORMATS.md` 第 4 节的格式写 `work/scripts/EPxx.md`。写完自己跑：

```bash
python tools/parse_script.py EPxx && python tools/lint_script.py EPxx
```

**G4 过关**：lint 0 错误；估算时长在目标的 ±15% 以内；警告逐条处理或在 `备注` 里说明保留理由。

### P5 双审（tech-reviewer + viewer，并行）

- tech-reviewer（T-TECH-REVIEW，新会话）：逐镜头核对技术准确性、数字条件、`scope` 标注、事实引用是否真的支撑这句话。
- viewer（T-VIEW，新会话）：只拿到脚本（不给事实账本和大纲），扮演委托人看一遍。列出看不懂的地方、没解释的术语、读完的疑问；用自己的话复述三句话；回答 5 道题（由 showrunner 从方案的"三句话"出题，viewer 看不到答案）。

showrunner 汇总两份记录，写修改指令，派 screenwriter 修改（T-REVISE）。最多 3 轮；3 轮后仍有"错误"级问题，showrunner 把该段降级（删掉或改成"公开资料没有说明"），不得硬留。

**G5 过关**：tech-review 无"错误"级问题；viewer 复述与方案的三句话一致；5 道题答对 ≥ 4 道。

### P6 分镜（storyboarder）

模板 T-BOARD。输入：锁定的脚本、视觉词典、`manim_lib/dvlib.py` 组件清单、本集事实账本中的 `screen` 字段。输出 `work/storyboards/EPxx.md`：每个镜头的版式、元素（只能用视觉词典里的图形和颜色语义）、按 cue 分步的动作、屏幕文字、角标。需要新组件时，写进分镜末尾的"组件需求"，由 animator 实现进 `dvlib.py`。

**G6 过关**：每个镜头都有分镜；每个 `until("cue")` 对应的 cue 在脚本里存在；art-director 对分镜做一次纸面审（T-ART-BOARD），无"必须改"项。

### P7 配音与粗剪（pipeline-engineer，可与 P6 并行）

```bash
python tools/tts.py EPxx
python tools/render.py EPxx --animatic --quality preview
python tools/assemble.py EPxx --quality preview
```

粗剪 = 正式配音 + 占位画面（AutoCard 显示镜头标题和屏幕字）。用它检查节奏和总时长。pipeline-engineer 报告每个镜头实际时长与目标的偏差。

**G7 过关**：总时长在目标 ±15% 以内；偏差超过 30% 的镜头已回到 P4 调整。**试点集 EP07 在这里过人类检查点 H2。**

### P8 动画实现与审片（animator → art-director + tech-reviewer）

1. animator（T-ANIM）：按分镜写 `work/scenes/EPxx.py`，一个镜头一个类。只用 `until()`/`finish()` 对时，不写死秒数。逐镜头渲染预览，修掉所有 `[dvlib] WARN`。
2. pipeline-engineer：`render.py --quality preview` + `assemble.py` + `keyframes.py`。
3. art-director（T-ART-REVIEW）：看 `work/build/EPxx/keyframes/sheet_*.png` 与 `index.md`，按视觉清单审。
4. tech-reviewer（T-TECH-FRAMES）：看同一批关键帧，只查屏幕上的数字、标签、代码路径、角标。
5. animator 修改，最多 3 轮。

**G8 过关**：两份审片记录无"必须改"项；渲染日志无 WARN。

### P9 成片与 QC（pipeline-engineer + screenwriter + showrunner）

1. pipeline-engineer：`make_episode.sh EPxx final`，按 QC 清单测量（分辨率、帧率、时长、响度、字幕轨、章节），复制到 `work/release/`。
2. screenwriter（T-COMPANION）：写《观看手册》。
3. showrunner：看完整集（或关键帧 + 字幕），对照方案的三句话做最终验收，更新看板。

**G9 过关**：QC 清单全过。**试点集 EP07 在这里过人类检查点 H3**；H3 的反馈要回写到规范（风格、节奏、视觉），记进 `decisions.md`，再推进其他集。

### P10 系列统合（showrunner）

- 把每集冷开场和结尾"三句话"按顺序连起来读，检查是不是一条连贯的主线。
- 术语、配色、数字写法全系列一致；"下集预告"与下一集开头对得上。
- 生成系列总图 `series_map.png`（animator 用 dvlib 渲染一张静帧）。
- **人类检查点 H4**：委托人抽看，决定是否做精华版。

## 5. 调度协议（showrunner 必须遵守）

### 5.1 看板

`work/STATUS.md` 是唯一的进度真相。每派发或验收一个任务就更新一次。格式见 `templates/STATUS.md`：每集一行，每个阶段一列，状态取值 `—`（未开始）、`▶`（进行中）、`✓`（过关）、`✗N`（第 N 次打回）、`⏸`（阻塞，附原因）。

### 5.2 派发

每次派发都用 `docs/08_DISPATCH_TEMPLATES.md` 的模板，填齐五项：**任务编号、输入文件路径、输出文件路径、验收标准、报告格式**。只给路径，不把文件内容粘进提示词（子代理自己读）。

### 5.3 推进顺序

1. P0 → P1 → H1。
2. P2：全部 14 集一次性并行派发（★★★ 集各派 2 份 + 1 份对比）。并发上限按你的 OpenCode 配置；建议一次 6–8 个。
3. **试点**：EP07 单独走完 P3–P9，过 H2、H3。试点的目的是校准风格和管线，问题要回写进规范。
4. 试点之后按概念依赖顺序推进：EP00 → EP01 → EP02 → EP03 → EP04 → EP05 → EP06 →（EP07 已完成，只做一致性回修）→ EP08 → EP09 → EP10 → EP11 → EP12 → EP13。
5. 流水线并行：同一时间最多 3 集在 P3–P5（文字阶段），最多 3 集在 P6–P9（制作阶段）。P3 方案必须在前一集方案锁定之后再写，保证"前置概念"有据可查。

### 5.4 验收与打回

- 收到子代理报告后，showrunner 读**输出文件**（不是报告）验收。
- 打回时写清楚：哪个文件、哪个位置、什么问题、改成什么样算过。只说"再改改"不算打回。
- 同一任务第 3 次打回，先停下来判断：是任务描述有问题、输入材料有问题，还是这个点本来就做不到？把判断写进 `decisions.md` 再决定下一步。

### 5.5 冲突处理

| 冲突 | 处理 |
| --- | --- |
| 两份事实账本不一致 | 派 T-FACT-DIFF，要求给出源码原文；源码说了算 |
| 源码与官方文档不一致 | 以源码为准，两者都上屏，并说明"文档口径 vs 代码口径"。这本身是好素材 |
| 技术审校与编剧争执（例如为了好懂而简化） | 允许简化，不允许说错。简化处在屏幕上标"示意"，在旁白里说一句"这里简化了，真实情况是……" |
| 观众审读说看不懂，技术审校说不能改 | 换讲法（比喻、图、例子），不改事实。派 screenwriter 出 2 个讲法，viewer 盲选 |
| 动画实现不了分镜 | animator 在报告里写明原因与替代方案；storyboarder 改分镜 |

### 5.6 上下文管理

- showrunner 不读源码、不读整份研究笔记。需要技术判断时派 fact-checker 写短答（T-FACT-QUERY）。
- showrunner 不写事实账本，也不在 `verified_by` 签名。账本只由 fact-checker 写；补事实也要派 T-FACT 任务（`lint_facts.py` 对其他角色的签名报错）。
- 每集完成后，showrunner 在 `STATUS.md` 的"备注"写一行本集要点，供后面的集回指。系列一致性靠 `STATUS.md`、`decisions.md`、已锁定的方案，而不是靠记忆。

## 6. 人类检查点

| 编号 | 时机 | 给委托人看什么 | 委托人决定什么 |
| --- | --- | --- | --- |
| H1 | P1 之后 | `work/plan.md` | 论点、集数与时长、优先级 |
| H2 | 试点 P7 之后 | `work/build/EP07/EP07.mp4`（粗剪） | 讲法、节奏、音色与语气预设、提问者是否保留；通过后音色和预设锁定 |
| H3 | 试点 P9 之后 | `work/release/EP07.mp4` + 观看手册 | 是否真的看懂了；视觉风格；整体方向 |
| H4 | P10 之后 | 全部成片 | 是否需要精华版、是否返工某集 |

在非交互环境中运行时，showrunner 到达检查点就把要看的材料列在 `work/STATUS.md` 顶部的"等待人类"区，然后停止派发，不要自己代替人类通过。

- 检查点只能由委托人本人通过：`decisions.md` 里记录委托人的原话与时间。showrunner 或任何代理写的"无人值守授权""默认通过""代为确认"一律无效，该检查点之后的产物都只算草稿。
- 委托人事先说"这一轮不用等我"，也只能把检查点**推迟**：继续往下做，但在 `STATUS.md` 把该检查点标 `⏸ 待 H2`，成片文件名加 `_draft`，不得标 `✓`。
- 试点 EP07 第一轮的 H1/H2/H3 都被 showrunner 自批，属于违规；按草稿处理，重新提交。

## 7. 铁律

1. **不编造。** 账本里没有的技术内容，不进成片。查不到就说"公开资料没有说明"。
2. **开源边界不混淆。** 只在文档里描述的组件，每次出现都带"仅文档描述"角标。
3. **数字带条件，不跨条件比较。** 特别是 README 的 Pareto 图：它是"实测步频 × 假设接受率"的换算值，不是端到端实测（见 `07_KNOWLEDGE_BASE.md`）。
4. **不说跑过。** 所有运行行为都来自读代码或官方文档。
5. **不吹不贬。** 每个机制都讲代价；DeepInfer 的局限和长处同样认真讲。
6. **简化要声明。** 示意图里的比例、格数是象征性的，屏幕上标"示意"。
7. **代码上屏要真实。** 摘录必须来自固定 commit，路径行号准确；改写过的伪代码必须标"示意，非原文"。
8. **子代理不越界。** Gemini 代理不生成技术事实；DeepSeek 代理不写旁白。

## 8. 规模估算

| 项 | 估算 |
| --- | --- |
| 总时长 | 约 200 分钟（14 集，大纲合计 199 分钟） |
| 镜头数 | 平均 20 秒一个镜头，约 600 个 |
| 事实条目 | 每集 25–60 条，共约 600 条 |
| 子代理调用 | P2 约 20 次；每集 P3–P9 约 15–25 次；合计约 300 次 |
| 渲染 | preview 每集几分钟；final 1080p 每集约 20–60 分钟 CPU 时间（视动画复杂度） |

## 9. 常见问题处理

| 情况 | 处理 |
| --- | --- |
| 配音请求失败 | `tts.py` 自带重试与分句缓存，重跑即可。401/403 查凭据与白名单出口，429 调小 `--jobs`（见 `09_PRODUCTION_PIPELINE.md` 第 2 节）。qwen 长期不可用时，在 `decisions.md` 记录后改用 `--backend edge` 或 `command`，并整集重配，不混用 |
| 某句语气不对 | 先改写句子；仍不对再给镜头换语气预设（`tone:`）；预设都不合适时由 pipeline-engineer 提议新预设（`03_NARRATION_STYLE.md` 第 12.3 节） |
| 某个术语总是读错 | 加进 `tools/lexicon.yaml`，或在脚本里用 `{写法|读法}` |
| 镜头动画比旁白长 | 渲染日志会有 WARN；优先改动画节奏，其次在旁白里加 `[pause:x]` |
| 某集材料太少 | 与相邻集合并，写进 `decisions.md`；不要注水 |
| 某个机制讲了两遍还是看不懂 | 换"具体数字的例子"而不是换形容词；必要时拆成两个镜头 |
| 发现上一集有错 | 回到那一集的 P4 修，重新走 P5、P7–P9 中受影响的部分，记进 `decisions.md` |
