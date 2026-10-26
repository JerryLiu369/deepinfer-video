"""EP07 scenes: SWA 有界重放 (shots S01-S20)."""
from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path for manim_lib imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import (
    DOWN, LEFT, RIGHT, UP, UL, UR, DL, DR, ORIGIN,
    FadeIn, FadeOut, Create, Write, Transform, Indicate,
    Line, Arrow, Rectangle, RoundedRectangle, VGroup,
)
from manim_lib.dvlib import (
    BG, FG, MUTED, GRID, PREFILL, DECODE, KV, SWA, WARN, EXPERT, DRAFT,
    T, M, Pill, DVScene, header, MiniMap, Block, TokenRow, window_bracket,
    code_panel, number_card, LayerStack, AttentionMatrix, Scale,
)


class EP07_S01(DVScene):
    SHOT = "EP07-S01"

    def construct(self):
        head = self.fit_left_of_tags(header("后二十层只算一百四十个位置", "EP07 · S01 冷开场"))
        self.add(head)

        # Height 4.0, centered at y=-0.2 => y in [-2.2, 1.8], safely above -2.75
        stack = LayerStack(40, split=20, w=0.9, h=4.0).move_to([-4.8, -0.2, 0])

        # 40 rows of token indicators on the left side (x around -2.2)
        rows = VGroup()
        for i in range(40):
            col = PREFILL if i < 20 else DECODE
            r = RoundedRectangle(corner_radius=0.02, width=3.4, height=0.06,
                                 stroke_width=0, fill_color=col, fill_opacity=0.85)
            r.move_to([-2.2, stack.layer(i).get_y(), 0])
            rows.add(r)

        self.play(FadeIn(stack), FadeIn(rows), run_time=1.2)

        self.until("rows")
        # Place text in right half空白处 (x = 3.2), no overlap with rows (which end at x = -0.5)
        txt1 = T("输入 10,000 token（示意）", 22, FG).move_to([3.2, 1.0, 0])
        self.play(FadeIn(txt1), run_time=0.6)

        self.until("keep")
        # Back 20 rows turn muted except rightmost tip
        tip_group = VGroup()
        faded_group = VGroup()
        for i in range(20, 40):
            orig = rows[i]
            y = orig.get_y()
            faded = RoundedRectangle(corner_radius=0.02, width=3.0, height=0.06,
                                     stroke_width=0, fill_color=MUTED, fill_opacity=0.25)
            faded.move_to([-2.4, y, 0])
            tip = RoundedRectangle(corner_radius=0.02, width=0.35, height=0.08,
                                   stroke_width=0, fill_color=SWA, fill_opacity=1.0)
            tip.move_to([-0.65, y, 0])
            faded_group.add(faded)
            tip_group.add(tip)

        txt2 = T("后 20 层：只算末尾 140 个", 22, SWA).move_to([3.2, 0.2, 0])
        self.play(
            FadeOut(rows[20:]),
            FadeIn(faded_group),
            FadeIn(tip_group),
            FadeIn(txt2),
            run_time=1.2,
        )

        self.until("answer")
        self.play(Indicate(tip_group, color=FG, scale_factor=1.1), run_time=0.8)

        self.finish()


class EP07_S02(DVScene):
    SHOT = "EP07-S02"

    def construct(self):
        title = T("第七集 · SWA 有界重放", 44, FG).move_to([0, 1.2, 0])
        sub = T("只重算最后一小段", 26, MUTED).next_to(title, DOWN, buff=0.35)
        # Center MiniMap directly below subtitle, well above subtitle band (y >= -2.75)
        mmap = MiniMap(active="Prefill", scale=1.0).next_to(sub, DOWN, buff=0.8)

        self.play(FadeIn(title), FadeIn(sub), FadeIn(mmap), run_time=0.8)
        self.finish()


class EP07_S03(DVScene):
    SHOT = "EP07-S03"

    def construct(self):
        head = self.fit_left_of_tags(header("有一种 KV 没存下来", "EP07 · S03 本集问题"))
        self.add(head)

        mmap = MiniMap(active="Prefill", scale=0.9).move_to([0, 1.4, 0])
        # Font size 18, outside of MiniMap
        req_lbl = Pill("当前：第五轮请求", color=DECODE, size=18).next_to(mmap, DOWN, buff=0.25)

        self.play(FadeIn(mmap), FadeIn(req_lbl), run_time=0.8)

        # Left Block (Block KV)
        b_kv = Block("块状 KV", color=KV, w=3.8, h=1.8, size=24, sub="前四轮 · 长期保留")
        b_kv.move_to([-3.2, -1.1, 0])
        squares = VGroup(*[
            Rectangle(width=0.35, height=0.35, stroke_color=KV, stroke_width=1.5,
                      fill_color=KV, fill_opacity=0.6)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.15).next_to(b_kv.submobjects[1], DOWN, buff=0.12)
        b_kv.add(squares)

        self.until("missing")
        # Right Block (SWA state missing) - stroke in SWA purple per review D3
        b_swa = Block("SWA 状态", color=SWA, w=3.8, h=1.8, size=24, sub="未存 / 跨机调度缺失", fill=0.1)
        b_swa.move_to([3.2, -1.1, 0])

        missing_badge = Pill("未存 / 缺失", color=WARN, size=18).next_to(b_swa, UP, buff=0.15)

        self.play(FadeIn(b_kv), FadeIn(b_swa), FadeIn(missing_badge), run_time=1.0)
        self.finish()


class EP07_S04(DVScene):
    SHOT = "EP07-S04"

    def construct(self):
        head = self.fit_left_of_tags(header("SWA 只看最近 128 个", "EP07 · S04 回顾"))
        self.add(head)

        row = TokenRow(24, color=PREFILL, size=0.42, gap=0.08).move_to([0, 0.2, 0])
        # Footnote at y >= -2.75 per review D4
        decl = T("示意：8 格代表 128 个 token", 18, MUTED).move_to([0, -1.4, 0])

        self.until("win")
        wb = window_bracket(row, 0, 7, color=SWA, label="窗口 128")
        for cell in row.cells()[8:]:
            cell.set_fill(color=MUTED, opacity=0.25)
        self.play(FadeIn(row), FadeIn(wb), FadeIn(decl), run_time=0.8)

        self.until("slide")
        wb_target = window_bracket(row, 16, 23, color=SWA, label="窗口 128")
        anims = [Transform(wb, wb_target)]
        for i, cell in enumerate(row.cells()):
            if 16 <= i <= 23:
                anims.append(cell.animate.set_fill(color=PREFILL, opacity=0.85))
            else:
                anims.append(cell.animate.set_fill(color=MUTED, opacity=0.25))

        self.play(*anims, run_time=2.0)
        self.finish()


class EP07_S05(DVScene):
    SHOT = "EP07-S05"

    def construct(self):
        head = self.fit_left_of_tags(header("层是叠起来的", "EP07 · S05 感受野扩张"))
        self.add(head)

        r1 = TokenRow(16, color=PREFILL, size=0.32, gap=0.06).move_to([-1.5, 1.1, 0])
        r2 = TokenRow(16, color=PREFILL, size=0.32, gap=0.06).move_to([-1.5, 0.2, 0])
        r3 = TokenRow(16, color=PREFILL, size=0.32, gap=0.06).move_to([-1.5, -0.7, 0])
        r1.cells()[-1].set_fill(color=DECODE, opacity=1.0)
        token_group = VGroup(r1, r2, r3)

        # Footnote at y >= -2.75
        decl = T("示意：3 层代表 20 层感受野累积", 18, MUTED).move_to([-3.2, -1.8, 0])

        self.until("stack")
        self.play(FadeIn(token_group), FadeIn(decl), run_time=0.8)

        self.until("grow")
        b2 = window_bracket(r2, 10, 15, color=SWA)
        b3 = window_bracket(r3, 4, 15, color=WARN, label="感受野向左扩大")
        self.play(FadeIn(b2), run_time=0.6)
        self.play(FadeIn(b3), run_time=0.8)

        self.until("doc")
        # Shift token rows left and dim them before showing the number card (review D5)
        self.play(
            token_group.animate.shift(LEFT * 1.5).set_opacity(0.35),
            b2.animate.shift(LEFT * 1.5).set_opacity(0.35),
            b3.animate.shift(LEFT * 1.5).set_opacity(0.35),
            decl.animate.shift(LEFT * 0.8),
            run_time=0.8,
        )
        card = number_card("2,560", "token × 20 层", "DeepSeek 部署问答的说法", color=WARN)
        card.move_to([3.4, 0.0, 0])
        self.play(FadeIn(card), run_time=0.8)

        self.finish()


class EP07_S06(DVScene):
    SHOT = "EP07-S06"

    def construct(self):
        head = self.fit_left_of_tags(header("有界重放：只重算一小段", "EP07 · S06 截断机制"))
        self.add(head)

        # Height >= 3.5 (14 * 0.26 = 3.64), with axes (review D6)
        mat = AttentionMatrix(14, window=4, cell=0.26).move_to([-3.4, -0.4, 0])
        ax = mat.axes("查询位置 i ↓", "键位置 j →", size=18)
        decl = T("示意：每格代表 32 个 token", 18, MUTED).move_to([3.2, -2.1, 0])
        self.play(FadeIn(mat), FadeIn(ax), FadeIn(decl), run_time=0.8)

        self.until("formula")
        line_x = mat.cells(0, 7).get_left()[0]
        s_line = Line([line_x, mat.get_top()[1] + 0.1, 0],
                      [line_x, mat.get_bottom()[1] - 0.1, 0],
                      color=WARN, stroke_width=3)
        s_lbl = T("s", 18, WARN).next_to(s_line, UP, buff=0.06)

        masked_cells = mat.mask_left_of(7)
        # Formula block with size >= 18 (review D6)
        f_card = Block("截断重放规则", color=DECODE, w=5.2, h=1.8, size=22,
                       sub="max(s, i − 127) … i\n只看重放段内部")
        f_card.move_to([3.2, 0.6, 0])

        self.play(
            Create(s_line), FadeIn(s_lbl),
            masked_cells.animate.set_fill(color=MUTED, opacity=0.2),
            FadeIn(f_card),
            run_time=1.0,
        )

        self.until("approx")
        approx_pill = Pill("近似重建：重算变为常数", color=WARN, size=20).move_to([3.2, -0.9, 0])
        self.play(
            Indicate(masked_cells, color=WARN, scale_factor=1.05),
            FadeIn(approx_pill),
            run_time=0.8,
        )

        self.finish()


class EP07_S07(DVScene):
    SHOT = "EP07-S07"

    def construct(self):
        head = self.fit_left_of_tags(header("它用在两个地方", "EP07 · S07 两处用法"))
        self.add(head)

        # Height 4.0, bottom -2.2 >= -2.75 (review D7)
        stack = LayerStack(40, split=20, w=1.0, h=4.0).move_to([-2.2, -0.2, 0])
        lbl_enc = stack.range_label(0, 20, "encoder (前20层)", side=LEFT, size=16)
        lbl_dec = stack.range_label(20, 40, "decoder (后20层)", side=LEFT, size=16)

        self.play(FadeIn(stack), FadeIn(lbl_enc), FadeIn(lbl_dec), run_time=0.8)

        self.until("enc")
        hi_enc = VGroup(*[stack.layer(k) for k in range(20)])
        card1 = Block("① 前 20 层：命中补算", color=PREFILL, w=4.8, h=1.3, size=20,
                      sub="重算命中前缀末尾 128 个 token")
        card1.move_to([3.0, 0.8, 0])
        self.play(hi_enc.animate.set_fill(color=SWA, opacity=0.8), FadeIn(card1), run_time=0.8)

        self.until("dec")
        hi_dec = VGroup(*[stack.layer(k) for k in range(20, 40)])
        card2 = Block("② 后 20 层：每次 prefill", color=DECODE, w=4.8, h=1.3, size=20,
                      sub="仅算末尾一小段 · 不进前缀缓存")
        card2.move_to([3.0, -0.8, 0])
        self.play(hi_dec.animate.set_fill(color=SWA, opacity=0.8), FadeIn(card2), run_time=0.8)

        self.finish()


class EP07_S08(DVScene):
    SHOT = "EP07-S08"

    def construct(self):
        head = self.fit_left_of_tags(header("文档说 128，代码要 140", "EP07 · S08 口径对照"))
        self.add(head)

        self.until("doc")
        b_doc = Block("部署问答文档", color=MUTED, w=4.2, h=2.0, size=22, sub="官方：重算最后 128 个 token")
        b_doc.move_to([-3.4, 0.4, 0])
        self.play(FadeIn(b_doc), run_time=0.8)

        self.until("code")
        # Code panel font size 20 >= 18 (review D8)
        snippet = "assert window_size + BACKTRACKING \\\n    <= YOCO_PREFILL_KEEP_TOKENS"
        code = code_panel(snippet, "model_runner.py", size=20, width=5.8)
        code.move_to([3.2, 0.8, 0])
        tag = Pill("下限：128 + 6 = 134", color=DECODE, size=18).move_to([3.2, -0.4, 0])
        self.play(FadeIn(code), FadeIn(tag), run_time=0.8)

        self.until("readme")
        b_readme = Block("README 推荐：140", color=FG, w=3.6, h=1.0, size=20)
        b_readme.move_to([-3.4, -1.5, 0])
        off_pill = Pill("代码默认：关闭 (off)", color=WARN, size=18).move_to([3.2, -1.5, 0])
        self.play(FadeIn(b_readme), FadeIn(off_pill), run_time=0.8)

        self.finish()


class EP07_S09(DVScene):
    SHOT = "EP07-S09"

    def construct(self):
        head = self.fit_left_of_tags(header("算一笔示意账", "EP07 · S09 aha 时刻"))
        self.add(head)

        # Footnote at y >= -2.75 (review D4)
        decl = T("示意：输入长度为假设值；行·层 ≠ 计算量", 18, MUTED).move_to([0, -1.8, 0])

        bar_full = VGroup()
        for i in range(40):
            seg = Rectangle(width=0.18, height=0.5, stroke_width=0.5, stroke_color=BG,
                            fill_color=PREFILL, fill_opacity=0.9)
            bar_full.add(seg)
        bar_full.arrange(RIGHT, buff=0.02).move_to([-1.5, 0.9, 0])
        lbl_full = T("不截断：", 20, FG).next_to(bar_full, LEFT, buff=0.3)

        self.until("full")
        self.play(FadeIn(lbl_full), FadeIn(bar_full), FadeIn(decl), run_time=0.8)

        self.until("cut")
        bar_cut = VGroup()
        for i in range(20):
            seg = Rectangle(width=0.18, height=0.5, stroke_width=0.5, stroke_color=BG,
                            fill_color=PREFILL, fill_opacity=0.9)
            bar_cut.add(seg)
        for i in range(20):
            bg_seg = Rectangle(width=0.18, height=0.5, stroke_width=0.5, stroke_color=GRID,
                               fill_color=MUTED, fill_opacity=0.15)
            tip_seg = Rectangle(width=0.03, height=0.5, stroke_width=0,
                                fill_color=SWA, fill_opacity=1.0).align_to(bg_seg, RIGHT)
            bar_cut.add(VGroup(bg_seg, tip_seg))
        bar_cut.arrange(RIGHT, buff=0.02).move_to([-1.5, -0.1, 0])
        lbl_cut = T("截断后：", 20, FG).next_to(bar_cut, LEFT, buff=0.3)

        self.play(FadeIn(lbl_cut), FadeIn(bar_cut), run_time=1.0)

        self.until("total")
        t1 = T("不截断：400,000 行·层", 20, MUTED)
        t2 = T("截断后：202,800 行·层", 20, SWA)
        t3 = T("约 50.7% (理论减半)", 26, FG)
        res_box = VGroup(t1, t2, t3).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.2, 0.4, 0])
        self.play(FadeIn(res_box), run_time=0.8)

        self.finish()


class EP07_S10(DVScene):
    SHOT = "EP07-S10"

    def construct(self):
        head = self.fit_left_of_tags(header("这笔账简化了什么", "EP07 · S10 边界与代价"))
        self.add(head)

        box20 = RoundedRectangle(corner_radius=0.12, width=7.2, height=1.6,
                                 stroke_color=WARN, stroke_width=3, fill_color=WARN, fill_opacity=0.15)
        box20.move_to([0, 0.6, 0])
        t_l20 = T("第 20 层：交接点仍处理全长", 24, FG).move_to(box20).shift(UP * 0.3)
        sub_l20 = T("对全长 10,000 行执行全量归一化 + KV 投影", 18, MUTED).next_to(t_l20, DOWN, buff=0.15)
        g20 = VGroup(box20, t_l20, sub_l20)

        self.until("l20")
        self.play(FadeIn(g20), run_time=0.8)

        self.until("rows")
        c1 = Block("行数 ≠ 计算量", color=MUTED, w=3.6, h=1.0, size=20)
        c1.move_to([-2.4, -1.4, 0])
        c2 = Block("计算量减半 ≠ 速度快一倍", color=WARN, w=4.0, h=1.0, size=20)
        c2.move_to([2.4, -1.4, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.8)

        self.finish()


class EP07_S11(DVScene):
    SHOT = "EP07-S11"

    def construct(self):
        head = self.fit_left_of_tags(header("代价：它是近似", "EP07 · S11 总结与定调"))
        self.add(head)

        # Scale in top half (review D8, D9)
        scale = Scale("收益：常数重算", "代价：近似 SWA KV", left_color=KV, right_color=WARN,
                      w=6.4, h=2.2, size=20)
        scale.move_to([0, 0.9, 0])

        self.until("approx")
        self.play(FadeIn(scale), run_time=0.8)
        self.play(
            scale.beam.animate.rotate(-0.06),
            scale.right_pan.animate.shift(DOWN * 0.15),
            scale.left_pan.animate.shift(UP * 0.15),
            run_time=0.8,
        )

        self.until("test")
        snippet = "mode = 'compact' if cfg.compact else 'mask'"
        code = code_panel(snippet, "yoco_equiv.py:534", size=18, width=7.2)
        code.move_to([0, -0.5, 0])
        t_compare = Pill("测试仅比对：mask vs compact 两种写法", color=FG, size=18).move_to([0, -1.4, 0])
        t_not = Pill("未比较：截断 vs 不截断", color=WARN, size=18).move_to([0, -2.1, 0])
        test_group = VGroup(code, t_compare, t_not)
        self.play(FadeIn(test_group), run_time=1.0)

        self.until("report")
        # Replace test_group with report card to eliminate overlap (review D9)
        report_card = Block("官方技术报告：影响可忽略", color=DECODE, w=8.2, h=1.4, size=22,
                            sub="后训练专门模拟重放自适应（train-aware adaptation）")
        report_card.move_to([0, -1.1, 0])
        self.play(FadeOut(test_group), FadeIn(report_card), run_time=0.8)

        self.finish()


class EP07_S12(DVScene):
    SHOT = "EP07-S12"

    def construct(self):
        head = self.fit_left_of_tags(header("两种实现：盖住还是删掉", "EP07 · S12 机制实现"))
        self.add(head)

        # Matrices height >= 3.5 (12 * 0.30 = 3.6), with axes (review D10)
        m_mask = AttentionMatrix(12, window=4, cell=0.30).move_to([-3.4, -0.4, 0])
        ax_mask = m_mask.axes("查询 i ↓", "键 j →", size=16)
        lbl_mask = Pill("mask 模式 (保留全行)", color=MUTED, size=18).next_to(m_mask, UP, buff=0.3)

        m_comp = AttentionMatrix(12, window=4, cell=0.30).move_to([3.4, -0.4, 0])
        ax_comp = m_comp.axes("查询 i ↓", "键 j →", size=16)
        lbl_comp = Pill("compact 模式 (物理删行)", color=DECODE, size=18).next_to(m_comp, UP, buff=0.3)

        self.until("mask")
        self.play(FadeIn(m_mask), FadeIn(ax_mask), FadeIn(lbl_mask), run_time=0.8)

        self.until("compact")
        self.play(FadeIn(m_comp), FadeIn(ax_comp), FadeIn(lbl_comp), run_time=0.8)

        self.until("cut")
        mask_cells = m_mask.mask_left_of(6)
        comp_fade = VGroup(*[m_comp.cells(r, c) for r in range(6) for c in range(12) if m_comp.cells(r, c)])
        self.play(
            mask_cells.animate.set_fill(color=MUTED, opacity=0.2),
            FadeOut(comp_fade),
            run_time=1.2,
        )
        self.finish()


class EP07_S13(DVScene):
    SHOT = "EP07-S13"

    def construct(self):
        head = self.fit_left_of_tags(header("占位行：不能真正删空", "EP07 · S13 工程保护"))
        self.add(head)

        chunks = VGroup()
        for c_idx in range(4):
            ch = TokenRow(6, color=PREFILL, size=0.35, gap=0.06)
            chunks.add(ch)
        chunks.arrange(RIGHT, buff=0.45).move_to([0, 0.9, 0])
        c_lbl = T("输入分块处理（chunk = 2048）", 20, FG).next_to(chunks, UP, buff=0.25)

        # Footnote at y >= -2.75 (review D4, D10)
        decl = T("C++ clip_prefix 上界保护 (q_len − 1)", 18, MUTED).move_to([0, -2.4, 0])

        self.until("chunk")
        self.play(FadeIn(chunks), FadeIn(c_lbl), FadeIn(decl), run_time=0.8)

        self.until("hole")
        anims = []
        for ch in chunks[:3]:
            for cell in ch.cells():
                anims.append(cell.animate.set_fill(color=MUTED, opacity=0.2))
        self.play(*anims, run_time=0.8)

        self.until("assert")
        placeholder_dots = VGroup()
        for ch in chunks[:3]:
            last_cell = ch.cells()[-1]
            dot = Rectangle(width=0.35, height=0.35, stroke_color=DECODE, stroke_width=2,
                            fill_color=DECODE, fill_opacity=0.9).move_to(last_cell)
            placeholder_dots.add(dot)
        p_pill = Pill("强行保留 1 行占位符", color=DECODE, size=20).move_to([0, -0.4, 0])
        code_card = Block("内核前缀和越界保护", color=WARN, w=8.0, h=1.2, size=20,
                          sub="避免出现零长度块破坏 GPU 变长注意力指针")
        code_card.move_to([0, -1.4, 0])
        self.play(FadeIn(placeholder_dots), FadeIn(p_pill), FadeIn(code_card), run_time=0.8)
        self.finish()


class EP07_S14(DVScene):
    SHOT = "EP07-S14"

    def construct(self):
        head = self.fit_left_of_tags(header("回退预算：为什么多出六个", "EP07 · S14 投机协同"))
        self.add(head)

        draft_row = TokenRow(5, color=DRAFT, size=0.55, gap=0.18).move_to([0, 0.8, 0])
        lbl = T("投机草稿头预演：5 个候选 token", 20, DRAFT).next_to(draft_row, UP, buff=0.25)

        self.until("spec")
        self.play(FadeIn(draft_row), FadeIn(lbl), run_time=0.8)

        self.until("reject")
        rej_cross = T("✗", 36, WARN).move_to(draft_row.cells()[3])
        rej_txt = T("主模型验证未通过 → 回退指针", 20, WARN).next_to(draft_row, DOWN, buff=0.3)
        self.play(FadeIn(rej_cross), FadeIn(rej_txt), run_time=0.8)

        self.until("margin")
        bracket_card = Block("回退安全预算：5 + 1 = 6", color=DECODE, w=6.8, h=1.4, size=22,
                             sub="推断：保证最大回退时滑动窗口仍完整 (128 + 6 = 134)")
        bracket_card.move_to([0, -1.4, 0])
        self.play(FadeIn(bracket_card), run_time=0.8)
        self.finish()


class EP07_S15(DVScene):
    SHOT = "EP07-S15"

    def construct(self):
        head = self.fit_left_of_tags(header("决定权在仓库之外", "EP07 · S15 开源边界"))
        self.add(head)

        b_entry = Block("Entrypoint 网关", color="#D29922", w=3.6, h=1.4, size=20, sub="统一入口 · 未开源")
        b_entry.move_to([-3.6, 0.8, 0])
        b_fs = Block("3FS 存储集群", color="#D29922", w=3.6, h=1.4, size=20, sub="长前缀匹配与命中决策")
        b_fs.move_to([-3.6, -1.0, 0])

        b_engine = Block("DeepInfer 引擎", color=KV, w=4.2, h=2.0, size=22, sub="离线推理执行体")
        b_engine.move_to([3.4, 0.6, 0])

        self.until("arch")
        self.play(FadeIn(b_entry), FadeIn(b_fs), FadeIn(b_engine), run_time=0.8)

        self.until("missing")
        # Material from doc on screen (review B2)
        rule_pill = Pill("文档规则：最大命中 ≤ L − 134", color=DECODE, size=18).move_to([0, -0.1, 0])
        no_prefix_pill = Pill("仓库内无前缀匹配代码", color=WARN, size=18).move_to([3.4, -0.8, 0])
        self.play(FadeIn(rule_pill), FadeIn(no_prefix_pill), run_time=0.8)

        self.until("recv")
        # Pull apart recv_slot from b_engine to eliminate overlap (review D11)
        arr = Arrow(b_entry.get_right(), b_engine.get_left(), color=DECODE, stroke_width=3)
        recv_slot = Pill("接收字段: cached_hit_tokens", color=DECODE, size=18).move_to([3.4, -1.8, 0])
        self.play(Create(arr), FadeIn(recv_slot), run_time=0.8)
        self.finish()


class EP07_S16(DVScene):
    SHOT = "EP07-S16"

    def construct(self):
        head = self.fit_left_of_tags(header("第三方怎么看：vLLM 的实测", "EP07 · S16 业界对照"))
        self.add(head)

        # Fix screen text: "默认关闭；README 推荐 140" (review B3)
        c_deep = Block("DeepInfer 原版", color=MUTED, w=3.5, h=2.5, size=20,
                       sub="默认关闭\nREADME 推荐 140")
        c_deep.move_to([-3.8, 0.4, 0])

        # Separate conditions per review B1
        c_vllm = Block("vLLM (PR #58132)", color=DECODE, w=3.8, h=2.5, size=20,
                       sub="GB200 (16K起)\nTP4: −25–36%\nDEP4: −37–45%")
        c_vllm.move_to([0, 0.4, 0])

        c_sgl = Block("SGLang 适配", color=MUTED, w=3.5, h=2.5, size=20,
                       sub="跨层共享注意力\n统一流水线")
        c_sgl.move_to([3.8, 0.4, 0])

        self.until("compare")
        self.play(FadeIn(c_deep), FadeIn(c_vllm), FadeIn(c_sgl), run_time=0.8)

        self.until("vllm")
        self.play(c_vllm.animate.scale(1.05), run_time=0.6)

        self.until("eval")
        stat_card = Block("评测准确率分差 < 1.5 标准误", color=FG, w=7.8, h=1.2, size=20,
                          sub="GSM8K 与 GPQA 基准 · 逐点公开数据仅限 GSM8K")
        stat_card.move_to([0, -1.8, 0])
        self.play(FadeIn(stat_card), run_time=0.8)
        self.finish()


class EP07_S17(DVScene):
    SHOT = "EP07-S17"

    def construct(self):
        head = self.fit_left_of_tags(header("暂停题：设成 128 会怎样", "EP07 · S17 自测题"))
        self.add(head)

        q_card = Block("自测题", color=DECODE, w=8.5, h=2.0, size=24,
                       sub="如果为了省显存，手动将 KEEP_TOKENS 设为 128 会发生什么？")
        q_card.move_to([0, 0.6, 0])

        self.until("quiz")
        self.play(FadeIn(q_card), run_time=0.8)

        self.until("answer")
        ans_box = Block("答案：启动断言失败，拒绝运行", color=WARN, w=8.5, h=1.8, size=22,
                        sub="window_size(128) + backtracking(6) = 134 > 128\n模型初始化时硬性断言崩溃")
        ans_box.move_to([0, -1.5, 0])
        self.play(FadeIn(ans_box), run_time=0.8)
        self.finish()


class EP07_S18(DVScene):
    SHOT = "EP07-S18"

    def construct(self):
        head = self.fit_left_of_tags(header("算一算总账", "EP07 · S18 架构取舍"))
        self.add(head)

        # Scale pans <= 8 chars per review D12
        scale = Scale("收益：常数重算", "代价：数学近似", left_color=KV, right_color=WARN,
                      w=6.4, h=2.2, size=20)
        scale.move_to([0, 1.0, 0])

        left_list = VGroup(
            Pill("前缀补算变为常数", color=KV, size=18),
            Pill("后20层计算量近乎减半", color=KV, size=18),
            Pill("显存无需持久化SWA", color=KV, size=18),
        ).arrange(DOWN, buff=0.15).move_to([-3.2, -0.9, 0])

        right_list = VGroup(
            Pill("非严格数学等价", color=WARN, size=18),
            Pill("依赖后训练重放适配", color=WARN, size=18),
            Pill("需网关与存储深度协同", color=WARN, size=18),
        ).arrange(DOWN, buff=0.15).move_to([3.2, -0.9, 0])

        self.until("scale")
        self.play(FadeIn(scale), FadeIn(left_list), FadeIn(right_list), run_time=0.8)

        self.until("cost")
        self.play(
            scale.beam.animate.rotate(-0.04),
            scale.right_pan.animate.shift(DOWN * 0.1),
            scale.left_pan.animate.shift(UP * 0.1),
            run_time=0.8,
        )
        tag = Pill("压低单 token 成本 > 理论对称", color=DECODE, size=18).move_to([0, -2.1, 0])
        self.play(FadeIn(tag), run_time=0.8)
        self.finish()


class EP07_S19(DVScene):
    SHOT = "EP07-S19"

    def construct(self):
        head = self.fit_left_of_tags(header("三句话", "EP07 · S19 核心复述"))
        self.add(head)

        c1 = Block("1. 精确重建很贵，有界重放做近似", color=DECODE, w=8.8, h=1.0, size=20)
        c1.move_to([0, 0.8, 0])
        c2 = Block("2. 后 20 层算力近乎减半，代码保留 ≥ 134 行", color=DECODE, w=8.8, h=1.0, size=20)
        c2.move_to([0, -0.3, 0])
        c3 = Block("3. 测试验证写法一致，精度靠后训练兜底", color=DECODE, w=8.8, h=1.0, size=20)
        c3.move_to([0, -1.4, 0])

        self.until("c1")
        self.play(FadeIn(c1), run_time=0.8)

        self.until("c2")
        self.play(FadeIn(c2), run_time=0.8)

        self.until("c3")
        self.play(FadeIn(c3), run_time=0.8)
        self.finish()


class EP07_S20(DVScene):
    SHOT = "EP07-S20"

    def construct(self):
        head = self.fit_left_of_tags(header("下集预告：宽专家并行", "EP07 · S20 下集钩子"))
        self.add(head)

        # MiniMap in stage center, well above subtitle band (review D2, D13)
        mmap = MiniMap(active="Prefill", scale=1.0).move_to([0, 0.8, 0])
        hook_txt = T("Prefill 阶段完成：共享 KV 就绪", 22, PREFILL).next_to(mmap, UP, buff=0.35)
        self.play(FadeIn(mmap), FadeIn(hook_txt), run_time=0.8)

        self.until("hook")
        self.play(Indicate(mmap.submobjects[0][2], color=FG, scale_factor=1.1), run_time=0.8)

        self.until("next")
        next_mmap = MiniMap(active="Decode", scale=1.0).move_to([0, 0.8, 0])
        exp_box = Block("Decode 站：专家太多，单卡装不下", color=EXPERT, w=8.0, h=1.4, size=22,
                        sub="EP64 宽专家并行：几十张卡如何分工？")
        exp_box.move_to([0, -1.2, 0])
        self.play(Transform(mmap, next_mmap), FadeIn(exp_box), run_time=0.8)
        self.finish()
