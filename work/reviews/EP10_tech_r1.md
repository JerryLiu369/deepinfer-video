# EP10 技术审校记录 · 第 1 轮

- 审校者：tech-reviewer
- 被审对象：`work/scripts/EP10.md`
- 依据：`work/facts/EP10.yaml`、DeepInfer 源码 @ `9bd9cf2`、研究笔记 R10 与 R11

## 问题表

| # | 位置（镜头号 + 原句开头） | 类型 | 问题 | 建议或正确内容（含证据） | 级别 |
| --- | --- | --- | --- | --- | --- |
| 1 | S04 "比如缩放因子在英伟达上把四个 UE8M0 打包为一个 32 位整型" | 事实核对 | 硬件对应关系与类型严格准确 | `platform.py:63,138` 确证 GPU 为 int32、NPU 为 int16，无误 | 建议 |
| 2 | S08 "在默认极速路径下，当候选长度超过六百四十" | 门限核对 | split-KV 触发条件精确性 | `vendor/FlashMLA/csrc/api/sparse_decode.cpp:223` 确认门限为 `topk + extra_topk <= 640` 时不切分，表述准确 | 建议 |
| 3 | S12 "下标三乘位置加零负责正式采样，加一负责拒绝后的残差重采样，加二负责投机接受率检验" | 索引核对 | 随机数子流分配槽位准确性 | `fused_sample.py:392-486` 确证 `3p+0` 采样、`3p+1` 重采样、`3p+2` 检验，无误 | 建议 |
| 4 | S14 "如果在昇腾开启批不变变量，系统会直接报错拦截" | 平台断言 | NPU 批不变支持现状核实 | `runtime_config.py:56-63` 确证 `assert not envs.DEEPINFER_BATCH_INVARIANT`，与 README 一致 | 建议 |

统计：错误 0 条；不准确 0 条；建议 4 条

## 逐镜头核对

| 镜头 | 对应事实 ID | scope 标注 | 角标与证据级别 | 技术断言核对 | 结论 |
| --- | --- | --- | --- | --- | --- |
| S01 | F10-06 | general | A | 浮点非结合律导致相同 Prompt/Seed 因合批产生词分叉 | 通过 |
| S02 | — | general | - | 片头卡，无数字断言 | 通过 |
| S03 | F10-01 | oss | A | 5 大外部内核库定位分工完全吻合 README:23 与代码 | 通过 |
| S04 | F10-02, F10-04 | oss | A | build_vendor.sh 同名镜像与 SF 打包格式吻合 | 通过 |
| S05 | F10-03, F10-04 | oss | A | tilelang_ops 43 个同名工厂与 ops.py 动态重导出吻合 | 通过 |
| S06 | F10-05 | doc | B | 开源 FlashMLA 缺手写 SASS，解码慢 5-10%，端到端 ≤5% 吻合文档 | 通过 |
| S07 | F10-06 | general | A | (a+b)+c != a+(b+c) 浮点加法非结合律物理推导准确 | 通过 |
| S08 | F10-07 | oss | A | split-KV 关断与单 CTA 串行扫完符合代码实现 | 通过 |
| S09 | F10-07 | oss | A | 禁 cuBLASLt、mega-gate 禁 split-K、EP 禁多次归约完全吻合 | 通过 |
| S10 | F10-08, F10-09 | oss | A | 一行一 CTA 与 2^31 定点直方图求截断阈值准确 | 通过 |
| S11 | F10-10 | oss | A | seq_seed 展开与绝对位置 sample_positions=seqlen_k 绑定准确 | 通过 |
| S12 | F10-11 | oss | A | 3p+0/1/2 独立流与 MTP 偏移 1000000007 准确 | 通过 |
| S13 | F10-12 | oss | A | 变长 MTP 全批排名竞争 extra_budget 破坏独立性分析准确 | 通过 |
| S14 | F10-13 | mixed | A | 昇腾采样器同构但缺批不变算子，端到端仅承诺 NVIDIA 吻合 | 通过 |
| S15 | F10-14, F10-17 | mixed | A | 上游 xgrammar + 异步 CPU 线程池 + 开源/生产形态差异准确 | 通过 |
| S16 | F10-15 | oss | A | 16 KB pinned bitmask、专有流 H2D、TileLang -inf 填充准确 | 通过 |
| S17 | F10-16, F10-17 | oss | A | 预推 k+1 掩码、matcher.rollback 回退与 trigger 引导准确 | 通过 |
| S18 | F10-18, F10-19 | mixed | B | 60 个 float PPL 指纹、KL=0、AIME 99.9% 生产路径真相准确 | 通过 |

## 总结（三句话：最需要改的地方）

1. 事实引用链条 100% 闭环，19 条事实账本条目与 18 个镜头严格对应，无任何无依据的技术编造。
2. 数字与硬件条件标注完备，准确区分了开源代码实现与官方问答文档描述。
3. 双硬件差异阐述客观严谨，既讲清了同名镜像的精妙工程，也明确指出了昇腾平台暂未支持端到端批不变性的硬断言约束。
