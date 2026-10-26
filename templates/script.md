# EPxx <标题>
<!-- episode: EPxx | target_min: 15 -->

（给人看的说明，不会被解析。`tone:` 只在冷开场 hook、片头卡 card、代价 cost、限制 caveat、三句话 recap 等镜头写，见 `docs/03_NARRATION_STYLE.md` 第 12 节。格式：`docs/05_FORMATS.md` 第 4 节；文风：`docs/03_NARRATION_STYLE.md`；样板：`examples/ep07_sample/scripts/EP07.md`。写完运行 `python tools/parse_script.py EPxx && python tools/lint_script.py EPxx`。）

## S01 冷开场：<标题>
<!-- shot: S01 | target_s: 30 | facts: Fxx-01 | badge: A | scope: oss | tone: hook -->
**画面**：（给分镜师的画面意图，1–3 句）
**屏幕字**：
- （≤ 20 字，≤ 4 行）
**旁白**：
（每行一个段落。第一句是要点。）[#cue_name]
（数字写成 {1,234|一千二百三十四}。需要停顿时 [pause:0.8]。）
Q：（提问者，一句话，每 3–4 个镜头最多一次）
**备注**：（可选：给审校/分镜的说明；保留 lint 警告的理由）

## S02 片头卡
<!-- shot: S02 | target_s: 5 | facts: - | badge: - | scope: general | tone: card -->
**画面**：段落卡：集号、标题；左下小地图高亮 <站点>。
**屏幕字**：
- 第 x 集 · <标题>
**旁白**：
第 x 集，<标题>。

## S03 本集问题：<标题>
<!-- shot: S03 | target_s: 25 | facts: Fxx-02 | badge: B | scope: doc -->
**画面**：
**屏幕字**：
- 
**旁白**：
（讲"仅文档描述"的内容时，至少说一次"这部分代码没有开源"。）

## 修订记录

| 轮次 | 日期 | 依据 | 改动摘要 | 未采纳的意见及理由 |
| --- | --- | --- | --- | --- |
