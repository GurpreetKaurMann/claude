"""Lesson 8 lab B: MEASURED. Does adding context to each chunk help retrieval?

Idea (contextual retrieval): a small chunk like 'k = 60' loses meaning on its own. Prepend the title of the notebook topic it came from.
Here the context is just the topic title, added by a simple rule, not written by an LLM (the real method asks a model to write 50 to 100 tokens).
Same 24 questions and retrievers as l08_rag_eval.py, chunks of 100 words. Run from the lab folder: python3 l08_context_prefix.py
"""
import re, numpy as np
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import l08_rag_eval as R
text = R.text; N = 100; step = 85
# topic titles from the 'Topic N of 10 <Title> Oct 2026' markers
marks = [(m.start(), m.group(1).strip()) for m in re.finditer(r'Topic \d+ of 10 (.+?) Oct 2026', text)]
def title_at(pos):
    t = 'Introduction'
    for p, name in marks:
        if p <= pos: t = name
    return t
# word offsets -> character positions
offs = np.cumsum([0] + [len(w) + 1 for w in R.words])
raw, ctx = [], []
for i in range(0, len(R.words), step):
    c = ' '.join(R.words[i:i + N]); raw.append(c); ctx.append(title_at(offs[i]) + '. ' + c)
def run(chs):
    bm = BM25Okapi([R.tok(c) for c in chs]); vec = TfidfVectorizer(sublinear_tf=True, token_pattern=r'[A-Za-z0-9]+'); X = vec.fit_transform(chs)
    svd = TruncatedSVD(200, random_state=0); M = svd.fit_transform(X); M /= np.linalg.norm(M, axis=1, keepdims=True) + 1e-9
    res = {'BM25': [0, 0], 'dense (LSA)': [0, 0]}
    for q, gold in R.Q:
        hit = [gold.lower() in c.lower() for c in raw]                 # truth is judged on the ORIGINAL chunk text
        qv = svd.transform(vec.transform([q]))[0]; qv /= np.linalg.norm(qv) + 1e-9
        for name, order in [('BM25', np.argsort(-bm.get_scores(R.tok(q)))), ('dense (LSA)', np.argsort(-(M @ qv)))]:
            res[name][0] += hit[order[0]]; res[name][1] += any(hit[i] for i in order[:3])
    return {k: [100 * x / len(R.Q) for x in v] for k, v in res.items()}
a, b = run(raw), run(ctx)
print(f'{len(raw)} chunks of {N} words · titles found: {sorted(set(t for _, t in marks))[:3]} ...')
print(f'{"method":>12} {"plain hit@1":>12} {"+title hit@1":>13} {"plain hit@3":>12} {"+title hit@3":>13}')
for k in a: print(f'{k:>12} {a[k][0]:11.1f}% {b[k][0]:12.1f}% {a[k][1]:11.1f}% {b[k][1]:12.1f}%')
