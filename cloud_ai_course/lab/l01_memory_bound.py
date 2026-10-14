"""Lesson 1 lab B: MEASURED on this CPU. Why chat speed is set by memory speed.

A chat model makes ONE new token per step, so each layer does a matrix x vector.
That reads every weight once and does almost no arithmetic per byte read.
We measure: (1) memory read speed, (2) matrix x vector time vs matrix size,
(3) what happens when we serve several vectors at once (batching).
One CPU thread, float32, fixed seed. No GPU. The GPU numbers at the end are ARITHMETIC
from vendor specs (notebook, 14 Oct 2026), not measured here.
Run: OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 l01_memory_bound.py
"""
import os, time
os.environ.setdefault('OMP_NUM_THREADS', '1'); os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import numpy as np
rng = np.random.default_rng(0)

def best(fn, reps=7):
    ts = []
    for _ in range(reps):
        t = time.perf_counter(); fn(); ts.append(time.perf_counter() - t)
    return min(ts)

print('== 1. memory read speed (sum of a 512 MB float32 array)')
a = rng.standard_normal(128 * 1024 * 1024, dtype=np.float32)
t = best(lambda: a.sum(), 5); bw = a.nbytes / t / 1e9
print(f'read {a.nbytes/1e6:.0f} MB in {t*1000:.0f} ms  =  {bw:.1f} GB/s')
del a

print('\n== 2. one token = matrix x vector. time follows the bytes read')
print(f'{"matrix":>12} {"MB":>7} {"ms":>7} {"GB/s":>7} {"GFLOP/s":>8}')
for n in [1024, 2048, 4096, 8192]:
    W = rng.standard_normal((n, n), dtype=np.float32); x = rng.standard_normal(n, dtype=np.float32)
    t = best(lambda: W @ x); mb = W.nbytes / 1e6
    print(f'{n:>6}x{n:<5} {mb:7.0f} {t*1000:7.2f} {W.nbytes/t/1e9:7.1f} {2*n*n/t/1e9:8.1f}')

print('\n== 3. batching: 4096x4096 matrix, serve B tokens at once (matrix x matrix)')
n = 4096; W = rng.standard_normal((n, n), dtype=np.float32)
print(f'{"batch":>6} {"ms":>8} {"tokens/s":>10} {"GFLOP/s":>9} {"vs batch 1":>11}')
base = None
for B in [1, 2, 4, 8, 16, 32, 64, 128, 256]:
    X = rng.standard_normal((n, B), dtype=np.float32)
    t = best(lambda: W @ X)
    base = base or t
    print(f'{B:>6} {t*1000:8.2f} {B/t:10.0f} {2*n*n*B/t/1e9:9.1f} {t/base:10.2f}x')

print('\n== 4. ARITHMETIC (vendor specs, not measured): decode step floor = weight bytes / memory bandwidth')
for name, bwtb in [('H100 3.4 TB/s', 3.4), ('H200 4.8 TB/s', 4.8), ('B200 8.0 TB/s', 8.0)]:
    ms = 70e9 / (bwtb * 1e12) * 1000
    print(f'70B in FP8 (70 GB), batch 1, {name}: >= {ms:5.1f} ms/token  (<= {1000/ms:3.0f} tokens/s)')
