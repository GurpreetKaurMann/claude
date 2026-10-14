"""Lesson 10 lab D: MEASURED recall of a simple pattern-based PII redactor, on 30 SYNTHETIC test strings I wrote (made-up data, not real people).

The redactor uses regular expressions for emails, phone numbers and card numbers (with a Luhn check). Recall = share of the personal items it found.
Names and addresses have no fixed pattern, so patterns cannot find them: real systems add entity recognisers (the notebook names Presidio, Comprehend,
Sensitive Data Protection). Run: python3 l10_pii_redact.py
"""
import re
CASES = [  # (text, kind of PII it contains)
 ('mail me at anna.k@example.com please', 'email'), ('contact: j_doe99@shop.example.org', 'email'), ('my work email is dev+tag@co.example', 'email'), ('reach AMIT@Example.COM today', 'email'),
 ('email: first.last@sub.domain.example.co.uk', 'email'), ('write to support at example dot com', 'email'),
 ('call +44 20 7946 0958', 'phone'), ('phone 020-7946-0958', 'phone'), ('my number is (415) 555-0132', 'phone'), ('ring me on 07700 900123', 'phone'),
 ('whatsapp +91 98765 43210', 'phone'), ('tel: 4155550132', 'phone'), ('call me five five five zero one three two', 'phone'),
 ('card 4111 1111 1111 1111 expires 12/28', 'card'), ('pay with 4111-1111-1111-1111', 'card'), ('my visa is 4111111111111111', 'card'), ('card number 5500 0000 0000 0004', 'card'),
 ('card ending 4242', 'card'), ('order number 1234 5678 9012 3456', 'none'), ('tracking 4111 1111 1111 1112', 'none'),
 ('I am Priya Sharma and I live at 12 Rose Lane', 'name'), ('ask for Mr. John Smith', 'name'), ('this is Maria Garcia speaking', 'name'), ('deliver to 221B Baker Street, London', 'address'),
 ('my address is Flat 3, 45 High Street', 'address'), ('Sofia Rossi, 10 Via Roma, Milano', 'name'), ('national id AB 12 34 56 C', 'id'), ('passport X1234567', 'id'),
 ('the weather is nice and the refund is late', 'none'), ('order 998877 has not arrived', 'none')]
def luhn(num):
    d = [int(c) for c in re.sub(r'\D', '', num)][::-1]
    return len(d) in (13, 15, 16) and sum(x if i % 2 == 0 else (x * 2 - 9 if x * 2 > 9 else x * 2) for i, x in enumerate(d)) % 10 == 0
EMAIL = re.compile(r'[\w.+-]+@[\w-]+(\.[\w-]+)+', re.I)
PHONE = re.compile(r'(?<!\d)(\+?\d[\d\s().-]{8,}\d)(?!\d)')
CARD = re.compile(r'(?<!\d)(?:\d[ -]?){13,16}(?!\d)')
def redact(text):
    found = []
    for m in EMAIL.finditer(text): found.append('email')
    for m in CARD.finditer(text):
        if luhn(m.group(0)): found.append('card')
    for m in PHONE.finditer(text):
        if not any(m.group(0).replace(' ', '').replace('-', '') in c.group(0).replace(' ', '').replace('-', '') for c in CARD.finditer(text) if luhn(c.group(0))): found.append('phone')
    return found
rows = {}
for text, kind in CASES:
    f = redact(text)
    if kind != 'none': r = rows.setdefault(kind, [0, 0]); r[1] += 1; r[0] += kind in f
fp = sum(1 for t, k in CASES if k == 'none' and redact(t))
print(f'{"kind of PII":10} {"found":>6} {"of":>3} {"recall":>8}')
for k, (a, b) in rows.items(): print(f'{k:10} {a:6d} {b:3d} {100*a/b:7.0f}%')
tot = sum(a for a, _ in rows.values()); allb = sum(b for _, b in rows.values())
print(f'{"ALL":10} {tot:6d} {allb:3d} {100*tot/allb:7.0f}%      false alarms on {fp} of {sum(1 for t,k in CASES if k=="none")} harmless strings')
