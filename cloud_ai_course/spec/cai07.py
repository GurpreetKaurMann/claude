import sys; sys.path.insert(0, '/home/claude/caigen')
from cai_lib import *
from c07_diagrams import DIAGRAMS
from c07_long import LONG
from c07_notes import NOTES

L = dict(
 code='CAI-07', num=7, num_word='seven', slug='MLOps_And_LLMOps',
 title='MLOps and LLMOps', title_html='MLOps<br>&amp; LLMOps', title_size=140,
 tagline='Ship AI changes safely, again and again.', module='Module 4 · Shipping it',
 toc=['MLOps levels', 'LLMOps: what changes', 'The eval gate', 'Several trials', 'Registries and prompts', 'Infrastructure as code', 'Canary releases'],
 data_label='Course project', project='ShopNest Copilot', project_desc='the AI support assistant we move to the cloud, step by step',
 prev='CAI-06', next=('CAI-08', '<b>GenAI apps: RAG</b>: from documents to cited answers'),
 next_say='generative A I apps. Starting with rag, from documents to cited answers.',
 diagrams=DIAGRAMS, long=LONG, notes=NOTES,
 glow=dict(a='MLOPS AND', b='LLMOPS', icons=['pipe1', '>', 'shield2']),
 thumb=dict(title='MLOps &amp;<br><span class="hl">LLMOps</span>', size=124, sub='the eval gate', chips=('+2 overall', '-50 refunds'), mini='mini_thumb'),

 short1=mk_short(1, 'A_Better_Prompt_That_Broke_Refunds', "I changed a prompt and the score went up. A simple gate blocked it anyway. Here is why.",
   ('SCORE UP', 'BLOCKED', 140, 140),
   ["On a toy model with synthetic tickets, my prompt change lifted the overall score from ninety to ninety-two percent. But refund tickets fell from a hundred percent to fifty.",
    "An eval gate, which also checks every slice, blocked it automatically. The toy model is a stand in, but the gate logic is real."],
   'mini_gate', "Averages hide damage. Score every slice.", 'Rule', 'gate every<br><b>slice</b>', dict(title='Score up.<br><span class="hl">Gate said no.</span>', size=100, sub='averages hide damage', mini='mini_gate'),
   dict(title='My Prompt Change Raised the Score and a Gate Still Blocked It #shorts',
     desc="Toy keyword model (a stand-in for an LLM), 100 synthetic tickets, a real gate:\\n• overall: 90% to 92%\\n• refund tickets: 100% to 50%\\n• gate: BLOCKED (no slice may drop more than 5 points)\\n\\nFull lesson: Cloud for AI Engineers, lesson 7.",
     tags='shorts, eval gate, llm evaluation, llmops, prompt testing, ci cd for llm, cloud for ai engineers, the code notebook',
     pinned='Do you score your prompts by slice or only overall? 👇')),

 short2=mk_short(2, 'A_90_Percent_Agent_Fails_Often', "An agent that works ninety percent of the time passes five runs in a row only fifty-nine percent of the time.",
   ('90% RELIABLE', '59% x5', 110, 150),
   ["Pass at k asks whether at least one run works. Pass hat k asks whether all of them do. For a ninety percent agent, the second is just point nine to the power of k.",
    "Five runs, fifty-nine percent. Ten runs, thirty-five. I checked the formulas against a hundred thousand simulated tasks. The ninety percent is my assumption."],
   'mini_trials', "Reliability falls fast with repeats. Test several runs.", 'Rule', 'run each case<br><b>several times</b>', dict(title='90% reliable?<br><span class="hl">59% x5</span>', size=100, sub='pass^k, simulated', mini='mini_trials'),
   dict(title='A 90% Reliable AI Agent Passes 5 Runs in a Row Only 59% of the Time #shorts',
     desc="pass@k = 1 - (1-p)^k (at least one run works)\\npass^k = p^k (all runs work)\\n\\nFor p = 0.9: all 3 runs 72.9%, all 5 runs 59.0%, all 10 runs 34.9%.\\nFormulas checked against 100,000 simulated tasks per row. p is assumed.\\n\\nFull lesson: Cloud for AI Engineers, lesson 7.",
     tags='shorts, pass at k, agent reliability, llm evaluation, ai agents, evals, cloud for ai engineers, the code notebook',
     pinned='How reliable is your agent across 5 runs? 👇')),

 reel=mk_reel('Canary_Releases_Cut_The_Damage', ["How a five percent canary cut the damage of a bad release by about sixteen times.",
   "I simulated a release that fails five percent of requests instead of one. Sent to everyone at once, about a hundred and fifty bad responses before the rollback. As a five percent canary, nine."],
   "Small first. Save this.", '150 TO 9', ['100% at once: ~150 bad', '5% canary: ~9 bad'], [3.4, 6.2], 'Simulation', 'damage = the<br><b>share</b> you expose',
   dict(title='5% canary:<br><span class="hl">150 to 9</span> bad', size=100, sub='damage scales with share', mini='mini_canary'),
   dict(title='A 5% canary cut the damage of a bad release 16x',
     caption="Canary releases, simulated. 🐤\\n\\n600 requests/min, new version fails 5% vs 1% for the old (assumed).\\n🔴 100% at once: about 150 bad responses before rollback\\n🟠 25% canary: about 38\\n🟢 5% canary: about 9\\n🟢 1% canary: about 4 (but only 45% caught at the first check)\\n\\nSmall first. Save this. Full lesson on YouTube: The Code Notebook.",
     pinned="Lesson 8 next: RAG, from documents to cited answers 📚 Follow so you don't miss it!")),

 upload=dict(
   title='How to Ship AI Without Breaking It: The Eval Gate That Blocked a "Better" Prompt',
   hook="Lesson 7 of Cloud for AI Engineers. I changed a prompt and the overall score went up. Refund tickets fell from 100% to 50%. A simple eval gate blocked it. This lesson is about shipping AI changes safely, again and again.",
   what="We cover the three MLOps maturity levels, what LLMOps versions and monitors, the release loop, three layers of tests, a working eval gate (toy keyword model, synthetic tickets), who should grade, why you run several trials (pass@k and pass^k), the gate as a CI file, registries and aliases, prompt versions, model cards, infrastructure as code and GitOps, canary releases with automatic rollback (simulated), traces and online judges, and cost as a metric. The eval gate uses a toy stand-in model on synthetic data. Trials and canary results are simulations with assumed rates.",
   bullets=['MLOps levels 0, 1 and 2', 'LLMOps: prompts, model settings, tools, retrieval index', 'The release loop: gate, canary, watch', 'Three layers of tests', 'A working eval gate: overall +2.0, refund -50.0, BLOCKED', 'Who grades: code graders first, calibrated LLM judges',
            'pass@k and pass^k: a 90% agent passes 5 runs 59% of the time', 'The gate as a CI file', 'Registries, aliases and prompt versions', 'Model cards', 'Infrastructure as code and GitOps', 'Canary releases: 150 bad responses vs 9 (simulation)',
            'Traces, online judges and cost as an alarm', 'ShopNest Copilot shipping plan', 'Interview questions with answers'],
   hashtags='#mlops #llmops #ai #cicd #aiengineering',
   tags='eval gate, llmops explained, mlops levels, how to test llm prompts, pass at k, canary release, gitops for ml, prompt versioning, model registry, llm evaluation ci, cloud for ai engineers, the code notebook',
   pinned="The eval gate runs a real check on a toy keyword model with synthetic tickets. The trials and canary results are simulations with assumed rates, all labelled in the video. 📊\\n\\nQuestion for you 👇\\nWhich surprised you more: a +2 point change blocked for a -50 slice, or a 90% agent passing 5 runs only 59% of the time?"),
)

import interview; L['notes'] = interview.add(L['notes'], L['num'])
