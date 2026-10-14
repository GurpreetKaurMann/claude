"""Lesson 11 lab 2: token bills. Part A is ARITHMETIC from the notebook's list prices (Anthropic $/MTok, 14 Oct 2026; they change).
Part B is a MEASURED run of a tiny prefix cache I wrote (a toy, not any vendor's cache): it counts how many request tokens match a cached prefix
for 5,000 simulated support requests, with a timestamp at the TOP of the system prompt versus AFTER the cached part. Part C checks the
hit-rate formula 1 - exp(-lambda*TTL) against a simulated arrival stream. Run: python3 l11_token_cost.py"""
import math, random
P = {'Opus 5.5': (4, 20, .05, 1.25), 'Sonnet 5.5': (2, 10, .05, 1.25), 'Haiku 5.5': (.10, .50, .10, 1.25)}   # in, out, cache-read multiplier, 5-min write multiplier
CACHEABLE, UNCACHED, OUT = 3000, 1000, 400
def cost(m, hit, batch=False):
    pin, pout, r, w = P[m]
    c = (CACHEABLE * pin * (r if hit else w) + UNCACHED * pin + OUT * pout) / 1e6
    return c * (0.5 if batch else 1)
print('A. cost per 1M requests (3,000 cacheable + 1,000 uncached input, 400 output)')
for m in P:
    print(f'  {m:11s} no cache ${(CACHEABLE+UNCACHED)*P[m][0]/1e6*1e6 + OUT*P[m][1]:>9,.0f}   cache hit ${cost(m, True)*1e6:>9,.0f}   cache write ${cost(m, False)*1e6:>9,.0f}')
nc = ((CACHEABLE + UNCACHED) * 2 + OUT * 10)
print(f'  Sonnet 5.5 batch + hit ${cost("Sonnet 5.5", True, True)*1e6:,.0f}')
for h in (.5, .8, .95): print(f'  Sonnet 5.5 at hit rate {h:.0%}: ${(h*cost("Sonnet 5.5", True) + (1-h)*cost("Sonnet 5.5", False))*1e6:,.0f} per 1M')
hit_cost = cost('Sonnet 5.5', True)*1e6
print(f'  cache hit saves {(1 - hit_cost/nc)*100:.1f}% vs no cache (Sonnet 5.5)')
casc = ((4000 * .1 + 400 * .5) / 1e6) + 0.3 * (4000 * 2 + 400 * 10) / 1e6
print(f'  cascade Haiku first, 30% escalate to Sonnet (no cache): ${casc*1e6:,.0f} per 1M ({(1 - casc*1e6/nc)*100:.0f}% below all-Sonnet)')
print(f'  output 400 -> 250 tokens on Sonnet: saves ${150*10:,.0f} per 1M = {150*10/nc*100:.1f}% of the uncached bill')

# B. toy prefix cache
random.seed(5)
SYSTEM = ('You are the ShopNest support assistant. ' + ' '.join(f'policy{i}' for i in range(2990))).split()
def build(ts_top, i):
    stamp = f'time-{i}'.split()   # a changing field
    user = [f'q{random.randrange(10**6)}' for _ in range(UNCACHED)]
    return (stamp + SYSTEM + user) if ts_top else (SYSTEM + stamp + user)
def run(ts_top, n=5000):
    seen = {}; matched = total = 0
    for i in range(n):
        toks = build(ts_top, i); node = seen; m = 0
        for t in toks:
            if t in node: node = node[t]; m += 1
            else: break
        matched += m; total += len(toks)
        node = seen
        for t in toks: node = node.setdefault(t, {})
    return matched / total
print('\nB. MEASURED toy prefix cache, 5,000 requests of ~4,000 tokens')
a, b = run(True), run(False)
print(f'  changing timestamp at the TOP of the system prompt: {a:.1%} of tokens served from cache')
print(f'  changing timestamp AFTER the cached prefix:         {b:.1%} of tokens served from cache')
print(f'  input cost per 1M requests (Sonnet 5.5): top {4000*(a*.1+(1-a)*2):,.0f}  vs after {4000*(b*.1+(1-b)*2):,.0f}  ({(a*.1+(1-a)*2)/(b*.1+(1-b)*2):.1f}x the bill)')

# C. TTL hit rate
def sim(rate_per_s, ttl, n=20000):
    t = 0.0; last = -1e9; hits = 0
    for _ in range(n):
        t += random.expovariate(rate_per_s)
        if t - last <= ttl: hits += 1
        last = t   # a read refreshes the TTL
    return hits / n
print('\nC. hit rate vs formula 1 - exp(-lambda*TTL), 5-minute TTL')
for name, lam in (('1 request / minute', 1/60), ('1 request / 10 minutes', 1/600), ('1 request / hour', 1/3600)):
    print(f'  {name:24s} formula {1-math.exp(-lam*300):6.1%}   simulated {sim(lam, 300):6.1%}')
