from cai_lib import bars, boxes, mini2

DIAGRAMS = {
'road': boxes([('F', 'cloud basics', 'blue'), ('C', 'containers', 'teal'), ('S', 'serve', 'orange'), ('R', 'RAG + evals', 'green'), ('M', 'MLOps', 'red'), ('D', 'distributed', 'gray')], [0, 0, 0, 1, 1, 1], y=50, h=170, arrows=True, size=64,
              note=('Frugal Coders Spend Really Modest Dollars', 1, 'green')),
'weeks': bars([('5 h a week', 32, 'red', '32 weeks'), ('10 h a week', 16, 'orange', '16 weeks'), ('15 h a week', 10.7, 'teal', '10.7 weeks'), ('20 h a week', 8, 'green', '8 weeks')], [0, 0, 1, 1], 32,
              head=('your pace', 'weeks to finish all six stops (160 hours, arithmetic)'), x0=190, wmax=470, y0=44, dy=54, bh=38, note=('about 160 hours in total', 1, 'green')),
'stagecost': bars([('1 fundamentals', 5, 'green', 'up to $5'), ('2 containers', 11, 'green', 'up to $11'), ('3 serving', 6, 'green', 'up to $6'), ('4 RAG + evals', 10, 'green', 'up to $10'), ('5 MLOps', 25, 'orange', 'up to $25'), ('6 distributed', 98, 'red', 'up to $98')], [0, 0, 0, 1, 1, 1], 100,
                  head=('stop', 'highest project estimate per stop (notebook estimates, before credits)'), x0=210, wmax=440, y0=40, dy=44, bh=32, note=('spend climbs along the road: pay for GPUs from stop 3', 1, 'orange')),
'forgot': bars([('whole path', 155, 'green', 'up to $155'), ('L4 month, low', 365, 'orange', '$365'), ('L4 month, high', 876, 'red', '$876')], [0, 1, 1], 900,
               head=('what you spend', 'estimate, 730 hours at $0.50 to $1.20 an hour vs the sum of all project estimates'), x0=230, wmax=440, y0=50, dy=62, bh=42, note=('one forgotten GPU can cost more than the whole path', 1, 'red')),
'ledger': bars([('measured', 11, 'green', '11 claims'), ('simulation', 13, 'teal', '13 claims'), ('arithmetic', 5, 'orange', '5 claims'), ('synthetic data', 3, 'gray', '3 claims')], [0, 0, 1, 1], 14,
               head=('label', '32 of 32 headline numbers found in their saved results'), x0=230, wmax=420, y0=44, dy=54, bh=38, note=('every number carries its label', 1, 'green')),
'mini_thumb': mini2('16 weeks at 10 hours a week', '160 h', 'green', 'out of pocket, notebook estimate', '$150-250', 'amber', 'if you tear everything down', fs=30, vs=50),
'mini_forgot': mini2('one L4 left up for a month', '$365-876', 'red', 'the whole 16-week path', 'up to $155', 'green', 'notebook estimates, Oct 2026', fs=32, vs=48),
'mini_cert': mini2('retired in 2026: MLS-C01', 'old code', 'red', 'check the exam code first', 'then book', 'green', 'notebook list, Oct 2026', fs=32, vs=48),
}
