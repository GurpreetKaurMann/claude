import sys; sys.path.insert(0, '/home/claude/caigen')
from frag import *
from gailab import CODE, OUT

LONG = [
 dict(id='s0', chap='A hundred hour job, never saved', say=[
   "I simulated a hundred hour training job on cheap spot machines that get taken away at random. If the job never saves its progress, the expected time to finish is over two million hours. It effectively never ends.",
   "Save progress every thirty-four minutes and it finishes in about a hundred and nine hours, for a third of the on-demand price. Save too often and it costs more than not using spot at all. This lesson is about renting compute without wasting money."],
  html=[H2('Never save: 2,203,564 hours', 0),
        DEF('save every <b>34 min</b>: <b>109 h</b> · cost <b>33%</b> of on-demand', 0, 0.5, style='margin-top:24px;font-size:50px'),
        MARK('simulation · assumed interruption rate', 1, 0.6)]),

 dict(id='s1', chap='Where we are', say=[
   "Welcome back. In lesson one we learned the four numbers on a GPU spec sheet, and how to check whether your model fits. Now we shop. Which chip do you rent, how do you pay for it, and how do you stop paying when you do not need it?",
   "Prices and chip names in this lesson come from vendors and are dated October twenty twenty-six. The sums and simulations are mine, and I label each one. Chip availability changes fast, so check the vendor page before you book anything."],
  html=[H2('Which chip? How to pay? When to stop?', 0),
        GRID([('which chip', 0, 0.3), ('how to pay', 0, 0.8), ('when to stop', 0, 1.3)], cols=3, h=150, fs=44),
        STICKY('Dated', 'vendor figures, <b>Oct 2026</b> · my sums and simulations are labelled', 1, 0.5, style='margin-top:26px;font-size:38px')]),

 dict(id='s2', chap='Four families of chips', say=[
   "Four families of chips matter. N V I D I A is the default and runs everywhere. A M D is the main alternative. Google makes its own chips, called TPUs, and rents them only on Google Cloud. Amazon makes Trainium, rented only on A W S.",
   "Think of four car brands. They all drive on the same road, but they need different fuel, and different mechanics. The fuel here is software, and that is what you will pay to switch."],
  html=[H2('Four families of chips', 0),
        ROW(COL(CARD('<b>NVIDIA</b><br>the default, every cloud', 0, 0.3, style='font-size:36px'), width='48%'),
            COL(CARD('<b>AMD</b><br>the main alternative', 0, 0.8, style='font-size:36px'), width='48%'), style='margin-top:24px'),
        ROW(COL(CARD('<b>Google TPU</b><br>Google Cloud only', 0, 1.3, style='font-size:36px'), width='48%'),
            COL(CARD('<b>AWS Trainium</b><br>Amazon only', 0, 1.8, style='font-size:36px'), width='48%'), style='margin-top:22px'),
        SUB('same road, different fuel: the fuel is software', 1, 0.5, style='margin-top:18px')]),

 dict(id='s3', chap='The map', say=[
   "Here is the map. N V I D I A uses a software stack called CUDA, and it has the widest support. A M D uses R O C m, and stock PyTorch runs on it.",
   "Google's TPUs work best with a framework called JAX. Amazon's Trainium uses the Neuron S D K.",
   "The pattern is simple. The more special the chip, the cheaper it can be, and the more you depend on one cloud. That is a trade, not a mistake. Just make it on purpose."],
  html=[H2('Four brands, four software stacks', 0), SVG('c3', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c3', 'families', 1000, 280, 1)]),

 dict(id='s4', chap='NVIDIA chips to know', say=[
   "Start with the N V I D I A names. The H one hundred and H two hundred are the workhorses, rentable almost everywhere. The B two hundred, from the Blackwell generation, is generally available too, and the B three hundred family is broadly rentable in twenty twenty-six.",
   "The newest, called Vera Rubin, is only in limited availability. One cloud began renting it on the thirtieth of September. If you are planning a project this quarter, plan around the chips you can actually book."],
  html=[H2('The NVIDIA names, October 2026', 0),
        TABLE(['Chip', 'Status', 'Memory'], [
          (['H100 / H200', 'workhorse', '80 / 141 GB'], 0, 0.4),
          (['B200', 'generally available', '192 GB'], 0, 1.0),
          (['B300 / GB300', 'broadly rentable', '288 GB'], 0, 1.6),
          (['Vera Rubin', '<b>limited</b>', '288 GB'], 1, 0.4)], style='margin-top:22px;font-size:40px'),
        SUB('vendor figures, Oct 2026', 1, 1.0, style='margin-top:14px')]),

 dict(id='s5', chap='AMD', say=[
   "A M D's chip to know is the M I three fifty-five X. It has two hundred and eighty-eight gigabytes of memory, the same as the top N V I D I A tier, and it is generally available on a couple of clouds.",
   "Its software is called R O C m, not CUDA. Stock PyTorch and the popular serving tools run on it. The risk is custom code written specifically for CUDA, which will need work."],
  html=[H2('AMD: the MI355X', 0),
        DEF('<b>288 GB</b> memory · rentable on OCI and Vultr (Oct 2026)', 0, 0.4, style='margin-top:24px;font-size:48px'),
        LIST([('software: ROCm, not CUDA', 1, 0.3), ('stock PyTorch and vLLM run on it', 1, 0.9), ('risk: custom CUDA code', 1, 1.5)], kind='ar', style='margin-top:20px;font-size:42px')]),

 dict(id='s6', chap='Google TPU', say=[
   "Google's newest TPU is called Ironwood. It became generally available in April twenty twenty-six, with one hundred and ninety-two gigabytes per chip. Its party trick is scale. A single pod links nine thousand, two hundred and sixteen chips together.",
   "A cheaper TPU called Trillium exists for serving and fine tuning smaller models. You rent TPUs only on Google Cloud, and the best framework for them is JAX."],
  html=[H2('Google TPU: Ironwood', 0),
        DEF('<b>192 GB</b> per chip · pod of <b>9,216</b> chips · generally available (Apr 2026)', 0, 0.4, style='margin-top:24px;font-size:46px'),
        LIST([('Trillium: the budget TPU', 1, 0.3), ('Google Cloud only', 1, 0.9), ('best with JAX', 1, 1.5)], kind='ar', style='margin-top:20px;font-size:42px')]),

 dict(id='s7', chap='AWS Trainium', say=[
   "Amazon's chip is Trainium. The third generation became generally available in December twenty twenty-five, with one hundred and forty-four gigabytes per chip. A big rack, called an UltraServer, links one hundred and forty-four of them.",
   "Amazon also makes a serving chip called Inferentia. You use both through the Neuron S D K, which works with PyTorch and JAX. The pitch is price for performance, in exchange for being tied to Amazon."],
  html=[H2('AWS Trainium and Inferentia', 0),
        DEF('Trainium3: <b>144 GB</b> per chip · UltraServer of <b>144</b> chips · GA Dec 2025', 0, 0.4, style='margin-top:24px;font-size:46px'),
        LIST([('Inferentia: the serving chip', 1, 0.3), ('software: Neuron SDK', 1, 0.9), ('trade: price for AWS lock-in', 1, 1.5)], kind='ar', style='margin-top:20px;font-size:42px')]),

 dict(id='s8', chap='The cost of switching', say=[
   "What does switching away from N V I D I A actually cost? Mostly one thing. Custom kernels written in CUDA. These are small programs, often hand tuned, that some projects rely on.",
   "If your model is stock PyTorch or JAX, it moves far more easily than you might fear. If you depend on custom kernels, budget engineering time. Always test your own workload before you sign anything."],
  html=[H2('The real cost of switching chips', 0),
        ROW(COL(CARD('<b>stock PyTorch / JAX</b><br>moves fairly easily', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>custom CUDA kernels</b><br>needs engineering time', 0, 1.0, style='font-size:38px'), width='48%'), style='margin-top:30px'),
        STICKY('Rule', 'test <b>your own workload</b> before you commit', 1, 0.5, style='margin-top:26px;font-size:42px')]),

 dict(id='s9', chap='Status words', say=[
   "A word on status. Vendors use words like generally available, limited, announced, and previous generation. Generally available means you can rent it today.",
   "Limited means a waiting list. Announced means a slide. And previous generation, which people call old, is often the best value. Never build a plan around a chip that is only announced."],
  html=[H2('Four status words', 0),
        GRID([('<b>GA</b><br>rent it today', 0, 0.3), ('<b>limited</b><br>waiting list', 0, 0.8), ('<b>announced</b><br>only a slide', 1, 0.3), ('<b>old</b><br>often best value', 1, 0.8)], cols=2, h=150, fs=40, style='margin-top:26px')]),

 dict(id='s10', chap='Reading instance names', say=[
   "Clouds name machines in a code. On A W S, p five dot forty-eight x large means one whole host with eight H one hundreds. On Google Cloud, a three dash highgpu dash eight g means eight GPUs, because the g count is the GPU count.",
   "On Azure, N D ninety-six I S R H one hundred v five means eight H one hundreds, and the letters I, S and R stand for isolated, premium storage and R D M A networking. Learn to read the name before you read the price."],
  html=[H2('Reading a machine name', 0),
        TABLE(['Cloud', 'Name', 'Means'], [
          (['AWS', 'p5.48xlarge', '8 × H100, whole host'], 0, 0.4),
          (['Google', 'a3-highgpu-8g', '8 GPUs (the 8g)'], 0, 1.0),
          (['Azure', 'ND96isr_H100_v5', '8 × H100, RDMA'], 1, 0.4)], style='margin-top:24px;font-size:40px'),
        SUB('read the name before you read the price', 1, 1.2, style='margin-top:16px')]),

 dict(id='s11', chap='Big clouds and neoclouds', say=[
   "Where do you rent? Two kinds of provider. The big clouds, called hyperscalers, and newer specialist GPU clouds, called neoclouds. Neoclouds often list the same GPU at roughly half to two thirds of the big cloud price, and they tend to get new chips first.",
   "The big clouds win on the things around the GPU. Your data is already there, your identity and network are set up, and they offer managed services and their own chips. A common answer is to do both."],
  html=[H2('Hyperscaler or neocloud?', 0),
        ROW(COL(CARD('<b>neocloud</b><br>about ½ to ⅔ of the price<br>new chips first', 0, 0.4, style='font-size:36px'), width='48%'),
            COL(CARD('<b>big cloud</b><br>your data and identity are there<br>managed services, own chips', 1, 0.3, style='font-size:36px'), width='48%'), style='margin-top:28px'),
        SUB('prices are list prices, Oct 2026', 0, 1.0, style='margin-top:16px')]),

 dict(id='s12', chap='The buying ladder', say=[
   "Now how to pay. There is a ladder, and every step down is cheaper and comes with strings. On demand is the base price, no promises.",
   "Queued capacity, called flex start, can be around half price, but your job waits for a slot. A one to three year commitment goes down to about forty-five percent of the price, if you use it.",
   "Spot is the cheapest, down to about nine percent, because the provider can take the machine back. These are the vendors' up to figures, and real discounts vary."],
  html=[H2('The buying ladder', 0), SVG('c12', 1400, 420, 'margin:14px auto 0')],
  svgs=[('c12', 'ladder', 1000, 330, 1)]),

 dict(id='s13', chap='Commitments', say=[
   "A commitment means you promise to pay for a GPU for one to three years, in return for a discount of up to about fifty-five percent. It is the right tool for a steady workload that never sleeps, like a live support assistant.",
   "There are also prepaid windows, such as A W S Capacity Blocks, where you reserve a stretch of time for a deadline, like a two week training run. Same idea, shorter promise."],
  html=[H2('Commit for steady load', 0),
        LIST([('promise 1 to 3 years, up to ~55% off', 0, 0.4), ('fits a workload that never sleeps', 0, 1.0), ('prepaid windows: a short promise for a deadline', 1, 0.4)], kind='ar', style='margin-top:26px;font-size:44px')]),

 dict(id='s14', chap='The commitment trap', say=[
   "Here is the trap, and it is a sum. You pay for a commitment even when the GPU sits idle. So the real price is the rate divided by how busy you keep it. Assume an on demand price of ten dollars an hour. That is my assumption, to keep the maths clean.",
   "A fifty-five percent commitment costs four fifty. At ninety percent busy, the real price is five dollars per used hour. At forty-five percent busy, it is ten, the same as on demand.",
   "At thirty percent busy, fifteen dollars. At ten percent, forty-five. The discount turned into a penalty."],
  html=[H2('Real price = rate ÷ how busy', 0), SVG('c14', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c14', 'realprice', 1000, 345, 1)]),

 dict(id='s15', chap='Break-even', say=[
   "So here is the rule. A commitment with a discount of fifty-five percent only pays off if you keep the GPU busy more than forty-five percent of the time. That is one minus the discount.",
   "If you are not sure, start on demand, measure your real busy time for a month, and then commit to only the steady part. Never commit to your peak."],
  html=[H2('The break-even rule', 0),
        DEF('commit pays off only if busy &gt; <b>1 − discount</b><br>55% off → busy more than <b>45%</b>', 0, 0.4, style='margin-top:24px;font-size:50px'),
        STICKY('Rule', 'commit to the <b>steady part</b>, never your peak', 1, 0.5, style='margin-top:26px;font-size:42px')]),

 dict(id='s16', chap='Queued capacity', say=[
   "A middle option is queued capacity. Google calls its version Flex start, and it can be around fifty percent off for some chips. You ask for machines, and they arrive when capacity frees up.",
   "That is fine for jobs that can wait, like a nightly evaluation or a batch run. It is a bad fit for anything a customer is waiting on. Match the plan to how patient the job is."],
  html=[H2('Queued: half price if you can wait', 0),
        ROW(COL(CARD('<b>good for</b><br>nightly evals, batch runs', 0, 0.4, style='font-size:40px'), width='48%'),
            COL(CARD('<b>bad for</b><br>a customer waiting', 1, 0.3, style='font-size:40px'), width='48%'), style='margin-top:30px')]),

 dict(id='s17', chap='Spot', say=[
   "Now spot, the biggest discount. Spot machines are spare capacity. They cost up to about ninety-one percent less, and the provider can take them back. On A W S you get two minutes of warning. On Azure, thirty seconds.",
   "That sounds scary. It is fine if your job saves its progress regularly. So the real question is how often to save. I simulated exactly that, so let me show you."],
  html=[H2('Spot: up to 91% off', 0),
        DEF('spare capacity · taken back with <b>2 min</b> notice on AWS, <b>30 s</b> on Azure', 0, 0.4, style='margin-top:24px;font-size:46px'),
        MARK('the real question: how often do you save?', 1, 0.5)]),

 dict(id='s18', chap='My spot simulation', say=[
   "The setup. A job needs a hundred hours of work. The spot machine is taken away at random, on average every eight hours. That rate is my assumption. After each interruption, I lose all the work since the last save, and wait six minutes to restart.",
   "A save costs seventy-two seconds of work time. I tried different save intervals, ran two thousand simulated jobs for each, and priced the result with an assumed seventy percent spot discount. This is a simulation, not real machines."],
  html=[H2('The spot simulation', 0),
        OUT(['job: 100 hours of work', 'interrupted every 8 h on average (assumed)', 'lose work since last save · 0.1 h to restart', 'one save costs 0.02 h (72 s)'], 0, 0.4, size=30, label='simulation setup', style='margin-top:22px'),
        SUB('2,000 simulated jobs per setting · spot = 30% of on-demand (assumed)', 1, 0.6, style='margin-top:14px')]),

 dict(id='s19', chap='Never save', say=[
   "First result. A job that never saves until the end needs eight hours of luck, twelve and a half times in a row. The average finish time was two million, two hundred and three thousand, five hundred and sixty-four hours.",
   "That is not a typo. A hundred hour job on interruptible machines, with no saving, effectively never finishes. Spot without checkpoints is not cheap. It is broken."],
  html=[H2('No saves: it never finishes', 0),
        OUT(['saves only at the end:   2,203,564 hours', 'on-demand:                100 hours'], 0, 0.4, size=34, label='simulation', style='margin-top:26px'),
        MARK('spot without saving is broken, not cheap', 1, 0.6)]),

 dict(id='s20', chap='How often to save', say=[
   "Now add saves. Every eight hours, the job takes a hundred and seventy-two hours. Every two hours, a hundred and sixteen. Every thirty minutes, a hundred and nine.",
   "Save every ten minutes and it is a hundred and fifteen. Every two minutes, a hundred and sixty-three. Every thirty seconds, three hundred and forty-five.",
   "A U shape. Too rare and you lose a lot of work. Too often and you spend your time saving."],
  html=[H2('Hours to finish, by save interval', 0), SVG('c20', 1400, 450, 'margin:6px auto 0')],
  svgs=[('c20', 'ckpt_hours', 1000, 395, 1)]),

 dict(id='s21', chap='The bill', say=[
   "Now the bill. Priced at thirty percent of on demand, a save every thirty minutes costs thirty-two point six, against a hundred on demand. A third of the price.",
   "Every two minutes it is forty-eight point eight. Every thirty seconds it is a hundred and three point five. Saving too often cost more than not using spot at all.",
   "The cheapest rental in the world is the most expensive one if you waste its hours."],
  html=[H2('Cost, with on-demand = 100', 0), SVG('c21', 1400, 450, 'margin:6px auto 0')],
  svgs=[('c21', 'ckpt_cost', 1000, 395, 1)]),

 dict(id='s22', chap='Young\'s rule', say=[
   "There is a simple rule to find the sweet spot. Save every square root of two times the average time between interruptions times the cost of one save. With my numbers, that is two times eight times point oh two, then the square root. About thirty-four minutes.",
   "That matches the simulation, where thirty and thirty-four minutes tied. Cheap saves and frequent interruptions mean you save more often. Expensive saves and rare interruptions mean less often."],
  html=[H2('Save every √(2 × MTBF × cost)', 0),
        DEF('√(2 × 8 h × 0.02 h) = <b>0.566 h</b> ≈ <b>34 min</b>', 0, 0.4, style='margin-top:26px;font-size:54px'),
        MARK('matches the simulation: 30 and 34 min tied', 1, 0.5)]),

 dict(id='s23', chap='When to use spot', say=[
   "So when do you use spot? For work that can be paused and resumed. Training with saves, batch evaluation, data processing. Pay attention to the warning notice and save when it arrives.",
   "Do not run your only live chat endpoint on spot. If you must, keep a few on demand machines behind it so users never see an outage."],
  html=[H2('Where spot fits', 0),
        ROW(COL(CARD('<b>yes</b><br>training with saves<br>batch evals, data jobs', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>careful</b><br>live chat endpoint<br>keep on-demand behind it', 1, 0.3, style='font-size:38px'), width='48%'), style='margin-top:28px')]),

 dict(id='s24', chap='Price per petaflop', say=[
   "How do you compare different chips? Divide the hourly price by the arithmetic the chip does, in petaflops. This uses vendor list prices on Google Cloud, from October fourteenth.",
   "Ironwood on demand is about two dollars sixty-one per petaflop hour. A B two hundred through Flex start is one seventy-nine. Ironwood with Flex or a three year commit is about one seventeen to one thirty.",
   "The chip with the lowest price per hour is not always the cheapest per unit of work. Divide first."],
  html=[H2('Price per petaflop-hour', 0), SVG('c24', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c24', 'ppf', 1000, 270, 1)]),

 dict(id='s25', chap='Autoscaling', say=[
   "Now stopping the meter. Autoscaling means adding machines when demand rises and removing them when it falls. It works at two levels.",
   "Pods are the running copies of your service. A tool called KEDA adds pods when requests queue up. If the pods have nowhere to run, a tool called Karpenter, or the Cluster Autoscaler, adds new machines.",
   "Adding a GPU machine can take minutes. So scale on a signal that moves early, like the queue length, not on how busy the GPU already is."],
  html=[H2('Two levels of autoscaling', 0), SVG('c25', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c25', 'autoscale', 1000, 290, 1)]),

 dict(id='s26', chap='Scale to zero', say=[
   "The cheapest GPU is one that is switched off. Scale to zero means shutting down every machine when nobody is using the service. You stop paying overnight and at weekends.",
   "The price is the cold start. The first request after a quiet spell must wait while a machine starts and loads the model. For real models that is tens of seconds to minutes. I simulated it with sixty seconds."],
  html=[H2('Scale to zero', 0),
        ROW(COL(CARD('<b>benefit</b><br>no idle GPU, no bill', 0, 0.4, style='font-size:42px'), width='48%'),
            COL(CARD('<b>price</b><br>first user waits, a cold start', 1, 0.3, style='font-size:42px'), width='48%'), style='margin-top:30px'),
        SUB('simulated with a 60 s cold start (assumed)', 1, 1.0, style='margin-top:16px')]),

 dict(id='s27', chap='Scale to zero, measured', say=[
   "The simulated day has a three hour busy window, a one hour light window, and silence otherwise. Always on bills twenty-four GPU hours. Scale to zero, with a five minute idle timeout, bills four point oh four. Eighty-three percent less.",
   "The average wait went from one point seven seconds to two point three. The slowest five percent went from seven point nine to eight point nine.",
   "But there were three point nine cold starts a day, and each of those users waited a full sixty seconds. Cheap on average, painful for the unlucky few."],
  html=[H2('A simulated day', 0), SVG('c27', 1400, 420, 'margin:10px auto 0')],
  svgs=[('c27', 'zero_cost', 1000, 250, 1)]),

 dict(id='s28', chap='Cold start trade-off', say=[
   "Here are the same numbers as a trade.",
   "Waits barely moved on average.",
   "But the cold starts are real. If a person is waiting, sixty seconds is a lot."],
  html=[H2('Cheap on average, ugly for the first user', 0), SVG('c28', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c28', 'zero_wait', 1000, 290, 1)]),

 dict(id='s29', chap='Fixing cold starts', say=[
   "How do you soften a cold start? Keep the model files cached close to the machine, so you do not download them every time. Save compiled artifacts, so the model does not recompile. Some platforms can snapshot a loaded model and restore it quickly.",
   "Or keep one warm machine and scale the rest to zero. I am teaching these as ideas here. They are not measured in this lesson. The next lesson covers the container side of it."],
  html=[H2('Softening a cold start', 0),
        LIST([('cache the model files near the GPU', 0, 0.4), ('save compiled artifacts', 0, 1.0), ('snapshot a loaded model', 0, 1.6), ('or keep one machine warm', 1, 0.4)], kind='ar', style='margin-top:24px;font-size:42px'),
        SUB('taught, not measured here · more in lesson 3', 1, 1.0, style='margin-top:14px')]),

 dict(id='s30', chap='ShopNest Copilot', say=[
   "Now apply it to ShopNest Copilot. The live support assistant never sleeps, so it earns a commitment, but only for the steady part, with on demand for peaks. The nightly evaluation run is patient work, so it goes on spot with saves about every half hour.",
   "And the staging environment, used a few hours a day, scales to zero. Three workloads, three different rungs of the ladder. That is the skill."],
  html=[H2('ShopNest Copilot: three workloads', 0),
        TABLE(['Workload', 'How to rent it'], [
          (['live assistant', 'commit the steady part + on-demand peaks'], 0, 0.4),
          (['nightly eval run', 'spot + save every ~30 min'], 1, 0.3),
          (['staging', 'scale to zero'], 1, 0.9)], style='margin-top:26px;font-size:42px')]),

 dict(id='s31', chap='Four words to keep', say=[
   "Four words to carry forward. Commitment: a promise to pay in return for a discount. Spot: spare capacity you can lose.",
   "Checkpoint: a saved copy of your progress. And cold start: the wait when a machine must start from nothing. You will hear all four again in the next lessons."],
  html=[H2('Four words to keep', 0),
        GRID([('<b>commitment</b>', 0, 0.3), ('<b>spot</b>', 0, 0.9), ('<b>checkpoint</b>', 1, 0.3), ('<b>cold start</b>', 1, 0.9)], cols=2, h=140, fs=48, style='margin-top:30px')]),

 dict(id='s32', chap='Interview corner', say=[
   "Interview corner. Asked when a commitment is worth it, say: only if you keep the GPU busy more than one minus the discount, so a fifty-five percent discount needs forty-five percent use. Otherwise the real price per used hour is higher than on demand.",
   "Asked how to use spot safely, say: checkpoint regularly, handle the warning notice, and pick the interval with the square root rule, which gave about thirty-four minutes in my simulation."],
  html=[H2('Interview corner', 0),
        Q('When is a commitment worth it?', 'Busy &gt; 1 − discount. 55% off needs &gt; 45% use.', 0, 0.4),
        Q('How do you use spot safely?', 'Checkpoint, handle the notice, interval ≈ √(2 × MTBF × cost).', 1, 0.4)]),

 dict(id='s33', chap='Your turn', say=[
   "Your turn. The zip for this lesson has three scripts. The first simulates spot interruptions. Change the average time between interruptions, and the cost of a save, and find your own sweet spot.",
   "The second does the buying maths, and the third simulates scale to zero. Put in your own traffic. One changed number teaches more than an hour of reading."],
  html=[H2('Your turn', 0),
        CARD('<b>l02_spot_checkpoint.py</b>: change the interruption rate and save cost.<br>'
             '<b>l02_buying_math.py</b>: your price, your busy time.<br><b>l02_scale_to_zero.py</b>: your traffic.', 0, 0.4, style='margin-top:22px;font-size:38px'),
        SUB('one changed number teaches more than an hour of reading', 1, 0.8, style='margin-top:16px')]),

 dict(id='s34', chap='Recap', say=[
   "Recap. Pick the chip for your software, not just the spec. A commitment only pays off above forty-five percent use at fifty-five percent off. Spot is brilliant with saves every thirty or so minutes, and broken without them.",
   "Scale to zero cut a simulated day from twenty-four GPU hours to four, at the price of sixty second cold starts. Next lesson: containers and Kubernetes. How to package a model so it runs the same everywhere."],
  html=[H2('Recap', 0),
        GRID([('chip for your software', 0, 0.3), ('commit if busy &gt; 45%', 0, 0.9), ('spot needs saves', 0, 1.5),
              ('save every ~30 min', 1, 0.3), ('24 → 4 GPU-hours', 1, 0.9), ('cold start: 60 s', 1, 1.5)], cols=3, h=150, fs=34)]),
]
