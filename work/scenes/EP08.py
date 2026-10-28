"""EP08 scenes: 并行：注意力用 DP，专家用宽 EP (shots S01-S20)."""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_lib.dvlib import (
    BG, FG, MUTED, GRID, PREFILL, DECODE, KV, SWA, WARN, EXPERT, DRAFT, GPU, CPU,
    T, M, Pill, DVScene, header, MiniMap, Block, TokenRow, code_panel,
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
        head = self.fit_left_of_tags(header("Wide-EP 的吞吐悖论", "从 8 卡到 64 卡的物理收敛"))
        self.add(head)

        card_mem = number_card("7.43", "倍", "单卡 MoE 权重访存削减 (52 → 7 专家)", color=EXPERT).move_to([-3.4, -0.4, 0])
        card_perf = number_card("5%", "吞吐增益", "并发 256 收敛极限 (24,850 vs 26,100)", color=WARN).move_to([3.4, -0.4, 0])
        foot_note = T("条件: 64 卡 SM100 · 131K 上下文 · 固定 nextn=3 · 假定接受率折算系数 3.25", 16, MUTED).move_to([0, -2.4, 0])

        self.play(FadeIn(card_mem), run_time=1.0)
        self.until("pareto_curve")
        self.until("traffic_gap")
        self.play(FadeIn(card_perf), FadeIn(foot_note), run_time=1.0)
        self.until("concurrency_limit")
        self.finish()

class EP08_S02(_E08):
    SHOT = "EP08-S02"
    def construct(self):
        head = self.fit_left_of_tags(header("架构真相：没有张量并行", "model_parallel_size = context_parallel_size"))
        self.add(head)

        code = "model_parallel_size = context_parallel_size\n# 配置定义中完全没有 TP 维度"
        cp = code_panel(code, "deepinfer/config.py:165", highlight=[1], size=18, width=5.5).move_to([-3.3, -0.4, 0])

        b1 = Block("ReplicatedLinear", color=PREFILL, sub="全卡复制完整权重 · QKV 投影", w=5.6, h=1.4).move_to([3.3, 0.4, 0])
        b2 = Block("ParallelRoutedLinear", color=EXPERT, sub="专家维度切分 · 仅路由专家参数", w=5.6, h=1.4).move_to([3.3, -1.2, 0])

        self.play(FadeIn(cp), run_time=0.8)
        self.until("config_check")
        self.play(FadeIn(b1), FadeIn(b2), run_time=1.0)
        self.until("linear_split")
        self.until("why_no_tp")
        self.finish()

class EP08_S03(_E08):
    SHOT = "EP08-S03"
    def construct(self):
        head = self.fit_left_of_tags(header("正交解耦：DP 切请求，EP 切专家", "Attention 走纯 DP · MoE 走纯 EP"))
        self.add(head)

        b_attn = Block("Attention 计算层：纯数据并行 (DP)", color=DECODE, sub="各 rank 独立持有完整 KV 缓存 · 独立处理不同请求序列", w=11.2, h=1.4).move_to([0, 0.7, 0])
        b_moe = Block("MoE 前馈层：纯专家并行 (EP)", color=EXPERT, sub="专家参数切分到各卡 · 词元跨卡飞散交换 (DeepEP All-to-All)", w=11.2, h=1.4).move_to([0, -1.0, 0])
        foot_lbl = T("默认离线配置: data_parallel_size = expert_parallel_size // context_parallel_size", 16, MUTED).move_to([0, -2.4, 0])

        self.play(FadeIn(b_attn), run_time=0.8)
        self.until("rank_topology")
        self.play(FadeIn(b_moe), run_time=0.8)
        self.until("process_orthogonal")
        self.play(FadeIn(foot_lbl), run_time=0.6)
        self.until("dp_ep_equal")
        self.finish()

class EP08_S04(_E08):
    SHOT = "EP08-S04"
    def construct(self):
        head = self.fit_left_of_tags(header("异步批处理：绝不同步批大小", "各 rank 独立调度 · 自主匹配 CUDA Graph 桶"))
        self.add(head)

        gpu0 = Block("Rank 0", color=DECODE, sub="并发 8 · 桶 8", w=2.6, h=2.2).move_to([-4.5, -0.4, 0])
        gpu1 = Block("Rank 1", color=DECODE, sub="并发 16 · 桶 16", w=2.6, h=2.2).move_to([-1.5, -0.4, 0])
        gpu2 = Block("Rank 2", color=DECODE, sub="并发 24 · 桶 32", w=2.6, h=2.2).move_to([1.5, -0.4, 0])
        gpu3 = Block("Rank 3", color=DECODE, sub="并发 32 · 桶 32", w=2.6, h=2.2).move_to([4.5, -0.4, 0])
        foot_msg = T("机制: 消除跨卡批对齐空泡 · 各卡自主进入最优执行图", 18, MUTED).move_to([0, -2.4, 0])

        self.play(FadeIn(gpu0), FadeIn(gpu1), FadeIn(gpu2), FadeIn(gpu3), run_time=1.0)
        self.until("async_batch")
        self.until("bucket_select")
        self.play(FadeIn(foot_msg), run_time=0.6)
        self.until("decoupled_load")
        self.finish()

class EP08_S05(_E08):
    SHOT = "EP08-S05"
    def construct(self):
        head = self.fit_left_of_tags(header("步型决策：C++ 调度器 MIN 规约", "统一全组步调：这一步跑 Prompt 还是 Decode"))
        self.add(head)

        box_vote = Block("MIN all_reduce 统一决策", color=GPU, sub="_dp_allreduce(want ? 0 : 1, ReduceOp::MIN)", w=10.5, h=1.4).move_to([0, 0.6, 0])
        b_all = Block("ALL 点判定", color=DECODE, sub="常规步：全员就绪才切入预填 · 避免拖垮全组", w=5.2, h=1.4).move_to([-3.0, -1.0, 0])
        b_any = Block("ANY 点兜底", color=WARN, sub="超时步：任一卡需预填即强切 · 防止长等待", w=5.2, h=1.4).move_to([3.0, -1.0, 0])

        self.play(FadeIn(box_vote), run_time=0.8)
        self.until("step_vote")
        self.play(FadeIn(b_all), FadeIn(b_any), run_time=0.8)
        self.until("all_vs_any")
        self.until("min_reduce")
        self.finish()

class EP08_S06(_E08):
    SHOT = "EP08-S06"
    def construct(self):
        head = self.fit_left_of_tags(header("占位陪跑：无活 rank 的假请求", "维系 DeepEP 集合通信拓扑的必要代价"))
        self.add(head)

        b_busy = Block("Rank 0 (繁忙卡)", color=DECODE, sub="正常批次 32 请求 · 提交有效 token 计算", w=5.6, h=1.8).move_to([-3.2, 0.0, 0])
        b_idle = Block("Rank 1 (空闲卡)", color=MUTED, sub="构造 1-token placeholder · 输出直接丢弃", w=5.6, h=1.8).move_to([3.2, 0.0, 0])
        foot_banner = T("铁律: 集合通信要求所有 rank 同时同频进入核函数 · 缺席即死锁", 18, WARN).move_to([0, -2.3, 0])

        self.play(FadeIn(b_busy), FadeIn(b_idle), run_time=1.0)
        self.until("placeholder_token")
        self.until("why_placeholder")
        self.play(FadeIn(foot_banner), run_time=0.8)
        self.until("collective_sync")
        self.finish()

class EP08_S07(_E08):
    SHOT = "EP08-S07"
    def construct(self):
        head = self.fit_left_of_tags(header("防死锁守护：两轮投票与退出规约", "规避空 prompt 活锁 · MAX all_reduce 守护退出"))
        self.add(head)

        b_p1 = Block("防御一：第二轮 any_scheduled 投票", color=GPU, sub="若第一轮判预填但实际全卡无调度 · 全员回退解码 · 破除死循环", w=11.2, h=1.4).move_to([0, 0.6, 0])
        b_p2 = Block("防御二：全局退出 MAX all_reduce", color=GPU, sub="未完成请求状态统一规约 · 先做完的卡持续陪跑直至全组退出", w=11.2, h=1.4).move_to([0, -1.0, 0])

        self.play(FadeIn(b_p1), run_time=0.8)
        self.until("second_vote")
        self.play(FadeIn(b_p2), run_time=0.8)
        self.until("anti_livelock")
        self.until("max_exit")
        self.finish()

class EP08_S08(_E08):
    SHOT = "EP08-S08"
    def construct(self):
        head = self.fit_left_of_tags(header("MoE 六段前向流水 (Stage 1 Gate)", "本地 Gate 打分 · 双 FP32 偏置校准"))
        self.add(head)

        card_gate = Block("Stage 1: 本地 Gate 计算", color=EXPERT, sub="sqrtsoftplus 评分 · 文本与视觉双校准偏置 · 全卡复制权重零通信", w=11.2, h=1.8).move_to([0, 0.3, 0])
        card_pipe = Block("完整六段流水架构", color=MUTED, sub="Gate → Dispatch → Grouped GEMM → Shared → Combine → Wait", w=11.2, h=1.2).move_to([0, -1.3, 0])

        self.play(FadeIn(card_pipe), run_time=0.8)
        self.until("six_stages")
        self.play(FadeIn(card_gate), run_time=0.8)
        self.until("gate_scoring")
        self.until("local_weights")
        self.finish()

class EP08_S09(_E08):
    SHOT = "EP08-S09"
    def construct(self):
        head = self.fit_left_of_tags(header("DeepEP 变长分发 (Stage 2-3)", "do_expand 展开插槽 · defer_epilogue 流水重叠"))
        self.add(head)

        b_disp = Block("Stage 2: DeepEP Dispatch", color=GPU, sub="变长 All-to-All · do_expand 展开 · MK 对齐", w=5.6, h=2.0).move_to([-3.2, -0.4, 0])
        b_gemm = Block("Stage 3: Grouped GEMM", color=EXPERT, sub="前缀和直接切分边界 · 隐藏通信等待", w=5.6, h=2.0).move_to([3.2, -0.4, 0])

        self.play(FadeIn(b_disp), run_time=0.8)
        self.until("deepep_dispatch")
        self.until("expand_layout")
        self.play(FadeIn(b_gemm), run_time=0.8)
        self.until("defer_event")
        self.finish()

class EP08_S10(_E08):
    SHOT = "EP08-S10"
    def construct(self):
        head = self.fit_left_of_tags(header("隐式融合归约 (Stage 4-5)", "共享专家计算与 combine 通信重叠 · 偏置累加"))
        self.add(head)

        b_shared = Block("Stage 4: 共享专家前向", color=EXPERT, sub="limit_num_sms 扣减通信 SM · 计算与传输硬件并发", w=11.0, h=1.3).move_to([0, 0.5, 0])
        b_comb = Block("Stage 5: DeepEP Combine", color=GPU, sub="共享专家结果作为 bias 传入 epilogue · 零额外通信归约", w=11.0, h=1.3).move_to([0, -1.0, 0])

        self.play(FadeIn(b_shared), run_time=0.8)
        self.until("shared_forward")
        self.until("sm_limit")
        self.play(FadeIn(b_comb), run_time=0.8)
        self.until("implicit_fuse")
        self.finish()

class EP08_S11(_E08):
    SHOT = "EP08-S11"
    def construct(self):
        head = self.fit_left_of_tags(header("Mega MoE：NVLink 域单核融合", "Dispatch + GEMM + Combine 熔于一炉"))
        self.add(head)

        b_mega = Block("Mega MoE 单 Kernel 融合", color=EXPERT, sub="仅限 NVLink 物理域内 · 对称显存直通 · 消除逐层缓冲区发射开销", w=11.2, h=2.0).move_to([0, -0.3, 0])
        foot_nvl = T("适用范围: 72 卡 NVL 物理域内 · FP8/FP4 混合精度支持", 18, MUTED).move_to([0, -2.3, 0])

        self.play(FadeIn(b_mega), run_time=1.0)
        self.until("mega_moe")
        self.until("nvl_domain")
        self.play(FadeIn(foot_nvl), run_time=0.6)
        self.until("single_kernel")
        self.finish()

class EP08_S12(_E08):
    SHOT = "EP08-S12"
    def construct(self):
        head = self.fit_left_of_tags(header("长尾倾斜危机与专家对齐", "padding = -(num_routed + min_extra) % ep_size"))
        self.add(head)

        card_ep64 = Block("EP64 对齐: 448 专家", color=EXPERT, sub="384 逻辑 + 64 冗余 · 每卡 7 专家", w=5.6, h=2.0).move_to([-3.3, -0.4, 0])
        card_ep8 = Block("EP8 对齐: 416 专家", color=DECODE, sub="384 逻辑 + 32 冗余 · 每卡 52 专家", w=5.6, h=2.0).move_to([3.3, -0.4, 0])

        self.play(FadeIn(card_ep64), run_time=0.8)
        self.until("routing_skew")
        self.play(FadeIn(card_ep8), run_time=0.8)
        self.until("padding_formula")
        self.until("redundant_experts")
        self.finish()

class EP08_S13(_E08):
    SHOT = "EP08-S13"
    def construct(self):
        head = self.fit_left_of_tags(header("EPLB 第一级：热点专家贪心复制", "定长滑动窗口 · 最小化每副本峰值负载"))
        self.add(head)

        b_win = Block("通信核函数零开销累加", color=GPU, sub="cumulative_expert_count 每步写入定长滑动环形窗口", w=11.0, h=1.3).move_to([0, 0.5, 0])
        b_g1 = Block("贪心追加冗余物理专家", color=EXPERT, sub="逐层独立决策 · 每轮选使最大每副本负载最小的热点专家追加副本", w=11.0, h=1.4).move_to([0, -1.0, 0])

        self.play(FadeIn(b_win), run_time=0.8)
        self.until("sliding_window")
        self.play(FadeIn(b_g1), run_time=0.8)
        self.until("greedy_copy")
        self.until("min_peak_load")
        self.finish()

class EP08_S14(_E08):
    SHOT = "EP08-S14"
    def construct(self):
        head = self.fit_left_of_tags(header("EPLB 第二级：最慢卡负载和最小化", "优化目标：min Σ_step max_rank(load)"))
        self.add(head)

        b_vs_avg = Block("为什么拒绝简单平均值？", color=WARN, sub="各专家激活随时间互补波动 · 平均值无法消除瞬时单点打爆", w=5.6, h=2.0).move_to([-3.2, -0.4, 0])
        b_bin = Block("历史峰值之和最小化", color=EXPERT, sub="逐物理槽位确定性装箱 · 兼顾时序动态互补与确定性", w=5.6, h=2.0).move_to([3.2, -0.4, 0])

        self.play(FadeIn(b_vs_avg), run_time=0.8)
        self.until("second_binpack")
        self.until("why_not_average")
        self.play(FadeIn(b_bin), run_time=0.8)
        self.until("sum_max_rank")
        self.finish()

class EP08_S15(_E08):
    SHOT = "EP08-S15"
    def construct(self):
        head = self.fit_left_of_tags(header("symm_mem 直读：零拷贝权重重排", "同机显存直读 vs 跨机 NCCL 分桶 P2P"))
        self.add(head)

        b_symm = Block("同机 NVLink 物理域", color=EXPERT, sub="单层镜像逐层复用 · CUDA IPC 共享显存直读 · 无网络协议开销", w=5.6, h=2.0).move_to([-3.2, -0.4, 0])
        b_p2p = Block("跨机跨物理域退回", color=GPU, sub="NCCL batch_isend_irecv · 按 rank 差模分桶 · 防交换机拥塞", w=5.6, h=2.0).move_to([3.2, -0.4, 0])

        self.play(FadeIn(b_symm), run_time=0.8)
        self.until("symm_mem")
        self.until("mirror_buffer")
        self.play(FadeIn(b_p2p), run_time=0.8)
        self.until("p2p_fallback")
        self.finish()

class EP08_S16(_E08):
    SHOT = "EP08-S16"
    def construct(self):
        head = self.fit_left_of_tags(header("Prefill 与 Decode 参数差异", "为什么 Decode 重排周期长达万步？"))
        self.add(head)

        card_p = Block("Prefill 阶段配置", color=PREFILL, sub="4 冗余专家/卡 · 100 步窗口 · 1,000 步重排 · 实测失衡 1.074", w=5.6, h=2.0).move_to([-3.2, -0.4, 0])
        card_d = Block("Decode 阶段配置", color=DECODE, sub="1 冗余专家/卡 · 1,000 步窗口 · 10,000 步重排 · 实测失衡 1.090", w=5.6, h=2.0).move_to([3.2, -0.4, 0])

        self.play(FadeIn(card_p), run_time=0.8)
        self.until("prefill_params")
        self.play(FadeIn(card_d), run_time=0.8)
        self.until("decode_params")
        self.until("pause_overhead")
        self.finish()

class EP08_S17(_E08):
    SHOT = "EP08-S17"
    def construct(self):
        head = self.fit_left_of_tags(header("Mirror CP：因果注意力的几何平衡", "锯齿交错配对 2*cp 块 · 理论计算偏差严格为 0%"))
        self.add(head)

        card_diag = Block("Zigzag 对称配对映射", color=SWA, sub="序列划分 2*cp 块 · Rank r 分配第 r 块与第 (2cp - 1 - r) 块", w=10.8, h=1.3).move_to([0, 0.4, 0])
        card_res = number_card("0.00%", "工作量偏差", "两块因果 Key 长度之和在各卡严格恒定", color=SWA).move_to([0, -1.2, 0])

        self.play(FadeIn(card_diag), run_time=0.8)
        self.until("mirror_cp")
        self.until("zigzag_split")
        self.play(FadeIn(card_res), run_time=0.8)
        self.until("zero_skew")
        self.finish()

class EP08_S18(_E08):
    SHOT = "EP08-S18"
    def construct(self):
        head = self.fit_left_of_tags(header("生产抉择：为什么暂不启用 TP 与 CP", "官方部署问答：TP and CP are not used for now"))
        self.add(head)

        b_notp = Block("不启用 TP 的根本原因", color=WARN, sub="MLA 将 KV 压至低维潜变量 · 切分投影严重恶化算术强度与通信比", w=5.6, h=2.0).move_to([-3.2, -0.4, 0])
        b_nocp = Block("不启用 CP 的务实考量", color=MUTED, sub="常规序列纯 DP+EP 足矣 · CP 引入额外的输入重排与全收集显存缓冲", w=5.6, h=2.0).move_to([3.2, -0.4, 0])

        self.play(FadeIn(b_notp), run_time=0.8)
        self.until("prod_no_tp_cp")
        self.play(FadeIn(b_nocp), run_time=0.8)
        self.until("mla_efficiency")
        self.until("why_not_prod_cp")
        self.finish()

class EP08_S19(_E08):
    SHOT = "EP08-S19"
    def construct(self):
        head = self.fit_left_of_tags(header("Wide-EP 的真实物理定义", "以通信换带宽：买交互响应，而非峰值吞吐"))
        self.add(head)

        card_hbm = Block("低并发区：交互响应大幅领先", color=DECODE, sub="纯 HBM 访存受限区 · 权重访存骤降 7.4 倍 · 交互延迟改善 35%", w=5.6, h=2.0).move_to([-3.2, -0.4, 0])
        card_comm = Block("高并发区：通信主导差距收敛", color=WARN, sub="算术强度饱和 · 瓶颈转向 64 卡全交换通信耗时 · 增益仅剩 5%", w=5.6, h=2.0).move_to([3.2, -0.4, 0])

        self.play(FadeIn(card_hbm), run_time=0.8)
        self.until("hbm_traffic_cut")
        self.play(FadeIn(card_comm), run_time=0.8)
        self.until("all2all_bottleneck")
        self.until("concurrency_sweet_spot")
        self.finish()

class EP08_S20(_E08):
    SHOT = "EP08-S20"
    def construct(self):
        head = self.fit_left_of_tags(header("总结：解耦并行架构的生产哲学", "以正交设计铸就大规模稳定推理基石"))
        self.add(head)

        b_sum = Block("DeepInfer 解耦并行体系", color=EXPERT, sub="DP 切请求 · EP 切专家 · C++ 规约投票 · EPLB 显存直读 · 极致务实", w=11.2, h=1.5).move_to([0, 0.4, 0])
        b_next = Block("下集预告：EP09 投机解码 DSpark", color=DRAFT, sub="多预测标记 (MTP) · 块并行草稿 · 只验证值得验证的 token", w=11.2, h=1.3).move_to([0, -1.3, 0])

        self.play(FadeIn(b_sum), run_time=0.8)
        self.until("arch_recap")
        self.until("philosophy_tradeoff")
        self.play(FadeIn(b_next), run_time=0.8)
        self.until("next_preview")
        self.finish()
