"""Lesson 7 lab C: SIMULATION. How much damage a bad release does, by how much traffic you send to it first (canary share).

Traffic: 600 requests per minute. The old version fails 1% of requests. The NEW version is bad: it fails 5% (ASSUMED rates).
An automatic check runs every 5 minutes (ASSUMED): it adds up all new-version requests so far and rolls back if the failures are far above
what 1% predicts (a z-test, z > 3). We run 2,000 simulated releases per canary share and count bad responses before the rollback,
and how often the very first check catches it. Run: python3 l07_canary_sim.py
"""
import numpy as np
rng = np.random.default_rng(8)
RPM, P0, P1, INTERVAL = 600, 0.01, 0.05, 5
def release(share):
    n = e = 0
    for step in range(1, 13):                              # up to 12 checks = one hour
        reqs = int(RPM * INTERVAL * share); errs = rng.binomial(reqs, P1); n += reqs; e += errs
        if n and (e - n * P0) / np.sqrt(n * P0 * (1 - P0)) > 3: return step, e, True
    return 12, e, False
print(f'{"canary share":>13} {"caught at 1st check":>20} {"mean checks":>12} {"bad responses before rollback":>30} {"requests on new version":>17}')
for share in [0.01, 0.05, 0.25, 1.0]:
    R = [release(share) for _ in range(2000)]
    first = np.mean([r[0] == 1 and r[2] for r in R]); steps = np.mean([r[0] for r in R]); bad = np.mean([r[1] for r in R])
    print(f'{share:12.0%} {first:19.0%} {steps:12.2f} {bad:30.1f} {RPM*INTERVAL*share*steps:23.0f}')
