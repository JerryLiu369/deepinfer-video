# EP02 分镜纸面审评报告（第 1 轮）

> art-director 依据 `docs/04_VISUAL_LANGUAGE.md` 与分镜清单，对 `work/storyboards/EP02.md` 进行纸面审查。

## 0. 元信息

- 审查对象：`work/storyboards/EP02.md`（19 个镜头）
- 依据标准：`docs/04_VISUAL_LANGUAGE.md`、`docs/10_REVIEW_CHECKLISTS.md`（G6 清单）
- 审查结论：**全部通过（PASS）**，0 必须改项。

## 1. 核心项逐条核验

1. **Cue 完整性与一一对应**：
   - 逐镜头核对 shots.json 中全部 19 个镜头共 112 个 cue 点；
   - 分镜中每一个 `until("cue")` 在脚本 shots.json 中均存在，覆盖率 100%，无任何虚构 cue 或拼写错误。
2. **安全边距与版式约束**：
   - 头部 Header 统一位于左上角 `UL, buff=0.45`，并受 `fit_left_of_tags` 保护不遮挡右上角角标；
   - 底部元素严格受限在 $y \ge -2.7$ 舞台安全区内，字幕带（$y < -2.9$）保持完全净空；
   - 水平边界严格控制在 $|x| \le 6.6$ 舞台宽度范围内。
3. **颜色语义一致性**：
   - 绿色（KV / GPU）：离线引擎核心、已算好缓存与代码证实；
   - 蓝色（DECODE / CPU）：解码超节点、SM100 与通用概念；
   - 橙色（PREFILL）：预填充集群、V4.1-Flash 模型卡；
   - 红色/暗金（WARN / EXPERT）：未开源三大缺件看板、警告与限制；
   - 灰色（MUTED / GRID）：外部未开源基础设施、网关与被蒙版阴影区。
4. **全景架构图（全系列最重要的一张图）设计规范**：
   - S07、S09、S11 架构图构图严密，层级分明（Entrypoint -> Prefill / Decode -> 3FS）；
   - S11 开源边界变色采用计算实例内绿亮、外部灰度遮罩的方式，边界一目了然，无任何模棱两可。

## 2. 结论

- 纸面审无“必须改”项。
- 允许进入 P7（配音与粗剪）与 P8（动画实现）。
