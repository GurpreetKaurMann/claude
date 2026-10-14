"""Lesson 4 lab A: MEASURED on this machine's local disk, plus an ASSUMED-latency model of an object store.

Part 1 (measured): read the same 80 MB as 20,000 files of 4 KB, as 80 files of 1 MB, and as ONE 80 MB file.
We drop the page cache before each read when the OS allows it (otherwise the numbers would be memory speed).
Part 2 (model, ASSUMED numbers): an object store charges a fixed delay per request (assumed 20 ms) plus bytes / bandwidth
(assumed 100 MB/s per stream). Real latency and bandwidth vary by service. Run: python3 l04_small_files.py
"""
import os, time, tempfile, shutil
import numpy as np
TOTAL = 80 * 1024 * 1024
rng = np.random.default_rng(3)

def drop_cache():
    try:
        os.sync(); open('/proc/sys/vm/drop_caches', 'w').write('3'); return True
    except Exception:
        return False

def make(n_files, d):
    os.makedirs(d); size = TOTAL // n_files
    for i in range(n_files):
        with open(f'{d}/{i:06d}', 'wb') as f: f.write(rng.integers(0, 256, size, dtype='uint8').tobytes())

def read_all(d):
    t = time.perf_counter(); n = 0
    for name in sorted(os.listdir(d)):
        with open(f'{d}/{name}', 'rb') as f: n += len(f.read())
    return time.perf_counter() - t, n

root = tempfile.mkdtemp(dir='/home/claude/cailab/data' if os.path.isdir('/home/claude/cailab/data') else None)
print('== 1. MEASURED: reading 80 MB from local disk')
print(f'{"layout":22} {"files":>7} {"seconds":>9} {"MB/s":>8}  {"vs one file":>12}')
res = []
cache_dropped = None
for label, n in [('4 KB files', 20000), ('1 MB files', 80), ('one 80 MB shard', 1)]:
    d = f'{root}/{n}'; make(n, d); cache_dropped = drop_cache()
    trials = []
    for _ in range(3):                      # best of three, cache dropped before each
        drop_cache(); trials.append(read_all(d)[0])
    sec = min(trials)
    res.append((label, n, sec))
base = res[-1][2]
for label, n, sec in res:
    print(f'{label:22} {n:7d} {sec:9.3f} {80/sec:8.0f}  {sec/base:11.1f}x')
print('page cache dropped before each read:', cache_dropped)
shutil.rmtree(root)

print('\n== 2. MODEL (assumed 20 ms per request, 100 MB/s per stream): time to read 80 MB')
LAT, BW = 0.020, 100.0
for label, n in [('4 KB files', 20000), ('1 MB files', 80), ('one 80 MB shard', 1)]:
    t = n * LAT + 80 / BW
    print(f'{label:22} {n:7d} requests -> {t:8.1f} s   ({80/t:6.1f} MB/s)')
