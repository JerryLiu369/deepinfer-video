# EP04 技术审校记录（第 1 轮）

- 审校人：tech-reviewer
- 审校时间：2026-10-26
- 审校对象：`work/scripts/EP04.md`（版本：21 镜头，基于正式事实账本 `work/facts/EP04.yaml`）
- 依据标准：`docs/10_REVIEW_CHECKLISTS.md` 第 3 节（技术审校清单）

## 1. 逐镜头事实引用核对

| 镜头号 | 引用事实 ID | 账本等级与状态 | 脚本陈述与数字条件核对 | 结论 |
| --- | --- | --- | --- | --- |
| S01 | F04-01, F04-03, F04-04 | A / verified | 4.7 万行 Python、23 个派生文件（12.4%）、49.5% 算子层、C++ 调度核心，与代码统计完全吻合 | **通过** |
| S02 | G-01 | A / verified | 代码版本固定在 commit 9bd9cf2，标题卡准确无误 | **通过** |
| S03 | F04-01, F04-02 | A / verified | 三层架构划分（Python 47,172 行、csrc 5,909 行、底层算子），纯 Host 侧调度 | **通过** |
| S04 | F04-03, F04-23 | A / verified | 算子 23,331 行（49.5%）、双端各 30 个镜像文件、昇腾侧多 2,450 行，数字精确无误 | **通过** |
| S05 | F04-04 | A / verified | 23 个 Derived from vLLM 文件、6,817 行、占比 12.4%、全部位于胶水层，核验一致 | **通过** |
| S06 | F04-05, F04-06 | A / verified | v0.2.x 骨架指纹（create_engine_configs 4 元组、探测命名）与 shm_broadcast (v0.6.3) 补丁 | **通过** |
| S07 | F04-07, F04-08 | A / verified | 单模型注册（DeepseekV41ForCausalLM）、无 AsyncLLM/流式、profile_server 探针定位明确 | **通过** |
| S08 | F04-09, F04-25 | B / verified | offline_inference.py 入口、单机 8 卡 EP8 默认配置、硬件常量硬编码 SM100 条件标明清晰 | **通过** |
| S09 | F04-10 | A / verified | 预分词为 np.int32、封装为 C++ Sequence、进入底层对象池，边界划分准确 | **通过** |
| S10 | F04-11, F04-24 | A / verified | 单引擎管 cp_size 卡、Driver 独占主控、Worker 派生子进程、顶层禁导 torch 规约准确 | **通过** |
| S11 | F04-12 | A / verified | 无张量并行（TP）通信组、仅保留 CP/DP/EP，定位说明严谨 | **通过** |
| S12 | F04-13 | A / verified | 10×1MB 环形 SHM、单向广播 (method, kwargs)、无返回值，参数核验准确 | **通过** |
| S13 | F04-14 | A / verified | Scheduler::schedule、全程释放 GIL、管理 SequenceMetadataPool，逻辑吻合 | **通过** |
| S14 | F04-15 | A / verified | _dp_allreduce 两轮投票统一步调为 prefill 或 decode、防止 EP 死锁，机理清晰 | **通过** |
| S15 | F04-16 | A / verified | 空闲 rank 强行运行 _placeholder_seq_metadata 陪跑步，保障全网 EP 对齐 | **通过** |
| S16 | F04-17 | A / verified | execute_model_step 固定时序：Forward(N) → Post(N-1) → Sample(N) → 条件推迟 | **通过** |
| S17 | F04-18, F04-19 | A / verified | 乐观推进（advance_optimistically）与事后回填（commit_processed_tokens），C++ 只算 offset/len | **通过** |
| S18 | F04-20 | A / verified | CUDA Graph 仅覆盖 decode 前向、2 的幂加步长 8 阶梯分桶、bisect_left 向上查找 | **通过** |
| S19 | F04-21, F04-22 | A / verified | Driver 独占采样、从属返回空 SamplerOutput、RequestOutputPool 返回 uint64 句柄 | **通过** |
| S20 | F04-23, F04-24 | A / verified | platform.py 抽象与 ops.py 派发，_so/<tag> 软链归档，顶层严禁 torch 导入 | **通过** |
| S21 | F04-01, F04-12, F04-17 | A / verified | 三句话总结严密支撑，下集预告衔接准确 | **通过** |

## 2. 审查项合规清单

- [x] **事实引用覆盖**：所有镜头均声明了事实 ID，数字与技术断言 100% 来自 `work/facts/EP04.yaml` 或 `GLOBAL.yaml`。
- [x] **开源边界标注**：S07 明确强调“生产所需的分布式缓存与负载均衡均不在本仓库中”，符合 Master Spec 铁律。
- [x] **无运行声称**：没有任何“我们跑过 DeepInfer”的话术，S08 明确说明“普通消费级单卡直接运行，系统会因找不到硬件算力而报错”。
- [x] **数字条件严密**：S04、S05、S08、S12、S18 等出现的每个数字均带有限定条件（物理行数、排除 vendor CUTLASS、单机 8 卡 EP8 假定、10×1MB 环形队列）。
- [x] **代码路径行号准确**：引用的文件路径（`offline_inference.py`、`llm_engine.py`、`scheduler.hpp`、`worker.py` 等）经源码精确核验。

## 3. 结论

**审校结论：放行（PASS）**。脚本技术事实严密准确，完全符合 Master Spec 与事实协议规范。
