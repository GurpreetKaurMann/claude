# CAI-09 · Agents and Reliability: Scripts

**Lesson 9 of 12 · Module 4 · Shipping it**

Voice: AI narrator (Kokoro `af_heart`). Final lesson video length: 17:20.

## Long video narration

**[The double refund]**

> I built a small agent that refunds a customer and then emails them. I crashed it just before the email step, and restarted it from scratch. The customer was refunded twice. Resumed from a saved checkpoint, once.

> That is one of three failures in this lesson. The second is a retry storm, where a simple fix cut the finish time from two hundred and eleven seconds to ten. The third is a cost curve, where eight times the steps cost twenty-four times the tokens.

**[Intro]**

> Welcome to lesson nine of the cloud for A I engineers course, on The Code Notebook.

> The handwritten notes and the code for this lesson are linked in the description.

**[Where we are]**

> Lesson eight built R A G, one of the two big patterns for A I applications. This lesson covers the other one, agents. That is, a model that decides what to do next, calls tools, and loops until a task is done.

> As always, I label my experiments. The agent loop uses a scripted stand in for the model, with no language model called. The retry and breaker results are simulations with assumed numbers. The token costs are arithmetic with assumed sizes.

**[What an agent is]**

> What is an agent? A language model that uses tools in a loop, with memory and stop conditions. The classic recipe is called react. The model thinks, then acts by calling a tool, then observes the result, and repeats.

> A chat answers once. An agent keeps going. It might search, read a file, call an A P I, check the result, and try again, until it decides it is finished or something stops it.

**[The loop]**

> Here is the loop in a few lines. The model picks a tool, your code runs it, and the result goes back in. Then comes the check. Is the model done, or has a limit been hit?

> The model never runs anything itself. It writes a tool name and some J S O N arguments. Your code does the work, in a sandbox, with a timeout.

> And there are always two stop conditions. The model says it is finished, or the step budget runs out, in which case you fail loudly, not quietly.

**[Designing tools]**

> Tools matter more than prompts. Describe each tool like documentation for a new colleague, with examples and edge cases. Return errors as ordinary results, so the model can read them and fix its next call.

> A trick from practice is to make mistakes impossible. One team found models kept getting relative file paths wrong, so they required absolute paths, and that whole class of error vanished.

**[Workflows or agents?]**

> A useful distinction. A workflow follows a path you wrote in code. An agent decides its own path. Most useful systems should start as workflows, because they are cheaper, faster and easier to test.

> Common workflow patterns. Chain steps in a fixed order. Route a request to a specialist prompt. Run independent parts in parallel. Let an orchestrator split work among workers. Or loop a writer and a critic. Use a true agent only when you cannot predict the steps.

**[Many agents]**

> What about many agents working together? A research system from Anthropic, with a lead agent and parallel helpers, beat a single agent by about ninety percent on its tests. But it used far more tokens.

> The rule of thumb is one, four, fifteen. A chat costs one unit of tokens. A single agent about four. A team of agents about fifteen. Pay that only for broad, parallel, high value work, not for most coding, where steps depend on each other.

**[Memory is a budget]**

> Agents need memory, in two kinds. Short term is the thread so far, saved so a run can resume. Long term is what carries across sessions.

> Treat the context window as a budget. Every tool result you keep costs tokens on every later step. Summarise, drop what is no longer needed, and write long plans to storage instead of keeping them in the prompt.

**[The cost of a loop]**

> Now the cost curve. A language model has no memory between calls, so an agent re sends its whole history at every step. Step ten carries everything from steps one to nine.

> I worked it out with assumed sizes. A system prompt with tools of four thousand tokens. Each step adds a hundred tokens of model reply and five hundred of tool result. That is arithmetic, not a measurement.

**[The cost curve]**

> Five steps bill twenty-six thousand input tokens. Ten steps, sixty-seven thousand, two point six times as much. Twenty steps, a hundred and ninety-four thousand, seven and a half times.

> Forty steps, six hundred and twenty-eight thousand tokens. Eight times the steps, twenty-four times the cost. The cost grows with the square of the number of steps, so long loops get expensive fast.

**[Caching to the rescue]**

> The rescue is prompt caching. The provider keeps the work for an identical prompt start, and charges only about a tenth for reading it back. I used the notebook's example prices. Two dollars per million tokens to read normally, two fifty to write into the cache, ten cents to read from it.

> The twenty step agent costs about thirty-nine cents without caching and about six cents with it, eighty-five percent less. And the notebook's example, a hundred calls sharing a fifty thousand token prefix, falls from ten dollars to sixty-two cents, ninety-four percent.

**[Caching rules]**

> Caching has rules. Put stable content first, and volatile content last. Never put a timestamp or a user name at the top, because one changed character ruins the match. The order of invalidation is tools, then system prompt, then messages, so changing a tool definition throws away everything.

> Prompts below a minimum length are silently not cached. And caches belong to one model, so if you fall back to a different model in an outage, you lose the cache.

**[Semantic caching: careful]**

> A different idea is semantic caching. Embed the question, and if a very similar question was answered before, return the old answer without calling the model. It is cheap, but it is lossy.

> Cancel my order and cancel my subscription look similar, but need different answers. And answers built from one user's documents must never be served to another. Use it only for frequently asked, generic questions, with strict thresholds, short lifetimes and keys per customer.

**[MCP]**

> Now protocols. M C P, the Model Context Protocol, is a standard way for an agent to use tools. Your application is the host. It runs one client per server. Each server offers tools, resources and prompts, over J S O N R P C.

> Think of it like U S B for tools. Write a tool server once, and any compatible agent can use it. Two ways to connect, a local process, or a web connection that can be shared and secured with O Auth.

> One way to remember who controls what. Tools are controlled by the model. Resources by the app. Prompts by the person.

**[MCP goes stateless]**

> A big change landed in July twenty twenty-six. The new M C P version is stateless. There is no opening handshake and no session I D. Every request carries its own version, identity and capabilities.

> That means any copy of a server behind a load balancer can answer any request. You can run an M C P server as a plain function in Lambda or Cloud Run. New headers also let gateways route and limit per tool without opening the message body.

**[A2A]**

> A second protocol, A two A, is for agent to agent. When one agent wants to hand a task to another team's agent, it finds it through a public card listing its skills, and delegates. It reached version one point zero in March twenty twenty-six.

> Short version. M C P is an agent calling tools. A two A is an agent delegating to another agent. Most teams need M C P now, and A two A when agents cross team boundaries.

**[Long tasks]**

> A chat turn fits one web request. An agent task, lasting minutes or hours, with approvals and crashes, does not. So make it asynchronous and durable.

> The A P I returns a task I D at once. The task goes on a queue. A durable workflow engine runs the loop, and every model or tool call is a retried step. Progress streams back, code runs in a sandbox, and state is checkpointed to a database.

**[My crash experiment]**

> Let me prove why checkpoints matter. I built a working agent loop. A step budget, tool errors returned to the model, an approval gate, and a checkpoint saved after every step. The model is a scripted stand in, so nothing is generated.

> The task. Look up an order, read the policy, check eligibility, draft a reply, get approval, issue a refund, send an email, update the ticket. Nine tool steps. I kill the process just before the email step, then recover two ways.

**[The crash, measured]**

> Restart from step one, with no protection. Fourteen tool calls in total, and the customer was refunded twice. With an idempotency key on the refund, still fourteen calls, but one refund.

> Resume from the checkpoint. Only eight tool calls in total, and one refund. Resume, do not restart.

**[Four rules for long runs]**

> So four rules. Checkpoint after every step, so a crash at step thirty-seven resumes at thirty-seven. Put an idempotency key on every tool with a side effect, so a replay cannot charge or email twice.

> Treat human approvals as a durable pause, not a blocked process, because approvals can take hours. And when you deploy a new version, let running tasks finish on the version they started with.

**[Sandboxes]**

> Agents run code, so run it somewhere safe. Three levels. A micro virtual machine gives each task its own kernel, and is the strongest. G Visor intercepts system calls, a middle option, often used with GPUs. A plain container shares the host's kernel, so only for code you trust.

> For untrusted code, use a micro V M. Add limits on time and memory, control outbound network traffic, and never put secrets inside the sandbox.

**[The reliability stack]**

> Failures also come from the outside. Rate limits, busy servers, outages. Reliability is built in layers. The S D K retries with jitter. A gateway adds circuit breakers, fallbacks and quotas. The workflow engine retries durably. And the app streams results and uses idempotency keys.

> Next I will measure two of those layers. First, why jitter matters. Then what a circuit breaker saves.

**[The retry storm]**

> When a server says too many requests, with a four twenty-nine, clients retry. How they wait matters enormously. I simulated two hundred clients all calling at second zero, to a server that accepts fifty requests per second. That capacity is my assumption.

> Three rules. Retry at once, every tenth of a second. Exponential backoff with no randomness. And exponential backoff with full jitter, a random wait between zero and the cap. Each client gives up after twelve tries.

**[Retry storm, measured]**

> Retrying at once made two thousand and ten rejected attempts, and a hundred and forty clients gave up completely. Backoff without jitter made the same two thousand and ten rejections, and the last client finished at two hundred and eleven seconds.

> Full jitter made only four hundred and forty-four rejected attempts, finished in nine point nine seconds, and nobody gave up.

**[Why jitter works]**

> Here is the other view. Without jitter, all the failed clients wait the same time and come back together, in waves. Each wave hits the same wall.

> With full jitter the retries spread out, so the server serves them as it has room. Same server, same clients. The only change was a random number.

**[Retry rules]**

> The practical rules. Wait a random time between zero and the smaller of a cap and base times two to the attempt number. If the server sends a retry after header, obey it first.

> Retry only what can succeed later. Four twenty-nine, five hundred, five oh three and five twenty-nine. Never blindly retry a four hundred, because the request itself is wrong.

**[Circuit breakers]**

> A circuit breaker protects you when a backend is down. It has three states. Closed is normal, and it counts failures. After enough failures it opens, and requests fail fast, or go to a fallback, without touching the broken service.

> After a cooldown it goes half open, and lets a trial request through. If that works, it closes. If not, it opens again. Like a fuse in your house, but one that resets itself.

**[The breaker, measured]**

> I simulated a backend that is down for thirty seconds, with twenty requests per second arriving for a minute. Without a breaker, six hundred calls hit the dead backend, each waiting and failing.

> With a breaker that opens after five failures and waits ten seconds before a trial, seven calls hit it. Same outage, a fraction of the wasted work, and quick fallbacks for users.

**[Fallbacks and gateways]**

> What should the fallback be? First, the same model in another region. Only then a different model. A different model changes behaviour, because prompts are tuned per model, and it loses the prompt cache.

> An A I gateway sits between your apps and the model providers. It offers one interface, key storage, quotas per team, routing, fallbacks and metrics. Open source options exist, and the simple rule is to extend what you already run.

**[Streaming and structured output]**

> Two small features that improve reliability. Streaming shows the first words quickly, and avoids idle timeouts on long answers. And structured outputs make the model follow a schema exactly.

> A caution. Valid does not mean correct. A response can be perfect J S O N and still wrong. Check the content, not just the shape.

**[One stack, three clouds]**

> Put it together. The same layers appear on every cloud. An edge firewall and A P I in front, then your app or agent runtime, then an A I gateway with guardrails, then the models. Beside them sit retrieval, state, queues with a durable workflow, sandboxed tool servers, identity and tracing.

> The names differ. A W S has Bedrock and AgentCore, Google has Gemini and its Agent Engine, Azure has Foundry. This is my synthesis, not a vendor table. The shape is what to remember.

**[ShopNest Copilot]**

> For ShopNest Copilot. Start as a workflow, not an agent. A fixed route from ticket to intent to retrieval to answer. Add a refund tool only behind a human approval, with an idempotency key and a checkpoint.

> Tools are served over M C P, stable prompt content goes first for caching, and calls go through a gateway with jittered retries and a breaker. We add loops and more agents only if the evaluations from lesson seven show they pay.

**[Four words to keep]**

> Four words to carry forward. Idempotency key: a label that makes a repeated action happen only once. Checkpoint: saved progress to resume from.

> Jitter: a random delay in retries. And circuit breaker: a switch that stops calls to a broken service.

**[Interview corner]**

> Interview corner. Asked how you make a long running agent safe to retry, say: checkpoint after every step, resume rather than restart, and put idempotency keys on tools with side effects. In my test, a restart refunded twice and a resume once.

> Asked why add jitter to retries, say: without it, clients retry in waves. With two hundred clients, full jitter finished in ten seconds against two hundred and eleven, with a third of the wasted attempts.

**[Your turn]**

> Your turn. The zip for this lesson has three scripts. The crash experiment, the retry and breaker simulator, and the agent cost calculator. Remove the idempotency key and watch the refund happen twice.

> Then change the capacity or the number of clients in the retry test. One changed number teaches more than an hour of reading.

**[Recap]**

> Recap. An agent is a model with tools in a loop, so start with a workflow. The loop re sends its history, so eight times the steps cost twenty-four times the tokens, and caching cuts it by about eighty-five to ninety-four percent.

> Checkpoint, resume and use idempotency keys, or a crash refunds twice. Jitter turned two hundred and eleven seconds into ten, and a breaker cut six hundred wasted calls to seven. Next lesson: security and governance.

**[Next lesson]**

> In the next lesson: security and governance. Identity, prompt injection and least privilege.

> Subscribe so you don't miss it. See you in the notebook.


## Short 1: My AI Agent Crashed and Refunded the Customer Twice #shorts

> I crashed an A I agent halfway through a refund. Restarting it refunded the customer twice.

> I built a working agent loop with a scripted stand in for the model. Nine tool steps, and I killed it just before the email step. Restarted from scratch, it issued the refund again. Two refunds.

> Resumed from its checkpoint, one refund, and only eight tool calls in total. An idempotency key on the refund also gives one. Checkpoint every step.

> Checkpoint every step. Key every side effect.


## Short 2: One Random Number Cut a Retry Storm From 211 s to 9.9 s #shorts

> One random number turned a two hundred and eleven second retry storm into nine point nine seconds.

> I simulated two hundred clients hitting a server that accepts fifty requests a second. With backoff but no jitter, the last client finished at two hundred and eleven seconds. With full jitter, nine point nine.

> Jitter means waiting a random time between zero and the cap, so retries spread out instead of arriving in waves. The capacity and client count are my assumptions.

> Always add jitter to your retries.


## Instagram Reel 1: Why long agent loops cost so much

> Why long agent loops cost so much.

> An agent re sends its whole history on every step. With assumed sizes, five steps bill twenty-six thousand input tokens. Forty steps, six hundred and twenty-eight thousand. Eight times the steps, twenty-four times the tokens. Caching the stable start of the prompt cuts that by about eighty-five percent.

> Cache the prefix. Save this.
