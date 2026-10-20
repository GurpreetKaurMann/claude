# CAI-09 Upload Copy

## 1. Lesson video (YouTube)

**Title:** Your AI Agent Will Crash: How to Stop It Refunding Twice (Retries, MCP, Caching)

**Description:**
```
Lesson 9 of Cloud for AI Engineers. I crashed a working agent loop just before its email step. Restarted from scratch, it refunded the customer twice. Resumed from a checkpoint, once. This lesson covers agents, the cost of loops, MCP and the reliability tricks that stop expensive mistakes.
We cover what an agent is, tools and workflows versus agents, many-agent costs, why loop cost grows with the square of the steps, prompt caching with worked prices, semantic caching risks, MCP (including the July 2026 stateless version) and A2A, long-running durable tasks, a crash experiment with checkpoints and idempotency keys, sandboxes, retries with jitter (simulated), circuit breakers (simulated), fallbacks and gateways. The agent loop uses a scripted stand-in for the model. Retry and breaker results are simulations with assumed numbers. Token costs are arithmetic with assumed sizes.
⏮️ Previous lesson: <CAI-08 link>

In this lesson:
✅ An agent is a model with tools in a loop
✅ Workflow first, agent when needed
✅ The 1-4-15 token rule for many agents
✅ Loop cost: 8x the steps, 24x the tokens (arithmetic)
✅ Prompt caching: 85% and 94% cheaper in worked examples
✅ Semantic caching: when it is dangerous
✅ MCP in plain words, and the July 2026 stateless version
✅ A2A: agent to agent
✅ Long tasks: 202, queues and durable workflows
✅ The crash experiment: restart 2 refunds, resume 1
✅ Sandboxes: micro-VM, gVisor, container
✅ Retry storm: 211 s without jitter, 9.9 s with it (simulation)
✅ Circuit breaker: 600 wasted calls down to 7 (simulation)
✅ Fallbacks, gateways, streaming, structured output
✅ ShopNest Copilot agent plan
✅ Interview questions with answers

⏱️ Chapters
0:00 The double refund
0:31 Intro
0:41 Where we are
1:12 What an agent is
1:39 The loop
2:09 Designing tools
2:35 Workflows or agents?
3:07 Many agents
3:37 Memory is a budget
4:01 The cost of a loop
4:27 The cost curve
4:53 Caching to the rescue
5:29 Caching rules
5:59 Semantic caching: careful
6:30 MCP
7:08 MCP goes stateless
7:39 A2A
8:09 Long tasks
8:36 My crash experiment
9:08 The crash, measured
9:28 Four rules for long runs
9:54 Sandboxes
10:25 The reliability stack
10:52 The retry storm
11:24 Retry storm, measured
11:48 Why jitter works
12:07 Retry rules
12:31 Circuit breakers
12:58 The breaker, measured
13:22 Fallbacks and gateways
13:50 Streaming and structured output
14:13 One stack, three clouds
14:46 ShopNest Copilot
15:16 Four words to keep
15:33 Interview corner
16:03 Your turn
16:25 Recap
16:55 Next lesson

Next lesson → CAI-10: Security and governance: identity, prompt injection, least privilege

🌐 Website: https://thecodenotebook.com/
📸 Instagram: https://www.instagram.com/thecodenotebookyt/

#aiagents #mcp #llm #reliability #aiengineering
```

**Tags:**
```
ai agents explained, idempotency key, agent crash recovery, retry with jitter, circuit breaker, mcp protocol, a2a protocol, prompt caching cost, agent loop cost, durable execution, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
The agent loop uses a scripted stand-in model, the retry and breaker results are simulations with assumed numbers, and the token costs are arithmetic with assumed sizes. 📊\n\nQuestion for you 👇\nWhich surprised you more: a restart refunding twice, or jitter turning 211 s into 9.9 s?
```

**Thumbnail:** CAI-09_Thumbnail.png

---

## 2. Short 1 (YouTube Shorts)

**Title:** My AI Agent Crashed and Refunded the Customer Twice #shorts

**Description:**
```
A working agent loop (the model is a scripted stand-in), 9 tool steps, process killed just before the email step:\n• restart from step 1, no keys: 14 tool calls, 2 refunds\n• restart + idempotency key: 1 refund\n• resume from checkpoint: 8 tool calls, 1 refund\n\nFull lesson: Cloud for AI Engineers, lesson 9.
```

**Tags:**
```
shorts, ai agents, idempotency key, agent reliability, checkpointing, durable execution, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Do your agents have idempotency keys? 👇
```

**Cover:** CAI-09_Short1_Cover.png

---

## 3. Short 2 (YouTube Shorts)

**Title:** One Random Number Cut a Retry Storm From 211 s to 9.9 s #shorts

**Description:**
```
Simulation: 200 clients call at second 0, the server accepts 50 requests per second (assumed), up to 12 retries:\n• no jitter: 2,010 rejected attempts, last client at 211 s, 140 clients gave up\n• full jitter: 444 rejected attempts, last client at 9.9 s, none gave up\n\nwait = random(0, min(cap, base x 2^attempt))\n\nFull lesson: Cloud for AI Engineers, lesson 9.
```

**Tags:**
```
shorts, retry with jitter, exponential backoff, thundering herd, api rate limits, llm api reliability, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Do you add jitter to your retries? 👇
```

**Cover:** CAI-09_Short2_Cover.png

---

## 4. Instagram Reel 1

**Caption:**
```
Agent loops re-send the whole history every step. 🔁\n\nAssumed sizes: 4,000-token prompt, each step adds 600 tokens.\n5 steps: 26,000 input tokens\n10 steps: 67,000\n20 steps: 194,000\n40 steps: 628,000\n\n8x the steps, 24x the tokens. Prompt caching cut it by 85 to 94% in my examples.\n\nArithmetic with assumed sizes. Save this. Full lesson on YouTube: The Code Notebook.
```

**First comment (pin it):**
```
Lesson 10 next: security and governance 🔐 Follow so you don't miss it!
```

**Cover:** CAI-09_Reel1_Cover_Instagram.png

---
