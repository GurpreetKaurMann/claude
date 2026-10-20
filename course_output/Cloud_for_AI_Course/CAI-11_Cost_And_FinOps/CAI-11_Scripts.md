# CAI-11 · Cost and FinOps: Scripts

**Lesson 11 of 12 · Module 5 · Safe, cheap, and your career**

Voice: AI narrator (Kokoro `af_heart`). Final lesson video length: 19:04.

## Long video narration

**[A three dollar GPU]**

> A G P U listed at three dollars seventeen an hour can really cost sixty-three dollars forty. Same machine, same invoice. The only thing that changed is how much of the time it was doing useful work. And one line in a prompt can triple an A P I bill without changing a single answer.

> This is the cost lesson. Every number comes from arithmetic on the notebook's prices, or from a small test I ran. You will leave knowing where the money goes and which lever to pull first.

**[Intro]**

> Welcome to lesson eleven of the cloud for A I engineers course, on The Code Notebook.

> The handwritten notes and the code for this lesson are linked in the description.

**[Where we are]**

> We built, trained, served, shipped and secured the assistant. Now someone has to pay for it. The surprise in A I costs is that the biggest waste is rarely the price per hour. It is hours that nobody was using, and tokens that were sent again and again.

> Honest labels. Prices are the notebook's approximate list prices from September and October twenty twenty-six, and they move often. The sums are arithmetic. The cache test uses a toy cache I wrote. The alert test uses invented logs.

**[The Fin Ops loop]**

> Fin Ops means engineering, finance and product sharing ownership of cloud spend, so cost becomes a design input, like latency. It runs as a loop. Inform, optimise, operate. Inform is seeing the spend, tagging G P Us and metering tokens per team and feature.

> Optimise fixes the rate and the amount used. Operate keeps it fixed with budgets and alerts. A memory hook is I, O, O. See it, fix it, keep it fixed. You cannot optimise what you have not allocated, and savings do not last without alerts.

**[Measure the right thing]**

> First, measure utilisation honestly. The number you see in nvidia dash smi says what share of the last second had at least one kernel running. A tiny kernel on a single processing block reads the same as one filling the whole chip. So a G P U can show one hundred percent while most of it sits idle.

> Better is the D C G M profiling field called S M active, the fraction of time warps were running, averaged over all the processing blocks. Watch S M active, occupancy, and tensor pipe activity. Above eighty percent S M active is necessary, not sufficient.

**[How idle is normal]**

> How idle is normal? A vendor study of tens of thousands of Kubernetes clusters that nobody had optimised found average G P U use around five percent. That is vendor telemetry, so treat it as a warning, not a law. A survey of five hundred seventy-three leaders found eighty-six percent of enterprises with their own G P Us report fifty percent or less.

> Another survey found forty-four percent assign G P Us by hand or have no strategy. So if your cluster looks busy on a dashboard, check which number the dashboard shows. Then fix idle capacity, because that is the biggest lever.

**[The real price]**

> The real price of a G P U hour is the list price divided by utilisation. At the three dollar seventeen index price, five percent use makes a useful hour cost sixty-three dollars forty. Twenty-two percent, fourteen forty-one. Fifty percent, six thirty-four. Eighty percent, three ninety-six.

> Going from five to fifty percent makes a useful hour ten times cheaper. The best rate discounts top out around two or three times. So fix idle time before you negotiate price. A three dollar H one hundred at five percent is a sixty-three dollar H one hundred.

**[Right size, then share]**

> Right size next. If weights and the memory cache fit in ten to twenty gigabytes, a full eighty gigabyte card is oversized. A seven billion parameter model at eight bit or four bit with modest traffic fits a small slice, or a cheaper card like an L four or L forty S class part.

> There are three ways to share. M I G cuts hardware slices with their own memory and fault isolation, up to seven per card, good for production multi tenant serving. Time slicing lets pods take turns with no isolation, fine for trusted development. M P S runs kernels together, for trusted workloads.

**[Ways to buy a GPU]**

> How you buy matters too. On demand has no commitment and is the baseline, good for bursty experiments. Neoclouds offer a lower list price and the newest chips first. Reserved commitments give a lower rate for steady load. Capacity blocks guarantee a cluster for a fixed window, which is not a discount.

> Spot or preemptible capacity is half to seventy percent off, with notice before eviction of two minutes on A W S, and thirty seconds on Azure and Google. Flex start queues your job until capacity frees. Every option has a catch. Pick by workload shape.

**[The commitment rule]**

> The commitment rule is simple. A commitment at discount d wins only if you use more than one minus d of the committed capacity. At a forty percent discount you need more than sixty percent use. At fifty-five percent for three years, more than forty-five percent.

> I checked it with arithmetic. At a forty percent discount, fifty percent use makes the commitment lose, and seventy percent makes it win. A discount of d buys you the right to waste d. With volatile prices, shorter terms limit the risk of being locked in above market.

**[One run, five ways]**

> Here is one training run. Sixty-four H one hundreds for fourteen days is twenty-one thousand five hundred and four G P U hours. At the index price of three seventeen it costs sixty-eight thousand dollars. At the market average, eighty-three thousand.

> As an A W S capacity block, about one hundred twenty-eight thousand. At hyperscaler on demand, about one hundred forty-eight thousand. Spot at sixty percent off is twenty-seven thousand before lost steps and restarts. Same job, a spread of five point four times. Buying is an engineering decision.

**[The token bill]**

> Now tokens. An A P I bill is a sum over token types. Uncached input at the input price. Cache writes at a premium. Cache reads at a fraction. And output tokens, including thinking, at the output price. Batch jobs cost half. Some regional options add ten percent.

> The shape is the same across vendors. Output costs about five to six times input. Cache reads cost a tenth of input or less. Batch is half. So the question is never just the price per million. It is how many tokens of each kind each request uses.

**[A real price table]**

> Here are list prices per million tokens from the notebook, October fourteenth, twenty twenty-six. Opus five point five costs four dollars in and twenty out. Sonnet five point five, two in and ten out. Haiku five point five, ten cents in and fifty cents out.

> Cache reads are five percent of input on Opus and Sonnet, and ten percent on Haiku. Writing a five minute cache costs one and a quarter times input. These figures change, so treat the table as an example of the shape, and check the vendor page before budgeting.

**[A support bot, costed]**

> Let me cost the support bot. Each request has a three thousand token system prompt that can be cached, a thousand uncached tokens of history and question, and four hundred tokens of output. On Sonnet five point five with no cache, that is one point two cents, twelve thousand dollars per million requests.

> When the cache hits, it drops to six thousand three hundred. A cascade, where Haiku answers first and thirty percent go to Sonnet, is four thousand two hundred. Batch on top of a cache hit is three thousand one hundred fifty. The model tier moves the bill most, then caching, then batch.

**[Lever one: caching]**

> Caching is lever one. A five minute cache write costs one and a quarter times the input price, and a read costs a tenth or twentieth. So a five minute cache pays back after a single read, and a one hour cache after two. Vendors report agent loops reading a median eighty-four percent of input from cache.

> In my arithmetic the cache hit saved forty-seven point five percent per request. And at a hit rate of fifty percent the bill is nine thousand nine hundred per million, at eighty percent seven thousand seven hundred forty, at ninety-five percent six thousand six hundred sixty.

**[Does the cache hit?]**

> A cache only helps if requests keep arriving. If requests share a prefix at a steady rate, the hit rate is one minus e to the minus rate times lifetime. I simulated random arrivals to check. One request a minute with a five minute lifetime hit ninety-nine point two percent of the time.

> One request every ten minutes hit thirty-eight point nine percent, and one an hour only eight percent. The formula agreed within a point. So a quiet feature can pay for cache writes and never get the reads. Measure the real hit rate, then decide the lifetime.

**[The timestamp mistake]**

> Here is the mistake that triples bills. A cache matches the start of a prompt. If a timestamp or user name sits at the very top of the system prompt, every request starts differently, and nothing is ever reused. I wrote a toy prefix cache and fed it five thousand requests.

> With the timestamp on top, zero percent of tokens were served from cache. With the same timestamp after the shared part, seventy-five percent were. The input bill was three and a half times higher. Rule. Stable text first, changing text last.

**[Lever two: batch]**

> Lever two is batch. Batch processing takes fifty percent off every token, including cached ones, in exchange for waiting up to twenty-four hours. It is the second biggest free lever after caching.

> Anything that does not need an instant answer belongs there. Offline evaluation runs, backfills, nightly labelling, summarising yesterday's tickets. On the support bot, batch on top of a cache hit halves the three thousand per million again.

**[Levers three and four]**

> Levers three and four are the prompt audit and effort. Trim what you send. Searching a tool list instead of sending all five hundred tools cut input forty-five percent in a published test. Pruning stale tool results saved thirty-nine, and a plain prompt audit fourteen.

> Effort is a price dial. On one benchmark, a cheaper model at high effort solved nearly as many tasks as a bigger one at low effort, at about the same cost. Running everything at low effort and re-running failures at high saved about forty percent, but only if you can detect a failure, like a failing test.

**[Lever five: routing]**

> Lever five comes last. Routing sends easy requests to a cheap model and hard ones to a big model. In the notebook's sum, Haiku first with thirty percent escalated to Sonnet cuts sixty-five percent against all Sonnet. That holds only if the escalation classifier is reliable.

> Quality on the easy seventy percent must stay acceptable. Caches are per model. And escalated requests pay twice. So compare against the best single model at lower effort with caching. Routing is the most common lever in industry, and the one most often done before the cheaper ones.

**[Self-host: the formula]**

> Should you host the model yourself? Start with the formula. Dollars per million tokens equals the G P U price per hour, divided by tokens per second times three thousand six hundred times utilisation, times a million. A seventy billion model at eight bit on one H one hundred does about four hundred tokens a second, a vendor figure likely conservative.

> At full use that is two dollars twenty per million tokens. At sixty percent, three sixty-seven. At forty percent, five fifty. At fifteen percent, fourteen sixty-eight. Utilisation again decides everything, and production use is often thirty to sixty percent.

**[The break-even volume]**

> Now the break-even volume. One H one hundred running all day costs seventy-six dollars eight cents. Divide by the A P I blended price. Against Opus, self hosting can win above ten point six million tokens a day. Against Sonnet, above twenty-one point one million, with a narrow window, because one card tops out at thirty-four point six million.

> Against Haiku, the break even is four hundred twenty-three million tokens a day, far beyond what one card can serve. So one H one hundred never beats a Haiku class A P I on G P U cost alone. Self hosting only competes with premium models.

**[Self-host: what the sum hides]**

> I also simulated a year of bursty traffic, averaging twenty million tokens a day, with one fixed G P U serving the base load and the A P I taking overflow. The hybrid cost thirty-one thousand six hundred seventy-eight dollars, against thirty-one thousand nine hundred nine for all A P I. Basically a tie, before any people.

> And the sum leaves things out. On call time, upgrades, spare replicas, and the weaker quality of an open model, which makes cost per successful task the fair test. The simple sum flatters self hosting. Price a hosted open model and a batch cached A P I first.

**[Who spent it?]**

> Now attribution. G P U cost can use cloud tags, Kubernetes labels, and a cost allocation tool. Tokens have no resource tags, so a gateway stamps team, feature and tenant on every request. Give each project its own key or workspace. And capture usage when the request happens, before billing aggregates it away.

> Agents fan out, so join calls with a trace identifier. Log the token counts, and compute the dollar cost at log time from a versioned price table. Never recompute old history with today's prices, and reconcile against the provider's cost report each month.

**[Showback and cost per ticket]**

> With stamped logs, you can report. Showback shows each team its cost with no payment enforced, and is the place to start. Chargeback lands the cost on the team's budget, once allocation rules are stable. In my invented logs, the triage bot cost about twenty-seven dollars a day, the order lookup six, and the refund agent a hundred and fourteen.

> The number that matters is cost per resolved ticket. Cost per conversation divided by the resolve rate. For the triage bot that came to about six cents, the lookup under one cent, the refund agent seventeen cents. Put it next to the cost of a human, and you show value, not just spend.

**[Budgets and alerts]**

> Operate means budgets and alarms. Set a monthly budget per workspace, alert at fifty, eighty and one hundred percent, and put hard spend caps at the gateway to stop a runaway agent. Then watch for anomalies. A daily cost more than three standard deviations above the trailing average is a good first rule.

> In my invented logs I broke the cache of one feature on day forty-five by moving a timestamp to the top. Daily cost rose one point eight times, and the cache read share fell from seventy percent to zero. Both alerts fired that same day, with no false alarms in the two healthy features.

**[Hidden lines]**

> The hidden lines are storage and network. On A W S, moving data between availability zones costs about two cents a gigabyte, counting both send and receive. A full training checkpoint of a seventy billion model is eleven hundred twenty gigabytes, twenty-two dollars forty to move, five hundred thirty-eight a day if hourly.

> Keeping forty-eight hourly checkpoints costs about twelve hundred thirty-six dollars a month. Keeping the last three costs seventy-seven, ninety-four percent less. Keep the last few full, every day's weights only, and expire or archive the rest. Keep G P Us, data and checkpoints in one zone.

**[ShopNest Copilot: cost plan]**

> For ShopNest Copilot. Put the stable system prompt first and the changing fields last, and alert on cache read share. Run offline evals and nightly labelling in batch. Start on a mid size model with low effort, and escalate only on a failing check.

> Stamp every call at the gateway with team, feature, tenant and trace. Report cost per resolved ticket. Cap spend per key. Keep the G P Us busy or do not rent them. And price a hosted open model before building your own.

**[Four words to keep]**

> Four words to carry forward. Utilisation: the share of paid hours doing useful work. Real price: list price divided by utilisation.

> Cache hit: a request whose prompt prefix was already stored, billed at a fraction. And unit cost: the cost of one useful outcome, like a resolved ticket.

**[Interview corner]**

> Interview corner. Asked how you cut the cost of an A I system, say: fix idle capacity first, because real price is list price over utilisation. Then caching, batch, a prompt audit, effort, and routing last. A prompt with a changing field on top got zero percent cache hits in my test.

> Asked whether to self host or use an A P I, say: compute the break even volume. One H one hundred beats a premium model above about eleven to twenty-one million tokens a day, and never beats a Haiku class model, so judge cost per task.

**[Your turn]**

> Your turn. The zip for this lesson has four scripts. The G P U price and commitment sums, the token cost and cache tests, the break even calculator, and the gateway alert test. Change the prices to your own provider's, and the utilisation to your own cluster's.

> Then move the timestamp in the cache test and watch the hit rate. One changed number teaches more than an hour of reading.

**[Recap]**

> Recap. Real price is list price over utilisation, so a three dollar G P U at five percent is sixty-three. A commitment at discount d needs more than one minus d use. One training run varied five point four times by how it was bought.

> For tokens, cache first, then batch, audit, effort, and routing last. A timestamp on top meant zero cache hits. One H one hundred never beats a Haiku class A P I. Stamp every call, report cost per resolved ticket. Next, the final lesson, your learning path.

**[Next lesson]**

> In the next lesson: your learning path. From zero to cloud A I engineer.

> Subscribe so you don't miss it. See you in the notebook.


## Short 1: Why a $3 GPU Really Costs $63 (The Utilisation Sum) #shorts

> A G P U listed at three dollars seventeen an hour can really cost sixty-three dollars. Here is the sum.

> The real price of a G P U hour is the list price divided by utilisation. At five percent use, a three dollar seventeen H one hundred costs sixty-three dollars forty per useful hour.

> At fifty percent it is six thirty-four. Ten times cheaper, with no negotiating. The best rate discounts only give two or three times. Fix idle time first.

> Real price is list price divided by utilisation.


## Short 2: One Line in Your Prompt Can Triple Your AI Bill (Cache Mistake) #shorts

> One line at the top of your prompt can triple your A I bill, and the answers stay identical.

> A prompt cache matches the start of a prompt. I wrote a toy cache and sent it five thousand requests. With a timestamp at the very top, zero percent of tokens were reused.

> Moving the same timestamp after the shared part, seventy-five percent were. The input bill was three and a half times higher. Stable text first, changing text last.

> Stable text first. Changing text last.


## Instagram Reel 1: One H100 never beats a Haiku-class API (the self-host break-even)

> Will one G P U ever beat a cheap A P I?

> I did the sum. One H one hundred costs seventy-six dollars a day and holds about thirty-five million tokens. Against a premium model it can win from about eleven to twenty-one million tokens a day. Against a Haiku class A P I it needs four hundred and twenty-three million. It never wins.

> Compare cost per task. Save this.
