---
description: 推进一集走完 P3–P9（从看板记录的断点继续）。参数：集号，如 EP07
agent: showrunner
---

推进 $ARGUMENTS 这一集。

1. 读 `work/STATUS.md`，找到这一集当前的阶段和状态；读 `work/decisions.md` 中与它相关的条目。
2. 检查前提：本集 G2 已过；如果不是 EP07，试点 EP07 的 H3 已通过；前一集的方案已锁定（P3 需要）。不满足就停下说明原因。
3. 从断点开始，按 `docs/00_MASTER_SPEC.md` 第 4 节逐阶段推进：
   - P3 T-TREAT → 验收 → T-VIEW-HOOK → 锁定方案
   - P4 T-SCRIPT → 验收（G4）
   - P5 T-TECH-REVIEW 与 T-VIEW 并行（新会话）→ 汇总 → T-REVISE；最多 3 轮
   - P6 T-BOARD → T-ART-BOARD；P7 T-VOICE（可与 P6 并行）
   - P8 T-ANIM → 构建关键帧 → T-ART-REVIEW 与 T-TECH-FRAMES 并行 → 修改；最多 3 轮
   - P9 T-BUILD、T-COMPANION → 最终验收
4. 每个阶段过关后更新 `STATUS.md`，在备注写一行要点。
5. EP07 到 P7 后停在 H2，到 P9 后停在 H3：在"等待人类"区列出要看的文件，然后停止。
6. 用中文汇报：走到了哪一步、每关的关键结果、遗留问题。
