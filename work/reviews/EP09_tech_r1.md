# EP09 技术审校报告（第 1 轮）

> 角色：tech-reviewer。规范依据：`docs/00_MASTER_SPEC.md` 第 4 节 P5、`docs/10_REVIEW_CHECKLISTS.md`。
> 输入：`work/scripts/EP09.md`、`work/facts/EP09.yaml`、源码 deepseek-ai/DeepInfer @ 9bd9cf2、`work/calc/EP09_curves.py`。

## 0. 审校结论

**全票通过（PASS）**。脚本严格对齐事实账本与源码物理实现，0 处“错误”级硬伤，0 处未核验事实调用，所有推断与实测数据均带严格约束条件，开源边界标注准确。

## 1. 逐镜头核验清单

| 镜头号 | 引用事实 ID | 账本状态 | 范围标注 (Scope) | 数字与公式核查 | 审校意见 |
| --- | --- | --- | --- | --- | --- |
| S01 | F09-17, F09-18 | verified / verified_with_caveat | mixed | 60 并发 +5.4% 吞吐，16 并发 -1.5% 吞吐 | 与官方 QA 评测及推导模型完全一致，通过 |
| S02 | - | - | general | EP09 片头卡 | 结构规范，通过 |
| S03 | F09-01, F09-17 | verified | mixed | 默认猜 5 个词 (`DEEPINFER_USE_NEXTN_DECODE=5`)，全验算力代价 | 与源码及官方文档吻合，通过 |
| S04 | F09-02 | verified | general | 传统自回归草稿 N 次串行前向瓶颈 | 理论陈述严谨，通过 |
| S05 | F09-01, F09-02, F09-04 | verified | oss | 1 次前向算 5 个 token，3 层草稿层，目标特征注入 | 与 `dflash.py:230-256` 吻合，通过 |
| S06 | F09-03 | verified | oss | 共享 kv_index 广播展开，块内非因果双向可见 | 与 `get_kv_index.py` 及 `attn.py` 吻合，通过 |
| S07 | F09-05 | verified | oss | 5 步 Markov 矩阵查表修正，半自回归机制 | 与 `dflash.py:290-339` 吻合，通过 |
| S08 | F09-06 | verified | oss | SWA 环形缓冲原地覆盖，无显式截断与释放 | 与 `attn.py:975-990` 吻合，通过 |
| S09 | F09-10, F09-17 | verified | mixed | 接受概率随位置指数衰减，变长剪裁萌芽 | 统计趋势与论文原理一致，通过 |
| S10 | F09-08, F09-09, F09-10 | verified | oss | ConfidenceHead 结构、带温 sigmoid、前缀累乘单调生存概率 | 与 `dflash.py` 及 `scheduler.hpp:1244` 吻合，通过 |
| S11 | F09-11, F09-12, F09-13 | verified | oss | 8 等距桶实测剖面，目标函数：预期接受数 ÷ 步耗时 | 与 `model_runner.py` 及 `mtp_varlen.hpp:228-258` 吻合，通过 |
| S12 | F09-14 | verified | oss | 批内所有请求槽位打平，降序全局竞争，尾巴挤龙头 | 与 `mtp_varlen.hpp:210-214` 吻合，通过 |
| S13 | F09-15 | verified | oss | C++ 同步双队列：N-2 定预算抓桶，N-1 定各请求分配 | 与 `mtp_varlen.hpp:160-207` 吻合，通过 |
| S14 | F09-16 | verified | oss | ZOS 异步下 CPU 定总预算，TileLang GPU 内核现场重排分配 | 与 `worker.py:218-231` 及 `schedule_mtp_varlen.py` 吻合，通过 |
| S15 | F09-17 | verified | doc | 60 并发：验证 5->3.58，接受 3.21，吞吐 +5.4%；16 并发：验证 4.44，吞吐 -1.5% | 与 `doc/inference_deployment_qa.md:245-256` 吻合，通过 |
| S16 | F09-18 | verified_with_caveat | mixed | 16 并发跨 1 桶受固定基线延迟主导；60 并发跨 11 桶算力饱和节省真实时间 | 与 `calc/EP09_curves.py` 计算结果完全吻合，通过 |
| S17 | F09-19, F09-20 | verified | mixed | 总结三大支柱，确定性采样必须关闭变长验证，下集算子预告 | 逻辑严密，出处详实，角标 B 与事实 B 级对齐，通过 |

## 2. 关键代码与数据一致性复核

1. **草稿生成单步性**：`dflash.py:230-256` 确认使用 `[golden_tokens, noise×4]` 拼接为 `(req_cnt, 5)` 张量输入，草稿 3 层各跑 1 次，非因果注意力共享展开的 `kv_index`，代码完全印证单次前向与块长解耦。
2. **前缀累乘数学逻辑**：`scheduler.hpp:1244-1252` 中，`accept_rate *= confidence_data[i][j]`，严格保证了每个请求的接受概率序列单调不增，物理上代表连续前缀全部存活的联合概率。
3. **全局预算竞争机制**：`mtp_varlen.hpp:210` 中 `std::sort(acc_queue_for_bsz.begin(), acc_queue_for_bsz.end(), by_rate_desc)`，候选按接受率全量排序，不受请求边界割裂，高置信度长草稿完全可以跨越其他低置信度请求获得调度名额。
4. **反差谜题曲线计算**：`calc/EP09_curves.py` 严格运行验证：
   - 16 并发：80 token 剪裁至 71 token，减少 9 token，跨桶数为 1，接受率损失 2.4%，因 baseline_ms 固定延迟地板主导，吞吐净收益 -1.5%；
   - 60 并发：300 token 剪裁至 215 token，减少 85 token，跨桶数达 11 桶，时间节省显著，吞吐净收益 +5.4%。
5. **开源与文档边界**：DFlash 与 DSpark 的 C++/CUDA/TileLang 实现均在开源仓库内（A 级），评测数据来自官方 QA（B 级），桶跨度推论标注 caveat（E 级），全集 scope 标注精准无越界。
