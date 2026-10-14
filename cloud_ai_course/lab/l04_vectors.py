"""Lesson 4 lab B: MEASURED on SYNTHETIC vectors. Memory, speed and recall of vector search.

Data: 50,000 vectors of 768 numbers drawn from 100 gaussian clusters (SYNTHETIC, not real embeddings), 300 query vectors
from the same clusters. "Truth" = exact search by brute force. recall@10 = share of the true top-10 that a method returns.
Part 1: storage formats (float32, float16, int8, binary). Part 2: a graph index (HNSW via the hnswlib package) at different
search effort (ef). One CPU thread. Run: python3 l04_vectors.py
"""
import time, os, numpy as np
rng = np.random.default_rng(11)
N, D, NQ, K, CL = 50_000, 768, 300, 10, 100
centers = rng.standard_normal((CL, D)).astype('float32') * 0.6
X = centers[rng.integers(0, CL, N)] + rng.standard_normal((N, D)).astype('float32')
Q = centers[rng.integers(0, CL, NQ)] + rng.standard_normal((NQ, D)).astype('float32')
X /= np.linalg.norm(X, axis=1, keepdims=True); Q /= np.linalg.norm(Q, axis=1, keepdims=True)   # unit length: dot = cosine

def topk_dot(Xs, Qs, k=K):
    S = Qs @ Xs.T
    idx = np.argpartition(-S, k, axis=1)[:, :k]
    return np.take_along_axis(idx, np.argsort(-np.take_along_axis(S, idx, 1), axis=1), 1)
recall = lambda got, truth: np.mean([len(set(g) & set(t)) / K for g, t in zip(got, truth)])

t = time.perf_counter(); truth = topk_dot(X, Q); t_exact = (time.perf_counter() - t) / NQ * 1000
print(f'{N:,} vectors x {D} dims (synthetic) · exact search: {t_exact:.2f} ms per query, float32 = {X.nbytes/1e6:.1f} MB')

print('\n== 1. storage formats (exact search on the compressed copy)')
print(f'{"format":10} {"bytes/vector":>13} {"total MB":>9} {"smaller":>8} {"recall@10":>10}')
print(f'{"float32":10} {D*4:13d} {X.nbytes/1e6:9.1f} {"1x":>8} {1.0:10.3f}')
x16 = X.astype('float16'); r16 = recall(topk_dot(x16.astype('float32'), Q), truth)
print(f'{"float16":10} {D*2:13d} {x16.nbytes/1e6:9.1f} {"2x":>8} {r16:10.3f}')
sc = 127 / np.abs(X).max(axis=1, keepdims=True); x8 = np.round(X * sc).astype('int8'); r8 = recall(topk_dot(x8.astype('float32') / sc, Q), truth)
print(f'{"int8":10} {D:13d} {x8.nbytes/1e6:9.1f} {"4x":>8} {r8:10.3f}')
Xb = np.packbits(X > 0, axis=1); Qb = np.packbits(Q > 0, axis=1)
pop = np.array([bin(i).count('1') for i in range(256)], dtype='uint8')
ham = np.stack([pop[np.bitwise_xor(Xb, q)].sum(axis=1) for q in Qb])
cand = np.argsort(ham, axis=1)[:, :100]                               # 100 closest by Hamming, then rescore with full vectors
rb_raw = recall(cand[:, :K], truth)
resc = np.stack([cand[i][np.argsort(-(X[cand[i]] @ Q[i]))[:K]] for i in range(NQ)]); rb = recall(resc, truth)
print(f'{"binary":10} {D//8:13d} {Xb.nbytes/1e6:9.1f} {"32x":>8} {rb_raw:10.3f}   (top-10 by Hamming only)')
print(f'{"binary+rescore":10} {D//8:13d} {Xb.nbytes/1e6:9.1f} {"32x":>8} {rb:10.3f}   (top-100 by Hamming, rescored with float32)')

print('\n== 2. graph index (HNSW, hnswlib, M=16, efConstruction=100), recall vs effort')
import hnswlib
M = 16
t = time.perf_counter(); idx = hnswlib.Index(space='cosine', dim=D); idx.init_index(max_elements=N, ef_construction=100, M=M)
idx.set_num_threads(1); idx.add_items(X); tb = time.perf_counter() - t
idx.save_index('/tmp/claude-0/hnsw.bin'); size = os.path.getsize('/tmp/claude-0/hnsw.bin') / 1e6; os.remove('/tmp/claude-0/hnsw.bin')
print(f'build {tb:.1f} s · index on disk {size:.1f} MB · formula N x (4d + 8M) = {N*(4*D+8*M)/1e6:.1f} MB')
print(f'{"ef (effort)":>12} {"recall@10":>10} {"ms/query":>9} {"vs exact":>9}')
for ef in [10, 20, 50, 100, 200]:
    idx.set_ef(ef); t = time.perf_counter(); lab, _ = idx.knn_query(Q, k=K); ms = (time.perf_counter() - t) / NQ * 1000
    print(f'{ef:12d} {recall(lab, truth):10.3f} {ms:9.3f} {t_exact/ms:8.0f}x')
