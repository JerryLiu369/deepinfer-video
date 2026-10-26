# 决策记录

> 所有对规范的偏离、基线变更、P0 校准结果、打回第 3 次时的判断、人类检查点的反馈，都记在这里。只追加，不删改；推翻旧决定时写新条目并引用旧编号。

## 格式

```markdown
### D-001 · 2026-10-25 · <标题>
- 背景：
- 决定：
- 理由：
- 影响的文件 / 集：
- 决定人：showrunner / 委托人（H1–H4）
```

## P0 管线（pipeline-engineer 填写）

- Python / manim / ffmpeg 版本：
- 配音后端与模型：qwen / qwen-audio-3.1-tts-plus（`DV_CHECK_TTS=1 tools/check_env.sh` 结果：）
- 旁白音色：longanhuan_v3.1　　提问者音色：longanlingxin_v3.1
- 连接方式：直连 / 代理（不写地址以外的凭据信息）
- 实测语速（spoken_len/秒）：　　`voices.yaml` 的 qwen `cps` 是否修改：
- 语气预设改动（如有）：
- 需要委托人试听的句子：
- lexicon 改动：
- 代码基线：deepseek-ai/DeepInfer @ 9bd9cf2（2026-10-21）；上游新提交：

## 决定
