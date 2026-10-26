"""EP01 scenes: 推理引擎到底在忙什么 (shots S01-S19)."""
from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path for manim_lib imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import (
    DOWN, LEFT, RIGHT, UP, UL, UR, DL, DR, ORIGIN,
    FadeIn, FadeOut, Create, Write, Transform, Indicate,
    Line, Arrow, Rectangle, RoundedRectangle, VGroup, Circle, Polygon, DashedLine,
)
from manim_lib.dvlib import (
    BG, FG, MUTED, GRID, PREFILL, DECODE, KV, SWA, WARN, EXPERT, DRAFT, GPU, CPU,
    GRADE_COLORS, Pill, DVScene, header, MiniMap, Block, TokenRow, window_bracket,
    code_panel, number_card, LayerStack, AttentionMatrix, Scale, T, M,
)


class EP01_S01(DVScene):
    SHOT = "EP01-S01"

    def construct(self):
        head = self.fit_left_of_tags(header("发呆的顶级加速卡", "EP01 · S01 冷开场"))
        self.add(head)

        # GPU frame container
        gpu_box = RoundedRectangle(corner_radius=0.15, width=5.6, height=3.6,
                                   stroke_color=GRID, stroke_width=2, fill_opacity=0)
        gpu_box.move_to([-2.2, -0.4, 0])
        gpu_title = T("加速卡 · 1000 TFLOPS", 18, MUTED).next_to(gpu_box.get_top(), DOWN, buff=0.18)

        # 3x4 Core grid inside GPU
        cores = VGroup()
        for r in range(3):
            row = VGroup()
            for c in range(4):
                core = RoundedRectangle(corner_radius=0.06, width=1.05, height=0.5,
                                        stroke_color=GRID, stroke_width=1.5, fill_color="#1E232D", fill_opacity=0.8)
                txt = T(f"C{r*4+c}", 16, MUTED).move_to(core)
                row.add(VGroup(core, txt))
            row.arrange(RIGHT, buff=0.15)
            cores.add(row)
        cores.arrange(DOWN, buff=0.12).move_to([-2.2, 0.12, 0])

        # HBM memory block below
        hbm_box = RoundedRectangle(corner_radius=0.1, width=5.0, height=0.65,
                                   stroke_color=DECODE, stroke_width=2, fill_color="#162235", fill_opacity=0.9)
        hbm_box.move_to([-2.2, -1.6, 0])
        hbm_txt = T("HBM3e 显存总线 (3.2 TB/s)", 18, DECODE).move_to(hbm_box)
        hbm_group = VGroup(hbm_box, hbm_txt)

        gpu_visual = VGroup(gpu_box, gpu_title, cores, hbm_group)
        self.play(FadeIn(gpu_visual), run_time=0.9)

        self.until("gpu")
        self.play(gpu_box.animate.set_stroke(DECODE, 2.5), run_time=0.6)

        self.until("idle")
        c1 = number_card(">1000", "TFLOPS", "峰值算力超千TFLOPS", color=PREFILL).move_to([3.6, 0.6, 0])
        c2 = number_card(">99%", "核心空转", "解码单字空转超99%", color=WARN).move_to([3.6, -1.2, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.8)

        self.until("myth")
        bus_tag = Pill("显存带宽传输受限", WARN, size=16).move_to([-2.2, -0.95, 0])
        self.play(FadeIn(bus_tag), run_time=0.6)

        self.until("wait")
        self.play(Indicate(c2), run_time=0.7)

        self.finish()


class EP01_S02(DVScene):
    SHOT = "EP01-S02"

    def construct(self):
        ep_tag = T("EP01 · 通用基座", 48, DECODE).move_to([0, 1.2, 0])
        title = T("推理引擎到底在忙什么", 36, FG).next_to(ep_tag, DOWN, buff=0.35)
        mmap = MiniMap(active="入口", scale=1.05).next_to(title, DOWN, buff=0.8)

        self.play(FadeIn(ep_tag), FadeIn(title), run_time=0.8)

        self.until("title")
        self.play(FadeIn(mmap), run_time=0.8)

        self.finish()


class EP01_S03(DVScene):
    SHOT = "EP01-S03"

    def construct(self):
        head = self.fit_left_of_tags(header("从单次运行到海量并发", "EP01 · S03 规模鸿沟"))
        self.add(head)

        # Left: Local code snippet
        left_box = RoundedRectangle(corner_radius=0.15, width=5.2, height=3.6,
                                    stroke_color=GRID, stroke_width=2, fill_color="#13171F", fill_opacity=0.9)
        left_box.move_to([-3.2, -0.5, 0])
        l_tag = Pill("本地脚本 · 极简前向", KV, size=16).next_to(left_box.get_top(), DOWN, buff=0.2)
        code_lines = VGroup(
            T("import torch", 16, MUTED),
            T("model = load_model()", 16, FG),
            T("out = model.generate(input)", 16, DECODE),
            T("# 单次运行：几毫秒搞定", 16, KV),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(l_tag, DOWN, buff=0.3)
        left_group = VGroup(left_box, l_tag, code_lines)

        # Right: Cloud cluster cards (without double background)
        r_card = number_card("155万亿", "token/天", "日服务155万亿token", color=WARN).move_to([3.4, 0.4, 0])
        r_box = RoundedRectangle(corner_radius=0.15, width=4.8, height=1.6,
                                 stroke_color=WARN, stroke_width=1.5, fill_color="#1F1616", fill_opacity=0.9).move_to([3.4, -1.4, 0])
        r_txt = T("生产环境必须跨越物理瓶颈\n单机简单循环将瞬间耗尽显存", 16, FG).move_to(r_box)
        right_group = VGroup(r_card, r_box, r_txt)

        self.play(FadeIn(left_group), run_time=0.8)

        self.until("script")
        self.play(Indicate(code_lines[2]), run_time=0.6)

        self.until("local")
        self.play(left_box.animate.set_stroke(KV, 2.5), run_time=0.6)

        self.until("scale")
        self.play(FadeIn(right_group), run_time=0.8)

        self.until("cluster")
        self.play(Indicate(r_card), run_time=0.6)

        self.until("split")
        wall_tag = Pill("两道物理高墙：算力墙 · 带宽墙", WARN, size=18).move_to([0, -2.4, 0])
        self.play(FadeIn(wall_tag), run_time=0.8)

        self.until("engine")
        self.play(wall_tag.animate.scale(1.05), run_time=0.5)

        self.finish()


class EP01_S04(DVScene):
    SHOT = "EP01-S04"

    def construct(self):
        head = self.fit_left_of_tags(header("预填充与自回归解码", "EP01 · S04 阶段划分"))
        self.add(head)

        # Left Prefill block
        p_box = RoundedRectangle(corner_radius=0.15, width=5.2, height=3.4,
                                 stroke_color=PREFILL, stroke_width=2, fill_opacity=0)
        p_box.move_to([-3.2, -0.5, 0])
        p_title = T("阶段一：预填充 (Prefill)", 20, PREFILL).next_to(p_box.get_top(), DOWN, buff=0.2)
        p_desc = T("输入 Prompt 一次性计算\n产出初始 KV · 算力受限", 18, FG).next_to(p_title, DOWN, buff=0.25)
        p_tokens = TokenRow(8, color=PREFILL, size=0.35).next_to(p_desc, DOWN, buff=0.3)
        p_group = VGroup(p_box, p_title, p_desc, p_tokens)

        # Right Decode block
        d_box = RoundedRectangle(corner_radius=0.15, width=5.2, height=3.4,
                                 stroke_color=DECODE, stroke_width=2, fill_opacity=0)
        d_box.move_to([3.2, -0.5, 0])
        d_title = T("阶段二：解码 (Decode)", 20, DECODE).next_to(d_box.get_top(), DOWN, buff=0.2)
        d_desc = T("逐步生成单个新 Token\n读历史 KV · 带宽受限", 18, FG).next_to(d_title, DOWN, buff=0.25)
        d_tok = Block("Token[t+1]", color=DECODE, w=2.6, h=0.6, size=18).next_to(d_desc, DOWN, buff=0.3)
        d_group = VGroup(d_box, d_title, d_desc, d_tok)

        self.play(FadeIn(p_group), run_time=0.8)

        self.until("twostage")
        self.play(FadeIn(d_group), run_time=0.8)

        self.until("prompt")
        self.play(Indicate(p_tokens), run_time=0.6)

        self.until("calc")
        p_badge = Pill("首词产出 + KV写入", KV, size=16).next_to(p_tokens, DOWN, buff=0.2)
        self.play(FadeIn(p_badge), run_time=0.6)

        self.until("decode")
        arrow = Arrow([-0.6, -0.6, 0], [0.6, -0.6, 0], color=FG, stroke_width=3)
        self.play(Create(arrow), Indicate(d_tok), run_time=0.7)

        self.until("reason")
        tag_conflict = Pill("相反物理特征：高强度矩阵 vs 访存搬运", EXPERT, size=16).move_to([0, -2.4, 0])
        self.play(FadeIn(tag_conflict), run_time=0.7)

        self.finish()


class EP01_S05(DVScene):
    SHOT = "EP01-S05"

    def construct(self):
        head = self.fit_left_of_tags(header("算力受限的密集运算", "EP01 · S05 预填充阶段"))
        self.add(head)

        # Left: Dense GEMM matrix illustration
        gemm_box = RoundedRectangle(corner_radius=0.15, width=5.4, height=3.6,
                                    stroke_color=PREFILL, stroke_width=2, fill_color="#211717", fill_opacity=0.9)
        gemm_box.move_to([-3.2, -0.6, 0])
        g_title = T("密集矩阵乘 (Dense GEMM)", 20, PREFILL).next_to(gemm_box.get_top(), DOWN, buff=0.2)
        m_q = RoundedRectangle(corner_radius=0.08, width=1.8, height=1.6, color=PREFILL, fill_opacity=0.4).move_to([-4.4, -0.7, 0])
        m_k = RoundedRectangle(corner_radius=0.08, width=1.8, height=1.6, color=DECODE, fill_opacity=0.4).move_to([-2.0, -0.7, 0])
        q_txt = T("Prompt\n(4096, D)", 16, FG).move_to(m_q)
        k_txt = T("Weights\n(D, D)", 16, FG).move_to(m_k)
        g_math = T("大矩阵并行计算 · 核心全速运转", 16, KV).next_to(gemm_box.get_bottom(), UP, buff=0.25)
        gemm_visual = VGroup(gemm_box, g_title, m_q, m_k, q_txt, k_txt, g_math)

        # Right: Roofline indicator and numbers
        right_box = RoundedRectangle(corner_radius=0.15, width=5.2, height=3.6,
                                     stroke_color=GRID, stroke_width=2, fill_color="#13171F", fill_opacity=0.9)
        right_box.move_to([3.2, -0.6, 0])
        c_intensity = number_card("8,192", "FLOP/Byte", "算术强度超8000FLOP/B", color=KV).move_to([3.2, 0.4, 0])
        c_status = Pill("状态：计算受限 (Compute-bound)", PREFILL, size=18).move_to([3.2, -1.0, 0])
        c_note = T("远超 Roofline 拐点 (312.5 FLOP/B)", 16, MUTED).move_to([3.2, -1.7, 0])
        right_visual = VGroup(right_box, c_intensity, c_status, c_note)

        self.play(FadeIn(gemm_visual), run_time=0.8)

        self.until("tokens")
        self.play(Indicate(m_q), run_time=0.6)

        self.until("gemm")
        self.play(Indicate(m_k), run_time=0.6)

        self.until("example")
        self.play(FadeIn(right_visual), run_time=0.8)

        self.until("roofline")
        self.play(Indicate(c_intensity), run_time=0.7)

        self.finish()


class EP01_S06(DVScene):
    SHOT = "EP01-S06"

    def construct(self):
        head = self.fit_left_of_tags(header("带宽受限的漫长搬运", "EP01 · S06 解码阶段"))
        self.add(head)

        # Memory bus animation layout
        hbm_block = Block("HBM 显存: 16 GB 权重", color=EXPERT, w=4.0, h=1.0, size=18, sub="FP8 模型激活权重").move_to([-3.6, 0.5, 0])
        core_block = Block("GPU 计算核心: GEMV", color=MUTED, w=4.0, h=1.0, size=18, sub="单向量乘法耗时仅微秒").move_to([3.6, 0.5, 0])
        bus_arrow = Arrow([-1.5, 0.5, 0], [1.5, 0.5, 0], color=WARN, stroke_width=4)
        bus_label = T("3.2 TB/s 传输总线 (5.0 ms)", 16, WARN).next_to(bus_arrow, UP, buff=0.15)

        # Bottom comparison timeline
        time_box = RoundedRectangle(corner_radius=0.15, width=9.6, height=1.6,
                                    stroke_color=GRID, stroke_width=1.5, fill_color="#141822", fill_opacity=0.9)
        time_box.move_to([0, -1.6, 0])
        t_title = T("单步耗时结构对比", 16, MUTED).next_to(time_box.get_top(), DOWN, buff=0.15)
        bar_mem = RoundedRectangle(corner_radius=0.08, width=7.6, height=0.45, color=WARN, fill_opacity=0.7).move_to([-0.6, -1.8, 0])
        lbl_mem = T("显存搬运权重: ~5.0 ms (99.4%)", 16, FG).move_to(bar_mem)
        bar_compute = RoundedRectangle(corner_radius=0.05, width=0.4, height=0.45, color=KV, fill_opacity=0.9).next_to(bar_mem, RIGHT, buff=0.1)
        lbl_c = T("算力: 0.032ms", 16, KV).next_to(bar_compute, UP, buff=0.1)
        time_group = VGroup(time_box, t_title, bar_mem, lbl_mem, bar_compute, lbl_c)

        self.play(FadeIn(hbm_block), FadeIn(core_block), run_time=0.8)

        self.until("switch")
        self.play(Create(bus_arrow), FadeIn(bus_label), run_time=0.7)

        self.until("single")
        in_tok = Pill("当前输入：仅 1 个 token", DECODE, size=16).move_to([3.6, 1.4, 0])
        self.play(FadeIn(in_tok), run_time=0.6)

        self.until("weight")
        self.play(Indicate(hbm_block), run_time=0.6)

        self.until("read")
        self.play(FadeIn(time_group), run_time=0.8)

        self.until("fast")
        self.play(Indicate(bar_compute), run_time=0.6)

        self.finish()


class EP01_S07(DVScene):
    SHOT = "EP01-S07"

    def construct(self):
        head = self.fit_left_of_tags(header("单请求下的荒谬现实", "EP01 · S07 算力天平"))
        self.add(head)

        scale = Scale("权重 16 GB", "计算 32 GFLOP", left_color=WARN, right_color=DECODE, w=6.4, h=2.2, size=20)
        scale.move_to([0, 0.9, 0])

        card_mem = number_card("5.0", "ms", "权重访存5.0ms (16GB)", color=WARN).move_to([-3.4, -1.6, 0])
        card_calc = number_card("0.032", "ms", "算力耗时0.032ms (32GFLOP)", color=DECODE).move_to([0, -1.6, 0])
        card_int = number_card("2.0", "FLOP/B", "算术强度仅2.0 FLOP/Byte", color=WARN).move_to([3.4, -1.6, 0])

        self.play(FadeIn(scale), run_time=0.8)

        self.until("model")
        self.play(
            scale.beam.animate.rotate(0.18),
            scale.left_pan.animate.shift(DOWN * 0.45),
            scale.right_pan.animate.shift(UP * 0.45),
            run_time=0.8
        )

        self.until("params")
        self.play(Indicate(scale.left_pan), run_time=0.6)

        self.until("bytes")
        self.play(FadeIn(card_mem), run_time=0.6)

        self.until("flops")
        self.play(FadeIn(card_calc), run_time=0.6)

        self.until("compute")
        self.play(Indicate(card_calc), run_time=0.6)

        self.until("memory")
        self.play(Indicate(card_mem), run_time=0.6)

        self.until("answer")
        self.play(FadeIn(card_int), run_time=0.8)

        self.finish()


class EP01_S08(DVScene):
    SHOT = "EP01-S08"

    def construct(self):
        head = self.fit_left_of_tags(header("批处理的均摊艺术", "EP01 · S08 破局之道"))
        self.add(head)

        w_bar = RoundedRectangle(corner_radius=0.1, width=10.4, height=0.7,
                                 color=EXPERT, fill_opacity=0.3, stroke_width=2).move_to([0, 1.3, 0])
        w_lbl = T("16 GB 权重单次搬运流 (耗时 ~5.0 ms)", 18, EXPERT).move_to(w_bar)
        top_group = VGroup(w_bar, w_lbl)

        # 4 rows of 16 tokens
        slots = VGroup()
        for r in range(4):
            row = VGroup()
            for c in range(16):
                cell = RoundedRectangle(corner_radius=0.04, width=0.55, height=0.32,
                                        color=DECODE, fill_opacity=0.6, stroke_width=1)
                row.add(cell)
            row.arrange(RIGHT, buff=0.08)
            slots.add(row)
        slots.arrange(DOWN, buff=0.08).move_to([0, 0.05, 0])

        c_batch = number_card("64", "并发", "Batch从1到64：权重读一次", color=DECODE, backdrop=False).move_to([-3.8, -1.6, 0])
        c_inten = number_card("128", "FLOP/B", "算术强度飙升至128 FLOP/B", color=KV, backdrop=False).move_to([0, -1.6, 0])
        c_util = number_card("40.8%", "利用率", "利用率飙升·单字成本暴降", color=KV, backdrop=False).move_to([3.8, -1.6, 0])

        self.play(FadeIn(top_group), run_time=0.8)

        self.until("batch")
        self.play(FadeIn(slots), run_time=0.8)

        self.until("sixtyfour")
        self.play(Indicate(slots), run_time=0.6)

        self.until("stream")
        arrows = VGroup(*[Arrow([x, 0.95, 0], [x, 0.45, 0], color=EXPERT, stroke_width=2)
                          for x in [-4.0, -1.5, 1.5, 4.0]])
        self.play(Create(arrows), run_time=0.7)

        self.until("share")
        self.play(FadeIn(c_batch), FadeIn(c_inten), run_time=0.7)

        self.until("intensity")
        self.play(FadeIn(c_util), run_time=0.7)

        self.finish()


class EP01_S09(DVScene):
    SHOT = "EP01-S09"

    def construct(self):
        head = self.fit_left_of_tags(header("批处理成本自测", "EP01 · S09 暂停题"))
        self.add(head)

        q_box = RoundedRectangle(corner_radius=0.15, width=9.8, height=3.6,
                                 stroke_color=DECODE, stroke_width=2, fill_color="#121824", fill_opacity=0.95)
        q_box.move_to([0, -0.6, 0])

        q_tag = Pill("自测题 · 暂停思考", EXPERT, size=18).next_to(q_box.get_top(), DOWN, buff=0.25)
        q_txt = T("解码时把批大小从 1 扩大到 64，\n每个词的生成成本为什么会大幅下降？", 22, FG).next_to(q_tag, DOWN, buff=0.3)

        self.play(FadeIn(q_box), FadeIn(q_tag), FadeIn(q_txt), run_time=0.8)

        self.until("timer")
        a_box = RoundedRectangle(corner_radius=0.1, width=8.6, height=1.3,
                                 stroke_color=KV, stroke_width=2, fill_color="#16261A", fill_opacity=0.9)
        a_box.move_to([0, -1.5, 0])
        a_txt = T("核心解答：解码受限于显存带宽！\n16 GB 权重单次搬运耗时(~5ms)不变，同时服务 64 路计算，\n均摊了固定访存开销，单字成本骤降 64 倍。",
                  18, FG).move_to(a_box)
        ans_group = VGroup(a_box, a_txt)
        self.play(FadeIn(ans_group), run_time=0.8)

        self.until("reveal")
        self.play(Indicate(a_box), run_time=0.7)

        self.until("done")
        self.play(ans_group.animate.set_stroke(KV, 3), run_time=0.5)

        self.finish()


class EP01_S10(DVScene):
    SHOT = "EP01-S10"

    def construct(self):
        head = self.fit_left_of_tags(header("KV Cache 的膨胀", "EP01 · S10 资源硬约束"))
        self.add(head)

        left_box = RoundedRectangle(corner_radius=0.15, width=5.4, height=3.6,
                                    stroke_color=GRID, stroke_width=1.5, fill_color="#13171F", fill_opacity=0.9)
        left_box.move_to([-3.2, -0.6, 0])
        l_title = T("自回归历史注意力依赖", 18, MUTED).next_to(left_box.get_top(), DOWN, buff=0.2)
        row = TokenRow(6, color=DECODE, size=0.35).next_to(l_title, DOWN, buff=0.3)
        new_tok = Block("Token[t]", color=PREFILL, w=1.6, h=0.5, size=16).next_to(row, DOWN, buff=0.35)
        attn_arc = Arrow(new_tok.get_top(), row.get_center(), color=KV, stroke_width=2)
        l_sub = T("避免每步二次重算历史状态", 16, KV).next_to(new_tok, DOWN, buff=0.2)
        left_visual = VGroup(left_box, l_title, row, new_tok, attn_arc, l_sub)

        # Right side cards
        c_kv = number_card("O(B × L)", "线性增长", "显存占用随长度并发膨胀", color=WARN, backdrop=False).move_to([3.2, 0.4, 0])
        r_box = RoundedRectangle(corner_radius=0.1, width=4.8, height=1.4,
                                 stroke_color=WARN, stroke_width=1.5, fill_color="#1E1616", fill_opacity=0.9).move_to([3.2, -1.3, 0])
        r_desc = T("长文本下 KV 显存远超模型权重\n成为单机并发容量第一瓶颈", 16, FG).move_to(r_box)
        right_visual = VGroup(c_kv, r_box, r_desc)

        self.play(FadeIn(left_visual), run_time=0.8)

        self.until("limit")
        self.play(FadeIn(right_visual), run_time=0.8)

        self.until("attn")
        self.play(Indicate(attn_arc), run_time=0.6)

        self.until("store")
        self.play(row.animate.set_stroke(KV, 2.5), run_time=0.6)

        self.until("kv")
        self.play(Indicate(c_kv), run_time=0.6)

        self.until("burst")
        self.play(r_box.animate.set_stroke(WARN, 3), run_time=0.6)

        self.until("huge")
        self.play(Indicate(r_desc), run_time=0.6)

        self.finish()


class EP01_S11(DVScene):
    SHOT = "EP01-S11"

    def construct(self):
        head = self.fit_left_of_tags(header("静态批处理的木桶短板", "EP01 · S11 调度进化"))
        self.add(head)

        grid_box = RoundedRectangle(corner_radius=0.15, width=9.8, height=3.6,
                                    stroke_color=GRID, stroke_width=1.5, fill_opacity=0)
        grid_box.move_to([0, -0.6, 0])
        g_title = T("静态批处理 (Static Batching)：同进同出", 18, MUTED).next_to(grid_box.get_top(), DOWN, buff=0.15)

        bars = VGroup()
        configs = [
            (2.8, 4.4, "Req 1: 300 token (结束早)"),
            (6.8, 0.4, "Req 2: 2000 token (最长木桶)"),
            (3.8, 3.4, "Req 3: 500 token"),
            (1.6, 5.6, "Req 4: 50 token (极短)"),
        ]
        for w_act, w_bub, desc in configs:
            row_g = VGroup()
            lbl = T(desc, 16, FG)
            act = RoundedRectangle(corner_radius=0.06, width=w_act, height=0.4, color=DECODE, fill_opacity=0.8)
            bub = RoundedRectangle(corner_radius=0.06, width=w_bub, height=0.4, color=MUTED, fill_opacity=0.25, stroke_width=1)
            pair = VGroup(act, bub).arrange(RIGHT, buff=0.05)
            row_g.add(lbl, pair).arrange(RIGHT, buff=0.25)
            bars.add(row_g)
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, -0.6, 0])

        self.play(FadeIn(grid_box), FadeIn(g_title), FadeIn(bars), run_time=0.8)

        self.until("sched")
        self.play(Indicate(bars[0]), run_time=0.6)

        self.until("static")
        self.play(grid_box.animate.set_stroke(DECODE, 2), run_time=0.6)

        self.until("differ")
        self.play(Indicate(bars[3]), run_time=0.6)

        self.until("short")
        bubble_tag = Pill("木桶效应：大面积算力与显存气泡", WARN, size=16).move_to([0, -2.4, 0])
        self.play(FadeIn(bubble_tag), run_time=0.7)

        self.finish()


class EP01_S12(DVScene):
    SHOT = "EP01-S12"

    def construct(self):
        head = self.fit_left_of_tags(header("连续批处理按步动态插入", "EP01 · S12 调度进化"))
        self.add(head)

        grid_box = RoundedRectangle(corner_radius=0.15, width=9.8, height=3.6,
                                    stroke_color=KV, stroke_width=2, fill_opacity=0)
        grid_box.move_to([0, -0.6, 0])
        g_title = T("连续批处理 (Continuous Batching)：迭代步级动态重排", 18, KV).next_to(grid_box.get_top(), DOWN, buff=0.15)

        rows = VGroup()
        for i in range(4):
            b1 = RoundedRectangle(corner_radius=0.06, width=2.4, height=0.42, color=DECODE, fill_opacity=0.8)
            t1 = T(f"Req {i*2+1}", 16, FG).move_to(b1)
            b2 = RoundedRectangle(corner_radius=0.06, width=2.8, height=0.42, color=KV, fill_opacity=0.8)
            t2 = T(f"Req {i*2+2} 动态", 16, FG).move_to(b2)
            b3 = RoundedRectangle(corner_radius=0.06, width=2.6, height=0.42, color=EXPERT, fill_opacity=0.8)
            t3 = T(f"Req {i*2+3}", 16, FG).move_to(b3)
            row = VGroup(VGroup(b1, t1), VGroup(b2, t2), VGroup(b3, t3)).arrange(RIGHT, buff=0.08)
            rows.add(row)
        rows.arrange(DOWN, buff=0.15).move_to([0, -0.65, 0])

        b_tag = Pill("气泡消除率 100% · 槽位全天候满载", KV, size=16).move_to([0, -2.4, 0])

        self.play(FadeIn(grid_box), FadeIn(g_title), FadeIn(rows), run_time=0.8)

        self.until("continuous")
        self.play(Indicate(rows[0][1]), run_time=0.6)

        self.until("retire")
        self.play(rows[0][0].animate.set_opacity(0.4), run_time=0.6)

        self.until("insert")
        self.play(Indicate(rows[1][1]), Indicate(rows[2][1]), run_time=0.6)

        self.until("full")
        self.play(FadeIn(b_tag), run_time=0.7)

        self.finish()


class EP01_S13(DVScene):
    SHOT = "EP01-S13"

    def construct(self):
        head = self.fit_left_of_tags(header("不可能三角的平衡艺术", "EP01 · S13 评价体系"))
        self.add(head)

        c_ttft = number_card("TTFT", "首字延迟", "预填充决定 · 交互首响", color=PREFILL).move_to([0, 1.2, 0])
        c_tpot = number_card("TPOT", "步进延迟", "解码决定 · 阅读流畅度", color=DECODE).move_to([-3.2, -1.2, 0])
        c_tput = number_card("Throughput", "吞吐量", "整体并发 · 决定单字成本", color=KV).move_to([3.2, -1.2, 0])

        tri_group = VGroup(c_ttft, c_tpot, c_tput)
        self.play(FadeIn(tri_group), run_time=0.9)

        self.until("metrics")
        self.play(Indicate(c_ttft), run_time=0.6)

        self.until("ttft")
        self.play(c_ttft.animate.scale(1.05), run_time=0.5)

        self.until("tpot")
        self.play(Indicate(c_tpot), Indicate(c_tput), run_time=0.7)

        center_tag = Pill("核心权衡：增大批次拉高吞吐，排队延长TTFT", EXPERT, size=16).move_to([0, -2.4, 0])
        self.play(FadeIn(center_tag), run_time=0.7)

        self.finish()


class EP01_S14(DVScene):
    SHOT = "EP01-S14"

    def construct(self):
        head = self.fit_left_of_tags(header("MoE 专家并行通信", "EP01 · S14 规模挑战"))
        self.add(head)

        gpus = VGroup()
        coords = [(-3.2, 0.4, 0), (3.2, 0.4, 0), (-3.2, -1.4, 0), (3.2, -1.4, 0)]
        for i, pt in enumerate(coords):
            box = RoundedRectangle(corner_radius=0.12, width=4.6, height=1.4,
                                   stroke_color=GRID, stroke_width=1.5, fill_opacity=0)
            box.move_to(pt)
            lbl = T(f"GPU {i} (专家 E{i*2}~E{i*2+1})", 16, EXPERT).next_to(box.get_top(), DOWN, buff=0.12)
            exp_row = TokenRow(2, color=EXPERT, size=0.35).next_to(lbl, DOWN, buff=0.12)
            gpus.add(VGroup(box, lbl, exp_row))

        arrows = VGroup(
            Arrow([-0.8, 0.4, 0], [0.8, 0.4, 0], color=WARN, stroke_width=2.5),
            Arrow([-0.8, -1.4, 0], [0.8, -1.4, 0], color=WARN, stroke_width=2.5),
        )

        self.play(FadeIn(gpus), run_time=0.8)

        self.until("moe")
        self.play(Create(arrows), run_time=0.8)

        self.until("sparse")
        tok = Pill("Token -> 跨卡派发到 E5", DECODE, size=16).move_to([0, 0.4, 0])
        self.play(FadeIn(tok), run_time=0.6)

        self.until("cards")
        self.play(FadeOut(tok), Indicate(gpus[3]), run_time=0.8)

        self.until("network")
        self.play(Indicate(gpus[3]), run_time=0.6)

        self.until("comm")
        comm_tag = Pill("跨卡通信瓶颈：全互联网络时延与重排开销", WARN, size=16).move_to([0, -2.4, 0])
        self.play(FadeIn(comm_tag), run_time=0.7)

        self.finish()


class EP01_S15(DVScene):
    SHOT = "EP01-S15"

    def construct(self):
        head = self.fit_left_of_tags(header("投机解码打破带宽限制", "EP01 · S15 降维打击"))
        self.add(head)

        top_box = RoundedRectangle(corner_radius=0.12, width=9.8, height=1.3,
                                   stroke_color=GRID, stroke_width=1.5, fill_color="#141822", fill_opacity=0.8)
        top_box.move_to([0, 0.7, 0])
        t_lbl = T("传统单步解码：每步仅产出 1 个词 (算术强度仅 2.0)", 16, MUTED).next_to(top_box.get_top(), DOWN, buff=0.15)
        t_toks = TokenRow(4, color=DECODE, size=0.35).next_to(t_lbl, DOWN, buff=0.15)
        top_track = VGroup(top_box, t_lbl, t_toks)

        bot_box = RoundedRectangle(corner_radius=0.12, width=9.8, height=1.5,
                                   stroke_color=KV, stroke_width=2, fill_color="#121F18", fill_opacity=0.9)
        bot_box.move_to([0, -1.0, 0])
        b_lbl = T("投机解码：轻量草稿猜测 5 个词 -> 主模型单步并行核验", 16, KV).next_to(bot_box.get_top(), DOWN, buff=0.15)
        b_draft = TokenRow(5, color=DRAFT, size=0.35).next_to(b_lbl, DOWN, buff=0.15)
        bot_track = VGroup(bot_box, b_lbl, b_draft)

        self.play(FadeIn(top_track), run_time=0.8)

        self.until("spec")
        self.play(FadeIn(bot_track), run_time=0.8)

        self.until("idea")
        self.play(Indicate(b_draft), run_time=0.6)

        self.until("draft")
        self.play(b_draft.animate.set_stroke(KV, 2), run_time=0.6)

        self.until("verify")
        speed_tag = Pill("逐字循环 -> 批量验证 · 步进效率跃升数倍", KV, size=16).move_to([0, -2.4, 0])
        self.play(FadeIn(speed_tag), run_time=0.7)

        self.finish()


class EP01_S16(DVScene):
    SHOT = "EP01-S16"

    def construct(self):
        head = self.fit_left_of_tags(header("预填充与解码分离部署", "EP01 · S16 物理隔离"))
        self.add(head)

        p_pool = RoundedRectangle(corner_radius=0.15, width=4.6, height=3.6,
                                  stroke_color=PREFILL, stroke_width=2, fill_color="#211717", fill_opacity=0.9)
        p_pool.move_to([-3.2, -0.6, 0])
        p_title = T("预填充池 (Prefill Pool)", 20, PREFILL).next_to(p_pool.get_top(), DOWN, buff=0.2)
        p_spec = T("标准 8 卡服务器 (EP8)\n专精大矩阵 GEMM 满载算力", 16, FG).next_to(p_title, DOWN, buff=0.25)
        p_chip = Block("算力密集芯片", color=PREFILL, w=3.4, h=0.8, size=18).next_to(p_spec, DOWN, buff=0.3)
        p_group = VGroup(p_pool, p_title, p_spec, p_chip)

        d_pool = RoundedRectangle(corner_radius=0.15, width=4.6, height=3.6,
                                  stroke_color=DECODE, stroke_width=2, fill_color="#141D2A", fill_opacity=0.9)
        d_pool.move_to([3.2, -0.6, 0])
        d_title = T("解码池 (Decode Pool)", 20, DECODE).next_to(d_pool.get_top(), DOWN, buff=0.2)
        d_spec = T("宽专家并行超节点 (EP64–128)\n专精大显存带宽与高并发", 16, FG).next_to(d_title, DOWN, buff=0.25)
        d_chip = Block("显存带宽集群", color=DECODE, w=3.4, h=0.8, size=18).next_to(d_spec, DOWN, buff=0.3)
        d_group = VGroup(d_pool, d_title, d_spec, d_chip)

        mid_arrow = Arrow([-0.8, -0.6, 0], [0.8, -0.6, 0], color=KV, stroke_width=3)
        mid_tag = Pill("KV 传输", KV, size=16).next_to(mid_arrow, UP, buff=0.1)

        self.play(FadeIn(p_group), FadeIn(d_group), run_time=0.9)

        self.until("revisit")
        self.play(Indicate(p_chip), run_time=0.6)

        self.until("conflict")
        self.play(Indicate(d_chip), run_time=0.6)

        self.until("disagg")
        self.play(Create(mid_arrow), FadeIn(mid_tag), run_time=0.7)

        self.until("split")
        iso_tag = Pill("物理资源彻底隔离 · 互不干扰", EXPERT, size=16).move_to([0, -2.4, 0])
        self.play(FadeIn(iso_tag), run_time=0.7)

        self.finish()


class EP01_S17(DVScene):
    SHOT = "EP01-S17"

    def construct(self):
        head = self.fit_left_of_tags(header("DeepInfer 的技术攻坚图", "EP01 · S17 系列全景"))
        self.add(head)

        core = Block("DeepInfer 专用引擎", color=KV, w=3.6, h=1.0, size=20, sub="面向硬件物理极限设计").move_to([0, 0.4, 0])

        b1 = Block("ZOS 零开销异步调度", color=DECODE, w=3.4, h=0.75, size=16, sub="EP05 细讲").move_to([-3.8, 1.2, 0])
        b2 = Block("SWA 有界重放", color=SWA, w=3.4, h=0.75, size=16, sub="EP07 细讲").move_to([3.8, 1.2, 0])
        b3 = Block("Wide-EP 宽专家并行", color=EXPERT, w=3.4, h=0.75, size=16, sub="EP08 细讲").move_to([-3.8, -1.0, 0])
        b4 = Block("投机解码与批不变", color=PREFILL, w=3.4, h=0.75, size=16, sub="EP09 / EP10 细讲").move_to([3.8, -1.0, 0])

        branches = VGroup(b1, b2, b3, b4)

        self.play(FadeIn(core), run_time=0.8)

        self.until("deepinfer")
        self.play(core.animate.set_stroke(KV, 3), run_time=0.6)

        self.until("zos")
        self.play(FadeIn(b1), FadeIn(b2), run_time=0.7)

        self.until("tech")
        self.play(FadeIn(b3), FadeIn(b4), run_time=0.7)
        foot = T("跟随同一个长请求 · 逐站拆解内部优化机制", 18, FG).move_to([0, -2.3, 0])
        self.play(FadeIn(foot), run_time=0.7)

        self.finish()


class EP01_S18(DVScene):
    SHOT = "EP01-S18"

    def construct(self):
        head = self.fit_left_of_tags(header("三句话总结", "EP01 · S18 本集要点"))
        self.add(head)

        c1 = Block("1. 推理两阶段物理割裂", color=DECODE, w=10.0, h=0.9, size=18,
                   sub="预填充 (Prefill) 受算力限制 · 解码 (Decode) 受显存带宽限制").move_to([0, 0.8, 0])
        c2 = Block("2. KV Cache 是第一约束", color=KV, w=10.0, h=0.9, size=18,
                   sub="避免历史二次重算 · 显存占用随长度与并发线性膨胀").move_to([0, -0.3, 0])
        c3 = Block("3. 引擎的权衡艺术", color=EXPERT, w=10.0, h=0.9, size=18,
                   sub="在吞吐、延迟与硬件成本之间做精密工程平衡").move_to([0, -1.4, 0])

        self.until("p1")
        self.play(FadeIn(c1), run_time=0.8)

        self.until("p2")
        self.play(FadeIn(c2), run_time=0.8)

        self.until("p3")
        self.play(FadeIn(c3), run_time=0.8)
        self.play(Indicate(c1), Indicate(c2), Indicate(c3), run_time=0.8)

        self.finish()


class EP01_S19(DVScene):
    SHOT = "EP01-S19"

    def construct(self):
        head = self.fit_left_of_tags(header("DeepInfer 是什么，不是什么", "EP01 · S19 下集预告"))
        self.add(head)

        card_box = RoundedRectangle(corner_radius=0.15, width=9.8, height=3.6,
                                    stroke_color=DECODE, stroke_width=2, fill_color="#121824", fill_opacity=0.95)
        card_box.move_to([0, -0.6, 0])

        tag = Pill("下集预告 · EP02", EXPERT, size=18).next_to(card_box.get_top(), DOWN, buff=0.25)
        title = T("DeepInfer 是什么，不是什么", 26, FG).next_to(tag, DOWN, buff=0.25)

        p_oss = Block("开源现状: 专用离线引擎", color=KV, w=4.2, h=0.9, size=18, sub="9bd9cf2 固定基线").move_to([-2.3, -1.3, 0])
        p_doc = Block("云端在线: 缺三大件", color=WARN, w=4.2, h=0.9, size=18, sub="KV存储 / P/D分离 / 负载均衡").move_to([2.3, -1.3, 0])
        teaser_group = VGroup(card_box, tag, title, p_oss, p_doc)

        self.play(FadeIn(teaser_group), run_time=0.8)

        self.until("focus")
        self.play(Indicate(p_oss), run_time=0.6)

        self.until("core")
        self.play(Indicate(p_doc), run_time=0.7)

        self.finish()
