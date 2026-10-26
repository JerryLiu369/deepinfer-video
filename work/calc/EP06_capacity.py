#!/usr/bin/env python3
"""Calculate GPU KV block capacity and memory planning for EP06.

Verified against deepseek-ai/DeepInfer @ 9bd9cf2:
  - deepinfer/worker/base.py:217-246, 264-267
  - deepinfer/engine/llm_engine.py:441-451
"""
import math

def calculate_capacity():
    # Example hardware: SM100 with 192 GB or H100 with 80 GB
    total_gpu_memory = 80 * (1024**3)  # 80 GiB
    gpu_memory_utilization = 0.90
    peak_allocated_memory = 28 * (1024**3)  # 28 GiB weights + workspace

    avail = total_gpu_memory * gpu_memory_utilization - peak_allocated_memory

    # State slots for max_num_seqs = 256 -> 308 slots
    num_state_slots = int(256 * 1.2) + 1  # 308
    # Slot bytes per seq (approx 2.8 MB in inference layout)
    slot_bytes = 20 * 134 * 528 + 20 * 134 * 528 + 20 * 7 * 2 * (576 * 4)  # ~3.6 MB
    slot_bytes = ((slot_bytes + 1055) // 1056) * 1056

    state_size = num_state_slots * slot_bytes
    # Base.py lines 243: state_size *= 2 (state store & copy buffer)
    avail_kv = avail - 2 * state_size

    # Cache block size (e.g. 1152 B * num_layers_quantized)
    # 4 layers of block KV in V4.1: ~890 B/token * 128 = 113,920 B per block
    block_bytes = 113920
    num_gpu_blocks = int(avail_kv // block_bytes)
    # Rounded to even
    num_gpu_blocks = (num_gpu_blocks // 2) * 2

    # Launch check: max_model_len <= block_size * num_gpu_blocks * 0.8
    max_supported_len = int(128 * num_gpu_blocks * 0.8)

    print(f"Total GPU memory: {total_gpu_memory / (1024**3):.1f} GiB")
    print(f"Available for cache before state: {avail / (1024**3):.2f} GiB")
    print(f"2x State memory reserve: {(2 * state_size) / (1024**3):.2f} GiB")
    print(f"Available for paged KV blocks: {avail_kv / (1024**3):.2f} GiB")
    print(f"Number of GPU blocks: {num_gpu_blocks}")
    print(f"Max supported sequence length (80% rule): {max_supported_len} tokens")

    assert num_gpu_blocks > 0
    assert max_supported_len > 131072  # Supports 128k context

if __name__ == "__main__":
    calculate_capacity()
