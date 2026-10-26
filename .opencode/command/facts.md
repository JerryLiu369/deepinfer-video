---
description: 派发 P2 事实包。参数：集号列表（如 EP07 EP03）或 all
agent: showrunner
---

执行 P2 事实包，范围：$ARGUMENTS（为空或 all 表示全部 14 集）。

前提：`work/STATUS.md` 显示 H1 已通过。没通过就停下，告诉委托人。

1. 读 `docs/00_MASTER_SPEC.md` 第 4 节 P2、第 5.3 节；读 `work/plan.md` 的派发计划。
2. 先派 EP00 与 EP03（它们负责建立 `work/facts/GLOBAL.yaml`）；GLOBAL 过 lint 后再派其他集。
3. 每集一个 T-FACT 任务。★★★ 集（EP03、EP04、EP07、EP12）派 `_a`、`_b` 两份独立任务，完成后派 T-FACT-DIFF。
4. 并发 6–8 个。每派发一批就更新 `STATUS.md`。
5. 逐集按 G2 清单验收：自己跑 `python tools/lint_facts.py EPxx --kb "$DV_KB"`；打开研究简报看六节是否齐全；不合格就打回。
6. 汇总所有集的 `open_questions.md` 新增项，影响主线的，在 `decisions.md` 写下口径。
7. 用中文汇报：各集事实数与等级分布、过关情况、需要委托人知道的意外发现。
