import sys; sys.path.insert(0, '/home/claude/caigen')
from frag import *
from gailab import CODE, OUT

LONG = [
 dict(id='s0', chap='The double refund', say=[
   "I built a small agent that refunds a customer and then emails them. I crashed it just before the email step, and restarted it from scratch. The customer was refunded twice. Resumed from a saved checkpoint, once.",
   "That is one of three failures in this lesson. The second is a retry storm, where a simple fix cut the finish time from two hundred and eleven seconds to ten. The third is a cost curve, where eight times the steps cost twenty-four times the tokens."],
  html=[H2('Restart = refunded twice', 0),
        DEF('crash, then <b>restart</b>: 2 refunds · <b>resume</b> or a key: 1 refund', 0, 0.5, style='margin-top:24px;font-size:48px'),
        MARK('plus a retry storm and a cost curve', 1, 0.6)]),

 dict(id='s1', chap='Where we are', say=[
   "Lesson eight built R A G, one of the two big patterns for A I applications. This lesson covers the other one, agents. That is, a model that decides what to do next, calls tools, and loops until a task is done.",
   "As always, I label my experiments. The agent loop uses a scripted stand in for the model, with no language model called. The retry and breaker results are simulations with assumed numbers. The token costs are arithmetic with assumed sizes."],
  html=[H2('Agents: the other big pattern', 0),
        GRID([('the agent loop', 0, 0.3), ('protocols: MCP, A2A', 0, 0.7), ('reliability', 0, 1.1)], cols=3, h=150, fs=38),
        STICKY('Honest label', 'scripted stand-in model · simulations · arithmetic with assumed sizes', 1, 0.5, style='margin-top:26px;font-size:36px')]),

 dict(id='s2', chap='What an agent is', say=[
   "What is an agent? A language model that uses tools in a loop, with memory and stop conditions. The classic recipe is called react. The model thinks, then acts by calling a tool, then observes the result, and repeats.",
   "A chat answers once. An agent keeps going. It might search, read a file, call an A P I, check the result, and try again, until it decides it is finished or something stops it."],
  html=[H2('An agent = a model + tools in a loop', 0),
        LIST([('the model thinks, then calls a tool', 0, 0.4), ('it observes the result, then repeats', 0, 1.0), ('memory + stop conditions', 1, 0.3), ('a chat answers once, an agent keeps going', 1, 0.9)], kind='ar', style='margin-top:26px;font-size:44px')]),

 dict(id='s3', chap='The loop', say=[
   "Here is the loop in a few lines. The model picks a tool, your code runs it, and the result goes back in. Then comes the check. Is the model done, or has a limit been hit?",
   "The model never runs anything itself. It writes a tool name and some J S O N arguments. Your code does the work, in a sandbox, with a timeout.",
   "And there are always two stop conditions. The model says it is finished, or the step budget runs out, in which case you fail loudly, not quietly."],
  html=[H2('The agent loop', 0), SVG('c3', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c3', 'agentloop', 1000, 290, 1)]),

 dict(id='s4', chap='Designing tools', say=[
   "Tools matter more than prompts. Describe each tool like documentation for a new colleague, with examples and edge cases. Return errors as ordinary results, so the model can read them and fix its next call.",
   "A trick from practice is to make mistakes impossible. One team found models kept getting relative file paths wrong, so they required absolute paths, and that whole class of error vanished."],
  html=[H2('Design tools for the model', 0),
        LIST([('document each tool: examples, edge cases', 0, 0.4), ('return errors as results: the model self-corrects', 0, 1.0), ('make mistakes impossible: absolute paths only', 1, 0.4)], kind='ar', style='margin-top:26px;font-size:46px')]),

 dict(id='s5', chap='Workflows or agents?', say=[
   "A useful distinction. A workflow follows a path you wrote in code. An agent decides its own path. Most useful systems should start as workflows, because they are cheaper, faster and easier to test.",
   "Common workflow patterns. Chain steps in a fixed order. Route a request to a specialist prompt. Run independent parts in parallel. Let an orchestrator split work among workers. Or loop a writer and a critic. Use a true agent only when you cannot predict the steps."],
  html=[H2('Workflow first, agent when needed', 0),
        TABLE(['Pattern', 'Use when'], [(['chain', 'fixed steps, trade speed for accuracy'], 0, 0.4), (['route', 'distinct categories of request'], 0, 0.9), (['parallel', 'independent parts, or vote'], 1, 0.3), (['orchestrator-workers', 'steps you cannot predict'], 1, 0.8), (['writer + critic', 'clear quality criteria'], 1, 1.3)], style='margin-top:22px;font-size:38px')]),

 dict(id='s6', chap='Many agents', say=[
   "What about many agents working together? A research system from Anthropic, with a lead agent and parallel helpers, beat a single agent by about ninety percent on its tests. But it used far more tokens.",
   "The rule of thumb is one, four, fifteen. A chat costs one unit of tokens. A single agent about four. A team of agents about fifteen. Pay that only for broad, parallel, high value work, not for most coding, where steps depend on each other."],
  html=[H2('1 · 4 · 15', 0),
        GRID([('<b>chat</b><br>1x tokens', 0, 0.3), ('<b>agent</b><br>about 4x', 0, 0.7), ('<b>many agents</b><br>about 15x', 0, 1.1)], cols=3, h=180, fs=40),
        SUB('reported by Anthropic (notebook) · pay 15x only for broad, parallel, valuable work', 1, 0.6, style='margin-top:20px')]),

 dict(id='s7', chap='Memory is a budget', say=[
   "Agents need memory, in two kinds. Short term is the thread so far, saved so a run can resume. Long term is what carries across sessions.",
   "Treat the context window as a budget. Every tool result you keep costs tokens on every later step. Summarise, drop what is no longer needed, and write long plans to storage instead of keeping them in the prompt."],
  html=[H2('Memory: a budget', 0),
        ROW(COL(CARD('<b>short term</b><br>this thread, checkpointed', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>long term</b><br>across sessions', 0, 0.9, style='font-size:38px'), width='48%'), style='margin-top:28px'),
        SUB('every kept token is paid for on every later step', 1, 0.6, style='margin-top:16px')]),

 dict(id='s8', chap='The cost of a loop', say=[
   "Now the cost curve. A language model has no memory between calls, so an agent re sends its whole history at every step. Step ten carries everything from steps one to nine.",
   "I worked it out with assumed sizes. A system prompt with tools of four thousand tokens. Each step adds a hundred tokens of model reply and five hundred of tool result. That is arithmetic, not a measurement."],
  html=[H2('Every step re-sends the history', 0),
        OUT(['system prompt + tools: 4,000 tokens (assumed)', 'each step adds 100 reply + 500 tool result', 'input at step n = 4,000 + 600 × (n − 1)'], 0, 0.4, size=32, label='assumed sizes', style='margin-top:22px'),
        SUB('arithmetic, not a measurement', 1, 0.6, style='margin-top:14px')]),

 dict(id='s9', chap='The cost curve', say=[
   "Five steps bill twenty-six thousand input tokens. Ten steps, sixty-seven thousand, two point six times as much. Twenty steps, a hundred and ninety-four thousand, seven and a half times.",
   "Forty steps, six hundred and twenty-eight thousand tokens. Eight times the steps, twenty-four times the cost. The cost grows with the square of the number of steps, so long loops get expensive fast."],
  html=[H2('Input tokens billed in total', 0), SVG('c9', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c9', 'cost_growth', 1000, 290, 1)]),

 dict(id='s10', chap='Caching to the rescue', say=[
   "The rescue is prompt caching. The provider keeps the work for an identical prompt start, and charges only about a tenth for reading it back. I used the notebook's example prices. Two dollars per million tokens to read normally, two fifty to write into the cache, ten cents to read from it.",
   "The twenty step agent costs about thirty-nine cents without caching and about six cents with it, eighty-five percent less. And the notebook's example, a hundred calls sharing a fifty thousand token prefix, falls from ten dollars to sixty-two cents, ninety-four percent."],
  html=[H2('Prompt caching: pay a tenth', 0), SVG('c10', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c10', 'cache_save', 1000, 290, 1)]),

 dict(id='s11', chap='Caching rules', say=[
   "Caching has rules. Put stable content first, and volatile content last. Never put a timestamp or a user name at the top, because one changed character ruins the match. The order of invalidation is tools, then system prompt, then messages, so changing a tool definition throws away everything.",
   "Prompts below a minimum length are silently not cached. And caches belong to one model, so if you fall back to a different model in an outage, you lose the cache."],
  html=[H2('Caching rules', 0),
        LIST([('stable first, volatile last', 0, 0.4), ('no timestamps or user names at the top', 0, 0.9), ('change a tool = lose the whole cache', 0, 1.4), ('too short = silently not cached · per-model cache', 1, 0.4)], kind='ar', style='margin-top:24px;font-size:42px')]),

 dict(id='s12', chap='Semantic caching: careful', say=[
   "A different idea is semantic caching. Embed the question, and if a very similar question was answered before, return the old answer without calling the model. It is cheap, but it is lossy.",
   "Cancel my order and cancel my subscription look similar, but need different answers. And answers built from one user's documents must never be served to another. Use it only for frequently asked, generic questions, with strict thresholds, short lifetimes and keys per customer."],
  html=[H2('Semantic caching: lossy', 0),
        ROW(COL(CARD('<b>risk 1</b><br>"cancel my order" ≈ "cancel my subscription"', 0, 0.4, style='font-size:34px'), width='48%'),
            COL(CARD('<b>risk 2</b><br>one user\'s answer served to another', 1, 0.3, style='font-size:34px'), width='48%'), style='margin-top:28px'),
        STICKY('Only for', 'generic FAQ · strict threshold · per-tenant keys', 1, 0.8, style='margin-top:22px;font-size:38px')]),

 dict(id='s13', chap='MCP', say=[
   "Now protocols. M C P, the Model Context Protocol, is a standard way for an agent to use tools. Your application is the host. It runs one client per server. Each server offers tools, resources and prompts, over J S O N R P C.",
   "Think of it like U S B for tools. Write a tool server once, and any compatible agent can use it. Two ways to connect, a local process, or a web connection that can be shared and secured with O Auth.",
   "One way to remember who controls what. Tools are controlled by the model. Resources by the app. Prompts by the person."],
  html=[H2('MCP: a standard plug for tools', 0), SVG('c13', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c13', 'mcp', 1000, 290, 1)]),

 dict(id='s14', chap='MCP goes stateless', say=[
   "A big change landed in July twenty twenty-six. The new M C P version is stateless. There is no opening handshake and no session I D. Every request carries its own version, identity and capabilities.",
   "That means any copy of a server behind a load balancer can answer any request. You can run an M C P server as a plain function in Lambda or Cloud Run. New headers also let gateways route and limit per tool without opening the message body."],
  html=[H2('MCP, July 2026: stateless', 0),
        LIST([('no handshake, no session ID', 0, 0.4), ('each request carries version + identity', 0, 0.9), ('any instance behind a load balancer', 1, 0.3), ('headers let gateways route per tool', 1, 0.8)], kind='ar', style='margin-top:26px;font-size:44px'),
        SUB('spec date 2026-07-28 (notebook)', 1, 1.4, style='margin-top:14px')]),

 dict(id='s15', chap='A2A', say=[
   "A second protocol, A two A, is for agent to agent. When one agent wants to hand a task to another team's agent, it finds it through a public card listing its skills, and delegates. It reached version one point zero in March twenty twenty-six.",
   "Short version. M C P is an agent calling tools. A two A is an agent delegating to another agent. Most teams need M C P now, and A two A when agents cross team boundaries."],
  html=[H2('A2A: agent to agent', 0),
        TABLE(['Protocol', 'What it connects'], [(['MCP', 'an agent calls a server\'s tools'], 0, 0.4), (['A2A', 'an agent delegates to another agent'], 0, 0.9)], style='margin-top:26px;font-size:44px'),
        SUB('A2A v1.0: March 2026 · found through an "Agent Card" · notebook', 1, 0.6, style='margin-top:16px')]),

 dict(id='s16', chap='Long tasks', say=[
   "A chat turn fits one web request. An agent task, lasting minutes or hours, with approvals and crashes, does not. So make it asynchronous and durable.",
   "The A P I returns a task I D at once. The task goes on a queue. A durable workflow engine runs the loop, and every model or tool call is a retried step. Progress streams back, code runs in a sandbox, and state is checkpointed to a database."],
  html=[H2('Long tasks: async and durable', 0),
        LIST([('API returns a task ID at once (HTTP 202)', 0, 0.4), ('queue → durable workflow runs the loop', 0, 0.9), ('each call is a retried step, checkpointed', 1, 0.3), ('progress by streaming or webhook', 1, 0.8)], kind='ar', style='margin-top:24px;font-size:44px')]),

 dict(id='s17', chap='My crash experiment', say=[
   "Let me prove why checkpoints matter. I built a working agent loop. A step budget, tool errors returned to the model, an approval gate, and a checkpoint saved after every step. The model is a scripted stand in, so nothing is generated.",
   "The task. Look up an order, read the policy, check eligibility, draft a reply, get approval, issue a refund, send an email, update the ticket. Nine tool steps. I kill the process just before the email step, then recover two ways."],
  html=[H2('A crash, on purpose', 0),
        OUT(['look up → policy → eligibility → draft → approval', '→ ISSUE REFUND → send email → update ticket', 'process dies just before the email (step 8 of 9)'], 0, 0.4, size=30, label='the task', style='margin-top:22px'),
        SUB('a scripted stand-in model: the loop and the side effects are real', 1, 0.6, style='margin-top:14px')]),

 dict(id='s18', chap='The crash, measured', say=[
   "Restart from step one, with no protection. Fourteen tool calls in total, and the customer was refunded twice. With an idempotency key on the refund, still fourteen calls, but one refund.",
   "Resume from the checkpoint. Only eight tool calls in total, and one refund. Resume, do not restart."],
  html=[H2('After the crash', 0), SVG('c18', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c18', 'replay', 1000, 290, 1)]),

 dict(id='s19', chap='Four rules for long runs', say=[
   "So four rules. Checkpoint after every step, so a crash at step thirty-seven resumes at thirty-seven. Put an idempotency key on every tool with a side effect, so a replay cannot charge or email twice.",
   "Treat human approvals as a durable pause, not a blocked process, because approvals can take hours. And when you deploy a new version, let running tasks finish on the version they started with."],
  html=[H2('Four rules for long runs', 0),
        LIST([('checkpoint after every step', 0, 0.4), ('idempotency key on side-effect tools', 0, 0.9), ('approvals = durable pause, not a blocked process', 1, 0.3), ('running tasks finish on their starting version', 1, 0.8)], kind='ok', style='margin-top:26px;font-size:44px')]),

 dict(id='s20', chap='Sandboxes', say=[
   "Agents run code, so run it somewhere safe. Three levels. A micro virtual machine gives each task its own kernel, and is the strongest. G Visor intercepts system calls, a middle option, often used with GPUs. A plain container shares the host's kernel, so only for code you trust.",
   "For untrusted code, use a micro V M. Add limits on time and memory, control outbound network traffic, and never put secrets inside the sandbox."],
  html=[H2('Where agent code runs', 0),
        TABLE(['Sandbox', 'Strength'], [(['micro-VM (Firecracker)', 'strongest: its own kernel'], 0, 0.4), (['gVisor', 'middle: intercepts system calls'], 0, 0.9), (['container', 'weakest: shares the host kernel'], 1, 0.3)], style='margin-top:24px;font-size:42px'),
        STICKY('Rule', 'untrusted code → micro-VM · time limits · no secrets inside', 1, 0.8, style='margin-top:22px;font-size:36px')]),

 dict(id='s21', chap='The reliability stack', say=[
   "Failures also come from the outside. Rate limits, busy servers, outages. Reliability is built in layers. The S D K retries with jitter. A gateway adds circuit breakers, fallbacks and quotas. The workflow engine retries durably. And the app streams results and uses idempotency keys.",
   "Next I will measure two of those layers. First, why jitter matters. Then what a circuit breaker saves."],
  html=[H2('Reliability in layers', 0),
        TABLE(['Layer', 'Does'], [(['SDK', 'jittered retries'], 0, 0.4), (['gateway', 'circuit breaker, fallback, quotas'], 0, 0.9), (['workflow engine', 'durable retries'], 0, 1.4), (['app', 'streaming + idempotency keys'], 1, 0.3)], style='margin-top:22px;font-size:42px')]),

 dict(id='s22', chap='The retry storm', say=[
   "When a server says too many requests, with a four twenty-nine, clients retry. How they wait matters enormously. I simulated two hundred clients all calling at second zero, to a server that accepts fifty requests per second. That capacity is my assumption.",
   "Three rules. Retry at once, every tenth of a second. Exponential backoff with no randomness. And exponential backoff with full jitter, a random wait between zero and the cap. Each client gives up after twelve tries."],
  html=[H2('200 clients, 50 requests per second', 0),
        LIST([('retry at once, every 0.1 s', 0, 0.4), ('exponential backoff, no randomness', 0, 0.9), ('exponential backoff, full jitter', 1, 0.3), ('give up after 12 tries', 1, 0.8)], kind='ar', numbered=True, style='margin-top:24px;font-size:44px'),
        SUB('simulation · capacity assumed', 1, 1.4, style='margin-top:14px')]),

 dict(id='s23', chap='Retry storm, measured', say=[
   "Retrying at once made two thousand and ten rejected attempts, and a hundred and forty clients gave up completely. Backoff without jitter made the same two thousand and ten rejections, and the last client finished at two hundred and eleven seconds.",
   "Full jitter made only four hundred and forty-four rejected attempts, finished in nine point nine seconds, and nobody gave up."],
  html=[H2('Rejected attempts', 0), SVG('c23', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c23', 'jitter_att', 1000, 270, 1)]),

 dict(id='s24', chap='Why jitter works', say=[
   "Here is the other view. Without jitter, all the failed clients wait the same time and come back together, in waves. Each wave hits the same wall.",
   "With full jitter the retries spread out, so the server serves them as it has room. Same server, same clients. The only change was a random number."],
  html=[H2('Same clients, same server', 0), SVG('c24', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c24', 'jitter_time', 1000, 290, 1)]),

 dict(id='s25', chap='Retry rules', say=[
   "The practical rules. Wait a random time between zero and the smaller of a cap and base times two to the attempt number. If the server sends a retry after header, obey it first.",
   "Retry only what can succeed later. Four twenty-nine, five hundred, five oh three and five twenty-nine. Never blindly retry a four hundred, because the request itself is wrong."],
  html=[H2('Retry rules', 0),
        DEF('wait = random(0, min(cap, base × 2<sup>attempt</sup>))', 0, 0.4, style='margin-top:24px;font-size:48px'),
        LIST([('server says Retry-After? obey it first', 0, 1.0), ('retry 429, 500, 503, 529', 1, 0.3), ('never blindly retry a 400', 1, 0.8)], kind='ar', style='margin-top:20px;font-size:42px')]),

 dict(id='s26', chap='Circuit breakers', say=[
   "A circuit breaker protects you when a backend is down. It has three states. Closed is normal, and it counts failures. After enough failures it opens, and requests fail fast, or go to a fallback, without touching the broken service.",
   "After a cooldown it goes half open, and lets a trial request through. If that works, it closes. If not, it opens again. Like a fuse in your house, but one that resets itself."],
  html=[H2('A circuit breaker', 0), SVG('c26', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c26', 'states', 1000, 290, 1)]),

 dict(id='s27', chap='The breaker, measured', say=[
   "I simulated a backend that is down for thirty seconds, with twenty requests per second arriving for a minute. Without a breaker, six hundred calls hit the dead backend, each waiting and failing.",
   "With a breaker that opens after five failures and waits ten seconds before a trial, seven calls hit it. Same outage, a fraction of the wasted work, and quick fallbacks for users."],
  html=[H2('Calls that hit a dead backend', 0), SVG('c27', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c27', 'breaker', 1000, 270, 1)]),

 dict(id='s28', chap='Fallbacks and gateways', say=[
   "What should the fallback be? First, the same model in another region. Only then a different model. A different model changes behaviour, because prompts are tuned per model, and it loses the prompt cache.",
   "An A I gateway sits between your apps and the model providers. It offers one interface, key storage, quotas per team, routing, fallbacks and metrics. Open source options exist, and the simple rule is to extend what you already run."],
  html=[H2('Fallbacks and gateways', 0),
        LIST([('1st: same model, another region', 0, 0.4), ('2nd: another model (behaviour + cache change)', 0, 1.0), ('a gateway: one API, keys, quotas, routing, metrics', 1, 0.4), ('extend what you already run', 1, 1.0)], kind='ar', numbered=True, style='margin-top:24px;font-size:42px')]),

 dict(id='s29', chap='Streaming and structured output', say=[
   "Two small features that improve reliability. Streaming shows the first words quickly, and avoids idle timeouts on long answers. And structured outputs make the model follow a schema exactly.",
   "A caution. Valid does not mean correct. A response can be perfect J S O N and still wrong. Check the content, not just the shape."],
  html=[H2('Streaming and structured output', 0),
        ROW(COL(CARD('<b>streaming</b><br>first words fast<br>no idle timeouts', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>structured output</b><br>exactly the schema<br>valid ≠ correct', 1, 0.3, style='font-size:38px'), width='48%'), style='margin-top:28px')]),

 dict(id='s30', chap='One stack, three clouds', say=[
   "Put it together. The same layers appear on every cloud. An edge firewall and A P I in front, then your app or agent runtime, then an A I gateway with guardrails, then the models. Beside them sit retrieval, state, queues with a durable workflow, sandboxed tool servers, identity and tracing.",
   "The names differ. A W S has Bedrock and AgentCore, Google has Gemini and its Agent Engine, Azure has Foundry. This is my synthesis, not a vendor table. The shape is what to remember."],
  html=[H2('The same stack everywhere', 0),
        TABLE(['Layer', 'What lives there'], [(['edge + API', 'firewall, API gateway'], 0, 0.4), (['agent runtime', 'your loop, with a durable workflow'], 0, 0.9), (['AI gateway', 'quotas, fallback, guardrails'], 1, 0.3), (['beside them', 'retrieval, state, queues, sandboxes, tracing'], 1, 0.8)], style='margin-top:22px;font-size:40px'),
        SUB('my synthesis, not a vendor table', 1, 1.4, style='margin-top:12px')]),

 dict(id='s31', chap='ShopNest Copilot', say=[
   "For ShopNest Copilot. Start as a workflow, not an agent. A fixed route from ticket to intent to retrieval to answer. Add a refund tool only behind a human approval, with an idempotency key and a checkpoint.",
   "Tools are served over M C P, stable prompt content goes first for caching, and calls go through a gateway with jittered retries and a breaker. We add loops and more agents only if the evaluations from lesson seven show they pay."],
  html=[H2('ShopNest Copilot: agent plan', 0),
        TABLE(['Piece', 'Plan'], [(['shape', 'a workflow first; an agent only if evals say so'], 0, 0.4), (['refund tool', 'human approval + idempotency key + checkpoint'], 0, 0.9), (['tools', 'served over MCP'], 1, 0.3), (['calls', 'stable prefix first, gateway, jitter, breaker'], 1, 0.8)], style='margin-top:22px;font-size:38px')]),

 dict(id='s32', chap='Four words to keep', say=[
   "Four words to carry forward. Idempotency key: a label that makes a repeated action happen only once. Checkpoint: saved progress to resume from.",
   "Jitter: a random delay in retries. And circuit breaker: a switch that stops calls to a broken service."],
  html=[H2('Four words to keep', 0),
        GRID([('<b>idempotency key</b>', 0, 0.3), ('<b>checkpoint</b>', 0, 0.9), ('<b>jitter</b>', 1, 0.3), ('<b>circuit breaker</b>', 1, 0.9)], cols=2, h=140, fs=42, style='margin-top:30px')]),

 dict(id='s33', chap='Interview corner', say=[
   "Interview corner. Asked how you make a long running agent safe to retry, say: checkpoint after every step, resume rather than restart, and put idempotency keys on tools with side effects. In my test, a restart refunded twice and a resume once.",
   "Asked why add jitter to retries, say: without it, clients retry in waves. With two hundred clients, full jitter finished in ten seconds against two hundred and eleven, with a third of the wasted attempts."],
  html=[H2('Interview corner', 0),
        Q('How do you make an agent safe to retry?', 'Checkpoint each step, resume (not restart), idempotency keys on side effects. A restart refunded twice.', 0, 0.4),
        Q('Why add jitter to retries?', 'Clients retry in waves otherwise. 200 clients: 9.9 s vs 211 s.', 1, 0.4)]),

 dict(id='s34', chap='Your turn', say=[
   "Your turn. The zip for this lesson has three scripts. The crash experiment, the retry and breaker simulator, and the agent cost calculator. Remove the idempotency key and watch the refund happen twice.",
   "Then change the capacity or the number of clients in the retry test. One changed number teaches more than an hour of reading."],
  html=[H2('Your turn', 0),
        CARD('<b>l09_agent_loop.py</b>: crash, restart, resume, keys.<br><b>l09_retry_breaker.py</b>: jitter and the breaker.<br><b>l09_agent_cost.py</b>: loop cost and caching.', 0, 0.4, style='margin-top:22px;font-size:38px'),
        SUB('one changed number teaches more than an hour of reading', 1, 0.8, style='margin-top:16px')]),

 dict(id='s35', chap='Recap', say=[
   "Recap. An agent is a model with tools in a loop, so start with a workflow. The loop re sends its history, so eight times the steps cost twenty-four times the tokens, and caching cuts it by about eighty-five to ninety-four percent.",
   "Checkpoint, resume and use idempotency keys, or a crash refunds twice. Jitter turned two hundred and eleven seconds into ten, and a breaker cut six hundred wasted calls to seven. Next lesson: security and governance."],
  html=[H2('Recap', 0),
        GRID([('workflow first, agent if needed', 0, 0.3), ('8x steps = 24x tokens', 0, 0.9), ('caching: 85 to 94% cheaper', 0, 1.5),
              ('checkpoint + keys: 1 refund', 1, 0.3), ('jitter: 211 s → 9.9 s', 1, 0.9), ('breaker: 600 → 7 calls', 1, 1.5)], cols=3, h=150, fs=30)]),
]
