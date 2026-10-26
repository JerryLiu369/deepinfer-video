"""历史版本（独立核验 b）：数字已并入正式 EP03_kv_bytes.py / EP03_params.py / EP03_state_crossover.py，保留作对照。
EP03: SWA state 槽的每序列字节数与"状态 vs 块状 KV"的交叉点（独立核验 b）。

来源：
- 窗口 128、回退 6、环 134：F03-15（cache_engine.py get_inference_swa_block_size、
  environ.py MAX_BACKTRACKING_TOKENS）。
- 每层每 token 528 B：F03-12（V41_FORMAT）。
- 43 个带 SWA 的 runtime attn 模块 = 40 主干 + 3 DFlash 草稿层；stored 只含
  layer 0-19 的 20 层（cache_engine.py:265-306）。
- 3 个 C2 层的压缩状态：7 个 token 的 [score|latent] fp32，每层 7×2×512×4。
- state 槽按 lcm(32,528)=1056 字节对齐：cache_engine.py:301-305。

无假设参数。所有数字来自默认配置；未计 num_state_slots 的 1.2 冗余。
"""
WINDOW = 128
BACKTRACK = 6
RING = WINDOW + BACKTRACK          # 134
SWA_BYTES = 528
MAIN_LAYERS = 40
DRAFT_LAYERS = 3
C2_LAYERS = 3
C2_RING = 2 + (BACKTRACK - 1)      # 7
COMPRESS_DIM = 512
FP32 = 4
ALIGN = 1056                       # lcm(32, 528)

per_layer = RING * SWA_BYTES       # 70,752
swa_main = MAIN_LAYERS * per_layer
swa_all = (MAIN_LAYERS + DRAFT_LAYERS) * per_layer
compress = C2_LAYERS * C2_RING * 2 * COMPRESS_DIM * FP32
total = swa_all + compress
aligned = (total + ALIGN - 1) // ALIGN * ALIGN
disk = 20 * per_layer
per_token = 890

print(f"state_swa_ring_tokens = {RING}")
print(f"state_swa_bytes_per_layer = {per_layer}")
print(f"state_swa_main_40_layers = {swa_main}")
print(f"state_swa_all_43_layers = {swa_all}")
print(f"state_compress_bytes = {compress}")
print(f"state_slot_bytes_unaligned = {total}")
print(f"state_slot_bytes = {aligned}")
print(f"state_slot_MiB = {aligned / 2**20:.3f}")
print(f"state_main_40_layers_MiB = {swa_main / 2**20:.3f}")
print(f"state_size_to_disk = {disk}")
print(f"state_size_to_disk_MiB = {disk / 2**20:.3f}")
print(f"crossover_all_state_tokens = {aligned / per_token:.1f}")
print(f"crossover_main_40_layers_tokens = {swa_main / per_token:.1f}")
print(f"crossover_40_layers_plus_compress_tokens = {(swa_main + compress) / per_token:.1f}")
