"""Lesson 9 lab B: ARITHMETIC. Why agent loops get expensive, and what prompt caching does.

An agent re-sends its whole history every step. Assumed sizes (ASSUMED, typical shape): system prompt + tools 4,000 tokens; each step adds a model
reply of 100 tokens and a tool result of 500 tokens. Input tokens in step n = 4,000 + 600 x (n - 1). Total input over N steps grows with N squared.
Caching: prices in USD per million tokens are the example in the notebook (a Sonnet-class model): input 2.00, cache write 2.50, cache read 0.10 (vendor example, Oct 2026).
Part 3 reproduces the notebook's example: 100 calls with a 50,000-token shared prefix. Run: python3 l09_agent_cost.py
"""
SYS, REPLY, RESULT = 4000, 100, 500
IN, WRITE, READ = 2.00, 2.50, 0.10
def totals(n):
    ins = [SYS + (REPLY + RESULT) * i for i in range(n)]          # input tokens at each step
    return sum(ins), ins
print('== 1. input tokens billed by an agent that re-sends its history every step')
print(f'{"steps":>6} {"last step input":>16} {"total input tokens":>19} {"vs 5 steps":>11}')
base = totals(5)[0]
for n in [5, 10, 20, 40]:
    t, ins = totals(n); print(f'{n:6d} {ins[-1]:16,} {t:19,} {t/base:10.1f}x   (steps x {n/5:.0f}, cost x {t/base:.1f})')
print('\n== 2. the same 20-step agent, with and without prompt caching (cost per run, USD)')
t, ins = totals(20)
nocache = t / 1e6 * IN
cached = 0.0; seen = 0
for x in ins:
    cached += (x - seen) / 1e6 * WRITE + seen / 1e6 * READ; seen = x   # new tokens are written to the cache, earlier ones are read
print(f'no cache: ${nocache:.4f}   cached: ${cached:.4f}   saving {100*(1-cached/nocache):.0f}%   (assumes every step is within the cache lifetime)')
print('\n== 3. notebook example: 100 calls, a 50,000-token shared prefix')
n, pre = 100, 50_000
a = n * pre / 1e6 * IN; b = pre / 1e6 * WRITE + (n - 1) * pre / 1e6 * READ
print(f'no cache: ${a:.2f}   cached: ${b:.3f}   saving {100*(1-b/a):.0f}%')
