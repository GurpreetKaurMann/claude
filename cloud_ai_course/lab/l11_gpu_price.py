"""Lesson 11 lab 1 (ARITHMETIC, no measurement): the real price of a GPU hour, the commitment rule, and one training run five ways.
Prices are the notebook's approximate figures (Sep-Oct 2026, vendor / index / aggregator numbers) and move often. Run: python3 l11_gpu_price.py"""
rate_idx, rate_aws = 3.17, 6.88
print('REAL PRICE = list $/GPU-hr / utilisation  (utilisation = share of paid hours doing useful work)')
print(f'{"util":>6} {"H100 @ $3.17":>14} {"H100 @ $6.88":>14}')
for u in (0.05, 0.22, 0.50, 0.80, 1.00): print(f'{u:6.0%} {rate_idx/u:14.2f} {rate_aws/u:14.2f}')
print(f'\n5% -> 50% utilisation makes a useful hour {0.50/0.05:.0f}x cheaper; the best rate discounts are ~2-3x. Fix idle before you negotiate price.')

print('\nCOMMITMENT RULE: commit at discount d wins only if utilisation of the committed capacity > 1 - d')
print(f'{"discount":>9} {"break-even util":>16}   check at 100 paid hours of a $10 rate (commit pays for all hours)')
for d in (0.30, 0.40, 0.55):
    be = 1 - d
    for u in (be - 0.10, be + 0.10):
        commit = (1 - d) * 10 * 100; ondemand = 10 * 100 * u
        print(f'{d:9.0%} {be:16.0%}   util {u:4.0%}: commit ${commit:7.0f} vs on-demand ${ondemand:7.0f} -> {"commit wins" if commit < ondemand else "on-demand wins"}')

print('\nONE TRAINING RUN: 64 H100 x 14 days x 24 h')
hrs = 64 * 14 * 24; print(f'{hrs:,} GPU-hours')
rows = [('neocloud index $3.17', 3.17), ('market average $3.84', 3.84), ('AWS Capacity Block $5.97', 5.97), ('hyperscaler on-demand $6.88', 6.88), ('spot ~60% off index ($1.27) before restarts', 3.17 * 0.4)]
base = None
for n, r in rows:
    c = hrs * r; base = base or c
    print(f'{n:46s} ${c:10,.0f}')
print(f'spread between cheapest and dearest: {hrs*6.88/(hrs*3.17*0.4):.1f}x  (spot excludes lost steps and restarts: see lesson 2)')

print('\nAWS CAPACITY BLOCK price rises in 2026: +15%, +20%, +15%')
print(f'compounded: {1.15*1.20*1.15:.2f}x in a year')
