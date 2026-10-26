#!/usr/bin/env python3
"""Calculate KV cache token bytes and block alignment values for EP06.

Verified against deepseek-ai/DeepInfer @ 9bd9cf2:
  - deepinfer/model_executor/layers/tilelang_ops/cache_common.py:99-155
  - deepinfer/worker/cache_engine.py:479-484
"""
import math

def calculate_bytes():
    # V4.1 parameters
    kv_lora_rank = 512
    qk_rope_head_dim = 64  # total 512 elements in latent
    # Main KV: 512 quantized elements
    # FP4: 512 elements / 2 = 256 bytes data + 512 / 16 (scale factor e4m3) = 32 bytes scale -> 288 bytes
    fp4_main_bytes = 512 // 2 + 512 // 16
    # MXFP8: 512 elements * 1 = 512 bytes data + 512 / 32 (scale factor ue8m0) = 16 bytes scale -> 528 bytes
    mxfp8_main_bytes = 512 * 1 + 512 // 32

    # Indexer K: 128 elements
    # FP4: 128 elements / 2 = 64 bytes data + 128 / 32 (ue8m0) = 4 bytes scale -> 68 bytes
    fp4_index_bytes = 128 // 2 + 128 // 32
    # MXFP8: 128 elements * 1 = 128 bytes data + 128 / 32 = 4 bytes scale -> 132 bytes
    mxfp8_index_bytes = 128 * 1 + 128 // 32

    # SWA: always MXFP8 (512 elements -> 528 bytes)
    swa_bytes = 528

    # Block alignment calculations
    align_to = 128
    lcm_fp4 = math.lcm(align_to, fp4_main_bytes)      # math.lcm(128, 288) = 1152
    lcm_mxfp8 = math.lcm(align_to, mxfp8_main_bytes)  # math.lcm(128, 528) = 4224
    lcm_state = math.lcm(32, swa_bytes)              # math.lcm(32, 528) = 1056

    print(f"FP4 Main KV: {fp4_main_bytes} B/token")
    print(f"MXFP8 Main KV: {mxfp8_main_bytes} B/token")
    print(f"FP4 Indexer K: {fp4_index_bytes} B/token")
    print(f"MXFP8 Indexer K: {mxfp8_index_bytes} B/token")
    print(f"SWA (fixed MXFP8): {swa_bytes} B/token")
    print(f"Block alignment (FP4): lcm(128, {fp4_main_bytes}) = {lcm_fp4} B")
    print(f"Block alignment (MXFP8): lcm(128, {mxfp8_main_bytes}) = {lcm_mxfp8} B")
    print(f"State slot alignment: lcm(32, {swa_bytes}) = {lcm_state} B")

    assert fp4_main_bytes == 288
    assert mxfp8_main_bytes == 528
    assert fp4_index_bytes == 68
    assert mxfp8_index_bytes == 132
    assert swa_bytes == 528
    assert lcm_fp4 == 1152
    assert lcm_mxfp8 == 4224
    assert lcm_state == 1056

if __name__ == "__main__":
    calculate_bytes()
