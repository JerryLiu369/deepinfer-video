# 05 交付物格式

所有中间产物的格式。机器要读的（事实账本、脚本）格式是硬性的，工具会解析；人读的（方案、分镜、审校记录）格式可以略调，但字段要齐。空白模板在 `templates/`。

## 1. 事实账本 `work/facts/EPxx.yaml`

写：fact-checker。读：所有人。校验：`python tools/lint_facts.py EPxx`。

```yaml
episode: EP07
facts:
  - id: F07-03                      # 必填。F<集号>-<序号>；跨集共用的放 GLOBAL.yaml，用 G-<序号>
    claim: >-                       # 必填。一句完整的技术断言，中文，可含代码标识符
      decoder 层 prefill 只对末尾 KEEP_TOKENS 个 query 行做前向；代码断言
      KEEP_TOKENS ≥ window + MAX_BACKTRACKING_TOKENS。
    screen: 保留 ≥ 128 + 6          # 选填。可以直接上屏的短写法（≤ 20 字）
    grade: A                        # 必填。A/B/C/D/E，见 06_FACT_PROTOCOL.md
    status: verified                # 必填。verified / verified_with_caveat / unverifiable / conflict / pending
    evidence:                       # 必填。A 级必须有"路径:行号"；B/C/D 必须有 URL 或文档路径:行号
      - "deepinfer/worker/model_runner.py:107-113"
      - "deepinfer/environ.py:191-194"
    quote: >-                       # 选填但强烈建议。原文摘录 ≤ 5 行（中文注释照抄）
      assert self.window_size + envs.DEEPINFER_MAX_BACKTRACKING_TOKENS <= envs.DEEPINFER_YOCO_PREFILL_KEEP_TOKENS
    commit: 9bd9cf2                 # A 级必填
    kb: [R07#1]                     # 选填。来自哪条知识库笔记
    calc: calc/EP07_rows.py         # 选填。派生数字的计算脚本
    conditions: >-                  # 数字类必填。谁说的/测的、硬件、配置、负载
      代码默认 TRUNCATION_MODE=off；按 README 设 compact + 140 才生效
    caveat: >-                      # 选填。容易说错的地方、口径差异
      134 是存储/命中口径，140 是保留行数，二者是不等式关系
    verified_by: fact-checker@P2    # 选填。谁、在哪个阶段核验
```

`status` 含义：

| 值 | 含义 | 能否上屏 |
| --- | --- | --- |
| `verified` | 已回到一手来源核对 | 能 |
| `verified_with_caveat` | 核对过，但有口径差异或限制，`caveat` 必填 | 能，且旁白要体现 caveat |
| `unverifiable` | 查不到一手证据 | 只能以"公开资料没有说明"的方式出现 |
| `conflict` | 来源互相矛盾，未解决 | 不能 |
| `pending` | 还没核 | 不能 |

## 2. 研究简报 `work/research/EPxx.md`

写：fact-checker。读：screenwriter、showrunner。短句要点，不写成段说明。

```markdown
# EPxx 研究简报
## 0. 元信息
- 代码版本；查阅的来源；本集账本条目数（按等级统计）
## 1. 最重要的 3–5 个发现（每条一句，附事实 ID）
## 2. aha 候选（最反直觉的 1–3 点：为什么反直觉、证据 ID、可以怎么画）
## 3. 观众最容易误解的地方（误解 → 真相 → 事实 ID）
## 4. 与大纲的出入（大纲说法 → 核验结果 → 建议改法）
## 5. 可视化素材（时序步骤、数据表、结构关系，均附事实 ID 或 calc 脚本）
## 6. 未解决问题（问题 → 已查过什么 → 建议口径）
```

## 3. 剧集方案 `work/treatments/EPxx.md`

写：screenwriter。模板：`templates/treatment.md`。必含：

- 一句话梗概；核心问题；看完能说出的三句话
- 站点（小地图高亮哪一站）；三源头（本集机制挂在哪个源头）
- 前置概念表：概念 → 在哪一集讲过 → 本集是否要补
- 冷开场 A / B 两版（各 60–120 字旁白 + 一句画面说明）
- aha 时刻：观众"原来如此"的那一刻，用什么画面实现
- 节拍表：

| # | 时间 | 节拍 | 要点（一句） | 事实 ID | 画面意图 |
| --- | --- | --- | --- | --- | --- |
| 1 | 0:00–0:45 | 冷开场 | …… | F07-01 | …… |

- 暂停题（1–2 个，带答案）
- 下集钩子

## 4. 脚本 `work/scripts/EPxx.md`（机器解析，格式硬性）

写：screenwriter。解析：`tools/parse_script.py`。校验：`tools/lint_script.py`。

### 4.1 结构

```markdown
# EP07 SWA 有界重放：只重算最后一小段
<!-- episode: EP07 | target_min: 18 -->

（这里可以写给人看的说明，不会被解析）

## S01 冷开场：后二十层只算一百四十行
<!-- shot: S01 | target_s: 30 | facts: F07-01, F07-05 | badge: B | scope: mixed | tone: hook -->
**画面**：40 层竖排……（给分镜师的画面意图，1–3 句）
**屏幕字**：
- 后 20 层只算 140 行
**旁白**：
一个四十层的模型，处理一万个 token 的输入。[#rows]
后面二十层，只算了最后 {140|一百四十} 个位置。[pause:0.8]
Q：那答案还对吗？
[#answer]大部分时候是对的。这一集讲它为什么敢这么做。
**备注**：（可选，给审校/分镜的说明，不上屏不配音）
```

### 4.2 字段

| 元素 | 规则 |
| --- | --- |
| `## Sxx 标题` | 镜头号两位或三位数字，集内唯一、递增。标题是给人看的，会出现在章节标记里 |
| `shot:` | 与标题里的 Sxx 一致 |
| `target_s` | 目标时长（秒） |
| `facts` | 逗号分隔的事实 ID；本镜头没有技术断言时写 `-` |
| `badge` | 本镜头引用事实里最弱的等级（A–E）；无事实写 `-` |
| `scope` | `oss`（开源代码里有）/ `doc`（仅文档描述）/ `mixed` / `general`（通用概念） |
| `scene` | 选填。Manim 类名，默认 `EP07_S01`；写 `auto` 则用占位卡 |
| `type` | 选填。`anim`（默认）/ `silent`（无旁白的段落卡） |
| `tone` | 选填。本镜头旁白的配音语气预设：`hook` / `card` / `cost` / `caveat` / `recap`（定义在 `tools/voices.yaml`，规则见 `03_NARRATION_STYLE.md` 第 12 节）。不写用默认语气；`Q：` 行不受影响 |
| `**屏幕字**：` | 每行 `- ` 开头，≤ 20 字，≤ 4 行 |
| `**旁白**：` | 每行一个段落；`Q：` 开头的行由提问者声音读 |

### 4.3 旁白内联标记

| 标记 | 作用 | 例子 |
| --- | --- | --- |
| `[#name]` | 对时点。动画用 `self.until("name")` 等到旁白读到这里 | `[#keep]后面二十层……` |
| `[pause:秒]` | 插入静音 | `[pause:0.8]` |
| `{写法\|读法}` | 字幕显示写法，配音读读法 | `{EP64\|E P 六十四}` |
| `Q：` | 行首，提问者 | `Q：那代价呢？` |

cue 名只能用字母、数字、下划线。cue 放在要对齐的那句话**前面**。

## 5. 分镜 `work/storyboards/EPxx.md`

写：storyboarder。读：animator、art-director。模板：`templates/storyboard.md`。

```markdown
## S03 有界重放的可见域
- 版式：主舞台左 60% 为注意力矩阵（AttentionMatrix 16×16，示意），右 40% 为公式卡
- 元素：
  - AttentionMatrix：行 = query 位置，列 = key 位置；可见格用 SWA 紫，不可见格灰
  - 公式卡：`max(s, i−127) ≤ j ≤ i`，等宽字体
  - 角标：B（自动）；范围：mixed（自动）
- 动作（按 cue）：
  1. 开场：矩阵淡入，显示普通 SWA 的带状可见域（宽 8 格，示意 128）
  2. `until("replay")`：从第 s 行起画一条竖线，竖线左侧的可见格变灰
  3. `until("formula")`：公式卡从右侧滑入，`max(s, ·)` 高亮
- 屏幕字：与脚本一致（不得新增数字）
- 示意声明：右下角"示意：每格代表 16 个 token"
- 复用：与 S02 的矩阵是同一个对象，S03 开头不重新淡入
```

末尾两节：

- **组件需求**：本集需要、`dvlib.py` 里还没有的组件，写清输入参数和外观。
- **全集一致性**：本集新引入的视觉约定（例如"第 20 层用粗边框"），会被后续集复用。

## 6. 动画代码 `work/scenes/EPxx.py`

写：animator。规则见 `09_PRODUCTION_PIPELINE.md` 第 4 节。要点：

- 一个镜头一个类，类名 `EPxx_Syy`，继承 `dvlib.DVScene`，`SHOT = "EPxx-Syy"`。
- 只用 `self.until("cue")` 和 `self.finish()` 控制时长。
- 只用 dvlib 的颜色常量和组件。

## 7. 审校记录 `work/reviews/`

文件名：`EPxx_<类型>_r<轮次>.md`，类型为 `tech`（技术审）、`viewer`（观众审）、`visual`（审片）、`frames`（屏幕技术审）、`board`（分镜纸面审）。

所有审校记录共用一张问题表：

```markdown
| # | 位置（镜头号 + 原句开头 / 关键帧文件名） | 类型 | 问题 | 建议或正确内容（含证据） | 级别 |
| --- | --- | --- | --- | --- | --- |
| 1 | S04 "第 20 层只算……" | 事实错误 | …… | …… F07-09 / 源码路径:行号 | 错误 |
```

级别：`错误`（必须改，否则不过关）/ `不准确`（应改）/ `建议`（可选）。审片类用 `必须改` / `应改` / `建议`。

viewer 记录另含：用自己的话复述三句话；5 道自测题的作答；"最想问的一个问题"。

## 8. 观看手册 `work/release/companion/EPxx.md`

写：screenwriter。模板：`templates/companion.md`。一页纸：

- 三句话
- 一张关键图（关键帧文件名）
- 本集的"为什么"：机制 → 源头 → 代价，一张小表
- 代码阅读入口：3–5 个 `路径:行号`，每个一句"看什么"
- 5 道自测题（答案折叠在文末）
- 本集没讲透、留给以后的问题
