"""Lesson 5 lab A: MEASURED bytes of a real (small) model, then ARITHMETIC for big ones.

Part 1 (measured): build a 4-layer model with PyTorch, run ONE training step with the Adam optimiser, and add up the real bytes of
weights, gradients and optimiser state. float32 everywhere (a CPU test), so it is 4 + 4 + 8 = 16 bytes per parameter.
Part 2 (arithmetic): the mixed-precision recipe used on GPUs is bf16 weights 2 + bf16 grads 2 + fp32 master 4 + Adam m 4 + Adam v 4 = 16 bytes.
Part 3 (arithmetic): what ZeRO / FSDP sharding does to the per-GPU share (formulas from the notebook, Oct 2026).
Run: python3 l05_memory_ledger.py
"""
import torch, torch.nn as nn
torch.manual_seed(0); torch.set_num_threads(1)
model = nn.Sequential(*[nn.Sequential(nn.Linear(1024, 4096), nn.GELU(), nn.Linear(4096, 1024)) for _ in range(4)])
n = sum(p.numel() for p in model.parameters())
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
model(torch.randn(8, 1024)).square().mean().backward(); opt.step()
w = sum(p.numel() * p.element_size() for p in model.parameters())
g = sum(p.grad.numel() * p.grad.element_size() for p in model.parameters())
o = sum(t.numel() * t.element_size() for s in opt.state.values() for t in s.values() if torch.is_tensor(t) and t.dim() > 0)
print(f'== 1. MEASURED: {n:,} parameters, one Adam step, float32')
print(f'weights   {w:>12,} bytes  = {w/n:.1f} bytes per parameter')
print(f'gradients {g:>12,} bytes  = {g/n:.1f} bytes per parameter')
print(f'Adam m+v  {o:>12,} bytes  = {o/n:.1f} bytes per parameter')
print(f'total     {w+g+o:>12,} bytes  = {(w+g+o)/n:.1f} bytes per parameter')

print('\n== 2. ARITHMETIC: mixed precision on GPUs = 2 + 2 + (4 + 4 + 4) = 16 bytes per parameter')
print(f'{"model":6} {"training state":>15}')
for name, p in [('7B', 7e9), ('70B', 70e9), ('405B', 405e9)]:
    print(f'{name:6} {p*16/1e9:12,.0f} GB')

print('\n== 3. ARITHMETIC: per-GPU bytes with sharding (N = GPUs sharing the state; K = 12 for Adam)')
print(f'{"method":16} {"7B, 8 GPUs":>11} {"70B, 64 GPUs":>13}')
def row(name, f):
    print(f'{name:16} {f(7e9, 8)/1e9:9.1f}GB {f(70e9, 64)/1e9:11.1f}GB')
K = 12
row('DDP (nothing)', lambda P, N: 16 * P)
row('ZeRO-1', lambda P, N: 2 * P + 2 * P + K * P / N)
row('ZeRO-2', lambda P, N: 2 * P + (2 + K) * P / N)
row('ZeRO-3 / FSDP', lambda P, N: 16 * P / N)

print('\n== 4. MEASURED: LoRA. Freeze the model, train two small matrices per layer (rank r) instead')
class LoRA(nn.Module):
    def __init__(self, base, r):
        super().__init__(); self.base = base
        for p in base.parameters(): p.requires_grad = False
        self.A = nn.Parameter(torch.randn(base.in_features, r) * 0.01); self.B = nn.Parameter(torch.zeros(r, base.out_features))
    def forward(self, x): return self.base(x) + x @ self.A @ self.B
for r in [8, 16]:
    m = nn.Sequential(*[nn.Sequential(LoRA(nn.Linear(1024, 4096), r), nn.GELU(), LoRA(nn.Linear(4096, 1024), r)) for _ in range(4)])
    tr = sum(p.numel() for p in m.parameters() if p.requires_grad); tot = sum(p.numel() for p in m.parameters())
    o2 = torch.optim.Adam([p for p in m.parameters() if p.requires_grad], lr=1e-3)
    m(torch.randn(8, 1024)).square().mean().backward(); o2.step()
    ob = sum(t.numel() * t.element_size() for s in o2.state.values() for t in s.values() if torch.is_tensor(t) and t.dim() > 0)
    print(f'rank {r:2d}: trains {tr:,} of {tot:,} parameters = {tr/tot:.2%} · Adam state {ob/1e6:.1f} MB vs {o/1e6:.1f} MB for full training')
