"""Lesson 11 lab 3 (ARITHMETIC + a small simulation): self-host vs API.
Inputs from the notebook (Oct 2026, approximate): one H100 at $3.17/hr, ~400 tok/s for a 70B model at FP8 (vendor, likely conservative),
API blended list price at 80% input / 20% output: Opus 5.5 $7.20, Sonnet 5.5 $3.60, Haiku 5.5 $0.18 per million tokens. Run: python3 l11_breakeven.py"""
import math, random
GPU_HR, TOKS = 3.17, 400
day_cost = GPU_HR * 24; cap = TOKS * 86400 / 1e6
print(f'one H100 24/7 = ${day_cost:.2f}/day; capacity at {TOKS} tok/s = {cap:.1f}M tokens/day')
print('\nSELF-HOST $/MTok = GPU $/hr / (tok/s x 3600 x utilisation) x 1e6')
for u in (1.0, .6, .4, .15): print(f'  utilisation {u:4.0%}: ${GPU_HR/(TOKS*3600*u)*1e6:5.2f} per MTok')
print('\nBREAK-EVEN volume = GPU $/day / API blended $/MTok')
for n, p in (('Opus 5.5', 7.20), ('Sonnet 5.5', 3.60), ('Haiku 5.5', 0.18)):
    be = day_cost / p
    v = 'self-host can win above this' if be < cap * .5 else ('narrow window up to the GPU limit' if be < cap else 'never on one GPU (above its capacity)')
    print(f'  {n:11s} ${p:5.2f}: {be:6.1f}M tokens/day -> {v}')
print(f'  Sonnet 5.5 with the GPU at an AWS block price $5.97/hr: {5.97*24/3.60:.1f}M tokens/day (capacity {cap:.1f}M) -> never on one GPU')

print('\nSHAPES: cost per day at different volumes (M tokens/day), one H100, step when full')
print(f'{"volume":>8} {"API Sonnet":>11} {"self-host":>10}')
for v in (5, 10, 21.1, 30, 34.0, 45, 69.0):
    gpus = math.ceil(v / cap); print(f'{v:8.1f} {v*3.60:11.2f} {gpus*day_cost:10.2f}  ({gpus} GPU{"s" if gpus>1 else ""})')

print('\nSIMULATION: bursty daily traffic on a fixed single GPU (mean 20M tokens/day, daily swings)')
random.seed(11)
vol = [max(1, random.lognormvariate(math.log(20), .6)) for _ in range(365)]
served_self = sum(min(v, cap) for v in vol); overflow = sum(max(0, v - cap) for v in vol)
api_only = sum(v * 3.60 for v in vol); hybrid = 365 * day_cost + overflow * 3.60
print(f'  all API (Sonnet 5.5): ${api_only:,.0f}/yr   self-host base load + API overflow: ${hybrid:,.0f}/yr')
print(f'  GPU actually used: {served_self/(cap*365):.0%} of its capacity; {overflow/sum(vol):.1%} of tokens overflowed to the API')
print('  (excludes on-call, upgrades, spare replicas, quality gap of an open model: the simple sum flatters self-hosting)')
