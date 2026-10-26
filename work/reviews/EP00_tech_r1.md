# EP00 技术审校记录 · 第 1 轮

- 审校者：tech-reviewer@P5
- 被审对象：`work/scripts/EP00.md`
- 依据：`work/facts/EP00.yaml`、`work/facts/GLOBAL.yaml`、`docs/06_FACT_PROTOCOL.md`

## 问题表

| # | 位置 | 类型 | 问题 | 建议或正确内容（含证据） | 级别 |
| --- | --- | --- | --- | --- | --- |
| 1 | 全片 | 范围核验 | 检查各镜头 scope 标注是否准确 | S01/S04/S09 为 mixed（兼顾源码与未开源在线文档），S05 为 doc（引用生产吞吐与收入），其他为 general，符合规范 | 建议（已达标） |

统计：错误 0 条；不准确 0 条；建议 1 条

## 逐镜头核对

| 镜头 | 引用事实 ID | 事实状态与等级 | 旁白断言是否真正支撑 | 数字与条件核实 | scope 标注 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | F00-01, F00-06 | B/verified | 完全支撑（2026-10-20发布，官方动机原话） | 吻合 | mixed | PASS |
| S02 | F00-12 | B/verified | 支撑系列集数与站点定位 | 吻合 | general | PASS |
| S03 | F00-02, G-02 | B/verified | 支撑离线推理及仅支持单一模型 | 吻合 | general | PASS |
| S04 | F00-02, F00-03 | B/verified | 支撑缺失 KV 存储、P/D 分离、负载均衡 | 吻合 | mixed | PASS |
| S05 | F00-04, F00-05 | B/verified | 支撑 155万亿token/天及 $38/卡·时谷价收入 | 吻合 | doc | PASS |
| S06 | F00-09, F00-11 | B/verified | 支撑 A 到 E 证据等级及无硬件实测声明 | 吻合 | general | PASS |
| S07 | F00-10 | B/verified | 支撑绿标开源与琥珀标仅文档描述定义 | 吻合 | general | PASS |
| S08 | F00-10 | B/verified | 支撑暂停自测题设问与解答 | 吻合 | general | PASS |
| S09 | F00-07, G-06, G-07 | B/A/verified | 支撑模型结构、部署形态与生产需求三源头 | 吻合 | mixed | PASS |
| S10 | F00-08 | E/verified | 支撑第五轮约 6 万 token 上下文示意设定 | 吻合 | general | PASS |
| S11 | F00-12 | B/verified | 支撑 14 集站点与约 200 分钟总大纲规划 | 吻合 | general | PASS |
| S12 | F00-02, F00-07, F00-12 | B/verified | 支撑全片核心要点总结 | 吻合 | general | PASS |
| S13 | F00-02, G-06 | B/A/verified | 支撑下集物理瓶颈与算/搬悬念 | 吻合 | general | PASS |

## 总结

1. 逐镜头引用的 12 项本集事实与全局事实均处于 verified 状态，技术断言无超纲越界。
2. 涉及的生产规模数字（155万亿、38美元）均严格标明谷时定价口径，开源范围明确区分离线代码与未开源在线组件。
3. 结论：技术审校全项过关，准予放行。
