# EP08 美术审片记录（第 1 轮）

- 审校者：art-director
- 审校时间：2026-10-26
- 审校对象：`work/build/EP08/keyframes/`（共 25 张关键帧）与各镜头渲染结果
- 依据标准：`docs/04_VISUAL_LANGUAGE.md`（视觉词典）、`docs/10_REVIEW_CHECKLISTS.md` 第 5 节（关键帧与成片清单）

## 1. 逐镜头审查表

| 镜头号 | 查验的关键帧 | layout WARN | 字号/重叠/出画 | 颜色语义 | 舞台利用与排版 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | cue-wide_ep, cue-paradox, end | 0 | 字号 $\ge 18$pt，无重叠 | EXPERT金 / DECODE蓝 / WARN橙 | 左右对比清晰，访存与吞吐收敛反差突出 | **通过** |
| S02 | cue-no_tp, cue-linear_types, end | 0 | 字号 $\ge 18$pt，边距适度 | WARN橙 / PREFILL绿 / EXPERT金 | 顶部 Pill 警示醒目，左右 DP/EP 双块对称平稳 | **通过** |
| S03 | cue-voting, cue-placeholder, end | 0 | 字号 $\ge 18$pt，居中整齐 | GPU蓝 / MUTED灰 | 调度器两级投票与占位请求上下排布分明 | **通过** |
| S04 | cue-pipe, cue-shared_fusion, end | 0 | 字号 $\ge 16$pt，管道自适应 | GPU蓝 / EXPERT金 / PREFILL绿 | 六段流水横向贯穿，底部融合偏置说明清晰 | **通过** |
| S05 | cue-eplb, end | 0 | 字号 $\ge 18$pt，无冲突 | EXPERT金 / GPU蓝 | 两级贪心与 NVLink 显存直读左右呼应 | **通过** |
| S06 | cue-tradeoff, end | 0 | number_card 大号字体醒目 | DECODE蓝 / MUTED灰 | 60 并发能效拐点居中聚焦，视觉落点明确 | **通过** |
| S07 | cue-summary, end | 0 | 总结卡与 Pill 居中平衡 | GPU蓝 / DRAFT红 | 架构收拢有力，下集预告醒目 | **通过** |

## 2. 审查项合规清单

- [x] **0 layout WARN**：全部 7 个镜头在渲染和关键帧抽取中均为 0 `[dvlib] WARN`。
- [x] **字幕安全区保障**：所有图形、卡片与文字元素下边缘均在 $y \ge -2.25$，距离底部硬字幕保留区（$y \le -2.75$）留有充足安全裕量。
- [x] **字号下限遵守**：所有正文文字标签 $\ge 18$pt，最小注释注脚 $\ge 16$pt，清晰易读。
- [x] **色彩语义纯正**：严格遵守视觉词典：Attention DP 采用 PREFILL 蓝绿、MoE 宽 EP 采用 EXPERT 金色、调度与硬件采用 GPU/CPU 色、投机草稿采用 DRAFT。

## 3. 结论

**审校结论：放行（PASS）**。全片 7 个镜头视觉语言统一，排版紧凑无遮挡，批准进入成片导出阶段。
