"""Lesson 12 capstone (CHECK, not a new experiment): the claims ledger.
For each headline number I quoted in lessons 1-11, this script looks it up in the saved output of the lab that produced it (results/*.txt) and
prints the label it carries: measured (timed or counted on this machine), simulation (code with assumed inputs), arithmetic (a formula on listed
inputs) or synthetic (made-up data). A claim that is not found in its file shows MISSING. Run the lab scripts to regenerate the files.
Run from the lab folder: python3 l12_claims_ledger.py"""
import re, os
R = 'results'
CLAIMS = [  # (lesson, claim, label, results file, regex that must match)
 (1, '70B FP8 + 32 chats + headroom = 187 GB', 'arithmetic', 'l01_fit_math', r'= 187 GB'),
 (1, 'batch 256 serves 4,180 tokens/s vs 387 at batch 1', 'measured', 'l01_memory_bound', r'256\s+61\.24\s+4180'),
 (2, 'spot with no checkpoints: 2,203,564 hours for a 100 hour job', 'simulation', 'l02_spot_checkpoint', r'2203564'),
 (2, 'checkpoint about every 34 min: 108.8 hours', 'simulation', 'l02_spot_checkpoint', r'34 min \(Young\)\s+108\.8'),
 (2, 'scale to zero: 4.04 GPU-hours a day instead of 24', 'simulation', 'l02_scale_to_zero', r'scale to zero\s+4\.04'),
 (3, 'code change ships 1 MB, new weights 401 MB (layer order)', 'measured', 'l03_layers', r'A: weights baked in, code last\s+611 MB\s+1 MB\s+401 MB'),
 (3, '3 jobs on 16 GPUs deadlock 94.8% without gang scheduling', 'simulation', 'l03_gang', r'3\s+94\.8%\s+0\.0%'),
 (4, '20,000 small files read 25.1x slower than one shard', 'measured', 'l04_small_files', r'25\.1x'),
 (4, 'int8 vectors: 4x smaller, recall@10 0.985', 'measured', 'l04_vectors', r'int8\s+768\s+38\.4\s+4x\s+0\.985'),
 (4, '100 TB egress at $0.09/GB = $9,000', 'arithmetic', 'l04_checkpoint_math', r'100 TB out =\s+100,000 GB x \$0\.09 = \$\s+9,000'),
 (5, 'mixed Adam training state = 16.0 bytes per parameter', 'measured', 'l05_memory_ledger', r'16\.0 bytes per parameter'),
 (5, 'LoRA rank 8 trains 0.97% of parameters', 'measured', 'l05_memory_ledger', r'rank  8: trains .* = 0\.97%'),
 (5, 'pipeline bubble 42.9% at p=4, m=4', 'simulation', 'l05_bubble_sim', r'idle share: 42\.9%'),
 (6, 'KV cache: 12.1x faster generation', 'measured', 'l06_decode_kv', r'12\.1x slower'),
 (6, 'continuous batching 1,243 vs 335 tokens/s', 'simulation', 'l06_batching_sim', r'continuous\s+192s\s+1243'),
 (6, 'int8 groups of 64: 1.4% error', 'measured', 'l06_quant_error', r'int8, groups of 64\s+1\.06\s+0\.01414'),
 (7, 'eval gate blocks a prompt that raised the average (refund -50)', 'synthetic', 'l07_eval_gate', r'BLOCKED: refund dropped 50\.0 points'),
 (7, 'a 90% agent passes 5 runs in a row 59% of the time', 'simulation', 'l07_trials', r'0\.90\s+5\s+1\.000\s+1\.000\s+0\.590'),
 (7, '5% canary: 9.4 bad responses before rollback', 'simulation', 'l07_canary_sim', r'5%\s+77%\s+1\.25\s+9\.4'),
 (8, '300-word chunks, dense stand-in hit@3 91.7%', 'measured', 'l08_rag_eval', r'300 wd\s+177\s+dense \(LSA\)\s+66\.7%\s+91\.7%'),
 (9, 'restart without keys: 2 refunds', 'simulation', 'l09_agent_loop', r'no keys\s+tool calls in total: 14 · refunds issued: 2'),
 (9, 'retries without jitter: last success at 211 s', 'simulation', 'l09_retry_breaker', r'exponential, no jitter\s+2070\s+2010\s+211\.0s'),
 (9, '8x steps = 24.2x input tokens', 'arithmetic', 'l09_agent_cost', r'40\s+27,400\s+628,000\s+24\.2x'),
 (10, 'keyword filter: 9 of 12 attacks still leaked', 'simulation', 'l10_injection_toy', r'B  keyword filter on retrieved text\s+9/12\s+9/12'),
 (10, 'egress allowlist: 0 of 12 left, model fooled 12/12', 'simulation', 'l10_injection_toy', r'C  egress allowlist \(email \+ images\)\s+12/12\s+0/12'),
 (10, 'no tenant filter: 833 of 1,000 results not yours', 'synthetic', 'l10_tenant_leak', r'no filter\s+833\s+5\.00'),
 (10, 'broad role allowed 9 of 12, narrow 2', 'simulation', 'l10_iam_check', r'narrow role 2 of 12 · broad role 9 of 12'),
 (10, 'PII patterns found 58% overall, 0% of names', 'synthetic', 'l10_pii_redact', r'name\s+0\s+4\s+0%'),
 (11, 'H100 at 5% use: $63.40 per useful hour', 'arithmetic', 'l11_gpu_price', r'5%\s+63\.40'),
 (11, 'timestamp on top of the prompt: 0% of tokens cached', 'measured', 'l11_token_cost', r'TOP of the system prompt: 0\.0% of tokens'),
 (11, 'timestamp after the shared part: 74.9% cached', 'measured', 'l11_token_cost', r'AFTER the cached prefix:\s+74\.9%'),
 (11, 'one H100 beats a Sonnet-class API above 21.1M tokens/day', 'arithmetic', 'l11_breakeven', r'Sonnet 5\.5\s+\$ 3\.60:\s+21\.1M'),
]
found = 0; by = {}
print(f'{"L":>2} {"label":11s} {"status":8s} claim')
for n, claim, label, f, rx in CLAIMS:
    p = os.path.join(R, f + '.txt'); ok = os.path.exists(p) and re.search(rx, open(p).read()) is not None
    found += ok; by[label] = by.get(label, 0) + 1
    print(f'{n:2d} {label:11s} {"ok" if ok else "MISSING":8s} {claim}')
print(f'\n{found} of {len(CLAIMS)} headline claims found in their saved results')
print('by label: ' + ' · '.join(f'{k} {v}' for k, v in sorted(by.items())))
