# Bytes, Not FLOPs, Now Steer Cloud AI

As of October 2026, the most useful thing an AI engineer can know about the cloud is that nearly every hard decision (which accelerator to rent, how to shard a training run, how many users one serving replica can hold, what an agent costs) comes down to storing and moving bytes, not to doing arithmetic. LLM decode is limited by memory bandwidth. Mixed-precision training carries about **16 bytes of state per parameter**. The KV cache often outweighs the model weights. And the size of the NVLink domain (**8 GPUs in an HGX node, 72 in an NVL72 rack**) now matters as much as which GPU you pick. Around those constraints the stack has largely standardized. On hardware: Hopper and Blackwell GPUs, with 288 GB Blackwell Ultra widely rentable and Vera Rubin in limited availability since 30 September 2026. On orchestration: Kubernetes with Dynamic Resource Allocation (DRA) now generally available, plus Kueue, JobSet or Slurm for gang-scheduled jobs. On serving: vLLM, SGLang or TensorRT-LLM behind inference-aware gateways. For tools, MCP (the Model Context Protocol), which became stateless in July 2026, and for traces, OpenTelemetry. The economics are lopsided, and that should set your priorities. GPU rental prices rose through 2026: AWS raised Capacity Block rates three times, about 59% compounded. Yet vendor telemetry puts average GPU utilization near **5%** in unoptimized Kubernetes clusters, and Anthropic measures agent loops costing **1.7–7.3× more without prompt caching**. Raising utilization and cache hit rates therefore pays more than any rate discount. Regulation moved as well: the EU's Digital Omnibus pushed high-risk AI obligations back to December 2027, but enforcement for general-purpose AI (GPAI) models and the Article 50 transparency duties took effect in August 2026. Many prices and performance numbers below come from aggregators or vendor claims. Treat them as approximate; where sources conflict, the text says so.

## The infrastructure layer: memory, interconnect and data gravity decide placement

The bottom of the stack saw 2026's biggest changes: new memory tiers, NVLink at rack scale, rising rental prices, and Kubernetes finally treating accelerators as first-class devices. These three subsections cover what to rent, how to schedule it, and where the data should live.

### Compute: rent HBM capacity and NVLink domains, then buy GPU time like a commodity

The rental market in October 2026 is still anchored on NVIDIA Hopper (H100, H200) and Blackwell (B200, GB200). **Blackwell Ultra (B300/GB300, 288 GB of HBM3e per GPU) is now widely rentable.** **Vera Rubin (288 GB of HBM4 at about 22 TB/s, with NVLink 6 at 3.6 TB/s per GPU) has been in limited availability at CoreWeave since 30 September 2026.** There, Cognition reports 4.8× the token throughput of a GB200 NVL72 baseline; that is a customer claim, not an independent benchmark ([CoreWeave](https://www.coreweave.com/news/coreweave-delivers-nvidia-vera-rubin-nvl72-performance-at-production-scale-starting-with-cognition); [Barrack.ai](https://blog.barrack.ai/nvidia-rubin-specs-architecture-2026/)). NVIDIA said Rubin began shipping to AWS, Google Cloud, Azure and OCI in July, but no hyperscaler Rubin instance was confirmed generally available by mid-October, and one vendor expects most teams to wait until 2027 ([Spheron](https://www.spheron.network/blog/vera-rubin-nvl72-cloud-availability-cost-per-token/)). AMD's current cloud part is the **MI355X (288 GB HBM3E, ~8 TB/s, ~10 PF dense FP4)**, generally available on OCI and Vultr. The older MI300X (192 GB) is still common on Azure ([SemiAnalysis InferenceX](https://inferencex.semianalysis.com/chips/mi355x); [Microsoft Docs: ND MI300X v5](https://github.com/MicrosoftDocs/azure-compute-docs/blob/main/articles/virtual-machines/sizes/gpu-accelerated/ndmi300xv5-series.md)).

| Accelerator | HBM per chip | HBM bandwidth | Dense low-precision peak | Scale-up domain | Status (Oct 2026) |
|---|---|---|---|---|---|
| H100 | 80 GB | 3.4 TB/s | 2.0 PF FP8 | 8 GPUs (NVLink 4, 450 GB/s per direction) | Shipping, widely rented |
| H200 | 141 GB | 4.8 TB/s | 2.0 PF FP8 | 8 GPUs | Shipping |
| B200 / GB200 | 192 GB | 8.0 TB/s | 4.5 PF FP8, 9 PF FP4 | 8 (HGX) or 72 (NVL72), NVLink 5 at 900 GB/s per direction | Shipping |
| B300 / GB300 | 288 GB | ~8 TB/s | ~15 PF FP4 (secondary sources) | 72 | Shipping |
| Vera Rubin | 288 GB HBM4 | ~22 TB/s | ~50 PF NVFP4 inference (secondary) | 72, NVLink 6 at 3.6 TB/s | Limited (CoreWeave) |
| AMD MI355X | 288 GB | ~8 TB/s | ~10 PF FP4 | 8 | GA on OCI, Vultr |
| Google TPU7x Ironwood | 192 GB | 7.4 TB/s | ~4.6 PF FP8 | 9,216-chip pod (ICI) | GA (Apr 2026) |
| AWS Trainium3 | 144 GiB | 4.9 TB/s | 2.5 PF MXFP8 | 144-chip UltraServer | GA (Dec 2025) |
| Azure Maia 200 | 216 GB | ~7 TB/s | ~10 PF FP4 | Up to 6,144 accelerators | Internal Azure services only |

The Hopper and Blackwell rows come from the JAX team's scaling book ([How to Scale Your Model: GPUs](https://github.com/jax-ml/scaling-book/blob/main/gpus.md)). The B300 row comes from Azure's ND GB300 v6 documentation and vendor guides; one datasheet lists 279 GB rather than 288 GB ([Microsoft Docs: ND GB300 v6](https://github.com/MicrosoftDocs/azure-compute-docs/blob/main/articles/virtual-machines/sizes/gpu-accelerated/nd-gb300-v6-series.md); [Spheron B300](https://www.spheron.network/blog/nvidia-b300-blackwell-ultra-guide/)). The custom-silicon rows come from Google's, AWS's and Microsoft's own documents, cited below.

Two patterns in that table drive selection. First, **per-GPU memory now comes in three tiers (80 GB, 141–192 GB and 288 GB), and HBM bandwidth roughly doubles each generation (3.4 → 4.8 → 8 → ~22 TB/s)**. Every decode step re-reads the weights and the KV cache, so for chat and long-context serving, bandwidth and capacity per dollar matter more than peak FLOPs. Peak FLOPs matter mostly for prefill and training. Second, **the NVLink domain is now a first-class selection criterion**. NVLink 4 gives 450 GB/s per direction inside an 8-GPU Hopper node. NVLink 5 doubles that to 900 GB/s and stretches the domain to **72 GPUs in a GB200 NVL72 rack**. Scale-out bandwidth, meanwhile, stays near 400 Gb/s (about 50 GB/s) per GPU ([Scaling Book](https://github.com/jax-ml/scaling-book/blob/main/gpus.md)). Azure's GB300 VM shows the shape concretely: four 288 GB GPUs per VM, NVLink at 1.8 TB/s across up to 72 GPUs, and 4 × 800 Gb/s InfiniBand that scales "to up to 100,000 GPUs" ([Microsoft Docs](https://github.com/MicrosoftDocs/azure-compute-docs/blob/main/articles/virtual-machines/sizes/gpu-accelerated/nd-gb300-v6-series.md)). For mixture-of-experts (MoE) serving, or any tensor or expert parallelism wider than eight GPUs, an NVL72-class domain keeps the all-to-all traffic off the slower network.

Custom silicon gives up CUDA's ecosystem in exchange for better price-performance, and in 2026 it finally became easy to price. **Google's TPU7x Ironwood is generally available with a public list price of $12.00 per chip-hour on demand in us-central1.** That falls to $6.00 under Dynamic Workload Scheduler (DWS) Flex-start and $5.40 on a three-year commitment; Trillium (v6e) lists at $2.70 ([Cloud TPU pricing](https://cloud.google.com/tpu/pricing); [Scaling Book: TPUs](https://github.com/jax-ml/scaling-book/blob/main/tpus.md)). Dividing price by FP8 peak:

- on-demand Ironwood costs about $2.6 per FP8 petaflop-hour;
- a B200 bought through DWS Flex-start costs about $1.8;
- Ironwood under Flex-start or a three-year commitment costs about $1.2–1.3.

So TPUs win mainly under commitment or queued capacity, and at scales where a 9,216-chip interconnect domain saves you an InfiniBand tier. **AWS Trainium3 (144 GiB at 4.9 TB/s, 2.5 PF MXFP8) ships in UltraServers of up to 144 chips on an all-to-all switched fabric.** The design targets MoE serving and mirrors NVL72 ([Neuron docs: Trainium3](https://github.com/aws-neuron/aws-neuron-sdk/blob/master/about-neuron/arch/neuron-hardware/trainium3.rst); [Neuron docs: Trn3 architecture](https://github.com/aws-neuron/aws-neuron-sdk/blob/master/about-neuron/arch/neuron-hardware/trn3-arch.rst)). Anthropic is a named customer, and Amazon Bedrock serves production traffic on it ([Business Wire](https://www.businesswire.com/news/home/20251201046353/en/Trainium3-UltraServers-Now-Available-Enabling-Customers-to-Train-and-Deploy-AI-Models-Faster-at-Lower-Cost)). **Azure's Maia 200 is an inference chip** that serves GPT-5.2, Microsoft Foundry and Microsoft 365 Copilot. You consume it through Azure services rather than renting it as a VM ([Microsoft](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/)). The cost of porting is in software: JAX/XLA is first-class on TPU and the Neuron SDK on Trainium, and custom CUDA kernels are what break.

Sizing starts with arithmetic that every AI engineer should be able to do in their head. **Inference weights ≈ parameters × bytes per parameter**: 2 bytes for BF16, 1 for FP8 or INT8, 0.5 for FP4 or INT4. The KV cache adds **2 × layers × KV heads × head dimension × bytes, per token**. A single 8,192-token LLaMA-13B sequence in BF16 already needs 6.7 GB, and "just 4 of these exceed the memory usage of our parameters" ([Scaling Book: inference](https://github.com/jax-ml/scaling-book/blob/main/inference.md)). Training with Adam needs **at least 10 bytes per parameter** (BF16 weights plus FP32 moments), or **16 bytes** in classic mixed precision with FP32 master weights. Both figures exclude activations, which often dominate ([Scaling Book: training](https://github.com/jax-ml/scaling-book/blob/main/training.md); [ZeRO, Rajbhandari et al.](https://arxiv.org/abs/1910.02054)). The consequences are concrete:

- **70B model in BF16 (140 GB):** does not fit one 80 GB H100 and is borderline on a 141 GB H200, but fits a single MI300X, B200, B300 or MI355X with room left for KV cache.
- **70B model in FP8:** fits comfortably on one H200.
- **7B full fine-tune (about 112 GB of optimizer and weight state):** overflows one H100 unless you shard, offload or use LoRA.

A good rule is to keep 20–40% of HBM free beyond the weights for KV cache, activations and CUDA graphs.

Buying GPU time has split into four modes with very different risk profiles:

- **Short-term guaranteed capacity:** AWS EC2 Capacity Blocks and GCP DWS Calendar mode. Calendar mode reserves 1–90 days, comes only in 8-GPU shapes, and is paid in full even if you don't use it ([GCP DWS pricing](https://cloud.google.com/products/dws/pricing)). This suits training runs with a deadline.
- **Queued flexible capacity:** DWS Flex-start. You wait for capacity, then pay on-demand-style usage billing, at half the on-demand rate for TPUs.
- **Long commitments:** up to 55% off on GCP three-year resource commitments (CUDs). GPU commitments need attached reservations to guarantee capacity in a zone, and spend-based flexible CUDs do not cover GPUs at all ([GCP GPU pricing](https://cloud.google.com/compute/gpus-pricing)).
- **Spot:** up to 91% off on GCP. AWS gives a **2-minute** interruption notice and Azure only **30 seconds** ([AWS EC2 guide](https://github.com/awsdocs/amazon-ec2-user-guide/blob/master/doc_source/spot-instance-termination-notices.md); [Azure Spot VMs](https://github.com/MicrosoftDocs/azure-compute-docs/blob/main/articles/virtual-machines/spot-vms.md)). Neither is long enough to write a large checkpoint, so periodic asynchronous checkpointing is mandatory.

The defining 2026 trend is scarcity. AWS raised Capacity Block prices about **15% on 4 January, 20% on 1 July and 15% on 7 October 2026**. Third-party trackers put P6-B300 at about $16.15 and P5 (H100) at about $5.97 per GPU-hour afterwards, roughly a 59% compounded rise for the year ([The Register](https://www.theregister.com/2026/01/05/aws_price_increase/); [ecorpit](https://ecorpit.com/aws-ec2-capacity-blocks-gpu-price-rise-finops-2026/); [FastGPU](https://dev.to/fastgpu/15-gpu-list-prices-rose-in-september-and-none-fell-today-aws-raises-capacity-blocks-15-44l)). One tracker counted 15 GPU list-price increases and no decreases in September alone.

| Purchase option (Oct 2026, per GPU-hour) | H100 | B200 | Source |
|---|---|---|---|
| Marketplace spot (Vast.ai) | ~$1.73 | — | [Aliteq](https://aliteq.com/h100-vs-b200-rental-cost-2026) |
| Executed-trade index (Ornn OCPI, 13 Oct) | $3.17 | $7.83 | [Ornn](https://data.ornn.com/) |
| Average across 27 / 12 providers (Mercatus, Sept) | $3.84 | $6.39 | [Mercatus](https://www.mercatus-ai.com/blog/gpu-rental-prices) |
| Neocloud on-demand (Lambda) | $2.49–3.99 | ~$6.69 | [Spheron comparison](https://www.spheron.network/blog/gpu-cloud-pricing-comparison-2026/) |
| GCP DWS Flex-start (from 8-GPU VM price) | ~$4.79–5.04 | ~$8.06 | [GCP DWS pricing](https://cloud.google.com/products/dws/pricing) |
| AWS Capacity Block (from 7 Oct) | $5.97 | $14.21 | [FourWeekMBA](https://fourweekmba.com/ai-aws-ec2-capacity-block-rates-october-2026/) |
| AWS on-demand (p5) | ~$6.88 (one source says ~$3.90 after a 2025 cut) | ~$14.24 | [CloudZero](https://www.cloudzero.com/blog/h100-gpu-cost/); [Spheron](https://www.spheron.network/blog/spot-gpu-instances-2026-savings-and-what-breaks/) |

The spreads are large. Neocloud on-demand H100s cost about $2.5–4 per GPU-hour against $5–7 at hyperscalers, and B200s about $6.7–8.6 against $8–14. The hyperscaler premium buys integration (IAM, VPC, compliance and managed services such as Bedrock or Foundry), not faster silicon. Neoclouds get new parts first (CoreWeave had Rubin first) and often sell in 8-GPU node bundles; CoreWeave's HGX H100 node lists at $49.24/hour ([CloudZero on CoreWeave](https://www.cloudzero.com/blog/coreweave-pricing/)). But egress fees, minimum commitments and term contracts can change the real cost more than the headline rate does ([Spheron comparison](https://www.spheron.network/blog/gpu-cloud-pricing-comparison-2026/)). The resulting decision ladder:

- **Deadline-bound training:** a Capacity Block or Calendar reservation. But after the 2026 hikes, AWS B200 and B300 blocks ($14–16) can cost more than neocloud on-demand ($6–9).
- **Fault-tolerant batch work and fine-tunes:** Flex-start or spot.
- **A steady inference fleet:** commitments.
- **Everything:** keep the stack portable (containers plus Kubernetes or Slurm) so you can multi-source across two or three providers.

Autoscaling GPU workloads is mostly a fight against cold start. Image pull, weight download, loading into HBM, and compilation or CUDA-graph capture add up to tens of seconds or minutes. Three autoscalers handle the scaling itself:

- **Kubernetes Cluster Autoscaler** counts only GPU requests on GPU nodes and uses a **default scale-down threshold of 0.5**. An 8-GPU node with three GPUs requested is therefore a scale-down candidate, which can make a bin-packed inference fleet thrash ([Cluster Autoscaler FAQ](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md)).
- **Karpenter** on AWS watches an SQS interruption queue and provisions a replacement in parallel while it drains a spot node ([Karpenter disruption docs](https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/docs/concepts/disruption.md)).
- **KEDA** scales event-driven workloads to and from zero ([KEDA](https://github.com/kedacore/keda)).

Serverless GPU platforms package the cold-start mitigations. Modal caches weights and vLLM compilation artifacts in Volumes, which cuts startup "to about ten seconds when loaded from the cache," and it offers experimental GPU memory snapshots ([Modal vLLM example](https://github.com/modal-labs/modal-examples/blob/main/06_gpu_and_ml/llm-serving/vllm_inference.py); [Modal GPU snapshot example](https://github.com/modal-labs/modal-examples/blob/main/06_gpu_and_ml/gpu_snapshot.py)). RunPod bills worker start time but not image pull, defaults to a 5-second idle timeout, and offers FlashBoot and minimum active workers ([RunPod pricing](https://github.com/runpod/docs/blob/main/serverless/pricing.mdx); [RunPod overview](https://github.com/runpod/docs/blob/main/serverless/overview.mdx)). Google Cloud Run now bills GPUs per second: **an L4 works out to about $0.67/hour and an RTX PRO 6000 to about $1.31/hour**. Google's worked example puts an L4 service that peaks at two instances at about $822/month ([Cloud Run pricing](https://cloud.google.com/run/pricing)). The break-even logic is simple. One always-warm H100 replica costs roughly $1.8k–5k a month, so scale-to-zero pays only when traffic is spiky and a queue can hide the cold start.

### Containers and orchestration: Kubernetes absorbed the GPU, but gang scheduling still rides on add-ons

The mental model to hold is that the host owns the kernel driver, the image carries the CUDA user-space libraries, and the NVIDIA Container Toolkit injects the device nodes and host driver libraries when a container starts. Since 2025 it does this through the **Container Device Interface (CDI), which has been the default since GPU Operator 25.10**. One gotcha follows: workloads that rely on the `NVIDIA_VISIBLE_DEVICES` environment variable must now set `runtimeClassName: nvidia` ([GPU Operator release notes](https://github.com/NVIDIA/cloud-native-docs/blob/main/gpu-operator/release-notes.rst)). Toolkit v1.20.1 (19 September 2026) adds per-GPU CUDA memory limits, which require R615+ drivers; GPU Operator 26.7.1 exposes them through `NVIDIA_GPU_MEMORY_REQUEST` and `NVIDIA_GPU_MEMORY_LIMIT` ([NVIDIA Container Toolkit releases](https://github.com/NVIDIA/nvidia-container-toolkit/releases)). Security matters here too. **CVE-2025-23266 ("NVIDIAScape") is a CVSS 9.0 container escape fixed in toolkit 1.17.8 and GPU Operator 25.3.2**, so any cluster on an older version has a critical exposure ([NVIDIA security bulletin](https://nvidia.custhelp.com/app/answers/detail/a_id/5659/~/security-bulletin:-nvidia-container-toolkit---july-2025)).

The biggest packaging change came in **Kubernetes 1.36, which made OCI image volumes stable**. The kubelet can now mount model weights from a registry as a digest-pinned volume, separate from the application image; this needs containerd 2.1 or later ([Kubernetes v1.36 release](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-36-release/index.md); [arXiv 2607.16596](https://arxiv.org/html/2607.16596v1)). The rule that follows: bake small models (under 1–2 GB) into the image, and mount multi-gigabyte weights from image volumes, node-local NVMe caches, or Lustre or object-storage volumes. A 100 GB layer per model version slows every rebuild and pull and defeats registry deduplication.

GPU allocation is in transition. The classic device plugin, which exposes the `nvidia.com/gpu` extended resource, is still the most widely deployed path. It has one well-known gotcha: a pod that requests no GPUs on a GPU node sees *all* of them ([NVIDIA k8s-device-plugin](https://github.com/NVIDIA/k8s-device-plugin)). There are three ways to share a GPU:

- **Time-slicing:** no memory isolation and a shared fault domain, so use it only for development and notebooks.
- **MPS:** gives each client an equal fraction of memory. It is still experimental and does not work on MIG devices.
- **MIG:** hardware isolation with up to seven instances per GPU. This is the right choice for multi-tenant production inference.

Meanwhile **DRA reached general availability in Kubernetes 1.34** ([Kubernetes blog](https://kubernetes.io/blog/2025/09/01/kubernetes-v1-34-dra-updates/)). Kubernetes 1.37 (26 August 2026) made two more DRA features stable. The first is the extended-resource bridge: tenants keep requesting `nvidia.com/gpu` while a DRA driver serves the request underneath. The second is device taints with a cluster-wide `DeviceTaintRule`, which lets operators fence off a bad GPU natively ([Kubernetes v1.37 DRA updates](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-dra-updates.md)). NVIDIA donated its DRA driver to the CNCF at KubeCon EU 2026 ([NVIDIA](https://blogs.nvidia.com/blog/nvidia-at-kubecon-2026/)). The driver's README, though, says only **ComputeDomains (multi-node NVLink for GB200-class racks) are officially supported; per-GPU allocation through DRA is "not yet officially supported"** ([k8s-dra-driver-gpu](https://github.com/NVIDIA/k8s-dra-driver-gpu)). In practice: use the device plugin for whole-GPU pods today, and DRA wherever NVL72 racks require it.

Gang scheduling (starting every pod of a job together or not at all) is still bolted on. Kubernetes' native Workload/PodGroup API reached Beta in 1.37, but **the `GenericWorkload` feature gate is off by default**. JobSet integration is targeted for 1.38, and Kueue does not integrate with it yet. Some outlets wrongly reported it as on by default ([Kubernetes v1.37 workload-aware scheduling](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-advancing-workload-aware-scheduling.md)). The production path is add-ons:

- **Kueue** v0.20.1 (8 October 2026) handles quota, admission, fair sharing, topology-aware placement and multi-cluster dispatch. Its v0.20.0 release stopped serving the v1beta1 API, so migrate your objects before upgrading ([Kueue releases](https://github.com/kubernetes-sigs/kueue/releases)).
- **JobSet** runs a group of Jobs as one unit, with failure and success policies ([JobSet](https://github.com/kubernetes-sigs/jobset)).
- **LeaderWorkerSet** handles inference replicas that span several hosts. It offers all-or-nothing group restart and a new DisaggregatedSet for prefill/decode serving, co-designed with llm-d ([LWS](https://github.com/kubernetes-sigs/lws)).
- **Volcano** (CNCF incubating) and **NVIDIA's KAI Scheduler** (CNCF sandbox, from Run:ai) supply gang scheduling, hierarchical queues and topology-aware placement ([Volcano](https://github.com/volcano-sh/volcano); [KAI Scheduler](https://github.com/NVIDIA/KAI-Scheduler)).

| Need | Default choice in October 2026 | Why |
|---|---|---|
| Whole-GPU training or serving pod | Device plugin, `nvidia.com/gpu` | Most mature and widely supported |
| Multi-node NVLink on GB200/GB300 racks | NVIDIA DRA driver ComputeDomains | The only officially supported DRA path |
| Quota, queueing, fair share across teams | Kueue v0.20.x | Admits Jobs, JobSets, TrainJobs and RayJobs |
| Multi-node training job | JobSet, Kubeflow TrainJob, or Slurm | Gang semantics, stable hostnames, restart policies |
| Inference replica spanning several hosts | LeaderWorkerSet | Group restart and group rolling updates |
| LLM-aware load balancing | Gateway API Inference Extension with llm-d | Routes on KV-cache use and queue depth |
| Researcher batch at 1,000+ GPUs | Slurm, or Slurm on Kubernetes via Slinky | Whole-node gangs, fair-share accounting |

The managed Kubernetes services have productized GPU node lifecycle. **EKS Auto Mode cut its GPU management fees from 1 July 2026 (35% for G-series, 60% for P-series and Trainium)** and includes accelerator-aware node repair ([AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-eks-auto-mode-gpu-price/)). Its node monitoring agent sets an `AcceleratedHardwareReady` condition, and repair starts 10 minutes after a fault is detected, respecting PodDisruptionBudgets ([AWS containers blog](https://aws.amazon.com/blogs/containers/how-to-run-ai-model-inference-with-gpus-on-amazon-eks-auto-mode)). GKE Autopilot provisions B200, H200, H100 and A100 nodes through ComputeClasses ([GKE docs](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/autopilot-gpus)). GKE Inference Gateway integrates llm-d scheduling and multi-cluster routing; Google's benchmark claims for it are vendor-reported ([Google Cloud blog](https://cloud.google.com/blog/topics/ai-infrastructure/whats-new-in-ai-infrastructure-this-month)). The upstream Gateway API Inference Extension it implements has declared itself GA, and its endpoint picker has moved into the llm-d repositories ([Gateway API Inference Extension](https://github.com/kubernetes-sigs/gateway-api-inference-extension)). AKS offers the KAITO add-on, which needs Ampere-generation or newer GPUs ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/aks/ai-toolchain-operator)). SageMaker HyperPod runs on either EKS or Slurm and adds deep health checks, automatic node recovery and Kueue-based task governance ([HyperPod CLI](https://github.com/aws/sagemaker-hyperpod-cli)).

Above Kubernetes, three systems matter:

- **Ray** became a PyTorch Foundation project in October 2025 ([PyTorch Foundation](https://pytorch.org/blog/pytorch-foundation-welcomes-ray-to-deliver-a-unified-open-source-ai-compute-stack/)). **Ray 2.59.0 (2 October 2026) made Ray Data LLM and Ray Serve LLM GA** and turned token authentication on by default for local clusters ([Ray releases](https://github.com/ray-project/ray/releases)). That this default arrived only now says a lot about Ray's historical security posture: never expose a Ray dashboard or job API to the internet. KubeRay 1.7 added incremental RayService upgrades and deprecated `ray.io/v1alpha1` ([KubeRay releases](https://github.com/ray-project/kuberay/releases)). Use Ray for mixed CPU/GPU Python pipelines: batch embedding, RL rollouts, sweeps, multi-model serving. For fixed-shape SPMD pretraining (every GPU running the same step in lockstep), torchrun with JobSet or Slurm is simpler.
- **Kubeflow** reorganized. **Trainer v2 (TrainJob on top of JobSet; v2.3.0 in August 2026) supersedes Training Operator v1**, which now gets only bug fixes ([Kubeflow Trainer releases](https://github.com/kubeflow/trainer/releases)). Kubeflow Pipelines is at 2.17.2; version 2.15 replaced MinIO with SeaweedFS as the default object store and removed the ML Metadata (MLMD) store ([KFP releases](https://github.com/kubeflow/pipelines/releases)). KServe v0.21 (25 September 2026) is now LLM-centric, with `LLMInferenceService`, KEDA scaling and DRA claims ([KServe releases](https://github.com/kserve/kserve/releases)).
- **Slurm** remains the scheduler of choice for large training clusters. **NVIDIA acquired SchedMD in December 2025** and pledged to keep Slurm open source and vendor-neutral. NVIDIA says Slurm runs on more than half of the top-10 and top-100 TOP500 systems ([Network World](https://www.networkworld.com/article/4106930/nvidia-moves-deeper-into-ai-infrastruct-with-schedmd-acquisition.html)). The Slinky slurm-operator runs the Slurm controller and worker daemons as Kubernetes custom resources. It drains workers in Slurm before Kubernetes terminates them and can scale to zero ([Slinky slurm-operator](https://github.com/SlinkyProject/slurm-operator)).

The pragmatic split is Slurm for large pretraining and researcher batch work, Kubernetes for inference and data pipelines, and hybrids such as Slinky to share one GPU pool. Note one vendor-neutrality issue: NVIDIA now shapes Slurm, KAI and Dynamo, and wrote the DRA driver it donated.

Health handling has native pieces but vendor glue. Kubernetes 1.36 promoted per-device health in pod status (`allocatedResourcesStatus`) to Beta ([Kubernetes v1.36](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-36-release/index.md)). Kubernetes 1.37 made DRA device taints stable and added node lifecycle conditions as alpha; nothing in core acts on those conditions yet ([Kubernetes node lifecycle conditions](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-node-lifecycle-conditions.md)). The automation that actually cordons and replaces bad GPUs still comes from managed services (EKS repair, HyperPod deep health checks) or from DCGM-based tooling that you wire to Kueue or Slurm.

### Data and storage: object storage holds the truth, everything else is a rebuildable projection

Regional object storage is the durable source of truth for nearly all AI data. S3 has been strongly consistent for reads after writes since December 2020 ([AWS](https://aws.amazon.com/about-aws/whats-new/2020/12/amazon-s3-now-delivers-strong-read-after-write-consistency-automatically-for-all-applications)). It scales by parallelism across key prefixes: **at least 3,500 writes and 5,500 reads per second per partitioned prefix**. After a sudden spike, S3 re-partitions automatically; until it finishes, clients get 503 "Slow Down" errors and must retry with backoff ([AWS knowledge center](https://repost.aws/knowledge-center/s3-object-key-naming-pattern)). Each hyperscaler now also sells a low-latency zonal tier for data that sits next to accelerators:

- **S3 Express One Zone** cut prices in April 2025 (storage −31%, PUTs −55%, GETs −85%) and handles up to 2 million GETs per second per directory bucket ([AWS News Blog](https://aws.amazon.com/es/blogs/aws/up-to-85-price-reductions-for-amazon-s3-express-one-zone/)).
- **GCS Rapid Storage** offers sub-millisecond latency, up to 15 TB/s aggregate throughput, 20 million queries per second, and appendable objects, which suit checkpoints and logs ([GCS Rapid docs](https://docs.cloud.google.com/storage/docs/rapid/high-performance-storage)).

Google's reference pattern makes the hierarchy explicit: the regional bucket is the durable copy, and the zonal layer is a fast cache or scratch space ([GCS AI zones](https://docs.cloud.google.com/storage/docs/ai-zones)). Because these tiers live in a single availability zone, they should hold only data you can recreate.

For training input, shard the data into sequential objects of 100 MB to 1 GB. **Sequential 100 MB reads reach about 80% of object-store bandwidth, while random 1 KB reads reach about 1%** ([ZeroEntropy](https://zeroentropy.dev/concepts/streaming-datasets/)). MosaicML StreamingDataset (the MDS format) streams shards from any major cloud and supports deterministic, resumable multi-node training ([PyPI: mosaicml-streaming](https://pypi.org/project/mosaicml-streaming)); WebDataset tar shards are the simpler alternative. Text LLM pretraining is rarely I/O-bound: 15T tokens stored as 2-byte ids is about 30 TB per epoch. Storage strain comes from multimodal and video data, small-file random access, and checkpoint bursts. Network egress is what usually decides storage cost. Entry-level internet egress runs about $0.09/GB on AWS, $0.087 on Azure and $0.12 on GCP's Premium tier, against $0 on Cloudflare R2 ([eCorpIT](https://ecorpit.com/cloud-egress-fees-ai-inference-bill-comparison-2026/)). The hyperscalers waive egress only for customers leaving their platform ([The Register](https://www.theregister.com/2025/09/10/big_clouds_scramble_over_eu/)). Moving a 100 TB dataset out of AWS therefore costs roughly $8–9k, which matters if you plan to chase GPU capacity across clouds.

Managed Lustre is now the standard fast POSIX file tier on all three clouds:

- **FSx for Lustre** reaches **1,200 Gbps per client with EFA plus GPUDirect Storage**. Its Intelligent-Tiering file systems provision up to 2 TB/s of throughput independently of capacity ([FSx Lustre performance](https://docs.aws.amazon.com/fsx/latest/LustreGuide/performance.html); [FSx throughput capacity](https://docs.aws.amazon.com/fsx/latest/LustreGuide/managing-throughput-capacity.html)).
- **Google Cloud Managed Lustre** went GA on 30 June 2025, with tiers of 125 to 1,000 MB/s per TiB and up to 10 TB/s in aggregate (documentation versions disagree on the maximum) ([GCP Managed Lustre tiers](https://docs.cloud.google.com/managed-lustre/docs/performance-tiers)).
- **Azure Managed Lustre** offers tiers of 40 to 500 MB/s per TiB ([Azure pricing](https://www.azure.cn/en-us/pricing/details/managed-lustre/index.html)).

You need a parallel file system in four cases: small files or random reads you cannot re-shard, very high aggregate bandwidth (video training), fast synchronous checkpoints, or HPC-style shared scratch. Otherwise object storage plus streaming is cheaper. The checkpoint math explains why it matters for training. A full training state at about 16 bytes per parameter is about 1.1 TB for a 70B model. Writing it takes about 10 seconds at 100 GB/s, but about 100 seconds of idle GPUs at 10 GB/s. Per-TiB throughput pricing also often forces you to buy capacity just to get bandwidth: a 50 TB working set that needs 50 GB/s requires the 1,000 MB/s/TiB tier. The usual pattern is to keep the master copy in object storage and run Lustre as a hydrated cache for the duration of a job, then tear it down.

Lakehouses are where curated training data, evaluation sets, features and traces live. **Apache Iceberg v3 added deletion vectors, row lineage and a VARIANT type**, and the upgrade is one-way ([Google Open Source Blog](https://opensource.googleblog.com/2025/08/whats-new-in-iceberg-v3.html?m=0)). Databricks Unity Catalog supports v3 on Databricks Runtime 18 LTS and later, with Delta interoperability ([Databricks](https://www.databricks.com/en/blog/iceberg-v3-moving-ecosystem-towards-unification)), and Snowflake reportedly made v3 GA on 7 May 2026 ([Atlan](https://atlan.com/know/snowflake/apache-iceberg-v3/)). With file formats converging, lock-in has moved to the catalog and governance layer. Each platform now bundles AI features next to the data. BigQuery's `VECTOR_SEARCH` supports IVF indexes and ScaNN-based TreeAH indexes, plus in-SQL `AI.EMBED` ([BigQuery vector index docs](https://docs.cloud.google.com/bigquery/docs/vector-index)). Databricks launched Lakebase, a managed Postgres built on Neon ([Databricks](https://www.databricks.com/company/newsroom/press-releases/databricks-launches-lakebase-new-class-operational-database-ai-apps)), and agreed in August 2025 to acquire Tecton for real-time features ([Perficient](https://blogs.perficient.com/2025/09/26/databricks-acquires-tecton/)). Design every vector index and online feature store as a rebuildable projection of lakehouse tables. Watch retention, too: Delta's default 7-day retention for deleted files, alongside a 30-day log retention, is too short for ML reproducibility, so set both to cover your lookback window ([Databricks VACUUM docs](https://docs.databricks.com/aws/sql/language-manual/delta-vacuum)).

Vector search trades recall for speed and memory. Three index families matter:

- **HNSW**, an in-RAM proximity graph, is the low-latency default.
- **IVF with product quantization (PQ)** compresses vectors to cut memory.
- **DiskANN** keeps the graph and full vectors on SSD. It **indexes a billion points on a workstation with 64 GB of RAM at over 95% recall@1 and under 5 ms latency** ([DiskANN paper](https://www.cs.utexas.edu/~rak/papers/neurips19-diskann.pdf)).

The products have split into cold object-backed tiers, provisioned hot serving, vectors inside existing databases, and search platforms with built-in hybrid search and reranking. The 2025–26 releases worth knowing:

- **Amazon S3 Vectors** went GA on 2 December 2025, with up to 2 billion vectors per index, about 100 ms warm queries and top-k capped at 100 ([AWS News Blog](https://aws.amazon.com/blogs/aws/amazon-s3-vectors-now-generally-available-with-increased-scale-and-performance)). AWS positions OpenSearch as the hot tier in front of it ([S3 Vectors](https://aws.amazon.com/s3/features/vectors)).
- **Pinecone** made Dedicated Read Nodes GA on 15 April 2026 for steady workloads ([Pinecone](https://pinecone.io/newsroom/zoominfo-pinecone-drn/)).
- **pgvector** 0.8 added iterative index scans, which fix HNSW queries with selective filters returning fewer rows than the LIMIT ([pgvector guide](https://tessl.io/registry/skills/github/timescale/pg-aiguide/pgvector-semantic-search)).
- **Milvus** 2.6 added hot/cold tiered storage and writes directly to object storage ([BigDATAwire](https://www.bigdatawire.com/this-just-in/zilliz-releases-milvus-2-6-with-tiered-storage-and-int8-compression-to-cut-vector-search-costs)).
- **Qdrant** 1.16 added ACORN for filtered search ([Qdrant](https://qdrant.tech/blog/qdrant-1.16.x/index.md)).
- **Elastic** DiskBBQ performs well up to about 95% recall ([Elastic](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/bbq)).
- **Vertex AI Vector Search 2.0** went GA on 5 March 2026 with hybrid search and built-in semantic reranking ([Vertex AI release notes](https://docs.cloud.google.com/vertex-ai/docs/release-notes)).

Filtered search is the most common production failure: queries return fewer than k results, or recall collapses under selective filters. Test with your real filter selectivity. The vendor benchmarks (pgvectorscale's 2024 comparison with Pinecone, Pinecone's "97% lower costs", AWS's "90%") are not comparable with each other, so run your own test of recall@k against p99 latency against cost ([TigerData](https://www.tigerdata.com/blog/pgvector-is-now-as-fast-as-pinecone-at-75-less-cost)). The standard retrieval stack runs BM25 and vector search in parallel, fuses the two lists with Reciprocal Rank Fusion (RRF, k ≈ 60), then applies a cross-encoder reranker ([RRF paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)).

| Situation | Sensible vector store choice |
|---|---|
| Up to roughly 10–50M vectors, already on Postgres, need joins and filters | pgvector with halfvec and iterative scans; pgvectorscale or AlloyDB as you grow |
| Billions of vectors, low QPS, cost-dominated (archives, agent memory) | S3 Vectors, optionally fronted by OpenSearch |
| Spiky traffic and no ops team | Pinecone serverless, Zilliz Serverless or Qdrant Cloud |
| Steady high QPS | Provisioned capacity (Pinecone Dedicated Read Nodes, dedicated clusters) |
| Self-hosted at large scale; filter-heavy multi-tenant SaaS | Milvus; Qdrant |
| Data already in the lakehouse or warehouse | Databricks Vector Search, BigQuery `VECTOR_SEARCH` (batch), Snowflake Cortex Search |
| Single-cloud enterprise RAG needing hybrid search and reranking | Vertex AI Vector Search 2.0 or Azure AI Search |

Embedding storage cost scales with dimensions times bytes. **A float32 vector takes 4 × d bytes, so 10 million 1536-d vectors take about 61 GB as float32, 15 GB as int8, and 1.9 GB as binary.** A June 2026 neutral benchmark measured average retrieval-quality drops of **1.95 points for int8 and 6.50 points for binary** ([HAKARI-Bench](https://arxiv.org/pdf/2606.22778)). You can recover most of the binary loss by oversampling candidates and rescoring them with full-precision vectors. Matryoshka-style truncation compounds the savings: int8 at 256 dimensions takes 256 bytes per vector, against 2 KB for int8 at 2048 dimensions ([MongoDB/Voyage](https://www.mongodb.com/docs/voyageai/tutorials/dimensions-and-quantization/)). A practical recipe:

1. Pick an embedding model trained with Matryoshka representation learning (MRL).
2. Store full-precision vectors cheaply, in object storage or a lakehouse column.
3. Index a truncated, quantized copy in RAM.
4. Oversample 3–10× and rescore with the full vectors.
5. Rerank the survivors with a cross-encoder.
6. Measure recall on your own data.

Switching embedding models means re-embedding and re-indexing everything, which is another reason to keep source text and chunk metadata in the lakehouse.

Four other data concerns round out the layer:

- **Feature stores** must guarantee point-in-time correctness: join each training label only with feature values timestamped at or before the label's event time. Otherwise future information leaks into training and the model sees different data at training and serving time.
- **Dataset versioning** consolidated when lakeFS acquired DVC on 18 November 2025 ([lakeFS](https://lakefs.io/blog/lakefs-acquires-dvc/)). Pin every training run to a table snapshot ID.
- **Streaming ingestion** follows one pattern: change-data capture into Kafka, Kinesis or Pub/Sub, then Flink, then upserts into the vector database or online store, with a copy landed in Iceberg for training and rebuilds. The biggest industry event here was IBM's agreement to buy Confluent for about $11B, announced 8 December 2025 ([MarketScreener](https://www.marketscreener.com/news/international-business-machines-corporation-entered-into-a-definitive-agreement-to-acquire-confluent-ce7d51d2d988f220)).
- **Governance** applies to derived data too. Embeddings and chunks count as personal data if their source did. Retrieval needs per-user ACL filters. Deletion requests must reach snapshots, indexes and backups, and purging data from fine-tuned weights is practically infeasible, which is the strongest argument for not training on raw PII.

## The model layer: training and serving are data-movement problems

Once hardware and data are in place, the two core workloads behave the same way underneath. Training is limited by how much state fits in memory and how fast gradients cross the network. Serving is limited by how many bytes each decode step must read.

### Training at scale: 16 bytes per parameter and an interruption every three hours

The ZeRO paper's ledger is still the standard reference. In mixed-precision Adam, each parameter carries 2 bytes of FP16/BF16 weights, 2 bytes of gradients and 12 bytes of FP32 optimizer state (a master copy of the weights plus momentum and variance), for **16 bytes per parameter** before activations ([ZeRO, SC20](https://aiichironakano.github.io/cs596/Rajbhandari-ZeRO-SC20.pdf)). ZeRO-Infinity also counts an FP32 copy of the gradients and arrives at 20 bytes ([ZeRO-Infinity](https://arxiv.org/pdf/2104.07857)). At 16 bytes:

- a 7B model needs 112 GB;
- a 70B model needs 1.12 TB;
- sharding that 70B state with ZeRO-3/FSDP across 64 GPUs brings it to 17.5 GB per GPU.

Taking a 7.5B model across 64 data-parallel ranks, each ZeRO stage shrinks per-GPU state from 120 GB to 31.4 GB (stage 1, shard optimizer state), 16.6 GB (stage 2, also shard gradients) and 1.9 GB (stage 3, also shard weights).

Compute follows **training FLOPs ≈ 6 × parameters × tokens**. A 7B model on 2T tokens needs 8.4 × 10²² FLOPs, about 59,000 H100-hours at 40% model-FLOPs utilization (MFU), or about 2.4 days on 1,024 GPUs. Two published runs give reference points:

- **Meta's Llama 3 405B** trained on up to 16K H100s ([Llama 3 paper](https://arxiv.org/pdf/2407.21783)).
- **DeepSeek-V3** (671B total parameters, 37B active) trained on 14.8T tokens in **2.788M H800 GPU-hours, about $5.576M at an assumed $2/GPU-hour**. That figure covers only the official run, not ablations ([DeepSeek-V3 report](https://arxiv.org/pdf/2412.19437)).

Applying 6ND to DeepSeek gives about 330 TFLOP/s per GPU. That is roughly 33% of the H800's BF16 peak or 17% of its FP8 peak, depending on which peak you divide by. TorchTitan's authors warn that MFU numbers from FP8 runs are not comparable with BF16 MFU ([TorchTitan, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/e6231c5f46598cfd09ff1970524e0436-Paper-Conference.pdf)). Activation memory usually dominates at long context. Activation recomputation saves memory but raises compute from about 6ND to about 8ND ([Scaling Book: transformers](https://github.com/jax-ml/scaling-book/blob/main/transformers.md)). That raises hardware FLOPs utilization while leaving MFU unchanged.

The parallelism strategies map onto the network from innermost to outermost:

- **Tensor parallelism (TP, plus sequence parallelism)** all-reduces activations several times per layer on the critical path, so it must stay on NVLink. On 8-GPU nodes that caps TP at 8; NVL72 lets TP and expert parallelism span 72 GPUs.
- **Context parallelism (CP) and expert parallelism (EP)** come next, for long sequences and MoE models respectively.
- **Pipeline parallelism (PP)** sends only the activations at stage boundaries, point to point, so it tolerates the slower scale-out network.
- **Data parallelism with FSDP sharding** goes outermost, because its gradient reduce-scatters and parameter all-gathers overlap with compute.

Pipelines waste time in "bubbles". Under the common 1F1B schedule the idle fraction is **(p−1)/(m+p−1)** for p stages and m micro-batches, so 8 stages with 32 micro-batches idle about 18% of the time. Interleaved schedules shrink that by the number of model chunks per GPU. Zero Bubble's ZB1P cuts it to about a third of 1F1B's, and ZB2P approaches zero at roughly twice the activation memory ([Zero Bubble](https://arxiv.org/pdf/2401.10241)). DeepSeek's DualPipe also hides MoE all-to-all traffic behind compute ([DeepSeek-V3 report](https://arxiv.org/pdf/2412.19437)). FSDP2 shards per parameter on DTensor. Over already-optimized baselines, TorchTitan's composed parallelism added 65% throughput for an 8B model on 128 GPUs, 12.6% for 70B on 256 GPUs, and 30% for 405B on 512 GPUs ([TorchTitan](https://proceedings.iclr.cc/paper_files/paper/2025/file/e6231c5f46598cfd09ff1970524e0436-Paper-Conference.pdf)). Megatron Bridge 0.6 (August 2026) trained GLM-5.2 at 128K context using context parallelism ([Megatron Bridge](https://github.com/NVIDIA-NeMo/Megatron-Bridge)). Note that FSDP/ZeRO-3 moves about 50% more network traffic than plain data parallelism. Hybrid sharding (shard within the fast domain, replicate across it) is the usual compromise on cloud networks.

The networking gap behind those placement rules is about **18–36×**: NVLink 5 delivers about 1.8 TB/s per GPU, while every major cloud gives about **400 Gb/s (≈50 GB/s) per GPU** across nodes. Ring all-reduce moves 2(N−1)/N of the message per GPU regardless of GPU count, which makes it bandwidth-optimal for large messages; tree algorithms win on small, latency-bound ones. NCCL does not always choose well. On GB200 NVL72 partitions spanning racks, tree reached **485.68 GB/s against ring's 393.66 GB/s at 24 GPUs** even though NCCL picked ring ([NVIDIA/nccl issue #1801](https://github.com/NVIDIA/nccl/issues/1801)). The three clouds reach the same per-GPU bandwidth with different fabrics:

- **AWS** gives P5 and P5en instances 3,200 Gbps of EFA, and P6e-GB200 UltraServers 28.8 Tb/s of EFAv4 in total across 72 GPUs ([AWS EC2 docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa-acc-inst-types.html); [AWS P6](https://aws.amazon.com/ec2/instance-types/p6)).
- **GCP** gives A3 Ultra and A4 3.2 Tb/s of non-blocking RoCE with GPUDirect RDMA, and A3 Mega 1,800 Gbps via GPUDirect-TCPXO. **GPUDirect RDMA is incompatible with the TCPX/TCPXO plugins**, so don't install them on RDMA clusters ([GCP GPU network bandwidth](https://docs.cloud.google.com/compute/docs/gpus/gpu-network-bandwidth); [GKE GPUDirect-TCPX](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/gpu-bandwidth-gpudirect-tcpx)).
- **Azure** uses NVIDIA InfiniBand.

Each fabric needs its own NCCL plugin and environment variables, and a misconfigured plugin is a common cause of slow training. The stakes are easy to compute. A 7B model's BF16 gradients total 14 GB, so a ring all-reduce moves about 28 GB per GPU per step. That takes 0.56 seconds at 50 GB/s if not overlapped, against 0.06 seconds over NVLink.

On numeric precision, **BF16 with FP32 master weights is the default** and needs no loss scaling. **FP8 is proven at frontier scale.** DeepSeek-V3 used fine-grained scaling: 1×128 tiles for activations and 128×128 blocks for weights ([DeepSeek-V3 report](https://arxiv.org/pdf/2412.19437)). **4-bit training is now real.** NVIDIA's NVFP4 recipe trained a 12B hybrid Mamba-Transformer on 10T tokens with MMLU-Pro of 62.58%, against 62.62% for FP8. The recipe relies on random Hadamard transforms, two-dimensional block quantization, stochastic rounding, and a few layers kept in higher precision ([NVFP4 paper](https://arxiv.org/pdf/2509.25149)). Nemotron 3 was pretrained in NVFP4 for up to 25T tokens ([Nemotron 3](https://arxiv.org/pdf/2512.20856)). NVIDIA reports that MXFP4 needs 36% more tokens than NVFP4 to reach the same loss ([NVIDIA Research](https://research.nvidia.com/labs/eai/blogs/pushing-intelligence-to-4-bit/)). Optimizer states typically stay in FP32, so lower precision mainly speeds up matrix multiplies; it barely shrinks the 16-byte ledger. BF16 is the safe baseline, FP8 the mainstream speedup on Hopper and Blackwell, and NVFP4 the Blackwell frontier, still lightly tested outside NVIDIA's own runs.

Reliability is now a design input, not an afterthought. Over a 54-day snapshot of Llama 3 training on 16K H100s, Meta logged **466 job interruptions, 419 of them unexpected**. About 78% of the unexpected ones were confirmed or suspected hardware faults, and GPU issues alone were 58.7%. Even so, the run kept **over 90% effective training time**, and only three interruptions needed significant manual intervention ([Llama 3 paper](https://arxiv.org/pdf/2407.21783); [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/faulty-nvidia-h100-gpus-and-hbm3-memory-caused-half-of-the-failures-during-llama-3-training-one-failure-every-three-hours-for-metas-16384-gpu-training-cluster)). That is a mean time between failures of about 3.1 hours. If failures scale linearly with GPU count, a 100K-GPU job would see one about every 30 minutes.

The **Young/Daly rule sets the checkpoint interval at W ≈ √(2 × MTBF × C)**, where C is the cost of one checkpoint ([Benoit et al.](https://dl.acm.org/doi/pdf/10.1145/3549206.3549328)). Wasted time at that optimum is roughly √(2C/MTBF). With Meta's 186-minute MTBF:

- a 5-minute blocking checkpoint implies one every 43 minutes, wasting about 23% of the run;
- a 6-second asynchronous checkpoint implies one every 6 minutes, wasting about 3%.

So the levers are clear. Cut C with asynchronous distributed checkpointing: PyTorch reported more than 10× faster checkpointing, then about 19× with sub-second blocking once the GPU-to-CPU copy overlaps compute ([PyTorch blog](https://pytorch.org/blog/reducing-checkpointing-times/); [PyTorch forums](https://discuss.pytorch.org/t/distributed-w-torchtitan-optimizing-checkpointing-efficiency-with-pytorch-dcp/211250)). A known race condition can corrupt async saves, so verify your loads ([torchtitan #930](https://github.com/pytorch/torchtitan/issues/930)). Cut restart time with hot spares and automatic node replacement. Cut lost work with in-memory replicas. Raise MTBF with burn-in and health checks. AWS packaged several of these levers: **SageMaker HyperPod's checkpointless training (December 2025) recovers from healthy accelerators' in-memory state**. AWS claims over 95% goodput on clusters with thousands of accelerators and 80–93% lower recovery time, and pairs it with elastic training that scales jobs around higher-priority work ([AWS What's New](https://aws.amazon.com/about-aws/whats-new/2025/12/amazon-sagemaker-hyperpod-checkpointless-training); [AWS News Blog](https://aws.amazon.com/blogs/aws/introducing-checkpointless-and-elastic-training-on-amazon-sagemaker-hyperpod)).

The framework landscape has settled into two families:

- **PyTorch-native:** FSDP2, DTensor, torchtitan and distributed checkpointing.
- **NVIDIA's Megatron Core:** packaged through Megatron Bridge (v0.6.0, August 2026, with conversion to and from Hugging Face checkpoints), plus NeMo AutoModel (v0.6.0) for fine-tuning Hugging Face models on day zero ([Megatron Bridge](https://github.com/NVIDIA-NeMo/Megatron-Bridge); [NeMo AutoModel](https://pypi.org/project/nemo-automodel/)).

JAX with MaxText remains the TPU path. Meta's torchtune stopped active development in 2025 ([torchtune issue #2883](https://github.com/meta-pytorch/torchtune/issues/2883)).

For fine-tuning, **QLoRA fits a 65B model on a single 48 GB GPU, against more than 780 GB for 16-bit full fine-tuning**, provided LoRA is applied to all linear layers ([QLoRA](https://arxiv.org/pdf/2305.14314)). The standard post-training pipeline is supervised fine-tuning (SFT), then DPO for preferences, then RL. GRPO, the common RL choice, drops PPO's learned critic and uses a group of sampled responses' mean reward as the baseline ([DeepSeekMath](https://arxiv.org/pdf/2402.03300)). RL at scale has become a distributed-systems problem: it mixes vLLM-style generation with training, so rollout throughput and moving weights between the two dominate cost.

Managed fine-tuning shifted sharply in 2026. **OpenAI is winding down self-serve fine-tuning.** The platform is closed to new users (page updated 8 May 2026), existing customers can reportedly create jobs until 6 January 2027, and fine-tuned models keep serving until their base models are deprecated ([OpenAI](https://developers.openai.com/api/docs/guides/model-optimization); [OpenAI community](https://community.openai.com/t/openai-s-self-serve-fine-tuning-availability/1380481)). AWS moved the other way: Bedrock launched reinforcement fine-tuning on Nova models in December 2025 and extended it to the open-weight qwen3-32b and gpt-oss-20b in February 2026 ([AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/02/amazon-bedrock-reinforcement-fine-tuning-openai/)). Fine-tuned models cannot move between platforms, so choosing a platform means lock-in. For experiment tracking, **Weights & Biases has belonged to CoreWeave since 5 May 2025 (about $1.7B)**. Since 30 September 2026 users sign in through CoreWeave Forge, with contracts and pricing unchanged ([CoreWeave](https://www.coreweave.com/news/coreweave-completes-acquisition-of-weights-biases-2); [CoreWeave W&B page](https://www.coreweave.com/companies/weights-and-biases)). For large runs, log per step: MFU, per-rank step time (to catch stragglers), checkpoint save and load durations, and restart events (to compute goodput).

### Inference and serving: decode is bandwidth-bound, so batching, KV reuse and disaggregation win

LLM inference has two phases with opposite bottlenecks:

- **Prefill** processes the whole prompt in parallel. It is compute-bound and sets **time to first token (TTFT)**.
- **Decode** emits one token per step and must re-read every weight plus the KV cache each step. It is memory-bandwidth-bound and sets **time per output token (TPOT)**, or inter-token latency (ITL). At batch size 1, decode matrix multiplies run at about 1% of peak FLOPS ([Baseten Inference Engineering](https://www.baseten.co/inference-engineering/book/02-models/calculating-inference-bottlenecks/)).

The H100's roofline "ridge point" (989 dense BF16 TFLOPS divided by 3.35 TB/s) is about 295 FLOPs per byte. Batching raises decode's arithmetic intensity roughly in proportion to batch size. A worked bound makes this concrete. A 70B FP8 model on one H100 needs at least 21 ms per decode step (70 GB ÷ 3.35 TB/s), capping a single stream at about 48 tokens/s. At batch 64 the same weight read serves 64 streams, approaching 3,000 tokens/s in aggregate at nearly the same per-user TPOT. Batching therefore adds throughput almost for free until the GPU becomes compute-bound or runs out of KV memory.

The metric that matters is **goodput: the request rate that still meets both the TTFT and TPOT targets**. DistServe, which defined it, served 7.4× more requests or met 12.6× tighter latency targets than the systems it compared against ([DistServe, OSDI '24](https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin)). Always report p50, p90 and p99 TTFT and ITL alongside throughput, because throughput can always be bought with worse tail latency. In MLPerf Inference v6.0 (April 2026), NVIDIA reported a GB300 NVL72 rack at 575,580 tokens/s on DeepSeek-R1 in the latency-constrained Server scenario, and AMD reported an 87-GPU MI355X system at 1.04M tokens/s Offline on Llama 2 70B. Both are vendor-reported ([NVIDIA](https://developer.nvidia.com/blog/nvidia-extreme-co-design-delivers-new-mlperf-inference-records/); [AMD](https://www.amd.com/en/blogs/2026/amd-delivers-breakthrough-mlperf-inference-6-0-results.html)).

KV cache size usually decides how many sequences fit on a GPU. For a Llama-3-70B-class model (80 layers, 8 KV heads under grouped-query attention, head dimension 128), the arithmetic works out as follows:

| KV format | Per token | 8K-token sequence | 128K-token sequence |
|---|---|---|---|
| BF16 | ≈320 KiB | ≈2.5 GiB | ≈40 GiB |
| FP8 | ≈160 KiB | ≈1.25 GiB | ≈20 GiB |
| NVFP4 (~4.5 bits including scales) | ≈90 KiB | ≈0.7 GiB | ≈11 GiB |
| Same model with full multi-head attention (64 KV heads), BF16 | ≈2.5 MiB | ≈20 GiB | ≈320 GiB |

Four lines of work shrink or stretch the cache:

- **Smaller KV per token.** Grouped-query and multi-query attention share KV heads. DeepSeek-V2's multi-head latent attention (MLA) cut KV cache by 93.3% relative to DeepSeek 67B and raised maximum throughput 5.76× ([DeepSeek-V2](https://arxiv.org/html/2405.04434v2)). NVFP4 KV cache is up to 50% smaller than FP8 with under 1% accuracy loss, and FP8 KV is already the production baseline ([NVIDIA](https://developer.nvidia.com/blog/optimizing-inference-for-long-context-and-large-batch-sizes-with-nvfp4-kv-cache/)).
- **Less fragmentation.** PagedAttention delivered 2–4× throughput at the same latency ([vLLM paper](https://arxiv.org/abs/2309.06180)).
- **Reuse across requests.** Prefix caching is on by default in vLLM V1 ([vLLM Ascend release notes](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/release_notes.html)), and SGLang's RadixAttention serves the same purpose.
- **More capacity through tiered offload.** LMCache, presented at MLSys 2026, claims up to 15× throughput on multi-round QA. Its CacheBlend reuses KV for RAG chunks that are not prefixes ([MLSys 2026: LMCache](https://mlsys.org/virtual/2026/oral/3646)). NVIDIA Dynamo's KV Block Manager offloads to CPU memory, SSD and network storage, and supports vLLM and TensorRT-LLM but not SGLang ([Dynamo KVBM](https://docs.nvidia.com/dynamo/components/kvbm)).

On two 80 GB GPUs serving 70B FP8 weights, roughly 70–80 GB remains for KV. That holds about 30 concurrent 8K-token sequences with BF16 KV; FP8 KV doubles it. Prefix caching only pays off when the shared content (system prompt, tool definitions, documents) comes first in the prompt and is byte-identical across requests.

Scheduling evolved from static batching to continuous (iteration-level) batching, then to chunked prefill, and now to disaggregation. Sarathi-Serve's chunked prefill splits long prompts so ongoing decodes never stall. It reported up to 2.6× capacity within latency targets versus vLLM, and up to 5.6× for Falcon-180B with pipeline parallelism ([Sarathi-Serve](https://arxiv.org/pdf/2403.02310)). **Disaggregated serving runs prefill and decode on separate GPU pools** connected by fast KV transfer:

- **NVIDIA Dynamo 1.0**, GA on 16 March 2026, packages disaggregated serving, a KV-aware router, an autoscaling planner, the KV Block Manager and the NIXL transfer library. NVIDIA claims up to 7× on Blackwell; that is a vendor figure ([NVIDIA Newsroom](https://nvidianews.nvidia.com/news/dynamo-1-0)). Documentation exists for v1.3.0 ([Dynamo docs](https://docs.nvidia.com/dynamo/v1.3.0/kubernetes-deployment/request-routing/gateway-api-inference-extension/overview.md)).
- **SGLang** with disaggregation and large-scale expert parallelism reached about 52.3k input and 22.3k output tokens/s per node on 96 H100s serving DeepSeek ([LMSYS](https://lmsys.org/blog/2025-05-05-large-scale-ep/)).
- **llm-d** has been a CNCF Sandbox project since March 2026 ([llm-d](https://github.com/llm-d/llm-d)).
- **Heterogeneous pools** are real: Cerebras's SEC filing describes AWS pairing Trainium3 for prefill with Cerebras CS-3 for decode ([Cerebras 8-K](https://www.sec.gov/Archives/edgar/data/0002021728/000162828026044941/cbrsannouncesfinancialresu.htm)).

Disaggregation pays for long prompts, strict ITL targets, wide-expert-parallel MoE models and high scale. In small deployments, KV transfer overhead and fixed pool ratios hurt, and aggregated serving with chunked prefill stays simpler.

Open-source serving is effectively a three-engine world:

- **vLLM** (0.31.0 on 5 October 2026, releasing roughly every 9 days) has the broadest hardware and model coverage ([PyPI: vllm](https://pypi.org/project/vllm/)).
- **SGLang** leads on prefix-heavy, agentic and RL-rollout workloads, and on large MoE expert parallelism.
- **TensorRT-LLM** removed its TensorRT engine backend; PyTorch is now the only execution backend, and `trtllm-serve <hf_model>` needs no engine-build step ([TensorRT-LLM migration guide](https://nvidia.github.io/TensorRT-LLM/legacy/tensorrt-backend-removal.html)).

**Hugging Face TGI is in maintenance mode**, and Hugging Face itself recommends vLLM, SGLang, llama.cpp or MLX ([TGI README](https://trendshift.io/admin/repository/ask-ai/4188)). KServe became a CNCF incubating project in September 2025 and integrates llm-d through `LLMInferenceService` ([CNCF](https://www.cncf.io/blog/2025/11/11/kserve-becomes-a-cncf-incubating-project/)). Triton remains useful for non-LLM and multi-framework ensembles. Ray Serve and BentoML cover application-level composition, and llama.cpp and Ollama cover local or low-concurrency use.

The 2026 optimization defaults are FP8 weights and activations, NVFP4 as the Blackwell 4-bit format, FP8 KV cache, FlashAttention-4, and speculative decoding where latency matters:

- **NVFP4 quantization:** NVIDIA reports at most 1% accuracy loss when post-training quantizing DeepSeek-R1 to NVFP4 (vendor claim). INT4 weight-only methods (AWQ, GPTQ) remain useful on older GPUs.
- **FlashAttention-4** (MLSys 2026) reaches up to **1,605 TFLOP/s on B200 in BF16 (about 71% utilization)**, 1.3× faster than cuDNN 9.13 and 2.7× faster than Triton. Part of the gain comes from emulating `exp()` with polynomials on the FMA units ([Tri Dao](https://tridao.me/blog/2026/flash4/)).
- **Speculative decoding:** with per-token acceptance rate α and draft length γ, each target forward pass yields (1−α^(γ+1))/(1−α) tokens on average; for α = 0.7 and γ = 5, that is 2.94. EAGLE-3 delivers about 2× on Llama-3.1-8B in vLLM and SGLang ([BentoML](https://bentoml.com/blog/3x-faster-llm-inference-with-speculative-decoding)). One test measured 1.84× on code refactoring but only **0.99× on general chat** ([mohakchugh](https://mohakchugh.is-a.dev/blog/eagle-3-speculative-decoding-training-time-test)), and below α ≈ 0.55 speculation is a net loss ([PremAI](https://blog.premai.io/speculative-decoding-2-3x-faster-llm-inference-2026)).

Speculation spends spare compute to save bandwidth-bound steps. At high batch sizes that spare compute disappears, so enable it for low-latency tiers and use n-gram (prompt-lookup) drafting for RAG and code edits, where outputs copy the input.

Production deployment on Kubernetes has converged on a few patterns:

- **Routing:** **the Gateway API Inference Extension's InferencePool is at v1 and GA.** Its endpoint picker chooses replicas by KV-cache utilization and queue length ([GAIE InferencePool](https://gateway-api-inference-extension.sigs.k8s.io/api-types/inferencepool/)). Routing requests to the replica that already holds their prefix, while staying load-aware, is the main win over round-robin.
- **Autoscaling:** scale on queue depth, KV-cache utilization and TTFT/ITL against targets, never on GPU utilization, which reads near 100% even under light decode load.
- **Weight loading:** the Run:ai Model Streamer reads safetensors concurrently from SSD, network file systems or S3 ([NVIDIA](https://developer.nvidia.com/blog/reducing-cold-start-latency-for-llm-inference-with-nvidia-runai-model-streamer)). Combined with Lustre file striping, it cut one 554 GiB, 16-way tensor-parallel load from about 76 minutes to about 5 ([Dynamo fast model loading](https://docs.dynamo.nvidia.com/dynamo/kubernetes/model-deployment/model-loading/fast-model-loading)).
- **Many fine-tunes on one base model:** S-LoRA serves thousands of LoRA adapters on shared GPUs at up to 4× the throughput of naive vLLM LoRA serving ([S-LoRA](https://arxiv.org/abs/2311.03285v2)).
- **Multi-region:** managed APIs differ. Azure offers Global, Data Zone and Regional deployments with spillover from provisioned to standard capacity ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/provisioned-throughput)). Vertex AI provisioned throughput is bound to a project, region and model version ([Vertex AI docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput/measure-provisioned-throughput?hl=en)). Prompt caches are scoped to a model and region, so failing over costs cache hits.

Managed model APIs now share four pricing levers: on-demand per-token rates; asynchronous batch processing at about 50% off within 24 hours; priority or provisioned capacity; and prompt caching, with cache reads at about 10% of the input price or less. OpenAI's Flex tier is synchronous but billed at batch rates, and it can return 429 errors when capacity is short ([OpenAI Flex processing](https://developers.openai.com/api/docs/guides/flex-processing)). Vertex turns implicit caching on by default at a 90% discount, but its batch and cache discounts do not stack ([Vertex context caching](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview)). Anthropic's cache multipliers do stack with batch ([Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)).

Among specialist inference providers, **NVIDIA licensed Groq's inference technology non-exclusively for about $20B in December 2025**. Groq's founders joined NVIDIA, Groq continues as an independent company, and a stockholder suit filed in October 2026 alleges a "lowball" price ([CNBC](https://www.cnbc.com/2025/12/24/nvidia-buying-ai-chip-startup-groq-for-about-20-billion-biggest-deal.html); [CNBC](https://www.cnbc.com/2026/10/05/nvidia-groq-deal-stockholder-lawsuit.html)). Secondhand Artificial Analysis figures put Cerebras at about 1,700 tokens/s on gpt-oss-120B, against about 690 for Fireworks and 564 for Together AI ([fast.io](https://fast.io/resources/fastest-ai-2026/)). One high-reasoning test of a single model measured 92 to 1,916 tokens/s across hosts, so always quote speed with the model, date and reasoning mode.

## The application layer: tokens, traces and tools replace weights and features

Most AI engineers now ship applications on top of models they did not train. That changes what gets versioned, tested and monitored.

### MLOps and LLMOps: the registry now versions prompts, judges and MCP servers

Google's three-level maturity model is still the standard reference ([Google Cloud MLOps guide](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)):

- **Level 0:** manual, notebook-driven work.
- **Level 1:** an automated continuous-training pipeline with data and model validation, a feature store, metadata tracking and triggers.
- **Level 2:** CI/CD for the pipeline itself, plus a model registry.

LLMOps changes what flows through that model. The versioned artifacts become prompts, model and provider configurations, tool and MCP definitions, retrieval indexes and agent harness code, often with no weights at all. The quality signal moves from accuracy to eval suites. The unit of monitoring becomes the trace. Cost per token becomes a service-level objective. Continuous training largely gives way to continuous evaluation and prompt optimization.

MLflow shows the shift. **MLflow 3 (11 June 2025) rebuilt itself around tracing** ([MLflow blog](https://www.mlflow.org/blog/mlflow-3-launch)). By 3.17.1 (13 October 2026) it versions prompts, evaluation datasets, judges and MCP servers (an MCP Registry arrived in 3.15), and runs an AI Gateway with traffic splits, fallbacks, budgets and guardrails. MLflow 3.16 switched to fail-closed authentication and removed the default admin password, so review the auth configuration on any self-hosted server upgraded from an older version ([MLflow changelog](https://raw.githubusercontent.com/mlflow/mlflow/master/CHANGELOG.md)). Google folded Vertex AI into the **Gemini Enterprise Agent Platform** on 22 April 2026 ([HPCwire](https://www.hpcwire.com/aiwire/2026/04/23/google-unveils-gemini-enterprise-agent-platform/)). The tooling market consolidated fast:

- ClickHouse acquired Langfuse, announced 16 January 2026 ([ClickHouse](https://clickhouse.com/blog/clickhouse-acquires-langfuse-open-source-llm-observability)).
- OpenAI announced it would acquire Promptfoo on 9 March 2026 ([OpenAI](https://openai.com/blog/openai-to-acquire-promptfoo)).
- Mintlify bought Helicone, which went into maintenance mode ([Helicone](https://helicone.ai/blog/joining-mintlify)).
- Apple acquired WhyLabs, and the commercial platform was discontinued ([GeekWire](https://www.geekwire.com/2025/founders-at-seattle-startup-whylabs-join-apple-following-under-the-radar-acquisition)).

That churn is the strongest argument for instrumenting with open standards, so you can swap backends.

CI for ML now has three test layers:

- **Code tests.**
- **Data and model tests,** such as Evidently Test Suites with pass/fail conditions ([Evidently](https://github.com/evidentlyai/evidently)).
- **LLM eval suites run as tests:** DeepEval's pytest-style `deepeval test run` ([DeepEval](https://github.com/confident-ai/deepeval)), promptfoo ([promptfoo](https://github.com/promptfoo/promptfoo)), and MLflow's `@mlflow.test` (added in 3.14).

The older Iterative tooling is fading: **CML's last release was v0.20.6 in October 2024** ([CML releases](https://github.com/iterative/cml/releases)). Anthropic's guidance separates two kinds of eval. Capability evals should start at a low pass rate, "a hill to climb". Regression evals should sit near 100%. A capability eval that saturates "graduates" into the regression suite ([Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)).

Infrastructure-as-code has diverged into two camps. Terraform is at 1.16.6, and the 1.17 release candidate makes Terraform Policy GA ([Terraform releases](https://github.com/hashicorp/terraform/releases)). OpenTofu 1.13.1 ships features such as state encryption and ephemeral resources first; ephemeral resources keep model-provider API keys out of state files ([OpenTofu releases](https://github.com/opentofu/opentofu/releases)). The GitOps tools are Crossplane 2.4 ([Crossplane](https://github.com/crossplane/crossplane/releases)), Argo CD 3.5.5, whose 3.6 release candidates fix four critical security issues ([Argo CD](https://github.com/argoproj/argo-cd/releases)), and Flux 2.9.6 ([Flux](https://github.com/fluxcd/flux2/releases)). The typical layering:

1. Terraform or OpenTofu provisions the VPC, cluster, GPU node pools, IAM and buckets.
2. GitOps reconciles the in-cluster pieces: GPU Operator, serving stack and telemetry collectors.
3. Argo Rollouts handles canary releases of model servers.

Deployment strategy splits by surface:

- **Managed endpoints:** SageMaker deployment guardrails do blue/green with all-at-once, canary or linear traffic shifting. Each step has a "baking period", and CloudWatch alarms trigger automatic rollback. Both fleets are billed for the whole update ([AWS docs](https://docs.aws.amazon.com/sagemaker/latest/dg/deployment-guardrails-blue-green.html)).
- **Kubernetes:** Argo Rollouts runs canary and blue/green releases with metric analysis, and traffic mirroring on some meshes supports shadow deployments ([Argo Rollouts](https://github.com/argoproj/argo-rollouts)).
- **LLM apps:** the unit of release is usually a prompt-plus-model-plus-parameters configuration, rolled out like a feature flag. LaunchDarkly's AI Configs guarded rollouts revert automatically when guardrail metrics regress ([LaunchDarkly](https://launchdarkly.com/changelog/guarded-rollouts-for-ai-configs/)).

For LLM apps, rollback triggers must include quality signals such as online judge scores and thumbs-down rates, not just errors and latency.

LLM observability has converged on **OpenTelemetry's GenAI semantic conventions**. All of them are still in "Development" status, and in June 2026 they moved to a dedicated repository, open-telemetry/semantic-conventions-genai ([DEV Community](https://dev.to/azena-ai/opentelemetrys-genai-semantic-conventions-are-not-stable-yet-heres-what-actually-shipped-in-2026-3mke); [semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai)). They define:

- **Operations:** chat, embeddings, retrieval, `execute_tool`, `invoke_agent` and memory operations.
- **Attributes:** such as `gen_ai.provider.name` and `gen_ai.usage.input_tokens`, which includes cached tokens.
- **Content capture:** opt-in and off by default ([gen-ai-spans](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-spans.md)).
- **Server metrics:** time to first token and time per output token ([gen-ai-metrics](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-metrics.md)).
- **Token counters:** with separate cache-read and reasoning-token counts ([gen-ai-token-metrics](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-token-metrics.md)).
- **Evaluations:** a `gen_ai.evaluation.result` event for judge scores.

Datadog has ingested OTel GenAI spans natively since December 2025 ([Datadog](https://datadoghq.com/blog/llm-otel-semantic-convention/)). Self-hostable backends include Langfuse (MIT core, built on ClickHouse) and Arize Phoenix (Elastic License 2.0) ([Langfuse](https://github.com/langfuse/langfuse); [Phoenix](https://github.com/Arize-ai/phoenix)). The conventions are still being renamed, so pin your instrumentation library versions and expect dashboards to break on upgrade. Track:

- TTFT and TPOT;
- tokens by type, and cost per request, user and feature;
- error types and fallbacks;
- tool calls per agent invocation, to detect loops;
- online judge scores;
- the empty-retrieval rate.

Classic drift statistics such as PSI and KS still apply to tabular models.

Evaluation practice has a clear consensus. Anthropic's January 2026 guide makes four main points ([Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)):

- The unit under test is the harness plus the model.
- Start with 20–50 tasks drawn from real failures.
- Grade outcomes, not the path taken.
- Distinguish **pass@k (at least one success in k trials) from pass^k (all k trials succeed)**. An agent that succeeds 75% of the time per trial passes all three of three trials only about 42% of the time, which is the figure that matters for customer-facing consistency.

Hamel Husain's methodology adds:

- binary pass/fail verdicts instead of Likert scales;
- one failure mode per judge;
- code-based checks before any LLM judge;
- about 100 traces of error analysis to saturate the failure taxonomy;
- judges calibrated against human labels using true- and false-positive rates ([evals-skills](https://github.com/hamelsmu/evals-skills); [skill mirror](https://tessl.io/registry/skills/github/hamelsmu/evals-skills/eval-audit)).

LLM judges have documented position, verbosity and self-enhancement biases. GPT-4 agreed with human preferences more than 80% of the time, but gave the same verdict after the answer order was swapped only 65% of the time ([Zheng et al.](https://arxiv.org/abs/2306.05685)). So swap answer orders and use a judge from a different model family than the generator. For RAG, RAGAS separates retriever metrics from generator metrics. Faithfulness is the share of response claims supported by the retrieved context. Context precision@K rewards ranking relevant chunks first. Context recall needs a reference answer ([RAGAS faithfulness](https://raw.githubusercontent.com/vibrantlabsai/ragas/main/docs/concepts/metrics/available_metrics/faithfulness.md); [RAGAS context precision](https://raw.githubusercontent.com/vibrantlabsai/ragas/main/docs/concepts/metrics/available_metrics/context_precision.md)). The UK AI Security Institute's Inspect framework ships more than 200 prebuilt evaluations ([Inspect](https://github.com/UKGovernmentBEIS/inspect_ai)).

Workflow orchestration has split into two tiers:

- **Offline batch work** (eval runs, index rebuilds, fine-tunes) runs on schedulers: Airflow 3.3.2, with asset partitioning, a state store and human-in-the-loop tasks ([Airflow](https://github.com/apache/airflow/releases)); Dagster; Prefect; or Kubeflow Pipelines.
- **Long-running agents** run on durable-execution engines. Temporal is the main example; its OpenAI Agents SDK integration is still in public preview and was extended to sandboxes in April 2026 ([Temporal](https://temporal.io/blog/announcing-openai-agents-sdk-integration); [Temporal changelog](https://temporal.io/change-log/product-area/python-sdk)).

### GenAI application architecture: hybrid retrieval, durable agents and a newly stateless MCP

Production RAG in 2026 is a multi-stage pipeline:

1. Parse documents with layout-aware parsers.
2. Chunk them and enrich each chunk with document context.
3. Embed the chunks and also build a BM25 index.
4. Retrieve with both and fuse the lists with RRF.
5. Rerank with a cross-encoder.
6. Generate an answer with citations.

Anthropic's Contextual Retrieval study is still the most-cited evidence. It prepends a 50–100-token, chunk-specific context to each chunk before embedding and BM25 indexing. With a top-20 baseline failure rate of 5.7%:

- contextual embeddings cut failures **35% (to 3.7%)**;
- adding contextual BM25 cut them **49% (2.9%)**;
- adding reranking cut them **67% (1.9%)**, retrieving 150 candidates and keeping 20.

With prompt caching, generating the contexts costs about $1.02 once per million document tokens. The study's rule is to skip RAG entirely for knowledge bases under about 200,000 tokens (roughly 500 pages) and put everything in a cached prompt instead ([Anthropic](https://www.anthropic.com/engineering/contextual-retrieval)). Large, changing, permissioned or multi-tenant corpora still need RAG, because per-query cost grows with context size and accuracy degrades for information buried mid-context ([Lost in the Middle](https://arxiv.org/abs/2307.03172)). Barnett et al. catalogue seven RAG failure points, from missing content to incomplete answers ([arXiv 2401.05856](https://arxiv.org/abs/2401.05856)). GraphRAG earns its indexing cost for global, thematic questions across a corpus ([GraphRAG](https://arxiv.org/abs/2404.16130)); LazyGraphRAG cuts indexing cost to about 0.1% of full GraphRAG ([Microsoft Research](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/)). Managed services wrap the same chain: Bedrock Knowledge Bases, RAG Engine inside Google's Agent Platform, and Azure's Foundry IQ. Foundry IQ breaks complex queries into parallel subqueries, enforces ACLs under the caller's Entra identity, and **exposes knowledge bases as MCP endpoints** ([Microsoft Foundry devblog](https://devblogs.microsoft.com/foundry/foundry-iq-agent-framework-integration/)). Choose a managed RAG service by where your data and identity already live.

On agents, Anthropic's December 2024 taxonomy remains the shared vocabulary. *Workflows* follow predefined code paths: prompt chaining, routing, parallelization, orchestrator-workers and evaluator-optimizer. *Agents* direct their own tool use. The advice is to start from raw APIs and design tools that are hard to misuse ([Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)). Anthropic's multi-agent research system, a lead agent spawning parallel subagents, beat a single agent by 90.2% on an internal eval. The cost: agents use about 4× the tokens of chat, and **multi-agent systems about 15×**. On the BrowseComp benchmark, token usage alone explained 80% of the variance in performance ([Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)). Context is a budget. Presenting MCP tools as code APIs that the agent calls from a sandbox cut one Drive-to-Salesforce workflow from about 150,000 tokens to 2,000 (−98.7%) ([Anthropic: code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)). Human-in-the-loop approval belongs in the runtime, not the prompt: implement it with pre-tool hooks and permission callbacks such as the Claude Agent SDK's `PreToolUse` and `can_use_tool` ([Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python)), or LangGraph interrupts ([LangGraph](https://github.com/langchain-ai/langgraph)).

Agent tooling has two layers. The code-first SDKs:

- **Claude Agent SDK:** the Claude Code harness as a library, with in-process MCP tool servers ([Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python)).
- **OpenAI Agents SDK:** handoffs, guardrails, sessions and sandbox agents, with support for other model providers ([OpenAI Agents SDK](https://github.com/openai/openai-agents-python)).
- **LangGraph:** durable, checkpointed graphs.
- **Microsoft Agent Framework:** the successor to Semantic Kernel and AutoGen; secondary sources report 1.0 GA on 3 April 2026 ([Microsoft Agent Framework](https://github.com/microsoft/agent-framework); [Atlan](https://atlan.com/know/ai-agent/microsoft/semantic-kernel/)).
- **Google ADK** ([ADK](https://github.com/google/adk-python)).

One legacy path to retire: **OpenAI's Assistants API was scheduled to shut down on 26 August 2026**, replaced by the Responses and Conversations APIs ([DEV Community](https://dev.to/mr_manushukla/openai-assistants-api-shuts-down-26-august-2026-a-3-week-migration-sprint-plan-596b)). The managed runtimes:

- **Amazon Bedrock AgentCore** bundles a serverless runtime, a gateway that turns APIs into MCP tools, identity, memory, a code interpreter, a browser, OpenTelemetry observability, evaluations, and Cedar-based policy ([AgentCore samples](https://github.com/awslabs/amazon-bedrock-agentcore-samples)).
- **Google's Agent Engine** sits inside the Gemini Enterprise Agent Platform.
- **Microsoft Foundry Agent Service** reportedly made hosted agents GA on 9 July 2026 ([tech-insider.org](https://tech-insider.org/aws-bedrock-agentcore-vs-azure-ai-foundry-vs-vertex-ai-agent-builder-2026/)).

The same secondary source puts AgentCore and Agent Engine runtime compute prices within about 4% of each other, so the runtimes now compete on identity, policy, evals and data integration.

The protocol layer matured. MCP, introduced by Anthropic in November 2024, now sits under the Linux Foundation's **Agentic AI Foundation, formed on 9 December 2025** ([WorkOS](https://workos.com/blog/the-linux-foundation-launches-the-aaif)). **The 2026-07-28 MCP revision made the protocol stateless** ([MCP blog](https://blog.modelcontextprotocol.io/posts/2026-07-28/)):

- It retires the `initialize` handshake and the `Mcp-Session-Id` header. Every request now carries its protocol version, client identity and capabilities, so any request can hit any server instance behind a plain round-robin load balancer.
- Multi Round-Trip Requests replace server-initiated sampling and elicitation.
- Required `Mcp-Method` and `Mcp-Name` headers let gateways and web application firewalls route and meter traffic without parsing request bodies.
- List results become cacheable, in deterministic order, which keeps upstream prompt caches stable.
- Dynamic Client Registration is deprecated in favor of Client ID Metadata Documents.
- Roots, Sampling and Logging are deprecated under a formal 12-month minimum deprecation policy.

The tier-one SDKs see about half a billion downloads a month. The earlier 2025-11-25 revision had added experimental long-running Tasks and URL-mode elicitation ([MCP changelog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/changelog.mdx)). **A2A, Google's agent-to-agent protocol, reached v1.0 on 12 March 2026** with a `tasks/list` method, PKCE and device-code OAuth flows, and gRPC multi-tenancy ([A2A releases](https://github.com/a2aproject/A2A/releases)). MCP connects agents to tools and data; A2A connects agents to other agents. The practical consequence is that MCP servers can now be deployed as ordinary stateless HTTP services on Lambda, Cloud Run or Azure Functions, with per-tool authorization at the gateway. Servers that relied on sessions or server-initiated sampling need refactoring.

Long-running agents deploy as durable workflows:

1. The API accepts the task and returns HTTP 202 with a task ID.
2. The task goes onto a queue.
3. A workflow engine (Temporal, Step Functions, Durable Functions or LangGraph) drives the agent loop, treating each model or tool call as a retried activity.
4. Checkpoints go to Postgres, DynamoDB, Cosmos DB or Firestore.
5. Progress streams back over server-sent events (SSE) or webhooks.

Code that agents generate needs isolation. Firecracker microVMs (used by E2B and AgentCore's code interpreter) put a hardware virtualization boundary between guest and host kernels. That is stronger than gVisor's syscall interception, which Modal uses and which supports GPUs ([Northflank](https://northflank.com/blog/e2b-vs-modal)). Firecracker boots in about 125 ms with under 5 MiB of overhead ([Firecracker, NSDI 2020](https://www.usenix.org/conference/nsdi20/presentation/agache)). The rule: microVMs for untrusted code, gVisor for semi-trusted code that needs GPUs, and plain containers only for trusted code.

Caching is the single biggest cost lever, and providers implement it differently:

| Provider | Mechanism | Cache-hit price | Retention |
|---|---|---|---|
| Anthropic | Explicit breakpoints or automatic caching; writes cost 1.25× (5-minute) or 2× (1-hour) | 0.1× input; 0.05× on Opus 5.5 and Sonnet 5.5; 0.025× on Fable 5.1 | 5 minutes default, refreshed on each hit; 1-hour option |
| OpenAI | Automatic prefix caching at 1,024+ tokens | ~10% of input on newer models | Optional 24-hour retention up to GPT-5.5; on GPT-5.6+ a 30-minute TTL, and cache writes are billed |
| Google Gemini | Implicit (free) or explicit (storage billed) | 90% off on Gemini 2.5+ | Configurable for explicit caches |

Sources for the table: [Anthropic prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching); [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching); [Microsoft Foundry docs](https://learn.microsoft.com/en-my/Azure/foundry/openai/how-to/prompt-caching); [Vertex context caching](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview).

Anthropic caches are invalidated in a hierarchy. Changing tool definitions invalidates everything; changing the system prompt invalidates the system prompt and messages. Prompts shorter than the model's minimum cacheable length (512–4,096 tokens, depending on model) silently don't cache. So lay prompts out with static tools first, then the system prompt, then stable documents, then the conversation, and volatile content last. Never put a timestamp near the top. Semantic caching, which reuses answers to similar-looking questions, is a separate and lossy layer: it produces false positives ([GPTCache](https://github.com/zilliztech/GPTCache)). Never apply it to answers that depend on user-specific context.

Production stacks also put an AI gateway between applications and providers. The main options:

- **LiteLLM:** 100+ providers, virtual keys and spend tracking. It claims 8 ms p95 overhead at 1,000 requests/s; a third party says it degrades around 2,000 ([LiteLLM](https://github.com/BerriAI/litellm); [Cloudnuro](https://www.cloudnuro.ai/blog/ai-gateway-buyers-guide-2026-kong-vs-portkey-vs-litellm-vs-truefoundry)).
- **Envoy AI Gateway:** renamed "Agent Router" and now an Agentic AI Foundation project ([Envoy AI Gateway](https://github.com/envoyproxy/ai-gateway)).
- **Kong** and **Azure API Management:** APIM adds token limits, semantic caching and MCP support ([Azure AI-Gateway samples](https://github.com/Azure-Samples/AI-Gateway)).

Client-side reliability is classic distributed-systems practice:

- **Retries:** capped exponential backoff with full jitter on 429 and 5xx responses, honoring `Retry-After` ([AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)).
- **Circuit breakers:** one per backend, so a failing endpoint triggers fallback instead of retries.
- **Fallback order:** same model in another region first, then a different model. Switching models changes behavior and loses the prompt cache.
- **Structured outputs:** schema-constrained decoding. When OpenAI introduced it, gpt-4o scored 100% schema adherence on OpenAI's eval, against under 40% for gpt-4-0613 ([OpenAI](https://openai.com/index/introducing-structured-outputs-in-the-api/)).

All three clouds converge on the same logical stack. Microsoft's baseline Foundry chat reference architecture is the most explicit published blueprint. It puts the chat front end on App Service behind Application Gateway with a web application firewall, runs Foundry Agent Service on customer-owned Cosmos DB, AI Search and Storage, uses private endpoints throughout, and forces egress through Azure Firewall ([Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-chat)). The table below is a synthesis from the components cited in this section, not a vendor-published artifact.

| Layer | AWS | Google Cloud | Azure |
|---|---|---|---|
| Edge and API | CloudFront, WAF, API Gateway or ALB | Cloud Load Balancing, Cloud Armor, Apigee | Front Door or App Gateway WAF, APIM |
| Agent runtime | Bedrock AgentCore Runtime | Agent Engine (Gemini Enterprise Agent Platform) | Foundry Agent Service |
| Models | Bedrock, with cross-region inference | Gemini and Model Garden | Foundry Models |
| Retrieval | Bedrock Knowledge Bases with OpenSearch, S3 Vectors or Aurora pgvector | RAG Engine, Vertex AI Search, Vector Search | Azure AI Search and Foundry IQ |
| State | DynamoDB, ElastiCache, AgentCore Memory | Firestore, Memorystore | Cosmos DB, Azure Cache for Redis |
| Durable async | SQS and Step Functions (or Temporal) | Pub/Sub and Workflows (or Temporal) | Service Bus and Durable Functions (or Temporal) |
| Code sandbox | AgentCore Code Interpreter (microVM) | Cloud Run (gVisor) | Container Apps dynamic sessions |

## The control layer: security is architectural and cost is utilization

The two disciplines that decide whether a system survives contact with production, security and cost, are both being reshaped by the same fact: the model is no longer the main unit of risk or spend. The system around it is.

### Security and governance: guardrails filter, architecture defends, and the EU clock is running

Cloud security for AI stacks five layers: **identity → network → encryption → logging → application authorization**. The cloud provider supplies the first four; you build the fifth, and it is where most LLM-specific incidents happen. In detail:

- **Identity.** Keyless workload identity through OIDC federation works the same way on EKS, GKE and AKS ([jorijn.com](https://jorijn.com/en/knowledge-base/kubernetes/security/workload-identity-irsa-eks-gke-aks/)). AWS recommends EKS Pod Identity over IRSA wherever possible ([Hidekazu Konishi](https://hidekazu-konishi.com/entry/amazon_eks_pod_identity_and_irsa_decision_guide.html)).
- **Network and encryption.** Bedrock supports customer-managed KMS keys and private connectivity through PrivateLink ([AWS](https://aws.amazon.com/bedrock/security-privacy-responsible-ai)).
- **Logging.** Bedrock model invocation logging, which captures prompts and responses, is off by default and separate from CloudTrail. Once enabled, those logs are themselves a sensitive data store ([Bedrock docs](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html)).
- **Application authorization.** One security vendor calls this the "request gap": guardrails, PrivateLink and IAM each do a different job, but none decides whether a specific authenticated caller should be allowed to send a given prompt ([DeepInspect](https://www.deepinspect.ai/blog/aws-bedrock-security)).

On data protection, the hyperscalers' commitment not to train on customer API data is settled table stakes ([AWS](https://aws.amazon.com/bedrock/security-privacy-responsible-ai)). Retention is the open question, because **zero data retention is not the default anywhere**:

- **Azure** grants it only through an approved Modified Abuse Monitoring exemption, typically for enterprise-agreement customers. Even then it covers only abuse-monitoring storage; the Responses API, stored completions, files and fine-tuning keep their own retention ([Microsoft Q&A](https://learn.microsoft.com/en-au/answers/questions/5954113/modified-abuse-monitoring-on-azure-foundry)).
- **Vertex AI** caches Gemini inputs and outputs in memory for up to 24 hours per project by default, so you must disable that to reach zero retention. Grounding with Google Search keeps logs for up to three days ([Google Cloud ZDR](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/vertex-ai-zero-data-retention)).

Check every feature you enable separately, including cross-region inference profiles that can route traffic out of a geography. Confidential GPU computing exists but has limits. Azure's NCC H100 v5 VMs pair AMD SEV-SNP CPUs with H100s in confidential mode ([Azure](https://azure.microsoft.com/en-us/blog/how-azure-is-ensuring-the-future-of-gpus-is-confidential/)), and Google offers Confidential Space with Hopper GPUs plus Blackwell-based G4 confidential VMs ([Google Cloud](https://cloud.google.com/blog/products/identity-security/verifiable-trust-in-the-ai-era-whats-new-in-confidential-computing)). A 2025 analysis found multi-GPU confidential computing disabled and limited protection against physical attacks ([arXiv 2507.02770](https://arxiv.org/html/2507.02770v1)). Confidential computing protects data in use from the cloud operator. It does nothing against prompt injection.

The threat taxonomies are settled. **The OWASP Top 10 for LLM Applications 2025** runs from LLM01 Prompt Injection to LLM10 Unbounded Consumption, which covers "denial of wallet" attacks that run up your bill ([Invicti](https://www.invicti.com/blog/web-security/owasp-top-10-risks-llm-security-2025)). **The OWASP Top 10 for Agentic Applications (9 December 2025)** opens with ASI01 Agent Goal Hijack. Its example is EchoLeak, where a hidden instruction in an email made Microsoft 365 Copilot exfiltrate data with zero clicks. The rest of the list covers tool misuse, identity and privilege abuse, the agentic supply chain, memory poisoning, and rogue agents ([Giskard](https://www.giskard.ai/knowledge/owasp-top-10-for-agentic-application-2026); [Cycode](https://cycode.com/blog/owasp-top-10-agentic-applications/)). Two mental models predict when injection turns into a real incident:

- **Simon Willison's "lethal trifecta":** an agent that has private data, exposure to untrusted content, and a way to communicate externally can be tricked into stealing the data ([Simon Willison](https://simonwillison.net/2025/jun/16/the-lethal-trifecta/)).
- **Meta's "Agents Rule of Two":** an agent should combine at most two of untrusted input, sensitive access, and state-changing or external actions. An agent that needs all three needs human supervision ([Simon Willison](https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/)).

Auto-rendered markdown images are the classic exfiltration channel. Injected text makes the model emit an image URL with the secret in its query string, and the client fetches it without user action ([Simon Willison](https://simonwillison.net/tags/markdown-exfiltration/)). The supply chain now covers models and MCP servers. The "nullifAI" models on Hugging Face hid malicious pickle files inside 7z-compressed archives that evaded the Picklescan scanner ([The Hacker News](https://thehackernews.com/2025/02/malicious-ml-models-found-on-hugging.html)). Safetensors files have no executable code path. OpenSSF Model Signing v1.0 (4 April 2025) proves a model's integrity and provenance, but not that it is benign ([OpenSSF](https://openssf.org/blog/2025/04/04/launch-of-model-signing-v1-0-openssf-ai-ml-working-group-secures-the-machine-learning-supply-chain/)).

Defenses fall into two classes. Guardrail classifiers are probabilistic filters, useful but bypassable:

- **Bedrock Guardrails** offers content filters including prompt-attack detection, PII masking and contextual grounding checks. Its `ApplyGuardrail` API also works with non-Bedrock models ([AWS](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-components.html)), and Automated Reasoning checks went GA in August 2025 ([AWS](https://aws.amazon.com/about-aws/whats-new/2025/08/automated-reasoning-checks-amazon-bedrock-guardrails)).
- **Azure Prompt Shields** detect direct and indirect attacks, but indirect-attack detection requires you to delimit documents when you build the prompt ([Microsoft](https://learn.microsoft.com/en-us/azure/foundry-classic/foundry-models/concepts/content-filter)).
- **Open source:** Llama Guard 4 and NeMo Guardrails protect at runtime, and garak and PyRIT test ([TraeAI](https://learn.traeai.com/t/ai-engineering/phases/18-ethics-safety-alignment/16-red-team-tooling-garak-llamaguard-pyrit)).

**Architectural defenses are what hold up.** The clearest example is CaMeL. A privileged LLM plans only from the trusted user query, a quarantined LLM parses untrusted data with no tool access, and an interpreter tracks where every value came from before each tool call. On the AgentDojo benchmark it solved **77% of tasks with provable security against 84% undefended**, and for Claude 3.5 Sonnet successful attacks fell from 44 to zero ([CaMeL, arXiv](https://arxiv.org/html/2503.18813v2); [SaTML 2026](https://www.computer.org/csdl/proceedings-article/satml/2026/785900a587/2jZks3ksGT6)). That seven-point utility cost is the current price of provable injection resistance, so expect production systems to apply CaMeL-style data-flow policies only on high-risk tool paths. Rank defenses by reliability:

1. **Architecture:** plan/data separation, the Rule of Two, no auto-rendered external URLs.
2. **Least privilege:** per-user on-behalf-of tokens and scoped, read-only-by-default tools.
3. **Containment:** sandboxes, egress allowlists and budgets.
4. **Detection:** guardrail classifiers.
5. **Assurance:** red teaming in CI, mapped to MITRE ATLAS. ATLAS grew to about 120 techniques by v2026.09 with new autonomous-agent techniques, though secondary sources' counts conflict ([CallSphere](https://callsphere.ai/blog/td30-rp-mitre-atlas-2026-update)).

Governance deadlines moved in 2026. **The EU's Digital Omnibus on AI (Regulation (EU) 2026/1744, in force 27 July 2026) deferred high-risk obligations but left GPAI and transparency duties on schedule** ([Usercentrics](https://usercentrics.com/knowledge-hub/eu-ai-act-high-risk-delay-article-50-transparency-consent/); [CSA](https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-high-risk-deadline-omnibus-20260/)). The Official Journal text was not retrieved; these dates come from law-firm and advisory summaries that agree with one another.

| Date | What applies under the EU AI Act |
|---|---|
| 2 Feb 2025 | Prohibited practices and the AI literacy duty |
| 2 Aug 2025 | GPAI provider obligations |
| 2 Aug 2026 | Commission enforcement powers over GPAI (fines up to €15M or 3% of turnover); Article 50 transparency duties (disclosing chatbots, labelling deepfakes) |
| 2 Dec 2026 | End of the grace period for machine-readable marking on systems already on the market; new prohibition on "nudification" systems |
| 2 Aug 2027 | Deadline for GPAI models placed on the market before August 2025 |
| 2 Dec 2027 | Stand-alone high-risk systems (Annex III: employment, credit, education, and similar) |
| 2 Aug 2028 | High-risk systems embedded in regulated products (Annex I) |

Sources for the table: [artificialintelligenceact.eu](https://artificialintelligenceact.eu/enforcement-of-chapter-v-under-the-eu-ai-act/); [Beam AI](https://beam.ai/agentic-insights/eu-ai-act-enforcement-august-2-2026-gpai-fines); [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj).

GPAI models are presumed to carry systemic risk above 10²⁵ FLOPs of training compute ([EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)). Whether the omnibus changed the AI literacy duty is unresolved. In the US, NIST's AI Risk Management Framework (Govern, Map, Measure, Manage) and its Generative AI Profile (AI 600-1, July 2024) are the baseline ([NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)). A Cyber AI Profile, IR 8596, was released as a preliminary draft on 16 December 2025 ([NIST CSRC](https://csrc.nist.gov/News/2025/nist-releases-prelim-draft-cyber-ai-profile)). HIPAA has no certification. Compliance depends on what each Business Associate Agreement (BAA) covers, feature by feature:

- **AWS:** the BAA is self-service through AWS Artifact and covers Claude on Bedrock ([Aptible](https://www.aptible.com/hipaa-compliant-ai-tools/aws-bedrock-baa)).
- **OpenAI:** offers an API BAA, but its web search is documented as not HIPAA-eligible ([CallSphere](https://callsphere.ai/blog/vw1f-hipaa-eligible-model-providers-2026)).
- **Anthropic:** secondary sources conflict on what its BAA covers ([Strac](https://www.strac.io/blog/is-claude-hipaa-compliant)).

The cloud controls are what produce compliance evidence. Invocation logs and audit trails support record-keeping duties; KMS keys and private networking support ISO/IEC 42001 and SOC 2 controls; and an AI inventory listing every model, vendor, use case, risk tier and owner ties it together.

### Cost and FinOps: idle GPUs and broken caches cost more than any list price

FinOps (cloud financial operations) has pivoted to AI. **98% of State of FinOps 2026 respondents manage AI spend, up from 63% a year earlier** ([Flexera](https://www.flexera.com/blog/finops/finops-x-2026-recap)). FOCUS, the open billing-data specification, reached version 1.4 in June 2026. Version 1.5, targeted for December 2026, is slated to add native AI token tracking and a price-sheet dataset ([Finout](https://finout.io/blog/finops-x-2026-conference-recap-key-takeaways-and-product-launches)). The Linux Foundation also announced a sister Tokenomics Foundation for token economics ([TechTarget](https://www.techtarget.com/searchcio/news/366644142/linux-foundation-announces-tokenomicon-at-finops-x)). The FinOps Foundation's unit-economics framing treats cost per token as an efficiency metric and cost per resolved case or per agent action as the outcome metric to report ([Finout](https://www.finout.io/blog/token-economics-and-tokenops-the-definitive-guide-to-finops-for-tokens)).

GPU utilization is the first lever, and it is usually measured wrong. **nvidia-smi's "GPU-Util" reports the fraction of time any kernel was running**, so one small kernel on one streaming multiprocessor (SM) reads the same 100% as a kernel filling the chip ([Arthur Chiao](https://arthurchiao.art/blog/understanding-gpu-performance/)). Use DCGM's SM-activity metric (`DCGM_FI_PROF_SM_ACTIVE`) and tensor-pipe activity instead; SM activity of 0.8 or higher is necessary but not sufficient for good use ([Netdata](https://www.netdata.cloud/guides/nvidia-gpu/nvidia-gpu-dcgm-vs-nvidia-smi-nvml/)). Measured that way, real utilization is dismal:

- Cast AI's telemetry finds **about 5% average GPU utilization across non-optimized Kubernetes clusters**. This is vendor telemetry ([VentureBeat via finanzen.net](https://www.finanzen.net/nachricht/aktien/5-gpu-utilization-the-401-billion-ai-infrastructure-problem-enterprises-can-t-keep-ignoring-15671084)).
- 86% of enterprises running their own GPUs self-report 50% utilization or less ([RuntimeWire](https://runtimewire.com/article/enterprise-gpu-utilization-ai-agents-venturebeat-survey)).
- 44% still assign workloads to GPUs manually ([HackerNoon](https://hackernoon.com/nearly-half-of-enterprises-waste-millions-on-underutilized-gpu-capacity)).

**Effective cost per useful GPU-hour equals the list price divided by utilization.** At the $3.17 H100 index, 5% utilization means $63.40 per useful hour, 50% means $6.34, and 80% means $3.96. Raising utilization from 5% to 50% saves 10×, far more than any commitment discount. Practical moves:

- Serve models of 7B or less in FP8 with modest concurrency on MIG slices or L4/L40S-class cards, not full H100s.
- Alert on allocated GPUs whose SM activity stays below about 0.1, which catches idle notebooks and stalled jobs.
- Charge idle cost to the owning team through OpenCost- or Kubecost-style allocation, so teams have a reason to release GPUs.

Purchasing math is simple but often skipped. **A commitment at discount d beats on-demand only if you use more than (1 − d) of it**, so a 40% discount needs over 60% sustained use. A 64-GPU, 14-day H100 run (21,504 GPU-hours) shows the spread:

- about $68k at the $3.17 index;
- about $128k at the October AWS Capacity Block rate;
- about $148k at $6.88 hyperscaler on-demand;
- roughly $27k on spot at 60% off the index, before the cost of restarts and lost progress.

Reported spot interruption rates for H100s range from about 4% to 20% per hour across sources ([Thunder Compute](https://www.thundercompute.com/blog/should-i-use-cloud-gpu-spot-instances)). Capacity Blocks are guaranteed capacity, not a discount product. They are charged up front, so unused hours are sunk cost ([AWS Capacity Blocks pricing](https://aws.amazon.com/es/ec2/capacityblocks/pricing/)).

For API spend, Anthropic's published October 2026 prices and its own internal measurements are the most complete public dataset on cost levers.

| Model | Input ($/MTok) | 5-minute cache write | Cache read | Output | Batch (input / output) |
|---|---|---|---|---|---|
| Claude Fable 5.1 | $10 | $12.50 | $0.25 | $50 | $5 / $25 |
| Claude Opus 5.5 | $4 | $5 | $0.20 | $20 | $2 / $10 |
| Claude Sonnet 5.5 | $2 | $2.50 | $0.10 | $10 | $1 / $5 |
| Claude Haiku 5.5 (prompts ≤100K tokens) | $0.10 | $0.125 | $0.01 | $0.50 | $0.05 / $0.25 |

Sources for the table: [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing); [Anthropic cost-optimization guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence.md).

Output costs 5× input, and cache multipliers stack with the batch discount. Anthropic's measurements quantify each lever ([Anthropic cost-optimization guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence.md)):

- **Caching:** across a day of real traffic, agent loops read a **median 84% of their input from cache**. Running without caching cost **3.3×** on Opus 5.5 (SWE-bench Pro), 3.1× on Sonnet 5.5, 1.7× on Haiku 5.5, and **7.3×** for a Sonnet 5.5 bug-triage agent. A single broken cache turn on a 100K-token prefix costs $0.50 instead of a $0.02 read on Opus 5.5, 25× more.
- **Effort:** on a SWE-bench Pro subset, Sonnet 5.5 at high effort solved 87.6% of tasks at **$0.11 per solved task**, against $0.22 for Opus 5.5 at medium effort (92.8%). Running everything at low effort and re-running only the failures at high reached about 97% at $0.17 per task, against 95.3% at $0.29 for all-high, about 40% cheaper. This needs a reliable failure signal, such as tests.
- **Output limits:** setting `max_tokens` too low backfires. Opus 5.5 capped at 16,384 tokens solved 57.6% of tasks, against 75.6% at 64,000, for the same cost per solved task.
- **Input handling:** passing data files through code execution instead of pasting them into the prompt cut cost from $5.01 to $0.40 per run while accuracy rose from 7/25 to 25/25.
- **Model generations:** upgrades usually cut cost per solved task (Sonnet 5 → 5.5: −87%), but not always (Fable 5.1: +46% over Fable 5).
- **Tokenizers:** Claude 4.7 and later models produce about 30% more tokens for the same text, so compare cost per task, not list price per token, across generations ([Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)).

Anthropic recommends applying the levers in this order: caching and trimming, then batch, then a prompt audit, then effort and model choice, with multi-model cascades last, because caches are per model and a cascade forfeits cross-model cache hits. OpenAI and Gemini prices circulate mainly through aggregators that contradict each other, so budget from the providers' own pages.

Two worked examples make the levers concrete:

- **Support chatbot on Sonnet 5.5.** Each request has a 3,000-token cacheable system prompt and tool block, 1,000 uncached tokens and 400 output tokens. Uncached, a request costs $0.012; with a cache hit it costs $0.0063, about 47% less. At an 80% hit rate, a million requests cost about $7,740.
- **Cascade.** Sending everything to Haiku 5.5 and escalating 30% to Sonnet 5.5 costs about $4,200 per million requests against $12,000 all-Sonnet (−65%). That holds only if the escalation classifier is reliable and the quality loss on the 70% is acceptable.

Self-hosting cost per token equals the GPU's hourly price divided by (tokens per second × 3,600 × utilization). One vendor estimates a 70B FP8 model on one H100 at about 400 tokens/s; this is conservative for well-batched serving ([Spheron](https://www.spheron.network/blog/migrate-from-openai-api-to-self-hosted-llms-cost-2026/)). At the $3.17 index that gives **$2.20 per million tokens at full utilization and $5.50 at 40%**. One H100 running 24/7 costs about $76 a day, so it breaks even at:

- about 10.6M tokens/day against Opus 5.5's blended $7.20/MTok (80/20 input/output split);
- about 21.1M against Sonnet 5.5;
- never against Haiku 5.5, which would need about 423M tokens/day, far beyond one GPU's roughly 35M-token daily capacity.

Published estimates agree on the shape. Two H100s running gpt-oss-120b cost about 2× a hosted provider's price for the same model ([General Compute](https://www.generalcompute.com/blog/vllm-vs-managed-inference-apis-when-to-self-host-vs-pay-as-you-go?agent=true)), and production utilization of 30–60% makes self-hosted tokens cost 2–3× the peak-throughput estimate ([Codewave](https://codewave.com/feeds/blog/self-hosted-llm-cost)). Self-hosting wins in four situations: steady high-volume traffic on small or fine-tuned models, strict data residency, latency targets that APIs cannot meet, or GPUs you already own with idle headroom.

Attribution needs metadata captured at request time, because LLM APIs have no resource tags. Stamp every call at the gateway with team, feature, tenant, environment, model and trace ID, plus the four token counts and a cost computed from a versioned price table ([Gravitee](https://gravitee.io/corpus/gen-1210/ocnosispa/ocnosispa-llm-gateway-finops-usage-metering-chargeback-and-cost-allocation.html)). Anthropic's Usage and Cost Admin API groups usage by model, API key and workspace, but excludes Bedrock, Vertex and Foundry traffic ([Anthropic Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api.md)). Start with showback, which only reports costs, and move to chargeback, which bills teams, once the allocation rules are stable. The most valuable anomaly alert is a sudden drop in the ratio of cache reads to total input: a timestamp added to a system prompt can multiply input cost overnight.

Network charges hide in training too. **AWS bills cross-AZ traffic at $0.01/GB in each direction**, about $0.02 effective ([Last Week in AWS](https://www.lastweekinaws.com/blog/aws-cross-az-data-transfer-costs-more-than-aws-says)). Hourly full checkpoints of a 70B model written across zones would cost about $538 a day, so never stripe a training cluster across availability zones, and expire old checkpoints with lifecycle rules.

On sustainability, carbon-aware scheduling suits long training runs. But a 2026 study of scheduling across three AI data-center parks found only about **4.5% lower carbon emissions and 1.7% lower cost** ([arXiv 2609.11649](https://arxiv.org/pdf/2609.11649); [University of Alberta](https://sites.ualberta.ca/~oardakan/files/PESGM26.pdf)). Region choice is the bigger lever. A 64-H100, two-week run uses about 18 MWh at a PUE of 1.2, which is roughly 0.9 tonnes of CO₂e on a hydro- or nuclear-heavy grid and roughly 9 tonnes on a coal-heavy one, using illustrative grid intensities.

## A six-stage learning path fits inside about $250

Employers set the curriculum. An analysis of 43,480 US AI-engineering job postings through July 2026 found **Python in 62%, cloud platforms in 55% and foundation-model work in 51%**, with about 1,550 new roles a week, aimed mostly at people 3–7 years into their careers ([Axial Search](https://axialsearch.com/insights/ai-ml-engineering-jobs/)). ML-platform and LLMOps postings add Terraform, Kubernetes with multi-GPU orchestration, and serving stacks such as vLLM, SGLang, Triton and Ray Serve, "with attention to GPU utilization, latency, and throughput" ([Turing/Greenhouse posting](https://job-boards.greenhouse.io/turingportal/jobs/5537879004); [Dice posting](https://www.dice.com/job-detail/92bc7960-ba8d-4a26-a144-0413768e1899)). Headline estimates of the market's size conflict wildly, so treat them as noise. The profile that gets rewarded combines Python, one hyperscaler in depth, foundation-model apps with RAG, agents and evals, Kubernetes plus Terraform for GPU workloads, a serving stack, and observability.

Learn the fundamentals in the order the job punishes mistakes: IAM, then VPC networking and private endpoints, then object storage, then GPU instance families, quotas and spot, then billing controls. New accounts come with credits:

- **AWS:** accounts opened after 15 July 2025 get $100 in credit and can earn up to $100 more.
- **Google Cloud:** $300 for 90 days.
- **Azure:** $200 for 30 days ([freetier.co](https://freetier.co/articles/cloud-provider-free-tiers-2026)).
- **Kaggle:** about 30 free GPU-hours a week ([gpuperhour](https://gpuperhour.com/blog/free-cloud-gpus-and-credits)).

The billing traps are part of the curriculum:

- An EKS cluster on an extended-support Kubernetes version costs about $0.60 per cluster-hour instead of $0.10 ([TechTarget](https://www.techtarget.com/it-infrastructure/tip/Break-down-the-Amazon-EKS-pricing-model)).
- GKE's monthly management-fee credit does not cover regional Standard clusters ([Finout](https://www.finout.io/blog/gke-pricing-tiers)).
- A spot job without checkpoints that gets evicted mid-run can cost more than running it on demand ([GPUnex](https://www.gpunex.com/blog/cloud-gpu-pricing-comparison-2026)).

Product renames make old study material stale. Vertex AI is now the Gemini Enterprise Agent Platform, and Azure's AI platform is Microsoft Foundry, so prefer exam guides and docs updated after April 2026.

Certifications churned heavily in 2026. Check exam codes on the official pages right before booking.

| Certification | Status in October 2026 | Cost |
|---|---|---|
| AWS Machine Learning – Specialty (MLS-C01) | Retired 31 March 2026 | n/a |
| AWS Generative AI Developer – Professional (AIP-C01) | New; standard registration since 17 March 2026 | $300 |
| AWS ML Engineer – Associate | MLA-C01 → MLA-C02 (English MLA-C01 closed 28 Sept 2026); shifted toward Bedrock, RAG and agents | Not confirmed |
| Google Professional ML Engineer | Active; updated for the Agent Platform rename | $200 |
| Google Generative AI Leader | Active; non-technical | $99 |
| Microsoft AI-102 / DP-100 | Retired 30 June / 1 June 2026, replaced by AI-103 (AI apps and agents, beta) and AI-300 (MLOps) | AI-103 price conflicts across sources |
| NVIDIA NCP-GENL / NCP-AAI (agentic AI) | Active / newly listed | $200 each |
| CNCF CKA / CKAD / CKS | Active; hands-on, performance-based | $445 |
| CNCF Cloud Native Platform Engineer (CNPE) | New, launched November 2025 | $445 |

Sources for the table: [AWS MLS page](https://aws.amazon.com/certification/certified-machine-learning-specialty/); [AWS March 2026 offerings](https://aws.amazon.com/es/blogs/training-and-certification/march-2026-new-offerings/); [AWS MLA-C02](https://aws.amazon.com/blogs/training-and-certification/updates-to-aws-certified-machine-learning-engineer-associate-mla-c02/); [Google PMLE](https://cloud.google.com/learn/certification/machine-learning-engineer); [Google Gen AI Leader](https://cloud.google.com/learn/certification/generative-ai-leader); [Vlad Talks Tech](https://vladtalkstech.com/microsoft-learning-and-credential-news/microsoft-certification-retirements-2026/); [NVIDIA NCP-AAI](https://nvidia.com/en-us/learn/certification/agentic-ai-professional); [FlashGenius](https://flashgenius.net/blog-article/nvidia-certification-cost-2026-exam-fees-renewal-costs-full-pricing-breakdown); [Sailor.sh](https://www.sailor.sh/blog/cka-certification-cost-2026); [CNCF CNPE](https://www.cncf.io/training/certification/cnpe/).

The hands-on CNCF exams are a stronger skill signal than multiple-choice cloud AI exams, because they require real terminal work. That is an inference from the exam format; no employer data was found on how much hiring managers value specific certifications.

A free or low-cost core curriculum covers the whole stack:

- **Chip Huyen's *AI Engineering*** (O'Reilly, December 2024, 534 pages) covers evaluation, RAG, agents and fine-tuning. Pair it with her *Designing Machine Learning Systems* for classic ML ([O'Reilly](https://www.oreilly.com/library/view/-/9781098166298/); [aie-book](https://github.com/chiphuyen/aie-book)).
- **Made With ML** teaches production MLOps with Ray, MLflow and GitHub Actions ([Made With ML](https://github.com/GokuMohandas/Made-With-ML)).
- **Hugging Face's free courses** on LLMs, agents and MCP (the last built with Anthropic) cover the application layer ([Agents Course](https://github.com/huggingface/agents-course); [MCP Course](https://github.com/huggingface/mcp-course)).
- **The Ultra-Scale Playbook** draws on more than 4,000 scaling experiments on up to 512 GPUs to teach data, tensor, pipeline and context parallelism ([Ultra-Scale Playbook](https://nanotron-ultrascale-playbook.static.hf.space/)).
- **Stanford CS336** published its Spring 2026 lectures ([Latent Space](https://news.latent.space/topic/language-modeling)).
- **Karpathy's nanochat** trains a GPT-2-class chat model end to end (tokenizer, pretraining, SFT, RL) in about two hours on an 8×H100 node, roughly $48 on demand or $15 on spot ([nanochat](https://github.com/karpathy/nanochat)).

| Stage | Hands-on project | Approximate cost | Cheapest route |
|---|---|---|---|
| 1. Cloud and deep-learning fundamentals | Terraform a VPC with private subnets, a least-privilege role and an encrypted dataset bucket plus a budget alert; destroy and recreate it. Train a small character-level model | $0–5 | Provider credits; Kaggle or Colab GPUs |
| 2. Containers and Kubernetes | Containerize a FastAPI inference service, deploy it to managed Kubernetes with autoscaling, then add a scale-to-zero GPU node pool with the GPU Operator | $3–10 per 4–6-hour lab | GKE fee credit; credits |
| 3. Model serving | Serve a 7–8B open model with vLLM on an L4 or L40S; benchmark TTFT, ITL and throughput across batch sizes and quantization | $2–6 per session (L40S about $0.92–0.99/hr) | Marketplace GPUs ([Hostinger](https://www.hostinger.com/tutorials/?p=158956)) |
| 4. RAG, agents and MCP | Build a hybrid-retrieval RAG app with RAGAS-style evals wired into CI; build an MCP server and connect an agent with tracing | $0–10, mostly API tokens | Hugging Face courses; local models |
| 5. MLOps and LLMOps | Run a QLoRA fine-tune on spot with checkpoint-resume to object storage, track it in MLflow, deploy behind vLLM, with a canary and drift monitoring | $2–15 (A100 spot from about $0.36/hr) | Kaggle T4s for small models ([Jarvislabs](https://docs.jarvislabs.ai/blog/a100-price)) |
| 6. Distributed training | Do a nanochat speedrun; compare DDP, FSDP and tensor parallelism on 2–8 GPUs, measuring MFU and memory | $15–50 | Single-GPU nanochat at about 8× the time |

Using credits for the CPU and networking stages and marketplace GPUs for the GPU stages keeps total out-of-pocket GPU spend at roughly $150–250. The biggest risk is forgetting to shut down a cluster or GPU node. Run Stage 4 in parallel with Stages 2–3: it needs little cloud spend and maps most directly to what job postings ask for.

## Conclusion

The most durable thing an AI engineer can learn is not any product, because the products churned within twelve months:

- Vertex AI became the Gemini Enterprise Agent Platform.
- OpenAI's Assistants API shut down, and its self-serve fine-tuning platform closed to new users.
- TGI, torchtune and CML went dormant or into maintenance.
- Training Operator v1 gave way to TrainJob.
- Four major cloud AI certifications retired.

What survived intact is a way of reasoning in bytes and queues: bytes per parameter, KV bytes per token, bytes per training step across which link, bytes per dollar, and then goodput, utilization and cache-hit rate on top. An engineer who can work out on paper a 21 ms decode floor, a 16-byte-per-parameter ledger, a three-hour MTBF and a cache break-even can evaluate a new GPU SKU, serving engine or managed API in minutes. That skill also makes vendor benchmarks, most of which this research could not verify independently, much less persuasive.

2026 also overturned two economic assumptions, with implications that are easy to miss. GPU-hour prices stopped falling predictably and rose instead. Meanwhile the token price of comparable capability fell about tenfold within a single vendor's generation (Haiku 4.5 at $1/$5 to Haiku 5.5 at $0.10/$0.50). The self-host break-even therefore keeps moving toward APIs for everything except steady, high-volume, data-sovereign workloads. The engineer's leverage shifts from procuring GPUs to raising utilization, cache-hit rates and cost per successful task. At the same time, the control points of the stack are consolidating under a few owners:

- NVIDIA with SchedMD, KAI, Dynamo and the Groq license;
- CoreWeave with Weights & Biases;
- OpenAI with Promptfoo;
- ClickHouse with Langfuse.

That makes open interfaces the practical hedge against lock-in: OpenTelemetry GenAI, MCP, the Gateway API Inference Extension and Iceberg REST catalogs. The security lesson runs in parallel. The incidents that mattered were system-level failures that a classifier did not catch, and the defenses that hold are architectural, such as the Rule of Two and CaMeL. That makes AI security a design discipline you practice, not a filter you buy.
