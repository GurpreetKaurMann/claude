"""Lesson 1 lab A: will a model fit on a GPU?  ARITHMETIC, not a benchmark.

Prints (1) weight memory = parameters x bytes per parameter, (2) KV-cache memory
per token and per sequence, (3) which GPU memory sizes can hold the weights.
GPU memory sizes are vendor figures from the notebook (14 Oct 2026), not measured here.
The 70B-class layer/head numbers are an ASSUMED example config (typical GQA shape).
Run: python3 l01_fit_math.py
"""
BYTES = {'BF16': 2.0, 'FP8': 1.0, 'FP4': 0.5}
MODELS = {'8B': 8e9, '70B': 70e9, '405B': 405e9}
GPUS = {'H100 80 GB': 80, 'H200 141 GB': 141, 'B200 192 GB': 192, 'B300 288 GB': 288}

print('== 1. weights = parameters x bytes per parameter (GB, decimal)')
print(f'{"model":6}' + ''.join(f'{p:>9}' for p in BYTES))
for m, n in MODELS.items():
    print(f'{m:6}' + ''.join(f'{n*b/1e9:9.0f}' for b in BYTES.values()))

print('\n== 2. KV cache = 2 x layers x kv_heads x head_dim x bytes, per token')
cfgs = {'assumed 8B-class': (32, 8, 128), 'assumed 70B-class': (80, 8, 128)}
for name, (layers, kvh, hd) in cfgs.items():
    for prec, b in [('BF16', 2), ('FP8', 1)]:
        per_tok = 2 * layers * kvh * hd * b
        seq = per_tok * 8192
        print(f'{name:18} {prec:5} {per_tok:>9,} bytes/token   8,192-token chat = {seq/1e9:5.2f} GB   '
              f'32 chats = {32*seq/1e9:6.1f} GB')

print('\n== 3. does 70B fit? weights + 32 chats of 8,192 tokens (BF16 KV), 20% headroom')
w_fp8 = 70e9 * 1.0
kv = 32 * 2 * 80 * 8 * 128 * 2 * 8192
need = (w_fp8 + kv) * 1.2 / 1e9
print(f'70B FP8 weights {w_fp8/1e9:.0f} GB + KV {kv/1e9:.1f} GB, with headroom = {need:.0f} GB')
for g, cap in GPUS.items():
    print(f'  {g:12} {"fits" if cap >= need else "does NOT fit":14} ({need/cap*100:.0f}% of memory)')
