#!/usr/bin/env python3
"""Calculate bitmask memory and bandwidth for Structured Output in EP10.

Verifies:
1. Vocab bitmask size per step
2. MTP (5 draft tokens) multi-step bitmask memory
3. High-concurrency host-to-device transfer volume
4. Fixed-point CDF resolution (2^-31)
"""

def main():
    vocab_size = 129280
    uint32_words = (vocab_size + 31) // 32
    bytes_per_mask = uint32_words * 4
    
    print(f"Vocab size: {vocab_size}")
    print(f"Words per mask (uint32): {uint32_words}")
    print(f"Bytes per mask: {bytes_per_mask} B ({bytes_per_mask / 1024:.2f} KB)")
    
    # MTP 5 draft tokens -> 1 main + 5 drafts = 6 masks
    mtp_value = 5
    masks_per_req = mtp_value + 1
    bytes_per_req = masks_per_req * bytes_per_mask
    print(f"\nWith MTP={mtp_value} (1 main + 5 drafts = {masks_per_req} masks):")
    print(f"Bytes per request per step: {bytes_per_req} B ({bytes_per_req / 1024:.2f} KB)")
    
    # 384 concurrent requests (eval max_num_seqs)
    concurrency = 384
    total_bytes = concurrency * bytes_per_req
    print(f"\nAt {concurrency} concurrent requests:")
    print(f"Total H2D transfer per step: {total_bytes / (1024 * 1024):.2f} MB")
    
    # Fixed-point CDF resolution
    scale_bits = 31
    resolution = 1.0 / (1 << scale_bits)
    print(f"\nFixed-point CDF scale: 2^{scale_bits}")
    print(f"Resolution / precision bound: {resolution:.4e}")

if __name__ == "__main__":
    main()
