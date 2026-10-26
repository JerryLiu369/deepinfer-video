# EP06 技术审校报告（第 1 轮）

> 角色：tech-reviewer。规范依据：`docs/00_MASTER_SPEC.md` 第 4 节 P5、`docs/10_REVIEW_CHECKLISTS.md`。
> 输入：`work/scripts/EP06.md`、`work/facts/EP06.yaml`、源码 deepseek-ai/DeepInfer @ 9bd9cf2。

## 0. 审校结论

**全票通过（PASS）**。脚本严格对齐事实账本与源码物理实现，0 处“错误”级硬伤，0 处未核验事实调用，量化公式与代码边界完全吻合。

## 1. 逐镜头核验清单

| 镜头号 | 引用事实 ID | 账本状态 | 范围标注 (Scope) | 数字与公式核查 | 审校意见 |
| --- | --- | --- | --- | --- | --- |
| S01 | F06-02, F06-08 | verified | oss | 块状 KV 变长 vs 状态缓存定长对比 | 符合源码实现，通过 |
| S02 | G-01 | verified | oss | EP06 片头卡（时长 5s） | 规范合规，通过 |
| S03 | F06-02, F06-07, F06-08 | verified | oss | 40层全SWA，仅4层块状KV，双分配器独立 | 与 EP03 模型设定完全一致，通过 |
| S04 | F06-02, F06-06 | verified | oss | 128 压缩前 token 分页块，FIFO 链表管理 | 与 `block_manager.hpp` 一致，通过 |
| S05 | F06-04 | verified | oss | 物理块结构提问（Q行） | 语气与结构合规，通过 |
| S06 | F06-04 | verified | oss | FP4 主KV 288B (256+32), MXFP8 528B, Index 68B, SWA 528B | 与 `cache_common.py` 完全吻合，通过 |
| S07 | F06-02, F06-03 | verified | oss | 扁平一维字节带，层内 32B，整块 lcm(128, 288)=1152B | 与 `cache_engine.py:479-484` 吻合，通过 |
| S08 | F06-05 | verified | oss | `slot = block_id * tokens_per_block + offset`，-1 为 padding | 与 `store_kv_cache.py` 吻合，通过 |
| S09 | F06-08 | verified | oss | StateBlock 内部结构提问（Q行） | 提问契合节拍，通过 |
| S10 | F06-08, F06-13 | verified | oss | 存储区（前20层SWA）在前，丢弃区（后20层+压缩边界）在后 | 与 `cache_engine.py:221-241` 吻合，通过 |
| S11 | F06-09 | verified | oss | 134 = 128 滑窗 + 6 回退预算 (5+1) | 与 `environ.py:128-132` 吻合，通过 |
| S12 | F06-10 | verified | oss | 存储视角 262 环 (134+128)，默认零重排直接内存拷贝 | 与 `cache_engine.py:101-110, 788-797` 吻合，通过 |
| S13 | F06-11, F06-12 | verified | oss | 每序列落盘固定 1,415,040 字节 (20×134×528)，128 整数倍落盘 | 与 `doc/inference_deployment_qa.md:169` 吻合，通过 |
| S14 | F06-01 | verified | oss | 代码到处是 128 的困惑提问（Q行） | 引出 Aha 时刻，通过 |
| S15 | F06-01, F06-03 | verified | oss | 三个 128：块容器 128 token、落盘步长 128 token、硬件 128 字节 | 概念边界完全清晰，通过 |
| S16 | F06-13, F06-14, F06-15 | verified | oss | 90%利用率，扣除 2×StateBuffer，算物理块，80% 启动硬校验 | 与 `base.py:217-246, llm_engine.py:441` 吻合，通过 |
| S17 | F06-06, F06-16 | verified | oss | 开源版零自动前缀缓存，BlockManager 纯 FIFO 链表加引用计数 | 严格区分开源实现与文档宣传，通过 |
| S18 | F06-17 | verified | oss | 显式 fork_seq，pin 块表，首次 decode 写时复制 (COW) 复制末块 | 与 `scheduler.hpp:1082-1121` 吻合，通过 |
| S19 | F06-18, F06-19, F06-20 | verified | mixed | 生产三层存储（HBM/Host/3FS）与 vLLM/SGLang 路线对比 | 准确标注 mixed/doc 属性，通过 |
| S20 | F06-01, F06-08, F06-11, F06-16 | verified | mixed | 三句话回顾与 EP07 SWA 有界重放伏笔 | 总结有力，伏笔准确，通过 |

## 2. 关键代码与数据一致性复核

1. **量化字节数**：`512 // 2 + 512 // 16 = 288`，`512 + 512 // 32 = 528`，`128 // 2 + 128 // 32 = 68`。脚本数值与 `calc/EP06_bytes.py` 实测完全一致。
2. **对齐约束**：`math.lcm(128, 288) = 1152`，`math.lcm(32, 528) = 1056`。脚本数值准确无误。
3. **落盘常数**：`20 * 134 * 528 = 1,415,040 字节`。精确等于 1.3495 MiB，脚本口径严密。
4. **范围标注**：开源代码事实严格标 `oss`，三层存储与横向架构对比标 `mixed`，绝无将未开源的 3FS 客户端说成“代码里有”。
