"""EP02 scenes: DeepInfer 是什么，不是什么 (shots S01-S19)."""
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
    code_panel, number_card, LayerStack, AttentionMatrix, Scale, T, M, arrow,
)


class EP02_S01(DVScene):
    SHOT = "EP02-S01"

    def construct(self):
        head = self.fit_left_of_tags(header("寻找不存在的 API 入口", "EP02 · S01 冷开场"))
        self.add(head)

        panel = code_panel(
            "git clone https://github.com/deepseek-ai/DeepInfer\n"
            "cd DeepInfer\n"
            "grep -rn 'FastAPI\\|uvicorn\\|server' .\n"
            "# 0 matches found",
            "terminal",
            highlight=[1, 3],
            size=18,
            width=6.8,
        ).move_to([-2.6, -0.4, 0])
        self.play(FadeIn(panel), run_time=0.8)

        self.until("clone")
        self.play(Indicate(panel, color=DECODE), run_time=0.6)

        self.until("search")
        warn_box = Block("未找到 API 服务组件", WARN, w=3.8, h=0.8, size=18, sub="全仓无 HTTP 路由入口").move_to([3.4, 0.4, 0])
        self.play(FadeIn(warn_box), run_time=0.6)

        self.until("offline")
        offline_box = Block("examples/offline_inference.py", KV, w=4.5, h=0.9, size=18, sub="离线推理入口 (LLM.generate)").move_to([3.4, -0.7, 0])
        self.play(FadeIn(offline_box), run_time=0.6)

        self.until("engine")
        tag = Pill("生产离线推理框架 · 纯批处理", DECODE, size=18).move_to([0, -2.1, 0])
        self.play(FadeIn(tag), run_time=0.6)

        self.until("title")
        self.play(Indicate(tag, color=FG), run_time=0.5)
        self.finish()


class EP02_S02(DVScene):
    SHOT = "EP02-S02"

    def construct(self):
        title = T("EP02 · DeepInfer 是什么，不是什么", 36, FG).move_to([0, 1.0, 0])
        mmap = MiniMap(active=None, scale=1.1).move_to([0, -0.6, 0])
        self.play(FadeIn(title), FadeIn(mmap), run_time=0.8)

        self.until("title")
        self.play(Indicate(title, color=DECODE), run_time=0.6)
        self.finish()


class EP02_S03(DVScene):
    SHOT = "EP02-S03"

    def construct(self):
        head = self.fit_left_of_tags(header("官方定位：生产离线推理框架", "EP02 · S03 官方定位"))
        self.add(head)

        doc_box = RoundedRectangle(corner_radius=0.12, width=7.2, height=2.0,
                                   stroke_color=GRID, stroke_width=2, fill_color="#161B22", fill_opacity=0.95).move_to([-1.8, -0.3, 0])
        doc_tag = M("README.md:3", 16, MUTED).next_to(doc_box.get_top(), DOWN, buff=0.15).align_to(doc_box, LEFT).shift(RIGHT * 0.3)
        doc_t1 = T("DeepInfer is the high-performance inference framework", 18, FG).next_to(doc_tag, DOWN, buff=0.15).align_to(doc_tag, LEFT)
        doc_t2 = T("that powers DeepSeek's large-scale production services.", 18, FG).next_to(doc_t1, DOWN, buff=0.1).align_to(doc_t1, LEFT)
        doc_t3 = T("This release provides offline inference with core features.", 18, DECODE).next_to(doc_t2, DOWN, buff=0.1).align_to(doc_t2, LEFT)
        doc_group = VGroup(doc_box, doc_tag, doc_t1, doc_t2, doc_t3)
        self.play(FadeIn(doc_group), run_time=0.8)

        self.until("readme")
        self.play(doc_box.animate.set_stroke(DECODE, 2.5), run_time=0.5)

        self.until("quote")
        self.play(Indicate(doc_t3, color=PREFILL), run_time=0.6)

        self.until("offline")
        c1 = Block("离线批处理 (Offline)", DECODE, w=3.4, h=0.85, size=18, sub="专注计算 · 无网络时延").move_to([4.2, 0.4, 0])
        self.play(FadeIn(c1), run_time=0.5)

        self.until("mission")
        c2 = Block("规模化生产能力", PREFILL, w=3.4, h=0.85, size=18, sub="核心调度与算子开源").move_to([4.2, -0.7, 0])
        self.play(FadeIn(c2), run_time=0.5)

        self.until("focus")
        pill = Pill("纯本地单机计算极限", KV, size=18).move_to([0, -2.1, 0])
        self.play(FadeIn(pill), run_time=0.5)
        self.finish()


class EP02_S04(DVScene):
    SHOT = "EP02-S04"

    def construct(self):
        head = self.fit_left_of_tags(header("模型限定：专供 V4.1-Flash", "EP02 · S04 模型限定"))
        self.add(head)

        box_left = Block("DeepSeek-V4.1-Flash", PREFILL, w=5.0, h=1.4, size=24, sub="官方唯一支持主干模型\n40层SWA + 4层KV + YOCO").move_to([-3.0, -0.3, 0])
        self.play(FadeIn(box_left), run_time=0.8)

        self.until("list")
        self.play(box_left.animate.set_stroke(EXPERT, 3), run_time=0.6)

        self.until("model")
        self.play(Indicate(box_left, color=FG), run_time=0.6)

        self.until("not_generic")
        generic_group = VGroup()
        for idx, name in enumerate(["Llama-3 (通用模型)", "Qwen-2.5 (通用模型)", "Mistral (通用模型)"]):
            b = RoundedRectangle(corner_radius=0.08, width=3.8, height=0.48, stroke_color=GRID, stroke_width=1.5, fill_color="#12161D", fill_opacity=0.7)
            t = T(f"✕ {name}", 16, MUTED).move_to(b)
            generic_group.add(VGroup(b, t))
        generic_group.arrange(DOWN, buff=0.15).move_to([3.4, -0.3, 0])
        self.play(FadeIn(generic_group), run_time=0.7)

        self.until("design")
        line = DashedLine(box_left.get_right(), generic_group.get_left(), color=WARN)
        self.play(Create(line), run_time=0.5)

        self.until("custom")
        pill = Pill("深度定制的专用推理引擎", EXPERT, size=18).move_to([0, -2.1, 0])
        self.play(FadeIn(pill), run_time=0.5)

        self.until("mismatch")
        self.play(Indicate(generic_group, color=WARN), run_time=0.5)
        self.finish()


class EP02_S05(DVScene):
    SHOT = "EP02-S05"

    def construct(self):
        head = self.fit_left_of_tags(header("硬件边界：SM100 与昇腾 950 双轨支持", "EP02 · S05 硬件支持"))
        self.add(head)

        chip_nv = Block("NVIDIA SM100", DECODE, w=4.0, h=1.1, size=20, sub="TileLang + CUDA 13\nSM100 架构算子").move_to([-3.2, 0.4, 0])
        chip_asc = Block("Huawei Ascend 950", PREFILL, w=4.0, h=1.1, size=20, sub="TileLang + CANN 9.2\n昇腾 950 专用算子").move_to([3.2, 0.4, 0])
        self.play(FadeIn(chip_nv), FadeIn(chip_asc), run_time=0.8)

        self.until("hw_title")
        self.until("two_hw")
        self.play(Indicate(chip_nv, color=FG), Indicate(chip_asc, color=FG), run_time=0.6)

        self.until("chips")
        tree_panel = code_panel(
            "csrc/\n"
            "├── cuda/  # NVIDIA SM100 算子镜像\n"
            "└── asc/   # 华为昇腾 950 算子镜像",
            "csrc/ 目录结构",
            highlight=[2, 3],
            size=18,
            width=7.2,
        ).move_to([0, -1.0, 0])
        self.play(FadeIn(tree_panel), run_time=0.7)

        self.until("tree")
        self.until("mirror")
        self.play(tree_panel.animate.set_stroke(DECODE, 2), run_time=0.5)

        self.until("vendor")
        pill = Pill("生产多厂商战略 · 双平台镜像对齐", KV, size=18).move_to([0, -2.15, 0])
        self.play(FadeIn(pill), run_time=0.5)

        self.until("barrier")
        self.play(Indicate(pill, color=FG), run_time=0.5)
        self.finish()


class EP02_S06(DVScene):
    SHOT = "EP02-S06"

    def construct(self):
        head = self.fit_left_of_tags(header("八大核心特性与全系列导航", "EP02 · S06 特性地图"))
        self.add(head)

        features = [
            ("TileLang 硬件算子", "EP10", DECODE),
            ("注意力DP / 宽EP", "EP08", EXPERT),
            ("DSpark 投机解码", "EP09", DRAFT),
            ("SWA 有界重放", "EP07", SWA),
            ("ZOS 零开销调度", "EP05", GPU),
            ("批不变推理", "EP10", CPU),
            ("确定性采样", "EP10", KV),
            ("结构化输出", "EP10", PREFILL),
        ]

        grid = VGroup()
        for name, ep, col in features:
            b = RoundedRectangle(corner_radius=0.08, width=2.8, height=0.7, stroke_color=GRID, stroke_width=1.5, fill_color="#161B22", fill_opacity=0.9)
            t = T(name, 16, FG).move_to(b).shift(UP * 0.08)
            p = T(f"[{ep}]", 16, col).next_to(t, DOWN, buff=0.04)
            grid.add(VGroup(b, t, p))
        grid.arrange_in_grid(rows=2, cols=4, buff=(0.25, 0.2)).move_to([0, -0.6, 0])
        self.play(FadeIn(grid), run_time=0.8)

        self.until("features")
        self.until("map")
        self.play(Indicate(grid, color=DECODE), run_time=0.6)

        self.until("kernel")
        self.play(grid[0].animate.set_stroke(DECODE, 2.5), run_time=0.5)

        self.until("parallel")
        self.play(grid[1].animate.set_stroke(EXPERT, 2.5), run_time=0.5)

        self.until("spec")
        self.play(grid[2].animate.set_stroke(DRAFT, 2.5), grid[3].animate.set_stroke(SWA, 2.5), run_time=0.5)

        self.until("zos")
        self.play(grid[4].animate.set_stroke(GPU, 2.5), run_time=0.5)

        self.until("det")
        self.play(grid[5].animate.set_stroke(CPU, 2.5), grid[6].animate.set_stroke(KV, 2.5), grid[7].animate.set_stroke(PREFILL, 2.5), run_time=0.5)
        self.finish()


class EP02_S07(DVScene):
    SHOT = "EP02-S07"

    def construct(self):
        head = self.fit_left_of_tags(header("为什么不能直接对外提供服务？", "EP02 · S07 提问介入"))
        self.add(head)

        q_box = Block("提问：既然实现了这么多特性，为何无法直接做 API 服务？", EXPERT, w=8.5, h=0.75, size=18).move_to([0, 0.8, 0])
        self.play(FadeIn(q_box), run_time=0.6)

        self.until("ask")
        self.play(Indicate(q_box, color=FG), run_time=0.5)

        self.until("answer")
        left_c = Block("在线 API 云服务", WARN, w=4.5, h=1.4, size=20, sub="HTTP 入口 + 鉴权路由\n请求排队 + 流量调度\n分布式 KV 缓存共享").move_to([-3.0, -0.6, 0])
        right_c = Block("DeepInfer 开源版", KV, w=4.5, h=1.4, size=20, sub="单机离线批处理 (LLM)\n高性能计算算子与调度\n无网络通信 · 无分布式存储").move_to([3.0, -0.6, 0])
        self.play(FadeIn(left_c), FadeIn(right_c), run_time=0.7)

        self.until("offline")
        self.play(right_c.animate.set_stroke(KV, 3), run_time=0.5)

        self.until("queue")
        self.play(left_c.animate.set_stroke(WARN, 3), run_time=0.5)

        self.until("gap")
        pill = Pill("单机计算核心 vs 分布式在线系统", MUTED, size=18).move_to([0, -2.15, 0])
        self.play(FadeIn(pill), run_time=0.5)
        self.finish()


class EP02_S08(DVScene):
    SHOT = "EP02-S08"

    def construct(self):
        head = self.fit_left_of_tags(header("官方明确不包含的三大基建", "EP02 · S08 缺件清单"))
        self.add(head)

        gaps = [
            ("缺件一：分布式 KV 系统", "集中式存储 · 72h+ 生命周期"),
            ("缺件二：E/P/D 分离部署", "跨机传输 · 预填充与解码解耦"),
            ("缺件三：在线负载均衡", "数据并行副本间在线请求路由"),
        ]
        cards = VGroup()
        for t, s in gaps:
            b = Block(t, WARN, w=3.6, h=1.1, size=18, sub=s)
            cards.add(b)
        cards.arrange(RIGHT, buff=0.35).move_to([0, -0.2, 0])
        self.play(FadeIn(cards), run_time=0.8)

        self.until("gaplist")
        self.until("three")
        self.play(Indicate(cards, color=FG), run_time=0.6)

        self.until("gap_kv")
        self.play(cards[0].animate.set_stroke(WARN, 3.5), run_time=0.5)

        self.until("gap_pd")
        self.play(cards[1].animate.set_stroke(WARN, 3.5), run_time=0.5)

        self.until("gap_lb")
        self.play(cards[2].animate.set_stroke(WARN, 3.5), run_time=0.5)

        self.until("infra")
        pill = Pill("与内部基础设施强耦合 · 暂未完整开源", MUTED, size=18).move_to([0, -2.15, 0])
        self.play(FadeIn(pill), run_time=0.5)

        self.until("unreleased")
        self.play(Indicate(pill, color=FG), run_time=0.5)
        self.finish()


class EP02_S09(DVScene):
    SHOT = "EP02-S09"

    def construct(self):
        head = self.fit_left_of_tags(header("生产拓扑：E/P/D 三段分离架构", "EP02 · S09 生产全景"))
        self.add(head)

        # E/P/D Architecture Map
        ep_box = Block("Entrypoint (入口网关)", CPU, w=7.5, h=0.65, size=18, sub="协议转换 · 元数据前缀匹配 · 路由分发").move_to([0, 0.9, 0])
        p_box = Block("Prefill 集群", PREFILL, w=3.4, h=0.9, size=18, sub="标准 8 卡服务器\nEP2–8 / DP2–8 (算力受限)").move_to([-2.4, -0.3, 0])
        d_box = Block("Decode 集群", DECODE, w=3.4, h=0.9, size=18, sub="64–128 卡超节点\nWide-EP (带宽受限)").move_to([2.4, -0.3, 0])
        store_box = Block("专用 3FS 分布式存储集群", KV, w=7.5, h=0.65, size=18, sub="20 × NVMe SSD · 10+2 EC · KV 留存 72 小时以上").move_to([0, -1.5, 0])

        ar_ep_p = arrow(ep_box.get_bottom() + LEFT * 2.4, p_box.get_top(), color=MUTED)
        ar_ep_d = arrow(ep_box.get_bottom() + RIGHT * 2.4, d_box.get_top(), color=MUTED)
        ar_p_s = arrow(p_box.get_bottom(), store_box.get_top() + LEFT * 2.4, color=MUTED)
        ar_d_s = arrow(d_box.get_bottom(), store_box.get_top() + RIGHT * 2.4, color=MUTED)

        sys_map = VGroup(ep_box, p_box, d_box, store_box, ar_ep_p, ar_ep_d, ar_p_s, ar_d_s)
        self.play(FadeIn(sys_map), run_time=0.9)

        self.until("fullmap")
        self.until("epd")
        self.play(Indicate(sys_map, color=FG), run_time=0.6)

        self.until("ep")
        self.play(ep_box.animate.set_stroke(DECODE, 2.5), run_time=0.5)

        self.until("prefill")
        self.play(p_box.animate.set_stroke(PREFILL, 2.5), run_time=0.5)

        self.until("decode")
        self.play(d_box.animate.set_stroke(DECODE, 2.5), run_time=0.5)

        self.until("storage")
        self.play(store_box.animate.set_stroke(KV, 2.5), run_time=0.5)

        self.until("decouple")
        pill = Pill("计算解耦 · 算力受限与带宽受限物理隔离", MUTED, size=18).move_to([0, -2.3, 0])
        self.play(FadeIn(pill), run_time=0.5)
        self.finish()


class EP02_S10(DVScene):
    SHOT = "EP02-S10"

    def construct(self):
        head = self.fit_left_of_tags(header("实例分工：Prefill 8卡 vs Decode 超节点", "EP02 · S10 实例配置"))
        self.add(head)

        box_p = Block("Prefill 计算节点", PREFILL, w=4.8, h=1.6, size=20, sub="硬件规格：标准 8 卡服务器\n并行策略：EP2–8 / DP2–8\n物理瓶颈：算力受限 (Compute)\n核心诉求：大矩阵乘满载吞吐").move_to([-3.0, -0.4, 0])
        box_d = Block("Decode 计算节点", DECODE, w=4.8, h=1.6, size=20, sub="硬件规格：64–128 卡超节点\n并行策略：Wide-EP (EP64–128)\n物理瓶颈：显存带宽受限 (Memory)\n收益指标：削减单步权重访存流量").move_to([3.0, -0.4, 0])
        self.play(FadeIn(box_p), FadeIn(box_d), run_time=0.8)

        self.until("diff")
        self.play(Indicate(box_p, color=FG), Indicate(box_d, color=FG), run_time=0.6)

        self.until("p8")
        self.play(box_p.animate.set_stroke(PREFILL, 3), run_time=0.5)

        self.until("d_bw")
        self.until("d_super")
        self.play(box_d.animate.set_stroke(DECODE, 3), run_time=0.5)

        self.until("traffic")
        self.until("tps")
        pill = Pill("Wide-EP 超节点：有效提升整机解码 TPS", EXPERT, size=18).move_to([0, -2.15, 0])
        self.play(FadeIn(pill), run_time=0.5)
        self.finish()


class EP02_S11(DVScene):
    SHOT = "EP02-S11"

    def construct(self):
        head = self.fit_left_of_tags(header("开源边界：高亮真实的开源部分", "EP02 · S11 开源边界"))
        self.add(head)

        # System overview with open-source highlight
        ep_box = Block("Entrypoint (入口)", GRID, w=7.2, h=0.6, size=18, sub="未开源 (HTTP网关/路由LB)", fill=0.08).move_to([0, 0.9, 0])
        p_outer = RoundedRectangle(corner_radius=0.1, width=3.4, height=1.3, stroke_color=GRID, stroke_width=1.5, fill_color="#12161D", fill_opacity=0.6).move_to([-2.2, -0.2, 0])
        p_lbl = T("Prefill 实例 (未开源机柜)", 16, MUTED).next_to(p_outer.get_top(), DOWN, buff=0.1)
        p_eng = Block("DeepInfer 引擎内核", KV, w=2.8, h=0.6, size=16, sub="[已开源代码]").move_to([-2.2, -0.45, 0])

        d_outer = RoundedRectangle(corner_radius=0.1, width=3.4, height=1.3, stroke_color=GRID, stroke_width=1.5, fill_color="#12161D", fill_opacity=0.6).move_to([2.2, -0.2, 0])
        d_lbl = T("Decode 实例 (未开源超节点)", 16, MUTED).next_to(d_outer.get_top(), DOWN, buff=0.1)
        d_eng = Block("DeepInfer 引擎内核", KV, w=2.8, h=0.6, size=16, sub="[已开源代码]").move_to([2.2, -0.45, 0])

        store_box = Block("专用 3FS 分布式存储集群", GRID, w=7.2, h=0.6, size=18, sub="未开源 (集中式存储系统)", fill=0.08).move_to([0, -1.4, 0])

        all_sys = VGroup(ep_box, p_outer, p_lbl, p_eng, d_outer, d_lbl, d_eng, store_box)
        self.play(FadeIn(all_sys), run_time=0.8)

        self.until("overlay")
        self.until("highlight")
        self.play(p_eng.animate.set_stroke(KV, 3.5), d_eng.animate.set_stroke(KV, 3.5), run_time=0.6)

        self.until("engine")
        self.play(Indicate(p_eng, color=FG), Indicate(d_eng, color=FG), run_time=0.5)

        self.until("outer")
        self.play(ep_box.animate.set_stroke(WARN, 1.5), run_time=0.5)

        self.until("grey")
        self.play(store_box.animate.set_stroke(WARN, 1.5), run_time=0.5)

        self.until("core")
        pill = Pill("开源范围：仅单机计算核心 · 外部在线网络未公开", KV, size=18).move_to([0, -2.2, 0])
        self.play(FadeIn(pill), run_time=0.5)

        self.until("boundary")
        self.play(Indicate(pill, color=FG), run_time=0.5)
        self.finish()


class EP02_S12(DVScene):
    SHOT = "EP02-S12"

    def construct(self):
        head = self.fit_left_of_tags(header("规模真相：155 万亿与 38 美元口径", "EP02 · S12 规模营收"))
        self.add(head)

        q_txt = Block("提问：官方公布的生产指标代表什么口径？", EXPERT, w=8.2, h=0.65, size=18).move_to([0, 0.85, 0])
        self.play(FadeIn(q_txt), run_time=0.6)

        self.until("ask")
        card1 = number_card("155", "万亿 / 天", "单集群日服务吞吐 (~179万 token/s)", color=PREFILL).move_to([-3.0, -0.4, 0])
        card2 = number_card("38", "美元 / 卡·时", "按官方公布谷时优惠定价折算营收", color=DECODE).move_to([3.0, -0.4, 0])
        self.play(FadeIn(card1), FadeIn(card2), run_time=0.8)

        self.until("rate")
        self.play(Indicate(card1, color=FG), run_time=0.6)

        self.until("revenue")
        self.play(Indicate(card2, color=FG), run_time=0.6)

        self.until("valley")
        pill = Pill("限定条件：整体营收而非利润 · 谷时定价测算", WARN, size=18).move_to([0, -2.15, 0])
        self.play(FadeIn(pill), run_time=0.5)

        self.until("scale")
        self.play(Indicate(pill, color=FG), run_time=0.5)
        self.finish()


class EP02_S13(DVScene):
    SHOT = "EP02-S13"

    def construct(self):
        head = self.fit_left_of_tags(header("外置存储：14.4 TB/卡与专用 3FS 集群", "EP02 · S13 存储规格"))
        self.add(head)

        b1 = Block("最小高效服务单元", CPU, w=3.4, h=1.3, size=18, sub="64P + 64D\n合计 128 张 GPU\n生产集群标准单元").move_to([-4.0, -0.3, 0])
        b2 = Block("存储配比与容量", KV, w=3.4, h=1.3, size=18, sub="每卡 14.4 TB (逻辑)\n128卡对应 1.84 PB\nKV 留存 72 小时以上").move_to([0, -0.3, 0])
        b3 = Block("单台存储机规格", EXPERT, w=3.4, h=1.3, size=18, sub="20 × NVMe SSD (614 TB)\n读写比 8:1 (40G读/5G写)\n跨机互联 400G / 8卡").move_to([4.0, -0.3, 0])

        cards = VGroup(b1, b2, b3)
        self.play(FadeIn(cards), run_time=0.8)

        self.until("unit")
        self.play(b1.animate.set_stroke(CPU, 3), run_time=0.5)

        self.until("storage")
        self.until("ratio")
        self.play(b2.animate.set_stroke(KV, 3), run_time=0.5)

        self.until("ssd")
        self.until("bandwidth")
        self.play(b3.animate.set_stroke(EXPERT, 3), run_time=0.5)

        self.until("network")
        pill = Pill("集中式 SSD 存储集群：支撑数万人在线长会话", MUTED, size=18).move_to([0, -2.15, 0])
        self.play(FadeIn(pill), run_time=0.5)

        self.until("cost")
        self.play(Indicate(pill, color=FG), run_time=0.5)
        self.finish()


class EP02_S14(DVScene):
    SHOT = "EP02-S14"

    def construct(self):
        head = self.fit_left_of_tags(header("外部装甲：deepseek-recipe 独立定位", "EP02 · S14 辅助仓库"))
        self.add(head)

        top_box = Block("deepseek-recipe (独立开源仓库)", CPU, w=7.8, h=0.75, size=20, sub="Rust 核心实现 · PyO3 Python 绑定 · 请求与流式数据处理").move_to([0, 0.7, 0])
        self.play(FadeIn(top_box), run_time=0.7)

        self.until("recipe")
        self.until("name")
        self.until("rust")
        self.play(top_box.animate.set_stroke(DECODE, 2.5), run_time=0.5)

        self.until("pre")
        c1 = Block("协议转换", DECODE, w=3.2, h=1.0, size=18, sub="OpenAI / Anthropic\n输入格式标准化").move_to([-3.4, -0.65, 0])
        c2 = Block("防Token注入", PREFILL, w=3.2, h=1.0, size=18, sub="BPE词表剥离与并行编码\n杜绝特殊标记伪造").move_to([0, -0.65, 0])
        c3 = Block("流式解析", SWA, w=3.2, h=1.0, size=18, sub="11阶段状态机\n逐字解析DSML与思考").move_to([3.4, -0.65, 0])

        armors = VGroup(c1, c2, c3)
        self.play(FadeIn(armors), run_time=0.8)

        self.until("protocol")
        self.play(c1.animate.set_stroke(DECODE, 3), run_time=0.5)

        self.until("sec")
        self.play(c2.animate.set_stroke(PREFILL, 3), run_time=0.5)

        self.until("stream")
        self.play(c3.animate.set_stroke(SWA, 3), run_time=0.5)

        self.until("armor")
        pill = Pill("外围防线：物理解耦的协议与安全网关", KV, size=18).move_to([0, -2.15, 0])
        self.play(FadeIn(pill), run_time=0.5)
        self.finish()


class EP02_S15(DVScene):
    SHOT = "EP02-S15"

    def construct(self):
        head = self.fit_left_of_tags(header("Aha 揭晓：仓库里的“架构插槽”", "EP02 · S15 架构插槽"))
        self.add(head)

        q_box = Block("提问：既然没有网络传输，为何官方称大部分功能已实现？", EXPERT, w=8.5, h=0.65, size=18).move_to([0, 0.85, 0])
        self.play(FadeIn(q_box), run_time=0.6)

        self.until("ask")
        self.until("aha")
        panel1 = code_panel(
            "class EngineType(enum.Enum):\n"
            "    NORMAL = 0\n"
            "    PROMPT = 1     # 预填充\n"
            "    COMPLETION = 2 # 解码",
            "engine_type.py",
            highlight=[2, 3, 4],
            size=16,
            width=5.2,
        ).move_to([-3.4, -0.5, 0])

        panel2 = code_panel(
            "def init_pd_split(self): pass\n"
            "def do_save_kvcache(self, ...): pass\n"
            "def should_copy_state(self, seq):\n"
            "    return False",
            "llm_engine.py",
            highlight=[1, 2, 3, 4],
            size=16,
            width=5.2,
        ).move_to([3.4, -0.5, 0])

        self.play(FadeIn(panel1), FadeIn(panel2), run_time=0.8)

        self.until("enum")
        self.play(panel1.animate.set_stroke(DECODE, 2.5), run_time=0.5)

        self.until("funcs")
        self.until("slots")
        self.play(panel2.animate.set_stroke(WARN, 2.5), run_time=0.5)

        self.until("empty")
        pill = Pill("架构插槽完备：函数签名俱在 · 具体实现留空", KV, size=18).move_to([0, -2.15, 0])
        self.play(FadeIn(pill), run_time=0.5)
        self.finish()


class EP02_S16(DVScene):
    SHOT = "EP02-S16"

    def construct(self):
        head = self.fit_left_of_tags(header("调度接缝：C++ 移交注释与显存副本", "EP02 · S16 调度接缝"))
        self.add(head)

        panel_cpp = code_panel(
            "// prefill_engine won't change status\n"
            "// because it will be transferred to\n"
            "// complete_engine\n"
            "TORCH_CHECK(engine_type != EngineType::COMPLETION\n"
            "    || stop_preempted_request);",
            "scheduler.hpp:941",
            highlight=[1, 2, 3],
            size=16,
            width=6.0,
        ).move_to([-2.8, -0.3, 0])

        box_mem = Block("显存副本区 copy_state", SWA, w=4.5, h=1.4, size=18, sub="跨128边界异步拷贝当前窗口\nSequence 暴露 num_cached_tokens\n为外部注入已算好 KV 预留接缝").move_to([3.4, -0.3, 0])

        self.play(FadeIn(panel_cpp), FadeIn(box_mem), run_time=0.8)

        self.until("cpp")
        self.until("transfer")
        self.play(panel_cpp.animate.set_stroke(DECODE, 2.5), run_time=0.5)

        self.until("stop")
        self.play(Indicate(panel_cpp, color=WARN), run_time=0.5)

        self.until("copystate")
        self.play(box_mem.animate.set_stroke(SWA, 3), run_time=0.5)

        self.until("trigger")
        self.play(Indicate(box_mem, color=FG), run_time=0.5)

        self.until("ready")
        pill = Pill("调度状态机：专为 P/D 分离量身定制", KV, size=18).move_to([0, -2.15, 0])
        self.play(FadeIn(pill), run_time=0.5)
        self.finish()


class EP02_S17(DVScene):
    SHOT = "EP02-S17"

    def construct(self):
        head = self.fit_left_of_tags(header("开源演进：从 2025 障碍到 2026 官方动机", "EP02 · S17 开源演进"))
        self.add(head)

        box_2025 = Block("2025 年 4 月 说明", WARN, w=4.5, h=1.5, size=20, sub="暂缓开源内部完整代码仓：\n1. 代码分叉过深 (vLLM fork)\n2. 内部机房基建强耦合\n3. 研发团队维护人力受限").move_to([-3.2, -0.3, 0])
        box_2026 = Block("2026 年 10 月 开源", KV, w=4.5, h=1.5, size=20, sub="剥离耦合组件 · 正式独立开源\n官方唯一开源动机说明：\n分享技术栈 · 降低算力成本\n减少能源消耗 · 使 AI 更可负担").move_to([3.2, -0.3, 0])

        self.play(FadeIn(box_2025), FadeIn(box_2026), run_time=0.8)

        self.until("history")
        self.play(box_2025.animate.set_stroke(WARN, 3), run_time=0.5)

        self.until("solution")
        self.until("strip")
        self.until("release")
        self.play(box_2026.animate.set_stroke(KV, 3), run_time=0.5)

        self.until("quote")
        self.until("purpose")
        self.play(Indicate(box_2026, color=FG), run_time=0.5)

        self.until("affordable")
        pill = Pill("降成本 · 降能耗 · 让 AI 更可负担", EXPERT, size=18).move_to([0, -2.15, 0])
        self.play(FadeIn(pill), run_time=0.5)
        self.finish()


class EP02_S18(DVScene):
    SHOT = "EP02-S18"

    def construct(self):
        head = self.fit_left_of_tags(header("思考自测：自建在线服务最少补哪几块？", "EP02 · S18 暂停题"))
        self.add(head)

        q_txt = T("若想用 DeepInfer 直接对外提供在线服务，最少自建哪两块？", 20, FG).move_to([0, 0.8, 0])
        self.play(FadeIn(q_txt), run_time=0.6)

        self.until("question")
        self.until("pause_card")
        slot1 = Block("自建缺件一：？", WARN, w=6.8, h=0.75, size=18, sub="待补齐组件").move_to([0, 0.05, 0])
        slot2 = Block("自建缺件二：？", WARN, w=6.8, h=0.75, size=18, sub="待补齐组件").move_to([0, -1.0, 0])
        self.play(FadeIn(slot1), FadeIn(slot2), run_time=0.6)

        self.until("thinking")
        self.play(Indicate(slot1, color=EXPERT), Indicate(slot2, color=EXPERT), run_time=0.5)

        self.until("answer1")
        ans1 = Block("补件一：请求接收与路由入口 (Entrypoint / LB)", DECODE, w=6.8, h=0.75, size=18, sub="HTTP 网关 · 会话管理 · 副本负载均衡")
        ans1.move_to(slot1)
        self.play(Transform(slot1, ans1), run_time=0.5)

        self.until("answer2")
        ans2 = Block("补件二：KV 缓存存储与传输网络通道", KV, w=6.8, h=0.75, size=18, sub="P 到 D 跨机传输 · 集中式持久化存储")
        ans2.move_to(slot2)
        self.play(Transform(slot2, ans2), run_time=0.5)
        self.finish()


class EP02_S19(DVScene):
    SHOT = "EP02-S19"

    def construct(self):
        head = self.fit_left_of_tags(header("总结三句话与下集预告", "EP02 · S19 总结"))
        self.add(head)

        t1 = T("1. 生产离线引擎：仅支持 V4.1-Flash 与双硬件", 18, FG)
        t2 = T("2. 缺三项在线基建：源码完整保留架构插槽", 18, FG)
        t3 = T("3. 生产拓扑：E/P/D 三段分离 + 独立 3FS 存储", 18, FG)
        recap_group = VGroup(t1, t2, t3).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-2.4, -0.4, 0])

        box_next = Block("EP03 下集预告", PREFILL, w=3.4, h=1.4, size=20, sub="先认识它服务的模型\nV4.1-Flash 架构剖析\n40层SWA · 4层KV · YOCO").move_to([3.4, -0.4, 0])

        self.play(FadeIn(recap_group), FadeIn(box_next), run_time=0.8)

        self.until("recap")
        self.until("p1")
        self.play(t1.animate.set_color(DECODE), run_time=0.5)

        self.until("p2")
        self.play(t2.animate.set_color(KV), run_time=0.5)

        self.until("p3")
        self.play(t3.animate.set_color(EXPERT), run_time=0.5)

        self.until("next")
        self.until("lead")
        self.play(box_next.animate.set_stroke(PREFILL, 3), run_time=0.5)

        self.until("outro")
        self.play(Indicate(box_next, color=FG), run_time=0.5)
        self.finish()
