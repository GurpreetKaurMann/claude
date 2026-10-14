# Learning Path & Resources: Becoming a Cloud-Strong AI Engineer (state as of October 2026)

> Research method note: Research date 2026-10-14. The sandbox's egress proxy blocked direct fetches of most primary pages: aws.amazon.com, learn.microsoft.com, nvidia.com, cncf.io, huggingface.co, oreilly.com, stanford.edu and axialsearch.com all returned DNS/403 errors. For those domains, facts come from search-engine summaries of the primary pages, which are still linked below. Pages fetched directly and verified: cloud.google.com (PMLE and Gen AI Leader cert pages), and github.com (nanochat, Made With ML, aie-book, HF agents-course and mcp-course, CS336 assignment repo). The web-search budget ran out before every gap could be closed (see the Gaps sections).

---

## 1. Core cloud fundamentals that matter most for AI engineers (IAM, networking/VPC, storage, compute, billing) and best free resources per provider

### Takeaway
Job postings for ML platform and LLMOps roles explicitly ask engineers to provision clusters, storage and networking with IaC. That makes IAM, VPC networking, object storage, GPU compute quotas and billing controls the base layer. Every provider gives new accounts credits: AWS up to $200, GCP $300 for 90 days, Azure $200 for 30 days. Billing traps like EKS extended support, regional GKE clusters and spot evictions are part of what you need to learn.

### Cited Findings
**Why fundamentals matter (employer evidence)**
- ML platform/LLMOps postings expect engineers to "provision compute clusters (e.g., Azure Kubernetes Service, Azure Machine Learning compute), storage, and networking," and ask for "Solid Terraform expertise (IaC best practices, multi-env setups)" — [Dice LLMOps posting](https://www.dice.com/job-detail/92bc7960-ba8d-4a26-a144-0413768e1899); [Turing/Greenhouse posting](https://job-boards.greenhouse.io/turingportal/jobs/5537879004); [GulfTalent Senior MLOps](https://www.gulftalent.com/uae/jobs/senior-mlops-engineer-643631)
- In an analysis of 43,480 US AI-engineering postings (through July 2026), "cloud platforms" appeared in 55% of postings, second only to Python (62%) — [Axial Search market map](https://axialsearch.com/insights/ai-ml-engineering-jobs/)
- Google's Professional ML Engineer cert recommends "3+ years of industry experience, including 1+ year designing and managing solutions on Google Cloud". Cloud-platform fluency is treated as a prerequisite for ML roles — [Google Cloud PMLE page](https://cloud.google.com/learn/certification/machine-learning-engineer)

**Free tiers / credits (the "free resource" for hands-on fundamentals)**
- **AWS:** accounts opened after July 15, 2025 choose a Free plan or a Paid plan. Both start with a $100 credit, and onboarding tasks earn up to $100 more, for a $200 maximum. Credits expire 12 months after the account opens. Both plans include 30+ "always free" services. The old 12-month free tier applies only to accounts created before the change — [freetier.co 2026 comparison](https://freetier.co/articles/cloud-provider-free-tiers-2026); [InfoQ, Jul 2025](https://www.infoq.com/news/2025/07/aws-risk-free-account-credits/); [Rackspace AWS Free Tier explainer](https://spot.rackspace.com/blog/aws-free-tier). Conflict: one table ([agentdeals.dev](https://agentdeals.dev/cloud-free-tier-comparison-2026)) lists AWS as having no blanket credit.
- **Google Cloud:** a 90-day, $300 free trial plus an "Always Free" tier. Billing does not start automatically when the trial ends; you must activate a paid account — [freetier.co](https://freetier.co/articles/cloud-provider-free-tiers-2026)
- **Azure:** $200 credit for the first 30 days, 25+ always-free services, and selected services free for 12 months. When the credit ends, the subscription downgrades rather than charging the card — [freetier.co](https://freetier.co/articles/cloud-provider-free-tiers-2026); [InfoWorld free-tier comparison](https://www.infoworld.com/article/2255593/aws-vs-azure-vs-google-cloud-which-free-tier-is-best.html)
- **Free GPU notebooks:** Kaggle gives about 30 GPU-hours/week (P100 16GB or 2×T4) with 12-hour sessions, but the quota "floats" and is undocumented. Colab's free tier has no published quota. Lightning AI's free plan has 15 monthly credits, about 22 T4-hours/month — [gpuperhour free GPU roundup](https://gpuperhour.com/blog/free-cloud-gpus-and-credits); [AIMultiple](https://aimultiple.com/free-cloud-gpu); [Spheron free credits 2026](https://www.spheron.network/blog/free-gpu-cloud-credits-2026/)

**Billing lessons that surface in AI work (cited cost traps)**
- EKS control plane costs about $0.10/cluster-hour (about $73/month) on standard-support Kubernetes versions. On extended-support versions it jumps to about $0.60/cluster-hour (about $438/month). One source says $0.50 instead — [TechTarget EKS pricing](https://www.techtarget.com/it-infrastructure/tip/Break-down-the-Amazon-EKS-pricing-model); [Spendark, prices checked Jul 2026](https://spendark.com/compare/doks-vs-eks-vs-aks-vs-gke/); [PerfectScale](https://www.perfectscale.io/blog/managed-kubernetes-pricing)
- The GKE management fee is $0.10/cluster-hour. A $74.40 monthly credit per billing account offsets it, but the credit does not apply to regional Standard clusters or to node/compute SKUs — [Finout GKE pricing](https://www.finout.io/blog/gke-pricing-tiers)
- Spot discounts are roughly AWS ~57%, GCP 60–91%, Azure ~80%. A spot job without checkpoints that gets evicted mid-run "can end up costing more than an on-demand run" — aggregated GPU-pricing comparisons ([GPUnex 2026](https://www.gpunex.com/blog/cloud-gpu-pricing-comparison-2026); [Deploybase](https://deploybase.ai/articles/gpu-cloud-pricing-comparison))

**Provider product churn to know (affects study materials)**
- Google renamed Vertex AI to **Gemini Enterprise Agent Platform** at Cloud Next 2026, live April 22, 2026. Vertex AI Studio became Agent Studio, Model Garden stays Model Garden, and Agent Engine became Agent Runtime. Agent Builder was folded in, and old links redirect — [Wikipedia](https://en.wikipedia.org/wiki/Gemini_Enterprise_Agent_Platform); [Google release notes](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes); [HPCwire, Apr 23 2026](https://www.hpcwire.com/aiwire/2026/04/23/google-unveils-gemini-enterprise-agent-platform/); [THE Journal, May 2026](https://thejournal.com/articles/2026/05/04/google-announces-new-gemini-enterprise-agent-platform.aspx)
- Microsoft's AI-103 exam centers on "Python and Microsoft Foundry". Foundry is the current Azure AI app/agent platform name to study — [Microsoft Learn AI-103 page (via search)](https://learn.microsoft.com/credentials/certifications/exams/ai-103/)

### Inferences
- A sensible fundamentals order for AI engineers: IAM (roles/service accounts, least privilege for training jobs and buckets) → VPC (private subnets, NAT/egress, private endpoints to model APIs and object storage) → object storage (S3/GCS/Blob, for datasets and checkpoints) → GPU compute (instance families, quotas, spot) → billing (budgets/alerts, tagging, avoiding idle clusters). The ordering is my synthesis of what the postings and cost traps above punish.
- The rename churn (Vertex to Gemini Enterprise Agent Platform; Azure AI to Foundry) means study material from before mid-2026 will use stale product names. Learners should prefer exam guides and docs updated after April 2026.
- The cheapest way to practice fundamentals: one provider's credits for IaC/networking/IAM labs, plus Kaggle/Colab for GPU notebook work. Pay for hyperscaler GPU time only at the serving and training stages.

### Gaps
- Could not verify the current catalog and free status of **AWS Skill Builder**, **Google Cloud Skills Boost**, and **Microsoft Learn** learning paths (e.g., AWS Cloud Practitioner Essentials, Google "Cloud Digital Leader" path, Azure AZ-900 path). The search budget was exhausted and those domains were blocked. These are the standard free provider resources, but the writer should treat specifics as unverified.
- Could not confirm whether GPU quota is available on GCP/Azure free-trial accounts. Historically it was not, but this was not verified this session.
- No authoritative source found ranking which fundamentals topics matter most. The ordering above is an inference.

---

## 2. Certifications relevant to AI/cloud engineers — status, cost, difficulty, value (as of October 2026)

### Takeaway
2026 brought major churn. **Retired:** AWS ML Specialty (March 31, 2026), Microsoft AI-102 (June 30, 2026) and DP-100 (June 1, 2026). **Replaced/updated:** AWS MLA-C01 → MLA-C02 (English MLA-C01 closed Sept 28, 2026), Microsoft AI-900 → AI-901. **New:** AWS Generative AI Developer – Professional (AIP-C01, GA March 2026, $300), Microsoft AI-103 (Azure AI Apps and Agents Developer, beta), AI-300 (MLOps Engineer), NVIDIA NCP-AAI, CNCF CNPE. The Google PMLE ($200) and Gen AI Leader ($99) were refreshed for the Gemini Enterprise Agent Platform rename.

### Cited Findings

**Status table**

| Cert | Status Oct 2026 | Cost | Format / notes | Source |
|---|---|---|---|---|
| AWS Certified AI Practitioner (AIF-C01) | Active (foundational) | $100 | 65 Q, 90 min, pass 700/1000 (third-party sources) | [ResumeLens](https://www.resumelens.org/blog/aws/aws-certified-ai-practitioner); [itsourcecode](https://itsourcecode.com/cert-prep/aws-ai-practitioner-aif-c01/) |
| AWS Certified ML Engineer – Associate | **CHANGED:** MLA-C01 → **MLA-C02**. English MLA-C01 last day Sept 28, 2026; MLA-C02 beta registration (English) from Sept 1, 2026; MLA-C01 stays in JA/KO/zh-CN during beta; non-English MLA-C01 retirement reported as Jan 14, 2027 | MLA-C02 price not confirmed | Same 4 domains, revised task statements shifted toward GenAI (Bedrock, RAG, agentic AI). Sources conflict on beta delivery start: Sept 28 vs Sept 29 | [AWS blog: MLA-C02 updates](https://aws.amazon.com/blogs/training-and-certification/updates-to-aws-certified-machine-learning-engineer-associate-mla-c02/); [AWS Sept 2026 new offerings](https://aws.amazon.com/blogs/training-and-certification/september-2026-new-offerings/); [K21 Academy](https://k21academy.com/?p=347735); [Tutorials Dojo](https://tutorialsdojo.com/whats-new-with-the-aws-certified-machine-learning-engineer-associate-mla-c02-in-2026/) |
| AWS Certified ML – Specialty (MLS-C01) | **RETIRED.** Last exam day March 31, 2026; holders stay active 3 years from date earned | n/a | AWS lists AI Practitioner, MLA, Data Engineer – Associate and the new GenAI Developer – Pro as successors | [AWS MLS cert page](https://aws.amazon.com/certification/certified-machine-learning-specialty/); [AWS blog](https://aws.amazon.com/ko/blogs/training-and-certification/big-news-aws-expands-ai-certification-portfolio-and-updates-security-certification/); [CBT Nuggets](https://www.cbtnuggets.com/blog/technology/networking/aws-ml-specialty-cert-retirement) |
| AWS Certified Generative AI Developer – Professional (AIP-C01) | **NEW / GA.** Announced Oct 15, 2025; beta registration Nov 18, 2025 (beta $150, last beta day Mar 31, 2026); standard registration opened Mar 17, 2026 | $300 | 85 Q (MC/MR), about 204 min (beta); English, Japanese, Simplified Chinese; beta passers got an Early Adopter badge | [AWS blog (announcement)](https://aws.amazon.com/ko/blogs/training-and-certification/big-news-aws-expands-ai-certification-portfolio-and-updates-security-certification/); [AWS March 2026 offerings](https://aws.amazon.com/es/blogs/training-and-certification/march-2026-new-offerings/); [Digital Cloud Training](https://digitalcloud.training/the-new-aws-certified-generative-ai-developer-professional/) |
| Google Professional Machine Learning Engineer | Active; **updated** for Vertex AI → Gemini Enterprise Agent Platform and data/analytics stack changes | $200 | 2 h, 50–60 MC/MS Q, EN/JA, online or onsite; recommends 3+ yrs industry incl. 1+ yr GCP; six areas: low-code AI, data/model mgmt, scaling prototypes, serving/scaling, pipelines, monitoring; covers foundation models, prompt & context engineering, gen AI tuning/deploy/monitor | [Google Cloud PMLE page (fetched)](https://cloud.google.com/learn/certification/machine-learning-engineer) |
| Google Cloud Generative AI Leader | Active (non-technical/business); recently updated for branding changes | $99 (a limited-time 50% exam-code offer has run) | 90 min, 50–60 MCQ, EN/JA/ES/PT, valid 3 yrs, no prereqs; domains: gen AI fundamentals, Google Cloud gen AI offerings, output-improvement techniques, business strategy | [Google Cloud Gen AI Leader page (fetched)](https://cloud.google.com/learn/certification/generative-ai-leader); [Google offer page](https://cloud.google.com/resources/offers/north-america-gen-ai-certification) |
| Microsoft Azure AI Engineer Associate (AI-102) | **RETIRED** June 30, 2026 (exam and renewals) | n/a | Successor is AI-103, a new exam rather than a renamed AI-102 | [DEV Community](https://dev.to/victoria_meisel_d65e0bad3/ai-103-replaces-ai-102-microsofts-new-azure-ai-certification-path-explained-16la); [Vlad Talks Tech](https://vladtalkstech.com/microsoft-learning-and-credential-news/microsoft-certification-retirements-2026/); [Pearson VUE MS updates](https://www.pearsonvue.com/us/en/microsoft/updates.html) |
| **AI-103: Developing AI Apps and Agents on Azure** → *Microsoft Certified: Azure AI Apps and Agents Developer Associate* | **NEW, beta** (mid-2026). One prep site claims it goes GA as "AI-200" (unverified) | Conflicting: $165 / about $99 / €126 / £106 | Associate, pass 700; 40–60 Q; 100 or 120 min (conflict); Python + Microsoft Foundry; generative & agentic solutions weighted 30–35% (Global Knowledge) or 35–40% (prep site); also vision, text analysis, info extraction | [Microsoft Learn AI-103 (via search)](https://learn.microsoft.com/credentials/certifications/exams/ai-103/); [Global Knowledge](https://www.globalknowledge.com/en-be/products/microsoft/ai-103); [aguidetocloud](https://www.aguidetocloud.com/cert-tracker/ai-103); [MSCertQuiz](https://mscertquiz.com/blog/ai-103-study-guide) |
| Microsoft DP-100 (Azure Data Scientist) | **RETIRED** June 1, 2026 → **AI-300: MLOps Engineer Associate** (MLOps + GenAIOps) | not found | — | [Vlad Talks Tech](https://vladtalkstech.com/microsoft-learning-and-credential-news/microsoft-certification-retirements-2026/); [Whizlabs](https://www.whizlabs.com/blog/microsofts-next-generation-ai-certifications/) |
| Microsoft AI-900 (AI Fundamentals) | **Version change:** AI-900 exam retired June 30, 2026 → **AI-901** (credential continues, now includes gen AI) | not found | — | [Vlad Talks Tech](https://vladtalkstech.com/microsoft-learning-and-credential-news/microsoft-certification-retirements-2026/); [Whizlabs](https://www.whizlabs.com/blog/microsofts-next-generation-ai-certifications/) |
| Microsoft AB-100 (Agentic AI Business Solutions Architect Expert) | New, expert-level; recommended forward path for retiring PL-600, though not one-to-one; "recognition still forming" | not found | — | [Vlad Talks Tech](https://vladtalkstech.com/microsoft-learning-and-credential-news/microsoft-certification-retirements-2026/); [Citizen Development Academy](https://citizendevelopmentacademy.com/ai-solution-architect-certification-path/) |
| NVIDIA NCA-GENL (Gen AI LLMs Associate) | Active | $125 most cited ($135 and about $150 also reported) | Valid 2 yrs | [FlashGenius cost breakdown](https://flashgenius.net/blog-article/nvidia-certification-cost-2026-exam-fees-renewal-costs-full-pricing-breakdown); [PassITExams](https://passitexams.com/articles/nvidia-certification-cost/); [CertDemand](https://certdemand.com/certs/nvidia-nca-genl) |
| NVIDIA NCP-GENL (Gen AI LLMs Professional) | Active | $200 | Valid 2 yrs | [FlashGenius](https://flashgenius.net/blog-article/nvidia-certification-cost-2026-exam-fees-renewal-costs-full-pricing-breakdown); [PassITExams](https://passitexams.com/articles/nvidia-certification-cost/) |
| NVIDIA NCP-AAI (Agentic AI Professional) | Listed by NVIDIA (one NVIDIA page still says "coming soon") | $200 | 60–70 Q, 120 min, remote-proctored via Certiverse; suggests 1–2 yrs AI/ML plus production agentic projects; topics include multi-agent design, RAG, evaluation, deployment, monitoring, safety, NVIDIA platform | [NVIDIA NCP-AAI page](https://nvidia.com/en-us/learn/certification/agentic-ai-professional); [Ascendient](https://www.ascendientlearning.com/certification/nvidia/337/nvidia-certified-professional-agentic-ai-ncp-aai); [Whizlabs NCP-AAI guide](https://www.whizlabs.com/blog/ncp-aai-guide/) |
| NVIDIA AI Infrastructure (NCP-AII) / AI Ops | NVIDIA webinar previews hands-on portions of professional exams launching in 2026; no format/price details found | not found | — | [NVIDIA certification hub](https://www.nvidia.com/certification) |
| CNCF CKA / CKAD / CKS | Active | $445 (raised from $395; announced Dec 19, 2024); frequent promos of 35–40% off | Performance-based | [Sailor.sh CKA cost 2026](https://www.sailor.sh/blog/cka-certification-cost-2026); [MacMyths LF pricing](https://macmyths.com/new-certification-pricing-cka-ckad-cks-and-lfcs-costs-explained/) |
| CNCF KCNA / KCSA | Active (entry level, multiple choice) | $250 each (KCNA course+exam bundle $299) | KCSA: 90 min, 60 Q, 75% pass, valid 24 months | [Splunk K8s certs](https://www.splunk.com/en_us/blog/learn/kubernetes-certifications?p=3); [MentorCruise](https://mentorcruise.com/certifications/kubernetes) |
| Kubestronaut bundle (KCNA+KCSA+CKA+CKAD+CKS) | Active | $1,645 regular | — | [Kubestronaut roadmap, Jul 2026](https://www.youngju.dev/blog/culture/2026-07-02-how-to-become-kubestronaut-cncf-cka-ckad-cks-kcna-kcsa-roadmap-deep-dive.en) |
| CNCF CNPE (Certified Cloud Native Platform Engineer) | **NEW.** Launched Nov 11, 2025 at KubeCon NA (Atlanta) | $445 (one community guide says $395) | Performance-based in a remote Linux desktop; 12-month eligibility, one retake. A CNPA associate-level exam also exists | [CNCF CNPE page](https://www.cncf.io/training/certification/cnpe/); [Linux Foundation announcement](https://training.linuxfoundation.org/?p=40977); [DataCentreNews](https://datacentrenews.uk/story/cncf-launches-new-certification-for-cloud-native-engineers); [CNCF CNPA page](https://www.cncf.io/training/certification/cnpa/) |

**Value / difficulty signals**
- CBT Nuggets says AIP-C01 is not a direct replacement for MLS-C01 and is "focusing more on current in-demand skills". AWS frames it as a successor. Sources disagree on how direct the succession is — [CBT Nuggets](https://www.cbtnuggets.com/blog/training/certification-paths/tech-news-generative-ai-developer-cert)
- PMLE "does not directly assess coding", though Python/SQL proficiency helps with code snippets in questions — [Google Cloud PMLE page](https://cloud.google.com/learn/certification/machine-learning-engineer)
- Gen AI Leader is "for anyone in any job role, with or without hands-on technical experience". It is a business/literacy credential, not an engineering one — [Google Cloud Gen AI Leader page](https://cloud.google.com/learn/certification/generative-ai-leader)
- For NCP-AAI, one commentator says official NVIDIA resources (study guide/blueprint, DLI courseware) are the main anchor, and the third-party prep ecosystem is "less mature" — [Rick High Substack](https://rickhigh.substack.com/p/the-agentic-ai-certification-landscape)
- One article title says four AI certs the author researched "had already been retired", which shows how much churn there is — [AI in Plain English](https://ai.plainenglish.io/i-spent-a-weekend-figuring-out-which-ai-certs-are-worth-it-four-had-already-been-retired-122fc2f0f966)

### Inferences
- **Recommended cert sequence for a cloud-strong AI engineer (my synthesis):**
  1. Optional foundational cert: AWS AIF-C01 ($100), AI-901, or Google Gen AI Leader ($99).
  2. KCNA ($250) for Kubernetes vocabulary.
  3. One provider's ML associate: AWS MLA-C02 or Azure AI-103.
  4. CKA or CKAD ($445) for real k8s/GPU platform work.
  5. A professional cert: AWS AIP-C01 ($300), Google PMLE ($200), or NVIDIA NCP-GENL/NCP-AAI ($200).
  6. CNPE ($445) for ML-platform specialists.
- Performance-based CNCF exams (CKA/CKAD/CKS/CNPE) are probably a stronger skill signal than multiple-choice cloud AI exams, because they require hands-on terminal work. This is inferred from the format, not from employer survey data.
- Given the churn, learners should check exam codes against the official pages right before booking. Many prep resources still target MLS-C01, MLA-C01, AI-102 or DP-100.

### Gaps
- MLA-C02 standard price and GA date are not confirmed. MLA-C01 was historically $150 (associate tier), but this was not verified this session.
- AI-103 price, duration and final GA exam code are conflicting or unverified. The "AI-200" GA claim comes from a single prep site.
- No official NVIDIA page was directly retrieved. NCA-GENL/NCP-GENL question counts, durations and the full current NVIDIA catalog (AI Infrastructure, AI Operations, Multimodal) are unverified.
- AI-300 and AI-901 prices and skills outlines were not found.
- No employer-survey data was found on how much hiring managers value each cert. Value judgments above are inferences.
- Could not check whether Google launched any new 2026 AI/agent engineering certification beyond PMLE and Gen AI Leader. The fetch of the full Google cert catalog returned truncated content.

---

## 3. Well-regarded courses and books (status and what each is good for)

### Takeaway
The core free/low-cost curriculum in 2026 is Chip Huyen's two books (DMLS for classic ML systems, *AI Engineering* for foundation-model apps and evals), Made With ML (production MLOps with Ray/MLflow), the Hugging Face LLM, Agents and MCP courses (free), and for depth Karpathy's Zero to Hero and nanochat. Stanford CS336 (with Spring 2026 lectures online) and HF's Ultra-Scale Playbook cover pretraining and distributed training. fast.ai remains a practice-first DL option. Full Stack Deep Learning's latest material is from 2022.

### Cited Findings
**Books**
- *AI Engineering: Building Applications with Foundation Models* (Chip Huyen, O'Reilly): published Dec 2024 per O'Reilly (the GitHub citation says 2025), 534 pages, intermediate-to-advanced. It "builds upon and is complementary to" *Designing Machine Learning Systems* — [O'Reilly listing](https://www.oreilly.com/library/view/-/9781098166298/)
- Topics in *AI Engineering*: whether to build an AI app, evaluation including AI-as-judge, hallucinations, prompt engineering, context construction, RAG, agents, finetuning including PEFT, data quality/quantity, latency/cost/security optimization, and feedback loops. The companion repo has the TOC, chapter summaries, study notes and a resources list. DMLS covers traditional ML, *AI Engineering* covers foundation models, and "real systems often use both" — [chiphuyen/aie-book (fetched)](https://github.com/chiphuyen/aie-book)
- Reviews: praised for focusing on concepts over fast-changing tools, with the evaluation chapters singled out. Some say it is dense or dry and math sections need supplemental reading — [Javarevisited/Medium review](https://medium.com/javarevisited/review-is-ai-engineering-book-by-chip-huyen-worth-it-61e5f435e8ac); [Mark Ferree review](https://markferree.substack.com/p/ai-engineering-book-review); [Scott Pearson](https://scottjpearson.substack.com/p/ai-engineering-building-applications)

**MLOps / production courses**
- **Made With ML** (Goku Mohandas): open-source, MIT-licensed course and codebase on designing, developing, deploying and iterating on production ML. Topics: training/tuning/eval/serving, testing, CI/CD with GitHub Actions, experiment tracking, orchestration, continual learning. Tools: Ray (data/train/tune/Serve), MLflow, Anyscale, KubeRay, S3. The example compute config uses g5.4xlarge. About 49.7k GitHub stars — [Made-With-ML repo (fetched)](https://github.com/GokuMohandas/Made-With-ML)
- **Full Stack Deep Learning:** the archived 2022 course says "all the lecture and lab material is free forever". No newer iteration was confirmed. It covers the full ML lifecycle from problem definition to deployment and continual learning — [AITopics FSDL tag](https://aitopics.org/tag/full%20stack%20deep%20learning); [G2 profile](https://www.g2.com/sellers/fullstackdeeplearning-com)
- **fast.ai:** 2026 review estimates the full course at about 70–100 hours over 2–4 months for beginners with strong programming. It is commonly paired with Andrew Ng's courses for foundations — [AIAgentRank fast.ai review 2026](https://aiagentrank.io/blog/fast-ai-review-2026); [AIAgentRank best AI courses 2026](https://aiagentrank.io/blog/best-ai-courses-2026)

**Hugging Face (free)**
- **LLM Course:** free, about 12 chapters from transformers to fine-tuning — [KDnuggets](https://www.kdnuggets.com/5-free-ai-courses-from-hugging-face)
- **Agents Course:** free, Apache-2.0.
  - Unit 1: agent fundamentals, plus a bonus on fine-tuning for function-calling.
  - Unit 2: frameworks (smolagents, LlamaIndex, LangGraph), plus a bonus on observability and evaluation.
  - Unit 3: agentic RAG.
  - Unit 4: final project, benchmark and leaderboard, and certification.
  - Prereqs: basic Python and basic LLM knowledge — [huggingface/agents-course (fetched)](https://github.com/huggingface/agents-course). Estimated 20–30 hrs per a review site — [AIAgentRank](https://aiagentrank.io/learn/provider/huggingface)
- **MCP Course:** free, "built in partnership with Anthropic".
  - Units: intro to MCP, building MCP clients and servers with SDKs, advanced features/architecture, and bonus partner units.
  - Prereqs: basic AI/LLM knowledge, API concepts, and one language (Python/TypeScript emphasized).
  - About 10–15 hrs (third-party estimate) — [HF MCP course intro](https://huggingface.co/learn/mcp-course/en/unit0/introduction); [huggingface/mcp-course (fetched)](https://github.com/huggingface/mcp-course); [AIAgentRank MCP course](https://aiagentrank.io/learn/course/huggingface-mcp-course)
- DeepLearning.AI offers a competing MCP short course, "MCP: Build Rich-Context AI Apps/Agents" (with Anthropic) — [AIAgentRank comparison](https://aiagentrank.io/learn/compare/deeplearning-ai-mcp-build-rich-context-agents-vs-huggingface-mcp-course)

**Distributed training / from-scratch depth**
- **Ultra-Scale Playbook** (Hugging Face/nanotron, released about Feb–Mar 2025, free):
  - Takes readers from single-GPU training to thousands of GPUs.
  - Covers data, tensor, pipeline and context parallelism, ZeRO, and kernel fusion.
  - Based on 4,000+ scaling experiments (about 4,100 distributed runs, 16k+ including tests) on up to 512 GPUs.
  - The authors stress that the best config depends on hardware and interconnect, so the book offers a benchmarking method rather than a single recipe.
  - Sources: [Ultra-Scale Playbook](https://nanotron-ultrascale-playbook.static.hf.space/); [InfoQ, Mar 2025](https://www.infoq.com/news/2025/03/huggingface-ultra-scale-playbook); [HF Space source](https://huggingface.co/spaces/nanotron/ultrascale-playbook/blob/main/ultra_blog.md)
- **Stanford CS336 Language Modeling from Scratch** (Tatsunori Hashimoto and Percy Liang):
  - A Spring 2026 offering exists, and lecture videos ("Spring 2026 | Lecture N") are on Stanford Online's YouTube.
  - Topics seen in listings include tokenization, parallelism, inference (Lecture 10), data (Lecture 14), and post-training/RLVR (Lecture 16).
  - The aggregator listings were somewhat inconsistent — [Latent Space CS336](https://news.latent.space/topic/language-modeling); [lecture listing aggregator](https://summify.io/discover/stanford-cs336-language-modeling-from-scratch-spring-2026-le-JuoVZk/)
  - Public assignment repos exist. Assignment 1 "Basics" (Spring 2025) uses TinyStories and OpenWebText and is test-driven via `tests/adapters.py` — [stanford-cs336/assignment1-basics (fetched)](https://github.com/stanford-cs336/assignment1-basics)
- **Karpathy:**
  - *Neural Networks: Zero to Hero* is about 19 hours, from micrograd/backprop to building GPT from scratch, and is recommended as a starting point for newcomers — [CSDIY wiki](https://csdiy.wiki/en/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD/Neural%20Networks:%20Zero%20to%20Hero); [FutureAGI reading guide](https://futureagi.com/blog/large-language-model-training-books-2025/)
  - **nanochat** is "the simplest experimental harness for training LLMs". It covers tokenizer training, pretraining with CORE eval, SFT, RL, eval and a chat CLI/inference. A GPT-2-class model trains in about 2 hours on an 8×H100 node: about $48 at about $3/GPU-hr, or about $15 on spot. A single GPU works via gradient accumulation at about 8× the time, and there is a CPU/MPS mini-run — [karpathy/nanochat README (fetched)](https://github.com/karpathy/nanochat)
  - At its Oct 2025 launch, nanochat was billed as a "$100, 4-hour" ChatGPT clone on 8×H100 and as the planned capstone of Eureka Labs' LLM101n — [CXO Digital Pulse](https://www.cxodigitalpulse.com/andrej-karpathy-launches-nanochat-an-open-source-chatgpt-style-model-training-pipeline/). A community HF org hosts student notebooks and checkpoints — [nanochat-students](https://huggingface.co/nanochat-students)

### Inferences
- Suggested mapping to stages:
  - Fundamentals/DL: fast.ai or Karpathy Zero to Hero.
  - Classic ML systems: DMLS.
  - Production MLOps: Made With ML, plus FSDL 2022 for lifecycle concepts.
  - LLM apps/RAG/agents/evals: Huyen *AI Engineering*, HF LLM/Agents/MCP courses, DeepLearning.AI short courses.
  - Distributed training: Ultra-Scale Playbook, CS336, nanochat.
- nanochat's README cost has dropped from the $100 launch claim to about $48 on-demand or about $15 spot. That makes "train your own small LLM end to end" a realistic capstone at hobby budgets.

### Gaps
- *Hands-On Large Language Models* (Jay Alammar and Maarten Grootendorst, O'Reilly) could not be verified this session (O'Reilly blocked, search budget exhausted). Publication date, page count and content are unconfirmed here.
- Current DeepLearning.AI short-course catalog, pricing (historically free) and the 2026 additions were not verified.
- Made With ML's last content update date and the status of its paid cohort are unknown.
- Whether Full Stack Deep Learning has any post-2022 iteration (e.g., its 2023 LLM Bootcamp) was not confirmed.
- The LLM101n status (Eureka Labs) is unconfirmed.
- The official CS336 2026 syllabus and assignment list could not be fetched (stanford.edu blocked).

---

## 4. Staged learning path with hands-on project ideas, approximate cloud cost, and free-tier/credit options

### Takeaway
Six stages: fundamentals → containers/Kubernetes → model serving → RAG/agents → MLOps → distributed training. Almost all of it fits inside new-account credits plus free GPU notebooks. Fundamentals and RAG/agents projects cost close to $0. A serving lab on an L4/A10G-class GPU costs a few dollars per session. A LoRA fine-tune on a spot A100 costs single-digit dollars. A full nanochat speedrun on 8×H100 costs about $15 (spot) to about $48 (on-demand). The usual way to overspend is leaving a cluster or GPU node running.

### Cited Findings
**Reference prices used for project costing**
- H100 on-demand per GPU-hr (Sept 2026 comparison): RunPod $2.89, Vast.ai from $1.33, Lambda $3.29, AWS $6.88. Hyperscaler range is $3.00–$6.98; marketplaces $1.49–$2.50. AWS H100 spot is about $2.96/GPU-hr (p5.48xlarge) — [GPUnex 2026](https://www.gpunex.com/blog/cloud-gpu-pricing-comparison-2026); [Deploybase](https://deploybase.ai/articles/gpu-cloud-pricing-comparison); [Keenable H100 reality check](https://select.keenable.ai/r/nvidia-h100-cloud-cost-sticker-vs-real-effective-rate/BJgquDi6wKxZyFJssxeBDw)
- A100 80GB on-demand: $1.49/hr at Jarvislabs and RunPod Secure, $2.06 at Lambda, $3.43/GPU at AWS. RunPod spot from about $0.36/hr — [Jarvislabs A100 price 2026](https://docs.jarvislabs.ai/blog/a100-price)
- L40S: $0.92/hr (Hostinger), $0.99/hr (RunPod) as of Sept 2026 — [Hostinger GPU pricing 2026](https://www.hostinger.com/tutorials/?p=158956)
- L4 about $0.50–$1.20/hr and A10G about $0.75–$1.50/hr come from a low-authority source, with no reliable spot data — [Cyfuture](https://cyfuture.ai/kb/gpu/gpu-cloud-pricing)
- Managed k8s control planes: EKS about $0.10/hr; GKE $0.10/hr offset by a $74.40/month credit (zonal/Autopilot only) — [TechTarget](https://www.techtarget.com/it-infrastructure/tip/Break-down-the-Amazon-EKS-pricing-model); [Finout](https://www.finout.io/blog/gke-pricing-tiers)
- Credits: AWS up to $200, GCP $300/90 days, Azure $200/30 days; Kaggle about 30 GPU-hrs/week free — [freetier.co](https://freetier.co/articles/cloud-provider-free-tiers-2026); [gpuperhour](https://gpuperhour.com/blog/free-cloud-gpus-and-credits)

**Stage-by-stage resources and cited project anchors**
- **Stage 1 – Cloud & DL fundamentals:** provider credits for IAM/VPC/storage labs; fast.ai or Karpathy Zero to Hero for DL; free Kaggle/Colab GPUs. Certs: AIF-C01 / AI-901 / Gen AI Leader (optional). Sources as cited in sections 1–3.
- **Stage 2 – Containers & Kubernetes:** KCNA → CKA/CKAD. Postings ask for Docker, Kubernetes (GKE/AKS "preferred" in some) and Terraform — [Dice](https://www.dice.com/job-detail/92bc7960-ba8d-4a26-a144-0413768e1899); [Greenhouse/Turing](https://job-boards.greenhouse.io/turingportal/jobs/5537879004)
- **Stage 3 – Model serving:** postings name vLLM, SGLang, TGI, Triton and Ray Serve, "with attention to GPU utilization, latency, and throughput" — [Greenhouse/Turing posting](https://job-boards.greenhouse.io/turingportal/jobs/5537879004); [Dice](https://www.dice.com/job-detail/92bc7960-ba8d-4a26-a144-0413768e1899). CS336 has a dedicated inference lecture — [lecture aggregator](https://git.handmade.network/stanford-cs336-language-modeling-from-scratch-spring-2026-lecture-10-inference.html)
- **Stage 4 – RAG / agents / MCP:** Huyen *AI Engineering* (RAG, agents, AI-as-judge evals); HF Agents course (agentic RAG, observability/eval bonus); HF MCP course (build MCP servers/clients) — [aie-book](https://github.com/chiphuyen/aie-book); [agents-course](https://github.com/huggingface/agents-course); [mcp-course](https://github.com/huggingface/mcp-course). Certs: AWS AIP-C01, Azure AI-103, NVIDIA NCP-AAI.
- **Stage 5 – MLOps / LLMOps:** Made With ML (Ray, MLflow, CI/CD, KubeRay; example g5.4xlarge) — [Made-With-ML](https://github.com/GokuMohandas/Made-With-ML). Postings ask for monitoring, model versioning, drift detection, Prometheus/Grafana — [GulfTalent](https://www.gulftalent.com/uae/jobs/senior-mlops-engineer-643631). Certs: AWS MLA-C02, Microsoft AI-300, Google PMLE, CNCF CNPE.
- **Stage 6 – Distributed training:** Ultra-Scale Playbook (DP/TP/PP/CP, ZeRO); CS336 parallelism lectures; nanochat speedrun (about 2 hrs on 8×H100, about $48 on-demand / about $15 spot; single-GPU option at about 8× time) — [Ultra-Scale Playbook](https://nanotron-ultrascale-playbook.static.hf.space/); [nanochat](https://github.com/karpathy/nanochat). Postings ask for Ray/Kubeflow and "multi-GPU orchestration" — [CVBankas MLOps posting](https://www.cvbankas.lt/mlops-engineer-with-expertise-in-ray-and-kubeflow-vllm-skypikot-on-kubernetes-darbas-namuose/1-13742747). Cert: NVIDIA NCP-GENL.
- Spot caveat for stages 5–6: checkpoint, or eviction can make spot cost more than on-demand — [GPUnex](https://www.gpunex.com/blog/cloud-gpu-pricing-comparison-2026)

### Inferences
**Project menu with estimated costs.** These are my arithmetic using the cited prices; actual costs vary by region and provider.

| Stage | Project | Est. cost | Free/credit route |
|---|---|---|---|
| 1 | Terraform a VPC with private subnets, a least-privilege IAM role/service account, an encrypted bucket for datasets, plus a budget alert. Destroy and recreate it from code | about $0–5 (avoid NAT gateways and idle resources) | AWS $100–200 / GCP $300 / Azure $200 credits |
| 1 | Train a small classifier/char-level model (Karpathy makemore/GPT) on free GPUs | $0 | Kaggle (about 30 GPU-hr/wk), Colab |
| 2 | Containerize a FastAPI inference service (Docker), push it to a registry, deploy to a managed k8s cluster with HPA, then tear it down | GKE zonal/Autopilot mgmt fee covered by the $74.40 credit; EKS about $0.10/hr (about $0.40–1 for a 4–8 hr lab) plus small CPU nodes | GKE free-tier credit; provider credits |
| 2→3 | **Terraform an EKS/GKE GPU node pool** (one L4/A10G-class node, autoscale to zero, NVIDIA device plugin/GPU operator) | about $0.10/hr control plane + about $0.50–1.50/hr GPU node → about $3–10 for a 4–6 hr lab | Credits. GPU quota requests may need a paid upgrade (unverified) |
| 3 | **Deploy vLLM** serving an open 7–8B model on one L4/A10G/L40S. Benchmark throughput and latency (tokens/s, TTFT, p95) across batch sizes and quantization | L40S about $0.92–0.99/hr; L4 about $0.50–1.20/hr → about $2–6 per session | Marketplace GPUs (RunPod/Vast) are cheaper than hyperscalers; credits |
| 4 | **RAG app with an eval suite**: ingestion → vector DB → retrieval → generation, plus offline evals (retrieval recall, faithfulness, AI-as-judge) wired into CI | about $0–10, mostly LLM API tokens; local models on free GPUs to minimize | Kaggle/Colab for embeddings; free tiers of vector DBs (unverified) |
| 4 | **Build an MCP server** exposing a tool or data source, connect it to an agent (HF Agents/MCP course frameworks), add tracing/observability | about $0 (local) | HF courses are free |
| 5 | **LoRA/QLoRA fine-tune on spot instances** with checkpoint-resume to object storage; track with MLflow; register the model; deploy behind vLLM | A100 spot from about $0.36/hr or on-demand $1.49/hr → about $2–15 for 4–10 GPU-hrs | Kaggle T4s for QLoRA on small models: $0 |
| 5 | CI/CD for ML (GitHub Actions): data validation, training, eval gate, canary deploy; drift monitoring with Prometheus/Grafana (Made With ML pattern) | about $0–10 | GitHub free tier; credits |
| 6 | **nanochat speedrun** (tokenizer → pretrain → SFT → RL → eval) on 8×H100 | about $15 (spot) – about $48 (on-demand at $3/GPU-hr); AWS on-demand H100 at $6.88/GPU-hr would be about $110 for 2 hrs | Single-GPU run at about 8× time on a marketplace H100 ($1.33–2.89/hr) → about $21–46 |
| 6 | Reproduce Ultra-Scale Playbook experiments: compare DDP vs FSDP/ZeRO-3 vs TP on 2–8 GPUs, measuring MFU and memory | about $10–50 (a few hours on a 2–8 GPU marketplace node) | Start on 2×T4 Kaggle for DDP basics: $0 |

- Total for the whole path is plausibly under about $150–250 of out-of-pocket GPU spend if credits are used for the CPU/networking stages and marketplace GPUs for the GPU stages. Leaving resources idle is the biggest risk.
- Sequencing advice: do Stage 4 (RAG/agents) in parallel with Stage 2–3. It needs little cloud spend and maps most directly to the most common 2026 job asks (foundation models in 51% of postings).

### Gaps
- No reliable 2026 spot pricing was found for L4/A10G. The L4/A10G figures come from a low-authority source.
- The H100 per-provider figures (RunPod $2.89, Vast $1.33, Lambda $3.29, AWS $6.88; AWS spot $2.96) and the spot-discount percentages came via a search summary of several aggregator pages (GPUnex, Deploybase, Hostinger, Keenable). It is not certain which page holds each figure, and all are vendor or aggregator blogs, not provider price lists.
- Hyperscaler-specific per-instance prices (e.g., AWS g6.xlarge L4, GCP g2-standard-4) were not verified this session.
- Vector-DB and LLM-API free tiers were not researched (search budget exhausted).
- Whether new free-trial accounts get GPU quota on GCP/Azure/AWS is unverified. This affects whether credits can fund GPU projects.

---

## 5. Skills employers ask for in AI engineer / ML platform / LLMOps job postings (2025–2026)

### Takeaway
Postings are dominated by Python (62–71%), cloud platforms (55%; AWS ahead of Azure), and foundation-model/LLM work (51%). Premium skills are RAG, vector databases, fine-tuning (LoRA/QLoRA), agents and LLM evaluation. ML platform/LLMOps roles add inference-serving stacks (vLLM, SGLang, TGI, Triton, Ray Serve), Kubernetes with GPU orchestration, Terraform, CI/CD and observability. They typically want 3–7 years of experience. Market-size claims vary widely, so treat headline numbers as directional.

### Cited Findings
- **Axial Search** (43,480 US AI-engineering postings, through July 2026) — [Axial Search market map](https://axialsearch.com/insights/ai-ml-engineering-jobs/); [Axial Search AI engineering jobs](https://axialsearch.com/insights/ai-engineering-jobs); [Axial demand](https://axialsearch.com/insights/ai-engineering-job-demand):
  - Skill frequency: Python 62%, cloud platforms 55%, foundation models 51%, which the authors read as employers wanting breadth across the stack.
  - Hiring pace: about 1,550 new US AI-engineering roles/week, steady through H1 2026.
  - Who posts: professional services 28%, technology 24%, IT services 15%.
  - Seniority: IC-heavy, centered on people 3–7 years into their careers.
- **365 Data Science** (1,000 postings): Python required in 71%. Among cloud skills, one dataset reports AWS at 32.9% and Azure at 26% — [365 Data Science AI Engineer Job Outlook](https://365datascience.com/career-advice/career-guides/ai-engineer-job-outlook-2025/). (The AWS/Azure figures came via a search summary; I could not confirm which report contains them.)
- Fine-tuning LLMs, building RAG pipelines and working with vector databases "command a premium" — [Interview Query AI engineer demand](https://www.interviewquery.com/p/ai-engineers-demand)
- **ML platform/LLMOps postings** (small sample of about 8 listings, snapshot not survey) — [Turing/Greenhouse](https://job-boards.greenhouse.io/turingportal/jobs/5537879004); [Dice Senior LLMOps/MLOps](https://www.dice.com/job-detail/92bc7960-ba8d-4a26-a144-0413768e1899); [GulfTalent Senior MLOps](https://www.gulftalent.com/uae/jobs/senior-mlops-engineer-643631); [CVBankas Ray/Kubeflow/vLLM/SkyPilot](https://www.cvbankas.lt/mlops-engineer-with-expertise-in-ray-and-kubeflow-vllm-skypikot-on-kubernetes-darbas-namuose/1-13742747); [ITJobsWatch Ray jobs](https://www.itjobswatch.co.uk/search?q=Ray&r=1):
  - Experience: 3–7 years, e.g. "5-7 years of experience in MLOps, LLMOps, AI/ML Platform Engineering".
  - Serving: vLLM, SGLang, TGI, Triton, Ray Serve, with GPU utilization, latency and throughput tuning.
  - Platform: Kubernetes (GKE or AKS "preferred" in some), Ray and Kubeflow, multi-GPU orchestration, SkyPilot.
  - IaC: Terraform for clusters and networking.
  - Basics: Python, Docker, Git, CI/CD.
  - Observability: monitoring, model versioning, drift detection, Prometheus/Grafana.
  - Nice-to-haves: LoRA/QLoRA, RAG and vector DBs, LLM eval frameworks.
- The certification market follows the same shift. AWS's MLA-C02 revision moves toward Bedrock, RAG and agentic AI, and Microsoft's replacement for AI-102 centers on "AI Apps and Agents" — [Tutorials Dojo MLA-C02](https://tutorialsdojo.com/whats-new-with-the-aws-certified-machine-learning-engineer-associate-mla-c02-in-2026/); [Microsoft Learn AI-103](https://learn.microsoft.com/credentials/certifications/exams/ai-103/)
- **Weakly sourced or conflicting market claims (flag for the writer):**
  - About 1.6M open AI positions vs about 518k qualified candidates is hard to reconcile with about 1,550 weekly US postings — [FutureProofing.dev](https://www.futureproofing.dev/resources/ai-talent-gap/ai-engineer-demand-2026).
  - "Agentic AI" posting mentions reportedly rose 986% from 2023 to 2024, and average AI engineer salary reportedly crossed $206k in 2025. Exact originating source is unclear among aggregators — [Interview Query](https://www.interviewquery.com/p/ai-engineers-demand); [Hakia AI talent market](https://hakia.com/tech-insights/ai-talent-market/).
  - Headline YoY growth figures range from about 70% to 143% across 2026 pages using different datasets. The search summary noted Axial's 43k-posting analysis as the most transparent.

### Inferences
- The "cloud-strong AI engineer" profile employers reward in 2026 is:
  - Python plus one hyperscaler in depth (AWS leads in posting share).
  - Shipping foundation-model apps with RAG, agents and evals.
  - Kubernetes plus Terraform to run GPU workloads.
  - An inference-serving stack (vLLM first).
  - Observability and CI/CD.
- ML platform/LLMOps roles skew more senior (3–7+ years) than generic AI engineer roles. For career switchers, the realistic entry point is AI engineer / applied LLM roles, with platform skills built on top.
- Portfolio evidence from the Section 4 projects maps directly onto posting language. Examples: "vLLM throughput benchmark", "Terraform GPU node pool", "RAG eval suite in CI", "LoRA on spot with checkpointing".

### Gaps
- Could not access LinkedIn, Indeed Hiring Lab or other first-party job-market reports this session (search budget exhausted, many domains blocked). No LinkedIn/Indeed 2025–2026 figures are included.
- No quantitative frequency data was found specifically for Kubernetes, Terraform, vLLM or MLOps keywords across a large posting sample. The platform-role evidence is a small sample of individual postings.
- Salary data is weakly sourced and was left out of the findings except as flagged above.
- No data was found on how often postings require or prefer specific certifications.
