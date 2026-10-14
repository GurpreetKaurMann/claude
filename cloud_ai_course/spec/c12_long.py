import sys; sys.path.insert(0, '/home/claude/caigen')
from frag import *
from gailab import CODE, OUT

LONG = [
 dict(id='s0', chap='Zero to cloud A I engineer', say=[
   "In sixteen weeks, at about ten hours a week, you can go from knowing nothing about the cloud to having shipped six projects that match what employers ask for. The notebook estimates it costs about one hundred fifty to two hundred fifty dollars out of pocket, if you tear everything down.",
   "And if you forget one G P U for a month, that single mistake can cost more than the whole path. This final lesson is the road map, the money, the certificates, and one last check on every number in this course."],
  html=[H2('Zero to cloud AI engineer', 0),
        DEF('<b>16 weeks</b> · ~10 h a week · <b>$150-250</b> out of pocket (notebook estimate)', 0, 0.5, style='margin-top:24px;font-size:44px'),
        MARK('one forgotten GPU can cost more than the whole path', 1, 0.6)]),

 dict(id='s1', chap='Where we are', say=[
   "You have seen the whole stack. Compute and chips, containers, data, training, serving, shipping, retrieval and agents, security, and cost. Each lesson ended with a lab you can run, and each number carried a label saying how it was produced.",
   "Now the question is order. What do you learn first, what do you build, and how do you know you are done with each stop. Honest label. The order is my synthesis of what job postings ask for and which cost traps catch beginners. No source ranks it officially."],
  html=[H2('Where we are', 0),
        GRID([('11 lessons', 0, 0.3), ('11 lab sets', 0, 0.7), ('labelled numbers', 0, 1.1)], cols=3, h=150, fs=40),
        STICKY('Honest label', 'the stage order is my own synthesis, not an official ranking', 1, 0.5, style='margin-top:26px;font-size:36px')]),

 dict(id='s2', chap='Six stops', say=[
   "The road has six stops. Cloud fundamentals, containers and Kubernetes, serving a model, retrieval and agents with evaluations, MLOps and infrastructure as code, and finally distributed training. Each stop uses the one before. You cannot put a model on Kubernetes without identity and networking.",
   "You cannot debug a slow retrieval app if you do not know what batching does. Distributed training costs the most and is the rarest ask for entry roles, so it goes last. The first letters, F, C, S, R, M, D, spell, Frugal Coders Spend Really Modest Dollars."],
  html=[H2('The road: six stops', 0), SVG('c2', 1400, 406, 'margin:14px auto 0')],
  svgs=[('c2', 'road', 1000, 290, 1)]),

 dict(id='s3', chap='Run stage four alongside', say=[
   "One twist. Run stop four, retrieval, agents and evaluations, alongside stops two and three. It needs almost no cloud spend, mostly A P I tokens, and it maps to the most common ask in the postings. Foundation models appear in fifty-one percent of them.",
   "So start reading for it in week five. Every stop ends with a project, an estimated cost, and a done when check. Do not skip the check. Being able to show the thing working is what turns a course into portfolio evidence."],
  html=[H2('Stop 4 runs in parallel', 0),
        LIST([('almost no cloud spend: about $0-10, mostly API tokens', 0, 0.4), ('foundation models: 51% of postings', 0, 0.9), ('start reading in week 5', 1, 0.3), ('every stop ends with a project and a "done when" check', 1, 0.8)], kind='ar', style='margin-top:24px;font-size:42px')]),

 dict(id='s4', chap='Stop 1: fundamentals', say=[
   "Stop one, cloud fundamentals, weeks one and two. Learn in this order. Identity with least privilege, private networking, object storage for data and checkpoints, G P U compute and quotas, and billing with budgets and alerts. Learn deep learning basics in parallel.",
   "Project. Use Terraform to build a private network, a least privilege role, an encrypted bucket and a budget alert. Destroy it and rebuild from code. Done when destroy then apply rebuilds everything with zero console clicks, the role can read only its own bucket, and the budget alert actually fired."],
  html=[H2('Stop 1: cloud fundamentals (weeks 1-2)', 0),
        LIST([('IAM → private network → object storage → GPU quotas → budgets', 0, 0.4), ('Terraform: network + role + bucket + budget alert', 1, 0.3), ('done: destroy → apply rebuilds it, no console clicks', 1, 0.8), ('done: another bucket is DENIED · budget alert fired', 1, 1.3)], kind='ck', style='margin-top:22px;font-size:40px')]),

 dict(id='s5', chap='Stop 2: containers', say=[
   "Stop two, containers and Kubernetes, weeks three to five. Dockerfiles for machine learning, registries, Deployments, Services and autoscaling, managed Kubernetes, and G P U node pools that scale to zero. Project. Containerise an inference service, deploy it on managed Kubernetes with autoscaling, and tear it down.",
   "Then Terraform a G P U node pool of one small card that scales to zero. Done when the node shows one allocatable G P U, a pod runs nvidia dash smi, and the pool drops back to zero nodes when idle. Request G P U quota in week one, because new accounts may need it."],
  html=[H2('Stop 2: containers + Kubernetes (weeks 3-5)', 0),
        LIST([('Dockerfile → registry → Deployment + autoscaling → tear down', 0, 0.4), ('Terraform a GPU node pool: one L4, scale to zero', 0, 0.9), ('done: node shows nvidia.com/gpu: 1', 1, 0.3), ('done: pod runs nvidia-smi · pool returns to 0 nodes', 1, 0.8)], kind='ck', style='margin-top:22px;font-size:40px')]),

 dict(id='s6', chap='Stop 3: serving', say=[
   "Stop three, serving a model, weeks six and seven. The servers postings name are vLLM, SGLang, T G I, Triton and Ray Serve. Learn time to first token, tokens per second, and ninety-fifth percentile latency, and the levers, batching, the memory cache, quantisation and G P U choice.",
   "Project. Serve a seven or eight billion parameter model on one small card and benchmark it. Done when you have a table of tokens per second, first token time and tail latency at three concurrency levels and two precisions, and you can explain why throughput and tail latency both rise with concurrency. Cost, a few dollars a session."],
  html=[H2('Stop 3: serving (weeks 6-7)', 0),
        LIST([('vLLM on one L4 / A10G / L40S, 7-8B model', 0, 0.4), ('measure TTFT · tokens/s · p95', 0, 0.9), ('done: a table, 3 concurrency levels × 2 precisions', 1, 0.3), ('done: explain why throughput and p95 both rise', 1, 0.8)], kind='ck', style='margin-top:22px;font-size:40px')]),

 dict(id='s7', chap='Stop 4: retrieval and agents', say=[
   "Stop four, retrieval, agents and evaluations, weeks eight to ten. Build the pipeline, ingest, chunk, embed, store, retrieve, generate. Add agents with tool calling, an M C P server, and tracing. Wire evaluations of recall and faithfulness into your build.",
   "Done when your build goes red on a change that drops recall below your threshold, traces show every tool call with inputs and outputs, and you can say how big your evaluation set is and what it does not cover. Cost, mostly tokens, around zero to ten dollars."],
  html=[H2('Stop 4: RAG, agents, MCP + evals (weeks 8-10)', 0),
        LIST([('RAG app + eval suite in CI · MCP server + traced agent', 0, 0.4), ('done: CI goes red when recall or faithfulness drops', 1, 0.3), ('done: every tool call traced', 1, 0.8), ('done: you can state the eval set size and its gaps', 1, 1.3)], kind='ck', style='margin-top:22px;font-size:40px')]),

 dict(id='s8', chap='Stop 5: MLOps', say=[
   "Stop five, MLOps and observability, weeks eleven to thirteen. Experiment tracking, a model registry, pipelines with an evaluation gate and a canary, Terraform for several environments, and monitoring with drift alerts. Fine tune with LoRA on spot capacity, saving checkpoints to object storage.",
   "Done when you kill the spot machine mid run and the job resumes from the last checkpoint, the registry shows a versioned model with its metrics, and a dashboard alert fires on fake drift. Cost, roughly two to twenty-five dollars."],
  html=[H2('Stop 5: MLOps + observability (weeks 11-13)', 0),
        LIST([('LoRA on spot → checkpoints in a bucket → registry → vLLM', 0, 0.4), ('CI/CD with an eval gate · drift dashboard + alert', 0, 0.9), ('done: kill the VM, job resumes, loss curve continuous', 1, 0.3), ('done: versioned model + alert fires on fake drift', 1, 0.8)], kind='ck', style='margin-top:22px;font-size:40px')]),

 dict(id='s9', chap='Stop 6: distributed', say=[
   "Stop six, distributed training, weeks fourteen to sixteen. Data, tensor and pipeline parallelism, ZeRO and F S D P, collective communication, and the memory and efficiency accounting you saw in lesson five. Start with basic data parallel on a free two card notebook.",
   "Then compare layouts on a few rented cards, and finish with the nanochat speed run. About two hours on eight H one hundreds, around forty-eight dollars on demand, fifteen on spot. Done when, from model size alone, you can say whether plain data parallel fits, and your measured memory roughly agrees."],
  html=[H2('Stop 6: distributed training (weeks 14-16)', 0),
        LIST([('DDP on free 2×T4 → compare layouts on 2-8 rented GPUs', 0, 0.4), ('nanochat speedrun: ~2 h on 8×H100 ≈ $48 ($15 spot)', 0, 0.9), ('done: say from model size whether DDP fits or you need FSDP', 1, 0.3), ('done: measured memory roughly agrees; MFU table; chat CLI works', 1, 0.8)], kind='ck', style='margin-top:22px;font-size:40px')]),

 dict(id='s10', chap='How long', say=[
   "How long does it take? The plan is sixteen weeks at about ten hours a week, a hundred and sixty hours. That ten is my assumption. At five hours a week it is thirty-two weeks. At fifteen, ten point seven. At twenty, eight.",
   "There is also a twelve week fast track that skips or merges four of the weeks, the quantisation week, the agents week, the observability week and the efficiency week. Change the hours in the script and read your own date."],
  html=[H2('How long?', 0), SVG('c10', 1400, 427, 'margin:14px auto 0')],
  svgs=[('c10', 'weeks', 1000, 305, 1)]),

 dict(id='s11', chap='What it costs', say=[
   "What does it cost? The notebook's own estimate for the whole path is about one hundred fifty to two hundred fifty dollars, if you tear everything down. I added up the project estimates, and got thirty-two to a hundred fifty-five before credits. So budget the higher figure.",
   "Spend climbs along the road. Zero for stop one, a few dollars a lab for two to five, tens for stop six. Pay for G P U time only from stop three on. Free tiers help. New accounts get credits, and Kaggle gives about thirty free G P U hours a week."],
  html=[H2('What the path costs', 0), SVG('c11', 1400, 560, 'margin:6px auto 0')],
  svgs=[('c11', 'stagecost', 1000, 400, 1)]),

 dict(id='s12', chap='The forgotten GPU', say=[
   "Now the mistake. A single small G P U node left up for a month is seven hundred thirty hours at fifty cents to a dollar twenty, three hundred sixty-five to eight hundred seventy-six dollars. That is two to six times the cost of the entire path. Idle resources are the number one way to overspend.",
   "So the habit is simple. After every lab, run the destroy command, then list your clusters and expect nothing. Every Friday, check the billing page. Habit, not heroics."],
  html=[H2('The forgotten GPU', 0), SVG('c12', 1400, 413, 'margin:14px auto 0')],
  svgs=[('c12', 'forgot', 1000, 295, 1)]),

 dict(id='s13', chap='Teardown traps', say=[
   "Other traps worth knowing. Free networking labs that include a managed N A T gateway keep billing by the hour, so avoid them or destroy the same day. An old Kubernetes version on A W S can move from ten cents to about sixty cents an hour for the control plane, so keep versions current.",
   "On Google, the monthly management credit covers zonal and Autopilot clusters only, not regional clusters or machine costs. And spot machines with no checkpoints can cost more than on demand, as lesson two showed. Read the bill, not just the plan."],
  html=[H2('Teardown traps', 0),
        LIST([('NAT gateways in "free" network labs: destroy the same day', 0, 0.4), ('old EKS version: $0.10/h → about $0.60/h control plane', 0, 0.9), ('GKE $74.40 credit: zonal or Autopilot only, not nodes', 1, 0.3), ('spot with no checkpoints can cost more than on-demand', 1, 0.8)], kind='ar', style='margin-top:22px;font-size:40px')]),

 dict(id='s14', chap='Cheap GPUs by stage', say=[
   "Which G P U for which stop? Free notebooks for stop one and basic data parallel. A small twenty-four gigabyte card, roughly fifty cents to a dollar twenty an hour, for stops two and three. A mid size card around ninety-two cents for bigger benchmarks. An A one hundred, about a dollar fifty, for stop five.",
   "And rented H one hundreds, about a dollar thirty-three to three dollars on marketplaces, for stop six. Prices are vendor and aggregator figures from September twenty twenty-six, and they move. Spend credits on the central processor and Kubernetes stops, and rent marketplace cards for stops three, five and six."],
  html=[H2('Cheap GPUs by stop', 0),
        TABLE(['GPU', 'About $/hr', 'Stop'], [(['T4 / P100', 'free (Kaggle, Colab)', '1, DDP basics'], 0, 0.4), (['L4 / A10G (24 GB)', '$0.50-1.50', '2-3'], 0, 0.8), (['L40S (48 GB)', '~$0.92-0.99', '3 benchmarks'], 1, 0.3), (['A100 80 GB', '~$1.49', '5 LoRA'], 1, 0.7), (['H100', '$1.33-3.00 (marketplaces)', '6 nanochat'], 1, 1.1)], style='margin-top:14px;font-size:34px'),
        SUB('vendor and aggregator figures, Sep 2026', 1, 1.5, style='margin-top:8px')]),

 dict(id='s15', chap='Certificates in 2026', say=[
   "Certificates. In twenty twenty-six there was big churn. The A W S Machine Learning Specialty exam retired in March, the Azure A I Engineer exam in June, and the Azure Data Scientist exam in June. A mnemonic is, who went M A D. M L S, A I one oh two, D P one hundred.",
   "Swaps. The A W S ML Engineer exam moved to version C zero two. The Azure engineer exam became A I one oh three, a new exam, and Azure A I Fundamentals became nine oh one. If you hold an old one, it stays active for its normal period. Always check the exam code on the official page right before booking."],
  html=[H2('Certificates: check the code', 0),
        TABLE(['Retired / changed', 'Next'], [(['AWS MLS-C01 (Mar 31, 2026)', 'AIP-C01 · MLA-C02'], 0, 0.4), (['Azure AI-102 (Jun 30)', 'AI-103 (a new exam)'], 0, 0.8), (['Azure DP-100 (Jun 1)', 'AI-300 MLOps'], 1, 0.3), (['AI-900', 'AI-901'], 1, 0.7)], style='margin-top:18px;font-size:38px'),
        SUB('MAD: MLS-C01, AI-102, DP-100 · notebook, Oct 2026', 1, 1.1, style='margin-top:10px;font-size:32px')]),

 dict(id='s16', chap='Which cert, when', say=[
   "Which certificate when? Stop one, a fundamentals exam, like the A W S A I Practitioner at one hundred dollars. Stop two, the Kubernetes associate at two hundred fifty, then the hands on Kubernetes administrator at four hundred forty-five. Stop four, the A W S Generative A I Developer Professional at three hundred.",
   "Stop five, the Google Professional ML Engineer at two hundred, or the A W S ML Engineer. Hands on exams in a live terminal are probably a stronger signal than multiple choice, though that is inferred from format, not from an employer survey. No data shows how often postings require a specific cert. Projects beat badges. Use certs as structure and a tiebreaker."],
  html=[H2('Which cert, when', 0),
        LIST([('stop 1: AWS AI Practitioner ($100)', 0, 0.4), ('stop 2: KCNA ($250) → CKA ($445), a live terminal', 0, 0.9), ('stop 4: AWS AIP-C01 ($300) or Azure AI-103', 1, 0.3), ('stop 5: Google PMLE ($200) or AWS MLA-C02', 1, 0.8), ('projects beat badges: certs are structure and a tiebreaker', 1, 1.3)], kind='ar', style='margin-top:20px;font-size:38px')]),

 dict(id='s17', chap='Books and courses', say=[
   "What to read and watch. If you are short on time, a minimal stack. Karpathy's Zero to Hero for from scratch intuition. Made With ML to learn how to ship. The A I Engineering book, plus the Hugging Face agents course, for foundation model apps. Then the Ultra Scale Playbook and nanochat for training at scale.",
   "Free options include fast dot A I, the Hugging Face language model and M C P courses, and Stanford's language models from scratch lectures. The notebook marks anything it could not verify this round, such as current course catalogs, so check before you buy."],
  html=[H2('A minimal reading stack', 0),
        LIST([('Zero to Hero → Made With ML', 0, 0.4), ('AI Engineering (book) + HF Agents course', 0, 0.9), ('Ultra-Scale Playbook + nanochat', 1, 0.3), ('free: fast.ai · HF LLM + MCP courses · Stanford CS336', 1, 0.8)], kind='ar', style='margin-top:24px;font-size:42px')]),

 dict(id='s18', chap='What employers ask', say=[
   "What do employers ask for? In a sample of forty-three thousand four hundred eighty United States A I engineering postings through July twenty twenty-six, Python appeared in sixty-two percent, cloud platforms in fifty-five, foundation models in fifty-one. About fifteen hundred new roles a week.",
   "Platform and L L M ops roles add vLLM, Kubernetes with G P Us, Terraform and observability, and usually want three to seven years. If you are switching careers, the realistic way in is an applied A I engineer role, stops one to four, with platform skills added on the job."],
  html=[H2('What employers ask for', 0),
        GRID([('Python<br>62%', 0, 0.3), ('cloud platforms<br>55%', 0, 0.7), ('foundation models<br>51%', 0, 1.1)], cols=3, h=210, fs=36),
        SUB('43,480 US AI-engineering postings to Jul 2026 · one analyst sample · platform roles want 3-7 years', 1, 0.5, style='margin-top:18px')]),

 dict(id='s19', chap='Use the posting words', say=[
   "A practical trick. The projects here map onto posting language. vLLM throughput benchmark. Terraform G P U node pool. RAG evaluation suite in C I. LoRA on spot with checkpointing. Put those exact phrases in your repository read me files and your resume.",
   "Show the thing working, with the number. A table of tokens per second you measured beats a badge. A repository that says what it cost and what it does not cover earns trust. That is the habit this whole course has tried to build."],
  html=[H2('Name projects in the posting\'s words', 0),
        LIST([('"vLLM throughput benchmark"', 0, 0.4), ('"Terraform GPU node pool"', 0, 0.8), ('"RAG eval suite in CI"', 0, 1.2), ('"LoRA on spot with checkpointing"', 1, 0.3), ('say what it cost and what it does not cover', 1, 0.8)], kind='ck', style='margin-top:22px;font-size:42px')]),

 dict(id='s19b', chap='What to double check', say=[
   "A few honest limits before you start. Prices, exam codes and free credit rules change monthly, so treat every dollar figure here as a dated estimate. Sources disagree on several certificate prices and dates, and the notebook flags them.",
   "Free trial G P U quota was not rechecked in twenty twenty-six, so do not plan stop three around it. And the career numbers come from public posting samples, which are directional, not guarantees. Verify the one or two that decide your next purchase."],
  html=[H2('Double-check before you pay', 0),
        LIST([('prices, exam codes and credit rules change monthly', 0, 0.4), ('sources disagree on some cert prices and dates', 0, 0.9), ('free-trial GPU quota not rechecked in 2026', 1, 0.3), ('posting samples are directional, not guarantees', 1, 0.8)], kind='ar', style='margin-top:24px;font-size:42px')]),

 dict(id='s20', chap='The claims ledger', say=[
   "One last lab, and it is a different kind. I made a claims ledger. For thirty-two headline numbers from lessons one to eleven, a script looks the number up in the saved output of the lab that produced it, and prints its label. All thirty-two were found.",
   "Eleven were measured on one machine, thirteen came from simulations with assumed inputs, five were arithmetic, and three used synthetic data. It cannot prove the experiments are good. It proves each claim came from a file you can rerun, and that is the standard to hold anyone to, including me."],
  html=[H2('The claims ledger', 0), SVG('c20', 1400, 413, 'margin:14px auto 0')],
  svgs=[('c20', 'ledger', 1000, 295, 1)]),

 dict(id='s21', chap='What we measured', say=[
   "A few things the labs showed. A seventy billion model at eight bit plus thirty-two chats needs one hundred eighty-seven gigabytes. Skipping checkpoints on spot turned a hundred hour job into over two million hours in simulation. Twenty thousand small files read twenty-five times slower than one shard.",
   "Mixed precision training state measured sixteen bytes per parameter. The memory cache made generation twelve times faster. An eval gate blocked a change that raised the average. And the keyword filter stopped three of twelve attacks, where an egress allowlist leaked none."],
  html=[H2('What the labs showed', 0),
        GRID([('187 GB: 70B + 32 chats', 0, 0.3), ('no checkpoints: 2.2M h', 0, 0.8), ('small files: 25× slower', 0, 1.3),
              ('16 bytes per parameter', 1, 0.3), ('KV cache: 12× faster', 1, 0.8), ('filter 3/12 · allowlist 0 leaks', 1, 1.3)], cols=3, h=170, fs=30)]),

 dict(id='s22', chap='ShopNest Copilot: the full picture', say=[
   "Our course project, ShopNest Copilot, is now a full plan. It fits its memory, runs on the right mix of capacity, ships as layered images, reads sharded data, and serves with a cache and batching. It deploys through an eval gate and a canary.",
   "It retrieves with chunks that were tested, agents that survive a crash, and an architecture that limits what an injected instruction can do. And it is priced per resolved ticket. That is what a cloud A I engineer builds. Not any single trick, but all of them, in the right order."],
  html=[H2('ShopNest Copilot: the whole plan', 0),
        TABLE(['Layer', 'Decision'], [(['capacity', 'fit memory first · spot with checkpoints · scale to zero'], 0, 0.4), (['ship + data', 'layered images · sharded data · eval gate + canary'], 0, 0.9), (['app', 'tested chunks · idempotent agent · egress allowlist · tenant filter'], 1, 0.3), (['money', 'cache first · cost per resolved ticket · budgets and alerts'], 1, 0.8)], style='margin-top:18px;font-size:34px')]),

 dict(id='s23', chap='Your first week', say=[
   "What do you do this week? Open one cloud account and set a budget alert before anything else. Request G P U quota now, since approval can take days. Pick one stop one project, the Terraform network, role, bucket and budget alert.",
   "Run the lab scripts from this course, change a number in each, and write down what you saw. Then on Friday, run the teardown commands and check the bill. That is week one. Sixteen of those, and you are a cloud A I engineer."],
  html=[H2('Your first week', 0),
        LIST([('open one account · set a budget alert first', 0, 0.4), ('request GPU quota now', 0, 0.9), ('build the stop 1 Terraform project', 1, 0.3), ('run the labs, change one number each', 1, 0.8), ('Friday: teardown commands + billing check', 1, 1.3)], kind='ck', style='margin-top:22px;font-size:42px')]),

 dict(id='s24', chap='Interview corner', say=[
   "Interview corner. Asked why you run retrieval and agents in parallel with the infrastructure stops, say: it needs almost no cloud spend, and foundation models appear in half of postings. Asked how a spot run can cost more than on demand, say: with no checkpoints, an eviction loses all work.",
   "Asked how to avoid a surprise bill, say: set a budget alert before anything else, tear down after every lab, and check for idle resources every week. One forgotten G P U can cost more than the rest of the path combined."],
  html=[H2('Interview corner', 0),
        Q('Why run RAG and agents alongside infrastructure?', 'Almost no cloud spend; foundation models in 51% of postings.', 0, 0.4),
        Q('How do you avoid a surprise bill?', 'Budget alert first, tear down after every lab, check idle weekly.', 1, 0.4)]),

 dict(id='s25', chap='Four words to keep', say=[
   "Four last words to keep. Teardown: destroy what you built, then confirm nothing is left billing. Done when: a check that proves a stage works.",
   "Portfolio: a project you can show running, with its numbers. And label: the honest note on whether a number was measured, simulated, calculated, or made up."],
  html=[H2('Four words to keep', 0),
        GRID([('<b>teardown</b>', 0, 0.3), ('<b>done when</b>', 0, 0.9), ('<b>portfolio</b>', 1, 0.3), ('<b>label</b>', 1, 0.9)], cols=2, h=140, fs=42, style='margin-top:30px')]),

 dict(id='s26', chap='Recap', say=[
   "Recap of the road. Six stops, frugal coders spend really modest dollars. Run retrieval alongside. Sixteen weeks at ten hours a week, about a hundred fifty to two hundred fifty dollars if you tear down. A forgotten G P U costs more than the path.",
   "Check the exam code before you book. Projects beat badges. And label every number you quote. Thank you for learning with me. The notes and code are free at the code notebook dot com. Now go and build."],
  html=[H2('Recap', 0),
        GRID([('6 stops: F-C-S-R-M-D', 0, 0.3), ('16 weeks · ~10 h a week', 0, 0.9), ('$150-250 if you tear down', 0, 1.5),
              ('one forgotten GPU > the path', 1, 0.3), ('check the exam code', 1, 0.9), ('projects beat badges', 1, 1.5)], cols=3, h=150, fs=30)]),
]
