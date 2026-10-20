# CAI-11 Upload Copy

## 1. Lesson video (YouTube)

**Title:** Why a $3 GPU Really Costs $63 (and the Prompt Line That Triples Your AI Bill)

**Description:**
```
Lesson 11 of Cloud for AI Engineers. A GPU listed at $3.17 an hour costs $63.40 per useful hour at 5% utilisation. And one changing line at the top of a prompt gave 0% cache hits in my test, a 3.5x higher input bill.
We cover the FinOps loop (inform, optimise, operate), measuring utilisation honestly, the real price of a GPU hour, right-sizing and sharing (MIG, time-slicing, MPS), ways to buy GPU time and the commitment rule (use must beat 1 minus the discount), one training run priced five ways (5.4x spread), token pricing, a costed support bot, the five levers in order (cache, batch, prompt audit, effort, routing), cache hit rate against traffic, the timestamp mistake measured with a toy cache, self-hosting versus API with a break-even calculator, attribution with a gateway, cost per resolved ticket, budgets and anomaly alerts, and hidden storage and network lines. Prices are the notebook's approximate list prices (Oct 2026) and move often, the cache is a toy I wrote, and the gateway logs are invented.
⏮️ Previous lesson: <CAI-10 link>

In this lesson:
✅ The Fin Ops loop: inform, optimise, operate
✅ Why nvidia-smi utilisation misleads
✅ Real price = list price / utilisation: $3.17 becomes $63.40 at 5%
✅ MIG, time-slicing and MPS
✅ Ways to buy: on-demand, reserved, capacity block, spot, flex start
✅ The commitment rule: use must beat 1 minus the discount
✅ One training run, five ways to pay: 5.4x spread
✅ Token pricing and a costed support bot
✅ Caching, batch, prompt audit, effort and routing: the lever order
✅ Cache hit rate vs traffic (simulated)
✅ The timestamp mistake: 0% cached vs 75% (toy cache, measured)
✅ Self-host vs API break-even volume
✅ Attribution, showback and cost per resolved ticket
✅ Budgets and anomaly alerts (invented logs)
✅ Hidden lines: cross-AZ and checkpoint storage
✅ Interview questions with answers

⏱️ Chapters
0:00 A three dollar GPU
0:32 Intro
0:42 Where we are
1:15 The Fin Ops loop
1:50 Measure the right thing
2:29 How idle is normal
3:08 The real price
3:46 Right size, then share
4:26 Ways to buy a GPU
5:03 The commitment rule
5:37 One run, five ways
6:14 The token bill
6:50 A real price table
7:25 A support bot, costed
8:02 Lever one: caching
8:40 Does the cache hit?
9:15 The timestamp mistake
9:49 Lever two: batch
10:18 Levers three and four
10:55 Lever five: routing
11:33 Self-host: the formula
12:14 The break-even volume
12:55 Self-host: what the sum hides
13:34 Who spent it?
14:13 Showback and cost per ticket
14:53 Budgets and alerts
15:33 Hidden lines
16:13 ShopNest Copilot: cost plan
16:45 Four words to keep
17:06 Interview corner
17:41 Your turn
18:06 Recap
18:41 Next lesson

Next lesson → CAI-12: Your learning path: from zero to cloud AI engineer

🌐 Website: https://thecodenotebook.com/
📸 Instagram: https://www.instagram.com/thecodenotebookyt/

#finops #aicost #gpu #llm #cloudcomputing
```

**Tags:**
```
finops for ai, gpu utilization, real price of a gpu, llm api cost, prompt caching, self host vs api, break even calculator, cost per resolved ticket, ai cost optimization, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Prices are the notebook's approximate Oct 2026 list prices and change often, the cache test uses a toy cache I wrote, and the gateway logs are invented. 📊\n\nQuestion for you 👇\nWhat is your biggest AI cost: GPUs sitting idle, or tokens you send again and again?
```

**Thumbnail:** CAI-11_Thumbnail.png

---

## 2. Short 1 (YouTube Shorts)

**Title:** Why a $3 GPU Really Costs $63 (The Utilisation Sum) #shorts

**Description:**
```
Arithmetic from the notebook's Oct 2026 prices (they move often):\n• H100 listed $3.17/hr\n• real price = list price / utilisation\n• 5% use: $63.40 per useful hour\n• 50% use: $6.34\n• best rate discounts: about 2-3x, fixing idle: 10x\n\nFull lesson: Cloud for AI Engineers, lesson 11.
```

**Tags:**
```
shorts, gpu cost, finops, gpu utilization, cloud cost, ai infrastructure cost, h100 price, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
What utilisation does your GPU cluster really run at? 👇
```

**Cover:** CAI-11_Short1_Cover.png

---

## 3. Short 2 (YouTube Shorts)

**Title:** One Line in Your Prompt Can Triple Your AI Bill (Cache Mistake) #shorts

**Description:**
```
Measured with a toy prefix cache I wrote (not any vendor's cache), 5,000 requests of about 4,000 tokens:\n• changing timestamp at the TOP of the system prompt: 0% of tokens cached\n• same timestamp AFTER the shared part: 74.9% cached\n• input bill 3.5x higher with the timestamp on top\n\nFull lesson: Cloud for AI Engineers, lesson 11.
```

**Tags:**
```
shorts, prompt caching, llm cost, finops, claude api cost, ai bill, prompt engineering, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Is anything at the top of your system prompt changing per request? 👇
```

**Cover:** CAI-11_Short2_Cover.png

---

## 4. Instagram Reel 1

**Caption:**
```
Self-host or API? 🤔\n\nThe break-even sum (arithmetic, notebook prices Oct 2026):\n🟢 vs Opus 5.5: one H100 can win above ~10.6M tokens/day\n🟠 vs Sonnet 5.5: above ~21.1M (one card tops out at 34.6M)\n🔴 vs Haiku 5.5: needs ~423M/day, never on one GPU\n\nCompare cost per solved task. Save this. Full lesson on YouTube: The Code Notebook.
```

**First comment (pin it):**
```
Lesson 12 next: your learning path, the finale 🎓 Follow so you don't miss it!
```

**Cover:** CAI-11_Reel1_Cover_Instagram.png

---
