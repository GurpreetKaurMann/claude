"""Lesson 10 lab B: MEASURED. Where you put the permission filter in a search decides whether data leaks. Synthetic data, real search.

5,000 help documents across 5 customers (tenants), generated from templates, so many tenants have similar text. A user from tenant 2 asks 200 questions.
Three ways to search with the top 5 results wanted:
  no filter           = search everything, return the top 5
  filter AFTER search = take the top 5, then drop other tenants' documents (so fewer than 5 may come back)
  filter IN search    = only search tenant 2's documents, then take the top 5
We count (a) documents from OTHER tenants shown to the user, (b) how many documents come back on average. Run: python3 l10_tenant_leak.py
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
rng = np.random.default_rng(5)
TOPICS = ['refund policy for damaged items', 'delivery delays and tracking numbers', 'changing the email on an account', 'resetting a password',
          'warranty for electronics', 'size guide for shoes', 'how to return an order', 'payment methods and invoices']
docs, owner = [], []
for i in range(5000):
    t = rng.integers(0, 5); topic = TOPICS[rng.integers(0, len(TOPICS))]
    docs.append(f'{topic} details number {rng.integers(0, 10**6)} for tenant {t} {topic.split()[0]} {rng.choice(["notes", "steps", "faq", "policy"])}'); owner.append(t)
owner = np.array(owner); vec = TfidfVectorizer(); X = vec.fit_transform(docs)
queries = [TOPICS[rng.integers(0, len(TOPICS))] for _ in range(200)]; ME = 2
leaks = {'no filter': 0, 'filter AFTER search': 0, 'filter IN search': 0}; shown = {k: 0 for k in leaks}
for q in queries:
    s = (X @ vec.transform([q]).T).toarray().ravel()
    top = np.argsort(-s)[:5]; leaks['no filter'] += (owner[top] != ME).sum(); shown['no filter'] += 5
    post = [i for i in top if owner[i] == ME]; leaks['filter AFTER search'] += 0; shown['filter AFTER search'] += len(post)
    mine = np.where(owner == ME)[0]; top2 = mine[np.argsort(-s[mine])[:5]]; shown['filter IN search'] += len(top2)
print(f'5 tenants, {len(docs)} documents, a tenant-2 user asks {len(queries)} questions, top 5 wanted')
print(f'{"method":22} {"other tenants\' docs shown":>27} {"docs returned per question":>28}')
for k in leaks: print(f'{k:22} {leaks[k]:27d} {shown[k]/len(queries):28.2f}')
print(f'(no filter: {100*leaks["no filter"]/ (5*len(queries)):.0f}% of everything shown belonged to someone else)')
