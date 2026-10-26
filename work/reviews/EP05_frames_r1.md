# EP05 屏幕技术审校记录（第 1 轮）

- 审校人：tech-reviewer
- 审校时间：2026-10-26
- 审校对象：`work/build/EP05/keyframes/` 143 张关键帧及屏幕呈现内容
- 依据标准：`work/facts/EP05.yaml`、`docs/06_FACT_PROTOCOL.md`、`docs/10_REVIEW_CHECKLISTS.md`

## 1. 逐镜头屏幕文字与技术事实核对表

| 镜头号 | 查验的关键帧（编号） | 屏幕技术陈述与数字 | 事实账本依据 (ID) | 技术准确性核对 | 结论 |
| --- | --- | --- | --- | --- | --- |
| S01 | 1, 3, 5 | 前向 4.0ms / CPU 1.5ms / 空转 24.6% / 吞吐 +32.6% | F05-01, F05-02, F05-21 | 计算脚本 calc/EP05_bubble.py 推导一致 | **准确** |
| S02 | 7, 9 | EP05 · 调度中枢 / 让 GPU 一刻不停 / MiniMap 5 | G-01 | 系列大纲与站点一致 | **准确** |
| S03 | 11, 12, 14, 15 | Forward 4.0ms / Sample 0.6ms / synchronize / 空转 24.6% | F05-01, F05-02 | 同步时序与阻塞等待点真实 | **准确** |
| S04 | 18, 20, 23 | ZOS / Forward(N) 与 Post(N-1) 并发 / 等待点后移 / 0ms 等待 | F05-01, F05-05 | 异步重叠核心机制真实 | **准确** |
| S05 | 26, 28, 30, 32 | worker.py / execute_model_step / 1.Fwd 2.Post 3.Smp 4.Defer | F05-03 | 源码 worker.py:96-187 四段式骨架一致 | **准确** |
| S06 | 35, 36, 38, 39 | is_prompt=True / 连续两次后处理 / 排空流水线 / 首步无重叠 | F05-04 | 源码 worker.py:182-187 边界一致 | **准确** |
| S07 | 42, 44, 46 | 输入未知 / CPU 滞后准备 N+1 / 采样在显卡运行 / 无法构造输入 | F05-06 | 异步调度因果矛盾表述精准 | **准确** |
| S08 | 49, 51, 53, 54 | 存量 0 字节 / TileLang gather_input_ids_zos / 显存就地捡词 | F05-06 | 源码 zos.cpp:84 与 gather_input_ids_zos 一致 | **准确** |
| S09 | 57, 59, 61, 62 | get_len() 降序重排 / 动态换位 / remap 映射 / 杜绝索引踩踏 | F05-07 | 源码 scheduler.hpp:648 与 zos.cpp:147 一致 | **准确** |
| S10 | 65, 66, 68 | EOS 终止符 / CPU 滞后不知情 / 第 N+1 步幽灵前向 (Ghost) | F05-08 | 源码 zos.cpp:298 额外前向事实真实 | **准确** |
| S11 | 72, 74, 76, 77 | 输出丢弃 / N+2 步释放 / 500词多跑1步浪费 0.2% / 换消灭 24.6% 空泡 | F05-08, F05-21 | 算力天平推导完全闭环 | **准确** |
| S12 | 79, 81, 82 | advance_optimistically / total_inflight / commit_processed | F05-09, F05-11 | 源码 sequence.hpp:216 双层记账一致 | **准确** |
| S13 | 85, 87, 88 | DecodePerfCache 延迟曲线 / 锁定 best_bsz / TileLang 变长切分 / D2H | F05-10, F05-15 | 源码 mtp_varlen.hpp:235 与 worker.py:218 一致 | **准确** |
| S14 | 91, 93, 94 | LCFS 短输出优先 / 抢占长输出老请求 / stop_preempted 直接终止 | F05-12 | 源码 scheduler.hpp:622, 771 一致 | **准确** |
| S15 | 97, 99, 100 | 单步禁混合 / _dp_allreduce / 每 70 步 ALL / 每 100 步 ANY | F05-13 | 源码 scheduler.hpp:308 投票机制一致 | **准确** |
| S16 | 103, 105, 106 | 文档二次模型 / 代码 quota 0 命中 / 硬 Token 预算 / FlopsEstimator 日志 | F05-14 | 文档与源码真实边界比对严密 | **准确** |
| S17 | 109, 111, 112 | DeferredRelease 延迟释放 / 与前向重叠 / flush_inflight_reqs 冲刷 | F05-16, F05-17 | 源码 llm_engine.py:67 与 llm.py:176 一致 | **准确** |
| S18 | 115, 117, 118 | NanoFlow 源头 / 文档注明参考 SGLang / vLLM 默认 / SGLang v0.4 默认 | F05-18, F05-19, F05-20 | 工业界横向事实核验吻合 | **准确** |
| S19 | 121, 123, 124 | 1.时空错位重叠 2.现场捡词重组 3.千分之二换三成吞吐 / 答题卡 | F05-01, F05-06, F05-08, F05-21 | 三句话总结精准支撑，题目答案完全准确 | **准确** |
| S20 | 127, 128 | 下集预告 · EP06 / KV 与状态缓存: 两种记忆，两种管法 / MiniMap 6 | G-02 | 下集衔接顺畅，无前置剧透 | **准确** |

## 2. 审查项合规清单

- [x] **屏幕文字与脚本 100% 对应**：没有任何屏幕文字脱离脚本定义，数字与单位严格具备前提条件。
- [x] **开源范围与角标准确**：S06、S14、S16 明确声明开源实现边界，角标与 scope 标签准确无误。
- [x] **代码路径无笔误**：`deepinfer/worker/worker.py`、`csrc/engine/scheduler.hpp`、`zos.cpp` 等路径与源码完全吻合。

## 3. 结论

**审校结论：放行（PASS）**。屏幕技术呈现零硬伤，批准进入成片导出与观看手册编制。
