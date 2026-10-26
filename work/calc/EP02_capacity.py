#!/usr/bin/env python3
"""EP02 Capacity, Throughput, and Cluster Sizing Calculations.

Computes cluster scale, 3FS storage sizing, daily throughput rate,
and bandwidth budgets cited in EP02 fact ledger (work/facts/EP02.yaml).
All formulas use standard library python.
"""


def calculate_throughput_metrics():
    # Official claim: 155 trillion tokens / day
    tokens_per_day = 155e12
    seconds_per_day = 86400
    aggregate_tokens_per_sec = tokens_per_day / seconds_per_day  # tokens/s

    # Revenue claim: $38 per GPU-hour (valley pricing)
    revenue_per_gpu_hour = 38.0
    revenue_per_gpu_day = revenue_per_gpu_hour * 24.0

    return {
        "tokens_per_day": tokens_per_day,
        "aggregate_tokens_per_sec": aggregate_tokens_per_sec,
        "revenue_per_gpu_hour": revenue_per_gpu_hour,
        "revenue_per_gpu_day": revenue_per_gpu_day,
    }


def calculate_cluster_and_storage_sizing():
    # Smallest efficient deployment unit: 64 Prefill GPUs + 64 Decode GPUs = 128 GPUs
    prefill_gpus_per_unit = 64
    decode_gpus_per_unit = 64
    total_gpus_per_unit = prefill_gpus_per_unit + decode_gpus_per_unit

    # Logical KV storage ratio: ~14.4 TB per online GPU
    logical_storage_per_gpu_tb = 14.4
    logical_storage_per_unit_tb = total_gpus_per_unit * logical_storage_per_gpu_tb  # TB

    # 3FS Storage server hardware configuration
    # 20 SSDs per server, each 30.73 TB NVMe SSD
    ssds_per_server = 20
    ssd_capacity_tb = 30.73
    raw_server_capacity_tb = ssds_per_server * ssd_capacity_tb  # 614.6 TB

    read_bandwidth_gb_s = 40.0
    write_bandwidth_gb_s = 5.0
    read_write_ratio = read_bandwidth_gb_s / write_bandwidth_gb_s  # 8:1

    # Number of raw storage servers needed for 1 unit (128 GPUs, logical ~1843.2 TB)
    # Note: 1843.2 / 614.6 = 3.0 servers (raw logical equivalent, physical is larger due to 10+2 EC)
    servers_needed_for_unit = logical_storage_per_unit_tb / raw_server_capacity_tb

    return {
        "total_gpus_per_unit": total_gpus_per_unit,
        "logical_storage_per_gpu_tb": logical_storage_per_gpu_tb,
        "logical_storage_per_unit_tb": logical_storage_per_unit_tb,
        "raw_server_capacity_tb": raw_server_capacity_tb,
        "read_write_ratio": read_write_ratio,
        "servers_needed_for_unit": servers_needed_for_unit,
    }


def calculate_network_bandwidth_budget():
    # 400 Gbps per 8 GPUs
    bandwidth_gbps_per_8_gpus = 400.0
    bandwidth_gbps_per_gpu = bandwidth_gbps_per_8_gpus / 8.0  # 50.0 Gbps/GPU

    return {
        "bandwidth_gbps_per_8_gpus": bandwidth_gbps_per_8_gpus,
        "bandwidth_gbps_per_gpu": bandwidth_gbps_per_gpu,
    }


def calculate_swa_disk_size():
    # SWA KV store size per sequence:
    # 20 layers x 134 tokens x 528 bytes (MXFP8)
    layers = 20
    tokens_stored = 134  # 128 window + 6 extra ring positions
    bytes_per_token = 528  # MXFP8 format
    bytes_per_seq = layers * tokens_stored * bytes_per_token
    mib_per_seq = bytes_per_seq / (1024 * 1024)

    return {
        "bytes_per_seq": bytes_per_seq,
        "mib_per_seq": mib_per_seq,
    }


def main():
    tp = calculate_throughput_metrics()
    print("=== Throughput & Revenue Metrics ===")
    print(f"Daily Tokens: {tp['tokens_per_day']:.1e} tokens/day (155万亿)")
    print(f"Aggregate Rate: {tp['aggregate_tokens_per_sec']:.2f} tokens/s (~1.79M tokens/s)")
    print(f"Revenue per GPU-Hour: ${tp['revenue_per_gpu_hour']:.2f} (valley pricing)")
    print(f"Revenue per GPU-Day: ${tp['revenue_per_gpu_day']:.2f}")

    cs = calculate_cluster_and_storage_sizing()
    print("\n=== Cluster & 3FS Storage Sizing ===")
    print(f"Smallest Unit GPUs: {cs['total_gpus_per_unit']} (64P + 64D)")
    print(f"Logical Storage per GPU: {cs['logical_storage_per_gpu_tb']} TB")
    print(f"Logical Storage per 128-GPU Unit: {cs['logical_storage_per_unit_tb']:.1f} TB (~1.84 PB)")
    print(f"Single 3FS Server Raw Capacity: {cs['raw_server_capacity_tb']:.1f} TB (20 x 30.73 TB)")
    print(f"Single Server Read/Write Ratio: {cs['read_write_ratio']:.1f}:1 (40 GB/s read / 5 GB/s write)")
    print(f"Raw Servers per 128-GPU Unit: {cs['servers_needed_for_unit']:.2f} servers (before EC & watermark)")

    net = calculate_network_bandwidth_budget()
    print("\n=== Network Bandwidth Budget ===")
    print(f"Cross-DC Bandwidth per 8 GPUs: {net['bandwidth_gbps_per_8_gpus']} Gbps")
    print(f"Cross-DC Bandwidth per GPU: {net['bandwidth_gbps_per_gpu']} Gbps")

    swa = calculate_swa_disk_size()
    print("\n=== SWA KV Store Size ===")
    print(f"SWA State per Sequence: {swa['bytes_per_seq']} bytes ({swa['mib_per_seq']:.2f} MiB)")


if __name__ == "__main__":
    main()
