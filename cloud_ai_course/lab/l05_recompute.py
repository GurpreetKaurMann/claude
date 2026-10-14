"""Lesson 5 lab B: MEASURED on this CPU. Activation recomputation (gradient checkpointing): memory saved vs time paid.

A stack of 12 blocks (Linear 768 -> 3072 -> GELU -> Linear 3072 -> 768) processes 2,048 tokens. For the backward pass, normal training
keeps every block's internal activations in memory. With checkpointing, only each block's input is kept, and the block's forward pass is
RE-RUN during backward. Each setting runs in its own process so we can read that process's peak memory (ru_maxrss).
Float32, 1 thread, random data. Peak memory includes a few hundred MB for Python and PyTorch themselves. (At 8,192 tokens the time cost vanished in one run, probably memory pressure on a busy shared machine, so we report the stable 2,048-token size.) Run: python3 l05_recompute.py
"""
import sys, time, resource, subprocess

def child(mode):
    import torch, torch.nn as nn
    from torch.utils.checkpoint import checkpoint
    torch.manual_seed(0); torch.set_num_threads(1)
    blocks = nn.ModuleList([nn.Sequential(nn.Linear(768, 3072), nn.GELU(), nn.Linear(3072, 768)) for _ in range(12)])
    x = torch.randn(2048, 768, requires_grad=True)
    best = 1e9
    if mode == 'base':                      # fixed costs only: Python, PyTorch, weights, gradient buffers, no forward pass
        for p in blocks.parameters(): p.grad = torch.zeros_like(p)
        print(f'0 {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f}'); return
    for _ in range(3):
        t = time.perf_counter(); h = x
        for b in blocks: h = checkpoint(b, h, use_reentrant=False) if mode == 'recompute' else b(h)
        h.square().mean().backward(); best = min(best, time.perf_counter() - t)
    print(f'{best:.3f} {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f}')

if len(sys.argv) > 1: child(sys.argv[1]); sys.exit()
print(f'{"setting":24} {"seconds / step":>15} {"peak memory MB":>15}')
res = {}
for mode, label in [('base', 'fixed costs only (no pass)'), ('normal', 'keep all activations'), ('recompute', 'recompute per block')]:
    out = subprocess.run([sys.executable, __file__, mode], capture_output=True, text=True).stdout.split()
    res[mode] = (float(out[0]), float(out[1])); print(f'{label:24} {res[mode][0]:15.3f} {res[mode][1]:15.0f}')
n, r, b = res['normal'], res['recompute'], res['base']
print(f'\nactivation memory = peak - fixed costs: {n[1]-b[1]:.0f} MB kept vs {r[1]-b[1]:.0f} MB recomputed  ({(r[1]-b[1])/(n[1]-b[1]):.2f}x)')
print(f'whole-process peak: {r[1]/n[1]:.2f}x the memory, {r[0]/n[0]:.2f}x the time  (notebook rule of thumb: about +33% compute)')
