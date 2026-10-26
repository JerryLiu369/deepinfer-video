"""EP07: '行·层' 示意账（F07-10）。

只数每层要做前向的 query 行数，用来说明"prefill 计算量约减半"的来源。
假设参数（示意）：输入长度 L。KEEP=140 来自 README（F07-05）；40 层、前 20 层为 encoder 来自 F07-01 / R02b。
不计第 20 层的全长 attn_norm 与 KV 投影（F07-08），也不区分各层每行的开销差异。
"""
L = 10_000          # 示意：输入 token 数
LAYERS, ENC, KEEP = 40, 20, 140

full = LAYERS * L
enc_rows = ENC * L
dec_rows = (LAYERS - ENC) * min(KEEP, L)
cut = enc_rows + dec_rows
print("note = 示意计算，行·层 ≠ FLOPs")
print(f"input_tokens = {L}")
print(f"rows_no_truncation = {full}")
print(f"rows_encoder = {enc_rows}")
print(f"rows_decoder_truncated = {dec_rows}")
print(f"rows_truncated_total = {cut}")
print(f"ratio = {cut / full:.3f}")
