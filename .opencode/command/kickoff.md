---
description: 开工：完成 P0（环境与基线）和 P1（开工计划），停在人类检查点 H1
agent: showrunner
---

开始本项目。按 `docs/00_MASTER_SPEC.md` 第 4 节执行 P0 和 P1，然后停在 H1。

1. 读 `docs/00_MASTER_SPEC.md` 全文，再读 `docs/` 其余文件。
2. 如果 `work/` 不存在：建立 `docs/09_PRODUCTION_PIPELINE.md` 第 1 节列出的目录；把 `templates/STATUS.md`、`templates/decisions.md`、`templates/open_questions.md`、`templates/glossary.md` 复制进 `work/`。已存在就先读 `work/STATUS.md`，从断点继续，不要覆盖。
3. P0：并行派发
   - pipeline-engineer：T-ENV（`docs/08_DISPATCH_TEMPLATES.md`）
   - fact-checker：确认知识库 DeepInfer 基线 commit 与上游是否有新提交（用 T-FACT-QUERY 模板，编号 P0/Q-BASELINE）
4. 按 G0 清单验收；把音色、语速、代码基线写进 `work/decisions.md`。
5. P1：按 `templates/plan.md` 写 `work/plan.md`。
6. 更新 `work/STATUS.md`：P0 ✓（或 ⏸ 附原因）；在"等待人类"区写 H1 与要看的文件。
7. 停止。用中文告诉委托人：P0 结果、`plan.md` 里最需要他拍板的三件事。

委托人附加说明（可能为空）：$ARGUMENTS
