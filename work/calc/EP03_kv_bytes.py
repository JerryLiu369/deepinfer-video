"""EP03: 块状 KV 每输入 token 的字节数、每 128-token block 的字节数。

输入（A 级）：
  F03-12  V41_FP4_FORMAT     = e2m1 ×512, e4m3 scale per-16 -> 512*4/8 + 512/16 = 288 B
          FP4_INDEX_KV_FORMAT = e2m1 ×128, ue8m0 scale per-32 -> 128*4/8 + 128/32 = 68 B
          V41_FORMAT          = e4m3 ×512, ue8m0 scale per-32 -> 512 + 512/32 = 528 B
          源文件 deepinfer/model_executor/layers/tilelang_ops/cache_common.py:109-137
  F03-06  KV 源层只有 2/8/14（ratio 2）与 20（ratio 1）；
          源文件 config.json 的 compress_ratios / kv_source_layer_ids
  F03-14  block_size = 128 个“压缩前 token”（model_metadata_utils.py:133-140）

无假设参数。890 与官方技术报告摘要的 890 bytes per token 独立吻合（F03-13）。
"""
MAIN_BYTES = 512 * 4 // 8 + 512 // 16      # 288
INDEX_BYTES = 128 * 4 // 8 + 128 // 32     # 68
SWA_BYTES = 512 + 512 // 32                # 528

KV_SOURCE_LAYERS = {2: 2, 8: 2, 14: 2, 20: 1}   # layer -> compress ratio
BLOCK_TOKENS = 128

main_per_token = sum(MAIN_BYTES / r for r in KV_SOURCE_LAYERS.values())
index_per_token = sum(INDEX_BYTES / r for r in KV_SOURCE_LAYERS.values())
per_token = main_per_token + index_per_token

print(f"main_kv_bytes_per_compressed_token = {MAIN_BYTES}")
print(f"index_k_bytes_per_compressed_token = {INDEX_BYTES}")
print(f"swa_kv_bytes_per_token_per_layer = {SWA_BYTES}")
print(f"kv_source_layers = {sorted(KV_SOURCE_LAYERS)}")
print(f"main_share_bytes_per_input_token = {main_per_token:g}")
print(f"index_share_bytes_per_input_token = {index_per_token:g}")
print(f"c2_source_layer_bytes_per_input_token = {(MAIN_BYTES + INDEX_BYTES) / 2:g}")
print(f"c1_source_layer_bytes_per_input_token = {MAIN_BYTES + INDEX_BYTES}")
print(f"block_kv_bytes_per_input_token = {per_token:g}")
print(f"block_bytes_layer2_8_14 = {64 * (MAIN_BYTES + INDEX_BYTES)}")
print(f"block_bytes_layer20 = {128 * (MAIN_BYTES + INDEX_BYTES)}")
print(f"block_kv_bytes_per_128_token_block = {int(per_token * BLOCK_TOKENS)}")
print(f"block_kv_MiB_per_131072_tokens = {per_token * 131072 / 2**20:g}")
print(f"block_kv_MiB_per_1048576_tokens = {per_token * 1048576 / 2**20:g}")

# 反证：若把 24/28/32/36 的 indexer 也算成独立 index-K 副本，总量对不上 890
index_if_8_copies = 3 * INDEX_BYTES / 2 + 5 * INDEX_BYTES
print(f"counterfactual_index_8_copies_bytes_per_input_token = {index_if_8_copies:g}")
print(f"counterfactual_total_if_8_index_copies = {main_per_token + index_if_8_copies:g}")
