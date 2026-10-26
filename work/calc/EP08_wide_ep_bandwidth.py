"""EP08 Wide-EP 与 HBM 访存/吞吐收敛推导计算脚本。

基于官方 sweep 数据 (doc/images/wide_ep_decode_pareto.png, R16 #7, #8, #9, R08 #47)
与 doc/inference_deployment_qa.md:103。
"""

def calc_expert_counts():
    num_logical = 384
    
    # EP8 配置 (min_extra=32)
    ep8_size = 8
    ep8_min_extra = 32
    ep8_pad = -(num_logical + ep8_min_extra) % ep8_size
    ep8_total_physical = num_logical + ep8_min_extra + ep8_pad
    ep8_local = ep8_total_physical // ep8_size
    
    # EP64 配置 (min_extra=64, 即 1/GPU)
    ep64_size = 64
    ep64_min_extra = 64
    ep64_pad = -(num_logical + ep64_min_extra) % ep64_size
    ep64_total_physical = num_logical + ep64_min_extra + ep64_pad
    ep64_local = ep64_total_physical // ep64_size
    
    bandwidth_reduction_ratio = ep8_local / ep64_local
    
    return {
        "ep8_total_physical": ep8_total_physical,
        "ep8_local_experts": ep8_local,
        "ep64_total_physical": ep64_total_physical,
        "ep64_local_experts": ep64_local,
        "bandwidth_reduction_ratio": bandwidth_reduction_ratio,
    }

def calc_pareto_convergence():
    # 数据点: (batch, ep8_tok_s_user, ep8_tok_s_gpu, ep64_tok_s_user, ep64_tok_s_gpu)
    data = [
        (8, 243, 1700, 327, 2600),
        (16, 233, 3350, 319, 5050),
        (32, 222, 6900, 298, 9600),
        (64, 200, 12450, 248, 15800),
        (128, 150, 19100, 177, 22800),
        (256, 100, 24850, 103, 26100),
    ]
    
    rows = []
    for b, u8, g8, u64, g64 in data:
        tps_mult = g64 / g8
        user_mult = u64 / u8
        tps_gain = (g64 - g8) / g8 * 100.0
        rows.append({
            "batch": b,
            "ep8_user": u8,
            "ep8_gpu": g8,
            "ep64_user": u64,
            "ep64_gpu": g64,
            "tps_mult": tps_mult,
            "user_mult": user_mult,
            "tps_gain_pct": tps_gain,
        })
    return rows

if __name__ == "__main__":
    counts = calc_expert_counts()
    print("=== MoE 专家槽位与访存对比 ===")
    print(f"EP8:  总物理专家 {counts['ep8_total_physical']}, 每卡专家 {counts['ep8_local_experts']}")
    print(f"EP64: 总物理专家 {counts['ep64_total_physical']}, 每卡专家 {counts['ep64_local_experts']}")
    print(f"单卡本地权重访存理论削减比: {counts['bandwidth_reduction_ratio']:.2f}x (52 / 7 = {52/7:.3f})")
    
    print("\n=== Wide-EP 吞吐与交互性收敛表 ===")
    print("Batch | EP8 tok/s/GPU | EP64 tok/s/GPU | 吞吐倍数 (增益) | 每用户速度倍数")
    rows = calc_pareto_convergence()
    for r in rows:
        print(f"{r['batch']:5d} | {r['ep8_gpu']:13d} | {r['ep64_gpu']:14d} | {r['tps_mult']:.2f}x (+{r['tps_gain_pct']:.1f}%) | {r['user_mult']:.2f}x")
