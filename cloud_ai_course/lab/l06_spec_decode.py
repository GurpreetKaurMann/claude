"""Lesson 6 lab D: SIMULATION + formula. Speculative decoding.

A cheap draft guesses gamma tokens. The big model checks them in ONE pass and keeps the accepted run plus one more token. If each guess is accepted with probability alpha,
expected tokens per big-model pass = (1 - alpha^(gamma+1)) / (1 - alpha). We simulate 200,000 passes and compare with the formula, then compute speedup when the draft costs
c (a fraction of a big-model step): speedup = tokens per pass / (1 + gamma x c). alpha, gamma and c are ASSUMED inputs; alpha depends on your model and task.
Run: python3 l06_spec_decode.py
"""
import numpy as np
rng = np.random.default_rng(9)
def tokens_per_pass(alpha, gamma, trials=200_000):
    acc = rng.random((trials, gamma)) < alpha                     # each guess accepted or not
    run = np.where(acc.all(axis=1), gamma, np.argmin(acc, axis=1))   # length of the accepted run
    return (run + 1).mean()
print(f'{"alpha":>6} {"gamma":>6} {"simulated":>10} {"formula":>9} {"speedup (c=0.05)":>17}')
for alpha, gamma in [(0.5, 3), (0.6, 5), (0.7, 5), (0.8, 5), (0.9, 5), (0.55, 5)]:
    sim = tokens_per_pass(alpha, gamma); f = (1 - alpha ** (gamma + 1)) / (1 - alpha)
    print(f'{alpha:6.2f} {gamma:6d} {sim:10.2f} {f:9.2f} {f/(1+gamma*0.05):16.2f}x')
print('speedup below 1.0x = the draft costs more than it saves')
