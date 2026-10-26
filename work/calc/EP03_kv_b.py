"""历史版本（独立核验 b）：数字已并入正式 EP03_kv_bytes.py / EP03_params.py / EP03_state_crossover.py，保留作对照。
EP03: 块状 KV 每输入 token 的字节数与每 128-token block 的字节数（独立核验 b）。

来源：
- F03-10 主 KV：FP4 E2M1 + E4M3 per-16 = 512/2 + 512/16 = 288 B/压缩 token
  （cache_common.py 的 V41_FP4_FORMAT、cache_engine.py 的 _kv_bytes_per_token）。
- F03-11 indexer K：MXFP4 E2M1 + UE8M0 per-32 = 128/2 + 128/32 = 68 B/压缩 token
  （cache_common.py 的 FP4_INDEX_KV_FORMAT、cache_engine.py 的 _get_qk_topk_bytes）。
- F03-04 源层：2/8/14 为 ratio 2；20 为 ratio 1（HF config.json 的 kv_source_layer_ids
  与 compress_ratios）。
无假设参数；全部是配置常量与算术。
"""
MAIN = 512 // 2 + 512 // 16          # 288
INDEX = 128 // 2 + 128 // 32         # 68
SWA = 512 + 512 // 32                # 528
PER_COMPRESSED = MAIN + INDEX        # 356

# 3 个 C2 源层按 2:1 摊半，1 个 C1 源层 1:1
main_per_token = 3 * MAIN / 2 + MAIN
index_per_token = 3 * INDEX / 2 + INDEX
per_token = main_per_token + index_per_token

# 一个 128-token block：C2 层 64 条，C1 层 128 条
block_bytes = 3 * (128 // 2) * PER_COMPRESSED + 128 * PER_COMPRESSED

print(f"kv_main_bytes_per_compressed_token = {MAIN}")
print(f"kv_index_bytes_per_compressed_token = {INDEX}")
print(f"kv_swa_bytes_per_token_per_layer = {SWA}")
print(f"kv_main_per_input_token = {main_per_token:g}")
print(f"kv_index_per_input_token = {index_per_token:g}")
print(f"kv_block_bytes_per_input_token = {per_token:g}")
print(f"kv_block_bytes_per_128_tokens = {block_bytes}")
print(f"kv_block_MiB_per_131072_tokens = {per_token * 131072 / 2**20:g}")
print(f"kv_block_MiB_per_1048576_tokens = {per_token * 1048576 / 2**20:g}")

# 反例：主 KV 退回 MXFP8（use_fp4_sparse_kv=False）
main8_per_token = 3 * SWA / 2 + SWA
print(f"kv_block_bytes_per_token_if_main_mxfp8 = {main8_per_token + index_per_token:g}")
print(f"kv_main_only_per_token_if_mxfp8 = {main8_per_token:g}")
