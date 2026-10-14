# Course roadmap: Cloud for AI Engineers (code CAI)

Channel: The Code Notebook. 12 long lessons, 15-20 min each, 2 Shorts + 1 Reel per lesson, notes PDF, thumbnail, subtitles, scripts, upload copy, code zip.
Audience: total beginners. Every topic is taught in depth, but every term is explained in plain words first.
Running project: **ShopNest Copilot** (the AI support assistant for an online store), now moved to the cloud step by step.
Numbers: measured by CPU labs where possible. Chip specs and prices come from the notebook (dated 14 Oct 2026) and are labelled "from vendors, not measured here".

Source: the Cloud for AI Engineers notebook (`handwritten_notes`, branch `claude/serene-sagan-cr4kve`).

## Module 1 · Compute: the chips you rent
**1. What a GPU really is, and will your model fit?** (Compute I)
- Why AI needs GPUs. The four numbers: memory size, memory speed, FLOPs, how GPUs connect.
- Memory math: weights = parameters x bytes. 8B, 70B, 405B models, BF16 vs FP8 vs FP4.
- KV cache: the part everyone forgets. Why decode speed depends on memory speed.
- Lab: compute weights and KV cache sizes in code; a tiny CPU test showing memory-bound vs compute-bound.
- Teaser: which chip to rent.

**2. Renting compute: chips, prices and autoscaling** (Compute II)
- NVIDIA, AMD, Google TPU, AWS Trainium: what each is for. Reading instance names (p5, a3, ND96).
- Buying ladder: on-demand, commitments, reserved windows, queued, spot (and what "2 minutes warning" means).
- Autoscaling and scale to zero: the cold-start trade-off. Neoclouds vs big clouds.
- Lab: simulate spot interruptions with and without checkpoints; cost of idle vs scale-to-zero.

## Module 2 · Packaging and storing
**3. Containers and Kubernetes for AI**
- Image vs host: who owns the driver, who owns CUDA libraries. Mount weights, don't bake them in.
- Kubernetes GPU scheduling, gang scheduling, Ray, Kubeflow, Slurm: when to use which.
- Lab: image size with and without baked weights; startup time comparison.

**4. Data and storage: object stores, lakehouses, vectors**
- Object storage as the source of truth; region = truth, zone = speed.
- Why shards beat millions of small files. Lakehouse, feature stores, point-in-time joins.
- Vector databases: bytes per vector, HNSW vs IVF, compression.
- Lab: read speed of small files vs shards; vector memory at float32/int8/binary and recall measured.

## Module 3 · Training and serving
**5. Training at scale**
- Where training memory goes (the 16 bytes per parameter rule). Data, tensor, pipeline parallelism, FSDP.
- Mixed precision, checkpointing, failures as routine. LoRA and fine-tuning for most jobs.
- Lab: memory ledger calculator; a tiny training run with and without gradient checkpointing; checkpoint interval simulation.

**6. Inference and serving**
- Prefill vs decode, TTFT, ITL, goodput. Batching, paged KV cache, quantization, speculative decoding.
- Managed APIs vs self-hosting.
- Lab: toy batching simulator (throughput vs latency); quantization error measured.

## Module 4 · Shipping it
**7. MLOps and LLMOps**
- The 3 maturity levels. CI/CD, infrastructure as code, registries, canary rollouts.
- Evals: code graders, LLM judges, traces. Observability.
- Lab: a small eval gate that blocks a bad prompt change.

**8. GenAI apps I: RAG from documents to cited answers**
- Parse, chunk, context, embed, hybrid search, fuse, rerank, answer with citations.
- Lab: chunk size vs retrieval hit rate; BM25 vs vector vs fused (RRF) measured on a small set.

**9. GenAI apps II: agents, tools, MCP and reliability**
- Agent = model + tools + loop + memory + stop rules. MCP and A2A in simple words.
- Long tasks, queues, sandboxes, caching, gateways, retries, circuit breakers.
- Lab: retry with jitter vs without under a simulated overloaded server.

## Module 5 · Safe, cheap, and your career
**10. Security and governance**
- Shared responsibility. Identity, network, encryption, logs. The missing lock: app-level authorisation.
- Prompt injection and the "lethal trifecta". Guardrails vs architecture. Compliance basics.
- Lab: a toy prompt-injection test against ShopNest Copilot, with and without least-privilege tools.

**11. Cost and FinOps**
- Real GPU price = rate / utilisation. Token economics: input vs output vs cache.
- Self-host vs API break-even. Tagging, showback, cost per task.
- Lab: break-even calculator; cache savings on a real prompt trace.

**12. Your learning path: from zero to cloud AI engineer**
- 6 stages, projects, certifications, how to practise on free credits.
- Closes the course.

## Open items before building
1. `video/ms01/thumbs4.html` (cover CSS) is **missing from the course-factory kit**; a stub is in place. Short/Reel covers need the original file from the PC (`/home/claude/video/ms01/thumbs4.html` in the old account) or a redesign.
2. The pipeline is built for 4 Shorts + 2 Reels. For 2 Shorts + 1 Reel, `lib.py`, `check.py` and the upload code need a small change.
3. New colour theme and thumbnail layout to add (not orchid, terracotta, violet, pine or cobalt).
4. Lesson 1 and one thumbnail are shown to Gurpreet before the rest are made.
