# EP01 分镜纸面审片记录

> art-director 审分镜文档（纸面审查），把控视觉语言、颜色语义、信息密度与跨集一致性。

## 0. 审查概况

- 分镜文件：`work/storyboards/EP01.md`
- 对应脚本：`work/scripts/EP01.md`
- 参照规范：`docs/04_VISUAL_LANGUAGE.md`
- 审查镜头：S01 至 S19 全部 19 个镜头

## 1. 审查清单核验

1. **颜色语义一致性**：
   - 橙色（PREFILL）代表输入、Prompt、Prefill 阶段。
   - 蓝色（DECODE）代表输出、自回归 Token、Decode 阶段。
   - 绿色（KV）代表 KV Cache 键值缓存。
   - 金色（EXPERT）代表模型权重与 MoE 专家。
   - 红色（WARN）代表带宽拥堵、等待气泡、显存告警。
   - 全部严格吻合视觉词典。
2. **信息密度与构图**：
   - 每个镜头主体视觉单一明确（如 S07 的 Scale 天平、S11 的木桶网格、S13 的雷达三角）。
   - 动画元素严格遵守安全区：底部边界 $y \ge -2.7$，彻底消除对底部硬字幕（$y < -2.9$）的遮挡。
   - 文字层级分明，主标题 22–24pt，正文说明 18–20pt，无小于 16pt 的微小字。
3. **cue 同步覆盖度**：
   - 逐一比对 `work/build/EP01/shots.json`，19 个镜头里的所有 `until("cue")` 100% 存在且一一对应，无悬空或漏配。
4. **组件复用度**：
   - 充分复用已有的 `dvlib.py` 资产（Scale, MiniMap, Block, TokenRow, number_card, header, Pill），无须重复造轮子。

## 2. 审查结论

- 必须改（Blocker）：0 条
- 应该改（Major）：0 条
- 建议（Minor）：0 条
- 结论：**分镜纸面审查通过，准予进入配音合成与动画实现阶段**。
