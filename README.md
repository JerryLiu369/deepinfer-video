# 读懂 DeepInfer：跟着一个请求走完 DeepSeek 的推理引擎（视频系列）

[中文](#中文) · [English](#english)

---

## 中文

这是一部关于 [DeepSeek DeepInfer](https://github.com/deepseek-ai/DeepInfer) 推理引擎的中文技术科普视频系列，同时也是它完整的制作工程：规范、事实账本、脚本、分镜、Manim 动画代码、配音与合成工具、每一轮审校记录，都在这个仓库里。

系列计划 14 集（EP00–EP13），沿着"一个请求的一生"讲清 DeepInfer 的架构本质，以及每个设计**为什么这样做、付出了什么代价**。配套的书见 [deepinfer-book](https://github.com/JerryLiu369/deepinfer-book)，本仓库把它的 `research/` 当作知识库。

### 制作进度

| 状态 | 集 |
| --- | --- |
| 已完成并入库字幕与观看手册 | EP00 全景导览、EP01 通用基座、EP02 定位全景、EP03 模型结构、EP04 代码地图、EP07 SWA 有界重放（试点标杆集） |
| 进行中 | EP05 调度（脚本、分镜、动画代码与审校已在，成片未验收） |
| 未开始 | EP06、EP08–EP13 |

逐集的阶段状态以 [`work/STATUS.md`](work/STATUS.md) 为准。成片 `.mp4` 体积大，不入库（见 `.gitignore`），只保留字幕和观看手册，见 [`work/release/`](work/release/)。

### 这个项目怎么做出来的

两个模型在 [OpenCode](https://opencode.ai) 里分工协作，由人在 4 个检查点把关：

| | Gemini | DeepSeek |
| --- | --- | --- |
| 负责 | **怎么讲**：统筹、叙事、脚本、分镜、视听审片、观众视角 | **真不真、能不能跑**：事实核验、读码、数值计算、动画代码、管线工程、技术审校 |
| 代理 | showrunner、screenwriter、storyboarder、viewer、art-director | fact-checker、tech-reviewer、animator、pipeline-engineer |

两边之间唯一的技术信息通道是**事实账本**（`work/facts/*.yaml`）。脚本里每个数字和技术断言都要挂一个事实 ID，`tools/lint_script.py` 逐条检查。账本里没有的，不许出现在成片里。

几条需要观众和读者知道的前提：

- **读码，不是实测。** 内容来自对固定版本源码和公开资料的阅读，没有人在文中提到的硬件上运行过 DeepInfer。
- **代码版本固定**为 `deepseek-ai/DeepInfer @ 9bd9cf2`（2026-10-21）。
- **"代码里有"和"文档里说"分开标注。** KV 存储、P/D 分离部署、负载均衡等只在官方文档里描述，开源代码里没有实现，每个镜头都标 `scope`。
- **内容由 AI 生成。** 事实经过账本与双审机制核验，但仍可能有错。发现问题欢迎提 issue。

### 仓库结构

```
deepinfer-video/
├── docs/            # 规范 00–11：总控指南、系列圣经、集大纲、旁白与视觉规范、格式、事实协议、管线、验收清单
├── .opencode/       # OpenCode 的 9 个代理定义与 5 个命令（/kickoff /facts /episode /review /status）
├── opencode.json    # OpenCode 项目配置
├── AGENTS.md        # 所有代理共享的项目规则
├── templates/       # 各类交付物的空白模板
├── tools/           # 管线脚本：解析、校验、配音、渲染、合成、关键帧
├── manim_lib/       # 视觉词典的代码实现（dvlib.py）
├── examples/        # smoke（冒烟测试）与 ep07_sample（风格样板）
└── work/            # 工作区：全部制作产物，按下表组织
```

`work/` 里每一步的产物都能追溯到上一步：

| 目录 | 内容 | 阶段 |
| --- | --- | --- |
| `STATUS.md` `plan.md` `decisions.md` `open_questions.md` `glossary.md` | 看板、开工计划、决策记录、未决问题、术语 | 全程 |
| `facts/` `calc/` `research/` | 事实账本、计算脚本、研究简报 | P2 |
| `treatments/` | 剧集方案 | P3 |
| `scripts/` | 旁白脚本（机器可解析） | P4 |
| `storyboards/` | 分镜 | P6 |
| `scenes/` | Manim 动画代码 | P8 |
| `reviews/` | 全部审校与 QC 记录 | P5–P9 |
| `release/` | 字幕 `.srt` 和每集《观看手册》 | P9 |

从哪里开始读：

- **想看成片的制作逻辑**：[`docs/00_MASTER_SPEC.md`](docs/00_MASTER_SPEC.md)，然后看 `work/decisions.md`。
- **想看一集是怎么走完全流程的**：EP07，对应 [`docs/11_SAMPLE_EP07.md`](docs/11_SAMPLE_EP07.md) 以及 `work/` 下各目录里的 `EP07.*`。
- **想核对某个数字**：在 `work/facts/EPxx.yaml` 找事实 ID，里面有出处、证据等级和对应的 `work/calc/` 脚本。

### 复现

1. **准备知识库。** 与本仓库同级克隆 [deepinfer-book](https://github.com/JerryLiu369/deepinfer-book)，并还原上游源码：

   ```bash
   git clone https://github.com/JerryLiu369/deepinfer-book ../deepinfer-book
   bash ../deepinfer-book/scripts/fetch_sources.sh
   ```

   知识库默认路径是 `../deepinfer-book/research`，放在别处时设置环境变量 `DV_KB`。

2. **装环境。** Python 3.10+（3.12 已测）、ffmpeg（含 libx264）、Noto Sans CJK SC 字体。Linux 上 manimpango 需要先装 `libpango1.0-dev libcairo2-dev pkg-config`：

   ```bash
   python3 -m venv .venv && . .venv/bin/activate
   pip install -r tools/requirements.txt
   cp .env.example .env              # 填入配音服务凭据，见下
   DV_CHECK_TTS=1 tools/check_env.sh # 全部 PASS 再往下走
   ```

3. **跑冒烟测试**（约 1–2 分钟，需要联网调用配音服务）：

   ```bash
   cp -r examples/smoke /tmp/smoke && DV_WORK=/tmp/smoke tools/make_episode.sh EP99 draft
   ```

4. **配置模型。** `.opencode/agent/` 里的模型 ID 是作者所用服务商的写法（Gemini 类为 `axon-responses/gemini-3.8-flash`，DeepSeek 类为 `axon-completions/deepseek-flash`）。运行 `opencode models` 查看自己的 ID，再整体替换；`opencode.json` 里的默认模型同理。

5. **开工。** 在仓库根目录启动 `opencode`，切到 `showrunner`，输入 `/kickoff`。

常用命令（完整列表见 [`AGENTS.md`](AGENTS.md)）：

```bash
python tools/lint_facts.py EP07 --kb "$DV_KB"   # 校验事实账本
python tools/lint_script.py EP07                # 校验脚本
tools/make_episode.sh EP07 final                # 配音、渲染、合成一条龙
```

### 配音

正式配音用阿里云百炼的 Qwen-Audio-3.1-TTS-Plus，两个音色：解说 `longanhuan_v3.1`，提问者 `longanlingxin_v3.1`。凭据放在 `.env`（模板 `.env.example`，不入库）。没有 Key 时可用 `python tools/tts.py EPxx --backend edge` 免 Key 试听。选型与排错见 [`docs/09_PRODUCTION_PIPELINE.md`](docs/09_PRODUCTION_PIPELINE.md)。

### 许可证

[MIT](LICENSE)。

---

## English

A Chinese-language technical video series on the [DeepSeek DeepInfer](https://github.com/deepseek-ai/DeepInfer) inference engine, published together with its complete production project: specs, fact ledgers, scripts, storyboards, Manim animation code, TTS and assembly tooling, and every round of review records.

The plan is 14 episodes (EP00–EP13) that follow one request through the engine and explain **why each design choice was made and what it costs**. The companion book is [deepinfer-book](https://github.com/JerryLiu369/deepinfer-book); this repository uses its `research/` directory as the knowledge base.

### Progress

| State | Episodes |
| --- | --- |
| Done (subtitles and viewing guide committed) | EP00, EP01, EP02, EP03, EP04, EP07 (pilot) |
| In progress | EP05 (script, storyboard, animation code and reviews exist; final cut not accepted) |
| Not started | EP06, EP08–EP13 |

Per-episode stage status lives in [`work/STATUS.md`](work/STATUS.md). Rendered `.mp4` files are not tracked; only subtitles and viewing guides are in [`work/release/`](work/release/).

### How it is made

Two models collaborate in [OpenCode](https://opencode.ai), with four human checkpoints. Gemini-class agents own *how to tell it* (showrunner, screenwriter, storyboarder, viewer, art-director). DeepSeek-class agents own *whether it is true and whether it runs* (fact-checker, tech-reviewer, animator, pipeline-engineer). The only technical channel between them is the fact ledger (`work/facts/*.yaml`): every number and technical claim in a script must cite a ledger entry, and `tools/lint_script.py` enforces it.

Caveats:

- **Code reading, not benchmarking.** Nobody ran DeepInfer on the hardware discussed.
- **Pinned code version:** `deepseek-ai/DeepInfer @ 9bd9cf2` (2026-10-21).
- **Code vs. documentation is labeled.** KV storage, P/D disaggregation and load balancing are described only in the official docs, not implemented in the open-source code.
- **AI-generated content.** Facts are verified through the ledger and review process, but errors are possible. Issues are welcome.

### Layout

| Path | Contents |
| --- | --- |
| `docs/` | Specs 00–11: master guide, series bible, episode outline, narration and visual style, formats, fact protocol, pipeline, checklists |
| `.opencode/`, `opencode.json`, `AGENTS.md` | Agent definitions, commands, shared rules |
| `templates/` | Blank templates for every deliverable |
| `tools/` | Pipeline scripts: parse, lint, TTS, render, assemble, keyframes |
| `manim_lib/` | Code implementation of the visual vocabulary |
| `examples/` | `smoke` (smoke test) and `ep07_sample` (style sample) |
| `work/` | All production artifacts: facts, calc, research, treatments, scripts, storyboards, scenes, reviews, release |

### Reproduce

```bash
git clone https://github.com/JerryLiu369/deepinfer-book ../deepinfer-book
bash ../deepinfer-book/scripts/fetch_sources.sh      # upstream sources at pinned commits
python3 -m venv .venv && . .venv/bin/activate
pip install -r tools/requirements.txt
cp .env.example .env                                 # DashScope credentials for TTS
DV_CHECK_TTS=1 tools/check_env.sh                    # environment check
cp -r examples/smoke /tmp/smoke && DV_WORK=/tmp/smoke tools/make_episode.sh EP99 draft
```

The knowledge base defaults to `../deepinfer-book/research`; override with `DV_KB`. Model IDs in `.opencode/agent/` use the author's provider naming; replace them with the IDs from `opencode models`. Then run `opencode`, switch to `showrunner`, and enter `/kickoff`.

### License

[MIT](LICENSE).
