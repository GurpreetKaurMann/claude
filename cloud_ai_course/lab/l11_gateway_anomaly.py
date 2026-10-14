"""Lesson 11 lab 4: attribution and anomaly alerts on SYNTHETIC gateway logs (I generated them; not real spend).
Part A: 60 days of per-call gateway lines (team, feature, tokens, cost computed with a versioned price table) -> showback by feature and cost per RESOLVED ticket.
Part B: on day 45 a developer puts a timestamp at the top of one feature's prompt (the cache breaks). Does an alert on daily cost (> mean + 3 sigma of the
trailing 14 days) catch it, and does an alert on cache-read share? Also arithmetic for 70B checkpoints. Run: python3 l11_gateway_anomaly.py"""
import random, statistics as st
random.seed(21)
PRICE = {'table': '2026-10-14', 'in': 2.0, 'cache_read': 0.10, 'out': 10.0}   # Sonnet 5.5 list $/MTok, notebook
FEATURES = {'triage-bot': (4000, 3000, 400, 0.70), 'order-lookup': (1500, 1000, 200, 0.95), 'refund-agent': (9000, 6000, 900, 0.45)}   # req/day, cacheable, out, resolve rate
def call_cost(unc, cr, out): return (unc * PRICE['in'] + cr * PRICE['cache_read'] + out * PRICE['out']) / 1e6
days = {}
for d in range(60):
    for f, (req, cache_t, out, res) in FEATURES.items():
        broken = (f == 'triage-bot' and d >= 45)
        n = int(req / 10 * random.uniform(.9, 1.1))      # 1 sampled request stands for 10 real ones, keeps this fast
        unc = cr = tot = 0; cost = 0.0
        for _ in range(n):
            u = 1000 + random.randint(-150, 150); c = 0 if broken else (cache_t if random.random() < .93 else 0)
            u += (cache_t - c); cost += 10 * call_cost(u, c, out); unc += u; cr += c
        days[(d, f)] = dict(cost=cost, share=cr / (unc + cr), n=n * 10)
print('A. SHOWBACK, days 0-44 (healthy), per feature')
print(f'{"feature":14s} {"requests":>10} {"cost/day":>9} {"cost/1k req":>12} {"resolve":>8} {"cost per resolved":>18}')
for f, (req, _, _, res) in FEATURES.items():
    cs = [days[(d, f)]['cost'] for d in range(45)]; ns = [days[(d, f)]['n'] for d in range(45)]
    per_req = sum(cs) / sum(ns); turns = 6 if f != 'order-lookup' else 2
    print(f'{f:14s} {sum(ns)/45:10,.0f} {st.mean(cs):9.2f} {per_req*1000:12.2f} {res:8.0%} {per_req*turns/res:18.4f}')
print('  (cost per resolved = cost per request x turns per conversation / resolve rate; turns assumed 6, 2 for lookups)')

print('\nB. THE BROKEN CACHE (triage-bot, day 45 on)')
def first_alert(f, key, ratio_mode=False):
    for d in range(15, 60):
        hist = [days[(x, f)][key] for x in range(d - 14, d)]; v = days[(d, f)][key]
        thr = st.mean(hist) + 3 * st.pstdev(hist)
        if (v < st.mean(hist) - 3 * st.pstdev(hist)) if ratio_mode else (v > thr): return d
    return None
before = st.mean(days[(d, 'triage-bot')]['cost'] for d in range(31, 45)); after = st.mean(days[(d, 'triage-bot')]['cost'] for d in range(45, 60))
print(f'  triage-bot cost/day: ${before:,.2f} before -> ${after:,.2f} after ({after/before:.1f}x)')
print(f'  cache-read share: {st.mean(days[(d,"triage-bot")]["share"] for d in range(31,45)):.0%} before -> {st.mean(days[(d,"triage-bot")]["share"] for d in range(45,60)):.0%} after')
a1 = first_alert('triage-bot', 'cost'); a2 = first_alert('triage-bot', 'share', True)
print(f'  alert on daily cost (> trailing mean + 3 sigma) first fires on day: {a1}')
print(f'  alert on cache-read share (< trailing mean - 3 sigma) first fires on day: {a2}')
for f in ('order-lookup', 'refund-agent'): print(f'  false alarms in {f} before day 45 (cost rule): {sum(1 for d in range(15,45) if days[(d,f)]["cost"] > st.mean(days[(x,f)]["cost"] for x in range(d-14,d)) + 3*st.pstdev(days[(x,f)]["cost"] for x in range(d-14,d)))} of 30 days')
extra = (after - before) * 30
print(f'  extra spend if nobody notices for 30 days: ${extra:,.0f}')

print('\nC. CHECKPOINT STORAGE (arithmetic, notebook assumptions: 70B model, 16 bytes/param, $0.02/GB cross-AZ, $0.023/GB-month)')
full = 70e9 * 16 / 1e9
print(f'  one full training-state checkpoint: {full:,.0f} GB; cross-AZ transfer ${full*.02:.2f} each, ${full*.02*24:,.0f}/day if hourly')
print(f'  keep 48 hourly: {48*full/1000:.2f} TB = ${48*full*.023:,.0f}/month; keep last 3: ${3*full*.023:,.0f}/month ({(1-3/48)*100:.0f}% less)')
