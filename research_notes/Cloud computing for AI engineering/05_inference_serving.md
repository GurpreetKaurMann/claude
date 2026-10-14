# Model Inference & Serving in the Cloud (LLMs), as of October 2026

> Researcher notes, compiled 2026-10-14. Conventions: **[2026]** = current-state finding dated 2026; **[OLDER: yyyy]** = foundational or pre-2026 item that's still relevant but not current news; **[VENDOR]** = self-reported vendor claim; **[2NDARY]** = third-party blog or aggregator, not a primary source. Method note: WebFetch failed with DNS errors (ENOTFOUND) on every domain tried (docs.nvidia.com, vllm.ai, llm-d.ai, arxiv.org), and the shared web-search budget ran out before the last three queries (torch.compile/CUDA graphs, Medusa/n-gram, autoscaling metrics). Most findings below therefore come from search-result summaries, not full-page reads. Where the summary named the primary page, that page is cited. Anthropic API facts come from Anthropic's bundled `claude-api` reference (cached 2026-10-06), which mirrors the official docs linked below.

---

## 1. Metrics: TTFT, TPOT/ITL, throughput, goodput, tail latency; prefill vs decode; arithmetic intensity; why batch size matters

### Takeaway
LLM inference has two phases. Prefill processes the whole prompt in parallel, so it is compute-bound and sets TTFT. Decode emits one token per step and has to re-read all weights plus the KV cache each step, so it is memory-bandwidth-bound and sets TPOT/ITL. Batching is the main lever: it amortizes weight reads across more tokens and raises decode's arithmetic intensity roughly linearly with batch size, until the GPU becomes compute-bound or KV memory runs out. The serving-relevant metric is **goodput**: throughput that still meets both the TTFT and the TPOT SLO.

### Cited Findings
- **Prefill is compute-bound; decode is memory-bound.** Prefill runs the whole prompt as one batched matrix multiply, so its arithmetic intensity is high. At batch 1, decode GEMMs have intensity around 1 and run at about 1% of peak FLOPS. Extra FLOPS shorten prefill but don't improve decode latency. — [Baseten Inference Engineering: Calculating Inference Bottlenecks](https://www.baseten.co/inference-engineering/book/02-models/calculating-inference-bottlenecks/); [dev.to: Why LLM decoding is memory-bound](https://dev.to/ji_ai/why-llm-decoding-is-memory-bound-prefill-vs-decode-roofline-223f) [2NDARY]; [Spheron: Roofline model for LLM inference](https://www.spheron.network/blog/the-roofline-model-for-llm-inference-are-you-compute-bound-o/) [2NDARY]
- **Roofline ridge point on H100:** 989 TFLOPS dense FP16/BF16 against 3.35 TB/s HBM gives an ops:byte ratio of about **295**. A kernel below that intensity is bandwidth-limited. — [Baseten](https://www.baseten.co/inference-engineering/book/02-models/calculating-inference-bottlenecks/); [ZeroEntropy: Arithmetic Intensity](https://www.zeroentropy.dev/concepts/arithmetic-intensity/) [2NDARY] (the search summary merged these sources, so the exact attribution is uncertain)
- **Batch-size rule of thumb:** for a weight-dominated linear layer, arithmetic intensity ≈ B, the batch size in tokens. Batching reuses the same weight traffic across more tokens. One source notes that batch 32 is "still memory-bound (ridge is ~295 on H100), but 30x faster per token than batch 1". Estimates of the crossover vary: one says an H100 needs about 280 tokens of batch in BF16 to cross the ridge, others say production batches of 16–32 usually stay memory-bound. — [dev.to](https://dev.to/ji_ai/why-llm-decoding-is-memory-bound-prefill-vs-decode-roofline-223f) [2NDARY]; [Spheron](https://www.spheron.network/blog/the-roofline-model-for-llm-inference-are-you-compute-bound-o/) [2NDARY]
- **KV reads cap decode intensity at long context.** Decode runs at intensity of about 1–4 even with batching, because per-sequence KV-cache reads grow with sequence length and are not shared across the batch. — [Spheron: AI memory wall / inference latency guide 2026](https://www.spheron.network/blog/ai-memory-wall-inference-latency-guide-2026/) [2NDARY]
- **Goodput (DistServe, OSDI '24) [OLDER: 2024]:** the maximum request rate per GPU that still meets both the TTFT and the TPOT (time-per-output-token) constraint. DistServe reports serving 7.4× more requests, or meeting 12.6× tighter SLOs, than the state-of-the-art systems it compared against, with more than 90% of requests within latency constraints. — [USENIX OSDI '24 DistServe](https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin); [arXiv 2401.09670](https://arxiv.org/abs/2401.09670v2)
- **How public benchmarks define output speed:** Artificial Analysis reports output speed (tokens/s) as a median over a rolling 72-hour window, sampled several times a day, with a default 10,000-token input. TTFT is reported separately; one example is Llama 3.3 70B on Groq at about 297 tok/s with about 1.01 s TTFT. — reported secondhand via [fast.io: Fastest AI 2026](https://fast.io/resources/fastest-ai-2026/); [TokenDyno leaderboard](https://tokendyno.com/blog/fastest-llm-inference/) [2NDARY] (no primary Artificial Analysis page was retrievable)
- **Reasoning modes widen the spread.** In one high-reasoning gpt-oss-120B test, measured output speed ranged from about 92 to 1,916 tok/s across hosts. — [fast.io](https://fast.io/resources/fastest-ai-2026/); [Kingy AI: providers compared](https://kingy.ai/blog/ai-inference-providers-compared/) [2NDARY]
- **MLPerf Inference v6.0 [2026] (published April 1, 2026)** reports throughput in Server scenarios (latency-constrained, Poisson arrivals) and Offline scenarios (pure throughput):
  - NVIDIA: a full-rack GB300 NVL72 posted 575,580 tok/s (Server) and 673,936 tok/s (Offline) on DeepSeek-R1, scaling linearly from smaller configurations. — [NVIDIA Technical Blog](https://developer.nvidia.com/blog/nvidia-extreme-co-design-delivers-new-mlperf-inference-records/) [VENDOR]
  - AMD: an 11-node, 87-GPU MI355X system reached 1,042,110 tok/s Offline on Llama 2 70B, AMD's first result above 1M tok/s. AMD also submitted first-time results for the new gpt-oss-120b and Wan2.2 benchmarks. — [AMD blog](https://www.amd.com/en/blogs/2026/amd-delivers-breakthrough-mlperf-inference-6-0-results.html); [ROCm blog](https://rocm.blogs.amd.com/artificial-intelligence/mlperf-inference-v6.0/README.html) [VENDOR]
  - Lambda: one GB300 compute tray delivered up to 29% more throughput on GPT-OSS-120B than four B200s, and a software-only update added up to 9% on identical B200 hardware for Llama 3.1 8B. — [Lambda](https://lambda.ai/blog/lambdas-mlperf-inference-v6.0-hardware-leap-software-maturity-research-breakthrough) [VENDOR]
  - Intel: Arc Pro B70 delivers up to 1.8× the inference performance of the Arc Pro B60. — [Intel Newsroom](https://newsroom.intel.com/artificial-intelligence/intel-delivers-ai-performance-mlperf-inference-v6-0) [VENDOR]; see also [Nebius](https://nebius.com/blog/posts/mlperf-inference-v6-0-results)

### Inferences
- **Metric definitions as used in practice:**
  - **TTFT** = queueing + prefill (+ network). It is dominated by prompt length and by scheduler contention.
  - **TPOT** = mean time per output token after the first. **ITL** (inter-token latency) is the per-gap distribution; vendors often use TPOT and ITL interchangeably, but ITL's p99 captures stalls that the TPOT mean hides.
  - **End-to-end latency** ≈ TTFT + (output_tokens − 1) × TPOT.
  - **Throughput** is quoted as either aggregate output tok/s per GPU (or per node) or requests/s. Report p50, p90 and p99 TTFT/ITL alongside throughput, because throughput can always be raised by sacrificing tail latency.
- **Worked decode lower bound (derived; hardware numbers are assumptions):** TPOT ≥ (weight bytes + KV bytes read per step) / HBM bandwidth.
  - A 70B dense model in FP8 has about 70 GB of weights. On one H100 (3.35 TB/s): 70e9 / 3.35e12 ≈ 21 ms per step, so at most about 48 tok/s per stream at batch 1.
  - At batch 64, the same weight read serves 64 tokens, so aggregate throughput approaches 64 × 48 ≈ 3,000 tok/s (minus KV-read overhead) while per-user TPOT barely changes. This is why batching is close to "free" for throughput until the system becomes compute- or KV-memory-bound.
- **FP8 doesn't move the crossover much (derived):** FP8 weights halve bytes per FLOP, so intensity is about 2·B FLOPs per byte. But H100 FP8 peak is also about 2× BF16, so the batch size where decode crosses the ridge stays roughly the same (around 300 tokens). FP8's main decode win is lower bandwidth time per step, not a different crossover point.
- **Prefill can saturate a GPU on its own (derived):** a single 2K-token prompt has intensity of about 2,000, well above the ridge. A prefill of that size can occupy the GPU by itself. This is the root cause of the prefill/decode interference that chunked prefill and disaggregation address (Section 3).

### Gaps
- No primary Artificial Analysis methodology page could be fetched. The 72-hour median and 10K-token input details are secondhand.
- No MLPerf Inference v6.1 round (normally around September) was found in results, so whether a fall-2026 round was published is unverified. The official MLCommons results tables were not retrieved; all MLPerf numbers above are vendor-reported.
- Standard definitions of TTFT/TPOT/ITL from an authoritative glossary (for example the vLLM or NVIDIA GenAI-Perf docs) were not retrieved. The definitions above are synthesized.

---

## 2. KV cache: size formula, GQA/MQA/MLA, PagedAttention, prefix caching / RadixAttention, KV offloading (LMCache, Dynamo KVBM)

### Takeaway
KV memory per token is 2 × layers × kv_heads × head_dim × bytes. It scales linearly with context and concurrency, so in practice it decides how many sequences fit on a GPU. Four lines of work shrink or stretch it:
- **Smaller per-token KV:** GQA, MQA, MLA, and FP8/NVFP4 KV quantization.
- **Less fragmentation:** PagedAttention.
- **Reuse across requests:** prefix caching / RadixAttention.
- **More capacity per GPU:** tiered offload to CPU, SSD and network storage (LMCache, Dynamo KVBM). In 2026 these tiers also serve as the transport for disaggregated serving.

### Cited Findings
- **PagedAttention / vLLM (SOSP '23) [OLDER: 2023]:** reports near-zero waste in KV cache memory, flexible KV sharing within and across requests, and **2–4× higher throughput at the same latency** compared with FasterTransformer and Orca. — [arXiv 2309.06180](https://arxiv.org/abs/2309.06180)
- **Waste in pre-paging systems [2NDARY]:**
  - Only about 20.4%–38.2% of KV-cache memory in the compared systems held actual token states (a secondhand reading of the paper's profiling). — [iThome article](https://ithelp.ithome.com.tw/articles/10409678)
  - The common shorthand "60–80% waste reduced to under 4%" appears in a personal blog, **not in the paper's abstract**. — [mohakchugh.is-a.dev](https://mohakchugh.is-a.dev/blog/paged-attention-virtual-memory-llm-kv-cache-management)
- **MLA (DeepSeek-V2) [OLDER: 2024]:** compresses keys and values into a latent vector. Compared with DeepSeek 67B, DeepSeek-V2 reduced the KV cache by **93.3%** and raised maximum generation throughput **5.76×**. The baseline is DeepSeek 67B, not a generic MHA model; some secondary sites misreport it as "vs standard MHA". — [DeepSeek-V2 paper, arXiv 2405.04434](https://arxiv.org/html/2405.04434v2); mechanism summary at [memx.app](https://memx.app/glossary/deepseek-architecture/) [2NDARY]
- **GQA/MQA:** these reduce the KV cache by sharing K/V heads, but they can lose quality relative to full MHA, which motivated MLA (as stated in the DeepSeek-V2 motivation). — [DeepSeek-V2 paper](https://arxiv.org/html/2405.04434v2)
- **Prefix caching is on by default in vLLM V1 [2026].** The vLLM-Ascend release notes state that prefix caching is enabled by default in vLLM V1 and that v0.18.0 added prefix-cache support for hybrid models. — [vLLM Ascend release notes](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/release_notes.html)
- **RadixAttention (SGLang)** stores KV for prefixes in a radix tree so that requests sharing a prefix reuse it. Secondary sources claim "up to 5× faster" on high-prefix-reuse workloads, with lower TTFT as the main benefit; gains depend on how much prefixes overlap. — [PyShine: SGLang](https://pyshine.com/SGLang-Fast-LLM-Serving-System/); [ChatForest SGLang review](https://chatforest.com/reviews/sglang-structured-generation-llm-serving/) [2NDARY]
- **SGLang now has a decode-side radix cache for PD-disaggregated deployments** (added in v0.5.x), according to ChatForest. ChatForest misdates the LMSYS large-scale EP post, so treat its details cautiously. — [ChatForest](https://chatforest.com/reviews/sglang-structured-generation-llm-serving/) [2NDARY]
- **LMCache [2026]:**
  - An open-source KV cache layer that extracts KV caches from vLLM and SGLang and stores them outside GPU memory. It supports offloading (prefix reuse across queries) and PD disaggregation (cross-engine KV transfer).
  - It was presented as an **MLSys 2026** oral/invited talk claiming up to **15× throughput** with vLLM on multi-round QA and document analysis. — [MLSys 2026: LMCache](https://mlsys.org/virtual/2026/oral/3646); [arXiv 2510.09665](https://arxiv.org/abs/2510.09665v1)
  - **CacheBlend** reuses KV for *non-prefix* chunks (useful for RAG) and recomputes a small subset of tokens to keep cross-attention correct.
  - **CacheGen** compresses KV caches for disk storage and cross-instance sharing. — [LMCache docs](https://docs.lmcache.ai); [LMCache blog (2024)](https://blog.lmcache.ai/en/2024/09/17/lmcache-turboboosting-vllm-with-7x-faster-access-to-100x-more-kv-caches/)
  - vLLM Production Stack documents LMCache-based offload to CPU or disk to raise KV-hit rates. — [vLLM production-stack KV offloading tutorial](https://docs.vllm.ai/projects/production-stack/en/vllm-stack-0.1.1/tutorials/kv_cache.html)
- **NVIDIA Dynamo KV Block Manager (KVBM) [2026]:**
  - Offloads KV to system CPU memory, local SSDs, and network-attached storage. — [Dynamo architecture doc (v0.9.1)](https://docs.nvidia.com/dynamo/v-0-9-1/design-docs/overall-architecture)
  - The v1.0.0 KVBM guide covers vLLM and TensorRT-LLM in aggregated and disaggregated modes. — [Dynamo v1.0.0 KVBM guide](https://docs.nvidia.com/dynamo/v1.0.0/user-guides/kv-cache-offloading)
  - The current component page marks Disaggregated ✅ with vLLM and TRT-LLM supported and **SGLang not supported**. An older intro page lists vLLM only. — [Dynamo KVBM component page](https://docs.nvidia.com/dynamo/components/kvbm); [older KVBM intro](https://docs.nvidia.com/dynamo/latest/architecture/kvbm_intro.html)
  - In disaggregated mode, prefill workers offload KV to CPU/disk tiers and share it with decode workers over **NIXL** (NVIDIA Inference Xfer Library). — [Vultr guide](https://docs.vultr.com/how-to-manage-kv-cache-in-nvidia-dynamo) [2NDARY]
- **Storage vendors integrate with Dynamo for context reuse** (for example VAST Data). — [VAST Data blog](https://www.vastdata.com/blog/how-nvidia-dynamo-vast-unlock-context-reuse-at-scale) [VENDOR]
- **KV cache quantization [2026]:**
  - **NVFP4 KV cache** (Blackwell) cuts KV memory by up to 50% versus FP8 and can double the context budget, with less than 1% accuracy loss on code-generation, knowledge and long-context benchmarks. Values are dequantized from NVFP4 to FP8 before attention math. **FP8 KV is already the common production baseline.** — [NVIDIA Technical Blog: NVFP4 KV cache](https://developer.nvidia.com/blog/optimizing-inference-for-long-context-and-large-batch-sizes-with-nvfp4-kv-cache/) [VENDOR]

### Inferences
- **The formula (standard MHA/GQA):** KV_bytes_per_token = 2 (K and V) × n_layers × n_kv_heads × head_dim × bytes_per_elem. Total KV = that × Σ over sequences of (prompt + generated tokens).
- **Worked example (derived).** Config is a Llama-3-70B-class model: 80 layers, 8 KV heads (GQA, 64 query heads), head_dim 128. These values are from the public model config and were not re-verified this session.

  | KV format | Per token | 8K-token sequence | 128K-token sequence |
  |---|---|---|---|
  | BF16 (2 bytes) | 2·80·8·128·2 = 327,680 B ≈ **320 KiB** | ≈ 2.5 GiB | ≈ **40 GiB** |
  | FP8 KV | ≈ 160 KiB | ≈ 1.25 GiB | ≈ 20 GiB |
  | NVFP4 KV (~4.5 bits incl. scales) | ≈ 90 KiB | ≈ 0.7 GiB | ≈ 11 GiB |
  | Same model with full MHA (64 KV heads) | ≈ 2.5 MiB (8× BF16) | ≈ 20 GiB | ≈ 320 GiB |
  | MQA (1 KV head) | ≈ 40 KiB | ≈ 0.3 GiB | ≈ 5 GiB |

  The NVFP4 row is consistent with NVIDIA's "up to 50% vs FP8".
- **MLA changes the formula.** It caches one shared latent per layer per token (plus a small decoupled RoPE key) instead of separate K and V per head, so the leading "2×" and the n_kv_heads × head_dim term are replaced by the latent width. With DeepSeek-V3-style values (512-dim latent + 64-dim RoPE key, 61 layers, BF16), that is 576 × 61 × 2 ≈ **69 KiB/token**: smaller than GQA-8 on a 70B model, despite a far larger (671B MoE) model. The config values are background knowledge, not verified in this session.
- **Capacity planning (derived):** on 2 × 80 GB GPUs (TP=2) serving 70B FP8 weights (~70 GB), roughly 70–80 GB remains for KV after activations and CUDA-graph buffers. At 320 KiB/token (BF16 KV) that is about 230–250K tokens, or about 30 concurrent 8K-context sequences. FP8 KV doubles that, which is why FP8 KV is the default lever before adding GPUs.
- **Why paging matters (derived from the cited figures):** pre-allocating max-length contiguous KV per request wastes most of the reservation through internal fragmentation (the ~20–38% utilization figure above). Fixed-size blocks (vLLM's default is 16 tokens per block, background knowledge) allocated on demand bound waste to under one block per sequence and enable copy-on-write sharing for parallel sampling and beam search.
- **Prefix caching depends on prompt layout.** Gains appear only when shared content (system prompt, tools, documents) comes *first* and is byte-identical. The same rule governs managed-API prompt caching (Section 7), and both use block or prefix hashing.
- **Hierarchy (2026 mental model):**

  | Tier | Typical access | Role |
  |---|---|---|
  | GPU HBM | ns–µs | Active KV |
  | CPU DRAM (via PCIe or NVLink-C2C on Grace) | µs | Warm prefixes |
  | Local NVMe | ~100 µs–ms | Large reusable contexts |
  | Network/object storage (VAST, Lustre, S3-class) | ms | Cross-node, cross-session reuse |

  KV offload pays off when recomputing prefill for the same prefix costs more than transferring it, which is typically true for long prefixes (thousands of tokens) and agentic or multi-turn workloads.

### Gaps
- A primary source for the exact KV formula and for vLLM's current default block size (and the V1 hybrid-allocator details for sliding-window, Mamba and hybrid models) was not retrieved.
- No measured, independent benchmark of Dynamo KVBM vs LMCache was found.
- The Dynamo docs conflict on KVBM's framework support (vLLM-only vs vLLM + TRT-LLM). The newer page is probably current, but this was not confirmed against release notes.

---

## 3. Batching & scheduling: static vs dynamic vs continuous (in-flight) batching, chunked prefill, disaggregated prefill/decode (DistServe, Dynamo, llm-d)

### Takeaway
Serving has moved from request-level batching (static/dynamic) to iteration-level continuous batching (Orca, vLLM). The next step was chunked prefill, which mixes prompt chunks with ongoing decodes so decodes don't stall. By 2026 the frontier is **disaggregated prefill/decode**: separate GPU pools (even different chip types) for each phase, connected by fast KV transfer. Dynamo 1.0, llm-d, SGLang, vLLM's KV-connector interface, and KServe's LLMInferenceService all productize it.

### Cited Findings
- **Orca, iteration-level scheduling [OLDER: 2022].** Requests can enter or exit a batch at the granularity of individual iterations. Weakness: Orca prioritizes prefills, so a long prefill occupies a full iteration and decodes of running requests wait behind it. Sarathi-Serve calls this a "generation stall" and says it can last several seconds in vLLM. — [Sarathi-Serve paper, arXiv 2403.02310](https://arxiv.org/pdf/2403.02310)
- **Sarathi-Serve, chunked prefill / stall-free batching (OSDI '24) [OLDER: 2024]:**
  - Splits each prefill into near-equal chunks and builds stall-free schedules that add new requests without pausing ongoing decodes.
  - A per-iteration prefill token budget bounds iteration latency, making it nearly independent of prompt length. Uniform iteration times also reduce pipeline-parallel bubbles.
  - Reported gains differ by version. v1: up to 2.6× capacity within SLO on one A100 for Mistral-7B and up to 6.9× for Falcon-180B on 8 A100s, versus Orca and vLLM. OSDI version: 2.6× vs vLLM, and up to 5.6× for Falcon-180B with pipeline parallelism. — [arXiv 2403.02310](https://arxiv.org/pdf/2403.02310); [OSDI '24 PDF](https://usenix.org/system/files/osdi24-agrawal.pdf)
- **Chunked prefill is now standard; research is moving to adaptive budgets.** vLLM adopted chunked prefill. P-PAS (2026) adapts the scheduling token budget online instead of using Sarathi's fixed chunk size. "Layered prefill" (2025) proposes layer-wise prefill for MoE models to avoid repeated expert-weight loads under token chunking. — [P-PAS, arXiv 2608.15171](https://arxiv.org/pdf/2608.15171) [2026]; [Layered Prefill, arXiv 2510.08055](https://arxiv.org/pdf/2510.08055)
- **DistServe [OLDER: 2024]** places prefill and decode on separate GPUs to remove interference and decouple their resource and parallelism plans. It picks parallelism per phase to meet TTFT and TPOT SLOs and places phases according to cluster bandwidth to limit KV-transfer cost. Result: 7.4× more requests, or 12.6× tighter SLOs, with over 90% of requests within SLO. — [USENIX OSDI '24](https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin)
- **SGLang PD disaggregation + large-scale expert parallelism [OLDER: May 2025]:** DeepSeek on 12 nodes × 8 H100 (96 GPUs) reached about **52.3k input and 22.3k output tok/s per node** at 2,000-token inputs. Prefill uses DeepEP "normal" mode and decode uses "low-latency" mode. SGLang's docs motivate PD disaggregation as a fix for the interference of combined prefill/decode scheduling in unified engines. — [LMSYS blog, 2025-05-05](https://lmsys.org/blog/2025-05-05-large-scale-ep/); [SGLang PD disaggregation docs](https://docs.sglang.io/docs/advanced_features/pd_disaggregation)
- **NVIDIA Dynamo 1.0 [2026]** was announced at GTC on **March 16, 2026** as production-ready open-source "inference OS" software:
  - Claims up to **7×** Blackwell inference performance. — [NVIDIA Newsroom](https://nvidianews.nvidia.com/news/dynamo-1-0) [VENDOR]
  - Components: disaggregated serving, a KV-aware router, a planner (autoscaling), KVBM, and NIXL. — [Dynamo GitHub](https://github.com/ai-dynamo/dynamo); [NVIDIA Developer Blog: Dynamo 1.0](https://developer.nvidia.com/blog/nvidia-dynamo-1-production-ready/)
- **llm-d** (Kubernetes-native distributed inference, from IBM Research, Google, Red Hat, CoreWeave and NVIDIA):
  - Release history from the blog archive [OLDER: 2025]: 0.2 "first well-lit paths" (Jul 29, 2025), 0.3 "Wider Well-Lit Paths" (Oct 10, 2025), 0.4 "SOTA Performance Across Accelerators" (Dec 2, 2025). — [llm-d blog archive](https://llm-d.ai/blog/archive)
  - KServe v0.19 release notes mention migration support to **llm-d v0.7**, implying llm-d reached v0.7 by mid-2026. — [KServe release tracker (everydev.ai)](https://www.everydev.ai/developers/kserve) [2NDARY]
  - A personal blog claims llm-d became a **CNCF sandbox** project at KubeCon EU 2026 (unverified). — [lucaberton.com](https://lucaberton.com/blog/llm-d-cncf-kubernetes-distributed-inference-2026/) [2NDARY]
- **Heterogeneous disaggregation is real in 2026:**
  - A vLLM blog post (July 14, 2026) describes vLLM prefill paired with **TileRT decode** through vLLM V1's KV-connector interface. — [vLLM blog](https://vllm.ai/blog) (via search summary)
  - Cerebras's SEC filing describes an AWS partnership where **Trainium 3 performs prefill and Cerebras CS-3 performs decode**. — [Cerebras Form 8-K (FY2026)](https://www.sec.gov/Archives/edgar/data/0002021728/000162828026044941/cbrsannouncesfinancialresu.htm)
- **KServe LLMInferenceService:** became production-ready in **v0.17 (March 13, 2026)** with KV-cache-aware routing, disaggregated prefill/decode, distributed parallelism, Envoy AI Gateway integration, and modular Helm charts. — [KServe release tracker (everydev.ai)](https://www.everydev.ai/developers/kserve) [2NDARY]; see also [Red Hat Developer, Apr 21, 2026: KServe + llm-d](https://developers.redhat.com/articles/2026/04/21/kserve-llm-d-optimized-gen-ai-inference)

### Inferences
- **Taxonomy for study:**
  - **Static batching:** a fixed batch runs to completion; short requests wait for the longest one. Worst utilization.
  - **Dynamic batching** (Triton-style): collects requests up to a size or timeout, but still runs each batch to completion. Fine for fixed-shape models such as CNNs and encoders, poor for autoregressive generation.
  - **Continuous / in-flight batching:** the scheduler re-forms the batch every decode iteration; finished sequences leave and new ones join immediately. "In-flight batching" is TensorRT-LLM's name for it.
  - **Chunked prefill:** a token budget per iteration (for example a few thousand tokens) is filled first with decodes, then with prefill chunks. This bounds ITL at some cost to TTFT for long prompts.
  - **Disaggregation:** separate prefill and decode pools, each sized and parallelized for its own bottleneck (prefill: compute, often higher TP; decode: bandwidth and KV capacity, often wide EP for MoE). KV moves over RDMA/NVLink via NIXL, LMCache or Mooncake-style transfer engines.
- **When disaggregation pays:** long prompts, strict ITL SLOs, MoE models needing wide EP, and high scale. **When it doesn't:** small deployments where KV transfer overhead and fixed pool ratios hurt. Aggregated serving with chunked prefill stays simpler there. Dynamo's planner and llm-d's "variant autoscaling" exist precisely to re-balance the prefill:decode ratio as traffic changes.
- **Why heterogeneous chips fit (derived from Section 1):** compute-dense chips suit prefill, while SRAM-heavy or very-high-bandwidth chips (Cerebras, Groq) suit decode. The AWS Trainium3 + Cerebras pairing and the Nvidia–Groq licensing deal (Section 8) both align with that split.

### Gaps
- Primary llm-d 2026 release notes (v0.5–v0.7+) could not be fetched, because llm-d.ai was unreachable.
- No independent benchmark comparing Dynamo, llm-d and SGLang PD on the same hardware was found.
- Mooncake (Kimi's KV-centric architecture) and the Mooncake transfer engine were not researched in this session.

---

## 4. Serving engines and frameworks: vLLM, SGLang, TensorRT-LLM, Triton/Dynamo, TGI (status), llama.cpp/Ollama, KServe, Ray Serve, BentoML

### Takeaway
As of October 2026, open serving is effectively a three-engine world:
- **vLLM:** the default, broadest hardware and model coverage. V1 engine; ~0.31.x release.
- **SGLang:** strongest on prefix-heavy and agentic workloads, and on large-scale MoE/EP with PD disaggregation.
- **TensorRT-LLM:** NVIDIA peak performance, now PyTorch-native; the TensorRT engine backend has been removed.

These sit under orchestration layers: NVIDIA Dynamo 1.x, llm-d, KServe, Ray Serve and BentoML. **Hugging Face TGI is in maintenance mode.** llama.cpp/Ollama own local and edge.

### Cited Findings
- **vLLM, current version [2026]:**
  - **0.31.0 released October 5, 2026** per PyPI (0.26–0.30 shipped July–September 2026), with roughly a 9-day release cadence. 0.31.0 had 717 commits from 307 contributors. — [PyPI: vllm](https://pypi.org/project/vllm/); [freedom.tech release history](https://freedom.tech/project/vllm/) [2NDARY]
  - Wikipedia lists v0.30.0 (September 22, 2026) as stable, so it lags. — [Wikipedia: vLLM](https://en.wikipedia.org/wiki/VLLM)
  - NVIDIA also ships monthly NGC vLLM containers (release notes v26.08). — [NVIDIA vLLM Release Notes PDF](https://docs.nvidia.com/deeplearning/frameworks/pdf/vLLM-Release-Notes.pdf)
- **vLLM V1 architecture:** V1 is the default (no flag needed). It splits the engine into processes connected by ZeroMQ sockets, which fixes V0's problem of Python work (scheduling, detokenization) blocking the GPU. "Model Runner V2" expanded to Llama/Mistral in about 0.23 (per a third-party tracker). — [Inside the vLLM Engine](https://rohitghumare.com/guides/inside-vllm/) [2NDARY]; [vLLM V1: what changed in 2025](https://theneuralbase.com/vllm/learn/beginner/vllm-v1-engine-what-changed-in-2025/) [2NDARY]
- **vLLM fast weight loading:** `--load-format runai_streamer` (and `runai_streamer_sharded`) loads Safetensors via the Run:ai Model Streamer. `instanttensor` enables distributed loading with pipelined prefetch and direct I/O. — [vLLM docs: load config (v0.21)](https://docs.vllm.ai/en/v0.21.0/api/vllm/config/load/)
- **SGLang:** RadixAttention prefix cache, PD disaggregation, and large-scale EP with DeepEP (Section 3). The latest release cited by a secondary source is **v0.5.11 (May 5, 2026)**; this is unverified. — [ChatForest](https://chatforest.com/reviews/sglang-structured-generation-llm-serving/) [2NDARY]; [LMSYS large-scale EP](https://lmsys.org/blog/2025-05-05-large-scale-ep/)
- **vLLM vs SGLang positioning:** both are described as "the two inference engines powering every coding agent". — [Morph: vLLM vs SGLang](https://www.morphllm.com/comparisons/vllm-vs-sglang) [2NDARY]
- **TensorRT-LLM [2026]:**
  - The **TensorRT engine backend has been removed**. **PyTorch is now the sole execution backend**, and AutoDeploy, built on it, remains. `trtllm-serve <hf_model>` works with no engine-build step. — [TensorRT-LLM migration guide: TensorRT backend removed](https://nvidia.github.io/TensorRT-LLM/legacy/tensorrt-backend-removal.html)
  - Docs exist for 1.3.0 release candidates (rc21–rc27). — [TRT-LLM 1.3.0rc27 docs](https://nvidia.github.io/TensorRT-LLM/1.3.0rc27/legacy/tensorrt-backend-removal.html)
  - TensorRT-LLM 1.0 shipped in September 2025 and made the PyTorch backend the stable default. — [aiwiki: TensorRT-LLM](https://aiwiki.ai/wiki/tensorrt-llm) [2NDARY] [OLDER: 2025]
- **NVIDIA Dynamo [2026]:**
  - 1.0 GA on March 16, 2026. Integrates natively with **LangChain, llm-d, LMCache, SGLang and vLLM**, plus TensorRT-LLM. Supported by **AWS, Azure, Google Cloud and OCI**, and by partners including Alibaba Cloud, CoreWeave, Together AI and Nebius. — [NVIDIA Newsroom](https://nvidianews.nvidia.com/news/dynamo-1-0); [NVIDIA investor release](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Enters-Production-With-Dynamo-the-Broadly-Adopted-Inference-Operating-System-for-AI-Factories/default.aspx) [VENDOR]
  - 1.0 added native video-generation model support and **ModelExpress** checkpoint restore and weight streaming over NIXL/NVLink, claiming up to **7× faster startup** for large MoE models (DeepSeek-V3 on H200). — [NVIDIA Developer Blog](https://developer.nvidia.com/blog/nvidia-dynamo-1-production-ready/) [VENDOR]
  - License: Apache 2.0 per a third-party guide. — [Digital Applied](https://www.digitalapplied.com/blog/nvidia-dynamo-1-0-open-source-inference-os-ai-factories) [2NDARY]
  - Docs for **v1.3.0** exist, including a Gateway API Inference Extension integration page, so Dynamo is at least 1.3 by October 2026. — [Dynamo v1.3.0 GAIE docs](https://docs.nvidia.com/dynamo/v1.3.0/kubernetes-deployment/request-routing/gateway-api-inference-extension/overview.md)
- **Triton Inference Server:** no evidence was found of a 2026 rename or deprecation. Secondary sources describe TRT-LLM integrating with "NVIDIA Triton Inference Server and NVIDIA Dynamo", with Dynamo as the orchestration layer above engines. — [aiwiki: TensorRT-LLM](https://aiwiki.ai/wiki/tensorrt-llm) [2NDARY]
- **Hugging Face TGI: maintenance mode.**
  - The repository README states it accepts only minor bug-fix, documentation and lightweight-maintenance PRs, and recommends **vLLM, SGLang, and local engines (llama.cpp, MLX)**, which build on `transformers` model definitions. — [TGI README mirror (trendshift)](https://trendshift.io/admin/repository/ask-ai/4188)
  - A wiki dates the change to **December 2025** and lists v3.3.7 (December 2025) as the last release; this is unconfirmed against an HF announcement. — [aiwiki: TGI](https://aiwiki.ai/wiki/huggingface_tgi) [2NDARY] [OLDER: 2025]
- **KServe:**
  - Accepted as a **CNCF incubating** project in September 2025 (19 maintainers, 300+ contributors, 30+ adopters). Integrates with llm-d through the **LLMInferenceService** CRD for disaggregated serving, prefix caching, intelligent scheduling and variant autoscaling. — [CNCF blog, Nov 11, 2025](https://www.cncf.io/blog/2025/11/11/kserve-becomes-a-cncf-incubating-project/)
  - **v0.17 (Mar 13, 2026)**: LLMInferenceService production-ready. **v0.19**: static LoRA adapters, model-name routing, graceful vLLM pod draining, llm-d v0.7 migration. **v0.20** is the current documented release. — [KServe release tracker (everydev.ai)](https://www.everydev.ai/developers/kserve); [beri.net KServe docs summary](https://www.beri.net/learning/kserve-docs) [2NDARY]
- **Ray Serve LLM vs BentoML:**
  - Ray Serve LLM adds multi-replica autoscaling, multi-model routing and an OpenAI-compatible API on top of vLLM workers ("Ray Serve + vLLM workers" is the standard production pattern). It is heavier but scales horizontally. BentoML is Python-first and easy to adopt, with OpenLLM for one-line LLM services, and is easier for single-GPU single-model deployments.
  - One unverified chart (Llama 3.1 8B on A100, May 2026) shows Ray Serve + vLLM at about 6,050 tok/s versus about 6,200 for vLLM alone, i.e. small overhead. — [Swfte: LLM serving frameworks 2026](https://www.swfte.com/blog/llm-serving-frameworks-2026-comparison); [VIPS: BentoML vs Ray Serve LLM](https://learn.engineering.vips.edu/compare/bentoml-vs-ray-serve-llm) [2NDARY]
- **llama.cpp / Ollama (edge and local):**
  - Ollama installs in minutes, needs no cluster, and runs GGUF models on the local card. Ray Serve LLM is preferable for multi-GPU or multi-node scaling, autoscaling and pipelines. — [Markaicode: Ollama vs Ray Serve LLM](https://markaicode.com/vs/ollama-vs-ray/) [2NDARY]
  - Under about 20 concurrent users on a single-GPU-sized model, llama.cpp is simpler and lower latency (single binary, no orchestration layer). — [Markaicode: llama.cpp vs Ray](https://markaicode.com/vs/llamacpp-vs-ray/) [2NDARY]
  - Ollama has about 120K GitHub stars vs about 7K for BentoML (popularity, not performance). — [Toolhalla: BentoML vs Ollama](https://toolhalla.ai/compare/bentoml-vs-ollama) [2NDARY]
  - A "vLLM vs Ollama 2026: 9× throughput gap" comparison exists but is out of date (it names vLLM v0.24 as current). — [tech-insider](https://tech-insider.org/vllm-vs-ollama-2026/) [2NDARY, stale]

### Inferences
- **Quick "strengths" matrix for the report:**

  | Engine / layer | Main strengths |
  |---|---|
  | vLLM | Broadest model and hardware support (NVIDIA, AMD, TPU, Ascend, Neuron/Trainium plugins); OpenAI-compatible server; prefix caching on by default; KV-connector API for LMCache, Dynamo NIXL and custom decode engines; fastest release cadence |
  | SGLang | RadixAttention and a structured-generation front-end; best-in-class large-scale MoE/EP + PD disaggregation recipes (DeepSeek); popular for agentic and RL-rollout workloads |
  | TensorRT-LLM | NVIDIA-tuned kernels (FP8/NVFP4, in-flight batching, spec decoding); now Hugging Face/PyTorch-native, which removes the old engine-compile friction; usually leads NVIDIA MLPerf submissions |
  | Dynamo | Engine-agnostic distributed layer (router, planner, KVBM, NIXL) for multi-node and disaggregated serving; NVIDIA's strategic "inference OS" |
  | llm-d / KServe | Kubernetes-native control planes (Gateway API Inference Extension + vLLM) for enterprises standardizing on K8s |
  | Ray Serve / BentoML | Python app-level composition, autoscaling and packaging |
  | Triton | Still relevant for multi-framework, non-LLM model serving and ensembles |
  | llama.cpp / Ollama | CPU, Apple Silicon and consumer-GPU inference with GGUF quantization; low concurrency |

- **Mark TGI as legacy** in any 2026 recommendation. Existing TGI users should migrate to vLLM or SGLang, which are HF's own recommendation.

### Gaps
- Primary vLLM 2026 blog posts and release notes could not be fetched (DNS failure), so Model Runner V2 details, V1's piecewise CUDA graphs and torch.compile, and the hybrid KV allocator are not sourced.
- The current SGLang version as of October 2026 is unverified; the last secondary data point is v0.5.11 (May 2026).
- No 2026 primary source on Triton Inference Server's status or roadmap was found.
- Baseten's Truss and Modal-style serverless GPU platforms were not covered.

---

## 5. Optimizations: quantization (INT8/FP8/INT4 AWQ-GPTQ/NVFP4/MXFP4/KV quant), FlashAttention, speculative decoding (draft, Medusa, EAGLE-3, n-gram), tensor parallelism, CUDA graphs, torch.compile

### Takeaway
On Blackwell-era hardware in 2026, the defaults are:
- **FP8 weights and activations** as the safe default, with **NVFP4** as the 4-bit format. NVFP4 is more accurate than MXFP4 because of its smaller blocks and FP8 scales.
- **FP8 KV cache**, with NVFP4 KV emerging.
- **FlashAttention-4** for Blackwell attention kernels.
- **EAGLE-3 speculative decoding** for latency-bound, low-batch traffic. Expect about 2–3× on typical chat, more on code, and much less at large batch or on unpredictable text.

### Cited Findings
- **NVFP4 vs MXFP4 formats [2026]:**
  - NVFP4 uses 16-value blocks with an E4M3 FP8 scale plus a per-tensor FP32 scale. MXFP4 uses 32-value blocks with power-of-two scales.
  - NVFP4 is more accurate but requires Blackwell.
  - In a head-to-head *pretraining* run, MXFP4 needed **36% more tokens** to reach the same loss as NVFP4. — [NVIDIA Research: Pushing Intelligence to 4-bit](https://research.nvidia.com/labs/eai/blogs/pushing-intelligence-to-4-bit/) [VENDOR]
- **NVFP4 PTQ accuracy:** quantizing **DeepSeek-R1-0528 from FP8 to NVFP4** with post-training quantization showed **≤1% accuracy degradation** on key language-modeling tasks. — NVIDIA Technical Blog ([post](https://developer.nvidia.com/blog/?p=102000); the search summary didn't isolate which NVIDIA post) [VENDOR]
- **Mixed-precision "dynamic" NVFP4:** Unsloth keeps sensitive layers in FP8 (W8A8) or BF16 and runs the rest as W4A4 NVFP4. On Qwen3.6-27B, MMLU-Pro, GPQA and AIME-2025 scores land within about 1 point of FP8 and BF16. — [Unsloth NVFP4 docs](https://unsloth.ai/docs/basics/nvfp4) [VENDOR]
- **A reported 5% MMLU gap between NVFP4 and MXFP4** appears only on a secondary site and was not verified. — [oxmaint](https://oxmaint.com/sap-integration/on-prem-ai/fp4-vs-fp8-quantization-maintenance) [2NDARY]
- **KV cache quantization:** NVFP4 KV is up to 50% smaller than FP8 KV with under 1% accuracy loss, and is dequantized to FP8 before attention. FP8 KV is already common in production. — [NVIDIA Technical Blog](https://developer.nvidia.com/blog/optimizing-inference-for-long-context-and-large-batch-sizes-with-nvfp4-kv-cache/) [VENDOR]
- **FlashAttention-4 [2026]:**
  - Paper: arXiv **2603.05451** (March 5, 2026), MLSys 2026. Authors: Zadouri, Hoehnerbach, Shah, Thakkar, Tri Dao.
  - Problem: on Blackwell, tensor-core throughput doubled while shared-memory bandwidth and exponential (MUFU) units scaled slower.
  - Techniques: a redesigned pipeline, **software-emulated exp() via polynomial approximation on FMA units**, tensor memory (TMEM), and **2-CTA MMA**.
  - Result: on B200 BF16, up to **1,605 TFLOPs/s (~71% utilization)**, **1.3× faster than cuDNN 9.13** and **2.7× faster than Triton** implementations. — [Tri Dao blog: FlashAttention-4](https://tridao.me/blog/2026/flash4/); [MLSys 2026 paper PDF](https://proceedings.mlsys.org/paper_files/paper/2026/file/ae8b0b5838ba510daff1198474e7b984-Paper-Conference.pdf); [Emergent Mind summary](https://www.emergentmind.com/papers/2603.05451)
  - Conflicts: hyper.ai gives 1,613 TFLOPs/s, and one article cites 2.4× over Triton. — [hyper.ai](https://hyper.ai/fr/papers/2603.05451); [ascii.co.uk](https://ascii.co.uk/news/article/news-20260123-e5a5676f/flashattention-4-achieves-24x-speedup-on-blackwell-gpus) [2NDARY]
- **FA-4 availability:** pip package `flash-attn-4`; reportedly integrated into cuDNN 9.14 and compatible with SGLang and vLLM. — [ascii.co.uk](https://ascii.co.uk/news/article/news-20260123-e5a5676f/flashattention-4-achieves-24x-speedup-on-blackwell-gpus) [2NDARY]; [Lambda](https://lambda.ai/blog/flashattention-4-gives-the-nvidia-blackwell-platform-its-most-optimized-attention-kernel-yet); [Together AI](https://together.ai/blog/flashattention-4)
- **EAGLE-3 design:** the draft head takes hidden states from **three intermediate target layers** (configurable via `eagle_aux_hidden_state_layer_ids`), concatenates them and fuses them through a linear projection. EAGLE-1 used only the final hidden state. — [AWS Neuron vLLM speculative decoding design](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/_sources/vllm-neuron/docs/design/speculation/speculative_decoding_design.md)
- **EAGLE-3 measured speedups:**
  - Llama-3.1-8B-Instruct with EAGLE-3 in vLLM and SGLang: about **2×** speedup, with real acceptance lengths below ideal and acceptance rates α of roughly 0.6–0.8. — [BentoML: 3× faster LLM inference with speculative decoding](https://bentoml.com/blog/3x-faster-llm-inference-with-speculative-decoding)
  - Off-the-shelf EAGLE-3 drafts give a realistic **2–3×** range. Below α ≈ 0.55, speculative decoding is net-negative on most 2026 hardware. — [PremAI: Speculative decoding 2026](https://blog.premai.io/speculative-decoding-2-3x-faster-llm-inference-2026) [2NDARY]
  - Single-GPU 8B test: **1.84× on code refactoring** but **0.99× (break-even) on general chat**, with acceptance lengths of about 2.54 (code) vs about 1.19 (chat). — [mohakchugh: EAGLE-3 test](https://mohakchugh.is-a.dev/blog/eagle-3-speculative-decoding-training-time-test) [2NDARY]
  - Optimistic claims of about 4.5 tokens per verify (4–5×) exist in tutorials and should be treated as best case. — [TraeAI EAGLE-3 in production](https://learn.traeai.com/t/ai-engineering/phases/17-infrastructure-and-production/05-eagle3-speculative-decoding) [2NDARY]
- **Expected tokens per round:** one source gives about 2.9 at α = 0.7, γ = 5 and about 3.8 at α = 0.8. — [PremAI](https://blog.premai.io/speculative-decoding-2-3x-faster-llm-inference-2026) [2NDARY]

### Inferences
- **Speculative decoding math (standard result from Leviathan et al., 2023; background, not fetched).** With per-token acceptance α and draft length γ, expected tokens per target forward pass is E = (1 − α^(γ+1)) / (1 − α).
  - α = 0.7, γ = 5 → (1 − 0.1176) / 0.3 ≈ **2.94**, matching the 2.9 above.
  - α = 0.8, γ = 5 → (1 − 0.262) / 0.2 ≈ **3.69**. The cited "3.8" is slightly high; it may assume a different γ.
  - Wall-clock speedup ≈ E / (1 + γ·c), where c is the draft's cost relative to one target step. EAGLE-style heads keep c small.
- **Why spec decoding loses at large batch (derived from Section 1):** speculation spends spare compute to cut memory-bound steps. At high batch, decode is already near the compute ridge, so verifying γ extra tokens per sequence costs real FLOPs. This explains break-even results on mixed chat and why providers enable it mainly for low-latency tiers.
- **Draft-method taxonomy:**
  - **Separate draft model:** a small LM of the same family.
  - **Medusa:** extra decoding heads on the target, verified with tree attention.
  - **EAGLE 1/2/3:** a feature-level autoregressive draft head; EAGLE-3 adds multi-layer feature fusion and training-time test.
  - **n-gram / prompt-lookup:** no model; copies spans from the prompt. Very cheap and effective for RAG, code edits and summarization with high input-output overlap.
  - **MTP heads:** native multi-token prediction heads, as in DeepSeek-V3. These are increasingly the built-in draft for MoE models.
  - The Medusa, n-gram and MTP characterizations are background knowledge, not sourced this session.
- **Quantization ladder for study:**

  | Format | Notes |
  |---|---|
  | BF16 | Reference |
  | INT8 W8A8 (SmoothQuant-style) | Ampere-era |
  | FP8 W8A8 (Hopper/Blackwell) | Near-lossless, the 2026 default |
  | INT4 weight-only (AWQ/GPTQ, W4A16) | Good for memory-bound decode on older GPUs; still dequantizes to 16-bit for the math |
  | MXFP4 (OCP microscaling; e.g. gpt-oss ships MXFP4 MoE weights, background) | Cross-vendor |
  | NVFP4 (Blackwell, W4A4) | True 4-bit tensor-core math; NVIDIA reports ≤1% loss |

  - For KV cache: FP8 by default, NVFP4 emerging.
  - Bandwidth logic: decode time scales roughly with bytes per parameter, so 16 → 8 → 4 bits gives up to about 2× and 4× decode speedups when memory-bound.
- **Tensor parallelism for inference (background).** TP shards each layer across GPUs and adds two all-reduces per transformer layer, so it needs NVLink-class bandwidth and is usually kept within a node (TP ≤ 8, or across an NVL72 domain).
  - It reduces per-GPU weight bytes, which lowers TPOT, and increases aggregate KV capacity.
  - Pipeline parallelism adds capacity across nodes at the cost of bubbles.
  - Expert parallelism (EP) is the dominant strategy for large MoE models (DeepSeek, Qwen-MoE, gpt-oss) and pairs with data-parallel attention.
- **CUDA graphs and torch.compile (background).** CUDA graphs capture the decode step's kernel sequence once per batch-size bucket and replay it, removing CPU launch overhead, which matters at small batch and short steps. vLLM V1 combines torch.compile (fusing ops such as RMSNorm+quant and activation+quant) with piecewise CUDA graphs, leaving attention outside the graph to support variable shapes.

### Gaps
- The search budget ran out before torch.compile/CUDA graphs, Medusa/n-gram and TP could be sourced; those paragraphs are background knowledge and should be verified (vLLM docs, the Medusa paper arXiv 2401.10774, the EAGLE-3 paper arXiv 2503.01840).
- No primary sources were retrieved for AWQ/GPTQ (arXiv 2306.00978 / 2210.17323), FlashAttention-2/3 (FA-3: Hopper, FP8, arXiv 2407.08608), or SmoothQuant.
- No independent (non-vendor) NVFP4 vs MXFP4 *inference* accuracy study was found.

---

## 6. Deployment patterns: autoscaling on queue depth/KV utilization, weight-loading speed, multi-LoRA serving (S-LoRA, Punica), routing (Gateway API Inference Extension), multi-region failover, edge vs cloud

### Takeaway
Production LLM serving on Kubernetes in 2026 has converged on a few patterns:
- **Routing:** an L7 gateway with the **Gateway API Inference Extension**. **InferencePool is GA (v1)**, and its Endpoint Picker routes on KV-cache utilization, queue length and prefix affinity.
- **Autoscaling:** on engine-level signals (queue depth, KV usage) rather than CPU.
- **Cold starts:** attacked with weight streaming (Run:ai Model Streamer, Dynamo ModelExpress).
- **Fine-tunes:** served as many LoRA adapters over one base model (S-LoRA/Punica lineage).

### Cited Findings
- **Gateway API Inference Extension (GAIE):**
  - Introduced in June 2025. — [Kubernetes blog, 2025-06-05](https://kubernetes.io/blog/2025/06/05/introducing-gateway-api-inference-extension/) [OLDER: 2025]
  - **InferencePool has graduated to v1 and is stable/GA (since v1.0.0).** An InferencePool is a group of model-server Pods on shared compute that acts like a Service aware of model-serving protocols, so you replace the backend Service with an InferencePool. — [GAIE: InferencePool API](https://gateway-api-inference-extension.sigs.k8s.io/api-types/inferencepool/); [GAIE API overview](https://gateway-api-inference-extension.sigs.k8s.io/concepts/api-overview)
- **Endpoint Picker (EPP):** tracks metrics such as **KV-cache utilization and queue length** to choose a replica. One EPP serves exactly one InferencePool, and an HTTPRoute may reference several InferencePools. Since **v1.5.0**, `endpointPickerRef` is optional, so pools can work without a user-managed EPP. — [GAIE InferencePool](https://gateway-api-inference-extension.sigs.k8s.io/api-types/inferencepool/)
- **Related CRDs:** `InferenceObjective` (serving objective with priority) and `InferenceModelRewrite` (model-name rewriting) per an Istio guide; not confirmed in official docs. Istio, NVIDIA Dynamo (v1.3.0) and KServe integrate GAIE. — [OneUptime: Istio GAIE](https://oneuptime.com/blog/post/2026-02-24-how-to-use-istio-gateway-api-inference-extension/markdown) [2NDARY]; [Dynamo GAIE docs](https://docs.nvidia.com/dynamo/v1.3.0/kubernetes-deployment/request-routing/gateway-api-inference-extension/overview.md)
- **Autoscaling and routing in K8s stacks:** KServe + llm-d provide "intelligent scheduling" and **variant autoscaling**. — [CNCF blog](https://www.cncf.io/blog/2025/11/11/kserve-becomes-a-cncf-incubating-project/)
- **KServe v0.19** added graceful vLLM pod draining (needed for scale-in without dropping streams) and model-name routing. — [KServe tracker](https://www.everydev.ai/developers/kserve) [2NDARY]
- **Run:ai Model Streamer:**
  - Open-source SDK that reads tensors concurrently (multi-threaded C++ backend) from local SSD, network filesystems or S3 and streams them into GPU memory. It is Safetensors-compatible, so no weight conversion is needed.
  - Significantly faster than vLLM's default HF Safetensors loader and CoreWeave Tensorizer in NVIDIA's tests. — [NVIDIA Technical Blog: Reducing cold start latency with Run:ai Model Streamer](https://developer.nvidia.com/blog/reducing-cold-start-latency-for-llm-inference-with-nvidia-runai-model-streamer) [VENDOR]
  - GKE documents `--load-format=runai_streamer` with vLLM. — [GKE docs](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/run-ai-model-streamer)
  - Azure reports reading directly from Blob Storage via `az://` URIs (May 2026). — [Azure SDK blog](https://devblogs.microsoft.com/azure-sdk/?p=3825)
- **Storage layout matters as much as the loader:** on Lustre-style filesystems a single-stripe file is capped at one storage target's bandwidth. In one 554 GiB TP16 deployment, combining `runai_streamer` with file striping cut weight load from **~76 min to ~5 min**. — [Dynamo docs: Fast Model Weight Loading](https://docs.dynamo.nvidia.com/dynamo/kubernetes/model-deployment/model-loading/fast-model-loading)
- **Dynamo ModelExpress (1.0):** checkpoint restore and weight streaming over NIXL/NVLink, claiming up to 7× faster startup for large MoE models. — [NVIDIA Developer Blog](https://developer.nvidia.com/blog/nvidia-dynamo-1-production-ready/) [VENDOR]
- **S-LoRA [OLDER: 2023/24]:**
  - Keeps all adapters in host memory and moves only the active ones to the GPU.
  - **Unified Paging** manages adapter weights of different ranks and KV cache tensors in one memory pool, with custom kernels for heterogeneous-rank batched LoRA and a tensor-parallel strategy.
  - Serves **thousands of adapters** on one or more GPUs, with **up to 4× throughput vs vLLM-naive-LoRA** and up to 30× vs HF PEFT. — [S-LoRA, arXiv 2311.03285](https://arxiv.org/abs/2311.03285v2)
- **Punica [OLDER: 2023]:** consolidates multi-tenant LoRA serving onto a few GPUs (via its SGMV batched kernel, background) to raise utilization. AWS says SageMaker LMI's LMI-Dist backend uses vLLM, which "in turn uses S-LoRA and Punica" for unmerged multi-adapter serving. — [AWS ML blog (mirror): multi-tenant LoRA serving with SageMaker](https://aihub.hkuspace.hku.hk/2024/05/21/efficient-and-cost-effective-multi-tenant-lora-serving-with-amazon-sagemaker/) [VENDOR]
- **Multi-region and residency options in managed clouds:**
  - **Azure:** Global, Data Zone (US/EU) and Regional deployment types for Standard, Provisioned and Batch. A single Global PTU reservation can cover Global deployments across regions. **Spillover** routes overflow from a saturated provisioned deployment to a standard deployment. — [Microsoft Learn: Provisioned throughput](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/provisioned-throughput)
  - **Vertex AI:** Provisioned Throughput is scoped to project + region + model + version, so it does not follow traffic to another region. — [Vertex PT docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput/measure-provisioned-throughput?hl=en)
  - **Bedrock:** cross-region inference profiles route requests across regions; inference profiles cannot front provisioned models. — [Sailor.sh: Bedrock inference options](https://sailor.sh/blog/aws-ai-practitioner-bedrock-cross-region-inference-prompt-caching-prompt-routing-distillation/) [2NDARY]
- **Edge vs cloud:** llama.cpp/Ollama fit single-machine, low-concurrency use (fewer than ~20 users, GGUF, no orchestration). Cloud stacks (Ray Serve/vLLM, K8s) fit multi-GPU, multi-model and autoscaled serving. — [Markaicode](https://markaicode.com/vs/llamacpp-vs-ray/) [2NDARY]

### Inferences
- **Autoscaling signals (synthesis).** GPU utilization is a poor signal: it reads near 100% even when lightly loaded, because decode keeps kernels busy. Better signals, roughly in order:
  1. Queue depth / waiting requests per replica (vLLM exposes running and waiting request gauges plus KV-cache usage; background knowledge, metric names unverified).
  2. KV-cache utilization; sustained >90% means preemptions are coming.
  3. TTFT and ITL p95 against SLO.

  Scale-out must account for cold start (minutes for large weights), so use weight streaming, pre-pulled images, warm pools, or "scale-to-N-minimum". In disaggregated setups, scale the prefill pool on TTFT/queue and the decode pool on ITL/KV usage; Dynamo's planner and llm-d variant autoscaling do this.
- **Routing.** Prefix-cache-aware routing (send a request to the replica that already holds its prefix's KV) combined with load-awareness (KV usage, queue) is the main K8s-native win over round-robin. It is the core idea behind the GAIE EPP, the Dynamo KV router, SGLang's router and llm-d's inference scheduler.
- **Multi-LoRA (background):** current engines (vLLM, SGLang, TRT-LLM) batch requests for different adapters together, which works when adapters share a base model and rank limits. Model-name routing (KServe v0.19, GAIE `InferenceModelRewrite`) maps the API `model` field to base + adapter.
- **Multi-region failover with managed APIs:** combine (a) the provider's global or cross-region routing (Bedrock cross-region profiles, Azure Global/Data Zone, Vertex `global` endpoint), (b) PT plus spillover to on-demand, and (c) app-level fallback across providers or models. Note that prompt caches are model- and region-scoped, so failover costs cache hits.

### Gaps
- The search budget ran out before autoscaling-metric specifics (vLLM metric names, KEDA/HPA recipes, Dynamo planner algorithm) could be sourced.
- No benchmark comparing Run:ai Streamer, fastsafetensors and ModelExpress load times was found.
- The current upstream vLLM LoRA implementation's relationship to the Punica kernels is asserted only by AWS (2024).

---

## 7. Managed model APIs: Bedrock, Vertex AI, Azure AI Foundry / Azure OpenAI, Anthropic Claude API, OpenAI API; provisioned vs on-demand; batch (~50%); prompt caching; self-host vs API break-even

### Takeaway
Every major platform now offers the same four levers:
1. **On-demand / standard** per-token pricing.
2. A **cheaper asynchronous tier**: Batch at about 50% off within 24 h (Anthropic, OpenAI, Bedrock, Vertex, Azure), plus "Flex" tiers at batch-like prices.
3. **Premium latency or capacity**: Priority/Fast tiers, or provisioned throughput (PTUs on Azure, GSUs on Vertex, model units on Bedrock).
4. **Prompt caching** with cache reads at about 10% of input price (lower on some 2026 Anthropic models) and a write premium.

Self-hosting beats APIs only at sustained high utilization and volume, or when data-control requirements force it.

### Cited Findings
**Anthropic Claude API [2026]** (Anthropic `claude-api` skill reference, cached 2026-10-06, mirroring the [Anthropic pricing docs](https://platform.claude.com/docs/en/about-claude/pricing), [prompt-caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) and [models overview](https://platform.claude.com/docs/en/about-claude/models/overview)):
- **Per-MTok prices (input / output):**

  | Model | Input | Output |
  |---|---|---|
  | Claude Fable 5.1 / Fable 5 (most capable; Mythos 5.1 is Project Glasswing only) | $10 | $50 |
  | **Claude Opus 5.5** (current Opus) | $4 | $20 |
  | Opus 5 / 4.8 / 4.7 / 4.6 | $5 | $25 |
  | **Sonnet 5.5** / Sonnet 5 | $2 | $10 |
  | Sonnet 4.6 | $3 | $15 |
  | **Haiku 5.5** (prompts ≤100K tokens) | $0.10 | $0.50 |
  | Haiku 5.5 (prompts >100K tokens) | $0.50 | $2.50 |
  | Haiku 4.5 | $1 | $5 |

  Most current models have 1M-token context; Haiku 4.5 has 200K.
- **Batch API (Message Batches): 50% of standard cost**, asynchronous; results are returned in arbitrary order keyed by `custom_id`.
- **Prompt caching:**
  - Cache **writes** cost 1.25× base input for the 5-minute TTL (default) and 2× for the 1-hour TTL.
  - Cache **reads** cost about 0.1× base input on most models, **0.05× on Opus 5.5 ($0.20/MTok)** and **0.025× on Fable 5.1 ($0.25/MTok)**.
  - Break-even: two requests for the 5-minute TTL (1.25 + 0.1 = 1.35 vs 2.0 uncached); three for the 1-hour TTL (2 + 0.2 = 2.2 vs 3.0).
  - A read refreshes the TTL for free, and TTL counts from request *start*. Up to 4 breakpoints; minimum cacheable prefix is 512–4,096 tokens depending on the model.
  - Cache reads do **not count toward input-token rate limits** on most models.
- **Fast mode** (research preview; Claude API only; Opus 5 / Opus 5.5 / Opus 4.8): up to **2.5× higher output tokens/s** at premium prices. On Opus 5.5 that is $8 / $40, i.e. 2× standard. It is not available with Batch or Priority Tier.
- **Priority Tier** is supported on Fable 5, Opus 4.8 and older models, but **not** on Opus 5.5, Opus 5, Sonnet 5 / 5.5, Fable 5.1 or Mythos.
- **Data residency:** `inference_geo` request parameter (e.g. `"us"`), billed as a price modifier.
- **Platforms:** Claude on **Microsoft Foundry** is billed at standard first-party API rates via Microsoft Marketplace. **Bedrock and Vertex AI** are partner-operated with separate pricing. "Claude Platform on AWS" is Anthropic-operated with same-day API parity.

**OpenAI API [2026]:**
- **Batch API:** jobs that complete within 24 h are billed at half the synchronous rate. — [CloudZero: OpenAI pricing 2026](https://www.cloudzero.com/blog/openai-pricing/); [Creuto: Batch vs Flex](https://creuto.com/openai-batch-api-vs-flex-processing) [2NDARY]
- **Flex processing:** a *synchronous* lower-priority tier priced at Batch API rates, with prompt-caching discounts on top. Still beta with limited model availability. It can return 429 when capacity is unavailable, and those requests are not charged. — [OpenAI docs: Flex processing](https://developers.openai.com/api/docs/guides/flex-processing); [Creuto](https://creuto.com/openai-batch-api-vs-flex-processing)
- **Priority / "Fast mode":** sources conflict. One says Fast mode replaced Priority Processing at 2.5× speed for 2× price; another describes Priority as about 2× cost. — [Silicon Data](https://www.silicondata.com/use-cases/openai-api-pricing-per-1m-tokens); [BenchLM](https://benchlm.ai/openai/api-pricing) [2NDARY, conflicting]
- **Cached input:** about a 90% discount on most models. One source lists GPT-6.1 Sol cache reads at 5% of input and GPT-6 Astra/Luna and GPT-5.4–5.6 at 10%. — [CloudZero](https://www.cloudzero.com/blog/openai-pricing/); [CostGoat (Oct 2026)](https://costgoat.com/pricing/openai-api) [2NDARY]
- **Model prices conflict:** GPT-5.6 Sol is listed at $4 / $20 per MTok as promotional pricing "at least through 21 November 2026" in some sources, and at $5 / $30 standard in another. — [Credit for Startups](https://creditforstartups.com/pricing/openai-api-pricing); [Silicon Data](https://www.silicondata.com/use-cases/openai-api-pricing-per-1m-tokens) [2NDARY, conflicting]

**Amazon Bedrock [2026]** (mostly third-party sources; verify on the AWS pricing page):
- **Batch inference:** about 50% off on-demand for supported models, asynchronous within 24 h. Not available for Provisioned Throughput models; reportedly no tool calling, structured output or multi-turn in batch. — [Caylent](https://caylent.com/blog/amazon-bedrock-pricing-explained); [CloudForecast](https://www.cloudforecast.io/blog/aws-bedrock-pricing/); [Wring](https://wring.co/blog/aws-bedrock-pricing-guide) [2NDARY]
- **Service tiers:** one source describes **Reserved, Priority, Standard and Flex** selected via a `service_tier` parameter, with Flex at about 50% off for supported models (unverified). — [Sailor.sh](https://sailor.sh/blog/aws-ai-practitioner-bedrock-cross-region-inference-prompt-caching-prompt-routing-distillation/); [Flexprice](https://flexprice.io/pricing-index/aws-bedrock) [2NDARY]
- **Provisioned Throughput:** hourly per **model unit**, with no-commitment, 1-month and 6-month terms. Discounts are cited as about 15%, 20% and 35% off on-demand by one source, while another says many models are quote-only via the AWS account team. — [Avahi](https://avahi.ai/blog/aws-bedrock-pricing/); [CloudForecast](https://www.cloudforecast.io/blog/aws-bedrock-pricing/) [2NDARY, conflicting]
- **Prompt caching:** reads up to 90% off; writes cost more than standard input (one source: a 25% premium and a 5-minute default TTL). — [Caylent](https://caylent.com/blog/amazon-bedrock-pricing-explained) [2NDARY]

**Google Vertex AI [2026]:**
- **Provisioned Throughput** is purchased in **GSUs**. Each model publishes burndown rates that convert input, output and modalities into GSU consumption. PT is bound to project + region + model + version. — [Vertex AI: Calculate PT requirements](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput/measure-provisioned-throughput?hl=en)
- Requests beyond PT quota spill over to on-demand by default. — [nOps](https://www.nops.io/blog/gcp-provisioned-throughput/) [2NDARY]
- **Context caching:** **implicit caching is on by default** with a **90% discount** on cached tokens. **Explicit caching** gives 90% off on Gemini 2.5+ (75% on Gemini 2.0) plus a storage charge. — [Vertex AI: Context cache overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview)
- **Batch prediction:** about 50% off online. Batch and cache discounts **don't stack**; the cache-hit discount takes precedence. — [nOps cost guide](https://www.nops.io/blog/vertex-ai-cost-optimization-guide/) [2NDARY]
- Model Garden hosts first-party Gemini, partner models (Claude) and open models. Claude on Vertex is partner-priced (see the Anthropic section above).

**Azure AI Foundry / Azure OpenAI [2026]:**
- **Deployment types:** **Standard** (per-token, no latency SLA), **Priority processing**, **Provisioned** (per PTU-hour, with a per-model latency target) and **Batch**. — [Microsoft Learn: Provisioned throughput](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/provisioned-throughput)
- **Batch:** 24-hour turnaround at up to 50% less than Global Standard. — [Azure blog](https://azure.microsoft.com/en-us/blog/?p=41803)
- **PTU SKUs:** `GlobalProvisionedManaged`, `DataZoneProvisionedManaged`, `ProvisionedManaged`. For gpt-4o-class models, Global/Data Zone deployments start at a 15-PTU minimum in increments of 5 (newer models may differ). Spillover to Standard is available. Reservations must match the deployment type, and deleting a deployment doesn't cancel its reservation. — [Microsoft Learn: PT sizing](https://learn.microsoft.com/en-my/Azure/foundry/openai/how-to/provisioned-throughput-sizing); [Microsoft Learn: PT concepts](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/provisioned-throughput)

**Self-host vs API break-even [2026]:**
- **Simple formula:** break-even tokens/month = monthly GPU cost ÷ blended API price per token. One practitioner computes about 82M tokens/month against GPT-5.6 Sol and about 96M against Claude Opus 5, and says most teams should stay on APIs. — [HatchWorks: How to deploy an LLM](https://hatchworks.com/blog/gen-ai/how-to-deploy-an-llm/) [2NDARY]
- **A higher estimate:** about 256M tokens/month against GPT-5.4 for one A100 running a 70B model, with the caveat that this compares models of different quality. Against budget APIs (e.g. DeepSeek V4), break-even is in the *billions* of tokens per month. — [Marka: Self-hosted vs API 2026](https://www.marka.net.ua/news/self-hosted-llm-vs-api-the-real-cost-and-security-trade-offs-for-enterprise-in-2026/) [2NDARY]
- **Utilization is the key variable.** Self-hosted cost per token falls with achieved throughput, while API cost is roughly linear. Measured production GPU utilization is commonly below 60% and sometimes below 50%. — [IntuitionLabs: Hosted API vs self-hosted cost](https://intuitionlabs.ai/articles/hosted-ai-api-vs-self-hosted-llm-cost) [2NDARY]
- **Hidden costs:** about $145K/year per MLOps engineer, with teams underestimating by about 60% (one source); about $275K/year fully loaded for a GPU-infrastructure engineer (another). Compliance (healthcare, finance, legal) can override cost. — [Netzstrategen](https://ai.netzstrategen.com/en/insights/self-hosting-llm-costs-guide/); [IBL.ai](https://ibl.ai/resources/comparisons/api-inference-vs-self-hosted-gpu.md); [GMI Cloud](https://www.gmicloud.ai/en/blog/open-source-vs-proprietary-llm-cost) [2NDARY]
- **A primary-research case study exists:** "Inference Economics of Enterprise Coding Agents: Cloud vs On-Premise LLMs" (arXiv 2607.13080, 2026). It was not read. — [arXiv 2607.13080](https://arxiv.org/pdf/2607.13080)

### Inferences
- **Effective-price stacking (derived from Anthropic figures):** for an agent loop on Opus 5.5 with a 50K-token stable prefix and 2K new tokens per turn:
  - Uncached input per turn: 52K × $4/MTok ≈ $0.208.
  - Cached: 50K × $0.20 + 2K × $4 ≈ $0.018, about **11× cheaper on input**.
  - Batch halves base rates further. Whether caching multipliers apply on top of batch pricing (Anthropic documents that they do stack) was not re-verified this session; Vertex says its batch and cache discounts *don't* stack.
- **Self-host cost-per-token formula (illustrative; assumptions are mine, not sourced):** $/MTok = (node $/hr) ÷ (sustained tok/s × 3,600 × utilization) × 10⁶.
  - An 8-GPU node at an assumed $25/hr sustaining 20,000 output tok/s at 50% average utilization gives 36M tok/hr and about **$0.69/MTok**.
  - At 15% utilization (spiky internal traffic) it is about $2.30/MTok, which is above several hosted open-model prices.
  - Conclusion: self-hosting wins with (a) steady high-volume traffic, (b) an open-weight model that is "good enough", (c) batch-friendly or long-prefix-reuse workloads, or (d) hard data-sovereignty needs. APIs win for frontier closed models, spiky traffic and small teams.
- **Provisioned vs on-demand rule:** buy PT/PTU/GSU only for a predictable baseline with latency SLAs, and let on-demand or spillover absorb peaks. PT is region-pinned, which constrains multi-region failover.

### Gaps
- Official AWS Bedrock pricing and service-tier pages, the official OpenAI pricing page, and Google's Gemini price list could not be fetched. Bedrock and OpenAI figures are third-party and partly conflicting.
- Whether Anthropic's batch discount stacks with cache pricing was not confirmed in this session's sources.
- No primary Bedrock doc confirmed the Reserved / Priority / Standard / Flex service-tier naming.

---

## 8. Inference providers: Together, Fireworks, Groq, Cerebras, Baseten, etc.

### Takeaway
The "neocloud / inference API" market splits into:
- **GPU-based providers** (Together, Fireworks, Baseten, DeepInfra, Nebius, CoreWeave): competitive on price and breadth, increasingly running Dynamo/vLLM/SGLang stacks.
- **Custom-silicon speed specialists:** Cerebras (wafer-scale, SRAM) leads output speed at about 1,700+ tok/s on gpt-oss-120B. Groq's LPU technology was **licensed non-exclusively to NVIDIA for about $20B (December 2025)**; its founders moved to NVIDIA and GroqCloud continues independently.

### Cited Findings
- **Groq–NVIDIA deal [OLDER: Dec 2025, with 2026 developments]:**
  - Groq "entered into a non-exclusive licensing agreement with Nvidia for Groq's inference technology". The price was reported at about **$20B in cash**.
  - Jensen Huang: "we are not acquiring Groq as a company"; NVIDIA plans to integrate Groq's low-latency processors into the "AI factory" architecture.
  - Founder **Jonathan Ross** and president **Sunny Madra** joined NVIDIA. Groq continues as an independent company with former CFO **Simon Edwards as CEO**. — [CNBC, Dec 24, 2025](https://www.cnbc.com/2025/12/24/nvidia-buying-ai-chip-startup-groq-for-about-20-billion-biggest-deal.html); [GovConWire](https://www.govconwire.com/articles/groq-nvidia-ai-inference-tech-licensing-deal)
  - NVIDIA is reportedly working on an inference chip using Groq technology. — [Techzine](https://www.techzine.eu/news/devices/139180/nvidia-is-working-on-a-chip-for-ai-inferencing-with-groq-technology/)
  - **Oct 2, 2026:** a stockholder lawsuit filed in Delaware Chancery Court alleges a "lowball" price. — [CNBC, Oct 5, 2026](https://www.cnbc.com/2026/10/05/nvidia-groq-deal-stockholder-lawsuit.html)
- **Cerebras [2026]:**
  - Declined NVIDIA's approach and signed a commercial deal with **OpenAI valued at over $20B**.
  - Has an **AWS partnership: Trainium 3 for prefill, CS-3 for decode**. — [Cerebras Form 8-K](https://www.sec.gov/Archives/edgar/data/0002021728/000162828026044941/cbrsannouncesfinancialresu.htm); [TrendForce, Feb 3, 2026: OpenAI reportedly discontent with NVIDIA GPUs for inference; Groq, Cerebras gain attention](https://www.trendforce.com/news/2026/02/03/news-openai-reportedly-discontent-with-nvidia-gpus-for-inference-groq-cerebras-gain-attention/)
- **Speed benchmarks** (Artificial Analysis figures reported secondhand; the search summary didn't map each number to a specific article):
  - **Cerebras:** about **1,700 tok/s sustained** on gpt-oss-120B (AA, July 2026) vs about 3,000 claimed in Cerebras's docs; another article cites 1,753 tok/s (June 2026). It is the most expensive in that comparison at **$0.39/MTok blended** for gpt-oss-120B.
  - **GPU clouds** on the same model (June 2026): **Fireworks ~690 tok/s**, **Together AI ~564 tok/s**.
  - **Groq:** about 478 tok/s on gpt-oss-120B; on Llama 3.3 70B, figures of 322 tok/s and 297 tok/s (with about 1.01 s TTFT).
  - **Cerebras on Llama 4 Scout:** over 2,600 tok/s claimed (a different model, so not comparable).
  - Sources: [fast.io: Fastest AI 2026](https://fast.io/resources/fastest-ai-2026/); [fast.io: Best inference providers for agents](https://fast.io/resources/best-inference-providers-ai-agents/); [Kingy AI](https://kingy.ai/blog/ai-inference-providers-compared/); [Infrabase](https://infrabase.ai/blog/ai-inference-api-providers-compared); [TokenDyno](https://tokendyno.com/blog/fastest-llm-inference/); [Digital Applied Q2 2026 pricing matrix](https://www.digitalapplied.com/blog/ai-inference-providers-pricing-matrix-q2-2026); [DeepInfra blog](https://deepinfra.com/blog/best-ai-inference-platforms) [2NDARY]
- **Together AI** is a listed NVIDIA Dynamo partner, alongside CoreWeave, Nebius and Alibaba Cloud. — [NVIDIA investor release](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Enters-Production-With-Dynamo-the-Broadly-Adopted-Inference-Operating-System-for-AI-Factories/default.aspx)
- **Together AI co-published FlashAttention-4 material** (Tri Dao is associated with Together). — [Together AI blog: FlashAttention-4](https://together.ai/blog/flashattention-4)
- **Baseten** publishes an "Inference Engineering" book (cited in Section 1). No benchmark data for Baseten appeared in the provider searches. — [Baseten Inference Engineering](https://www.baseten.co/inference-engineering/book/02-models/calculating-inference-bottlenecks/)

### Inferences
- **Provider selection heuristics:**
  - Custom-silicon providers (Cerebras; Groq and its NVIDIA-integrated successors) win on single-stream output speed for interactive and agentic loops, at a price premium and with a narrower model catalog.
  - GPU providers (Together, Fireworks, Baseten, DeepInfra) win on price, breadth, fine-tune/LoRA hosting and dedicated deployments.
  - Hyperscaler-hosted open models (Bedrock, Vertex Model Garden, Azure Foundry) win on enterprise controls such as VPC, IAM, residency and committed spend.
- **Industry trajectory:** the market is converging on disaggregation and heterogeneous hardware. NVIDIA licensing Groq's tech and AWS pairing Trainium3 prefill with Cerebras decode both reflect the prefill-compute / decode-bandwidth split from Section 1.
- **Speed numbers are model-, reasoning-mode- and date-specific.** Always cite the model, date and AA methodology; the 92–1,916 tok/s spread on one model shows how much the host matters.

### Gaps
- No primary Artificial Analysis leaderboard page was retrieved; all provider speed and price figures are secondhand and should be re-checked on artificialanalysis.ai.
- No data was found on Baseten, DeepInfra, Nebius or SambaNova speeds or prices.
- NVIDIA's productization of Groq LPU tech (a chip name or timeline) was not confirmed in 2026 primary sources.
- Groq's own current GroqCloud status and pricing after the deal were not researched.
