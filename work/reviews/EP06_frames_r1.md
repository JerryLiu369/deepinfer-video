# EP06 屏幕技术审校记录（第 1 轮）

- 审校人：tech-reviewer
- 审校时间：2026-10-26
- 审校对象：`work/build/EP06/keyframes/` 85 张关键帧及屏幕呈现内容
- 依据标准：`work/facts/EP06.yaml`、`docs/06_FACT_PROTOCOL.md`、`docs/10_REVIEW_CHECKLISTS.md`

## 1. 逐镜头屏幕文字与技术事实核对表

| 镜头号 | 查验的关键帧 | 屏幕技术陈述与数字 | 事实账本依据 (ID) | 技术准确性核对 | 结论 |
| --- | --- | --- | --- | --- | --- |
| S01 | cue-curve_show, cue-state_flat, cue-split_mind | 块状 KV 随长度线性膨胀 (0-80GB) / 状态缓存首字定长 3.6MB / 双轨制 | F06-02, F06-08 | 显存双轨制宏观对比准确，数字条件与单位符合账本 | **准确** |
| S02 | mid, cue-card | EP06 · 显存架构 / 两种记忆 · 两种管法 / MiniMap 4 (KV 存储) | G-01 | 全系列路线图站点映射准确 | **准确** |
| S03 | cue-arch_split, cue-lifecycle_diff, cue-two_managers | 40层结构 / 4层全局保留 (2,8,14,20) / 36层滑窗只留128 / BlockManager vs StateManager | F06-02, F06-07, F06-08 | V4.1 模型结构与双管理器分工与源码完全一致 | **准确** |
| S04 | cue-paged_concept, cue-alloc_new_block, cue-zero_frag | 块容量 128 token / 按需弹出物理块 / 块表映射 / 零外部碎片 / Block 0 保留禁用 | F06-02, F06-06 | 源码 block_manager.cpp 与 128 token 分页机制一致 | **准确** |
| S05 | mid, cue-q_block_layout | 一个物理块长什么样 / 独立张量还是扁平字节切片 / uint8 连续字节带 | F06-04 | 物理块底层剖面提问准确，预告扁平 uint8 结构 | **准确** |
| S06 | cue-byte_calc, cue-mxfp8_calc | FP4 288B (256B+32B) / MXFP8 528B (512B+16B) / 索引K 68B / SWA 528B | F06-04 | 计算脚本 calc/EP06_bytes.py 精确闭环，数字 100% 吻合 | **准确** |
| S07 | cue-flat_byte_tape, cue-block_lcm | 扁平 uint8 切片 / 32B 硬件对齐 / lcm(128, 288)=1152 字节 / C2 层 64 token | F06-02, F06-03 | 源码 kv_cache.py 与算子硬件对齐步长一致 | **准确** |
| S08 | cue-slot_formula, cue-unified_path | slot = block_id * tokens_per_block + offset / -1 跳过写入 / 统一寻址 | F06-05 | TileLang 算子内核代码寻址公式与边界处理真实 | **准确** |
| S09 | mid, cue-q_state_layout | 状态缓存为什么定长 / 前存后丢哲学 / 低地址持久化与高地址截断 | F06-08 | 状态槽位结构提问精准，符合 StateBlock 特征 | **准确** |
| S10 | cue-state_anatomy, cue-store_drop_split, cue-prefix_truncate | 低地址存储区前20层SWA环 / 高地址丢弃区后20层+压缩边界 / 前缀截断零拷贝 | F06-08, F06-13 | 源码 state_block.py 分区设计与前缀截断机制一致 | **准确** |
| S11 | cue-ring_134, cue-why_134, cue-backtrack_role | 134 = 128滑窗 + 6回退预算 (5+1) / 容忍投机回退 / 吸收异步落盘滞后 | F06-09 | 源码 rolling_buffer.hpp:42 回退预算推导一致 | **准确** |
| S12 | cue-kvstore_262, cue-default_zero_copy | 262环 (134+128余量) 重排 / 默认134环单次 memcpy 零重排连续切片直发 | F06-10 | 源码 kvstore_state.cpp 存储模式与默认行为核对吻合 | **准确** |
| S13 | cue-disk_size_calc, cue-fixed_1_35mb | 20层 × 134 token × 528B = 1,415,040 字节 (1.35 MiB) / 128 整数倍边界 | F06-11, F06-12 | 计算脚本 calc/EP06_state_disk.py 验证完全一致 | **准确** |
| S14 | mid, cue-q_three_128 | 为什么代码里到处是 128 / 块大小、步长与对齐是同一回事吗 | F06-01 | 抓住源码深层概念混淆点，设问精准 | **准确** |
| S15 | cue-aha_three_128, cue-card_container, cue-card_grain, cue-card_align | ①逻辑容器 128 tok / ②调度步长 128 tok / ③硬件物理 128 字节对齐 | F06-01, F06-03 | 彻底剥离三个“128”核心认知，概念解耦无懈可击 | **准确** |
| S16 | cue-mem_plan_flow, cue-deduct_2x_state, cue-launch_check_80 | 90% 水位扣峰值 / 显式扣除 2×StateBuffer / 物理块数 / 80% 单请求硬校验 | F06-13, F06-14, F06-15 | 源码 engine_config.py 规划公式与准入断言一致 | **准确** |
| S17 | cue-prefix_truth, cue-fifo_only, cue-overwrite_risk | 开源版零自动前缀树 / C++ FIFO 链表与计数 / 释放即归还直接覆盖 | F06-06, F06-16 | 源码 block_manager.hpp:88 证实无 Radix Tree 与哈希表 | **准确** |
| S18 | cue-fork_seq_anim, cue-cow_action | 显式 fork_seq / pin 块表 (ref_count 1→2) / 写时复制克隆末尾未满块 | F06-17 | 源码 scheduler.cpp:fork_seq 与 COW 逻辑一致 | **准确** |
| S19 | cue-three_tier_storage, cue-route_compare | L1 GPU HBM / L2 主机 1.4MB SWA / L3 3FS 100+PB / 网关前置匹配与外部注入 | F06-18, F06-19, F06-20 | 官方部署架构文档与主流引擎对比准确无误 | **准确** |
| S20 | mid, cue-recap_cards, cue-next_hook | 全集三大认知总结 / 下集预告：EP07 SWA 有界重放突破 | F06-01, F06-08, F06-11, F06-16 | 总结凝练，下集衔接严密，无过度前置剧透 | **准确** |

## 2. 审查项合规清单

- [x] **屏幕文字与脚本 100% 对应**：所有屏幕文字严格来自 `work/scripts/EP06.md`，无私自篡改或未经验证的技术断言。
- [x] **开源范围与角标完全匹配**：S01–S18 均标注 `oss`（代码证实），S19 标注 `mixed` 并明确区分代码有无，角标体系严密。
- [x] **所有数字具备明确边界条件**：
  - 主 KV 尺寸：明确区分 FP4（288B）与 MXFP8（528B）。
  - 落盘数据量：明确限定为前 20 层、134 滚动环长、528 字节单 token 状态。
  - 显存准入：明确标注 90% 显存利用率上限、2 倍 StateBuffer 预留、80% 单请求硬上限。
- [x] **代码路径无笔误**：`deepinfer/worker/kv_cache.py`、`csrc/engine/block_manager.cpp`、`engine_config.py` 与源码仓库严格吻合。

## 3. 结论

**审校结论：放行（PASS）**。屏幕技术呈现零硬伤，数据推演严格闭环，批准进入成片制作。
