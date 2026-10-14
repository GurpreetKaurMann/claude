# FINDINGS: Lesson 1 (GPUs and "will it fit")

Machine: shared 4-core Linux box, no GPU, one BLAS thread, float32. Timings are noisy: two full runs agreed on the story (numbers below are run 1, run 2 in brackets where they differ). No API, nothing simulated. Part A is arithmetic; GPU figures are vendor specs from the notebook (14 Oct 2026), not measured.

## l01_fit_math.py (arithmetic)
- Weights GB (decimal): 8B: 16 BF16 / 8 FP8 / 4 FP4. 70B: 140 / 70 / 35. 405B: 810 / 405 / 202.
- KV bytes per token, ASSUMED configs: 8B-class (32 layers, 8 KV heads, head dim 128): 131,072 B BF16, 65,536 B FP8. 70B-class (80 layers, 8 KV heads, 128): 327,680 B BF16, 163,840 B FP8.
- One 8,192-token chat: 70B-class 2.68 GB BF16 / 1.34 GB FP8. 8B-class 1.07 GB / 0.54 GB.
- 32 chats of 8,192 tokens: 70B-class 85.9 GB BF16 KV, 42.9 GB FP8 KV. 8B-class 34.4 GB / 17.2 GB.
- **Surprise:** 70B in FP8 = 70 GB of weights, fits an 80 GB H100 on paper. Add 32 chats (85.9 GB KV) and 20% headroom = 187 GB. H100 80 GB no (234%), H200 141 GB no (133%), B200 192 GB yes (97%), B300 288 GB yes (65%).

## l01_memory_bound.py (MEASURED on this CPU)
- Read speed of a plain 537 MB sum: 7.1 GB/s (7.0). (numpy sum is not a good bandwidth test, quote with care; do not use as headline.)
- Matrix x vector (one token's worth of work), float32:
  - 1024x1024 (4 MB): 0.15 ms, 27 GB/s. 2048 (17 MB): 0.62 ms. 4096 (67 MB): 2.43 ms (2.47), 27.6 GB/s.
  - 8192x8192 (268 MB): 20.35 ms (22.48), 13.2 GB/s (11.9).
  - **Surprise:** 4x the bytes (67 MB to 268 MB) took 8.4x (9.1x) the time. Small matrices sat in the CPU's fast cache; the big one had to come from main memory, at about half the speed. GPUs solve this with HBM, very fast memory next to the chip.
  - Arithmetic done per byte read is tiny: only 6.6 to 13.8 GFLOP/s achieved.
- Batching, 4096x4096 matrix, B tokens at once:
  - B=1: 2.58 ms, 387 tokens/s (390). B=8: 6.87 ms, 1,165 (988). B=64: 18.86 ms, 3,393 (2,860). B=256: 61.24 ms, 4,180 (3,967).
  - B=256 vs B=1: 23.7x (25.2x) the time per step for 256x the tokens, so about 10.8x (10.2x) the tokens per second.
  - Note: batch 2 and 4 jump to about 2.4x batch 1 in time (a different BLAS kernel). Do not tell a story about that.
- Arithmetic from vendor specs: 70B FP8 (70 GB) batch 1, floor per token = bytes / bandwidth: H100 3.4 TB/s 20.6 ms (<= 49 tok/s); H200 4.8 TB/s 14.6 ms (<= 69); B200 8.0 TB/s 8.8 ms (<= 114). A floor, not a benchmark.
