"""Lesson 5 lab C: SIMULATION. The pipeline bubble.

p pipeline stages (GPUs in a chain), m micro-batches per step. GPipe schedule: all forwards, then all backwards. We draw the time grid
(forward and backward both take one slot, a simplification, real backward is about 2x) and COUNT the idle slots, then compare with the
formula bubble = (p - 1) / (m + p - 1). Interleaving with v chunks per GPU divides the bubble by about v (formula, not simulated).
Run: python3 l05_bubble_sim.py
"""
def simulate(p, m):
    T = 2 * (m + p - 1); busy = 0
    grid = [['.'] * T for _ in range(p)]
    for s in range(p):
        for mb in range(m):
            grid[s][s + mb] = 'F'; grid[s][(m + p - 1) + (p - 1 - s) + mb] = 'B'; busy += 2
    return grid, 1 - busy / (p * T)

grid, idle = simulate(4, 4)
print('GPipe, p = 4 stages, m = 4 micro-batches (F forward, B backward, . idle):')
for s, row in enumerate(grid): print(f'  stage {s}  ' + ''.join(row))
print(f'  idle share: {idle:.1%}   formula (p-1)/(m+p-1) = {3/7:.1%}')
print(f'\n{"p":>3} {"m":>4} {"simulated idle":>15} {"formula":>9} {"interleaved v=4":>16}')
for p, m in [(4, 4), (4, 16), (8, 8), (8, 32), (8, 128), (16, 32), (16, 128)]:
    _, idle = simulate(p, m); f = (p - 1) / (m + p - 1)
    print(f'{p:3d} {m:4d} {idle:14.1%} {f:9.1%} {f/4:15.1%}')
