"""EP08 scenes: 并行：注意力用 DP，专家用宽 EP (shots S01-S07)."""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_lib.dvlib import (
    BG, FG, MUTED, GRID, PREFILL, DECODE, KV, SWA, WARN, EXPERT, DRAFT, GPU, CPU,
    T, M, Pill, DVScene, header, MiniMap, Block, TokenRow,
    number_card, LayerStack, Scale,
)

class _E08(DVScene):
    def foot(self, text: str, x: float = 6.4, y: float = -2.25, size: int = 16):
        t = T(text, size, MUTED)
        t.move_to([x, y, 0], aligned_edge=UR)
        return t

class EP08_S01(_E08):
    SHOT = "EP08-S01"
    def construct(self):
        head = self.fit_left_of_tags(header("Wide-EP 的悖论：理论访存 vs 吞吐收敛", "EP08 · S01 冷开场"))
        self.add(head)

        box_l = RoundedRectangle(width=5.8, height=3.4, corner_radius=0.15, stroke_color=EXPERT,
                                 stroke_width=1.5, fill_color=EXPERT, fill_opacity=0.08).move_to([-3.2, -0.2, 0])
        t_l = T("单卡权重访存：大幅下降 7.43 倍", 18, EXPERT).move_to([-3.2, 1.2, 0])
        card_mem = number_card("52 → 7", "个路由专家", "每卡专家数 (EP8 vs EP64)", color=EXPERT).move_to([-3.2, -0.2, 0])
        grp_l = VGroup(box_l, t_l, card_mem)

        box_r = RoundedRectangle(width=5.8, height=3.4, corner_radius=0.15, stroke_color=DECODE,
                                 stroke_width=1.5, fill_color=DECODE, fill_opacity=0.08).move_to([3.2, -0.2, 0])
        t_r = T("吞吐增益：高并发下收敛至 5%", 18, DECODE).move_to([3.2, 1.2, 0])
        card_perf = number_card("53% → 5%", "吞吐增益", "并发 8 → 256 (Pareto 实测)", color=WARN).move_to([3.2, -0.2, 0])
        grp_r = VGroup(box_r, t_r, card_perf)

        self.play(FadeIn(grp_l), run_time=1.0)
        self.until("wide_ep")
        self.play(FadeIn(grp_r), run_time=1.0)
        self.until("paradox")
        self.finish()

class EP08_S02(_E08):
    SHOT = "EP08-S02"
    def construct(self):
        head = self.fit_left_of_tags(header("正交切分：DP 切请求，EP 切专家", "EP08 · S02 架构"))
        self.add(head)

        pill_tp = Pill("开源配置无 Tensor Parallel (TP=1)", WARN).move_to([0, 1.2, 0])
        card_dp = Block("Attention 采用 DP", color=PREFILL, sub="请求维切分 · 独立 KV Cache", w=5.5, h=2.2).move_to([-3.2, -0.5, 0])
        card_ep = Block("MoE 采用 EP", color=EXPERT, sub="专家维切分 · DeepEP 全交换", w=5.5, h=2.2).move_to([3.2, -0.5, 0])

        self.play(FadeIn(pill_tp), run_time=0.8)
        self.until("no_tp")
        self.play(FadeIn(card_dp), FadeIn(card_ep), run_time=1.0)
        self.until("linear_types")
        self.finish()

class EP08_S03(_E08):
    SHOT = "EP08-S03"
    def construct(self):
        head = self.fit_left_of_tags(header("C++ 调度器：步型投票与占位对齐", "EP08 · S03 调度"))
        self.add(head)

        box_vote = Block("MIN all_reduce 步型投票", color=GPU, sub="统一决策这一步全员执行 Prompt 还是 Decode", w=10.0, h=1.4).move_to([0, 0.8, 0])
        box_place = Block("1-Token Placeholder 占位陪跑", color=MUTED, sub="无任务 Rank 发送假请求，确保 EP 集合通信严格对齐", w=10.0, h=1.4).move_to([0, -0.8, 0])

        self.play(FadeIn(box_vote), run_time=0.8)
        self.until("voting")
        self.play(FadeIn(box_place), run_time=0.8)
        self.until("placeholder")
        self.finish()

class EP08_S04(_E08):
    SHOT = "EP08-S04"
    def construct(self):
        head = self.fit_left_of_tags(header("MoE 6 段流水线与共享专家融合", "EP08 · S04 执行"))
        self.add(head)

        stages = ["1. Gate 打分", "2. DeepEP 交换", "3. 分组 GEMM", "4. 共享专家", "5. 融合偏置", "6. 同步等待"]
        colors = [GPU, EXPERT, EXPERT, PREFILL, DECODE, MUTED]
        pipe = VGroup(*[Pill(st, c) for st, c in zip(stages, colors)]).arrange(RIGHT, buff=0.15).move_to([0, 0.5, 0])
        if pipe.width > 12.0:
            pipe.scale_to_fit_width(12.0)
        card_fusion = Block("共享专家融合归约", color=PREFILL, sub="Shared Expert 输出直接作为 Combine 的 Bias 传入，免除独立 all_reduce", w=10.0, h=1.4).move_to([0, -1.0, 0])

        self.play(FadeIn(pipe), run_time=1.0)
        self.until("pipe")
        self.play(FadeIn(card_fusion), run_time=0.8)
        self.until("shared_fusion")
        self.finish()

class EP08_S05(_E08):
    SHOT = "EP08-S05"
    def construct(self):
        head = self.fit_left_of_tags(header("EPLB 两级贪心与 NVLink 显存直读", "EP08 · S05 平衡"))
        self.add(head)

        card_policy = Block("逐层两级贪心策略", color=EXPERT, sub="1. 复制历史热点逻辑专家\n2. 装箱最小化各步最慢 Rank 负载", w=5.5, h=2.4).move_to([-3.2, -0.3, 0])
        card_mem = Block("NVLink symm_mem 直读", color=GPU, sub="单层镜像逐层复用 · CUDA IPC 直读对端显存 · 零 P2P 通信", w=5.5, h=2.4).move_to([3.2, -0.3, 0])

        self.play(FadeIn(card_policy), FadeIn(card_mem), run_time=1.0)
        self.until("eplb")
        self.finish()

class EP08_S06(_E08):
    SHOT = "EP08-S06"
    def construct(self):
        head = self.fit_left_of_tags(header("Wide-EP 商业真意：极速交互 vs 显存平摊", "EP08 · S06 权衡"))
        self.add(head)

        card_val = number_card("60 并发", "/ GPU", "单卡能效与交互平衡最佳拐点", color=DECODE).move_to([0, 0.0, 0])
        self.play(FadeIn(card_val), run_time=1.0)
        self.until("tradeoff")
        self.finish()

class EP08_S07(_E08):
    SHOT = "EP08-S07"
    def construct(self):
        head = self.fit_left_of_tags(header("并行总结与下集预告", "EP08 · S07 结语"))
        self.add(head)

        card_sum = Block("并行架构总结", color=GPU, sub="注意力 DP + 专家宽 EP · 调度器投票统一 · NVLink 显存直读", w=10.0, h=1.6).move_to([0, 0.6, 0])
        card_next = Pill("下一集：DSpark 投机解码（多预测标记与置信度验证）", DRAFT).move_to([0, -1.0, 0])

        self.play(FadeIn(card_sum), run_time=0.8)
        self.until("summary")
        self.play(FadeIn(card_next), run_time=0.8)
        self.finish()
