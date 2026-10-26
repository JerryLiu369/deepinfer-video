#!/usr/bin/env python3
"""EP00: 导览与全局规模指标计算。
来源：F00-04 (155万亿 token/天, 38美元/卡·时), F00-12 (全系列集数与站点).
"""

SECONDS_PER_DAY = 86400
DAILY_TOKENS = 155e12
tokens_per_second = DAILY_TOKENS / SECONDS_PER_DAY
tokens_per_second_billion = tokens_per_second / 1e9

# 官方公布单卡每小时收入（谷时定价）
hourly_revenue_per_gpu = 38.0

# 全系列 14 集规划（大纲标准）
episodes_count = 14
ep00_target_minutes = 5.0
series_total_outline_minutes = 199.0

print(f"daily_tokens = {DAILY_TOKENS:.0e}")
print(f"tokens_per_second_billion = {tokens_per_second_billion:.3f}")
print(f"hourly_revenue_per_gpu = {hourly_revenue_per_gpu:.1f}")
print(f"episodes_count = {episodes_count}")
print(f"ep00_target_minutes = {ep00_target_minutes:.1f}")
print(f"series_total_outline_minutes = {series_total_outline_minutes:.1f}")
