"""Lesson 3 lab B: SIMULATION. Why distributed jobs need gang scheduling.

A cluster has 16 GPUs. Each job needs 8 pods x 1 GPU and only makes progress when ALL 8 are placed.
Default scheduler: places pods one at a time in the order they arrive (we shuffle the arrival order, 10,000 times).
Gang scheduler: places a job only if all 8 GPUs are free at once. Finished jobs release their GPUs and then run to completion.
We count how often the cluster ends up DEADLOCKED: GPUs full, no job complete, nothing can move.
Run: python3 l03_gang.py
"""
import random
GPUS, PODS, TRIALS = 16, 8, 10_000

def default_sched(njobs, rng):
    arrivals = [j for j in range(njobs) for _ in range(PODS)]; rng.shuffle(arrivals)
    placed = [0] * njobs; free = GPUS; done = [False] * njobs; queue = list(arrivals)
    while True:
        progress = False
        for j in range(njobs):                          # complete any job that has all its pods
            if not done[j] and placed[j] == PODS: done[j] = True; free += PODS; placed[j] = 0; progress = True
        nxt = []
        for j in queue:                                 # place waiting pods while GPUs are free
            if free > 0 and not done[j]: placed[j] += 1; free -= 1; progress = True
            elif not done[j]: nxt.append(j)
        queue = nxt
        if all(done): return False
        if not progress: return True                    # nobody can move: deadlock

def gang_sched(njobs, rng):
    pending = list(range(njobs)); rng.shuffle(pending); free = GPUS; running = []
    while pending or running:
        while pending and free >= PODS: pending.pop(0); free -= PODS; running.append(1)
        if running: running.pop(); free += PODS
        elif pending: return True
    return False

print(f'{GPUS} GPUs, each job = {PODS} pods x 1 GPU, {TRIALS:,} random arrival orders')
print(f'{"jobs submitted":>15} {"default: deadlocked":>20} {"gang: deadlocked":>18}')
for n in [2, 3, 4, 6]:
    rng = random.Random(5)
    d = sum(default_sched(n, rng) for _ in range(TRIALS)) / TRIALS
    g = sum(gang_sched(n, rng) for _ in range(TRIALS)) / TRIALS
    print(f'{n:15d} {d:19.1%} {g:17.1%}')
