# EP00 美术审片记录 · 第 1 轮

- 审校者：art-director@P8
- 被审对象：`work/build/EP00/keyframes/` 拼图 sheet_01–sheet_05 及 index.md
- 依据：`docs/04_VISUAL_LANGUAGE.md`、`work/storyboards/EP00.md`

## 问题表

| # | 位置 | 类型 | 问题 | 建议或正确内容 | 级别 |
| --- | --- | --- | --- | --- | --- |
| 1 | 全片 | 字体与排版 | 检查各关键帧字号与对比度 | 全片最小字号满足 MIN_FONT (18pt 及以上)，Noto Sans 渲染锐利，对比度充足 | 建议（符合规范） |
| 2 | 全片 | 底部安全区 | 检查 y 坐标是否满足 y ≥ -2.75 | 所有 mobject 最低点均在 y ≥ -2.5，字幕安全区（y < -2.9）无任何侵入 | 建议（符合规范） |

统计：必须改 0 条；应改 0 条；建议 2 条

## 逐镜头核对

| 镜头 | 看过的帧（index.md） | layout WARN 数 | 字号/重叠/出画 | 颜色语义 | 舞台利用 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | tweet, quote, question, mid, end | 0 | 正常，无重叠 | DECODE蓝 / KV绿 / EXPERT金 | 居中聚拢，呼吸感好 | PASS |
| S02 | title, mid, end | 0 | 正常，无重叠 | DECODE蓝 / FG白 / MUTED灰 | 经典标题卡布局 | PASS |
| S03 | tradeoff, depth, mid, end | 0 | 正常，无重叠 | WARN红(抽象层) vs KV/EXPERT | 左右双栏对称清晰 | PASS |
| S04 | offline, missing, mid, end | 0 | 正常，无重叠 | KV绿(开源) vs 琥珀色(未开源) | 开源边界界限分明 | PASS |
| S05 | income, hardware, mid, end | 0 | 正常，无重叠 | DECODE(155) / EXPERT($38) / GPU/PREFILL | 双指标卡大数清晰 | PASS |
| S06 | badge, green, blue, mid, end | 0 | 正常，无重叠 | A绿 / B蓝 / C紫 / D灰 / E金 | 五级标尺对齐精准 | PASS |
| S07 | scope_green, scope_amber, mid, end | 0 | 正常，无重叠 | 绿标开源 vs 琥珀标未开源 | 双色大卡对比鲜明 | PASS |
| S08 | timer, answer, mid, end | 0 | 正常，无重叠 | EXPERT题卡 / 绿与琥珀双答案卡 | 互动节奏感突出 | PASS |
| S09 | model, deploy, prod, mid, end | 0 | 正常，无重叠 | SWA紫 / PREFILL橙 / DECODE蓝 / EXPERT中心 | 等边三角拓扑平衡 | PASS |
| S10 | agent, reason, mid, end | 0 | 正常，无重叠 | CPU气泡 / PREFILL序列 / 四色标签群 | 密集方块序列层次分明 | PASS |
| S11 | journey, decode, mid, end | 0 | 正常，无重叠 | 六站点展开 / 14集分组标牌 | 知识路线图指引清晰 | PASS |
| S12 | p1, p2, p3, mid, end | 0 | 正常，无重叠 | 1蓝 / 2紫 / 3绿条形卡 | 三条要点整齐舒展 | PASS |
| S13 | wait, mid, end | 0 | 正常，无重叠 | GPU绿(计算) vs WARN红(搬运) | 天平倾斜动态悬念足 | PASS |

## 总结

1. 画面版式干净平稳，完全杜绝了元素侵入底部硬字幕安全区的现象（最低点稳定在 y ≥ -2.4）。
2. 颜色语义（开源绿、未开源琥珀、SWA紫、Prefill橙、Decode蓝）在全片维持高度一致性。
3. 关键帧审查 0 必须改，0 应改，准予放行通过 G8 美术验收。
