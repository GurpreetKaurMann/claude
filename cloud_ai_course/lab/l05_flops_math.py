"""Lesson 5 lab D: ARITHMETIC. How many GPU-hours, and what does the network cost per step?

Rule: training FLOPs ~ 6 x N (parameters) x D (training tokens). GPU-hours = FLOPs / (peak FLOP/s x MFU x 3600).
H100 dense BF16 peak 989 TFLOP/s (vendor), MFU 40% (the notebook says well-tuned dense runs reach about 35 to 45%), price $2 per GPU-hour is ASSUMED.
Ring all-reduce sends about 2 x (message size) per GPU. Bandwidths are vendor figures: 50 GB/s scale-out per GPU, about 450 GB/s NVLink 4 each way.
Run: python3 l05_flops_math.py
"""
PEAK, MFU, PRICE = 989e12, 0.40, 2.0
print('== 1. GPU-hours = 6 x N x D / (peak x MFU x 3600)')
print(f'{"model":10} {"tokens":>8} {"FLOPs":>10} {"GPU-hours":>11} {"days on 1,024 GPUs":>19} {"cost at $2":>12}')
for name, n, d in [('1B', 1e9, 0.1e12), ('7B', 7e9, 2e12), ('70B', 70e9, 1.4e12)]:
    fl = 6 * n * d; gh = fl / (PEAK * MFU * 3600)
    print(f'{name:10} {d/1e12:6.1f}T {fl:10.2e} {gh:11,.0f} {gh/1024/24:19.1f} ${gh*PRICE:11,.0f}')
print('\n== 2. reverse check: Llama 3 had 419 unexpected interruptions in 54 days (notebook, reported)')
print(f'one interruption every {54*24/419:.1f} hours')
print('\n== 3. ring all-reduce of bf16 gradients, 7B model: 14 GB message, about 2 x 14 = 28 GB sent per GPU per step')
for name, bw in [('scale-out 50 GB/s', 50), ('NVLink 4, 450 GB/s', 450)]:
    print(f'{name:22} {28/bw:6.2f} s per step if not overlapped with compute')
print('70B at 50 GB/s:', f'{2*140/50:.1f} s per step (140 GB of bf16 gradients)')
