"""Lesson 6 lab C: MEASURED error from compressing weights. Computed with real numbers (numpy), on SYNTHETIC weights.

A 1024 x 1024 weight matrix: gaussian, plus 8 'outlier' columns 20x larger (large models are known to have a few such channels, ASSUMED shape here).
We round the weights to int8 or int4 with different scale choices, multiply by 200 random input vectors, and report the relative error of the output:
|W x - W_q x| / |W x|. Lower is better. Bytes per weight are exact. Run: python3 l06_quant_error.py
"""
import numpy as np
rng = np.random.default_rng(2)
W = rng.standard_normal((1024, 1024)).astype('float32'); W[:, rng.choice(1024, 8, replace=False)] *= 20
X = rng.standard_normal((1024, 200)).astype('float32'); ref = W @ X

def quant(W, bits, scale_axis=None, group=None):
    qmax = 2 ** (bits - 1) - 1
    if group:
        Wg = W.reshape(W.shape[0], -1, group); s = np.abs(Wg).max(axis=2, keepdims=True) / qmax
        return (np.round(Wg / s).clip(-qmax, qmax) * s).reshape(W.shape)
    s = np.abs(W).max() / qmax if scale_axis is None else np.abs(W).max(axis=scale_axis, keepdims=True) / qmax
    return np.round(W / s).clip(-qmax, qmax) * s
err = lambda Wq: np.linalg.norm(ref - Wq @ X) / np.linalg.norm(ref)
print(f'{"format":34} {"bytes/weight":>13} {"relative error":>15}')
print(f'{"bf16-like (16 bit)":34} {2:13.2f} {err(W.astype("float16").astype("float32")):15.5f}   (float16 stands in for bf16)')
rows = [('int8, one scale for the whole matrix', 1, quant(W, 8)), ('int8, one scale per row', 1, quant(W, 8, 1)), ('int8, groups of 64', 1 + 4 / 64, quant(W, 8, group=64)),
        ('int4, one scale for the whole matrix', 0.5, quant(W, 4)), ('int4, one scale per row', 0.5, quant(W, 4, 1)), ('int4, groups of 64', 0.5 + 4 / 64, quant(W, 4, group=64))]
for name, b, Wq in rows: print(f'{name:34} {b:13.2f} {err(Wq):15.5f}')
print('(groups add 4 bytes of scale per 64 weights)')
