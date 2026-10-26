"""dvlib: shared visual language for the DeepInfer video series (Manim CE >= 0.19).

Every shot scene subclasses DVScene and declares SHOT = "EPxx-Syy".
Timing comes from build/EPxx/timing.json (written by tools/tts.py); before TTS
exists, an estimate from shots.json is used so previews still render.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from manim import (
    DOWN, LEFT, RIGHT, UP, UL, UR, DL, DR, ORIGIN,
    Arrow, Create, FadeIn, FadeOut, Line, Polygon, Rectangle, RoundedRectangle,
    Scene, SurroundingRectangle, Text, VGroup, Write, config,
)

# ---------------------------------------------------------------- palette
BG = "#0E1117"
FG = "#E6EDF3"
MUTED = "#8B949E"
GRID = "#30363D"

PREFILL = "#F0883E"   # prefill / input side
DECODE = "#58A6FF"    # decode / generation side
KV = "#3FB950"        # block KV cache
SWA = "#D2A8FF"       # sliding-window state
EXPERT = "#E3B341"    # MoE experts / EP
CPU = "#A5D6FF"       # host-side work
GPU = "#7EE787"       # device-side work
WARN = "#F85149"      # cost, waste, error
DRAFT = "#FF7B72"     # speculative draft tokens

GRADE_COLORS = {"A": "#3FB950", "B": "#58A6FF", "C": "#D2A8FF", "D": "#8B949E", "E": "#E3B341"}
GRADE_LABELS = {"A": "A 代码证实", "B": "B 官方文档", "C": "C 第三方实测", "D": "D 社区说法", "E": "E 推断/示意"}
SCOPE_LABELS = {"oss": ("开源代码里有", "#3FB950"), "doc": ("仅文档描述 · 未开源", "#D29922"),
                "mixed": ("代码 + 文档", "#58A6FF"), "general": ("通用概念", "#8B949E")}

SANS = os.environ.get("DV_FONT", "Noto Sans CJK SC")
MONO = os.environ.get("DV_MONO_FONT", "Noto Sans Mono")

config.background_color = BG
Text.set_default(font=SANS, color=FG)

# Bottom band reserved for subtitles (in Manim units, frame height is 8).
SUBTITLE_SAFE_Y = -2.9

# Layout grid (Manim units; frame is 14.22 x 8, origin at the centre). docs/04_VISUAL_LANGUAGE.md section 2.
MIN_FONT = 16                     # smallest font_size allowed on screen, after any scaling
FRAME_X = config.frame_width / 2
FRAME_Y = config.frame_height / 2
SAFE_X = FRAME_X - 0.3            # nothing may cross |x| > SAFE_X
STAGE = {"left": -6.6, "right": 6.6, "top": 2.3, "bottom": -2.75}   # below the header, above subtitles


def _sized(t: Text, size: float) -> Text:
    # Remember the requested size so check_layout() can compute the size actually shown after scaling.
    t._dv_size = float(size)
    t._dv_h0 = t.height
    return t


def _min_size(size: float, s: str) -> float:
    if size < MIN_FONT:
        print(f"[dvlib] WARN font_size {size} < {MIN_FONT} for {s[:16]!r}; raised to {MIN_FONT}")
        return MIN_FONT
    return size


def T(s: str, size: int = 36, color: str = FG, **kw) -> Text:
    size = _min_size(size, s)
    return _sized(Text(s, font_size=size, color=color, **kw), size)


def M(s: str, size: int = 28, color: str = FG, **kw) -> Text:
    size = _min_size(size, s)
    return _sized(Text(s, font=MONO, font_size=size, color=color, **kw), size)


def shown_size(t: Text) -> float:
    """font_size as it appears on screen (requested size times any later scaling)."""
    h0 = getattr(t, "_dv_h0", 0) or 0
    return t._dv_size * t.height / h0 if h0 else getattr(t, "_dv_size", MIN_FONT)


def fit_stage(mob, center: bool = True, buff: float = 0.0):
    """Shrink mob to fit the main stage (never enlarges); optionally centre it there."""
    w = STAGE["right"] - STAGE["left"] - 2 * buff
    h = STAGE["top"] - STAGE["bottom"] - 2 * buff
    k = min(1.0, w / max(mob.width, 1e-6), h / max(mob.height, 1e-6))
    if k < 1.0:
        mob.scale(k)
    if center:
        mob.move_to([(STAGE["left"] + STAGE["right"]) / 2, (STAGE["top"] + STAGE["bottom"]) / 2, 0])
    return mob


def layout_exempt(mob):
    """Exclude mob (and its children) from check_layout, e.g. an element sliding in from off-screen."""
    mob._dv_exempt = True
    return mob


def _box(m):
    return (m.get_left()[0], m.get_right()[0], m.get_bottom()[1], m.get_top()[1])


def _inter(a, b) -> float:
    w = min(a[1], b[1]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[2], b[2])
    return w * h if w > 0 and h > 0 else 0.0


def _area(a) -> float:
    return max(a[1] - a[0], 0) * max(a[3] - a[2], 0)


def _contains(outer, inner, tol: float = 0.03) -> bool:
    return (outer[0] - tol <= inner[0] and inner[1] <= outer[1] + tol
            and outer[2] - tol <= inner[2] and inner[3] <= outer[3] + tol)


def _visible(m) -> bool:
    fam = m.family_members_with_points()
    return any(x.get_fill_opacity() > 0.05 or x.get_stroke_opacity() > 0.05 for x in fam)


def _walk(mobs, texts, shapes):
    for m in mobs:
        if getattr(m, "_dv_exempt", False):
            continue
        if isinstance(m, Text):
            if _visible(m):
                texts.append(m)
            continue
        if m.has_points() and not type(m).__name__.endswith("Tip") \
                and isinstance(m, (Rectangle, Polygon)) and m.get_fill_opacity() >= 0.3:
            shapes.append(m)
        _walk(m.submobjects, texts, shapes)

# ---------------------------------------------------------------- timing
def _work_dir() -> Path:
    return Path(os.environ.get("DV_WORK", "work")).resolve()


def load_shot(shot_id: str) -> dict:
    ep = shot_id.split("-")[0]
    build = _work_dir() / "build" / ep
    meta = {}
    shots_path = build / "shots.json"
    if shots_path.exists():
        for s in json.loads(shots_path.read_text(encoding="utf-8"))["shots"]:
            if s["id"] == shot_id:
                meta = s
                break
    timing = {}
    timing_path = build / "timing.json"
    if timing_path.exists():
        timing = json.loads(timing_path.read_text(encoding="utf-8")).get("shots", {}).get(shot_id, {})
    if not timing:
        timing = {"duration": float(meta.get("est_s") or meta.get("target_s") or 8.0),
                  "cues": meta.get("est_cues", {}), "estimated": True}
    return {"meta": meta, "timing": timing}


class DVScene(Scene):
    """Base scene: background, evidence badge, scope tag, cue-synced waiting."""

    SHOT: str = ""
    SHOW_BADGE = True

    def setup(self):
        shot_id = os.environ.get("DV_SHOT") or self.SHOT
        info = load_shot(shot_id) if shot_id else {"meta": {}, "timing": {"duration": 8.0, "cues": {}}}
        self.shot_id = shot_id
        self.meta = info["meta"]
        self.timing = info["timing"]
        # Scene already uses .duration internally; keep shot timing under its own name.
        self.shot_duration = float(self.timing.get("duration", 8.0))
        self.cues = {k: float(v) for k, v in self.timing.get("cues", {}).items()}
        if self.SHOW_BADGE:
            self.add_corner_tags()

    # elapsed seconds of rendered animation so far
    @property
    def now(self) -> float:
        return float(self.renderer.time)

    def cue(self, name: str) -> float:
        if name not in self.cues:
            raise KeyError(f"{self.shot_id}: cue [#{name}] not found; known: {sorted(self.cues)}")
        return self.cues[name]

    def until(self, name: str, min_wait: float = 0.0):
        """Hold until narration reaches cue [#name]."""
        self.check_layout(f"cue {name}")
        gap = self.cue(name) - self.now
        if gap < -0.25:
            print(f"[dvlib] WARN {self.shot_id}: animation is {-gap:.2f}s late for cue {name}")
        self.wait(max(gap, min_wait, 1 / config.frame_rate))

    def finish(self, fade: bool = False):
        """Hold the last frame until the shot's narration ends."""
        self.check_layout("end")
        if fade:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)
        gap = self.shot_duration - self.now
        if gap < -0.25:
            print(f"[dvlib] WARN {self.shot_id}: animation runs {-gap:.2f}s past narration; assemble will pad audio")
        self.wait(max(gap, 1 / config.frame_rate))

    def check_layout(self, where: str = ""):
        """Warn about what frame reviewers otherwise have to catch by eye (docs/04 section 2):
        text below MIN_FONT, text on text, text cut by a filled shape, anything outside the frame,
        in the subtitle band, or on the corner tags. Runs at every until() and at finish().
        DV_LAYOUT=strict turns warnings into errors; DV_LAYOUT=off disables the check."""
        mode = os.environ.get("DV_LAYOUT", "warn")
        if mode == "off":
            return
        seen = self.__dict__.setdefault("_layout_seen", set())
        tags = getattr(self, "corner_tags", VGroup())
        tag_ids = {id(m) for m in tags.get_family()}
        texts, shapes = [], []
        _walk([m for m in self.mobjects if id(m) not in tag_ids], texts, shapes)
        problems = []
        tb = [(t, _box(t)) for t in texts]
        sb = [(s, _box(s)) for s in shapes]
        free_band = getattr(self, "ALLOW_SUBTITLE_BAND", False)
        for t, b in tb:
            label = getattr(t, "text", "?")[:12]
            if hasattr(t, "_dv_size") and shown_size(t) < MIN_FONT - 0.5:
                problems.append(f"'{label}' shown at font_size {shown_size(t):.0f} (< {MIN_FONT})")
            if b[0] < -SAFE_X or b[1] > SAFE_X or b[3] > FRAME_Y - 0.15:
                problems.append(f"'{label}' leaves the safe frame")
            if b[2] < SUBTITLE_SAFE_Y and not free_band:
                problems.append(f"'{label}' enters the subtitle band (bottom {b[2]:.2f} < {SUBTITLE_SAFE_Y})")
            if len(tags) and _inter(b, _box(tags)) > 0:
                problems.append(f"'{label}' collides with the corner tags")
            fam = {id(x) for x in t.get_family()}
            for s, c in sb:
                if id(s) in fam:
                    continue
                if _inter(b, c) > 0.15 * min(_area(b), _area(c)) and not _contains(c, b):
                    problems.append(f"'{label}' overlaps a filled shape near ({c[0]:.1f}, {c[2]:.1f}); "
                                    f"move it off or put it fully inside")
                    break
        for i in range(len(tb)):
            for j in range(i + 1, len(tb)):
                (t1, b1), (t2, b2) = tb[i], tb[j]
                if _inter(b1, b2) > 0.1 * min(_area(b1), _area(b2)):
                    problems.append(f"text overlaps text: '{getattr(t1, 'text', '?')[:10]}' / "
                                    f"'{getattr(t2, 'text', '?')[:10]}'")
        for m in self.mobjects:
            if id(m) in tag_ids or getattr(m, "_dv_exempt", False) or not m.get_family()[-1].has_points():
                continue
            if m.width >= config.frame_width * 0.95:
                continue  # full-frame backdrops
            b = _box(m)
            if b[2] < SUBTITLE_SAFE_Y - 0.02 and not free_band:
                problems.append(f"{type(m).__name__} enters the subtitle band (bottom {b[2]:.2f})")
            if b[0] < -FRAME_X or b[1] > FRAME_X or b[3] > FRAME_Y:
                problems.append(f"{type(m).__name__} leaves the frame")
        new = [p for p in dict.fromkeys(problems) if p not in seen]
        seen.update(new)
        for p in new:
            msg = f"[dvlib] WARN {self.shot_id} layout @{where} t={self.now:.1f}s: {p}"
            if mode == "strict":
                raise RuntimeError(msg)
            print(msg)

    def add_corner_tags(self):
        tags = VGroup()
        self.corner_tags = tags
        grade = (self.meta.get("badge") or "").upper()
        if grade in GRADE_LABELS:
            tags.add(Pill(GRADE_LABELS[grade], GRADE_COLORS[grade]))
        scope = self.meta.get("scope") or ""
        if scope in SCOPE_LABELS:
            label, color = SCOPE_LABELS[scope]
            tags.add(Pill(label, color))
        if len(tags):
            tags.arrange(LEFT, buff=0.15).to_corner(UR, buff=0.3)
            self.add(tags)

    def fit_left_of_tags(self, mob, gap: float = 0.3):
        """Shrink a top-left element (e.g. header) so it stops short of the corner tags."""
        right = self.corner_tags.get_left()[0] - gap if len(self.corner_tags) else config.frame_width / 2 - 0.45
        room = right - mob.get_left()[0]
        if mob.width > room > 0:
            left = mob.get_left()
            mob.scale(room / mob.width, about_point=left)
        return mob


# ---------------------------------------------------------------- components
class Pill(VGroup):
    def __init__(self, label: str, color: str, size: int = 20):
        super().__init__()
        txt = T(label, size, color)
        box = RoundedRectangle(corner_radius=0.12, width=txt.width + 0.35, height=txt.height + 0.22,
                               stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.12)
        txt.move_to(box)
        self.add(box, txt)


def header(title: str, subtitle: str | None = None) -> VGroup:
    g = VGroup(T(title, 40))
    if subtitle:
        g.add(T(subtitle, 24, MUTED))
    g.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.45)
    return g


class TokenRow(VGroup):
    """A row of token cells. colors: one color or a list per cell.

    Per-cell labels are only readable when they are short (1-3 characters at MIN_FONT fit a 0.32 cell);
    for longer names label every k-th cell or put one caption under the whole row."""

    def __init__(self, n: int, color=PREFILL, size: float = 0.32, gap: float = 0.06,
                 labels: list[str] | None = None, opacity: float = 0.85):
        super().__init__()
        cols = color if isinstance(color, list) else [color] * n
        for i in range(n):
            sq = Rectangle(width=size, height=size, stroke_width=1, stroke_color=BG,
                           fill_color=cols[i], fill_opacity=opacity)
            self.add(sq)
        self.arrange(RIGHT, buff=gap)
        if labels:
            for sq, lab in zip(self, labels):
                if lab:
                    t = T(lab, MIN_FONT, MUTED).next_to(sq, DOWN, buff=0.06)
                    self.add(t)

    def cells(self):
        return [m for m in self.submobjects if isinstance(m, Rectangle)]

    def span(self, i: int, j: int) -> VGroup:
        """Cells i..j inclusive, for highlighting a window."""
        c = self.cells()
        return VGroup(*c[i:j + 1])


def window_bracket(row: TokenRow, i: int, j: int, color=SWA, label: str | None = None) -> VGroup:
    box = SurroundingRectangle(row.span(i, j), color=color, buff=0.06, stroke_width=3)
    g = VGroup(box)
    if label:
        g.add(T(label, 20, color).next_to(box, UP, buff=0.1))
    return g


class Block(VGroup):
    """Labelled box: GPU, engine, KV block, storage node..."""

    def __init__(self, label: str, color=FG, w: float = 2.4, h: float = 1.0, size: int = 24,
                 sub: str | None = None, fill: float = 0.12):
        super().__init__()
        txt = VGroup(T(label, size, FG))
        if sub:
            txt.add(T(sub, max(MIN_FONT, int(size * 0.7)), MUTED))
        txt.arrange(DOWN, buff=0.06)
        # The box grows to fit its text; shrinking the text instead is what made labels unreadable.
        w, h = max(w, txt.width + 0.35), max(h, txt.height + 0.25)
        box = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color,
                               stroke_width=2.5, fill_color=color, fill_opacity=fill)
        txt.move_to(box)
        self.box = box
        self.add(box, txt)


def arrow(a, b, color=MUTED, label: str | None = None) -> VGroup:
    ar = Arrow(a.get_right() if hasattr(a, "get_right") else a, b.get_left() if hasattr(b, "get_left") else b,
               buff=0.1, color=color, stroke_width=3, max_tip_length_to_length_ratio=0.12)
    g = VGroup(ar)
    if label:
        g.add(T(label, 18, color).next_to(ar, UP, buff=0.05))
    return g


class Timeline(VGroup):
    """Swim-lane timeline (e.g. CPU vs GPU). Units: seconds of the depicted process."""

    def __init__(self, lanes: list[str], width: float = 11.0, lane_h: float = 0.7, scale: float = 1.0):
        super().__init__()
        self.lane_names = lanes
        self.width, self.lane_h, self.scale_x = width, lane_h, scale
        self.labels = VGroup(*[T(n, 22, MUTED) for n in lanes]).arrange(DOWN, buff=lane_h - 0.3, aligned_edge=RIGHT)
        self.axis_x0 = 0.0
        self.rows = VGroup()
        for k, _ in enumerate(lanes):
            ln = Line(LEFT * width / 2, RIGHT * width / 2, color=GRID, stroke_width=1)
            ln.shift(DOWN * k * lane_h)
            self.rows.add(ln)
        self.labels.next_to(self.rows, LEFT, buff=0.3)
        for lab, row in zip(self.labels, self.rows):
            lab.set_y(row.get_y())
        self.add(self.rows, self.labels)

    def bar(self, lane: int, start: float, dur: float, label: str = "", color=GPU) -> VGroup:
        row = self.rows[lane]
        x0 = row.get_left()[0] + start * self.scale_x
        rect = Rectangle(width=max(dur * self.scale_x, 0.02), height=self.lane_h * 0.6, stroke_width=1,
                         stroke_color=BG, fill_color=color, fill_opacity=0.85)
        rect.move_to([x0 + rect.width / 2, row.get_y(), 0])
        g = VGroup(rect)
        if label:
            t = T(label, MIN_FONT, BG)
            if t.width <= rect.width - 0.08:
                g.add(t.move_to(rect))
            else:  # too narrow to hold readable text: label goes above the bar instead of shrinking
                g.add(T(label, MIN_FONT, color).next_to(rect, UP, buff=0.05))
        return g


class MiniMap(VGroup):
    """'一个请求的一生' station map shown in a corner; highlight the active station."""

    STATIONS = ["入口", "路由", "Prefill", "KV 存储", "Decode", "输出解析"]

    def __init__(self, active: str | None = None, scale: float = 1.0):
        """scale only sizes the boxes; labels stay at MIN_FONT or larger (about 7.3 units wide at 1.0).
        Use it as a section opener or in the top band, not as a permanent corner decoration."""
        super().__init__()
        dots = VGroup()
        for name in self.STATIONS:
            on = name == active
            t = T(name, MIN_FONT + 2 if on else MIN_FONT, FG if on else MUTED)
            box = RoundedRectangle(corner_radius=0.08, width=max(1.0 * scale, t.width + 0.25),
                                   height=max(0.42 * scale, t.height + 0.18),
                                   stroke_color=DECODE if on else GRID, stroke_width=3 if on else 1.5,
                                   fill_color=DECODE if on else BG, fill_opacity=0.25 if on else 0.0)
            dots.add(VGroup(box, t.move_to(box)))
        dots.arrange(RIGHT, buff=0.1)
        self.add(dots)


def code_panel(code: str, path_label: str, highlight: list[int] | None = None, size: int = 20,
               width: float | None = None) -> VGroup:
    """Monospace code card; highlight uses 1-based line numbers of the snippet."""
    lines = code.rstrip("\n").split("\n")
    rows = VGroup()
    for k, line in enumerate(lines, 1):
        col = FG if (not highlight or k in highlight) else MUTED
        rows.add(M(line if line else " ", size, col))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    pad = 0.3
    lab = M(path_label, max(MIN_FONT, int(size * 0.75)), MUTED)
    w = max(width or 0, rows.width + 2 * pad, lab.width + 2 * pad)
    bg = RoundedRectangle(corner_radius=0.1, width=w, height=rows.height + lab.height + 2 * pad + 0.15,
                          stroke_color=GRID, fill_color="#161B22", fill_opacity=1)
    lab.align_to(bg, UL).shift(DOWN * 0.15 + RIGHT * pad)
    rows.next_to(lab, DOWN, buff=0.15, aligned_edge=LEFT)
    g = VGroup(bg, rows, lab)
    if highlight:
        for k in highlight:
            hl = Rectangle(width=w - 0.1, height=rows[k - 1].height + 0.08, stroke_width=0,
                           fill_color=DECODE, fill_opacity=0.12).move_to([bg.get_x(), rows[k - 1].get_y(), 0])
            g.add_to_back(hl)
        g.add_to_back(g.submobjects.pop(g.submobjects.index(bg)))
    return g


def number_card(value: str, unit: str, condition: str, color=DECODE, backdrop: bool = True) -> VGroup:
    """Big number with its mandatory condition line underneath.

    The card sits on an opaque backdrop so it can never be read through the diagram behind it;
    still, place it in free space or dim the diagram first (docs/04 section 2)."""
    v = T(value, 72, color)
    u = T(unit, 30, FG).next_to(v, RIGHT, buff=0.2, aligned_edge=DOWN)
    c = T(condition, 20, MUTED)
    g = VGroup(VGroup(v, u), c).arrange(DOWN, buff=0.2)
    if backdrop:
        bg = RoundedRectangle(corner_radius=0.12, width=g.width + 0.6, height=g.height + 0.45,
                              stroke_color=GRID, stroke_width=1.5, fill_color=BG, fill_opacity=0.96).move_to(g)
        g = VGroup(bg, g)
    return g


class LayerStack(VGroup):
    """40 thin horizontal layer bars stacked vertically."""

    def __init__(self, n: int = 40, split: int = 20, colors=(PREFILL, DECODE),
                 w: float = 1.2, h: float = 5.2):
        super().__init__()
        self.n = n
        self.split = split
        self.colors = colors
        self.bars = []
        bar_h = (h - 0.2) / n
        gap = 0.02
        split_gap = 0.14
        y = h / 2
        for i in range(n):
            col = colors[0] if i < split else colors[1]
            rect = RoundedRectangle(corner_radius=0.02, width=w, height=bar_h,
                                    stroke_color=col, stroke_width=1.5,
                                    fill_color=col, fill_opacity=0.35)
            rect.move_to([0, y, 0])
            self.bars.append(rect)
            self.add(rect)
            y -= (bar_h + (split_gap if i == split - 1 else gap))
        self.center()

    def layer(self, k: int) -> RoundedRectangle:
        return self.bars[k]

    def segment(self, a: int, b: int) -> VGroup:
        return VGroup(*self.bars[a:b])

    def range_label(self, a: int, b: int, label: str, side=LEFT, color=MUTED, size: int = 20) -> VGroup:
        """Brace-like tick plus label for layers a..b-1 (0-based), e.g. range_label(0, 20, "第 1–20 层")."""
        seg = self.segment(a, b)
        tick = Line(seg.get_corner(UP + side), seg.get_corner(DOWN + side), color=color, stroke_width=2)
        tick.shift(side * 0.15)
        return VGroup(tick, T(label, size, color).next_to(tick, side, buff=0.12))


class AttentionMatrix(VGroup):
    """n x n attention grid with causal SWA band."""

    def __init__(self, n: int = 16, window: int = 4, cell: float = 0.28):
        super().__init__()
        self.n = n
        self.window = window
        self.cell_size = cell
        self.grid = {}
        for r in range(n):
            for c in range(n):
                is_visible = (c <= r) and (r - c < window)
                col = SWA if is_visible else GRID
                op = 0.85 if is_visible else 0.15
                sq = Rectangle(width=cell, height=cell, stroke_width=1, stroke_color=BG,
                               fill_color=col, fill_opacity=op)
                sq.move_to([(c - n / 2 + 0.5) * cell, (n / 2 - r - 0.5) * cell, 0])
                self.grid[(r, c)] = sq
                self.add(sq)

    def cells(self, r: int, c: int) -> Rectangle:
        return self.grid.get((r, c))

    def axes(self, row_label: str = "当前 token（查询）↓", col_label: str = "被看的位置 →",
             size: int = 20) -> VGroup:
        """Axis captions; every matrix on screen needs them (docs/04 section 4)."""
        top = T(col_label, size, MUTED).next_to(self, UP, buff=0.15).align_to(self, LEFT)
        left = T(row_label, size, MUTED).rotate(1.5708).next_to(self, LEFT, buff=0.15)
        return VGroup(top, left)

    def mask_left_of(self, col: int) -> VGroup:
        """Returns VGroup of visible cells in column < col for turning MUTED."""
        group = VGroup()
        for (r, c), sq in self.grid.items():
            if c < col and (c <= r) and (r - c < self.window):
                group.add(sq)
        return group


class Scale(VGroup):
    """Cost/benefit balance scale with triangle fulcrum, beam, and two pans.

    Pan labels are 22 and the pans grow to fit them; keep each label to one short line (<= 8 characters)."""

    def __init__(self, left: str, right: str, left_color=KV, right_color=WARN,
                 w: float = 6.0, h: float = 2.8, size: int = 22):
        super().__init__()
        l_txt, r_txt = T(left, size, FG), T(right, size, FG)
        pw = max(w * 0.42, l_txt.width + 0.4, r_txt.width + 0.4)
        ph = max(0.75, l_txt.height + 0.3, r_txt.height + 0.3)
        w = max(w, pw + 0.6)
        fulcrum = Polygon([-0.35, -0.9, 0], [0.35, -0.9, 0], [0, -0.1, 0],
                          stroke_color=MUTED, stroke_width=2, fill_color=MUTED, fill_opacity=0.3)
        beam = Line([-w / 2, 0, 0], [w / 2, 0, 0], color=FG, stroke_width=4)

        l_rope = Line([-w / 2, 0, 0], [-w / 2, -0.65, 0], color=MUTED, stroke_width=1.5)
        l_box = RoundedRectangle(corner_radius=0.1, width=pw, height=ph,
                                 stroke_color=left_color, stroke_width=2,
                                 fill_color=left_color, fill_opacity=0.2).move_to([-w / 2, -0.65 - ph / 2, 0])
        l_txt.move_to(l_box)
        left_pan = VGroup(l_rope, l_box, l_txt)

        r_rope = Line([w / 2, 0, 0], [w / 2, -0.65, 0], color=MUTED, stroke_width=1.5)
        r_box = RoundedRectangle(corner_radius=0.1, width=pw, height=ph,
                                 stroke_color=right_color, stroke_width=2,
                                 fill_color=right_color, fill_opacity=0.2).move_to([w / 2, -0.65 - ph / 2, 0])
        r_txt.move_to(r_box)
        right_pan = VGroup(r_rope, r_box, r_txt)

        self.beam = beam
        self.left_pan = left_pan
        self.right_pan = right_pan
        self.fulcrum = fulcrum
        self.add(fulcrum, beam, left_pan, right_pan)


__all__ = [n for n in dir() if not n.startswith("_")]
