# CAI-01 Upload Copy

## 1. Lesson video (YouTube)

**Title:** Will Your Model Fit on a GPU? The 70B Model That Fits, Then Fails | Cloud for AI Engineers 1

**Description:**
```
A 70 billion parameter model fits on one H100. Then 32 people start chatting and you need 187 GB. This lesson explains why, and gives you the sum.
Lesson 1 of Cloud for AI Engineers. We learn the four numbers on every GPU spec sheet (memory size, memory speed, compute, connection), turn parameters into gigabytes, meet the KV cache, and measure why chat speed is set by memory speed. Chip specs are vendor figures from October 2026, the sums are labelled arithmetic, and the CPU tests are measured by me.

In this lesson:
✅ The four numbers on every GPU spec sheet
✅ Weights in gigabytes: parameters × bytes per number
✅ Precision: BF16, FP8 and FP4 in plain English
✅ GPU memory tiers: 80, about 141 to 192, 288 GB
✅ The KV cache: why 32 chats need 86 GB of notes
✅ The fit rule: weights + chats + headroom
✅ Measured: 4x the bytes took 8.4x the time on my CPU
✅ Same law on H100, H200 and B200 (arithmetic from specs)
✅ Batching: about 10x the tokens per second, measured
✅ Why the connection between GPUs matters for big models
✅ ShopNest Copilot: sizing our own assistant
✅ Interview questions with answers

⏱️ Chapters
0:00 The model fits. The chats do not.
0:24 Intro
0:35 What this course is
1:06 What the cloud is
1:32 CPU versus GPU
2:00 The four numbers
2:27 Parameters and weights
2:57 Weights in gigabytes
3:23 Precision
3:52 Does it fit?
4:29 Three memory tiers
4:58 The KV cache
5:24 How big is one token of notes?
5:54 Adding it up
6:29 The numbers per chat
6:52 The fit rule
7:18 Shrinking the notes
7:45 Number two: memory speed
8:09 One word, all the weights
8:34 Let me measure it
9:01 Measured: size and time
9:36 Same law, on a GPU
10:16 The bandwidth ladder
10:44 Number three: compute
11:12 Batching
11:47 What limits batching
12:10 Number four: connection
12:45 When one GPU is not enough
13:15 How to choose
13:34 ShopNest Copilot
14:03 Four words to keep
14:23 Interview corner
14:52 Your turn
15:13 Recap
15:50 Next lesson

Next lesson → CAI-02: Renting compute: which chip, what it costs, spot and autoscaling

🌐 Website: https://thecodenotebook.com/
📸 Instagram: https://www.instagram.com/thecodenotebookyt/

#cloudcomputing #gpu #ai #llm #aiengineering
```

**Tags:**
```
will my model fit on a gpu, gpu memory explained, kv cache explained, llm memory, h100 vs h200, how much gpu memory do I need, hbm memory bandwidth, batching llm, cloud for ai engineers, ai infrastructure for beginners, the code notebook
```

**Pinned comment:**
```
Every measured number in this lesson came from code that ran on a CPU, and every GPU figure is labelled as a vendor number from Oct 2026. 📊

Question for you 👇
Which surprised you more: the chats needing more memory than the model, or 4x the data taking 8x the time?
```

**Thumbnail:** CAI-01_Thumbnail.png

---

## 2. Short 1 (YouTube Shorts)

**Title:** A 70B Model Fits Your GPU, Then Fails (Here's Why) #shorts

**Description:**
```
70B parameters in FP8 = 70 GB of weights. One H100 has 80 GB. It fits... until people start chatting.

Every open chat keeps a KV cache in GPU memory:
• 32 chats × 8,192 tokens = 85.9 GB of notes
• plus 20% headroom = 187 GB needed

Arithmetic with an assumed model shape (80 layers, 8 KV heads, head size 128). GPU memory from vendor specs, Oct 2026.

Full lesson: Cloud for AI Engineers, lesson 1.
```

**Tags:**
```
shorts, gpu memory, kv cache, llm serving, will my model fit, h100, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Did you know the chat notes can use more memory than the model? 👇
```

**Cover:** CAI-01_Short1_Cover.png

---

## 3. Short 2 (YouTube Shorts)

**Title:** Why AI Chips Need Special Memory (I Measured It) #shorts

**Description:**
```
One token of a chat model = reading ALL the weights once, so memory speed sets the pace.

Measured on a CPU, one core, matrix × vector:
• 67 MB table: 2.43 ms
• 268 MB table: 20.35 ms

4x the bytes, 8.4x the time. The small table fit in the CPU cache.

This is a CPU, not a GPU. The law is the same: time ≥ weight bytes ÷ bandwidth.

Full lesson: Cloud for AI Engineers, lesson 1.
```

**Tags:**
```
shorts, memory bandwidth, hbm, gpu memory, llm inference, why gpus need fast memory, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Would you rather have a faster GPU or faster memory for chat? 👇
```

**Cover:** CAI-01_Short2_Cover.png

---

## 4. Instagram Reel 1

**Caption:**
```
Why serving many people at once makes AI cheaper. 💸

I measured it on a CPU (one core):
1️⃣ one token at a time: about 390 tokens/s
2️⃣5️⃣6️⃣ at once: about 4,000 tokens/s

About 10x the output. Each step took about 24x longer, but the weights were read once for everyone.

That's batching, and it's why chat APIs can be priced so low.

Save this. Full lesson on YouTube: The Code Notebook.
```

**First comment (pin it):**
```
Lesson 2 next: which GPU to rent, what it costs, and how spot machines cut the bill 💸 Follow so you don't miss it!
```

**Cover:** CAI-01_Reel1_Cover_Instagram.png

---
