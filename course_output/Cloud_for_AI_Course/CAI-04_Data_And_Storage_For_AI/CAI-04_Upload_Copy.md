# CAI-04 Upload Copy

## 1. Lesson video (YouTube)

**Title:** Why 20,000 Small Files Read 25x Slower Than One (AI Data Storage)

**Description:**
```
Lesson 4 of Cloud for AI Engineers. I read the same 80 MB as 20,000 small files and as one shard. The small files took 25 times longer. This lesson is about where AI data lives and how to read it fast.
We cover object storage tiers, the egress bill, why small files hurt and shards fix it, checkpoint size and stalls, the lakehouse, dataset versioning and the 7 day retention trap, then vectors: what they are, how much memory they need, how float16 and int8 shrink them with almost no loss, and how HNSW finds neighbours fast. File reads and vector tests are measured on the build machine (vectors are synthetic), the object store timing is a model with assumed numbers, and prices are list prices from October 2026.
⏮️ Previous lesson: <CAI-03 link>

In this lesson:
✅ Object storage: a filing cabinet with tiers
✅ Region is truth, zone is speed
✅ Egress: why moving 100 TB costs about $9,000 at list price
✅ Small files vs shards: measured 25x
✅ An object store model with assumed latency
✅ WebDataset and Mosaic streaming
✅ Checkpoint size: 14 bytes per parameter, and the stall
✅ The lakehouse in four boxes
✅ Dataset versioning and the 7 day default trap
✅ What a vector is and how big it is
✅ Shrinking vectors: float16, int8 and binary, measured
✅ HNSW: layers, M and ef, and recall vs effort
✅ Choosing a vector store
✅ ShopNest Copilot data plan
✅ Interview questions with answers

⏱️ Chapters
0:00 80 megabytes, 25 times slower
0:29 Intro
0:39 Where we are
1:09 Object storage
1:36 Region is truth, zone is speed
2:09 What lives where
2:37 Egress is the real bill
3:10 An egress sum
3:36 Small files
4:04 My file experiment
4:30 Measured: small files
4:56 The object store model
5:19 Shards
5:52 Text is rarely the bottleneck
6:18 Fast file systems
6:51 Checkpoint size
7:19 The stall
7:43 The lakehouse
8:11 Versioning data
8:35 The retention trap
8:56 Reproducibility and quality
9:23 What a vector is
9:50 How big are vectors?
10:16 My compression experiment
10:43 Compression, measured
11:16 Finding neighbours fast
11:42 HNSW knobs and memory
12:09 HNSW, measured
12:33 Other index families
13:06 Choosing a vector store
13:34 ShopNest Copilot
14:04 Four words to keep
14:21 Interview corner
14:54 Your turn
15:17 Recap
15:52 Next lesson

Next lesson → CAI-05: Training at scale: where the memory goes and how to split a model

🌐 Website: https://thecodenotebook.com/
📸 Instagram: https://www.instagram.com/thecodenotebookyt/

#cloudcomputing #datastorage #vectordatabase #ai #aiengineering
```

**Tags:**
```
small files problem, data sharding, object storage explained, s3 egress cost, vector database memory, hnsw explained, quantization embeddings, pgvector, lakehouse, delta lake time travel, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
File reads and vector tests were measured on the build machine (synthetic vectors). The object store timing is a model with assumed numbers. 📊

Question for you 👇
Which surprised you more: 25x slower for small files, or 98% recall at a quarter of the vector memory?
```

**Thumbnail:** CAI-04_Thumbnail.png

---

## 2. Short 1 (YouTube Shorts)

**Title:** Why 20,000 Small Files Read 25x Slower Than One #shorts

**Description:**
```
Same 80 MB, three layouts, local disk, page cache dropped, best of 3:
• 20,000 files of 4 KB: 1.34 s
• 80 files of 1 MB: 0.08 s
• one 80 MB shard: 0.05 s

Cloud object stores add a delay per request, so the gap is bigger there (model with assumed numbers).

Full lesson: Cloud for AI Engineers, lesson 4.
```

**Tags:**
```
shorts, small files problem, data sharding, webdataset, ai training data, object storage, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
How many files is your training set made of? 👇
```

**Cover:** CAI-04_Short1_Cover.png

---

## 3. Short 2 (YouTube Shorts)

**Title:** Shrink Your Vector Database 4x and Keep 98% Recall #shorts

**Description:**
```
50,000 SYNTHETIC vectors x 768 numbers (not real embeddings), recall@10 vs exact float32 search:
• float32: 153.6 MB, 1.000
• float16: 76.8 MB, 1.000
• int8: 38.4 MB, 0.985
• 1-bit (Hamming only): 4.8 MB, 0.212

Full lesson: Cloud for AI Engineers, lesson 4.
```

**Tags:**
```
shorts, vector database, quantization, embeddings memory, pgvector halfvec, rag cost, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Do you compress your embeddings? 👇
```

**Cover:** CAI-04_Short2_Cover.png

---

## 4. Instagram Reel 1

**Caption:**
```
The cloud bill nobody warns you about. 💸

Storing data: cheap.
Moving it OUT (egress): about $0.09 per GB at list price.

100 TB = 100,000 GB x $0.09 = $9,000.

Move the job to the data, not the data to the job.

Arithmetic from list prices, not a quote. Save this. Full lesson on YouTube: The Code Notebook.
```

**First comment (pin it):**
```
Lesson 5 next: training at scale 🧠 Follow so you don't miss it!
```

**Cover:** CAI-04_Reel1_Cover_Instagram.png

---
