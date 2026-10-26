# 09 制作管线

这一份是给 pipeline-engineer 和 animator 的技术手册。所有工具都在 `tools/`，已在 Ubuntu 24.04 + Python 3.12 + Manim CE 0.22 + ffmpeg 6 上用 `examples/smoke` 跑通。

## 1. 工作区结构

```
work/
├── STATUS.md              # 看板（showrunner）
├── plan.md                # 开工计划（showrunner）
├── decisions.md           # 决策记录（所有对规范的偏离、基线变更、P0 校准结果）
├── open_questions.md      # 未解决的事实问题
├── glossary.md            # 术语表（showrunner 维护）
├── facts/                 # 事实账本 EPxx.yaml、GLOBAL.yaml；_alt/ 双人核验草稿（合并成正式账本后即删除，不入库）
├── calc/                  # 计算脚本 EPxx_*.py
├── research/              # 研究简报 EPxx.md；queries/ 技术短问
├── treatments/            # 剧集方案
├── scripts/               # 脚本（机器解析）
├── storyboards/           # 分镜
├── scenes/                # Manim 代码 EPxx.py
├── reviews/               # 全部审校与 QC 记录
├── build/EPxx/            # 构建产物（可随时删掉重建）
│   ├── shots.json         #   parse_script 输出
│   ├── timing.json        #   tts 输出：每镜头时长、cue 时刻、字幕分句
│   ├── audio/             #   每镜头 wav；cache/ 分句缓存
│   ├── manim/             #   Manim 原始输出
│   ├── renders/           #   每镜头视频
│   ├── segments/          #   音画合并后的分段
│   ├── logs/              #   渲染日志
│   ├── keyframes/         #   审片关键帧、拼图、index.md
│   ├── EPxx.mp4 / .srt    #   本集成片
│   └── chapters.txt
└── release/               # 最终交付：EPxx.mp4、EPxx.srt、companion/、series_map.png
```

## 2. 环境

```bash
# 系统依赖（Debian/Ubuntu）
sudo apt-get install -y ffmpeg fonts-noto-cjk fonts-noto-mono libpango1.0-dev libcairo2-dev pkg-config
# Python
python3 -m venv .venv && . .venv/bin/activate
pip install -r tools/requirements.txt
cp .env.example .env            # 填入百炼凭据（qwen 配音后端）
tools/check_env.sh "$DV_KB"
DV_CHECK_TTS=1 tools/check_env.sh "$DV_KB"   # 另外实际合成一句，验证凭据、端点和网络
```

已知坑：

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `Failed to build 'manimpango'` | Linux 上 manimpango 没有预编译 wheel，需要 pango 头文件 | 装 `libpango1.0-dev libcairo2-dev pkg-config` |
| Python 3.14 上装不上 | manimpango 尚未支持 | 用 3.12（`uv venv -p 3.12`） |
| `cannot import name ... from 'click'` | 外部 `PYTHONPATH` 混入了别的 site-packages | 用 `env -u PYTHONPATH` 运行，或清掉 `PYTHONPATH`（`render.py` 给 Manim 子进程设置了干净的 `PYTHONPATH`） |
| 中文显示为方块 | 缺字体 | 装 `fonts-noto-cjk`；`fc-list | grep "Noto Sans CJK SC"` |
| `backend qwen needs DASHSCOPE_API_KEY` | 没有 `.env` | `cp .env.example .env` 后填凭据；临时没有 Key 就 `--backend edge` |
| Qwen 返回 401/403 | Key 错，或出口 IP 不在工作空间白名单里 | 核对 Key；确认 `DASHSCOPE_PROXY` 是否该设；保持 `DASHSCOPE_IPV4_ONLY=1` |
| Qwen 返回 429 | 并发太高 | `tts.py --jobs 2`；重跑只补缺的分句 |
| Qwen 连接被拒 / 超时 | 代理没开，或 shell 里残留的 `DASHSCOPE_PROXY` 覆盖了 `.env` | `env | grep DASHSCOPE` 查实际生效的值 |
| Edge TTS 超时或 403 | 网络，或 edge-tts 版本太旧 | 自动重试 4 次；仍失败就升级 edge-tts，或改回 qwen |

## 3. 从脚本到成片

```
scripts/EPxx.md ──parse_script──► build/EPxx/shots.json ──lint_script──► (0 ERROR)
                                         │
                                         ├──tts──► audio/*.wav + timing.json（cue 时刻）
                                         │                 │
scenes/EPxx.py ──────────────────────────┴──render──► renders/*.mp4（动画按 cue 对时）
                                                           │
                                         assemble ◄────────┘──► EPxx.mp4 + .srt + 章节
                                                           │
                                         keyframes ──► keyframes/sheet_*.png + index.md
```

**配音先行**：先有配音，再有动画。每个镜头的时长由旁白决定；动画通过 cue 等待旁白。这样改一句旁白只需要重配那一句、重渲那一个镜头。

### 3.1 parse_script.py

- 输入 `work/scripts/EPxx.md`，输出 `shots.json`。
- 把旁白按句号/问号/分号、cue、pause、说话人切成"分句"（chunk）。每个分句单独配音，单独成为一条字幕。
- 处理 `{写法|读法}`，并用 `tools/lexicon.yaml` 生成配音文本（字幕保留写法）。
- 估算时长：语速系数 `CPS` 取当前后端在 `tools/voices.yaml` 里的 `cps`（qwen 4.9，edge 3.8；单位是 `spoken_len()` 计数/秒，中文一字计 1），可用环境变量 `DV_CPS` 临时覆盖；P0 用实测值校准。分句间隔 0.12 秒，镜头前 0.35 秒、后 0.6 秒留白。

### 3.2 lint_script.py

报错（必须修）：缺旁白、事实 ID 不存在、事实状态不可用、有数字没挂事实、有事实没有角标、`scope` 非法、禁用词、句子超过 60 字、镜头 ID 重复、动画等待的 cue 在旁白里不存在。

警告：句子超过 42 字、估算时长偏离目标 30%、屏幕字超过 20 字或 4 行、角标比引用事实强、D 级事实、`unverifiable` 事实、带逗号的数字（配音会读坏）。

INFO：配音会原样读出的大写/数字词，供补 lexicon。

### 3.3 lint_facts.py

检查账本格式、ID 前缀、等级与状态取值、A 级是否有 `路径:行号` 与 commit、`calc` 脚本是否存在；加 `--kb $DV_KB` 时还会检查源码路径存在、行号不越界。

### 3.4 tts.py

```bash
python tools/tts.py EP07                         # 全集（默认 qwen 后端）
python tools/tts.py EP07 --shots S03,S04         # 只重配两个镜头
python tools/tts.py EP07 --backend edge          # 免 Key 备选
python tools/qwen_tts.py --speaker q --text "那代价是什么？" --out /tmp/q.wav   # 单句试听
DV_TTS_BACKEND=command DV_TTS_CMD='python cosy.py --spk {speaker} --text-file {text} --out {out}' python tools/tts.py EP07
```

#### 3.4.1 后端选型

| 后端 | 定位 | 音色 | 语气控制 | 需要 |
| --- | --- | --- | --- | --- |
| `qwen` | **推荐，正式配音一律用它** | 旁白 `longanhuan_v3.1`，提问者 `longanlingxin_v3.1` | 有：每次请求带一条 `instruction` | `.env` 里的百炼凭据 |
| `edge` | 备选：没有 Key 时调试、CI（仍需联网） | 旁白 `zh-CN-YunxiNeural`，提问者 `zh-CN-XiaoxiaoNeural` | 无 | 联网 |
| `command` | 完全离线时接本地 TTS（CosyVoice、Fish-Speech 等） | 由命令按 `{speaker}` 决定 | 由命令决定 | `DV_TTS_CMD` |

选 Qwen-Audio-3.1-TTS-Plus（阿里云百炼）的理由：

1. **委托人已实测通过**：音色与口吻是委托人亲自试听后定下的，这是 H2 之前唯一需要人耳判断的事。
2. **语气可控**：每句话可以带一条自然语言 `instruction`。冷开场、讲代价、讲不确定的事、总结，需要不同的语气；Edge 只能调语速。
3. **两个声音分得开**：解说和提问者用同一系列的两个音色，一听就知道谁在说话，又不会像两个节目拼在一起。
4. **格式直接对齐**：返回 24 kHz 单声道 WAV，与 `timing.json` 和 `assemble.py` 的采样率一致（`tts.py` 仍会用 ffmpeg 统一转一次，防止服务端格式变化）。
5. **服务稳定、有账号与白名单**：走工作空间专属端点。Edge TTS 走的是非官方接口，曾出现过握手被拒（403）的情况，只适合做备选。

一集之内**不能混用后端**：两个后端的音色、语速都不同，混用会让同一个"人"换了声音。改后端就整集重配。

#### 3.4.2 配置

- 凭据放在 Spec 根目录的 `.env`（模板 `.env.example`），**不进版本库、不进压缩包、不写进日志或报告**。
  - `DASHSCOPE_API_KEY`（必填）、`DASHSCOPE_ENDPOINT`（工作空间专属端点）、`DASHSCOPE_MODEL`（`qwen-audio-3.1-tts-plus`）
  - `DASHSCOPE_PROXY`：不设或留空就直连；出口必须走白名单代理时设置，例如 `http://127.0.0.1:7890`
  - `DASHSCOPE_IPV4_ONLY`：默认 `1`，域名只解析到 IPv4。专属端点按 IP 白名单放行，双栈机器若从 IPv6 出去会被拒
  - 已经在 shell 里 export 的同名变量优先于 `.env`
- 音色、语气预设、语速估算系数都在 `tools/voices.yaml`。默认后端也在这里（`backend: qwen`），可用 `DV_TTS_BACKEND` 或 `--backend` 临时覆盖。
- `tools/qwen_tts.py` 是唯一的 Qwen 调用实现：`tts.py` 把它当模块导入，它自己也能当命令行单句试听。只用 Python 标准库，网络错误与 429/5xx 自动重试 4 次。

#### 3.4.3 语气（instruction）

- 旁白默认用 `voices.yaml` 里的 `n`，提问者（`Q：` 行）永远用 `q`。
- 某个镜头需要别的语气时，在镜头元数据里写 `tone: <预设名>`，例如 `<!-- shot: S11 | ... | tone: cost -->`。只影响本镜头的旁白行。
- 预设名必须在 `voices.yaml` 的 `qwen.tones` 里，`lint_script.py` 会检查。脚本里不允许写自由文本的 instruction。
- 写法规则、预设清单、什么时候用哪个，见 `docs/03_NARRATION_STYLE.md` 第 12 节。

#### 3.4.4 缓存与输出

- 分句按"后端 + 模型 + 音色 + 语气 + 语速 + 读音文本"的哈希缓存在 `audio/cache/`。改了任何一项，只重配受影响的分句。
- 输出 `timing.json`：每镜头 `duration`、`cues`（镜头内秒数）、`chunks`（字幕分句的起止时刻），以及本集用的 `backend`、`model`、`voices`；qwen 后端还记录每个镜头的 `tone`。
- `--rate` 只对 edge 有效；qwen 的快慢由语气预设决定。
- 并发默认 qwen 4、edge 6（`--jobs` 可改）。遇到限流（429）先把 `--jobs` 调小。
### 3.5 render.py

```bash
python tools/render.py EP07 --quality preview      # 854x480 15fps，审片用
python tools/render.py EP07 --quality draft        # 1280x720 30fps
python tools/render.py EP07 --quality final        # 1920x1080 30fps
python tools/render.py EP07 --animatic             # 全部用占位卡（粗剪）
python tools/render.py EP07 --shots S05 --jobs 1   # 单镜头调试
```

- 脚本里写了 `scene: auto`，或者 `scenes/EPxx.py` 里没有对应类的镜头，自动用 `manim_lib/autocard.py` 的占位卡，所以任何阶段都能合成整集。
- 每个镜头单独一个 Manim 进程，默认并行数为 CPU 核数的一半。
- 日志在 `build/EPxx/logs/render_<镜头>.log`；`[dvlib] WARN`（对时晚到、字号、版式重叠，见 04 第 2.1 节）逐镜头打印，最后给总数。
- `--quality final` 只要有 WARN 就以非零退出；确有理由放行时加 `--allow-warn`，并在 `decisions.md` 写明是哪几条、为什么。

### 3.6 assemble.py

- 每个镜头：视频补帧到配音长度（定格最后一帧），配音补静音到视频长度；统一分辨率、30 fps、yuv420p、48 kHz 立体声。
- 镜头段缓存：`build/EPxx/segments/<镜头>.mp4` 旁边有一个 `.key`，记录渲染文件与配音文件的修改时间、大小、分辨率和时长；任何一项变了就重新合成该镜头。（试点版只看"文件存在且大于 10 KB"，重渲过的镜头不会进成片。）
- 拼接；整集做响度标准化（`loudnorm I=-16 TP=-1.5 LRA=11`）。loudnorm 内部会把音频升到 192 kHz，所以最终输出显式写 `-ar 48000`。（试点版漏了这一步，成片是 96 kHz。）
- 生成 `EPxx.srt`（每行 ≤ 20 字，按字数分配时间；提问者台词前加"（问）"）和章节标记（每个镜头一个章节，标题为镜头标题）。
- 默认全量硬压字幕（burn-subs，通过 libass 将精准样式的中文字幕烧进画面，保证任何终端与播放器均无障碍显示）；如需输出无字幕母带加 `--soft-subs`。
- `--bgm music.mp3 --bgm-db -30`：循环铺底音乐。

### 3.6.1 pacing_report.py

```bash
python tools/pacing_report.py EP07   # 配音之后；make_episode.sh 自动跑
```

读 `shots.json` 与 `timing.json`，写 `build/EPxx/pacing.md`：每镜目标/实际时长、字/秒、静音占比、Q 数；各语气平均语速；整集时长对目标。警告项：单镜偏差 > 30%、片头卡 > 8 秒、静音 > 25%、某语气语速偏离正文 > 20%、正文语速偏离 `voices.yaml` 的 `cps` > 10%、Q 太少或连续 8 镜无 Q。整集偏离 `target_min` 超过 15% 是 ERROR，在 `final` 构建中会中止 `make_episode.sh`。这份报告是 G7 的输入。

### 3.7 keyframes.py

每个镜头在每个 cue 后 0.6 秒、中点、结尾各取一帧，生成 4×3 拼图 `sheet_NN.png` 和 `index.md`（每帧对应的镜头、时刻、此刻旁白）。art-director 与 tech-reviewer 看这个，不需要看视频。

### 3.8 make_episode.sh

```bash
tools/make_episode.sh EP07 preview            # 审片版
tools/make_episode.sh EP07 preview --animatic # 粗剪
tools/make_episode.sh EP07 final              # 成片，并复制到 work/release/
```

- 成片**只能**由 `make_episode.sh EPxx final` 产出，不能手动拼 `assemble.py` 的参数代替；QC 测的必须是这条命令复制到 `work/release/` 的文件。
- `work/release/` 只放 `EPxx.mp4`（内嵌硬字幕成片）、`EPxx.srt` 和 `companion/EPxx.md`。无字幕母带或打包 zip 这类额外产物放 `build/EPxx/extra/`，并在 `decisions.md` 说明用途。

## 4. Manim 镜头写法（animator）

### 4.1 骨架

```python
from manim import DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, VGroup
from dvlib import DECODE, MUTED, PREFILL, SWA, DVScene, T, TokenRow, header, window_bracket


class EP07_S04(DVScene):
    SHOT = "EP07-S04"            # 必须与脚本镜头号一致

    def construct(self):
        self.add(header("只重算最后一小段", "decoder 层的 prefill"))
        row = TokenRow(24, PREFILL)
        self.play(FadeIn(row), run_time=0.8)
        self.until("keep")       # 等旁白读到 [#keep]
        self.play(Create(window_bracket(row, 17, 23, DECODE, "保留 140 行")), run_time=0.8)
        self.finish()            # 定格到旁白结束
```

### 4.2 规则

1. 一个镜头一个类，类名 `EPxx_Syy`，`SHOT = "EPxx-Syy"`。
2. 时长只由 `until()` 和 `finish()` 控制。允许 `self.wait(≤1)` 做节奏停顿；不允许用长 `wait` 凑时长。
3. 动画在 cue 之后发生。如果动画比旁白慢，`until` 会打印 `late` 警告；`finish` 会打印 `runs past` 警告。两种警告都要修（缩短 `run_time`，或请编剧在旁白里加 `[pause:x]`）。
4. 颜色只用 dvlib 常量；文字只用 `T()`（正文）和 `M()`（代码）。
5. 角标和范围标签由 `DVScene` 根据脚本元数据自动加，不要手动画。不需要角标的镜头（片头卡）设 `SHOW_BADGE = False`。标题较长时用 `self.fit_left_of_tags(header(...))`，避免压到右上角的标签。
6. 不在镜头代码里写任何不在脚本/分镜里的数字或文字。
7. 镜头之间不共享状态。需要"接着上一个镜头"的画面时，在本镜头开头直接 `self.add()` 上一镜头结束时的画面元素（不做淡入）。
8. 新组件写进 `manim_lib/dvlib.py`，带 docstring，并在 `docs/04_VISUAL_LANGUAGE.md` 第 4 节登记。改动已有组件前，确认不会破坏已完成的集（重渲一遍 EP99 冒烟测试）。新组件里的文字一律用 `T()`/`M()`，框随文字撑开，不把文字缩到装得下为止。
9. 版式：主角放在 `STAGE` 里（04 第 2 节），"示意"脚注和出处放在 y ≥ −2.75；新卡片出现前，先让底下的图变暗或移开。每个镜头预览渲染后 `[dvlib] WARN … layout` 必须为 0。
10. 不要对整组元素 `.scale(<1)` 来"塞进去"——缩完的字号会被 `check_layout` 报出来。装不下就拆镜头或删内容。

### 4.3 调试

```bash
# 只渲一个镜头并直接看日志
python tools/render.py EP07 --shots S04 --jobs 1 && cat work/build/EP07/logs/render_EP07-S04.log
# 没有 timing.json 时也能渲：DVScene 会用 shots.json 的估算时长和估算 cue
```

## 5. QC 测量

```bash
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels -show_entries format=duration -of compact work/release/EP07.mp4   # 音频必须 sample_rate=48000
ffmpeg -i work/release/EP07.mp4 -af loudnorm=print_format=summary -f null - 2>&1 | tail -12   # Input Integrated 应在 -16±1 LUFS
ffprobe -v error -show_chapters -of compact work/release/EP07.mp4 | head
```

## 6. 精华版（可选，H4 之后）

从各集挑镜头组成新脚本 `work/scripts/DIGEST.md`（镜头标题后用 `<!-- shot: S01 | ... | scene: EP07_S04 -->` 复用已有类时，需要把对应类复制进 `work/scenes/DIGEST.py`），重新配音（衔接句由 screenwriter 新写），按普通一集走 P4–P9。
