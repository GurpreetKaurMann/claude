# CAI-12 · Your Learning Path: Scripts

**Lesson 12 of 12 · Module 5 · Safe, cheap, and your career**

Voice: AI narrator (Kokoro `af_heart`). Final lesson video length: 17:02.

## Long video narration

**[Zero to cloud A I engineer]**

> In sixteen weeks, at about ten hours a week, you can go from knowing nothing about the cloud to having shipped six projects that match what employers ask for. The notebook estimates it costs about one hundred fifty to two hundred fifty dollars out of pocket, if you tear everything down.

> And if you forget one G P U for a month, that single mistake can cost more than the whole path. This final lesson is the road map, the money, the certificates, and one last check on every number in this course.

**[Intro]**

> Welcome to lesson twelve of the cloud for A I engineers course, on The Code Notebook.

> The handwritten notes and the code for this lesson are linked in the description.

**[Where we are]**

> You have seen the whole stack. Compute and chips, containers, data, training, serving, shipping, retrieval and agents, security, and cost. Each lesson ended with a lab you can run, and each number carried a label saying how it was produced.

> Now the question is order. What do you learn first, what do you build, and how do you know you are done with each stop. Honest label. The order is my synthesis of what job postings ask for and which cost traps catch beginners. No source ranks it officially.

**[Six stops]**

> The road has six stops. Cloud fundamentals, containers and Kubernetes, serving a model, retrieval and agents with evaluations, MLOps and infrastructure as code, and finally distributed training. Each stop uses the one before. You cannot put a model on Kubernetes without identity and networking.

> You cannot debug a slow retrieval app if you do not know what batching does. Distributed training costs the most and is the rarest ask for entry roles, so it goes last. The first letters, F, C, S, R, M, D, spell, Frugal Coders Spend Really Modest Dollars.

**[Run stage four alongside]**

> One twist. Run stop four, retrieval, agents and evaluations, alongside stops two and three. It needs almost no cloud spend, mostly A P I tokens, and it maps to the most common ask in the postings. Foundation models appear in fifty-one percent of them.

> So start reading for it in week five. Every stop ends with a project, an estimated cost, and a done when check. Do not skip the check. Being able to show the thing working is what turns a course into portfolio evidence.

**[Stop 1: fundamentals]**

> Stop one, cloud fundamentals, weeks one and two. Learn in this order. Identity with least privilege, private networking, object storage for data and checkpoints, G P U compute and quotas, and billing with budgets and alerts. Learn deep learning basics in parallel.

> Project. Use Terraform to build a private network, a least privilege role, an encrypted bucket and a budget alert. Destroy it and rebuild from code. Done when destroy then apply rebuilds everything with zero console clicks, the role can read only its own bucket, and the budget alert actually fired.

**[Stop 2: containers]**

> Stop two, containers and Kubernetes, weeks three to five. Dockerfiles for machine learning, registries, Deployments, Services and autoscaling, managed Kubernetes, and G P U node pools that scale to zero. Project. Containerise an inference service, deploy it on managed Kubernetes with autoscaling, and tear it down.

> Then Terraform a G P U node pool of one small card that scales to zero. Done when the node shows one allocatable G P U, a pod runs nvidia dash smi, and the pool drops back to zero nodes when idle. Request G P U quota in week one, because new accounts may need it.

**[Stop 3: serving]**

> Stop three, serving a model, weeks six and seven. The servers postings name are vLLM, SGLang, T G I, Triton and Ray Serve. Learn time to first token, tokens per second, and ninety-fifth percentile latency, and the levers, batching, the memory cache, quantisation and G P U choice.

> Project. Serve a seven or eight billion parameter model on one small card and benchmark it. Done when you have a table of tokens per second, first token time and tail latency at three concurrency levels and two precisions, and you can explain why throughput and tail latency both rise with concurrency. Cost, a few dollars a session.

**[Stop 4: retrieval and agents]**

> Stop four, retrieval, agents and evaluations, weeks eight to ten. Build the pipeline, ingest, chunk, embed, store, retrieve, generate. Add agents with tool calling, an M C P server, and tracing. Wire evaluations of recall and faithfulness into your build.

> Done when your build goes red on a change that drops recall below your threshold, traces show every tool call with inputs and outputs, and you can say how big your evaluation set is and what it does not cover. Cost, mostly tokens, around zero to ten dollars.

**[Stop 5: MLOps]**

> Stop five, MLOps and observability, weeks eleven to thirteen. Experiment tracking, a model registry, pipelines with an evaluation gate and a canary, Terraform for several environments, and monitoring with drift alerts. Fine tune with LoRA on spot capacity, saving checkpoints to object storage.

> Done when you kill the spot machine mid run and the job resumes from the last checkpoint, the registry shows a versioned model with its metrics, and a dashboard alert fires on fake drift. Cost, roughly two to twenty-five dollars.

**[Stop 6: distributed]**

> Stop six, distributed training, weeks fourteen to sixteen. Data, tensor and pipeline parallelism, ZeRO and F S D P, collective communication, and the memory and efficiency accounting you saw in lesson five. Start with basic data parallel on a free two card notebook.

> Then compare layouts on a few rented cards, and finish with the nanochat speed run. About two hours on eight H one hundreds, around forty-eight dollars on demand, fifteen on spot. Done when, from model size alone, you can say whether plain data parallel fits, and your measured memory roughly agrees.

**[How long]**

> How long does it take? The plan is sixteen weeks at about ten hours a week, a hundred and sixty hours. That ten is my assumption. At five hours a week it is thirty-two weeks. At fifteen, ten point seven. At twenty, eight.

> There is also a twelve week fast track that skips or merges four of the weeks, the quantisation week, the agents week, the observability week and the efficiency week. Change the hours in the script and read your own date.

**[What it costs]**

> What does it cost? The notebook's own estimate for the whole path is about one hundred fifty to two hundred fifty dollars, if you tear everything down. I added up the project estimates, and got thirty-two to a hundred fifty-five before credits. So budget the higher figure.

> Spend climbs along the road. Zero for stop one, a few dollars a lab for two to five, tens for stop six. Pay for G P U time only from stop three on. Free tiers help. New accounts get credits, and Kaggle gives about thirty free G P U hours a week.

**[The forgotten GPU]**

> Now the mistake. A single small G P U node left up for a month is seven hundred thirty hours at fifty cents to a dollar twenty, three hundred sixty-five to eight hundred seventy-six dollars. That is two to six times the cost of the entire path. Idle resources are the number one way to overspend.

> So the habit is simple. After every lab, run the destroy command, then list your clusters and expect nothing. Every Friday, check the billing page. Habit, not heroics.

**[Teardown traps]**

> Other traps worth knowing. Free networking labs that include a managed N A T gateway keep billing by the hour, so avoid them or destroy the same day. An old Kubernetes version on A W S can move from ten cents to about sixty cents an hour for the control plane, so keep versions current.

> On Google, the monthly management credit covers zonal and Autopilot clusters only, not regional clusters or machine costs. And spot machines with no checkpoints can cost more than on demand, as lesson two showed. Read the bill, not just the plan.

**[Cheap GPUs by stage]**

> Which G P U for which stop? Free notebooks for stop one and basic data parallel. A small twenty-four gigabyte card, roughly fifty cents to a dollar twenty an hour, for stops two and three. A mid size card around ninety-two cents for bigger benchmarks. An A one hundred, about a dollar fifty, for stop five.

> And rented H one hundreds, about a dollar thirty-three to three dollars on marketplaces, for stop six. Prices are vendor and aggregator figures from September twenty twenty-six, and they move. Spend credits on the central processor and Kubernetes stops, and rent marketplace cards for stops three, five and six.

**[Certificates in 2026]**

> Certificates. In twenty twenty-six there was big churn. The A W S Machine Learning Specialty exam retired in March, the Azure A I Engineer exam in June, and the Azure Data Scientist exam in June. A mnemonic is, who went M A D. M L S, A I one oh two, D P one hundred.

> Swaps. The A W S ML Engineer exam moved to version C zero two. The Azure engineer exam became A I one oh three, a new exam, and Azure A I Fundamentals became nine oh one. If you hold an old one, it stays active for its normal period. Always check the exam code on the official page right before booking.

**[Which cert, when]**

> Which certificate when? Stop one, a fundamentals exam, like the A W S A I Practitioner at one hundred dollars. Stop two, the Kubernetes associate at two hundred fifty, then the hands on Kubernetes administrator at four hundred forty-five. Stop four, the A W S Generative A I Developer Professional at three hundred.

> Stop five, the Google Professional ML Engineer at two hundred, or the A W S ML Engineer. Hands on exams in a live terminal are probably a stronger signal than multiple choice, though that is inferred from format, not from an employer survey. No data shows how often postings require a specific cert. Projects beat badges. Use certs as structure and a tiebreaker.

**[Books and courses]**

> What to read and watch. If you are short on time, a minimal stack. Karpathy's Zero to Hero for from scratch intuition. Made With ML to learn how to ship. The A I Engineering book, plus the Hugging Face agents course, for foundation model apps. Then the Ultra Scale Playbook and nanochat for training at scale.

> Free options include fast dot A I, the Hugging Face language model and M C P courses, and Stanford's language models from scratch lectures. The notebook marks anything it could not verify this round, such as current course catalogs, so check before you buy.

**[What employers ask]**

> What do employers ask for? In a sample of forty-three thousand four hundred eighty United States A I engineering postings through July twenty twenty-six, Python appeared in sixty-two percent, cloud platforms in fifty-five, foundation models in fifty-one. About fifteen hundred new roles a week.

> Platform and L L M ops roles add vLLM, Kubernetes with G P Us, Terraform and observability, and usually want three to seven years. If you are switching careers, the realistic way in is an applied A I engineer role, stops one to four, with platform skills added on the job.

**[Use the posting words]**

> A practical trick. The projects here map onto posting language. vLLM throughput benchmark. Terraform G P U node pool. RAG evaluation suite in C I. LoRA on spot with checkpointing. Put those exact phrases in your repository read me files and your resume.

> Show the thing working, with the number. A table of tokens per second you measured beats a badge. A repository that says what it cost and what it does not cover earns trust. That is the habit this whole course has tried to build.

**[What to double check]**

> A few honest limits before you start. Prices, exam codes and free credit rules change monthly, so treat every dollar figure here as a dated estimate. Sources disagree on several certificate prices and dates, and the notebook flags them.

> Free trial G P U quota was not rechecked in twenty twenty-six, so do not plan stop three around it. And the career numbers come from public posting samples, which are directional, not guarantees. Verify the one or two that decide your next purchase.

**[The claims ledger]**

> One last lab, and it is a different kind. I made a claims ledger. For thirty-two headline numbers from lessons one to eleven, a script looks the number up in the saved output of the lab that produced it, and prints its label. All thirty-two were found.

> Eleven were measured on one machine, thirteen came from simulations with assumed inputs, five were arithmetic, and three used synthetic data. It cannot prove the experiments are good. It proves each claim came from a file you can rerun, and that is the standard to hold anyone to, including me.

**[What we measured]**

> A few things the labs showed. A seventy billion model at eight bit plus thirty-two chats needs one hundred eighty-seven gigabytes. Skipping checkpoints on spot turned a hundred hour job into over two million hours in simulation. Twenty thousand small files read twenty-five times slower than one shard.

> Mixed precision training state measured sixteen bytes per parameter. The memory cache made generation twelve times faster. An eval gate blocked a change that raised the average. And the keyword filter stopped three of twelve attacks, where an egress allowlist leaked none.

**[ShopNest Copilot: the full picture]**

> Our course project, ShopNest Copilot, is now a full plan. It fits its memory, runs on the right mix of capacity, ships as layered images, reads sharded data, and serves with a cache and batching. It deploys through an eval gate and a canary.

> It retrieves with chunks that were tested, agents that survive a crash, and an architecture that limits what an injected instruction can do. And it is priced per resolved ticket. That is what a cloud A I engineer builds. Not any single trick, but all of them, in the right order.

**[Your first week]**

> What do you do this week? Open one cloud account and set a budget alert before anything else. Request G P U quota now, since approval can take days. Pick one stop one project, the Terraform network, role, bucket and budget alert.

> Run the lab scripts from this course, change a number in each, and write down what you saw. Then on Friday, run the teardown commands and check the bill. That is week one. Sixteen of those, and you are a cloud A I engineer.

**[Interview corner]**

> Interview corner. Asked why you run retrieval and agents in parallel with the infrastructure stops, say: it needs almost no cloud spend, and foundation models appear in half of postings. Asked how a spot run can cost more than on demand, say: with no checkpoints, an eviction loses all work.

> Asked how to avoid a surprise bill, say: set a budget alert before anything else, tear down after every lab, and check for idle resources every week. One forgotten G P U can cost more than the rest of the path combined.

**[Four words to keep]**

> Four last words to keep. Teardown: destroy what you built, then confirm nothing is left billing. Done when: a check that proves a stage works.

> Portfolio: a project you can show running, with its numbers. And label: the honest note on whether a number was measured, simulated, calculated, or made up.

**[Recap]**

> Recap of the road. Six stops, frugal coders spend really modest dollars. Run retrieval alongside. Sixteen weeks at ten hours a week, about a hundred fifty to two hundred fifty dollars if you tear down. A forgotten G P U costs more than the path.

> Check the exam code before you book. Projects beat badges. And label every number you quote. Thank you for learning with me. The notes and code are free at the code notebook dot com. Now go and build.

**[Next lesson]**

> That was the last lesson of the course. Thank you for learning with me. Now go and build your first project.

> Subscribe so you don't miss it. See you in the notebook.


## Short 1: One Forgotten GPU Costs More Than the Whole Cloud AI Path #shorts

> One forgotten G P U can cost more than learning the entire cloud A I path. Here is the sum.

> A G P U node left up for a month is seven hundred thirty hours at fifty cents to a dollar twenty. That is three hundred sixty-five to eight hundred seventy-six dollars, estimated.

> The whole sixteen week learning path adds up to at most about a hundred fifty-five dollars in project estimates. So after every lab, destroy, then list your clusters and expect nothing.

> Destroy it, then check the list.


## Short 2: The 16-Week Cloud AI Engineer Roadmap (6 Stops, Frugal Coders) #shorts

> Zero to cloud A I engineer in sixteen weeks. Six stops, in a specific order, and the order has a reason.

> Cloud basics, containers, serving, retrieval with evaluations, MLOps, then distributed training. Each stop uses the one before, and the rarest, most expensive one goes last.

> Frugal Coders Spend Really Modest Dollars. About ten hours a week, a hundred and sixty hours. Every stop ends with a project and a done when check.

> Order matters. Cheapest first.


## Instagram Reel 1: 3 popular cloud AI certs were retired in 2026 (check before you book)

> Three popular cloud A I certificates were retired in twenty twenty-six.

> The A W S Machine Learning Specialty in March. The Azure A I Engineer exam in June. And the Azure Data Scientist exam in June. Who went mad, M L S, A I one oh two, D P one hundred. Check the exam code before you book. Projects beat badges anyway.

> Check the code first. Save this.
