# EP08 屏幕技术审校记录（第 1 轮）

- 审校者：tech-reviewer
- 审校时间：2026-10-26
- 审校对象：`work/build/EP08/keyframes/` 关键帧上的文字、数字与技术引用
- 依据标准：`docs/06_FACT_PROTOCOL.md`、`docs/10_REVIEW_CHECKLISTS.md`

## 1. 逐镜头审查表

| 镜头号 | 查验内容 | 事实支撑 | 真实性与准确度 | 结论 |
| --- | --- | --- | --- | --- |
| S01 | 52 → 7 个专家，53% → 5% 吞吐收敛 | F08-08, F08-12 | 与 calc/EP08_wide_ep_bandwidth.py 精确一致 | **通过** |
| S02 | 无张量并行，Attention DP + MoE EP | F08-01, F08-02 | 与 deepinfer/config.py 源码定义一致 | **通过** |
| S03 | MIN all_reduce 投票，1-token placeholder | F08-03, F08-04 | 与 csrc/engine/scheduler.hpp 源码一致 | **通过** |
| S04 | MoE 六段流水，Shared Expert 作为 Bias 融合 | F08-05, F08-06 | 与 deepinfer/model_executor/models/v4_modules/mlp.py 一致 | **通过** |
| S05 | EPLB 两级贪心，symm_mem 显存直读 | F08-09, F08-10 | 与 policy.py 及 shuffle.py 源码一致 | **通过** |
| S06 | 60 并发生产拐点 | F08-11, F08-12 | 与官方 QA 部署文档叙述一致 | **通过** |
| S07 | 总结与 DSpark 下集预告 | F08-14, F08-15 | 概念准确无歧义 | **通过** |

## 2. 结论

**审校结论：放行（PASS）**。屏幕文字与数字全部可追溯至账本事实与源码实现，无未核验内容。
