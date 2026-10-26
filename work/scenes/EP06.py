"""EP06 scenes: KV 与状态缓存：两种记忆，两种管法 (shots S01-S20).

Layout convention used throughout this episode:
  * header via self.fit_left_of_tags(header(...))
  * hero content lives in y in [-2.2, 1.8]
  * bottom safe line stays at y >= -2.65 (subtitle safe zone below -2.75)
  * text sizes >= 18 pt (small labels >= 16 pt)
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path for manim_lib imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import (
    DOWN, LEFT, RIGHT, UP, UL, UR, DL, DR, ORIGIN,
    FadeIn, FadeOut, Create, Indicate, Transform,
    Line, Arrow, Rectangle, RoundedRectangle, Circle, VGroup, DashedLine,
)
from manim_lib.dvlib import (
    BG, FG, MUTED, GRID, PREFILL, DECODE, KV, SWA, WARN, EXPERT, DRAFT, GPU, CPU,
    T, M, Pill, DVScene, header, MiniMap, Block, TokenRow,
    number_card, LayerStack, Scale,
)


class _E06(DVScene):
    """Small helpers shared by every EP06 shot."""

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
class EP06_S01(_E06):
    SHOT = "EP06-S01"

    def construct(self):
        head = self.fit_left_of_tags(header("两种截然相反的显存记忆", "EP06 · S01 冷开场"))
        self.add(head)

        box_left = RoundedRectangle(width=5.8, height=3.2, corner_radius=0.15, stroke_color=DECODE,
                                    stroke_width=1.5, fill_color=DECODE, fill_opacity=0.08).move_to([-3.2, 0.0, 0])
        t_left_title = T("块状 KV：随长度线性膨胀", 20, DECODE).move_to([-3.2, 1.25, 0])

        # Axes for left panel
        ax_l_x = Line([-5.6, -1.2, 0], [-0.8, -1.2, 0], color=GRID, stroke_width=1.5)
        ax_l_y = Line([-5.6, -1.2, 0], [-5.6, 0.9, 0], color=GRID, stroke_width=1.5)
        lbl_l_x = T("Token 长度 →", 16, MUTED).move_to([-1.6, -1.4, 0])
        lbl_l_y = T("显存占用 (80GB)", 16, WARN).move_to([-4.4, 0.95, 0])
        curve_kv = Line([-5.6, -1.15, 0], [-1.0, 0.7, 0], color=DECODE, stroke_width=3.5)
        dot_kv = Circle(radius=0.08, color=WARN, fill_color=WARN, fill_opacity=1).move_to([-1.0, 0.7, 0])
        tag_kv_cost = T("十万字吃光显存", 16, WARN).move_to([-2.1, 0.45, 0])
        grp_left = VGroup(box_left, t_left_title, ax_l_x, ax_l_y, lbl_l_x, lbl_l_y, curve_kv, dot_kv, tag_kv_cost)

        box_right = RoundedRectangle(width=5.8, height=3.2, corner_radius=0.15, stroke_color=SWA,
                                     stroke_width=1.5, fill_color=SWA, fill_opacity=0.08).move_to([3.2, 0.0, 0])
        t_right_title = T("状态缓存：序列级定长槽位", 20, SWA).move_to([3.2, 1.25, 0])

        # Axes for right panel
        ax_r_x = Line([0.8, -1.2, 0], [5.6, -1.2, 0], color=GRID, stroke_width=1.5)
        ax_r_y = Line([0.8, -1.2, 0], [0.8, 0.9, 0], color=GRID, stroke_width=1.5)
        lbl_r_x = T("Token 长度 →", 16, MUTED).move_to([4.8, -1.4, 0])
        lbl_r_y = T("显存占用 (MB)", 16, SWA).move_to([2.0, 0.95, 0])
        flat_state = Line([0.8, -0.4, 0], [5.6, -0.4, 0], color=SWA, stroke_width=3.5)
        tag_state_fixed = T("首字划定 · 恒定 3.6 MB", 16, SWA).move_to([3.2, -0.15, 0])
        grp_right = VGroup(box_right, t_right_title, ax_r_x, ax_r_y, lbl_r_x, lbl_r_y, flat_state, tag_state_fixed)

        card_split = Block("双轨制管理体系：变长分页块池  vs  序列级定长槽位", color=EXPERT, w=10.5, h=0.65, size=18).move_to([0, -2.15, 0])

        self.play(FadeIn(box_left), FadeIn(t_left_title), FadeIn(ax_l_x), FadeIn(ax_l_y), FadeIn(lbl_l_x), FadeIn(lbl_l_y), run_time=1.0)

        self.until("curve_show")
        self.play(Create(curve_kv), FadeIn(dot_kv), FadeIn(tag_kv_cost), run_time=1.0)

        self.until("state_flat")
        self.play(FadeIn(grp_right), run_time=1.0)
        self.play(Indicate(flat_state, color=SWA), run_time=0.8)

        self.until("split_mind")
        self.play(FadeIn(card_split), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S02
class EP06_S02(_E06):
    SHOT = "EP06-S02"

    def construct(self):
        title = T("EP06 · 显存架构", 44, DECODE).move_to([0, 0.6, 0])
        sub = T("两种记忆 · 两种管法", 30, FG).move_to([0, -0.2, 0])
        mmap = MiniMap(active="KV 存储", scale=1.05).move_to([0, -1.3, 0])

        self.play(FadeIn(title), FadeIn(sub), run_time=0.8)

        self.until("card")
        self.play(FadeIn(mmap), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S03
class EP06_S03(_E06):
    SHOT = "EP06-S03"

    def construct(self):
        head = self.fit_left_of_tags(header("架构两分：两套独立缓存", "EP06 · S03 核心矛盾"))
        self.add(head)

        stack = LayerStack(40, split=20, w=1.0, h=3.2).move_to([-4.8, 0.15, 0])

        # Highlight layers 2, 8, 14, 20 (0-indexed: 1, 7, 13, 19)
        global_layers = [1, 7, 13, 19]
        hl_boxes = VGroup()
        for idx in global_layers:
            bar = stack.layer(idx)
            hl = RoundedRectangle(corner_radius=0.03, width=1.1, height=bar.height + 0.04,
                                  stroke_color=KV, stroke_width=2.5, fill_color=KV, fill_opacity=0.6).move_to(bar)
            hl_boxes.add(hl)

        tag_stack = T("V4.1 模型全部 40 层", 16, MUTED).next_to(stack, UP, buff=0.1)

        b_global = Block("4 层 全局注意力 (Global Attention)\n第 2、8、14、20 层：必须跨全序列保留块状 KV",
                         color=KV, w=7.2, h=1.0, size=18).move_to([1.5, 0.9, 0])
        b_swa = Block("36 层 局部滑窗注意力 (SWA)\n其余全部层：只保留最近 128 局部窗口，历史状态即刻丢弃",
                      color=SWA, w=7.2, h=1.0, size=18).move_to([1.5, -0.35, 0])
        b_mgmt = Block("生命周期分化带来双轨机制：BlockManager (分页块池)  vs  StateManager (定长槽位)",
                       color=EXPERT, w=11.2, h=0.65, size=18).move_to([0, -2.15, 0])

        arr1 = Arrow(stack.get_right() + UP * 0.6, b_global.get_left(), color=KV, stroke_width=2, buff=0.15)
        arr2 = Arrow(stack.get_right() + DOWN * 0.3, b_swa.get_left(), color=SWA, stroke_width=2, buff=0.15)

        self.play(FadeIn(stack), FadeIn(tag_stack), run_time=1.0)

        self.until("arch_split")
        self.play(FadeIn(hl_boxes), FadeIn(arr1), FadeIn(b_global), run_time=1.0)

        self.until("lifecycle_diff")
        self.play(FadeIn(arr2), FadeIn(b_swa), run_time=1.0)

        self.until("two_managers")
        self.play(FadeIn(b_mgmt), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S04
class EP06_S04(_E06):
    SHOT = "EP06-S04"

    def construct(self):
        head = self.fit_left_of_tags(header("变长分页块：按需索取的内存积木", "EP06 · S04 分页机制"))
        self.add(head)

        # Logic sequence row
        t_seq = T("逻辑请求序列 (自回归持续增长)", 18, FG).move_to([-2.6, 1.45, 0])
        row_b1 = Block("逻辑块 0 (128 tok)", color=DECODE, w=2.4, h=0.6, size=16).move_to([-4.2, 0.9, 0])
        row_b2 = Block("逻辑块 1 (128 tok)", color=DECODE, w=2.4, h=0.6, size=16).move_to([-1.6, 0.9, 0])
        row_b3 = Block("逻辑块 2 (128 tok)", color=WARN, w=2.4, h=0.6, size=16).move_to([1.0, 0.9, 0])

        # Physical pool
        t_pool = T("GPU 物理显存块池 (Block Pool)", 18, FG).move_to([-2.6, -0.05, 0])
        p_b0 = Block("Block 0 (保留/禁用)", color=MUTED, w=2.2, h=0.6, size=16).move_to([-4.5, -0.6, 0])
        slash_0 = Line(p_b0.get_corner(DL), p_b0.get_corner(UR), color=WARN, stroke_width=2.5)
        p_b1 = Block("Block 1 (物理块)", color=DECODE, w=2.0, h=0.6, size=16).move_to([-2.2, -0.6, 0])
        p_b2 = Block("Block 2 (物理块)", color=DECODE, w=2.0, h=0.6, size=16).move_to([0.0, -0.6, 0])
        p_b3 = Block("Block 3 (空闲块)", color=GPU, w=2.0, h=0.6, size=16).move_to([2.2, -0.6, 0])
        p_bn = Block("Block N ...", color=GRID, w=1.8, h=0.6, size=16).move_to([4.3, -0.6, 0])

        grp_pool = VGroup(t_pool, p_b0, slash_0, p_b1, p_b2, p_b3, p_bn)

        # Bottom card
        b_bottom = Block("按需弹出物理块挂入块表 · 零外部碎片 · C++ 纳秒级链表管理",
                         color=EXPERT, w=10.5, h=0.65, size=18).move_to([0, -2.15, 0])

        self.play(FadeIn(t_seq), FadeIn(row_b1), FadeIn(row_b2), FadeIn(grp_pool), run_time=1.0)

        self.until("paged_concept")
        self.play(Indicate(row_b1, color=DECODE), Indicate(row_b2, color=DECODE), run_time=0.8)

        self.until("alloc_new_block")
        arr_alloc = Arrow(p_b3.get_top(), row_b3.get_bottom(), color=GPU, stroke_width=2.5, buff=0.1)
        self.play(FadeIn(arr_alloc), FadeIn(row_b3), run_time=1.0)
        self.play(Indicate(p_b3, color=GPU), run_time=0.8)

        self.until("zero_frag")
        self.play(FadeIn(b_bottom), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S05
class EP06_S05(_E06):
    SHOT = "EP06-S05"

    def construct(self):
        pill = Pill("Q · 深入物理底层", DECODE, size=20).move_to([0, 1.3, 0])
        q1 = T("一个物理块在显存里到底长什么样？", 32, FG).move_to([0, 0.5, 0])
        q2 = T("它是独立张量集合，还是一整块连续单字节切片？", 22, MUTED).move_to([0, -0.2, 0])

        card_preview = Block("底层揭秘：扁平 uint8 连续字节带 · 严格 32 字节硬件硬件对齐",
                             color=GRID, w=9.2, h=0.9, size=18).move_to([0, -1.3, 0])

        self.play(FadeIn(pill), FadeIn(q1), FadeIn(q2), run_time=1.0)

        self.until("q_block_layout")
        self.play(FadeIn(card_preview), Indicate(card_preview, color=DECODE), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S06
class EP06_S06(_E06):
    SHOT = "EP06-S06"

    def construct(self):
        head = self.fit_left_of_tags(header("量化字节账本：物理尺寸推演", "EP06 · S06 尺寸精算"))
        self.add(head)

        b_fp4 = Block("主 KV (FP4 稀疏模式)：512 元素 ÷ 2 = 256 字节 + 32 字节尺度 = 288 字节 / token",
                      color=DECODE, w=11.2, h=0.85, size=18).move_to([0, 0.9, 0])

        b_mxfp8 = Block("主 KV (MXFP8 密集模式)：512 元素 × 1 = 512 字节 + 16 字节尺度 = 528 字节 / token",
                        color=KV, w=11.2, h=0.85, size=18).move_to([0, -0.05, 0])

        b_aux = Block("索引 K (FP4): 128 元素 ÷ 2 + 4 尺度 = 68 字节  |  SWA 局部状态: 固定 528 字节 (MXFP8)",
                      color=SWA, w=11.2, h=0.85, size=18).move_to([0, -1.0, 0])

        foot = self.foot("数据来源：DeepInfer 源码与量化规范 (F06-04)", y=-2.15)

        self.play(FadeIn(b_fp4), run_time=1.0)

        self.until("byte_calc")
        self.play(Indicate(b_fp4, color=DECODE), run_time=0.8)

        self.until("mxfp8_calc")
        self.play(FadeIn(b_mxfp8), FadeIn(b_aux), FadeIn(foot), run_time=1.0)
        self.play(Indicate(b_mxfp8, color=KV), Indicate(b_aux, color=SWA), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S07
class EP06_S07(_E06):
    SHOT = "EP06-S07"

    def construct(self):
        head = self.fit_left_of_tags(header("扁平连续字节带：消除碎片的一维切片", "EP06 · S07 物理排布"))
        self.add(head)

        b_tape = Block("物理块内存形态：扁平一维 uint8 字节切片 (零张量元数据开销)",
                       color=DECODE, w=11.2, h=0.75, size=18).move_to([0, 0.95, 0])

        # Tape representation
        tape_box = RoundedRectangle(width=11.0, height=0.9, corner_radius=0.08, stroke_color=GRID,
                                    fill_color="#161B22", fill_opacity=0.8).move_to([0, 0.05, 0])
        seg1 = Block("L0 索引K (68B→96B)", color=SWA, w=2.4, h=0.65, size=16).move_to([-4.1, 0.05, 0])
        seg2 = Block("L0 主KV (288B)", color=DECODE, w=2.5, h=0.65, size=16).move_to([-1.5, 0.05, 0])
        seg3 = Block("L1 索引K (96B)", color=SWA, w=2.3, h=0.65, size=16).move_to([1.0, 0.05, 0])
        seg4 = Block("L1 主KV (288B) ...", color=DECODE, w=2.6, h=0.65, size=16).move_to([3.6, 0.05, 0])
        grp_tape = VGroup(tape_box, seg1, seg2, seg3, seg4)

        b_align = Block("硬件对齐规则：层内局部段落严格 32 字节对齐 · 算子全局访存吞吐最大化",
                        color=KV, w=11.2, h=0.7, size=18).move_to([0, -0.9, 0])
        b_lcm = Block("整块跨度对齐：lcm(128, 288) = 1152 字节 · 压缩 C2 层每块容纳 64 token",
                      color=EXPERT, w=11.2, h=0.7, size=18).move_to([0, -1.8, 0])

        self.play(FadeIn(b_tape), FadeIn(grp_tape), run_time=1.0)

        self.until("flat_byte_tape")
        self.play(FadeIn(b_align), Indicate(tape_box, color=DECODE), run_time=0.8)

        self.until("block_lcm")
        self.play(FadeIn(b_lcm), Indicate(b_lcm, color=EXPERT), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S08
class EP06_S08(_E06):
    SHOT = "EP06-S08"

    def construct(self):
        head = self.fit_left_of_tags(header("槽位寻址：全局一维 slot 映射", "EP06 · S08 算子寻址"))
        self.add(head)

        b_formula = Block("slot = block_id * tokens_per_block + offset",
                          color=DECODE, w=10.0, h=1.0, size=22,
                          sub="TileLang 内核：槽位编号为 -1 时，跳过写入（无效填充处理）").move_to([0, 0.75, 0])

        b_pref = Block("预填充 (Prefill) 阶段\n批量映射并行写入上千 token 槽位",
                       color=PREFILL, w=5.2, h=1.1, size=18).move_to([-2.8, -0.5, 0])
        b_deco = Block("解码 (Decode) 阶段\n每步追加单 token，复用一维槽位坐标",
                       color=GPU, w=5.2, h=1.1, size=18).move_to([2.8, -0.5, 0])

        b_unified = Block("统一寻址路径：两阶段复用同一极简内核，消除 GPU 地址转换开销",
                          color=EXPERT, w=10.8, h=0.65, size=18).move_to([0, -1.9, 0])

        self.play(FadeIn(b_formula), run_time=1.0)

        self.until("slot_formula")
        self.play(Indicate(b_formula, color=DECODE), run_time=0.8)

        self.until("unified_path")
        self.play(FadeIn(b_pref), FadeIn(b_deco), FadeIn(b_unified), run_time=1.0)
        self.play(Indicate(b_unified, color=EXPERT), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S09
class EP06_S09(_E06):
    SHOT = "EP06-S09"

    def construct(self):
        pill = Pill("Q · 状态缓存解剖", SWA, size=20).move_to([0, 1.3, 0])
        q1 = T("定长状态缓存内部又是如何排布的？", 32, FG).move_to([0, 0.5, 0])
        q2 = T("为什么它的大小完全不受上下文长度的影响？", 22, MUTED).move_to([0, -0.2, 0])

        card_preview = Block("结构内幕：前存后丢哲学 · 低地址持久化 · 高地址即刻截断",
                             color=GRID, w=9.2, h=0.9, size=18).move_to([0, -1.3, 0])

        self.play(FadeIn(pill), FadeIn(q1), FadeIn(q2), run_time=1.0)

        self.until("q_state_layout")
        self.play(FadeIn(card_preview), Indicate(card_preview, color=SWA), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S10
class EP06_S10(_E06):
    SHOT = "EP06-S10"

    def construct(self):
        head = self.fit_left_of_tags(header("解剖 StateBlock：前存后丢的分区哲学", "EP06 · S10 槽位分区"))
        self.add(head)

        t_slot = T("单个序列专享的 StateBlock 物理槽", 18, FG).move_to([-3.0, 1.25, 0])

        # StateBlock layout
        box_slot = RoundedRectangle(width=11.2, height=1.5, corner_radius=0.1, stroke_color=GRID,
                                    fill_color="#161B22", fill_opacity=0.9).move_to([0, 0.35, 0])

        b_stored = Block("低地址存储区 (Stored Region)\n前 20 层 SWA 环 · 需落盘持久化",
                         color=KV, w=5.2, h=1.2, size=18).move_to([-2.7, 0.35, 0])
        b_dropped = Block("高地址丢弃区 (Dropped Region)\n后 20 层 consumer SWA + 压缩边界",
                          color=WARN, w=5.2, h=1.2, size=18).move_to([2.7, 0.35, 0])
        split_line = DashedLine([0, 1.1, 0], [0, -0.4, 0], color=FG, stroke_width=2.5)

        grp_slot = VGroup(t_slot, box_slot, b_stored, b_dropped, split_line)

        b_truncate = Block("前缀截断 (Prefix Truncate)：落盘时直接切取低地址切片，零拷贝剔除丢弃区",
                           color=EXPERT, w=11.2, h=0.8, size=18).move_to([0, -1.35, 0])
        foot = self.foot("落盘数据量：20层 × 134 token × 528字节 = 1.35 MiB", y=-2.15)

        self.play(FadeIn(grp_slot), run_time=1.0)

        self.until("state_anatomy")
        self.play(Indicate(box_slot, color=DECODE), run_time=0.8)

        self.until("store_drop_split")
        self.play(Indicate(b_stored, color=KV), Indicate(b_dropped, color=WARN), run_time=0.8)

        self.until("prefix_truncate")
        self.play(FadeIn(b_truncate), FadeIn(foot), run_time=1.0)
        self.play(Indicate(b_truncate, color=EXPERT), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S11
class EP06_S11(_E06):
    SHOT = "EP06-S11"

    def construct(self):
        head = self.fit_left_of_tags(header("134 环形窗口：128 滑窗与 6 步回退预算", "EP06 · S11 环形缓冲区"))
        self.add(head)

        b_ring_title = Block("SWA 滚动环容量 = 134 token\n128 (注意力局部滑窗) + 6 (最大回退预算 5+1)",
                             color=SWA, w=11.2, h=0.9, size=18).move_to([0, 0.9, 0])

        b_spec = Block("容忍投机解码回退\n推演验证拒绝时，写入指针顺畅向后倒退 5 步，无缝接续",
                       color=DRAFT, w=5.4, h=1.2, size=18).move_to([-2.9, -0.35, 0])
        b_lag = Block("吸收异步落盘滞后\n存储落盘边界存在微小延迟，多余 6 步确保存储窗口不被覆写",
                      color=DECODE, w=5.4, h=1.2, size=18).move_to([2.9, -0.35, 0])

        b_summary = Block("严密双重冗余设计：保障滑动窗口在复杂推演与异步落盘中稳固有效",
                          color=EXPERT, w=11.2, h=0.65, size=18).move_to([0, -1.85, 0])

        self.play(FadeIn(b_ring_title), run_time=1.0)

        self.until("ring_134")
        self.play(Indicate(b_ring_title, color=SWA), run_time=0.8)

        self.until("why_134")
        self.play(FadeIn(b_spec), Indicate(b_spec, color=DRAFT), run_time=0.8)

        self.until("backtrack_role")
        self.play(FadeIn(b_lag), FadeIn(b_summary), run_time=1.0)
        self.play(Indicate(b_lag, color=DECODE), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S12
class EP06_S12(_E06):
    SHOT = "EP06-S12"

    def construct(self):
        head = self.fit_left_of_tags(header("存储视角 262 环与零重排直接拷贝", "EP06 · S12 存储模式"))
        self.add(head)

        b_262 = Block("开启额外状态 (EXTRA_STATE)：262 环 (134 + 128 余量)\n跨越落盘边界防丢，需专用 gather 算子内核重排为 134",
                      color=WARN, w=11.2, h=1.0, size=18).move_to([0, 0.7, 0])

        b_134 = Block("默认开源配置 (默认模式)：134 环直接单次内存拷贝 (memcpy)\n两环合一，零额外重排算子计算，连续显存切片直发出库",
                      color=DECODE, w=11.2, h=1.0, size=18).move_to([0, -0.45, 0])

        b_footer = Block("极简性能取舍：默认零重排整段拷贝，将计算开销压缩到极致",
                         color=EXPERT, w=11.2, h=0.65, size=18).move_to([0, -1.85, 0])

        self.play(FadeIn(b_262), run_time=1.0)

        self.until("kvstore_262")
        self.play(Indicate(b_262, color=WARN), run_time=0.8)

        self.until("default_zero_copy")
        self.play(FadeIn(b_134), FadeIn(b_footer), run_time=1.0)
        self.play(Indicate(b_134, color=DECODE), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S13
class EP06_S13(_E06):
    SHOT = "EP06-S13"

    def construct(self):
        head = self.fit_left_of_tags(header("落盘数据量：死死锁在 1.35 MiB", "EP06 · S13 落盘精算"))
        self.add(head)

        b_calc = Block("落盘状态体积计算式：\n20 层 × 134 token × 528 字节 = 1,415,040 字节",
                       color=DECODE, w=6.8, h=1.2, size=20).move_to([-2.6, 0.35, 0])

        card_num = number_card("1.35", "MiB", "单序列固定落盘量", color=KV).move_to([3.4, 0.35, 0])

        b_fixed = Block("常数级定长约束：无论对话是一千字还是十万字，落盘状态恒定 1.35 MiB\n仅在 token 计数为 128 整数倍的边界处触发持久化",
                        color=EXPERT, w=11.2, h=0.85, size=18).move_to([0, -1.5, 0])

        self.play(FadeIn(b_calc), run_time=1.0)

        self.until("disk_size_calc")
        self.play(FadeIn(card_num), Indicate(card_num, color=KV), run_time=0.8)

        self.until("fixed_1_35mb")
        self.play(FadeIn(b_fixed), Indicate(b_fixed, color=EXPERT), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S14
class EP06_S14(_E06):
    SHOT = "EP06-S14"

    def construct(self):
        pill = Pill("Q · 概念辨析", EXPERT, size=20).move_to([0, 1.3, 0])
        q1 = T("代码里到处都是 128，难道都是巧合？", 32, FG).move_to([0, 0.5, 0])
        q2 = T("块大小、步长与硬件对齐是同一回事吗？", 22, MUTED).move_to([0, -0.2, 0])

        card_preview = Block("代码迷雾：三个独立的“128”彼此交织，必须彻底解耦剖析",
                             color=GRID, w=9.2, h=0.9, size=18).move_to([0, -1.3, 0])

        self.play(FadeIn(pill), FadeIn(q1), FadeIn(q2), run_time=1.0)

        self.until("q_three_128")
        self.play(FadeIn(card_preview), Indicate(card_preview, color=EXPERT), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S15
class EP06_S15(_E06):
    SHOT = "EP06-S15"

    def construct(self):
        head = self.fit_left_of_tags(header("彻底拆解三个相互独立的“128”", "EP06 · S15 认知突破"))
        self.add(head)

        c1 = Block("① 逻辑容器\nblock_size = 128\n每个物理块容纳 128 个\n压缩前 token 数据",
                   color=DECODE, w=3.6, h=2.1, size=18).move_to([-4.0, 0.05, 0])
        c2 = Block("② 调度步长\nKVSTORE_GRAIN = 128\n状态数据仅在 128 整数倍\n时钟边界执行落盘",
                   color=KV, w=3.6, h=2.1, size=18).move_to([0.0, 0.05, 0])
        c3 = Block("③ 硬件物理\n128 字节硬件对齐\n底层算子访存跨度\n必须满足 128B 对齐",
                   color=SWA, w=3.6, h=2.1, size=18).move_to([4.0, 0.05, 0])

        b_rule = Block("核心法则：容器容量 · 调度步长 · 硬件对齐 —— 三个概念完全独立，切勿混淆！",
                       color=WARN, w=11.2, h=0.65, size=18).move_to([0, -1.85, 0])

        self.play(FadeIn(c1), FadeIn(c2), FadeIn(c3), run_time=1.0)

        self.until("aha_three_128")
        self.play(FadeIn(b_rule), run_time=0.8)

        self.until("card_container")
        self.play(Indicate(c1, color=DECODE), run_time=0.8)

        self.until("card_grain")
        self.play(Indicate(c2, color=KV), run_time=0.8)

        self.until("card_align")
        self.play(Indicate(c3, color=SWA), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S16
class EP06_S16(_E06):
    SHOT = "EP06-S16"

    def construct(self):
        head = self.fit_left_of_tags(header("显存容量规划：扣除两倍状态算物理块数", "EP06 · S16 启动规划"))
        self.add(head)

        b_step1 = Block("步骤一：90% 水位与峰值扣除\n可用显存 = GPU 总显存 × 90% - 实测峰值显存 (模型权重 + 运行时临时区)",
                        color=DECODE, w=11.2, h=0.85, size=18).move_to([0, 0.9, 0])

        b_step2 = Block("步骤二：显式扣除 2 × StateBuffer (双倍预留)\n为主槽位与解码副本各预留一份完整状态缓冲，严格防止解码阶段 OOM",
                        color=SWA, w=11.2, h=0.85, size=18).move_to([0, -0.05, 0])

        b_step3 = Block("步骤三：计算物理块数 = 剩余显存 // 单块字节数\n准入硬约束：单请求最大长度 ≤ 总块数容量的 80%，超限直接拒绝启动",
                        color=EXPERT, w=11.2, h=0.85, size=18).move_to([0, -1.0, 0])

        foot = self.foot("依据：engine_config 与 BlockManager 准入校验 (F06-13, F06-15)", y=-2.15)

        self.play(FadeIn(b_step1), run_time=1.0)

        self.until("mem_plan_flow")
        self.play(Indicate(b_step1, color=DECODE), run_time=0.8)

        self.until("deduct_2x_state")
        self.play(FadeIn(b_step2), Indicate(b_step2, color=SWA), run_time=0.8)

        self.until("launch_check_80")
        self.play(FadeIn(b_step3), FadeIn(foot), run_time=1.0)
        self.play(Indicate(b_step3, color=EXPERT), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S17
class EP06_S17(_E06):
    SHOT = "EP06-S17"

    def construct(self):
        head = self.fit_left_of_tags(header("前缀缓存真相：开源版其实“完全没有”", "EP06 · S17 源码底牌"))
        self.add(head)

        b_real = Block("C++ BlockManager 真实数据结构\n• _free_blocks: std::list<int> (FIFO 空闲链表)\n• ref_count: std::vector<int> (引用计数数组)\n仅提供 O(1) 槽位分配与回收，无内容感知能力",
                       color=DECODE, w=6.4, h=2.2, size=18).move_to([-3.0, 0.0, 0])

        b_miss = Block("开源代码中完全缺失：\n✗ 前缀树 (Radix Tree)\n✗ 块哈希表 (Block Hash Table)\n✗ LRU 淘汰与复用索引\n物理块释放直接塞回尾部，新请求立即覆盖！",
                       color=WARN, w=5.4, h=2.2, size=18).move_to([3.3, 0.0, 0])

        b_bot = Block("真实底牌：开源版零自动前缀复用 · 释放即归还队列 · 绝无常驻内容缓存",
                      color=EXPERT, w=11.2, h=0.65, size=18).move_to([0, -1.85, 0])

        self.play(FadeIn(b_real), run_time=1.0)

        self.until("prefix_truth")
        self.play(FadeIn(b_miss), Indicate(b_miss, color=WARN), run_time=0.8)

        self.until("fifo_only")
        self.play(Indicate(b_real, color=DECODE), run_time=0.8)

        self.until("overwrite_risk")
        self.play(FadeIn(b_bot), Indicate(b_bot, color=EXPERT), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S18
class EP06_S18(_E06):
    SHOT = "EP06-S18"

    def construct(self):
        head = self.fit_left_of_tags(header("显式 fork_seq：显存内唯一的前缀共享", "EP06 · S18 显存原语"))
        self.add(head)

        # Parent sequence blocks
        t_p = T("父序列 (Seq 0) 块表:", 18, FG).move_to([-3.4, 1.25, 0])
        pb1 = Block("Block 1", color=DECODE, w=1.8, h=0.6, size=16).move_to([-1.0, 1.25, 0])
        pb2 = Block("Block 2", color=DECODE, w=1.8, h=0.6, size=16).move_to([1.0, 1.25, 0])
        pb3 = Block("Block 3 (未满)", color=WARN, w=2.0, h=0.6, size=16).move_to([3.2, 1.25, 0])
        grp_parent = VGroup(t_p, pb1, pb2, pb3)

        # Child sequence blocks
        t_c = T("Fork 子序列 (Seq 1):", 18, FG).move_to([-3.4, 0.15, 0])
        cb1 = Block("Block 1 (共享)", color=DECODE, w=1.8, h=0.6, size=16).move_to([-1.0, 0.15, 0])
        cb2 = Block("Block 2 (共享)", color=DECODE, w=1.8, h=0.6, size=16).move_to([1.0, 0.15, 0])
        cb3 = Block("Block 4 (COW克隆)", color=GPU, w=2.0, h=0.6, size=16).move_to([3.2, 0.15, 0])
        grp_child = VGroup(t_c, cb1, cb2, cb3)

        b_pin = Block("显式共享原语：通过 pin 操作将块表引用计数加 1 (ref_count 1 → 2)",
                      color=KV, w=11.2, h=0.65, size=18).move_to([0, -0.8, 0])
        b_cow = Block("写时复制 (COW)：子序列首步 Decode 时，仅克隆末尾未满块 (Block 3 → 4)，共享整段历史",
                      color=EXPERT, w=11.2, h=0.65, size=18).move_to([0, -1.75, 0])

        self.play(FadeIn(grp_parent), run_time=1.0)

        self.until("fork_seq_anim")
        self.play(FadeIn(grp_child), FadeIn(b_pin), run_time=1.0)
        self.play(Indicate(b_pin, color=KV), run_time=0.8)

        self.until("cow_action")
        self.play(FadeIn(b_cow), Indicate(cb3, color=GPU), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S19
class EP06_S19(_E06):
    SHOT = "EP06-S19"

    def construct(self):
        head = self.fit_left_of_tags(header("工业生产立面：三层存储架构", "EP06 · S19 生产视角"))
        self.add(head)

        b_l1 = Block("L1 显存层 (GPU HBM)：在飞动态计算与序列活跃状态", color=GPU, w=11.2, h=0.65, size=18).move_to([0, 0.95, 0])
        b_l2 = Block("L2 主机层 (Host RAM)：本地 1.4MB SWA 状态单副本", color=CPU, w=11.2, h=0.65, size=18).move_to([0, 0.2, 0])
        b_l3 = Block("L3 存储层 (3FS 分布式集群)：跨机共享 100+ PB 持久化 KV 块池", color=DECODE, w=11.2, h=0.65, size=18).move_to([0, -0.55, 0])

        b_comp = Block("横向对比：vLLM (引擎内块哈希) vs SGLang (引擎内基数树) vs DeepInfer (网关前置匹配+外部注入)",
                       color=EXPERT, w=11.2, h=0.75, size=18).move_to([0, -1.75, 0])

        self.play(FadeIn(b_l1), FadeIn(b_l2), FadeIn(b_l3), run_time=1.0)

        self.until("three_tier_storage")
        self.play(Indicate(b_l1, color=GPU), Indicate(b_l2, color=CPU), Indicate(b_l3, color=DECODE), run_time=0.8)

        self.until("route_compare")
        self.play(FadeIn(b_comp), Indicate(b_comp, color=EXPERT), run_time=0.8)

        self.finish()


# ---------------------------------------------------------------- S20
class EP06_S20(_E06):
    SHOT = "EP06-S20"

    def construct(self):
        head = self.fit_left_of_tags(header("全集总结与下集预告", "EP06 · S20 认知归宿"))
        self.add(head)

        b_r1 = Block("① 显存双轨制：变长分页块管长程 KV，定长状态槽管局部滑窗",
                     color=DECODE, w=11.2, h=0.7, size=18).move_to([0, 0.95, 0])
        b_r2 = Block("② 三个 128：逻辑容器容量、落盘调度步长、底层硬件对齐彼此独立",
                     color=KV, w=11.2, h=0.7, size=18).move_to([0, 0.1, 0])
        b_r3 = Block("③ 开源极简与生产三层：开源版零自动前缀树，匹配逻辑完全前置网关",
                     color=EXPERT, w=11.2, h=0.7, size=18).move_to([0, -0.75, 0])

        b_next = Block("下集预告：EP07 · SWA 有界重放 —— 为什么后 20 层只需重放 140 步？",
                       color=PREFILL, w=11.2, h=0.7, size=18).move_to([0, -1.8, 0])

        self.play(FadeIn(b_r1), FadeIn(b_r2), FadeIn(b_r3), run_time=1.0)

        self.until("recap_cards")
        self.play(Indicate(b_r1, color=DECODE), Indicate(b_r2, color=KV), Indicate(b_r3, color=EXPERT), run_time=0.8)

        self.until("next_hook")
        self.play(FadeIn(b_next), Indicate(b_next, color=PREFILL), run_time=0.8)

        self.finish()
