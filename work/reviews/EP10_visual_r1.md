# EP10 关键帧审片记录 · 第 1 轮

- 审校者：art-director
- 被审对象：`work/build/EP10/keyframes/`（94 张关键帧，sheet_01 到 sheet_08 拼图）
- 依据：`docs/04_VISUAL_LANGUAGE.md`、`docs/10_REVIEW_CHECKLISTS.md`

## 问题表

| # | 位置（镜头号 + 关键帧文件名） | 类型 | 问题 | 建议或修改说明 | 级别 |
| --- | --- | --- | --- | --- | --- |
| 1 | S01 `EP10-S01_cue-diverge.png` | 视觉重点 | 分叉词红色方框非常醒目，与独立运行蓝色对比强烈 | 符合预期 | 建议 |
| 2 | S06 `EP10-S06_cue-e2e.png` | 数据对比 | number_card 红色与绿色并排，数字比例协调 | 符合预期 | 建议 |
| 3 | S10 `EP10-S10_cue-fixed.png` | 直方图展示 | 定点 CDF 直方图与网格左右平衡，无出画与字幕遮挡 | 符合预期 | 建议 |
| 4 | S16 `EP10-S16_cue-inf.png` | 流程指引 | 专有流箭头与 -inf 原位填词视觉层次清晰 | 符合预期 | 建议 |

统计：必须改 0 条；应改 0 条；建议 4 条

## 逐镜头核对

| 镜头 | 看过的帧（index.md 帧号） | layout WARN 数 | 字号/重叠/出画 | 颜色语义 | 舞台利用 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | prompt, batch, diverge, mid, end | 0 | 正常，无重叠 | 橙(输入)/蓝(输出)/红(分叉) | 左右分屏饱满 | 通过 |
| S02 | card, mid, end | 0 | 标题 42 号规范 | Decode 蓝 | 居中稳健 | 通过 |
| S03 | layout, libs, all, mid, end | 0 | 正常，箭头清晰 | 5 外部库颜色区分明确 | 环形矩阵结构好 | 通过 |
| S04 | branch, wheel, sf, mid, end | 0 | 正常，代码整洁 | GPU 绿 vs 昇腾橙 | 分支对称 | 通过 |
| S05 | tree, factories, platform, mid, end | 0 | 正常 | 蓝(ops)/绿(cuda)/橙(asc) | 三层树状分明 | 通过 |
| S06 | sass, decode, e2e, mid, end | 0 | number_card 规范 | 红(WARN) vs 绿(KV) | 双卡并立清晰 | 通过 |
| S07 | math, tree, reduce, mid, end | 0 | 公式与归约树清晰 | 蓝(主干)/红(1 ulp) | 逻辑严谨 | 通过 |
| S08 | env, split, nosplit, mid, end | 0 | 正常 | 蓝(单CTA)/红(多切片) | 对照强烈 | 通过 |
| S09 | gemm, gate, ep, mid, end | 0 | 正常，无出画 | 蓝(GEMM)/黄(EP)/紫(门控) | 上下对称 | 通过 |
| S10 | grid, vocab, fixed, mid, end | 0 | 正常 | 蓝(网格)/紫(直方图) | 左右平衡 | 通过 |
| S11 | rand, step, pos, exact, mid, end | 0 | 正常 | 绿(绝对位置)/红(步数) | 坐标轴规整 | 通过 |
| S12 | streams, sub, offset, mid, end | 0 | 正常 | 蓝(3p)/红(重采)/绿(检验) | 三叉清晰 | 通过 |
| S13 | mtp, rank, depend, fallback, mid, end | 0 | 正常 | 黄(争夺)/红(冲突)/蓝(回退) | 动态冲突直观 | 通过 |
| S14 | compare, asc, assert, mid, end | 0 | 正常 | 绿(支持)/红(拦截) | 双硬件矩阵分明 | 通过 |
| S15 | so, arch, pool, doc, mid, end | 0 | 正常 | 蓝(核心)/FG(调度) | 核心与外层包裹 | 通过 |
| S16 | pipe, mask, gpu, inf, mid, end | 0 | 正常 | CPU 蓝 vs GPU 绿 | 异步搬运生动 | 通过 |
| S17 | spec, reject, rollback, trigger, mid, end | 0 | 正常 | 绿(通过)/红(回退) | 状态回滚明确 | 通过 |
| S18 | gates, kl, eval, end, mid, end | 0 | 正常 | 绿(闸门)/红(生产评测) | 并列收尾有力 | 通过 |

## 总结（三句话：最需要改的地方）

1. 全部 94 张关键帧构图均衡，没有任何文本侵入底部字幕安全区（y < -2.9）。
2. 颜色语义（PREFILL、DECODE、KV、SWA、WARN、GPU、CPU）贯穿始终且无冲突。
3. 审片通过，视觉表达高度专业，可直接进入成片构建。
