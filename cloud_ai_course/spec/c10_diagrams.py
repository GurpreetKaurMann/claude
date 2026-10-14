from cai_lib import bars, boxes, mini2

DIAGRAMS = {
'locks': boxes([('I', 'Identity', 'blue'), ('N', 'Network', 'teal'), ('E', 'Encryption', 'orange'), ('L', 'Logging', 'green'), ('A', 'App authorisation', 'red')], [0, 0, 1, 1, 1], y=50, h=180, size=40,
               note=('I Need Every Lock, Always: you build the last one yourself', 1, 'red')),
'iam': bars([('narrow role', 2, 'green', '2 of 12 requests allowed'), ('broad role', 9, 'red', '9 of 12 allowed')], [0, 1], 12,
            head=('role', 'requests allowed out of 12 (policy checker on the notebook\'s policies)'), x0=190, wmax=440, y0=50, dy=72, bh=48, note=('the broad role could delete models and change the logging', 1, 'red')),
'pii': bars([('emails', 83, 'green', '83%'), ('phone numbers', 86, 'green', '86%'), ('card numbers', 80, 'green', '80%'), ('names', 0, 'red', '0%'), ('addresses', 0, 'red', '0%'), ('ID numbers', 0, 'red', '0%')], [0, 0, 0, 1, 1, 1], 100,
             head=('kind of personal data', 'found by a pattern-based redactor (30 synthetic strings)'), x0=230, wmax=480, y0=40, dy=48, bh=34, note=('patterns cannot find names: add entity recognisers', 1, 'orange')),
'trifecta': boxes([('untrusted content', 'web page, email, RAG chunk', 'orange'), ('private data', 'records, secrets, files', 'blue'), ('external action', 'email, links, images, deletes', 'red')], [0, 0, 1], y=50, h=190, size=28,
                  note=('an agent with all three can be tricked into stealing: pick two', 1, 'red')),
'inject': bars([('A: nothing in place', 12, 'red', '12 of 12 left'), ('B: keyword filter', 9, 'orange', '9 of 12'), ('C: egress allowlist', 0.15, 'green', '0 of 12')], [0, 0, 1], 12,
               head=('setup', 'times the private record LEFT the system (12 attacks, gullible stand-in model)'), x0=270, wmax=400, y0=50, dy=64, bh=42),
'path': boxes([('poisoned page', 'hidden instruction', 'orange'), ('the model reads it', 'and obeys', 'teal'), ('email or image', 'carries the record out', 'red'), ('attacker', 'receives it', 'gray')], [0, 0, 1, 1], y=50, h=180, arrows=True, size=26,
              note=('break any arrow and the leak stops', 1, 'green')),
'tenant': bars([('no filter', 833, 'red', '833 of 1,000 results were another tenant\'s'), ('filter after search', 0.5, 'orange', '0 leaked, but only 0.83 docs returned'), ('filter inside search', 0.5, 'green', '0 leaked, 5.00 docs returned')], [0, 1, 1], 833,
           head=('method', 'other tenants\' documents shown to the user (200 questions, top 5)'), x0=210, wmax=300, y0=50, dy=64, bh=42),
'mini_thumb': mini2('keyword filter stopped', '3 of 12', 'red', 'egress allowlist leaked', '0 of 12', 'green', 'prompt-injection toy test'),
'mini_inject': mini2('no protection: record left', '12 / 12', 'red', 'egress allowlist', '0 / 12', 'green', 'same fooled model', fs=32),
'mini_tenant': mini2('no tenant filter', '83% not yours', 'red', 'filter inside the search', '0% leaked', 'green', 'results shown, 200 questions', fs=34, vs=44),
'mini_iam': mini2('broad role allowed', '9 of 12', 'red', 'narrow role allowed', '2 of 12', 'green', 'requests, policy checker'),
}
