"""Lesson 7 lab B: SIMULATION + formula. Why you run several trials when you evaluate an LLM or an agent.

An agent solves a task correctly with probability p each time you run it (ASSUMED per-trial success rate).
pass@k = chance AT LEAST ONE of k runs succeeds = 1 - (1 - p)^k      (good for 'can it ever do it?')
pass^k = chance ALL k runs succeed = p^k                              (good for 'can I rely on it?')
We check both formulas with 100,000 simulated tasks. Run: python3 l07_trials.py
"""
import numpy as np
rng = np.random.default_rng(6)
print(f'{"p":>5} {"k":>3} {"pass@k formula":>15} {"simulated":>10} {"pass^k formula":>15} {"simulated":>10}')
for p in [0.8, 0.9, 0.95]:
    for k in [1, 3, 5, 10]:
        runs = rng.random((100_000, k)) < p
        print(f'{p:5.2f} {k:3d} {1-(1-p)**k:15.3f} {runs.any(axis=1).mean():10.3f} {p**k:15.3f} {runs.all(axis=1).mean():10.3f}')
