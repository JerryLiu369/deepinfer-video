"""Placeholder scene used for animatics and for shots that have no scene class yet."""
import os

from manim import DOWN, FadeIn, VGroup, config

from dvlib import MUTED, DVScene, T, header


class AutoCard(DVScene):
    def construct(self):
        m = self.meta
        g = self.fit_left_of_tags(header(f"{self.shot_id}  {m.get('title', '')}"))
        lines = m.get("screen_text") or []
        body = VGroup(*[T(s, 40) for s in lines]).arrange(DOWN, buff=0.35) if lines else VGroup()
        vis = (m.get("visual") or "").strip().splitlines()
        note = T(("画面：" + vis[0])[:60] if vis else "（无画面说明）", 20, MUTED).to_edge(DOWN, buff=1.4)
        if note.width > config.frame_width - 1.0:
            note.scale_to_fit_width(config.frame_width - 1.0)
        self.add(g)
        if len(body):
            self.play(FadeIn(body), run_time=0.5)
        self.add(note)
        self.finish()
