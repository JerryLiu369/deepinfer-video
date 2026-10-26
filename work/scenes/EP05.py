"""EP05 scenes: 调度：让 GPU 一刻不停 (shots S01-S20).

Layout convention used throughout this episode:
  * header via self.fit_left_of_tags(header(...))
  * hero content lives in y in [-2.2, 2.0]
  * bottom safe line stays at y >= -2.65 (subtitle safe zone below -2.75)
  * text sizes >= 18 pt (small labels >= 16 pt)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import (
    DOWN, LEFT, RIGHT, UP, UL, UR, DL, DR, PI, TAU,
    FadeIn, FadeOut, Create, Indicate, Rotate, LaggedStart,
    Line, Arrow, Rectangle, RoundedRectangle, Circle, Polygon, VGroup, DashedLine,
    SurroundingRectangle,
)
from manim_lib.dvlib import (
    BG, FG, MUTED, GRID, PREFILL, DECODE, KV, SWA, WARN, EXPERT, DRAFT, GPU, CPU,
    T, M, Pill, DVScene, header, MiniMap, Block, TokenRow,
    number_card, Timeline, Scale,
)


class _E05(DVScene):
    """Small helpers shared by every EP05 shot."""

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
class EP05_S01(_E05):
    SHOT = "EP05-S01"

    def construct(self):
        head = self.fit_left_of_tags(header("GPU 空泡之谜", "EP05 · S01 冷开场"))
        self.add(head)

        box_sync = RoundedRectangle(width=6.0, height=1.6, corner_radius=0.15, stroke_color=MUTED,
                                    stroke_width=1.5, fill_color=MUTED, fill_opacity=0.12).move_to([-3.4, 0.5, 0])
        t_sync_title = T("传统同步调度: GPU 跑4ms / 等1.5ms", 18, WARN).move_to([-3.4, 1.05, 0])
        b_fwd = Block("Forward 4.0ms", color=GPU, w=2.8, h=0.6, size=16).move_to([-4.6, 0.4, 0])
        b_idle = Block("GPU 空闲 1.5ms", color=WARN, w=2.0, h=0.6, size=16).move_to([-2.0, 0.4, 0])
        grp_sync = VGroup(box_sync, t_sync_title, b_fwd, b_idle)

        box_zos = RoundedRectangle(width=6.0, height=1.6, corner_radius=0.15, stroke_color=DECODE,
                                   stroke_width=1.5, fill_color=DECODE, fill_opacity=0.12).move_to([-3.4, -1.3, 0])
        t_zos_title = T("ZOS 零开销重叠: GPU 一刻不停", 18, DECODE).move_to([-3.4, -0.75, 0])
        b_z1 = Block("Forward N", color=GPU, w=2.6, h=0.6, size=16).move_to([-4.7, -1.4, 0])
        b_z2 = Block("Forward N+1", color=GPU, w=2.6, h=0.6, size=16).move_to([-2.0, -1.4, 0])
        grp_zos = VGroup(box_zos, t_zos_title, b_z1, b_z2)

        card_bubble = Block("GPU 周期空转占比: 24.6%\n4.0ms 前向 vs 1.5ms 等待", color=WARN, w=5.2, h=1.2, size=18).move_to([3.4, 0.5, 0])
        card_boost = Block("解码吞吐理论提升: +32.6%\n彻底消除 1.5ms 调度延迟", color=DECODE, w=5.2, h=1.2, size=18).move_to([3.4, -1.1, 0])

        self.play(FadeIn(grp_sync), run_time=1.0)

        self.until("timeline_contrast")
        self.play(FadeIn(card_bubble), run_time=0.8)

        self.until("sync_bubble")
        self.play(Indicate(b_idle, color=WARN), run_time=0.8)

        self.until("bubble_stat")
        self.play(Indicate(card_bubble, color=WARN), run_time=0.8)

        self.until("zos_reveal")
        self.play(FadeIn(grp_zos), FadeIn(card_boost), run_time=1.0)

        self.finish()


# ---------------------------------------------------------------- S02
class EP05_S02(_E05):
    SHOT = "EP05-S02"

    def construct(self):
        title = T("EP05 · 调度中枢", 46, DECODE).move_to([0, 0.6, 0])
        sub = T("让 GPU 一刻不停", 32, FG).move_to([0, -0.2, 0])
        mmap = MiniMap(active="Decode", scale=1.05).move_to([0, -1.3, 0])

        self.play(FadeIn(title), FadeIn(sub), run_time=0.8)

        self.until("card")
        self.play(FadeIn(mmap), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S03
class EP05_S03(_E05):
    SHOT = "EP05-S03"

    def construct(self):
        head = self.fit_left_of_tags(header("同步调度的阻塞等待", "EP05 · S03 核心矛盾"))
        self.add(head)

        b_fwd = Block("1. Forward(N)\nGPU 计算 4.0ms", color=GPU, w=3.4, h=1.0, size=18).move_to([-4.2, 0.8, 0])
        b_smp = Block("2. Sample(N)\nGPU 采样 0.6ms", color=GPU, w=3.4, h=1.0, size=18).move_to([-0.4, 0.8, 0])
        b_sync = Block("3. synchronize()\n阻塞等待 GPU 落地", color=WARN, w=3.4, h=1.0, size=18).move_to([3.4, 0.8, 0])

        b_cpu = Block("CPU 主机侧后处理与调度\n解包结果 + 显存分配 + 下步调度 (1.5ms)", color=CPU, w=7.2, h=1.0, size=18).move_to([0, -0.6, 0])
        b_idle = Block("GPU 状态: 完全挂起休眠 (空泡 24.6%)", color=WARN, w=7.2, h=0.7, size=18).move_to([0, -1.65, 0])

        arr1 = Arrow(b_fwd.get_right(), b_smp.get_left(), color=FG, stroke_width=2, buff=0.1)
        arr2 = Arrow(b_smp.get_right(), b_sync.get_left(), color=FG, stroke_width=2, buff=0.1)
        arr3 = Arrow(b_sync.get_bottom(), b_cpu.get_top(), color=WARN, stroke_width=2, buff=0.1)

        self.play(FadeIn(b_fwd), run_time=0.8)

        self.until("zoom_sync")
        self.play(FadeIn(arr1), FadeIn(b_smp), run_time=0.8)

        self.until("step_flow")
        self.play(FadeIn(arr2), FadeIn(b_sync), run_time=0.8)

        self.until("sync_block")
        self.play(Indicate(b_sync, color=WARN), run_time=0.8)

        self.until("cpu_cost")
        self.play(FadeIn(arr3), FadeIn(b_cpu), run_time=0.8)

        self.until("gpu_idle")
        self.play(FadeIn(b_idle), Indicate(b_idle, color=WARN), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S04
class EP05_S04(_E05):
    SHOT = "EP05-S04"

    def construct(self):
        head = self.fit_left_of_tags(header("让 CPU 永远晚一步", "EP05 · S04 破局之道"))
        self.add(head)

        t_gpu_lane = T("GPU 计算轨", 20, GPU).move_to([-5.2, 0.9, 0])
        b_gpu_n = Block("Forward(N) 4.0ms", color=GPU, w=4.5, h=0.9, size=18).move_to([-1.5, 0.9, 0])
        b_gpu_n1 = Block("Forward(N+1) 4.0ms", color=GPU, w=4.5, h=0.9, size=18).move_to([3.4, 0.9, 0])

        t_cpu_lane = T("CPU 调度轨", 20, CPU).move_to([-5.2, -0.6, 0])
        b_cpu_prev = Block("Post-process(N-1) 1.5ms\n(与 Forward(N) 并发重叠)", color=CPU, w=4.5, h=0.9, size=18).move_to([-1.5, -0.6, 0])
        b_cpu_curr = Block("Post-process(N) 1.5ms\n(与 Forward(N+1) 并发重叠)", color=CPU, w=4.5, h=0.9, size=18).move_to([3.4, -0.6, 0])

        card_zero = Pill("GPU 等待时间 = 0 ms · 零开销调度", DECODE, size=20).move_to([0, -1.8, 0])

        self.play(FadeIn(t_gpu_lane), FadeIn(b_gpu_n), run_time=0.8)

        self.until("zos_intro")
        self.play(FadeIn(t_cpu_lane), run_time=0.6)

        self.until("time_shift")
        self.play(FadeIn(b_cpu_prev), run_time=0.8)

        self.until("forward_n")
        self.play(Indicate(b_gpu_n, color=DECODE), run_time=0.8)

        self.until("post_n_minus_1")
        self.play(Indicate(b_cpu_prev, color=CPU), run_time=0.8)

        self.until("sync_early")
        self.play(FadeIn(b_gpu_n1), FadeIn(b_cpu_curr), run_time=0.8)

        self.until("zero_block")
        self.play(FadeIn(card_zero), Indicate(card_zero, color=DECODE), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S05
class EP05_S05(_E05):
    SHOT = "EP05-S05"

    def construct(self):
        head = self.fit_left_of_tags(header("worker 的四段式单步循环", "EP05 · S05 骨架剖析"))
        self.add(head)

        box_fn = RoundedRectangle(width=10.6, height=3.6, corner_radius=0.15, stroke_color=MUTED,
                                  stroke_width=1.5, fill_color=MUTED, fill_opacity=0.08).move_to([0, -0.2, 0])
        fn_title = T("deepinfer/worker/worker.py: execute_model_step", 18, FG).move_to([-2.2, 1.3, 0])

        s1 = Block("1. Forward(curr)\n发射当前步主模型", color=GPU, w=4.8, h=0.85, size=16).move_to([-2.5, 0.45, 0])
        s2 = Block("2. Post-process(prev)\n并发处理上一步结果", color=CPU, w=4.8, h=0.85, size=16).move_to([2.5, 0.45, 0])
        s3 = Block("3. Sample(curr)\n发射当前步采样", color=GPU, w=4.8, h=0.85, size=16).move_to([-2.5, -0.75, 0])
        s4 = Block("4. Post-process(curr)\n留到下一步与新前向重叠", color=WARN, w=4.8, h=0.85, size=16).move_to([2.5, -0.75, 0])

        pill_q = Pill("Q：四阶段交错执行，底层如何排布？", DECODE, size=18).move_to([0, -1.8, 0])

        self.play(FadeIn(box_fn), FadeIn(fn_title), run_time=0.8)

        self.until("q_overlap_stages")
        self.play(FadeIn(pill_q), run_time=0.6)

        self.until("code_entry")
        self.play(Indicate(fn_title, color=DECODE), run_time=0.6)

        self.until("four_stages")
        self.play(FadeIn(s1), run_time=0.6)

        self.until("stage1")
        self.play(Indicate(s1, color=GPU), run_time=0.6)

        self.until("stage2")
        self.play(FadeIn(s2), Indicate(s2, color=CPU), run_time=0.6)

        self.until("stage3")
        self.play(FadeIn(s3), Indicate(s3, color=GPU), run_time=0.6)

        self.until("stage4")
        self.play(FadeIn(s4), Indicate(s4, color=WARN), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S06
class EP06_S06_fallback(_E05):
    pass


class EP05_S06(_E05):
    SHOT = "EP05-S06"

    def construct(self):
        head = self.fit_left_of_tags(header("ZOS 仅管解码，Prefill 纯同步", "EP05 · S06 关键界限"))
        self.add(head)

        d1 = Block("Decode 1\n(ZOS 异步)", color=DECODE, w=2.4, h=1.0, size=18).move_to([-4.5, 0.4, 0])
        d2 = Block("Decode 2\n(ZOS 异步)", color=DECODE, w=2.4, h=1.0, size=18).move_to([-1.8, 0.4, 0])
        p1 = Block("Prefill 步\n(is_prompt=True)", color=PREFILL, w=2.8, h=1.2, size=18).move_to([1.2, 0.4, 0])
        d3 = Block("Decode 3\n(无前序重叠)", color=WARN, w=2.4, h=1.0, size=18).move_to([4.1, 0.4, 0])

        pill_drain = Pill("Prefill 强制排空异步流水线: 当场同步两次后处理", WARN, size=18).move_to([0, -1.0, 0])
        t_note = T("注：预填后首个解码步无前序任务可供重叠", 16, MUTED).move_to([0, -1.75, 0])

        self.play(FadeIn(d1), FadeIn(d2), run_time=0.8)

        self.until("boundary_note")
        self.play(Indicate(d2, color=DECODE), run_time=0.6)

        self.until("is_prompt_check")
        self.play(FadeIn(p1), run_time=0.8)

        self.until("prefill_interrupt")
        self.play(Indicate(p1, color=PREFILL), run_time=0.8)

        self.until("drain_pipeline")
        self.play(FadeIn(pill_drain), run_time=0.8)

        self.until("first_decode_bubble")
        self.play(FadeIn(d3), FadeIn(t_note), Indicate(d3, color=WARN), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S07
class EP05_S07(_E05):
    SHOT = "EP05-S07"

    def construct(self):
        head = self.fit_left_of_tags(header("还没算出的词怎么输入？", "EP05 · S07 难题之一"))
        self.add(head)

        b_gpu_cur = Block("第 N 步: GPU 正在执行采样\n(输出结果仍躺在显存内部)", color=GPU, w=5.2, h=1.2, size=18).move_to([-3.0, 0.6, 0])
        b_cpu_next = Block("第 N+1 步: CPU 正在调度输入\n(需要知道下一步输入词是什么)", color=CPU, w=5.2, h=1.2, size=18).move_to([3.0, 0.6, 0])

        box_conflict = RoundedRectangle(width=8.0, height=1.6, corner_radius=0.15, stroke_color=WARN,
                                        stroke_width=2, fill_color=WARN, fill_opacity=0.12).move_to([0, -1.1, 0])
        t_paradox = T("因果倒置难题: 词还没生成，怎么提前输入？", 20, WARN).move_to([0, -0.85, 0])
        t_desc = T("CPU 无法从主机内存构造存量请求的输入 Token", 18, FG).move_to([0, -1.35, 0])

        self.play(FadeIn(b_gpu_cur), run_time=0.8)

        self.until("time_lag")
        self.play(FadeIn(b_cpu_next), run_time=0.8)

        self.until("paradox_reveal")
        self.play(FadeIn(box_conflict), FadeIn(t_paradox), run_time=0.8)

        self.until("cpu_prepare")
        self.play(Indicate(b_cpu_next, color=CPU), run_time=0.6)

        self.until("unknown_tokens")
        self.play(FadeIn(t_desc), run_time=0.6)

        self.until("question_how")
        self.play(Indicate(box_conflict, color=WARN), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S08
class EP05_S08(_E05):
    SHOT = "EP05-S08"

    def construct(self):
        head = self.fit_left_of_tags(header("TileLang 内核就地索引", "EP05 · S08 现场捡词"))
        self.add(head)

        b_cpu = Block("CPU 侧: fresh_input_ids\n存量请求写入 0 字节 (全部留空)", color=CPU, w=5.0, h=2.4, size=18).move_to([-3.4, -0.1, 0])
        b_gpu = Block("GPU 侧: TileLang gather 算子\n从 prev_sampled 张量就地捡词", color=GPU, w=5.0, h=2.4, size=18).move_to([3.4, -0.1, 0])

        pill_bypass = Pill("CPU 压根不传存量词 · 显存内部闭环", DECODE, size=20).move_to([0, -1.8, 0])

        self.play(FadeIn(b_cpu), run_time=0.8)

        self.until("clever_solution")
        self.play(FadeIn(b_gpu), run_time=0.8)

        self.until("cpu_bypass")
        self.play(Indicate(b_cpu, color=CPU), run_time=0.6)

        self.until("zero_bytes")
        self.play(FadeIn(pill_bypass), run_time=0.8)

        self.until("gpu_kernel")
        self.play(Indicate(b_gpu, color=GPU), run_time=0.8)

        self.until("gather_kernel")
        self.play(Indicate(b_gpu, color=DECODE), run_time=0.8)

        self.until("onsite_pick")
        self.play(Indicate(pill_bypass, color=DECODE), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S09
class EP05_S09(_E05):
    SHOT = "EP05-S09"

    def construct(self):
        head = self.fit_left_of_tags(header("行序动态重排与 remap", "EP05 · S09 行序重排"))
        self.add(head)

        b_order1 = Block("上一步行序: [Seq A, Seq B, Seq C]\n按长度降序排布", color=MUTED, w=5.0, h=1.0, size=18).move_to([-3.2, 0.8, 0])
        b_order2 = Block("下一步行序: [Seq B, Seq A, Seq C]\n长度增长触发重排换位", color=WARN, w=5.0, h=1.0, size=18).move_to([3.2, 0.8, 0])

        b_remap = Block("remap 映射数组: CPU 按 seq_id 哈希构建\n[行0 -> 行1, 行1 -> 行0, 行2 -> 行2]", color=DECODE, w=8.6, h=1.1, size=18).move_to([0, -0.6, 0])
        pill_safe = Pill("精准找回上下文 · 杜绝张量索引踩踏", DECODE, size=18).move_to([0, -1.75, 0])

        self.play(FadeIn(b_order1), run_time=0.8)

        self.until("q_why_remap")
        self.play(FadeIn(b_order2), run_time=0.8)

        self.until("sort_explain")
        self.play(Indicate(b_order2, color=WARN), run_time=0.6)

        self.until("length_sort")
        self.play(FadeIn(b_remap), run_time=0.8)

        self.until("mismatch_risk")
        self.play(Indicate(b_order2, color=WARN), run_time=0.6)

        self.until("remap_gen")
        self.play(Indicate(b_remap, color=DECODE), run_time=0.8)

        self.until("remap_wire")
        self.play(FadeIn(pill_safe), Indicate(pill_safe, color=DECODE), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S10
class EP05_S10(_E05):
    SHOT = "EP05-S10"

    def construct(self):
        head = self.fit_left_of_tags(header("请求已经结束了怎么办？", "EP05 · S10 难题之二"))
        self.add(head)

        b1 = Block("Token 1", color=DECODE, w=1.8, h=0.75, size=16)
        b2 = Block("Token 2", color=DECODE, w=1.8, h=0.75, size=16)
        b3 = Block("Token 3", color=DECODE, w=1.8, h=0.75, size=16)
        b_eos = Block("EOS (终止)", color=WARN, w=2.0, h=0.75, size=16)
        t_row = VGroup(b1, b2, b3, b_eos).arrange(RIGHT, buff=0.25).move_to([0, 1.0, 0])
        b_ghost = Block("第 N+1 步: 幽灵前向 (Ghost Forward)\nCPU 不知已结束，以 EOS 为输入再跑一次", color=WARN, w=8.8, h=1.1, size=18).move_to([0, -0.2, 0])

        pill_quest = Pill("这看似荒谬的现象，会不会拖垮系统？", FG, size=20).move_to([0, -1.6, 0])

        self.play(FadeIn(t_row), run_time=0.8)

        self.until("eos_dilemma")
        self.play(Indicate(t_row[-1], color=WARN), run_time=0.8)

        self.until("cpu_blind")
        self.play(FadeIn(b_ghost), run_time=0.8)

        self.until("still_running")
        self.play(Indicate(b_ghost, color=WARN), run_time=0.8)

        self.until("ghost_step")
        self.play(FadeIn(pill_quest), Indicate(pill_quest, color=DECODE), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S11
class EP05_S11(_E05):
    SHOT = "EP05-S11"

    def construct(self):
        head = self.fit_left_of_tags(header("多跑一步的算术账本", "EP05 · S11 确定性代价"))
        self.add(head)

        scale = Scale(left="0.2% 算力浪费\n(多跑 1 步)", right="消灭 24.6% 空泡\n(全流程受益)",
                      left_color=MUTED, right_color=DECODE, w=8.0, h=2.4).move_to([0, 0.1, 0])
        pill_tilt = Pill("千分之二微弱代价 · 换取近三成全局吞吐提升", DECODE, size=20).move_to([0, -1.75, 0])

        self.play(FadeIn(scale), run_time=1.0)

        self.until("not_a_bug")
        self.play(Indicate(scale.left_pan, color=MUTED), run_time=0.6)

        self.until("discard_result")
        self.play(Indicate(scale.left_pan, color=WARN), run_time=0.6)

        self.until("free_step")
        self.play(Indicate(scale.right_pan, color=DECODE), run_time=0.6)

        self.until("balance_calc")
        self.play(scale.beam.animate.rotate(-0.15),
                  scale.left_pan.animate.shift(UP * 0.4),
                  scale.right_pan.animate.shift(DOWN * 0.4),
                  run_time=1.0)

        self.until("five_hundred_tokens")
        self.play(Indicate(scale.left_pan, color=WARN), run_time=0.6)

        self.until("scale_tilt")
        self.play(FadeIn(pill_tilt), Indicate(pill_tilt, color=DECODE), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S12
class EP05_S12(_E05):
    SHOT = "EP05-S12"

    def construct(self):
        head = self.fit_left_of_tags(header("虚高账本与真实回填", "EP05 · S12 乐观推进"))
        self.add(head)

        b_push = Block("1. advance_optimistically\n假定预测词全部被接受，显存顶格预留", color=WARN, w=8.6, h=0.9, size=18).move_to([0, 0.9, 0])
        b_safe = Block("2. total_inflight_tokens\n在途安全护栏，防御显存被其它请求抢占", color=CPU, w=8.6, h=0.9, size=18).move_to([0, -0.1, 0])
        b_commit = Block("3. commit_processed_tokens\n拿到显卡真实接受数，精准回填真实长度", color=DECODE, w=8.6, h=0.9, size=18).move_to([0, -1.1, 0])

        self.play(FadeIn(b_push), run_time=0.8)

        self.until("bookkeeping_challenge")
        self.play(Indicate(b_push, color=WARN), run_time=0.6)

        self.until("dual_ledger")
        self.play(FadeIn(b_safe), run_time=0.8)

        self.until("optimistic_push")
        self.play(Indicate(b_safe, color=CPU), run_time=0.6)

        self.until("commit_tokens")
        self.play(FadeIn(b_commit), run_time=0.8)

        self.until("rebound_fill")
        self.play(Indicate(b_commit, color=DECODE), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S13
class EP05_S13(_E05):
    SHOT = "EP05-S13"

    def construct(self):
        head = self.fit_left_of_tags(header("DSpark 投机在 ZOS 下的双层切分", "EP05 · S13 变长协作"))
        self.add(head)

        b_top = Block("CPU 宏观决策: 查阅延迟曲线，锁定固定总预算 best_bsz\n(完美适配 CUDA Graph 桶，批次大小恒定)",
                      color=CPU, w=9.0, h=1.1, size=18).move_to([0, 0.65, 0])
        b_bot = Block("GPU 微观分配: TileLang 内核按置信度切分单项验证长度\n(D2H 回写固定内存，总和等于 best_bsz)",
                      color=GPU, w=9.0, h=1.1, size=18).move_to([0, -0.65, 0])

        pill_sync = Pill("宏观总量固定 · 微观动态切分", DECODE, size=20).move_to([0, -1.75, 0])

        self.play(FadeIn(b_top), run_time=0.8)

        self.until("q_varlen_graph")
        self.play(Indicate(b_top, color=CPU), run_time=0.6)

        self.until("design_highlight")
        self.play(FadeIn(b_bot), run_time=0.8)

        self.until("perf_curve")
        self.play(Indicate(b_top, color=DECODE), run_time=0.6)

        self.until("total_q_fix")
        self.play(Indicate(b_bot, color=GPU), run_time=0.6)

        self.until("gpu_realloc")
        self.play(Indicate(b_bot, color=DECODE), run_time=0.6)

        self.until("d2h_pinned")
        self.play(FadeIn(pill_sync), Indicate(pill_sync, color=DECODE), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S14
class EP05_S14(_E05):
    SHOT = "EP05-S14"

    def construct(self):
        head = self.fit_left_of_tags(header("LCFS 选拔与残忍抢占", "EP05 · S14 调度取舍"))
        self.add(head)

        b_lcfs = Block("解码调度: LCFS (后到先服务)\n优先调度输出最短的最新请求", color=DECODE, w=8.8, h=1.0, size=18).move_to([0, 0.8, 0])
        b_preempt = Block("显存超限抢占: 牺牲输出最长的老请求\n默认直接判死终止 (stop_preempted=True，不重算)",
                          color=WARN, w=8.8, h=1.0, size=18).move_to([0, -0.4, 0])
        pill_cold = Pill("冷酷策略杜绝长尾霸占 · 容错推给外层网关", MUTED, size=18).move_to([0, -1.65, 0])

        self.play(FadeIn(b_lcfs), run_time=0.8)

        self.until("sched_policy")
        self.play(Indicate(b_lcfs, color=DECODE), run_time=0.6)

        self.until("lcfs_logic")
        self.play(FadeIn(b_preempt), run_time=0.8)

        self.until("mem_pressure")
        self.play(Indicate(b_preempt, color=WARN), run_time=0.8)

        self.until("preempt_old")
        self.play(Indicate(b_preempt, color=WARN), run_time=0.6)

        self.until("kill_request")
        self.play(FadeIn(pill_cold), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S15
class EP05_S15(_E05):
    SHOT = "EP05-S15"

    def construct(self):
        head = self.fit_left_of_tags(header("DP 副本的 70 步与 100 步投票", "EP05 · S15 步型共识"))
        self.add(head)

        b_rule = Block("单步严禁混合: 全组步型必须 100% 一致 (防 EP 死锁)", color=FG, w=8.8, h=0.8, size=18).move_to([0, 1.1, 0])
        c_70 = Block("每 70 步: ALL 投票\n全员就绪才转 Prefill", color=PREFILL, w=4.2, h=1.2, size=18).move_to([-2.4, -0.15, 0])
        c_100 = Block("每 100 步: ANY 投票\n任一就绪即转防饿死", color=WARN, w=4.2, h=1.2, size=18).move_to([2.4, -0.15, 0])
        pill_vote = Pill("_dp_allreduce 统一步调 · 兼顾吞吐与首字延迟", DECODE, size=18).move_to([0, -1.6, 0])

        self.play(FadeIn(b_rule), run_time=0.8)

        self.until("dist_heading")
        self.play(FadeIn(c_70), run_time=0.8)

        self.until("dp_vote")
        self.play(FadeIn(c_100), run_time=0.8)

        self.until("interval_70")
        self.play(Indicate(c_70, color=PREFILL), run_time=0.6)

        self.until("interval_100")
        self.play(Indicate(c_100, color=WARN), run_time=0.6)

        self.until("any_vote")
        self.play(FadeIn(pill_vote), Indicate(pill_vote, color=DECODE), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S16
class EP05_S16(_E05):
    SHOT = "EP05-S16"

    def construct(self):
        head = self.fit_left_of_tags(header("文档里的二次模型去哪了？", "EP05 · S16 代码真相"))
        self.add(head)

        b_doc = Block("部署问答文档声称:\nprefill 二次代价模型 + compute_quota_limit 时间预算",
                      color=WARN, w=8.8, h=1.0, size=18).move_to([0, 0.9, 0])
        b_code = Block("代码事实 (commit 9bd9cf2):\n全仓 quota 变量 0 命中 · 纯硬 Token 计数剪裁",
                       color=DECODE, w=8.8, h=1.0, size=18).move_to([0, -0.25, 0])
        pill_truth = Pill("FlopsEstimator 仅在步进结束时打印利用率日志 · 不做调度", MUTED, size=17).move_to([0, -1.5, 0])

        self.play(FadeIn(b_doc), run_time=0.8)

        self.until("q_where_quota")
        self.play(Indicate(b_doc, color=WARN), run_time=0.6)

        self.until("doc_audit")
        self.play(FadeIn(b_code), run_time=0.8)

        self.until("code_search")
        self.play(Indicate(b_code, color=DECODE), run_time=0.6)

        self.until("zero_hit")
        self.play(Indicate(b_code, color=WARN), run_time=0.6)

        self.until("hard_token")
        self.play(FadeIn(pill_truth), run_time=0.8)

        self.until("flops_calc")
        self.play(Indicate(pill_truth, color=DECODE), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S17
class EP05_S17(_E05):
    SHOT = "EP05-S17"

    def construct(self):
        head = self.fit_left_of_tags(header("Deferred 释放与 flush 兜底", "EP05 · S17 严谨收尾"))
        self.add(head)

        b_def = Block("DeferredRelease: 延后一轮释放 SequenceMetadata 对象池\n(在下一次显卡前向期间并行回收，杜绝资源踩踏)",
                      color=CPU, w=9.0, h=1.1, size=18).move_to([0, 0.7, 0])
        b_flush = Block("flush_inflight_reqs: 请求全结束时强制冲刷\n(为最后一个在途步骤补做后处理，防止末尾词遗失)",
                        color=DECODE, w=9.0, h=1.1, size=18).move_to([0, -0.6, 0])
        pill_guard = Pill("微秒级生命周期管理 · 工业实现的严密之处", FG, size=18).move_to([0, -1.75, 0])

        self.play(FadeIn(b_def), run_time=0.8)

        self.until("async_cleanup")
        self.play(Indicate(b_def, color=CPU), run_time=0.6)

        self.until("deferred_release")
        self.play(FadeIn(b_flush), run_time=0.8)

        self.until("overlap_free")
        self.play(Indicate(b_def, color=DECODE), run_time=0.6)

        self.until("final_step")
        self.play(Indicate(b_flush, color=WARN), run_time=0.6)

        self.until("flush_call")
        self.play(Indicate(b_flush, color=DECODE), run_time=0.6)

        self.until("prevent_loss")
        self.play(FadeIn(pill_guard), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S18
class EP05_S18(_E05):
    SHOT = "EP05-S18"

    def construct(self):
        head = self.fit_left_of_tags(header("工业全景：殊途同归的重叠调度", "EP05 · S18 工业全景"))
        self.add(head)

        b_origin = Block("思想源头: NanoFlow 纳米流水线 (2024)", color=MUTED, w=8.8, h=0.75, size=18).move_to([0, 1.25, 0])
        c_vllm = Block("vLLM 对照:\nAsyncScheduler 默认开启\n(使用 -1 占位符跨步重叠)", color=CPU, w=4.2, h=1.4, size=16).move_to([-2.4, -0.05, 0])
        c_sgl = Block("SGLang 对照:\noverlap 调度器 v0.4 默认\n(三流并发重叠调度)", color=GPU, w=4.2, h=1.4, size=16).move_to([2.4, -0.05, 0])
        pill_all = Pill("现代大模型推理: 向延迟要吞吐的统一共识", DECODE, size=18).move_to([0, -1.55, 0])

        self.play(FadeIn(b_origin), run_time=0.8)

        self.until("industry_view")
        self.play(Indicate(b_origin, color=MUTED), run_time=0.6)

        self.until("doc_cite")
        self.play(FadeIn(c_vllm), run_time=0.8)

        self.until("broad_view")
        self.play(FadeIn(c_sgl), run_time=0.8)

        self.until("consensus")
        self.play(FadeIn(pill_all), run_time=0.8)

        self.until("vllm_async")
        self.play(Indicate(c_vllm, color=CPU), run_time=0.6)

        self.until("sglang_overlap")
        self.play(Indicate(c_sgl, color=GPU), run_time=0.6)

        self.finish()


# ---------------------------------------------------------------- S19
class EP05_S19(_E05):
    SHOT = "EP05-S19"

    def construct(self):
        head = self.fit_left_of_tags(header("三句话总结与暂停题作答", "EP05 · S19 三句话"))
        self.add(head)

        c1 = Block("1. ZOS 时空错位重叠: 显卡算当前 · CPU 处理前后 (消灭 24.6% 空泡)", color=DECODE, w=9.0, h=0.8, size=17).move_to([0, 1.15, 0])
        c2 = Block("2. GPU 现场捡词重组: 存量请求输入由 TileLang 就地完成", color=GPU, w=9.0, h=0.8, size=17).move_to([0, 0.25, 0])
        c3 = Block("3. 确定性固定代价: 0.2% 算力浪费换取近三成全局吞吐提升", color=WARN, w=9.0, h=0.8, size=17).move_to([0, -0.65, 0])
        pill_ans = Pill("暂停题答案：已结束请求多跑一步后丢弃，换取最大吞吐", DECODE, size=18).move_to([0, -1.65, 0])

        self.play(FadeIn(c1), run_time=0.8)

        self.until("recap_start")
        self.play(Indicate(c1, color=DECODE), run_time=0.6)

        self.until("recap_1")
        self.play(FadeIn(c2), run_time=0.8)

        self.until("recap_2")
        self.play(FadeIn(c3), run_time=0.8)

        self.until("recap_3")
        self.play(Indicate(c3, color=WARN), run_time=0.6)

        self.until("qa_reveal")
        self.play(FadeIn(pill_ans), run_time=0.8)

        self.until("qa_answer")
        self.play(Indicate(pill_ans, color=DECODE), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S20
class EP05_S20(_E05):
    SHOT = "EP05-S20"

    def construct(self):
        title = T("下集预告 · EP06", 36, DECODE).move_to([0, 0.8, 0])
        sub = T("KV 与状态缓存: 两种记忆，两种管法", 26, FG).move_to([0, 0.1, 0])
        mmap = MiniMap(active="KV 存储", scale=1.05).move_to([0, -1.0, 0])

        self.play(FadeIn(title), FadeIn(sub), run_time=0.8)

        self.until("outro_sched")
        self.play(Indicate(title, color=DECODE), run_time=0.6)

        self.until("outro_memory")
        self.play(FadeIn(mmap), run_time=0.8)

        self.until("preview_ep06")
        self.play(Indicate(mmap, color=PREFILL), run_time=0.8)

        self.finish()
