# 项目规则（所有代理共享）

本项目制作一部关于 DeepSeek DeepInfer 推理引擎的中文技术科普视频系列。完整规范在 `docs/`，主控指南是 `docs/00_MASTER_SPEC.md`。

## 所有代理都必须遵守

1. **只写自己的文件。** 每个代理只能写派发任务里指定的输出路径。不修改别的代理的产物；发现别人的问题，写进自己的报告。
2. **技术事实只有一个来源：事实账本 `work/facts/*.yaml`。** 脚本、分镜、动画里出现的数字和技术断言，都必须能对应到账本里 `status: verified` 或 `verified_with_caveat` 的条目。账本里没有的，不许出现在成片里。
3. **区分"代码里有"和"文档里说"。** DeepInfer 开源仓库只是引擎，只做离线推理。KV 存储（3FS）、P/D 分离部署、负载均衡器、Entrypoint、弹性伸缩都**只在文档里描述**，代码里没有实现。每个镜头都要标 `scope`。
4. **不说"我们跑过 DeepInfer"。** 没有人在 SM100 / 昇腾 950 上跑过它。读代码不等于运行。
5. **数字必须带条件**：谁说的/谁测的、什么硬件、什么配置、什么负载。不同条件的数字不能放在一起比。
6. **代码版本固定**：`deepseek-ai/DeepInfer @ 9bd9cf2`（2026-10-21）。基线变更必须先写进 `work/decisions.md`。
7. **知识库优先级**：源码 > 官方文档 > 研究笔记 `R01–R18` > 上一轮书稿。书稿已知有错，不能当证据（见 `docs/07_KNOWLEDGE_BASE.md`）。
8. **凭据不外露。** `.env` 里的配音服务凭据不许打开、打印、复制，不许写进任何文件、报告或日志。
9. **完成任务后的报告**不超过 15 行：写了哪些文件、自查结果、遗留问题。不要把文件内容贴进报告。

## 路径约定

- 规范：`docs/`；模板：`templates/`；工具：`tools/`；动画库：`manim_lib/dvlib.py`
- 知识库：环境变量 `DV_KB`，默认 `../deepinfer-book-spec/work`（`notes/`、`sources/`、`versions.md`）
- 工作区：`work/`（结构见 `docs/09_PRODUCTION_PIPELINE.md` 第 1 节）
- 集号：`EP00`–`EP13`；镜头号：`EP07-S03`；事实号：`F07-03`（跨集共用为 `G-xx`）

## 常用命令

```bash
python tools/parse_script.py EP07          # 脚本 -> work/build/EP07/shots.json
python tools/lint_script.py EP07           # 校验脚本（事实、句长、禁用词、对时 cue）
python tools/lint_facts.py EP07            # 校验事实账本格式与证据
python tools/tts.py EP07                   # 配音 + timing.json（默认 qwen 后端；--backend edge 为免 Key 备选）
python tools/pacing_report.py EP07         # 节奏报告：每镜时长、语速、Q 密度 -> build/EP07/pacing.md
python tools/render.py EP07 --quality preview [--animatic]
python tools/assemble.py EP07 --quality preview
python tools/keyframes.py EP07             # 审片用关键帧与拼图
tools/make_episode.sh EP07 final           # 一条龙
```
