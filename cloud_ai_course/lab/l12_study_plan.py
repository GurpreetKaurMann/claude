"""Lesson 12 lab (ARITHMETIC on the notebook's estimates, Oct 2026): how long the six-stop path takes at your weekly hours, what it costs out of pocket,
and what one forgotten GPU costs. Project costs are the notebook's ESTIMATES from Sep-Oct 2026 list prices, credits not subtracted.
Edit HOURS_PER_WEEK and run: python3 l12_study_plan.py"""
HOURS_PER_WEEK = 10
STAGES = [  # (stop, weeks in the 12-16 week plan, project cost low $, high $)
 ('1 Cloud fundamentals', 2, 0, 5), ('2 Containers + Kubernetes', 3, 3.4, 11), ('3 Serve a model', 2, 2, 6),
 ('4 RAG, agents, MCP + evals', 3, 0, 10), ('5 MLOps, IaC, observability', 3, 2, 25), ('6 Distributed training', 3, 25, 98)]
weeks = sum(s[1] for s in STAGES); hours = weeks * 10
print(f'plan: {weeks} weeks at about 10 h/week = {hours} hours')
print(f'\n{"hours/week":>10} {"weeks":>7}')
for h in (5, 10, 15, 20): print(f'{h:10d} {hours / h:7.1f}')
print(f'\nyour setting: {HOURS_PER_WEEK} h/week -> {hours / HOURS_PER_WEEK:.1f} weeks')
print(f'\n{"stop":30s} {"weeks":>5} {"low $":>7} {"high $":>7}')
lo = hi = 0
for n, w, a, b in STAGES: lo += a; hi += b; print(f'{n:30s} {w:5d} {a:7.0f} {b:7.0f}')
print(f'{"all six stops (before credits)":30s} {weeks:5d} {lo:7.0f} {hi:7.0f}')
print(f'new-account credits quoted: AWS up to $200 + GCP $300 + Azure $200 = $700 -> the notebook estimates $150-250 out of pocket in total if everything is torn down')
print(f'stages 1-5 only: ${sum(s[2] for s in STAGES[:5]):.0f} to ${sum(s[3] for s in STAGES[:5]):.0f}')
print('\nTHE FORGOTTEN GPU: one L4 node left up for a month = 730 h x $0.50-1.20')
a, b = 730 * .50, 730 * 1.20
print(f'  ${a:,.0f} to ${b:,.0f}  vs the whole path at ${hi:,.0f} (high) -> {a / hi:.1f}x to {b / hi:.1f}x the entire path')
print('  teardown habit: terraform destroy, then list clusters and expect nothing')
print('\nEKS control plane: $0.10/h standard support vs ~$0.60/h extended support (notebook; one source says $0.50)')
print(f'  per month: ${0.10*730:.0f} vs ${0.60*730:.0f}')
