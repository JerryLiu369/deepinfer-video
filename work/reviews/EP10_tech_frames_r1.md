# EP10 关键帧技术核对记录 · 第 1 轮

- 审校者：tech-reviewer
- 被审对象：`work/build/EP10/keyframes/`
- 依据：`work/facts/EP10.yaml`、代码路径与数据准确性

## 问题表

| # | 位置（镜头号 + 关键帧文件名） | 类型 | 问题 | 建议或正确内容 | 级别 |
| --- | --- | --- | --- | --- | --- |
| 1 | S04 `EP10-S04_cue-sf.png` | 屏幕技术核对 | 缩放因子打包格式：int32（4x UE8M0）vs int16（2x UE8M0） | 确证无误，符合 `DeepGEMM` 与 `DeepGEMM-Ascend` 规范 | 建议 |
| 2 | S06 `EP10-S06_cue-sass.png` | 屏幕数字核对 | 5%–10% 与 ≤ 5% 标注精确 | 确证无误，符合 `inference_deployment_qa.md:235` | 建议 |
| 3 | S14 `EP10-S14_cue-assert.png` | 代码路径行号 | `runtime_config.py:56` 引用准确 | 确证无误，行号与源码 `@9bd9cf2` 完全一致 | 建议 |
| 4 | S18 `EP10-S18_cue-gates.png` | 回归指标核对 | 60 个 float 全等指纹与 max_kl = 0.0 | 确证无误，符合 `test_offline_inference.py` 与 `test_kl.py` | 建议 |

统计：错误 0 条；不准确 0 条；建议 4 条

## 逐镜头核对

| 镜头 | 屏幕技术内容与数字 | 事实依据 | 代码路径/行号核查 | 结论 |
| --- | --- | --- | --- | --- |
| S01 | 相同 Prompt/Seed，第 40 步产生词分叉 | F10-06 | 浮点非结合律推导 | 通过 |
| S02 | 集号第十集，Decode 与输出解析站 | — | 全局流程图定位 | 通过 |
| S03 | 5 大外部库（FlashMLA, DeepGEMM, DeepEP, TileKernels, DeepSelect） | F10-01 | README.md:23 | 通过 |
| S04 | scripts/build_vendor.sh 同名镜像，int32 vs int16 | F10-02, F10-04 | scripts/build_vendor.sh:7-22 | 通过 |
| S05 | 43 个同名工厂，ops.py 动态重导出 | F10-03, F10-04 | ops.py:13-32 | 通过 |
| S06 | 缺少手写 SASS，解码慢 5-10%，端到端 ≤5% | F10-05 | inference_deployment_qa.md:233-237 | 通过 |
| S07 | (a+b)+c != a+(b+c)，1 ulp 舍入漂移 | F10-06 | IEEE 754 浮点累加 | 通过 |
| S08 | DEEPINFER_BATCH_INVARIANT=1，关闭 split-KV | F10-07 | sparse_decode.cpp:220-223 | 通过 |
| S09 | 禁 cuBLASLt，mega-gate split-K=1，关多次归约 | F10-07 | gemm.hpp:519, mega_gate.hpp:110 | 通过 |
| S10 | 一行一 CTA，2^31 定点直方图求阈值 | F10-08, F10-09 | fused_sample.py:36-122 | 通过 |
| S11 | sample_positions = seqlen_k，绝对物理序号 | F10-10 | prepare_sample.cpp:198-206 | 通过 |
| S12 | 3p+0, 3p+1, 3p+2 三独立流，草稿 +1000000007 | F10-11 | fused_sample.py:392-486 | 通过 |
| S13 | extra_budget 全局排名，ENABLE_MTP_VARLEN=0 回退 | F10-12 | schedule_mtp_varlen.py:17-98 | 通过 |
| S14 | NVIDIA 端到端承诺 vs 昇腾 assert 拦截 | F10-13 | runtime_config.py:56-63 | 通过 |
| S15 | 上游 xgrammar + ThreadPoolExecutor 异步编译 | F10-14, F10-17 | compiler.py:6-7, so_matcher_builder.py:29 | 通过 |
| S16 | 16 KB pinned bitmask，专用流 H2D，TileLang -inf | F10-15 | matcher.py:36-45, sampler.py:320 | 通过 |
| S17 | 一次预推 6 份掩码，matcher.rollback(2) 回滚 | F10-16, F10-17 | matcher.py:206-232 | 通过 |
| S18 | 60 个 float PPL 指纹，max_kl=0.0，AIME 99.9% 生产条件 | F10-18, F10-19 | test_offline_inference.py, eval/README.md | 通过 |

## 总结（三句话：最需要改的地方）

1. 关键帧上展示的全部公式、数字、硬件格式、代码路径与行号 100% 真实准确。
2. 屏幕信息密度适中，角标与代码标注规范。
3. 技术审校全票通过。
