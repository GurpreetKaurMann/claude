# Cloud Compute & Infrastructure for AI Engineering (state as of 14 Oct 2026)

> Research-process caveats for the report writer (read first):
> - The session's shared WebSearch budget ran out after ~14 searches. WebFetch failed with DNS errors on every domain tried, and the egress proxy blocked nvidia.com, amd.com, aws.amazon.com, docs.aws.amazon.com, learn.microsoft.com, docs.cloud.google.com, modal.com, coreweave.com and most vendor sites.
> - What I could read directly: (a) live **cloud.google.com pricing pages**, fetched 14 Oct 2026; (b) **official vendor docs in their GitHub source repos** (MicrosoftDocs/azure-compute-docs = learn.microsoft.com source; aws-neuron/aws-neuron-sdk = Neuron docs source; aws/karpenter-provider-aws; kubernetes/autoscaler; runpod/docs; modal-labs/modal-examples; jax-ml/scaling-book = Google DeepMind's "How to Scale Your Model").
> - Everything else comes from search-result summaries. Many of those are third-party aggregators (Spheron, Introl, getdeploying, etc.). They are flagged where used, and the numbers should be treated as approximate.
> - Legend: **[SHIPPING]** = generally available; **[LIMITED]** = limited or early availability; **[ANNOUNCED]** = announced but not broadly shipped; **[OLDER]** = previous generation, still widely rented.

---

## 1. Current NVIDIA and AMD data-center GPUs (memory, bandwidth, FP8/FP4, NVLink) and the cloud instance families that expose them

### Takeaway
As of October 2026:
- **The workhorses are Hopper (H100/H200) and Blackwell (B200/GB200)**, with Blackwell Ultra (B300/GB300 NVL72, 288 GB HBM3e) now broadly rentable.
- **Vera Rubin (288 GB HBM4, ~22 TB/s, NVLink 6) went into limited cloud availability at CoreWeave on 30 Sep 2026.** Hyperscaler Rubin instances are expected but not confirmed GA.
- **AMD's current cloud part is the MI355X (288 GB HBM3E, ~8 TB/s, ~10 PF dense FP4).** MI300X is still common (e.g., Azure ND MI300X v5). The MI400-series/Helios rack is announced and ramping, not broadly available.

### Cited Findings

**NVIDIA Hopper / Blackwell per-GPU specs (dense numbers)**
- Per-chip peak, from the JAX/DeepMind scaling book's GPU table (dense, no sparsity) — [How to Scale Your Model: GPUs](https://github.com/jax-ml/scaling-book/blob/main/gpus.md):

  | GPU | HBM | HBM bandwidth | BF16 | FP8 | FP4 |
  |---|---|---|---|---|---|
  | H100 | 80 GB | 3.4 TB/s | 990 TFLOPS | 2.0 PFLOPS | – |
  | H200 | 141 GB | 4.8 TB/s | 990 TFLOPS | 2.0 PFLOPS | – |
  | B200 | 192 GB | 8.0 TB/s | 2.3 PFLOPS | 4.5 PFLOPS | 9.0 PFLOPS |
  | A100 [OLDER] | 80 GB | 2.0 TB/s | 312 TFLOPS | 624 TOPS (INT8) | – |

- NVLink generations, from the same source — [scaling-book gpus.md](https://github.com/jax-ml/scaling-book/blob/main/gpus.md):
  - **NVLink 3** (Ampere): 300 GB/s per GPU, full-duplex (each direction).
  - **NVLink 4** (Hopper): 18 links × 25 GB/s = **450 GB/s per direction** (≈900 GB/s bidirectional), 8-GPU node, 4 NVSwitches.
  - **NVLink 5** (Blackwell): 18 links × 50 GB/s = **900 GB/s per direction** (≈1.8 TB/s bidirectional). The NVLink domain is 8 GPUs (HGX B200) or **72 GPUs (GB200 NVL72)**.
- Scale-out reference design: an H100 node has 8 × 400 Gbps ConnectX-7 NICs, i.e. ~400 GB/s per node into a fat-tree InfiniBand network, with full bisection bandwidth in the DGX SuperPod reference design. A Scalable Unit (SU) is 32 nodes = 256 GPUs — [scaling-book gpus.md](https://github.com/jax-ml/scaling-book/blob/main/gpus.md).
- **Inference rule of thumb from the NVLink domain sizes:** GB200 NVL72 gives 72 GPUs full 900 GB/s GPU-to-GPU bandwidth. The "node" (NVLink domain, 72 GPUs) is now distinct from the "host" (still 4 GPUs per Grace host on GB200) — [scaling-book gpus.md](https://github.com/jax-ml/scaling-book/blob/main/gpus.md).

**Blackwell Ultra (B300 / GB300 NVL72) [SHIPPING]**
- B300 per GPU:
  - **288 GB HBM3e at ~8 TB/s**, **~15 PFLOPS dense FP4** (20 PF sparse per Runpod), ~1,400 W TDP, NVLink 5 at 1.8 TB/s per GPU.
  - Dual-die, 208B transistors.
  - For comparison, these sources list B200 at 9 PF dense FP4.
  - Sources: [Spheron B300 guide](https://www.spheron.network/blog/nvidia-b300-blackwell-ultra-guide/), [Runpod B300 article](https://www.runpod.io/articles/guides/nvidia-b300), [Introl](https://introl.com/blog/nvidia-blackwell-ultra-b300-infrastructure-requirements-2025). All are secondary/vendor-reseller sources.
- GB300 NVL72 rack — [Introl](https://introl.com/blog/why-nvidia-gb300-nvl72-blackwell-ultra-matters), [Spheron GB300](https://www.spheron.network/gpu-rental/gb300/):
  - 72 B300 GPUs + 36 Grace CPUs in one NVLink domain.
  - ~20–20.7 TB HBM3e.
  - FP4 is ~1.08 EF dense / 1.44 EF sparse (another source says "1.1 EF").
  - One vendor note flags a datasheet that lists **279 GB** per GPU rather than 288 GB, so the figures are inconsistent.
- Azure confirms the B300 figures from an official doc — [MicrosoftDocs: ND GB300 v6](https://github.com/MicrosoftDocs/azure-compute-docs/blob/main/articles/virtual-machines/sizes/gpu-accelerated/nd-gb300-v6-series.md):
  - Each Standard_ND128isr_GB300_v6 VM has **4 GPUs × 288 GB**, 128 vCPUs and 864 GiB RAM.
  - Scale-up: NVLink at 1.8 TB/s, up to **72 GPUs per NVLink domain**.
  - Scale-out: **4 × 800 Gbps InfiniBand**, "to up to 100,000 GPUs".
- Timing conflict: one secondary source says NVIDIA shipped B300 in January 2026, with cloud listings within weeks — [Spheron B300](https://www.spheron.network/blog/nvidia-b300-blackwell-ultra-guide/). Not independently verified; earlier GB300 deployments may predate that.

**Vera Rubin [LIMITED → ramping]**
- Per-GPU specs from secondary sources citing CES/GTC 2026 — [Barrack.ai GTC 2026 breakdown](https://blog.barrack.ai/nvidia-rubin-specs-architecture-2026/), [VRLA Tech](https://vrlatech.com/nvidia-vera-rubin-architecture-explained/), [cyfuture](https://cyfuture.ai/nvidia-vera-rubin-gpu):
  - **288 GB HBM4** (8 stacks), **~22 TB/s**. NVIDIA raised this from an earlier 13 TB/s target.
  - **50 PFLOPS NVFP4 inference / 35 PFLOPS NVFP4 training**, roughly 5× and 3.5× B200.
  - TSMC N3, two reticle-size dies, ~336B transistors.
  - **NVLink 6: 3.6 TB/s per GPU** (2× NVLink 5).
- Rack figures — [timewell](https://timewell.jp/en/columns/nvidia-gpu), [cudocompute](https://www.cudocompute.com/?p=219):
  - The "Vera Rubin NVL72" has ~260 TB/s aggregate NVLink, ~3.6 EF NVFP4 inference and ~2.5 EF training.
  - **Naming note:** the same rack was earlier marketed as "NVL144" (counting dies, not packages) — [Wikipedia (via search)](https://en.wikipedia.org/wiki/Rubin_(microarchitecture)), [NADDOD](https://www.naddod.com/blog/nvidia-vera-rubin-nvl144-next-generation-high-performance-computing-platform).
- **Availability:** On **30 Sep 2026, CoreWeave announced Vera Rubin NVL72 in limited availability.** Cognition (Devin) is the first production customer, reporting **4.8× total token throughput vs a GB200 NVL72 baseline** (vendor/customer claim) — [CoreWeave press release](https://www.coreweave.com/news/coreweave-delivers-nvidia-vera-rubin-nvl72-performance-at-production-scale-starting-with-cognition), [DCD](https://www.datacenterdynamics.com/en/news/coreweave-makes-nvidia-vera-rubin-nvl72-available-cognition-is-early-customer/).
- NVIDIA said in July 2026 that Rubin chips had begun shipping to cloud providers. AWS, Google Cloud, Microsoft Azure and OCI were named among the first to deploy — [GCN](https://gcn.com/nvidia-vera-rubin-chips-begin-shipping/20421/).
- I found no confirmation of hyperscaler Rubin GA as of mid-October 2026. One vendor blog expects most teams won't get access until 2027 — [Spheron Rubin availability](https://www.spheron.network/blog/vera-rubin-nvl72-cloud-availability-cost-per-token/).
- Timeline conflict: Spheron says CoreWeave first ran Rubin compute on 1 Jun 2026, while DCD says Cognition began use in early September. These may be internal bring-up vs customer use.

**AMD Instinct**
- **MI300X [OLDER, still widely deployed]:** Azure Standard_ND96isr_MI300X_v5 has **8 GPUs with 1,535 GB total (~192 GB each)**, 96 vCPUs and 1,850 GiB RAM — [MicrosoftDocs: ND MI300X v5](https://github.com/MicrosoftDocs/azure-compute-docs/blob/main/articles/virtual-machines/sizes/gpu-accelerated/ndmi300xv5-series.md).
- **MI355X (CDNA 4) [SHIPPING]:** **288 GB HBM3E at ~8 TB/s**, 256 CUs, ~1,400 W board power, **~10 PF dense FP4** (10,066 TFLOPS) — [SemiAnalysis InferenceX MI355X](https://inferencex.semianalysis.com/chips/mi355x), [Spheron MI300X/MI355X pricing](https://www.spheron.network/blog/amd-mi300x-mi355x-pricing-2026/).
  - Some aggregators report 8-GPU platform totals as per-GPU figures, so ignore inflated numbers.
- MI355X availability — [Spheron](https://www.spheron.network/blog/amd-mi300x-mi355x-pricing-2026/), [getdeploying](https://getdeploying.com/gpus/amd-mi355x):
  - GA on **Oracle OCI** and **Vultr**.
  - Spot-only preview on DigitalOcean.
  - Contact-sales at TensorWave and Crusoe.
- **MI400 series / Helios rack [ANNOUNCED, early ramp]** — [Tech-Insider MI400](https://tech-insider.org/amd-mi400-series-ai-gpu-data-center-2026/), [Spheron](https://www.spheron.network/blog/amd-mi300x-mi355x-pricing-2026/):
  - Top part is the **MI455X**; Helios = 72 × MI455X, **2.9 EF FP4, 31 TB HBM4**. There is also an MI430X "sovereign AI" variant.
  - Timing conflict: "first Helios shipments Q3 2026" in one source vs "engineering samples / low-volume H2 2026, mass production Q2 2027" in another.

**Cloud instance families (names to know)**
- **AWS:**
  - NVLink-generation table from AWS's own distributed-training repo — [awslabs EFA cheatsheet](https://github.com/awslabs/awsome-distributed-training/blob/main/docs/efa-cheatsheet.md):

    | Instance | GPU | NVLinks per GPU | NVLink gen |
    |---|---|---|---|
    | p4de.24xlarge [OLDER] | A100 80GB | 12 | 3rd |
    | p5.48xlarge | H100 | 18 | 4th |
    | p5en.48xlarge | H200 | 18 | 4th |
    | p6-b200.48xlarge | B200 | 18 | 5th |
    | p6e-gb200.36xlarge (GB200 UltraServer node) | B200 | 18 | 5th |

  - Capacity-Block price lists also name **P5e (H200)** and **P6-B300** — [ecorpit](https://ecorpit.com/aws-ec2-capacity-blocks-gpu-price-rise-finops-2026/), [FastGPU / dev.to](https://dev.to/fastgpu/15-gpu-list-prices-rose-in-september-and-none-fell-today-aws-raises-capacity-blocks-15-44l).
- **GCP** (accelerator-optimized families A4X, A4, A3, A2 plus G4/G2 for graphics/inference) — [GCP pricing page](https://cloud.google.com/compute/gpus-pricing), [GCP Spot pricing](https://cloud.google.com/spot-vms/pricing), [DWS pricing](https://cloud.google.com/products/dws/pricing):
  - **a4-highgpu-8g:** 8 × B200, 224 vCPU, 3,968 GB RAM, 12 TB local SSD.
  - **a3-ultragpu-8g:** 8 × H200, 224 vCPU, 2,952 GB.
  - **a3-megagpu-8g:** 8 × H100, 208 vCPU, 1,872 GB.
  - **a3-highgpu-1g/2g/4g/8g:** H100.
  - **g4-standard-48/96/192/384:** 1/2/4/8 × **RTX PRO 6000**.
  - **A4X:** Grace Blackwell family.
- **Azure** — [ND GB200 v6](https://github.com/MicrosoftDocs/azure-compute-docs/blob/main/articles/virtual-machines/sizes/gpu-accelerated/nd-gb200-v6-series.md), [ND H200 v5](https://github.com/MicrosoftDocs/azure-compute-docs/blob/main/articles/virtual-machines/sizes/gpu-accelerated/nd-h200-v5-series.md), [ND H100 v5](https://github.com/MicrosoftDocs/azure-compute-docs/blob/main/articles/virtual-machines/sizes/gpu-accelerated/ndh100v5-series.md):
  - **Standard_ND96isr_H100_v5:** 8 × H100, 640 GB total, 96 vCPU, 1,900 GiB, InfiniBand supported.
  - **Standard_ND96isr_H200_v5:** 8 × H200, 1,128 GB total.
  - **Standard_ND128isr_NDR_GB200_v6:** 4 × GB200 GPUs at 192 GB each, 128 vCPU, 900 GiB, NDR InfiniBand, NVLink domain up to 72 GPUs.
  - **Standard_ND128isr_GB300_v6** (and a "G5" variant): 4 × 288 GB, 4 × 800 Gbps IB.
  - **Standard_ND96isr_MI300X_v5:** 8 × MI300X.
- **OCI:** MI355X GA — [Spheron](https://www.spheron.network/blog/amd-mi300x-mi355x-pricing-2026/).
- **CoreWeave:** GB200 / GB300 fleets plus Vera Rubin NVL72 (limited) — [CoreWeave press release](https://www.coreweave.com/news/coreweave-delivers-nvidia-vera-rubin-nvl72-performance-at-production-scale-starting-with-cognition).

**Typical $/GPU-hour (approximate, USD, 2026)**
- **Aggregator on-demand list rates (mostly ≤ Sep 2026)** — [Spheron comparison](https://www.spheron.network/blog/gpu-cloud-pricing-comparison-2026/), [CloudZero on CoreWeave](https://www.cloudzero.com/blog/coreweave-pricing/), [GMI Cloud H200](https://www.gmicloud.ai/en/blog/h200-gpu-provider-pricing), [effectstory](https://effectstory.com/en/articles/cloud-gpu-h100-b200-pricing-comparison-2026):

  | GPU | AWS | CoreWeave | Lambda |
  |---|---|---|---|
  | H100 | ~$6.88 | ~$6.16 (8× node $49.24/hr) | ~$2.49–3.99 |
  | H200 | conflicting: ~$4.98 vs ~$8+ | ~$6.31 | ~$4.49 |
  | B200 | ~$14.24 (8-GPU instance ~$113.93/hr) | ~$8.60 (node $68.80/hr) | ~$6.69–6.99 |

  - CoreWeave GB200 NVL72 config: ~$10.50/GPU-hr.
  - One guide cites an AWS H100 cut "up to 45%" giving ~$3.90, which conflicts with $6.88. Unresolved.
- **B300:** Runpod $6.94 (Community) / $7.89 (Secure); Spheron from ~$5.84 — [Runpod B300](https://www.runpod.io/articles/guides/nvidia-b300), [Spheron B300](https://www.spheron.network/gpu-rental/b300/).
- **MI355X:** ~$2.95 (TensorWave, custom terms) to ~$5.99 (Daytona) — [getdeploying](https://getdeploying.com/gpus/amd-mi355x), [gpus.io](https://gpus.io/en/gpus/mi355x).
- **GCP official (14 Oct 2026), derived per GPU from 8-GPU VM prices including vCPU/RAM/SSD** — [DWS pricing](https://cloud.google.com/products/dws/pricing), [Spot pricing](https://cloud.google.com/spot-vms/pricing):

  | VM (GPU) | DWS Flex-start | DWS Calendar | Spot |
  |---|---|---|---|
  | a4-highgpu-8g (B200) | $64.44/hr ≈ **$8.06/GPU-hr** | $90.22 ≈ **$11.28** | $39.63 ≈ **$4.95** |
  | a3-ultragpu-8g (H200) | $42.40 ≈ $5.30 | $59.36 ≈ $7.42 | $50.80 ≈ $6.35 |
  | a3-megagpu-8g (H100) | $40.32 ≈ $5.04 | $44.00 ≈ $5.50 | ≈ $6.31 |
  | a3-highgpu-8g (H100) | $38.32 ≈ $4.79 | $41.60 ≈ $5.20 | ≈ $6.60 |
  | g4-standard-48 (1 × RTX PRO 6000) | $2.25 | – | $1.63 |

  - The spot prices came from the static page's default region, which was not confirmed. Spot prices change up to daily.

### Inferences
- **Per-GPU memory now clusters at three tiers:** 80 GB (H100), 141–192 GB (H200, B200, MI300X, GB200) and **288 GB** (B300, GB300, MI355X, Rubin). HBM bandwidth roughly doubles per generation (3.4 → 4.8 → 8 → ~22 TB/s).
- **Rubin's ~22 TB/s matters most for bandwidth-bound decode.** Its 50 PF NVFP4 matters most for prefill and training.
- **The NVLink domain (8 vs 72 GPUs) is now as important a selection criterion as the GPU itself.** For large-MoE inference and tensor/expert parallelism beyond 8 GPUs, NVL72-class systems (GB200/GB300 NVL72, Vera Rubin NVL72) keep all-to-all traffic on NVLink instead of InfiniBand.
- **Spreads between providers are large:** neocloud on-demand H100 is ~$2.5–4 vs hyperscaler ~$5–7, and B200 runs ~$6.7–8.6 vs ~$8–14. Hyperscaler premiums buy integration (IAM, VPC, managed K8s, compliance), not faster silicon.
- **GCP's B200 DWS Flex-start (~$8/GPU-hr) is well below AWS's B200 Capacity Block (~$14.2/GPU-hr after Oct 2026)**, suggesting GCP is pricing aggressively for queued capacity.

### Gaps
- I could not fetch any NVIDIA, AMD or AWS official spec or pricing page (proxy-blocked). Unverified as a result:
  - B300 FP8 dense figure.
  - The exact usable HBM on B200 (some listings use ~180 GB vs the 192 GB above).
  - MI300X bandwidth (commonly 5.3 TB/s) and FP8 figures.
  - All **MI325X** specs (commonly 256 GB HBM3E, ~6 TB/s).
  - MI355X FP8 dense figures.
- No official AWS instance-page specs were captured: per-instance EFA bandwidth (e.g., 3,200 Gbps on P5, 6,400 Gbps on P6-B300), P6e-GB300 UltraServer details, and official on-demand prices.
- I found no GCP official doc for the A4X Max / GB300 machine type name, or for GCP and Azure Rubin instance names or dates.
- The Azure ND GB200 v6 doc's network table appears to have mislabeled column headers ("Scale-Up 400 Gbps", "Scale-Out 1.8 TBps"). The likely meaning is 4 × 400 Gb NDR IB scale-out and 1.8 TB/s NVLink scale-up; this was not verified.
- No MLPerf v5.x/v6.0 results could be retrieved (search budget exhausted).

---

## 2. Custom silicon: Google TPU (v5e, v5p, v6e Trillium, TPU7x Ironwood), AWS Trainium2/3 and Inferentia2, Azure Maia

### Takeaway
- **TPU7x Ironwood is GA on Google Cloud (Apr 2026) and has a public list price: $12.00/chip-hr on-demand in us-central1.** Each chip has 192 GB HBM, ~7.4 TB/s and ~4.6 PF FP8, and pods scale to 9,216 chips.
- **AWS Trainium3 (GA Dec 2025)** has 144 GiB, 4.9 TB/s and 2.5 PF MXFP8 per chip, with 64- or 144-chip UltraServers.
- **Azure Maia 200 (Jan 2026) is an inference chip** serving Microsoft's own services (OpenAI models, Copilot, Foundry).
- These chips trade ecosystem breadth (CUDA) for price-performance. The software stacks are JAX/XLA (and PyTorch/vLLM on TPU), the Neuron SDK and the Maia SDK.

### Cited Findings

**Google TPU per-chip specs** — [scaling-book tpus.md](https://github.com/jax-ml/scaling-book/blob/main/tpus.md)

| TPU | HBM | HBM BW | BF16 peak | INT8 peak | Pod / topology | Host |
|---|---|---|---|---|---|---|
| v5e | 16 GB | 0.82 TB/s | 197 TF | 394 TOPS | 16×16 = 256 chips | 4×2 = 8 chips |
| v5p | 96 GB | 2.8 TB/s | 459 TF | 918 TOPS | 16×20×28 = 8,960 chips | 2×2×1 |
| v6e Trillium | 32 GB | 1.6 TB/s | 920 TF | 1.84 POPS | 16×16 = 256 chips | – |
| TPU7x Ironwood | 192 GB | 7.4 TB/s | 2.3 PF | 4.61 P (8-bit) | 4×4×576 = 9,216 chips | 2×2×1 |

- ICI bandwidth per link, one-way: v5e 45 GB/s; v5p, v6e and TPU7x **90 GB/s** (180 GB/s bidirectional) — [scaling-book tpus.md](https://github.com/jax-ml/scaling-book/blob/main/tpus.md).
- **Ironwood per chip:** ~4,614 FP8 TFLOPS, 192 GB HBM3E at ~7.37 TB/s. It is the first TPU with native FP8 — [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/google-deploys-new-axion-cpus-and-seventh-gen-ironwood-tpu-training-and-inferencing-pods-beat-nvidia-gb300-and-shape-ai-hypercomputer-model), [qscompute](https://qscompute.com/products/gpu-accelerators/google-ironwood-tpu-v7/).
- **Ironwood pod:** 9,216 chips, ~42.5 FP8 EF (peak), ~1.77 PB HBM, 9.6 Tb/s ICI — [TrendForce](https://www.trendforce.com/news/2025/11/07/news-google-unveils-7th-gen-tpu-ironwood-with-9216-chip-superpod-taking-aim-at-nvidia/).
  - The Register cautioned that Google's El Capitan comparison mixed FP8 and FP64 — [The Register](https://www.theregister.com/2025/04/10/googles_7thgen_ironwood_tpus_debut/).
- **Ironwood GA date:** most sources say **22 Apr 2026 (Cloud Next 2026)**; one says Nov 2025, likely conflating the pod announcement with GA — [qscompute](https://qscompute.com/products/gpu-accelerators/google-ironwood-tpu-v7/), [andrew.ooo](https://andrew.ooo/answers/what-is-ironwood-tpu-google-7th-gen-may-2026/).
- **8th-gen TPU [ANNOUNCED]:** Google previewed an eighth generation split into separate training and inference chips on TSMC 2 nm — [The Next Web](https://thenextweb.com/news/google-ironwood-tpu-inference-cloud-next).
- **Official TPU prices per chip-hour (USD, 14 Oct 2026)** — [Cloud TPU pricing](https://cloud.google.com/tpu/pricing), [Spot pricing](https://cloud.google.com/spot-vms/pricing):

  | TPU (region) | On-demand | DWS Flex-start | DWS Calendar | 1-yr CUD | 3-yr CUD | Spot |
  |---|---|---|---|---|---|---|
  | Ironwood (us-central1) | **$12.00** | $6.00 | $8.40 | $8.40 | $5.40 | ~$4.12 |
  | Trillium v6e (us-east1) | $2.70 | $1.35 | $1.89 | $1.89 | $1.22 | ~$0.58 |
  | v5p | $4.20 | $2.10 | $2.94 | $2.94 | $1.89 | ~$0.93 |
  | v5e (us-central1) | $1.20 | $0.60 | $0.84 | $0.84 | $0.54 | ~$0.36 |

  - Ironwood in europe-west2 is $13.20 on-demand.
  - Older: v4 pod $3.22, v3 pod $2.00, v2 pod $1.50.
  - Billing is shown in VM-hours (e.g., a v4 host with 4 chips = $12.88/hr).
  - An earlier article (~mid-2026) said Ironwood had no public price three months after launch — [Techi](https://www.techi.com/google-ironwood-tpu-no-public-price/). That is now superseded by the pricing page above.
- TPU usage-option guidance from Google — [Cloud TPU pricing](https://cloud.google.com/tpu/pricing):
  - **1-yr CUD** for users needing consistent access to **32–512 cores**.
  - **3-yr CUD** for **512+ cores**.
  - **On-demand** for short experiments.
  - **Spot/preemptible** for fault-tolerant batch.

**AWS Trainium / Inferentia (official Neuron docs)**
- **Trainium2** (3rd-gen AWS ML chip, 8 × NeuronCore-v3) — [Neuron docs: Trainium2](https://github.com/aws-neuron/aws-neuron-sdk/blob/master/about-neuron/arch/neuron-hardware/trainium2.rst):
  - **1,299 FP8 TFLOPS dense**, 667 BF16/FP16/TF32 TFLOPS, 2,563 sparse, 181 FP32.
  - **96 GiB HBM at 2.9 TB/s**.
  - NeuronLink-v3 at **1.28 TB/s per chip**.
  - Trn2 instance = up to 16 chips; Trn2 UltraServer = up to 64 chips.
  - Trn2 GA was announced Dec 2024 — [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2024/12/amazon-ec2-trn2-instances-available).
- **Trainium3** [SHIPPING; GA announced at re:Invent, early Dec 2025] (4th gen, 8 × NeuronCore-v4) — [Neuron docs: Trainium3](https://github.com/aws-neuron/aws-neuron-sdk/blob/master/about-neuron/arch/neuron-hardware/trainium3.rst), [Amazon announcement](https://www.aboutamazon.com/news/aws/trainium-3-ultraserver-faster-ai-training-lower-cost), [Business Wire](https://www.businesswire.com/news/home/20251201046353/en/Trainium3-UltraServers-Now-Available-Enabling-Customers-to-Train-and-Deploy-AI-Models-Faster-at-Lower-Cost):
  - **2,517 MXFP8/MXFP4 TFLOPS** (same peak for FP4 as FP8), 671 BF16/FP16/TF32 dense (2,517 sparse), 183 FP32.
  - **144 GiB HBM at 4.9 TB/s.** Clarigital notes some Neuron pages say 4.7 TB/s.
  - NeuronLink-v4 at **2.56 TB/s per chip**.
  - Hardware support for dynamic shapes/control flow and stochastic rounding.
  - First AWS chip on 3 nm.
- **Trn3 UltraServers** — [Neuron docs: Trn3 architecture](https://github.com/aws-neuron/aws-neuron-sdk/blob/master/about-neuron/arch/neuron-hardware/trn3-arch.rst):
  - **Gen1:** 64 chips (4 servers × 16), 161 PF dense MXFP8, 9 TB HBM, 314 TB/s.
  - **Gen2:** **144 chips** (36 servers × 4), **362 PF MXFP8, 20 TB HBM, 706 TB/s**.
  - The topology changes from Trn2's 2D torus to an **all-to-all switched fabric (NeuronSwitch-v1, PCIe Gen6-based)**, aimed at MoE and autoregressive serving.
  - Per-chip links: 256 GB/s intra-server, 320 GB/s inter-server, 128 GB/s inter-rack.
- Vendor claims for Trn3 vs Trn2 UltraServers — [Business Wire](https://www.businesswire.com/news/home/20251201046353/en/Trainium3-UltraServers-Now-Available-Enabling-Customers-to-Train-and-Deploy-AI-Models-Faster-at-Lower-Cost), [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/amazon-launches-trainium3-ai-accelerator-competing-directly-against-blackwell-ultra-in-fp8-performance-new-trn3-gen2-ultraserver-takes-vertical-scaling-notes-from-nvidias-playbook):
  - Up to **4.4× compute, 4× energy efficiency, ~4× memory bandwidth**; chip-to-chip latency under 10 µs.
  - Clusters scale to up to **1M Trainium chips**.
  - Named customers: **Anthropic**, Karakuri, Metagenomi, NetoAI, Ricoh, Splash Music. **Amazon Bedrock** serves production on Trn3.
- **Trainium4** is in preview / announced only — [The AI Economy](https://theaieconomy.substack.com/p/aws-trainium3-ultraservers-trainium4-preview).
- **Inferentia2** (Inf2 instances, up to 12 chips) — [Neuron docs: Inferentia2](https://github.com/aws-neuron/aws-neuron-sdk/blob/master/about-neuron/arch/neuron-hardware/inferentia2.rst):
  - 2 × NeuronCore-v2 per chip: **190 FP16/BF16/cFP8/TF32 TFLOPS**, 380 INT8 TOPS, 47.5 FP32.
  - **32 GiB HBM at 820 GiB/s**; NeuronLink-v2.
- **Software:** Neuron SDK, with Logical NeuronCore Configuration (LNC) for combining physical cores. Trn3 adds custom operators via GPSIMD engines — [Neuron docs: Trainium3](https://github.com/aws-neuron/aws-neuron-sdk/blob/master/about-neuron/arch/neuron-hardware/trainium3.rst).

**Azure Maia 200 [SHIPPING inside Azure, Jan 2026]**
- Specs — [Microsoft blog](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/), [Guru3D](https://www.guru3d.com/story/microsoft-maia-200-ai-accelerator-debuts-targets-azure-inference-scale/), [NAND Research](https://nand-research.com/?p=5185):
  - Inference-only, TSMC 3 nm, ~140–144B transistors.
  - **216 GB HBM3e at ~7 TB/s**, ~272 MB on-die SRAM.
  - **~10.15 PF FP4** at **750 W**; native FP8/FP4.
  - Four accelerators per tray connected switchlessly, scaling to 6,144 accelerators.
- Deployment — [Microsoft blog](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/), [AI Magazine](https://aimagazine.com/news/microsoft-unveils-maia-200-ai-accelerator):
  - Live in **US Central (Iowa)**, with **US West 3 (Phoenix)** next.
  - Serves OpenAI **GPT-5.2**, Microsoft Foundry and M365 Copilot, plus synthetic data/RL for Microsoft's Superintelligence team.
  - **Maia SDK in preview.**
  - The ~30% perf/$ improvement claim is vendor-stated.

### Inferences
- **Price-performance on GCP's list prices:**
  - **Ironwood:** ~$12 per ~4.6 PF FP8 ≈ **$2.6 per FP8-PF-hour** with 192 GB HBM.
  - **B200 via DWS Flex-start:** ~$8 per ~4.5 PF FP8 ≈ $1.8 per FP8-PF-hour.
  - **Ironwood via DWS Flex or 3-yr CUD:** ~$5.4–6/chip-hr ≈ $1.2–1.3 per FP8-PF-hour.
  - TPUs are most attractive under commitment or DWS, and at very large scale where the 9,216-chip ICI domain avoids an InfiniBand tier.
- **Trillium (v6e) at $2.70 on-demand / $1.35 Flex-start is the budget TPU for serving and fine-tuning** small to mid models (32 GB per chip, so shard larger models). v5e (16 GB) is now mostly for small models and cheap batch.
- **Trn3's all-to-all switched 144-chip domain mirrors NVIDIA's NVL72 approach.** It signals that MoE serving is the design target across vendors.
- **Maia is not an accelerator most external customers can rent as a VM.** You consume it indirectly through Azure AI services. This is inferred from the deployment description.
- **Software rule of thumb:**
  - TPUs mean **JAX/XLA first-class**, with PyTorch and vLLM on TPU available.
  - Trainium/Inferentia mean **Neuron SDK** (PyTorch/JAX integration; NKI for kernels).
  - CUDA-specific custom kernels are the main porting cost.

### Gaps
- I could not access docs.cloud.google.com to confirm current Ironwood machine-type names (e.g., tpu7x-standard-4t), PyTorch/vLLM-on-TPU support status, or Ironwood availability by region.
- Official Trn2/Trn3/Inf2 on-demand and Savings-Plan prices were not retrieved (AWS pages blocked).
- I could not confirm whether Maia 200 is exposed as a customer-rentable VM SKU.
- No independent MLPerf comparisons of TPU7x, Trn3 and GB300 were found within the budget.

---

## 3. Choosing a GPU for a workload: memory rules of thumb (bytes/param, KV cache, optimizer states), one GPU vs many

### Takeaway
**Inference weights ≈ params × bytes-per-param**: 2 for BF16, 1 for FP8/INT8, 0.5 for FP4/INT4. Add a KV cache of **2 · L · K_kv · d_head · bytes per token**, which often exceeds the weights at long context or high batch.

**Training with Adam needs ≥10 bytes/param** (BF16 weights + FP32 moments), or **~16 bytes/param** for classic mixed precision with FP32 master weights and gradients. Activations add more, often dominating unless checkpointed. FSDP/ZeRO-3 or model parallelism is needed once that exceeds a single GPU's HBM.

### Cited Findings
- **Training memory, minimum:** with BF16 params and FP32 Adam state (first and second moments) you need **2 + 8 = 10 bytes per parameter**. So the largest model trainable with pure data parallelism ≈ **HBM per device / 10**, e.g. **~9B params on a 96 GB TPU v5p**. This excludes activations/gradient checkpoints, so it is an absolute lower bound — [scaling-book training.md](https://github.com/jax-ml/scaling-book/blob/main/training.md).
- **Classic mixed-precision Adam** (FP16/BF16 weights + FP16/BF16 grads + FP32 master weights, momentum and variance) = 2 + 2 + 12 = **16 bytes/param**. A 7.5B model therefore needs ~120 GB before activations — [ZeRO paper, Rajbhandari et al., arXiv:1910.02054](https://arxiv.org/abs/1910.02054). Cited from the well-known paper; not re-fetched this session.
- **Activations often dominate training memory.**
  - Example: a 13B model needs ~130 GB for params + Adam state, but **~42 TB** of checkpointed activations at a 16M-token batch (3 checkpoints/layer) — [scaling-book training.md](https://github.com/jax-ml/scaling-book/blob/main/training.md).
  - "Block remat" saves only layer inputs and raises training FLOPs from ~6·N·D to ~8·N·D — [scaling-book transformers.md](https://github.com/jax-ml/scaling-book/blob/main/transformers.md).
- **FLOPs rules:** training ≈ **6 × params × tokens** (2 forward + 4 backward); inference ≈ **2 × params per token** — [scaling-book transformers.md](https://github.com/jax-ml/scaling-book/blob/main/transformers.md).
- **FSDP / ZeRO** — [scaling-book training.md](https://github.com/jax-ml/scaling-book/blob/main/training.md):
  - ZeRO-1/2/3 shard optimizer state / gradients / weights.
  - ZeRO-3 turns the gradient AllReduce into AllGather + ReduceScatter with the same comms volume, so it "basically always" makes sense.
  - It stays compute-bound when per-device batch exceeds C/W_ici (≈2,550 tokens on v5p).
- **Inference memory:** one copy of weights (13B at BF16 = 26 GB); no optimizer or gradients; activations are negligible with FlashAttention (8k-token prefill ≈ 80 MB per activation) — [scaling-book inference.md](https://github.com/jax-ml/scaling-book/blob/main/inference.md).
- **KV cache formula** — [scaling-book inference.md](https://github.com/jax-ml/scaling-book/blob/main/inference.md):
  - **KV bytes = 2 · bytes_per_float · H(head dim) · K(KV heads) · L(layers) · T(tokens)**.
  - Example: LLaMA-13B (K=40, H=128, L=40) with one 8,192-token sequence at BF16 = **6.7 GB**. "Just 4 of these exceed the memory usage of our parameters."
  - GQA/MQA (small K, as in LLaMA-3), KV quantization, paging (PagedAttention) and cross-layer sharing can cut KV size by over an order of magnitude.
- **Another KV example** — [scaling-book transformers.md](https://github.com/jax-ml/scaling-book/blob/main/transformers.md):
  - 8k context, 64 layers, K·H = 8,192, int8 → **8 GiB per sequence**.
  - Per token in int8 for MHA with D=4,096 and L=64: 512 KiB.
- **Decode is memory-bandwidth-bound.** Theoretical min step time = (batch × KV size + param bytes) / total HBM bandwidth. MLPs become compute-bound only above a critical batch B_crit ≈ FLOPs / HBM-BW (~240 for TPU v5e in BF16) — [scaling-book inference.md](https://github.com/jax-ml/scaling-book/blob/main/inference.md).
  - Weight quantization to int8/fp8 halves B_crit; doing the FLOPs in int8/fp8 doubles it.
  - Worked example: a 30B int8 model on a 16-chip v5e slice has a ~2.5 ms step at batch 4 and ~21 ms at batch 256.
- **Quantization:** inference is "usually less sensitive" to the precision of params and KV. Int8/int4/fp8 cuts both memory and bandwidth and can be applied post-training — [scaling-book inference.md](https://github.com/jax-ml/scaling-book/blob/main/inference.md).

### Inferences
- **Worked fit checks** (weights only; then leave ~20–40% headroom for KV cache, activations, CUDA graphs and fragmentation):
  - **8B model:** BF16 16 GB → 1 × L4/RTX PRO 6000-class card or larger; FP8 8 GB.
  - **70B model:**
    - BF16 140 GB → does not fit 1 × H100 (80 GB), and is borderline on 1 × H200 (141 GB, no KV room).
    - Fits 1 × MI300X (192 GB), 1 × B200 (~180–192 GB) or 1 × B300/MI355X (288 GB) with KV headroom; otherwise use 2 × H100 with tensor parallelism.
    - FP8 70 GB → 1 × H100 is tight; 1 × H200 is comfortable.
  - **405B model:**
    - FP8 ~405 GB → 8 × H100 (640 GB) or 2 × B300/MI355X (576 GB), plus KV.
    - BF16 ~810 GB → 8 × H200 (1,128 GB) or 4 × B300/MI355X (1,152 GB).
  - **Trillion-parameter-class MoE** (~1 TB at FP8): an NVL72 domain (GB200 ~13.8 TB, GB300 ~20 TB HBM) or a TPU7x/Trn3 multi-chip slice.
- **Training fit:** using ~16 bytes/param (plus activations), a 7B full fine-tune needs ~112 GB of states. That exceeds one 80 GB H100 without ZeRO/FSDP, 8-bit optimizers or LoRA.
  - LoRA/QLoRA reduces optimizer state to the adapter only, so a 70B QLoRA (~35 GB of 4-bit weights) fits on a single 80 GB GPU.
- **Selection heuristics:**
  - Decode-heavy chat or long-context serving → maximize **HBM bandwidth and capacity per $** (H200, B300, MI355X, Ironwood).
  - Prefill-heavy, batch or training work → maximize **dense FP8/FP4 FLOPs per $** and interconnect.
  - **MoE / >8-way tensor or expert parallelism** → prefer NVL72 / Trn3 Gen2 / TPU ICI domains over 8-GPU nodes linked by InfiniBand.
  - Small models and embeddings → L4 / RTX PRO 6000 / Inferentia2 / v5e on serverless.

### Gaps
- No vendor (NVIDIA/vLLM) published calculator or official sizing guide was retrievable this session.
- The fit checks above are arithmetic inferences, not benchmarked results.
- FP4 accuracy tradeoffs (NVFP4/MXFP4) were not researched.

---

## 4. Purchasing models: on-demand, reserved/committed, savings plans, capacity blocks, DWS, spot (discounts, notice times, checkpointing)

### Takeaway
GPU purchasing has bifurcated:
- **Short-term guaranteed capacity:** AWS EC2 Capacity Blocks for ML, GCP DWS Calendar mode. You prepay a fixed window.
- **Queued / flexible capacity:** GCP DWS Flex-start, ~50% off TPU on-demand.
- **Long-term commits:** 1–3 yr CUDs / Savings Plans / reservations; GCP up to 55% off on 3-yr resource CUDs, and TPU 3-yr ≈ 55% off.
- **Spot:** up to 91% off on GCP; 2-minute notice on AWS, 30-second notice on Azure.

AWS raised Capacity Block prices three times in 2026: ~15% in Jan, ~20% in Jul, ~15% in Oct. That is a clear signal of GPU scarcity.

### Cited Findings

**AWS EC2 Capacity Blocks for ML (per GPU-hour, US)**
- **~15% increase on 4 Jan 2026**, done without a formal announcement — [The Register](https://www.theregister.com/2026/01/05/aws_price_increase/).
- **~20% increase on 1 Jul 2026** across P6-B300, P6-B200, P5, P5e, P5en and P4de: **P6-B300 $14.04, P6-B200 $12.355, P5 $5.191** — [ecorpit](https://ecorpit.com/aws-ec2-capacity-blocks-gpu-price-rise-finops-2026/), [Tech-Insider](https://tech-insider.org/aws-ec2-capacity-blocks-price-hike-2026/).
- **~15% increase on 7 Oct 2026** (up to 26.5% outside the US for P5/P5en) — [FastGPU / dev.to](https://dev.to/fastgpu/15-gpu-list-prices-rose-in-september-and-none-fell-today-aws-raises-capacity-blocks-15-44l), [FourWeekMBA](https://fourweekmba.com/ai-aws-ec2-capacity-block-rates-october-2026/), [explainx](https://www.explainx.ai/blog/aws-capacity-blocks-gpu-price-hike-october-2026):

  | Family | Price per GPU-hr |
  |---|---|
  | P6-B300 | **$16.146** |
  | P6-B200 | $14.208 |
  | P5en | $7.895 |
  | P5e | $6.866 |
  | P5 | **$5.970** |

  - The July and October figures are internally consistent (×1.15), but the sources are third-party trackers, not the AWS page.

**GCP**
- **DWS Flex-start** — [DWS pricing](https://cloud.google.com/products/dws/pricing):
  - Queued; provisions when capacity is available for a defined duration.
  - Billed on usage like on-demand.
  - Covers A4 (B200), A3 Ultra/Mega/High, A2, G4 (RTX PRO 6000) and TPU v6e/v5p/v5e.
- **DWS Calendar mode** — [DWS pricing](https://cloud.google.com/products/dws/pricing), [DWS calendar mode summary](https://daily.dev/posts/dynamic-workload-scheduler-calendar-mode-reserves-gpus-and-tpus-yvusfiaxy):
  - Reserves a **fixed window of 1–90 days**, paid in full even if unused.
  - **8-GPU shapes only.**
  - **Flex-start and Calendar prices are "scheduled to be updated in November 2026."**
  - A 2025 blog says GPUs needed a ~4-day lead time; this may be outdated.
- **TPU discount ladder** (derived from the price table in section 2) — [Cloud TPU pricing](https://cloud.google.com/tpu/pricing):

  | Option | Price vs on-demand | Discount |
  |---|---|---|
  | DWS Flex-start | 50% | 50% |
  | DWS Calendar | 70% | 30% |
  | 1-yr CUD | 70% | 30% |
  | 3-yr CUD | 45% | 55% |

- **Compute Engine discounts** — [GCP pricing page](https://cloud.google.com/compute/gpus-pricing):
  - **Resource-based CUDs:** up to 37% (1-yr) and up to 55% (3-yr), or 70% for memory-optimized types.
  - **Flexible (spend-based) CUDs:** 28% (1-yr) / 46% (3-yr), but **these apply only to vCPU/memory of general-purpose and compute-optimized series, not GPUs**.
  - **GPU commitments must have reservations attached.** A commitment alone does not reserve zonal capacity; you need commitment + reservation.
  - **Sustained-use discounts:** up to 30%.
  - Discounts are mutually exclusive; Spot VMs get no CUDs or SUDs.
  - Billing is per-second after a 1-minute minimum.
- **GCP Spot:** "up to 91%" off. Prices can change up to once per day (TPU page says up to once every 30 days) — [GCP Spot pricing](https://cloud.google.com/spot-vms/pricing), [Cloud TPU pricing](https://cloud.google.com/tpu/pricing).

**Interruption notice times**
- **AWS Spot:** **2-minute** interruption notice via EventBridge/CloudWatch events and instance metadata. Hibernation is the exception: it starts immediately with no 2-minute warning — [AWS EC2 User Guide (GitHub source, archived)](https://github.com/awsdocs/amazon-ec2-user-guide/blob/master/doc_source/spot-instance-termination-notices.md).
- **Karpenter on AWS** — [Karpenter disruption docs](https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/docs/concepts/disruption.md):
  - Watches an **SQS interruption queue** fed by EventBridge.
  - On a Spot warning it drains the node **while provisioning a replacement in parallel**. Average node startup "generally" fits within the 2-minute window.
  - Rebalance Recommendations raise events only; drain/terminate on them requires the AWS Node Termination Handler, which causes more churn.
- **Azure Spot** — [Azure Spot VMs doc](https://github.com/MicrosoftDocs/azure-compute-docs/blob/main/articles/virtual-machines/spot-vms.md):
  - Evicted with **30-seconds notice**, delivered best-effort via **Scheduled Events**.
  - Eviction policy is Deallocate (default) or Delete.
  - Setting max price **-1** means no price-based eviction, capped at the pay-as-you-go price.
  - The portal shows per-hour eviction rates based on the last 7 days of history.
  - No SLA.

### Inferences
- **Decision ladder for a team:**
  - Bursty experiments → on-demand, or neocloud on-demand.
  - Multi-day training run with a fixed deadline → Capacity Block / DWS Calendar (prepaid, guaranteed). After the 2026 hikes, AWS Capacity Blocks for B200/B300 ($14–16/GPU-hr) can cost more than neocloud on-demand B200/B300 (~$6–9).
  - Tolerant batch / fine-tunes → DWS Flex-start or spot.
  - Steady inference fleet → 1–3 yr CUD/reservation or neocloud term contract.
- **Checkpointing implications:**
  - **Azure's 30 s (and GCP's, reportedly also short) notice is too short to write a large checkpoint.** On those clouds, checkpoint periodically (every N steps, sized so that lost work under the measured eviction rate stays small) to fast storage. Use async/sharded checkpointing (e.g., PyTorch DCP, Orbax for JAX) so writes overlap compute.
  - AWS's 2 minutes allows a final "emergency" sharded checkpoint for small to mid models.
  - Checkpoint size is ~bytes/param × params: ~16 B/param with optimizer state, e.g. ~1.1 TB for a 70B full-state checkpoint.
- **Capacity Block price trend:** compounding three 2026 hikes (1.15 × 1.20 × 1.15 ≈ **1.59×**) means AWS short-term reserved H100 rose ~59% in 2026. This is inferred from the reported percentages.

### Gaps
- **GCP Spot/preemptible notice time** (commonly 30 s) was not verified (docs.cloud.google.com blocked).
- AWS Savings Plans and EC2 Instance Savings Plan discount levels for P5/P6, and the exact June-2025 P5 on-demand price cut, were not verified from AWS.
- Azure reserved-instance discounts for ND-series, OCI pricing, and neocloud reserved-contract discounts were not found.
- AWS Capacity Block mechanics (durations of 1–182 days, up to 8 weeks advance booking, cluster sizes) were not verified this session.

---

## 5. Autoscaling for GPU workloads: Cluster Autoscaler / Karpenter, KEDA, scale-to-zero, cold starts and mitigations

### Takeaway
- **Node-level:** Cluster Autoscaler or Karpenter.
- **Pod-level:** HPA, or KEDA for event/queue-driven scaling including **to and from zero**.
- **Cold start is the core problem.** It is container pull + weight download + loading to GPU + compile/graph capture, taking tens of seconds to minutes.
- **Mitigations:** cache weights near the node (volumes, model caches), cache compile artifacts, keep minimum warm replicas, and use **GPU memory snapshots** (Modal, experimental) or snapshot/FlashBoot features (RunPod).

### Cited Findings
- **Kubernetes Cluster Autoscaler GPU specifics** — [Cluster Autoscaler FAQ](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md):
  - `--scale-down-gpu-utilization-threshold`, default **0.5**: for GPU nodes only GPU requests count toward utilization; CPU and memory are ignored.
  - `--gpu-total` caps the number of each GPU type ("currently only works on GKE").
  - Nodes whose GPU device driver hasn't come up appear as **`resourceUnready`** (CA ≥1.24).
- **Karpenter:** handles Spot interruption via an SQS queue (2-minute notice), draining and provisioning a replacement in parallel — [Karpenter disruption docs](https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/docs/concepts/disruption.md).
- **KEDA:** "fine-grained autoscaling (including to/from zero) for event driven Kubernetes workloads" — [KEDA README](https://github.com/kedacore/keda).
- **RunPod Serverless cold starts** — [RunPod docs: Serverless overview](https://github.com/runpod/docs/blob/main/serverless/overview.mdx):
  - Defined as the time from a request hitting an endpoint with no running workers until a worker is warm: container start, model load into GPU memory, runtime init.
  - Mitigations: **cached models, FlashBoot, active (min) workers > 0**, plus preflight "fitness checks".
- **RunPod billing** — [RunPod docs: Serverless pricing](https://github.com/runpod/docs/blob/main/serverless/pricing.mdx):
  - Billed per-second from worker start to full stop.
  - **Start time is billed**, mostly model loading in your handler. **Image pull and cached-model download are not billed.**
  - Default idle timeout is **5 s**.
  - **Flex workers** scale to zero at the standard rate; **active workers** run 24/7 with discounts via sales.
  - Default spend limit is $80/hr.
- **Modal** — [Modal example: gpu_snapshot.py](https://github.com/modal-labs/modal-examples/blob/main/06_gpu_and_ml/gpu_snapshot.py), [Modal example: vllm_inference.py](https://github.com/modal-labs/modal-examples/blob/main/06_gpu_and_ml/llm-serving/vllm_inference.py):
  - **GPU memory snapshots ("experimental")** are enabled with `enable_memory_snapshot=True` and `experimental_options={"enable_gpu_snapshot": True}`. The model loads onto the GPU in `@modal.enter(snap=True)`, and later cold starts restore from the snapshot. They work only on deployed Functions.
  - The vLLM example caches HF weights and **vLLM JIT compilation artifacts in Modal Volumes**. Startup latency is "typically tens of seconds to a few minutes, reduced to about ten seconds when loaded from the cache."
  - It uses `scaledown_window=15 min` to keep containers warm, with GPU spec like `gpu="H200:N"`.

### Inferences
- **Reference pattern on K8s** (EKS/GKE/AKS):
  - Karpenter or CA with GPU NodePools/node groups (separate pools for on-demand vs spot and per GPU type).
  - KEDA scaling inference Deployments on queue depth or in-flight requests (e.g., Prometheus metrics from vLLM).
  - minReplicas = 0 for dev/batch, ≥1 for latency-sensitive production.
  - Taint GPU nodes so only GPU pods land there.
- **Cold-start stack, slowest to fastest:**
  1. Pull a multi-GB image (pre-pull/stream images, slim images).
  2. Download weights (node-local NVMe cache, shared volume, in-region object storage).
  3. Load to GPU (safetensors, parallel loading).
  4. torch.compile / CUDA graph capture (cache artifacts).
  5. Memory or GPU snapshot restore, the fastest.
- **Scale-to-zero only pays off if** cold-start latency (tens of seconds to minutes for LLMs) is acceptable or masked by queues. Otherwise one warm replica of an H100 costs ~$2.5–7/hr × 730 hr ≈ **$1.8k–5k/month**.
- **The CA GPU utilization threshold of 0.5 means a node with 8 GPUs and only 3 requested (37.5%) is a scale-down candidate.** Bin-packing many small inference pods onto big 8-GPU nodes can thrash. Use smaller GPU shapes or MIG/time-slicing for small models.

### Gaps
- Not researched or verifiable here: GKE-specific features (GKE Autopilot GPU, image streaming, GCS FUSE caching), AWS SageMaker / EKS model-caching features, NVIDIA Run:ai / Dynamo autoscaling, and KServe/Knative scale-to-zero specifics.
- I found no independent cold-start benchmarks (e.g., seconds to first token for a 70B model across platforms) within budget.

---

## 6. Serverless GPU platforms (Modal, RunPod, Replicate, Baseten, Cloud Run GPUs, SageMaker, Vertex AI, Azure ML endpoints): tradeoffs

### Takeaway
- **Serverless GPU platforms bill per second and scale to zero.** You trade a higher per-hour rate and cold-start risk for zero idle cost and minimal ops.
- **Cloud Run** now offers **L4 (~$0.67/hr)** and **RTX PRO 6000 (~$1.31/hr)** GPUs on a per-second basis.
- **Modal and RunPod** differentiate on cold-start tech: GPU snapshots, FlashBoot, model caching.
- Managed hyperscaler endpoints (SageMaker, Vertex AI, Azure ML) trade cost for enterprise integration.

### Cited Findings
- **Cloud Run GPU pricing** (per second, first price tier) — [Cloud Run pricing](https://cloud.google.com/run/pricing):

  | GPU | No zonal redundancy | With zonal redundancy |
  |---|---|---|
  | NVIDIA L4 | **$0.0001867/s ≈ $0.67/hr** | $0.0002909/s ≈ $1.05/hr |
  | NVIDIA RTX PRO 6000 | **$0.00036522/s ≈ $1.31/hr** | $0.00056913/s ≈ $2.05/hr |

  - vCPU and memory are billed on top.
  - Google's worked example: an L4 service (4 vCPU, 16 GiB) in europe-west1 that peaks at 2 instances on a 24-hour cycle costs **~$822/month**.
- **GCP G4 VMs (RTX PRO 6000) for comparison:** DWS Flex-start g4-standard-48 is $2.25/hr; spot is $1.63/hr — [DWS pricing](https://cloud.google.com/products/dws/pricing), [Spot pricing](https://cloud.google.com/spot-vms/pricing).
- **RunPod Serverless:** per-second billing, flex workers that scale to zero vs always-on active workers, FlashBoot and model caching for cold starts. Container disk ~$0.10/GB-month; network volume $0.07/GB-month (<1 TB) or $0.05 (>1 TB) — [RunPod docs: pricing](https://github.com/runpod/docs/blob/main/serverless/pricing.mdx), [RunPod docs: overview](https://github.com/runpod/docs/blob/main/serverless/overview.mdx).
- **Modal:** Python-decorator-defined GPU functions (`gpu="H200:N"`, A10, etc.), Volumes for weight and compile caches, configurable `scaledown_window`, and experimental GPU memory snapshots — [Modal examples](https://github.com/modal-labs/modal-examples/blob/main/06_gpu_and_ml/llm-serving/vllm_inference.py), [gpu_snapshot.py](https://github.com/modal-labs/modal-examples/blob/main/06_gpu_and_ml/gpu_snapshot.py).
- **RunPod B300:** on-demand pods at $6.94 (Community) / $7.89 (Secure) per GPU-hr. This shows serverless-native providers now also carry frontier GPUs — [Runpod B300](https://www.runpod.io/articles/guides/nvidia-b300).

### Inferences
- **Break-even heuristic:** serverless wins when utilization is low (roughly under 30–50% of the hour) or traffic is spiky. Dedicated or reserved instances win for steady high utilization. At ~100% utilization, a Cloud Run L4 ($0.67/hr + vCPU/RAM) is comparable to an L4 VM, so the value is purely scale-to-zero and no ops.
- **Platform archetypes:**
  - **Modal:** code-first Python, fast iteration, snapshots.
  - **RunPod:** cheapest raw per-second GPU, broad GPU menu, community/secure tiers.
  - **Baseten:** production model serving, dedicated deployments, Truss packaging.
  - **Replicate:** model marketplace / public model APIs, Cog containers.
  - **Cloud Run:** inside GCP IAM/VPC, limited to L4 / RTX PRO 6000 class.
  - **SageMaker / Vertex AI / Azure ML managed endpoints:** enterprise integration, larger GPUs, usually always-on instances rather than true scale-to-zero.
  - These characterizations come from general knowledge; only the Modal, RunPod and Cloud Run details are verified in this session.
- **Cloud Run's GPU menu tops out at 96 GB (RTX PRO 6000, Blackwell).** This makes it suitable for ≤~70B models at FP8 or 4-bit and for diffusion/embedding models, not frontier-scale serving. The RTX PRO 6000 96 GB figure is general knowledge, not verified here.

### Gaps
- Unverified this session (search budget exhausted; sites blocked):
  - Modal per-second GPU price list (H100/B200).
  - Baseten and Replicate pricing and features.
  - SageMaker Serverless Inference GPU support (historically CPU-only), SageMaker async/real-time endpoint scale-to-zero.
  - Vertex AI prediction GPU pricing.
  - Azure ML managed online endpoint GPU pricing.
- Cloud Run GPU cold-start time, per-instance GPU limits and regional availability were not verified (docs blocked).

---

## 7. Neoclouds vs hyperscalers (CoreWeave, Lambda, Nebius, Crusoe, Together) and GPU availability dynamics

### Takeaway
- **Neoclouds (CoreWeave, Lambda, Nebius, Crusoe, Together, TensorWave, Vultr, RunPod) get new NVIDIA silicon first and list GPUs well below hyperscaler on-demand.**
  - CoreWeave was first to offer Vera Rubin NVL72 (Sep 2026).
  - Lambda's H100 is ~$2.5–4 vs AWS ~$6.9.
  - Neoclouds often sell in node bundles or reserved contracts.
- **2026 has been a tightening market:** AWS hiked Capacity Block prices three times, and one tracker reported 15 GPU list-price increases (and none falling) in September 2026.

### Cited Findings
- **CoreWeave:**
  - First cloud with **Vera Rubin NVL72 (limited availability, 30 Sep 2026)**; Cognition is the first customer.
  - Rubin runs under the same tooling as its GB200 and GB300 fleets.
  - Sources: [CoreWeave press release](https://www.coreweave.com/news/coreweave-delivers-nvidia-vera-rubin-nvl72-performance-at-production-scale-starting-with-cognition), [Network World](https://www.networkworld.com/article/4229739/coreweave-brings-nvidia-vera-rubin-ai-tools-to-its-cloud-services.html), [Datacentre Magazine: Dell & CoreWeave first Rubin deployment](https://datacentremagazine.com/news/inside-dell-and-coreweave-world-first-vera-rubin-deployment).
- **CoreWeave pricing:**
  - Sells in **8-GPU node bundles**: HGX H100 node $49.24/hr, H200 ~$6.31/GPU, HGX B200 node $68.80/hr. Effective per-GPU cost depends on utilization — [CloudZero](https://www.cloudzero.com/blog/coreweave-pricing/), [Spheron on CoreWeave](https://www.spheron.network/blog/coreweave-gpu-pricing-2026/).
  - Aggregators say CoreWeave and Lambda "typically offer the lowest on-demand rates" vs AWS. Egress fees, minimum commitments and spot discounts can change real cost more than the headline rate — [Spheron comparison](https://www.spheron.network/blog/gpu-cloud-pricing-comparison-2026/), [gpu.fm](https://www.gpu.fm/blog/cloud-gpu-providers-comparison-2026).
- **Lambda:** H100 SXM $2.49–3.99, H200 ~$4.49, B200 from ~$6.69 (8-GPU) / $6.99 (1-GPU) — [Spheron comparison](https://www.spheron.network/blog/gpu-cloud-pricing-comparison-2026/), [GMI Cloud](https://www.gmicloud.ai/en/blog/h200-gpu-provider-pricing).
- **AMD-focused neoclouds:** MI355X is GA at Vultr (and OCI), contact-sales at TensorWave and Crusoe, with prices ~$2.95–5.99/GPU-hr — [Spheron MI355X](https://www.spheron.network/blog/amd-mi300x-mi355x-pricing-2026/), [getdeploying](https://getdeploying.com/gpus/amd-mi355x).
- **Price direction:**
  - FastGPU reported that "15 GPU list prices rose in September [2026] and none fell," alongside AWS's 7 Oct Capacity Block hike — [FastGPU / dev.to](https://dev.to/fastgpu/15-gpu-list-prices-rose-in-september-and-none-fell-today-aws-raises-capacity-blocks-15-44l).
  - AWS's 2026 Capacity Block hikes: +15% Jan, +20% Jul, +15% Oct — [The Register](https://www.theregister.com/2026/01/05/aws_price_increase/), [ecorpit](https://ecorpit.com/aws-ec2-capacity-blocks-gpu-price-rise-finops-2026/).
- **Rubin access:** initial supply goes to large customers. Enterprise and on-prem delivery may extend into 2027 because of allocation queues — [Spheron Rubin](https://www.spheron.network/blog/vera-rubin-nvl72-cloud-availability-cost-per-token/), [VRLA roadmap](https://vrlatech.com/nvidia-gpu-roadmap-2026-2030/).
- **Some GPU-cloud comparisons list B300/GB300 as reserved-only at certain providers**, while others offer on-demand — [VESSL GB300](https://vessl.ai/en/gpu/gb300), [io.net GB300](https://io.net/p/gb300-nvl72-cloud-rental-how-to-access-nvidias-blackwell-ultra-architecture-in-2026).

### Inferences
- **When to pick a neocloud:**
  - Lowest $/GPU-hr.
  - Earliest access to the newest NVL72/Rubin systems.
  - Bare-metal or Slurm/K8s clusters with InfiniBand for large training.
  - Willingness to sign term contracts.
- **When to pick a hyperscaler:**
  - Data gravity (data already in S3/GCS/Blob, so you avoid egress).
  - Compliance, IAM and VPC integration.
  - Managed services (Bedrock/Vertex/Foundry).
  - Custom silicon (TPU, Trainium) that only exists there.
  - Existing committed-spend agreements.
- **2026 availability dynamics** point to persistent scarcity for frontier parts:
  - Price hikes rather than cuts, even for older H100/H200.
  - Rubin allocation queues.
  - Reserved-only listings for GB300.
  - Buyers should lock capacity early, multi-source across 2–3 providers, and design portable stacks (containers + K8s/Slurm, framework-agnostic serving) to arbitrage.
- **Hopper-generation pricing has not collapsed**, despite B200/B300 availability. The surge in inference demand appears to absorb older GPUs. This is inferred from the price-rise reports, not directly measured.

### Gaps
- Unverified within budget:
  - Nebius, Crusoe and Together AI specifics (fleet size, GPU types, pricing, 2026 financing or capacity announcements).
  - CoreWeave's 2026 backlog/revenue figures.
  - Lambda's corporate status.
  - SemiAnalysis ClusterMAX ratings.
- No authoritative index of H100 rental price trends over 2025–2026 was retrieved, e.g. SemiAnalysis or Ornn-style indices.
- The "15 GPU list prices rose" claim comes from a single developer-blog tracker.
