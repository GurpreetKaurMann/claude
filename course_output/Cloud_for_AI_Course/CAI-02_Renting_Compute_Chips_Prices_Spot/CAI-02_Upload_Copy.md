# CAI-02 Upload Copy

## 1. Lesson video (YouTube)

**Title:** Why Cheap Spot GPUs End Up Costing MORE (The Checkpoint Mistake)

**Description:**
```
Lesson 2 of Cloud for AI Engineers. I simulated a 100 hour job on cheap spot GPUs. With no saves it needs over two million hours. Save too often and it costs more than on-demand.
We pick a chip (NVIDIA, AMD, Google TPU, AWS Trainium), learn to read machine names, climb the buying ladder from on-demand to spot, find the commitment trap, simulate spot interruptions, work out the best save interval, compare price per petaflop and simulate scale to zero. Chip facts and prices are vendor figures dated October 2026, the sums are labelled arithmetic, and the spot and scale to zero results are simulations with assumed rates.
⏮️ Previous lesson: <CAI-01 link>

In this lesson:
✅ Four chip families and what each is for
✅ Which NVIDIA, AMD, TPU and Trainium chips you can really rent in October 2026
✅ How to read machine names on AWS, Google Cloud and Azure
✅ Big clouds versus neoclouds
✅ The buying ladder: on-demand, queued, commitment, spot
✅ The commitment trap: real price = rate ÷ how busy you are
✅ Spot simulation: no saves needs 2,203,564 hours for a 100 hour job
✅ The best save interval: about 34 minutes, and why 30 seconds costs more than on-demand
✅ Price per petaflop-hour for TPU and B200
✅ Autoscaling with KEDA and Karpenter
✅ Scale to zero: 24 to 4.04 GPU-hours a day, and the 60 second cold start
✅ ShopNest Copilot: three workloads, three rungs
✅ Interview questions with answers

⏱️ Chapters
0:00 A hundred hour job, never saved
0:31 Intro
0:41 Where we are
1:11 Four families of chips
1:40 The map
2:10 NVIDIA chips to know
2:41 AMD
3:08 Google TPU
3:36 AWS Trainium
4:06 The cost of switching
4:33 Status words
4:56 Reading instance names
5:30 Big clouds and neoclouds
6:00 The buying ladder
6:31 Commitments
6:58 The commitment trap
7:34 Break-even
7:56 Queued capacity
8:21 Spot
8:47 My spot simulation
9:19 Never save
9:45 How often to save
10:11 The bill
10:37 Young's rule
11:06 When to use spot
11:27 Price per petaflop
11:59 Autoscaling
12:31 Scale to zero
12:57 Scale to zero, measured
13:33 Cold start trade-off
13:43 Fixing cold starts
14:10 ShopNest Copilot
14:36 Four words to keep
14:55 Interview corner
15:24 Your turn
15:46 Recap
16:16 Next lesson

Next lesson → CAI-03: Containers and Kubernetes for AI: package a model so it runs the same everywhere

🌐 Website: https://thecodenotebook.com/
📸 Instagram: https://www.instagram.com/thecodenotebookyt/

#cloudcomputing #gpu #ai #spotinstances #aiengineering
```

**Tags:**
```
spot instances explained, gpu cost, how to rent gpus, checkpointing, reserved instances vs spot, scale to zero, ai infrastructure cost, tpu vs gpu, trainium, h100 price, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Every spot and scale to zero number here comes from a simulation with assumed rates, and every price is a vendor figure from Oct 2026. 📊

Question for you 👇
Which surprised you more: a job that never finishes without saves, or saving too often costing more than on-demand?
```

**Thumbnail:** CAI-02_Thumbnail.png

---

## 2. Short 1 (YouTube Shorts)

**Title:** Why a 100-Hour Job Can Take 2 Million Hours on Cheap GPUs #shorts

**Description:**
```
Spot GPUs are cheap because the provider can take them back.

Simulation (assumed: interrupted every 8 h on average, 100 h job):
• never save: 2,203,564 hours
• save every 34 min: about 109 hours

This is a simulation with assumed rates, not real machines.

Full lesson: Cloud for AI Engineers, lesson 2.
```

**Tags:**
```
shorts, spot instances, gpu cost, checkpointing, ai training cost, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Do you checkpoint your training runs? 👇
```

**Cover:** CAI-02_Short1_Cover.png

---

## 3. Short 2 (YouTube Shorts)

**Title:** When a 55% GPU Discount Costs You MORE #shorts

**Description:**
```
A commitment is a promise to pay, busy or idle.

Real price = rate ÷ how busy you keep it.
Assumed on-demand: $10/hr, commit: 55% off ($4.50)
• 90% busy: $5.00 per used hour
• 45% busy: $10.00
• 30% busy: $15.00
• 10% busy: $45.00

Arithmetic with assumed prices.

Full lesson: Cloud for AI Engineers, lesson 2.
```

**Tags:**
```
shorts, gpu commitment, reserved instances, cloud cost, ai infrastructure, finops, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
What percent busy is your GPU, really? 👇
```

**Cover:** CAI-02_Short2_Cover.png

---

## 4. Instagram Reel 1

**Caption:**
```
Scale to zero, simulated. 🔌

One GPU, one bursty day (assumed traffic):
🔴 always on: 24 GPU-hours
🟢 scale to zero: about 4 GPU-hours

83% fewer hours billed.
The catch: about 4 cold starts a day, each user waits a full 60 s (assumed cold start).

Save this. Full lesson on YouTube: The Code Notebook.
```

**First comment (pin it):**
```
Lesson 3 next: containers and Kubernetes for AI 📦 Follow so you don't miss it!
```

**Cover:** CAI-02_Reel1_Cover_Instagram.png

---
