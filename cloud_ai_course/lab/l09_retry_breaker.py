"""Lesson 9 lab A: SIMULATION. Retry storms, jitter, and circuit breakers.

Part 1: 200 clients all call a server at second 0. The server can ACCEPT 50 requests per second, the rest get a 429 'try again' (ASSUMED capacity).
Clients retry up to 12 times with different waiting rules. We count total attempts (work the server must reject), the busiest second, and when the last client succeeds.
Part 2: a backend goes DOWN for 30 seconds. 20 requests per second arrive for 60 seconds. We count calls that hit the dead backend, with and without a circuit breaker
(opens after 5 failures in a row, waits 10 s, then lets 1 trial through). Simulations with assumed numbers. Run: python3 l09_retry_breaker.py
"""
import random, collections
random.seed(1)
TICK, CAP, CLIENTS, MAXTRY = 0.1, 5, 200, 12          # time in 0.1 s ticks; the server accepts 5 per tick = 50 per second

def run(policy):
    pending = {c: 0 for c in range(CLIENTS)}; per_tick = collections.Counter(); last = 0; ok = 0
    attempts = {c: 0 for c in range(CLIENTS)}
    for tick in range(0, 3000):
        due = [c for c, t in pending.items() if t <= tick]; random.shuffle(due)
        for i, c in enumerate(due):
            attempts[c] += 1; per_tick[tick] += 1
            if i < CAP: del pending[c]; last = tick; ok += 1; continue                # accepted
            if attempts[c] >= MAXTRY: del pending[c]; continue                      # gave up
            a = attempts[c]
            wait = {'retry at once (every 0.1 s)': TICK, 'exponential, no jitter': min(30, 0.5 * 2 ** a),
                    'exponential, full jitter': random.uniform(0, min(30, 0.5 * 2 ** a))}[policy]
            pending[c] = tick + max(1, round(wait / TICK))
        if not pending: break
    return sum(attempts.values()), sum(attempts.values()) - ok, last * TICK, CLIENTS - ok

print(f'== 1. {CLIENTS} clients all call at second 0, server accepts {CAP/TICK:.0f} per second (assumed)')
print(f'{"retry rule":28} {"total attempts":>15} {"rejected (wasted)":>18} {"last success at":>16} {"gave up":>8}')
for pol in ['retry at once (every 0.1 s)', 'exponential, no jitter', 'exponential, full jitter']:
    a, peak, last, gave = run(pol); print(f'{pol:28} {a:15d} {peak:18d} {last:15.1f}s {gave:8d}')

print('\n== 2. backend dead from second 10 to 40; 20 requests per second for 60 seconds')
def breaker_run(use):
    state, fails, opened, calls_dead, calls_total = 'closed', 0, 0, 0, 0
    for sec in range(60):
        for _ in range(20):
            down = 10 <= sec < 40
            if use and state == 'open':
                if sec - opened >= 10: state = 'half-open'
                else: continue                                              # fail fast, no call made
            if use and state == 'half-open':
                trial = True
            calls_total += 1; calls_dead += down
            if down:
                fails += 1
                if use and (state == 'half-open' or fails >= 5): state, opened = 'open', sec
            else:
                fails = 0
                if use and state == 'half-open': state = 'closed'
    return calls_total, calls_dead
for use, name in [(False, 'no breaker'), (True, 'circuit breaker')]:
    t, d = breaker_run(use); print(f'{name:16} calls made {t:5d} · calls that hit the dead backend {d:5d}')
