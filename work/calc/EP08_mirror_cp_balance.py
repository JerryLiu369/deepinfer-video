"""EP08 Mirror CP (Zigzag) 因果计算量平衡证明与数值模拟。

依据 deepinfer/model_executor/layers/tilelang_ops/prepare_cp_mirror.py:143-156
与 R08 #23, #24。
"""

def simulate_cp_workload(seq_len=8192, cp_size=4):
    num_blocks = 2 * cp_size
    block_size = seq_len // num_blocks
    
    # Mirror / Zigzag 分配: rank r 获得 block r 和 block (2*cp - 1 - r)
    mirror_workloads = [0] * cp_size
    for r in range(cp_size):
        b1 = r
        b2 = 2 * cp_size - 1 - r
        # 计算可见因果 key 总量: sum_{t=0}^{B-1} (block_idx * B + t + 1)
        w1 = sum(b1 * block_size + t + 1 for t in range(block_size))
        w2 = sum(b2 * block_size + t + 1 for t in range(block_size))
        mirror_workloads[r] = w1 + w2
        
    # 对比朴素顺序连续分块 (Naive Sequential): rank r 获得 block 2*r 和 2*r + 1
    naive_workloads = [0] * cp_size
    for r in range(cp_size):
        b1 = 2 * r
        b2 = 2 * r + 1
        w1 = sum(b1 * block_size + t + 1 for t in range(block_size))
        w2 = sum(b2 * block_size + t + 1 for t in range(block_size))
        naive_workloads[r] = w1 + w2
        
    return mirror_workloads, naive_workloads, block_size

if __name__ == "__main__":
    seq_len = 8192
    cp_size = 4
    mirror, naive, B = simulate_cp_workload(seq_len, cp_size)
    print(f"=== CP 序列因果注意力工作量模拟 (L={seq_len}, CP={cp_size}, 块数=8, 块长={B}) ===")
    print("Rank | Mirror CP 工作量 (Q*K 对) | 朴素顺序切分工作量 (Q*K 对)")
    for r in range(cp_size):
        print(f"  {r}  | {mirror[r]:23d} | {naive[r]:24d}")
    
    mirror_imbalance = (max(mirror) - min(mirror)) / mean if (mean := sum(mirror)/len(mirror)) else 0
    naive_imbalance = max(naive) / min(naive)
    print(f"\nMirror CP 最大/最小工作量偏差: {mirror_imbalance:.6%}")
    print(f"朴素顺序切分最慢卡/最快卡比值: {naive_imbalance:.2f}x")
