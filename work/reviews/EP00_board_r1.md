# EP00 分镜纸面审校记录 · 第 1 轮

- 审校者：art-director@P6
- 被审对象：`work/storyboards/EP00.md`
- 依据：`docs/04_VISUAL_LANGUAGE.md`、`work/scripts/EP00.md`、`manim_lib/dvlib.py`

## 问题表

| # | 位置 | 类型 | 问题 | 建议或正确内容 | 级别 |
| --- | --- | --- | --- | --- | --- |
| 1 | S02 | 版式 | MiniMap 作为开篇全图展示，注意 scale 不宜过大避免侵入底部安全区 | 设置 scale=1.1，y 坐标设在 -1.2，留出充足边距 | 建议 |
| 2 | S13 | 元素 | Scale 天平倾斜动画时，右盘下沉需控制在 y ≥ -2.75 之上 | 初始 y=-0.5，最大倾斜角设为 12°，右盘最低点不低于 -2.5 | 建议 |

统计：必须改 0 条；应改 0 条；建议 2 条

## 逐镜头核对

| 镜头 | 版式规划 | 视觉词典与颜色语义 | 脚本 cue 对齐 (100%) | 屏幕字与数字一致性 | 示意声明 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | 公告聚焦卡 | BG/FG/DECODE，语义准确 | tweet, quote, question 均吻合 | 一致 | — | PASS |
| S02 | 集号大标题+全亮小地图 | DECODE/FG/MUTED | title 吻合 | 一致 | — | PASS |
| S03 | 左右双栏抽象vs啮合 | WARN/MUTED vs KV/EXPERT | tradeoff, depth 均吻合 | 一致 | 包含 | PASS |
| S04 | 三列网格系统边界图 | KV(开源) vs WARN(未开源虚框) | offline, missing, slots 均吻合 | 一致 | — | PASS |
| S05 | 双数字指标卡+硬件徽标 | DECODE(吞吐) / EXPERT(收入) | income, hardware 均吻合 | 一致 | 包含 | PASS |
| S06 | 五级证据横向标尺 | A绿/B蓝/C紫/D灰/E金 | badge, green, blue 均吻合 | 一致 | — | PASS |
| S07 | 四色开源范围对比卡 | 绿开源 / 琥珀文档 / 蓝代码+文档 | scope_green, scope_amber 均吻合 | 一致 | — | PASS |
| S08 | 倒计时互动自测卡 | EXPERT/KV/WARN，倒计时环 | timer, answer 均吻合 | 一致 | — | PASS |
| S09 | 三源头等边三角网络图 | SWA紫/PREFILL橙/DECODE蓝 | model, deploy, prod 均吻合 | 一致 | — | PASS |
| S10 | 序列流转全景 | PREFILL橙小方块长序列 | agent, reason 均吻合 | 一致 | 包含 | PASS |
| S11 | 六大站点全景路线图 | 六站点展开+14集标牌 | journey, decode 均吻合 | 一致 | 包含 | PASS |
| S12 | 三要点顺序滑入卡 | 1蓝/2紫/3绿，要点整齐 | p1, p2, p3 均吻合 | 一致 | — | PASS |
| S13 | 算力/带宽天平悬念卡 | GPU绿(计算) vs WARN红(搬运) | wait 吻合 | 一致 | 包含 | PASS |

## 总结

1. 13 个镜头的分镜设计完整严谨，各步骤动作严格锚定脚本 cue 点，无悬空 cue 与多余 cue。
2. 颜色语义完全遵循 Series Bible，严格区分开源（绿）与文档未开源（琥珀），为全系列观影建立清晰视觉防线。
3. 纸面审全项达标，准予放行进入动画工程与配音。
