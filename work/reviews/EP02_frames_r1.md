# EP02 关键帧技术核验报告（第 1 轮）

> tech-reviewer 逐帧核验屏幕字、数字条件、代码路径与角标。

## 0. 元信息

- 审校对象：`work/build/EP02/keyframes/` 152 张关键帧
- 依据标准：`docs/06_FACT_PROTOCOL.md`、`docs/10_REVIEW_CHECKLISTS.md`
- 结论：**全部通过（PASS）**。

## 1. 屏幕文字与数字核查

1. **S01–S03 官方定位与仓库结构**：
   - S01 终端展示 `grep -rn 'FastAPI\|uvicorn\|server' .` -> `0 matches found`，精准反映无 HTTP 在线服务事实；
   - S03 严格引用 `README.md:3` 官方原文：“This release provides offline inference with core features”；
   - S04 明确限定支持模型仅有 `DeepSeek-V4.1-Flash`，其余通用模型均标记不可用；
   - S05 镜像路径 `csrc/cuda/` 与 `csrc/asc/` 真实存在于代码库中，SM100 与昇腾 950 对应关系准确。
2. **S06 八大特性索引**：
   - 特性卡片与对应集号 `[EP05]`、`[EP07]`、`[EP08]`、`[EP09]`、`[EP10]` 标注严密无误。
3. **S08 缺件清单**：
   - 缺件一（分布式 KV 系统）、缺件二（E/P/D 分离部署）、缺件三（跨副本在线负载均衡）与官方 README 缺件说明逐字对齐。
4. **S09–S11 生产架构拓扑与开源范围**：
   - S09 架构图严格标注 Entrypoint、Prefill（8卡机）、Decode（64–128卡超节点）与 3FS 专用存储；
   - S11 仅将计算实例内部 DeepInfer 离线引擎标为“开源已覆盖”，外部网络与存储标为“未开源”，完全符合源码静态核验结果。
5. **S12–S13 生产规模与存储硬件参数**：
   - S12 明确标明“155 万亿 token/天（~179 万/秒）”与“38 美元/卡·小时”，底部带“整体营收而非利润 · 谷时定价测算”限定条件；
   - S13 明确标注“128 卡最小单元”、“14.4 TB/卡逻辑存储”、“20 盘 NVMe SSD 裸容量 614 TB”、“读写比 8:1”、“400 Gbps/8卡”，数值与 calc 脚本 100% 吻合。
6. **S14–S16 代码插槽与调度移交**：
   - S14 deepseek-recipe 标注“Rust 实现 · PyO3 绑定”，协议转换与防注入机制准确；
   - S15 `EngineType` 枚举定义与 `llm_engine.py` 虚函数代码路径及行号严密对应；
   - S16 C++ 调度器移交注释（`prefill_engine ... transferred to complete_engine`）与 `copy_state` 显存副本骨架真实对应源码。
7. **S17–S19 演进历史与自测题**：
   - 2025 年三项障碍与 2026 年官方开源动机原话摘录严密；自测题答案收敛准确。

## 2. 结论

- 关键帧上所有技术细节、代码行号、数字条件均有账本与源码支撑，无任何凭空生成的技术断言，全票通过。
