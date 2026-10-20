import sys; sys.path.insert(0, '/home/claude/caigen')
from cai_lib import *
from c11_diagrams import DIAGRAMS
from c11_long import LONG
from c11_notes import NOTES

L = dict(
 code='CAI-11', num=11, num_word='eleven', slug='Cost_And_FinOps',
 title='Cost and FinOps', title_html='Cost &amp;<br>Fin Ops', title_size=120,
 tagline='Where the money really goes, and which lever to pull first.', module='Module 5 · Safe, cheap, and your career',
 toc=['The Fin Ops loop', 'The real price of a GPU', 'Ways to buy', 'The token bill and five levers', 'Self-host or API', 'Attribution and alerts', 'Hidden lines'],
 data_label='Course project', project='ShopNest Copilot', project_desc='the AI support assistant we move to the cloud, step by step',
 prev='CAI-10', next=('CAI-12', '<b>Your learning path</b>: from zero to cloud AI engineer'),
 next_say='your learning path. From zero to cloud A I engineer.',
 diagrams=DIAGRAMS, long=LONG, notes=NOTES,
 glow=dict(a='A $3 GPU', b='REALLY COSTS $63', icons=['chip1', '>', 'check2']),
 thumb=dict(title='A $3 GPU<br><span class="hl">costs $63</span>', size=110, sub='at 5% use', chips=('list: $3.17', 'real: $63.40'), mini='mini_thumb'),

 short1=mk_short(1, 'A_3_Dollar_GPU_Really_Costs_63', "A G P U listed at three dollars seventeen an hour can really cost sixty-three dollars. Here is the sum.",
   ('$3.17 → $63', 'AT 5% USE', 110, 120),
   ["The real price of a G P U hour is the list price divided by utilisation. At five percent use, a three dollar seventeen H one hundred costs sixty-three dollars forty per useful hour.",
    "At fifty percent it is six thirty-four. Ten times cheaper, with no negotiating. The best rate discounts only give two or three times. Fix idle time first."],
   'mini_thumb', "Real price is list price divided by utilisation.", 'Rule', 'divide by<br><b>utilisation</b>', dict(title='A $3 GPU<br><span class="hl">costs $63</span>', size=100, sub='at 5% use', mini='mini_thumb'),
   dict(title='Why a $3 GPU Really Costs $63 (The Utilisation Sum) #shorts',
     desc="Arithmetic from the notebook's Oct 2026 prices (they move often):\\n• H100 listed $3.17/hr\\n• real price = list price / utilisation\\n• 5% use: $63.40 per useful hour\\n• 50% use: $6.34\\n• best rate discounts: about 2-3x, fixing idle: 10x\\n\\nFull lesson: Cloud for AI Engineers, lesson 11.",
     tags='shorts, gpu cost, finops, gpu utilization, cloud cost, ai infrastructure cost, h100 price, cloud for ai engineers, the code notebook',
     pinned='What utilisation does your GPU cluster really run at? 👇')),

 short2=mk_short(2, 'One_Prompt_Line_Triples_Your_AI_Bill', "One line at the top of your prompt can triple your A I bill, and the answers stay identical.",
   ('0% CACHED', '3.5X THE BILL', 130, 100),
   ["A prompt cache matches the start of a prompt. I wrote a toy cache and sent it five thousand requests. With a timestamp at the very top, zero percent of tokens were reused.",
    "Moving the same timestamp after the shared part, seventy-five percent were. The input bill was three and a half times higher. Stable text first, changing text last."],
   'mini_ts', "Stable text first. Changing text last.", 'Rule', 'stable first,<br>changing <b>last</b>', dict(title='One line<br><span class="hl">triples the bill</span>', size=100, sub='the prompt cache mistake', mini='mini_ts'),
   dict(title='One Line in Your Prompt Can Triple Your AI Bill (Cache Mistake) #shorts',
     desc="Measured with a toy prefix cache I wrote (not any vendor's cache), 5,000 requests of about 4,000 tokens:\\n• changing timestamp at the TOP of the system prompt: 0% of tokens cached\\n• same timestamp AFTER the shared part: 74.9% cached\\n• input bill 3.5x higher with the timestamp on top\\n\\nFull lesson: Cloud for AI Engineers, lesson 11.",
     tags='shorts, prompt caching, llm cost, finops, claude api cost, ai bill, prompt engineering, cloud for ai engineers, the code notebook',
     pinned='Is anything at the top of your system prompt changing per request? 👇')),

 reel=mk_reel('Self_Hosting_Never_Beats_A_Cheap_API', ["Will one G P U ever beat a cheap A P I?",
   "I did the sum. One H one hundred costs seventy-six dollars a day and holds about thirty-five million tokens. Against a premium model it can win from about eleven to twenty-one million tokens a day. Against a Haiku class A P I it needs four hundred and twenty-three million. It never wins."],
   "Compare cost per task. Save this.", '423M', ['Sonnet API: wins above 21M/day', 'Haiku API: needs 423M/day'], [3.0, 5.6], 'Rule', 'cost per<br><b>solved task</b>',
   dict(title='One GPU never<br><span class="hl">beats this API</span>', size=100, sub='the self-host sum', mini='mini_be'),
   dict(title='One H100 never beats a Haiku-class API (the self-host break-even)',
     caption="Self-host or API? 🤔\\n\\nThe break-even sum (arithmetic, notebook prices Oct 2026):\\n🟢 vs Opus 5.5: one H100 can win above ~10.6M tokens/day\\n🟠 vs Sonnet 5.5: above ~21.1M (one card tops out at 34.6M)\\n🔴 vs Haiku 5.5: needs ~423M/day, never on one GPU\\n\\nCompare cost per solved task. Save this. Full lesson on YouTube: The Code Notebook.",
     pinned="Lesson 12 next: your learning path, the finale 🎓 Follow so you don't miss it!")),

 upload=dict(
   title='Why a $3 GPU Really Costs $63 (and the Prompt Line That Triples Your AI Bill)',
   hook="Lesson 11 of Cloud for AI Engineers. A GPU listed at $3.17 an hour costs $63.40 per useful hour at 5% utilisation. And one changing line at the top of a prompt gave 0% cache hits in my test, a 3.5x higher input bill.",
   what="We cover the FinOps loop (inform, optimise, operate), measuring utilisation honestly, the real price of a GPU hour, right-sizing and sharing (MIG, time-slicing, MPS), ways to buy GPU time and the commitment rule (use must beat 1 minus the discount), one training run priced five ways (5.4x spread), token pricing, a costed support bot, the five levers in order (cache, batch, prompt audit, effort, routing), cache hit rate against traffic, the timestamp mistake measured with a toy cache, self-hosting versus API with a break-even calculator, attribution with a gateway, cost per resolved ticket, budgets and anomaly alerts, and hidden storage and network lines. Prices are the notebook's approximate list prices (Oct 2026) and move often, the cache is a toy I wrote, and the gateway logs are invented.",
   bullets=['The Fin Ops loop: inform, optimise, operate', 'Why nvidia-smi utilisation misleads', 'Real price = list price / utilisation: $3.17 becomes $63.40 at 5%', 'MIG, time-slicing and MPS', 'Ways to buy: on-demand, reserved, capacity block, spot, flex start',
            'The commitment rule: use must beat 1 minus the discount', 'One training run, five ways to pay: 5.4x spread', 'Token pricing and a costed support bot', 'Caching, batch, prompt audit, effort and routing: the lever order', 'Cache hit rate vs traffic (simulated)',
            'The timestamp mistake: 0% cached vs 75% (toy cache, measured)', 'Self-host vs API break-even volume', 'Attribution, showback and cost per resolved ticket', 'Budgets and anomaly alerts (invented logs)', 'Hidden lines: cross-AZ and checkpoint storage', 'Interview questions with answers'],
   hashtags='#finops #aicost #gpu #llm #cloudcomputing',
   tags='finops for ai, gpu utilization, real price of a gpu, llm api cost, prompt caching, self host vs api, break even calculator, cost per resolved ticket, ai cost optimization, cloud for ai engineers, the code notebook',
   pinned="Prices are the notebook's approximate Oct 2026 list prices and change often, the cache test uses a toy cache I wrote, and the gateway logs are invented. 📊\\n\\nQuestion for you 👇\\nWhat is your biggest AI cost: GPUs sitting idle, or tokens you send again and again?"),
)

import interview; L['notes'] = interview.add(L['notes'], L['num'])
