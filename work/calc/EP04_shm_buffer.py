"""EP04: SHM 控制面广播环形缓冲区与溢出回退计算。

证据来源：
- deepinfer/model_executor/parallel_utils/parallel_state.py:122-124
  MessageQueue.create_from_process_group(self.cpu_cp_group, 1 << 20, 10)
- deepinfer/distributed/shm_broadcast.py:396-404
  overflow = len(serialized_obj) >= self.buffer.max_chunk_bytes
"""

def main():
    chunk_bytes = 1 << 20  # 1 MiB = 1,048,576 字节
    num_chunks = 10
    total_shm_bytes = chunk_bytes * num_chunks
    total_shm_mib = total_shm_bytes / (1024 * 1024)

    print("=== EP04 SHM 广播缓冲区参数计算 ===")
    print(f"每块槽位大小 (max_chunk_bytes): {chunk_bytes:,} 字节 (1 MiB)")
    print(f"槽位数量 (num_chunks): {num_chunks} 块")
    print(f"共享内存总环形区: {total_shm_bytes:,} 字节 ({total_shm_mib:.1f} MiB)")

    typical_msg_size = 256  # 方法名 'execute_model_step' + 字典 kwargs 约 200-300 字节
    headroom = chunk_bytes / typical_msg_size
    print(f"典型 RPC 消息大小: ~{typical_msg_size} 字节")
    print(f"单槽位安全余量: {headroom:,.0f}x 空间容限")
    print("溢出机制: 当序列化载荷 >= 1 MiB 时，buf[0]=1，退回本地 ZMQ/Socket 传输。")

if __name__ == "__main__":
    main()
