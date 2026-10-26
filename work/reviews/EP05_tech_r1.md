# EP05 技术审校记录（第 1 轮）

- 审校人：tech-reviewer
- 审校时间：2026-10-26
- 审校对象：`work/scripts/EP05.md`（版本：20 镜头，基于正式事实账本 `work/facts/EP05.yaml`）
- 依据标准：`docs/10_REVIEW_CHECKLISTS.md` 第 3 节（技术审校清单）

## 1. 逐镜头事实引用核对

| 镜头号 | 引用事实 ID | 账本等级与状态 | 脚本陈述与数字条件核对 | 结论 |
| --- | --- | --- | --- | --- |
| S01 | F05-01, F05-02, F05-21 | E / verified | 4.0 毫秒前向 vs 1.5 毫秒后处理，传统同步调度 24.6% 空泡，ZOS 让 CPU 晚一步，核验一致 | **通过** |
| S02 | G-01 | A / verified | 代码版本固定在 commit 9bd9cf2，标题卡与副标题准确无误 | **通过** |
| S03 | F05-01, F05-02 | A / verified | 同步循环 sample_end_evt.synchronize 阻塞挂起 CPU，1.5 毫秒调度空闲，机理吻合 | **通过** |
| S04 | F05-01, F05-05 | A / verified | ZOS 概念与重叠时序：显卡算第 N 步，CPU 处理第 N-1 步，等待点后移至上上轮采样 | **通过** |
| S05 | F05-03 | A / verified | execute_model_step 四段式骨架：Forward(curr) → Post(prev) → Sample(curr) → Post(curr)延后 | **通过** |
| S06 | F05-04 | A / verified | 边界声明：is_prompt 强制同步并排空流水线，prefill 之后首个 decode 步无重叠 | **通过** |
| S07 | F05-06 | A / verified | 难题一引出：CPU 滞后一步导致第 N+1 步输入 token 未知，因果矛盾阐释严密 | **通过** |
| S08 | F05-06 | A / verified | TileLang 内核 gather_input_ids_zos 在 GPU 就地切片组装，CPU 对存量行写入 0 字节 | **通过** |
| S09 | F05-07 | A / verified | batch 每步按 get_len() 降序重排，CPU 生成 remap 映射表防止张量索引错位 | **通过** |
| S10 | F05-08 | A / verified | 难题二引出：第 N 步生成 EOS 时 CPU 不知情，第 N+1 步多跑一次额外 forward | **通过** |
| S11 | F05-08, F05-21 | E / verified | 代价天平：500 token 下多跑 1 步浪费 0.2% 算力，换取消除 24.6% 空泡与 30% 吞吐提升 | **通过** |
| S12 | F05-09, F05-11 | A / verified | 乐观推进 advance_optimistically 与真实接受 commit_processed_tokens 回填，按最大 q 防御 | **通过** |
| S13 | F05-10, F05-15 | A / verified | DSpark 变长投机分工：CPU 查延迟曲线锁定总预算 best_bsz，GPU 按置信度切分并 D2H | **通过** |
| S14 | F05-12 | A / verified | LCFS 最短输出优先，显存超限牺牲最老请求，默认 stop_preempted_request=True 直接终止 | **通过** |
| S15 | F05-13 | A / verified | DP 组步型共识：每 70 步 ALL 投票，每 100 步 ANY 投票防饿死，单步禁混合 batch | **通过** |
| S16 | F05-14 | A / verified | 源码核验：文档 compute_quota_limit 二次模型全仓 0 匹配，FlopsEstimator 仅打日志 | **通过** |
| S17 | F05-16, F05-17 | A / verified | DeferredRelease 延迟一轮回收资源，终点显式调用 flush_inflight_reqs 补做后处理 | **通过** |
| S18 | F05-18, F05-19, F05-20 | B / verified | 工业全景：文档注明借鉴 NanoFlow 与 SGLang，vLLM/SGLang 默认异步调度对照 | **通过** |
| S19 | F05-01, F05-06, F05-08, F05-21 | E / verified | 三句话总结高度提炼，公布暂停题标准答案（多跑一步后丢弃，换取最大吞吐） | **通过** |
| S20 | G-02 | B / verified | 从调度流水线过渡到显存管理，自然预告 EP06 KV 与状态缓存 | **通过** |

## 2. 审查项合规清单

- [x] **事实引用覆盖**：所有 20 个镜头均声明了事实 ID，全部引自 `work/facts/EP05.yaml` 或 `GLOBAL.yaml`，0 假事实。
- [x] **开源边界标注**：S06、S14、S16 明确标明开源版边界（Prefill 纯同步、抢占直接终止、二次配额在文档而未开源），完全契合 Master Spec 规范。
- [x] **无运行声称**：没有出现任何“我们跑过 DeepInfer”的不实陈述，所有性能与空泡数据均标明是基于典型参数的量化推导或官方公布数据。
- [x] **数字条件严密**：S01、S03、S11、S15 等出现的数字均标注了限定条件（4.0ms 与 1.5ms 假定、500 token 生成、70/100 步计数器）。
- [x] **代码路径行号准确**：引用的文件路径（`worker.py`、`zos.cpp`、`scheduler.hpp`、`gather_input_ids_zos.py`、`mtp_varlen.hpp` 等）与源码行号完全对应。

## 3. 结论

**审校结论：放行（PASS）**。技术事实链条闭环无瑕疵，完全满足 G5 关卡要求。
