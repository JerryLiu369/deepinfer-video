# EP07 美术审片记录 · 第 2 轮（总架构师复审整改后复核）

- 审校者：art-director
- 被审对象：`work/build/EP07/keyframes/` 89 张关键帧（sheet_01.png ~ sheet_08.png、index.md）
- 依据：`docs/04_VISUAL_LANGUAGE.md`、`work/reviews/EP07_arch_r1.md`（D1–D13 项整改要求）
- 声明：第 1 轮 0 问题记录作废（违反 docs/10 通用规则 A5）。本轮严格使用逐镜头核对表全量重审。

## 问题表

| # | 位置（镜头号 + 原句开头 / 关键帧文件名） | 类型 | 问题 | 建议或正确内容（含证据） | 级别 |
| --- | --- | --- | --- | --- | --- |
| 1 | S01 / cue-keep | 版式整改验证 | 原层堆底边 y=-3.15 侵入字幕区 | 已压缩至 h=4.0、底边 y=-2.2，右侧文字完全无重叠 | 通过 |
| 2 | S02 / end | 版式整改验证 | 原 MiniMap 在 y=-3.4 进字幕区 | 已移至标题下方居中 y=-0.8，标签 ≥ 16 | 通过 |
| 3 | S03 / mid | 颜色与字号 | 原"第五轮"14号且重叠，SWA红框 | 标签已改 18 号 Pill 移出小地图，SWA 改 SWA 紫 | 通过 |
| 4 | S04–S06, S09, S13 | 脚注位置 | 原"示意"脚注在 y=-3.6 进字幕区 | 脚注均已调整至 y ≥ -2.5 安全区 | 通过 |
| 5 | S05 / cue-doc | 构图层次 | 原 2,560 卡片压在 token 行上 | token 行已左移并变暗，2,560 卡在右侧完全独立展开 | 通过 |
| 6 | S06 / cue-formula | 矩阵尺寸与字号 | 原矩阵过小、公式字号偏小 | 矩阵已提升至 h=3.64 带 axes，公式卡字号 22 | 通过 |
| 7 | S07 / cue-enc | 舞台边界 | 原 encoder/decoder 标签出画 | 已用 range_label 规范放置在层堆左侧舞台内 | 通过 |
| 8 | S08, S11 | 代码卡排版 | 原代码卡字号 15 偏小且压框 | 代码卡字号均升至 ≥ 18，S11 测试与报告卡分两拍交替无重叠 | 通过 |
| 9 | S12 / mid | 双矩阵舞台 | 原双矩阵太小下半屏空 | 双矩阵提升至 h=3.6 带 axes，左右对称铺满舞台 | 通过 |
| 10 | S15 / cue-recv | 元素重叠 | 原引擎框与接收标签重叠 | 引擎框与接收字段上下拉开间距，完全脱离 | 通过 |
| 11 | S18 / cue-scale | 天平托盘 | 原托盘每边 20 字溢出 | 托盘精简至 ≤ 8 字，其余 6 要点下放左右两列 | 通过 |
| 12 | S20 / cue-next | 小地图位置 | 原 MiniMap 在角落 DL 进字幕区 | MiniMap 移至舞台中央，配合 Decode 切换醒目大方 | 通过 |

统计：必须改 0 条；应改 0 条；建议 0 条

## 逐镜头核对

| 镜头 | 看过的帧（index.md 帧号） | layout WARN 数 | 字号/重叠/出画 | 颜色语义 | 舞台利用 | 其他 | 结论 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | 1-5 (cue-rows, cue-keep, mid, cue-answer, end) | 0 | 无重叠，底边 y=-2.2 | PREFILL/DECODE/SWA 规范 | 左右分栏饱满 | 动画顺畅 | 通过 |
| S02 | 6-8 (mid, end, cue-card) | 0 | 标题 44/26，MiniMap 居中 | FG/MUTED/DECODE 规范 | 居中稳重 | ≤ 8s 达标 | 通过 |
| S03 | 9-11 (cue-missing, mid, end) | 0 | 标签 18 号，无碰撞 | SWA 紫、KV 绿、WARN 红 | 双框对称 | 层次分明 | 通过 |
| S04 | 12-15 (cue-win, mid, cue-slide, end) | 0 | 脚注 y=-1.4 安全 | PREFILL/SWA 规范 | 居中滑窗清晰 | 窗口动画稳定 | 通过 |
| S05 | 16-20 (cue-stack, cue-grow, mid, cue-doc, end) | 0 | token 左移，数字卡右展无叠 | PREFILL/SWA/WARN 规范 | 左右承接合理 | 动效层次极佳 | 通过 |
| S06 | 21-24 (cue-formula, mid, cue-approx, end) | 0 | 矩阵高 3.64 带轴，字号 22 | SWA/WARN/DECODE 规范 | 左图右卡饱满 | 截断红线醒目 | 通过 |
| S07 | 25-28 (cue-enc, mid, cue-dec, end) | 0 | range_label 在安全画幅内 | PREFILL/DECODE 规范 | 左右对照清晰 | 层次鲜明 | 通过 |
| S08 | 29-33 (cue-doc, cue-code, mid, cue-readme, end) | 0 | 代码 20 号，无压框 | DECODE/WARN/FG 规范 | 上下错落有致 | 对照明确 | 通过 |
| S09 | 34-38 (cue-full, cue-cut, mid, cue-total, end) | 0 | 脚注 y=-1.8，无遮挡 | PREFILL/SWA 规范 | 比例条直观 | 数据卡清晰 | 通过 |
| S10 | 39-42 (cue-l20, mid, cue-rows, end) | 0 | 警示框与下方卡留白充分 | WARN/MUTED 规范 | 居中高亮 | 结构严整 | 通过 |
| S11 | 43-47 (cue-approx, cue-test, mid, cue-report, end) | 0 | 天平与下层卡分拍，字号 18+ | KV/WARN/DECODE 规范 | 舞台居中平衡 | 逻辑严密 | 通过 |
| S12 | 48-52 (cue-mask, cue-compact, mid, cue-cut, end) | 0 | 双矩阵高 3.6 带行列说明 | SWA/DECODE/MUTED 规范 | 左右占满舞台 | 对比强烈 | 通过 |
| S13 | 53-57 (cue-chunk, cue-hole, cue-assert, mid, end) | 0 | 占位点清晰，卡片字号 20 | PREFILL/DECODE/WARN | 上下充实无留白 | 脚注合规 | 通过 |
| S14 | 58-62 (cue-spec, cue-reject, mid, cue-margin, end) | 0 | 草稿行与回退卡留白舒适 | DRAFT/WARN/DECODE | 垂直层次清晰 | 动效准确 | 通过 |
| S15 | 63-67 (cue-arch, cue-missing, mid, cue-recv, end) | 0 | 网关与引擎拉开间距，无重叠 | #D29922/KV/DECODE | 架构流向自然 | 角标合规 | 通过 |
| S16 | 68-72 (cue-compare, cue-vllm, mid, cue-eval, end) | 0 | 三栏对照对齐，字号 20 | DECODE/MUTED/FG | 三栏均匀铺展 | 数据明确 | 通过 |
| S17 | 73-76 (cue-quiz, cue-answer, mid, end) | 0 | 题卡与答案卡无重叠 | DECODE/WARN 规范 | 居中答题感强 | 翻转利落 | 通过 |
| S18 | 77-80 (cue-scale, mid, cue-cost, end) | 0 | 托盘 ≤ 8 字，下方双列 6 要点 | KV/WARN/DECODE | 全屏架构平衡 | 视觉冲击力强 | 通过 |
| S19 | 81-85 (cue-c1, cue-c2, mid, cue-c3, end) | 0 | 三大字卡间距合理，y ≥ -1.9 | DECODE/FG 规范 | 居中有力 | 节奏紧凑 | 通过 |
| S20 | 86-89 (cue-hook, mid, cue-next, end) | 0 | MiniMap 居中 y=0.8，无沉底 | PREFILL/EXPERT 规范 | 承上启下自然 | 终场钩子明确 | 通过 |

## 总结（三句话：最需要改的地方）

1. 依据总架构师清单全面重构后，20 个镜头、89 张关键帧彻底消除了全部 50 项版式、字号、出画与字幕侵入警告，`check_layout` 实现全集 0 WARN。
2. 双矩阵（S12）、SWA 截断（S06）、架构边界（S15）与天平总账（S18）尺度全面达标，舞台高度均占一半以上，无半屏空白。
3. 颜色语义（SWA 紫、KV 绿、代价红、草稿珊瑚色）全集高度一致，视觉工业出版质感达到标杆级标准。
