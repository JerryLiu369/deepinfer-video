"""EP00 scenes: 一个引擎、一个模型、三个源头 (shots S01-S13)."""
from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path for manim_lib imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import (
    DOWN, LEFT, RIGHT, UP, UL, UR, DL, DR, ORIGIN,
    FadeIn, FadeOut, Create, Write, Transform, Indicate,
    Line, Arrow, Rectangle, RoundedRectangle, VGroup, Circle,
)
from manim_lib.dvlib import (
    BG, FG, MUTED, GRID, PREFILL, DECODE, KV, SWA, WARN, EXPERT, DRAFT, GPU, CPU,
    GRADE_COLORS, Pill, DVScene, header, MiniMap, Block, TokenRow, window_bracket,
    code_panel, number_card, LayerStack, AttentionMatrix, Scale, T, M,
)


class EP00_S01(DVScene):
    SHOT = "EP00-S01"

    def construct(self):
        head = self.fit_left_of_tags(header("一句话背后的推理引擎", "EP00 · S01 冷开场"))
        self.add(head)

        # Card container: width 8.4, height 2.6, centered at [0, -0.15, 0]
        card_bg = RoundedRectangle(corner_radius=0.15, width=8.6, height=2.6,
                                   stroke_color=GRID, stroke_width=2, fill_color="#161B22", fill_opacity=0.96)
        card_bg.move_to([0, -0.15, 0])

        tag = Pill("官方发布公告 · 2026-10-20", DECODE, size=18).next_to(card_bg.get_top(), DOWN, buff=0.25)
        raw_text = T("We're sharing our production stack to help the community\nlower compute costs, reduce energy use, and make AI more affordable.",
                     size=18, color=FG).next_to(tag, DOWN, buff=0.22)
        card = VGroup(card_bg, tag, raw_text)

        self.play(FadeIn(card), run_time=1.0)

        self.until("tweet")
        self.play(card_bg.animate.set_stroke(DECODE, 2.5), run_time=0.6)

        self.until("quote")
        box = RoundedRectangle(corner_radius=0.1, width=7.6, height=0.7,
                               stroke_color=KV, stroke_width=2, fill_color=KV, fill_opacity=0.2)
        box.move_to([0, -0.45, 0])
        quote_zh = T("降低计算成本 · 减少能耗 · 使 AI 更可负担", 20, FG).move_to(box)
        hl = VGroup(box, quote_zh)
        self.play(FadeIn(hl), run_time=0.8)

        self.until("question")
        q_box = RoundedRectangle(corner_radius=0.1, width=8.6, height=0.8,
                                 stroke_color=EXPERT, stroke_width=2, fill_color="#1F1A12", fill_opacity=0.95)
        q_box.move_to([0, -1.9, 0])
        q_txt = T("为何专一离线引擎，值得花 3 小时从头拆解？", 20, EXPERT).move_to(q_box)
        q_group = VGroup(q_box, q_txt)
        self.play(FadeIn(q_group), run_time=0.8)

        self.finish()


class EP00_S02(DVScene):
    SHOT = "EP00-S02"

    def construct(self):
        ep_tag = T("EP00 · 导览", 48, DECODE).move_to([0, 1.2, 0])
        title = T("一个引擎 · 一个模型 · 三个源头", 34, FG).next_to(ep_tag, DOWN, buff=0.35)
        mmap = MiniMap(active=None, scale=1.05).next_to(title, DOWN, buff=0.8)

        self.play(FadeIn(ep_tag), FadeIn(title), run_time=0.8)

        self.until("title")
        self.play(FadeIn(mmap), run_time=0.8)

        self.finish()


class EP00_S03(DVScene):
    SHOT = "EP00-S03"

    def construct(self):
        head = self.fit_left_of_tags(header("为什么只支持一个模型？", "EP00 · S03 核心疑问"))
        self.add(head)

        # Left: General engine abstract layers
        l_title = T("通用引擎：兼容海量模型", 22, MUTED).move_to([-3.4, 1.1, 0])
        b1 = Block("通用框架接口层", color=MUTED, w=3.6, h=0.65, size=18)
        b2 = Block("动态多模型调度器", color=MUTED, w=3.6, h=0.65, size=18)
        b3 = Block("设备兼容分发算子", color=MUTED, w=3.6, h=0.65, size=18)
        left_stack = VGroup(b1, b2, b3).arrange(DOWN, buff=0.12).next_to(l_title, DOWN, buff=0.25)
        left_group = VGroup(l_title, left_stack)

        # Right: DeepInfer + V4.1-Flash tight coupling
        r_title = T("DeepInfer：仅服务 V4.1-Flash", 22, KV).move_to([3.4, 1.1, 0])
        rb1 = Block("DeepInfer 专用引擎", color=KV, w=3.8, h=1.0, size=20, sub="离线流水线 / 零开销异步调度")
        rb2 = Block("DeepSeek-V4.1-Flash", color=EXPERT, w=3.8, h=1.0, size=20, sub="40层SWA / YOCO共享KV")
        right_stack = VGroup(rb1, rb2).arrange(DOWN, buff=0.15).next_to(r_title, DOWN, buff=0.25)
        right_group = VGroup(r_title, right_stack)

        self.play(FadeIn(left_group), FadeIn(right_group), run_time=1.0)

        self.until("tradeoff")
        warn_pill = Pill("层层通用抽象开销", WARN, size=16).next_to(left_stack, DOWN, buff=0.25)
        self.play(FadeIn(warn_pill), run_time=0.6)

        self.until("depth")
        fit_pill = Pill("放弃通用，换取深度协同", KV, size=16).next_to(right_stack, DOWN, buff=0.25)
        self.play(FadeIn(fit_pill), Indicate(right_stack, color=EXPERT, scale_factor=1.04), run_time=0.8)

        self.finish()


class EP00_S04(DVScene):
    SHOT = "EP00-S04"

    def construct(self):
        head = self.fit_left_of_tags(header("离线推理与缺失的三大件", "EP00 · S04 开源边界"))
        self.add(head)

        # Left: Open source offline engine
        oss_box = Block("DeepInfer 离线推理", color=KV, w=4.5, h=2.5, size=22,
                        sub="单机 / 超节点批处理\n已包含核心引擎与优化内核", fill=0.15)
        oss_box.move_to([-3.4, -0.4, 0])
        oss_tag = Pill("开源代码里有", KV, size=18).next_to(oss_box, UP, buff=0.15)
        oss_group = VGroup(oss_box, oss_tag)

        # Right: Unreleased online components (amber)
        un_tag = Pill("仅文档描述 · 未开源", "#D29922", size=18).move_to([3.4, 1.0, 0])
        mb1 = Block("3FS 独立 KV 存储系统", color="#D29922", w=4.4, h=0.9, size=18, sub="跨机器 72h+ 状态持久化")
        mb2 = Block("E/P/D 分阶段部署机制", color="#D29922", w=4.4, h=0.9, size=18, sub="Prefill / Decode 物理集群解耦")
        mb3 = Block("副本间全局负载均衡器", color="#D29922", w=4.4, h=0.9, size=18, sub="PLB / DLB / VELB / EPLB")
        un_stack = VGroup(mb1, mb2, mb3).arrange(DOWN, buff=0.12).next_to(un_tag, DOWN, buff=0.15)
        un_group = VGroup(un_tag, un_stack)

        self.play(FadeIn(oss_group), run_time=0.8)

        self.until("offline")
        self.play(Indicate(oss_box, color=KV, scale_factor=1.03), run_time=0.6)

        self.until("missing")
        self.play(FadeIn(un_group), run_time=1.0)

        self.finish()


class EP00_S05(DVScene):
    SHOT = "EP00-S05"

    def construct(self):
        head = self.fit_left_of_tags(header("每天 155 万亿 Token 的生产底气", "EP00 · S05 生产背景"))
        self.add(head)

        # Left card: daily tokens
        c1 = number_card("155", "万亿 Token/天", "单一集群生产日吞吐（官方披露）", color=DECODE).move_to([-3.4, 0.2, 0])
        self.play(FadeIn(c1), run_time=0.8)

        self.until("income")
        c2 = number_card("$38", "/ GPU·小时", "整体收入折算（夜间谷时定价口径）", color=EXPERT).move_to([3.4, 0.2, 0])
        self.play(FadeIn(c2), run_time=0.8)

        self.until("hardware")
        hw_title = T("官方声明支持硬件平台", 18, MUTED).move_to([0, -1.4, 0])
        hw1 = Block("NVIDIA SM100 GPU", color=GPU, w=3.4, h=0.65, size=18)
        hw2 = Block("华为昇腾 950 NPU", color=PREFILL, w=3.4, h=0.65, size=18)
        hw_row = VGroup(hw1, hw2).arrange(RIGHT, buff=0.5).next_to(hw_title, DOWN, buff=0.15)
        hw_group = VGroup(hw_title, hw_row)
        self.play(FadeIn(hw_group), run_time=0.8)

        self.finish()


class EP00_S06(DVScene):
    SHOT = "EP00-S06"

    def construct(self):
        head = self.fit_left_of_tags(header("看懂右上角：事实证据等级", "EP00 · S06 观影指南"))
        self.add(head)

        # 5 evidence badges in a row
        p_a = Pill("A 代码证实", GRADE_COLORS["A"], size=18)
        p_b = Pill("B 官方文档", GRADE_COLORS["B"], size=18)
        p_c = Pill("C 第三方实测", GRADE_COLORS["C"], size=18)
        p_d = Pill("D 社区说法", GRADE_COLORS["D"], size=18)
        p_e = Pill("E 推断/示意", GRADE_COLORS["E"], size=18)
        row = VGroup(p_a, p_b, p_c, p_d, p_e).arrange(RIGHT, buff=0.25).move_to([0, 0.6, 0])

        self.play(FadeIn(row), run_time=0.8)

        self.until("badge")
        info_a = T("A 级：源码 commit 9bd9cf2 逐行核对，绝对一手证据", 20, FG).move_to([0, -0.3, 0])
        self.play(FadeIn(info_a), run_time=0.6)

        self.until("green")
        self.play(Indicate(p_a, color=FG, scale_factor=1.15), run_time=0.6)

        self.until("blue")
        info_be = T("B 级：官方文档与报告 | E 级：明确标明推断与示意计算", 20, MUTED).move_to([0, -1.1, 0])
        decl = Pill("基于源码与文档静态剖析 · 无硬件实测", "#8B949E", size=18).move_to([0, -1.9, 0])
        self.play(FadeIn(info_be), FadeIn(decl), Indicate(p_b, color=FG), Indicate(p_e, color=FG), run_time=0.8)

        self.finish()


class EP00_S07(DVScene):
    SHOT = "EP00-S07"

    def construct(self):
        head = self.fit_left_of_tags(header("看懂右上角：开源范围标签", "EP00 · S07 观影指南"))
        self.add(head)

        # Green card vs Amber card
        b_green = Block("开源代码里有", color=KV, w=4.5, h=2.0, size=24,
                        sub="在当前开源仓库有完整实现\n函数、类、内核与调度器", fill=0.15).move_to([-3.2, -0.2, 0])
        b_amber = Block("仅文档描述 · 未开源", color="#D29922", w=4.5, h=2.0, size=24,
                        sub="仅在知乎/QA技术文档中描述\n生产在线服务与外部基础设施", fill=0.15).move_to([3.2, -0.2, 0])

        self.play(FadeIn(b_green), FadeIn(b_amber), run_time=0.8)

        self.until("scope_green")
        self.play(Indicate(b_green, color=KV, scale_factor=1.06), run_time=0.6)

        self.until("scope_amber")
        self.play(Indicate(b_amber, color="#D29922", scale_factor=1.06), run_time=0.6)

        bottom_hint = T("通过颜色标签，一眼区分代码现状与生产构想", 20, FG).move_to([0, -1.9, 0])
        self.play(FadeIn(bottom_hint), run_time=0.6)

        self.finish()


class EP00_S08(DVScene):
    SHOT = "EP00-S08"

    def construct(self):
        head = self.fit_left_of_tags(header("暂停自测题", "EP00 · S08 互动检查点"))
        self.add(head)

        q_card = RoundedRectangle(corner_radius=0.15, width=9.6, height=2.8,
                                  stroke_color=EXPERT, stroke_width=2.5, fill_color="#161B22", fill_opacity=0.96)
        q_card.move_to([0, 0.1, 0])
        q_title = T("停一下，做一道快速自测题：", 22, EXPERT).next_to(q_card.get_top(), DOWN, buff=0.3)
        q_text = T("右上角绿色和琥珀色的标签分别是什么意思？", 26, FG).next_to(q_title, DOWN, buff=0.35)
        q_group = VGroup(q_card, q_title, q_text)

        self.play(FadeIn(q_group), run_time=0.8)

        self.until("timer")
        cd_text = T("思考时间 5 秒", 18, MUTED).next_to(q_text, DOWN, buff=0.3)
        self.play(FadeIn(cd_text), run_time=0.5)

        self.until("answer")
        ans_green = Pill("绿色：开源代码里有（仓库真实源码）", KV, size=18).move_to([-0.1, -1.7, 0])
        ans_amber = Pill("琥珀色：仅文档描述（未开源在线组件）", "#D29922", size=18).next_to(ans_green, DOWN, buff=0.15)
        self.play(FadeIn(ans_green), FadeIn(ans_amber), run_time=0.8)

        self.finish()


class EP00_S09(DVScene):
    SHOT = "EP00-S09"

    def construct(self):
        head = self.fit_left_of_tags(header("架构设计的三个源头", "EP00 · S09 核心线索"))
        self.add(head)

        # Triangle arrangement
        # Top: Model Structure
        b_model = Block("源头一：模型结构", color=SWA, w=3.8, h=0.9, size=20, sub="40层SWA / YOCO共享KV").move_to([0, 1.2, 0])
        # Bottom left: Deployment
        b_deploy = Block("源头二：部署形态", color=PREFILL, w=3.8, h=0.9, size=20, sub="P 8卡机 / D 64-128卡宽EP").move_to([-3.6, -1.2, 0])
        # Bottom right: Production requirements
        b_prod = Block("源头三：生产需求", color=DECODE, w=3.8, h=0.9, size=20, sub="双硬件 / 批不变与确定性").move_to([3.6, -1.2, 0])

        # Center core
        b_center = Block("DeepInfer", color=EXPERT, w=2.4, h=0.8, size=22, fill=0.25).move_to([0, -0.3, 0])

        # Arrows to center
        a1 = Arrow(b_model.get_bottom(), b_center.get_top(), color=SWA, stroke_width=2.5, buff=0.1)
        a2 = Arrow(b_deploy.get_top() + RIGHT * 0.5, b_center.get_left() + DOWN * 0.2, color=PREFILL, stroke_width=2.5, buff=0.1)
        a3 = Arrow(b_prod.get_top() + LEFT * 0.5, b_center.get_right() + DOWN * 0.2, color=DECODE, stroke_width=2.5, buff=0.1)

        self.play(FadeIn(b_center), run_time=0.6)

        self.until("model")
        self.play(FadeIn(b_model), Create(a1), run_time=0.7)

        self.until("deploy")
        self.play(FadeIn(b_deploy), Create(a2), run_time=0.7)

        self.until("prod")
        self.play(FadeIn(b_prod), Create(a3), Indicate(b_center, color=EXPERT, scale_factor=1.08), run_time=0.8)

        self.finish()


class EP00_S10(DVScene):
    SHOT = "EP00-S10"

    def construct(self):
        head = self.fit_left_of_tags(header("贯穿案例：第五轮请求", "EP00 · S10 案例设定"))
        self.add(head)

        # Agent chat bubble
        chat_box = RoundedRectangle(corner_radius=0.12, width=8.5, height=1.0,
                                    stroke_color=CPU, stroke_width=2, fill_color="#161B22", fill_opacity=0.95)
        chat_box.move_to([0, 0.9, 0])
        c_title = T("编程智能体：第 5 轮修改计划请求", 20, CPU).next_to(chat_box.get_top(), DOWN, buff=0.2)
        c_desc = T("输入包含前 4 轮代码与历史上下文（约 60,000 token），要求 JSON 输出", 18, FG).next_to(c_title, DOWN, buff=0.15)
        chat_group = VGroup(chat_box, c_title, c_desc)

        # Token row schematic
        row = TokenRow(24, color=PREFILL, size=0.25, gap=0.05).move_to([0, -0.3, 0])
        row_label = T("~60,000 token 长上下文序列（示意）", 18, MUTED).next_to(row, UP, buff=0.12)
        token_group = VGroup(row, row_label)

        self.play(FadeIn(chat_group), FadeIn(token_group), run_time=0.8)

        self.until("agent")
        self.play(Indicate(row, color=FG, scale_factor=1.05), run_time=0.6)

        self.until("reason")
        p1 = Pill("长前缀命中", KV, size=16)
        p2 = Pill("SWA 有界重放", SWA, size=16)
        p3 = Pill("宽 EP 专家解码", EXPERT, size=16)
        p4 = Pill("结构化 JSON 输出", DECODE, size=16)
        trigger_row = VGroup(p1, p2, p3, p4).arrange(RIGHT, buff=0.25).move_to([0, -1.6, 0])
        self.play(FadeIn(trigger_row), run_time=0.8)

        self.finish()


class EP00_S11(DVScene):
    SHOT = "EP00-S11"

    def construct(self):
        head = self.fit_left_of_tags(header("穿过六大站点，走完十四集", "EP00 · S11 路线地图"))
        self.add(head)

        # Large station flow layout
        mmap = MiniMap(active="入口", scale=1.05).move_to([0, 0.7, 0])
        self.play(FadeIn(mmap), run_time=0.8)

        ep_guide = VGroup(
            T("入口/路由：EP02, EP11", 18, FG),
            T("Prefill 计算与 KV 存储：EP03, EP06, EP07", 18, SWA),
            T("Decode 调度与宽专家并行：EP05, EP08, EP09, EP10", 18, DECODE),
            T("代码地图与生态统合：EP04, EP12, EP13", 18, EXPERT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -0.9, 0])

        self.until("journey")
        self.play(FadeIn(ep_guide[:2]), run_time=0.7)

        self.until("decode")
        self.play(FadeIn(ep_guide[2:]), run_time=0.8)

        self.finish()


class EP00_S12(DVScene):
    SHOT = "EP00-S12"

    def construct(self):
        head = self.fit_left_of_tags(header("本集要点 · 三句话总结", "EP00 · S12 本集要点"))
        self.add(head)

        c1 = Block("1. 专用离线引擎，仅服务 V4.1-Flash", color=DECODE, w=8.8, h=0.75, size=20, fill=0.15).move_to([0, 0.5, 0])
        c2 = Block("2. 特色设计源自模型结构、部署形态与生产需求", color=SWA, w=8.8, h=0.75, size=20, fill=0.15).move_to([0, -0.4, 0])
        c3 = Block("3. 跟随单个长请求走完六个站点，看懂系统全貌", color=KV, w=8.8, h=0.75, size=20, fill=0.15).move_to([0, -1.3, 0])

        self.until("p1")
        self.play(FadeIn(c1), run_time=0.6)

        self.until("p2")
        self.play(FadeIn(c2), run_time=0.6)

        self.until("p3")
        self.play(FadeIn(c3), run_time=0.6)

        self.finish()


class EP00_S13(DVScene):
    SHOT = "EP00-S13"

    def construct(self):
        head = self.fit_left_of_tags(header("下一集：推理引擎到底在忙什么？", "EP00 · S13 下集钩子"))
        self.add(head)

        # Scale component: left GPU compute, right memory traffic
        scale = Scale(left="算力 FLOPs", right="搬运权重与 KV", left_color=GPU, right_color=WARN,
                      w=6.4, h=2.5, size=20).move_to([0, -0.6, 0])

        self.play(FadeIn(scale), run_time=0.8)

        self.until("wait")
        # Tilt the beam towards right (traffic bottleneck)
        # Rotate beam around its center, right pan moves down, left pan moves up
        self.play(
            scale.beam.animate.rotate(-0.15),
            scale.right_pan.animate.shift(DOWN * 0.45),
            scale.left_pan.animate.shift(UP * 0.45),
            run_time=1.0,
        )
        warn_txt = T("生成 token 时：大部分时间在'搬'而不是'算'", 20, WARN).move_to([0, -2.0, 0])
        self.play(FadeIn(warn_txt), run_time=0.6)

        self.finish()
