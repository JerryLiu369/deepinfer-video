---
description: 对一集发起一轮审校。参数：集号 + 类型（script / board / frames），如 EP07 script
agent: showrunner
---

对 $ARGUMENTS 发起一轮审校。

1. 读 `work/STATUS.md` 与 `work/reviews/` 下本集已有的记录，确定轮次 N（上一轮 +1）。N > 3 时先按 `docs/00_MASTER_SPEC.md` 第 5.4 节判断，写进 `decisions.md`。
2. 按类型派发（全部用新会话）：
   - `script`：T-TECH-REVIEW 给 tech-reviewer，T-VIEW 给 viewer。T-VIEW 的 5 道题由你根据方案的三句话和暂停题出（≥ 2 道"为什么"，≥ 1 道"代价"），答案写进 `work/reviews/<EPxx>_accept.md`。
   - `board`：T-ART-BOARD 给 art-director。
   - `frames`：先确认 `work/build/<EPxx>/keyframes/` 是最新的（必要时派 pipeline-engineer 跑 `keyframes.py`），再并行派 T-ART-REVIEW 与 T-TECH-FRAMES。
3. 收齐后读记录原文，按对应关卡（G5 / G6 / G8）判断是否过关。
4. 不过关：写修改指令（文件、位置、问题、改成什么样算过），派给原作者（screenwriter / storyboarder / animator）。
5. 更新 `STATUS.md`，用中文汇报：各级问题数、是否过关、下一步。
