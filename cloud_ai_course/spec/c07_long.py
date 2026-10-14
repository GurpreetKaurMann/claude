import sys; sys.path.insert(0, '/home/claude/caigen')
from frag import *
from gailab import CODE, OUT

LONG = [
 dict(id='s0', chap='A better score that broke refunds', say=[
   "I changed one prompt. The overall score went up, from ninety percent to ninety-two. Everyone would have shipped it. But one group of customers got much worse. Refund tickets fell from a hundred percent right to fifty.",
   "A simple automatic check, an eval gate, caught it and blocked the change. This lesson is about shipping A I changes safely, again and again, without breaking what already works."],
  html=[H2('Score up 2 points. Refunds down 50.', 0),
        DEF('overall <b>90% → 92%</b> · refund tickets <b>100% → 50%</b> · gate: <b>BLOCKED</b>', 0, 0.5, style='margin-top:24px;font-size:48px'),
        MARK('a toy model, a real gate · synthetic tickets', 1, 0.6)]),

 dict(id='s1', chap='Where we are', say=[
   "So far we built the pieces of an A I system. Now we run it as a product. That means changing it often, without breaking it, and knowing quickly when something goes wrong.",
   "That discipline has two names. M L Ops for classic models, and L L M Ops for language model apps. As always I label my experiments. The eval gate uses a toy keyword model as a stand in for a language model, with synthetic tickets. The canary and trials results are simulations."],
  html=[H2('Shipping AI like a product', 0),
        GRID([('MLOps: classic models', 0, 0.3), ('LLMOps: language model apps', 0, 0.8)], cols=2, h=170, fs=40),
        STICKY('Honest label', 'toy model + synthetic tickets · canary and trials are <b>simulations</b>', 1, 0.5, style='margin-top:26px;font-size:36px')]),

 dict(id='s2', chap='Three maturity levels', say=[
   "Classic M L Ops has three levels, from a well known Google guide. Level zero is everything by hand. Notebooks, a model handed over to an engineer, and nobody watching afterwards.",
   "Level one automates the training. A pipeline retrains the model on fresh data by itself, when new data arrives, on a schedule, or when performance drops.",
   "Level two automates the shipping of that pipeline. The pipeline code itself is tested and deployed like any other service."],
  html=[H2('Three levels of MLOps', 0), SVG('c2', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c2', 'levels', 1000, 290, 1)]),

 dict(id='s3', chap='LLMOps is different', say=[
   "Language model apps change the picture. Often you train nothing. You call a hosted model. So what do you version? The prompts. The model and its settings. The tools the model may call. The retrieval index. And the code that wraps it all.",
   "Quality is no longer one accuracy number. It is a set of evaluations, plus checks on live traffic. The thing you watch is the trace of one request. And the same input can give different outputs, so you must run several trials."],
  html=[H2('What LLMOps versions', 0),
        LIST([('prompts and model settings', 0, 0.4), ('tools the model may call', 0, 0.9), ('the retrieval index', 0, 1.3), ('the code that wraps it', 0, 1.7)], kind='ar', style='margin-top:22px;font-size:42px'),
        SUB('quality = evals + live checks · the unit to watch = the trace', 1, 0.6, style='margin-top:16px')]),

 dict(id='s3b', chap='Models decay silently', say=[
   "There is one more reason for all this. Models decay without anyone touching them. The world changes, customers write differently, new products appear, and the model's inputs drift away from what it saw in training.",
   "Without monitoring, nothing crashes. The answers just get slowly worse. That is why level zero is so risky. Classic M L Ops watches the distribution of inputs and the quality of outputs, and retrains when they move too far."],
  html=[H2('Models decay silently', 0),
        LIST([('the world changes, inputs drift', 0, 0.4), ('nothing crashes, answers just get worse', 0, 1.0), ('watch inputs and outputs, retrain when they move', 1, 0.4)], kind='ar', style='margin-top:26px;font-size:46px')]),

 dict(id='s4', chap='The release loop', say=[
   "Here is the loop to build. Make a change, to a prompt or a model. Score the whole test set with an eval gate. Send a little traffic to the new version first, called a canary.",
   "Then watch it with traces and automatic judges on live requests. When something fails in production, turn that failure into a new test case. Every change is then scored against everything that ever went wrong.",
   "That last arrow is the whole point. The loop gets harder to fool every week."],
  html=[H2('The release loop', 0), SVG('c4', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c4', 'loop', 1000, 290, 1)]),

 dict(id='s5', chap='Three layers of tests', say=[
   "Testing an A I system has three layers, and each catches a different break. Code tests, the normal kind. Do the functions work and do the parts fit together?",
   "Data and model tests. Does training converge, are there missing values, does the data still look like the reference data? And evaluation suites for language models, where graders score answers on a fixed, golden set of examples.",
   "Run all three on every change. A failure in any layer blocks the merge."],
  html=[H2('Three layers of tests', 0), SVG('c5', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c5', 'layers', 1000, 290, 1)]),

 dict(id='s6', chap='What a gate checks', say=[
   "An eval gate is the check that stands between a change and production. It asks several questions. Does the challenger beat the current champion by a real margin, not just match it?",
   "Does any important slice get worse, meaning a group of cases such as refunds? Are the speed and size limits met? And does the model actually load and serve in a test container? Only if every answer is yes does the change move on."],
  html=[H2('What a gate checks', 0),
        LIST([('challenger beats champion by a margin', 0, 0.4), ('no important slice gets worse', 0, 0.9), ('speed and size limits are met', 1, 0.3), ('it loads and serves in a test container', 1, 0.8)], kind='ok', style='margin-top:26px;font-size:44px')]),

 dict(id='s7', chap='My toy gate', say=[
   "I built a working gate. The task is to route a support ticket to an intent, refund, delivery, account or product. The model is a toy. A keyword scorer. It is a stand in for a language model, and the prompt is its list of keywords.",
   "I generated a hundred synthetic tickets from templates. Sixty are about delivery, the rest split between the others, which is my assumption of a typical imbalanced mix. Version one is the baseline. Version two adds one keyword, the word order, to delivery."],
  html=[H2('A working gate, on a toy model', 0),
        OUT(['task: route a ticket to refund / delivery / account / product', 'model: a keyword scorer (a stand-in, not a language model)', '100 synthetic tickets, 60 about delivery', 'v2 = v1 + the word "order" counts as delivery'], 0, 0.4, size=28, label='setup', style='margin-top:20px'),
        SUB('toy model · synthetic data · real gate logic', 1, 0.6, style='margin-top:14px')]),

 dict(id='s8', chap='The result', say=[
   "Delivery tickets improved, from eighty-six point seven percent to a hundred. Great, the new keyword fixed tickets like, where is my order.",
   "But the word order also appears in refund tickets. Refund went from a hundred percent to fifty. Overall, the score went up by two points, because delivery tickets were the majority.",
   "The average improved. The product got worse for an important group."],
  html=[H2('Better on average, worse for refunds', 0), SVG('c8', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c8', 'gate', 1000, 290, 1)]),

 dict(id='s9', chap='The gate says no', say=[
   "The gate has two rules. The overall score must not fall, and no single intent may drop by more than five points. Version two passed the first and failed the second.",
   "The gate printed blocked and exited with code one. In a pipeline, that failure code stops the merge. No person had to notice anything."],
  html=[H2('The gate decides', 0),
        OUT(['GATE: BLOCKED: refund dropped 50.0 points', 'exit code: 1'], 0, 0.4, size=38, label='measured output', style='margin-top:26px'),
        STICKY('Rule', 'overall must not fall · <b>no slice</b> may drop &gt; 5 points', 1, 0.5, style='margin-top:26px;font-size:40px')]),

 dict(id='s10', chap='Averages hide', say=[
   "The lesson is simple. Averages hide damage. Always score by slice, meaning by type of request, language, customer group, whatever matters. A model that is better on average can be much worse for a minority.",
   "Also keep a regression suite, a set of cases that must stay at a hundred percent. New capability tests start low, like a hill to climb. When one reaches the top, graduate it into the regression suite."],
  html=[H2('Averages hide damage', 0),
        LIST([('score by slice, not just overall', 0, 0.4), ('regression suite: must stay at ~100%', 1, 0.3), ('capability tests: a hill to climb, then graduate', 1, 0.8)], kind='ar', style='margin-top:26px;font-size:46px')]),

 dict(id='s10b', chap='Choosing slices', say=[
   "How do you choose slices? Start from your own failure reports. Group tickets by type of request, by language, by customer tier, by length, and by which tool the answer needed. Any group you would be embarrassed to fail is a slice.",
   "Give each slice enough test cases to be meaningful. Ten refund tickets can move fifty points on a single mistake, so keep growing the small slices from real production failures."],
  html=[H2('Choosing slices', 0),
        LIST([('type of request, language, customer tier', 0, 0.4), ('length, and which tool was needed', 0, 1.0), ('any group you would hate to fail', 0, 1.5), ('enough cases per slice: grow from production failures', 1, 0.4)], kind='ar', style='margin-top:24px;font-size:42px')]),

 dict(id='s11', chap='Who grades?', say=[
   "Who does the grading? Start with error analysis. Read real failures and group them. That tells you what to test. Then prefer simple code graders, a program that checks the answer, wherever you can.",
   "Use a language model as judge only for what code cannot check. Keep judges to yes or no questions, and check them against human labels, so you know the judge itself is trustworthy."],
  html=[H2('Who grades the answers?', 0),
        LIST([('1. read real failures first (error analysis)', 0, 0.4), ('2. code graders where you can', 0, 0.9), ('3. LLM judge only for the rest', 1, 0.3), ('yes/no judges, checked against humans', 1, 0.8)], kind='ar', style='margin-top:26px;font-size:44px')]),

 dict(id='s12', chap='Why several trials?', say=[
   "One more trap. A language model can answer differently each time. So an eval that runs each case once is noisy. You run each case several times.",
   "There are two ways to count. Pass at k asks whether at least one of k runs succeeds. Pass hat k asks whether all of k runs succeed. The first measures can it ever do it. The second measures can I rely on it."],
  html=[H2('Run each case several times', 0),
        ROW(COL(CARD('<b>pass@k</b><br>at least one of k runs works<br>can it ever do it?', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>pass^k</b><br>all k runs work<br>can I rely on it?', 1, 0.3, style='font-size:38px'), width='48%'), style='margin-top:28px'),
        SUB('formulas: 1 − (1 − p)^k and p^k', 1, 1.0, style='margin-top:14px')]),

 dict(id='s13', chap='Reliability, simulated', say=[
   "I simulated it. Suppose an agent succeeds ninety percent of the time. That sounds great. Run it five times, and the chance that all five succeed is only fifty-nine percent.",
   "Ten runs, thirty-five percent. And with an eighty percent agent, all ten runs succeed just eleven percent of the time. Reliability falls fast with repeats. I checked both formulas against a hundred thousand simulated tasks, and they matched."],
  html=[H2('A 90% agent, run again and again', 0), SVG('c13', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c13', 'trials', 1000, 300, 1)]),

 dict(id='s14', chap='The gate in CI', say=[
   "Here is the gate as a pipeline file, a sketch for GitHub. On every pull request, run the unit tests, the data checks, and the evaluation suites. Any step that exits with a failure blocks the merge.",
   "The same idea works in any C I system. What matters is that the gate is automatic, runs on every change, and cannot be skipped by someone in a hurry."],
  html=[H2('The gate as a CI file (sketch)', 0),
        CODE(['on: pull_request', 'jobs:', '  test-and-eval:', '    steps:', '      - run: pytest tests/unit          # code', '      - run: python checks/data_suite.py  # data', '      - run: deepeval test run tests/    # LLM evals'], 0, 0.3, step=0.8, size=26, hl=False, lang='yaml', style='margin-top:16px'),
        SUB('any non-zero exit blocks the merge', 1, 1.0, style='margin-top:12px')]),

 dict(id='s15', chap='Registries and aliases', say=[
   "A registry answers one question. Which exact version is in production, who approved it, and what did it score? Today a registry tracks more than models. Prompts, judges, test datasets, even tool servers.",
   "Use aliases, not stages. Instead of moving a model into a production stage, you point a name like champion at one immutable version. Promoting or rolling back is just moving the name."],
  html=[H2('Registry: which version is live?', 0),
        LIST([('models, prompts, judges, datasets, tool servers', 0, 0.4), ('every version immutable', 0, 1.0), ('an alias like "champion" points at one', 1, 0.4), ('promote or roll back = move the alias', 1, 1.0)], kind='ar', style='margin-top:24px;font-size:42px')]),

 dict(id='s16', chap='Prompts as versions', say=[
   "Treat prompts like code. A prompt is a template, its variables, and the model settings, stored outside the application. Every change is a new immutable version. You never edit one in place.",
   "The app fetches the prompt by alias and caches it. So moving the alias is an instant rollback, no redeploy. And every trace records the prompt version, so you can slice failures by version."],
  html=[H2('Prompts: versions and an alias', 0), SVG('c16', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c16', 'alias', 1000, 290, 1)]),

 dict(id='s17', chap='Model cards', say=[
   "A model card is the label on a model. Short settings at the top, in a few lines. What base model, what data, what licence, what kind of fine tune. Then prose below. What it is for, its limits, how it was trained, how it scored.",
   "On Hugging Face the model card is simply the readme file. Writing one forces you to say what your model should not be used for."],
  html=[H2('A model card: the label', 0),
        OUT(['license: apache-2.0', 'base_model: BASE_MODEL', 'datasets: [your-data]', 'tags: [support, lora]'], 0, 0.4, size=34, label='top of the card (sketch)', style='margin-top:22px'),
        SUB('then: intended use, limits, training, results', 1, 0.6, style='margin-top:16px')]),

 dict(id='s18', chap='Infrastructure as code', say=[
   "Now the machines. Infrastructure as code means describing your cloud setup in files. Tools called Terraform and OpenTofu create the network, the cluster, the GPU machine pools, the permissions, and the storage.",
   "A second layer, called GitOps, uses a tool like Argo C D or Flux to keep what runs in the cluster matching what is in Git. A third layer, rollouts, does canary releases with automatic rollback."],
  html=[H2('Infrastructure as code', 0), SVG('c18', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c18', 'iac', 1000, 290, 1)]),

 dict(id='s19', chap='Why GitOps', say=[
   "Why this style? Git becomes the source of truth and the audit trail. If someone changes the cluster by hand, the tool notices and puts it back. And a rollback is just reverting a commit.",
   "One more rule from the notebook. Keep your model provider keys out of the state files, using the tools' ephemeral and write only values. A leaked state file should never leak a key."],
  html=[H2('Why GitOps', 0),
        LIST([('git = source of truth + audit trail', 0, 0.4), ('manual drift gets undone automatically', 0, 1.0), ('rollback = git revert', 0, 1.5), ('keep API keys out of state files', 1, 0.4)], kind='ar', style='margin-top:24px;font-size:44px')]),

 dict(id='s20', chap='A GPU pool as code', say=[
   "Here is a taste of the code, from the notebook. A pool of spot GPU machines for inference. The minimum is zero, so with no traffic there is no GPU bill. The maximum is four. The machines are spot, so cheaper and interruptible.",
   "Notice that it ties back to lesson two. Scale to zero, spot, and a GPU taint from lesson three, all in a dozen lines. Check the current provider documentation before using anything like this, because settings change."],
  html=[H2('A spot GPU pool in code (sketch)', 0),
        CODE(['resource "google_container_node_pool" "l4_infer" {', '  autoscaling {', '    min_node_count = 0   # no traffic, no GPU bill', '    max_node_count = 4', '  }', '  node_config { spot = true }', '}'], 0, 0.3, step=0.8, size=26, hl=False, lang='sh', style='margin-top:16px'),
        SUB('illustrative: check the provider docs before use', 1, 1.0, style='margin-top:12px')]),

 dict(id='s21', chap='Canary releases', say=[
   "Now the canary. Even with a good gate, real traffic finds new problems. So you send the new version to a small share of users first, and an automatic check decides whether to continue or roll back.",
   "I simulated it. Six hundred requests a minute. The old version fails one percent. The new version is bad and fails five percent. Both rates are my assumptions. An automatic check runs every five minutes, and rolls back if failures are far above what one percent predicts."],
  html=[H2('A canary: a little traffic first', 0),
        OUT(['600 requests per minute', 'old version fails 1% · NEW version fails 5% (assumed)', 'check every 5 min · roll back if z > 3', '2,000 simulated releases per setting'], 0, 0.4, size=30, label='simulation setup', style='margin-top:22px'),
        SUB('a simulation with assumed rates', 1, 0.6, style='margin-top:14px')]),

 dict(id='s22', chap='Canary, measured', say=[
   "Release to everyone at once, and about a hundred and fifty bad responses went out before the rollback. A twenty-five percent canary, thirty-eight. A five percent canary, nine point four. A one percent canary, four.",
   "The rule of thumb is that the damage scales with the share of traffic you expose. A small canary turns a disaster into a footnote."],
  html=[H2('Bad responses before the rollback', 0), SVG('c22', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c22', 'canary_bad', 1000, 290, 1)]),

 dict(id='s23', chap='The canary trade-off', say=[
   "But small is not free. With a one percent canary, the very first check caught the problem only forty-five percent of the time. There were not enough requests yet. It took about two point seven checks on average.",
   "A five percent canary caught it first time seventy-seven percent of the time. Bigger canaries decide faster and expose more users. Pick a share small enough to be safe and big enough to learn quickly."],
  html=[H2('Small is safe, but slow to prove', 0), SVG('c23', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c23', 'canary_first', 1000, 300, 1)]),

 dict(id='s24', chap='Observability', say=[
   "After release, you watch. For language model apps the unit to watch is the trace, one tree per request, showing each model call, each tool call and each retrieval, with time and cost.",
   "The tooling market is changing fast. Langfuse was bought by ClickHouse, Promptfoo by OpenAI, and Helicone went into maintenance mode, according to the notebook. So record traces in the open O Tel standard for generative A I, and your backend stays swappable."],
  html=[H2('Watch the trace', 0),
        LIST([('one tree per request: model, tools, retrieval', 0, 0.4), ('with time and cost on every step', 0, 1.0), ('record in the open OTel GenAI standard', 1, 0.4), ('so the backend stays swappable', 1, 1.0)], kind='ar', style='margin-top:24px;font-size:44px'),
        SUB('tool market news: notebook, Oct 2026', 1, 1.5, style='margin-top:14px')]),

 dict(id='s25', chap='Online judges', say=[
   "Graders can run on live traffic too. An online judge samples real traces and scores them, for example, did the answer cite a source, or did the user have to ask again. Scores feed dashboards and alerts.",
   "When a trace fails, save it as a new test case. That closes the loop from earlier. Production teaches the test set."],
  html=[H2('Judges on live traffic', 0),
        LIST([('sample real traces, score them', 0, 0.4), ('dashboards and alerts on the scores', 0, 1.0), ('failures become new test cases', 1, 0.4)], kind='ar', style='margin-top:26px;font-size:46px'),
        STICKY('The loop', 'production teaches the <b>test set</b>', 1, 0.8, style='margin-top:24px;font-size:42px')]),

 dict(id='s25b', chap='Continuous evaluation', say=[
   "For language model apps that train nothing, the idea of continuous training becomes continuous evaluation. Judges score live traces all the time. Prompt optimisers propose changes. Every candidate passes through the gate before an alias moves.",
   "A registry hook or an alias change can start the deployment job, which runs a canary with an alarm based rollback. People review the dashboards, not each change."],
  html=[H2('Continuous evaluation', 0),
        LIST([('judges score live traces all the time', 0, 0.4), ('optimisers propose changes', 0, 1.0), ('every candidate passes the gate first', 0, 1.5), ('alias moves start a canary with auto-rollback', 1, 0.4)], kind='ar', style='margin-top:24px;font-size:42px')]),

 dict(id='s26', chap='Cost as a limit', say=[
   "One more thing to watch. Cost. For language model apps, the cost per token and per request deserves its own alarm, next to speed. A prompt change that doubles the input length can double the bill overnight.",
   "Record the cost on every trace, and add a cost check to the gate. Lesson eleven goes deep on this."],
  html=[H2('Cost is a quality metric', 0),
        LIST([('cost per request: an alarm, like latency', 0, 0.4), ('a longer prompt can double the bill overnight', 0, 1.0), ('record cost on every trace · cost check in the gate', 1, 0.4)], kind='ar', style='margin-top:26px;font-size:44px')]),

 dict(id='s27', chap='ShopNest Copilot', say=[
   "For ShopNest Copilot. Prompts live in a registry, with versions and a production alias. Every pull request runs the unit tests, a golden set of tickets scored by slice, and a cost check.",
   "Infrastructure is code. New versions go to five percent of traffic first, with an automatic rollback. Traces and online judges watch live, and failed traces become new golden cases."],
  html=[H2('ShopNest Copilot: shipping plan', 0),
        TABLE(['Piece', 'Plan'], [(['prompts', 'registry, versions, "production" alias'], 0, 0.4), (['pull request', 'unit tests + golden set by slice + cost check'], 0, 1.0), (['release', '5% canary, automatic rollback'], 1, 0.3), (['watch', 'traces + online judges → new golden cases'], 1, 0.9)], style='margin-top:22px;font-size:38px')]),

 dict(id='s28', chap='Four words to keep', say=[
   "Four words to carry forward. Eval gate: an automatic test that blocks a worse change. Champion and challenger: the current version and the proposed one.",
   "Canary: sending a little traffic first. And trace: the record of everything one request did."],
  html=[H2('Four words to keep', 0),
        GRID([('<b>eval gate</b>', 0, 0.3), ('<b>champion / challenger</b>', 0, 0.9), ('<b>canary</b>', 1, 0.3), ('<b>trace</b>', 1, 0.9)], cols=2, h=140, fs=42, style='margin-top:30px')]),

 dict(id='s29', chap='Interview corner', say=[
   "Interview corner. Asked how you ship a prompt change safely, say: version it, run an eval gate that checks the overall score and every slice, canary it on a small share of traffic with automatic rollback, and watch traces. In my toy gate, a change that raised the average by two points was blocked for dropping refunds by fifty.",
   "Asked why run evaluations several times, say: model output varies, and reliability falls quickly with repeats. A ninety percent agent passes five runs in a row only fifty-nine percent of the time."],
  html=[H2('Interview corner', 0),
        Q('How do you ship a prompt change safely?', 'Version it, eval gate (overall + every slice), small canary with auto rollback, watch traces.', 0, 0.4),
        Q('Why run evals several times?', 'Outputs vary. A 90% agent passes 5 runs in a row only 59% of the time.', 1, 0.4)]),

 dict(id='s30', chap='Your turn', say=[
   "Your turn. The zip for this lesson has three scripts. The eval gate, the trials calculator, and the canary simulator. Change the keyword list so the gate passes, or change the canary share.",
   "Try adding a keyword to refund tickets that fixes the problem, and watch the gate go green. One changed number teaches more than an hour of reading."],
  html=[H2('Your turn', 0),
        CARD('<b>l07_eval_gate.py</b>: fix version 2 so the gate passes.<br><b>l07_trials.py</b>: pass@k and pass^k.<br><b>l07_canary_sim.py</b>: change the canary share.', 0, 0.4, style='margin-top:22px;font-size:38px'),
        SUB('one changed number teaches more than an hour of reading', 1, 0.8, style='margin-top:16px')]),

 dict(id='s31', chap='Recap', say=[
   "Recap. Ship the pipeline, not just the model. Run a gate on every change, by slice, because averages hide damage. My toy gate blocked a plus two point change that cost refunds fifty points. Run several trials, since a ninety percent agent passes five runs only fifty-nine percent of the time.",
   "Move aliases, not code, to promote and roll back. Canary small, and the damage in my simulation fell from about a hundred and fifty bad responses to nine. Next lesson: G E N A I app architecture. R A G, agents and tools."],
  html=[H2('Recap', 0),
        GRID([('gate by slice: averages hide', 0, 0.3), ('toy gate: +2 overall, −50 refund', 0, 0.9), ('90% agent: all 5 runs = 59%', 0, 1.5),
              ('promote = move an alias', 1, 0.3), ('canary 5%: 150 → 9 bad', 1, 0.9), ('traces + online judges', 1, 1.5)], cols=3, h=150, fs=30)]),
]
