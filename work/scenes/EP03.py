"""EP03 scenes: 先认识它服务的模型 (shots S01-S22).

Layout convention used throughout this episode:
  * header via self.fit_left_of_tags(header(...))
  * hero content lives in y in [-2.2, 2.0]
  * the running "screen line" sits in a strip at y = -2.45 when the frame is dense
  * the "示意 / 出处" footnote sits at y in [-2.75, -2.2], right aligned, 16-17 pt
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import (
    DOWN, LEFT, RIGHT, UP, UL, UR, PI, TAU,
    FadeIn, FadeOut, Create, Indicate, Rotate, LaggedStart,
    Line, Arrow, Rectangle, RoundedRectangle, Circle, VGroup, DashedLine, DashedVMobject,
    Arc, Sector, ArcBetweenPoints, SurroundingRectangle,
)
from manim_lib.dvlib import (
    BG, FG, MUTED, GRID, PREFILL, DECODE, KV, SWA, WARN, EXPERT, DRAFT, GPU, CPU,
    T, M, Pill, DVScene, header, MiniMap, Block, TokenRow, window_bracket,
    code_panel, number_card, LayerStack, Scale,
)


class _E03(DVScene):
    """Small helpers shared by every EP03 shot."""

    def swap_line(self, old, new, run_time: float = 0.4):
        anims = [FadeIn(new)]
        if old is not None:
            anims.append(FadeOut(old))
        self.play(*anims, run_time=run_time)
        return new

    def foot(self, text: str, x: float = 6.55, y: float = -2.22, size: int = 16):
        """Right-aligned 示意/出处 footnote, two lines max, bottom stays above -2.75."""
        t = T(text, size, MUTED)
        t.move_to([x, y, 0], aligned_edge=UR)
        return t

    def foot_lines(self, lines, x: float = 6.55, y: float = -2.18, size: int = 16):
        g = VGroup(*[T(s, size, MUTED) for s in lines])
        g.arrange(DOWN, buff=0.06, aligned_edge=RIGHT)
        g.move_to([x, y, 0], aligned_edge=UR)
        return g


# ---------------------------------------------------------------- S01
class EP03_S01(_E03):
    SHOT = "EP03-S01"

    def construct(self):
        head = self.fit_left_of_tags(header("四十层，只有四层写块状 KV", "EP03 · S01 冷开场"))
        self.add(head)

        stack = LayerStack(40, split=20, colors=(PREFILL, DECODE), w=1.0, h=4.6).move_to([-5.35, -0.2, 0])

        frames = VGroup()
        for i in range(40):
            frames.add(Rectangle(width=0.62, height=0.072, stroke_color=MUTED, stroke_width=1,
                                 fill_color=MUTED, fill_opacity=0.22
                                 ).move_to([-4.5, stack.layer(i).get_y(), 0]))
        lamps = VGroup()
        for i in (2, 8, 14, 20):
            lamps.add(Rectangle(width=0.15, height=0.15, stroke_width=0,
                                fill_color=KV, fill_opacity=1.0
                                ).move_to([-4.02, stack.layer(i).get_y(), 0]))
        swa = VGroup()
        for i in range(40):
            swa.add(Rectangle(width=0.11, height=0.072, stroke_width=0,
                              fill_color=SWA, fill_opacity=0.95
                              ).move_to([-4.93, stack.layer(i).get_y(), 0]))

        src_y = {2: stack.layer(2).get_y(), 8: stack.layer(8).get_y(),
                 14: stack.layer(14).get_y(), 20: stack.layer(20).get_y()}
        arcs = VGroup()
        for a, b, s in ((3, 8, 2), (9, 14, 8), (15, 20, 14), (21, 40, 20)):
            for i in range(a, b):
                arcs.add(ArcBetweenPoints([-4.52, stack.layer(i).get_y(), 0],
                                          [-4.52, src_y[s], 0], angle=0.55,
                                          stroke_color=MUTED, stroke_width=1.2).set_stroke(opacity=0.45))

        l1 = T("40层模型输入数万词", 22, FG).move_to([1.35, 1.98, 0], aligned_edge=UL)
        l2 = T("仅第 2/8/14/20 层写块状KV", 22, FG).move_to([1.35, 1.34, 0], aligned_edge=UL)
        l3 = T("40层均写128窗口局部SWA", 22, FG).move_to([1.35, 0.70, 0], aligned_edge=UL)
        l4 = T("全局KV仅约 890 B/token", 22, KV).move_to([1.35, 0.06, 0], aligned_edge=UL)

        self.play(FadeIn(stack), run_time=1.0)
        self.play(FadeIn(l1), run_time=0.5)

        self.until("layers")
        self.play(FadeIn(frames), run_time=0.5)
        self.play(LaggedStart(*[frames[i].animate.set_fill(MUTED, 0.18) for i in range(40)
                                if i not in (2, 8, 14, 20)],
                              *[frames[i].animate.set_fill(KV, 0.65).set_stroke(KV) for i in (2, 8, 14, 20)],
                              lag_ratio=0.02), run_time=1.6)
        self.play(FadeIn(lamps), FadeIn(l2), run_time=0.6)

        self.until("alloc")
        self.play(LaggedStart(*[FadeIn(s) for s in swa], lag_ratio=0.02), run_time=1.6)
        pure = Pill("纯 SWA · 无全局分支", MUTED, size=16).move_to([-3.05, 1.95, 0])
        self.play(FadeIn(pure), FadeIn(l3), run_time=0.6)

        self.until("four")
        self.play(Indicate(lamps, color=KV, scale_factor=1.5), run_time=1.0)

        self.until("report")
        card = number_card("890", "B / token", "官方技术报告全局 KV 均摊（FP4格式）", color=KV)
        card.move_to([3.5, -1.3, 0])
        self.play(FadeIn(card), FadeIn(l4), run_time=0.8)

        self.until("bytes")
        self.play(FadeIn(arcs), run_time=1.2)
        decl = self.foot_lines(["示意：40 层竖排结构", "每层比例示意"], x=-1.2, y=-2.2)
        self.play(FadeIn(decl), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- S02
class EP03_S02(_E03):
    SHOT = "EP03-S02"

    def construct(self):
        num = T("EP03", 52, DECODE)
        title = T("先认识它服务的模型", 38, FG)
        tg = VGroup(num, title).arrange(DOWN, buff=0.25).move_to([0, 1.2, 0])
        mm = MiniMap(active="Prefill", scale=1.05).move_to([0, -1.05, 0])

        self.play(FadeIn(tg, shift=UP * 0.2), run_time=0.8)
        self.until("title")
        self.play(FadeIn(mm, shift=UP * 0.3), run_time=0.8)
        self.play(Indicate(mm.submobjects[0][2], color=DECODE, scale_factor=1.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- S03
class EP03_S03(_E03):
    SHOT = "EP03-S03"

    def construct(self):
        head = self.fit_left_of_tags(header("参数口径：总容量与主干参数", "EP03 · S03 两个口径"))
        self.add(head)

        scale = Scale("官方报告：552B", "权重元数据：763.2B", left_color=DECODE, right_color=EXPERT,
                      w=8.5, h=2.5, size=22).move_to([0, 0.45, 0])

        card_l = Block("主干参数：552B", DECODE, sub="纯 Backbone 结构", w=3.0, h=0.9, size=22)
        card_l.move_to([-4.25, -1.45, 0])
        card_r = Block("存储约 510 GB", EXPERT, sub="48 个 safetensors 分片", w=3.0, h=0.9, size=22)
        card_r.move_to([4.25, -1.45, 0])
        diff = Block("差额约 211B", MUTED, sub="196.9B 查表 + 14.2B 草稿 + 视觉", w=4.4, h=0.9, size=22, fill=1.0)
        diff.box.set_fill(BG, opacity=1.0)
        diff.move_to([0, 1.3, 0])

        slots = [-0.72, -1.17, -1.62, -2.07]
        s1 = T("权重元数据：763.2B 逻辑参数", 20, EXPERT).move_to([0, slots[0], 0])
        s2 = T("存储约 510 GB（48个分片）", 20, EXPERT).move_to([0, slots[1], 0])
        s3 = T("官方报告：552B 主干参数", 20, DECODE).move_to([0, slots[2], 0])
        s4 = T("差额来自查表·草稿与视觉", 20, MUTED).move_to([0, slots[3], 0])

        foot = self.foot_lines(["比例来自 work/calc/EP03_params.py", "763.2B 包含未分类小张量"],
                               x=6.55, y=-2.3)

        self.play(FadeIn(scale), run_time=0.8)

        self.until("balance")
        self.play(FadeIn(s1), FadeIn(s3), run_time=0.5)

        self.until("hf_total")
        self.play(scale.beam.animate.rotate(-0.05),
                  scale.right_pan.animate.shift(DOWN * 0.14),
                  scale.left_pan.animate.shift(UP * 0.14),
                  Indicate(scale.right_pan, color=EXPERT, scale_factor=1.03), run_time=0.9)

        self.until("storage")
        self.play(FadeIn(card_r), FadeIn(s2), run_time=0.7)

        self.until("report_backbone")
        self.play(FadeIn(card_l), Indicate(scale.left_pan, color=DECODE, scale_factor=1.03), run_time=0.7)

        self.until("backbone")
        bridge_l = DashedLine(diff.get_left() + LEFT * 0.05, scale.left_pan.get_top() + UP * 0.05,
                              color=MUTED, stroke_width=1.5)
        bridge_r = DashedLine(diff.get_right() + RIGHT * 0.05, scale.right_pan.get_top() + UP * 0.05,
                              color=MUTED, stroke_width=1.5)
        self.play(FadeIn(diff), Create(bridge_l), Create(bridge_r), FadeIn(s4), run_time=0.8)
        self.play(scale.beam.animate.rotate(0.05),
                  scale.right_pan.animate.shift(UP * 0.14),
                  scale.left_pan.animate.shift(DOWN * 0.14), run_time=0.8)
        self.play(FadeIn(foot), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- S04
class EP03_S04(_E03):
    SHOT = "EP03-S04"

    def construct(self):
        head = self.fit_left_of_tags(header("激活真相：全 MoE 与极端稀疏", "EP03 · S04 参数与激活"))
        self.add(head)

        col = RoundedRectangle(corner_radius=0.1, width=1.9, height=3.3, stroke_color=EXPERT,
                               stroke_width=2.5, fill_color=EXPERT, fill_opacity=0.06).move_to([-5.4, -0.35, 0])
        col_lbl = T("763.2B 总逻辑参数", 22, EXPERT).move_to([-5.4, 1.58, 0])

        cells = VGroup()
        for r in range(24):
            for c in range(16):
                x = -5.4 + (c - 7.5) * 0.08
                y = 0.0 + (11.5 - r) * 0.08
                cells.add(Rectangle(width=0.062, height=0.062, stroke_width=0,
                                    fill_color=GRID, fill_opacity=0.9).move_to([x, y, 0]))
        shared = Rectangle(width=1.25, height=0.13, stroke_width=0, fill_color=DECODE,
                           fill_opacity=0.9).move_to([-5.4, -1.35, 0])
        shared_lbl = T("共享专家", 16, DECODE).move_to([-5.4, -1.62, 0])

        act = Rectangle(width=0.32, height=0.30, stroke_width=0, fill_color=DECODE,
                        fill_opacity=0.95).move_to([-3.5, -1.85, 0])
        act_lbl = T("16.42B 激活", 18, DECODE).move_to([-3.5, -1.45, 0])

        card = number_card("2.15%", "激活比例", "每步激活 16.42B / 总参数 763.2B", color=DECODE)
        card.move_to([2.9, 0.95, 0])
        cap = Block("配置上限：1,048,576 Token", DECODE, sub="YaRN 扩展 factor=16", w=3.6, h=1.0, size=22)
        cap.move_to([2.9, -1.55, 0])

        strip = T("40层全MoE · 无Dense前缀", 20, FG).move_to([-2.2, -2.45, 0])
        foot = self.foot_lines(["按比例：激活量与专家数来自", "work/calc/EP03_params.py；1M 为配置上限"],
                               x=6.55, y=-2.22)

        self.play(FadeIn(col), FadeIn(col_lbl), FadeIn(strip), run_time=0.8)

        self.until("moe_all")
        self.play(FadeIn(cells), FadeIn(shared), FadeIn(shared_lbl), run_time=0.8)

        self.until("experts")
        self.play(cells.animate.set_fill(EXPERT, 0.25), run_time=0.4)
        self.play(cells.animate.set_fill(GRID, 0.9), run_time=0.6)

        self.until("routed")
        picked = [cells[3], cells[70], cells[140], cells[199], cells[261], cells[330]]
        self.play(*[c.animate.set_fill(EXPERT, 1.0) for c in picked], run_time=0.6)
        newr = T("384路由专家 · 每步激活6个", 20, EXPERT).move_to([-2.2, -2.45, 0])
        self.play(Indicate(VGroup(*picked), color=EXPERT, scale_factor=1.6),
                  FadeIn(newr), FadeOut(strip), run_time=0.7)
        strip = newr

        self.until("decode_act")
        newstrip = T("解码仅激活约 16.42B（2.15%）", 20, DECODE).move_to([-2.2, -2.45, 0])
        self.play(FadeIn(act), FadeIn(act_lbl), FadeIn(card), FadeIn(newstrip),
                  FadeOut(strip), run_time=0.8)
        strip = newstrip

        self.until("ratio")
        b1 = DashedLine([-4.35, -1.95, 0], [-3.7, -1.95, 0], color=DECODE, stroke_width=2)
        b2 = DashedLine([-4.35, -1.15, 0], [-4.35, -1.95, 0], color=DECODE, stroke_width=1.2)
        b3 = DashedLine([-3.7, -1.6, 0], [-3.7, -1.95, 0], color=DECODE, stroke_width=1.2)
        self.play(Create(b1), Create(b2), Create(b3), Indicate(act, color=DECODE, scale_factor=1.6), run_time=0.8)

        self.until("q_answer")
        newstrip2 = T("配置上限 1M（YaRN×16）", 20, DECODE).move_to([-2.2, -2.45, 0])
        self.play(FadeIn(cap), FadeIn(foot), FadeIn(newstrip2), FadeOut(strip), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------- S05
class EP03_S05(_E03):
    SHOT = "EP03-S05"

    def construct(self):
        head = self.fit_left_of_tags(header("查表巨物：两层近两千亿参数", "EP03 · S05 Engram 规模"))
        self.add(head)

        stack = LayerStack(20, split=20, colors=(PREFILL, PREFILL), w=0.9, h=4.4).move_to([-5.6, -0.2, 0])
        hi = VGroup()
        for i in (1, 14):
            hi.add(SurroundingRectangle(stack.layer(i), color=EXPERT, buff=0.03, stroke_width=3))
        conn = VGroup(*[Line(hi[k].get_right(), [hi[k].get_right()[0] + 0.5, hi[k].get_right()[1], 0],
                             color=EXPERT, stroke_width=2) for k in range(2)])

        pie_bg = Circle(radius=1.0, stroke_color=MUTED, stroke_width=2,
                        fill_color=MUTED, fill_opacity=0.12).move_to([0.6, 0.9, 0])
        pie = Sector(radius=1.0, start_angle=PI / 2, angle=0.258 * TAU, stroke_color=EXPERT,
                     stroke_width=1.5, fill_color=EXPERT, fill_opacity=0.5).move_to([0.6, 0.9, 0])
        plbl = T("25.8%", 22, EXPERT).move_to([0.12, 1.28, 0])
        pcap = T("Engram 查表含投影 196.9B", 18, MUTED).move_to([0.6, -0.45, 0])

        t1 = Block("Layer 1 表", EXPERT, sub="384,006,168 行 × 256 维 (FP8)", w=3.1, h=0.85, size=20)
        t1.move_to([4.8, 1.2, 0])
        t2 = Block("Layer 14 表", EXPERT, sub="384,016,682 行 × 256 维 (FP8)", w=3.1, h=0.85, size=20)
        t2.move_to([4.8, 0.1, 0])
        t3 = Block("投影权重 0.31B", EXPERT, sub="合计 196.9B", w=3.1, h=0.65, size=20)
        t3.move_to([4.8, -0.95, 0])

        pill = Pill("条件记忆模块 (Conditional Memory)", EXPERT, size=18).move_to([3.0, -1.95, 0])

        line1 = T("位于 Layer 1 与 14", 20, EXPERT).move_to([-2.8, -2.45, 0])
        line2 = T("查表参数 196.6B（FP8存储）", 20, EXPERT).move_to([-2.8, -2.45, 0])
        line3 = T("含投影 196.9B（占总数25.8%）", 20, EXPERT).move_to([-2.8, -2.45, 0])
        line4 = T("条件记忆 · 多阶哈希查表", 20, EXPERT).move_to([-2.8, -2.45, 0])
        foot = self.foot_lines(["按比例：196.93B / 763.2B", "来自 work/calc/EP03_params.py"],
                               x=6.55, y=-2.28)

        self.play(FadeIn(stack), FadeIn(line1), run_time=0.8)

        self.until("engram_pos")
        self.play(FadeIn(hi), FadeIn(conn), run_time=0.6)

        self.until("tables")
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.7)
        self.swap_line(line1, line2)
        cur = line2

        self.until("proj")
        self.play(FadeIn(t3), run_time=0.6)

        self.until("share")
        self.play(FadeIn(pie_bg), FadeIn(pie), FadeIn(plbl), FadeIn(pcap), run_time=0.8)
        self.swap_line(cur, line3)
        cur = line3

        self.until("name")
        self.play(FadeIn(pill), FadeIn(foot), run_time=0.6)
        self.swap_line(cur, line4)
        self.finish()


# ---------------------------------------------------------------- S06
class EP03_S06(_E03):
    SHOT = "EP03-S06"

    def construct(self):
        head = self.fit_left_of_tags(header("查表机制：每 token 24 行", "EP03 · S06 Engram 查表"))
        self.add(head)

        row = TokenRow(3, color=PREFILL, size=0.55, labels=["2g", "3g", "4g"]).move_to([-5.55, 1.05, 0])
        cap = VGroup(T("2-gram / 3-gram / 4-gram", 18, MUTED), T("多阶哈希输入", 18, MUTED))
        cap.arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([-5.6, 0.36, 0], aligned_edge=UL)

        hbox = RoundedRectangle(corner_radius=0.1, width=2.0, height=0.8, stroke_color=DECODE,
                                stroke_width=2, fill_color=DECODE, fill_opacity=0.08).move_to([-2.85, 1.1, 0])
        heads = VGroup(*[Rectangle(width=0.16, height=0.16, stroke_width=0, fill_color=DECODE,
                                   fill_opacity=0.85).move_to([-2.85 + (k - 3.5) * 0.2, 1.1, 0])
                         for k in range(8)])
        hlbl = T("8 哈希头", 16, DECODE).move_to([-2.85, 1.68, 0])

        idx = VGroup()
        for r in range(3):
            for c in range(8):
                idx.add(Rectangle(width=0.12, height=0.12, stroke_width=0, fill_color=DECODE,
                                  fill_opacity=0.7).move_to([-2.5 + (c - 3.5) * 0.19, 0.05 - r * 0.2, 0]))

        table = VGroup()
        for r in range(10):
            for c in range(12):
                table.add(Rectangle(width=0.2, height=0.2, stroke_width=0, fill_color=GRID,
                                    fill_opacity=0.9).move_to([1.5 + (c - 5.5) * 0.22, 1.55 - r * 0.22, 0]))
        tborder = DashedVMobject(Rectangle(width=2.75, height=2.32, stroke_color=MUTED, stroke_width=1.5),
                                 num_dashes=44).move_to([1.5, 0.56, 0])
        tlbl = T("rank 分片表", 16, MUTED).move_to([1.5, 1.86, 0])
        size_t = T("24 行 × 256 维 (FP8) ≈ 6,144 浮点值", 18, EXPERT).move_to([1.6, -0.95, 0])

        res = VGroup(*[Line([4.35, y, 0], [5.6, y, 0], color=MUTED, stroke_width=5).set_stroke(opacity=0.85)
                       for y in (1.2, 0.7, 0.2, -0.3)])
        res_lbl = T("4 路残差主干", 16, MUTED).move_to([4.95, -0.72, 0])
        inject = Arrow([2.9, 0.45, 0], [4.28, 0.45, 0], color=MUTED, stroke_width=3,
                       max_tip_length_to_length_ratio=0.15)

        gemm = T("Dense GEMM", 18, MUTED).move_to([5.0, -1.55, 0])
        gemm_x = Line([4.35, -1.55, 0], [5.65, -1.55, 0], color=WARN, stroke_width=3)
        gemm_mark = T("✗", 30, WARN).move_to([3.95, -1.55, 0])

        l1 = T("3阶×8头 = 24行/Engram层", 20, FG).move_to([-2.2, -2.45, 0])
        foot = self.foot_lines(["示意：切分表格与哈希拉取过程示意", "行数比例非实际比例"], x=6.55, y=-2.2)

        self.play(FadeIn(row), FadeIn(cap), FadeIn(l1), run_time=0.8)

        self.until("lookup24")
        self.play(FadeIn(hbox), FadeIn(heads), FadeIn(hlbl), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(s) for s in idx], lag_ratio=0.03), run_time=1.0)

        self.until("heads")
        newlbl = T("每行256维 · 单词读6k值", 20, FG).move_to([-2.2, -2.45, 0])
        self.play(FadeIn(table), FadeIn(tborder), FadeIn(tlbl), FadeIn(size_t),
                  FadeIn(newlbl), FadeOut(l1), run_time=0.8)
        l1 = newlbl

        self.until("fetch")
        rows24 = VGroup(*[c for c in table if abs(c.get_y() - (1.55 - 8 * 0.22)) < 0.02
                          or abs(c.get_y() - (1.55 - 9 * 0.22)) < 0.02])
        rows24_ids = {id(c) for c in rows24}
        self.play(*[c.animate.set_fill(EXPERT, 1.0) for c in rows24], run_time=0.8)
        self.play(Indicate(size_t, color=EXPERT), run_time=0.6)

        self.until("dist")
        pk1 = DashedLine([-2.05, -0.1, 0], [-0.2, 0.35, 0], color=MUTED, stroke_width=2)
        pk2 = DashedLine([-2.05, -0.45, 0], [-0.2, 0.05, 0], color=MUTED, stroke_width=2)
        net = Pill("跨卡 / 跨 rank", MUTED, size=16).move_to([-1.35, -1.0, 0])
        newlbl = T("跨卡/跨rank拉取", 20, FG).move_to([-2.2, -2.45, 0])
        self.play(Create(pk1), Create(pk2), FadeIn(net), FadeIn(newlbl), FadeOut(l1), run_time=0.7)
        l1 = newlbl

        self.until("sparse")
        self.play(*[c.animate.set_fill(MUTED, 0.12) for c in table if id(c) not in rows24_ids], run_time=1.0)
        newlbl = T("无百亿规模密集GEMM", 20, FG).move_to([-2.2, -2.45, 0])
        self.play(FadeIn(gemm), Create(gemm_x), FadeIn(gemm_mark), FadeIn(newlbl), FadeOut(l1), run_time=0.6)
        l1 = newlbl

        self.until("hook")
        self.play(Create(inject), FadeIn(res), FadeIn(res_lbl), FadeIn(foot), run_time=0.8)
        self.play(Indicate(res, color=DECODE), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- S07
class EP03_S07(_E03):
    SHOT = "EP03-S07"

    def construct(self):
        head = self.fit_left_of_tags(header("残差主干：Single-Pass mHC", "EP03 · S07 超连接"))
        self.add(head)

        trunk = Line([-6.4, 0.0, 0], [-4.85, 0.0, 0], color=MUTED, stroke_width=8).set_stroke(opacity=0.85)
        node = Circle(radius=0.09, stroke_width=0, fill_color=MUTED, fill_opacity=0.9).move_to([-4.85, 0, 0])
        lanes = VGroup()
        for y in (1.15, 0.38, -0.38, -1.15):
            lanes.add(Line([-4.85, 0, 0], [-4.25, y, 0], color=MUTED, stroke_width=4).set_stroke(opacity=0.8))
            lanes.add(Line([-4.25, y, 0], [0.35, y, 0], color=MUTED, stroke_width=4).set_stroke(opacity=0.8))
            lanes.add(Line([3.45, y, 0], [5.5, y, 0], color=MUTED, stroke_width=4).set_stroke(opacity=0.8))

        mhc_pill = Pill("Single-Pass mHC (Hyper-Connections)", DECODE, size=18).move_to([4.0, 1.85, 0])
        hc = M("hc_mult = 4", 20, DECODE).move_to([-3.4, 1.6, 0])
        mat = Block("4×4 动态混合矩阵", DECODE, sub="权重 24×20480 (FP32)", w=3.0, h=1.4, size=22)
        mat.move_to([1.9, 0.0, 0])
        ring = Arc(radius=1.62, start_angle=0.15, angle=TAU - 0.5, arc_center=[1.9, 0, 0],
                   stroke_color=DECODE, stroke_width=2.5).set_stroke(opacity=0.8)
        ring_lbl = T("20 次 Sinkhorn 归一化（双随机矩阵）", 18, DECODE).move_to([2.0, -1.8, 0])

        hook = Rectangle(width=0.3, height=2.75, stroke_color=EXPERT, stroke_width=2,
                         fill_color=EXPERT, fill_opacity=0.18).move_to([-3.2, 0.0, 0])
        hook_lbl = T("Engram Hook（Layer 1 / 14）", 16, EXPERT).move_to([-3.15, -1.62, 0])

        strip = T("Single-Pass mHC 残差", 20, FG).move_to([-2.2, -2.45, 0])
        foot = self.foot("示意：4 路超连接与归一化流程示意", x=6.55, y=-2.5)

        self.play(FadeIn(trunk), FadeIn(node), FadeIn(strip), run_time=0.8)

        self.until("mhc_overview")
        new = T("残差主干扩展为 4 路数据流", 20, FG).move_to([-2.2, -2.45, 0])
        self.play(Create(lanes), FadeIn(new), FadeOut(strip), run_time=1.0)
        strip = new

        self.until("mhc_title")
        self.play(FadeIn(mhc_pill), run_time=0.6)

        self.until("mult4")
        self.play(FadeIn(hc), Indicate(lanes, color=DECODE), run_time=0.7)

        self.until("matrix")
        self.play(FadeIn(mat), FadeIn(ring), run_time=0.8)

        self.until("sinkhorn")
        self.play(Rotate(ring, angle=TAU * 0.9, about_point=[1.9, 0, 0]), run_time=1.8)
        new = T("20 次 Sinkhorn 双随机归一化", 20, FG).move_to([-2.2, -2.45, 0])
        self.play(FadeIn(ring_lbl), FadeIn(new), FadeOut(strip), run_time=0.6)
        strip = new

        # no cue for the Engram hook (storyboard notes it is still missing); play with the narration tail
        self.play(FadeIn(hook), FadeIn(hook_lbl), run_time=0.8)
        pre = Block("pre 内核", EXPERT, w=1.25, h=0.5, size=16).move_to([-4.9, -1.85, 0])
        post = Block("post 内核", EXPERT, w=1.35, h=0.5, size=16).move_to([-1.5, -1.85, 0])
        new = T("遇 Engram 钩子拆分内核调用", 20, FG).move_to([-2.2, -2.45, 0])
        self.play(FadeIn(pre), FadeIn(post), FadeIn(foot), run_time=0.6)
        self.play(FadeIn(new), FadeOut(strip), run_time=0.5)
        self.play(Indicate(VGroup(pre, post), color=EXPERT), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------- S08
class EP03_S08(_E03):
    SHOT = "EP03-S08"

    def construct(self):
        head = self.fit_left_of_tags(header("注意力骨架：全 SWA", "EP03 · S08 局部注意力"))
        self.add(head)

        stack = LayerStack(40, split=20, colors=(PREFILL, DECODE), w=1.0, h=4.6).move_to([-5.5, -0.2, 0])
        ticks = VGroup(*[Rectangle(width=0.1, height=0.07, stroke_width=0, fill_color=SWA,
                                   fill_opacity=0.95).move_to([-4.93, stack.layer(i).get_y(), 0])
                         for i in range(40)])

        row = TokenRow(16, color=PREFILL, size=0.26, gap=0.05).move_to([2.3, 1.0, 0])
        bracket = window_bracket(row, 8, 15, color=SWA,
                                 label="窗口 128：本位置 + 左侧 127 邻居")

        snippet = ('# cache_engine.py:695-699\n'
                   '@staticmethod\n'
                   'def _is_full(cfg: dict | None) -> bool:\n'
                   '    return (ratio == 0 and\n'
                   '            sink_mode != "swa")')
        code = code_panel(snippet, "deepinfer/worker/cache_engine.py:695", highlight=[4, 5], size=16, width=5.6)
        code.move_to([2.5, -0.85, 0])

        old = VGroup()
        for k in range(3):
            old.add(TokenRow(6, color=[MUTED] * 6, size=0.16, gap=0.04))
        old.arrange(DOWN, buff=0.07).move_to([-3.7, -1.72, 0])
        old_lbl = T("传统：局部 + 全量", 16, MUTED).move_to([-3.7, -2.2, 0])

        strip = T("主干 40 层全部具备 SWA", 20, FG).move_to([0.8, -2.5, 0])
        foot = self.foot_lines(["示意：Token 行中 8 格", "代表 128 个 token"], x=6.55, y=-2.35)

        self.play(FadeIn(stack), FadeIn(strip), run_time=0.9)

        self.until("swa_all")
        self.play(LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.02), run_time=1.6)

        self.until("contrast")
        self.play(FadeIn(old), FadeIn(old_lbl), run_time=0.6)

        self.until("all_swa")
        self.play(Indicate(ticks, color=SWA, scale_factor=1.0), run_time=1.0)
        self.play(FadeOut(old), FadeOut(old_lbl), run_time=0.5)

        self.until("win128")
        new = T("局部注意力可见窗口 128", 20, SWA).move_to([0.8, -2.5, 0])
        self.play(FadeIn(row), Create(bracket), FadeIn(foot), FadeIn(new), FadeOut(strip), run_time=0.8)
        strip = new

        self.until("no_full")
        new = T("无传统全量注意力层", 20, SWA).move_to([0.8, -2.5, 0])
        self.play(FadeIn(code), FadeIn(new), FadeOut(strip), run_time=0.8)
        strip = new

        # question line waits for the narration question (storyboard r2 note 11)
        q = T("长程依赖如何跨层建立？", 20, FG).move_to([0.8, -2.5, 0])
        self.play(Indicate(bracket, color=SWA), run_time=0.8)
        self.play(FadeIn(q), FadeOut(strip), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- S09
class EP03_S09(_E03):
    SHOT = "EP03-S09"

    def construct(self):
        head = self.fit_left_of_tags(header("结构密码：compress_ratios", "EP03 · S09 压缩率数组"))
        self.add(head)

        cols = []
        for i in range(43):
            if i < 2:
                cols.append(MUTED)
            elif i < 20:
                cols.append(PREFILL)
            elif i < 40:
                cols.append(DECODE)
            else:
                cols.append(DRAFT)
        tiles = VGroup(*[Rectangle(width=0.26, height=0.62, stroke_width=1, stroke_color=BG,
                                   fill_color=cols[i], fill_opacity=0.85
                                   ).move_to([(i - 21) * 0.29, 0.9, 0]) for i in range(43)])

        h1 = T("2 项 0", 16, MUTED).move_to([(0.5 - 21) * 0.29, 1.45, 0])
        h2 = T("18 项 2", 16, PREFILL).move_to([(10.5 - 21) * 0.29, 1.45, 0])
        h3 = T("20 项 1", 16, DECODE).move_to([(29.5 - 21) * 0.29, 1.45, 0])
        h4 = T("3 项 0", 16, DRAFT).move_to([(41 - 21) * 0.29, 1.45, 0])

        c1 = Block("[0, 0]", MUTED, sub="Layer 0-1 纯 SWA", w=2.4, h=0.9, size=20).move_to([-4.85, -1.5, 0])
        c2 = Block("18 个 2", PREFILL, sub="Layer 2-19 2:1 压缩", w=2.4, h=0.9, size=20).move_to([-1.95, -1.5, 0])
        c3 = Block("20 个 1", DECODE, sub="L20产/L21-39复用", w=2.4, h=0.9, size=20).move_to([1.15, -1.5, 0])
        c4 = Block("末尾 3 个 0", DRAFT, sub="3 个草稿层 (DFlash)", w=2.4, h=0.9, size=20).move_to([4.3, -1.5, 0])

        cut = DashedLine([-0.435, -0.6, 0], [-0.435, 2.05, 0], color=EXPERT, stroke_width=3)
        cut_lbl = T("编码器 / 解码器 架构分水岭", 18, EXPERT).move_to([0.9, 1.9, 0])

        strip = T("压缩率数组共 43 项", 20, FG).move_to([-3.2, -2.45, 0])
        foot = self.foot_lines(["示意：43 项磁贴示意；后 3 项对应", "辅助草稿层，主干共 40 层"],
                               x=6.55, y=-2.26)

        self.play(LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.015), FadeIn(strip), run_time=1.2)
        self.play(FadeIn(h1), FadeIn(h2), FadeIn(h3), FadeIn(h4), run_time=0.5)

        self.until("ratios_array")
        self.play(Indicate(tiles[20], color=FG, scale_factor=1.0), run_time=1.0)

        self.until("zeros")
        new = T("[0,0]：L0-1 纯SWA", 20, MUTED).move_to([-3.2, -2.45, 0])
        self.play(tiles[0].animate.shift(UP * 0.12), tiles[1].animate.shift(UP * 0.12),
                  FadeIn(c1), FadeIn(new), FadeOut(strip), run_time=0.7)
        strip = new

        self.until("twos")
        new = T("18个2：L2-19 压缩", 20, PREFILL).move_to([-3.2, -2.45, 0])
        self.play(*[tiles[i].animate.shift(UP * 0.12) for i in range(2, 20)],
                  FadeIn(c2), FadeIn(new), FadeOut(strip), run_time=0.9)
        strip = new

        self.until("ones")
        new = T("20个1：L20产/L21-39复用", 20, DECODE).move_to([-3.2, -2.45, 0])
        self.play(*[tiles[i].animate.shift(UP * 0.12) for i in range(20, 40)],
                  FadeIn(c3), FadeIn(new), FadeOut(strip), run_time=0.9)
        strip = new

        self.until("draft_zeros")
        lbl = T("草稿层（不参与主干建层）", 16, DRAFT).move_to([5.2, 1.9, 0])
        self.play(*[tiles[i].animate.shift(RIGHT * 0.18) for i in range(40, 43)],
                  FadeIn(c4), FadeIn(lbl), run_time=0.7)

        self.until("q_reason")
        self.play(Create(cut), FadeIn(cut_lbl), FadeIn(foot), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------- S10
class EP03_S10(_E03):
    SHOT = "EP03-S10"

    def construct(self):
        head = self.fit_left_of_tags(header("结构分水岭：CED 体系", "EP03 · S10 编码器与解码器"))
        self.add(head)

        stack = LayerStack(40, split=20, colors=(PREFILL, DECODE), w=0.8, h=4.4).move_to([-5.9, -0.2, 0])
        lbl_enc = stack.range_label(0, 20, "因果编码器 (Causal Encoder)", side=RIGHT, color=PREFILL, size=18)
        lbl_dec = stack.range_label(20, 40, "解码器 (Decoder)", side=RIGHT, color=DECODE, size=18)
        l20 = SurroundingRectangle(stack.layer(20), color=DECODE, buff=0.05, stroke_width=3.5)

        cache = Block("共享全局 KV 缓存 (ca_cache)", KV, sub="来自 Layer 20 单次全长投影", w=4.2, h=1.2, size=20)
        cache.move_to([1.8, 0.85, 0])
        proj = Arrow([-5.5, stack.layer(20).get_y(), 0], [cache.get_left()[0] - 0.05, 0.75, 0],
                     color=KV, stroke_width=3.5, max_tip_length_to_length_ratio=0.1)
        yoco = Pill("灵感来源：YOCO 架构", MUTED, size=18).move_to([3.6, 1.92, 0])

        reads = VGroup(*[Arrow([-5.5, y, 0], [-0.35, 0.42, 0], color=MUTED,
                               stroke_width=1.8, max_tip_length_to_length_ratio=0.12).set_stroke(opacity=0.55)
                         for y in (-0.62, -0.92)])
        free = Pill("免除自身块状 KV 计算", MUTED, size=16).move_to([1.9, -0.05, 0])
        diff = Block("报告：每层专属投影权重", MUTED, sub="开源：单份投影复用", w=4.8, h=1.0, size=18)
        diff.move_to([2.4, -1.55, 0])

        strip = T("CED：因果编码器-解码器", 20, FG).move_to([-3.2, -2.45, 0])
        foot = self.foot_lines(["示意：CED 结构示意；开源实现为", "单份投影复用"], x=6.55, y=-2.3)

        self.play(FadeIn(stack), FadeIn(strip), run_time=0.9)
        self.play(FadeIn(lbl_enc), FadeIn(lbl_dec), run_time=0.6)

        self.until("ced_overview")
        new = T("Layer 0-19 编码器处理全长", 20, PREFILL).move_to([-3.2, -2.45, 0])
        self.play(FadeIn(l20), FadeIn(new), FadeOut(strip), run_time=0.7)
        strip = new

        self.until("ced_name")
        self.play(FadeIn(yoco), run_time=0.5)

        self.until("encoder")
        self.play(Indicate(lbl_enc, color=PREFILL), FadeIn(proj), run_time=0.8)

        self.until("layer20")
        new = T("Layer 20 统一投影全局KV", 20, DECODE).move_to([-3.2, -2.45, 0])
        self.play(Indicate(lbl_dec, color=DECODE, scale_factor=1.04),
                  Indicate(l20, color=EXPERT, scale_factor=1.06), FadeIn(new), FadeOut(strip), run_time=0.7)
        strip = new

        self.until("source")
        self.play(FadeIn(cache), FadeIn(free), run_time=0.7)

        self.until("proj_caveat")
        new = T("Layer 21-39 复用第20层投影", 20, DECODE).move_to([-3.2, -2.45, 0])
        self.play(Create(reads), FadeIn(diff), FadeIn(new), FadeOut(strip), run_time=0.9)
        self.play(FadeIn(foot), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- S11
class EP03_S11(_E03):
    SHOT = "EP03-S11"

    def construct(self):
        head = self.fit_left_of_tags(header("潜在注意力：MLA 拓扑", "EP03 · S11 64 头共享 KV"))
        self.add(head)

        heads = VGroup(*[Rectangle(width=0.11, height=0.11, stroke_width=0, fill_color=PREFILL,
                                   fill_opacity=0.8).move_to([-5.95 + (c - 3.5) * 0.15, 0.75 - r * 0.15, 0])
                          for r in range(8) for c in range(8)])
        heads_lbl = T("64 个 Q 头", 16, PREFILL).move_to([-5.65, -0.62, 0])
        fan = VGroup(*[Line([-5.3, 0.75 - r * 0.15, 0], [-4.2, 0.6, 0], color=PREFILL,
                            stroke_width=1.2).set_stroke(opacity=0.5) for r in range(8)])
        qnode = Block("Q 低秩 1280 维", PREFILL, w=2.2, h=0.7, size=18).move_to([-3.0, 0.6, 0])
        qexp = T("再升维 64 头", 16, PREFILL).move_to([-3.0, -0.15, 0])

        kv_pipe = Line([-1.3, -1.1, 0], [0.35, 0.55, 0], color=KV, stroke_width=7).set_stroke(opacity=0.9)
        kv_lbl = M("num_key_value_heads = 1", 18, KV).move_to([-2.1, -1.25, 0])

        lat = Rectangle(width=4.4, height=0.85, stroke_color=KV, stroke_width=2.5,
                        fill_color=KV, fill_opacity=0.45).move_to([2.7, 0.85, 0])
        rope = Rectangle(width=0.55, height=0.85, stroke_color=MUTED, stroke_width=2.5,
                         fill_color=MUTED, fill_opacity=0.55).move_to([4.625, 0.85, 0])
        nope_lbl = T("448 维 NoPE 内容向量 (kv_lora_rank=448)", 16, KV).move_to([2.4, 0.05, 0])
        rope_lbl = T("64 维 RoPE 位置编码", 16, MUTED).move_to([4.3, 1.55, 0])

        snippet = "assert self.num_lora_rope_head == 1"
        code = code_panel(snippet, "deepinfer/model_executor/models/\nv4_modules/mla_attn.py:175-180",
                          highlight=[1], size=18, width=4.8)
        code.move_to([2.6, -1.35, 0])

        strip = T("64 个Q头 · 1条KV头", 20, FG).move_to([-3.0, -2.45, 0])
        foot = self.foot_lines(["按比例：512 维分解为 448 维", "NoPE 与 64 维 RoPE"], x=6.55, y=-2.2)

        self.play(FadeIn(heads), FadeIn(heads_lbl), FadeIn(strip), run_time=0.8)

        self.until("mla_overview")
        self.play(FadeIn(fan), FadeIn(qnode), FadeIn(qexp), FadeIn(kv_pipe), run_time=0.8)

        self.until("mqa_assert")
        self.play(FadeIn(code), FadeIn(kv_lbl), run_time=0.7)

        self.until("dim512")
        new = T("共享 512 维 KV Latent", 20, KV).move_to([-3.0, -2.45, 0])
        self.play(FadeIn(lat), FadeIn(rope), FadeIn(new), FadeOut(strip), run_time=0.8)
        strip = new

        self.until("nope")
        new = T("448 维内容 + 64 维位置编码", 20, KV).move_to([-3.0, -2.45, 0])
        self.play(Indicate(lat, color=KV, scale_factor=1.02), FadeIn(nope_lbl), FadeIn(new),
                  FadeOut(strip), run_time=0.7)
        strip = new

        self.until("rope")
        self.play(Indicate(rope, color=MUTED, scale_factor=1.3), FadeIn(rope_lbl), run_time=0.8)

        self.until("q_lora")
        new = T("显著压缩KV访存量", 20, KV).move_to([-3.0, -2.45, 0])
        self.play(FadeIn(foot), Indicate(qnode, color=PREFILL), FadeIn(new), FadeOut(strip), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------- S12
class EP03_S12(_E03):
    SHOT = "EP03-S12"

    def construct(self):
        head = self.fit_left_of_tags(header("块状 KV 来源：仅此 4 层", "EP03 · S12 四源层"))
        self.add(head)

        stack = LayerStack(40, split=20, colors=(PREFILL, DECODE), w=0.9, h=4.6).move_to([-5.7, -0.2, 0])
        src = (2, 8, 14, 20)
        boxes = VGroup(*[SurroundingRectangle(stack.layer(i), color=KV, buff=0.04, stroke_width=3) for i in src])
        chips = VGroup()
        for i in src:
            y = stack.layer(i).get_y()
            chips.add(Rectangle(width=0.85, height=0.17, stroke_color=KV, stroke_width=1.5,
                                fill_color=KV, fill_opacity=0.45).move_to([-4.55, y, 0]))
            chips.add(T("PackedWkv", 16, KV).move_to([-3.55, y, 0]))

        def _arcs(layers, target):
            g = VGroup()
            ty = stack.layer(target).get_y()
            for i in layers:
                g.add(ArcBetweenPoints([-4.9, stack.layer(i).get_y(), 0], [-4.9, ty, 0], angle=0.5,
                                       stroke_color=MUTED, stroke_width=1.1).set_stroke(opacity=0.5))
            return g

        enc_arcs = VGroup(_arcs(range(3, 8), 2), _arcs(range(9, 14), 8), _arcs(range(15, 20), 14))
        dec_arcs = _arcs(range(21, 40), 20)

        wcard = VGroup(
            RoundedRectangle(corner_radius=0.1, width=4.4, height=1.1, stroke_color=GRID, stroke_width=1.5,
                             fill_color=GRID, fill_opacity=0.14),
            M("attn.compressor.*", 18, KV),
        )
        wcard[1].move_to(wcard[0]).shift(UP * 0.18)
        wcard.add(T("权重索引：仅这 4 层存在", 16, MUTED).move_to(wcard[0]).shift(DOWN * 0.2))
        wcard.move_to([2.3, 1.2, 0])

        pure = Pill("纯 SWA (无全局分支)", MUTED, size=16).move_to([-1.0, 2.05, 0])
        swa_pill = Pill("40 层各独立写 128 局部 SWA", SWA, size=18).move_to([2.3, -1.2, 0])

        strip = T("仅 4 层产块状KV", 20, FG).move_to([-3.4, -2.45, 0])
        foot = self.foot("示意：40 层复用连接拓扑示意", x=6.55, y=-2.45)

        self.play(FadeIn(stack), FadeIn(strip), run_time=0.9)

        self.until("compressor_4")
        self.play(FadeIn(boxes), FadeIn(chips), run_time=0.8)

        self.until("weights")
        self.play(FadeIn(wcard), run_time=0.6)

        self.until("pure_swa")
        new = T("34层复用源层 · 2层纯SWA", 20, MUTED).move_to([-3.4, -2.45, 0])
        self.play(FadeIn(pure), FadeIn(new), FadeOut(strip), run_time=0.7)
        strip = new

        self.until("reuse_enc")
        self.play(FadeIn(enc_arcs), run_time=0.9)

        self.until("reuse20")
        new = T("L21-39 复用第20层缓存", 20, KV).move_to([-3.4, -2.45, 0])
        self.play(FadeIn(dec_arcs), FadeIn(new), FadeOut(strip), run_time=1.0)
        strip = new

        self.until("q_answer")
        new = T("局部 SWA 仍由每层独立维护", 20, SWA).move_to([-3.4, -2.45, 0])
        self.play(FadeIn(swa_pill), FadeIn(new), FadeOut(strip), run_time=0.7)
        self.play(FadeIn(foot), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- S13
class EP03_S13(_E03):
    SHOT = "EP03-S13"

    def construct(self):
        head = self.fit_left_of_tags(header("稀疏索引：8 个 indexer", "EP03 · S13 top-512"))
        self.add(head)

        stack = LayerStack(40, split=20, colors=(PREFILL, DECODE), w=0.9, h=4.4).move_to([-5.75, -0.1, 0])
        full = (2, 8, 14, 20)
        reindex = (24, 28, 32, 36)
        marks = VGroup()
        for i in range(40):
            if i in full:
                col = KV
            elif i in reindex:
                col = DECODE
            elif i < 2:
                col = MUTED
            else:
                col = GRID
            marks.add(Rectangle(width=0.14, height=0.07, stroke_width=0, fill_color=col,
                                fill_opacity=0.95 if col != GRID else 0.6
                                ).move_to([-5.12, stack.layer(i).get_y(), 0]))

        lg = VGroup(
            Pill("4 层 Full Indexer", KV, size=16),
            Pill("4 层 Reindex", DECODE, size=16),
            Pill("30 层 Reuse", MUTED, size=16),
            Pill("2 层纯 SWA", MUTED, size=16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        lg.move_to([-4.3, 0.95, 0], aligned_edge=UL)

        pool = DashedVMobject(Rectangle(width=4.0, height=2.3, stroke_color=DECODE, stroke_width=2),
                              num_dashes=52).move_to([2.6, 0.35, 0])
        dots = VGroup()
        for r in range(12):
            for c in range(20):
                dots.add(Rectangle(width=0.09, height=0.09, stroke_width=0, fill_color=GRID,
                                   fill_opacity=0.85).move_to([2.6 + (c - 9.5) * 0.17, 1.28 - r * 0.17, 0]))
        pool_lbl = T("Decoder 候选池：2,048 数据块 × 8 = 16,384 位置", 16, DECODE).move_to([2.6, 1.75, 0])
        topk = VGroup(*[dots[k] for k in (12, 34, 55, 78, 99, 120, 141, 162, 183, 204, 225, 230,
                                          15, 40, 63, 88, 110, 132, 155, 177, 199, 220, 236, 3)])
        formula = T("8 + 30 + 2 = 40", 24, FG).move_to([2.6, -1.55, 0])

        strip = T("8层带Indexer · 30层复用", 20, FG).move_to([-3.0, -2.45, 0])
        foot = self.foot_lines(["按比例：候选池 2,048 块 × 8 = 16,384 位置", "top-512 为压缩 token 数"],
                               x=6.55, y=-2.24)

        self.play(FadeIn(stack), FadeIn(marks), FadeIn(lg), FadeIn(strip), run_time=0.9)

        self.until("indexer_overview")
        self.play(Indicate(VGroup(*[marks[i] for i in full + reindex]), color=FG), run_time=0.9)

        self.until("full_idx")
        self.play(Indicate(VGroup(*[marks[i] for i in full]), color=KV, scale_factor=1.6), run_time=0.9)

        self.until("reindex")
        new = T("另2层纯SWA · 凑齐40层主干", 20, DECODE).move_to([-3.0, -2.45, 0])
        self.play(Indicate(VGroup(*[marks[i] for i in reindex]), color=DECODE, scale_factor=1.6),
                  FadeIn(new), FadeOut(strip), run_time=0.9)
        strip = new

        self.until("reuse_main")
        self.play(Indicate(marks[20], color=KV, scale_factor=1.8), run_time=0.8)

        self.until("reuse_idx")
        self.play(FadeIn(formula), run_time=0.7)

        self.until("candidate")
        new1 = T("8个检索层筛选 top-512", 20, FG).move_to([-3.0, -2.45, 0])
        self.play(FadeIn(pool), FadeIn(dots), FadeIn(pool_lbl), run_time=0.9)
        new2 = T("Decoder 候选池 16k位置", 18, DECODE).move_to([2.6, -1.15, 0])
        self.play(LaggedStart(*[d.animate.set_fill(EXPERT, 1.0) for d in topk], lag_ratio=0.02),
                  FadeIn(new1), FadeIn(new2), FadeOut(strip), run_time=1.1)
        self.play(FadeIn(foot), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- S14
class EP03_S14(_E03):
    SHOT = "EP03-S14"

    def construct(self):
        head = self.fit_left_of_tags(header("算式揭晓：890 B/token 账本", "EP03 · S14 精确算式"))
        self.add(head)

        base = -1.9
        unit = 1.5 / 178.0
        xs = (-4.6, -3.5, -2.4, -1.0)
        spec = [(144, 34), (144, 34), (144, 34), (288, 68)]
        bars = VGroup()
        for x, (kv_b, idx_b) in zip(xs, spec):
            kv = Rectangle(width=0.7, height=kv_b * unit, stroke_width=0, fill_color=KV,
                           fill_opacity=0.85).move_to([x, base + kv_b * unit / 2, 0])
            idx = Rectangle(width=0.7, height=idx_b * unit, stroke_width=0, fill_color=DECODE,
                            fill_opacity=0.85).move_to([x, base + kv_b * unit + idx_b * unit / 2, 0])
            bars.add(VGroup(kv, idx))
        lbls = VGroup(*[T(s, 16, MUTED).move_to([x, -2.08, 0]) for x, s in zip(xs, ("L2", "L8", "L14", "L20"))])
        totals = VGroup(*[T(s, 16, FG).move_to([x, base + h + 0.18, 0])
                          for x, s, h in zip(xs, ("178 B", "178 B", "178 B", "356 B"),
                                             (178 * unit, 178 * unit, 178 * unit, 356 * unit))])

        panel_bg = RoundedRectangle(corner_radius=0.12, width=6.0, height=1.85, stroke_color=GRID,
                                    stroke_width=1.5, fill_color=GRID, fill_opacity=0.14)
        panel_bg.move_to([3.55, 1.18, 0])
        p1 = T("3 × (288 + 68) / 2 = 534 B", 18, KV).move_to([3.55, 1.62, 0])
        p2 = T("1 × (288 + 68) / 1 = 356 B", 18, KV).move_to([3.55, 1.2, 0])
        p3 = T("主 KV: 720 B · 检索 K: 170 B · 合计 890 B", 18, FG).move_to([3.55, 0.75, 0])

        card = number_card("890", "B / token", "3 × 178 B + 1 × 356 B（精确吻合）", color=KV)
        card.move_to([3.7, -1.0, 0])

        strip = T("每压缩token：288B+68B", 20, FG).move_to([-3.0, -2.45, 0])
        foot = self.foot_lines(["计算来自 work/calc/EP03_kv_bytes.py", "精确吻合官方报告摘要 890 B/token"],
                               x=6.55, y=-2.24)

        self.play(FadeIn(panel_bg), FadeIn(p1), FadeIn(strip), run_time=0.8)

        self.until("math_intro")
        self.play(FadeIn(bars[3]), run_time=0.7)

        self.until("fp4_main")
        self.play(Indicate(bars[3][0], color=KV, scale_factor=1.05), run_time=0.8)

        self.until("fp4_index")
        self.play(Indicate(bars[3][1], color=DECODE, scale_factor=1.3), FadeIn(p2), run_time=0.8)

        self.until("c2_share")
        new = T("3个C2源层：3×178B=534B", 20, FG).move_to([-3.0, -2.45, 0])
        self.play(*[FadeIn(b) for b in bars[:3]], FadeIn(lbls), FadeIn(totals),
                  FadeIn(new), FadeOut(strip), run_time=0.9)
        strip = new

        self.until("c1_share")
        new = T("第20层源层：1×356B=356B", 20, FG).move_to([-3.0, -2.45, 0])
        self.play(Indicate(bars[3], color=KV, scale_factor=1.03), FadeIn(new), FadeOut(strip), run_time=0.8)
        strip = new

        self.until("sum890")
        new = T("精确合计：890 B/token", 20, KV).move_to([-3.0, -2.45, 0])
        self.play(FadeIn(card), FadeIn(p3), FadeIn(new), FadeOut(strip), run_time=0.9)
        strip = new

        self.until("breakdown")
        self.play(FadeIn(foot), Indicate(bars, color=KV, scale_factor=1.0), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- S15
class EP03_S15(_E03):
    SHOT = "EP03-S15"

    def construct(self):
        head = self.fit_left_of_tags(header("另一种记忆：SWA 状态槽", "EP03 · S15 固定开销"))
        self.add(head)

        blocks = VGroup(*[Block("128 Token 块", KV, sub="113,920 字节", w=1.6, h=1.35, size=16)
                          .move_to([x, 1.05, 0]) for x in (-5.55, -3.7, -1.85, 0.0)])
        grow_lbl = T("随长度不断分配新块", 18, KV).move_to([-2.8, 0.05, 0])

        cx, cy, r = 4.35, 0.9, 1.0
        ring = Circle(radius=r, stroke_color=SWA, stroke_width=2.5).move_to([cx, cy, 0])
        ticks = VGroup()
        for k in range(134):
            ang = k / 134 * TAU
            col = SWA if k < 128 else DRAFT
            p0 = [cx + r * math.cos(ang), cy + r * math.sin(ang), 0]
            p1 = [cx + (r + 0.17) * math.cos(ang), cy + (r + 0.17) * math.sin(ang), 0]
            ticks.add(Line(p0, p1, color=col, stroke_width=2).set_stroke(opacity=0.85))
        clbl = T("134", 24, FG).move_to([cx, cy, 0])

        card = number_card("3.13", "MB / 序列", "43层×134×528B + 3层压缩状态（主干40层约2.8MB）", color=SWA)
        card.move_to([1.7, -1.35, 0])

        strip = T("块状KV：每块 113,920 字节", 20, FG).move_to([-6.4, 2.15, 0], aligned_edge=UL)
        foot = self.foot_lines(["计算来自 work/calc/EP03_state_crossover.py", "3.13 MB 含 40 主干+3 草稿+压缩状态"])
        foot.move_to([-6.45, -2.22, 0], aligned_edge=UL)

        self.play(FadeIn(blocks[0]), FadeIn(strip), run_time=0.8)

        self.until("state_intro")
        self.play(LaggedStart(*[FadeIn(b) for b in blocks[1:]], lag_ratio=0.4), FadeIn(grow_lbl), run_time=1.6)

        self.until("block_alloc")
        self.play(Indicate(blocks[3], color=KV, scale_factor=1.05), run_time=0.8)

        self.until("state_diff")
        self.play(FadeIn(ring), run_time=0.8)

        self.until("ring134")
        new = T("SWA环：134 = 128+默认6回退", 20, SWA).move_to([-6.4, 2.15, 0], aligned_edge=UL)
        self.play(LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=0.01), FadeIn(clbl),
                  FadeIn(new), FadeOut(strip), run_time=2.0)
        strip = new

        self.until("budget")
        self.play(Indicate(ticks[131], color=DRAFT, scale_factor=1.6), run_time=0.9)

        self.until("mb313")
        new = T("全槽固定占用约 3.13 MB", 20, SWA).move_to([-6.4, 2.15, 0], aligned_edge=UL)
        self.play(FadeIn(card), FadeIn(new), FadeOut(strip), run_time=0.8)
        strip = new

        self.until("mb28")
        new = T("开销与序列长度完全解耦", 20, SWA).move_to([-6.4, 2.15, 0], aligned_edge=UL)
        self.play(FadeIn(foot), FadeIn(new), FadeOut(strip), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------- S16
class EP03_S16(_E03):
    SHOT = "EP03-S16"

    def construct(self):
        head = self.fit_left_of_tags(header("状态分工：落盘区与丢弃区", "EP03 · S16 存本机 or 传输"))
        self.add(head)

        stored = Block("stored 区：前 20 层 SWA", CPU, sub="1,415,040 B ≈ 1.35 MiB", w=4.4, h=1.5, size=20)
        stored.move_to([-4.0, 1.1, 0])

        drop_bg = RoundedRectangle(corner_radius=0.12, width=4.6, height=1.5, stroke_width=0,
                                   fill_color=MUTED, fill_opacity=0.2).move_to([1.6, 1.1, 0])
        drop_edge = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=4.6, height=1.5,
                                                    stroke_color=MUTED, stroke_width=2.2),
                                   num_dashes=44).move_to([1.6, 1.1, 0])
        drop_t1 = T("dropped 区：后 20 层 SWA + 草稿", 20, FG)
        drop_t2 = T("约 1.63 MiB · 内存不持久化", 16, MUTED)
        drop_txt = VGroup(drop_t1, drop_t2).arrange(DOWN, buff=0.08).move_to([1.6, 1.1, 0])
        dropped = VGroup(drop_bg, drop_edge, drop_txt)

        split = DashedLine([-1.3, 0.2, 0], [-1.3, 2.0, 0], color=MUTED, stroke_width=2)

        host = Block("Local host memory", KV, sub="本机主机内存 · 不进 3FS", w=3.8, h=1.2, size=20)
        host.move_to([-4.0, -0.9, 0])
        down = Arrow([-4.0, 0.3, 0], [-4.0, -0.25, 0], color=KV, stroke_width=3,
                     max_tip_length_to_length_ratio=0.2)
        no3fs = Pill("不进 3FS", WARN, size=16).move_to([-1.7, -0.55, 0])

        ce = Pill("Decode CE 实例", DECODE, size=16).move_to([5.3, 0.55, 0])
        right = Arrow([3.95, 0.75, 0], [4.55, 0.6, 0], color=DECODE, stroke_width=3,
                      max_tip_length_to_length_ratio=0.25)

        code = code_panel("state = {\n  'stored': host,\n  'dropped': remote}",
                          "示意：两区内存分工，非原文", size=18, width=4.2)
        code.move_to([1.5, -1.5, 0])
        cross = Block("跨请求命中前缀", SWA, sub="后 20 层靠有界重放恢复 (EP07)", w=4.6, h=1.0, size=20)
        cross.move_to([1.5, -1.5, 0])

        strip = T("前20层SWA存本机（1.35MiB）", 20, FG).move_to([-3.8, -2.45, 0])
        foot = self.foot_lines(["数据来自 work/calc/EP03_state_crossover.py", "文档证实 SWA 存本机 Host 内存"],
                               x=6.55, y=-2.22)

        self.play(FadeIn(stored), FadeIn(dropped), FadeIn(strip), run_time=0.9)

        self.until("split_intro")
        self.play(Create(split), run_time=0.6)

        self.until("storage_doc")
        new = T("本地Host内存 · 不进3FS", 20, WARN).move_to([-3.8, -2.45, 0])
        self.play(Create(down), FadeIn(host), FadeIn(no3fs), FadeIn(new), FadeOut(strip), run_time=0.8)
        strip = new

        self.until("oss_note")
        self.play(FadeIn(code), run_time=0.7)

        self.until("stored_20")
        self.play(Indicate(stored, color=CPU, scale_factor=1.03), run_time=0.8)

        self.until("dropped_23")
        self.play(Indicate(dropped, color=MUTED, scale_factor=1.02), run_time=0.9)

        self.until("transfer")
        new = T("dropped区随PE→CE传输", 20, DECODE).move_to([-3.8, -2.45, 0])
        self.play(Create(right), FadeIn(ce), FadeIn(new), FadeOut(strip), run_time=0.8)
        strip = new

        self.until("cross_hit")
        new = T("跨请求命中靠有界重放恢复", 20, SWA).move_to([-3.8, -2.45, 0])
        self.play(FadeOut(code), FadeIn(cross), FadeIn(new), FadeOut(strip), run_time=0.8)
        self.play(FadeIn(foot), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- S17
class EP03_S17(_E03):
    SHOT = "EP03-S17"

    def construct(self):
        head = self.fit_left_of_tags(header("显存反转：状态槽与块状 KV 的交汇", "EP03 · S17 aha 时刻"))
        self.add(head)

        x0, x1, y0, y1 = -5.7, 5.3, -1.65, 2.05

        def X(L):
            return x0 + L / 8000.0 * (x1 - x0)

        def Y(mb):
            return y0 + mb / 8.0 * (y1 - y0)

        xax = Line([x0, y0, 0], [x1, y0, 0], color=MUTED, stroke_width=2)
        yax = Line([x0, y0, 0], [x0, y1, 0], color=MUTED, stroke_width=2)
        xticks = VGroup(*[T(s, 16, MUTED).move_to([X(v), y0 - 0.22, 0])
                          for s, v in (("0", 0), ("2000", 2000), ("4000", 4000), ("6000", 6000), ("8000", 8000))])
        yticks = VGroup(*[T(s, 16, MUTED).move_to([x0 - 0.26, Y(mb), 0])
                          for s, mb in (("0", 0), ("2", 2), ("4", 4), ("6", 6), ("8", 8))])
        xlbl = T("输入 Token 长度 L", 18, MUTED).move_to([-2.6, -2.22, 0])
        ylbl = T("显存占用 (MB)", 18, MUTED).rotate(PI / 2).move_to([-6.45, 0.4, 0])

        shade = Rectangle(width=abs(X(3516) - x0), height=abs(Y(3.13) - y0), stroke_width=0,
                          fill_color=SWA, fill_opacity=0.1).move_to([(X(3516) + x0) / 2, (Y(3.13) + y0) / 2, 0])
        flat = Line([x0, Y(3.13), 0], [x1, Y(3.13), 0], color=SWA, stroke_width=4)
        slope = Line([x0, y0, 0], [x1, Y(7.12), 0], color=KV, stroke_width=4)

        dot = Circle(radius=0.14, stroke_color=EXPERT, stroke_width=3).move_to([X(3516), Y(3.13), 0])
        drop = DashedLine([X(3516), Y(3.13), 0], [X(3516), y0, 0], color=EXPERT, stroke_width=2)
        cross_lbl = T("显存交叉点：约 3,516 token", 18, EXPERT).move_to([-3.0, 0.5, 0])
        flat_lbl = T("固定状态槽：平直 3.13 MB", 18, SWA).move_to([2.9, -0.55, 0])
        slope_lbl = T("块状KV：890B/token", 18, KV).move_to([4.6, 0.75, 0])
        block_lbl = T("第 28 个 128-token 数据块（3,584 token）", 16, EXPERT).move_to([-3.5, -1.42, 0])
        adv = T("突破3.5k后块状KV才占主导", 18, KV).move_to([3.3, -1.2, 0])

        foot = self.foot_lines(["按比例绘制：曲线来自 work/calc/", "EP03_state_crossover.py；单序列 HBM 对比"],
                               x=6.55, y=-2.3)

        self.play(Create(xax), Create(yax), FadeIn(flat_lbl), run_time=0.9)

        self.until("aha_title")
        self.play(FadeIn(xticks), FadeIn(yticks), FadeIn(xlbl), FadeIn(ylbl), run_time=0.7)

        self.until("aha_contrast")
        self.play(Indicate(flat_lbl, color=SWA), run_time=0.7)

        self.until("purple_line")
        self.play(Create(flat), FadeIn(shade), run_time=1.0)

        self.until("green_line")
        self.play(Create(slope), FadeIn(slope_lbl), run_time=1.0)

        self.until("cross_calc")
        self.play(FadeIn(dot), Create(drop), FadeIn(cross_lbl), run_time=0.8)

        self.until("short_ctx")
        self.play(shade.animate.set_fill(SWA, 0.25), Indicate(flat, color=SWA), run_time=0.9)

        self.until("grain_blocks")
        self.play(FadeIn(block_lbl), FadeIn(adv), Indicate(slope, color=KV), run_time=0.9)
        self.play(FadeIn(foot), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- S18
class EP03_S18(_E03):
    SHOT = "EP03-S18"

    def construct(self):
        head = self.fit_left_of_tags(header("原生草稿：多词预测与非因果块", "EP03 · S18 DFlash"))
        self.add(head)

        mod = Block("DFlash (DSpark) 草稿网络", DRAFT, sub="3 层 (num_nextn_predict_layers=3)",
                    w=3.4, h=1.5, size=20)
        mod.move_to([-4.7, 0.5, 0])
        code_p = Pill("代码：DFlash", DRAFT, size=16).move_to([-0.9, 1.9, 0])
        report_p = Pill("报告：DSpark", MUTED, size=16).move_to([1.5, 1.9, 0])

        chip_x = (-0.5, 0.3, 1.1, 1.9, 2.7)
        chips = VGroup(*[Rectangle(width=0.55, height=0.42, stroke_color=EXPERT, stroke_width=2,
                                   fill_color=EXPERT, fill_opacity=0.15).move_to([x, 0.75, 0]) for x in chip_x])
        chip_lbl = T("1 组 Markov 头 (rank-256) 自回归采样 5 步", 16, EXPERT).move_to([1.1, 1.35, 0])
        streams = VGroup(*[Arrow([-2.72, 0.5, 0], [x - 0.3, 0.75, 0], color=DRAFT, stroke_width=2,
                                 max_tip_length_to_length_ratio=0.15).set_stroke(opacity=0.8) for x in chip_x])

        toks = VGroup(*[Rectangle(width=0.55, height=0.5, stroke_color=DRAFT, stroke_width=2,
                                  fill_color=DRAFT, fill_opacity=0.3).move_to([x, -0.45, 0]) for x in chip_x])
        tok_lbls = VGroup(*[T(s, 16, DRAFT).move_to([x, -0.45, 0]) for x, s in zip(chip_x, ("T1", "T2", "T3", "T4", "T5"))])
        link = VGroup(*[Line([x, 0.5, 0], [x, -0.18, 0], color=MUTED, stroke_width=2) for x in chip_x])
        share = DashedVMobject(Rectangle(width=4.3, height=0.86, stroke_color=DRAFT, stroke_width=2),
                               num_dashes=40).move_to([1.1, -0.45, 0])
        share_lbl = T("共享同一段 KV 索引（块内非因果可见）", 18, DRAFT).move_to([1.1, -1.25, 0])

        strip = T("3 层原生草稿网络（DFlash）", 20, FG).move_to([-3.4, -2.45, 0])
        foot = self.foot_lines(["示意：PyTorch 参考实现索引构造示意", "生产走 TileLang 算子"], x=6.55, y=-2.2)

        self.play(FadeIn(mod), FadeIn(strip), run_time=0.8)

        self.until("draft_intro")
        self.play(Indicate(mod, color=DRAFT, scale_factor=1.03), run_time=0.9)

        self.until("dflash_name")
        self.play(FadeIn(code_p), FadeIn(report_p), run_time=0.6)

        self.until("hyperparams")
        new = T("一次前向预测 5 个草稿位置", 20, DRAFT).move_to([-3.4, -2.45, 0])
        env = T("环境变量默认预测5个位置", 18, MUTED).move_to([-4.7, -0.72, 0])
        self.play(FadeIn(chips), FadeIn(chip_lbl), FadeIn(env), FadeIn(new), FadeOut(strip), run_time=0.7)
        strip = new
        self.play(Indicate(chips[0], color=EXPERT), run_time=0.6)

        self.until("fwd_parallel")
        self.play(LaggedStart(*[Create(a) for a in streams], lag_ratio=0.12), run_time=1.2)

        self.until("markov")
        self.play(FadeIn(toks), FadeIn(tok_lbls), FadeIn(link), run_time=0.8)
        self.play(*[Indicate(c, color=EXPERT, scale_factor=1.2) for c in chips], run_time=0.8)

        self.until("share_idx")
        new = T("草稿块内共享索引 · 呈现非因果", 20, DRAFT).move_to([-3.4, -2.45, 0])
        self.play(Create(share), FadeIn(share_lbl), FadeIn(new), FadeOut(strip), run_time=0.8)
        self.play(FadeIn(foot), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- S19
class EP03_S19(_E03):
    SHOT = "EP03-S19"

    def construct(self):
        head = self.fit_left_of_tags(header("动态验证：置信度头与变长预算", "EP03 · S19 投机验证"))
        self.add(head)

        probs = (0.92, 0.85, 0.61, 0.28, 0.09)
        xs = (-2.2, -1.1, 0.0, 1.1, 2.2)
        toks = VGroup(*[Rectangle(width=0.62, height=0.62, stroke_color=DRAFT, stroke_width=2,
                                  fill_color=DRAFT, fill_opacity=0.25).move_to([x, -0.2, 0]) for x in xs])
        tlbl = VGroup(*[T(s, 16, DRAFT).move_to([x, -0.2, 0]) for x, s in zip(xs, ("T1", "T2", "T3", "T4", "T5"))])

        bars = VGroup()
        for x, p in zip(xs, probs):
            col = GPU if p >= 0.6 else WARN
            bars.add(Rectangle(width=0.62, height=p * 1.6, stroke_width=1, stroke_color=BG,
                               fill_color=col, fill_opacity=0.8
                               ).move_to([x, 0.12 + p * 0.8, 0]))
        vals = VGroup(*[T(f"{p:.2f}", 16, GPU if p >= 0.6 else WARN).move_to([x, 0.12 + p * 1.6 + 0.2, 0])
                        for x, p in zip(xs, probs)])
        conf_lbl = T("内置置信度头", 18, GPU).move_to([-3.9, 1.9, 0])

        vbox = DashedVMobject(Rectangle(width=3.6, height=0.92, stroke_color=GPU, stroke_width=2.5),
                              num_dashes=32).move_to([-1.1, -0.2, 0])
        dim_lbl = T("T4 / T5 暂不验证", 16, MUTED).move_to([3.6, 0.45, 0])

        c_left = Block("固定验证：浪费算力", WARN, sub="低置信词进入验证浪费算力",
                       w=4.4, h=1.0, size=20).move_to([-3.6, -1.5, 0])
        c_right = Block("生产变长验证：节约算力", GPU, sub="置信度预估，按预算动态决定验证长度",
                        w=4.8, h=1.0, size=20).move_to([3.2, -1.5, 0])

        p_off = Pill("开源默认关闭", MUTED, size=16).move_to([5.2, -0.35, 0])
        p_doc = Pill("官方文档：生产使用", DECODE, size=16).move_to([5.2, -0.95, 0])

        strip = T("内置置信度头", 20, GPU).move_to([-3.0, -2.45, 0])
        foot = self.foot_lines(["示意：接受概率数值为示意", "最终正确性由拒绝采样严格兜底"], x=6.55, y=-2.2)

        self.play(FadeIn(toks), FadeIn(tlbl), FadeIn(conf_lbl), FadeIn(strip), run_time=0.8)

        self.until("conf_intro")
        new = T("输出逐位置接受概率", 20, GPU).move_to([-3.0, -2.45, 0])
        self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.1), FadeIn(vals),
                  FadeIn(new), FadeOut(strip), run_time=1.2)
        strip = new

        self.until("decay")
        self.play(Indicate(vals[3:], color=WARN, scale_factor=1.3), run_time=0.9)

        self.until("waste")
        self.play(FadeIn(c_left), run_time=0.7)

        self.until("prob")
        new = T("动态分配草稿验证长度", 20, GPU).move_to([-3.0, -2.45, 0])
        self.play(Create(vbox), FadeIn(new), FadeOut(strip), run_time=0.8)
        strip = new

        self.until("budget")
        self.play(*[t.animate.set_fill(MUTED, 0.12) for t in toks[3:]],
                  FadeIn(dim_lbl), FadeIn(c_right), run_time=0.9)

        self.until("oss_off")
        self.play(FadeIn(p_off), run_time=0.6)

        self.until("doc_prod")
        new = T("开源默认关闭 · 生产使用变长验证", 20, MUTED).move_to([-3.0, -2.45, 0])
        self.play(FadeIn(p_doc), FadeIn(new), FadeOut(strip), run_time=0.7)
        self.play(FadeIn(foot), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- S20
class EP03_S20(_E03):
    SHOT = "EP03-S20"

    def construct(self):
        head = self.fit_left_of_tags(header("暂停互动：解码半区为什么能被截断？", "EP03 · S20 思考题"))
        self.add(head)

        q = Block("思考题：为何21-39层不产块状KV", DECODE, sub="是有界重放成立的前提？",
                  w=8.5, h=2.0, size=22).move_to([0, 0.7, 0])
        ring = Circle(radius=0.7, stroke_color=MUTED, stroke_width=3).move_to([0, -1.35, 0])
        ring_n = T("5", 30, MUTED).move_to([0, -1.35, 0])

        self.play(FadeIn(q), run_time=0.8)
        self.play(FadeIn(ring), FadeIn(ring_n), run_time=0.6)
        self.play(ring.animate.scale(0.35), ring_n.animate.set_opacity(0.15), run_time=4.8)

        self.until("explain")
        self.play(FadeOut(q), FadeOut(ring), FadeOut(ring_n), run_time=0.6)

        l20 = RoundedRectangle(corner_radius=0.1, width=8.6, height=0.72, stroke_color=KV, stroke_width=2.5,
                               fill_color=KV, fill_opacity=0.3).move_to([-1.2, 1.55, 0])
        l20_t = T("Layer 20 全长投影 · 产出解码半区唯一全局KV", 18, FG).move_to(l20)
        l21 = Rectangle(width=8.6, height=0.72, stroke_color=MUTED, stroke_width=2,
                        fill_color=MUTED, fill_opacity=0.12).move_to([-1.2, 0.65, 0])
        l21_t = T("Layer 21-39", 18, FG).move_to([-5.0, 0.65, 0])
        keep = Rectangle(width=0.8, height=0.72, stroke_color=SWA, stroke_width=3,
                         fill_color=SWA, fill_opacity=0.35).move_to([2.7, 0.65, 0])
        keep_lbl = T("末尾 140 行（≥134）", 16, SWA).move_to([4.75, 0.65, 0])
        trad = T("传统：每层都写块状 KV → 无法截断", 18, MUTED).move_to([-1.4, -0.35, 0])
        trad_x = T("✗", 26, WARN).move_to([-4.5, -0.35, 0])

        code = code_panel("assert window_size + max_backtracking <= keep_tokens",
                          "model_runner.py:110 (下限: 128+6=134)",
                          highlight=[1], size=16, width=6.2)
        code.move_to([2.4, -1.55, 0])

        strip = T("L20全长投影 · 后续免除写入", 20, FG).move_to([-4.0, -2.45, 0])
        foot = self.foot_lines(["134 为代码启动硬断言下限", "140 为官方 README 推荐配置"], x=6.55, y=-2.3)

        self.play(FadeIn(l20), FadeIn(l20_t), FadeIn(strip), run_time=0.8)

        self.until("ced_proj")
        self.play(Indicate(l20, color=EXPERT, scale_factor=1.02), run_time=0.8)

        self.until("full_l20")
        self.play(Indicate(l20_t, color=KV), run_time=0.7)

        self.until("free_l21_39")
        self.play(FadeIn(l21), FadeIn(l21_t), run_time=0.8)

        self.until("traditional")
        self.play(FadeIn(trad), FadeIn(trad_x), run_time=0.8)

        self.until("bound_134")
        self.play(FadeIn(code), run_time=0.7)

        self.until("keep_140")
        new = T("推荐截断至末尾140行（≥134）", 20, SWA).move_to([-4.0, -2.45, 0])
        self.play(FadeIn(keep), FadeIn(keep_lbl), FadeIn(new), FadeOut(strip), run_time=0.8)
        self.play(FadeIn(foot), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------- S21
class EP03_S21(_E03):
    SHOT = "EP03-S21"

    ROWS = [
        ("40 层全 SWA (窗口 128)", "每序列固定 134 位置状态槽", "EP06", SWA),
        ("仅 4 层产块状 KV", "分段存储与 890 B/token 均摊", "EP06/11", KV),
        ("前 20/后 20 的 CED", "末尾 140 行截断与有界重放", "EP07", DECODE),
        ("8 层筛选 / 30 层复用", "跨层单槽位索引共享", "EP06", KV),
        ("196.9B Engram 查表", "分片存储与跨 rank gather 算子", "EP08", EXPERT),
        ("3 层草稿 × 5 位置", "6 个回退位与动态投机验证", "EP09", DRAFT),
        ("FP4 低精度 KV", "定制 FP4 反量化与注意力内核", "EP10", GPU),
    ]

    def construct(self):
        head = self.fit_left_of_tags(header("全景索引：模型特性与引擎机制", "EP03 · S21 全系列地图"))
        self.add(head)

        top, rh = 1.7, 0.5
        ys = [top - rh * (k + 1.5) for k in range(7)]
        vs = [-6.3, -2.25, 2.4, 6.3]
        grid = VGroup(*[Line([x, top, 0], [x, top - rh * 8, 0], color=GRID, stroke_width=1.2) for x in vs])
        grid.add(*[Line([vs[0], top - rh * k, 0], [vs[-1], top - rh * k, 0], color=GRID, stroke_width=1.2)
                   for k in range(9)])
        hdr = VGroup(T("模型物理特性", 18, MUTED).move_to([-6.2, top - rh * 0.5, 0], aligned_edge=LEFT),
                     T("引擎工程设计", 18, MUTED).move_to([-2.1, top - rh * 0.5, 0], aligned_edge=LEFT),
                     T("后续集号", 18, MUTED).move_to([4.35, top - rh * 0.5, 0]))

        rows = []
        for k, (a, b, tag, col) in enumerate(self.ROWS):
            y = ys[k]
            hl = Rectangle(width=12.6, height=rh, stroke_width=0, fill_color=DECODE, fill_opacity=0.08
                           ).move_to([0, y, 0])
            t1 = T(a, 18, FG).move_to([-6.2, y, 0], aligned_edge=LEFT)
            t2 = T(b, 18, MUTED).move_to([-2.1, y, 0], aligned_edge=LEFT)
            pill = Pill(tag, col, size=16).move_to([4.35, y, 0])
            rows.append((VGroup(hl, t1, t2, pill), pill, hl))

        strip = T("模型物理形状 → 引擎工程索引", 20, FG).move_to([1.2, 2.08, 0], aligned_edge=UL)
        foot = T("编辑性汇总：客观对照模型物理形状与引擎工程映射", 16, MUTED).move_to([-6.3, -2.6, 0],
                                                                                     aligned_edge=UL)

        self.play(FadeIn(grid), FadeIn(hdr), FadeIn(strip), run_time=0.9)

        self.until("table_intro")
        # Fade in all rows together so reference table is complete on screen
        self.play(*[FadeIn(r[0]) for r in rows], run_time=0.9)

        # rows light up one by one with the narration
        self.until("map_swa")
        self.play(Indicate(rows[0][1], color=SWA, scale_factor=1.2),
                  rows[0][2].animate.set_fill(opacity=0.22), run_time=0.8)

        self.until("map_kv")
        new = T("全SWA与4层块状KV（EP06/11）", 20, FG).move_to([1.2, 2.08, 0], aligned_edge=UL)
        self.play(Indicate(rows[1][1], color=KV, scale_factor=1.2),
                  rows[1][2].animate.set_fill(opacity=0.22),
                  FadeIn(new), FadeOut(strip), run_time=0.8)
        strip = new

        self.until("map_ced")
        new = T("CED与有界重放（EP07）", 20, FG).move_to([1.2, 2.08, 0], aligned_edge=UL)
        self.play(Indicate(rows[2][1], color=DECODE, scale_factor=1.2),
                  rows[2][2].animate.set_fill(opacity=0.22),
                  FadeIn(new), FadeOut(strip), run_time=0.8)
        strip = new

        self.until("map_idx")
        self.play(Indicate(rows[3][1], color=KV, scale_factor=1.2),
                  rows[3][2].animate.set_fill(opacity=0.22), run_time=0.8)

        self.until("map_engram")
        self.play(Indicate(rows[4][1], color=EXPERT, scale_factor=1.2),
                  rows[4][2].animate.set_fill(opacity=0.22), run_time=0.8)

        self.until("map_mtp")
        new = T("查表·MTP·FP4（EP08-10）", 20, FG).move_to([1.2, 2.08, 0], aligned_edge=UL)
        self.play(Indicate(rows[5][1], color=DRAFT, scale_factor=1.2),
                  Indicate(rows[6][1], color=GPU, scale_factor=1.2),
                  rows[5][2].animate.set_fill(opacity=0.22),
                  rows[6][2].animate.set_fill(opacity=0.22),
                  FadeIn(new), FadeOut(strip), FadeIn(foot), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- S22
class EP03_S22(_E03):
    SHOT = "EP03-S22"

    def construct(self):
        head = self.fit_left_of_tags(header("总结预告：请求在代码里的一生", "EP03 · S22 收束"))
        self.add(head)

        panel = RoundedRectangle(corner_radius=0.14, width=5.9, height=3.9, stroke_color=GRID,
                                 stroke_width=2, fill_color=GRID, fill_opacity=0.12).move_to([3.6, 0.0, 0])
        ptitle = T("本集要点", 24, FG).move_to([3.6, 1.6, 0])
        slots = VGroup(*[DashedVMobject(Rectangle(width=5.2, height=0.85, stroke_color=GRID, stroke_width=1.5),
                                        num_dashes=32).move_to([3.6, y, 0]) for y in (0.95, 0.05, -0.85)])

        cards = VGroup(
            Block("1. 40层全SWA · 仅4层产块状KV", KV, sub="均摊 890 B/token", w=5.2, h=0.9, size=18),
            Block("2. L20全长投影 · L21-39复用", DECODE, sub="截断重放能够成立的物理前提", w=5.2, h=0.9, size=18),
            Block("3. 查表占1/4 · 内置3层草稿", EXPERT, sub="极端稀疏与原生投机解码", w=5.2, h=0.9, size=18),
        )
        for c, y in zip(cards, (0.95, 0.05, -0.85)):
            c.move_to([3.6, y, 0])
        checks = VGroup(*[T("✓", 24, col).move_to([5.9, y, 0])
                          for col, y in ((KV, 0.95), (DECODE, 0.05), (EXPERT, -0.85))])

        l1 = T("40层SWA · 仅4层产块状KV", 22, FG).move_to([-6.5, 1.9, 0], aligned_edge=UL)
        l2 = T("L20全长投影 · L21-39复用", 22, FG).move_to([-6.5, 1.25, 0], aligned_edge=UL)
        l3 = T("查表占1/4 · 内置3层草稿", 22, FG).move_to([-6.5, 0.6, 0], aligned_edge=UL)

        bp = LayerStack(40, split=20, colors=(PREFILL, DECODE), w=1.1, h=3.4).move_to([-5.6, 0.1, 0])
        bp_engram = Rectangle(width=0.55, height=0.5, stroke_color=EXPERT, stroke_width=2,
                              fill_color=EXPERT, fill_opacity=0.4).move_to([-4.3, -0.6, 0])
        bp_draft = VGroup(*[Rectangle(width=0.3, height=0.3, stroke_color=DRAFT, stroke_width=2,
                                      fill_color=DRAFT, fill_opacity=0.35).move_to([-4.3 + k * 0.4, 0.9, 0])
                            for k in range(3)])
        bp_lbl = T("模型异构蓝图", 18, MUTED).move_to([-4.4, -1.35, 0])

        tree = VGroup(
            M("deepinfer @ 9bd9cf2", 18, FG),
            M("├── examples/offline_inference.py", 18, KV),
            M("├── deepinfer/engine/llm_engine.py", 18, MUTED),
            M("└── csrc/engine/scheduler.hpp", 18, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-6.4, 1.15, 0], aligned_edge=UL)

        nxt = Block("下集预告：EP04", DECODE, sub="请求在代码里的一生", w=4.5, h=1.1, size=20)
        nxt.move_to([-3.4, -1.35, 0])
        l4 = T("下集：请求在代码里的一生", 20, DECODE).move_to([-6.5, -2.15, 0], aligned_edge=UL)

        foot = T("代码结构源自 deepseek-ai/DeepInfer @ 9bd9cf2 开源仓库", 16, MUTED)
        foot.move_to([6.55, -2.6, 0], aligned_edge=UR)

        self.play(FadeIn(panel), FadeIn(ptitle), FadeIn(slots), run_time=0.9)

        self.until("recap_intro")
        self.play(Indicate(ptitle, color=DECODE), run_time=0.6)

        self.until("recap1")
        self.play(FadeIn(cards[0], shift=LEFT * 0.3), FadeIn(l1), run_time=0.7)
        self.play(FadeIn(checks[0]), run_time=0.4)

        self.until("recap2")
        self.play(FadeIn(cards[1], shift=LEFT * 0.3), FadeIn(l2), run_time=0.7)
        self.play(FadeIn(checks[1]), run_time=0.4)

        self.until("recap3")
        self.play(FadeIn(cards[2], shift=LEFT * 0.3), FadeIn(l3), run_time=0.7)
        self.play(FadeIn(checks[2]), run_time=0.4)

        self.until("blueprint")
        self.play(FadeOut(l1), FadeOut(l2), FadeOut(l3), run_time=0.6)
        self.play(FadeIn(bp), FadeIn(bp_engram), FadeIn(bp_draft), FadeIn(bp_lbl), run_time=0.8)

        self.until("reason")
        self.play(Indicate(bp_engram, color=EXPERT, scale_factor=1.3),
                  Indicate(bp_draft, color=DRAFT, scale_factor=1.3), run_time=0.9)

        self.until("code_tree")
        self.play(FadeOut(bp), FadeOut(bp_engram), FadeOut(bp_draft), FadeOut(bp_lbl), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(t) for t in tree], lag_ratio=0.15), run_time=1.0)
        self.play(Indicate(tree[1], color=KV), run_time=0.8)

        self.until("next_ep")
        self.play(FadeIn(nxt, shift=UP * 0.2), FadeIn(l4), FadeIn(foot), run_time=0.5)
        self.finish()
