"""EP03: 每序列 SWA 状态缓存（state slot）的字节数，以及“状态缓存 vs 块状 KV”的交叉点。

输入（A 级）：
  F03-15  cache_engine.py:88-93 的 get_inference_swa_block_size
            = window 128 + MAX_BACKTRACKING_TOKENS 6 = 134
            environ.py:129-132：MAX_BACKTRACKING = max(设定值, USE_NEXTN_DECODE+1)，
            USE_NEXTN_DECODE 默认 5 -> 6。
  F03-16  cache_engine.py:260-306 的 StateBlock 布局：
            swa_num_layer = 40 个主干层 + 3 个 DFlash 草稿层 = 43
              （config.py:146-155 把 3 个 _dflash_spec 加进 attn_module_list；
                _dflash_spec 的 sink_mode="swa"，config.py:136-143；
                _has_SWA 见 cache_engine.py:683-687）
            swa_store_num_layer = 20（layer 0-19，_is_dropped_swa_layer，cache_engine.py:113-116）
            C2 压缩状态：3 层（2/8/14）× ring 7 × 2 通道 × 512 维 × fp32
              ring = ratio + (MAX_BACKTRACKING - 1) = 2 + 5 = 7（cache_engine.py:131-133）
            槽长按 lcm(32, 528) = 1056 对齐（cache_engine.py:301-305）
  F03-12  V41_FORMAT = 528 B/token/层
  F03-13  块状 KV = 890 B/输入 token
  F03-14  块状 KV 以 128-token block 为单位分配，每 block 113,920 B

无假设参数；交叉点是纯算术（E 级），并给出 block 粒度下的量化版本。
"""
SWA_BYTES_PER_TOKEN = 512 + 512 // 32        # 528
WINDOW = 128
BACKTRACK = max(5 + 1, 6)                    # USE_NEXTN_DECODE 默认 5 -> 6
RING = WINDOW + BACKTRACK                    # 134
N_MAIN_LAYERS = 40
N_DRAFT_LAYERS = 3
STORE_LAYER = 20                             # n_prefill_layer = 20
RATIO = 2
COMPRESS_RING = RATIO + (BACKTRACK - 1)      # 7
COMPRESS_LAYERS = 3                          # layer 2/8/14
DIM = 512

swa_per_layer = RING * SWA_BYTES_PER_TOKEN   # 70,752
swa_main = N_MAIN_LAYERS * swa_per_layer
swa_all = (N_MAIN_LAYERS + N_DRAFT_LAYERS) * swa_per_layer
compress_state = COMPRESS_LAYERS * COMPRESS_RING * 2 * DIM * 4
raw_total = swa_all + compress_state
align = 1056                                 # lcm(32, 528)
aligned_total = (raw_total + align - 1) // align * align
stored = STORE_LAYER * swa_per_layer

print(f"swa_ring_positions_per_seq = {RING}")
print(f"swa_state_per_layer_bytes = {swa_per_layer}")
print(f"swa_state_main_40_layers_bytes = {swa_main}")
print(f"swa_state_all_43_layers_bytes = {swa_all}")
print(f"c2_compress_state_bytes = {compress_state}")
print(f"state_raw_bytes_per_seq = {raw_total}")
print(f"state_slot_bytes_per_seq = {aligned_total}")
print(f"state_slot_MiB_per_seq = {aligned_total / 2**20:.3f}")
print(f"state_slot_MB_per_seq = {aligned_total / 1e6:.3f}")
print(f"state_main_40_layers_MiB = {swa_main / 2**20:.3f}")
print(f"state_to_disk_bytes_per_seq = {stored}")
print(f"state_to_disk_MiB_per_seq = {stored / 2**20:.3f}")

BLOCK_KV_PER_TOKEN = 890
BLOCK_BYTES = 113920

print(f"block_kv_bytes_per_input_token = {BLOCK_KV_PER_TOKEN}")
print(f"crossover_tokens_continuous = {aligned_total / BLOCK_KV_PER_TOKEN:.2f}")
print(f"crossover_tokens_main_40_layers = {swa_main / BLOCK_KV_PER_TOKEN:.2f}")
print(f"crossover_tokens_partial_40_plus_compress = {(swa_main + compress_state) / BLOCK_KV_PER_TOKEN:.2f}")
partial_aligned = (swa_main + compress_state + 1055) // 1056 * 1056
print(f"crossover_tokens_partial_aligned = {partial_aligned / BLOCK_KV_PER_TOKEN:.2f}")
blocks = -(-aligned_total // BLOCK_BYTES)          # ceil
print(f"crossover_blocks = {blocks}")
print(f"crossover_tokens_block_granular = {blocks * 128}")
print(f"block_kv_MiB_at_1048576_tokens = {BLOCK_KV_PER_TOKEN * 1048576 / 2**20:g}")
print(f"block_kv_over_state_ratio_at_1M = {BLOCK_KV_PER_TOKEN * 1048576 / aligned_total:.1f}")
