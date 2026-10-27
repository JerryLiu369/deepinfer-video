"""EP10 scenes: 内核、双硬件与结果可信 (shots S01-S18)."""
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
    BG, FG, MUTED, GRID, PREFILL, DECODE, KV, SWA, WARN, EXPERT, DRAFT, CPU, GPU,
    T, M, Pill, DVScene, header, MiniMap, Block, TokenRow, window_bracket,
    code_panel, number_card, arrow,
)


class EP10_S01(DVScene):
    SHOT = "EP10-S01"

    def construct(self):
        head = self.fit_left_of_tags(header("旁边换了一个邻居，输出居然变了", "EP10 · S01 冷开场"))
        self.add(head)

        # Left side: Request A alone
        left_title = T("单请求独立执行", 20, DECODE).move_to([-3.6, 1.1, 0])
        left_prompt = TokenRow(8, color=PREFILL, size=0.32, gap=0.06).move_to([-3.6, 0.4, 0])
        left_gen = TokenRow(6, color=DECODE, size=0.32, gap=0.06).move_to([-3.6, -0.4, 0])
        left_box = RoundedRectangle(corner_radius=0.1, width=4.8, height=2.4, stroke_color=GRID, stroke_width=1.5, fill_opacity=0.05).move_to([-3.6, 0.0, 0])
        self.play(FadeIn(left_title), FadeIn(left_box), run_time=0.6)

        self.until("prompt")
        txt1 = T("相同 Prompt 与 Seed", 20, FG).move_to([-3.6, -1.8, 0])
        self.play(FadeIn(left_prompt), FadeIn(left_gen), FadeIn(txt1), run_time=0.8)

        self.until("batch")
        # Right side: Request A with neighbors
        right_title = T("合批多请求执行", 20, PREFILL).move_to([3.4, 1.1, 0])
        right_box = RoundedRectangle(corner_radius=0.1, width=5.2, height=2.4, stroke_color=GRID, stroke_width=1.5, fill_opacity=0.05).move_to([3.4, 0.0, 0])
        r1 = TokenRow(8, color=PREFILL, size=0.26, gap=0.04).move_to([3.4, 0.6, 0])
        r2 = TokenRow(10, color=MUTED, size=0.26, gap=0.04).move_to([3.4, 0.2, 0])
        r3 = TokenRow(6, color=MUTED, size=0.26, gap=0.04).move_to([3.4, -0.2, 0])
        r4 = TokenRow(11, color=MUTED, size=0.26, gap=0.04).move_to([3.4, -0.6, 0])
        txt2 = T("批组成变化（示意）", 20, MUTED).move_to([3.4, -1.8, 0])
        self.play(FadeIn(right_title), FadeIn(right_box), FadeIn(r1), FadeIn(r2), FadeIn(r3), FadeIn(r4), FadeIn(txt2), run_time=1.0)

        self.until("diverge")
        # Highlight divergent token at end of r1
        divergent_tok = Rectangle(width=0.28, height=0.28, stroke_color=WARN, stroke_width=2, fill_color=WARN, fill_opacity=0.9).move_to([5.0, 0.6, 0])
        div_lbl = T("第 40 步分叉！", 20, WARN).move_to([3.4, -1.3, 0])
        self.play(FadeIn(divergent_tok), FadeIn(div_lbl), Indicate(divergent_tok), run_time=1.0)

        self.finish()


class EP10_S02(DVScene):
    SHOT = "EP10-S02"

    def construct(self):
        t1 = T("第十集 · 内核与双硬件", 42, FG).move_to([0, 1.1, 0])
        t2 = T("结果可信的物理边界", 24, MUTED).move_to([0, 0.3, 0])
        mm = MiniMap(active="Decode").move_to([0, -1.2, 0])
        self.play(FadeIn(t1), FadeIn(t2), FadeIn(mm), run_time=0.6)

        self.until("card")
        self.finish()


class EP10_S03(DVScene):
    SHOT = "EP10-S03"

    def construct(self):
        head = self.fit_left_of_tags(header("算子底座：5 个外部内核库的分工版图", "EP10 · S03 外部库版图"))
        self.add(head)

        center_engine = Block("DeepInfer 执行引擎", FG, w=2.8, h=0.8, size=20).move_to([0, 0.2, 0])
        self.play(FadeIn(center_engine), run_time=0.6)

        self.until("layout")
        b_flash = Block("FlashMLA", DECODE, w=2.4, h=0.7, sub="稀疏注意力", size=18).move_to([-3.8, 1.2, 0])
        b_gemm = Block("DeepGEMM", PREFILL, w=2.4, h=0.7, sub="FP8/FP4 矩阵乘", size=18).move_to([3.8, 1.2, 0])
        ar1 = arrow(b_flash, center_engine, color=DECODE)
        ar2 = arrow(b_gemm, center_engine, color=PREFILL)
        self.play(FadeIn(b_flash), FadeIn(b_gemm), Create(ar1), Create(ar2), run_time=0.8)

        self.until("libs")
        b_ep = Block("DeepEP", EXPERT, w=2.4, h=0.7, sub="专家跨卡通信", size=18).move_to([-4.0, -1.0, 0])
        b_tile = Block("TileKernels", GPU, w=2.4, h=0.7, sub="门控与量化", size=18).move_to([4.0, -1.0, 0])
        b_sel = Block("DeepSelect", SWA, w=2.4, h=0.7, sub="TopK 筛选", size=18).move_to([0, -1.3, 0])
        ar3 = arrow(b_ep, center_engine, color=EXPERT)
        ar4 = arrow(b_tile, center_engine, color=GPU)
        ar5 = arrow(b_sel, center_engine, color=SWA)
        self.play(FadeIn(b_ep), FadeIn(b_tile), FadeIn(b_sel), Create(ar3), Create(ar4), Create(ar5), run_time=1.0)

        self.until("all")
        footer = T("5 个外部库 + 自研 TileLang = 完整执行底座", 22, FG).move_to([0, 1.8, 0])
        self.play(FadeIn(footer), Indicate(center_engine), run_time=0.8)

        self.finish()


class EP10_S04(DVScene):
    SHOT = "EP10-S04"

    def construct(self):
        head = self.fit_left_of_tags(header("极薄双硬件抽象：构建期的同名镜像", "EP10 · S04 平台同名包"))
        self.add(head)

        top_script = Block("scripts/build_vendor.sh", FG, w=4.2, h=0.7, size=20).move_to([0, 1.5, 0])
        self.play(FadeIn(top_script), run_time=0.6)

        self.until("branch")
        b_cuda = Block("NVIDIA CUDA", GPU, w=3.4, h=1.0, sub="deep_gemm / deep_ep\nflash_mla / deep_select", size=18).move_to([-3.4, 0.3, 0])
        b_asc = Block("Huawei Ascend", PREFILL, w=3.4, h=1.0, sub="deep_gemm / deep_ep (同名)\nflash_mla / deep_select", size=18).move_to([3.4, 0.3, 0])
        ar_l = Arrow(top_script.get_bottom(), b_cuda.get_top(), color=GPU, buff=0.1)
        ar_r = Arrow(top_script.get_bottom(), b_asc.get_top(), color=PREFILL, buff=0.1)
        self.play(Create(ar_l), Create(ar_r), FadeIn(b_cuda), FadeIn(b_asc), run_time=0.8)

        self.until("wheel")
        note_wheel = T("构建期二选一 · Python 导入完全同名", 20, DECODE).move_to([0, 0.3, 0])
        self.play(FadeIn(note_wheel), Indicate(b_cuda), Indicate(b_asc), run_time=0.8)

        self.until("sf")
        sf_l = Block("int32 容器 (4x UE8M0)", GPU, w=3.4, h=0.6, sub="英伟达 SF 格式", size=17).move_to([-3.4, -1.3, 0])
        sf_r = Block("int16 容器 (2x UE8M0)", PREFILL, w=3.4, h=0.6, sub="昇腾 SF 格式", size=17).move_to([3.4, -1.3, 0])
        self.play(FadeIn(sf_l), FadeIn(sf_r), run_time=0.8)

        self.finish()


class EP10_S05(DVScene):
    SHOT = "EP10-S05"

    def construct(self):
        head = self.fit_left_of_tags(header("自研 TileLang 算子：43 个工厂的名字级分发", "EP10 · S05 TileLang 分发"))
        self.add(head)

        b_root = Block("tilelang_ops/", FG, w=2.8, h=0.9, sub="API + 参考测试", size=19).move_to([-4.0, 0.6, 0])
        b_ops = Block("ops.py", DECODE, w=2.2, h=0.9, sub="动态重导出分发", size=19).move_to([-0.5, 0.6, 0])
        ar1 = arrow(b_root, b_ops, color=MUTED)
        self.play(FadeIn(b_root), FadeIn(b_ops), Create(ar1), run_time=0.6)

        self.until("tree")
        txt_tree = T("三层解耦：根目录定义规范 · ops.py 名字级分发", 20, FG).move_to([0, 1.7, 0])
        self.play(FadeIn(txt_tree), run_time=0.6)

        self.until("factories")
        b_cuda = Block("cuda/ (43 个 *_tl)", GPU, w=3.2, h=0.7, sub="T.Kernel + TMA/PDL", size=17).move_to([3.8, 1.1, 0])
        b_asc = Block("asc/ (43 个 *_tl)", PREFILL, w=3.2, h=0.7, sub="Persistent + UB/SIMD", size=17).move_to([3.8, 0.1, 0])
        ar_c = Arrow(b_ops.get_right(), b_cuda.get_left(), color=GPU, buff=0.1)
        ar_a = Arrow(b_ops.get_right(), b_asc.get_left(), color=PREFILL, buff=0.1)
        self.play(Create(ar_c), Create(ar_a), FadeIn(b_cuda), FadeIn(b_asc), run_time=0.8)

        self.until("platform")
        footer = T("昇腾采用 rstd_1ulp 两段补偿对齐 hai-llm 精度", 20, MUTED).move_to([0, -1.4, 0])
        self.play(FadeIn(footer), Indicate(b_asc), run_time=0.8)

        self.finish()


class EP10_S06(DVScene):
    SHOT = "EP10-S06"

    def construct(self):
        head = self.fit_left_of_tags(header("开源 FlashMLA 的手写 SASS 之差", "EP10 · S06 开源与内部对比"))
        self.add(head)

        txt_source = T("官方文档明确承认的架构差异", 22, MUTED).move_to([0, 1.4, 0])
        self.play(FadeIn(txt_source), run_time=0.6)

        self.until("sass")
        c1 = number_card("5%–10%", "慢 (解码内核)", "缺少内部手写 SASS 优化", color=WARN).move_to([-3.4, -0.4, 0])
        self.play(FadeIn(c1), run_time=0.8)

        self.until("decode")
        self.play(Indicate(c1), run_time=0.6)

        self.until("e2e")
        c2 = number_card("≤ 5%", "端到端差距", "通信与矩阵乘计算摊薄影响", color=KV).move_to([3.4, -0.4, 0])
        self.play(FadeIn(c2), Indicate(c2), run_time=0.8)

        self.finish()


class EP10_S07(DVScene):
    SHOT = "EP10-S07"

    def construct(self):
        head = self.fit_left_of_tags(header("批为什么破坏一致性：浮点加法非结合律", "EP10 · S07 浮点非结合律"))
        self.add(head)

        formula = T("(a + b) + c ≠ a + (b + c)", 32, FG).move_to([0, 1.3, 0])
        self.play(FadeIn(formula), run_time=0.6)

        self.until("math")
        sub_math = T("实数满足结合律 · 计算机有限精度浮点不满足结合律", 20, MUTED).move_to([0, 0.7, 0])
        self.play(FadeIn(sub_math), run_time=0.6)

        self.until("tree")
        # Tree A: (a+b)+c
        tree_a = Block("Batch = 1 归约树", DECODE, w=3.4, h=1.4, sub="先算 a + b -> 再加 c\n尾数舍入：...001", size=18).move_to([-3.4, -0.6, 0])
        # Tree B: a+(b+c)
        tree_b = Block("Batch = 64 归约树", WARN, w=3.4, h=1.4, sub="先算 b + c -> 再加 a\n尾数舍入：...010", size=18).move_to([3.4, -0.6, 0])
        self.play(FadeIn(tree_a), FadeIn(tree_b), run_time=0.8)

        self.until("reduce")
        diff_txt = T("1 ulp 微小舍入漂移 -> 改变 top-p 截断阈值 -> 词分叉", 20, WARN).move_to([0, -1.9, 0])
        self.play(FadeIn(diff_txt), Indicate(tree_b), run_time=0.8)

        self.finish()


class EP10_S08(DVScene):
    SHOT = "EP10-S08"

    def construct(self):
        head = self.fit_left_of_tags(header("批维度的外科手术：关闭 split-KV", "EP10 · S08 关 split-KV"))
        self.add(head)

        env_tag = Block("DEEPINFER_BATCH_INVARIANT = 1", DECODE, w=4.8, h=0.6, size=20).move_to([0, 1.4, 0])
        self.play(FadeIn(env_tag), run_time=0.6)

        self.until("env")
        b_split = Block("默认快路径：启用 split-KV", WARN, w=4.5, h=2.2, sub="候选长度 > 640 时切分 KV 范围\n多个线程块并行分块归约\n(归约顺序随批大小动态改变)", size=18).move_to([-3.4, -0.4, 0])
        self.play(FadeIn(b_split), run_time=0.8)

        self.until("split")
        self.play(Indicate(b_split), run_time=0.6)

        self.until("nosplit")
        b_nosplit = Block("批不变模式：关闭 split-KV", KV, w=4.5, h=2.2, sub="强制单个 CTA 独占\n按固定从前到后扫完全部 KV\n(归约树与批大小完全解耦)", size=18).move_to([3.4, -0.4, 0])
        self.play(FadeIn(b_nosplit), Indicate(b_nosplit), run_time=0.8)

        self.finish()


class EP10_S09(DVScene):
    SHOT = "EP10-S09"

    def construct(self):
        head = self.fit_left_of_tags(header("算子与通信双重封印：禁 split-K 与多次归约", "EP10 · S09 封印算子通信"))
        self.add(head)

        self.until("gemm")
        b_gemm = Block("DeepGEMM 封印：禁用 cuBLASLt 分派", DECODE, w=8.5, h=1.0, sub="绕过按输入动态选 tile 的 heuristic，走固定 JIT", size=19).move_to([0, 1.0, 0])
        self.play(FadeIn(b_gemm), run_time=0.8)

        self.until("gate")
        b_gate = Block("mega-gate 封印：split-K 强制锁死为 1", SWA, w=8.5, h=1.0, sub="禁止在特征 K 维度切分累加，杜绝并行求和舍入误差", size=19).move_to([0, -0.2, 0])
        self.play(FadeIn(b_gate), Indicate(b_gate), run_time=0.8)

        self.until("ep")
        b_ep = Block("DeepEP 封印：allow_multiple_reduction = False", EXPERT, w=8.5, h=1.0, sub="开 EPLB 重排时，禁止多路数据流无序累加到同一共享缓冲区", size=19).move_to([0, -1.4, 0])
        self.play(FadeIn(b_ep), Indicate(b_ep), run_time=0.8)

        self.finish()


class EP10_S10(DVScene):
    SHOT = "EP10-S10"

    def construct(self):
        head = self.fit_left_of_tags(header("采样器的批无关设计：一行一个 CTA 与定点 CDF", "EP10 · S10 采样批无关"))
        self.add(head)

        b_grid = Block("采样网格：每行一个独立 CTA", DECODE, w=4.5, h=2.2, sub="with T.Kernel(total_q, threads=256)\n归约树形状只与词表大小有关\n绝不随 Batch 变化改变形状", size=18).move_to([-3.4, -0.2, 0])
        self.play(FadeIn(b_grid), run_time=0.6)

        self.until("grid")
        self.play(Indicate(b_grid), run_time=0.6)

        self.until("vocab")
        txt_v = T("词表固定归约树 · 消除线程并发调度扰动", 20, MUTED).move_to([0, 1.5, 0])
        self.play(FadeIn(txt_v), run_time=0.6)

        self.until("fixed")
        b_fixed = Block("2^31 定点整数直方图找阈值", SWA, w=4.5, h=2.2, sub="概率 × 2^31 量化为 uint32\n基数直方图多轮原子累加\n整数加法天然满足结合律！", size=18).move_to([3.4, -0.2, 0])
        self.play(FadeIn(b_fixed), Indicate(b_fixed), run_time=0.8)

        self.finish()


class EP10_S11(DVScene):
    SHOT = "EP10-S11"

    def construct(self):
        head = self.fit_left_of_tags(header("确定性采样的绝对坐标：绑定 token 绝对位置", "EP10 · S11 绝对位置采样"))
        self.add(head)

        txt_seed = T("seq_seed (请求级 uint64) 决定随机流", 22, DECODE).move_to([0, 1.4, 0])
        self.play(FadeIn(txt_seed), run_time=0.6)

        self.until("rand")
        b_bad = Block("传统方式：按执行步数递增 (Step)", WARN, w=4.5, h=1.4, sub="抢占重算、分块 prefill\n步数对不上 -> 随机流错位！", size=18).move_to([-3.4, 0.1, 0])
        self.play(FadeIn(b_bad), run_time=0.8)

        self.until("step")
        self.play(Indicate(b_bad), run_time=0.6)

        self.until("pos")
        b_good = Block("DeepInfer：绑定绝对位置 seqlen_k", KV, w=4.5, h=1.4, sub="sample_positions = seqlen_k\n上下文绝对物理坐标\n重放/抢占永不漂移！", size=18).move_to([3.4, 0.1, 0])
        self.play(FadeIn(b_good), Indicate(b_good), run_time=0.8)

        self.until("exact")
        footer = T("无论第几步调度执行，同一上下文位置永远抽出相同随机数", 20, FG).move_to([0, -1.6, 0])
        self.play(FadeIn(footer), run_time=0.8)

        self.finish()


class EP10_S12(DVScene):
    SHOT = "EP10-S12"

    def construct(self):
        head = self.fit_left_of_tags(header("随机数的三条独立子流与 MTP 隔离", "EP10 · S12 独立子流"))
        self.add(head)

        pos_node = Block("绝对位置 p", FG, w=2.4, h=0.8, size=20).move_to([-4.2, 0.2, 0])
        self.play(FadeIn(pos_node), run_time=0.6)

        self.until("streams")
        s1 = Block("3p + 0 · 正式采样", DECODE, w=3.4, h=0.6, size=18).move_to([0, 1.1, 0])
        s2 = Block("3p + 1 · 拒绝重采样", WARN, w=3.4, h=0.6, size=18).move_to([0, 0.2, 0])
        s3 = Block("3p + 2 · 投机接受检验", KV, w=3.4, h=0.6, size=18).move_to([0, -0.7, 0])
        a1 = Arrow(pos_node.get_right(), s1.get_left(), color=DECODE, buff=0.1)
        a2 = Arrow(pos_node.get_right(), s2.get_left(), color=WARN, buff=0.1)
        a3 = Arrow(pos_node.get_right(), s3.get_left(), color=KV, buff=0.1)
        self.play(FadeIn(s1), FadeIn(s2), FadeIn(s3), Create(a1), Create(a2), Create(a3), run_time=1.0)

        self.until("sub")
        self.play(Indicate(s2), run_time=0.6)

        self.until("offset")
        mtp_offset = Block("MTP 草稿模型偏移\n+1,000,000,007", DRAFT, w=3.0, h=1.8, size=18).move_to([4.2, 0.2, 0])
        self.play(FadeIn(mtp_offset), Indicate(mtp_offset), run_time=0.8)

        self.finish()


class EP10_S13(DVScene):
    SHOT = "EP10-S13"

    def construct(self):
        head = self.fit_left_of_tags(header("变长 MTP 的致命权衡：全局排名击碎独立性", "EP10 · S13 变长 MTP 权衡"))
        self.add(head)

        b_drafts = Block("候选草稿池", FG, w=2.8, h=1.6, sub="每请求 5 个 draft\n全批扁平汇总", size=18).move_to([-4.0, 0.3, 0])
        self.play(FadeIn(b_drafts), run_time=0.6)

        self.until("mtp")
        b_rank = Block("全批置信度全局排序", EXPERT, w=3.2, h=1.6, sub="extra_budget = total_q - num_seqs\n全局 argsort 争夺预算", size=18).move_to([0, 0.3, 0])
        ar1 = arrow(b_drafts, b_rank, color=EXPERT)
        self.play(Create(ar1), FadeIn(b_rank), run_time=0.8)

        self.until("rank")
        self.play(Indicate(b_rank), run_time=0.6)

        self.until("depend")
        b_clash = Block("破坏同批独立性！", WARN, w=3.0, h=1.6, sub="单请求验证长度\n取决于批里邻居的置信度！", size=18).move_to([4.0, 0.3, 0])
        ar2 = arrow(b_rank, b_clash, color=WARN)
        self.play(Create(ar2), FadeIn(b_clash), Indicate(b_clash), run_time=0.8)

        self.until("fallback")
        footer = Block("确定性模式硬性要求：DEEPINFER_ENABLE_MTP_VARLEN = 0 (固定 5 槽位)", DECODE, w=8.5, h=0.6, size=18).move_to([0, -1.6, 0])
        self.play(FadeIn(footer), run_time=0.8)

        self.finish()


class EP10_S14(DVScene):
    SHOT = "EP10-S14"

    def construct(self):
        head = self.fit_left_of_tags(header("确定性采样的双硬件边界：端到端仅承诺 NVIDIA", "EP10 · S14 双硬件边界"))
        self.add(head)

        b_nv = Block("NVIDIA 平台", GPU, w=4.5, h=2.2, sub="1. 采样器绝对位置定序 [支持]\n2. 注意力/GEMM 批不变 [支持]\n端到端跨批确定性：官方严格承诺", size=18).move_to([-3.4, -0.2, 0])
        b_asc = Block("Huawei 昇腾平台", PREFILL, w=4.5, h=2.2, sub="1. 采样器绝对位置定序 [支持]\n2. 算子层批不变性     [未支持]\n开启直接触发断言报错！", size=18).move_to([3.4, -0.2, 0])
        self.play(FadeIn(b_nv), FadeIn(b_asc), run_time=0.8)

        self.until("compare")
        self.play(Indicate(b_nv), run_time=0.6)

        self.until("asc")
        self.play(Indicate(b_asc), run_time=0.6)

        self.until("assert")
        code = code_panel("if PLATFORM.is_npu:\n    assert not envs.DEEPINFER_BATCH_INVARIANT", "runtime_config.py:56", size=18).move_to([0, -1.8, 0])
        self.play(FadeIn(code), run_time=0.8)

        self.finish()


class EP10_S15(DVScene):
    SHOT = "EP10-S15"

    def construct(self):
        head = self.fit_left_of_tags(header("结构化输出真实血统：xgrammar 核心与异步编排", "EP10 · S15 结构化输出架构"))
        self.add(head)

        b_core = Block("上游 xgrammar 引擎", DECODE, w=4.0, h=1.0, sub="JSON / Regex / EBNF 语法自动机", size=20).move_to([0, 0.8, 0])
        self.play(FadeIn(b_core), run_time=0.6)

        self.until("so")
        self.play(Indicate(b_core), run_time=0.6)

        self.until("arch")
        b_outer = Block("DeepInfer 异步编排调度", FG, w=8.5, h=1.0, sub="独立 ThreadPoolExecutor 绑定空闲 CPU 核心", size=20).move_to([0, -0.5, 0])
        self.play(FadeIn(b_outer), run_time=0.8)

        self.until("pool")
        txt_pool = T("未编完暂挂 · pump 唤醒入队 · 避免主循环卡顿", 20, MUTED).move_to([0, -1.3, 0])
        self.play(FadeIn(txt_pool), run_time=0.6)

        self.until("doc")
        footer = T("开源版：服务进程内现编   vs   生产文档：独立 SO 机器集群预编译", 19, FG).move_to([0, -2.1, 0])
        self.play(FadeIn(footer), run_time=0.8)

        self.finish()


class EP10_S16(DVScene):
    SHOT = "EP10-S16"

    def construct(self):
        head = self.fit_left_of_tags(header("掩码流水线：CPU 预生成与 GPU 负无穷填充", "EP10 · S16 掩码流水线"))
        self.add(head)

        b_cpu = Block("CPU 锁页内存池", CPU, w=3.4, h=2.0, sub="129,280 / 32 = 4,040 字\n约 16 KB / 请求 / 步\npinned uint32 bitmask", size=18).move_to([-3.6, -0.2, 0])
        self.play(FadeIn(b_cpu), run_time=0.6)

        self.until("pipe")
        ar_stream = Arrow([-1.8, -0.2, 0], [1.8, -0.2, 0], color=DECODE, stroke_width=4)
        lbl_stream = T("专有流异步 H2D", 18, MUTED).next_to(ar_stream, UP, buff=0.1)
        self.play(Create(ar_stream), FadeIn(lbl_stream), run_time=0.8)

        self.until("mask")
        self.play(Indicate(b_cpu), run_time=0.6)

        self.until("gpu")
        b_gpu = Block("GPU 显存 logits", GPU, w=3.4, h=2.0, sub="TileLang 专用算子\n根据 bitmask 进行位与判断", size=18).move_to([3.6, -0.2, 0])
        self.play(FadeIn(b_gpu), run_time=0.8)

        self.until("inf")
        fill_txt = T("非法 token logits 原位填 -inf！", 20, WARN).move_to([0, -1.8, 0])
        self.play(FadeIn(fill_txt), Indicate(b_gpu), run_time=0.8)

        self.finish()


class EP10_S17(DVScene):
    SHOT = "EP10-S17"

    def construct(self):
        head = self.fit_left_of_tags(header("投机解码联动与 rollback 状态回退", "EP10 · S17 投机与回滚"))
        self.add(head)

        # 6 masks row
        mask_row = TokenRow(6, color=DECODE, size=0.4, gap=0.15, labels=["Main", "D1", "D2", "D3", "D4", "D5"]).move_to([0, 1.0, 0])
        self.play(FadeIn(mask_row), run_time=0.6)

        self.until("spec")
        txt_spec = T("当前步一次预生成 1 + 5 = 6 份语法掩码", 20, FG).move_to([0, 1.8, 0])
        self.play(FadeIn(txt_spec), run_time=0.6)

        self.until("reject")
        # D1, D2 accept (green), D3 reject (red cross)
        cross = T("✗ 拒绝！", 22, WARN).move_to([0.6, 0.2, 0])
        self.play(FadeIn(cross), run_time=0.6)

        self.until("rollback")
        rb_arrow = Arrow([0.6, -0.3, 0], [-1.0, -0.3, 0], color=WARN, stroke_width=4)
        rb_txt = T("matcher.rollback(2) 回滚自动机历史状态", 20, WARN).move_to([0, -0.8, 0])
        self.play(Create(rb_arrow), FadeIn(rb_txt), run_time=0.8)

        self.until("trigger")
        footer = Block("支持 trigger 触发词：自由思考结束后才启动语法约束", FG, w=7.5, h=0.6, size=18).move_to([0, -1.8, 0])
        self.play(FadeIn(footer), run_time=0.8)

        self.finish()


class EP10_S18(DVScene):
    SHOT = "EP10-S18"

    def construct(self):
        head = self.fit_left_of_tags(header("测试防线与评测真相：60 个浮点数与生产口径", "EP10 · S18 测试与评测"))
        self.add(head)

        b_tests = Block("四道回归测试防线", KV, w=4.5, h=2.4, sub="1. offline_decode_ppl (60 个 float 全等)\n2. test_kl (max_kl = 0.0 散度上界)\n3. test_batch_invariant (64 序列全等)\n4. test_sampler (KS 检验无偏采样)", size=17).move_to([-3.4, -0.3, 0])
        self.play(FadeIn(b_tests), run_time=0.8)

        self.until("gates")
        self.play(Indicate(b_tests), run_time=0.6)

        self.until("kl")
        txt_kl = T("散度上界 0.0 · 证明分块不改数学本质", 19, KV).move_to([-3.4, -1.8, 0])
        self.play(FadeIn(txt_kl), run_time=0.6)

        self.until("eval")
        b_eval = Block("官方公开评测 (非确定极速路径)", WARN, w=4.5, h=2.4, sub="AIME 2026: 99.9%  |  GPQA: 93.4%\n必须条件：\n• 开启变长 MTP (VARLEN=1)\n• 关闭批不变性 (BATCH_INVARIANT=0)", size=17).move_to([3.4, -0.3, 0])
        self.play(FadeIn(b_eval), Indicate(b_eval), run_time=0.8)

        self.until("end")
        footer = T("追求可复现性 vs 追求极限吞吐：走向不同的分支", 20, FG).move_to([0, 1.4, 0])
        self.play(FadeIn(footer), run_time=0.8)

        self.finish()
