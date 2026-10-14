"""Lesson 8 lab: MEASURED retrieval quality on a REAL text with HAND-WRITTEN questions.

Corpus: the text of the Cloud for AI Engineers study notebook (data/notebook_text.txt, 45,060 words). 24 questions I wrote, each with an answer
phrase that appears in the notebook. A chunk counts as a HIT if it contains the answer phrase (case-insensitive). hit@k = share of questions with
a hit in the top k chunks. Three retrievers:
  BM25   = keyword scoring (the rank_bm25 package)
  dense  = a STAND-IN for embeddings: TF-IDF + a 200-dimension SVD ('LSA'), cosine similarity. NOT a neural embedding model (none could be downloaded here).
  hybrid = reciprocal rank fusion of the two lists, score = sum of 1 / (60 + rank).
Chunking: windows of N words with 15% overlap. Run from the lab folder: python3 l08_rag_eval.py
"""
import re, numpy as np
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
text = open('data/notebook_text.txt').read(); words = text.split()
Q = [("Which storage tier is the durable source of truth for training data?", "durable source of truth"),
     ("How long does S3 take to auto-partition after a load spike?", "30–60 min"),
     ("How much notice does AWS give before taking back a spot instance?", "2 min notice on AWS"),
     ("How many unexpected interruptions did Llama 3 report in 54 days?", "419 unexpected interruptions"),
     ("What does RRF use instead of raw scores when fusing results?", "Ranks, not raw scores"),
     ("What value of k does reciprocal rank fusion use?", "k = 60"),
     ("What is the rule of thumb for chunk size in tokens?", "300–800 tokens"),
     ("How much did contextual retrieval plus reranking cut retrieval failures?", "−67% retrieval failures"),
     ("What is the CVE for the NVIDIAScape container escape?", "CVE-2025-23266"),
     ("Which toolkit version fixed the NVIDIAScape flaw?", "1.17.8"),
     ("How many bytes per parameter does mixed precision Adam need before activations?", "≈ 16 bytes/param"),
     ("What does the bubble formula for pipeline parallelism look like?", "(p − 1) / (m + p − 1)"),
     ("Which HNSW parameter sets how many links each node keeps?", "M links per node"),
     ("What is the HNSW memory formula?", "N × (4·d + 8·M) bytes"),
     ("What does gang scheduling mean for distributed training?", "Gang = place all or none"),
     ("What default retention does Delta use for deleted files?", "defaults: files 7 days"),
     ("What is the S3 Vectors vector limit per index?", "2B vectors / index"),
     ("Which engine is in maintenance mode for LLM serving?", "TGI = maintenance mode"),
     ("What is the Chinchilla compute-optimal tokens per parameter?", "≈ 20 tokens/param"),
     ("How many tokens per parameter did Llama 3 405B train on?", "≈ 38 tokens/param"),
     ("What is the real price of a GPU in terms of utilization?", "Real price = $/GPU-hr ÷ utilization"),
     ("What does MIG stand for in terms of walls and rooms mnemonic?", "MIG = walls"),
     ("What are the three levels of Google's MLOps maturity?", "0 manual"),
     ("What is the multi-agent token multiplier compared to chat?", "multi-agent ≈ 15×")]
tok = lambda s: re.findall(r'[a-z0-9]+', s.lower())

def chunks(n, overlap=0.15):
    step = max(1, int(n * (1 - overlap))); return [' '.join(words[i:i + n]) for i in range(0, len(words), step)]

def evaluate(n):
    ch = chunks(n); bm = BM25Okapi([tok(c) for c in ch])
    vec = TfidfVectorizer(sublinear_tf=True, token_pattern=r'[A-Za-z0-9]+'); X = vec.fit_transform(ch)
    svd = TruncatedSVD(200, random_state=0); M = svd.fit_transform(X); M /= np.linalg.norm(M, axis=1, keepdims=True) + 1e-9
    out = {m: [0, 0, 0] for m in ['BM25', 'dense (LSA)', 'hybrid RRF']}
    for q, gold in Q:
        gold = gold.lower(); hit = [gold in c.lower() for c in ch]
        r_bm = list(np.argsort(-bm.get_scores(tok(q))))
        qv = svd.transform(vec.transform([q]))[0]; qv /= np.linalg.norm(qv) + 1e-9; r_dn = list(np.argsort(-(M @ qv)))
        rrf = {}
        for lst in (r_bm[:50], r_dn[:50]):
            for rank, i in enumerate(lst, 1): rrf[i] = rrf.get(i, 0) + 1 / (60 + rank)
        r_h = sorted(rrf, key=rrf.get, reverse=True)
        for name, lst in [('BM25', r_bm), ('dense (LSA)', r_dn), ('hybrid RRF', r_h)]:
            for j, k in enumerate((1, 3, 5)): out[name][j] += any(hit[i] for i in lst[:k])
    return len(ch), {k: [100 * x / len(Q) for x in v] for k, v in out.items()}

if __name__ == '__main__':
    print(f'{len(words):,} words · {len(Q)} questions · hit@k = share of questions with the answer phrase in the top k chunks')
    print(f'{"chunk size":>11} {"chunks":>7} {"method":>12} {"hit@1":>7} {"hit@3":>7} {"hit@5":>7}')
    for n in [100, 300, 800]:
        nch, res = evaluate(n)
        for name, (a, b, c) in res.items(): print(f'{n:8d} wd {nch:7d} {name:>12} {a:6.1f}% {b:6.1f}% {c:6.1f}%')

    # who finds what? at 300-word chunks, top 3
    ch = chunks(300); bm = BM25Okapi([tok(c) for c in ch])
    vec = TfidfVectorizer(sublinear_tf=True, token_pattern=r'[A-Za-z0-9]+'); X = vec.fit_transform(ch)
    svd = TruncatedSVD(200, random_state=0); M = svd.fit_transform(X); M /= np.linalg.norm(M, axis=1, keepdims=True) + 1e-9
    both = only_bm = only_dn = neither = 0
    for q, gold in Q:
        hit = [gold.lower() in c.lower() for c in ch]
        qv = svd.transform(vec.transform([q]))[0]; qv /= np.linalg.norm(qv) + 1e-9
        a = any(hit[i] for i in np.argsort(-bm.get_scores(tok(q)))[:3]); b = any(hit[i] for i in np.argsort(-(M @ qv))[:3])
        both += a and b; only_bm += a and not b; only_dn += b and not a; neither += not a and not b
    print(f'\n300-word chunks, top 3: both found it {both} · only BM25 {only_bm} · only dense {only_dn} · neither {neither}   (24 questions, each worth 4.2 points)')
