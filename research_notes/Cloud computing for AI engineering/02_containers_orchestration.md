# Containers and Orchestration for AI/ML Workloads (state as of October 2026)

> **Research-session note for the report writer.** WebFetch could not reach several doc domains this session (kubernetes.io, docs.nvidia.com, docs.aws.amazon.com, docs.cloud.google.com, openai.com, blog.kubeflow.org all returned DNS errors), and the shared web-search budget ran out partway through. To get around the fetch problem, primary sources were read from **GitHub** where possible: the kubernetes/website blog sources, NVIDIA/cloud-native-docs, and project READMEs and release pages. Facts tagged with a source link were verified this session. Items tagged **(background, not re-verified)** are standard practitioner knowledge, included because the brief asked for commands and YAML. Treat them as illustrative and check them before quoting as fact. The version timeline below is reconstructed from the sources: K8s 1.34 (Aug 2025), 1.35 (Dec 2025), 1.36 (Apr 22 2026), 1.37 "Garhwal" (Aug 26 2026).

---

## 1. Docker for ML: CUDA base images, driver/toolkit/runtime compatibility, NVIDIA Container Toolkit, image size, model weights, reproducibility

### Takeaway
The host owns the kernel driver. The image carries CUDA user-space libraries. The NVIDIA Container Toolkit connects the two, and since 2025 it does this mainly through **CDI (Container Device Interface)**: CDI became the GPU Operator default in 25.10, and toolkit v1.20.x (Sep 2026) is CDI/JIT-CDI-centric. Large model weights are increasingly **mounted, not baked**. Kubernetes **OCI image volumes went GA in v1.36**, so weights can ship as a separate, digest-pinned OCI artifact without being rebuilt into the app image.

### Cited Findings
**NVIDIA Container Toolkit: current state**
- Latest toolkit is **v1.20.1 (19 Sep 2026)**. It adds MIG management device injection in CDI and JIT-CDI mode, and **per-GPU CUDA memory limits (needs an R615+ driver)**. It also makes `nvidia-cdi-refresh` create device nodes before generating the CDI spec, and start before Docker/containerd/CRI-O — [NVIDIA/nvidia-container-toolkit releases](https://github.com/NVIDIA/nvidia-container-toolkit/releases)
- v1.20.0 (13 Aug 2026) improved CUDA compatibility handling: the compat hook reads libcuda.so ELF metadata and does exact driver-version matching. It also added driver discovery across multiple directories, IMEX channel request validation, and a hook that limits EGL/Vulkan visibility to the assigned GPUs. v1.19.0 (12 Mar 2026) treats unknown OCI spec fields as errors, supports read-only root filesystems, and adds CUDA forward compatibility on Tegra — [NVIDIA/nvidia-container-toolkit releases](https://github.com/NVIDIA/nvidia-container-toolkit/releases)
- GPU Operator 26.7.1 exposes the new soft/hard per-GPU CUDA memory limits through the env vars **`NVIDIA_GPU_MEMORY_REQUEST` and `NVIDIA_GPU_MEMORY_LIMIT`** (requires R615+) — [NVIDIA cloud-native-docs: GPU Operator release notes](https://github.com/NVIDIA/cloud-native-docs/blob/main/gpu-operator/release-notes.rst)
- **CDI is the default in GPU Operator 25.10.0 and later.** `cdi.enabled` is now `true` and `cdi.default` is deprecated/ignored. **Gotcha:** workloads that rely on the `NVIDIA_VISIBLE_DEVICES` env var must set `runtimeClassName: nvidia` — [GPU Operator release notes](https://github.com/NVIDIA/cloud-native-docs/blob/main/gpu-operator/release-notes.rst)
- GPU Operator 26.3.0 added an **NRI plugin** mode (containerd 1.7.30+, 2.1.x or 2.2.x; not CRI-O). In this mode no `nvidia` RuntimeClass is created and the containerd config is not modified. GPU Operator 26.7.0 raised the minimum supported containerd from 1.8 to **2.0** — [GPU Operator release notes](https://github.com/NVIDIA/cloud-native-docs/blob/main/gpu-operator/release-notes.rst)
- **Security: CVE-2025-23266 ("NVIDIAScape")** is a container escape in the toolkit's OCI hook, rated CVSS 9.0 Critical (CWE-426). Fixed in Container Toolkit **1.17.8** / GPU Operator **25.3.2** (also Device Plugin 0.17.3 and MIG Manager 0.12.2). NVIDIA lists all versions ≤1.17.7 as affected. Sources disagree on the CDI-mode cutoff: NVIDIA's bulletin says CDI mode before 1.17.5, Upwind says ≤1.17.4 — [NVIDIA security bulletin](https://nvidia.custhelp.com/app/answers/detail/a_id/5659/~/security-bulletin:-nvidia-container-toolkit---july-2025); [Wiz](https://www.wiz.io/vulnerability-database/cve/cve-2025-23266); [Upwind](https://www.upwind.io/feed/understanding-the-nvidiascape-cve%E2%80%912025%E2%80%9123266-container-toolkit-vulnerability-and-why-your-ai-workloads-are-most-likely-safe)
- A suggested interim mitigation for legacy runtimes is `disable-cuda-compat-lib-hook = true` in the toolkit config — [Fidelis](https://fidelissecurity.com/vulnerabilities/cve-2025-23266/)

**Driver versions in the field (late 2025 to 2026)**
- GPU Operator 25.10.0 defaulted to driver **580.95.05** (also 570.195.03 and 535.274.02). 26.3.0 defaulted to **580.126.20**. 26.7.0 bundles **595.91.07**, and 26.7.1 adds support for **615.71.09** — [GPU Operator release notes](https://github.com/NVIDIA/cloud-native-docs/blob/main/gpu-operator/release-notes.rst)

**Model weights: bake vs mount**
- **K8s v1.36 graduated "VolumeSource: OCI Artifact and/or Image" (KEP-4639) to stable.** The kubelet mounts content from OCI registries directly as a pod volume — [Kubernetes v1.36 release blog source](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-36-release/index.md)
- Timeline per an empirical study: alpha in 1.31, beta in 1.33, on by default in 1.35, GA in 1.36. Runtime support starts at containerd v2.1 (v2.2 for subPath) and CRI-O v1.31. The paper compares cold-start times of OCI image volumes, modelcar sidecars and S3 downloads — [arXiv 2607.16596](https://arxiv.org/html/2607.16596v1)
- Use case: model weights in an OCI registry are mounted as pod volumes, so updating the model no longer requires rebuilding the app image. Downstream tooling requires K8s 1.35+ with containerd 2.1+, and some operators reject tag references in favour of digest-pinned images — [bex.co blog](https://bex.co/blog/2026/07/11/kubernetes-136-oci-volumesource-build-artifacts); [LLMKube issue #1379](https://github.com/defilantech/LLMKube/issues/1379)
- KServe v0.20.0 added support for **multiple OCI sources in `storageUris`** — [KServe releases](https://github.com/kserve/kserve/releases)
- On managed clusters, EKS Auto Mode ships the **SOCI snapshotter** (lazy-loading pulls) and parallel image pull/unpack on GPU instances with local NVMe, to speed up large images — [AWS EKS docs (search snippet)](https://docs.aws.amazon.com/eks/latest/userguide/ml-node-pools.html); [AWS blog](https://aws.amazon.com/blogs/containers/how-to-run-ai-model-inference-with-gpus-on-amazon-eks-auto-mode)

### Inferences
- **Mental model: driver vs toolkit vs runtime (background, not re-verified).**
  - **Kernel driver + user-mode driver (`libcuda.so`)** live on the host, or in the GPU Operator's driver container. They are never baked into the app image.
  - **CUDA Toolkit** (nvcc, headers) is only needed in a *build* stage, i.e. the `-devel` image.
  - **CUDA runtime libraries** (cudart, cuBLAS, cuDNN, NCCL) ship in the image: `-runtime` / `-cudnn-runtime` tags, or the `nvidia-*` pip wheels that PyTorch pulls in.
  - **NVIDIA Container Toolkit** on the host injects the device nodes and the host driver libraries at container start.
  - **Compatibility rule:** the host driver must meet the minimum for the image's CUDA *major* version. Within a major version, minor-version compatibility applies. Generally cited minimums are R525+ for CUDA 12.x and R580+ for CUDA 13.x. The `cuda-compat` forward-compatibility package lets newer CUDA run on older datacenter drivers.
  - Canonical reference: [CUDA Compatibility guide](https://docs.nvidia.com/deploy/cuda-compatibility/). It was unreachable this session.
- The 580 default drivers in GPU Operator 25.10/26.3 fit a CUDA 13-era baseline. The jump to 595/615 drivers in 26.7 suggests clusters on the latest operator can run the newest CUDA 13.x images. This is an inference from the driver versions only.
- **Image-size and caching patterns (background, not re-verified):**
  ```dockerfile
  # syntax=docker/dockerfile:1.7
  ARG CUDA=12.8.1
  FROM nvidia/cuda:${CUDA}-cudnn-devel-ubuntu24.04 AS build
  RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv && rm -rf /var/lib/apt/lists/*
  COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
  WORKDIR /app
  COPY pyproject.toml uv.lock ./
  RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev   # lockfile => reproducible
  COPY src/ src/
  FROM nvidia/cuda:${CUDA}-cudnn-runtime-ubuntu24.04                        # no nvcc in final image
  COPY --from=build /app /app
  ENV PATH=/app/.venv/bin:$PATH
  ENTRYPOINT ["python","-m","src.serve"]
  ```
  - Put rarely changing layers (OS, CUDA, Python deps) first and code last.
  - Use BuildKit cache mounts for pip/uv caches.
  - Pin the base image by **digest** (`@sha256:...`), not by tag.
  - Commit lockfiles.
  - Since PyTorch wheels bundle the CUDA runtime, a `-base` or even a slim Python image is often enough for PyTorch-only workloads.
- **Local GPU containers (background, not re-verified):**
  ```bash
  sudo nvidia-ctk runtime configure --runtime=docker && sudo systemctl restart docker
  docker run --rm --gpus all nvidia/cuda:12.8.1-base-ubuntu24.04 nvidia-smi          # legacy/hook path
  sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml && nvidia-ctk cdi list    # CDI path
  docker run --rm --device nvidia.com/gpu=all ubuntu:24.04 nvidia-smi                  # CDI device syntax
  docker run --gpus all --ipc=host --shm-size=16g ...   # PyTorch DataLoader needs large /dev/shm
  ```
  - `nvidia-docker2` and `--runtime=nvidia` are **legacy**.
  - In Kubernetes, the `/dev/shm` equivalent is an `emptyDir: {medium: Memory}` mounted at `/dev/shm`.
- **Bake vs mount decision rule:**
  - Bake small models (<~1–2 GB) for hermetic, single-artifact deploys.
  - Mount multi-GB/TB weights from an OCI image volume (K8s ≥1.36, containerd ≥2.1), a node-local NVMe cache, a PVC/FSx/Filestore/Lustre volume, or object storage via a CSI driver. This keeps rebuilds and pulls fast and avoids having one 100 GB layer per model version.
  - Bake-in images also defeat registry layer dedup whenever the weights change.

### Gaps
- Exact current CUDA-major-to-minimum-driver table, and the latest CUDA 13.x minor version as of Oct 2026. docs.nvidia.com was unreachable and search budget was exhausted.
- Whether Docker Engine enables CDI by default in current versions, and which version made it default. Not verified.
- No primary source found this session on the current `nvidia/cuda` image tag policy (EOL of older CUDA/OS tags).

---

## 2. Kubernetes GPU scheduling: device plugin, GPU Operator, MIG/time-slicing/MPS, DRA, topology-aware and gang scheduling, Kueue/Volcano/KAI/JobSet/LWS, Karpenter

### Takeaway
As of Oct 2026, the core building blocks look like this:
- **DRA is GA** (core since 1.34). In 1.37, device taints, extended-resource mapping and device status also went **stable**.
- **Native gang scheduling** (Workload/PodGroup API) went **Beta in 1.37**, but is still **off by default** behind `GenericWorkload`.
- NVIDIA's **DRA driver** was donated to the CNCF/Kubernetes project (KubeCon EU, Mar 2026). It now lives under `kubernetes-sigs`, and the GPU Operator gained a `GPUCluster` CR to deploy it. The classic `nvidia.com/gpu` device plugin remains the most widely deployed path.
- Batch admission and quota are handled by **Kueue (v0.20.x)**, with Volcano, KAI Scheduler, JobSet and LWS filling scheduler and workload-shape roles.

### Cited Findings
**DRA (Dynamic Resource Allocation)**
- **DRA core graduated to GA in Kubernetes 1.34.** It is enabled by default and the default API is `resource.k8s.io/v1`. The project says it won't make breaking changes to DRA after GA — [Kubernetes blog: v1.34 DRA GA](https://kubernetes.io/blog/2025/09/01/kubernetes-v1-34-dra-updates/)
- **K8s 1.36 (Apr 2026), DRA:**
  - Stable: AdminAccess for ResourceClaims (KEP-5018), Prioritized Alternatives in device requests (KEP-4816), and PodResources API including DRA resources (KEP-3695).
  - Beta, on by default: partitionable devices, consumable capacity, device taints/tolerations, ResourceClaim device status, device attachment before pod scheduling, and extended resource support.
  - Alpha: native ResourceClaim support for workloads, DRA-native CPU management, downward API for device attributes, and resource availability visibility.
  - Source: [v1.36 release blog source](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-36-release/index.md)
- **K8s 1.37 (Aug 26 2026), DRA**, per the official DRA post (Sep 3 2026):
  - **Stable:** DRA Extended Resource support (KEP-5004; DRA drivers can satisfy `example.com/gpu`-style extended resource requests without a device plugin, the "migration bridge"); ResourceClaim device status with network interface data (KEP-4817); **device taints and tolerations** with cluster-wide `DeviceTaintRule` (KEP-5055); standard `resource.kubernetes.io/numaNode` attribute.
  - **Beta (off by default):** ResourceClaims for Workloads/PodGroups (KEP-5729, gate `DRAWorkloadResourceClaims`); device attributes downward API (KEP-5304).
  - **Alpha:** list-typed attributes, node-allocatable resource requests, `ResourcePoolStatusRequest` availability snapshots, optional node operations, CEL-derived attributes, **Device Compatibility Groups** (KEP-5963; rejects incompatible MIG vs vGPU partition combos up front), and the `PreQueueingHint` scheduler extension point.
  - Source: [K8s v1.37 DRA updates blog source](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-dra-updates.md)
- Conflict on partitionable devices (KEP-4815): the 1.36 blog lists it as beta. A third-party write-up says it did **not** graduate in 1.37, and it is absent from the 1.37 stable list. No evidence it is GA — [DEV Community](https://dev.to/devopsdaily/kubernetes-137-garhwal-what-shipped-and-what-slipped-1cmi); [v1.37 DRA blog source](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-dra-updates.md)
- Ambiguity: the 1.37 DRA post lists consumable capacity's fractional ranges (`DRAFractionalCapacityRange`) under its "alpha" heading but calls it Beta in the text — [v1.37 DRA blog source](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-dra-updates.md)

**NVIDIA DRA driver, KAI, GPU Operator**
- NVIDIA announced at **KubeCon EU 2026 (Amsterdam)** that it is donating the **DRA Driver for NVIDIA GPUs** to the CNCF, moving it from vendor governance to community ownership under the Kubernetes project. AWS, Broadcom, Canonical, Google Cloud, Microsoft, Nutanix, Red Hat and SUSE are collaborating. **KAI Scheduler was onboarded as a CNCF Sandbox project** — [NVIDIA blog](https://blogs.nvidia.com/blog/nvidia-at-kubecon-2026/); [Rawkode Academy](https://rawkode.academy/news/nvidia-donates-gpu-dra-driver-to-cncf)
- The DRA driver repo is now under **`kubernetes-sigs`** and manages two resource types, **GPUs** and **ComputeDomains**:
  - **ComputeDomains are officially supported.** They provide Multi-Node NVLink (MNNVL) reachability and isolation (IMEX daemons, domains and channels) and target GB200-class systems.
  - **GPU allocation via DRA is "not yet officially supported"**: the GPU kubelet plugin is disabled by default in the Helm chart.
  - Requires K8s 1.32+.
  - Source: [kubernetes-sigs / NVIDIA k8s-dra-driver-gpu README](https://github.com/NVIDIA/k8s-dra-driver-gpu)
- **GPU Operator versions:** latest GitHub release is **26.7.1 (23 Sep 2026)**. Earlier: 26.7.0 (21 Aug), 26.3.0 (20 Mar 2026), 25.10.0 (28 Oct 2025). The versioning scheme is now YY.M — [NVIDIA/gpu-operator releases](https://github.com/NVIDIA/gpu-operator/releases)
- **GPU Operator 26.7.0:**
  - New **`GPUCluster` custom resource** deploys the DRA driver (with ComputeDomain/MNNVL support), DCGM, DCGM Exporter and a DRA validation workload. It **cannot run alongside `ClusterPolicy`**, and requires K8s **v1.34.2+**, driver **580+** and a CDI-capable runtime.
  - KubeVirt full-GPU passthrough via DRA ResourceClaims.
  - NVIDIADriver CRD migration path from ClusterPolicy.
  - Helm chart available as an OCI artifact in NGC.
  - K8s 1.37 support added post-release.
  - Component versions: Container Toolkit v1.20.0, Device Plugin v0.20.0, DRA Driver v0.5.0, DCGM 4.6.0, MIG Manager v0.15.0.
  - A docs-source entry for **26.7.2** (DRA Driver v0.5.1) exists, but it was not yet on the GitHub releases page at fetch time.
  - Source: [GPU Operator release notes](https://github.com/NVIDIA/cloud-native-docs/blob/main/gpu-operator/release-notes.rst)
- **GPU Operator 26.3.0:**
  - Dynamic per-node MIG config generation replaces the static ConfigMap.
  - NVIDIA Driver CRD for multiple driver types/OS versions.
  - GB200 NVL4 support.
  - **NVIDIA Kata Manager deprecated** in favour of `kata-deploy`.
  - Source: [GPU Operator release notes](https://github.com/NVIDIA/cloud-native-docs/blob/main/gpu-operator/release-notes.rst)
- **GPU Operator 25.10.0** added HGX B300 / GB300 NVL72 support (new MIG profiles) and K8s 1.34 support — [GPU Operator release notes](https://github.com/NVIDIA/cloud-native-docs/blob/main/gpu-operator/release-notes.rst)

**Device plugin: sharing (time-slicing, MPS, MIG)**
- **Device plugin basics:**
  - GPUs are requested via the `nvidia.com/gpu` extended resource in container limits.
  - **Gotcha:** if a pod does *not* request GPUs on a GPU node, the plugin exposes **all** GPUs inside the container.
  - Prereqs: NVIDIA driver, nvidia-container-toolkit, and the nvidia runtime as default, or a RuntimeClass `nvidia`.
  - Source: [NVIDIA/k8s-device-plugin README](https://github.com/NVIDIA/k8s-device-plugin)
- **Time-slicing** (`sharing.timeSlicing`):
  - Options are `replicas`, `renameByDefault` (advertise as `nvidia.com/gpu.shared`) and `failRequestsGreaterThanOne` (recommended `true`). Example: 10 replicas on an 8-GPU node advertises 80 GPUs.
  - **No memory isolation, shared fault domain**, and no proportional compute guarantee.
  - Source: [k8s-device-plugin README](https://github.com/NVIDIA/k8s-device-plugin)
- **MPS** (`sharing.mps`):
  - Partitions memory (each client gets an equal fraction) and limits compute.
  - Experimental since v0.15.0. Not supported on MIG devices, full GPUs only, and mutually exclusive with time-slicing.
  - Source: [k8s-device-plugin README](https://github.com/NVIDIA/k8s-device-plugin)
- **MIG strategies** are `none` (default), `single` and `mixed`. Mixed exposes `nvidia.com/mig-<g>g.<mem>gb` resources — [k8s-device-plugin README](https://github.com/NVIDIA/k8s-device-plugin)
- Device-list strategies:
  - `envvar` (default, `NVIDIA_VISIBLE_DEVICES`), `volume-mounts`, `cdi-annotations` and `cdi-cri`.
  - `DEVICE_ID_STRATEGY` is `uuid` (default) or `index`.
  - Version conflict: the README text says v0.17.1, while GPU Operator 26.7.1 bundles device plugin **v0.20.1**, so the README version string appears stale.
  - Sources: [k8s-device-plugin README](https://github.com/NVIDIA/k8s-device-plugin); [GPU Operator release notes](https://github.com/NVIDIA/cloud-native-docs/blob/main/gpu-operator/release-notes.rst)

**Native gang scheduling / Workload-Aware Scheduling (WAS)**
- **1.36:** the Workload and PodGroup APIs were alpha at `scheduling.k8s.io/v1alpha2`, replacing v1alpha1. 1.36 also added an atomic PodGroup scheduling cycle (bind all or none) and workload-aware preemption (KEP-5710) — [v1.36 release blog source](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-36-release/index.md); [ScaleOps](https://scaleops.com/blog/kubernetes-1-36/)
- **1.37: Workload and PodGroup are Beta at `scheduling.k8s.io/v1beta1`.**
  - Feature gate **`GenericWorkload` (Beta, disabled by default)**, to be enabled on apiserver, controller-manager and scheduler. It now also covers workload-aware preemption.
  - Only the top-level PodGroup is queued.
  - The gang policy sets `minCount`, which is **mutable in 1.37** for elastic resizing. The `basic` policy schedules pods individually.
  - `disruptionMode` values were renamed to `all` / `single`.
  - Source: [K8s v1.37 WAS blog source](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-advancing-workload-aware-scheduling.md)
- Conflict on defaults: one outlet (ByteIota) claimed 1.37 gang scheduling is on by default. The official post says `GenericWorkload` is Beta and **disabled by default**. TechTimes mentions `v1alpha3`, but per the official post that version applies only to the alpha CompositePodGroup — [ByteIota](https://byteiota.com/kubernetes-1-37-garhwal-gang-scheduling-dra-hpa/); [TechTimes](https://www.techtimes.com/articles/325879/20260828/kubernetes-137-lands-gang-scheduling-beta-cuts-gpu-idle-costs-default.htm); [official](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-advancing-workload-aware-scheduling.md)
- **1.37 alphas:**
  - **CompositePodGroup** (`scheduling.k8s.io/v1alpha3`): a hierarchy where a parent gates on `minGroupCount` children and the whole tree binds atomically.
  - **Multi-level topology-aware workload scheduling** (gate `TopologyAwareWorkloadScheduling`): zone, then rack constraints, resolved top-down.
  - **`batch/v1` Job `.spec.scheduling`** (gate `WorkloadWithJob`): the Job controller auto-creates the Workload/PodGroup; `gang: {}` defaults `minCount` to `parallelism`.
  - A `workloadbuilder` Go library for controllers.
  - **JobSet integration is targeted for 1.38. Kueue has no WAS integration yet**; the long-term goal is to use WAS as Kueue's scheduling engine.
  - Source: [K8s v1.37 WAS blog source](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-advancing-workload-aware-scheduling.md)
- Verbatim 1.37 examples from the official post:
  ```yaml
  # Shared DRA claim for a whole gang (DRAWorkloadResourceClaims, beta, off by default)
  apiVersion: scheduling.k8s.io/v1beta1
  kind: PodGroup
  metadata:
    name: training-job-workers-pg
  spec:
    ...
    resourceClaims:
      - name: pg-claim
        resourceClaimTemplateName: my-claim-template
  ---
  apiVersion: v1
  kind: Pod
  metadata:
    name: topology-aware-workers-pg-pod
  spec:
    ...
    schedulingGroup:
      podGroupName: training-job-workers-pg
    resourceClaims:
      - name: pg-claim
        resourceClaimTemplateName: my-claim-template
  ```
  ```yaml
  # Gang-scheduled Job (WorkloadWithJob alpha gate)
  apiVersion: batch/v1
  kind: Job
  metadata:
    name: distributed-training-job
  spec:
    parallelism: 8
    completions: 8
    scheduling:
      schedulingPolicy:
        gang: {}                # minCount omitted → defaults to parallelism (8)
      schedulingConstraints:
        topology:
        - key: topology.kubernetes.io/zone
      disruptionMode:
        all: {}
    template:
      spec:
        containers:
        ...
  ```
  Source: [K8s v1.37 WAS blog source](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-advancing-workload-aware-scheduling.md)
- Other 1.37 AI-relevant items:
  - **Pod-level resource managers** (Beta, `PodLevelResourceManagers`, off by default) for NUMA alignment.
  - **HPA scale-to-zero** (Beta, **on by default**, object/external metrics only).
  - Scheduler preemption for in-place pod resize (Alpha).
  - **cgroup v1:** `failCgroupV1` has defaulted to true since 1.35.
  - Source: [v1.37 release blog source](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)

**Kueue, JobSet, LWS, Volcano, KAI**
- **Kueue:**
  - Latest **v0.20.1 (8 Oct 2026)**.
  - **v0.20.0 (30 Sep 2026) stopped serving the `v1beta1` API**: migrate to `v1beta2` before upgrading, using the provided script.
  - Recent work covers TAS (topology-aware scheduling, including elastic TAS and failed-node replacement) and MultiKueue.
  - Source: [kueue releases](https://github.com/kubernetes-sigs/kueue/releases)
- Kueue is job-level queueing: it decides when a job starts and when its pods stop.
  - Concepts: ResourceFlavor, ClusterQueue, LocalQueue, Workload, cohorts, fair sharing, preemption, and StrictFIFO/BestEffortFIFO.
  - Integrations: batch Job, Kubeflow training jobs, RayJob/RayCluster, JobSet, and plain Pods and pod groups.
  - TAS and **MultiKueue** dispatch work to other clusters with capacity.
  - Supports cluster-autoscaler **ProvisioningRequest** via AdmissionChecks.
  - Officially supported on K8s 1.34+. Install: `kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.20.1/manifests.yaml`
  - Source: [kueue README](https://github.com/kubernetes-sigs/kueue)
- **JobSet** runs a group of Jobs as one unit for HPC/MPI and AI training:
  - `replicatedJobs` multi-template; `successPolicy` (Any/All); `failurePolicy` with per-error rules (v0.6+); `startupPolicy` ordering.
  - Headless service and stable hostnames via Indexed Jobs.
  - Exclusive 1:1 job-to-topology-domain placement annotation.
  - API `v1alpha2`; README install references **v0.13.0**; works with Kueue.
  - Source: [jobset README](https://github.com/kubernetes-sigs/jobset)
- **LeaderWorkerSet (LWS)** is a "group of pods as a unit of replication" for **multi-host inference**:
  - Leader and worker templates, a unique index per pod, and alpha gang scheduling.
  - Opt-in topology co-location and opt-in all-or-nothing group restart.
  - Group-level rolling updates; HPA via the scale subresource.
  - New **DisaggregatedSet** built on LWS for disaggregated (prefill/decode) serving, co-designed with **llm-d**.
  - Tested on K8s 1.34–1.37.
  - Source: [lws README](https://github.com/kubernetes-sigs/lws)
- **Volcano** is a **CNCF incubating** batch scheduler built on kube-batch. Its compatibility table lists **v1.15**, and it is doing network-topology-aware (HyperNode) scheduling for LLM training — [volcano README](https://github.com/volcano-sh/volcano)
- **KAI Scheduler** (NVIDIA, from Run:ai, built on kube-batch, **CNCF sandbox**):
  - Gang scheduling, hierarchical queues, DRF fair share plus time-based fairshare, GPU sharing.
  - TAS including hierarchical PodGroups, consolidation/defragmentation, and DRA support.
  - Source: [KAI-Scheduler README](https://github.com/NVIDIA/KAI-Scheduler)
- A third-party framing of the division of labour: "DRA models and allocates devices; KAI provides AI-focused scheduling policy; Kueue provides quota, admission, fair sharing, and preemption" — [Spheron guide (secondary)](https://www.spheron.network/blog/kubernetes-gpu-orchestration-2026/)

**Karpenter / node provisioning**
- On EKS, Karpenter's automatic node repair uses node conditions such as `AcceleratedHardwareReady`, which the EKS Node Monitoring Agent sets from kernel logs. The self-managed Karpenter path needs node repair, the monitoring agent and the NVIDIA device plugin to be set up separately — [AWS EKS docs (search snippet)](https://docs.aws.amazon.com/eks/latest/userguide/ml-node-pools.html); [AWS blog](https://aws.amazon.com/blogs/containers/how-to-run-ai-model-inference-with-gpus-on-amazon-eks-auto-mode)

### Inferences
- **Which GPU allocation mechanism to choose in Oct 2026:**
  - The **device plugin plus `nvidia.com/gpu`** is still the default mental model and the safest for whole-GPU training pods.
  - **DRA** is the strategic direction. It is required for MNNVL/GB200 ComputeDomains and gives richer selection via CEL, sharing and prioritized alternatives. The 1.37 GA "extended resource" bridge lets tenants keep requesting `nvidia.com/gpu` while a DRA driver serves it underneath.
  - NVIDIA still labels per-GPU DRA allocation as not officially supported, so production DRA today mostly means ComputeDomains, plus whatever the managed providers have productized.
- **Gang scheduling:** for production on K8s ≤1.37, use **Kueue** (admission/quota/TAS) with JobSet, TrainJob, RayJob or LWS, or a batch scheduler (Volcano/KAI). Native WAS is Beta but off by default, and JobSet/Kueue integration only lands from 1.38 onward. Expect migration churn: the v1alpha1, then v1alpha2, then v1beta1 API changes all broke manifests.
- **Reference snippets (background, not re-verified):**
  ```yaml
  # Whole-GPU pod via device plugin
  apiVersion: v1
  kind: Pod
  metadata: {name: cuda-smoke}
  spec:
    restartPolicy: Never
    nodeSelector: {nvidia.com/gpu.product: NVIDIA-H100-80GB-HBM3}   # GFD label
    tolerations: [{key: nvidia.com/gpu, operator: Exists, effect: NoSchedule}]
    containers:
    - name: cuda
      image: nvidia/cuda:12.8.1-base-ubuntu24.04
      command: ["nvidia-smi"]
      resources:
        limits: {nvidia.com/gpu: 1}     # extended resources: no overcommit; requests must equal limits
  ---
  # Device-plugin time-slicing config (referenced from GPU Operator ClusterPolicy devicePlugin.config)
  version: v1
  sharing:
    timeSlicing:
      renameByDefault: false
      failRequestsGreaterThanOne: true
      resources:
      - name: nvidia.com/gpu
        replicas: 4
  ---
  # DRA (resource.k8s.io/v1, GA since 1.34) with NVIDIA DRA driver device class
  apiVersion: resource.k8s.io/v1
  kind: ResourceClaimTemplate
  metadata: {name: single-gpu}
  spec:
    spec:
      devices:
        requests:
        - name: gpu
          exactly: {deviceClassName: gpu.nvidia.com}
  ---
  apiVersion: v1
  kind: Pod
  metadata: {name: dra-gpu}
  spec:
    resourceClaims: [{name: gpu, resourceClaimTemplateName: single-gpu}]
    containers:
    - name: ctr
      image: ubuntu:24.04
      command: ["nvidia-smi","-L"]
      resources: {claims: [{name: gpu}]}
  ```
  ```bash
  # GPU Operator install; set driver.enabled=false where the node image already has drivers (e.g., EKS accelerated AMIs, GKE default)
  helm repo add nvidia https://helm.ngc.nvidia.com/nvidia && helm repo update
  helm install --wait gpu-operator -n gpu-operator --create-namespace nvidia/gpu-operator --version=v26.7.1
  kubectl label node <node> nvidia.com/mig.config=all-1g.10gb --overwrite   # MIG Manager reconfigures the GPU
  ```
  ```yaml
  # Kueue minimal quota (field names per v1beta2; verify against current CRD)
  apiVersion: kueue.x-k8s.io/v1beta2
  kind: ClusterQueue
  metadata: {name: gpu-cq}
  spec:
    namespaceSelector: {}
    resourceGroups:
    - coveredResources: ["cpu","memory","nvidia.com/gpu"]
      flavors:
      - name: h100
        resources:
        - {name: cpu, nominalQuota: 1024}
        - {name: memory, nominalQuota: 8Ti}
        - {name: nvidia.com/gpu, nominalQuota: 64}
  # + ResourceFlavor "h100" (nodeLabels/tolerations), LocalQueue per namespace; jobs carry label kueue.x-k8s.io/queue-name and are created suspended.
  ---
  # Karpenter v1 GPU NodePool (AWS)
  apiVersion: karpenter.sh/v1
  kind: NodePool
  metadata: {name: gpu}
  spec:
    template:
      spec:
        nodeClassRef: {group: karpenter.k8s.aws, kind: EC2NodeClass, name: gpu}
        requirements:
        - {key: karpenter.k8s.aws/instance-family, operator: In, values: ["p5","p5en","g6e"]}
        - {key: karpenter.sh/capacity-type, operator: In, values: ["on-demand","reserved"]}
        taints: [{key: nvidia.com/gpu, effect: NoSchedule}]
    limits: {nvidia.com/gpu: 64}
    disruption: {consolidationPolicy: WhenEmpty, consolidateAfter: 1h}   # avoid consolidating running training pods
  ```
- **Sharing choice:**
  - **MIG** gives hardware isolation for inference and multi-tenant dev on A100/H100/B200-class GPUs.
  - **MPS** gives better throughput for cooperative small inference, but has a shared failure domain.
  - **Time-slicing** is for dev/notebooks only (no isolation).
  - The new per-GPU CUDA memory limits (R615+, toolkit 1.20.1, GPU Operator 26.7.1) look like a step toward soft memory isolation for shared GPUs.
- **Taints/tolerations pattern:** taint GPU node pools `nvidia.com/gpu=present:NoSchedule` (GKE/AKS/EKS each have their own default taint conventions) so CPU-only pods don't land on expensive nodes. Pair this with GFD labels (`nvidia.com/gpu.product`, `nvidia.com/gpu.memory`) for selection.

### Gaps
- Exact list of NVIDIA DRA-driver features at v0.5.x (GPU allocation, MIG via DRA) and when per-GPU DRA allocation becomes "officially supported". The README fetch did not show the version.
- KAI Scheduler's current release number (the README mentions v0.10.0 from Oct 2025, but newer releases likely exist). Volcano's exact latest release.
- Precise Kueue v1beta2 field changes vs v1beta1. Not fetched.
- Karpenter latest version and any GPU-specific features in 2026. Not fetched (search budget exhausted).

---

## 3. Managed Kubernetes for AI: EKS, GKE, AKS

### Takeaway
All three clouds now productize GPU node lifecycle (auto-provisioning, accelerator health detection and auto-repair) and LLM-serving add-ons:
- **EKS:** Auto Mode with accelerator-aware repair, and GPU fees cut in July 2026.
- **GKE:** Autopilot GPUs via ComputeClasses, Inference Gateway (multi-cluster, llm-d-integrated), and managed DRANET.
- **AKS:** KAITO AI toolchain operator add-on.
- **SageMaker HyperPod:** EKS or Slurm with deep health checks.

### Cited Findings
**EKS**
- **EKS Auto Mode GPU fee cut:** from **July 1 2026**, Auto Mode management fees fall 35% for G-series and 60% for P-series and Trainium. Auto Mode includes **accelerator-aware node repair** that detects GPU hardware failures and replaces unhealthy nodes — [AWS What's New (Jul 2026)](https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-eks-auto-mode-gpu-price/)
- **Node Monitoring Agent and Node Auto Repair** detect GPU failures and start recovery **10 minutes after detection**: cordon, then reboot or replace, respecting PDBs. The agent sets the `AcceleratedHardwareReady` node condition — [AWS containers blog](https://aws.amazon.com/blogs/containers/how-to-run-ai-model-inference-with-gpus-on-amazon-eks-auto-mode); [EKS node monitoring/auto-repair announcement (Dec 2024)](https://aws.amazon.com/about-aws/whats-new/2024/12/node-health-monitoring-auto-repair-amazon-eks)
- Auto Mode also bundles the SOCI snapshotter and a GPU-ready default NodeClass. A community sample notes the compute controller also polls EC2 status checks and scheduled maintenance events, independent of the agent (secondary source) — [AWS EKS ML node pools doc (snippet)](https://docs.aws.amazon.com/eks/latest/userguide/ml-node-pools.html); [aws-samples/sample-eks-gpu-node-auto-repair](https://github.com/aws-samples/sample-eks-gpu-node-auto-repair)

**SageMaker HyperPod (on EKS)**
- The HyperPod CLI (`hyp`) manages EKS-orchestrated HyperPod clusters, training jobs and inference endpoints:
  - PyTorchJobs require the HyperPod Training Operator.
  - Optional **deep health check**: pods schedule only on nodes that passed it.
  - `--max-retry`, and `hyp update cluster` with node-recovery `Automatic`.
  - **Task governance** with queue names and priorities, plus a Kueue scheduler type.
  - Inference endpoints from JumpStart or custom models (S3, FSx, HF), with autoscaling, intelligent routing and KV caching.
  - Source: [aws/sagemaker-hyperpod-cli README](https://github.com/aws/sagemaker-hyperpod-cli)
  ```bash
  hyp list-cluster
  hyp create hyp-pytorch-job --version 1.0 --job-name test-pytorch-job --image pytorch/pytorch:latest ...
  hyp list hyp-pytorch-job
  ```
  (verbatim, truncated in source) — [sagemaker-hyperpod-cli](https://github.com/aws/sagemaker-hyperpod-cli)

**GKE**
- **Autopilot GPUs:** request them via **ComputeClasses** or node selectors in the pod spec, and GKE places pods on matching GPU nodes. Docs list **B200, H200, H100, A100** among the supported GPUs. From **Oct 1 2026**, RTX PRO 6000 (G4) on Autopilot is billed the Autopilot node-management premium on top of hardware — [GKE docs: Autopilot GPUs (snippet)](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/autopilot-gpus)
- Autopilot GPU pods are billed **per node plus a premium**, not per pod — [third-party comparison](https://www.alekseialeinikov.com/en/blog/topics/cloud/gke-autopilot-vs-standard-2026)
- **GKE Inference Gateway:**
  - **Multi-cluster** version for global/multi-region routing (<1% overhead in Google's tests).
  - March 2026 release note: it integrates **llm-d inference scheduling**, and **GKE Inference Quickstart (GIQ)** recommends distributed-inference configurations (Qwen, gpt-oss) on GPUs and TPUs.
  - A June 2026 benchmark cited by Google claims 15.7% higher throughput and 62.6% lower ITL than "the next leading managed Kubernetes service". This is vendor-reported.
  - Source: [Google Cloud blog: what's new in AI infrastructure](https://cloud.google.com/blog/topics/ai-infrastructure/whats-new-in-ai-infrastructure-this-month)
- The upstream **Gateway API Inference Extension** (which GKE Inference Gateway implements) declares itself **GA**. `InferencePool` stays in that repo. The Endpoint Picker (EPP), `InferenceObjective` (formerly InferenceModel), `InferenceModelRewrite` and Body-Based Router have **moved to llm-d repos**, and the old packages will be archived. Ext-proc-capable gateways named: Envoy Gateway, kgateway, GKE Gateway — [gateway-api-inference-extension README](https://github.com/kubernetes-sigs/gateway-api-inference-extension)
- **Managed DRANET** (DRA-based networking for GPU/TPU NICs) is reportedly GA for Autopilot and Standard (Jul 2026, secondary source) — [Medium / Google Cloud community](https://medium.com/google-cloud/part-1-use-gke-managed-dranet-with-gpus-and-autopilot-cluster-c7ea13be10f8)

**AKS**
- The **AI toolchain operator (KAITO)** managed add-on is built on the CNCF-sandbox KAITO project:
  - A workspace controller triggers GPU node auto-provisioning and uses model presets.
  - Exposes OpenAI-compatible APIs with streaming.
  - **Requires Ampere or newer (CUDA compute capability ≥8.0)**: T4, V100, M60 and K80 are unsupported, as are AMD GPU VM sizes.
  - Sources: [Microsoft Learn: AI toolchain operator](https://learn.microsoft.com/en-us/azure/aks/ai-toolchain-operator); [CNCF sandbox issue](https://github.com/cncf/sandbox/issues/106)
- A third-party blog claims KAITO now sits under "AI Runway" (introduced at KubeCon EU 2026), provisions via Karpenter and launches vLLM. Unverified against Microsoft primary sources — [wenfeng.my](https://wenfeng.my/aks-2026-build-announcements-production-workloads/)

### Inferences
- **Notable features by provider:**
  - **EKS:** Auto Mode (Karpenter-based) with GPU health-repair and big GPU fee cuts, plus HyperPod for resilient training.
  - **GKE:** the most mature inference-routing stack (Inference Gateway, llm-d, GIQ), Autopilot GPUs/TPUs via ComputeClasses, and DRA-networking.
  - **AKS:** KAITO-based "model-as-a-workspace" serving.
  - The GKE benchmark claims are vendor-sourced; treat them as marketing until reproduced.
- **(Background, not re-verified):**
  - EKS announced support for very large ("ultra scale", up to 100k-node) clusters in 2025, and GKE has supported 65k-node clusters.
  - GKE's Dynamic Workload Scheduler (flex-start, calendar mode) and EC2 Capacity Blocks for ML are the typical ways to obtain scarce H100/B200 capacity for batch jobs.
  - Azure offers ND-series GPU VMs with InfiniBand for AKS node pools.
  - Verify all of these before citing.

### Gaps
- Official GA date of GKE Inference Gateway (docs unreachable; search found no explicit GA announcement).
- EKS "ultra scale" 100k-node support, and EKS DRA support status. Search didn't cover them and docs were unreachable.
- Current AKS GPU features beyond KAITO (managed GPU driver installation, AKS Automatic GPU support, DRA on AKS). Not found.
- SageMaker HyperPod 2026 features (checkpointless training, Slurm-orchestrated HyperPod changes). AWS docs were unreachable.

---

## 4. Ray: core concepts, Ray Train/Serve/Data, KubeRay, Anyscale; when to use Ray

### Takeaway
Ray is now a **PyTorch Foundation project** (Oct 2025) and releases frequently: **Ray 2.59.0 (2 Oct 2026)** made **Ray Data LLM and Ray Serve LLM GA**. **KubeRay v1.7.x** (Aug–Sep 2026) is the standard way to run it on Kubernetes. Use Ray when you need Python-native heterogeneous pipelines (data processing, training, RL/rollouts, serving) on one cluster. If you only need fixed-shape SPMD training, plain torchrun with JobSet/TrainJob or Slurm is simpler.

### Cited Findings
- **The PyTorch Foundation adopted Ray as a hosted project** (announced 22 Oct 2025 at PyTorch Conference), describing it as a distributed compute framework for data processing, training and inference. Stats at the time: 39k+ GitHub stars and 237M+ downloads — [PyTorch Foundation blog](https://pytorch.org/blog/pytorch-foundation-welcomes-ray-to-deliver-a-unified-open-source-ai-compute-stack/); [InfoQ](https://infoq.com/news/2025/10/pytorch-conf-ray-monarch)
- **Ray 2.59.0 (2 Oct 2026):**
  - **Ray Data LLM GA**; disk-backed shuffle_v2 gains Join/Aggregation.
  - **Ray Serve LLM GA** with vLLM 0.27.0 and a KV-aware routing guide.
  - Serve per-deployment backpressure can return 429 with `Retry-After`, and **gang-scheduled deployments can scale to zero**.
  - **Token authentication on by default for local clusters** (`RAY_AUTH_MODE=disabled` to opt out); the dashboard redacts `runtime_env`.
  - Core fix for placement-group retry storms on large clusters.
  - Deprecated: `ray_remote_args` on read APIs.
  - Source: [ray releases](https://github.com/ray-project/ray/releases)
- **Ray 2.58.0 (23 Aug 2026):**
  - Train: **TorchTPU backend**, a public preemption API, data-ingest metrics.
  - Core: experimental **Ray Sandbox (gVisor)**, `SubslicePlacementGroup` for TPU subslices, active-passive GCS leader election.
  - Serve LLM: KV-cache and token-aware routing, vLLM 0.26.0.
  - Source: [ray releases](https://github.com/ray-project/ray/releases)
- **Ray 2.57.0 (11 Aug 2026):**
  - **Embedded RocksDB for GCS fault tolerance** (no external Redis needed) and a **public topology-aware scheduling API**.
  - Ray Data `DataSourceV2` on by default, plus Unity Catalog, `read_zarr` and `read_lerobot`.
  - Serve's default proxy binary is HAProxy (`ray-haproxy`).
  - **Cluster autoscaler v1 removed.** Low-level scheduling APIs (`DataContext.scheduling_strategy`, `actor_locality_enabled`, etc.) deprecated.
  - Source: [ray releases](https://github.com/ray-project/ray/releases)
- **KubeRay v1.7.1 (21 Sep 2026)** is latest; it is a bug fix release, and History Server live-cluster support is now off by default.
  - **v1.7.0 (20 Aug 2026):** History Server beta; **RayService incremental upgrades beta and on by default** (Gateway-API based, with mid-upgrade rollback); alpha mTLS between pods via cert-manager, NetworkPolicy and RocksDB GCS FT; `priority` on worker groups. **`ray.io/v1alpha1` deprecated in favour of `ray.io/v1`.**
  - **v1.6.0 (19 Mar 2026):** History Server alpha; Ray token auth via K8s RBAC; **RayCronJob** alpha; RayJob deletion policy beta; `managedBy` on RayService for MultiKueue.
  - Source: [kuberay releases](https://github.com/ray-project/kuberay/releases)
- Historical context: Ray 2.7 (Sep 2023) made Ray Train and Ray Serve GA alongside KubeRay GA. KubeRay replaced the legacy Python-based Ray operator — [Anyscale blog](https://anyscale.com/blog/ray-2-7-features-major-stability-improvements-to-ray-ai-libraries-and-kuberay-introduces-rayllm); [Ray 2.0 discussion](https://discuss.ray.io/t/ray-version-2-0-is-here/7398)
- Kueue integrates RayJob and RayCluster, and MultiKueue supports Ray (KubeRay `managedBy`) — [kueue README](https://github.com/kubernetes-sigs/kueue); [kuberay releases](https://github.com/ray-project/kuberay/releases)

### Inferences
- **Core concepts (background, not re-verified):**
  - **Tasks:** stateless `@ray.remote` functions.
  - **Actors:** stateful `@ray.remote` classes pinned to a worker process.
  - **Object store:** per-node shared memory (Plasma) addressed by `ObjectRef`s, with zero-copy reads and spilling to disk.
  - **GCS:** the head-node control plane. Its fault tolerance no longer needs Redis as of 2.57, per the citation above.
  - **Placement groups:** gang reservation of resource bundles (`PACK`/`SPREAD`/`STRICT_PACK`).
  - Resources are logical (`num_gpus=1` is a scheduling claim, not isolation).
  ```python
  import ray
  ray.init()                                     # or ray.init("ray://head:10001") / RAY_ADDRESS
  @ray.remote(num_gpus=1)
  def embed(batch): ...
  @ray.remote
  class KVStore:
      def __init__(self): self.d = {}
      def put(self, k, v): self.d[k] = v
  refs = [embed.remote(b) for b in batches]; out = ray.get(refs)
  # Ray Train (V2 API)
  from ray.train import ScalingConfig
  from ray.train.torch import TorchTrainer
  TorchTrainer(train_loop_per_worker, scaling_config=ScalingConfig(num_workers=16, use_gpu=True)).fit()
  # Ray Serve
  from ray import serve
  @serve.deployment(num_replicas="auto", ray_actor_options={"num_gpus": 1})
  class Model:
      async def __call__(self, req): ...
  serve.run(Model.bind())
  ```
  ```yaml
  # KubeRay RayJob skeleton (ray.io/v1; v1alpha1 is deprecated)
  apiVersion: ray.io/v1
  kind: RayJob
  metadata: {name: finetune}
  spec:
    entrypoint: python train.py
    shutdownAfterJobFinishes: true
    rayClusterSpec:
      headGroupSpec:
        rayStartParams: {}
        template: {spec: {containers: [{name: ray-head, image: rayproject/ray:2.59.0-gpu}]}}
      workerGroupSpecs:
      - groupName: gpu
        replicas: 4
        rayStartParams: {}
        template:
          spec:
            containers:
            - name: ray-worker
              image: rayproject/ray:2.59.0-gpu
              resources: {limits: {nvidia.com/gpu: 8}}
  ```
- **Which KubeRay CRD to use (background):** RayCluster for long-lived interactive clusters, RayJob for an ephemeral cluster per job (pairs with Kueue), RayService for Serve with zero-downtime upgrades (now incremental, via Gateway API).
- **When to use Ray:**
  - Heterogeneous CPU+GPU pipelines, e.g. batch inference or embedding over large datasets with Ray Data streaming.
  - RL and post-training loops with many actors (rollout workers plus learners; common in LLM RLHF frameworks).
  - Hyperparameter sweeps (Ray Tune).
  - Python-first multi-model serving and composition (Ray Serve).
- **When to avoid Ray:** single fixed-shape SPMD pretraining, where torchrun/Slurm/JobSet are simpler. It also adds an extra control plane (GCS/head) to operate and secure. The token-auth default arriving only in 2.59 for local clusters hints at the historical security posture; Ray dashboards and job APIs must never be internet-exposed.
- **Anyscale (background, not re-verified):** the company founded by Ray's creators. It sells a managed Ray platform with a proprietary optimized runtime and runs on customer cloud accounts or Kubernetes.

### Gaps
- Anyscale's 2026 product state (platform features, BYOC/K8s operator, pricing). Not researched this session (search budget exhausted).
- Whether Ray Train V1 APIs are formally removed or still only deprecated as of 2.59. Not stated in the release notes fetched.
- Ray Compiled Graphs / RDT (Ray Direct Transport) status. Only an RDT NIXL mention in 2.58.

---

## 5. Kubeflow: Pipelines, Trainer/Training Operator, Katib, KServe — current status

### Takeaway
Kubeflow is very much alive but has reorganized:
- **Kubeflow Trainer v2** (`TrainJob` plus `ClusterTrainingRuntime`, built on **JobSet**; latest **v2.3.0, Aug 2026**) supersedes Training Operator v1 (PyTorchJob/MPIJob etc.), which now gets only patch releases.
- **KFP 2.17.x** is current.
- **KServe v0.21** has pivoted heavily toward LLM serving (`LLMInferenceService`, llm-d, Gateway API Inference Extension).
- The platform bundle uses calendar versioning (**Kubeflow 26.03**).

### Cited Findings
- **Kubeflow Trainer v2.3.0 (7 Aug 2026)** is latest:
  - Breaking: runtime finalizers removed, and the CRD moved into the Helm chart; you must upgrade from v2.0/2.1/2.2 to v2.3 first.
  - New **OptimizationJob CRD** (KEP-3562), runtime snapshots (KEP-2599), MPI launcher waits for worker readiness, Flux integration.
  - JobSet and LWS images are pinned to released versions.
  - Source: [kubeflow/trainer releases](https://github.com/kubeflow/trainer/releases)
- **Trainer v2.2.0 (20 Mar 2026):**
  - One-command Helm install of control plane and runtimes; SDK via **`pip install kubeflow`**.
  - **JAX and XGBoost runtimes**, a Flux runtime for MPI/HPC, TrainJob progress/metrics propagation, `activeDeadlineSeconds`.
  - Breaking: **RuntimePatches replaced PodTemplateOverrides**, and **ElasticPolicy and `numProcPerNode` were removed from the Torch API**.
  - Sources: [trainer releases](https://github.com/kubeflow/trainer/releases); [Kubeflow blog v2.2](https://blog.kubeflow.org/kubeflow-trainer-v2.2-release/)
- **Training Operator v1** (legacy PyTorchJob/MPIJob/etc.) still received **v1.9.4 (18 Aug 2026)**, a bug-fix and dependency-bump release only. A migration guide to Trainer v2 exists — [trainer releases](https://github.com/kubeflow/trainer/releases); [Migrating to Kubeflow Trainer v2](https://trainer.kubeflow.org/en/latest/operator-guides/migration.html)
- Search-snippet claim (secondary) of "full compatibility with Training Operator v1 CRDs (PyTorchJob, MPIJob, JAXJob, XGBoostJob) handled through the single TrainJob abstraction". Not confirmed in the primary release notes — [byteiota](https://byteiota.com/?p=22655)
- CNCF (Jul 2026): work is underway to support **RL workloads for LLM post-training** in Kubeflow Trainer — [CNCF blog](https://www.cncf.io/blog/2026/07/28/kubeflow-unveils-new-cloud-native-innovations-to-supercharge-ai/)
- Red Hat OpenShift AI 3.4 uses Kubeflow Trainer v2 for distributed training (29 Sep 2026 article) — [Red Hat Developer](https://developers.redhat.com/index%2ephp/articles/2026/09/29/distributed-training-openshift-ai-34-kubeflow-trainer-v2)
- A **Kubeflow AI reference platform 26.03** release exists, i.e. calendar versioning for the platform bundle. Component versions not retrieved — [Kubeflow docs](https://www.kubeflow.org/docs/kubeflow-platform/releases/kubeflow-26.03)
- **Kubeflow Pipelines:**
  - Latest **2.17.2 (4 Sep 2026)**. 2.17.0 (Jul 2026) brought multi-arch images and a frontend rewrite.
  - 2.16.x (2026) enforces pipeline authorization, adds OIDC, and lets admins **block v1 pipeline runs by namespace**.
  - **2.15.0 (Nov 2025) replaced MinIO with SeaweedFS** as the default object store, included a non-reversible DB index migration, added K8s-native API filtering, and **removed MLMD** via a proposal.
  - Source: [kubeflow/pipelines releases](https://github.com/kubeflow/pipelines/releases)
- **KServe:**
  - **v0.21.0 (25 Sep 2026)**: `LLMInferenceService` gains direct KEDA scaling and a `rolloutStrategy`; canary splitting for RawDeployment HTTPRoutes; CRDs split into separate Helm charts; **DRA `resourceClaims` for ServingRuntimes**.
  - **v0.20.0 (6 Aug 2026)**: routing moved to llm-d.ai CRDs, llm-d components at v0.8.0, **Gateway API Inference Extension v1.5.0**, managed DRA, KV-cache offloading, vLLM as a supported runtime.
  - Source: [kserve releases](https://github.com/kserve/kserve/releases)
- **llm-d** (vLLM-based distributed inference stack):
  - **CNCF Sandbox since March 2026**; founders Red Hat, Google Cloud, IBM Research, CoreWeave, NVIDIA.
  - Features: prefix-cache/load-aware routing, P/D disaggregation, wide expert parallelism, tiered KV offload, SLO-aware autoscaling.
  - README lists v0.7 (May 2026) as latest, which conflicts with KServe v0.20 citing "llm-d components v0.8.0". The README may be stale, or component versions may differ.
  - Sources: [llm-d README](https://github.com/llm-d/llm-d); [kserve releases](https://github.com/kserve/kserve/releases)

### Inferences
- **Status summary (Oct 2026):**
  - **Trainer v2 / TrainJob** is the current API. **Training Operator v1 (PyTorchJob etc.) is legacy/maintenance**: still common in existing clusters and in SageMaker HyperPod's own operator, but new work should target TrainJob.
  - **KFP v2** is current; KFP v1-style runs are being fenced off.
  - **KServe** is the main Kubeflow-family serving project, now LLM-centric and converging with llm-d/GIE.
  - **Katib's** future is unclear; Trainer's new OptimizationJob CRD may absorb HPO, but that is unconfirmed.
- **Reference YAML (background, not re-verified; check field names against current CRDs):**
  ```yaml
  # Kubeflow Trainer v2
  apiVersion: trainer.kubeflow.org/v1alpha1
  kind: TrainJob
  metadata: {name: llm-sft}
  spec:
    runtimeRef: {name: torch-distributed}     # ClusterTrainingRuntime (JobSet template under the hood)
    trainer:
      image: ghcr.io/acme/train:2026.10
      command: ["torchrun","train.py"]
      numNodes: 4
      resourcesPerNode: {limits: {nvidia.com/gpu: 8}}
  ---
  # LEGACY (Training Operator v1) — still seen widely
  apiVersion: kubeflow.org/v1
  kind: PyTorchJob
  metadata: {name: ddp}
  spec:
    pytorchReplicaSpecs:
      Master: {replicas: 1, restartPolicy: OnFailure, template: {spec: {containers: [{name: pytorch, image: ..., resources: {limits: {nvidia.com/gpu: 8}}}]}}}
      Worker: {replicas: 3, restartPolicy: OnFailure, template: {spec: {containers: [{name: pytorch, image: ..., resources: {limits: {nvidia.com/gpu: 8}}}]}}}
  ```
- Design rationale: TrainJob separates the **platform-owned runtime** (ClusterTrainingRuntime: images, launcher, networking, JobSet policies) from the **data scientist's job** (image, command, nodes). This makes it a natural fit for Kueue admission and the upcoming native WAS JobSet integration.

### Gaps
- **Katib** 2026 release/status. Not fetched; unknown whether it's being folded into Trainer's OptimizationJob.
- Kubeflow 26.03 component version matrix (page unreachable).
- KServe's CNCF status (it was accepted as CNCF incubating in 2025 per background knowledge, but not verified this session). ModelMesh status unknown.

---

## 6. Slurm for AI clusters: why labs use it, Slinky / Slurm-on-K8s, SageMaker HyperPod, Slurm vs Kubernetes

### Takeaway
Slurm remains the dominant batch scheduler for large training clusters: gang/whole-node allocation, topology-aware placement, fair-share accounting and a familiar `sbatch`/`srun` UX. **NVIDIA acquired SchedMD in Dec 2025** and pledged to keep Slurm open source and vendor-neutral. The industry is converging on **Slurm-on-Kubernetes hybrids**: SchedMD/NVIDIA's **Slinky slurm-operator**, CoreWeave SUNK and HyperPod Slurm. These keep Slurm's scheduler while using Kubernetes for node lifecycle, images and services.

### Cited Findings
- **NVIDIA acquired SchedMD** (announced ~15 Dec 2025; terms undisclosed) and said it will keep developing and distributing Slurm as **open-source, vendor-neutral** software. Some HPC users voiced concern ("fingers hovering over the fork button") — [The Stack](https://www.thestack.technology/nvidia-schlurps-slurm-snaffles-schedmd/); [Network World](https://www.networkworld.com/article/4106930/nvidia-moves-deeper-into-ai-infrastruct-with-schedmd-acquisition.html)
- Slurm's reach: NVIDIA says it is used in more than half of the TOP500 top-10 and top-100 systems; Gigazine reports >65% of TOP500 systems. The figures differ by source — [Network World](https://www.networkworld.com/article/4106930/nvidia-moves-deeper-into-ai-infrastruct-with-schedmd-acquisition.html); [Gigazine](https://gigazine.net/gsc_news/en/20251216-nvidia-acquire-schedmd-slurm)
- Current Slurm stable branches are **26.05.x and 25.11.x** — [Wikipedia (secondary)](https://en.wikipedia.org/wiki/Slurm_Workload_Manager)
- **Slinky slurm-operator:**
  - SchedMD's operator manages the Slurm cluster lifecycle (create, upgrade, graceful shutdown) on Kubernetes.
  - **CRDs:** `Controller` (slurmctld; HA with an RWX PVC; config changes without control-plane downtime), `NodeSet` (homogeneous slurmd workers; StatefulSet-style or **DaemonSet-style one-pod-per-node** scaling), `LoginSet` (login nodes with SSSD), `Accounting`, `RestApi`, `Token`. The `Cluster` CRD is defunct.
  - Worker pods are **drained in Slurm before termination**, and NodeSet pods report Slurm node state in pod conditions.
  - NodeSets/LoginSets support **scale-to-zero** with HPA.
  - Releases 1.0.x–1.3.x require **Slurm ≥25.11**; 1.2/1.3 support K8s 1.35–1.37.
  - Source: [SlinkyProject/slurm-operator README](https://github.com/SlinkyProject/slurm-operator)
  ```bash
  helm install slurm-operator-crds oci://ghcr.io/slinkyproject/charts/slurm-operator-crds
  helm install slurm-operator oci://ghcr.io/slinkyproject/charts/slurm-operator \
    --namespace=slinky --create-namespace
  helm install slurm oci://ghcr.io/slinkyproject/charts/slurm \
    --set-json 'nodesets={"slinky":{}}' \
    --set "partitions.all.enabled=true" \
    --namespace=slurm --create-namespace
  ```
  (verbatim; requires cert-manager first) — [slurm-operator README](https://github.com/SlinkyProject/slurm-operator)
- **Slinky release timeline:**
  - v1.0.0 reportedly released **20 Nov 2025** (supporting Slurm 25.11) — [Medium (secondary)](https://medium.com/@TASDesignGroupInc/implementing-slurm-on-kubernetes-with-slinky-v1-0-0-bb553ed7a165)
  - v1.1.0 added topology handling for dynamic nodes (registering by the underlying K8s node) and DaemonSet-style worker scaling — [NVIDIA developer blog](https://developer.nvidia.com/blog/running-large-scale-gpu-workloads-on-kubernetes-with-slurm/)
  - A community repo pinned v1.2.0 (Slurm 26.05) in Sep 2026, while the operator README compatibility matrix already lists 1.3.x — [slinky-gitops](https://github.com/Zhanyl-tech/slinky-gitops); [slurm-operator README](https://github.com/SlinkyProject/slurm-operator)
- GPU Operator 25.10.1 added "HPC job mapping" for DCGM Exporter, i.e. attributing GPU metrics to Slurm/HPC jobs — [GPU Operator release notes](https://github.com/NVIDIA/cloud-native-docs/blob/main/gpu-operator/release-notes.rst)
- Kubeflow Trainer v2.2/2.3 added a **Flux** runtime (Flux Framework is an HPC resource manager) for MPI/HPC-style jobs on Kubernetes, another HPC/K8s convergence point — [trainer releases](https://github.com/kubeflow/trainer/releases)

### Inferences
- **Why AI labs use Slurm (background, not re-verified):**
  - Native **gang allocation** of whole nodes (`--nodes=N --exclusive`).
  - **Topology-aware placement** (topology/tree and the newer block plugin for NVL72-style domains).
  - Mature **fair-share/QOS/accounting** (slurmdbd).
  - **Low scheduling latency** at thousands of nodes.
  - Researcher-friendly interactive allocation (`salloc`, `srun --pty`).
  - Containers via **Pyxis/Enroot** or Apptainer without a daemon.
  - Bare-metal-like access to InfiniBand/RDMA.
- **Kubernetes strengths:** declarative services and inference, autoscaling, a rich operator ecosystem (KServe, Ray, Kueue), multi-tenancy and RBAC, and cloud-managed control planes.
- **Kubernetes weaknesses for training:** gang scheduling is historically bolted on (Kueue/Volcano; native only Beta-off-by-default in 1.37), API-server/etcd scale limits, and per-pod scheduling overhead.
- **Practical pattern:** Slurm for large pretraining and researcher batch; Kubernetes for inference, data pipelines and platform services; hybrids (Slinky, SUNK, HyperPod) to share one GPU pool.
- **Example batch script (background, not re-verified):**
  ```bash
  #!/bin/bash
  #SBATCH --job-name=pretrain
  #SBATCH --nodes=16
  #SBATCH --ntasks-per-node=1
  #SBATCH --gpus-per-node=8
  #SBATCH --cpus-per-task=96
  #SBATCH --exclusive
  #SBATCH --time=48:00:00
  head=$(scontrol show hostnames "$SLURM_JOB_NODELIST" | head -n1)
  srun --container-image=nvcr.io#nvidia/pytorch:<yy.mm>-py3 --container-mounts=/fsx:/fsx \
    torchrun --nnodes=$SLURM_NNODES --nproc-per-node=8 \
      --rdzv-backend=c10d --rdzv-endpoint=$head:29500 --rdzv-id=$SLURM_JOB_ID train.py
  ```
- The NVIDIA acquisition plus NVIDIA's ownership of KAI, the DRA driver (now donated) and Slinky means NVIDIA now influences both the HPC and the K8s scheduling stacks for GPU clusters. This is an inference worth flagging for vendor-neutrality discussions.

### Gaps
- **CoreWeave SUNK** details and **SageMaker HyperPod Slurm** 2026 features. Not fetched (search budget exhausted, AWS docs unreachable).
- `slurm-bridge` (Slinky's K8s-scheduler-plugin bridge) current status. Not on the README fetched.
- Slurm 26.05 AI-specific features (e.g. block topology improvements, GPU-related changes). Not researched.
- Any post-acquisition fork of Slurm. None found in sources.

---

## 7. Patterns: distributed training jobs (torchrun/PyTorchJob/TrainJob), inference deployments, GPU health checks, node-failure handling

### Takeaway
The 2026 reference patterns are:
- **Training:** a gang-admitted multi-node job (Kueue plus JobSet/TrainJob, or Slurm `sbatch`) running torchrun with c10d rendezvous, on topology-constrained nodes, with frequent checkpoints.
- **Inference:** vLLM/SGLang behind an inference-aware gateway (Gateway API Inference Extension / llm-d / KServe LLMInferenceService), with LWS for multi-host models.
- **Health:** layered GPU health detection (DCGM, XID/kernel-log node conditions, device-health status in pod status) feeding automated cordon/repair (EKS/HyperPod/GKE auto-repair, device taints via DRA `DeviceTaintRule`).

### Cited Findings
- **Device health in Pod status:** K8s 1.36 promoted **Resource health status (KEP-4680)** to beta. `allocatedResourcesStatus` shows whether an allocated device is Unhealthy or Unknown, for both device plugins and DRA — [v1.36 release blog source](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-36-release/index.md)
- **DRA device taints (stable in 1.37):** drivers can taint faulty devices so new pods avoid them and existing users are evicted unless they tolerate the taint. Admins can taint cluster-wide via `DeviceTaintRule` without touching drivers. This is a native mechanism for "this GPU is bad" — [v1.37 DRA blog source](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-dra-updates.md)
- **Node lifecycle conditions (alpha, 1.37, gate `NodeLifecycleConditions`):**
  - Well-known conditions `DrainInProgress`, `Drained`, `MaintenancePlanned`, `MaintenanceInProgress`, `GracefulNodeShutdownInProgress`.
  - Informational only in 1.37: no core controller acts on them yet.
  - Authored by NVIDIA (Ryan Hallisey), 9 Sep 2026.
  - Source: [K8s blog source: node lifecycle conditions](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-node-lifecycle-conditions.md)
- **EKS repair flow:** the Node Monitoring Agent parses kernel logs and sets `AcceleratedHardwareReady`; auto-repair cordons, then reboots or replaces, 10 min after detection, respecting PDBs — [AWS blog](https://aws.amazon.com/blogs/containers/how-to-run-ai-model-inference-with-gpus-on-amazon-eks-auto-mode)
- **HyperPod:** the deep-health-check flag schedules jobs only onto nodes that passed; automatic node recovery and job `--max-retry` are also available — [sagemaker-hyperpod-cli](https://github.com/aws/sagemaker-hyperpod-cli)
- **GPU Operator ops details:**
  - Driver Manager retries cordon/uncordon with backoff (26.7.1).
  - The `nvidia.com/gpu.deploy.client` label lets the operator restart third-party GPU client pods during driver upgrades and MIG changes (26.7.0).
  - In-place driver pod restarts on patch upgrades (26.7.0).
  - DCGM Exporter can attach pod labels and UID to metrics (26.3.2).
  - Source: [GPU Operator release notes](https://github.com/NVIDIA/cloud-native-docs/blob/main/gpu-operator/release-notes.rst)
- **JobSet failure handling:** `failurePolicy` sets max restarts, and the extended API (v0.6+) can apply different actions per error type. `successPolicy` lets a job succeed when, e.g., the leader/driver group completes — [jobset README](https://github.com/kubernetes-sigs/jobset)
- **LWS failure handling:** opt-in all-or-nothing restart of a whole group when one pod or container fails, which matters for tensor-parallel multi-host inference where one dead shard breaks the replica — [lws README](https://github.com/kubernetes-sigs/lws)
- **Kueue v0.20.1** fixed TAS failed-node replacement and delayed topology assignment, i.e. topology-aware recovery when a node in a gang dies — [kueue releases](https://github.com/kubernetes-sigs/kueue/releases)
- **Gang preemption semantics:** 1.37 `disruptionMode: all` evicts the whole group together, and default single-pod preemption now respects the PodGroup's disruptionMode — [K8s v1.37 WAS blog source](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-advancing-workload-aware-scheduling.md)
- **Ray resilience:**
  - Ray Train 2.58 public preemption API.
  - GCS fault tolerance via embedded RocksDB (Ray 2.57; KubeRay 1.7 alpha).
  - RayService incremental upgrades with rollback (KubeRay 1.7).
  - Sources: [ray releases](https://github.com/ray-project/ray/releases); [kuberay releases](https://github.com/ray-project/kuberay/releases)
- **Inference routing:**
  - Gateway API Inference Extension (GA) routes via an Endpoint Picker over Envoy ext-proc.
  - llm-d adds prefix-cache-aware and predicted-latency scheduling, P/D disaggregation and SLO-aware autoscaling (scale-to-zero since v0.5).
  - HPA scale-to-zero on external/object metrics is Beta and on by default in K8s 1.37.
  - Sources: [GIE README](https://github.com/kubernetes-sigs/gateway-api-inference-extension); [llm-d README](https://github.com/llm-d/llm-d); [v1.37 release blog source](https://github.com/kubernetes/website/blob/main/content/en/blog/_posts/2026/kubernetes-v1-37-release/index.md)

### Inferences
- **torchrun essentials (background, not re-verified):**
  ```bash
  torchrun --nnodes=$NNODES --nproc-per-node=8 \
    --rdzv-backend=c10d --rdzv-endpoint=$MASTER_ADDR:29500 --rdzv-id=$JOB_ID \
    --max-restarts=3 train.py          # elastic restarts; requires resumable checkpoints
  # env torchrun sets per process: RANK, LOCAL_RANK, WORLD_SIZE, MASTER_ADDR, MASTER_PORT
  ```
  - On K8s, the stable DNS names from JobSet/Indexed Jobs (`<jobset>-<rjob>-0-0.<subdomain>`) give a fixed rendezvous endpoint.
  - Set `NCCL_DEBUG=INFO` while bringing up a cluster.
  - Use hostNetwork or SR-IOV/RDMA (DRANET-style) NICs for multi-node bandwidth.
  - Mount `/dev/shm` as a memory-backed emptyDir.
- **Inference Deployment basics (background):**
  - **Readiness probe** on the model server's `/health` endpoint, gated on model load.
  - A generous **startupProbe** (weight loading can take minutes).
  - `terminationGracePeriodSeconds` long enough to drain in-flight streams.
  - PDBs so autoscalers/repair don't take all replicas at once.
  - Scale on queue depth or KV-cache utilization, not CPU.
- **GPU health checks (background, not re-verified):**
  - **Passive:** DCGM Exporter metrics (`DCGM_FI_DEV_XID_ERRORS`, ECC/row-remap, thermal), kernel XID messages, NVLink/IB counters.
  - **Active:** `dcgmi diag -r 2|3` (pre-job or periodic), NCCL `all_reduce_perf` burn-in across nodes, `nvidia-smi -q` checks.
  - Push results as node conditions or taints (Node Problem Detector custom plugins or vendor agents), then use Kueue/Slurm to exclude bad nodes.
  - Slurm equivalents: `HealthCheckProgram` plus drain states, and prolog/epilog GPU checks.
- **Node-failure handling for large training:**
  - Assume failures at scale.
  - Checkpoint frequently to parallel FS/object storage (async/sharded checkpoints).
  - Use gang restart semantics (JobSet failurePolicy, TrainJob, Kueue requeue, LWS group restart, Slurm `--requeue`).
  - Keep hot spares or over-provision a node pool so replacement doesn't wait on capacity.
  - Native K8s now has the pieces (device taints GA, resource health status beta, node lifecycle conditions alpha), but the automation glue is still vendor- or managed-service-provided.

### Gaps
- OpenAI's "Scaling Kubernetes to 7,500 nodes" lessons (2021). openai.com was unreachable, so not re-verified. It is dated anyway: it covers 2021-era GPU health checks and coscheduling plugins.
- CoreWeave, Anthropic, Meta or other 2026 engineering-blog posts on GPU fleet health. Not researched (search budget exhausted).
- NVIDIA's own fleet-health tooling for K8s (any 2026 open-source GPU health/remediation project). Not found in sources fetched.
- Quantitative failure-rate data for large GPU clusters. Not gathered this session.
