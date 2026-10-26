# 08 派发模板

showrunner 每次派发子任务，都从这里复制对应模板，填好 `<尖括号>`，作为 task 的提示词发给对应代理。代理的角色规则已经写在 `.opencode/agent/<代理>.md` 里，模板只写**这一次的任务**。

## 0. 通用骨架

每个模板都是这五段。不要省略任何一段。

```text
【任务】<编号，如 EP07/P4/T-SCRIPT/r1> —— <一句话说要干什么>
【输入】（自己去读，不要等我粘贴）
- <路径 1>：<为什么要读>
- ...
【输出】
- <路径>：<格式要求，引用 docs/05_FORMATS.md 的第几节>
【验收】
- <可检查的条件 1>
- ...
【报告】完成后回复不超过 15 行：写了哪些文件；验收条件逐条自查结果；遗留问题。不要贴文件内容。
```

---

## T-ENV 环境与冒烟测试 → pipeline-engineer

```text
【任务】P0/T-ENV —— 装好制作环境，跑通 EP99 冒烟测试（qwen 配音后端），校准配音
【输入】
- README.md 第"快速开始"节；docs/09_PRODUCTION_PIPELINE.md（第 3.4 节配音）；docs/03_NARRATION_STYLE.md 第 12 节
- .env（只确认存在，不要打开、不要打印内容）；tools/voices.yaml
- examples/smoke/
【输出】
- work/build/EP99/EP99.mp4、EP99.srt、keyframes/sheet_01.png（把 examples/smoke 的 scripts/ facts/ scenes/ 复制进 work/ 后构建）
- work/decisions.md 追加"P0 管线"一节：Python/manim/ffmpeg 版本、配音后端与模型、音色（应为 longanhuan_v3.1 / longanlingxin_v3.1）、实测语速、lexicon 改动、需要委托人试听的句子
【验收】
- DV_CHECK_TTS=1 tools/check_env.sh 全部 PASS（qwen 实际合成成功）
- make_episode.sh EP99 draft 退出码 0；渲染日志无 [dvlib] WARN
- timing.json 的 backend 为 qwen
- 实测语速与 tools/voices.yaml 中 qwen 的 cps 差距 < 10%（否则改 cps 并说明）
【报告】……
```

## T-FACT 事实包 → fact-checker

```text
【任务】<EPxx>/P2/T-FACT —— 为 <EPxx 标题> 建立事实账本、计算脚本和研究简报
【输入】
- docs/02_EPISODE_OUTLINE.md 中 <EPxx> 一节（必须讲、aha 候选、素材）
- docs/06_FACT_PROTOCOL.md（核验流程，严格执行）
- docs/07_KNOWLEDGE_BASE.md（笔记索引、书稿已知错误、易错陷阱）
- $DV_KB/notes/<R..>.md（只当线索）
- $DV_KB/sources/DeepInfer @ 9bd9cf2（A 级证据唯一来源）
- work/facts/GLOBAL.yaml（已有的跨集事实，只引用不重复建）
【输出】
- work/facts/<EPxx>.yaml（docs/05_FORMATS.md 第 1 节）
- work/calc/<EPxx>_*.py（所有派生数字）
- work/research/<EPxx>.md（docs/05_FORMATS.md 第 2 节）
【验收】
- python tools/lint_facts.py <EPxx> --kb $DV_KB 无 ERROR
- 大纲"必须讲"的每一项都有对应事实，或在研究简报第 4/6 节说明为什么没有
- 每个 aha 候选都有 A/B 级支撑，或已降级并说明
- 所有 calc 脚本可直接运行，输出与账本一致
- 易错陷阱清单中与本集相关的条目，都在 caveat 里体现
【报告】……另报：事实总数与等级分布；与大纲出入最大的一点
```

★★★ 集双人核验时，把输出路径改成 `work/facts/_alt/<EPxx>_a.yaml`（另一个是 `_b`），研究简报改成 `work/research/_alt/<EPxx>_a.md`，并加一句"不要读 _alt/ 下另一份文件"。

## T-FACT-DIFF 账本对比合并 → fact-checker

```text
【任务】<EPxx>/P2/T-FACT-DIFF —— 对比两份独立账本，合并成正式版
【输入】work/facts/_alt/<EPxx>_a.yaml、_b.yaml；work/research/_alt/<EPxx>_a.md、_b.md；$DV_KB/sources/DeepInfer
【输出】
- work/facts/<EPxx>.yaml（合并版，ID 重新编号连续）
- work/research/<EPxx>.md（合并版，末尾加"分歧记录"表：条目 | a 说 | b 说 | 源码定案 | 结论）
- 未定案的分歧追加到 work/open_questions.md
【验收】每个分歧都有源码原文或文档原文定案，或明确标 conflict；lint_facts 无 ERROR
【报告】……另报：分歧总数、定案数、遗留数
```

## T-FACT-QUERY 技术短问 → fact-checker

showrunner 遇到技术判断时用，不要自己去读源码。

```text
【任务】<编号>/T-FACT-QUERY —— 回答一个技术问题
【问题】<一句话>
【背景】<为什么要问，涉及哪集哪个镜头>
【输出】work/research/queries/<编号>.md：结论一句话 + 证据（路径:行号 + 摘录）+ 等级 + 是否需要新增/修改账本条目（给出 YAML）
【验收】结论有 A/B 级证据，或明确写"无法确认"及查过的地方
【报告】结论一句话 + 文件路径
```

## T-TREAT 剧集方案 → screenwriter

```text
【任务】<EPxx>/P3/T-TREAT —— 写 <EPxx> 的剧集方案
【输入】
- docs/01_SERIES_BIBLE.md、docs/02_EPISODE_OUTLINE.md（<EPxx> 一节）、docs/03_NARRATION_STYLE.md
- work/facts/<EPxx>.yaml、work/facts/GLOBAL.yaml、work/research/<EPxx>.md
- 已锁定的前序方案：work/treatments/<列出>.md（检查前置概念）
- work/glossary.md（如已有）
- 样板：docs/11_SAMPLE_EP07.md
【输出】work/treatments/<EPxx>.md（templates/treatment.md）
【验收】
- 三句话与大纲一致，或在方案开头写明改动理由
- 节拍表每一拍都标了事实 ID；没有任何不在账本里的技术内容
- 前置概念表完整；没讲过的概念本集有补
- 冷开场 A/B 两版，风格明显不同
- 节拍总时长在目标 ±10%
【报告】……
```

## T-VIEW-HOOK 冷开场盲选 → viewer

```text
【任务】<EPxx>/P3/T-VIEW-HOOK —— 从两个冷开场里选一个
【输入】只读 work/treatments/<EPxx>.md 中"冷开场 A""冷开场 B"两段（不要读其他部分）
【输出】work/reviews/<EPxx>_hook.md：选哪个；为什么（一句话）；另一个的问题；你看完开场最想知道的问题
【验收】给出选择与理由
【报告】选择 + 一句理由
```

## T-SCRIPT 脚本 → screenwriter

```text
【任务】<EPxx>/P4/T-SCRIPT —— 按锁定的方案写脚本
【输入】
- work/treatments/<EPxx>.md（已锁定，冷开场选 <A/B>）
- work/facts/<EPxx>.yaml、GLOBAL.yaml
- docs/03_NARRATION_STYLE.md、docs/05_FORMATS.md 第 4 节
- examples/ep07_sample/scripts/EP07.md（格式与文风样板）
- tools/lexicon.yaml（已有读音）
【输出】work/scripts/<EPxx>.md
【验收】
- python tools/parse_script.py <EPxx> && python tools/lint_script.py <EPxx>：0 ERROR
- 估算总时长在目标 ±15%
- 每个镜头的第一句是要点；每 3–4 个镜头最多一个 Q
- 节拍表的每一拍都落在了具体镜头里
- 剩余 WARN 逐条在 **备注** 里说明保留理由
【报告】……另报：镜头数、估算时长、lint 剩余警告数
```

## T-TECH-REVIEW 技术审校 → tech-reviewer（新会话）

```text
【任务】<EPxx>/P5/T-TECH-REVIEW/r<N> —— 逐镜头核对脚本的技术准确性
【输入】
- work/scripts/<EPxx>.md
- work/facts/<EPxx>.yaml、GLOBAL.yaml；work/calc/<EPxx>_*.py（重跑）
- docs/06_FACT_PROTOCOL.md 第 5 节；docs/07_KNOWLEDGE_BASE.md 第 3–4 节
- $DV_KB/sources/DeepInfer（需要时回源码）
- 上一轮记录（如有）：work/reviews/<EPxx>_tech_r<N-1>.md
【输出】work/reviews/<EPxx>_tech_r<N>.md（docs/05_FORMATS.md 第 7 节问题表）
【验收】每个镜头都看过；每个"错误"都给出正确内容与证据；最后三句话总结最需要改的地方
【报告】错误/不准确/建议各几条
```

## T-VIEW 观众审读 → viewer（新会话）

```text
【任务】<EPxx>/P5/T-VIEW/r<N> —— 以委托人的身份读脚本
【输入】只读 work/scripts/<EPxx>.md 的 **旁白** 与 **屏幕字**（不要读事实账本、大纲、方案、备注）
【题目】
1. <showrunner 出题>
2. ...
5. ...
【输出】work/reviews/<EPxx>_viewer_r<N>.md：
- 看不懂的地方（镜头号 + 原句 + 卡在哪）
- 第一次出现却没解释的术语
- 看完的疑问（"那为什么不……？"）
- 觉得多余的镜头
- 用自己的话复述三句话
- 5 道题的作答
- 最想问的一个问题
【验收】各项都有内容（"没有"也要写"没有"）
【报告】看不懂的地方几处；复述的三句话
```

出题规则：showrunner 根据方案里的"三句话"和"暂停题"出 5 道题，至少 2 道是"为什么"题，至少 1 道是"代价是什么"题。答案只写在 showrunner 自己的验收记录里。

## T-REVISE 修改 → screenwriter

```text
【任务】<EPxx>/P5/T-REVISE/r<N> —— 按审校意见修改脚本
【输入】work/scripts/<EPxx>.md；work/reviews/<EPxx>_tech_r<N>.md、<EPxx>_viewer_r<N>.md；showrunner 修改指令（见下）
【修改指令】
- <逐条：镜头号 → 改什么 → 改成什么样算过>
【输出】覆盖 work/scripts/<EPxx>.md；在文件末尾"修订记录"追加本轮改动摘要
【验收】指令逐条落实；lint 0 ERROR；未采纳的意见写明理由
【报告】……
```

## T-BOARD 分镜 → storyboarder

```text
【任务】<EPxx>/P6/T-BOARD —— 为锁定的脚本写分镜
【输入】
- work/scripts/<EPxx>.md（已锁定）；work/build/<EPxx>/shots.json（解析结果，含 cue 列表）
- docs/04_VISUAL_LANGUAGE.md；manim_lib/dvlib.py（只看组件名和参数）
- work/facts/<EPxx>.yaml 的 screen 字段
- 前序集分镜的"全集一致性"节：work/storyboards/<列出>.md
- 样板：examples/ep07_sample/storyboards/EP07.md
【输出】work/storyboards/<EPxx>.md（docs/05_FORMATS.md 第 5 节）
【验收】
- 每个镜头都有分镜；所有 until 的 cue 都在 shots.json 里
- 只用视觉词典的颜色语义与图形；新组件写进"组件需求"
- 不新增脚本里没有的数字或技术内容
- 示意图都有示意声明
【报告】……另报：新组件需求几个
```

## T-ART-BOARD 分镜纸面审 → art-director

```text
【任务】<EPxx>/P6/T-ART-BOARD —— 审分镜（还没有画面）
【输入】work/storyboards/<EPxx>.md；docs/04_VISUAL_LANGUAGE.md；前序集分镜的一致性节
【输出】work/reviews/<EPxx>_board.md（问题表，级别 必须改/应改/建议）
【验收】每个镜头都看过；重点查信息密度、颜色语义、跨集一致性、是否剧透
【报告】必须改/应改/建议各几条
```

## T-VOICE 配音与粗剪 → pipeline-engineer

```text
【任务】<EPxx>/P7/T-VOICE —— 配音并生成占位粗剪
【输入】work/scripts/<EPxx>.md（已锁定）
【输出】work/build/<EPxx>/timing.json、audio/、<EPxx>.mp4（animatic，preview 质量）
【命令】parse_script → tts → render --animatic --quality preview → assemble --quality preview
【验收】总时长在目标 ±15%；列出实际时长偏离 target_s 超过 30% 的镜头；列出 lint INFO 中可能读错的词
【报告】总时长；偏离镜头列表；疑似读错词列表
```

## T-ANIM 动画实现 → animator

```text
【任务】<EPxx>/P8/T-ANIM/r<N> —— 按分镜实现全部镜头
【输入】
- work/storyboards/<EPxx>.md；work/build/<EPxx>/shots.json、timing.json
- manim_lib/dvlib.py；docs/04_VISUAL_LANGUAGE.md；docs/09_PRODUCTION_PIPELINE.md 第 4 节
- examples/smoke/scenes/EP99.py（写法样板）
- 上一轮审片记录（如有）：work/reviews/<EPxx>_visual_r<N-1>.md、<EPxx>_frames_r<N-1>.md
【输出】
- work/scenes/<EPxx>.py
- 分镜"组件需求"里的新组件：实现进 manim_lib/dvlib.py，并在 docs/04_VISUAL_LANGUAGE.md 第 4 节登记
【验收】
- python tools/render.py <EPxx> --quality preview 全部 OK，日志无 [dvlib] WARN
- 每个类只用 until/finish 控制时长；没有写死的长 wait
- python tools/lint_script.py <EPxx> 无"scene waits for cues not in narration"错误
- 屏幕上的数字与 facts 的 screen 字段一致
【报告】……另报：新增组件；与分镜不一致的地方及原因
```

## T-ART-REVIEW 审片 → art-director

```text
【任务】<EPxx>/P8/T-ART-REVIEW/r<N> —— 审关键帧
【输入】work/build/<EPxx>/keyframes/sheet_*.png 与 index.md；单帧图按需打开；work/storyboards/<EPxx>.md；docs/04_VISUAL_LANGUAGE.md 第 7 节
【输出】work/reviews/<EPxx>_visual_r<N>.md（问题表，位置写关键帧文件名）
【验收】每张拼图都看过；每条"必须改"写清改成什么样
【报告】必须改/应改/建议各几条
```

## T-TECH-FRAMES 屏幕技术审 → tech-reviewer

```text
【任务】<EPxx>/P8/T-TECH-FRAMES/r<N> —— 核对画面上的技术内容
【输入】work/build/<EPxx>/keyframes/；work/facts/<EPxx>.yaml；work/calc/
【输出】work/reviews/<EPxx>_frames_r<N>.md
【验收】屏幕上每个数字、标签、代码路径与行号、角标颜色都核对过
【报告】错误几条
```

## T-BUILD 成片与 QC → pipeline-engineer

```text
【任务】<EPxx>/P9/T-BUILD —— 出 1080p 成片并做 QC
【命令】tools/make_episode.sh <EPxx> final
【输出】work/release/<EPxx>.mp4、<EPxx>.srt；work/reviews/<EPxx>_qc.md（docs/10_REVIEW_CHECKLISTS.md 的 QC 清单逐项结果，附 ffprobe 与 loudnorm 测量值）
【验收】QC 清单全部通过
【报告】……
```

## T-COMPANION 观看手册 → screenwriter

```text
【任务】<EPxx>/P9/T-COMPANION —— 写观看手册
【输入】work/scripts/<EPxx>.md；work/treatments/<EPxx>.md；work/facts/<EPxx>.yaml；work/build/<EPxx>/keyframes/index.md
【输出】work/release/companion/<EPxx>.md（templates/companion.md）
【验收】一页内；代码入口路径行号来自账本；自测题有答案，答案能在本集找到出处（镜头号）
【报告】……
```
