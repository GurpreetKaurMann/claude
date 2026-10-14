"""Lesson 7 lab A: a WORKING eval gate on a TOY model. The 'model' is a scripted stand-in: a keyword scorer, not a language model.

Task: route support tickets to one of four intents. The 'prompt' is a dictionary of keywords per intent (version 1 and 2). Tickets are SYNTHETIC,
generated from templates, with a deliberately imbalanced mix (delivery is 60 of 100, an ASSUMED shape, imbalance is common in real support traffic).
The gate runs the same test set on both versions and BLOCKS a change if the overall score drops OR any intent's score drops by more than 5 points.
Run: python3 l07_eval_gate.py     (exit code 1 = blocked, like a failing CI step)
"""
import random, sys
random.seed(11)
T = {'refund': ["I want my money back for order {n}", "please refund the charge on my card", "I was charged twice, refund me", "refund my order {n}, it never worked"],
     'delivery': ["my parcel has not arrived", "tracking has not moved for {d} days", "where is my order {n}", "the delivery is late"],
     'account': ["I cannot login to my account", "reset my password please", "change the email on my account", "my account email is wrong"],
     'product': ["the item arrived broken", "wrong size for the shoes", "the colour is different from the photo", "quality is poor"]}
MIX = {'delivery': 60, 'refund': 12, 'account': 14, 'product': 14}
TICKETS = [(random.choice(T[i]).format(n=random.randint(1000, 9999), d=random.randint(3, 12)) + random.choice(['', ' thanks', ' please help']), i) for i, c in MIX.items() for _ in range(c)]
ORDER = ['delivery', 'refund', 'account', 'product']                   # tie-break order
V1 = {'refund': ['refund', 'money back', 'charge'], 'delivery': ['parcel', 'delivery', 'arrive', 'tracking'], 'account': ['password', 'login', 'account', 'email'],
      'product': ['broken', 'size', 'colour', 'quality']}
V2 = {**V1, 'delivery': V1['delivery'] + ['order']}                   # the "improvement": also treat the word 'order' as a delivery signal

def predict(prompt, text):
    s = {i: sum(k in text.lower() for k in kws) for i, kws in prompt.items()}
    best = max(s.values()); return next(i for i in ORDER if s[i] == best) if best else 'unknown'

def score(prompt):
    ok = {i: [0, 0] for i in MIX}
    for text, truth in TICKETS: ok[truth][1] += 1; ok[truth][0] += predict(prompt, text) == truth
    return {i: 100 * a / b for i, (a, b) in ok.items()}, 100 * sum(a for a, _ in ok.values()) / len(TICKETS)

s1, o1 = score(V1); s2, o2 = score(V2)
print(f'{len(TICKETS)} synthetic tickets · version 1 = baseline · version 2 = the proposed change (adds the word "order" to delivery)')
print(f'{"":10} {"v1":>7} {"v2":>7} {"change":>8}')
for i in MIX: print(f'{i:10} {s1[i]:6.1f}% {s2[i]:6.1f}% {s2[i]-s1[i]:+7.1f}')
print(f'{"OVERALL":10} {o1:6.1f}% {o2:6.1f}% {o2-o1:+7.1f}')
reasons = []
if o2 < o1: reasons.append('overall score dropped')
reasons += [f'{i} dropped {s1[i]-s2[i]:.1f} points' for i in MIX if s1[i] - s2[i] > 5]
print('\nGATE:', 'BLOCKED: ' + '; '.join(reasons) if reasons else 'PASSED'); sys.exit(1 if reasons else 0)
