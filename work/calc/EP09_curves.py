#!/usr/bin/env python3
"""EP09 calculation script: Speculative decoding verification length, acceptance rate, and throughput analysis.

Based on official DeepInfer benchmark data (doc/inference_deployment_qa.md:249-256)
and CUDA Graph bucket interval settings (deepinfer/environ.py:155).
"""

# Benchmark table: conc, fixed_v, dyn_v, fixed_a, dyn_a, fixed_tp, dyn_tp, gain_str
DATA = [
    (16, 5.0, 4.44, 3.32, 3.24, 4891, 4816, "-1.5%"),
    (32, 5.0, 3.65, 3.25, 3.17, 8964, 9111, "+1.6%"),
    (48, 5.0, 3.94, 3.30, 3.26, 12032, 12467, "+3.6%"),
    (60, 5.0, 3.58, 3.30, 3.21, 13730, 14466, "+5.4%"),
    (72, 5.0, 3.24, 3.29, 3.12, 14962, 15961, "+6.7%"),
    (96, 5.0, 3.24, 3.30, 3.15, 16817, 18660, "+11.0%"),
]

def analyze():
    print(f"{'Conc':>5} | {'V-Cut%':>7} | {'Tau-Ratio':>9} | {'Tokens(F->D)':>14} | {'BucketSpan':>10} | {'ReportedGain':>12}")
    print("-" * 70)
    for conc, f_v, d_v, f_a, d_a, f_tp, d_tp, gain in DATA:
        v_cut = (f_v - d_v) / f_v * 100.0
        tau_ratio = d_a / f_a
        tok_f = int(conc * f_v)
        tok_d = int(round(conc * d_v))
        # CUDAGRAPH_BATCH_SIZE_INTERVAL defaults to 8
        bucket_f = (tok_f + 7) // 8 * 8
        bucket_d = (tok_d + 7) // 8 * 8
        buckets_saved = (bucket_f - bucket_d) // 8
        print(f"{conc:5d} | {v_cut:6.1f}% | {tau_ratio:9.3f} | {tok_f:4d} -> {tok_d:4d} | {buckets_saved:10d} | {gain:>12}")

if __name__ == "__main__":
    analyze()
