#!/usr/bin/env python3
"""Calculate GPU bubble elimination and EOS overhead under ZOS.

Reproducible derivation for EP05 facts F05-02, F05-08, F05-21.
"""
from __future__ import annotations


def calculate_zos_metrics():
    # 1. Typical Decode Step Latencies (single forward step under batch 64)
    t_forward = 4.0  # ms, main model forward (Blackwell / Ascend)
    t_sample = 0.6   # ms, sampler + MTP draft verify
    t_post = 0.8     # ms, CPU post-process (unembedding/token decode/MTP tracking)
    t_sched = 0.7    # ms, CPU scheduler.schedule() + input metadata prep

    t_gpu_active = t_forward + t_sample  # 4.6 ms
    t_cpu_total = t_post + t_sched       # 1.5 ms

    # Synchronous scheduling:
    # GPU runs forward + sample (4.6 ms), then CPU runs post + sched (1.5 ms) while GPU idles.
    t_sync_step = t_gpu_active + t_cpu_total  # 6.1 ms
    sync_bubble_ms = t_cpu_total               # 1.5 ms
    sync_bubble_pct = (sync_bubble_ms / t_sync_step) * 100.0  # 24.59%

    # ZOS (Zero-Overhead Scheduling):
    # Post-process(N-1) overlaps with Forward(N): max(0, t_post - t_forward) = max(0, 0.8 - 4.0) = 0 ms
    # Schedule(N+1) overlaps with Sample(N-1): max(0, t_sched - t_sample) = max(0, 0.7 - 0.6) = 0.1 ms residual
    # In practice with CUDA event queuing, schedule(N+1) is completely hidden.
    t_zos_step = t_gpu_active  # 4.6 ms
    zos_bubble_ms = 0.0
    zos_bubble_pct = 0.0
    throughput_gain_pct = ((t_sync_step - t_zos_step) / t_zos_step) * 100.0  # 32.61%
    latency_reduction_pct = ((t_sync_step - t_zos_step) / t_sync_step) * 100.0  # 24.59%

    # 2. EOS Extra Step Waste
    # Under ZOS, a sequence that finishes at step N runs an extra dummy forward at N+1.
    # Wasted forward steps per completed sequence = 1 step.
    lengths = [100, 250, 500, 1000]
    eos_waste = {L: (1.0 / L) * 100.0 for L in lengths}

    # 3. DP Voting Interval
    # decode_step % prefill_attempt_interval (70) == 0 (ALL)
    # decode_step % prefill_any_attempt_interval (100) == 0 (ANY)
    t_step_sec = t_zos_step / 1000.0
    time_70_steps_ms = 70 * t_zos_step
    time_100_steps_ms = 100 * t_zos_step

    print(f"--- 1. Synchronous vs ZOS Execution ---")
    print(f"GPU Active Time: {t_gpu_active:.2f} ms (Forward {t_forward} ms + Sample {t_sample} ms)")
    print(f"CPU Overhead:    {t_cpu_total:.2f} ms (Post {t_post} ms + Schedule {t_sched} ms)")
    print(f"Sync Step Time:  {t_sync_step:.2f} ms -> GPU Bubble: {sync_bubble_ms:.2f} ms ({sync_bubble_pct:.1f}%)")
    print(f"ZOS Step Time:   {t_zos_step:.2f} ms -> GPU Bubble: {zos_bubble_ms:.2f} ms ({zos_bubble_pct:.1f}%)")
    print(f"ZOS Throughput Boost: +{throughput_gain_pct:.1f}% (Step latency reduced by {latency_reduction_pct:.1f}%)")

    print(f"\n--- 2. EOS 1-Step Extra Forward Cost ---")
    for L, waste in eos_waste.items():
        print(f"Length {L:4d} tokens: 1 extra step = {waste:.2f}% wasted computation")

    print(f"\n--- 3. DP Prefill Attempt Intervals ---")
    print(f"Interval 70 (ALL):  {time_70_steps_ms:.1f} ms (~{time_70_steps_ms/1000.0:.2f} s)")
    print(f"Interval 100 (ANY): {time_100_steps_ms:.1f} ms (~{time_100_steps_ms/1000.0:.2f} s)")

    return {
        "sync_step_ms": t_sync_step,
        "zos_step_ms": t_zos_step,
        "sync_bubble_pct": sync_bubble_pct,
        "throughput_gain_pct": throughput_gain_pct,
        "eos_waste_500": eos_waste[500],
    }


if __name__ == "__main__":
    calculate_zos_metrics()
