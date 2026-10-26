"""EP99 smoke-test scenes. Also the reference for how shots use dvlib."""
from manim import DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Indicate, LaggedStart, Transform, VGroup, Write

from dvlib import (CPU, DECODE, GPU, MUTED, PREFILL, SWA, DVScene, MiniMap, T, Timeline, TokenRow, code_panel,
                   header, window_bracket)


class EP99_S01(DVScene):
    SHOT = "EP99-S01"
    SHOW_BADGE = False

    def construct(self):
        title = T("读懂 DeepInfer", 64)
        sub = T("一个请求的一生", 30, MUTED).next_to(title, DOWN, buff=0.3)
        self.play(Write(title), FadeIn(sub, shift=UP * 0.2), run_time=1.2)
        self.until("map")
        maps = [MiniMap(active=s, scale=0.9) for s in MiniMap.STATIONS]
        for m in maps:
            m.to_edge(DOWN, buff=1.6)
        cur = maps[0]
        self.play(FadeIn(cur), run_time=0.4)
        for m in maps[1:] + [MiniMap(active="Prefill", scale=0.9).to_edge(DOWN, buff=1.6)]:
            self.play(Transform(cur, m), run_time=0.45)
        self.finish()


class EP99_S02(DVScene):
    SHOT = "EP99-S02"

    def construct(self):
        self.add(header("只重算最后一小段", "decoder 层的 prefill"))
        n = 24  # each cell stands for a group of tokens; the scale is symbolic
        row = TokenRow(n, PREFILL, size=0.38).shift(UP * 0.2)
        note = T("每格代表一段 token（示意）", 18, MUTED).next_to(row, DOWN, buff=0.35).align_to(row, LEFT)
        self.play(LaggedStart(*[FadeIn(c) for c in row.cells()], lag_ratio=0.03), FadeIn(note), run_time=1.2)
        win = window_bracket(row, 0, 5, SWA, "窗口 128")
        self.play(Create(win), run_time=0.5)
        self.until("win")
        for start in (6, 12, 18):
            self.play(win.animate.move_to(window_bracket(row, start, start + 5, SWA, "窗口 128")), run_time=0.6)
        self.until("keep")
        keep = window_bracket(row, 17, 23, DECODE, "保留 140 ≥ 128 + 6")
        greys = [c.animate.set_fill(MUTED, opacity=0.25) for c in row.cells()[:17]]
        self.play(FadeOut(win), Create(keep), *greys, run_time=0.9)
        self.until("why")
        self.play(Indicate(keep[1], color=DECODE), run_time=0.8)
        self.finish()


class EP99_S03(DVScene):
    SHOT = "EP99-S03"

    def construct(self):
        self.add(header("CPU 永远晚一步", "零开销异步调度（ZOS）"))
        tl = Timeline(["CPU", "GPU"], width=7.0, scale=1.0).shift(LEFT * 2.2 + UP * 0.6)
        self.play(FadeIn(tl), run_time=0.5)
        self.until("lanes")
        bars = VGroup()
        for k in range(3):
            x = k * 2.2
            bars.add(tl.bar(1, x, 1.5, f"forward {k + 1}", GPU), tl.bar(1, x + 1.5, 0.6, "sample", DECODE))
            if k:
                bars.add(tl.bar(0, x + 0.1, 1.2, f"后处理 {k}", CPU))
        self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.15), run_time=1.6)
        self.until("code")
        code = code_panel(
            "def execute_model_step(...):\n"
            "    forward(step_N)\n"
            "    postprocess(step_N_minus_1)\n"
            "    sample(step_N)",
            "deepinfer/worker/worker.py:89-189（示意，非原文）", highlight=[2, 3, 4], size=18,
        ).to_edge(RIGHT, buff=0.4).shift(DOWN * 1.4)
        self.play(FadeIn(code, shift=LEFT * 0.3), run_time=0.6)
        self.finish()
