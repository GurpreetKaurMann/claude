# CAI-05 Upload Copy

## 1. Lesson video (YouTube)

**Title:** Why Training a 70B Model Needs 1,120 GB (The 16-Byte Rule)

**Description:**
```
Lesson 5 of Cloud for AI Engineers. A 70B model is 140 GB of weights, but training it needs 1,120 GB. This lesson explains the 16-byte rule, how to share the memory across GPUs, and what training really costs.
We build the training memory ledger (weights, gradients, optimiser state, activations), measure it on a real small model, see how ZeRO and FSDP shard it, measure what recomputation saves, count GPU-hours with the 6ND rule, compare the four ways to split a model, simulate the pipeline bubble, price the network, and measure why LoRA needs 100 times less optimiser memory. Measured on a CPU with a small model; large-model numbers are arithmetic and simulation, labelled on screen.
⏮️ Previous lesson: <CAI-04 link>

In this lesson:
✅ What training is: guess, blame, nudge
✅ The 16-byte ledger: 2 + 2 + 12
✅ Measured: 16.0 bytes per parameter on a real model
✅ ZeRO and FSDP: 1,120 GB to 17.5 GB per GPU
✅ Activations and recomputation: measured 0.54x memory for about 1.2x time
✅ The 6ND rule: 7B on 2T tokens is about 59,000 GPU-hours
✅ MFU, honestly
✅ Data, tensor, pipeline and expert parallel
✅ The pipeline bubble: 42.9% idle, simulated
✅ Mapping splits to the hardware
✅ NCCL and the silent 2 to 5x slowdown
✅ Failures: one every 3.1 hours
✅ LoRA: 0.97% trained, 100x less optimiser memory, measured
✅ ShopNest Copilot: fine-tune, do not pretrain
✅ Interview questions with answers

⏱️ Chapters
0:00 The 1,120 gigabyte surprise
0:26 Intro
0:37 Where we are
1:08 What training is
1:35 Four things in memory
2:03 The 16-byte ledger
2:34 Measured on a real model
2:59 Scaling up
3:23 Sharding the state
4:01 Why stage three
4:28 Activations
5:09 Recomputation
5:37 Recompute, measured
6:02 Counting compute
6:31 A worked example
7:11 MFU honesty
7:46 How many tokens?
8:13 Four ways to split
8:45 Tensor parallel
9:08 Pipeline parallel
9:34 The bubble, drawn
9:56 Shrinking the bubble
10:21 Mapping to the hardware
10:54 The network cost
11:25 The silent slowdown
11:55 Number formats
12:23 Failures are routine
12:46 Fine-tuning
13:13 The usual order
13:42 Tools to know
14:08 ShopNest Copilot
14:33 Four words to keep
14:51 Interview corner
15:22 Your turn
15:42 Recap
16:17 Next lesson

Next lesson → CAI-06: Inference and serving: how to make a trained model answer fast

🌐 Website: https://thecodenotebook.com/
📸 Instagram: https://www.instagram.com/thecodenotebookyt/

#machinelearning #llm #gpu #ai #aiengineering
```

**Tags:**
```
how much gpu memory to train llm, 16 bytes per parameter, adam optimizer memory, zero fsdp explained, gradient checkpointing, lora memory, pipeline parallelism bubble, tensor parallelism, 6nd flops, training cost, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
The ledger and LoRA numbers were measured on a small real model on a CPU. Big-model numbers are arithmetic from the notebook's formulas, and the bubble is a simulation. 📊

Question for you 👇
Which surprised you more: weights being only 1/8 of the training bill, or LoRA needing 100x less optimiser memory?
```

**Thumbnail:** CAI-05_Thumbnail.png

---

## 2. Short 1 (YouTube Shorts)

**Title:** Why Training a 70B Model Needs 1,120 GB (Not 140) #shorts

**Description:**
```
Training memory per parameter (mixed precision with Adam): 2 (weights) + 2 (gradients) + 12 (fp32 master + Adam m + Adam v) = 16 bytes.

Measured on a real 33.6M-parameter model: 16.0 bytes per parameter.
70B x 16 = 1,120 GB (arithmetic).

Full lesson: Cloud for AI Engineers, lesson 5.
```

**Tags:**
```
shorts, training memory, how much gpu memory to train, adam optimizer memory, zero fsdp, llm training, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Did you know weights are only 1/8 of the training memory? 👇
```

**Cover:** CAI-05_Short1_Cover.png

---

## 3. Short 2 (YouTube Shorts)

**Title:** LoRA Trains Under 1% of a Model: 100x Less Memory #shorts

**Description:**
```
MEASURED on a small 33.6M-parameter model (PyTorch, CPU):
• full training: Adam state 268.6 MB
• LoRA rank 8: trains 0.97% of parameters, Adam state 2.6 MB
• LoRA rank 16: 1.91%, 5.2 MB

Full lesson: Cloud for AI Engineers, lesson 5.
```

**Tags:**
```
shorts, lora explained, fine tuning memory, qlora, parameter efficient fine tuning, llm fine tuning, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Have you fine-tuned with LoRA yet? 👇
```

**Cover:** CAI-05_Short2_Cover.png

---

## 4. Instagram Reel 1

**Caption:**
```
The pipeline bubble, simulated. 🫧

Bubble = (p-1) / (m+p-1)
🔴 4 stages, 4 micro-batches: 42.9% idle
🟠 8 stages, 32 micro-batches: 17.9%
🟢 8 stages, 128 micro-batches: 5.2%

Keep the pipeline full.

Save this. Full lesson on YouTube: The Code Notebook.
```

**First comment (pin it):**
```
Lesson 6 next: inference and serving, how to make a trained model answer fast ⚡ Follow so you don't miss it!
```

**Cover:** CAI-05_Reel1_Cover_Instagram.png

---
