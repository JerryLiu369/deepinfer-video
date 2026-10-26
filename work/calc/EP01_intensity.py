#!/usr/bin/env python3
"""EP01: 推理引擎算术强度与访存特征计算脚本（示意模型）。
来源：F01-02, F01-03, F01-10。
用于定量说明：为什么 Prefill 是计算受限（Compute-bound），而 Decode 是显存带宽受限（Memory-bandwidth bound），
以及为什么将 Decode Batch 从 1 提升至 64 能大幅降低每个 Token 的边际成本。
"""

# 示意模型参数设定（对齐 V4.1-Flash 典型激活规模）
ACTIVE_PARAMS = 16e9         # 激活参数量：160 亿 (16B)
BYTES_PER_PARAM = 1.0        # 参数存储精度：FP8 / MXFP8，每个参数 1 字节
MODEL_WEIGHT_BYTES = ACTIVE_PARAMS * BYTES_PER_PARAM  # 权重大小：16 GB (16e9 字节)
FLOPS_PER_PARAM_PER_TOKEN = 2.0  # 矩阵乘前向计算：每个参数每 token 对应 2 次浮点运算 (乘加)
FLOPS_PER_TOKEN = ACTIVE_PARAMS * FLOPS_PER_PARAM_PER_TOKEN  # 32 GFLOP (3.2e10 FLOP)

# 典型现代数据中心 GPU 示意参数（如 SM100 / 近代高端加速卡量级）
GPU_PEAK_TFLOPS = 1000.0     # 峰值算力：1000 TFLOPS (1e15 FLOPS)
GPU_HBM_BANDWIDTH_TBS = 3.2  # 显存带宽：3.2 TB/s (3.2e12 Byte/s)
ROOFLINE_TURNING_POINT = (GPU_PEAK_TFLOPS * 1e12) / (GPU_HBM_BANDWIDTH_TBS * 1e12)  # ~312.5 FLOP/Byte

# Decode 阶段不同 Batch Size 下的算术强度与时间分析
def calc_decode(batch_size: int, seq_len: int = 1024, kv_bytes_per_token: int = 890):
    flops = batch_size * FLOPS_PER_TOKEN
    weight_bytes = MODEL_WEIGHT_BYTES
    kv_bytes = batch_size * seq_len * kv_bytes_per_token
    total_bytes = weight_bytes + kv_bytes
    # 算术强度 (FLOP / Byte)
    intensity_weight_only = flops / weight_bytes
    intensity_total = flops / total_bytes
    
    # 理论时间估算（忽略 kernel 开销与通信的极限 Roofline 时间）
    time_compute_ms = (flops / (GPU_PEAK_TFLOPS * 1e12)) * 1000.0
    time_mem_ms = (total_bytes / (GPU_HBM_BANDWIDTH_TBS * 1e12)) * 1000.0
    time_step_ms = max(time_compute_ms, time_mem_ms)
    compute_utilization = (time_compute_ms / time_step_ms) * 100.0
    
    return {
        "batch_size": batch_size,
        "flops_gflop": flops / 1e9,
        "weight_gb": weight_bytes / 1e9,
        "kv_mb": kv_bytes / 1e6,
        "intensity_weight_only": intensity_weight_only,
        "intensity_total": intensity_total,
        "time_compute_ms": time_compute_ms,
        "time_mem_ms": time_mem_ms,
        "time_step_ms": time_step_ms,
        "compute_utilization": compute_utilization,
    }

# Prefill 阶段分析（单请求，不同 Prompt 长度）
def calc_prefill(prompt_tokens: int):
    flops = prompt_tokens * FLOPS_PER_TOKEN
    weight_bytes = MODEL_WEIGHT_BYTES
    intensity = flops / weight_bytes
    time_compute_ms = (flops / (GPU_PEAK_TFLOPS * 1e12)) * 1000.0
    time_mem_ms = (weight_bytes / (GPU_HBM_BANDWIDTH_TBS * 1e12)) * 1000.0
    time_step_ms = max(time_compute_ms, time_mem_ms)
    return {
        "prompt_tokens": prompt_tokens,
        "flops_tflop": flops / 1e12,
        "intensity": intensity,
        "time_compute_ms": time_compute_ms,
        "time_mem_ms": time_mem_ms,
        "time_step_ms": time_step_ms,
    }

if __name__ == "__main__":
    print("=== EP01 算术强度与瓶颈分析计算 ===")
    print(f"模型激活参数: {ACTIVE_PARAMS/1e9:.1f} B | 权重显存: {MODEL_WEIGHT_BYTES/1e9:.1f} GB (FP8)")
    print(f"GPU 假设峰值: {GPU_PEAK_TFLOPS:.0f} TFLOPS | 显存带宽: {GPU_HBM_BANDWIDTH_TBS:.1f} TB/s")
    print(f"Roofline 拐点算术强度: {ROOFLINE_TURNING_POINT:.1f} FLOP/Byte\n")

    print("--- [Decode 阶段] 随 Batch Size 变化 ---")
    batches = [1, 4, 16, 64, 128]
    for b in batches:
        res = calc_decode(b)
        print(f"Batch={b:3d}: 算力={res['flops_gflop']:7.1f} GFLOP | 权重强度={res['intensity_weight_only']:6.1f} FLOP/B | "
              f"算力耗时={res['time_compute_ms']:6.3f}ms | 访存耗时={res['time_mem_ms']:6.3f}ms | "
              f"计算利用率={res['compute_utilization']:5.1f}%")

    print("\n--- [Prefill 阶段] 随 Prompt 长度变化 ---")
    prompts = [512, 1024, 4096, 16384]
    for p in prompts:
        res = calc_prefill(p)
        print(f"Prompt={p:5d} tokens: 算力={res['flops_tflop']:6.2f} TFLOP | 强度={res['intensity']:7.1f} FLOP/B | "
              f"算力耗时={res['time_compute_ms']:6.3f}ms | 访存耗时={res['time_mem_ms']:6.3f}ms | 瓶颈={'Compute' if res['time_compute_ms'] > res['time_mem_ms'] else 'Memory'}")
