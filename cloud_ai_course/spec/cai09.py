import sys; sys.path.insert(0, '/home/claude/caigen')
from cai_lib import *
from c09_diagrams import DIAGRAMS
from c09_long import LONG
from c09_notes import NOTES

L = dict(
 code='CAI-09', num=9, num_word='nine', slug='Agents_MCP_And_Reliability',
 title='Agents and Reliability', title_html='Agents &amp;<br>reliability', title_size=130,
 tagline='The agent loop, MCP, and how not to refund twice.', module='Module 4 · Shipping it',
 toc=['The agent loop', 'What loops cost', 'Prompt caching', 'MCP and A2A', 'The crash experiment', 'Jitter and breakers', 'Interview Q&amp;A'],
 data_label='Course project', project='ShopNest Copilot', project_desc='the AI support assistant we move to the cloud, step by step',
 prev='CAI-08', next=('CAI-10', '<b>Security and governance</b>: identity, prompt injection, least privilege'),
 next_say='security and governance. Identity, prompt injection and least privilege.',
 diagrams=DIAGRAMS, long=LONG, notes=NOTES,
 glow=dict(a='AGENTS AND', b='RELIABILITY', icons=['wheel1', '>', 'shield2']),
 thumb=dict(title='Agents &amp;<br><span class="hl">reliability</span>', size=110, sub='the double refund', chips=('restart: 2 refunds', 'resume: 1'), mini='mini_thumb'),

 short1=mk_short(1, 'My_Agent_Crashed_And_Refunded_Twice', "I crashed an A I agent halfway through a refund. Restarting it refunded the customer twice.",
   ('CRASH', '2 REFUNDS', 170, 130),
   ["I built a working agent loop with a scripted stand in for the model. Nine tool steps, and I killed it just before the email step. Restarted from scratch, it issued the refund again. Two refunds.",
    "Resumed from its checkpoint, one refund, and only eight tool calls in total. An idempotency key on the refund also gives one. Checkpoint every step."],
   'mini_replay', "Checkpoint every step. Key every side effect.", 'Rule', 'resume,<br><b>never restart</b>', dict(title='Crash, restart:<br><span class="hl">2 refunds</span>', size=100, sub='resume + idempotency keys', mini='mini_replay'),
   dict(title='My AI Agent Crashed and Refunded the Customer Twice #shorts',
     desc="A working agent loop (the model is a scripted stand-in), 9 tool steps, process killed just before the email step:\\n• restart from step 1, no keys: 14 tool calls, 2 refunds\\n• restart + idempotency key: 1 refund\\n• resume from checkpoint: 8 tool calls, 1 refund\\n\\nFull lesson: Cloud for AI Engineers, lesson 9.",
     tags='shorts, ai agents, idempotency key, agent reliability, checkpointing, durable execution, cloud for ai engineers, the code notebook',
     pinned='Do your agents have idempotency keys? 👇')),

 short2=mk_short(2, 'Jitter_211_Seconds_To_9_Seconds', "One random number turned a two hundred and eleven second retry storm into nine point nine seconds.",
   ('211 S TO 9.9 S', 'ONE RANDOM NUMBER', 110, 90),
   ["I simulated two hundred clients hitting a server that accepts fifty requests a second. With backoff but no jitter, the last client finished at two hundred and eleven seconds. With full jitter, nine point nine.",
    "Jitter means waiting a random time between zero and the cap, so retries spread out instead of arriving in waves. The capacity and client count are my assumptions."],
   'mini_jitter', "Always add jitter to your retries.", 'Rule', 'wait a<br><b>random</b> time', dict(title='One random number:<br><span class="hl">211 s to 9.9 s</span>', size=92, sub='retry jitter, simulated', mini='mini_jitter'),
   dict(title='One Random Number Cut a Retry Storm From 211 s to 9.9 s #shorts',
     desc="Simulation: 200 clients call at second 0, the server accepts 50 requests per second (assumed), up to 12 retries:\\n• no jitter: 2,010 rejected attempts, last client at 211 s, 140 clients gave up\\n• full jitter: 444 rejected attempts, last client at 9.9 s, none gave up\\n\\nwait = random(0, min(cap, base x 2^attempt))\\n\\nFull lesson: Cloud for AI Engineers, lesson 9.",
     tags='shorts, retry with jitter, exponential backoff, thundering herd, api rate limits, llm api reliability, cloud for ai engineers, the code notebook',
     pinned='Do you add jitter to your retries? 👇')),

 reel=mk_reel('Agent_Loops_Cost_Squared', ["Why long agent loops cost so much.",
   "An agent re sends its whole history on every step. With assumed sizes, five steps bill twenty-six thousand input tokens. Forty steps, six hundred and twenty-eight thousand. Eight times the steps, twenty-four times the tokens. Caching the stable start of the prompt cuts that by about eighty-five percent."],
   "Cache the prefix. Save this.", '8X = 24X', ['5 steps: 26K tokens', '40 steps: 628K tokens'], [3.0, 5.6], 'Arithmetic', 'cost grows with<br><b>steps squared</b>',
   dict(title='8x the steps,<br><span class="hl">24x the cost</span>', size=100, sub='agent loops, arithmetic', mini='mini_loop'),
   dict(title='Why long agent loops cost so much',
     caption="Agent loops re-send the whole history every step. 🔁\\n\\nAssumed sizes: 4,000-token prompt, each step adds 600 tokens.\\n5 steps: 26,000 input tokens\\n10 steps: 67,000\\n20 steps: 194,000\\n40 steps: 628,000\\n\\n8x the steps, 24x the tokens. Prompt caching cut it by 85 to 94% in my examples.\\n\\nArithmetic with assumed sizes. Save this. Full lesson on YouTube: The Code Notebook.",
     pinned="Lesson 10 next: security and governance 🔐 Follow so you don't miss it!")),

 upload=dict(
   title='Your AI Agent Will Crash: How to Stop It Refunding Twice (Retries, MCP, Caching)',
   hook="Lesson 9 of Cloud for AI Engineers. I crashed a working agent loop just before its email step. Restarted from scratch, it refunded the customer twice. Resumed from a checkpoint, once. This lesson covers agents, the cost of loops, MCP and the reliability tricks that stop expensive mistakes.",
   what="We cover what an agent is, tools and workflows versus agents, many-agent costs, why loop cost grows with the square of the steps, prompt caching with worked prices, semantic caching risks, MCP (including the July 2026 stateless version) and A2A, long-running durable tasks, a crash experiment with checkpoints and idempotency keys, sandboxes, retries with jitter (simulated), circuit breakers (simulated), fallbacks and gateways. The agent loop uses a scripted stand-in for the model. Retry and breaker results are simulations with assumed numbers. Token costs are arithmetic with assumed sizes.",
   bullets=['An agent is a model with tools in a loop', 'Workflow first, agent when needed', 'The 1-4-15 token rule for many agents', 'Loop cost: 8x the steps, 24x the tokens (arithmetic)', 'Prompt caching: 85% and 94% cheaper in worked examples', 'Semantic caching: when it is dangerous',
            'MCP in plain words, and the July 2026 stateless version', 'A2A: agent to agent', 'Long tasks: 202, queues and durable workflows', 'The crash experiment: restart 2 refunds, resume 1', 'Sandboxes: micro-VM, gVisor, container', 'Retry storm: 211 s without jitter, 9.9 s with it (simulation)',
            'Circuit breaker: 600 wasted calls down to 7 (simulation)', 'Fallbacks, gateways, streaming, structured output', 'ShopNest Copilot agent plan', 'Interview questions with answers'],
   hashtags='#aiagents #mcp #llm #reliability #aiengineering',
   tags='ai agents explained, idempotency key, agent crash recovery, retry with jitter, circuit breaker, mcp protocol, a2a protocol, prompt caching cost, agent loop cost, durable execution, cloud for ai engineers, the code notebook',
   pinned="The agent loop uses a scripted stand-in model, the retry and breaker results are simulations with assumed numbers, and the token costs are arithmetic with assumed sizes. 📊\\n\\nQuestion for you 👇\\nWhich surprised you more: a restart refunding twice, or jitter turning 211 s into 9.9 s?"),
)

import interview; L['notes'] = interview.add(L['notes'], L['num'])
