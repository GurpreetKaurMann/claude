# CAI-03 Upload Copy

## 1. Lesson video (YouTube)

**Title:** Why Changing One Line Re-Uploads 401 MB (Docker for AI Models)

**Description:**
```
Lesson 3 of Cloud for AI Engineers. I changed one line of code and shipped 1 MB or 401 MB, depending only on layer order. And three jobs on 16 GPUs deadlocked 95% of the time.
We learn what a container is, who owns the GPU driver, the host driver compatibility rule, why layer order decides what you re-ship, whether to bake or mount model weights, how Kubernetes hands out GPUs, how to share one GPU (MIG, MPS, time-slicing), why distributed training needs gang scheduling, and which tool fits which job (Kueue, Ray, Kubeflow, Slurm). The layer and scheduler results are experiments with real bytes and hashes but a simulated registry and scheduler. Docker was not running on the build machine.
⏮️ Previous lesson: <CAI-02 link>

In this lesson:
✅ What a container is, in meal-kit terms
✅ Who owns what: host driver, image CUDA libraries, the toolkit bridge
✅ The driver compatibility rule
✅ CVE-2025-23266 and why you patch the host
✅ Layers: why one line can re-ship 401 MB or 1 MB
✅ Bake or mount model weights (OCI image volumes)
✅ Kubernetes in one picture and how pods ask for GPUs
✅ Taints, labels and the GPU Operator
✅ Sharing one GPU: MIG vs MPS vs time-slicing
✅ DRA in plain words
✅ Gang scheduling: 94.8% deadlock without it, 0% with it
✅ Kueue, JobSet, Ray, Kubeflow and Slurm: which for what
✅ ShopNest Copilot on Kubernetes
✅ Interview questions with answers

⏱️ Chapters
0:00 One line of code, 401 megabytes
0:28 Intro
0:38 Where we are
1:07 What a container is
1:30 The GPU problem
2:03 Inside the box
2:32 The compatibility rule
2:59 Patch the host
3:25 Layers
3:53 My layers experiment
4:22 Layer order, measured
4:45 The layer rules
5:07 A Dockerfile sketch
5:36 Bake or mount the weights?
6:03 When the model changes
6:24 How to mount weights
6:51 Kubernetes in one picture
7:14 GPUs in Kubernetes
7:43 Keeping GPUs for GPU jobs
8:08 The GPU Operator
8:36 Sharing one GPU
9:02 Which sharing to use
9:23 Sharing, in numbers
9:51 The future: DRA
10:24 Why gang scheduling
10:53 My gang experiment
11:22 Deadlock, measured
11:42 Queues and gangs in practice
12:15 Ray, Kubeflow, Slurm
12:36 Slurm
13:03 Failures are normal
13:25 A small gotcha
13:49 ShopNest Copilot
14:15 Four words to keep
14:31 Interview corner
15:04 Your turn
15:27 Recap
15:56 Next lesson

Next lesson → CAI-04: Data and storage: where information lives, how to read it fast, and how vectors work

🌐 Website: https://thecodenotebook.com/
📸 Instagram: https://www.instagram.com/thecodenotebookyt/

#kubernetes #docker #gpu #ai #aiengineering
```

**Tags:**
```
docker layers explained, docker image size, kubernetes gpu, gang scheduling, kueue, bake vs mount model weights, nvidia container toolkit, mig mps time slicing, ai deployment kubernetes, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
The layer experiment uses real bytes and hashes with a simulated registry, and the gang result is a simulation, both labelled in the video. 📊

Question for you 👇
Which surprised you more: 1 MB vs 401 MB for the same change, or 95% deadlock?
```

**Thumbnail:** CAI-03_Thumbnail.png

---

## 2. Short 1 (YouTube Shorts)

**Title:** I Changed 1 Line of Code and Shipped 401 MB (Docker Layers) #shorts

**Description:**
```
An image is a stack of layers. Change one layer and every layer above it is rebuilt and re-shipped.

Real files and real hashes, simulated registry (Docker was not running here):
• code on the top layer: 1 MB after a one-line change
• code before the 400 MB weights layer: 401 MB

Full lesson: Cloud for AI Engineers, lesson 3.
```

**Tags:**
```
shorts, docker layers, docker image size, ai deployment, container best practices, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Where do your model weights live: in the image or mounted? 👇
```

**Cover:** CAI-03_Short1_Cover.png

---

## 3. Short 2 (YouTube Shorts)

**Title:** Why 3 AI Jobs on 16 GPUs Froze 95% of the Time #shorts

**Description:**
```
Distributed training needs ALL workers at once.

Simulation: 16 GPUs, each job = 8 pods, 10,000 random arrival orders
• default one-by-one scheduler, 3 jobs: 94.8% deadlock
• gang scheduler: 0%

A simulation of the idea, not of the real kube-scheduler.

Full lesson: Cloud for AI Engineers, lesson 3.
```

**Tags:**
```
shorts, gang scheduling, kubernetes gpu, distributed training, deadlock, kueue, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Have you ever had GPUs sit idle waiting for each other? 👇
```

**Cover:** CAI-03_Short2_Cover.png

---

## 4. Instagram Reel 1

**Caption:**
```
Bake model weights into the image, or mount them? 📦

Real files, simulated registry:
🔴 baked in: a new model re-ships 400 MB
🟢 mounted: 0 MB in the app image, a code change ships 1 MB

Big weights get their own life.

Save this. Full lesson on YouTube: The Code Notebook.
```

**First comment (pin it):**
```
Lesson 4 next: data and storage, and how vectors work 🗄️ Follow so you don't miss it!
```

**Cover:** CAI-03_Reel1_Cover_Instagram.png

---
