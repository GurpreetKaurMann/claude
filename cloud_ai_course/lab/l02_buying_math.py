"""Lesson 2 lab B: ARITHMETIC (no measurement). What a discount really costs you.

Discount sizes are the vendor 'up to' figures from the notebook (14 Oct 2026): commitments up to ~55% off,
queued/Flex ~50% off, spot up to 91% off. The $10 per GPU-hour on-demand price is an ASSUMED round number.
Key idea: you pay for a commitment even when the GPU is idle, so the real price is rate / utilisation.
Also: $ per petaflop-hour from the vendor list prices in the notebook. Run: python3 l02_buying_math.py
"""
OD = 10.0
print('== 1. real price per USED GPU-hour = rate / utilisation   (on-demand $10.00 assumed)')
print(f'{"plan":22} {"rate":>7} {"util":>6} {"real $/used hr":>15}  {"beats on-demand?":>17}')
for name, disc, util in [('on-demand', 0.0, 1.0), ('1-3 yr commit', 0.55, 0.9), ('1-3 yr commit', 0.55, 0.45),
                         ('1-3 yr commit', 0.55, 0.30), ('1-3 yr commit', 0.55, 0.10)]:
    rate = OD * (1 - disc); real = rate / util
    print(f'{name:22} {rate:7.2f} {util:5.0%} {real:15.2f}  {"yes" if real < OD else "NO":>17}')
print(f'break-even utilisation for a 55% commit = 1 - 0.55 = {1-0.55:.0%}')

print('\n== 2. $ per petaflop-hour = chip $/hr / dense FP8 PF   (vendor list prices, 14 Oct 2026, GCP)')
for name, price, pf in [('Ironwood on-demand', 12.00, 4.6), ('B200 via Flex-start', 8.06, 4.5),
                        ('Ironwood Flex or 3-yr', 5.40, 4.6), ('Ironwood Flex or 3-yr (high)', 6.00, 4.6)]:
    print(f'{name:30} ${price:5.2f} / {pf} PF = ${price/pf:4.2f} per PF-hr')

print('\n== 3. 1,000 GPU-hours of CHECKPOINTED batch work at the assumed $10 on-demand rate (rate only)')
for name, disc in [('on-demand', 0), ('queued / Flex ~50%', 0.50), ('commit ~55% (if fully used)', 0.55), ('spot, up to 91%', 0.91)]:
    print(f'{name:30} ${1000*OD*(1-disc):9,.0f}')
