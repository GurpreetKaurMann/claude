"""Lesson 6 lab A: MEASURED on this CPU. Prefill vs decode, and what the KV cache saves.

A small transformer written by hand in PyTorch (6 layers, 384 wide, 6 heads, 8,000-word vocabulary, RANDOM weights: we measure speed,
not answer quality). One CPU thread, float32.
Part 1: prefill time for prompts of different lengths (this is the wait before the first word, TTFT).
Part 2: generate 64 new tokens after a 256-token prompt, (a) with a KV cache: each step feeds ONE new token and reuses stored keys and values,
(b) without: each step re-runs the whole sequence from scratch.
Part 3: bytes of KV cache for this model, measured from the real tensors, against the formula 2 x layers x heads x head size x 4 bytes.
Run: python3 l06_decode_kv.py
"""
import time, torch, torch.nn as nn, torch.nn.functional as F
torch.manual_seed(0); torch.set_num_threads(1)
V, D, H, NL = 8000, 384, 6, 6; HD = D // H

class Block(nn.Module):
    def __init__(s):
        super().__init__(); s.qkv = nn.Linear(D, 3 * D); s.o = nn.Linear(D, D); s.up = nn.Linear(D, 4 * D); s.down = nn.Linear(4 * D, D)
        s.n1 = nn.LayerNorm(D); s.n2 = nn.LayerNorm(D)
    def forward(s, x, cache=None):
        B, T, _ = x.shape
        q, k, v = s.qkv(s.n1(x)).view(B, T, 3, H, HD).permute(2, 0, 3, 1, 4)
        if cache is not None and cache[0] is not None: k = torch.cat([cache[0], k], 2); v = torch.cat([cache[1], v], 2)
        new = (k, v)
        a = F.scaled_dot_product_attention(q, k, v, is_causal=(T > 1))
        x = x + s.o(a.transpose(1, 2).reshape(B, T, D))
        return x + s.down(F.gelu(s.up(s.n2(x)))), new

class LM(nn.Module):
    def __init__(s):
        super().__init__(); s.emb = nn.Embedding(V, D); s.blocks = nn.ModuleList([Block() for _ in range(NL)]); s.head = nn.Linear(D, V)
    def forward(s, ids, caches=None):
        x = s.emb(ids); out = []
        for i, b in enumerate(s.blocks):
            x, c = b(x, None if caches is None else caches[i]); out.append(c)
        return s.head(x[:, -1:]), out

m = LM().eval(); n_params = sum(p.numel() for p in m.parameters())
def timed(f, reps=3):
    best = 1e9
    for _ in range(reps):
        t = time.perf_counter(); f(); best = min(best, time.perf_counter() - t)
    return best
print(f'model: {n_params/1e6:.1f}M parameters, {NL} layers, {D} wide (random weights, speed test only)')
with torch.no_grad():
    print('\n== 1. prefill: time to process the prompt (the wait for the first word)')
    print(f'{"prompt tokens":>14} {"prefill ms":>11} {"ms per token":>13}')
    for L in [64, 256, 1024]:
        ids = torch.randint(0, V, (1, L)); t = timed(lambda: m(ids)) * 1000
        print(f'{L:14d} {t:11.1f} {t/L:13.2f}')

    print('\n== 2. generate 64 tokens after a 256-token prompt')
    prompt = torch.randint(0, V, (1, 256)); N = 64
    def with_cache():
        _, c = m(prompt); tok = torch.randint(0, V, (1, 1))
        for _ in range(N): _, c = m(tok, c)
    def without_cache():
        ids = prompt
        for _ in range(N): m(ids); ids = torch.cat([ids, torch.randint(0, V, (1, 1))], 1)
    tc, tn = timed(with_cache, 2), timed(without_cache, 2)
    _, c = m(prompt); t0 = time.perf_counter()
    for _ in range(20): _, c = m(torch.randint(0, V, (1, 1)), c)
    step = (time.perf_counter() - t0) / 20 * 1000
    print(f'with KV cache:    {tc:6.2f} s total  ({N/tc:5.1f} tokens/s)')
    print(f'without a cache:  {tn:6.2f} s total  ({N/tn:5.1f} tokens/s)   -> {tn/tc:.1f}x slower')
    print(f'one decode step with the cache: {step:.1f} ms (context about 276 tokens)')

    print('\n== 3. KV cache size, measured from the real tensors (256-token prompt)')
    _, c = m(prompt); real = sum(k.numel() * k.element_size() + v.numel() * v.element_size() for k, v in c)
    print(f'real tensors: {real:,} bytes = {real/256:,.0f} bytes per token   formula 2 x {NL} x {H} x {HD} x 4 = {2*NL*H*HD*4:,} bytes per token')
