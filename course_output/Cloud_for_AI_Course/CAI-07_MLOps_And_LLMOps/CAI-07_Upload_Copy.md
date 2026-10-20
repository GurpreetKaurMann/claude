# CAI-07 Upload Copy

## 1. Lesson video (YouTube)

**Title:** How to Ship AI Without Breaking It: The Eval Gate That Blocked a "Better" Prompt

**Description:**
```
Lesson 7 of Cloud for AI Engineers. I changed a prompt and the overall score went up. Refund tickets fell from 100% to 50%. A simple eval gate blocked it. This lesson is about shipping AI changes safely, again and again.
We cover the three MLOps maturity levels, what LLMOps versions and monitors, the release loop, three layers of tests, a working eval gate (toy keyword model, synthetic tickets), who should grade, why you run several trials (pass@k and pass^k), the gate as a CI file, registries and aliases, prompt versions, model cards, infrastructure as code and GitOps, canary releases with automatic rollback (simulated), traces and online judges, and cost as a metric. The eval gate uses a toy stand-in model on synthetic data. Trials and canary results are simulations with assumed rates.
⏮️ Previous lesson: <CAI-06 link>

In this lesson:
✅ MLOps levels 0, 1 and 2
✅ LLMOps: prompts, model settings, tools, retrieval index
✅ The release loop: gate, canary, watch
✅ Three layers of tests
✅ A working eval gate: overall +2.0, refund -50.0, BLOCKED
✅ Who grades: code graders first, calibrated LLM judges
✅ pass@k and pass^k: a 90% agent passes 5 runs 59% of the time
✅ The gate as a CI file
✅ Registries, aliases and prompt versions
✅ Model cards
✅ Infrastructure as code and GitOps
✅ Canary releases: 150 bad responses vs 9 (simulation)
✅ Traces, online judges and cost as an alarm
✅ ShopNest Copilot shipping plan
✅ Interview questions with answers

⏱️ Chapters
0:00 A better score that broke refunds
0:26 Intro
0:36 Where we are
1:07 Three maturity levels
1:39 LLMOps is different
2:10 Models decay silently
2:39 The release loop
3:08 Three layers of tests
3:38 What a gate checks
4:04 My toy gate
4:37 The result
5:02 The gate says no
5:22 Averages hide
5:49 Choosing slices
6:15 Who grades?
6:40 Why several trials?
7:04 Reliability, simulated
7:33 The gate in CI
7:56 Registries and aliases
8:23 Prompts as versions
8:48 Model cards
9:12 Infrastructure as code
9:40 Why GitOps
10:04 A GPU pool as code
10:35 Canary releases
11:06 Canary, measured
11:29 The canary trade-off
11:56 Observability
12:26 Online judges
12:48 Continuous evaluation
13:16 Cost as a limit
13:36 ShopNest Copilot
14:02 Four words to keep
14:19 Interview corner
14:54 Your turn
15:16 Recap
15:53 Next lesson

Next lesson → CAI-08: GenAI apps: RAG: from documents to cited answers

🌐 Website: https://thecodenotebook.com/
📸 Instagram: https://www.instagram.com/thecodenotebookyt/

#mlops #llmops #ai #cicd #aiengineering
```

**Tags:**
```
eval gate, llmops explained, mlops levels, how to test llm prompts, pass at k, canary release, gitops for ml, prompt versioning, model registry, llm evaluation ci, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
The eval gate runs a real check on a toy keyword model with synthetic tickets. The trials and canary results are simulations with assumed rates, all labelled in the video. 📊\n\nQuestion for you 👇\nWhich surprised you more: a +2 point change blocked for a -50 slice, or a 90% agent passing 5 runs only 59% of the time?
```

**Thumbnail:** CAI-07_Thumbnail.png

---

## 2. Short 1 (YouTube Shorts)

**Title:** My Prompt Change Raised the Score and a Gate Still Blocked It #shorts

**Description:**
```
Toy keyword model (a stand-in for an LLM), 100 synthetic tickets, a real gate:\n• overall: 90% to 92%\n• refund tickets: 100% to 50%\n• gate: BLOCKED (no slice may drop more than 5 points)\n\nFull lesson: Cloud for AI Engineers, lesson 7.
```

**Tags:**
```
shorts, eval gate, llm evaluation, llmops, prompt testing, ci cd for llm, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Do you score your prompts by slice or only overall? 👇
```

**Cover:** CAI-07_Short1_Cover.png

---

## 3. Short 2 (YouTube Shorts)

**Title:** A 90% Reliable AI Agent Passes 5 Runs in a Row Only 59% of the Time #shorts

**Description:**
```
pass@k = 1 - (1-p)^k (at least one run works)\npass^k = p^k (all runs work)\n\nFor p = 0.9: all 3 runs 72.9%, all 5 runs 59.0%, all 10 runs 34.9%.\nFormulas checked against 100,000 simulated tasks per row. p is assumed.\n\nFull lesson: Cloud for AI Engineers, lesson 7.
```

**Tags:**
```
shorts, pass at k, agent reliability, llm evaluation, ai agents, evals, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
How reliable is your agent across 5 runs? 👇
```

**Cover:** CAI-07_Short2_Cover.png

---

## 4. Instagram Reel 1

**Caption:**
```
Canary releases, simulated. 🐤\n\n600 requests/min, new version fails 5% vs 1% for the old (assumed).\n🔴 100% at once: about 150 bad responses before rollback\n🟠 25% canary: about 38\n🟢 5% canary: about 9\n🟢 1% canary: about 4 (but only 45% caught at the first check)\n\nSmall first. Save this. Full lesson on YouTube: The Code Notebook.
```

**First comment (pin it):**
```
Lesson 8 next: RAG, from documents to cited answers 📚 Follow so you don't miss it!
```

**Cover:** CAI-07_Reel1_Cover_Instagram.png

---
