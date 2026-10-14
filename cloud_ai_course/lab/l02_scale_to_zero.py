"""Lesson 2 lab C: SIMULATION. Always-on GPU vs scale-to-zero vs one warm GPU.

One GPU serves requests that each take 5 s. Traffic over 24 h is ASSUMED to be bursty: a 3-hour busy window
(1 request every 12 s on average) and a 1-hour light window (1 every 120 s). The rest of the day is silent.
Scale-to-zero shuts the GPU down after 5 idle minutes. Starting it again takes a cold start of 60 s (ASSUMED;
real cold starts are tens of seconds to minutes). Mean over 200 seeded days.
We measure GPU-hours billed and the wait before each request starts. Run: python3 l02_scale_to_zero.py
"""
import numpy as np
SERVICE, IDLE_OFF, COLD = 5.0, 300.0, 60.0

def day(rng):
    t = []
    for start, hours, gap in [(9, 3, 12.0), (20, 1, 120.0)]:
        x = start * 3600.0; end = (start + hours) * 3600.0
        while True:
            x += rng.exponential(gap)
            if x > end: break
            t.append(x)
    return np.array(t)

def sim(arr, policy):
    free_at, on, billed, waits, last_end, cold = 0.0, policy == 'always on', 0.0, [], 0.0, []
    on_since = 0.0 if on else None
    for a in arr:
        if policy == 'scale to zero' and on_since is not None and a - last_end > IDLE_OFF:
            billed += (last_end + IDLE_OFF) - on_since; on_since = None     # it shut down while idle
        start = max(a, free_at)
        if policy == 'scale to zero' and on_since is None:
            on_since = a; start = a + COLD                                  # cold start
            cold.append(len(waits))
        waits.append(start - a); free_at = start + SERVICE; last_end = free_at
    if policy == 'always on': billed = 24 * 3600.0
    elif policy == 'one warm GPU': billed = 24 * 3600.0
    else: billed += min(last_end + IDLE_OFF, 24 * 3600.0) - on_since
    return billed / 3600.0, np.array(waits), cold

print(f'{"policy":16} {"GPU-hours/day":>14} {"mean wait s":>12} {"p95 wait s":>11} {"max wait s":>11} {"cold starts/day":>16} {"wait when cold s":>17}')
for pol in ['always on', 'scale to zero']:
    rng = np.random.default_rng(7); H, W, CW = [], [], []
    for _ in range(200):
        h, w, c = sim(day(rng), pol); H.append(h); W.append(w); CW += [w[i] for i in c]
    w = np.concatenate(W)
    print(f'{pol:16} {np.mean(H):14.2f} {w.mean():12.2f} {np.percentile(w,95):11.2f} {w.max():11.2f} {len(CW)/200:16.2f} {(np.mean(CW) if CW else 0):17.2f}')
print('(one warm GPU bills like always on, and also waits like always on)')
