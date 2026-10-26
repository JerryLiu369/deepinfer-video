# DeepInfer 技术视频 · 协作 Spec

这是一套让两个模型在 OpenCode 里协作、做出一部 DeepInfer 技术科普视频系列的完整工作规范。它既是给人看的项目说明书，也是一个可以直接打开的 OpenCode 项目：主代理（showrunner）读完这里的文件，就能自己派发子代理、推进流水线。

- 片名（暂定）：《读懂 DeepInfer：跟着一个请求走完 DeepSeek 的推理引擎》
- 形态：14 集系列（EP00–EP13），每集 5–18 分钟，合计约 3 小时 20 分钟（大纲合计 199 分钟）；中文配音 + 字幕 + 章节标记；每集附一页《观看手册》
- 观众：委托人本人。懂软件工程和 Transformer/MoE 基础，没读过推理引擎源码
- 目标：看完能用自己的话讲清 DeepInfer 的架构本质、核心机制，以及每个设计**为什么**这样做、付出了什么代价

## 两个模型怎么分工（一句话版）

| | Gemini 3.8 Flash | DeepSeek V4.1 Flash |
| --- | --- | --- |
| 管什么 | **怎么讲**：统筹、叙事、脚本、分镜、视听审片、观众视角 | **真不真、能不能跑**：事实核验、读码、数值计算、动画代码、管线工程、技术审校 |
| 代理 | showrunner（主代理）、screenwriter、storyboarder、viewer、art-director | fact-checker、tech-reviewer、animator、pipeline-engineer |
| 不做什么 | 不自己发明技术事实；只能引用事实账本里的条目 | 不写旁白文案；不改叙事结构 |

两边唯一的技术信息通道是**事实账本**（`work/facts/*.yaml`）。脚本里每个数字、每个技术断言都要挂一个事实 ID，`tools/lint_script.py` 会逐条检查。

## 阅读顺序

| 顺序 | 文件 | 内容 | 主要读者 |
| --- | --- | --- | --- |
| 1 | `docs/00_MASTER_SPEC.md` | **主控调度指南**：目标、分工、P0–P10 流程与关卡、调度协议、人类检查点、铁律 | 人类 + showrunner |
| 2 | `docs/01_SERIES_BIBLE.md` | 系列圣经：核心论点、三条主线、贯穿案例"一个请求的一生"、每集固定结构、术语 | 全部 Gemini 代理 |
| 3 | `docs/02_EPISODE_OUTLINE.md` | 14 集逐集大纲：核心问题、看完能说出、必须讲、反直觉点、素材来源 | showrunner、screenwriter、fact-checker |
| 4 | `docs/03_NARRATION_STYLE.md` | 旁白写作规范：口语化、句长、数字口播、证据措辞、正反例 | screenwriter、viewer |
| 5 | `docs/04_VISUAL_LANGUAGE.md` | 视觉词典：配色语义、版式、固定图形、证据角标、动效节奏 | storyboarder、animator、art-director |
| 6 | `docs/05_FORMATS.md` | 所有交付物格式：事实账本、研究简报、剧集方案、脚本、分镜、审校记录 | 全部代理 |
| 7 | `docs/06_FACT_PROTOCOL.md` | 证据等级、核验流程、计算脚本规范 | fact-checker、tech-reviewer、showrunner |
| 8 | `docs/07_KNOWLEDGE_BASE.md` | 已有知识库（上一轮写书留下的 18 份研究笔记与源码）怎么用、哪些地方已知有错、易错陷阱 | fact-checker、tech-reviewer、showrunner |
| 9 | `docs/08_DISPATCH_TEMPLATES.md` | 每类子任务的派发模板（showrunner 原样填写） | showrunner |
| 10 | `docs/09_PRODUCTION_PIPELINE.md` | 制作管线：目录、命令、配音对时、渲染、合成、排错 | pipeline-engineer、animator |
| 11 | `docs/10_REVIEW_CHECKLISTS.md` | 每道关卡的验收清单 | 全部 |
| 12 | `docs/11_SAMPLE_EP07.md` + `examples/ep07_sample/` | 样板：EP07（SWA 有界重放）的方案、脚本片段、分镜、事实条目 | screenwriter、storyboarder（校准风格用） |

## 文件夹结构

```
deepinfer-video-spec/
├── README.md                 # 本文件
├── AGENTS.md                 # OpenCode 自动加载的项目规则（所有代理共享）
├── opencode.json             # OpenCode 项目配置
├── .env.example              # 配音服务凭据模板（复制为 .env，.env 不随包分发）
├── .opencode/
│   ├── agent/                # 9 个代理定义（模型、温度、权限、角色提示词）
│   └── command/              # 自定义命令：/kickoff /facts /episode /review /status
├── docs/                     # 00–11 规范文档
├── templates/                # 各类交付物的空白模板 + STATUS 看板
├── tools/                    # 已实测可用的管线脚本（解析/校验/配音/渲染/合成/关键帧）；voices.yaml 音色与语气预设
├── manim_lib/                # 视觉词典的代码实现 dvlib.py + 占位镜头 autocard.py
└── examples/
    ├── smoke/                # EP99 冒烟测试：3 个镜头跑通全流程（P0 关卡用）
    └── ep07_sample/          # EP07 样板：方案、脚本片段、分镜、事实条目
```

运行时会在根目录生成 `work/`（全部工作产物）。`work/` 的结构见 `docs/09_PRODUCTION_PIPELINE.md`。

## 快速开始

1. **准备知识库。** 本 Spec 复用上一轮写书项目留下的研究成果（`deepinfer-book-spec/work/`：18 份研究笔记、四个仓库的源码克隆、版本记录）。默认路径是本文件夹的同级目录 `../deepinfer-book-spec/work`，换位置就设置环境变量 `DV_KB`。
2. **装环境。** Python 3.10+（3.12 已测）、ffmpeg（含 libx264）、Noto Sans CJK SC 字体。Linux 上 manimpango 需要从源码编译，先装 `libpango1.0-dev libcairo2-dev pkg-config`。然后：
   ```bash
   python3 -m venv .venv && . .venv/bin/activate
   pip install -r tools/requirements.txt
   cp .env.example .env          # 填入阿里云百炼凭据（见下面"配音"）
   DV_CHECK_TTS=1 tools/check_env.sh   # 全部 PASS 才往下走；会实际合成一句话
   ```
   如果 shell 里设置了别的 `PYTHONPATH`，先 `unset PYTHONPATH`，否则可能混入别的环境的包。
3. **跑冒烟测试**（约 1–2 分钟，需要联网调用配音服务）：
   ```bash
   cp -r examples/smoke /tmp/smoke && DV_WORK=/tmp/smoke tools/make_episode.sh EP99 draft
   # 产物：/tmp/smoke/build/EP99/EP99.mp4、EP99.srt、keyframes/sheet_01.png
   ```
4. **配置模型。** 运行 `opencode models` 查看你的 provider 给这两个模型的实际 ID，然后替换代理文件里的占位符：
   ```bash
   grep -rl 'google/gemini-3.8-flash' .opencode opencode.json | xargs sed -i 's#google/gemini-3.8-flash#<你的 Gemini ID>#g'
   grep -rl 'deepseek/deepseek-v4.1-flash' .opencode | xargs sed -i 's#deepseek/deepseek-v4.1-flash#<你的 DeepSeek ID>#g'
   ```
5. **开工。** 在本目录启动 `opencode`，用 Tab 切到 `showrunner` 代理，输入 `/kickoff`。主代理会读完全部规范，写出 `work/plan.md`，然后停下来等你确认（人类检查点 H1）。

## 配音

正式配音用阿里云百炼的 **Qwen-Audio-3.1-TTS-Plus**（`tools/tts.py` 的默认后端 `qwen`）。选型理由、配置项、排错见 `docs/09_PRODUCTION_PIPELINE.md` 第 3.4 节，语气规则见 `docs/03_NARRATION_STYLE.md` 第 12 节。

| 角色 | 音色 | 默认语气 |
| --- | --- | --- |
| 解说 | `longanhuan_v3.1` | 沉稳、清晰、富有逻辑的科技讲解口吻 |
| 提问者（脚本里 `Q：` 开头） | `longanlingxin_v3.1` | 好奇、探究、求真的提问口吻 |

- **凭据**：`.env`（模板 `.env.example`）里放 `DASHSCOPE_API_KEY`、工作空间专属端点 `DASHSCOPE_ENDPOINT`、`DASHSCOPE_MODEL`。出口必须走白名单代理时再设 `DASHSCOPE_PROXY`（例如 `http://127.0.0.1:7890`），不设就直连；默认只走 IPv4。`.env` 不进版本库、不进压缩包。
- **音色与语气预设**：`tools/voices.yaml`。脚本里用镜头元数据 `tone: hook|card|cost|caveat|recap` 切换旁白语气，不能写自由文本。
- **单句试听**：`python tools/qwen_tts.py --speaker q --text "那代价是什么？" --out /tmp/q.wav`
- **备选**：没有 Key 时用 `python tools/tts.py EPxx --backend edge`（Edge 在线 TTS，免 Key，无语气控制），完全离线时用 `--backend command` 接本地 TTS。一集之内不混用后端；正式成片用 qwen。

## 你（人类）需要介入的地方

流程里只有 4 个必须由人确认的检查点，其余全部由 showrunner 自动推进。详见 `docs/00_MASTER_SPEC.md` 第 6 节。

| 检查点 | 时机 | 你要做的事 | 大约耗时 |
| --- | --- | --- | --- |
| H1 | 开工计划写完 | 读 `work/plan.md`，确认论点、集数、优先级 | 15 分钟 |
| H2 | 试点集 EP07 的粗剪（占位画面 + 正式配音）做完 | 听一遍：节奏、讲法、音色对不对 | 20 分钟 |
| H3 | 试点集 EP07 成片 | 看完，回答《观看手册》里的自测题；不满意就写下哪里没懂 | 30 分钟 |
| H4 | 全部成片 | 抽看；决定是否做精华版 | 自定 |

## 交付物

- `work/release/EP00.mp4 … EP13.mp4`（1080p30，软字幕，章节标记，响度 −16 LUFS）及同名 `.srt`
- `work/release/companion/EPxx.md`：每集《观看手册》（一页纸要点 + 5 道自测题 + 代码阅读入口）
- `work/release/series_map.png`：全系列"一个请求的一生"总图
- `work/` 全部中间产物：事实账本、计算脚本、方案、脚本、分镜、动画代码、审校记录，可追溯到每个数字的出处
