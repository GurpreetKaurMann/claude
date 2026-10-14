import sys; sys.path.insert(0, '/home/claude/caigen')
from frag import *
from gailab import CODE, OUT

LONG = [
 dict(id='s0', chap='A three dollar GPU', say=[
   "A G P U listed at three dollars seventeen an hour can really cost sixty-three dollars forty. Same machine, same invoice. The only thing that changed is how much of the time it was doing useful work. And one line in a prompt can triple an A P I bill without changing a single answer.",
   "This is the cost lesson. Every number comes from arithmetic on the notebook's prices, or from a small test I ran. You will leave knowing where the money goes and which lever to pull first."],
  html=[H2('A $3 GPU can cost $63', 0),
        DEF('listed <b>$3.17</b> an hour · used 5% of the time · real price <b>$63.40</b>', 0, 0.5, style='margin-top:24px;font-size:44px'),
        MARK('and one prompt line can triple the token bill', 1, 0.6)]),

 dict(id='s1', chap='Where we are', say=[
   "We built, trained, served, shipped and secured the assistant. Now someone has to pay for it. The surprise in A I costs is that the biggest waste is rarely the price per hour. It is hours that nobody was using, and tokens that were sent again and again.",
   "Honest labels. Prices are the notebook's approximate list prices from September and October twenty twenty-six, and they move often. The sums are arithmetic. The cache test uses a toy cache I wrote. The alert test uses invented logs."],
  html=[H2('Cost for AI systems', 0),
        GRID([('GPU hours', 0, 0.3), ('tokens', 0, 0.7), ('hidden lines', 0, 1.1)], cols=3, h=150, fs=40),
        STICKY('Honest label', 'list prices as of Oct 2026 · arithmetic · toy cache · invented logs', 1, 0.5, style='margin-top:26px;font-size:36px')]),

 dict(id='s2', chap='The Fin Ops loop', say=[
   "Fin Ops means engineering, finance and product sharing ownership of cloud spend, so cost becomes a design input, like latency. It runs as a loop. Inform, optimise, operate. Inform is seeing the spend, tagging G P Us and metering tokens per team and feature.",
   "Optimise fixes the rate and the amount used. Operate keeps it fixed with budgets and alerts. A memory hook is I, O, O. See it, fix it, keep it fixed. You cannot optimise what you have not allocated, and savings do not last without alerts."],
  html=[H2('The Fin Ops loop', 0), SVG('c2', 1400, 399, 'margin:14px auto 0')],
  svgs=[('c2', 'loop', 1000, 285, 1)]),

 dict(id='s4', chap='Measure the right thing', say=[
   "First, measure utilisation honestly. The number you see in nvidia dash smi says what share of the last second had at least one kernel running. A tiny kernel on a single processing block reads the same as one filling the whole chip. So a G P U can show one hundred percent while most of it sits idle.",
   "Better is the D C G M profiling field called S M active, the fraction of time warps were running, averaged over all the processing blocks. Watch S M active, occupancy, and tensor pipe activity. Above eighty percent S M active is necessary, not sufficient."],
  html=[H2('The misleading number', 0),
        TABLE(['Reading', 'Means'], [(['nvidia-smi GPU-Util 100%', 'a kernel ran at some point each second'], 0, 0.4), (['SM active 0.13', '2 of 16 processing blocks in use'], 1, 0.3), (['SM active 1.0', 'all 16 in use'], 1, 0.8)], style='margin-top:24px;font-size:38px')]),

 dict(id='s5', chap='How idle is normal', say=[
   "How idle is normal? A vendor study of tens of thousands of Kubernetes clusters that nobody had optimised found average G P U use around five percent. That is vendor telemetry, so treat it as a warning, not a law. A survey of five hundred seventy-three leaders found eighty-six percent of enterprises with their own G P Us report fifty percent or less.",
   "Another survey found forty-four percent assign G P Us by hand or have no strategy. So if your cluster looks busy on a dashboard, check which number the dashboard shows. Then fix idle capacity, because that is the biggest lever."],
  html=[H2('How idle is normal?', 0),
        GRID([('~5%<br>average use, vendor telemetry', 0, 0.3), ('86%<br>report 50% or less', 0, 0.8), ('44%<br>assign GPUs by hand', 1, 0.3)], cols=3, h=210, fs=34),
        SUB('vendor and survey figures, 2026, as reported in the notebook', 1, 1.0, style='margin-top:18px')]),

 dict(id='s6', chap='The real price', say=[
   "The real price of a G P U hour is the list price divided by utilisation. At the three dollar seventeen index price, five percent use makes a useful hour cost sixty-three dollars forty. Twenty-two percent, fourteen forty-one. Fifty percent, six thirty-four. Eighty percent, three ninety-six.",
   "Going from five to fifty percent makes a useful hour ten times cheaper. The best rate discounts top out around two or three times. So fix idle time before you negotiate price. A three dollar H one hundred at five percent is a sixty-three dollar H one hundred."],
  html=[H2('Divide by utilisation', 0), SVG('c6', 1400, 469, 'margin:14px auto 0')],
  svgs=[('c6', 'realprice', 1000, 335, 1)]),

 dict(id='s7', chap='Right size, then share', say=[
   "Right size next. If weights and the memory cache fit in ten to twenty gigabytes, a full eighty gigabyte card is oversized. A seven billion parameter model at eight bit or four bit with modest traffic fits a small slice, or a cheaper card like an L four or L forty S class part.",
   "There are three ways to share. M I G cuts hardware slices with their own memory and fault isolation, up to seven per card, good for production multi tenant serving. Time slicing lets pods take turns with no isolation, fine for trusted development. M P S runs kernels together, for trusted workloads."],
  html=[H2('Right-size, then share', 0),
        TABLE(['Method', 'What you get', 'Use for'], [(['MIG', 'own memory + fault isolation, up to 7 slices', 'production multi-tenant'], 0, 0.4), (['time-slicing', 'pods take turns, no isolation', 'trusted dev and test'], 1, 0.3), (['MPS', 'kernels run together', 'trusted workloads'], 1, 0.8)], style='margin-top:20px;font-size:34px')]),

 dict(id='s9', chap='Ways to buy a GPU', say=[
   "How you buy matters too. On demand has no commitment and is the baseline, good for bursty experiments. Neoclouds offer a lower list price and the newest chips first. Reserved commitments give a lower rate for steady load. Capacity blocks guarantee a cluster for a fixed window, which is not a discount.",
   "Spot or preemptible capacity is half to seventy percent off, with notice before eviction of two minutes on A W S, and thirty seconds on Azure and Google. Flex start queues your job until capacity frees. Every option has a catch. Pick by workload shape."],
  html=[H2('Ways to buy GPU time', 0),
        TABLE(['Option', 'Good for', 'Catch'], [(['on-demand', 'bursty experiments', 'highest rate'], 0, 0.4), (['reserved / commit', 'steady inference', 'paid used or not'], 0, 0.9), (['capacity block', 'deadline training', 'prepaid, not a discount'], 1, 0.3), (['spot', 'checkpointed batch', 'eviction'], 1, 0.7), (['flex start', 'fine-tunes, batch', 'you wait'], 1, 1.1)], style='margin-top:10px;font-size:30px')]),

 dict(id='s10', chap='The commitment rule', say=[
   "The commitment rule is simple. A commitment at discount d wins only if you use more than one minus d of the committed capacity. At a forty percent discount you need more than sixty percent use. At fifty-five percent for three years, more than forty-five percent.",
   "I checked it with arithmetic. At a forty percent discount, fifty percent use makes the commitment lose, and seventy percent makes it win. A discount of d buys you the right to waste d. With volatile prices, shorter terms limit the risk of being locked in above market."],
  html=[H2('Commit only if use > 1 − discount', 0),
        TABLE(['Discount', 'Break-even use', 'Check'], [(['30%', '> 70%', '60% use: on-demand wins'], 0, 0.4), (['40%', '> 60%', '50%: loses · 70%: wins'], 0, 0.9), (['55% (3-year)', '> 45%', '35%: loses · 55%: wins'], 1, 0.3)], style='margin-top:22px;font-size:38px'),
        STICKY('Remember', 'a discount of d buys you the right to waste d', 1, 0.9, style='margin-top:20px;font-size:38px')]),

 dict(id='s11', chap='One run, five ways', say=[
   "Here is one training run. Sixty-four H one hundreds for fourteen days is twenty-one thousand five hundred and four G P U hours. At the index price of three seventeen it costs sixty-eight thousand dollars. At the market average, eighty-three thousand.",
   "As an A W S capacity block, about one hundred twenty-eight thousand. At hyperscaler on demand, about one hundred forty-eight thousand. Spot at sixty percent off is twenty-seven thousand before lost steps and restarts. Same job, a spread of five point four times. Buying is an engineering decision."],
  html=[H2('One training run, five ways to pay', 0), SVG('c11', 1400, 469, 'margin:14px auto 0')],
  svgs=[('c11', 'five', 1000, 335, 1)]),

 dict(id='s14', chap='The token bill', say=[
   "Now tokens. An A P I bill is a sum over token types. Uncached input at the input price. Cache writes at a premium. Cache reads at a fraction. And output tokens, including thinking, at the output price. Batch jobs cost half. Some regional options add ten percent.",
   "The shape is the same across vendors. Output costs about five to six times input. Cache reads cost a tenth of input or less. Batch is half. So the question is never just the price per million. It is how many tokens of each kind each request uses."],
  html=[H2('Price every token type', 0),
        DEF('cost = uncached input + cache writes + cache reads + <b>output</b>', 0, 0.4, style='margin-top:24px;font-size:42px'),
        LIST([('output ≈ 5-6× the input price', 1, 0.3), ('cache reads ≤ 0.1× input', 1, 0.8), ('batch = 50% off', 1, 1.3)], kind='ck', style='margin-top:22px;font-size:42px')]),

 dict(id='s15', chap='A real price table', say=[
   "Here are list prices per million tokens from the notebook, October fourteenth, twenty twenty-six. Opus five point five costs four dollars in and twenty out. Sonnet five point five, two in and ten out. Haiku five point five, ten cents in and fifty cents out.",
   "Cache reads are five percent of input on Opus and Sonnet, and ten percent on Haiku. Writing a five minute cache costs one and a quarter times input. These figures change, so treat the table as an example of the shape, and check the vendor page before budgeting."],
  html=[H2('List prices, per million tokens', 0),
        TABLE(['Model', 'Input', 'Cache read', 'Output'], [(['Opus 5.5', '$4', '$0.20', '$20'], 0, 0.4), (['Sonnet 5.5', '$2', '$0.10', '$10'], 0, 0.8), (['Haiku 5.5', '$0.10', '$0.01', '$0.50'], 1, 0.3)], style='margin-top:22px;font-size:42px'),
        SUB('notebook list prices, 14 Oct 2026 · check the vendor page', 1, 0.9, style='margin-top:12px')]),

 dict(id='s16', chap='A support bot, costed', say=[
   "Let me cost the support bot. Each request has a three thousand token system prompt that can be cached, a thousand uncached tokens of history and question, and four hundred tokens of output. On Sonnet five point five with no cache, that is one point two cents, twelve thousand dollars per million requests.",
   "When the cache hits, it drops to six thousand three hundred. A cascade, where Haiku answers first and thirty percent go to Sonnet, is four thousand two hundred. Batch on top of a cache hit is three thousand one hundred fifty. The model tier moves the bill most, then caching, then batch."],
  html=[H2('Cost per million requests', 0), SVG('c16', 1400, 469, 'margin:14px auto 0')],
  svgs=[('c16', 'bot', 1000, 335, 1)]),

 dict(id='s17', chap='Lever one: caching', say=[
   "Caching is lever one. A five minute cache write costs one and a quarter times the input price, and a read costs a tenth or twentieth. So a five minute cache pays back after a single read, and a one hour cache after two. Vendors report agent loops reading a median eighty-four percent of input from cache.",
   "In my arithmetic the cache hit saved forty-seven point five percent per request. And at a hit rate of fifty percent the bill is nine thousand nine hundred per million, at eighty percent seven thousand seven hundred forty, at ninety-five percent six thousand six hundred sixty."],
  html=[H2('Cache: pays back after one read', 0),
        GRID([('write 1.25× once', 0, 0.3), ('read 0.05-0.1×', 0, 0.8), ('hit saves 47.5%', 1, 0.3)], cols=3, h=150, fs=38),
        TABLE(['Hit rate', 'Sonnet 5.5, per 1M requests'], [(['50%', '$9,900'], 1, 0.9), (['80%', '$7,740'], 1, 1.3), (['95%', '$6,660'], 1, 1.7)], style='margin-top:18px;font-size:36px')]),

 dict(id='s18', chap='Does the cache hit?', say=[
   "A cache only helps if requests keep arriving. If requests share a prefix at a steady rate, the hit rate is one minus e to the minus rate times lifetime. I simulated random arrivals to check. One request a minute with a five minute lifetime hit ninety-nine point two percent of the time.",
   "One request every ten minutes hit thirty-eight point nine percent, and one an hour only eight percent. The formula agreed within a point. So a quiet feature can pay for cache writes and never get the reads. Measure the real hit rate, then decide the lifetime."],
  html=[H2('Traffic decides the hit rate', 0), SVG('c18', 1400, 399, 'margin:14px auto 0')],
  svgs=[('c18', 'ttl', 1000, 285, 1)]),

 dict(id='s19', chap='The timestamp mistake', say=[
   "Here is the mistake that triples bills. A cache matches the start of a prompt. If a timestamp or user name sits at the very top of the system prompt, every request starts differently, and nothing is ever reused. I wrote a toy prefix cache and fed it five thousand requests.",
   "With the timestamp on top, zero percent of tokens were served from cache. With the same timestamp after the shared part, seventy-five percent were. The input bill was three and a half times higher. Rule. Stable text first, changing text last."],
  html=[H2('Stable first, changing last', 0), SVG('c19', 1400, 371, 'margin:14px auto 0')],
  svgs=[('c19', 'ts', 1000, 265, 1)]),

 dict(id='s20', chap='Lever two: batch', say=[
   "Lever two is batch. Batch processing takes fifty percent off every token, including cached ones, in exchange for waiting up to twenty-four hours. It is the second biggest free lever after caching.",
   "Anything that does not need an instant answer belongs there. Offline evaluation runs, backfills, nightly labelling, summarising yesterday's tickets. On the support bot, batch on top of a cache hit halves the three thousand per million again."],
  html=[H2('Batch: half price, within a day', 0),
        LIST([('50% off every token, cached ones too', 0, 0.4), ('results within 24 hours', 0, 0.9), ('offline evals · backfills · nightly labelling', 1, 0.3), ('never for live chat', 1, 0.8)], kind='ar', style='margin-top:24px;font-size:42px')]),

 dict(id='s21', chap='Levers three and four', say=[
   "Levers three and four are the prompt audit and effort. Trim what you send. Searching a tool list instead of sending all five hundred tools cut input forty-five percent in a published test. Pruning stale tool results saved thirty-nine, and a plain prompt audit fourteen.",
   "Effort is a price dial. On one benchmark, a cheaper model at high effort solved nearly as many tasks as a bigger one at low effort, at about the same cost. Running everything at low effort and re-running failures at high saved about forty percent, but only if you can detect a failure, like a failing test."],
  html=[H2('Trim input, tune effort', 0),
        LIST([('tool search instead of 500 tools: −45% input', 0, 0.4), ('prune stale tool results: −39%', 0, 0.9), ('prompt audit: −14%', 0, 1.4), ('low effort first, re-run failures at high: ≈ −40%', 1, 0.4), ('needs a reliable failure signal', 1, 1.0)], kind='ar', style='margin-top:22px;font-size:38px')]),

 dict(id='s22', chap='Lever five: routing', say=[
   "Lever five comes last. Routing sends easy requests to a cheap model and hard ones to a big model. In the notebook's sum, Haiku first with thirty percent escalated to Sonnet cuts sixty-five percent against all Sonnet. That holds only if the escalation classifier is reliable.",
   "Quality on the easy seventy percent must stay acceptable. Caches are per model. And escalated requests pay twice. So compare against the best single model at lower effort with caching. Routing is the most common lever in industry, and the one most often done before the cheaper ones."],
  html=[H2('Routing and cascades: last', 0),
        CARD('Haiku first, 30% to Sonnet: <b>$4,200</b> per million vs <b>$12,000</b> all-Sonnet (−65%)', 0, 0.4, style='margin-top:22px;font-size:40px'),
        LIST([('classifier must be reliable', 1, 0.3), ('quality on the easy 70% must hold', 1, 0.7), ('escalations pay twice', 1, 1.1)], kind='ck', style='margin-top:18px;font-size:40px')]),

 dict(id='s25', chap='Self-host: the formula', say=[
   "Should you host the model yourself? Start with the formula. Dollars per million tokens equals the G P U price per hour, divided by tokens per second times three thousand six hundred times utilisation, times a million. A seventy billion model at eight bit on one H one hundred does about four hundred tokens a second, a vendor figure likely conservative.",
   "At full use that is two dollars twenty per million tokens. At sixty percent, three sixty-seven. At forty percent, five fifty. At fifteen percent, fourteen sixty-eight. Utilisation again decides everything, and production use is often thirty to sixty percent."],
  html=[H2('Self-host cost per million tokens', 0),
        TABLE(['Utilisation', '70B FP8 on one H100 ($3.17/hr, 400 tok/s)'], [(['100%', '$2.20'], 0, 0.4), (['60%', '$3.67'], 0, 0.8), (['40%', '$5.50'], 1, 0.3), (['15%', '$14.68'], 1, 0.8)], style='margin-top:22px;font-size:40px')]),

 dict(id='s26', chap='The break-even volume', say=[
   "Now the break-even volume. One H one hundred running all day costs seventy-six dollars eight cents. Divide by the A P I blended price. Against Opus, self hosting can win above ten point six million tokens a day. Against Sonnet, above twenty-one point one million, with a narrow window, because one card tops out at thirty-four point six million.",
   "Against Haiku, the break even is four hundred twenty-three million tokens a day, far beyond what one card can serve. So one H one hundred never beats a Haiku class A P I on G P U cost alone. Self hosting only competes with premium models."],
  html=[H2('How many tokens a day to beat the API?', 0), SVG('c26', 1400, 441, 'margin:14px auto 0')],
  svgs=[('c26', 'breakeven', 1000, 315, 1)]),

 dict(id='s27', chap='Self-host: what the sum hides', say=[
   "I also simulated a year of bursty traffic, averaging twenty million tokens a day, with one fixed G P U serving the base load and the A P I taking overflow. The hybrid cost thirty-one thousand six hundred seventy-eight dollars, against thirty-one thousand nine hundred nine for all A P I. Basically a tie, before any people.",
   "And the sum leaves things out. On call time, upgrades, spare replicas, and the weaker quality of an open model, which makes cost per successful task the fair test. The simple sum flatters self hosting. Price a hosted open model and a batch cached A P I first."],
  html=[H2('A tie, before people costs', 0),
        TABLE(['One year, bursty traffic (simulated)', 'Cost'], [(['all API (Sonnet 5.5)', '$31,909'], 0, 0.4), (['1 GPU base load + API overflow', '$31,678'], 0, 0.9)], style='margin-top:22px;font-size:40px'),
        SUB('GPU used 62% of capacity · 12.2% of tokens overflowed · no on-call, spares or quality gap counted', 1, 0.5, style='margin-top:18px')]),

 dict(id='s29', chap='Who spent it?', say=[
   "Now attribution. G P U cost can use cloud tags, Kubernetes labels, and a cost allocation tool. Tokens have no resource tags, so a gateway stamps team, feature and tenant on every request. Give each project its own key or workspace. And capture usage when the request happens, before billing aggregates it away.",
   "Agents fan out, so join calls with a trace identifier. Log the token counts, and compute the dollar cost at log time from a versioned price table. Never recompute old history with today's prices, and reconcile against the provider's cost report each month."],
  html=[H2('Stamp every call at the gateway', 0),
        CODE(['{"trace_id": "conv-8f3a", "team": "support",', ' "feature": "triage-bot", "tenant_id": "acme",', ' "model": "sonnet-5.5", "uncached_in": 1000,', ' "cache_read": 3000, "output": 400,', ' "price_table": "2026-10-14", "cost_usd": 0.0063}'], 0, 0.3, step=0.5, size=30, style='margin-top:14px', lang='json'),
        SUB('price table version stored with the line · reconcile monthly', 1, 0.6, style='margin-top:14px')]),

 dict(id='s30', chap='Showback and cost per ticket', say=[
   "With stamped logs, you can report. Showback shows each team its cost with no payment enforced, and is the place to start. Chargeback lands the cost on the team's budget, once allocation rules are stable. In my invented logs, the triage bot cost about twenty-seven dollars a day, the order lookup six, and the refund agent a hundred and fourteen.",
   "The number that matters is cost per resolved ticket. Cost per conversation divided by the resolve rate. For the triage bot that came to about six cents, the lookup under one cent, the refund agent seventeen cents. Put it next to the cost of a human, and you show value, not just spend."],
  html=[H2('Showback → cost per resolved ticket', 0),
        TABLE(['Feature (invented logs)', 'Cost / day', 'Resolve', 'Per resolved'], [(['triage-bot', '$26.70', '70%', '$0.057'], 0, 0.4), (['order-lookup', '$6.41', '95%', '$0.009'], 0, 0.8), (['refund-agent', '$113.79', '45%', '$0.165'], 1, 0.3)], style='margin-top:20px;font-size:36px'),
        SUB('per resolved = cost per request × turns ÷ resolve rate (6 turns assumed, 2 for lookups)', 1, 0.8, style='margin-top:12px')]),

 dict(id='s31', chap='Budgets and alerts', say=[
   "Operate means budgets and alarms. Set a monthly budget per workspace, alert at fifty, eighty and one hundred percent, and put hard spend caps at the gateway to stop a runaway agent. Then watch for anomalies. A daily cost more than three standard deviations above the trailing average is a good first rule.",
   "In my invented logs I broke the cache of one feature on day forty-five by moving a timestamp to the top. Daily cost rose one point eight times, and the cache read share fell from seventy percent to zero. Both alerts fired that same day, with no false alarms in the two healthy features."],
  html=[H2('Budgets, caps, anomalies', 0),
        LIST([('monthly budget per workspace · alerts at 50 / 80 / 100%', 0, 0.4), ('hard spend cap at the gateway', 0, 0.9), ('alert: daily cost > mean + 3σ (14 days)', 0, 1.4), ('cache break found on day 45: cost 1.8×, cache share 70% → 0%', 1, 0.4), ('both alerts fired the same day, 0 false alarms (invented logs)', 1, 1.0)], kind='ar', style='margin-top:22px;font-size:36px')]),

 dict(id='s32', chap='Hidden lines', say=[
   "The hidden lines are storage and network. On A W S, moving data between availability zones costs about two cents a gigabyte, counting both send and receive. A full training checkpoint of a seventy billion model is eleven hundred twenty gigabytes, twenty-two dollars forty to move, five hundred thirty-eight a day if hourly.",
   "Keeping forty-eight hourly checkpoints costs about twelve hundred thirty-six dollars a month. Keeping the last three costs seventy-seven, ninety-four percent less. Keep the last few full, every day's weights only, and expire or archive the rest. Keep G P Us, data and checkpoints in one zone."],
  html=[H2('Hidden lines: checkpoints', 0), SVG('c32', 1400, 371, 'margin:14px auto 0')],
  svgs=[('c32', 'ckpt', 1000, 265, 1)]),

 dict(id='s33', chap='ShopNest Copilot: cost plan', say=[
   "For ShopNest Copilot. Put the stable system prompt first and the changing fields last, and alert on cache read share. Run offline evals and nightly labelling in batch. Start on a mid size model with low effort, and escalate only on a failing check.",
   "Stamp every call at the gateway with team, feature, tenant and trace. Report cost per resolved ticket. Cap spend per key. Keep the G P Us busy or do not rent them. And price a hosted open model before building your own."],
  html=[H2('ShopNest Copilot: cost plan', 0),
        TABLE(['Lever', 'Plan'], [(['cache', 'stable prompt first, changing fields last, alert on cache share'], 0, 0.4), (['batch + effort', 'evals and labelling in batch, low effort, escalate on failure'], 0, 0.9), (['attribution', 'gateway stamps, cost per resolved ticket, cap per key'], 1, 0.3), (['GPUs', 'busy or not rented; price a hosted open model first'], 1, 0.8)], style='margin-top:18px;font-size:34px')]),

 dict(id='s34', chap='Four words to keep', say=[
   "Four words to carry forward. Utilisation: the share of paid hours doing useful work. Real price: list price divided by utilisation.",
   "Cache hit: a request whose prompt prefix was already stored, billed at a fraction. And unit cost: the cost of one useful outcome, like a resolved ticket."],
  html=[H2('Four words to keep', 0),
        GRID([('<b>utilisation</b>', 0, 0.3), ('<b>real price</b>', 0, 0.9), ('<b>cache hit</b>', 1, 0.3), ('<b>unit cost</b>', 1, 0.9)], cols=2, h=140, fs=42, style='margin-top:30px')]),

 dict(id='s35', chap='Interview corner', say=[
   "Interview corner. Asked how you cut the cost of an A I system, say: fix idle capacity first, because real price is list price over utilisation. Then caching, batch, a prompt audit, effort, and routing last. A prompt with a changing field on top got zero percent cache hits in my test.",
   "Asked whether to self host or use an A P I, say: compute the break even volume. One H one hundred beats a premium model above about eleven to twenty-one million tokens a day, and never beats a Haiku class model, so judge cost per task."],
  html=[H2('Interview corner', 0),
        Q('How do you cut AI costs?', 'Utilisation first, then cache → batch → audit → effort → routing. Timestamp on top: 0% cache hits.', 0, 0.4),
        Q('Self-host or API?', 'Break-even volume: 11-21M tokens/day vs premium; never vs Haiku-class.', 1, 0.4)]),

 dict(id='s36', chap='Your turn', say=[
   "Your turn. The zip for this lesson has four scripts. The G P U price and commitment sums, the token cost and cache tests, the break even calculator, and the gateway alert test. Change the prices to your own provider's, and the utilisation to your own cluster's.",
   "Then move the timestamp in the cache test and watch the hit rate. One changed number teaches more than an hour of reading."],
  html=[H2('Your turn', 0),
        CARD('<b>l11_gpu_price.py</b> · <b>l11_token_cost.py</b><br><b>l11_breakeven.py</b> · <b>l11_gateway_anomaly.py</b>', 0, 0.4, style='margin-top:22px;font-size:36px'),
        SUB('put in your own prices and your own utilisation', 1, 0.8, style='margin-top:16px')]),

 dict(id='s37', chap='Recap', say=[
   "Recap. Real price is list price over utilisation, so a three dollar G P U at five percent is sixty-three. A commitment at discount d needs more than one minus d use. One training run varied five point four times by how it was bought.",
   "For tokens, cache first, then batch, audit, effort, and routing last. A timestamp on top meant zero cache hits. One H one hundred never beats a Haiku class A P I. Stamp every call, report cost per resolved ticket. Next, the final lesson, your learning path."],
  html=[H2('Recap', 0),
        GRID([('real price = list ÷ use', 0, 0.3), ('commit if use > 1 − d', 0, 0.9), ('same run: 5.4× spread', 0, 1.5),
              ('cache → batch → audit → effort → route', 1, 0.3), ('timestamp on top: 0% cached', 1, 0.9), ('cost per resolved ticket', 1, 1.5)], cols=3, h=150, fs=30)]),
]
