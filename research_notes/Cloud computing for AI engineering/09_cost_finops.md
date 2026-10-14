# Cost Management (FinOps) for AI Workloads in the Cloud (state as of October 2026)

> Researched 2026-10-14. **All prices are approximate, dated, and subject to change**. Check the provider page before you budget. Many GPU-price and OpenAI/Gemini figures come from third-party aggregators or vendor blogs, because WebFetch could not resolve finops.org, openai.com, aws.amazon.com and several index sites from this environment. The web-search budget ran out before I could search FinOps-framework basics, LLM price trends, energy per prompt, anomaly detection and Kubecost/OpenCost. Those items are listed under Gaps. Where a "Source" link is a search-result page whose figure came to me through a search summary, I note that the attribution should be verified. All worked calculations are mine (Inferences). They were computed with a script from the cited prices.

---

## 1. FinOps framework basics (FinOps Foundation phases, FinOps for AI guidance, FOCUS billing spec)

### Takeaway
FinOps practice in 2026 has moved from cloud cost control toward AI and token cost management. 98% of State of FinOps 2026 respondents manage some AI spend. FOCUS (the open billing-data spec) is moving quickly: 1.3 adds contract commitments and a multi-dataset structure, 1.4 was approved in June 2026, and 1.5, targeted for December 2026, is slated to add native AI token tracking and a Price Sheet dataset. The FinOps Foundation's Unit Economics capability ranks outcome metrics (cost per assist or resolved case) above raw cost per token.

### Cited Findings
- **State of FinOps 2026:** 98% of respondents manage some form of AI spend in 2026, up from 63% the prior year. AI is the top future FinOps priority. — [Flexera FinOps X 2026 recap](https://www.flexera.com/blog/finops/finops-x-2026-recap); [EfficientlyConnected](https://www.efficientlyconnected.com/finops-expands-from-cloud-control-to-ai-era-value-leadership/)
- **FOCUS 1.3:** adds a *contract commitments* dataset and moves the spec to a *multi-dataset structure*, per the FinOps Foundation's FOCUS product manager. A February 2026 analyst briefing also flagged contract-commitment tracking as a 1.3 emphasis. — [Apptio: Scaling FOCUS Across Cloud, SaaS, and AI](https://www.apptio.com/?p=178234); [theCUBE Research](https://thecuberesearch.com/?p=320541)
- **FOCUS 1.4:** announced at FinOps X 2026 (San Diego). One recap says it was approved June 4, 2026, adding invoice reconciliation, expanded commitment data and data-integrity rules. **FOCUS 1.5** roadmap targets December 2026 with native AI token tracking and a Price Sheet dataset. — [Flexera recap](https://www.flexera.com/blog/perspectives/finops-x-2026-recap/); [Finout FinOps X 2026 recap](https://finout.io/blog/finops-x-2026-conference-recap-key-takeaways-and-product-launches). Note: the recaps disagree on conference dates (Finout says June 8–11) and on when the 1.4 approval happened. I found no official 1.3 release date or changelog.
- **Tokenomics Foundation:** the Linux Foundation, working with the FinOps Foundation, announced a sister foundation for open standards, benchmarks and best practices on AI token economics. A successor event, "Tokenomicon", is set for San Diego, June 7–10, 2027. — [TechTarget](https://www.techtarget.com/searchcio/news/366644142/linux-foundation-announces-tokenomicon-at-finops-x)
- A **FOCUS MCP Server** is available so AI agents can pull the current spec on demand. — [Finout recap](https://finout.io/blog/finops-x-2026-conference-recap-key-takeaways-and-product-launches)
- **FinOps Foundation Unit Economics capability (per secondary sources):** cost per token is a *resource-efficiency* measure. Cost per assist, per agent action or per resolved case are *outcome* measures for GenAI. — [Finout: Token Economics and TokenOps](https://www.finout.io/blog/token-economics-and-tokenops-the-definitive-guide-to-finops-for-tokens); [CloudNuro: TokenOps vs FinOps for AI](https://www.cloudnuro.ai/blog/tokenops-vs-finops-for-ai). Secondary sources; verify against finops.org.

### Inferences
- FOCUS 1.5's planned token tracking would let a single FOCUS-normalized ledger hold both GPU-hour (IaaS) charges and per-token (API) charges. Until it ships, teams need a gateway or provider usage APIs (see §6) to get token-level granularity that billing exports do not carry.
- For study purposes, the "Inform → Optimize → Operate" loop maps onto AI like this:
  - **Inform:** tag GPUs, meter tokens per team/feature, and publish unit costs.
  - **Optimize:** right-size GPUs, use commitments and spot, cache, batch, route models, trim output.
  - **Operate:** set budgets and alerts, add anomaly detection, set policy guardrails such as gateway rate and spend limits, and run an approval process for GPU reservations.

### Gaps
- I could not fetch finops.org (DNS failure) and ran out of search budget, so the following rests on my background knowledge and is **unverified this session**:
  - The FinOps Framework's three iterative phases are **Inform** (visibility, allocation, benchmarking), **Optimize** (rates and usage) and **Operate** (continuous improvement, governance).
  - The Framework has six principles, e.g. "everyone takes ownership", "a centralized team drives FinOps", "take advantage of the variable cost model".
  - FOCUS 1.0 went GA around June 2024.
  - The FinOps Foundation runs a "FinOps for AI" working group and topic pages.

  Verify all of this on finops.org before citing.
- No primary text from the FinOps for AI working group papers (e.g., its recommended AI KPIs) was retrieved.

---

## 2. GPU cost levers: utilization measurement, right-sizing, MIG/time-slicing, bin packing, idle detection, scale-to-zero; typical utilization

### Takeaway
"GPU-Util" in nvidia-smi only measures the fraction of time *any* kernel is running. It can read 100% while most SMs sit idle. Use DCGM profiling metrics instead: SM activity, SM occupancy and tensor-pipe activity. Real-world utilization is low. Vendor telemetry finds about 5% average in non-optimized Kubernetes GPU clusters, and 86% of surveyed enterprises self-report ≤50%. Idle capacity is therefore usually the biggest GPU cost lever, ahead of rate discounts.

### Cited Findings
- **nvidia-smi "GPU-Util"** = the percent of time in the last sample period during which one or more kernels was executing. One tiny kernel on one SM reads the same as a kernel filling the whole chip. — [Arthur Chiao: Understanding NVIDIA GPU Performance: Utilization vs Saturation](https://arthurchiao.art/blog/understanding-gpu-performance/); [Netdata: GPU utilization misleading](https://www.netdata.cloud/guides/nvidia-gpu/nvidia-gpu-utilization-misleading/)
- **DCGM SM activity** (`DCGM_FI_PROF_SM_ACTIVE`) = "the fraction of time at least one warp was active on a multiprocessor, averaged over all multiprocessors". Worked example: two GPUs both show `DCGM_FI_DEV_GPU_UTIL` = 100%. GPU A runs a small kernel on 2 of 16 SMs (SM activity ≈ 0.13); GPU B uses all 16 SMs. Only SM activity tells them apart. — [Arthur Chiao](https://arthurchiao.art/blog/understanding-gpu-performance/); [Last9: DCGM Exporter guide](https://last9.io/blog/dcgm-exporter)
- Recommended practice: chart `DCGM_FI_PROF_SM_ACTIVE` (or `DCGM_FI_PROF_GR_ENGINE_ACTIVE`) next to utilization, and add the **tensor pipe** metric for DL workloads. SM activity ≥ 0.8 is "necessary but not sufficient" for effective GPU use. — [Netdata: DCGM vs nvidia-smi/NVML](https://www.netdata.cloud/guides/nvidia-gpu/nvidia-gpu-dcgm-vs-nvidia-smi-nvml/); [FOSDEM 2026 "Beyond nvidia-smi" slides](https://fosdem.org/2026/events/attachments/BBYZLU-gpu-performance-monitoring/slides/267271/beyond_nv_fxjpcvs.pdf)
- The error runs both ways. High util can give false confidence about saturation. Low util can wrongly blame the GPU when host, storage or network is the bottleneck. The sample period is about 1 s on many products, so short kernels can fall between samples. — [Netdata](https://www.netdata.cloud/guides/nvidia-gpu/nvidia-gpu-utilization-misleading/); a user on the [NVIDIA dev forum](https://forums.developer.nvidia.com/t/gpu-utilization/368787) reports near-binary 0/100% swings in both nvidia-smi and DCGM field 203.
- **Typical utilization (2026):**
  - **Cast AI 2026 State of Kubernetes Optimization:** average GPU utilization ≈ **5%** across tens of thousands of non-optimized clusters on AWS, Azure and GCP. This is vendor telemetry. — [finanzen.net (syndicated VentureBeat)](https://www.finanzen.net/nachricht/aktien/5-gpu-utilization-the-401-billion-ai-infrastructure-problem-enterprises-can-t-keep-ignoring-15671084)
  - **VentureBeat Research survey,** June 2026, 573 technical leaders at firms with ≥100 employees: **86%** of enterprises running their own GPUs report **≤50%** utilization. Self-reported. — [RuntimeWire](https://runtimewire.com/article/enterprise-gpu-utilization-ai-agents-venturebeat-survey)
  - **ClearML State of AI Infrastructure at Scale 2025–26:** 44% still assign workloads to GPUs manually or have no coherent utilization strategy. Only 27% have automated resource-sharing dashboards. — [HackerNoon](https://hackernoon.com/nearly-half-of-enterprises-waste-millions-on-underutilized-gpu-capacity)
  - **Production inference:** a 22% average is cited by [CloudNuro](https://www.cloudnuro.ai/blog/gpu-utilization-benchmarks-2026). I could not trace it to a primary study, so treat it as weak.
  - HPCwire, April 2026: "Companies are racing to buy GPUs, many sit idle". — [HPCwire](https://www.hpcwire.com/aiwire/2026/04/21/companies-are-racing-to-buy-gpus-many-sit-idle)
- **MIG vs time-slicing:**
  - MIG gives hardware-enforced isolation (memory, faults, QoS), with at most **7 instances per GPU**.
  - Time-slicing packs more workloads per GPU but gives no memory, fault or security isolation.
  - The usual guidance: MIG for production multi-tenant serving; time-slicing or MPS for trusted dev and test.
  — [Platform9 GPU partitioning strategies](https://docs.platform9.com/private-cloud-director/kubernetes-clusters/cluster-lifecycle/gpu-partitioning-strategies); [ayedo: GPUs in Kubernetes, H100, MIG & time-slicing](https://ayedo.de/en/posts/gpus-in-kubernetes-praxisleitfaden-fur-h100-mig-time-slicing/); [Luca Berton 2026: MIG/MPS/time-slicing](https://lucaberton.com/blog/gpu-sharing-kubernetes-mig-mps-time-slicing-2026/)
- **H100 MIG profiles** as listed by one guide: 1g.10gb ×7; 1g.20gb ×4; 2g.20gb; 3g.40gb; 4g.40gb; 7g.80gb (full). The device plugin exposes each profile as a schedulable resource. — [ayedo](https://ayedo.de/en/posts/gpus-in-kubernetes-praxisleitfaden-fur-h100-mig-time-slicing/). **Caveat:** the max instance counts for 2g/3g/4g in that summary looked inconsistent with what I recall of NVIDIA's MIG guide (3g.40gb ×2, 4g.40gb ×1). Verify against NVIDIA docs.
- **MIG throughput is not strictly proportional to slice size,** because memory bandwidth and cache behavior differ across profiles. Benchmark on the intended profile. — [Luca Berton](https://lucaberton.com/blog/gpu-sharing-kubernetes-mig-mps-time-slicing-2026/)
- **Can you time-slice inside a MIG instance?** Amazon EKS docs say a MIG instance cannot be further time-sliced; use MPS for sharing within an instance. Another source says time-slicing can be layered inside a MIG slice. **The sources conflict**, so verify for your GPU Operator version. — [Amazon EKS: NVIDIA MIG](https://docs.aws.amazon.com/eks/latest/userguide/device-management-nvidia-mig.md)
- Do not mix MIG and time-slicing on the same physical GPU; separate them by node pool. — [ScaleOps: Kubernetes GPU sharing](https://scaleops.com/blog/kubernetes-gpu-sharing)

### Inferences
- **Effective cost per useful GPU-hour = list $/GPU-hr ÷ utilization.** At the Oct 2026 H100 index price of $3.17/hr:
  - 5% util → **$63.40** per useful GPU-hour
  - 22% → $14.41
  - 50% → $6.34
  - 80% → $3.96

  At a hyperscaler on-demand-like $6.88/hr: 5% → $137.60; 80% → $8.60. Raising utilization from 5% to 50% saves far more than any rate discount, which tops out around 2–3×.
- **Right-sizing heuristics:**
  - If a model's weights + KV cache fit in 10–20 GB (e.g., a ≤7B model at FP8/INT4 with modest concurrency), a full 80 GB H100 is oversized. A MIG 1g.10gb or 2g.20gb slice, or an L4/L40S-class card, is the cheaper unit.
  - If the job is memory-bound (decode-heavy inference), compare $/GB-HBM and $/(TB/s) rather than FLOPs.
- **Bin packing / idle detection / scale-to-zero:**
  - Alert on SM activity < ~0.1 for N minutes on an allocated GPU. That flags "allocated but idle", e.g. notebooks and stalled jobs.
  - Pack inference replicas by GPU memory rather than one pod per GPU.
  - Use KEDA/Knative-style scale-to-zero for bursty internal endpoints, accepting cold-start latency (model load time from object storage or a local NVMe cache).

  These are standard practices; specific tool docs were not retrieved this session.

### Gaps
- No primary NVIDIA DCGM field-ID documentation was fetched (the DCGM field names above come from secondary guides).
- No 2026 data was retrieved on MFU (model FLOPs utilization) for large training runs, or on cold-start times for scale-to-zero LLM endpoints.
- No primary NVIDIA MIG user-guide profile table was fetched for H100/H200/B200.

---

## 3. Purchasing: on-demand vs reserved/committed vs savings plans vs spot, capacity blocks, neocloud vs hyperscaler; current $/GPU-hour (H100/H200/B200)

### Takeaway
As of mid-October 2026, market H100 rentals cluster around **$3–4/GPU-hr**, H200 around **$5.5**, and B200 around **$6.4–8.2**. Hyperscaler on-demand and reserve-ahead prices run materially higher: AWS Capacity Blocks were raised ~20% on July 1, 2026, to **$5.19 (P5/H100), $12.36 (P6-B200) and $14.04 (P6-B300) per accelerator-hour**. Spot H100 can be 50–70% cheaper where capacity exists, but AWS rarely sells it, and interruption rates of roughly 4–20%/hr have been reported.

### Cited Findings
- **Index prices (Oct 13, 2026, settled from executed trades, Ornn Compute Price Index):**
  - H100 SXM **$3.17**/GPU-hr
  - H200 **$5.51**
  - B200 **$7.83**

  — [Ornn OCPI](https://data.ornn.com/) (figures via search summary; direct fetch failed on DNS)
- **Other 2026 indices disagree:**
  - One October 2026 index: H100 SXM median **$4.20**; B200 median **$8.19**, B200 range $6.00–$14.24. — likely [Uvik GPU Price Index 2026](https://uvik.net/blog/gpu-price-index/) (search-summary attribution; verify)
  - **Mercatus GPU Index** (Sept 2026): H100 **$3.84** average across 27 providers; B200 **$6.39** across 12 providers. — [Mercatus](https://www.mercatus-ai.com/blog/gpu-rental-prices)
  - Median H100 ≈ **$3.38/hr**, down from >$7/hr in early 2024. — [Shattered.io](https://shattered.io/h100-h200-b200-cloud-gpu-pricing-2026/)
  - Some sources say H100 prices have stopped falling and are now volatile rather than declining. — [Akash: H100 rental price Sept 2026](https://akash.network/the-bid/h100-rental-price-2026-cost-per-hour/)
- **Cheap end (Sept 22, 2026 comparison):**
  - H100 ≈ **$1.73/hr** on Vast.ai spot and **$1.99/hr** on RunPod on-demand
  - B200 ≈ **$5.98/hr** on RunPod

  — [Aliteq: H100 vs B200 rental cost 2026](https://aliteq.com/h100-vs-b200-rental-cost-2026) / [GPUaaS](https://gpuaas.com/blog/h100-vs-h200-vs-b200-which-gpu-to-rent-2026) (search-summary attribution; verify)
- **Hyperscaler on-demand:**
  - AWS p5.48xlarge ≈ **$6.88/GPU-hr**
  - Azure ND H100 v5 up to **$6.98**

  — [CloudZero: H100 GPU cost 2026](https://www.cloudzero.com/blog/h100-gpu-cost/) / [Economize cloud GPU pricing](https://www.economize.cloud/resources/gpu/pricing/) (attribution via search summary)
  - **Conflict:** another source says AWS cut on-demand H100 prices 44% in June 2025 to about **$3.90/hr**. — [Spheron: spot GPU instances 2026](https://www.spheron.network/blog/spot-gpu-instances-2026-savings-and-what-breaks/)
  - Elsewhere, H100 is quoted from about $2.69/hr (RunPod community) to about $12.29/hr (Azure). — via [IntuitionLabs](https://intuitionlabs.ai/articles/hosted-ai-api-vs-self-hosted-llm-cost)
- **AWS EC2 Capacity Blocks for ML, effective July 1, 2026, per accelerator-hour:**
  - P6-B300 **$14.04**
  - P6-B200 **$12.355**
  - P5 (H100) **$5.191** (US)
  - P5e **$5.97**
  - P5en **$6.865**
  - P4de **$2.214**

  That is about a **20%** rise across six families, following a ~15% hike on Jan 4, 2026. AWS cited supply and demand. Pricing = reservation fee (charged **up front** at booking) + OS fee. A block booked before a price change keeps the rate in effect at purchase. — [AWS Capacity Blocks pricing (Spanish mirror)](https://aws.amazon.com/es/ec2/capacityblocks/pricing/); [Converge Digest](https://convergedigest.com/?p=112071); [Spheron](https://www.spheron.network/blog/aws-capacity-blocks-pricing-2026-b200-b300-hike/); [AI Weekly](https://aiweekly.co/alerts/aws-raises-ec2-gpu-capacity-block-prices-20-from-july-1)
- **Spot / preemptible:**
  - CoreWeave HGX H100 spot ≈ **$2.46/GPU-hr** vs **$6.16** on-demand (about 60% off)
  - Nebius preemptible H100 "from $0.79" (likely a floor price)
  - GCP spot can cut H100 prices by about two-thirds, usually with capacity available; preemption warning is **30 s**
  - AWS "mostly won't sell" spot H100. One guide claims a 50% AWS spot H100 discount (Mar 2026, unclear sourcing).
  - Azure spot has the steepest listed discount, but capacity is scarce.

  — [Spheron: spot GPU 2026](https://www.spheron.network/blog/spot-gpu-instances-2026-savings-and-what-breaks/); [Thunder Compute: spot availability](https://www.thundercompute.com/blog/cloud-gpu-spot-instance-availability); [DeployBase: spot GPU pricing](https://deploybase.ai/articles/spot-gpu-pricing)
- **Spot interruption rates (conflicting, ~4× spread):**
  - AWS p5: 10–20% (Spot Advisor snapshot, May 2025)
  - Another source: 4.1%/hr for H100, with no methodology
  - RunPod H100: 8–12%/hr with a 5-minute notice

  — [Thunder Compute](https://www.thundercompute.com/blog/should-i-use-cloud-gpu-spot-instances); [Introl](https://introl.com/blog/spot-instances-preemptible-gpus-ai-cost-savings)
- One analysis argues for committing **6 months rather than 12** on reserved GPUs, given price volatility. This is based on the article title/summary only. — [BERI](https://www.beri.net/article/reserved-vs-spot-gpu-commitment-break-even-utilisation-2026)

### Inferences
- **Price ladder** (H100, Oct 2026, approximate):
  - Marketplace spot ~$1.7–2.5
  - Neocloud on-demand or index ~$2–4
  - AWS Capacity Block ~$5.19
  - Hyperscaler on-demand ~$4–7 (conflicting sources)

  B200 sells at about 2–2.5× H100's hourly rate. It is only cheaper per unit of work if it delivers >2–2.5× throughput on *your* workload.
- **Training job example:** 64 H100s × 14 days = 21,504 GPU-hours.
  - @ $3.17 (index) = **$68.2k**
  - @ $3.84 (Mercatus avg) = $82.6k
  - @ $5.191 (AWS Capacity Block) = $111.6k
  - @ $6.88 (hyperscaler OD) = $147.9k

  Spot at ~60% off index would be about $27k, before the cost of restarts and lost progress between checkpoints.
- **Commitment break-even rule:** a commitment at discount *d* beats on-demand only if expected utilization of the committed capacity exceeds (1 − *d*). For example, a 40% discount needs >60% sustained use. With H100 prices falling or volatile, shorter terms reduce the risk of being locked above market.
- **Capacity Blocks** buy *guaranteed* short-term cluster capacity (co-located, for training bursts). They are not a discount product, and the up-front charge means unused hours are sunk cost.

### Gaps
- No primary-source 2026 numbers were retrieved for AWS/GCP/Azure **Savings Plans / Reserved Instances / Committed Use Discounts** on GPU instances. Background knowledge, **unverified**: hyperscalers have historically advertised up to ~72% for multi-year compute savings plans/RIs and up to ~90% for spot.
- No primary pricing pages were fetched for CoreWeave, Lambda, Nebius, GCP A3/A4 or Azure ND (domains unresolvable from this environment).
- No GB200/GB300 NVL72 rack-level hourly pricing was found. SemiAnalysis rental-price data was not accessed (likely paywalled).

---

## 4. LLM API cost: token pricing structure, worked examples, caching, batch, routing/cascades, prompt compression, output length control

### Takeaway
API bills = Σ over token types (uncached input, cache writes, cache reads, output) × each type's rate, plus tool fees and modifiers. Output tokens cost about **5×** input on current Claude models. Cache reads cost **0.025–0.1×** input. Batch is **50% off** at Anthropic, OpenAI and Google. Anthropic's own measurements rank the levers: caching first (agent loops cost 1.7–7.3× more without it), then batch, then effort/model choice. Judge cost per **completed task**, not cost per token.

### Cited Findings
- **Anthropic list prices** (fetched 2026-10-14), $/MTok, columns: base input / 5-min cache write / 1-h cache write / cache read / output:
  - **Claude Fable 5.1:** $10 / $12.50 / $20 / **$0.25** / $50
  - **Claude Opus 5.5:** **$4** / $5 / $8 / **$0.20** / **$20**
  - **Claude Opus 5:** $5 / $6.25 / $10 / $0.50 / $25
  - **Claude Sonnet 5.5:** **$2** / $2.50 / $4 / **$0.10** / **$10**
  - **Claude Sonnet 4.6:** $3 / $3.75 / $6 / $0.30 / $15
  - **Claude Haiku 5.5 (≤100K-token prompts):** **$0.10** / $0.125 / $0.20 / $0.01 / **$0.50**
  - **Claude Haiku 5.5 (>100K-token prompts):** $0.50 / … / $2.50 output
  - **Claude Haiku 4.5:** $1 / $1.25 / $2 / $0.10 / $5

  — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing). (The Sonnet 5.5 cache read is $0.10, i.e. 0.05× input, per the live page footnote. An Anthropic SDK skill table cached 2026-10-06 said $0.20, so the live page supersedes it.)
- **Cache multipliers** (Anthropic): 5-min write = **1.25×** input, 1-h write = **2×**, read = **0.1×** (0.05× on Opus 5.5/Sonnet 5.5; 0.025× on Fable 5.1/Mythos 5.1). Caching pays off after one read for the 5-minute TTL, or two reads for the 1-hour TTL. The multipliers **stack** with the Batch discount and data-residency multipliers. — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- **Batch API** (Anthropic): **50% off** input and output. Examples: Opus 5.5 batch = $2/$10; Sonnet 5.5 = $1/$5; Haiku 5.5 = $0.05/$0.25. Results arrive within 24 h. — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing); [Anthropic cost-optimization guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence.md)
- **Other Anthropic modifiers:**
  - `inference_geo: "us"` = **1.1×** on all token types
  - Bedrock/Vertex regional or multi-region endpoints = +10% vs global
  - Fast mode on Opus 5.5 = **$8/$40** (2×)
  - Web search = **$10 per 1,000 searches** plus tokens
  - Code execution: 1,550 free hours/month, then $0.05 per container-hour
  - Managed Agents runtime: $0.08 per session-hour
  - The full 1M-token context window is billed at standard rates on Claude 4.6+ (except Haiku 5.5's >100K tier)

  — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- **Tokenizer caveat:** Claude 4.7+ models use a newer tokenizer that produces about **30% more tokens** for the same text. Compare cost per task, not list $/MTok, across model generations. — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- **Price trend inside one vendor (list prices on the same page):**
  - Haiku 4.5 $1/$5 → Haiku 5.5 $0.10/$0.50 (10× cheaper)
  - Sonnet 4.6 $3/$15 → Sonnet 5.5 $2/$10
  - Opus 5 $5/$25 → Opus 5.5 $4/$20

  Sonnet 5's $2/$10 "introductory" price became the standard price; the scheduled Sept 1, 2026 rise to $3/$15 was cancelled. — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- **OpenAI** (aggregators only; they conflict):
  - GPT-5.6 "Sol" **$5/$30**, "Terra" $2.50/$15, "Luna" $1/$6 — [BenchLM](https://benchlm.ai/openai/api-pricing)
  - GPT-5.6 Sol at $4 input / $0.40 cached / $20 output, marked *promotional through Nov 21, 2026* — [Flexprice](https://flexprice.io/pricing-index/openai-api) or [LMMarketCap](https://www.lmmarketcap.com/openai-api-pricing)
  - GPT-5.5 $5 / $0.50 cached / $30 — [Puter](https://developer.puter.com/tutorials/openai-api-pricing/)
  - Cached input = **10%** of standard; Batch API = **50%** off; crossing the long-context threshold reportedly **doubles input and adds 50% to output**

  — same aggregators. Verify all OpenAI figures on openai.com/api/pricing (unreachable from here).
- **Google Gemini** (aggregators; conflicting):
  - Gemini 3.1 Pro: $2/$12 per MTok for ≤200K-token prompts, $4/$18 above — [MorphLLM](https://www.morphllm.com/gemini-api-pricing). Another source (Sept 2026) says $2.50/$15 — [AnotherWrapper](https://anotherwrapper.com/llm-pricing/gemini-3.1-pro-preview).
  - Gemini 2.5 Flash $0.30/$2.50; 2.5 Flash-Lite $0.10/$0.40; 3.1 Flash-Lite $0.25/$1.50
  - Batch = **50%** of interactive rates, ≤24 h turnaround
  - Context caching example: cached input about $0.20/MTok for a 3.1-Pro-class model, plus explicit-cache **storage ≈ $4.50 per MTok-hour** (unverified)

  — [MorphLLM](https://www.morphllm.com/gemini-api-pricing); [mem0](https://mem0.ai/library/llms-and-models/gemini-api-pricing)
- **Anthropic measured levers** (internal, directional; [cost-optimization guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence.md)):
  - **Caching**
    - Over a day of real traffic, agent loops read a **median 84%** of input from cache, and the top decile reads ≥94%.
    - Running without caching costs **3.3×** (Opus 5.5, SWE-bench Pro), **3.1×** (Sonnet 5.5), **1.7×** (Haiku 5.5, Managed Agents tasks), and **7.3×** (Sonnet 5.5 bug-triage agent).
    - DeepResearch Bench II, per task: Fable 5.1 $37.94 → **$6.89** with caching.
    - One broken cache turn on a 100K-token prefix costs $0.50 vs a $0.02 read on Opus 5.5 (25×).
    - With turns seconds apart, the 5-min TTL is 15–19% cheaper than the 1-h TTL. When 1 in 10 turns comes after a pause, the 5-min TTL costs 54% more.
  - **Batch:** 50% off every token, including cached tokens. Called "the second-largest free lever after caching".
  - **Effort, SWE-bench Pro subset, cost per solved task:**
    - Sonnet 5.5 at `high`: 87.6% solved, **$0.11**
    - Opus 5.5 at `low`: 87.4%, $0.12
    - Opus 5.5 at `medium`: 92.8%, $0.22
    - Fable 5.1 at `high`: 92.3%, $1.19
    - Opus 5.5 cost per task by effort: low $0.11 / medium $0.21 / high $0.29 / xhigh $0.74
  - **Re-run failures at higher effort:** run everything at `low`, re-run only the failures at `high`. This gives about 97% solved at about **$0.17/task**, vs 95.3% at $0.29 for all-`high` (**~40% cheaper**). It needs a reliable failure signal such as tests.
  - **Model choice:** Haiku 5.5 reaches 85% vs 91% on GPQA Diamond at about **1/20** of Opus 5.5's cost per correct answer (about 1/10 of Sonnet 5.5's). Generation upgrades cut cost per solved task: Sonnet 5→5.5 **−87%**, Opus 5→5.5 **−78%**, Haiku 4.5→5.5 **−84%**. Counterexample: Fable 5.1 cost **+46%** per task vs Fable 5 on DeepResearch Bench II.
  - **Output control:**
    - Output costs 5× input.
    - Format matters: one-line answer $0.49/run vs six-section memo $1.40/run at similar accuracy (78–85%).
    - **Too-low `max_tokens` backfires.** Opus 5.5 at 16,384: 25% of attempts capped, 57.6% solved. At 64,000: 75.6% solved, at the same $5.38 per solved task.
  - **Input trimming:**
    - Tool search with 500 tools attached: −45% ($1.02 → $0.56 per run)
    - Data files via code execution instead of pasting into the prompt: $5.01 → $0.40, with accuracy rising from 7/25 to 25/25 (−92%)
    - Pruning stale tool results: −39% on long runs
    - Prompt audit: −14%
  - **Multi-model:**
    - Advisor/escalation: about **2.1×** executor cost for +1.7 points (within noise).
    - Orchestrator delegation: about half the cost of Fable 5.1 alone, but 10–12 points lower.
    - Recommended order: caching & trimming → batch → prompt audit → effort tuning / re-run failures / model upgrade → multi-model last.
- **Cascades forfeit cache reuse.** Prompt caches are per-model, so a multi-model cascade gives up cross-model cache hits. Anthropic advises first measuring the single best model at lower effort before building one. — [Anthropic cost-optimization guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence.md)
- **Routing via gateway:** the most common industry lever is to send simple tasks to cheaper models and reserve expensive models for complex reasoning, usually enforced at an LLM gateway. — [CloudNuro](https://www.cloudnuro.ai/blog/tokenops-vs-finops-for-ai) (vendor)

### Inferences
**Core formula, per request:**
`cost = (U_in × p_in) + (W_5m × 1.25·p_in) + (W_1h × 2·p_in) + (R × r·p_in) + (O × p_out) + tool_fees`, then × batch (0.5) × geo (1.1) where they apply.
- U_in = uncached input tokens; W = cache-write tokens; R = cache-read tokens; *r* = the model's cache-read multiplier; O = output tokens (including thinking tokens).

**Worked example A: support chatbot.** Each request has a 3,000-token cacheable system prompt + tools, 1,000 uncached tokens (history + question) and 400 output tokens. Prices per the Oct 2026 Anthropic list. Cost per request, with the cost per 1M requests in parentheses:
- **Sonnet 5.5**
  - No caching: 4,000×$2/M + 400×$10/M = **$0.0120** ($12,000)
  - Cache hit: 3,000×$0.10/M + 1,000×$2/M + 400×$10/M = **$0.0063** ($6,300; −47.5%)
  - Cache-write request: $0.0135
  - Blended by cache hit rate: 50% → $9,900; 80% → $7,740; 95% → $6,660 per 1M
- **Opus 5.5**
  - No caching: **$0.024** ($24,000)
  - Cache hit: $0.0126 ($12,600)
- **Haiku 5.5**
  - No caching: **$0.0006** ($600)
  - Cache hit: $0.00033 ($330)
- **Batch** (offline eval or backfill only): halve every figure. Sonnet 5.5 batch + cache hit ≈ **$3,150 per 1M** requests.

**Worked example B: cascade.** Send everything to Haiku 5.5 first and escalate 30% to Sonnet 5.5. The escalated requests pay twice.
- Cost = $600 + 0.3×$12,000 = **$4,200 per 1M** vs $12,000 all-Sonnet (**−65%**)
- Only worth it if (a) the escalation classifier is reliable, (b) the quality loss on the 70% is acceptable, and (c) it beats Sonnet or Opus at lower effort with caching, which the cascade forfeits across models.

**Worked example C: output trim.** Cutting the average answer from 400 to 250 tokens on Sonnet 5.5 saves 150×$10/M = $0.0015 per request = **$1,500 per 1M** requests. That is 12.5% of the uncached bill and about 24% of the cached bill. Do this with format instructions or structured output, not with a low `max_tokens` (see the truncation finding above).

**Blended $/MTok at an 80/20 input/output split:** Opus 5.5 = $7.20; Sonnet 5.5 = $3.60; Haiku 5.5 = $0.18. Real agent workloads are often >90% input, so caching dominates for them.

**Cache-hit approximation for Poisson traffic:** hit ≈ 1 − e^(−λ·TTL), where λ = requests per second sharing the prefix. For example, 1 request/min with a 5-min TTL gives about 99%; 1 request/hour gives about 8%. Better still, simulate from real timestamps. — formula from Anthropic's claude-api skill cost-optimization reference (local file `shared/cost-optimization.md`, Oct 2026; no public URL).

**Prompt compression** (e.g., LLMLingua-style token dropping) acts only on U_in. It is typically worth less than caching when the prefix is static, and is most useful for long, variable RAG context.

### Gaps
- No primary OpenAI or Google pricing page was fetched, so all OpenAI/Gemini numbers are aggregator-sourced and conflicting.
- No quantitative results were retrieved for RouteLLM or similar router papers, or for LLMLingua compression ratios vs accuracy (search budget exhausted). Background recollection, **unverified**: RouteLLM (LMSYS, 2024) reported more than 2× cost reduction at near-equal quality on some benchmarks, and LLMLingua reported up to about 20× compression.
- No a16z "LLMflation" or Epoch AI cross-vendor price-decline figures were retrieved. Background, **unverified**: a16z (Nov 2024) estimated about 10×/year decline in cost at constant capability.

---

## 5. Self-host vs API break-even: tokens per GPU-hour math, utilization assumptions

### Takeaway
Self-hosting cost per token = GPU $/hr ÷ (effective tokens/s × 3,600 × utilization). Self-hosting beats premium APIs only at high, steady volume and high utilization. It essentially never beats cheap small-model APIs (e.g., Haiku 5.5 at $0.18/MTok blended) on a single H100 running a 70B model. Hosted open-weight endpoints are often about 2× cheaper than DIY.

### Cited Findings
- **Throughput estimates (vendor):**
  - 70B FP8 on one H100 SXM5 under vLLM continuous batching ≈ **400 tokens/s ≈ 1.44M tokens per GPU-hour**. At about $2.90/hr that implies about $2.02/MTok at full utilization.
  - Llama 3.1 8B on one GPU at peak load: **6,238 tok/s**, or **8,155 tok/s** with FP8.

  — [Spheron: migrate from OpenAI API to self-hosted 2026](https://www.spheron.network/blog/migrate-from-openai-api-to-self-hosted-llms-cost-2026/); [Spheron: GPT-6 vs self-hosted](https://www.spheron.network/blog/gpt-6-vs-self-hosted-llm-2026/); [GMI Cloud: inference cost per million tokens](https://www.gmicloud.ai/en/blog/llm-inference-cost-per-million-tokens) (attribution among these via search summary)
- **Production utilization** often sits at **30–60%**, which makes per-token cost **2–3×** the peak-throughput estimate. A 40% duty cycle means real cost is about 2.5× the formula output. — [Codewave: self-hosted LLM cost](https://codewave.com/feeds/blog/self-hosted-llm-cost); [Cohorte (Sept 20, 2026)](https://cohorte.co/blog/self-hosted-llm-cost-vs-api-break-even)
- **Published break-evens:**
  - About **12M tokens/day** on one H100 vs GPT-5.4 (80/20 input/output). Against GPT-5.4-mini, a 70B model on one H100 **never** breaks even.
  - About **16M tokens/day** vs a hypothetical GPT-6 API.
  - Two H100s running gpt-oss-120b cost about **2×** a hosted provider's price for the same model, even on a business-hours schedule.

  — [Spheron](https://www.spheron.network/blog/migrate-from-openai-api-to-self-hosted-llms-cost-2026/); [Spheron GPT-6](https://www.spheron.network/blog/gpt-6-vs-self-hosted-llm-2026/); [General Compute: vLLM vs managed APIs](https://www.generalcompute.com/blog/vllm-vs-managed-inference-apis-when-to-self-host-vs-pay-as-you-go?agent=true)
- API cost scales linearly with tokens. GPU cost is fixed per hour up to the throughput ceiling, then steps up in whole GPUs. Engineering and ops costs are often undercounted. — [IntuitionLabs](https://intuitionlabs.ai/articles/hosted-ai-api-vs-self-hosted-llm-cost); [General Compute](https://www.generalcompute.com/blog/vllm-vs-managed-inference-apis-when-to-self-host-vs-pay-as-you-go?agent=true)

### Inferences
- **Formula:** `$/MTok_self = (GPU_$/hr) / (tok_per_s × 3600 × util) × 1e6`
- **Worked costs** (my calculations, using the Oct 2026 prices cited in §3):

| GPU @ price | tok/s | util 100% | util 40% |
|---|---|---|---|
| H100 @ $3.17 | 400 (70B FP8) | $2.20/MTok | $5.50 |
| H100 @ $3.17 | 2,000 (assumed high-batch 70B) | $0.44 | $1.10 |
| H100 @ $3.17 | 6,238 (8B) | $0.14 | $0.35 |
| H100 @ $5.191 (AWS CB) | 400 | $3.61 | $9.01 |
| B200 @ $7.83 | 400 | $5.44 | $13.59 |

- **Break-even volume, one H100 running 24/7 at $3.17** (fixed cost = $76.08/day; capacity at 400 tok/s = 34.6M tokens/day):
  - vs **Opus 5.5** (blended $7.20/MTok): 10.6M tok/day
  - vs **Sonnet 5.5** ($3.60/MTok): 21.1M tok/day
  - vs **Haiku 5.5** ($0.18/MTok): **423M tok/day**, which exceeds one H100's capacity. Self-hosting can never win there on GPU cost alone.

  This assumes the open 70B model matches the API model's quality on the task. If it does not, compare cost per *successful task*.
- **Caveats on the math:**
  - Prefill (input) tokens are processed far faster than decode (output) tokens. A single blended tok/s figure overstates cost for input-heavy RAG and understates it for long generations. Benchmark with your real input/output lengths and concurrency.
  - Add ops overhead: on-call, upgrades, eval, autoscaling, redundancy (N+1 replicas, which often halves effective utilization at low volume).
  - APIs also give you caching, batch discounts and model upgrades for free.
- **Where self-hosting tends to win:**
  - Steady, high-volume traffic on small or fine-tuned models
  - Strict data residency
  - Latency or throughput SLOs that APIs don't meet
  - Already-committed or owned GPUs with idle headroom (marginal cost ≈ power)

### Gaps
- No independent, methodology-transparent 2026 benchmark (e.g., MLPerf Inference v6.x tokens/s per H100/B200 for 70B-class models) was retrieved.
- The 400 tok/s figure appears low for well-batched aggregate throughput. Treat it as conservative.

---

## 6. Cost attribution: tagging, per-team/feature/customer token tracking via gateways, showback/chargeback, unit economics, budgets/alerts, anomaly detection

### Takeaway
GPU (IaaS) spend is attributed with cloud tags and labels plus Kubernetes cost allocation. Token spend lacks resource tags, so attribution comes from three places: an LLM gateway that stamps every call with team, feature and customer metadata at request time; per-project API keys or workspaces; or provider usage/cost APIs. Start with showback and move to chargeback once allocation rules are stable. Report outcome unit costs (cost per resolved ticket or per document) alongside cost per token.

### Cited Findings
- Capture usage **inline at request time** (at the gateway) before billing or analytics systems aggregate it. A normalized cross-provider ledger enables comparisons. Agent workflows complicate attribution because one user prompt can fan out into many LLM and tool calls. — [Gravitee: LLM gateway FinOps metering & chargeback](https://gravitee.io/corpus/gen-1210/ocnosispa/ocnosispa-llm-gateway-finops-usage-metering-chargeback-and-cost-allocation.html); [Gravitee: FinOps for AI agent & LLM gateway traffic](https://gravitee.io/corpus/gen-1371/outline-of-management/finops-for-ai-agent-and-llm-gateway-traffic-budgeting-chargeback-and-unit-economics.html) (vendor content)
- **Showback** reports costs without enforcing payment and builds awareness. **Chargeback** assigns cost to a cost center and creates financial responsibility. Common practice: start with showback dashboards, move to chargeback once rules settle. — [OneUptime: AI/LLM spend showback (Jul 2026)](https://oneuptime.com/blog/post/2026-07-21-ai-llm-spend-showback/view); [Binadox](https://www.binadox.com/?p=21517)
- **Allocation:** direct costs go to owners by tokens or tool calls. Shared platform overhead (gateway, vector DB, eval infrastructure) is split by an agreed key such as token share or number of active agents. Gateways attach cost-center metadata because LLM APIs often lack cloud-style tagging. — [Gravitee](https://gravitee.io/corpus/gen-1020/enterprise-optimization/finops-chargeback-and-budget-allocation-for-ai-agent-and-llm-gateway-traffic.html); [CloudNuro](https://www.cloudnuro.ai/blog/tokenops-vs-finops-for-ai)
- **Unit metrics:** cost per resolved ticket and cost per document summarized are typical outcome metrics. Cost per token is an efficiency metric. — [Finout: TokenOps guide](https://www.finout.io/blog/token-economics-and-tokenops-the-definitive-guide-to-finops-for-tokens); [Microland: FinOps for AI part 2](https://www.microland.com/blogs/finops-for-ai-part-2)
- **Provider-side metering (Anthropic Usage & Cost Admin API):**
  - Needs an Admin API key.
  - `GET /v1/organizations/usage_report/messages` can `group_by` model, `api_key_id`, `workspace_id`, `service_tier` and `context_window`. It returns `uncached_input_tokens`, `cache_read_input_tokens`, `cache_creation` (5m/1h) and `output_tokens`.
  - `GET /v1/organizations/cost_report` returns daily USD and can group by description (model, cost_type, token_type, service_tier) or by workspace. It cannot filter by API key.
  - Data appears about 5 minutes after a request. Bedrock, Vertex and Foundry traffic is *not* included.
  - Recommendation: give each project its own API key or workspace so spend can be attributed.

  — [Anthropic Usage & Cost API docs](https://platform.claude.com/docs/en/manage-claude/usage-cost-api.md) (details taken from Anthropic's claude-api skill reference summarizing that page; the page itself was not fetched this session)

### Inferences
- **Minimum metadata on every LLM call** (gateway headers or logs): `team`, `feature/route`, `customer/tenant_id`, `environment`, `model`, `request_id/trace_id`, plus the four token counts and `cost_usd` computed at log time from a versioned price table.
  - Join on trace_id to roll agent fan-out up to "cost per conversation" or "cost per task".
- **Unit economics example** (Sonnet 5.5, example A in §4): a support conversation averages 6 turns, and the cached prefix makes most input cheap. Cost ≈ 6 × ~$0.0063–0.0135 ≈ **$0.04–0.08 per conversation**, before history growth. If 70% of conversations resolve without a human, cost per *resolved* ticket ≈ $0.06–0.11 in LLM cost. Compare that with human handling cost to show value.
- **Budgets and alerts:**
  - Set monthly budgets per workspace or key, with alerts at 50/80/100%.
  - Set hard caps at the gateway (spend or rate limits per key or team) to stop runaway agents.
- **Anomaly detection:** watch daily cost per feature against a trailing baseline, e.g. alert when it exceeds μ + 3σ or rises >X% day-over-day. Also watch a sudden drop in `cache_read/total_input`: a "silent cache invalidation" from a timestamp in the system prompt can multiply input cost several-fold overnight (see the 25–50× miss vs hit ratio in §4).
- **GPU attribution in Kubernetes:** label namespaces and pods (team, project), and use OpenCost or Kubecost-style allocation where idle GPU cost is either shared out or charged to the owning team. Charging idle to owners creates the incentive to release GPUs.

### Gaps
- No sourced details were retrieved on AWS Cost Anomaly Detection, AWS Budgets, GCP/Azure budget alerts, or OpenCost/Kubecost GPU and idle-cost allocation (search budget exhausted).
- No specific gateway product docs were retrieved (e.g., LiteLLM, Portkey, Kong AI Gateway, Cloudflare AI Gateway) covering per-team budgets.

---

## 7. Storage and network costs relevant to AI: egress, cross-AZ transfer, checkpoint storage lifecycle

### Takeaway
Within AWS, cross-AZ traffic is billed **$0.01/GB in each direction (≈$0.02/GB effective)**. That makes frequent checkpointing or data loading across AZs a hidden line item. Keep GPUs, data and checkpoint targets in the same AZ, and lifecycle old checkpoints to cheaper tiers or delete them.

### Cited Findings
- **AWS cross-AZ:** $0.01/GB charged on *both* sending and receiving sides, so about **$0.02/GB** effective. One author's tests matched the two-sided charge on the bill. — [Last Week in AWS](https://www.lastweekinaws.com/blog/aws-cross-az-data-transfer-costs-more-than-aws-says); [mkdev](https://mkdev.me/posts/understanding-aws-data-transfer-costs)
- 1 TB/day of cross-AZ reads ≈ **$7,300/year** from that pattern alone. — [Wring: AWS data transfer pricing guide](https://wring.co/blog/aws-data-transfer-pricing-guide) (attribution via search summary)
- **Inter-region:** $0.02/GB per several sources; another gives a $0.02–0.09/GB range. **The sources conflict.** — [Redress Compliance](https://redresscompliance.com/aws-data-transfer-pricing-hidden-costs.html); [Bacancy](https://www.bacancytechnology.com/blog/aws-data-transfer-pricing)
- Data transfer is widely described as the "hidden" AWS cost. — [Security Boulevard, Jun 2026](https://securityboulevard.com/2026/06/aws-data-transfer-costs-how-to-cut-your-egress-bill-without-rebuilding-your-stack/); [Kapex](https://getkapex.ai/blog/aws-cost-optimization-data-transfer)

### Inferences
- **Checkpoint sizing rule of thumb** (assumption: mixed-precision Adam ≈ 16 bytes/param for full training state; bf16 weights = 2 bytes/param):
  - A 70B model has about **1.12 TB** of full state per checkpoint (about 140 GB weights-only).
  - Hourly checkpoints written cross-AZ: 1,120 GB × $0.02 = **$22.40 per checkpoint**, or about **$538/day**. In the same AZ, that transfer cost is $0.
  - Keeping 48 hourly full checkpoints = about 53.8 TB. At an *assumed* S3-Standard-like $0.023/GB-month (unverified this session) that is about **$1,236/month**.
  - A lifecycle policy can cut this sharply: keep the last N=3 full checkpoints, keep every 24th as weights-only, and move older ones to infrequent-access or archive tiers or expire them.
- **Egress:** serving model weights or datasets to another cloud or a neocloud incurs internet egress, often the largest network line. Mitigations:
  - Co-locate data with GPUs.
  - Use the provider's private interconnect where it is cheaper.
  - Cache datasets on local NVMe.
  - Compress and dedupe.
  - Prefer neoclouds or storage tiers with zero or low egress when data must move.
- **Multi-node training** inside one placement group or AZ avoids cross-AZ fees for gradient traffic. Never stripe a training cluster across AZs.

### Gaps
- No current S3, GCS or Azure Blob storage-class prices, lifecycle rules or internet-egress tiers were retrieved (e.g., the AWS internet egress first-tier rate). The search returned nothing on checkpoint lifecycle specifically.
- No data was retrieved on neocloud egress policies (several advertise free egress, but this was not verified).

---

## 8. Sustainability: energy/carbon of AI workloads, carbon-aware scheduling, region choice

### Takeaway
Long-running, latency-insensitive AI training is the best candidate for carbon-aware scheduling, shifting in time and across regions. However, peer-reviewed 2026 simulations show modest gains (e.g., about 4.5% carbon and about 1.7% cost reductions in one multi-park study), and popular "30–50%" claims are poorly sourced. Region choice (grid carbon intensity) is usually the bigger lever. In this session I could not retrieve per-prompt energy figures or IEA totals.

### Cited Findings
- Carbon-aware scheduling using regional carbon-intensity forecasts is "particularly well suited for long-running AI training workloads, where network latency differences are negligible compared to total execution time". — [U. Alberta PESGM 2026 paper](https://sites.ualberta.ca/~oardakan/files/PESGM26.pdf)
- A 2026 arXiv study scheduling across three AI data-center parks with continuity-constrained workloads reports at least **1.69% lower operating cost** and **4.5% lower carbon emissions** vs four alternative schemes. — [arXiv 2609.11649: From Grid to Chip](https://arxiv.org/pdf/2609.11649) (attribution between this and the next paper is via search summary; verify)
- Joint compute–power scheduling for microgrid-equipped AI data centers (MILP) "substantially improves total operational benefit" over compute-only and energy-only baselines while reducing emissions. Test instances are synthetic. — [arXiv 2605.03751 / Microsoft Research](https://arxiv.org/pdf/2605.03751)
- The Green Software Foundation publishes a pattern, "Use carbon-aware scheduling and region selection for AI workloads". Its content was not retrieved because of DNS failure. — [GSF pattern](https://patterns.greensoftware.foundation/operations/carbon-aware-ai-scheduling)
- **Weakly sourced claims to avoid:** a blog's "30–50% footprint reduction" attributed to Nature Climate Change, and "200–250 TWh/yr" for global data centers. Neither had a verifiable citation. — [is4.ai blog](https://is4.ai/blog/our-blog-1/ai-environmental-cost-sustainability-guide-2026-281); [Luca Berton](https://lucaberton.com/blog/sustainable-computing-green-infrastructure/)

### Inferences
- **Carbon estimate formula:** `kgCO2e = GPU_count × avg_power_kW × hours × PUE × grid_intensity_kgCO2e/kWh` (+ embodied emissions).
  - Example with assumed inputs: 64 H100s at about 0.7 kW each over 336 h = 15.05 MWh IT load. At PUE 1.2 that is 18.06 MWh.
  - Grid intensity is assumed and illustrative only. At about 0.05 kgCO2e/kWh (a hydro- or nuclear-heavy grid) → about **0.9 t CO2e**. At about 0.5 kgCO2e/kWh (a coal-heavy grid) → about **9 t**.
  - Region choice is a ~10× lever. Time-shifting within one grid is usually tens of percent at most.
- **Cost and carbon often align:** higher utilization (§2), caching, smaller models and batching all cut both $ and energy per task. Spot and off-peak capacity may coincide with lower-carbon hours, but not necessarily.
- **Trade-offs:** low-carbon regions may have higher GPU prices or less capacity, data-residency limits, and egress costs to move data (§7).

### Gaps
- No primary 2026 figures were retrieved for: IEA data-center electricity projections; per-prompt energy (e.g., Google's published median Gemini text-prompt energy, which I recall as about 0.24 Wh from Aug 2025, **unverified**); H100/B200 TDP; cloud provider carbon tools (AWS Customer Carbon Footprint Tool, Google Cloud Carbon Footprint, Azure Emissions Impact Dashboard); or carbon-intensity APIs (Electricity Maps, WattTime, Carbon Aware SDK). The search budget was exhausted and the GSF page was unreachable.
- The power figure (0.7 kW per H100) and the grid intensities in the example above are assumptions, not sourced values.
