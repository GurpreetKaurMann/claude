"""Lesson 6 lab B: SIMULATION. Static vs continuous batching.

A GPU serves up to 32 requests at once. Every decode step takes 25 ms no matter how many are in the batch (ASSUMED, a memory-bound step: see lesson 1).
2,000 requests arrive together. Each wants a random number of output tokens (exponential, mean 120, capped at 600, a typical long-tailed shape, ASSUMED).
STATIC batching: take 32 requests, run until the LONGEST finishes, then take the next 32.
CONTINUOUS batching: after every step, finished requests leave and waiting ones join immediately.
We report total time, tokens per second, and the average time until a request finishes. Run: python3 l06_batching_sim.py
"""
import numpy as np
rng = np.random.default_rng(4)
N, SLOTS, STEP = 2000, 32, 0.025
lens = np.minimum(rng.exponential(120, N).astype(int) + 1, 600)

def static(lens):
    t, done = 0.0, []
    for i in range(0, N, SLOTS):
        grp = lens[i:i + SLOTS]; t += grp.max() * STEP; done += [t] * len(grp)
    return t, np.array(done)

def continuous(lens):
    t, done, rem = 0.0, np.zeros(N), {}
    queue = list(range(N)); finish = {}
    while queue or rem:
        while queue and len(rem) < SLOTS: j = queue.pop(0); rem[j] = lens[j]
        t += STEP
        for j in list(rem):
            rem[j] -= 1
            if rem[j] == 0: finish[j] = t; del rem[j]
    return t, np.array([finish[j] for j in range(N)])

print(f'{N} requests, mean {lens.mean():.0f} output tokens (max {lens.max()}), {SLOTS} slots, {STEP*1000:.0f} ms per step (assumed)')
print(f'{"policy":12} {"total time":>11} {"tokens/s":>9} {"mean finish":>12} {"slowest finish":>15}')
for name, f in [('static', static), ('continuous', continuous)]:
    t, done = f(lens)
    print(f'{name:12} {t:10.0f}s {lens.sum()/t:9.0f} {done.mean():11.0f}s {done.max():14.0f}s')
