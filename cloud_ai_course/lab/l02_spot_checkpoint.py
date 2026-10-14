"""Lesson 2 lab A: SIMULATION. Spot machines vs checkpoint interval.

A job needs 100 hours of work. A spot machine is taken away at random times (exponential gaps, mean
MTBF = 8 hours, an ASSUMED rate; real rates vary by region and chip). After each interruption we
lose all work since the last checkpoint and wait 0.1 h to restart. A checkpoint costs 0.02 h (72 s)
of work time. We compare checkpoint intervals, then price the result: on-demand = 1.00 per hour,
spot = 0.30 per hour (an ASSUMED 70% discount; vendors quote up to 91% off).
Mean over 2,000 seeded runs. Run: python3 l02_spot_checkpoint.py
"""
import numpy as np, math

WORK, MTBF, CKPT, RESTART = 100.0, 8.0, 0.02, 0.1
SPOT, ONDEMAND = 0.30, 1.00

def run(interval, rng):
    done, wall, saved = 0.0, 0.0, 0.0           # work finished, clock, work safely saved
    nxt = rng.exponential(MTBF)                  # time until the next interruption
    while saved < WORK:
        step = min(interval, WORK - saved)       # work we try to do before the next checkpoint
        need = step + (CKPT if saved + step < WORK else 0.0)
        if nxt >= need:                          # no interruption: finish the chunk
            wall += need; nxt -= need; saved += step
        else:                                    # interrupted: lose the chunk, restart
            wall += nxt + RESTART; nxt = rng.exponential(MTBF)
    return wall

print(f'job = {WORK:.0f} h of work, mean time between interruptions = {MTBF:.0f} h (assumed)')
print(f'{"checkpoint every":>18} {"mean hours":>11} {"vs no loss":>11} {"spot cost":>10} {"vs on-demand":>13}')
young = math.sqrt(2 * MTBF * CKPT)
rows = [('never (only at end)', WORK), ('8 h', 8), ('2 h', 2), ('30 min', 0.5), (f'{young*60:.0f} min (Young)', young),
        ('10 min', 10/60), ('2 min', 2/60), ('30 s', 30/3600)]
for name, iv in rows:
    rng = np.random.default_rng(42)
    w = np.mean([run(iv, rng) for _ in range(2000 if iv > 0.05 else 400)])
    print(f'{name:>18} {w:11.1f} {w/WORK:10.2f}x {w*SPOT:10.1f} {w*SPOT/(WORK*ONDEMAND):12.2f}x')
print(f'\nYoung/Daly rule of thumb: interval ≈ sqrt(2 x MTBF x checkpoint cost) = {young:.3f} h = {young*60:.0f} min')
print('on-demand, no interruptions: 100.0 h at 1.00 = 100.0')
