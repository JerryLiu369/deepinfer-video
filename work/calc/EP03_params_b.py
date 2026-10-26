"""历史版本（独立核验 b）：数字已并入正式 EP03_kv_bytes.py / EP03_params.py / EP03_state_crossover.py，保留作对照。
EP03: V4.1-Flash 参数量与每 token 激活参数量（独立核验 b）。

输入（B 级）：
- HF API `safetensors.total = 763,205,315,794`（48 个 shard，逻辑参数计数：
  FP4 路由专家以 I8 存储，每个 I8 元素计 2 个逻辑参数；*.scale 不计参数）。
- HF config.json 的维度：hidden 5120、40 层、384 路由专家/层、6 激活、1 共享专家、
  moe_intermediate 2304、64 Q 头、head_dim 512、q_lora 1280、o_groups 8、o_lora 1024、
  vocab 129280、Engram 两层的行数 384,006,168 / 384,016,682、行宽 256。
- HF 权重形状：每层共享专家 3×2304×5120；每个路由专家同宽；HC 两个 24×20480。

假设：把 Engram 表、MTP 草稿层、视觉塔、aligner 计入总参数；不计入任何 scale。
"""
TOTAL_HF = 763_205_315_794
LAYERS = 40
HIDDEN = 5120
EXPERTS = 384
TOPK = 6
MOE_INTER = 2304
VOCAB = 129280
ENGRAM_ROWS = (384_006_168, 384_016_682)
ENGRAM_ROW_DIM = 256
MTP_PARAMS = 14_225_362_530
VISION_PARAMS = 411_842_560
ALIGNER_PARAMS = 73_410_560
# 以下四项按 48 个 shard 的 tensor 形状分类求和（B 级权重元数据），
# 不是从 config 维度硬推；用于和总计对账。
ATTN_INCL_INDEXER = 5_126_564_864
SHARED_TOTAL = 1_415_577_600
GATE_HC_TOTAL = 78_673_920 + 39_323_760
EMBED_HEAD_TOTAL = 2 * VOCAB * HIDDEN

# 单层
attn = 1280 * 5120 + 32768 * 1280 + 512 * 5120 + 8192 * 4096 + 5120 * 8192 + 1280 + 512 + 64
gate = EXPERTS * HIDDEN + 2 * EXPERTS
one_expert = 3 * MOE_INTER * HIDDEN
shared = one_expert
hc = 2 * (24 * 20480 + 24 + 3)
norms = 2 * HIDDEN
per_layer_inactive = attn + gate + shared + hc + norms
per_layer_active = per_layer_inactive + TOPK * one_expert

# Engram：两层表 + 每层 wkv(25600×6144) 与 q/k(4×5120)
engram = sum(ENGRAM_ROWS) * ENGRAM_ROW_DIM + 2 * (25_600 * 6_144 + 2 * 4 * 5120)
routed = LAYERS * EXPERTS * one_expert
embed_head = 2 * VOCAB * HIDDEN

decode_active = LAYERS * per_layer_active + embed_head
prefill_active = (LAYERS // 2) * per_layer_active + VOCAB * HIDDEN
backbone = TOTAL_HF - engram - MTP_PARAMS - VISION_PARAMS - ALIGNER_PARAMS

print(f"params_total_hf = {TOTAL_HF}")
print(f"params_engram = {engram}")
print(f"params_engram_share = {engram / TOTAL_HF * 100:.2f}%")
print(f"params_routed_experts = {routed}")
print(f"params_routed_experts_share = {routed / TOTAL_HF * 100:.2f}%")
print(f"params_attn_incl_indexer = {ATTN_INCL_INDEXER}")
print(f"params_attn_incl_indexer_B = {ATTN_INCL_INDEXER / 1e9:.2f}")
print(f"params_shared_total_B = {SHARED_TOTAL / 1e9:.2f}")
print(f"params_embed_head_B = {EMBED_HEAD_TOTAL / 1e9:.2f}")
print(f"params_gate_hc_B = {GATE_HC_TOTAL / 1e9:.2f}")
print(f"params_vision_aligner_B = {(VISION_PARAMS + ALIGNER_PARAMS) / 1e9:.2f}")
print(f"params_component_sum = {routed + engram + MTP_PARAMS + ATTN_INCL_INDEXER + SHARED_TOTAL + EMBED_HEAD_TOTAL + VISION_PARAMS + ALIGNER_PARAMS + GATE_HC_TOTAL}")
print(f"params_backbone = {backbone}")
print(f"params_backbone_share = {backbone / TOTAL_HF * 100:.2f}%")
print(f"params_mtp = {MTP_PARAMS}")
print(f"params_vision_aligner = {VISION_PARAMS + ALIGNER_PARAMS}")
print(f"params_per_layer_inactive = {per_layer_inactive}")
print(f"params_per_layer_active = {per_layer_active}")
print(f"params_active_decode = {decode_active}")
print(f"params_active_decode_share = {decode_active / TOTAL_HF * 100:.2f}%")
print(f"params_active_prefill = {prefill_active}")
print(f"params_active_prefill_share = {prefill_active / TOTAL_HF * 100:.2f}%")
print(f"params_active_decode_B = {decode_active / 1e9:.2f}")
print(f"params_active_prefill_B = {prefill_active / 1e9:.2f}")
print(f"params_backbone_B = {backbone / 1e9:.2f}")
print(f"params_engram_B = {engram / 1e9:.2f}")
print(f"params_total_B = {TOTAL_HF / 1e9:.2f}")
