from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from manim import *
from manim_lib.dvlib import (
    PREFILL, DECODE, KV, SWA, WARN, EXPERT, DRAFT, GPU, CPU, MUTED,
    T, M, Pill, DVScene, header, Block, TokenRow, number_card,
)

class _E09(DVScene):
    def foot(self, text: str, x: float = 6.4, y: float = -2.25, size: int = 16):
        t = T(text, size, MUTED)
        t.move_to([x, y, 0], aligned_edge=UR)
        return t

class EP09_S01(_E09):
    SHOT = "EP09-S01"
    def construct(self):
        self.add(header("验证与收益的反差谜题", "EP09 · S01 冷开场"))
        box_l = Block("+5.4% 吞吐", color=DECODE, sub="60 并发", w=5.0, h=2.5).move_to([-3.5, 0, 0])
        box_r = Block("-1.5% 吞吐", color=WARN, sub="16 并发", w=5.0, h=2.5).move_to([3.5, 0, 0])
        q = T("?", 120, WARN).move_to([0, 0, 0])
        self.play(FadeIn(box_l), run_time=1.0)
        self.until("p1")
        self.play(FadeIn(box_r), run_time=1.0)
        self.until("p2")
        self.play(FadeIn(q), run_time=0.8)
        self.until("answer")
        self.finish()

class EP09_S02(_E09):
    SHOT = "EP09-S02"
    def construct(self):
        self.add(header("第九集 · 投机解码", "EP09 · S02 片头"))
        self.until("card")
        self.finish()

class EP09_S03(_E09):
    SHOT = "EP09-S03"
    def construct(self):
        self.add(header("全验划算吗？", "EP09 · S03 问题"))
        row = TokenRow(5, DRAFT)
        self.play(FadeIn(row), run_time=0.8)
        self.until("mtp")
        self.play(row.animate.shift(RIGHT*3), run_time=1.0)
        self.until("cost")
        self.finish()

class EP09_S04(_E09):
    SHOT = "EP09-S04"
    def construct(self):
        self.add(header("传统自回归草稿瓶颈", "EP09 · S04 瓶颈"))
        self.until("serial")
        self.until("loop")
        self.until("cost")
        self.finish()

class EP09_S05(_E09):
    SHOT = "EP09-S05"
    def construct(self):
        self.add(header("DFlash：块并行草稿", "EP09 · S05 DFlash"))
        self.until("block")
        self.until("one")
        self.until("inject")
        self.finish()

class EP09_S06(_E09):
    SHOT = "EP09-S06"
    def construct(self):
        self.add(header("块内双向注意力", "EP09 · S06 注意力"))
        self.until("attn")
        self.until("expand")
        self.finish()

class EP09_S07(_E09):
    SHOT = "EP09-S07"
    def construct(self):
        self.add(header("半自回归 Markov 头", "EP09 · S07 Markov"))
        self.until("markov")
        self.until("loop")
        self.until("semi")
        self.finish()

class EP09_S08(_E09):
    SHOT = "EP09-S08"
    def construct(self):
        self.add(header("零成本回退", "EP09 · S08 回退"))
        self.until("cache")
        self.until("ring")
        self.until("over")
        self.finish()

class EP09_S09(_E09):
    SHOT = "EP09-S09"
    def construct(self):
        self.add(header("变长验证的萌芽", "EP09 · S09 变长"))
        self.until("fixed")
        self.until("drop")
        self.until("dspark")
        self.finish()

class EP09_S10(_E09):
    SHOT = "EP09-S10"
    def construct(self):
        self.add(header("置信度预测与前缀累乘", "EP09 · S10 置信度"))
        self.until("head")
        self.until("temp")
        self.until("mono")
        self.finish()

class EP09_S11(_E09):
    SHOT = "EP09-S11"
    def construct(self):
        self.add(header("硬件吞吐曲线与目标函数", "EP09 · S11 吞吐"))
        self.until("no")
        self.until("profile")
        self.until("func")
        self.finish()

class EP09_S12(_E09):
    SHOT = "EP09-S12"
    def construct(self):
        self.add(header("跨请求全局预算竞争", "EP09 · S12 竞争"))
        self.until("global")
        self.until("queue")
        self.finish()

class EP09_S13(_E09):
    SHOT = "EP09-S13"
    def construct(self):
        self.add(header("同步 C++ 调度器", "EP09 · S13 调度器"))
        self.until("cpp")
        self.until("two")
        self.until("reason")
        self.finish()

class EP09_S14(_E09):
    SHOT = "EP09-S14"
    def construct(self):
        self.add(header("ZOS 异步与 GPU 内核重算", "EP09 · S14 ZOS"))
        self.until("zos")
        self.until("cpu")
        self.until("kernel")
        self.finish()

class EP09_S15(_E09):
    SHOT = "EP09-S15"
    def construct(self):
        self.add(header("并发反差谜题", "EP09 · S15 反差"))
        self.until("puzzle")
        self.until("gain")
        self.until("loss")
        self.finish()

class EP09_S16(_E09):
    SHOT = "EP09-S16"
    def construct(self):
        self.add(header("物理根因：桶跨度与延迟地板", "EP09 · S16 物理根因"))
        self.until("calc")
        self.until("flat")
        self.until("step")
        self.until("eleven")
        self.finish()

class EP09_S17(_E09):
    SHOT = "EP09-S17"
    def construct(self):
        self.add(header("总结与下集钩子", "EP09 · S17 总结"))
        self.until("sum")
        self.until("rule")
        self.until("next")
        self.finish()
