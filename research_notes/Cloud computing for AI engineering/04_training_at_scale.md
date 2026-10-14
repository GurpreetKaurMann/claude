# Training and Fine-Tuning Large Models at Scale in the Cloud (state as of October 2026)

*Method note for the report writer: this session ran 21 web searches (search summaries plus result URLs) before the shared search budget ran out. Full-page fetches failed: WebFetch got DNS errors and the egress proxy refused arxiv.org and huggingface.co, so primary papers (ZeRO, Megatron, Llama 3, LoRA, Ultra-Scale Playbook) could only be read through search snippets. The search budget ran out before Azure, Vertex/GKE resiliency, MaxText/DeepSpeed/Colossal-AI, the activation-memory formula and MLflow were covered. Well-known facts from the textbook papers that this session could not re-verify are listed under each section's "Gaps" as "Background (unverified this session)", with the canonical source to check. Worked numeric examples under "Inferences" are my own arithmetic on the cited formulas. Items marked [OLDER] are pre-2025 and still foundational but no longer current-generation.*

---

## 1. Memory math and compute math for training (bytes/param, activations, checkpointing, 6ND, MFU)

### Takeaway
Mixed-precision Adam training costs about **16 bytes per parameter** before activations: 2 for BF16/FP16 weights, 2 for gradients, and 12 for FP32 master weights plus Adam m and v. Accountings that also keep FP32 gradients give 18–20 B/param. Activations scale with sequence × batch × hidden × layers and usually dominate at long context, which is why activation checkpointing, sequence/context parallelism and FlashAttention are standard. Training compute ≈ **6 × N × D FLOPs**. Well-tuned dense runs on H100-class hardware typically reach about **35–45% BF16 MFU** (Llama 3 at 16K GPUs is reported in the high 30s to low 40s).

### Cited Findings
- **ZeRO's mixed-precision Adam ledger** [OLDER, 2020, still the standard reference]: FP16 params 2Ψ + FP16 grads 2Ψ + optimizer state 12Ψ (FP32 params 4Ψ, momentum 4Ψ, variance 4Ψ) = **16Ψ bytes** for Ψ parameters. ZeRO writes the optimizer multiplier as K = 12. — [ZeRO paper (SC20)](https://aiichironakano.github.io/cs596/Rajbhandari-ZeRO-SC20.pdf)
- **Alternative accounting = 20 B/param**: ZeRO-Infinity counts FP16 params and grads plus FP32 momentum, variance, params *and gradients* in the optimizer state, i.e. **20 bytes/param**. The gap from 16 is the FP32 gradient copy. — [ZeRO-Infinity paper](https://arxiv.org/pdf/2104.07857)
- A 2026 synthesis describes "roughly 16 bytes per parameter before activations and fragmentation", and notes that sharding changes the per-device share but not the aggregate volume. — [Placement Semantics for Distributed DL (arXiv 2601.02311)](https://arxiv.org/pdf/2601.02311)
- The Hugging Face **Ultra-Scale Playbook** (Feb 2025) is based on **4,000+ scaling experiments on 1–512 GPUs**. It frames the three core challenges as **memory usage, compute efficiency and communication overhead**, and treats activation recomputation as the main activation-memory lever. — [InfoQ coverage](https://www.infoq.com/news/2025/03/huggingface-ultra-scale-playbook); [Playbook (HF Space)](https://nanotron-ultrascale-playbook.static.hf.space/)
- **Llama 3 405B infrastructure** [2024]: trained on **up to 16K H100 GPUs, each at 700 W TDP with 80 GB HBM3**. — [Llama 3 Herd of Models (arXiv 2407.21783)](https://arxiv.org/pdf/2407.21783)
- Llama 3 utilization: secondary summaries report GPU utilization of **38–43%** during 405B training. The search tool could not confirm from the primary text that this is BF16 MFU. — [Medium/axinc-ai summary](https://medium.com/axinc-ai/takeaways-from-the-llama-3-release-paper-90428875b2d4); [shchegrikovich substack](https://shchegrikovich.substack.com/p/why-its-hard-to-train-a-model-like)
- **DeepSeek-V3** [Dec 2024]: 671B total / **37B active** params, **14.8T tokens**, **2.788M H800 GPU-hours** for pre-training + context extension + post-training, about **$5.576M at an assumed $2/GPU-hr** (official run only, excluding ablations). Secondary sources give **2,048 H800 GPUs**. — [DeepSeek-V3 Technical Report (arXiv 2412.19437)](https://arxiv.org/pdf/2412.19437); [summary](https://wentao.site/deepseek_v3_summary/)
- **TorchTitan** notes that once Float8 is enabled, MFU has to be computed against a *mix* of BF16 and FP8 Tensor Core peaks. MFU numbers from FP8 runs are therefore not directly comparable to BF16 MFU. — [TorchTitan, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/e6231c5f46598cfd09ff1970524e0436-Paper-Conference.pdf)

### Inferences
- **Worked memory examples (16 B/param, before activations):**
  - 7B: 7e9 × 16 = **112 GB**. A full fine-tune does not fit on a single 80 GB H100 without sharding or offload.
  - 70B: **1.12 TB**. Spread over 8 GPUs with ZeRO-3/FSDP that is 140 GB/GPU, which does not fit an 80 GB card. Over 64 GPUs it is **17.5 GB/GPU**.
  - 405B: **6.48 TB** of weights + grads + optimizer state.
- **ZeRO per-GPU formulas** (from the 2Ψ/2Ψ/KΨ ledger, data-parallel degree N_d):
  - Baseline DP: (2+2+K)Ψ.
  - ZeRO-1 (shard optimizer): 2Ψ + 2Ψ + KΨ/N_d.
  - ZeRO-2 (+ shard grads): 2Ψ + (2+K)Ψ/N_d.
  - ZeRO-3 / FSDP full-shard (+ shard params): (2+2+K)Ψ/N_d.
  - Example, 7.5B with N_d = 64: 120 GB → 31.4 GB (Z1) → 16.6 GB (Z2) → 1.9 GB (Z3).
  - The search tool also returned a 7.5B example of "120 → 52.5 → 41.3 GB" without a GPU count. That arithmetic matches N_d = 4: 30 + 90/4 = 52.5 and 15 + 105/4 = 41.25.
- **Where "16–18 bytes" comes from**: 16 is the ZeRO ledger. 18 shows up when a stack keeps BF16 weights (2) plus FP32 gradients (4) plus 12 B of optimizer state, with no separate BF16 gradient copy. 20 counts both BF16 and FP32 gradients (ZeRO-Infinity). All are variants of the same ledger. The 18 B breakdown is my reconstruction.
- **Compute examples with 6ND:**
  - 7B model × 2T tokens = 6 × 7e9 × 2e12 = **8.4e22 FLOPs**. Assuming an H100 dense BF16 peak of about 989 TFLOP/s (background value, unverified) at 40% MFU (about 396 TFLOP/s achieved), that is about 2.1e8 GPU-s ≈ **59K GPU-hours**, or about 2.4 days on 1,024 GPUs.
  - DeepSeek-V3: 6 × 37e9 × 14.8e12 ≈ **3.3e24 FLOPs** over 2.788M GPU-hours (1.0e10 GPU-s), giving about **330 TFLOP/s per GPU** on average. Against the H800's dense BF16 peak (about 989, background) that is about 33%; against its FP8 peak (about 1,979, background) it is about 17%. This is rough: it ignores attention FLOPs and the GPU-hours include post-training. It shows how sensitive "MFU" is to which peak you divide by.
- **MFU vs HFU**: MFU counts only the model's required FLOPs (6N per token plus attention). Hardware FLOPs utilization (HFU) also counts recomputation FLOPs, so full activation checkpointing raises HFU (about 8N/token) without raising MFU.

### Gaps
- Primary pages for the Ultra-Scale Playbook and Llama 3 could not be fetched, so exact playbook formulas and the Llama 3 MFU table are not verified here.
- **Background (unverified this session)**:
  - Activation memory per transformer layer (Korthikanti et al. 2022, "Reducing Activation Recomputation in Large Transformer Models", arXiv 2205.05198) ≈ **s·b·h·(34 + 5·a·s/h)** bytes with 16-bit activations (s = seq len, b = micro-batch, h = hidden, a = heads). **Selective recomputation** recomputes only the attention-score/softmax part (the 5as/h term), leaving about **34·s·b·h**. Tensor + sequence parallelism divide this by t. The paper reports about 5× activation memory reduction and about 54% MFU for a 530B model on 2,240 A100s [OLDER, 2022].
    - Worked example: h = 8192, a = 64, s = 8192, b = 1 gives about 23.8 GB/layer with no recompute and no FlashAttention, about 2.3 GB/layer with selective recompute, and about 0.29 GB/layer at TP = 8 + SP.
    - FlashAttention never materializes the s×s scores, which in practice removes the 5as/h term.
  - Llama 3 405B: about **3.8e25 FLOPs**, 15.6T tokens. Paper Table 4 reports **38–43% BF16 MFU** (about 380–430 TFLOP/s/GPU) for configurations with TP = 8, PP = 16, CP up to 16, DP up to 128. Verify at arXiv 2407.21783 §3.3.
  - **Chinchilla** compute-optimal ratio ≈ **20 tokens per parameter** (70B on 1.4T tokens; Hoffmann et al. 2022, arXiv 2203.15556) [OLDER]. Modern models deliberately "over-train" well past this ratio to get cheaper inference.
  - PaLM's MFU definition adds attention FLOPs (≈ 6N + 12·L·h·s per token). Check the PaLM paper (arXiv 2204.02311).

---

## 2. Parallelism strategies (DDP, ZeRO 1/2/3, FSDP/FSDP2, TP, PP, SP/CP, EP, 3D/4D) and how they map to NVLink vs the inter-node network

### Takeaway
Large runs stack data parallelism with sharding (ZeRO/FSDP) as the outer dimension on the cross-node network. Tensor and sequence parallelism, which are bandwidth-hungry and synchronous every layer, stay inside the NVLink domain. That domain was 8 GPUs per H100/B200 node and is now **72 GPUs per GB200/GB300 NVL72 rack**. Pipeline parallelism (low-volume point-to-point) spans nodes, and context and expert parallelism are added for long sequences and MoE. Pipeline "bubbles" cost **(p−1)/(m+p−1)** for 1F1B, about v× less with interleaving, and approach zero with Zero-Bubble or DualPipe schedules, which split the backward pass into separate weight-gradient and input-gradient steps.

### Cited Findings
- **1F1B bubble fraction = (p−1)/(m+p−1)** (p = stages, m = micro-batches). **ZB1P** (Zero Bubble, 1F1B-level memory) reduces the bubble to about **1/3 of 1F1B's**. **ZB2P** reaches **~zero bubble at ~2× activation memory**. The method splits the backward pass into B (input-grad) and W (weight-grad) and schedules W into idle slots. — [sail-sg Zero-Bubble repo](https://github.com/sail-sg/zero-bubble-pipeline-parallelism); [Zero Bubble paper (arXiv 2401.10241)](https://arxiv.org/pdf/2401.10241)
- The approximation (p−1)/m applies when m ≫ p. **Interleaved 1F1B** with v model chunks per GPU shrinks the bubble by a factor of v, to about (p−1)(F+B)/v, at the cost of **v× more point-to-point communication** and more activation memory. — [Bruno Maga, pipeline parallelism notes](https://brunomaga.github.io/pipeline-parallelism); also written as (p−1)/(v·m) in [whatdhack Medium overview](https://whatdhack.medium.com/distributed-compute-parallelisms-tensor-sequence-context-pipeline-expert-and-fully-sharded-78a666e9080e)
- **DualPipe** (DeepSeek-V3): a bidirectional pipeline schedule with **fewer pipeline bubbles that hides most communication** (including MoE all-to-all) behind compute. It is described as extending Zero Bubble ideas beyond 1F1B and ZB1P. — [DeepSeek-V3 report](https://arxiv.org/pdf/2412.19437); [Hybrid Parallelism comparative study (arXiv 2602.09109)](https://arxiv.org/pdf/2602.09109)
- **ZeRO stages**: Stage 1 shards optimizer states, Stage 2 also shards gradients, Stage 3 also shards parameters (memory formulas in §1). — [ZeRO paper](https://aiichironakano.github.io/cs596/Rajbhandari-ZeRO-SC20.pdf)
- **FSDP2** uses **per-parameter sharding built on DTensor**, replacing FSDP1's flat-parameter design. TorchTitan composes FSDP2 with TP, PP and CP ("4D"). — [TorchTitan PyTorch Conf 2024 slides](https://hosted-files.sched.co/pytorch2024/1c/torchtitan_%20Large%20Scale%20LLM%20Training%20Using%20Native%20PyTorch%203D%20Parallelism.pdf); [TorchTitan ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/e6231c5f46598cfd09ff1970524e0436-Paper-Conference.pdf)
- **Stacking parallelism pays off (TorchTitan on H100)**: over optimized baselines, **+65.08%** for Llama 3.1 8B (128 GPUs, 1D), **+12.59%** for 70B (256 GPUs, 2D), and **+30%** for 405B (512 GPUs, 3D). — [TorchTitan ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/e6231c5f46598cfd09ff1970524e0436-Paper-Conference.pdf); [ResearchGate copy](https://www.researchgate.net/publication/384770804_TorchTitan_One-stop_PyTorch_native_solution_for_production_ready_LLM_pre-training)
- **Context parallelism in production (2026)**: Megatron Bridge 0.6.0 (Aug 2026) highlights GLM-5.2 training with cuDNN fused DSA (DeepSeek sparse attention) at **128K context using THD-packed context-parallel training**. — [Megatron-Bridge GitHub](https://github.com/NVIDIA-NeMo/Megatron-Bridge)
- **GB200 NVL72 as one NVLink domain**: NVLink 5 provides **1.8 TB/s per GPU**, and the NVL72 rack forms a single **72-GPU NVLink domain**. — [abhik.ai multi-GPU communication](https://www.abhik.ai/concepts/gpu-computing/multi-gpu-communication); [yobitel NCCL KB](https://yobitel.com/knowledge-base/nccl) (search-summary attribution; pages not fetched)
- AWS P6e-GB200 UltraServers come in **36- and 72-GPU sizes under one NVLink domain**. — [AWS P6 page](https://aws.amazon.com/ec2/instance-types/p6); [HPCwire](https://www.hpcwire.com/off-the-wire/aws-launches-ec2-ultraservers-powered-by-nvidia-grace-blackwell/)

### Inferences
- **Mapping rule of thumb (innermost to outermost): TP(+SP) → CP → EP → PP → DP/FSDP.**
  - TP all-reduces/all-gathers activations several times per layer, every micro-batch, on the critical path, so it belongs on NVLink. With 8-GPU nodes that caps TP at 8. On NVL72, TP and EP can span up to 72 GPUs.
  - PP sends only boundary activations point-to-point, so it tolerates the slower 400 Gb/s-per-GPU scale-out network.
  - DP/FSDP gradient reduce-scatters and parameter all-gathers can be overlapped with compute (prefetch, bucketing), so they go outermost.
- **Bubble examples**:
  - p = 8, m = 32, 1F1B: 7/39 ≈ **18%** idle.
  - Interleaved with v = 4: about 7/(4·32) ≈ **5.5%**.
  - p = 16 (Llama 3 405B's background PP degree) needs m ≫ 16 to stay under 10%. That couples the global batch size to the pipeline depth, which is one reason Zero-Bubble and DualPipe exist.
- **Communication volume**:
  - DDP and ZeRO-1/2 move about 2Ψ of gradient traffic per step (reduce-scatter + all-gather, or all-reduce).
  - ZeRO-3/FSDP adds a parameter all-gather in the backward pass, about 1.5× DDP volume (3Ψ; background claim from the ZeRO paper).
  - So FSDP/ZeRO-3 trades roughly 50% more network traffic for N_d-way memory savings.
  - HSDP (hybrid sharding: shard within node or rack, replicate across) is the usual compromise on cloud networks.
- **MoE expert parallelism** turns gradient-style traffic into **all-to-all token dispatch/combine twice per MoE layer** in the forward pass (and again in the backward pass). That is why DeepSeek built DualPipe to overlap it, and why NVL72-scale NVLink domains favour large-EP MoE training.

### Gaps
- No source fetched this session gave Megatron's exact TP communication pattern or the ring-attention CP algorithm details. Exact DualPipe bubble formula: the snippet was truncated; check the DeepSeek DualPipe README (github.com/deepseek-ai/DualPipe).
- **Background (unverified this session)**:
  - Megatron TP (Shoeybi et al. 2019, arXiv 1909.08053 [OLDER]) splits MLP column-then-row and attention by heads, giving **2 all-reduces forward + 2 backward per layer**.
  - Sequence parallelism (Korthikanti 2022) shards LayerNorm/dropout activations along the sequence and replaces the all-reduces with all-gather + reduce-scatter.
  - Context parallelism shards the whole sequence across GPUs using ring attention (Liu et al. 2023) or all-gather KV.
  - GPipe (Huang et al. 2018, arXiv 1811.06965 [OLDER]) introduced micro-batch pipelining with an all-forward-all-backward (AFAB) schedule, which needs activations for all m micro-batches. 1F1B caps in-flight activations at about p micro-batches.
  - Llama 3 used a [TP, CP, PP, DP] ordering with TP = 8 inside nodes, plus FSDP-style ZeRO-1/2 sharding for DP. Verify at the Llama 3 paper §3.3.2.

---

## 3. Frameworks (PyTorch/torchrun/FSDP2/DTensor/torchtitan, DeepSpeed, Megatron Core, NeMo, JAX/MaxText, HF Accelerate/Trainer, Colossal-AI)

### Takeaway
By late 2026 the stack has consolidated around two families. **PyTorch-native** covers FSDP2 + DTensor, torchtitan as the reference pretraining platform, and DCP checkpointing, launched with torchrun or Kubernetes. **NVIDIA Megatron** covers Megatron Core, now packaged via **NeMo Megatron Bridge**, which converts both ways to and from Hugging Face checkpoints, plus **NeMo AutoModel** for day-0 fine-tuning of HF models. JAX/MaxText remains the TPU path. DeepSpeed (ZeRO) and HF Accelerate/Trainer remain common for mid-scale and fine-tuning work.

### Cited Findings
- **TorchTitan** (ICLR 2025): a "one-stop PyTorch-native solution for production-ready LLM pre-training". It integrates FSDP2 (per-parameter DTensor sharding), TP, PP, CP, Float8, torch.compile and async distributed checkpointing. Speedups are listed in §2. — [TorchTitan ICLR 2025 paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/e6231c5f46598cfd09ff1970524e0436-Paper-Conference.pdf); [GitHub pytorch/torchtitan](https://github.com/pytorch/torchtitan); [arXiv 2410.06511](https://arxiv.org/html/2410.06511v1)
- Community forks extend torchtitan to **DeepSeek V2/V3 training with block-wise FP8 or MXFP4** linear, grouped-GEMM and attention. — [hann-wang/torchtitan](https://github.com/hann-wang/torchtitan)
- **Megatron Bridge** is "a training library for Megatron-based models with bidirectional Hugging Face conversion".
  - **v0.6.0 released 2026-08-19**. The README date conflicts by one day with PyPI's 2026-08-20.
  - Later tags exist: 0.6.2 and a **26.09-alpha.rc1** container.
  - PyPI shows 0.6.1 as yanked for "wrong version".
  - — [Megatron-Bridge GitHub](https://github.com/NVIDIA-NeMo/Megatron-Bridge); [Releases](https://github.com/NVIDIA-NeMo/Megatron-Bridge/releases); [PyPI](https://pypi.org/project/megatron-bridge/)
- NeMo container **26.04** pins **Megatron Core 0.17.0** with Megatron-Bridge 0.4.0. The Megatron Bridge release notes reference NeMo **26.08** containers. — [Megatron Bridge software versions](https://docs.nvidia.com/nemo/megatron-bridge/latest/releases/software-versions.html); [NeMo Framework changelog](https://docs.nvidia.com/nemo-framework/user-guide/latest/changelog.html)
- **NeMo AutoModel** (Hugging Face-native, day-0 support for HF models): **v0.6.0 released 2026-08-26** (latest on PyPI). — [nemo-automodel PyPI](https://pypi.org/project/nemo-automodel/); [AutoModel discussion #477](https://github.com/NVIDIA-NeMo/Automodel/discussions/477)
- PyTorch DCP (torch.distributed.checkpoint) supports **async_save**, **process-based async checkpointing**, **save-plan caching** and **rank-local checkpointing** (details in §6). — [PyTorch blog: DCP efficient checkpointing](https://pytorch.org/blog/distributed-checkpoint-efficient-checkpointing-in-large-scale-jobs/); [DCP async tutorial](https://docs.pytorch.org/tutorials/recipes/distributed_async_checkpoint_recipe.html)

### Inferences
- **Naming as of 2026**: "NeMo" for LLM pretraining now effectively means *Megatron Core via Megatron Bridge*, and NeMo AutoModel covers HF-native fine-tuning. The older NeMo 1.x/2.0 "NeMo-Megatron" naming is legacy [OLDER]. Treat Megatron-LM (the repo) as the research and reference code and Megatron Core as the library.
- **Choosing a stack**:
  - Pure PyTorch / research / custom models → torchtitan or FSDP2 directly.
  - Max NVIDIA throughput at 1K+ GPUs, MoE, FP8/NVFP4 recipes → Megatron Core / Megatron Bridge with Transformer Engine.
  - TPUs → JAX + MaxText (and Pathways on Google Cloud).
  - Single node to a few nodes, or fine-tuning → HF Trainer/Accelerate with DeepSpeed ZeRO or FSDP2 backends, or TRL/Unsloth/Axolotl (§7).

### Gaps
- Search budget ran out before **JAX/XLA/MaxText**, **DeepSpeed** (latest version, DeepSpeed-Ulysses/ZeRO++ status), **HF Accelerate/Transformers Trainer** and **Colossal-AI** were checked. No 2026 status was verified for these.
- **Background (unverified this session)**:
  - **torchrun** = torch.distributed.run, the elastic launcher (sets RANK/WORLD_SIZE/LOCAL_RANK; c10d rendezvous; `--nnodes=min:max` for elasticity; restarts on failure).
  - **FSDP2** API = `torch.distributed.fsdp.fully_shard`. FSDP1 (`FullyShardedDataParallel` wrapper) is legacy.
  - **DTensor** + DeviceMesh express sharding layouts (Shard/Replicate/Partial) across N-D meshes.
  - **DeepSpeed** provides ZeRO-1/2/3, ZeRO-Offload/Infinity (CPU/NVMe offload) and DeepSpeed-Ulysses sequence parallelism.
  - **MaxText** is Google's reference JAX LLM trainer on TPU/GPU, using XLA SPMD/GSPMD sharding.
  - **Colossal-AI** offers ZeRO + TP/PP + Gemini memory manager.
  - **HF Accelerate** wraps FSDP/DeepSpeed configs for the Transformers Trainer.

---

## 4. Collective communication and networking (all-reduce/all-gather/reduce-scatter, NCCL ring vs tree, NVLink/NVSwitch, InfiniBand, RoCE, AWS EFA, GCP GPUDirect, Azure IB)

### Takeaway
Scale-up and scale-out bandwidth differ by about 18–36×. Inside a node or rack, **NVLink 5 provides about 1.8 TB/s per GPU**. Across nodes, every major cloud gives about **400 Gb/s (≈ 50 GB/s) per GPU**: AWS P5/P6 with **3.2 Tb/s EFA per 8-GPU instance**, GCP A3 Ultra/A4 with **3.2 Tb/s non-blocking RoCE GPUDirect-RDMA**, and Azure with InfiniBand. That gap drives the parallelism placement in §2. Ring all-reduce is bandwidth-optimal (each GPU sends and receives 2(N−1)/N × message size). Tree has lower latency for small messages. NCCL picks per message size and topology, and measured results sometimes beat its default choice.

### Cited Findings
- **Ring all-reduce** moves **2(N−1)/N of the data per GPU** regardless of N, which makes it bandwidth-optimal for large messages. **Tree** algorithms suit latency-bound small messages. NCCL "bus bandwidth" normalizes measured throughput by this per-collective factor so it can be compared against link peak. — [factryze NCCL ring vs tree](https://factryze.ai/scale-atlas/collectives/nccl-allreduce-ring-vs-tree); [Leviathan NCCL bandwidth validation](https://www.leviathansystems.co/articles/nccl-bandwidth-validation) (search-summary attribution)
- **Real-world exception (GB200 NVL72)**: with three NVL partitions across racks and NVLS disabled, NCCL chose ring, but tree reached higher bus bandwidth at large sizes (e.g. **485.68 vs 393.66 GB/s at 24 GPUs**). — [NVIDIA/nccl issue #1801](https://github.com/NVIDIA/nccl/issues/1801)
- **NVLink 5 = 1.8 TB/s per GPU** (bidirectional; about 900 GB/s per direction). Older sources quote 900 GB/s for NVLink 4 (H100). — [abhik.ai](https://www.abhik.ai/concepts/gpu-computing/multi-gpu-communication); [yobitel NCCL](https://yobitel.com/knowledge-base/nccl)
- **InfiniBand NDR = 400 Gb/s per port** (the H100-generation fabric). — [abhik.ai](https://www.abhik.ai/concepts/gpu-computing/multi-gpu-communication) (search-summary attribution)
- **AWS EFA**:
  - P5, P5e, P5en (H100/H200) and Trn2 instances get up to **3,200 Gbps EFA**. — [AWS EC2 multi-network-card docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa-acc-inst-types.html); [EC2 UltraClusters](https://aws.amazon.com/ec2/ultraclusters)
  - **P6-B200**: up to **3.2 Tb/s EFAv4**.
  - **P6e-GB200 UltraServers**: up to **28.8 Tb/s total EFAv4** (72 GPUs × 400 Gb/s) in 36/72-GPU NVLink domains, with up to **17 network cards** configurable.
  - EFAv4 gives **up to 18% faster collectives** in distributed training than P5en with EFAv3 (vendor claim).
  - — [AWS P6 instance page](https://aws.amazon.com/ec2/instance-types/p6); [HPCwire](https://www.hpcwire.com/off-the-wire/aws-launches-ec2-ultraservers-powered-by-nvidia-grace-blackwell/); [AWS EKS DRA on P6e-GB200 blog](https://aws.amazon.com/blogs/containers/unlocking-next-generation-ai-performance-with-dynamic-resource-allocation-on-amazon-eks-and-amazon-ec2-p6e-gb200/); [insideHPC](https://insidehpc.com/2025/07/aws-announces-ai-servers-with-nvidia-blackwell/)
  - Unit caution: some secondary sources write EFAv4 as "400 GB/s per GPU". The arithmetic (28.8 Tb/s ÷ 72) gives about **400 Gb/s per GPU**, so "GB/s" is likely a typo. That conclusion is my arithmetic, not confirmed by AWS.
- **Google Cloud GPUDirect variants**:
  - **A3 Mega (H100)**: **1,800 Gbps** via **GPUDirect-TCPXO**. TCPXO requires the `a3-megagpu-8g` machine type and GKE Dataplane V2.
  - **A3 Ultra (H200) and A4 (B200)**: **non-blocking 3.2 Tb/s inter-node GPU-to-GPU via RoCE (GPUDirect RDMA)**. The Compute Engine table lists A4 at **3,600 Gbps** maximum total bandwidth; the 3.2 Tb/s figure is the inter-node number.
  - **GPUDirect RDMA is not compatible with NCCL Fast Socket or the TCPX/TCPXO plugins**. Don't install those on RDMA clusters.
  - — [Compute Engine: Networking and GPU machines](https://docs.cloud.google.com/compute/docs/gpus/gpu-network-bandwidth); [GKE: GPUDirect-TCPX/TCPXO](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/gpu-bandwidth-gpudirect-tcpx); [AI Hypercomputer: GKE A4/A3 Ultra cluster](https://docs.cloud.google.com/ai-hypercomputer/docs/create/gke-ai-hypercompute-custom); [AI Hypercomputer networking overview](https://docs.cloud.google.com/ai-hypercomputer/docs/networking-overview); [DraNet GKE RDMA](https://dranet.sigs.k8s.io/docs/user/gke-rdma/)
- Meta's Llama 3 cluster networking is described in the paper. The interruptions data in §6 includes network switch/cable faults as a failure class. — [Llama 3 paper](https://arxiv.org/pdf/2407.21783)

### Inferences
- **Why bandwidth matters (worked numbers)**:
  - A 7B model's BF16 gradients are 14 GB. A ring all-reduce sends about 2 × 14 = 28 GB per GPU per step.
  - At 50 GB/s per GPU (400 Gb/s EFA/RoCE/IB) that is about **0.56 s per step** if not overlapped. Over NVLink 4 at about 450 GB/s per direction it is about **0.06 s**.
  - For a 70B model under DDP it would be about 5.6 s across nodes. This is why large models use sharding + overlap, HSDP (all-gather inside the fast domain), gradient accumulation (fewer syncs per token), and TP/EP placement on NVLink.
- **Cloud fabric summary**: all three hyperscalers converge on **8 × 400 Gb/s per 8-GPU node** for H100/H200/B200. The fabrics differ: AWS uses SRD-based EFA (not RoCE or IB), GCP uses RoCE (A3 Ultra/A4) or TCPXO (A3 Mega, older), and Azure uses NVIDIA InfiniBand. The NCCL plugins differ too: aws-ofi-nccl for EFA, Google's gIB/TCPXO plugins for GCP, native IB on Azure. Getting the plugin and environment variables right is a frequent source of 2–5× slowdowns. That last figure is my estimate, not a sourced number.
- **Collective semantics**:
  - all-reduce = reduce-scatter + all-gather. DDP and TP use all-reduce.
  - FSDP/ZeRO-3 use all-gather (params) + reduce-scatter (grads).
  - MoE uses all-to-all.
  - PP uses point-to-point send/recv.

### Gaps
- **Azure** (ND H100 v5, ND H200 v5, ND GB200 v6, ND GB300 v6) InfiniBand figures were not verified: the search budget ran out before that query.
- **InfiniBand XDR / Quantum-X800 (800 Gb/s)** and ConnectX-8 were not confirmed by any source this session.
- **Background (unverified this session)**:
  - Azure ND H100 v5 has 8 × 400 Gb/s NDR InfiniBand = 3.2 Tb/s per VM.
  - ND GB200 v6 uses NVL72 racks with 400 Gb/s IB per GPU. ND GB300 v6 uses Quantum-X800 at 800 Gb/s per GPU.
  - GB200 NVL72 has about 130 TB/s aggregate NVLink bandwidth. NVSwitch also offers in-network reduction (NVLS/SHARP).
  - XDR InfiniBand = 800 Gb/s per port.
  - Llama 3 used RoCE at 400 Gb/s per GPU on Meta's 24K-GPU clusters.
  - Verify all of these at NVIDIA and Microsoft Learn docs.

---

## 5. Mixed precision (FP32/TF32/BF16/FP16/FP8/MXFP4/NVFP4; loss scaling)

### Takeaway
**BF16 mixed precision with FP32 master weights is the default.** It needs no loss scaling because BF16 has FP32's exponent range. **FP8 training** (E4M3/E5M2 with per-tensor, per-block or MX scaling) is production-proven at frontier scale on Hopper and Blackwell; DeepSeek-V3 used tile/block-wise FP8. **4-bit training is now real**: NVIDIA's **NVFP4** recipe matched FP8 on a 12B model over **10T tokens** and was used for Nemotron 3 pretraining (up to 25T tokens). FP16 is legacy and needs loss scaling.

### Cited Findings
- **NVFP4 pretraining** (NVIDIA, arXiv 2509.25149; v2 March 2026):
  - **12B hybrid Mamba-Transformer trained on 10T tokens** in 4-bit, described as "the longest publicly documented training run in 4-bit precision to date".
  - Validation loss closely tracks the FP8 baseline. **MMLU-Pro 62.58% (NVFP4) vs 62.62% (FP8)**.
  - The recipe uses **Random Hadamard Transforms** to bound block-level outliers, **2-D (two-dimensional) block quantization**, **stochastic rounding** (for gradients) and **a few layers kept in higher precision**.
  - The paper also compares NVFP4 against **MXFP4** on final validation loss vs tokens.
  - — [arXiv 2509.25149 (PDF)](https://arxiv.org/pdf/2509.25149); [HTML v1](https://arxiv.org/html/2509.25149v1)
- **NVFP4 in production models**: NVIDIA **Nemotron 3** used NVFP4 pretraining for **up to 25T tokens** on a hybrid Mamba-MoE. **Nemotron 3 Super** (2026) was pretrained with the NVFP4 recipe "for the entire token horizon". — [Nemotron 3 report (arXiv 2512.20856)](https://arxiv.org/pdf/2512.20856); [Nemotron 3 Super (arXiv 2604.12374)](https://arxiv.org/pdf/2604.12374)
- **DeepSeek-V3 FP8**: the first FP8 mixed-precision training validated at this scale (671B MoE). It uses fine-grained tile-wise quantization: **1×128 tiles for activations (per token) and 128×128 blocks for weights**. — [DeepSeek-V3 report](https://arxiv.org/pdf/2412.19437); [summary](https://wentao.site/deepseek_v3_summary/)
- **FP8-LM** (Microsoft, 2023 [OLDER]) studied FP8 for weights, gradients, optimizer states and communication. — [FP8-LM (arXiv 2310.18313)](https://arxiv.org/pdf/2310.18313)
- TorchTitan supports Float8 training. When it is enabled, both BF16 and FP8 Tensor Cores are used, which complicates MFU accounting. — [TorchTitan ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/e6231c5f46598cfd09ff1970524e0436-Paper-Conference.pdf)
- Community torchtitan forks implement **block-wise FP8 and MXFP4** for linear, grouped-GEMM and attention (DeepSeek V2/V3). — [hann-wang/torchtitan](https://github.com/hann-wang/torchtitan)

### Inferences
- **Memory and throughput implications**:
  - FP8 and FP4 mainly speed up GEMMs (about 2× and 4× the BF16 peak on Blackwell; background, unverified ratios) and shrink activation/communication size.
  - The FP32 master weights and Adam states (12 B/param) usually stay in high precision. So the 16 B/param ledger only drops modestly unless optimizer states are also compressed (e.g. 8-bit Adam).
- **2026 practice**:
  - BF16 is the safe baseline.
  - FP8 (Transformer Engine, delayed/current or block/MX scaling) is the mainstream speed-up on H100/H200/B200.
  - NVFP4 is the frontier option on Blackwell (B200/B300/GB200/GB300). It has NVIDIA's published recipe, but it is newer and less battle-tested outside NVIDIA's own runs.

### Gaps
- A secondary blog among the results claims NVFP4 needs **36% fewer tokens than MXFP4** to reach the same loss. Not verified against the paper.
- Search budget ran out before Transformer Engine docs and FP16 loss-scaling specifics could be checked.
- **Background (unverified this session)**:
  - **FP32** (8-bit exponent, 23-bit mantissa).
  - **TF32** (8e/10m, used by Tensor Cores for FP32 matmuls on Ampere+).
  - **BF16** (8e/7m: FP32 range, low precision, no loss scaling needed).
  - **FP16** (5e/10m: narrow range, gradients underflow, so it needs **dynamic loss scaling**: multiply the loss by S, unscale the gradients, skip the step and lower S on inf/NaN, raise S periodically) [OLDER default].
  - **FP8 E4M3** (more precision; forward weights/activations) and **E5M2** (more range; gradients). Transformer Engine originally used **delayed scaling** (per-tensor scale from an amax history).
  - **MXFP8/MXFP4** (OCP Microscaling): blocks of 32 elements share an E8M0 power-of-two scale.
  - **NVFP4**: blocks of 16 elements with an FP8 E4M3 scale plus a per-tensor FP32 scale, so it has a finer scale than MXFP4.
  - Verify at the NVIDIA Transformer Engine docs and the OCP MX spec.

---

## 6. Reliability at scale (failure rates, checkpointing math, async/distributed checkpointing, elastic training, stragglers, HyperPod, GKE/Vertex)

### Takeaway
At 16K GPUs, Meta saw an **unexpected interruption about every 3 hours** (419 in 54 days), about **78% hardware-related** and roughly half GPU/HBM. It still reached **>90% effective training time** through automation. Failure rate scales linearly with GPU count, so 100K-GPU jobs face an interruption about every half hour. Checkpoint interval follows the Young/Daly rule **W ≈ √(2·MTBF·C)**. Asynchronous and distributed checkpointing cut the blocking cost C by 5–19×, to under 1 s in PyTorch DCP prototypes. Cloud platforms now sell resiliency directly: AWS HyperPod added **checkpointless and elastic training** in Dec 2025.

### Cited Findings
- **Llama 3 54-day snapshot** (16K H100):
  - **466 job interruptions: 47 planned** (automated maintenance) and **419 unexpected**.
  - **~78%** of unexpected interruptions were confirmed or suspected hardware issues (GPU or host component failures, suspected silent data corruption). **GPU issues were the largest category, 58.7%** of unexpected issues.
  - Only **3** needed significant manual intervention. Effective training time was **>90%**.
  - — [Llama 3 paper](https://arxiv.org/pdf/2407.21783); [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/faulty-nvidia-h100-gpus-and-hbm3-memory-caused-half-of-the-failures-during-llama-3-training-one-failure-every-three-hours-for-metas-16384-gpu-training-cluster)
- Press summary: **faulty H100 GPUs and HBM3 memory caused about half of failures**, i.e. **one failure every ~3 hours** on the 16,384-GPU cluster. — [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/faulty-nvidia-h100-gpus-and-hbm3-memory-caused-half-of-the-failures-during-llama-3-training-one-failure-every-three-hours-for-metas-16384-gpu-training-cluster); [TweakTown](https://www.tweaktown.com/news/99589/metas-huge-16-384-nvidia-h100-ai-gpu-cluster-hbm3-memory-crashed-half-of-llama-3-training/index.html)
- Practitioner observation (2026): new clusters fail more often than mature ones ("the first two weeks are the worst"), i.e. hardware burn-in / infant mortality. — [Meg McNulty on X](https://x.com/meggmcnulty/status/2047337611858227405) (opinion, single source)
- **Young/Daly optimal checkpoint period: W_YD = √(2μC)** (μ = application MTBF, C = checkpoint cost). It is a first-order approximation; the exact optimum uses the Lambert W function.
  - Example: **μ = 4 h, C = 6 min gives W ≈ 54 min**.
  - Application MTBF scales as **μ_individual / p** for p components.
  - Caveats: it assumes memoryless (exponential) failures and coordinated checkpointing.
  - — [Benoit et al., "Checkpointing à la Young/Daly: An Overview"](https://dl.acm.org/doi/pdf/10.1145/3549206.3549328); [ICL-UTK copy](https://icl.utk.edu/files/publications/2022/icl-utk-1569-2022.pdf); [Young/Daly not good enough for workflows](https://dl.acm.org/doi/full/10.1145/3548607)
- **PyTorch async DCP**:
  - The original blog reported **>10× reduction** in checkpointing time, using a dedicated process group and `async_save`. — [PyTorch blog: Reducing checkpointing times by over 10x](https://pytorch.org/blog/reducing-checkpointing-times/)
  - The torchtitan forum post reported **~19× lower checkpoint overhead** than synchronous saves, and a prototype that overlaps the GPU→CPU copy with forward/backward cut it **a further 5×, to under 1 second**. — [PyTorch forums: torchtitan DCP efficiency](https://discuss.pytorch.org/t/distributed-w-torchtitan-optimizing-checkpointing-efficiency-with-pytorch-dcp/211250)
  - The TorchTitan paper reports async checkpointing **5–15×** less overhead than synchronous DCP for Llama 3.1 8B. — [TorchTitan (arXiv 2410.06511)](https://arxiv.org/html/2410.06511v1)
  - Newer DCP features: **process-based async checkpointing** (async checkpointer type = process), **save-plan caching** and **rank-local checkpointing**. — [PyTorch blog: DCP efficient checkpointing in large-scale jobs](https://pytorch.org/blog/distributed-checkpoint-efficient-checkpointing-in-large-scale-jobs/)
  - Caveat: torchtitan issue #930 reports a race condition, where async `CheckpointManager.save` may not block until staging completes, leading to load failures in a reproducer. — [torchtitan issue #930](https://github.com/pytorch/torchtitan/issues/930)
- **SageMaker HyperPod (announced 2025-12-03)**:
  - **Checkpointless training** recovers from healthy accelerators' in-memory state instead of a checkpoint-restart cycle. Recovery takes **minutes instead of hours**, and goodput is **>95% on clusters with thousands of accelerators**. Recipes for Llama, GPT-OSS and others offer zero-code enablement; custom PyTorch needs minimal changes. — [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2025/12/amazon-sagemaker-hyperpod-checkpointless-training); [AWS News Blog](https://aws.amazon.com/blogs/aws/introducing-checkpointless-and-elastic-training-on-amazon-sagemaker-hyperpod)
  - Vendor-reported results: **80–93% lower recovery time** in production-scale validation, and **>80% less downtime** on clusters from 16 to 2,000+ GPUs. — [AWS ML blog (Dec 2025)](https://aws.amazon.com/blogs/machine-learning/category/artificial-intelligence/page/15); [aws-news mirror](https://aws-news.com/article/2025-12-15-checkpointless-training-on-amazon-sagemaker-hyperpod-production-scale-training-with-faster-fault-recovery); [AWS News Blog](https://aws.amazon.com/blogs/aws/introducing-checkpointless-and-elastic-training-on-amazon-sagemaker-hyperpod)
  - **Elastic training**: jobs scale up onto idle accelerators and scale down without halting when higher-priority inference or evaluation needs capacity, governed by task-governance priorities. — [HyperPod features](https://aws.amazon.com/sagemaker-ai/hyperpod/features/)
  - Available in all HyperPod Regions. — [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2025/12/amazon-sagemaker-hyperpod-checkpointless-training)

### Inferences
- **MTBF scaling from Llama 3 data**:
  - 54 days × 24 h / 419 ≈ **3.1 h job MTBF** at 16,384 GPUs.
  - That is about 51K GPU-hours per failure for each GPU-equivalent (all components included).
  - Scaled linearly: about **47 min at 64K GPUs** and **~30 min at 100K GPUs**.
- **Young/Daly applied (μ = 186 min)**:
  - C = 5 min (synchronous save of a large checkpoint) gives W ≈ √(2·186·5) ≈ **43 min**, with about 23% waste. Waste at the optimum ≈ √(2C/μ) and excludes restart time.
  - C = 1 min gives W ≈ 19 min and about 10% waste.
  - C = 6 s of blocking time (async) gives W ≈ 6 min and about 3% waste.
  - Restart/reload time R adds about R/μ: R = 10 min costs about 5% more.
  - This is why the levers are async checkpointing (cut C), in-memory/peer checkpoint replicas or "checkpointless" recovery (cut R and lost work), hot spares and node auto-replacement (cut R), and burn-in plus health checks (raise μ).
- **Checkpoint size**: a full training state is about 16 B/param, so **6.5 TB for 405B** and 1.1 TB for 70B. Writing it takes about 65 s at 100 GB/s aggregate storage throughput. Sharded DCP writes in parallel from every rank, and async saves hide most of the time behind compute after a short GPU→CPU staging copy.
- **Stragglers**: in synchronous SPMD training one slow GPU or link slows every rank. Straggler detection compares per-rank step and collective timings (e.g. NCCL flight recorder / watchdog timeouts) and evicts or replaces outliers. The Llama 3 failure taxonomy included NCCL watchdog timeouts and SDC (silent data corruption). Taxonomy detail is background; see Gaps.

### Gaps
- **GKE / Vertex AI resiliency equivalents** were not researched: the search budget ran out. **Background (unverified)**: Google Cloud offers Cluster Director (formerly Hypercompute Cluster), GKE **multi-tier checkpointing** (RAM/local SSD → peer replication → GCS), an ML Goodput measurement library, Pathways for resilient JAX on TPU, and Vertex AI Training managed clusters (Slurm-based). Verify at Google Cloud AI Hypercomputer docs.
- **Background (unverified)**: the Llama 3 root-cause table lists faulty GPU 148 (30.1%), GPU HBM3 72 (17.2%), software bugs 54 (12.9%), network switch/cable 35 (8.4%), host maintenance 32 (7.6%), GPU SRAM 19 (4.5%), GPU system processor 17 (4.1%), NIC 7, NCCL watchdog 7, SDC 6, GPU thermal 6, and others. Meta also noted diurnal throughput variation of 1–2% from temperature, and **tens-of-MW power swings** across the cluster at job start/stop/checkpoint. Meta used **NCCLX** (its NCCL fork) and the PyTorch NCCL flight recorder. Verify at arXiv 2407.21783 §3.3.4.
- **Background (unverified)**: HyperPod's earlier resiliency features (deep health checks, automatic node replacement, **auto-resume** from the last checkpoint on Slurm/EKS) predate the Dec 2025 launch.

---

## 7. Fine-tuning (full FT vs PEFT: LoRA/QLoRA/DoRA; memory; SFT; DPO/RLHF-PPO/GRPO; managed services; libraries)

### Takeaway
Full fine-tuning costs the same ~16 B/param as pretraining. **LoRA** trains only low-rank adapters. **QLoRA** also stores the frozen base in 4-bit NF4, which fits a **65B fine-tune on one 48 GB GPU, down from >780 GB** for 16-bit full FT. The post-training pipeline is **SFT → preference tuning (DPO) → RL**, where RL uses PPO or the critic-free **GRPO** with verifiable rewards. The managed-service landscape shifted in 2026. **OpenAI is winding down self-serve fine-tuning**: closed to new users since May 2026, new jobs end **Jan 6, 2027**. AWS Bedrock added **reinforcement fine-tuning** (Dec 2025), including open-weight models (Feb 2026). torchtune is no longer developed.

### Cited Findings
- **QLoRA** (Dettmers et al., 2023 [OLDER but still standard]):
  - Combines **4-bit NormalFloat (NF4)**, **double quantization** and **paged optimizers**.
  - Fine-tunes a **65B model on a single 48 GB GPU** without losing 16-bit performance: memory drops from **>780 GB to <48 GB** versus 16-bit full fine-tuning.
  - Double quantization saves about **0.37 bits/param (~3 GB for 65B)**.
  - Paged optimizers use NVIDIA unified memory to absorb gradient-checkpointing spikes on long sequences.
  - Applying LoRA to **all linear layers** is needed to match full 16-bit fine-tuning.
  - — [QLoRA (arXiv 2305.14314)](https://arxiv.org/pdf/2305.14314); [NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf)
- **GRPO** (introduced in DeepSeekMath, 2024): a PPO variant that **drops the learned value model (critic)**. It samples a **group of responses per prompt** and uses the group's mean reward as the baseline, which **reduces PPO's memory**. It is well suited to verifiable rewards (math, code). TRL provides **GRPOTrainer**. — [DeepSeekMath (arXiv 2402.03300)](https://arxiv.org/pdf/2402.03300); [TRL GRPO Trainer docs](https://huggingface.co/docs/trl/grpo_trainer); [HF LLM course GRPO chapter](https://huggingface.co/learn/llm-course/en/chapter12/3b)
- Sources disagree on GRPO's memory savings. One counts policy + frozen reference as 2 models vs PPO's 3 (policy, reference, value). Others point out that a reward model may still be resident. A "~40% savings" figure comes from a single secondary source. — [Kili Technology GRPO explainer](https://kili-technology.com/blog/grpo-group-relative-policy-optimization); [RL for LLMs survey (arXiv 2507.04136)](https://arxiv.org/pdf/2507.04136)
- **OpenAI fine-tuning wind-down (2026)**:
  - The model optimization page says OpenAI "is winding down the fine-tuning platform": no longer accessible to new users, existing users can create jobs "for the coming months", and **fine-tuned models remain available for inference until their base models are deprecated**. — [OpenAI model optimization guide](https://developers.openai.com/api/docs/guides/model-optimization)
  - Page updated **May 8, 2026**. The community thread reports active customers can run training jobs **through January 6, 2027**. — [OpenAI developer community](https://community.openai.com/t/openai-s-self-serve-fine-tuning-availability/1380481)
  - Single third-party source: since July 2, orgs with no fine-tuned-model inference in the previous 60 days lost new-job creation. — [usagebox analysis](https://usagebox.com/articles/openai-fine-tuning-wind-down-2027-cost-playbook)
- **OpenAI methods still documented**:
  - **SFT** is the default method.
  - **DPO** trains on prompt + preferred/rejected pairs and supports text only.
  - The cookbook recommends **SFT first, then DPO from the SFT model**.
  - 2026 third-party guides list GPT-4.1 / 4.1-mini for SFT and DPO, and **o4-mini for reinforcement fine-tuning (RFT)**. The GPT-5.x family is not fine-tunable.
  - — [OpenAI DPO guide](https://developers.openai.com/api/docs/guides/direct-preference-optimization); [OpenAI cookbook SFT/DPO/RFT](https://developers.openai.com/cookbook/examples/fine_tuning_direct_preference_optimization_guide); [respan 2026 guide](https://www.respan.ai/articles/openai-fine-tuning-guide)
- **Amazon Bedrock reinforcement fine-tuning**:
  - Launched **Dec 2025**, initially on **Amazon Nova** models. AWS claims **66% average accuracy gains over base models** (vendor claim). — [AWS What's New Dec 2025](https://aws.amazon.com/about-aws/whats-new/2025/12/bedrock-reinforcement-fine-tuning-66-base-models); [AWS ML blog: RFT for Nova](https://aws.amazon.com/blogs/machine-learning/reinforcement-fine-tuning-for-amazon-nova-teaching-ai-through-feedback)
  - **Feb 2026**: extended to **open-weight models with OpenAI-compatible APIs**, with launch models **qwen.qwen3-32b and openai.gpt-oss-20b**. Rewards can come from rule-based verifiable graders or AI judges. — [AWS What's New Feb 2026](https://aws.amazon.com/about-aws/whats-new/2026/02/amazon-bedrock-reinforcement-fine-tuning-openai/); [AWS ML blog technical walkthrough](https://aws.amazon.com/blogs/machine-learning/reinforcement-fine-tuning-on-amazon-bedrock-with-openai-compatible-apis-a-technical-walkthrough)
- Fine-tuned models are **not portable across managed platforms**, so platform choice means lock-in. — [bitslovers 2026 comparison](https://www.bitslovers.com/bedrock-vs-azure-ai-foundry-vs-vertex-ai/) (secondary)
- **torchtune** (PyTorch-native post-training) **wound down active development in 2025**. Maintainers promised only critical bug fixes and security patches through 2025, with no new features. The last PyPI release is **0.6.1**, and Snyk rates maintenance "Inactive". A May 2026 arXiv paper still describes it as a research tool. — [torchtune README](https://github.com/meta-pytorch/torchtune); ["The future of torchtune" issue #2883](https://github.com/meta-pytorch/torchtune/issues/2883); [Snyk](https://security.snyk.io/package/pip/torchtune); [arXiv 2605.21442](https://arxiv.org/abs/2605.21442)
- A secondary comparison recommends **Unsloth** for most teams that want fast single-GPU fine-tuning, and says torchtune's wind-down should shape new adoption decisions. — [aicoolies Unsloth vs torchtune](https://aicoolies.com/comparisons/unsloth-vs-torchtune) (low-confidence commercial source)
- **NeMo AutoModel** offers day-0 fine-tuning of Hugging Face models on NVIDIA's stack (v0.6.0, Aug 2026). — [nemo-automodel PyPI](https://pypi.org/project/nemo-automodel/); [discussion #477](https://github.com/NVIDIA-NeMo/Automodel/discussions/477)

### Inferences
- **Fine-tuning memory examples**:
  - Full FT of 7B ≈ 112 GB of states plus activations, so it needs 2+ 80 GB GPUs with FSDP/ZeRO.
  - LoRA on 7B: frozen BF16 base about 14 GB plus small adapters, adapter gradients and Adam states (tens to hundreds of MB), plus activations. Fits on one 24–48 GB GPU.
  - QLoRA on 7B: about 3.5–4 GB for 4-bit weights.
  - QLoRA on 70B: about 35–40 GB, so a single 48–80 GB GPU (my arithmetic, consistent with the 65B/48 GB result).
- **2026 managed-service picture**: OpenAI is exiting self-serve tuning while hyperscalers lean in, with Bedrock RFT including open weights. Enterprises wanting custom models increasingly move to open-weight models on Bedrock/Vertex/Foundry managed tuning, or self-host with TRL/Unsloth/Axolotl/NeMo on HyperPod/GKE.
- **RL post-training at scale** (GRPO-style) is now a distributed-systems problem in its own right. It mixes generation (inference engine, e.g. vLLM) with training, so rollout throughput and weight resharding between the two dominate cost. This is inferred from GRPO's group-sampling design; no source was fetched.

### Gaps
- **Vertex AI (Gemini tuning) and Azure AI Foundry fine-tuning** specifics for 2026 (methods, supported models, pricing) were not found in primary sources. Third-party comparison sites had unverifiable model and price claims.
- 2026 status of **Unsloth, Axolotl, LLaMA-Factory and TRL** (versions, multi-GPU support) was not verified.
- One vendor blog claims six OpenAI fine-tuned models shut down on **Oct 23, 2026**. Not verified on OpenAI's deprecations page.
- **Background (unverified this session)**:
  - **LoRA** (Hu et al. 2021, arXiv 2106.09685 [OLDER]): W = W₀ + (α/r)·B·A with B ∈ ℝ^{d×r} and A ∈ ℝ^{r×k}. Trainable params per adapted matrix = r(d+k).
    - On GPT-3 175B it cut trainable params by **~10,000×** and GPU memory by **~3×** versus Adam full FT, with **no added inference latency** once merged.
    - Example (my arithmetic): r = 16 on a 4096×4096 matrix trains 131K params instead of 16.8M (0.78%).
  - **DoRA** (Liu et al. 2024, arXiv 2402.09353): decomposes W into magnitude m and direction V/‖V‖ and applies LoRA to the direction only, getting closer to full-FT learning dynamics at the same inference cost.
  - **DPO** (Rafailov et al. 2023, arXiv 2305.18290): loss = −log σ(β[log πθ(y_w|x)/π_ref(y_w|x) − log πθ(y_l|x)/π_ref(y_l|x)]). No reward model and no online sampling, so it needs only 2 models (policy + frozen reference).
  - **RLHF-PPO** (InstructGPT) holds **4 models** (policy, reference, reward, value/critic).
  - **GRPO** advantage: Â_i = (r_i − mean(r))/std(r) over G samples per prompt, with a KL penalty to the reference added to the loss.
  - Verify all of these in the cited papers.

---

## 8. Experiment tracking (Weights & Biases, MLflow, TensorBoard)

### Takeaway
**Weights & Biases now belongs to CoreWeave**: the deal closed May 5, 2025 at about $1.7B. As of Sep 30, 2026, W&B SaaS accounts sign in through **CoreWeave Forge**, with existing contracts and pricing unchanged. W&B remains the de facto hosted tracker for large training runs. MLflow (open source, Databricks-backed) and TensorBoard (lightweight, local) are the main alternatives, but this session could not verify their 2026 status.

### Cited Findings
- CoreWeave announced the deal in March 2025 and **completed the acquisition on May 5, 2025**, at a reported **~$1.7B** (prior valuation $1.25B). — [CoreWeave: completes acquisition](https://www.coreweave.com/news/coreweave-completes-acquisition-of-weights-biases-2); [CoreWeave blog](https://coreweave.com/blog/coreweave-completes-acquisition-of-weights-biases); [StorageReview](https://www.storagereview.com/news/coreweave-acquires-weights-biases-for-1-7b-to-advance-ai-infrastructure); [PitchBook](https://pitchbook.com/news/articles/coreweave-acquires-ai-developer-platform-weights-biases)
- **As of September 30, 2026**, W&B Free, Pro and Enterprise SaaS accounts sign in through **CoreWeave Forge** with existing credentials. "Your current contract and pricing are not changing." W&B covers experiment tracking, evaluation and model management. — [CoreWeave: Weights & Biases is now part of CoreWeave](https://www.coreweave.com/companies/weights-and-biases)
- CoreWeave says existing W&B customers can keep deploying on-prem or on their preferred infrastructure providers, i.e. W&B is not tied to CoreWeave compute. — [CoreWeave acquisition announcement](https://www.coreweave.com/news/coreweave-to-acquire-weights-biases---industry-leading-ai-developer-platform-for-building-and-deploying-ai-applications)

### Inferences
- **What to log for large runs**: loss and grad-norm (spikes signal instability), learning rate, tokens/s and **MFU per step**, per-rank step time (straggler detection), memory high-water marks, checkpoint save/load durations, and restart events (goodput accounting).
- Ownership of trackers by GPU-cloud vendors (CoreWeave/W&B) and data platforms (Databricks/MLflow) may matter for procurement and data-residency decisions. That is my inference; there is no source on customer impact.

### Gaps
- **MLflow 3** (GenAI tracing/evaluation features, 2025–2026 releases), **TensorBoard** 2026 status, and cloud-native trackers (SageMaker managed MLflow, Vertex AI Experiments/TensorBoard, Azure ML MLflow integration) were not researched: the search budget ran out.
- **Background (unverified)**: SageMaker offers managed MLflow tracking servers. Vertex AI offers Vertex AI Experiments and a managed Vertex AI TensorBoard. Azure ML uses MLflow as its native tracking API.
