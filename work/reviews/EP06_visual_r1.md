# EP06 美术审片记录（第 1 轮）

- 审校者：art-director
- 审校时间：2026-10-26
- 审校对象：`work/build/EP06/keyframes/`（共 85 张关键帧，8 张拼图）与各镜头渲染结果
- 依据标准：`docs/04_VISUAL_LANGUAGE.md`（视觉词典）、`docs/10_REVIEW_CHECKLISTS.md` 第 5 节（关键帧与成片清单）

## 1. 逐镜头审查表

| 镜头号 | 查验的关键帧 | layout WARN | 字号/重叠/出画 | 颜色语义 | 舞台利用与排版 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | cue-curve_show, cue-state_flat, cue-split_mind, end | 0 | 字号 $\ge 18$pt，坐标轴边界清晰 | DECODE蓝(KV)/SWA紫(状态)/WARN橙(暴涨) | 左右双栏对比鲜明，底部双轨制卡片对称平稳 | **通过** |
| S02 | mid, cue-card, end | 0 | 标题 44pt，副标题 30pt | DECODE绿/蓝，MiniMap 亮第 4 站“KV 存储” | 极简居中，符合系列标准片头规范 | **通过** |
| S03 | cue-arch_split, cue-lifecycle_diff, cue-two_managers, end | 0 | 字号 $\ge 18$pt，LayerStack 边距充足 | KV绿/SWA紫/EXPERT金 | 40层立面与右侧双管理器卡片呼吸联动 | **通过** |
| S04 | cue-paged_concept, cue-alloc_new_block, cue-zero_frag, end | 0 | 字号 $\ge 18$pt，块池排布均匀 | DECODE蓝/GPU绿/WARN橙 | 逻辑请求与物理块池映射生动，斜杠禁用醒目 | **通过** |
| S05 | mid, cue-q_block_layout, end | 0 | 提问卡字号 32/22pt，居中舒适 | DECODE蓝/GRID灰 | 居中好奇徽章与卡片层次分明，引出物理块结构 | **通过** |
| S06 | cue-byte_calc, cue-mxfp8_calc, end | 0 | 算式字号 18pt，底部注脚 16pt | DECODE蓝/KV绿/SWA紫 | 精确字节账本三段式平铺，算式清晰可读 | **通过** |
| S07 | cue-flat_byte_tape, cue-block_lcm, end | 0 | 1D带状切片紧凑无穿插 | SWA紫/DECODE蓝/EXPERT金 | uint8 扁平连续带扫过，32B与1152B标尺明确 | **通过** |
| S08 | cue-slot_formula, cue-unified_path, end | 0 | 公式 22pt，副标题 18pt | DECODE蓝/PREFILL橙/GPU绿 | TileLang 公式居中，Prefill 与 Decode 统一收拢 | **通过** |
| S09 | mid, cue-q_state_layout, end | 0 | 提问卡字号 32/22pt，居中规范 | SWA紫/FG白 | 状态缓存内部解剖悬念感强，过渡平滑 | **通过** |
| S10 | cue-state_anatomy, cue-store_drop_split, cue-prefix_truncate, end | 0 | 槽位分区字号 $\ge 18$pt，虚线清晰 | KV绿(存储)/WARN红(丢弃) | 左右分界清晰，低地址前缀截断零拷贝意图突出 | **通过** |
| S11 | cue-ring_134, cue-why_134, cue-backtrack_role, end | 0 | 环形说明卡字号 $\ge 18$pt | SWA紫/DRAFT红/DECODE蓝 | 128滑窗与6步回退预算双重使命并列排布严整 | **通过** |
| S12 | cue-kvstore_262, cue-default_zero_copy, end | 0 | 字号 $\ge 18$pt，对比均衡 | WARN橙(重排)/DECODE蓝(memcpy) | 262环重排与134环直接拷贝优劣一目了然 | **通过** |
| S13 | cue-disk_size_calc, cue-fixed_1_35mb, end | 0 | number_card 72pt/30pt，算式 20pt | KV绿/DECODE蓝/EXPERT金 | 1.35 MiB 金色大字冲击力强，固定常数感鲜明 | **通过** |
| S14 | mid, cue-q_three_128, end | 0 | 提问卡字号 32/22pt，居中舒适 | EXPERT金/FG白 | “到处都是128”认知矛盾铺垫充分 | **通过** |
| S15 | cue-aha_three_128, cue-card_container, cue-card_grain, cue-card_align, end | 0 | 三联卡字号 18pt，间距 0.4 | 蓝(容器)/绿(步长)/紫(对齐) | Aha时刻三卡并列展开，视觉节奏与冲击力拉满 | **通过** |
| S16 | cue-mem_plan_flow, cue-deduct_2x_state, cue-launch_check_80, end | 0 | 三步阶梯卡字号 18pt，注脚 16pt | DECODE蓝/SWA紫/EXPERT金 | 显存规划流程由上至下递进，80%硬约束警示突出 | **通过** |
| S17 | cue-prefix_truth, cue-fifo_only, cue-overwrite_risk, end | 0 | 源码结构与红叉对比分明 | DECODE蓝/WARN红/EXPERT金 | 链表分配器 vs 红叉缺失项，打破前缀树幻觉 | **通过** |
| S18 | cue-fork_seq_anim, cue-cow_action, end | 0 | 父子请求块条对齐，字号 $\ge 16$pt | DECODE蓝/GPU绿/WARN橙 | fork_seq 引用计数递增与末尾块 COW 分裂生动 | **通过** |
| S19 | cue-three_tier_storage, cue-route_compare, end | 0 | 三层立体架构与横向对比天平 | GPU绿/CPU浅蓝/DECODE蓝 | L1-L2-L3 生产立面宏大，网关前置哲学对比突出 | **通过** |
| S20 | mid, cue-recap_cards, cue-next_hook, end | 0 | 三大要点卡整齐，下集预告醒目 | DECODE蓝/KV绿/PREFILL橙 | 全集三大认知收拢利落，SWA有界重放伏笔到位 | **通过** |

## 2. 审查项合规清单

- [x] **0 layout WARN**：全部 20 个镜头在渲染和关键帧抽取中均为 0 `[dvlib] WARN`。
- [x] **字幕安全区保障**：所有图形、卡片与文字元素下边缘均在 $y \ge -2.25$，距离底部硬字幕保留区（$y \le -2.75$）留有 $> 0.5$ 个安全单位，绝对不压字幕。
- [x] **字号下限遵守**：所有正文文字标签 $\ge 18$pt，最小注释注脚 $\ge 16$pt，高分辨率下清晰无噪点。
- [x] **色彩语义纯正**：严格遵守视觉词典：块状 KV 为蓝/绿、状态缓存为紫、硬件与存储为浅蓝/深灰、警告与丢弃为橙红、关键概念为金黄。
- [x] **跨镜头与跨集一致性**：LayerStack 与 EP03/EP07 规范完全一致，MiniMap 准确指向“KV 存储”，片尾预告无缝衔接 EP07。

## 3. 结论

**审校结论：放行（PASS）**。全片 20 个镜头视觉语言高度严谨，信息传达准确，排版无任何穿插冲突，批准进入全片交付与终混阶段。
