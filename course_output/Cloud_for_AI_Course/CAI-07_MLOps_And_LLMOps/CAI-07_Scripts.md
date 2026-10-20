# CAI-07 · MLOps and LLMOps: Scripts

**Lesson 7 of 12 · Module 4 · Shipping it**

Voice: AI narrator (Kokoro `af_heart`). Final lesson video length: 16:18.

## Long video narration

**[A better score that broke refunds]**

> I changed one prompt. The overall score went up, from ninety percent to ninety-two. Everyone would have shipped it. But one group of customers got much worse. Refund tickets fell from a hundred percent right to fifty.

> A simple automatic check, an eval gate, caught it and blocked the change. This lesson is about shipping A I changes safely, again and again, without breaking what already works.

**[Intro]**

> Welcome to lesson seven of the cloud for A I engineers course, on The Code Notebook.

> The handwritten notes and the code for this lesson are linked in the description.

**[Where we are]**

> So far we built the pieces of an A I system. Now we run it as a product. That means changing it often, without breaking it, and knowing quickly when something goes wrong.

> That discipline has two names. M L Ops for classic models, and L L M Ops for language model apps. As always I label my experiments. The eval gate uses a toy keyword model as a stand in for a language model, with synthetic tickets. The canary and trials results are simulations.

**[Three maturity levels]**

> Classic M L Ops has three levels, from a well known Google guide. Level zero is everything by hand. Notebooks, a model handed over to an engineer, and nobody watching afterwards.

> Level one automates the training. A pipeline retrains the model on fresh data by itself, when new data arrives, on a schedule, or when performance drops.

> Level two automates the shipping of that pipeline. The pipeline code itself is tested and deployed like any other service.

**[LLMOps is different]**

> Language model apps change the picture. Often you train nothing. You call a hosted model. So what do you version? The prompts. The model and its settings. The tools the model may call. The retrieval index. And the code that wraps it all.

> Quality is no longer one accuracy number. It is a set of evaluations, plus checks on live traffic. The thing you watch is the trace of one request. And the same input can give different outputs, so you must run several trials.

**[Models decay silently]**

> There is one more reason for all this. Models decay without anyone touching them. The world changes, customers write differently, new products appear, and the model's inputs drift away from what it saw in training.

> Without monitoring, nothing crashes. The answers just get slowly worse. That is why level zero is so risky. Classic M L Ops watches the distribution of inputs and the quality of outputs, and retrains when they move too far.

**[The release loop]**

> Here is the loop to build. Make a change, to a prompt or a model. Score the whole test set with an eval gate. Send a little traffic to the new version first, called a canary.

> Then watch it with traces and automatic judges on live requests. When something fails in production, turn that failure into a new test case. Every change is then scored against everything that ever went wrong.

> That last arrow is the whole point. The loop gets harder to fool every week.

**[Three layers of tests]**

> Testing an A I system has three layers, and each catches a different break. Code tests, the normal kind. Do the functions work and do the parts fit together?

> Data and model tests. Does training converge, are there missing values, does the data still look like the reference data? And evaluation suites for language models, where graders score answers on a fixed, golden set of examples.

> Run all three on every change. A failure in any layer blocks the merge.

**[What a gate checks]**

> An eval gate is the check that stands between a change and production. It asks several questions. Does the challenger beat the current champion by a real margin, not just match it?

> Does any important slice get worse, meaning a group of cases such as refunds? Are the speed and size limits met? And does the model actually load and serve in a test container? Only if every answer is yes does the change move on.

**[My toy gate]**

> I built a working gate. The task is to route a support ticket to an intent, refund, delivery, account or product. The model is a toy. A keyword scorer. It is a stand in for a language model, and the prompt is its list of keywords.

> I generated a hundred synthetic tickets from templates. Sixty are about delivery, the rest split between the others, which is my assumption of a typical imbalanced mix. Version one is the baseline. Version two adds one keyword, the word order, to delivery.

**[The result]**

> Delivery tickets improved, from eighty-six point seven percent to a hundred. Great, the new keyword fixed tickets like, where is my order.

> But the word order also appears in refund tickets. Refund went from a hundred percent to fifty. Overall, the score went up by two points, because delivery tickets were the majority.

> The average improved. The product got worse for an important group.

**[The gate says no]**

> The gate has two rules. The overall score must not fall, and no single intent may drop by more than five points. Version two passed the first and failed the second.

> The gate printed blocked and exited with code one. In a pipeline, that failure code stops the merge. No person had to notice anything.

**[Averages hide]**

> The lesson is simple. Averages hide damage. Always score by slice, meaning by type of request, language, customer group, whatever matters. A model that is better on average can be much worse for a minority.

> Also keep a regression suite, a set of cases that must stay at a hundred percent. New capability tests start low, like a hill to climb. When one reaches the top, graduate it into the regression suite.

**[Choosing slices]**

> How do you choose slices? Start from your own failure reports. Group tickets by type of request, by language, by customer tier, by length, and by which tool the answer needed. Any group you would be embarrassed to fail is a slice.

> Give each slice enough test cases to be meaningful. Ten refund tickets can move fifty points on a single mistake, so keep growing the small slices from real production failures.

**[Who grades?]**

> Who does the grading? Start with error analysis. Read real failures and group them. That tells you what to test. Then prefer simple code graders, a program that checks the answer, wherever you can.

> Use a language model as judge only for what code cannot check. Keep judges to yes or no questions, and check them against human labels, so you know the judge itself is trustworthy.

**[Why several trials?]**

> One more trap. A language model can answer differently each time. So an eval that runs each case once is noisy. You run each case several times.

> There are two ways to count. Pass at k asks whether at least one of k runs succeeds. Pass hat k asks whether all of k runs succeed. The first measures can it ever do it. The second measures can I rely on it.

**[Reliability, simulated]**

> I simulated it. Suppose an agent succeeds ninety percent of the time. That sounds great. Run it five times, and the chance that all five succeed is only fifty-nine percent.

> Ten runs, thirty-five percent. And with an eighty percent agent, all ten runs succeed just eleven percent of the time. Reliability falls fast with repeats. I checked both formulas against a hundred thousand simulated tasks, and they matched.

**[The gate in CI]**

> Here is the gate as a pipeline file, a sketch for GitHub. On every pull request, run the unit tests, the data checks, and the evaluation suites. Any step that exits with a failure blocks the merge.

> The same idea works in any C I system. What matters is that the gate is automatic, runs on every change, and cannot be skipped by someone in a hurry.

**[Registries and aliases]**

> A registry answers one question. Which exact version is in production, who approved it, and what did it score? Today a registry tracks more than models. Prompts, judges, test datasets, even tool servers.

> Use aliases, not stages. Instead of moving a model into a production stage, you point a name like champion at one immutable version. Promoting or rolling back is just moving the name.

**[Prompts as versions]**

> Treat prompts like code. A prompt is a template, its variables, and the model settings, stored outside the application. Every change is a new immutable version. You never edit one in place.

> The app fetches the prompt by alias and caches it. So moving the alias is an instant rollback, no redeploy. And every trace records the prompt version, so you can slice failures by version.

**[Model cards]**

> A model card is the label on a model. Short settings at the top, in a few lines. What base model, what data, what licence, what kind of fine tune. Then prose below. What it is for, its limits, how it was trained, how it scored.

> On Hugging Face the model card is simply the readme file. Writing one forces you to say what your model should not be used for.

**[Infrastructure as code]**

> Now the machines. Infrastructure as code means describing your cloud setup in files. Tools called Terraform and OpenTofu create the network, the cluster, the GPU machine pools, the permissions, and the storage.

> A second layer, called GitOps, uses a tool like Argo C D or Flux to keep what runs in the cluster matching what is in Git. A third layer, rollouts, does canary releases with automatic rollback.

**[Why GitOps]**

> Why this style? Git becomes the source of truth and the audit trail. If someone changes the cluster by hand, the tool notices and puts it back. And a rollback is just reverting a commit.

> One more rule from the notebook. Keep your model provider keys out of the state files, using the tools' ephemeral and write only values. A leaked state file should never leak a key.

**[A GPU pool as code]**

> Here is a taste of the code, from the notebook. A pool of spot GPU machines for inference. The minimum is zero, so with no traffic there is no GPU bill. The maximum is four. The machines are spot, so cheaper and interruptible.

> Notice that it ties back to lesson two. Scale to zero, spot, and a GPU taint from lesson three, all in a dozen lines. Check the current provider documentation before using anything like this, because settings change.

**[Canary releases]**

> Now the canary. Even with a good gate, real traffic finds new problems. So you send the new version to a small share of users first, and an automatic check decides whether to continue or roll back.

> I simulated it. Six hundred requests a minute. The old version fails one percent. The new version is bad and fails five percent. Both rates are my assumptions. An automatic check runs every five minutes, and rolls back if failures are far above what one percent predicts.

**[Canary, measured]**

> Release to everyone at once, and about a hundred and fifty bad responses went out before the rollback. A twenty-five percent canary, thirty-eight. A five percent canary, nine point four. A one percent canary, four.

> The rule of thumb is that the damage scales with the share of traffic you expose. A small canary turns a disaster into a footnote.

**[The canary trade-off]**

> But small is not free. With a one percent canary, the very first check caught the problem only forty-five percent of the time. There were not enough requests yet. It took about two point seven checks on average.

> A five percent canary caught it first time seventy-seven percent of the time. Bigger canaries decide faster and expose more users. Pick a share small enough to be safe and big enough to learn quickly.

**[Observability]**

> After release, you watch. For language model apps the unit to watch is the trace, one tree per request, showing each model call, each tool call and each retrieval, with time and cost.

> The tooling market is changing fast. Langfuse was bought by ClickHouse, Promptfoo by OpenAI, and Helicone went into maintenance mode, according to the notebook. So record traces in the open O Tel standard for generative A I, and your backend stays swappable.

**[Online judges]**

> Graders can run on live traffic too. An online judge samples real traces and scores them, for example, did the answer cite a source, or did the user have to ask again. Scores feed dashboards and alerts.

> When a trace fails, save it as a new test case. That closes the loop from earlier. Production teaches the test set.

**[Continuous evaluation]**

> For language model apps that train nothing, the idea of continuous training becomes continuous evaluation. Judges score live traces all the time. Prompt optimisers propose changes. Every candidate passes through the gate before an alias moves.

> A registry hook or an alias change can start the deployment job, which runs a canary with an alarm based rollback. People review the dashboards, not each change.

**[Cost as a limit]**

> One more thing to watch. Cost. For language model apps, the cost per token and per request deserves its own alarm, next to speed. A prompt change that doubles the input length can double the bill overnight.

> Record the cost on every trace, and add a cost check to the gate. Lesson eleven goes deep on this.

**[ShopNest Copilot]**

> For ShopNest Copilot. Prompts live in a registry, with versions and a production alias. Every pull request runs the unit tests, a golden set of tickets scored by slice, and a cost check.

> Infrastructure is code. New versions go to five percent of traffic first, with an automatic rollback. Traces and online judges watch live, and failed traces become new golden cases.

**[Four words to keep]**

> Four words to carry forward. Eval gate: an automatic test that blocks a worse change. Champion and challenger: the current version and the proposed one.

> Canary: sending a little traffic first. And trace: the record of everything one request did.

**[Interview corner]**

> Interview corner. Asked how you ship a prompt change safely, say: version it, run an eval gate that checks the overall score and every slice, canary it on a small share of traffic with automatic rollback, and watch traces. In my toy gate, a change that raised the average by two points was blocked for dropping refunds by fifty.

> Asked why run evaluations several times, say: model output varies, and reliability falls quickly with repeats. A ninety percent agent passes five runs in a row only fifty-nine percent of the time.

**[Your turn]**

> Your turn. The zip for this lesson has three scripts. The eval gate, the trials calculator, and the canary simulator. Change the keyword list so the gate passes, or change the canary share.

> Try adding a keyword to refund tickets that fixes the problem, and watch the gate go green. One changed number teaches more than an hour of reading.

**[Recap]**

> Recap. Ship the pipeline, not just the model. Run a gate on every change, by slice, because averages hide damage. My toy gate blocked a plus two point change that cost refunds fifty points. Run several trials, since a ninety percent agent passes five runs only fifty-nine percent of the time.

> Move aliases, not code, to promote and roll back. Canary small, and the damage in my simulation fell from about a hundred and fifty bad responses to nine. Next lesson: G E N A I app architecture. R A G, agents and tools.

**[Next lesson]**

> In the next lesson: generative A I apps. Starting with rag, from documents to cited answers.

> Subscribe so you don't miss it. See you in the notebook.


## Short 1: My Prompt Change Raised the Score and a Gate Still Blocked It #shorts

> I changed a prompt and the score went up. A simple gate blocked it anyway. Here is why.

> On a toy model with synthetic tickets, my prompt change lifted the overall score from ninety to ninety-two percent. But refund tickets fell from a hundred percent to fifty.

> An eval gate, which also checks every slice, blocked it automatically. The toy model is a stand in, but the gate logic is real.

> Averages hide damage. Score every slice.


## Short 2: A 90% Reliable AI Agent Passes 5 Runs in a Row Only 59% of the Time #shorts

> An agent that works ninety percent of the time passes five runs in a row only fifty-nine percent of the time.

> Pass at k asks whether at least one run works. Pass hat k asks whether all of them do. For a ninety percent agent, the second is just point nine to the power of k.

> Five runs, fifty-nine percent. Ten runs, thirty-five. I checked the formulas against a hundred thousand simulated tasks. The ninety percent is my assumption.

> Reliability falls fast with repeats. Test several runs.


## Instagram Reel 1: A 5% canary cut the damage of a bad release 16x

> How a five percent canary cut the damage of a bad release by about sixteen times.

> I simulated a release that fails five percent of requests instead of one. Sent to everyone at once, about a hundred and fifty bad responses before the rollback. As a five percent canary, nine.

> Small first. Save this.
