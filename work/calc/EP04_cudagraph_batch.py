"""EP04: CUDA Graph Batch 分桶与检索推导。

证据来源：
- deepinfer/worker/cuda_graph_runner.py:41-51
- deepinfer/worker/model_runner.py:76-79
- deepinfer/environ.py:155 (DEEPINFER_CUDAGRAPH_BATCH_SIZE_INTERVAL = 8)
"""
import bisect

def generate_batch_sizes(max_batch_size: int, interval: int = 8) -> list[int]:
    batch_sizes = []
    size = 1
    while size < interval:
        batch_sizes.append(size)
        size *= 2
    batch_sizes.extend(range(interval, max_batch_size + 1, interval))
    return batch_sizes

def main():
    interval = 8
    max_num_seqs = 4
    nextn = 5
    max_tokens = max_num_seqs * (1 + nextn)  # 4 * 6 = 24

    buckets = generate_batch_sizes(max_tokens, interval)
    print("=== EP04 CUDA Graph Batch 分桶计算 ===")
    print(f"参数: max_num_seqs={max_num_seqs}, nextn={nextn}, interval={interval}")
    print(f"最大 batch tokens: {max_tokens}")
    print(f"生成的分桶阶梯 (batch_sizes): {buckets}")

    test_queries = [1, 2, 3, 5, 8, 12, 16, 21, 24]
    print("\n检索测试 (bisect_left 向上取整对齐):")
    for q in test_queries:
        idx = bisect.bisect_left(buckets, q)
        matched = buckets[idx] if idx < len(buckets) else None
        pad = matched - q if matched else 0
        print(f"  total_q={q:2d} tokens -> 选用分桶={matched:2d} (填充 pad 序列数={pad})")

if __name__ == "__main__":
    main()
