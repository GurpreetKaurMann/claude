# MLOps and LLMOps Practices and Tooling in the Cloud (state as of October 2026)

> Research conditions (read this first): Notes compiled 2026-10-14. The shared WebSearch budget ran out partway through, and the egress proxy blocked most documentation hosts (mlflow.org, opentelemetry.io, docs.aws.amazon.com, docs.cloud.google.com, learn.microsoft.com, langfuse.com, docs.ragas.io and others). Primary facts were therefore taken mostly from **GitHub repos, release pages and raw docs** (which were reachable), **anthropic.com**, and search-result summaries. Anything that comes from prior knowledge and could not be re-checked this session is labeled **[UNVERIFIED-BACKGROUND]** and kept in the Gaps sections. "(older)" marks items from before 2025 that are still in use but may be dated.

---

## 1. MLOps maturity levels, ML lifecycle stages, and how LLMOps differs from classic MLOps

### Takeaway
Google's three-level model (Level 0 manual, Level 1 automated continuous-training pipeline, Level 2 automated CI/CD of the pipeline itself) is still the standard reference. By 2026, though, the tooling center of gravity has moved to GenAI/agents. MLflow 3 rebuilt itself around tracing, judges and prompts. Google folded Vertex AI into an agent-first "Gemini Enterprise Agent Platform". Eval guidance treats the agent harness plus the model as the unit under test, with non-deterministic multi-trial metrics (pass@k / pass^k), not single accuracy numbers.

### Cited Findings
**Google MLOps levels** (the doc is from 2020 and still the canonical reference; the URL now redirects to docs.cloud.google.com. The page could not be fetched this session, so the summary below is from prior knowledge of the doc and should be verified against the source) — [Google Cloud: MLOps: Continuous delivery and automation pipelines in ML](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
- **Level 0, manual process:** notebook-driven and script-driven work. Data science and ops are disconnected. Releases are rare, there is no CI/CD, deployment means handing over a model artifact rather than a pipeline, and there is no active performance monitoring.
- **Level 1, ML pipeline automation:** the goal is **continuous training (CT)**. The pipeline is orchestrated, and the same pipeline runs in dev, pre-prod and prod ("experimental-operational symmetry"). Code is modularized into components and containers, and the pipeline itself is deployed, not just the model. It adds **automated data validation** and **model validation**, a **feature store**, **ML metadata management**, and **pipeline triggers** (on demand, on a schedule, when new data arrives, on model performance degradation, on significant drift).
- **Level 2, CI/CD pipeline automation:** adds source control, test and build services, deployment services, a **model registry**, a feature store, an ML metadata store and a pipeline orchestrator. Stages: development and experimentation → pipeline CI (build and test components) → pipeline CD (deploy the pipeline) → automated triggering → model CD (serve the model) → monitoring.
- **Pipeline steps named in the doc:** data extraction, data analysis, data preparation, model training, model evaluation, model validation, model serving, monitoring.
- **CI tests named in the doc:** unit tests for feature engineering logic; tests of model methods; tests that training converges (loss goes down); checks that there are no NaNs; tests that each component produces the expected artifacts; integration tests between components.

**2025–2026 shift toward GenAI and agents**
- MLflow 3 launched June 11, 2025, with GenAI as its primary focus. It is described as a turn "from pure experiment ledger to a full AI engineering platform". Tracing is its centerpiece, and it introduced the **LoggedModel** entity as a first-class citizen, "moving beyond the traditional run-centric approach" — [MLflow 3 launch blog](https://www.mlflow.org/blog/mlflow-3-launch); [MLflow 3 docs](https://mlflow.org/docs/3.1.3/genai/mlflow-3); [pebblous summary](https://blog.pebblous.ai/report/mlflow-mlops-standard/en/)
- MLflow 3.10 (2026-02-20) added a **GenAI / Classical ML workflow switcher** to its navigation. Separate UX paths for the two disciplines show how far they have diverged — [MLflow CHANGELOG](https://raw.githubusercontent.com/mlflow/mlflow/master/CHANGELOG.md)
- At Cloud Next on April 22, 2026, Google announced the **Gemini Enterprise Agent Platform** as the successor to Vertex AI. Vertex AI was "rebranded and expanded". Model Registry, Endpoints, Model Garden, Pipelines and Custom Training now sit under a "Models" submenu, with a new "Agents" menu above it. One source says existing Vertex AI API code keeps working, while deprecated Vertex AI Python SDK modules had a June 24, 2026 migration deadline (secondary sources) — [Wikipedia](https://en.wikipedia.org/wiki/Gemini_Enterprise_Agent_Platform); [HPCwire](https://www.hpcwire.com/aiwire/2026/04/23/google-unveils-gemini-enterprise-agent-platform/); [Medium GDE post](https://medium.com/google-developer-experts/vertex-ai-is-gone-here-is-what-google-built-instead-92556d1c64eb); [beri.net](https://www.beri.net/article/vertex-ai-gone-google-agent-platform)
- Anthropic's agent-eval guidance (Jan 9, 2026): "evaluating 'an agent' means evaluating the harness and model together". It recommends multiple **trials** per task because outputs vary between runs, and it defines a **transcript/trace/trajectory** as the full record of outputs, tool calls, reasoning and intermediate results — [Anthropic Engineering: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- **LLM-native artifacts in registries:** MLflow added a Prompt Registry (APIs moved to `mlflow.genai.prompts` in 3.1) and an **MCP Registry** for registering and versioning MCP servers (3.15.0, 2026-07-31). Its AI Gateway has traffic splits, fallbacks, budgets and guardrails (3.9–3.16) — [MLflow CHANGELOG](https://raw.githubusercontent.com/mlflow/mlflow/master/CHANGELOG.md); [MLflow releases](https://github.com/mlflow/mlflow/releases)
- **Vendor consolidation in LLMOps, 2025–2026:**
  - ClickHouse acquired **Langfuse** (Jan 16, 2026) — [ClickHouse](https://clickhouse.com/blog/clickhouse-acquires-langfuse-open-source-llm-observability)
  - OpenAI announced it would acquire **Promptfoo** (Mar 9, 2026) — [OpenAI](https://openai.com/blog/openai-to-acquire-promptfoo)
  - Mintlify acquired **Helicone** (Mar 3, 2026), and Helicone went into maintenance mode — [Helicone](https://helicone.ai/blog/joining-mintlify)
  - Apple acquired **WhyLabs** (2025), the commercial platform was discontinued and the code was open-sourced — [GeekWire](https://www.geekwire.com/2025/founders-at-seattle-startup-whylabs-join-apple-following-under-the-radar-acquisition)
  - lakeFS acquired **DVC** (Nov 18, 2025) — [lakeFS](https://lakefs.io/blog/lakefs-acquires-dvc/)

### Inferences
- **How LLMOps differs from classic MLOps:**
  - **Artifacts:** the versioned artifacts are prompts, model/provider configurations, tool and MCP-server definitions, retrieval indexes and agent harness code. Model weights often aren't among them, because many teams call hosted APIs and train nothing.
  - **Quality signal:** offline accuracy or AUC gives way to eval suites (code graders, LLM judges, human review) plus online evals on production traces.
  - **Monitoring unit:** the trace or span tree (LLM calls, tool calls, retrieval), not the feature vector.
  - **Cost:** cost per token and per request becomes a first-class SLO next to latency.
  - **Continuous training → continuous evaluation and prompt optimization:** for API-consuming teams, "CT" is replaced by prompt optimization (MLflow GEPA/MemAlign, judge alignment) and eval-gated config rollouts.
- Google's Level 0/1/2 framing maps onto LLM teams roughly as follows:
  - Level 0: prompts in code, eyeballed outputs.
  - Level 1: a versioned prompt registry plus an automated eval suite run on every change.
  - Level 2: CI-gated prompt/model/config rollouts with feature-flag canaries, online judges and trace-driven dataset curation feeding back into the eval set.
  - This mapping is my synthesis, not a published standard.
- Commercial LLMOps tooling is consolidating fast (observability bought by data/infra companies, eval and red-teaming bought by model labs). Lock-in risk argues for instrumenting with OpenTelemetry GenAI conventions so backends stay swappable.

### Gaps
- The Google MLOps doc, the **AWS Well-Architected ML Lens / Generative AI Lens** and the **Azure Well-Architected AI workload** guidance could not be fetched (egress blocked, search budget exhausted). Their current 2026 revisions, and whether Google has published an LLMOps or agent-ops maturity model, are unverified.
- [UNVERIFIED-BACKGROUND] AWS publishes a Well-Architected *Machine Learning Lens* and a *Generative AI Lens* (the latter introduced around re:Invent 2024 and updated in 2025). Azure has Well-Architected "AI workloads" guidance and documents "GenAIOps" (a successor to the "LLMOps" term) for Azure AI Foundry. Verify names and dates.
- [UNVERIFIED-BACKGROUND] Microsoft renamed Azure AI Studio to Azure AI Foundry (late 2024) and later to "Microsoft Foundry" (2025). Not verified this session.

---

## 2. CI/CD for ML: GitHub Actions/GitLab CI, testing data and models, CML, validation gates, continuous training

### Takeaway
CI for ML in 2026 means three test layers: code tests, data and model tests (Evidently Test Suites, model-validation gates), and, for LLM apps, eval suites run as pytest-style or CLI checks (promptfoo, DeepEval `deepeval test run`, MLflow `@mlflow.test`). The older Iterative tools are drifting. CML's last release was October 2024, and DVC now belongs to lakeFS. Registry webhooks (MLflow 3.3+) and alarm-gated deployment (SageMaker guardrails) close the CD loop.

### Cited Findings
- **CML (Continuous Machine Learning)** is an open-source CLI for ML CI/CD (older):
  - It can train and evaluate models and post a visual metrics report on each PR. Commands include `cml comment create`, `cml check create`, `cml pr create` and `cml tensorboard connect`.
  - `cml runner launch` provisions runners locally or on AWS, Azure, GCP or Kubernetes. The README's example is a GPU job on AWS EC2 that shuts down after the job, and CML restarts jobs interrupted by GitHub Actions timeouts or EC2 spot interruptions.
  - GitHub Actions is the primary target. GitLab CI/CD (which needs a personal access token) and Bitbucket Cloud are also documented.
  - Source: [iterative/cml README](https://github.com/iterative/cml)
- **CML's latest release is v0.20.6 (Oct 24, 2024).** There is no archive banner, but the project shows no releases for about two years — [CML releases](https://github.com/iterative/cml/releases)
- **DVC:** lakeFS acquired the DVC open-source project from Iterative.ai, announced Nov 18, 2025. DVC stays a separate OSS tool aimed at smaller datasets, while lakeFS focuses on enterprise-scale data version control — [lakeFS blog](https://lakefs.io/blog/lakefs-acquires-dvc/); [DVC blog Q&A](https://dvc.org/blog/dvc-joins-lakefs-your-questions-answered/)
- **Data and model tests in CI (Evidently):** "Turn any Report into a Test Suite by adding pass/fail conditions, useful for regression testing, CI/CD, and data validation". Test conditions can be auto-generated from a reference dataset. Evidently has 100+ built-in metrics and 20+ drift tests and distance metrics, and is Apache-2.0 — [evidentlyai/evidently](https://github.com/evidentlyai/evidently)
- **LLM eval suites as CI tests:**
  - **DeepEval** is "similar to Pytest but specialized for unit testing LLM apps". Tests run with `deepeval test run <file>`, and it "integrates with any CI/CD environment" (Apache 2.0) — [confident-ai/deepeval](https://github.com/confident-ai/deepeval)
  - **promptfoo** is a CLI and library for evals and red teaming. It runs checks in CI/CD pipelines, scans PRs for LLM-related security and compliance issues (a `code-scan-action` folder is in the repo), and is MIT-licensed — [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo)
  - **MLflow 3.14.0** added "pytest regression testing via `@mlflow.test`", plus review queues and an LLM Playground — [MLflow CHANGELOG](https://raw.githubusercontent.com/mlflow/mlflow/master/CHANGELOG.md)
- **Registry events for CD:** MLflow 3.3.0 (2025-08-19) added **Model Registry webhooks** — [MLflow CHANGELOG](https://raw.githubusercontent.com/mlflow/mlflow/master/CHANGELOG.md)
- **Eval timing in the release cycle:** "Automated evals run pre-launch and in CI on each change". Production monitoring catches drift after launch, and A/B tests validate significant changes once traffic is sufficient — [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- **Capability vs regression suites:** capability evals should start at a low pass rate ("a hill to climb"). Regression evals should sit near 100%, and saturated capability evals "graduate" into regression suites — [Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- **Continuous training triggers** in Google's Level 1 (see §1): on demand, on schedule, on new data, on performance degradation, on drift — [Google Cloud MLOps doc](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) (not re-fetched this session)
- **Online judges as a CT/CE trigger:** MLflow 3.9 (2026-01-28) added "online monitoring with LLM judges on traces". A third-party listing describes "continuous monitoring with judge-in-the-loop alerting" — [MLflow CHANGELOG](https://raw.githubusercontent.com/mlflow/mlflow/master/CHANGELOG.md); [vantaige.io](https://vantaige.io/ai-tool/mlflow)

### Inferences
- A representative 2026 GitHub Actions or GitLab CI pipeline for an ML or LLM service:
  - **Classic ML:** lint and unit tests → data validation (Evidently Test Suite against a reference) → train on a GPU runner (cloud self-hosted runner or CML-style ephemeral runner) → evaluate against the champion → register the candidate in the registry with metrics.
  - **LLM app:** run promptfoo or DeepEval or `@mlflow.test` eval suites against a golden dataset → fail the PR on regression → publish the prompt version.
  - **Deploy:** a registry webhook or alias change triggers the CD job → canary or linear rollout with alarm-based auto-rollback.
- With CML dormant, teams that used it typically move to native CI features (self-hosted or larger GPU runners, PR comment actions) plus a tracking server's comparison UI. This is inferred from CML's release inactivity; I found no source that documents the migration.

### Gaps
- GitHub-hosted GPU runner availability, pricing and 2026 specs, and GitLab's GPU runner and CI/CD component catalog for ML, were not verified (search budget exhausted).
- [UNVERIFIED-BACKGROUND] Common model-validation gates:
  - candidate must beat the champion on the holdout by a margin
  - fairness and slice metrics checked
  - latency and size budgets met
  - infra validation, meaning the model loads and serves in a staging container. TFX calls this "InfraValidator"; TFX itself is older.
  - A model's eligibility for promotion is often tracked with the SageMaker Model Registry `ModelApprovalStatus` (PendingManualApproval → Approved/Rejected), with an EventBridge rule triggering the deploy pipeline.

---

## 3. Infrastructure as code: Terraform/OpenTofu, Pulumi, AWS CDK, Crossplane; GitOps (Argo CD, Flux); IaC for a GPU cluster or inference endpoint

### Takeaway
Terraform (HashiCorp, now IBM) and OpenTofu (Linux Foundation fork) are diverging. In October 2026 Terraform is at 1.16.6 stable, with 1.17 RC making Terraform Policy GA. OpenTofu is at 1.13.1, with state encryption, ephemeral resources, and the `enabled` meta-argument shipping there first. Kubernetes-native IaC (Crossplane v2.4) and GitOps (Argo CD 3.5, Flux 2.9) are the standard way to manage GPU inference clusters. Argo Rollouts and Flux handle progressive delivery.

### Cited Findings
**Terraform**
- Latest stable is **v1.16.6 (Oct 14, 2026)**. **v1.17.0-rc2** shipped the same day. Highlights of 1.17:
  - provider requirements can use variables and locals
  - new `-minimal-refresh` planning option
  - **Terraform Policy is GA**: the `-policies` flag works for plan, apply and query without an experimental build
  - `terraform version` JSON includes a `format_version` field
  - diagnostics from renewing ephemeral resources are now shown
  - Source: [hashicorp/terraform releases](https://github.com/hashicorp/terraform/releases)
- A 2026 guide describes the two projects as diverging. State encryption, ephemeral values, early variable evaluation and provider `for_each` shipped in OpenTofu first, and it lists Terraform under "HashiCorp / IBM, single vendor governance". This is a secondary source and not independently verified — [env.dev OpenTofu guide](https://env.dev/guides/opentofu)

**OpenTofu**
- Latest is **v1.13.1 (Oct 1, 2026)**. v1.13.0 shipped Sep 30, 2026. Features of 1.13:
  - official Windows on ARM64 support
  - new `assume...` functions and a `convert` function to reduce unknowns during planning
  - experimental linting with the `-lint` flag
  - experimental "Symbol Libraries" (reusable values, functions and type aliases)
  - plan files now embed provider schemas
  - `local-exec` sets `TRACEPARENT` when OpenTelemetry tracing is active
  - Breaking changes: WinRM provisioners dropped; macOS requires Ventura (13) or later; 1.13 is the last series with official 32-bit builds.
  - Source: [opentofu/opentofu releases](https://github.com/opentofu/opentofu/releases)
- OpenTofu 1.11's headline features were **ephemeral resources** (safer temporary credentials) and the **`enabled` lifecycle argument**, which replaces conditional `count`. It also brought RAM and CPU efficiency gains and S3 state and lock object tagging — [linuxiac](https://linuxiac.com/category/news/software/page/70/); [env.dev](https://env.dev/guides/opentofu)

**Crossplane** (Kubernetes control-plane IaC)
- Latest is **v2.4.2 (Sep 22)**. v2.4.0 (Aug 20) was a quarterly release that brought:
  - composite resources reconcile when the resources they require change
  - "safe-start" providers that scale to zero until a managed resource definition is activated
  - server-side apply for package runtime objects
- v1 legacy workloads such as Claims and cluster-scoped resources "remain supported in Crossplane v2".
- Source: [crossplane/crossplane releases](https://github.com/crossplane/crossplane/releases)

**GitOps**
- **Argo CD:**
  - The latest stable is **v3.5.5 (Oct 12, 2026)**. 3.4.x and 3.3.x are still patched, and **v3.6.0-rc2** shipped Oct 6, 2026.
  - The 3.6 RCs fix four critical security issues: command execution via a Kustomize remote ref and via a Kustomize Helm config home, reading repo-server files through a Jsonnet import, and an AppProject restriction bypass via PreDelete/PostDelete hooks.
  - Breaking change in 3.6: OCI manifests larger than 4 MiB are rejected.
  - 3.6.0-rc1 added hydrator commit signing (alpha).
  - Source: [argoproj/argo-cd releases](https://github.com/argoproj/argo-cd/releases)
- Argo CD 3.3 was released around February 2026, and the project releases about every 3 months — [InfoQ](https://infoq.com/news/2026/02/argocd-33); [skills.sh listing](https://skills.sh/nmime/infra-skills/k8s-gitops)
- **Flux:**
  - The latest is **v2.9.6 (Oct 1, 2026)**. **v2.9.0 (Jun 30, 2026)** added:
    - a CLI plugin system
    - SSA field-ignore rules for drift control
    - SOPS with the Age post-quantum cipher
    - Workload Identity auth for OpenBao and Vault and for AWS CodeCommit
    - Helm post-render strategies
    - Git commit signing and verification with SSH keys
    - Sigstore custom trusted roots for air-gapped clusters
    - monorepo path discovery (ArtifactGenerator)
    - secret-less OIDC webhook receivers
  - 2.9 supports Kubernetes 1.34–1.36 and removes the `image.toolkit.fluxcd.io/v1beta2` and `notification.toolkit.fluxcd.io/v1beta2` APIs.
  - Source: [fluxcd/flux2 releases](https://github.com/fluxcd/flux2/releases)
- **Flux v2.7** (older, 2025) made image update automation GA and added the ExternalArtifact and ArtifactGenerator APIs — [Flux blog](https://v2-6.docs.fluxcd.io/blog/)
- **Argo Rollouts:** a Kubernetes controller and CRDs for blue-green and canary rollouts, with weighted traffic shifting and manual judgement.
  - Analysis steps query Prometheus, Datadog, New Relic, InfluxDB, Wavefront, Kayenta, Kubernetes Jobs or web endpoints, and automatically promote or roll back.
  - Integrates with NGINX, ALB, APISIX, Traefik, Ambassador, Contour, Istio, Linkerd and SMI. Gateway API support is alpha.
  - Source: [argoproj/argo-rollouts](https://github.com/argoproj/argo-rollouts)
- **Self-hosting observability via IaC:** Langfuse ships Terraform templates for AWS, Azure and GCP plus a Helm chart, which is preferred for production — [langfuse/langfuse](https://github.com/langfuse/langfuse). MLflow 3.13 added an official Helm chart — [MLflow CHANGELOG](https://raw.githubusercontent.com/mlflow/mlflow/master/CHANGELOG.md)

### Inferences
- **Typical IaC layering for a GPU inference platform** (illustrative synthesis, not from a single source):
  1. **Terraform/OpenTofu (or Pulumi/CDK)** provisions the VPC, a managed Kubernetes cluster (EKS/GKE/AKS), GPU node pools or autoscaler config, IAM/workload identity, object storage for artifacts, and managed endpoints such as SageMaker or Agent Platform endpoints.
  2. **GitOps (Argo CD or Flux)** reconciles in-cluster add-ons and workloads from Git: the GPU operator and device plugin, the serving stack (KServe, vLLM or Triton deployments), and observability collectors.
  3. **Argo Rollouts** (or Flux with Flagger) handles canary or blue/green of model-server versions, with metric analysis.
  4. **Crossplane** suits teams that want cloud resources (buckets, databases, managed endpoints) declared as Kubernetes CRDs and reconciled by the same GitOps loop.
- OpenTofu's ephemeral resources and Terraform's write-only and ephemeral support matter for ML infrastructure, because they keep API keys and model-provider credentials out of state files.

### Gaps
- No 2026 primary source was fetched for **Pulumi** (e.g., Pulumi IaC versions or AI-agent features) or **AWS CDK** (v2 status), so they are unverified this session.
- Crossplane v2.0 details (namespaced managed resources, Operations, composition-function-only model) were not confirmed. The release page did not include the v2.0 notes.
- [UNVERIFIED-BACKGROUND] IBM completed its acquisition of HashiCorp in early 2025. Terraform moved to the BUSL 1.1 license in Aug 2023, which triggered the OpenTofu fork (OpenTofu is MPL-2.0 under the Linux Foundation, and joined the CNCF in 2025).
- [UNVERIFIED-BACKGROUND] Typical GPU-cluster modules (terraform-aws-modules/eks with Karpenter GPU NodePools, GKE node pools with accelerators, NVIDIA GPU Operator via Helm) were not verified for 2026 versions.

---

## 4. Model registries and artifact management: MLflow (MLflow 3 GenAI features), SageMaker Model Registry, Vertex AI Model Registry, Hugging Face Hub; model cards and versioning

### Takeaway
MLflow is the de facto open registry. As of 3.17.1 (Oct 13, 2026) it versions models (LoggedModel), prompts, evaluation datasets, judges and scorers, and MCP servers, with an embedded AI Gateway and RBAC. Cloud registries persist: SageMaker Model Registry, and Vertex AI Model Registry now under the "Models" section of Gemini Enterprise Agent Platform. Hugging Face Hub model cards (YAML metadata plus README) remain the documentation standard.

### Cited Findings
**MLflow 3.x release timeline**, from the official CHANGELOG and GitHub releases — [MLflow CHANGELOG](https://raw.githubusercontent.com/mlflow/mlflow/master/CHANGELOG.md); [MLflow GitHub releases](https://github.com/mlflow/mlflow/releases)

| Version (date) | Headline changes |
|---|---|
| **3.0 / 3.1 (2025-06-11)** | MLflow 3 GA, published as GitHub tag v3.0.0 on 11 Jun, while the changelog labels the headline entry "3.1 (2025-06-11)". Added `mlflow.genai.optimize_prompt`, custom prompt judges, and OpenAI token tracking. Breaking: prompt registry APIs moved under `mlflow.genai.prompts`; the default registry URI is `databricks-uc` when tracking on Databricks; the `search_traces` DataFrame uses the V3 schema. |
| 3.1.1 | Prompt text limit raised from 5K to 100K characters. |
| **3.2.0 (2025-08-05)** | TypeScript tracing SDK; feedback tracking (human feedback, ground truth, LLM judges on traces); PII masking via a span post-processor. |
| **3.3.0 (2025-08-19)** | Model Registry webhooks; "open-sourced GenAI evaluation"; FastAPI + Uvicorn as the default tracking server. |
| **3.4.0 (rc 2025-09-11)** | OpenTelemetry metrics export; MCP server integration; `make_judge` custom judges API; evaluation datasets stored in experiments. |
| **3.5.0 (2025-10-16)** | Job execution backend; GEPA prompt optimization; chat UI for the prompt registry; security middleware. |
| **3.6.0 (2025-11-07)** | Full OpenTelemetry support in the OSS server; TypeScript integrations (Vercel AI SDK, Gemini, Anthropic, Mastra); judge cost tracking; Agent Server. |
| **3.7.0 (2025-12-05)** | Multi-turn evaluation in `mlflow.genai.evaluate`; trace comparison view; structured outputs in `make_judge`; SQLite as the default tracking backend. |
| **3.8.0 (2025-12-19)** | Prompt model configuration; DeepEval judges integration; conversational safety and tool-call-efficiency scorers. |
| **3.9.0 (2026-01-28)** | MLflow Assistant (an in-product chatbot backed by Claude Code); AI Gateway revamp (runs inside the tracking server, with passthrough endpoints, traffic splits and fallbacks); online LLM-judge monitoring on traces; Judge Builder UI; distributed tracing APIs; MemAlign judge optimizer. |
| **3.10.0 (2026-02-20)** | Organizations (multi-workspace); multi-turn evaluation and conversation simulation; trace cost tracking; GenAI vs Classical ML navigation. |
| **3.11.1 (2026-04-07)** | Automatic issue detection on traces; gateway budget policies; an option to export OTLP with the **OTel GenAI semantic conventions**; UV dependency inference; pickle-free model formats (torch.export, skops). |
| **3.12.0 (2026-05-04)** | Multimodal tracing; Codex, Gemini and Qwen coding-agent tracing; gateway guardrails. |
| **3.13.0** | RBAC with admin UI; trace archival to object storage; Helm chart. Breaking: MLServer removed; `judge.align()` defaults to MemAlign; file-system stores error unless `MLFLOW_ALLOW_FILE_STORE` is set. |
| **3.14.0** | `mlflow agent setup`; review queues; `@mlflow.test`; LLM Playground. Breaking: default serialization is skops for sklearn and LightGBM, and pt2 for PyTorch. |
| **3.15.0 (2026-07-31)** | **MCP Registry**; multi-provider Assistant; image support in judges. |
| **3.16.0 (2026-09-03)** | Fail-closed basic-auth authorization by default; per-user budget policies in the AI Gateway. 3.16.1 removed the default admin password. |
| **3.17.0 (2026-10-06)** | Typed (Boolean and categorical) feedback for scorers and judges; fine-grained permissions on shared resources; trace analytics via daily rollups. SQL-backed servers need a coordinated `mlflow db upgrade`, and mixed-version rolling upgrades are unsupported. |
| **3.17.1 (2026-10-13)** | Latest release. Decision API in `make_judge()`; review-queue management for Databricks. |

- The MLflow Prompt Registry includes versioning, tracking and prompt optimization from evaluation feedback and labeled datasets — [MLflow 3 docs](https://mlflow.org/docs/3.1.3/genai/mlflow-3)
- 2.x is still maintained: **MLflow 2.11.5** shipped Sep 23 (opt-in routing of Unity Catalog artifact transfers through the Databricks SDK Files API) — [MLflow releases](https://github.com/mlflow/mlflow/releases)

**Vertex AI Model Registry**
- Now listed under the "Models" submenu of the **Gemini Enterprise Agent Platform**, with Endpoints, Model Garden, Pipelines, Custom Training and AutoML. Model Garden offers 200+ models, including Gemini 3.1 Pro (secondary sources) — [Medium GDE](https://medium.com/google-developer-experts/vertex-ai-is-gone-here-is-what-google-built-instead-92556d1c64eb); [Wikipedia](https://en.wikipedia.org/wiki/Gemini_Enterprise_Agent_Platform)

**Hugging Face Hub model cards**
- A model card is the repo's `README.md`, with YAML metadata at the top. Metadata fields include:
  - `license` (or `license_name` / `license_link`)
  - `datasets`
  - `base_model`, with optional `base_model_relation` for fine-tunes, adapters, quantizations and merges
  - `pipeline_tag`
  - `model-index` for structured eval results, using the Papers-with-Code format
  - `tags` and `library_name`
  - `new_version`, which links to a newer model; the Hub follows the chain to the latest
- Recommended sections cover the model description, intended uses and limitations (including bias and ethics), training parameters, datasets and evaluation results. The doc cites Mitchell et al., "Model Cards for Model Reporting" (arXiv 1810.03993).
- Source: [huggingface/hub-docs model-cards.md](https://raw.githubusercontent.com/huggingface/hub-docs/main/docs/hub/model-cards.md)

### Inferences
- In 2026 the "registry" has widened from a model registry into an **AI asset registry** covering models, prompts, judges and scorers, eval datasets (immutable versions arrived in MLflow 3.15.2), MCP servers and gateway routes. Registry governance features (RBAC, fail-closed auth, fine-grained permissions in 3.13–3.17) show MLflow being hardened for shared enterprise use.
- MLflow's security posture changed materially in 2026: fail-closed auth by default, and the default admin password removed. Self-hosted tracking servers upgraded from older versions need auth configuration reviewed.

### Gaps
- **SageMaker Model Registry** could not be verified this session: AWS docs were blocked and the search budget was exhausted. [UNVERIFIED-BACKGROUND]
  - The registry is organized as **Model Package Groups** containing versioned **Model Packages**, with `ModelApprovalStatus` values PendingManualApproval, Approved and Rejected.
  - Approval-status changes emit EventBridge events, which are used to trigger deployment pipelines.
  - Model packages can be linked to SageMaker Model Cards and Model Dashboard.
  - SageMaker offers **managed MLflow** tracking servers (launched in 2024), and later integrated MLflow with the SageMaker Model Registry.
- **Vertex AI Model Registry** specifics (version aliases such as `default`, BigQuery ML model registration, model evaluation import) are [UNVERIFIED-BACKGROUND] for 2026.
- **MLflow registry aliases.** [UNVERIFIED-BACKGROUND] MLflow deprecated model "stages" (Staging/Production/Archived) in 2.9 in favor of **aliases** (e.g., `@champion`) and tags. Prompt Registry versions also support aliases. Not re-verified in the 3.x docs this session.
- **Hugging Face Hub versioning** (git- and Xet-based repos with commits, branches and tags as revisions) was not described in the fetched page. [UNVERIFIED-BACKGROUND]

---

## 5. Deployment strategies: blue/green, canary, shadow, A/B, champion/challenger; rollbacks; feature flags for prompts and models

### Takeaway
On managed endpoints, SageMaker deployment guardrails implement blue/green with all-at-once, canary or linear traffic shifting. Each step has a "baking period", and CloudWatch alarms trigger auto-rollback. On Kubernetes, Argo Rollouts provides canary and blue-green with metric-analysis-driven promotion. For LLM apps the unit being rolled out is often a prompt/model config. These ship as runtime feature-flag variations (LaunchDarkly AI Configs with guarded rollouts) or gateway traffic splits (MLflow AI Gateway) rather than redeploys.

### Cited Findings
- **SageMaker deployment guardrails** — [AWS docs: Blue/Green Deployments](https://docs.aws.amazon.com/sagemaker/latest/dg/deployment-guardrails-blue-green.html); [AWS blog](https://aws.amazon.com/blogs/machine-learning/take-advantage-of-advanced-deployment-strategies-using-amazon-sagemaker-deployment-guardrails); [Launch announcement, Nov 2021](https://aws.amazon.com/about-aws/whats-new/2021/11/new-deployment-guardrails-amazon-sagemaker-inference-endpoints/)
  - Blue/green deployments offer three traffic-shifting modes: **all at once, canary, and linear**.
    - **Canary** sends a small slice of traffic to the green fleet first.
    - **Linear** moves traffic in fixed increments, with a baking period at each step.
  - A **baking period** is a fixed window for monitoring the green fleet before the next stage. A final bake can run after all traffic has shifted, before the blue fleet is terminated.
  - **Auto-rollback:** CloudWatch alarms are attached to the new fleet. If any alarm trips during any baking period, all traffic rolls back to the blue fleet.
  - **Cost:** multi-stage shifts bill both fleets for the whole update.
  - The feature dates to 2021 (older), and is still the documented mechanism.
- **Shadow deployment:** production traffic goes to both versions, but users only see the old version's responses. The search returned this definition from a third-party blog, not from SageMaker docs — [barkingiguana: Shadow, Canary, or Linear](https://barkingiguana.com/writing/shadow-canary-or-linear-rolling-out-a-new-model/)
- **Argo Rollouts (Kubernetes):**
  - blue-green and canary with weighted traffic shifting, manual judgement and experiments
  - analysis queries against Prometheus, Datadog and similar providers drive automatic promote or rollback
  - traffic **mirroring**, the mechanism behind shadow deployments, is supported on some mesh and ingress integrations
  - Source: [argoproj/argo-rollouts](https://github.com/argoproj/argo-rollouts)
- **Feature flags for prompts and models (LaunchDarkly AI Configs):**
  - A **variation** is the unit that gets versioned and rolled out: a specific combination of model, messages and parameters such as temperature and max tokens.
  - Prompt and model changes are made at runtime without redeploying, and rolled out gradually: internal testers → beta users → a small percentage of production.
  - **Guarded Rollouts for AI Configs** (July 2025) automatically roll back to the previous variation when guardrail metrics breach thresholds, for example completion error spikes.
  - The AI SDK auto-emits positive and negative feedback, tokens in and out, latency, and completion error and success rates.
  - Newer **AI Versioning** (track, compare, revert) and **AI Experiments** (compare prompt and model configs) build on this.
  - Sources: [LaunchDarkly changelog: Guarded rollouts for AI Configs](https://launchdarkly.com/changelog/guarded-rollouts-for-ai-configs/); [LaunchDarkly: AI Configs intro](https://launchdarkly.com/blog/launch-week-2024-introducing-ai-configs/); [LaunchDarkly: upgrading OpenAI models with AI Configs](https://launchdarkly.com/blog/upgrade-openai-models-python-fastapi-ai-configs/); [plushcap summary of AI Experiments/Versioning](https://plushcap.com/content/launchdarkly/blog/launchdarkly-introducing-ai-experiments-and-ai-versioning)
- **Gateway-level traffic splitting:** the MLflow AI Gateway revamp in 3.9.0 (Jan 2026) added traffic splits and fallbacks. 3.12 added guardrails, and 3.11 and 3.16 added budget policies, including per-user budgets — [MLflow CHANGELOG](https://raw.githubusercontent.com/mlflow/mlflow/master/CHANGELOG.md)
- **A/B tests "validate significant changes once traffic is sufficient"** and complement offline evals and monitoring in the "Swiss cheese" layered model — [Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- **Flux image update automation** reached GA in v2.7. It automatically bumps image tags in Git, the usual way new model-server images reach clusters through GitOps — [Flux blog](https://v2-6.docs.fluxcd.io/blog/)

### Inferences
- **Strategy cheat sheet** (synthesis):
  - **Blue/green:** two full fleets with an atomic switch. Fast rollback, but double cost during the switch.
  - **Canary or linear:** an incremental share of traffic, with metric or alarm gates at each step.
  - **Shadow (mirroring):** zero user impact. Use it to validate latency, errors and output distributions for a new model before exposing it. For LLMs, run offline judges on the shadow outputs.
  - **A/B:** randomized user split measured on business metrics. Needs enough traffic and statistical power.
  - **Champion/challenger:** the registry or alias pattern where the challenger is promoted only if it beats the champion on agreed metrics, offline and/or in an A/B test.
  - **Feature-flag rollouts:** the most natural fit for prompts and model selection, since they need no redeploy and can be targeted by user segment.
- For LLM apps the rollback trigger should include **quality signals** (online judge scores, thumbs-down rate) as well as error rate and latency. LaunchDarkly's auto-tracked feedback metrics and MLflow's online judges both point in this direction.

### Gaps
- [UNVERIFIED-BACKGROUND] SageMaker supports **shadow tests** (shadow variants comparing a production variant to a shadow variant on mirrored traffic; launched at re:Invent 2022) and **production variants** with weighted traffic for A/B testing. Not confirmed in this session's sources.
- Vertex AI / Agent Platform endpoint traffic-split semantics in 2026, and KServe's canary features (`canaryTrafficPercent`), were not verified.
- No primary source was found on champion/challenger tooling specifics for 2026.

---

## 6. Observability: classic ML monitoring (drift, PSI/KS) and LLM observability and tracing (OTel GenAI semconv, Langfuse, LangSmith, Phoenix, Helicone, Datadog, W&B Weave); what metrics to track

### Takeaway
LLM observability has converged on **OpenTelemetry-based tracing**. The OTel GenAI semantic conventions are still "Development", not stable, as of Oct 2026, and moved to a dedicated repo (open-telemetry/semantic-conventions-genai) in June 2026. They now cover inference, agent and workflow spans, tool and MCP spans, token-usage counters, server latency metrics (TTFT, TPOT) and a `gen_ai.evaluation.result` event. Backends (Datadog, MLflow, Langfuse, Phoenix) increasingly ingest OTel GenAI spans natively. The vendor field has consolidated sharply.

### Cited Findings
**OpenTelemetry GenAI semantic conventions: status and location**
- Every gen_ai attribute, span, metric and event is still labeled **Development** (formerly "experimental"). None were Stable as of mid-July 2026 — [greptime blog, May 2026](https://www.greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions); [DEV community write-up](https://dev.to/azena-ai/opentelemetrys-genai-semantic-conventions-are-not-stable-yet-heres-what-actually-shipped-in-2026-3mke)
- The conventions left the main semantic-conventions repo in June 2026. One account says GenAI, OpenAI-specific and MCP conventions were deprecated there in **v1.42.0 (June 12, 2026)** and moved to **open-telemetry/semantic-conventions-genai** (secondary) — [DEV community](https://dev.to/azena-ai/opentelemetrys-genai-semantic-conventions-are-not-stable-yet-heres-what-actually-shipped-in-2026-3mke)
- The new repo has a "Development" badge and no releases yet; its CHANGELOG has only an "Unreleased" section, managed by Towncrier. It uses Weaver to depend on the core conventions — [semantic-conventions-genai repo](https://github.com/open-telemetry/semantic-conventions-genai); [CHANGELOG](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/CHANGELOG.md)
- Doc set in `docs/gen-ai/`: client-inference, gen-ai-spans, gen-ai-agent-spans, gen-ai-events, gen-ai-exceptions, gen-ai-metrics, gen-ai-token-metrics, plus technology-specific docs for **Anthropic, AWS Bedrock, Azure AI Inference, OpenAI** and **MCP** — [docs/gen-ai directory](https://github.com/open-telemetry/semantic-conventions-genai/tree/main/docs/gen-ai)

**Spans** — [gen-ai-spans.md](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-spans.md)
- Well-known `gen_ai.operation.name` values: `chat`, `embeddings`, `retrieval`, `fetch_response`, `execute_tool`, `invoke_agent`, `text_completion`, and memory operations (`create_memory`, `search_memory`, `update_memory`, `upsert_memory`, `delete_memory`).
- Span names:
  - embeddings: `{operation} {gen_ai.request.model}`
  - retrieval: `{operation} {gen_ai.data_source.id}`
  - tool: `execute_tool {gen_ai.tool.name}` (INTERNAL kind)
- Key attributes:
  - `gen_ai.provider.name` (e.g., `openai`, `anthropic`, `gcp.gemini`, `aws.bedrock`)
  - `gen_ai.request.model`, `gen_ai.response.model`
  - `gen_ai.usage.input_tokens`, which includes cached tokens
  - `gen_ai.response.finish_reasons`
  - `gen_ai.conversation.id`: set only if the framework already has an ID. Never fall back to a UUID, trace ID or hash.
  - `gen_ai.tool.call.id`, `gen_ai.tool.type`, `gen_ai.retrieval.top_k`
  - `error.type`, which is required on failure.
- **Content capture is opt-in and off by default:** `gen_ai.system_instructions`, `gen_ai.input.messages`, `gen_ai.output.messages`, `gen_ai.tool.definitions`, tool call arguments and results, and retrieval documents and query text. It is gated by an explicit opt-in such as `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`. In production the spec recommends storing content externally and recording references.

**Agent spans** — [gen-ai-agent-spans.md](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-agent-spans.md)
- `create_agent {name}` (CLIENT) and `invoke_agent {name}`:
  - CLIENT kind for remote agent services such as the OpenAI Assistants API or AWS Bedrock Agents.
  - INTERNAL kind for in-process frameworks such as LangChain or CrewAI.
- `invoke_workflow {gen_ai.workflow.name}` (INTERNAL) for multi-agent coordination.
- `plan {name}`, reported only when planning can be reliably identified.
- Attributes: `gen_ai.agent.id` (e.g., a Bedrock agent ARN), `gen_ai.agent.name`, `gen_ai.agent.version`, `gen_ai.workflow.name`, `gen_ai.data_source.id`.
- A secondary source says v1.41 split invoke_agent into CLIENT and INTERNAL kinds and required the tool name in the execute_tool span name — [greptime](https://www.greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions)

**Metrics**, all Histograms in Development status — [gen-ai-metrics.md](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-metrics.md)
- `gen_ai.client.operation.duration` (s). Non-inference operations only; inference uses `gen_ai.client.inference.duration`.
- `gen_ai.server.request.duration`
- `gen_ai.server.time_to_first_token`, which includes queue and prefill time
- `gen_ai.server.time_per_output_token`, calculated as (request duration − TTFT) / (tokens after the first)
- `gen_ai.invoke_workflow.duration`
- `gen_ai.invoke_agent.duration`
- `gen_ai.invoke_agent.inference_calls`
- `gen_ai.invoke_agent.tool_calls`
- `gen_ai.execute_tool.duration`

**Token metrics, current repo** — [gen-ai-token-metrics.md](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-token-metrics.md)
- **Counters:** `gen_ai.client.inference.usage.input_tokens`, `.output_tokens` (includes reasoning tokens), `.cache_read.input_tokens`, `.cache_write.input_tokens`, `.reasoning.output_tokens`
- **Histograms:** `gen_ai.client.inference.operation.input_tokens` and `.output_tokens`, for percentiles and outliers rather than totals or cost
- `gen_ai.token.modality` (`text` / `image` / `audio` / `unknown`) is required on the counters.
- **(older naming)** Earlier spec versions defined a single histogram, **`gen_ai.client.token.usage`** (unit `{token}`), split by `gen_ai.token.type`. When both used and billable tokens are known, it must report billable tokens — [opentelemetry.io gen-ai-metrics](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-metrics/). The fetched new-repo doc doesn't mention it, so treat it as superseded or renamed in the new repo (inference).

**Evaluation event** — [gen-ai-events.md](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/gen-ai-events.md)
- `gen_ai.evaluation.result` carries `gen_ai.evaluation.name` (required, e.g., "Relevance"), `gen_ai.evaluation.score.value`, `gen_ai.evaluation.score.label` (low-cardinality, e.g., pass/fail), `gen_ai.evaluation.explanation` and `gen_ai.response.id`.
- It should be parented to the evaluated operation's span.

**Backend support for OTel GenAI**
- **Datadog:**
  - Since Dec 2025, LLM Observability (called "Agent Observability" in current docs) natively ingests OTel GenAI semconv **v1.37+** and OpenInference spans, with no Datadog SDK or Agent required.
  - Caveats: traces take 3–5 minutes to appear; evaluations on OTel spans need the `source:otel` tag; hex OTel IDs must be converted to decimal.
  - Sources: [Datadog blog](https://datadoghq.com/blog/llm-otel-semantic-convention/); [Datadog docs](https://docs.datadoghq.com/llm_observability/instrumentation/otel_instrumentation)
- **MLflow:** full OTel support in the OSS server (3.6), and an option to export with the OTel GenAI conventions (3.11) — [MLflow CHANGELOG](https://raw.githubusercontent.com/mlflow/mlflow/master/CHANGELOG.md)

**LLM observability vendors (Oct 2026 status)**
- **Langfuse:** open source (MIT except `ee` folders). Covers tracing, sessions, prompt management with caching, evals (LLM-as-judge, code evaluators, user feedback, manual labeling), datasets and experiments, and a playground. Self-hosting options are Docker Compose, a single VM, Kubernetes via Helm, or Terraform for AWS, Azure and GCP; it is built on ClickHouse — [langfuse/langfuse](https://github.com/langfuse/langfuse)
  - **ClickHouse acquired Langfuse (announced Jan 16, 2026)** alongside a $400M Series D at a reported $15B valuation. Langfuse says the roadmap, open-source and self-hosting commitments are unchanged. It had 2,000+ paying customers and 26M+ SDK installs per month — [ClickHouse blog](https://clickhouse.com/blog/clickhouse-acquires-langfuse-open-source-llm-observability); [Langfuse blog](https://langfuse.com/blog/joining-clickhouse); [SiliconANGLE](https://siliconangle.com/2026/01/16/database-maker-clickhouse-raises-400m-acquires-ai-observability-startup-langfuse/); [Orrick](https://www.orrick.com/en/news/2026/01/open-source-llm-observability-langfuse-acquired-by-clickhouse-inc)
- **Arize Phoenix:** open source under **Elastic License 2.0**. Tracing uses OpenTelemetry with OpenInference auto-instrumentation. Also offers evals, versioned datasets and experiments, a playground, prompt management (versioning and tagging), a built-in agent ("PXI") and a remote MCP server. Self-hostable via pip, Docker or Helm. **Arize AX** is the managed product — [Arize-ai/phoenix](https://github.com/Arize-ai/phoenix)
- **LangSmith (LangChain):** framework-agnostic tracing and evaluation, with Python and JS/TS SDKs (`wrap_openai`, the `traceable` decorator) and native LangChain integration — [langchain-ai/langsmith-sdk](https://github.com/langchain-ai/langsmith-sdk)
- **Helicone:** acquired by **Mintlify (Mar 3, 2026)** and in **maintenance mode**: security updates, new models and bug fixes continue, but there is no new feature development. It had processed 14.2T tokens for 16,000 organizations. Comparison articles advise against it for new deployments — [Helicone blog](https://helicone.ai/blog/joining-mintlify); [llmgateway.io](https://llmgateway.io/blog/helicone-alternatives)
- **W&B Weave:** Apache-2.0. `@weave.op` function tracing, auto-tracing of `openai` after `weave.init()`, an Agents tab for conversations, turns, LLM calls and tool calls (OpenAI Agents SDK, Claude Agent SDK, Google ADK), and evaluations — [wandb/weave](https://github.com/wandb/weave)
- **WhyLabs (classic ML and LLM monitoring):** Apple acquired it in an under-the-radar deal (2025; reported dates conflict). The commercial platform was discontinued and the code open-sourced. whylogs ("open standard for privacy-preserving data logging") and LangKit remain OSS — [GeekWire](https://www.geekwire.com/2025/founders-at-seattle-startup-whylabs-join-apple-following-under-the-radar-acquisition); [appsecsanta](https://appsecsanta.com/whylabs)
- **Evidently (classic and LLM):** 20+ statistical drift tests and distance metrics; `DataDriftPreset(method="psi")` selects PSI; LLM descriptors and judges; a self-hosted monitoring UI or Evidently Cloud with alerting — [evidentlyai/evidently](https://github.com/evidentlyai/evidently)
- **MLflow** also covers trace cost tracking (3.10), automatic issue detection (3.11), trace archival (3.13) and daily trace-analytics rollups (3.17) — [MLflow CHANGELOG](https://raw.githubusercontent.com/mlflow/mlflow/master/CHANGELOG.md)
- **Metrics LaunchDarkly auto-collects** for AI configs: positive and negative feedback, tokens in and out, latency, completion error and success rates — [LaunchDarkly changelog](https://launchdarkly.com/changelog/guarded-rollouts-for-ai-configs/)

### Inferences
- **Metrics to track for LLM systems** (synthesis from the OTel metrics above plus vendor defaults):
  - **Latency:** end-to-end and per-span; TTFT and time per output token for streaming; tool latency.
  - **Volume and cost:** input, output, cached and reasoning tokens; cost per request, user or feature; budget burn (MLflow gateway budgets).
  - **Reliability:** error rate by `error.type`, provider rate limits and fallbacks, finish reasons (length or content-filter truncations).
  - **Agent behavior:** inference calls and tool calls per invocation (loop detection), steps to completion.
  - **Quality:** online judge scores emitted as `gen_ai.evaluation.result`, user feedback (thumbs, edits, escalations), guardrail triggers.
  - **Retrieval:** top_k, empty-retrieval rate, retrieval eval scores.
- **Classic ML monitoring** remains feature and prediction drift (PSI, KS, chi-square, Wasserstein, JS), data quality, and delayed-label performance. Concept drift (P(y|x) changes) can only be confirmed with labels or proxies.
- Because the conventions are Development status and renames are still happening (e.g., `gen_ai.client.token.usage` → `gen_ai.client.inference.usage.*` counters), pin instrumentation library versions and expect dashboard breakage on upgrades.

### Gaps
- **PSI and KS details** could not be verified this session. [UNVERIFIED-BACKGROUND]
  - PSI = Σ (actual% − expected%) · ln(actual% / expected%) over bins. Common rule of thumb: < 0.1 no significant shift, 0.1–0.25 moderate, > 0.25 significant.
  - The two-sample KS statistic is the maximum distance between empirical CDFs and suits numerical features. Chi-square suits categoricals.
  - Evidently's documented default switches by dataset size: KS or chi-square for small samples (≤1,000 rows), and Wasserstein or Jensen-Shannon distance for larger ones.
- **Fiddler** and **Arize AX** 2026 feature and status details were not retrieved.
- [UNVERIFIED-BACKGROUND] CoreWeave acquired Weights & Biases (announced March 2025, closed around May 2025). The Weave README did not mention it.
- LangSmith's self-hosting and OTel ingestion status and 2026 product changes were not covered by the fetched README.
- [UNVERIFIED-BACKGROUND] `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` is the env var instrumentations use to emit the latest experimental GenAI conventions. It was not confirmed in the fetched docs.

---

## 7. Evaluation: offline evals, golden datasets, LLM-as-judge (and its biases), RAG metrics (RAGAS), agent evals, online evals, prompt regression testing; tools

### Takeaway
Practitioner consensus in 2026:
- Start from **error analysis on real traces** and build a small, unambiguous task set (about 20–50 tasks from real failures).
- Prefer **code-based graders**, using **binary pass/fail** LLM judges that each target **one failure mode** and are calibrated against human labels (TPR/TNR).
- Run multiple trials, reporting **pass@k vs pass^k**.
- Layer offline CI evals with online judges, A/B tests and transcript review.

Tooling: promptfoo (now OpenAI), DeepEval, RAGAS, Inspect (UK AISI), the OpenAI Evals API, Braintrust, and MLflow, Langfuse, Phoenix and LangSmith evals.

### Cited Findings
**Anthropic, "Demystifying evals for AI agents" (Jan 9, 2026)** — [Anthropic Engineering](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- **Vocabulary:**
  - **task:** a test with defined inputs and success criteria
  - **trial:** one attempt at a task
  - **grader:** logic that scores one aspect of performance
  - **transcript:** the full record of a trial
  - **outcome:** the final environment state, e.g., whether the reservation exists in the DB, not whether the agent said it booked one
  - **eval harness:** the infrastructure that runs evals
  - **agent harness / scaffold:** the system that lets a model act as an agent
  - **eval suite:** a collection of related tasks
- **Grader types:**
  - **Code-based:** string match, unit tests, static analysis, tool-call and outcome checks. Fast, cheap and reproducible, but brittle.
  - **Model-based:** rubrics, natural-language assertions, pairwise comparison, multi-judge. Flexible, but non-deterministic, costlier, and in need of calibration.
  - **Human:** gold standard, but slow and expensive.
- **pass@k vs pass^k:**
  - pass@k is the probability of at least one success in k trials, and rises with k.
  - pass^k is the probability that all k trials succeed, and falls with k. For example, 75% per trial over 3 trials gives about 42%.
  - Use pass^k for customer-facing consistency.
- **Practices:**
  - Start with 20–50 tasks drawn from real failures, and turn bug reports and support tickets into tasks.
  - Two experts should agree on each verdict, and every task needs a reference solution.
  - Near-0% pass rates usually mean a broken task or grader.
  - Balance positive and negative cases.
  - Run each trial in a clean, isolated environment.
  - **Grade outcomes, not paths.** Give partial credit for multi-part tasks.
  - Calibrate LLM judges against human experts. Give judges an "Unknown" option, and use one judge per dimension.
  - Read transcripts regularly, and watch for saturation.
- **Domain guidance:**
  - **Coding agents:** deterministic tests (SWE-bench Verified, Terminal-Bench).
  - **Conversational agents:** state checks, turn limits, LLM tone rubrics and a simulated user (τ-Bench, τ2-Bench).
  - **Research agents:** groundedness, coverage and source quality (BrowseComp).
  - **Computer-use agents:** URL, page and backend state (WebArena, OSWorld).
- **Layered "Swiss cheese" model:** automated evals in CI, production monitoring, A/B tests, user feedback, transcript review, and periodic human studies.
- **Frameworks named:** Harbor, Braintrust, LangSmith, Langfuse, Arize (Phoenix/AX).

**Hamel Husain's methodology** (his `evals-skills` repo; README fetched; numbers come from mirrored skill files)
- Skills: eval-audit, error-analysis, generate-synthetic-data (tuples across dimensions), write-judge-prompt, validate-evaluator (calibrate judges against human labels using data splits, **TPR/TNR** and bias correction), evaluate-rag, and build-review-interface.
- The repo was **archived Aug 16, 2026** and moved to `ai-evals-course/evals-skills`.
- Source: [hamelsmu/evals-skills](https://github.com/hamelsmu/evals-skills)
- Mirrored skill content:
  - **Avoid Likert scales and letter grades** in favor of **binary pass/fail**.
  - **One failure mode per judge**, with explicit definitions and few-shot examples.
  - **Exhaust code-based checks first.**
  - Do error analysis before writing judges.
  - About **100 traces** for error-analysis saturation.
  - Judge validation needs **about 50 pass and 50 fail** labeled examples, though another skill says at least 20/20, so the numbers are inconsistent.
  - Sources: [tessl mirror: eval-audit](https://tessl.io/registry/skills/github/hamelsmu/evals-skills/eval-audit); [skillselion mirror: write-judge-prompt](https://skillselion.com/skills/hamelsmu/evals-skills/write-judge-prompt)

**LLM-as-judge biases** — Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (NeurIPS 2023; older but foundational) — [arXiv 2306.05685](https://arxiv.org/abs/2306.05685)
- Names **position bias**, **verbosity bias**, **self-enhancement bias** and limited reasoning ability.
- GPT-4 as judge reaches **>80% agreement** with human preferences, matching human-human agreement.
- GPT-4's swap-consistency under the default prompt was **65.0%**. Weaker judges (Claude-v1, GPT-3.5) showed strong first-position preference.
- Mitigations: swap answer order and call disagreements a tie; few-shot examples; reference-guided grading.
- Secondary summary: [memx.app](https://memx.app/blog/llm-as-a-judge-biases-and-fixes/)
- Judge-calibration tooling shipped in MLflow: `make_judge` (3.4), Judge Builder UI and the MemAlign optimizer (3.9), `judge.align()` defaulting to MemAlign (3.13), and `generate_rationale_first` (3.16) — [MLflow CHANGELOG](https://raw.githubusercontent.com/mlflow/mlflow/master/CHANGELOG.md); [MLflow releases](https://github.com/mlflow/mlflow/releases)

**RAG metrics (RAGAS)**
- The repo is now under the **vibrantlabsai** GitHub organization (Apache-2.0). It offers test-set generation and integrates with LangChain and observability tools — [Ragas repo](https://github.com/explodinggradients/ragas)
- **Faithfulness** = (response claims supported by the retrieved context) / (total response claims), on a 0–1 scale.
  - Steps: extract claims from the response, then verify each against the context.
  - Inputs: `user_input`, `response`, `retrieved_contexts`.
  - Variant `FaithfulnesswithHHEM` uses Vectara's HHEM-2.1-Open T5 classifier instead of an LLM for verification.
  - The legacy `SingleTurnSample` API was deprecated in 0.4 and will be removed in 1.0.
  - Source: [ragas faithfulness.md](https://raw.githubusercontent.com/vibrantlabsai/ragas/main/docs/concepts/metrics/available_metrics/faithfulness.md)
- **Context Precision@K** = Σₖ (Precision@k × vₖ) / (number of relevant items in the top K), where vₖ is 1 if the chunk at rank k is relevant.
  - This rewards ranking relevant chunks first.
  - Variants: LLM-based with reference, LLM-based without reference (`ContextUtilization`, judged against the response), non-LLM (string similarity against reference contexts, e.g., Levenshtein via `rapidfuzz`), and ID-based (retrieved IDs found in reference IDs / total retrieved IDs).
  - Source: [ragas context_precision.md](https://raw.githubusercontent.com/vibrantlabsai/ragas/main/docs/concepts/metrics/available_metrics/context_precision.md)
- **Context Recall** = (reference claims attributable to the retrieved contexts) / (total reference claims). The LLM-based version uses the reference answer as a stand-in for annotated reference contexts. Non-LLM and ID-based variants divide matched reference contexts or IDs by the total — [ragas context_recall.md](https://raw.githubusercontent.com/vibrantlabsai/ragas/main/docs/concepts/metrics/available_metrics/context_recall.md)
- **Full metric catalogue** — [ragas metrics index](https://raw.githubusercontent.com/vibrantlabsai/ragas/main/docs/concepts/metrics/available_metrics/index.md):
  - **RAG:** Context Precision, Context Recall, Context Entities Recall, Noise Sensitivity, Response Relevancy, Faithfulness, multimodal variants
  - **NVIDIA metrics:** Answer Accuracy, Context Relevance, Response Groundedness
  - **Agents:** Topic Adherence, Tool Call Accuracy, Tool Call F1, Agent Goal Accuracy
  - **NL comparison:** Factual Correctness, Semantic Similarity, BLEU, CHRF, ROUGE, Exact Match
  - **SQL:** Datacompy execution score, SQL Query Equivalence
  - **General:** Aspect Critic, Rubrics-Based Scoring, Instance-Specific Rubrics
  - **Other:** Summarization

**Evaluation tools**
- **promptfoo:**
  - A CLI and library (`npx promptfoo@latest`, `promptfoo eval`, `promptfoo view`) for evals and red teaming, with side-by-side model comparison and CI/CD integration. MIT-licensed, about 26k GitHub stars.
  - The repo now says "**Promptfoo is now part of OpenAI**" and remains open source and MIT — [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo)
  - OpenAI announced the acquisition on **Mar 9, 2026**, to fold the technology into **OpenAI Frontier** (its agent platform) for automated red-teaming, security evaluation of agentic workflows, and risk and compliance monitoring. Promptfoo says more than 25% of the Fortune 500 use it. Terms were undisclosed — [OpenAI](https://openai.com/blog/openai-to-acquire-promptfoo); [Security Boulevard](https://securityboulevard.com/2026/03/openai-acquires-security-startup-promptfoo-to-fortify-ai-agents)
- **DeepEval (Confident AI):**
  - Pytest-style, run with `deepeval test run`, Apache 2.0.
  - **Custom metrics:** G-Eval, DAG.
  - **Agentic metrics:** Task Completion, Tool Correctness, Goal Accuracy, Step Efficiency, Plan Adherence and Plan Quality, Argument Correctness.
  - **RAG metrics:** Answer Relevancy, Faithfulness, Contextual Precision, Recall and Relevancy.
  - **Conversational metrics:** Knowledge Retention, Conversation Completeness, Turn Relevancy and Faithfulness, Role Adherence.
  - **Other:** Hallucination, Bias, Toxicity, JSON Correctness, MCP and multimodal metrics.
  - The Confident AI platform adds online evals and regression alerts — [confident-ai/deepeval](https://github.com/confident-ai/deepeval)
  - By default it uses gpt-4o to power its metrics — [deepeval.com](https://deepeval.com/integrations/models/openai)
- **Inspect (UK AI Security Institute):** an MIT-licensed LLM eval framework supporting prompt engineering, tool use, multi-turn dialog and model-graded evals, with "over 200 pre-built evaluations" (Inspect Evals). It is built from datasets, solvers, scorers, agents and sandboxes, and the sandboxing depends on Docker — [UKGovernmentBEIS/inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai); [beri.net summary](https://www.beri.net/learning/inspect-ai-evals-framework-docs)
- **OpenAI Evals API:**
  - An *eval* is a reusable definition of a data-source schema plus testing criteria (graders), executed as eval *runs*.
  - Grader types: string check, text similarity, score model and Python code.
  - OpenAI's graders doc reportedly says graders are being **deprecated** in the evals and fine-tuning workflows. Not verified; check the deprecations page.
  - Sources: [OpenAI graders guide](https://developers.openai.com/api/docs/guides/graders); [qaskills summary](https://qaskills.sh/blog/openai-evals-graders-complete-reference-2026)
- **Braintrust:** an AI evaluation and observability platform founded in 2023 by Ankur Goyal. Aggregators report an **$80M Series B in Feb 2026 led by ICONIQ at an $800M valuation**; one aggregator shows an outdated $400M figure — [simplify.jobs](https://simplify.jobs/c/Braintrust-AI); [trueup](https://trueup.io/co/braintrust-dev); [techstackipo (conflicting)](https://www.techstackipo.com/company/braintrust)
- **MLflow GenAI evaluation:**
  - `mlflow.genai.evaluate` with scorers and judges, open-sourced in 3.3.
  - Multi-turn evaluation (3.7) and conversation simulation with session-level scorers (3.10).
  - Online judges on production traces (3.9).
  - Immutable evaluation dataset versions and a `scorer_ensemble` primitive (3.15.2).
  - Regression testing with `@mlflow.test` (3.14).
  - Sources: [MLflow CHANGELOG](https://raw.githubusercontent.com/mlflow/mlflow/master/CHANGELOG.md); [MLflow releases](https://github.com/mlflow/mlflow/releases)
  - A third-party listing dates multi-turn conversation evaluation to 3.10 (Feb 2026). The official changelog shows multi-turn eval in 3.7 and simulation in 3.10 — [vantaige.io](https://vantaige.io/ai-tool/mlflow)

### Inferences
- **Recommended eval stack** (synthesis):
  1. **Error analysis on real traces:** open-code failures, cluster them into failure modes, then prioritize.
  2. **Golden dataset:** curated real and synthetic cases with reference answers, versioned immutably (MLflow eval datasets, Langfuse datasets, Phoenix datasets).
  3. **Graders:** code first, then per-failure-mode binary LLM judges validated on held-out human labels (TPR/TNR), then periodic human review.
  4. **CI regression gate:** promptfoo, DeepEval or `@mlflow.test` on each prompt, model or config change.
  5. **Online evals:** sampled production traces scored by the same judges and emitted as `gen_ai.evaluation.result`, feeding failures back into the dataset.
- **Judge bias mitigations** to remember:
  - **Position:** swap order and require both orders to agree.
  - **Verbosity:** length-controlled rubrics, or penalizing unnecessary length.
  - **Self-enhancement:** use a judge from a different model family than the generator.
  - Always calibrate against humans, and prefer binary verdicts with an "Unknown" escape hatch.
- **RAG eval split:** context precision and recall diagnose the retriever, while faithfulness and response relevancy diagnose the generator. Recall needs a reference answer; the precision variant without a reference (ContextUtilization) works on unlabeled production traffic.

### Gaps
- Eugene Yan's LLM-as-judge and eval writing was not retrieved (domain blocked; search did not surface it).
- Verbosity and self-enhancement bias magnitudes from Zheng et al. were not retrieved.
- OpenAI's grader deprecation timeline is unverified.
- Braintrust's product features (Loop, online scoring, playground) and its funding are from aggregators only.
- I could not confirm whether the OpenAI–Promptfoo deal has closed. The repo's "now part of OpenAI" suggests it has.

---

## 8. Prompt management and versioning

### Takeaway
Prompts are now first-class versioned artifacts, stored in a registry with versions and aliases or labels, fetched at runtime through cached SDKs, linked to traces and eval runs, and rolled out like feature flags. The main options: MLflow Prompt Registry (with GEPA/MemAlign-based optimization), Langfuse Prompt Management, Phoenix prompts, LangSmith, and LaunchDarkly AI Configs for flag-style targeting and guarded rollouts.

### Cited Findings
- **MLflow Prompt Registry:**
  - APIs live under `mlflow.genai.prompts` (since 3.1). The prompt text limit was raised to 100K characters (3.1.1).
  - A chat UI for the registry arrived in 3.5, an Experiment prompts UI in 3.7, and "prompt model configuration" in 3.8, which stores model settings with the prompt.
  - Prompt optimization: `mlflow.genai.optimize_prompt` (3.1) and GEPA optimization (3.5).
  - Source: [MLflow CHANGELOG](https://raw.githubusercontent.com/mlflow/mlflow/master/CHANGELOG.md)
  - The registry includes versioning, tracking and "prompt optimization … using evaluation feedback and labeled datasets" — [MLflow 3 docs](https://mlflow.org/docs/3.1.3/genai/mlflow-3)
- **Langfuse:** "centrally manage and version-control prompts, with server- and client-side caching so iteration adds no application latency". The playground can be opened directly from a bad trace — [langfuse/langfuse](https://github.com/langfuse/langfuse)
- **Arize Phoenix:** prompt management with version control, tagging, and experiment-based testing of prompt changes; a playground can replay traced LLM calls — [Arize-ai/phoenix](https://github.com/Arize-ai/phoenix)
- **LaunchDarkly AI Configs:**
  - A variation is a model plus messages plus parameters. Variations are updated at runtime without a redeploy and rolled out progressively.
  - Guarded rollouts auto-revert on metric regressions, and AI Versioning lets teams track, compare and revert configs.
  - Sources: [LaunchDarkly changelog](https://launchdarkly.com/changelog/guarded-rollouts-for-ai-configs/); [LaunchDarkly enterprise prompt management](https://launchdarkly.com/solutions/enterprise-prompt-management-tools/)
- **Version data alongside prompts:** MLflow 3.15.2 added immutable evaluation dataset versions, so a prompt version can be tied to a fixed eval-set version — [MLflow releases](https://github.com/mlflow/mlflow/releases)
- **Generic prompt "improvements" can hurt specific apps.** An arXiv paper (Jan 2026) argues for evaluation-driven iteration — [arXiv 2601.22025](https://arxiv.org/pdf/2601.22025). Only the title was seen in search results; the paper was not read.

### Inferences
- **Prompt lifecycle best practice** (synthesis):
  1. Store prompts outside code, as a template plus variables plus model config.
  2. Make every change a new immutable version.
  3. Promote by moving an alias or label (e.g., `production`, `staging`) rather than editing in place.
  4. The application fetches by alias and caches it. A label move is an instant rollback.
  5. Every trace records the prompt name and version, so failures can be sliced by version.
  6. CI runs the eval suite on any new version before the alias moves.
  7. Canary via a feature flag or gateway traffic split.
  8. Optimizers (GEPA, DSPy-style) propose versions, which still pass the same gates.
- Decide where prompts live (Git vs a registry vs flags). Git gives code review; registries and flags let non-engineers iterate without redeploys. Many teams sync registry versions back to Git for audit.

### Gaps
- Langfuse label semantics (the `production` and `latest` labels, the fetch-by-label API) could not be fetched (docs domain blocked; a guessed GitHub docs path returned 404). [UNVERIFIED-BACKGROUND] Langfuse prompts have versions plus labels. `production` is served by default, `latest` points to the newest version, and moving a label deploys or rolls back.
- [UNVERIFIED-BACKGROUND] Anthropic acquired Humanloop's team in Aug 2025 and the Humanloop platform was sunset. OpenAI acquired Statsig (experimentation and feature flags) in Sep 2025. Neither was verified this session.
- LangSmith Prompt Hub and PromptLayer 2026 specifics were not retrieved.

---

## 9. Workflow orchestration: Airflow, Prefect, Dagster, Kubeflow Pipelines, Argo Workflows, Metaflow, Step Functions, Vertex AI Pipelines, SageMaker Pipelines, Temporal

### Takeaway
Data and ML pipeline orchestrators are mature and on fast release trains: Airflow 3.3.2, Prefect 3.8.8, Dagster 1.13.26, KFP 2.17.2 on Argo Workflows 3.7/4.0, Argo Workflows 4.0. **Durable-execution engines** (Temporal) have become the pattern for long-running, failure-prone **agent workflows**. Temporal's OpenAI Agents SDK integration runs model calls as Activities, and is still in public preview.

### Cited Findings
**Apache Airflow** — [apache/airflow releases](https://github.com/apache/airflow/releases)
- Latest is **3.3.2 (Sep 17, 2026)**. Earlier: 3.3.1 (Aug 12, 2026), 3.3.0 (Jul 6, 2026), 3.2.2 (May 29, 2026), 3.2.1 (Apr 22, 2026).
- **3.3.0** features:
  - expanded **asset partitioning** (rollup, fan-out and fixed-key mappers; a runtime-assigned partition timetable)
  - a **task and asset state store** that persists key-value state across retries and runs
  - **pluggable retry policies**
  - an experimental **Coordinator layer for Java and Go tasks**
  - `rerun_with_latest_version`
  - a Deadlines page
- 3.3.1 records the pandas 3 class name for DataFrame XComs, so every component must be upgraded before pandas 3 reaches it.
- **Airflow 3.1.0 (2025-09-25)** (older):
  - **Human-in-the-loop (HITL) tasks** that pause in a deferred state for UI input
  - React plugin views
  - synchronous DAG execution
  - event-driven scheduling from SQS, Kafka and Redis
  - Sources: [Airflow 3.1.0 release notes](https://airflow.apache.org/docs/apache-airflow/3.1.0/release_notes.html); [Airflow Summit 2025 deck](https://airflowsummit.org/slides/2025/introducing-apache-airflow%c2%ae-3-%e2%80%93-the-next-evolution-in-orchestration.pdf)
- **Airflow 3** introduced native **DAG versioning**, which keeps historical structure and run history after tasks are removed. **Cloud Composer** supported Airflow 3.1 in preview in Jan 2026 — [Google Cloud blog](https://cloud.google.com/blog/products/data-analytics/cloud-composer-supports-apache-airflow-31)

**Prefect** — [PrefectHQ/prefect releases](https://github.com/PrefectHQ/prefect/releases)
- Latest stable is **3.8.8 (Oct 6, 2026)**, the last release supporting Python 3.10; later releases require 3.11 or newer.
- 3.8.7 (Sep 25, 2026) added a Docker worker `container_wait_timeout`.
- Nightly 3.8.9.dev builds continue.

**Dagster** — [dagster-io/dagster releases](https://github.com/dagster-io/dagster/releases)
- Latest is **1.13.26 (Oct 9, 2026)**.
- Breaking change: `dagster-dbt` no longer installs dbt-core by default; it is now the `dagster-dbt[dbt-core]` extra.
- Recent themes:
  - asset health and partition backfill semantics
  - **declarative automation** performance
  - **Components** and the `dg` CLI (`dg list envs`, `dg plus …`; `.yml` component files)
  - a Dagster+ **MCP server**
  - a Prefect integration in preview (1.13.22)

**Kubeflow Pipelines (KFP)**
- Latest is **2.17.2 (Sep 4)**.
- 2.17.0 (Jul 9) brought a Material UI v5 migration, an OpenAPI-generated client and Go 1.26.1.
- 2.16.0 (Feb 25) bumped Argo Workflows from 3.7.3 to 3.7.8.
- **2.15.0 (Nov 25) changed the default object store from MinIO to SeaweedFS** and required a DB index migration.
- Source: [kubeflow/pipelines releases](https://github.com/kubeflow/pipelines/releases)
- The KFP README lists its Argo Workflows dependency as **v3.7, v4.0** — [kubeflow/pipelines](https://github.com/kubeflow/pipelines)
- **Kubeflow 1.11** was released 2025-12-15 and bundles KFP 2.15.0. A third-party source says 1.11 rebranded the project as the "Kubeflow AI Reference Platform" — [Kubeflow 1.11 release page](https://www.kubeflow.org/docs/kubeflow-platform/releases/kubeflow-1.11); [stork.ai](https://www.stork.ai/en/kubeflow)

**Argo Workflows**
- **Argo Workflows 4.0** was announced around Feb 9, 2026, with "usability, security and performance improvements" (secondary repost) — [API Evangelist repost](https://blogs.apievangelist.com/blogs/argo-2026-02-09-argo-workflows-4-0/)

**Metaflow**
- A Python framework for AI and ML systems from prototype to production. It was originally developed at Netflix and is now supported by **Outerbounds**.
- It covers scaling across CPUs and GPUs (including gang-scheduled workloads), dependency management, experiment tracking and versioning, and "highly available production orchestrators".
- Source: [Netflix/metaflow](https://github.com/Netflix/metaflow)

**Temporal (durable agent workflows)**
- The **OpenAI Agents SDK integration** launched in **public preview on Jul 30, 2025**, Python first — [Temporal blog](https://temporal.io/blog/announcing-openai-agents-sdk-integration); [BusinessWire](https://www.businesswire.com/news/home/20250730783559/en/Temporal-and-OpenAI-Launch-Integration-for-Enterprises-Developing-Production-Agents)
- A durable agent needs three pieces: a Workflow that runs the agent, a Worker with the integration plugin, and a Client with the same plugin. In TypeScript, model calls run as **Activities** (retryable, recorded in history) — [Temporal docs](https://docs.temporal.io/develop/python/integrations/openai-agents)
- An **Apr 16, 2026** update extended the integration to **sandbox environments**, still in public preview. **Standalone Activities** went GA as a separate feature — [Temporal Python SDK changelog](https://temporal.io/change-log/product-area/python-sdk)
- I found no evidence the integration reached GA by Oct 2026.

**MLflow as a lightweight runner:** MLflow 3.5 added a "job execution backend" — [MLflow CHANGELOG](https://raw.githubusercontent.com/mlflow/mlflow/master/CHANGELOG.md)

### Inferences
- **Choosing an orchestrator** (synthesis):
  - **Airflow:** broad batch and ETL scheduling with a huge operator ecosystem and managed offerings (Composer, MWAA, Astronomer). Its 3.x asset partitioning, HITL tasks and state store make it increasingly usable for ML retraining and LLM batch jobs.
  - **Dagster:** asset-centric (software-defined assets), with strong lineage and dbt integration.
  - **Prefect:** Pythonic dynamic flows with low ceremony.
  - **KFP / Vertex AI Pipelines:** container-per-step ML pipelines with artifact lineage. Vertex AI Pipelines runs the KFP SDK and now lives under the Agent Platform "Models" menu.
  - **SageMaker Pipelines:** native to AWS, integrated with the SageMaker Model Registry.
  - **Argo Workflows:** Kubernetes-native DAGs, and KFP's engine.
  - **Metaflow:** data-scientist ergonomics, deploying to production orchestrators.
  - **Step Functions:** serverless state machines that glue AWS services together, including Bedrock and SageMaker calls.
  - **Temporal:** durable execution with arbitrarily long, stateful, retry-safe code. It fits agent loops with human approvals, long tool calls and crash recovery, which DAG schedulers handle poorly.
- **Two orchestration tiers in LLM systems:**
  - **Offline/batch:** eval runs, dataset curation, embedding and index rebuilds, fine-tuning, on Airflow, Dagster or KFP.
  - **Online/durable:** agent executions, on Temporal or similar durable-execution engines, or on agent runtimes inside cloud agent platforms.

### Gaps
- **AWS Step Functions, SageMaker Pipelines and Vertex AI Pipelines** 2026 specifics could not be retrieved (docs domains blocked, search budget exhausted). [UNVERIFIED-BACKGROUND]
  - SageMaker Pipelines steps include Processing, Training, Tuning, Model/RegisterModel, Condition, Transform, Lambda and others. The `@step` decorator converts Python functions into steps.
  - Step Functions has optimized integrations for SageMaker and Bedrock, and Distributed Map for large fan-out.
  - Vertex AI Pipelines runs KFP v2 and TFX pipelines serverlessly.
- The Argo Workflows 4.0 feature list and current Argo Workflows version are not verified from the primary release page.
- Prefect 3.x headline features (transactions, events/automations) and Metaflow's current version were not shown on the fetched pages.
- Other durable-execution options (Restate, DBOS, Inngest, AWS Lambda durable functions) were not researched.
