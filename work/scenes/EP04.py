"""EP04 scenes: 代码地图：一个请求在仓库里的一生 (shots S01-S21).

Layout convention used throughout this episode:
  * header via self.fit_left_of_tags(header(...))
  * hero content lives in y in [-2.2, 2.0]
  * bottom safe line stays at y >= -2.65 (subtitle safe zone below -2.75)
  * text sizes >= 18 pt (small labels >= 16 pt)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import (
    DOWN, LEFT, RIGHT, UP, UL, UR, DL, DR, PI, TAU,
    FadeIn, FadeOut, Create, Indicate, Rotate, LaggedStart,
    Line, Arrow, Rectangle, RoundedRectangle, Circle, VGroup, DashedLine, DashedVMobject,
    Arc, Sector, AnnularSector, ArcBetweenPoints, SurroundingRectangle,
)
from manim_lib.dvlib import (
    BG, FG, MUTED, GRID, PREFILL, DECODE, KV, SWA, WARN, EXPERT, DRAFT, GPU, CPU,
    T, M, Pill, DVScene, header, MiniMap, Block, TokenRow, window_bracket,
    code_panel, number_card, LayerStack, Scale, Timeline,
)


class _E04(DVScene):
    """Small helpers shared by every EP04 shot."""

    def foot(self, text: str, x: float = 6.4, y: float = -2.25, size: int = 16):
        """Right-aligned footnote, stays safely above -2.65."""
        t = T(text, size, MUTED)
        t.move_to([x, y, 0], aligned_edge=UR)
        return t

    def foot_lines(self, lines, x: float = 6.4, y: float = -2.20, size: int = 16):
        g = VGroup(*[T(s, size, MUTED) for s in lines])
        g.arrange(DOWN, buff=0.06, aligned_edge=RIGHT)
        g.move_to([x, y, 0], aligned_edge=UR)
        return g


# ---------------------------------------------------------------- S01
class EP04_S01(_E04):
    SHOT = "EP04-S01"

    def construct(self):
        head = self.fit_left_of_tags(header("代码树里的反直觉反差", "EP04 · S01 冷开场"))
        self.add(head)

        tree_box = RoundedRectangle(width=5.2, height=3.4, corner_radius=0.15, stroke_color=MUTED, stroke_width=1.5,
                                    fill_color=MUTED, fill_opacity=0.15).move_to([-3.6, -0.15, 0])
        tree_title = T("DeepInfer 仓库 (4.7万行 Python)", 20, FG).move_to([-3.6, 1.25, 0])

        items = VGroup(
            T("• deepinfer/ (核心包 · 4.7万行)", 18, DECODE),
            T("• csrc/ (C++ 引擎核 · 5,909行)", 18, PREFILL),
            T("• vendor/ (6个算子子模块)", 18, GPU),
            T("• examples/ & tests/ (样例与测试)", 18, MUTED),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([-3.4, -0.3, 0])

        pill_vllm = Pill("23 个派生文件 (仅 12.4%)", WARN, size=20).move_to([3.4, 1.4, 0])
        card_ops = number_card("49.5%", "算子层占比", "23,331 行 / 47,172 行", color=DECODE).move_to([3.4, 0.05, 0])
        block_cpp = Block("C++ 调度核心 (csrc/engine)\n完全释放 GIL · 管理对象池", color=PREFILL, w=5.0, h=1.1, size=18).move_to([3.4, -1.35, 0])

        self.play(FadeIn(tree_box), FadeIn(tree_title), FadeIn(items), run_time=1.0)

        self.until("repo_tree")
        self.play(Indicate(items[0], color=DECODE), run_time=0.8)

        self.until("scan_highlight")
        scan_line = Line(LEFT * 6, RIGHT * 6, color=WARN, stroke_width=3).move_to([0, 1.8, 0])
        self.play(FadeIn(scan_line), scan_line.animate.move_to([0, -1.8, 0]), run_time=1.2)
        self.play(FadeOut(scan_line), run_time=0.3)

        self.until("vllm_files")
        self.play(FadeIn(pill_vllm), run_time=0.8)

        self.until("tilelang_share")
        self.play(FadeIn(card_ops), run_time=0.8)

        self.until("cpp_core")
        self.play(FadeIn(block_cpp), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S02
class EP04_S02(_E04):
    SHOT = "EP04-S02"

    def construct(self):
        title = T("EP04 · 代码地图", 48, DECODE).move_to([0, 0.6, 0])
        sub = T("一个请求在仓库里的一生", 32, FG).move_to([0, -0.2, 0])
        mmap = MiniMap(active="Schedule", scale=1.05).move_to([0, -1.3, 0])

        self.play(FadeIn(title), FadeIn(sub), run_time=0.8)

        self.until("card")
        self.play(FadeIn(mmap), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S03
class EP04_S03(_E04):
    SHOT = "EP04-S03"

    def construct(self):
        head = self.fit_left_of_tags(header("三层架构立面与代码量", "EP04 · S03 目录全貌"))
        self.add(head)

        b_top = Block("顶层: Python 业务编排 (deepinfer/) · 47,172 行", color=DECODE, w=8.8, h=1.0, size=20).move_to([0, 1.25, 0])
        b_mid = Block("中间层: C++ 调度核心 (csrc/) · 5,909 行 (纯 Host 调度)", color=PREFILL, w=8.8, h=1.0, size=20).move_to([0, 0.0, 0])
        b_bot = Block("底层: 设备镜像算子库 (tilelang_ops/ + vendor/) · 2.3万+ 行", color=GPU, w=8.8, h=1.0, size=20).move_to([0, -1.25, 0])

        glue_line = DashedLine(LEFT * 4.6, RIGHT * 4.6, color=WARN, stroke_width=2).move_to([0, 0.62, 0])
        glue_tag = Pill("pybind11 胶水边界 · C++ 释放 GIL", WARN, size=18).move_to([0, 0.62, 0])

        foot = self.foot("代码统计口径: 物理行数 (排除 vendor CUTLASS 副本)")

        self.play(FadeIn(b_top), FadeIn(b_mid), FadeIn(b_bot), run_time=1.0)

        self.until("show_layers")
        self.play(Indicate(b_top, color=DECODE), run_time=0.8)

        self.until("top_py")
        self.play(Indicate(b_top, color=DECODE), run_time=0.8)

        self.until("mid_cpp")
        self.play(Indicate(b_mid, color=PREFILL), run_time=0.8)

        self.until("bot_ops")
        self.play(Indicate(b_bot, color=GPU), run_time=0.8)

        self.until("boundary_line")
        self.play(Create(glue_line), FadeIn(glue_tag), FadeIn(foot), run_time=1.0)

        self.finish()


# ---------------------------------------------------------------- S04
class EP04_S04(_E04):
    SHOT = "EP04-S04"

    def construct(self):
        head = self.fit_left_of_tags(header("算子层占半壁与双镜像", "EP04 · S04 代码重心"))
        self.add(head)

        card = number_card("49.5%", "tilelang_ops 占比", "23,331 行 / 47,172 行", color=KV).move_to([0, 1.35, 0])

        box_cuda = Block("NVIDIA CUDA 后端 (cuda/)\n30 个镜像算子文件 · 4,968 行", color=DECODE, w=5.0, h=2.2, size=18).move_to([-3.2, -0.65, 0])
        box_asc = Block("华为昇腾 Ascend 后端 (asc/)\n30 个镜像算子文件 · 7,418 行", color=PREFILL, w=5.0, h=2.2, size=18).move_to([3.2, -0.65, 0])

        dispatcher = Pill("ops.py (统一动态派发器)", FG, size=20).move_to([0, -0.65, 0])
        arr_l = Arrow(dispatcher.get_left(), box_cuda.get_right(), color=DECODE, buff=0.1)
        arr_r = Arrow(dispatcher.get_right(), box_asc.get_left(), color=PREFILL, buff=0.1)

        note = Pill("昇腾侧多 2,450 行 (手工分块与对齐约束)", WARN, size=18).move_to([3.2, -2.1, 0])

        self.play(FadeIn(card), run_time=0.8)

        self.until("focus_shift")
        self.play(FadeIn(box_cuda), FadeIn(box_asc), run_time=0.8)

        self.until("ops_percent")
        self.play(Indicate(card, color=KV), run_time=0.8)

        self.until("mirror_layout")
        self.play(FadeIn(dispatcher), Create(arr_l), Create(arr_r), run_time=1.0)

        self.until("asc_extra")
        self.play(FadeIn(note), Indicate(box_asc, color=WARN), run_time=1.0)

        self.finish()


# ---------------------------------------------------------------- S05
class EP04_S05(_E04):
    SHOT = "EP04-S05"

    def construct(self):
        head = self.fit_left_of_tags(header("23 个派生文件与 12% 胶水层", "EP04 · S05 血统剖析"))
        self.add(head)

        q_pill = Pill("Q：带有 vLLM 派生声明的文件，到底改了些什么？", WARN, size=20).move_to([0, 1.55, 0])

        donut_bg = Circle(radius=1.5, color=DECODE, fill_color=DECODE, fill_opacity=0.3, stroke_width=4).move_to([-3.5, -0.3, 0])
        donut_slice = AnnularSector(inner_radius=0.8, outer_radius=1.5, angle=TAU * 0.124, start_angle=PI/2,
                                    fill_color=WARN, fill_opacity=0.9, stroke_color=WARN, stroke_width=2).move_to([-3.5, -0.3, 0])
        pct_tag = T("12.4%\nvLLM胶水", 20, WARN).move_to([-3.5, -0.3, 0])

        card_glue = Block("23 个派生文件 (6,817 行)\n• arg_utils.py / config.py (参数解析)\n• llm_engine.py / worker.py (进程外壳)\n• sequence.py / sampling_params.py (容器)",
                          color=WARN, w=6.4, h=2.0, size=16).move_to([3.2, 0.4, 0])

        card_core = Block("100% 纯自研核心 (0 行借用)\n• 模型层: deepseek_vl.py / decoder_layer.py\n• 调度层: csrc/engine/ (纯 C++ 引擎核)\n• 算子层: tilelang_ops/ (双镜像算子)",
                          color=KV, w=6.4, h=2.0, size=16).move_to([3.2, -1.3, 0])

        self.play(FadeIn(q_pill), run_time=0.6)

        self.until("q_lineage")
        self.play(FadeIn(donut_bg), FadeIn(donut_slice), FadeIn(pct_tag), run_time=1.0)

        self.until("pie_slice")
        self.play(Indicate(donut_slice, color=WARN), run_time=0.8)

        self.until("glue_box")
        self.play(FadeIn(card_glue), run_time=0.8)

        self.until("clean_core")
        self.play(FadeIn(card_core), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S06
class EP04_S06(_E04):
    SHOT = "EP04-S06"

    def construct(self):
        head = self.fit_left_of_tags(header("v0.2.x 骨架与 shm 补丁", "EP04 · S06 历史分叉"))
        self.add(head)

        tline = Timeline(["上游 vLLM 演进", "DeepInfer 演进"], width=9.2, lane_h=0.8, scale=0.9).move_to([0.6, 0.6, 0])

        b_fork = tline.bar(0, 1.2, 3.2, "2023.12: v0.2.x 分叉点", color=DECODE)
        b_sync_bar = tline.bar(1, 4.8, 3.2, "2024 中期: shm_broadcast 同步", color=PREFILL)

        b_fingerprint = Block("API 指纹留存 (v0.2.x):\n• create_engine_configs 返回 4元组\n• profile/init/warmup 三连命名",
                              color=DECODE, w=5.2, h=1.6, size=16).move_to([-3.0, -1.0, 0])

        b_sync = Block("单文件反向同步 (v0.6.3+):\n• distributed/shm_broadcast.py (相似度 0.68)\n• 仅为多进程无拷贝广播",
                       color=PREFILL, w=5.2, h=1.6, size=16).move_to([3.0, -1.0, 0])

        self.play(FadeIn(tline), run_time=0.8)

        self.until("timeline_start")
        self.play(FadeIn(b_fork), run_time=0.6)

        self.until("v02_fingerprint")
        self.play(FadeIn(b_fingerprint), run_time=0.8)

        self.until("fork_point")
        self.play(FadeIn(b_sync_bar), run_time=0.6)

        self.until("shm_sync")
        self.play(FadeIn(b_sync), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S07
class EP04_S07(_E04):
    SHOT = "EP04-S07"

    def construct(self):
        head = self.fit_left_of_tags(header("单架构定位与在线缺失", "EP04 · S07 边界声明"))
        self.add(head)

        warning_pill = Pill("开源边界警示: 本仓库为离线推理引擎，非在线 Serving", WARN, size=20).move_to([0, 1.55, 0])

        box_model = Block("唯一模型注册:\nDeepseekV41ForCausalLM\n(统一映射到 deepseek_vl 纯文本/多模态)", color=KV, w=5.2, h=2.2, size=18).move_to([-3.2, -0.2, 0])

        box_missing = Block("开源代码缺失基建 (仅在文档描述):\n• 无 AsyncLLM 在线异步服务\n• 无 OpenAI API Server (HTTP/流式)\n• 无 3FS KV 存储与跨副本负载均衡",
                            color=WARN, w=5.6, h=2.2, size=16).move_to([3.1, -0.2, 0])

        box_profile = Block("仓库唯一的 HTTP 服务: engine/profile_server.py (仅用于 Torch Profiler 采样采样)", color=MUTED, w=8.8, h=0.8, size=16).move_to([0, -1.9, 0])

        self.play(FadeIn(warning_pill), run_time=0.6)

        self.until("scope_warning")
        self.play(FadeIn(box_model), run_time=0.8)

        self.until("single_model")
        self.play(Indicate(box_model, color=KV), run_time=0.8)

        self.until("no_serving")
        self.play(FadeIn(box_missing), run_time=0.8)

        self.until("profile_server")
        self.play(FadeIn(box_profile), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S08
class EP04_S08(_E04):
    SHOT = "EP04-S08"

    def construct(self):
        head = self.fit_left_of_tags(header("推理起点: offline_inference.py", "EP04 · S08 样例追踪"))
        self.add(head)

        q_pill = Pill("Q：代码里的第一行执行语句，究竟该从哪个文件看起？", WARN, size=20).move_to([0, 1.55, 0])

        snippet = ("# offline_inference.py\n"
                   "from deepinfer import LLM\n"
                   "llm = LLM(model='V4.1')\n"
                   "prompts = ['Hello', 'World']\n"
                   "outputs = llm.generate(prompts)")
        code = code_panel(snippet, "examples/offline_inference.py", highlight=[3, 5], size=16, width=5.6).move_to([-3.1, -0.25, 0])

        box_spec = Block("运行门槛假设:\n• 样例默认单机 8 卡 EP8\n• 硬件常量硬编码 SM100 2250 TFLOPS\n• 非 SM100 初始化抛出 unknown GPU",
                         color=WARN, w=4.4, h=2.5, size=16).move_to([3.8, -0.25, 0])

        self.play(FadeIn(q_pill), run_time=0.6)

        self.until("trace_start")
        self.play(FadeIn(code), run_time=0.8)

        self.until("q_where_start")
        self.play(Indicate(code, color=DECODE, scale_factor=1.0), run_time=0.8)

        self.until("code_entry")
        self.play(FadeIn(box_spec), run_time=0.8)

        self.until("eight_card_spec")
        self.play(Indicate(box_spec, color=WARN, scale_factor=1.0), run_time=0.8)

        self.until("hardware_check")
        foot = self.foot("读代码不等于能轻量运行它 (参见 R18 上手笔记)")
        self.play(FadeIn(foot), run_time=0.5)

        self.finish()


# ---------------------------------------------------------------- S09
class EP04_S09(_E04):
    SHOT = "EP04-S09"

    def construct(self):
        head = self.fit_left_of_tags(header("预分词与 C++ Sequence 接管", "EP04 · S09 请求入队"))
        self.add(head)

        box_text = Block("用户文本 Prompts\n['Hello, ...', ...]", color=FG, w=3.2, h=1.4, size=18).move_to([-4.4, 0.4, 0])
        t_row = TokenRow(6, color=PREFILL, size=0.35).move_to([0, 0.4, 0])
        box_seq = Block("C++ Sequence 对象\n(csrc/engine/sequence.hpp)\n• prompt_token_ids (np.int32)\n• 移交非阻塞内存池管理",
                        color=DECODE, w=4.5, h=2.2, size=16).move_to([4.2, 0.0, 0])

        arr1 = Arrow(box_text.get_right(), t_row.get_left(), color=MUTED, buff=0.1)
        arr2 = Arrow(t_row.get_right(), box_seq.get_left(), color=DECODE, buff=0.1)

        rule_pill = Pill("架构边界: 字符串就地分词，调度核心仅处理数字张量", KV, size=18).move_to([0, -1.7, 0])

        self.play(FadeIn(box_text), run_time=0.6)

        self.until("entry_tokenize")
        self.play(Create(arr1), FadeIn(t_row), run_time=0.8)

        self.until("pass_array")
        self.play(Create(arr2), FadeIn(box_seq), run_time=0.8)

        self.until("cpp_seq_box")
        self.play(Indicate(box_seq, color=DECODE), run_time=0.8)

        self.until("freeze_string")
        self.play(FadeIn(rule_pill), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S10
class EP04_S10(_E04):
    SHOT = "EP04-S10"

    def construct(self):
        head = self.fit_left_of_tags(header("单引擎管 CP 卡与主从 spawn", "EP04 · S10 进程拓扑"))
        self.add(head)

        b_driver = Block("Driver 进程 (卡0)\n• 运行 LLMEngine\n• 独占 C++ Scheduler\n• 负责全局决策与采样",
                         color=DECODE, w=4.0, h=2.8, size=16).move_to([-3.8, 0.0, 0])

        workers = VGroup(
            Block("Worker 1 (卡1 · spawn 子进程)", color=MUTED, w=4.2, h=0.7, size=16),
            Block("Worker 2 (卡2 · spawn 子进程)", color=MUTED, w=4.2, h=0.7, size=16),
            Block("Worker 3 (卡3 · spawn 子进程)", color=MUTED, w=4.2, h=0.7, size=16),
        ).arrange(DOWN, buff=0.25).move_to([3.4, 0.0, 0])

        lines = VGroup(*[Arrow(b_driver.get_right(), w.get_left(), color=MUTED, buff=0.1) for w in workers])

        pill_guard = Pill("深水铁律: 顶层严禁 import torch，防止多进程 fork 死锁", WARN, size=18).move_to([0, -2.0, 0])

        self.play(FadeIn(b_driver), run_time=0.8)

        self.until("topo_layout")
        self.play(Create(lines), FadeIn(workers), run_time=1.0)

        self.until("driver_focus")
        self.play(Indicate(b_driver, color=DECODE), run_time=0.8)

        self.until("spawn_followers")
        self.play(LaggedStart(*[Indicate(w, color=PREFILL) for w in workers], lag_ratio=0.15), run_time=1.0)

        self.until("no_torch_import")
        self.play(FadeIn(pill_guard), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S11
class EP04_S11(_E04):
    SHOT = "EP04-S11"

    def construct(self):
        head = self.fit_left_of_tags(header("告别 TP，走向 DP/CP/EP", "EP04 · S11 并行真相"))
        self.add(head)

        q_pill = Pill("Q：为什么代码库里找不到一行张量并行 (TP) 的初始化？", WARN, size=20).move_to([0, 1.55, 0])

        tp_box = Block("张量并行 (TP)\n卡内层内切分矩阵\n(已全盘移除，零通信组)", color=MUTED, w=4.2, h=2.2, size=18).move_to([-3.6, -0.2, 0])
        cross = VGroup(
            Line([-5.4, 0.6, 0], [-1.8, -1.0, 0], color=WARN, stroke_width=6),
            Line([-5.4, -1.0, 0], [-1.8, 0.6, 0], color=WARN, stroke_width=6),
        )

        right_groups = VGroup(
            Block("CP (上下文并行): 跨卡切分超长 Attention 序列", color=DECODE, w=6.0, h=0.7, size=16),
            Block("DP (数据并行): 跨卡切分独立批次 Batch 请求", color=PREFILL, w=6.0, h=0.7, size=16),
            Block("EP (专家并行): MoE 专家跨卡路由 All-to-All", color=EXPERT, w=6.0, h=0.7, size=16),
        ).arrange(DOWN, buff=0.2).move_to([3.0, -0.2, 0])

        self.play(FadeIn(q_pill), run_time=0.6)

        self.until("parallel_reveal")
        self.play(FadeIn(tp_box), run_time=0.8)

        self.until("q_where_tp")
        self.play(Create(cross), run_time=0.8)

        self.until("slash_tp")
        self.play(FadeIn(right_groups), run_time=1.0)

        self.until("show_groups")
        self.play(LaggedStart(*[Indicate(g, color=KV) for g in right_groups], lag_ratio=0.15), run_time=1.0)

        self.until("clean_comm")
        foot = self.foot("彻底消除单层高频 All-Reduce 通信开销")
        self.play(FadeIn(foot), run_time=0.5)

        self.finish()


# ---------------------------------------------------------------- S12
class EP04_S12(_E04):
    SHOT = "EP04-S12"

    def construct(self):
        head = self.fit_left_of_tags(header("10×1MB 环形 SHM 与单向 RPC", "EP04 · S12 控制面广播"))
        self.add(head)

        slots = VGroup()
        for i in range(10):
            ang = i * (TAU / 10)
            x, y = 2.0 * math.cos(ang) - 1.2, 1.4 * math.sin(ang) - 0.2
            slots.add(RoundedRectangle(width=0.7, height=0.45, corner_radius=0.08, stroke_color=PREFILL, stroke_width=1.5,
                                       fill_color=PREFILL, fill_opacity=0.25).move_to([x, y, 0]))

        center_txt = T("10 × 1 MiB\n环形共享内存", 16, FG).move_to([-1.2, -0.2, 0])

        driver_card = Block("Driver (卡0)\n广播: (method, kwargs)", color=DECODE, w=3.4, h=1.4, size=16).move_to([-5.2, -0.2, 0])
        follower_card = Block("Follower Worker\ngetattr(self, method)(**kwargs)\n(无任何返回值!)", color=MUTED, w=3.6, h=1.8, size=16).move_to([4.2, -0.2, 0])

        arrow_fwd = Arrow(driver_card.get_right(), [-2.8, -0.2, 0], color=DECODE, buff=0.1)
        arrow_out = Arrow([0.4, -0.2, 0], follower_card.get_left(), color=PREFILL, buff=0.1)

        cross_ret = VGroup(
            Line([2.5, -1.3, 0], [4.5, -1.3, 0], color=MUTED, stroke_width=2),
            Line([3.2, -1.1, 0], [3.8, -1.5, 0], color=WARN, stroke_width=4),
            Line([3.8, -1.1, 0], [3.2, -1.5, 0], color=WARN, stroke_width=4),
            T("零返回值传输 · 彻底消除双向等待", 16, WARN).move_to([3.5, -1.75, 0])
        )

        self.play(FadeIn(slots), FadeIn(center_txt), run_time=1.0)

        self.until("shm_ring_init")
        self.play(FadeIn(driver_card), Create(arrow_fwd), run_time=0.8)

        self.until("shm_chunks")
        self.play(LaggedStart(*[Indicate(s, color=KV) for s in slots], lag_ratio=0.08), run_time=1.2)

        self.until("oneway_arrow")
        self.play(Create(arrow_out), FadeIn(follower_card), run_time=0.8)

        self.until("no_return_cross")
        self.play(FadeIn(cross_ret), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S13
class EP04_S13(_E04):
    SHOT = "EP04-S13"

    def construct(self):
        head = self.fit_left_of_tags(header("C++ Scheduler 与释放 GIL", "EP04 · S13 调度核心"))
        self.add(head)

        code = code_panel("py::tuple Scheduler::schedule(SequenceMetadataPool *pool) {\n    py::gil_scoped_release release; // 释放 Python 全局解释器锁!\n    auto p_scheduler_outputs = _schedule();\n    for (size_t i = 0; i < scheduled_seqs.size(); ++i) {\n        seq_metadata_list[i] = pool->allocate(seq, ...);\n    }\n    return py::make_tuple(seq_metadata_list, p_scheduler_outputs);\n}",
                          "csrc/engine/scheduler.hpp", highlight=[2, 5], size=16).move_to([-2.6, -0.2, 0])

        box_gil = Block("GIL 锁状态: 已释放 (UNLOCKED)\n• 后台通信不受阻塞\n• 无 GC 垃圾回收暂停", color=KV, w=4.5, h=1.4, size=16).move_to([3.6, 0.6, 0])
        box_pool = Block("SequenceMetadataPool\n• C++ 静态预分配对象池\n• 消除单步数百对象创建开销", color=DECODE, w=4.5, h=1.4, size=16).move_to([3.6, -1.0, 0])

        self.play(FadeIn(code), run_time=0.8)

        self.until("enter_step")
        self.play(Indicate(code, color=DECODE), run_time=0.8)

        self.until("enter_cpp")
        self.play(FadeIn(box_gil), run_time=0.8)

        self.until("release_gil")
        self.play(Indicate(box_gil, color=KV), run_time=0.8)

        self.until("pack_outputs")
        self.play(FadeIn(box_pool), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S14
class EP04_S14(_E04):
    SHOT = "EP04-S14"

    def construct(self):
        head = self.fit_left_of_tags(header("DP 投票与防止 EP 死锁", "EP04 · S14 步型仲裁"))
        self.add(head)

        q_pill = Pill("Q：为什么各卡不能各顾各，想做预填就做预填？", WARN, size=20).move_to([0, 1.55, 0])

        ranks = VGroup(
            Block("DP Rank 0\n(想做 Prefill)", color=PREFILL, w=2.4, h=1.4, size=16),
            Block("DP Rank 1\n(想做 Decode)", color=DECODE, w=2.4, h=1.4, size=16),
            Block("DP Rank 2\n(想做 Decode)", color=DECODE, w=2.4, h=1.4, size=16),
            Block("DP Rank 3\n(想做 Decode)", color=DECODE, w=2.4, h=1.4, size=16),
        ).arrange(RIGHT, buff=0.35).move_to([0, 0.45, 0])

        vote_box = Block("全规约投票: _dp_allreduce(want_prefill ? 1 : 0, MIN)\n强制全组统一步调 · 消除 MoE 专家并行 All-to-All 死锁",
                         color=WARN, w=10.5, h=1.1, size=16).move_to([0, -0.85, 0])

        result_pill = Pill("裁决结果: 全组统一执行 DECODE (0 号卡顺延预填)", KV, size=18).move_to([0, -1.8, 0])

        self.play(FadeIn(q_pill), run_time=0.6)

        self.until("vote_trigger")
        self.play(FadeIn(ranks), run_time=0.8)

        self.until("q_why_vote")
        self.play(Indicate(ranks[0], color=WARN), run_time=0.8)

        self.until("deadlock_warn")
        self.play(FadeIn(vote_box), run_time=0.8)

        self.until("vote_grid")
        self.play(FadeIn(result_pill), ranks[0].animate.set_color(DECODE), run_time=1.0)

        self.finish()


# ---------------------------------------------------------------- S15
class EP04_S15(_E04):
    SHOT = "EP04-S15"

    def construct(self):
        head = self.fit_left_of_tags(header("空闲 Rank 为什么必须跟跑？", "EP04 · S15 陪跑步机制"))
        self.add(head)

        cards = VGroup(
            Block("GPU 0 (有效请求 A)", color=KV, w=2.6, h=1.5, size=16),
            Block("GPU 1 (有效请求 B)", color=KV, w=2.6, h=1.5, size=16),
            Block("GPU 2 (有效请求 C)", color=KV, w=2.6, h=1.5, size=16),
            Block("GPU 3 (无就绪请求!)", color=WARN, w=2.6, h=1.5, size=16),
        ).arrange(RIGHT, buff=0.3).move_to([0, 0.7, 0])

        mesh = VGroup()
        for i in range(4):
            for j in range(i + 1, 4):
                mesh.add(Line(cards[i].get_bottom(), cards[j].get_bottom(), color=MUTED, stroke_width=1.2))

        b_placeholder = Block("强行注入: _placeholder_seq_metadata (陪跑步)\n• 长度 1 token · 虚拟计算 · 丢弃输出\n• 唯一目的: 参与 EP 专家交换，保持 All-to-All 网络拓扑同步",
                              color=EXPERT, w=10.5, h=1.5, size=16).move_to([0, -1.2, 0])

        self.play(FadeIn(cards), run_time=0.8)

        self.until("idle_problem")
        self.play(Indicate(cards[3], color=WARN), run_time=0.8)

        self.until("placeholder_inject")
        self.play(Create(mesh), run_time=1.0)

        self.until("sync_exchange")
        self.play(FadeIn(b_placeholder), cards[3].animate.set_color(EXPERT), run_time=1.0)

        self.finish()


# ---------------------------------------------------------------- S16
class EP04_S16(_E04):
    SHOT = "EP04-S16"

    def construct(self):
        head = self.fit_left_of_tags(header("Forward(N) 与 Post-process(N-1)", "EP04 · S16 错步重叠"))
        self.add(head)

        tline = Timeline(["GPU 侧 (计算密集)", "CPU 侧 (调度掩盖)"], width=10.5, lane_h=1.0, scale=0.9).move_to([0, 0.4, 0])

        b_fwd = tline.bar(0, 1.0, 4.5, "Forward(N) 模型前向计算", color=GPU)
        b_post_prev = tline.bar(1, 1.2, 2.5, "Post(N-1) 上步后处理", color=CPU)
        b_sample = tline.bar(0, 5.8, 1.8, "Sample(N) 采样", color=DECODE)
        b_defer = tline.bar(1, 6.0, 3.5, "Post(N) 推迟至下步 Forward...", color=MUTED)

        overlap_box = SurroundingRectangle(VGroup(b_fwd, b_post_prev), color=KV, stroke_width=2, buff=0.1)
        overlap_tag = Pill("计算与传输重叠: D2H 延迟被前向时间彻底吸收", KV, size=18).move_to([0, -1.8, 0])

        self.play(FadeIn(tline), run_time=0.8)

        self.until("exec_order_flow")
        self.play(FadeIn(b_fwd), run_time=0.6)

        self.until("step1_fwd")
        self.play(FadeIn(b_post_prev), Create(overlap_box), run_time=0.8)

        self.until("step2_post_prev")
        self.play(FadeIn(b_sample), run_time=0.6)

        self.until("step3_sample")
        self.play(FadeIn(b_defer), run_time=0.6)

        self.until("step4_defer")
        self.play(FadeIn(overlap_tag), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S17
class EP04_S17(_E04):
    SHOT = "EP04-S17"

    def construct(self):
        head = self.fit_left_of_tags(header("乐观推进与事后真实回填", "EP04 · S17 账本推演"))
        self.add(head)

        q_pill = Pill("Q：后处理推迟了一步，调度器怎么知道为下个周期准备多少显存？", WARN, size=20).move_to([0, 1.55, 0])

        b_base = Rectangle(width=2.5, height=1.6, fill_color=DECODE, fill_opacity=0.8, stroke_color=DECODE).move_to([-3.0, -0.6, 0])
        t_base = T("真实确认 Token\n(commit: 120)", 16, FG).move_to(b_base.get_center())

        b_optimistic = Rectangle(width=2.5, height=1.0, fill_color=WARN, fill_opacity=0.4, stroke_color=WARN, stroke_width=2).move_to([-3.0, 0.7, 0])
        t_opt = T("乐观推进 +5\n(advance_optimistically)", 16, WARN).move_to(b_optimistic.get_center())

        card_logic = Block("账本结算机制:\n1. 调度时假设投机 Draft 全部被接受 (预占块)\n2. 真实采样出来后按接受数回填 (commit_processed)\n3. 差额计入 total_inflight_tokens 动态归还",
                           color=FG, w=6.0, h=2.2, size=16).move_to([3.0, -0.1, 0])

        offset_pill = Pill("优化精髓: C++ 只算 offset 和 len，展平留给 GPU 前向", KV, size=18).move_to([0, -2.0, 0])

        self.play(FadeIn(q_pill), run_time=0.6)

        self.until("q_how_ledger")
        self.play(FadeIn(b_base), FadeIn(t_base), FadeIn(card_logic), run_time=0.8)

        self.until("optimistic_advance")
        self.play(FadeIn(b_optimistic), FadeIn(t_opt), run_time=0.8)

        self.until("commit_backfill")
        self.play(Indicate(b_optimistic, color=KV), FadeIn(offset_pill), run_time=1.0)

        self.finish()


# ---------------------------------------------------------------- S18
class EP04_S18(_E04):
    SHOT = "EP04-S18"

    def construct(self):
        head = self.fit_left_of_tags(header("CUDA Graph 阶梯分桶与 Eager 模式", "EP04 · S18 图捕获"))
        self.add(head)

        buckets = [1, 2, 4, 8, 16, 24]
        bars = VGroup()
        for i, b in enumerate(buckets):
            h = 0.4 + (i * 0.4)
            r = RoundedRectangle(width=1.0, height=h, corner_radius=0.08, stroke_color=DECODE, stroke_width=1.5,
                                 fill_color=DECODE, fill_opacity=0.35).move_to([-4.5 + i * 1.5, -1.0 + h/2, 0])
            lbl = T(f"B={b}", 16, FG).move_to([-4.5 + i * 1.5, -1.3, 0])
            bars.add(VGroup(r, lbl))

        query_card = Block("当前输入: total_q = 12 tokens\n二分向上查找 (bisect_left) → 命中桶 B=16\n填充 4 个占位 padding 序列对齐",
                           color=WARN, w=6.5, h=1.5, size=16).move_to([0, 1.25, 0])

        pill_scope = Pill("执行分流: Decode 主模型走静态 Graph 重放；Prefill 与 Sampler 走 Eager 发射", KV, size=18).move_to([0, -2.1, 0])

        self.play(FadeIn(bars), run_time=1.0)

        self.until("cudagraph_reveal")
        self.play(FadeIn(query_card), run_time=0.8)

        self.until("graph_scope")
        self.play(Indicate(bars[4], color=WARN), run_time=0.8)

        self.until("bucket_steps")
        self.play(Indicate(bars[0], color=DECODE), Indicate(bars[1], color=DECODE), run_time=0.8)

        self.until("bisect_match")
        self.play(FadeIn(pill_scope), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S19
class EP04_S19(_E04):
    SHOT = "EP04-S19"

    def construct(self):
        head = self.fit_left_of_tags(header("Driver 独占采样与 C++ 对象池", "EP04 · S19 输出汇聚"))
        self.add(head)

        box_driver = Block("Driver (卡0)\n独占 Sampler\n产生采样 Token", color=DECODE, w=3.4, h=2.2, size=16).move_to([-3.6, 0.4, 0])
        box_worker = Block("Follower Worker (卡1-3)\n返回空 SamplerOutput\n(零采样同步开销!)", color=MUTED, w=3.4, h=2.2, size=16).move_to([-3.6, -1.35, 0])

        b_pool = Block("RequestOutputPool (C++ 静态内存池)\n• outputs.hpp: static std::vector<uint64_t>\n• 返回 uint64 内存指针数组至 Python\n• Python 仅在 step() 内通过 clone() 提取",
                       color=KV, w=6.4, h=2.5, size=16).move_to([3.1, -0.1, 0])

        arr1 = Arrow(box_driver.get_right(), b_pool.get_left(), color=DECODE, buff=0.1)

        pill_gc = Pill("核心价值: 静态借用消除每步分配，彻底消灭 GC 压力", PREFILL, size=18).move_to([0, -2.1, 0])

        self.play(FadeIn(box_driver), FadeIn(box_worker), run_time=0.8)

        self.until("sampler_diverge")
        self.play(Indicate(box_worker, color=MUTED), run_time=0.8)

        self.until("driver_sampler")
        self.play(Create(arr1), FadeIn(b_pool), run_time=0.8)

        self.until("static_pool")
        self.play(Indicate(b_pool, color=KV), run_time=0.8)

        self.until("clone_output")
        self.play(FadeIn(pill_gc), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S20
class EP04_S20(_E04):
    SHOT = "EP04-S20"

    def construct(self):
        head = self.fit_left_of_tags(header("platform.py 与顶层导包铁律", "EP04 · S20 平台切换"))
        self.add(head)

        hub = Block("platform.py\n硬件探测与抽象", color=FG, w=3.2, h=1.4, size=18).move_to([0, 0.6, 0])

        b_cuda = Block("PlatformGPU\ntilelang_ops_backend = 'cuda'\nNCCL 通信 / CUDA Graph", color=DECODE, w=4.5, h=1.6, size=16).move_to([-3.4, -0.85, 0])
        b_asc = Block("PlatformNPU\ntilelang_ops_backend = 'asc'\nHCCL 通信 / NPU Eager", color=PREFILL, w=4.5, h=1.6, size=16).move_to([3.4, -0.85, 0])

        arr_l = Arrow(hub.get_bottom(), b_cuda.get_top(), color=DECODE, buff=0.1)
        arr_r = Arrow(hub.get_bottom(), b_asc.get_top(), color=PREFILL, buff=0.1)

        pill_so = Pill("动态软链: deepinfer/_so/<tag>/ 分离归档，单代码树双平台共存", KV, size=18).move_to([0, 1.55, 0])
        pill_guard = Pill("顶层铁律: 严禁 import torch，捍卫多进程隔离底线", WARN, size=18).move_to([0, -2.1, 0])

        self.play(FadeIn(hub), FadeIn(pill_so), run_time=0.8)

        self.until("platform_hub")
        self.play(Create(arr_l), FadeIn(b_cuda), run_time=0.8)

        self.until("platform_split")
        self.play(Create(arr_r), FadeIn(b_asc), run_time=0.8)

        self.until("so_linking")
        self.play(Indicate(pill_so, color=KV), run_time=0.8)

        self.until("strict_init")
        self.play(FadeIn(pill_guard), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S21
class EP04_S21(_E04):
    SHOT = "EP04-S21"

    def construct(self):
        head = self.fit_left_of_tags(header("三句话与请求在代码里的一生", "EP04 · S21 总结预告"))
        self.add(head)

        c1 = Block("1. 三层架构 · C++调度下沉释放GIL，算子层占近半壁", color=DECODE, w=10.0, h=0.85, size=18).move_to([0, 1.15, 0])
        c2 = Block("2. 多卡无TP · 10×1MB 单向SHM广播，Driver 独占采样", color=PREFILL, w=10.0, h=0.85, size=18).move_to([0, 0.15, 0])
        c3 = Block("3. 错步流水 · DP 投票防死锁，空闲卡强行占位陪跑", color=KV, w=10.0, h=0.85, size=18).move_to([0, -0.85, 0])

        next_card = Block("下集预告: EP05 调度：让 GPU 一刻不停 (ZOS 异步调度解密)", color=WARN, w=10.0, h=0.75, size=18).move_to([0, -1.85, 0])

        self.until("recap_1")
        self.play(FadeIn(c1), run_time=0.8)

        self.until("recap_2")
        self.play(FadeIn(c2), run_time=0.8)

        self.until("recap_3")
        self.play(FadeIn(c3), run_time=0.8)

        self.play(FadeIn(next_card), run_time=0.8)

        self.finish()
