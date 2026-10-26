#!/usr/bin/env python3
"""Calculate StateBlock memory layout and disk persistence bytes for EP06.

Verified against deepseek-ai/DeepInfer @ 9bd9cf2:
  - deepinfer/worker/cache_engine.py:88-110, 306
  - doc/inference_deployment_qa.md:169
"""

def calculate_state_disk():
    n_prefill_layers = 20
    window_size = 128
    max_backtracking_tokens = 6  # 5 + 1
    swa_bytes_per_token = 528

    # Inference ring size
    inference_ring = window_size + max_backtracking_tokens  # 134 tokens
    # Layer bytes (aligned to 32 B)
    layer_bytes = ((inference_ring * swa_bytes_per_token + 31) // 32) * 32
    assert layer_bytes == 134 * 528  # 70,752 is already divisible by 32

    # Total bytes per sequence saved to persistent storage
    state_size_to_disk = n_prefill_layers * layer_bytes
    print(f"Inference ring: {inference_ring} tokens (128 window + {max_backtracking_tokens} backtracking)")
    print(f"Per-layer SWA stored bytes: {layer_bytes} B")
    print(f"State size to disk: {n_prefill_layers} * {layer_bytes} = {state_size_to_disk} B ({state_size_to_disk / (1024*1024):.4f} MiB)")

    assert state_size_to_disk == 1415040

    # kvstore ring size when DEEPINFER_PREFILL_STORE_EXTRA_STATE=True
    prefill_store_extra_size = 128
    kvstore_ring = inference_ring + prefill_store_extra_size  # 262 tokens
    print(f"kvstore ring (extra state enabled): {kvstore_ring} tokens (134 + 128)")
    assert kvstore_ring == 262

    # Slots calculation for max_num_seqs = 256
    max_num_seqs = 256
    num_state_slots = int(max_num_seqs * 1.2) + 1  # 308 slots
    print(f"State slots for max_num_seqs={max_num_seqs}: {num_state_slots}")
    assert num_state_slots == 308

if __name__ == "__main__":
    calculate_state_disk()
