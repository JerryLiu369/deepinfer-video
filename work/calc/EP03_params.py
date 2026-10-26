"""EP03: V4.1-Flash 参数量、主要分项与每 token 激活参数。

输入：
  B 级  HF API `safetensors.total = 763,205,315,794`（48 个 shard，逻辑参数计数：
        FP4 路由专家以 I8 存储，每个 I8 元素计 2 个逻辑参数；*.scale 不计参数）。
  B 级  HF config.json 的尺寸：hidden 5120、40 层、384 路由专家/层、6 激活、1 共享专家、
        moe_intermediate 2304、64 Q 头、head_dim 512、q_lora 1280、o_groups 8、o_lora 1024、
        vocab 129280、Engram 两层的行数 384,006,168 / 384,016,682、行宽 256。
  B 级  HF 权重形状（safetensors 头）：Engram embed [384006168,256] / [384016682,256] F8_E4M3；
        Engram q_weight / k_weight 各 [4,5120]，wkv [25600,6144]；
        mHC hc_attn_fn / hc_ffn_fn [24,20480] F32。

口径：
  * “参数”按逻辑参数计：FP4 专家权重以 I8 打包（2 值/字节），这里已按 2× 元素数还原。
  * 主要分项来自 48 个 shard 的 tensor 形状分类求和；与 HF total 差 430,080 个参数
    （0.00006%，未分类小张量），不是矛盾。
  * decode 激活 = 40 层全部 + 词嵌入 + 输出头；
  * prefill 激活 = 只算前 20 层（CED）+ 词嵌入，是 L >> nwin 的摊薄极限（E 级推断）。
  * 不计 Engram 查表命中、MTP 草稿前向与视觉塔。
"""
TOTAL_HF = 763_205_315_794
LAYERS = 40
HIDDEN = 5120
N_ROUTED = 384
N_ACT = 6
MOE_INTER = 2304
VOCAB = 129280
ENGRAM_ROWS = (384_006_168, 384_016_682)
ENGRAM_ROW_DIM = 256

# 主要分项：48 个 shard 的 tensor 形状分类求和（B 级）
ROUTED = LAYERS * N_ROUTED * 3 * MOE_INTER * HIDDEN
ENGRAM_TABLE = sum(ENGRAM_ROWS) * ENGRAM_ROW_DIM
ENGRAM_PROJ = 2 * (25_600 * 6_144 + 2 * 4 * HIDDEN)
ENGRAM = ENGRAM_TABLE + ENGRAM_PROJ
MTP = 14_225_362_530
ATTN_INCL_INDEXER = 5_126_564_864
SHARED = 1_415_577_600
EMBED_HEAD = 2 * VOCAB * HIDDEN
VISION_ALIGNER = 411_842_560 + 73_410_560
GATE_HC = 78_673_920 + 39_323_760

# 单层激活参数（decode）
attn = (
    1280 * HIDDEN
    + 32768 * 1280
    + 512 * HIDDEN
    + 8192 * 4096
    + HIDDEN * 8192
    + (1280 + 512 + HIDDEN + HIDDEN + 64)   # q_norm / kv_norm / 2×RMSNorm / attn_sink
)
gate = N_ROUTED * HIDDEN + 2 * N_ROUTED
one_expert = 3 * MOE_INTER * HIDDEN
shared = one_expert
hc = 2 * (24 * 20480 + 24 + 3)
per_layer_active = attn + gate + shared + N_ACT * one_expert + hc

decode_active = LAYERS * per_layer_active + EMBED_HEAD
prefill_active = (LAYERS // 2) * per_layer_active + VOCAB * HIDDEN
backbone = TOTAL_HF - ENGRAM - MTP - VISION_ALIGNER
component_sum = ROUTED + ENGRAM + MTP + ATTN_INCL_INDEXER + SHARED + EMBED_HEAD + VISION_ALIGNER + GATE_HC

print(f"params_total_hf = {TOTAL_HF}")
print(f"params_weight_storage_bytes = {510286023000}")
print(f"params_weight_storage_GB = {510286023000 / 1e9:.2f}")
print(f"params_total_B = {TOTAL_HF / 1e9:.2f}")
print(f"params_routed_experts = {ROUTED}")
print(f"params_routed_experts_B = {ROUTED / 1e9:.2f}")
print(f"params_engram = {ENGRAM}")
print(f"params_engram_B = {ENGRAM / 1e9:.2f}")
print(f"params_engram_table = {ENGRAM_TABLE}")
print(f"params_engram_table_B = {ENGRAM_TABLE / 1e9:.2f}")
print(f"params_engram_proj = {ENGRAM_PROJ}")
print(f"params_mtp = {MTP}")
print(f"params_mtp_B = {MTP / 1e9:.2f}")
print(f"params_attn_incl_indexer = {ATTN_INCL_INDEXER}")
print(f"params_attn_B = {ATTN_INCL_INDEXER / 1e9:.2f}")
print(f"params_shared_experts = {SHARED}")
print(f"params_shared_B = {SHARED / 1e9:.2f}")
print(f"params_embed_head = {EMBED_HEAD}")
print(f"params_embed_head_B = {EMBED_HEAD / 1e9:.2f}")
print(f"params_vision_aligner = {VISION_ALIGNER}")
print(f"params_vision_aligner_B = {VISION_ALIGNER / 1e9:.2f}")
print(f"params_gate_hc = {GATE_HC}")
print(f"params_gate_hc_B = {GATE_HC / 1e9:.2f}")
print(f"params_component_sum = {component_sum}")
print(f"params_component_sum_diff = {TOTAL_HF - component_sum}")
print(f"params_backbone = {backbone}")
print(f"params_backbone_B = {backbone / 1e9:.2f}")
print(f"params_engram_share_pct = {ENGRAM / TOTAL_HF * 100:.2f}")
print(f"params_hc_per_layer = {hc}")
print(f"params_per_layer_active = {per_layer_active}")
print(f"params_decode_active = {decode_active}")
print(f"params_decode_active_B = {decode_active / 1e9:.2f}")
print(f"params_decode_active_pct = {decode_active / TOTAL_HF * 100:.2f}")
print(f"params_prefill_active = {prefill_active}")
print(f"params_prefill_active_B = {prefill_active / 1e9:.2f}")
print(f"params_prefill_active_pct = {prefill_active / TOTAL_HF * 100:.2f}")
