# 术语表

> showrunner 维护。种子来自 `docs/01_SERIES_BIBLE.md` 第 7 节。脚本、屏幕字、观看手册全系列以这里为准；新术语在首次出现的那一集锁定方案时加入。读法需要特殊处理的，同步到 `tools/lexicon.yaml`。

| 写法（字幕） | 读法（配音） | 一句话 | 首次出现 | 备注 |
| --- | --- | --- | --- | --- |
| prefill | prefill | 一次性处理整段输入，算出它的 KV | EP01 | |
| decode | decode | 一步一步生成输出 token | EP01 | |
| KV cache | K V cache | 注意力里每个 token 的 key 和 value，存下来给后面的 token 复用 | EP01 | |
| SWA | S W A | 滑动窗口注意力：每个 token 只看最近 128 个 token | EP03 | |
| 有界重放 | 有界重放 | 只重算最后一小段 token 来近似重建 SWA KV | EP07 | |
| | | | | |

## 不用的说法

| 不用 | 改用 | 原因 |
| --- | --- | --- |
| 暴力截断 | 截断 / 有界重放 | 书稿错误说法，带情绪 |
