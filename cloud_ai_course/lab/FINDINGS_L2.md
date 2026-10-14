# FINDINGS: Lesson 2 (renting compute)
All three scripts are SIMULATIONS or ARITHMETIC (no cloud account, no GPU). Rates/prices marked ASSUMED are mine; chip facts and discount ranges are vendor figures from the notebook (14 Oct 2026).
## l02_spot_checkpoint.py (simulation, 2,000 runs per setting, seed 42, assumed MTBF 8 h, restart 0.1 h, save cost 0.02 h, spot 30% of on-demand)
never: 2,203,564.1 h (661,069 cost units) · 8 h: 172.4 h, 51.7 · 2 h: 116.3, 34.9 · 30 min: 108.8, 32.6 · 34 min (Young): 108.8, 32.6 · 10 min: 114.7, 34.4 · 2 min: 162.6, 48.8 · 30 s: 344.8, 103.5 (400 runs). Young: sqrt(2*8*0.02)=0.566 h = 34 min.
## l02_buying_math.py (arithmetic)
55% commit at assumed $10 on-demand: 90% busy $5.00, 45% busy $10.00, 30% busy $15.00, 10% busy $45.00. Break-even 45%. $/PF-hr: 2.61, 1.79, 1.17, 1.30.
## l02_scale_to_zero.py (simulation, 200 seeded days; busy 3 h at 1 req/12 s, light 1 h at 1 req/120 s, 5 s service, idle off 5 min, cold start 60 s assumed)
always on: 24.00 GPU-h, mean wait 1.71 s, p95 7.90 s, max 39.10 s. scale to zero: 4.04 GPU-h, mean 2.31 s, p95 8.86 s, max 80.42 s, 3.86 cold starts/day each 60.00 s.
