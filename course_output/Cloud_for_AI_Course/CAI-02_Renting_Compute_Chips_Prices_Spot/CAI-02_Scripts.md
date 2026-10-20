# CAI-02 · Renting Compute: Scripts

**Lesson 2 of 12 · Module 1 · Compute**

Voice: AI narrator (Kokoro `af_heart`). Final lesson video length: 16:40.

## Long video narration

**[A hundred hour job, never saved]**

> I simulated a hundred hour training job on cheap spot machines that get taken away at random. If the job never saves its progress, the expected time to finish is over two million hours. It effectively never ends.

> Save progress every thirty-four minutes and it finishes in about a hundred and nine hours, for a third of the on-demand price. Save too often and it costs more than not using spot at all. This lesson is about renting compute without wasting money.

**[Intro]**

> Welcome to lesson two of the cloud for A I engineers course, on The Code Notebook.

> The handwritten notes and the code for this lesson are linked in the description.

**[Where we are]**

> Welcome back. In lesson one we learned the four numbers on a GPU spec sheet, and how to check whether your model fits. Now we shop. Which chip do you rent, how do you pay for it, and how do you stop paying when you do not need it?

> Prices and chip names in this lesson come from vendors and are dated October twenty twenty-six. The sums and simulations are mine, and I label each one. Chip availability changes fast, so check the vendor page before you book anything.

**[Four families of chips]**

> Four families of chips matter. N V I D I A is the default and runs everywhere. A M D is the main alternative. Google makes its own chips, called TPUs, and rents them only on Google Cloud. Amazon makes Trainium, rented only on A W S.

> Think of four car brands. They all drive on the same road, but they need different fuel, and different mechanics. The fuel here is software, and that is what you will pay to switch.

**[The map]**

> Here is the map. N V I D I A uses a software stack called CUDA, and it has the widest support. A M D uses R O C m, and stock PyTorch runs on it.

> Google's TPUs work best with a framework called JAX. Amazon's Trainium uses the Neuron S D K.

> The pattern is simple. The more special the chip, the cheaper it can be, and the more you depend on one cloud. That is a trade, not a mistake. Just make it on purpose.

**[NVIDIA chips to know]**

> Start with the N V I D I A names. The H one hundred and H two hundred are the workhorses, rentable almost everywhere. The B two hundred, from the Blackwell generation, is generally available too, and the B three hundred family is broadly rentable in twenty twenty-six.

> The newest, called Vera Rubin, is only in limited availability. One cloud began renting it on the thirtieth of September. If you are planning a project this quarter, plan around the chips you can actually book.

**[AMD]**

> A M D's chip to know is the M I three fifty-five X. It has two hundred and eighty-eight gigabytes of memory, the same as the top N V I D I A tier, and it is generally available on a couple of clouds.

> Its software is called R O C m, not CUDA. Stock PyTorch and the popular serving tools run on it. The risk is custom code written specifically for CUDA, which will need work.

**[Google TPU]**

> Google's newest TPU is called Ironwood. It became generally available in April twenty twenty-six, with one hundred and ninety-two gigabytes per chip. Its party trick is scale. A single pod links nine thousand, two hundred and sixteen chips together.

> A cheaper TPU called Trillium exists for serving and fine tuning smaller models. You rent TPUs only on Google Cloud, and the best framework for them is JAX.

**[AWS Trainium]**

> Amazon's chip is Trainium. The third generation became generally available in December twenty twenty-five, with one hundred and forty-four gigabytes per chip. A big rack, called an UltraServer, links one hundred and forty-four of them.

> Amazon also makes a serving chip called Inferentia. You use both through the Neuron S D K, which works with PyTorch and JAX. The pitch is price for performance, in exchange for being tied to Amazon.

**[The cost of switching]**

> What does switching away from N V I D I A actually cost? Mostly one thing. Custom kernels written in CUDA. These are small programs, often hand tuned, that some projects rely on.

> If your model is stock PyTorch or JAX, it moves far more easily than you might fear. If you depend on custom kernels, budget engineering time. Always test your own workload before you sign anything.

**[Status words]**

> A word on status. Vendors use words like generally available, limited, announced, and previous generation. Generally available means you can rent it today.

> Limited means a waiting list. Announced means a slide. And previous generation, which people call old, is often the best value. Never build a plan around a chip that is only announced.

**[Reading instance names]**

> Clouds name machines in a code. On A W S, p five dot forty-eight x large means one whole host with eight H one hundreds. On Google Cloud, a three dash highgpu dash eight g means eight GPUs, because the g count is the GPU count.

> On Azure, N D ninety-six I S R H one hundred v five means eight H one hundreds, and the letters I, S and R stand for isolated, premium storage and R D M A networking. Learn to read the name before you read the price.

**[Big clouds and neoclouds]**

> Where do you rent? Two kinds of provider. The big clouds, called hyperscalers, and newer specialist GPU clouds, called neoclouds. Neoclouds often list the same GPU at roughly half to two thirds of the big cloud price, and they tend to get new chips first.

> The big clouds win on the things around the GPU. Your data is already there, your identity and network are set up, and they offer managed services and their own chips. A common answer is to do both.

**[The buying ladder]**

> Now how to pay. There is a ladder, and every step down is cheaper and comes with strings. On demand is the base price, no promises.

> Queued capacity, called flex start, can be around half price, but your job waits for a slot. A one to three year commitment goes down to about forty-five percent of the price, if you use it.

> Spot is the cheapest, down to about nine percent, because the provider can take the machine back. These are the vendors' up to figures, and real discounts vary.

**[Commitments]**

> A commitment means you promise to pay for a GPU for one to three years, in return for a discount of up to about fifty-five percent. It is the right tool for a steady workload that never sleeps, like a live support assistant.

> There are also prepaid windows, such as A W S Capacity Blocks, where you reserve a stretch of time for a deadline, like a two week training run. Same idea, shorter promise.

**[The commitment trap]**

> Here is the trap, and it is a sum. You pay for a commitment even when the GPU sits idle. So the real price is the rate divided by how busy you keep it. Assume an on demand price of ten dollars an hour. That is my assumption, to keep the maths clean.

> A fifty-five percent commitment costs four fifty. At ninety percent busy, the real price is five dollars per used hour. At forty-five percent busy, it is ten, the same as on demand.

> At thirty percent busy, fifteen dollars. At ten percent, forty-five. The discount turned into a penalty.

**[Break-even]**

> So here is the rule. A commitment with a discount of fifty-five percent only pays off if you keep the GPU busy more than forty-five percent of the time. That is one minus the discount.

> If you are not sure, start on demand, measure your real busy time for a month, and then commit to only the steady part. Never commit to your peak.

**[Queued capacity]**

> A middle option is queued capacity. Google calls its version Flex start, and it can be around fifty percent off for some chips. You ask for machines, and they arrive when capacity frees up.

> That is fine for jobs that can wait, like a nightly evaluation or a batch run. It is a bad fit for anything a customer is waiting on. Match the plan to how patient the job is.

**[Spot]**

> Now spot, the biggest discount. Spot machines are spare capacity. They cost up to about ninety-one percent less, and the provider can take them back. On A W S you get two minutes of warning. On Azure, thirty seconds.

> That sounds scary. It is fine if your job saves its progress regularly. So the real question is how often to save. I simulated exactly that, so let me show you.

**[My spot simulation]**

> The setup. A job needs a hundred hours of work. The spot machine is taken away at random, on average every eight hours. That rate is my assumption. After each interruption, I lose all the work since the last save, and wait six minutes to restart.

> A save costs seventy-two seconds of work time. I tried different save intervals, ran two thousand simulated jobs for each, and priced the result with an assumed seventy percent spot discount. This is a simulation, not real machines.

**[Never save]**

> First result. A job that never saves until the end needs eight hours of luck, twelve and a half times in a row. The average finish time was two million, two hundred and three thousand, five hundred and sixty-four hours.

> That is not a typo. A hundred hour job on interruptible machines, with no saving, effectively never finishes. Spot without checkpoints is not cheap. It is broken.

**[How often to save]**

> Now add saves. Every eight hours, the job takes a hundred and seventy-two hours. Every two hours, a hundred and sixteen. Every thirty minutes, a hundred and nine.

> Save every ten minutes and it is a hundred and fifteen. Every two minutes, a hundred and sixty-three. Every thirty seconds, three hundred and forty-five.

> A U shape. Too rare and you lose a lot of work. Too often and you spend your time saving.

**[The bill]**

> Now the bill. Priced at thirty percent of on demand, a save every thirty minutes costs thirty-two point six, against a hundred on demand. A third of the price.

> Every two minutes it is forty-eight point eight. Every thirty seconds it is a hundred and three point five. Saving too often cost more than not using spot at all.

> The cheapest rental in the world is the most expensive one if you waste its hours.

**[Young's rule]**

> There is a simple rule to find the sweet spot. Save every square root of two times the average time between interruptions times the cost of one save. With my numbers, that is two times eight times point oh two, then the square root. About thirty-four minutes.

> That matches the simulation, where thirty and thirty-four minutes tied. Cheap saves and frequent interruptions mean you save more often. Expensive saves and rare interruptions mean less often.

**[When to use spot]**

> So when do you use spot? For work that can be paused and resumed. Training with saves, batch evaluation, data processing. Pay attention to the warning notice and save when it arrives.

> Do not run your only live chat endpoint on spot. If you must, keep a few on demand machines behind it so users never see an outage.

**[Price per petaflop]**

> How do you compare different chips? Divide the hourly price by the arithmetic the chip does, in petaflops. This uses vendor list prices on Google Cloud, from October fourteenth.

> Ironwood on demand is about two dollars sixty-one per petaflop hour. A B two hundred through Flex start is one seventy-nine. Ironwood with Flex or a three year commit is about one seventeen to one thirty.

> The chip with the lowest price per hour is not always the cheapest per unit of work. Divide first.

**[Autoscaling]**

> Now stopping the meter. Autoscaling means adding machines when demand rises and removing them when it falls. It works at two levels.

> Pods are the running copies of your service. A tool called KEDA adds pods when requests queue up. If the pods have nowhere to run, a tool called Karpenter, or the Cluster Autoscaler, adds new machines.

> Adding a GPU machine can take minutes. So scale on a signal that moves early, like the queue length, not on how busy the GPU already is.

**[Scale to zero]**

> The cheapest GPU is one that is switched off. Scale to zero means shutting down every machine when nobody is using the service. You stop paying overnight and at weekends.

> The price is the cold start. The first request after a quiet spell must wait while a machine starts and loads the model. For real models that is tens of seconds to minutes. I simulated it with sixty seconds.

**[Scale to zero, measured]**

> The simulated day has a three hour busy window, a one hour light window, and silence otherwise. Always on bills twenty-four GPU hours. Scale to zero, with a five minute idle timeout, bills four point oh four. Eighty-three percent less.

> The average wait went from one point seven seconds to two point three. The slowest five percent went from seven point nine to eight point nine.

> But there were three point nine cold starts a day, and each of those users waited a full sixty seconds. Cheap on average, painful for the unlucky few.

**[Cold start trade-off]**

> Here are the same numbers as a trade.

> Waits barely moved on average.

> But the cold starts are real. If a person is waiting, sixty seconds is a lot.

**[Fixing cold starts]**

> How do you soften a cold start? Keep the model files cached close to the machine, so you do not download them every time. Save compiled artifacts, so the model does not recompile. Some platforms can snapshot a loaded model and restore it quickly.

> Or keep one warm machine and scale the rest to zero. I am teaching these as ideas here. They are not measured in this lesson. The next lesson covers the container side of it.

**[ShopNest Copilot]**

> Now apply it to ShopNest Copilot. The live support assistant never sleeps, so it earns a commitment, but only for the steady part, with on demand for peaks. The nightly evaluation run is patient work, so it goes on spot with saves about every half hour.

> And the staging environment, used a few hours a day, scales to zero. Three workloads, three different rungs of the ladder. That is the skill.

**[Four words to keep]**

> Four words to carry forward. Commitment: a promise to pay in return for a discount. Spot: spare capacity you can lose.

> Checkpoint: a saved copy of your progress. And cold start: the wait when a machine must start from nothing. You will hear all four again in the next lessons.

**[Interview corner]**

> Interview corner. Asked when a commitment is worth it, say: only if you keep the GPU busy more than one minus the discount, so a fifty-five percent discount needs forty-five percent use. Otherwise the real price per used hour is higher than on demand.

> Asked how to use spot safely, say: checkpoint regularly, handle the warning notice, and pick the interval with the square root rule, which gave about thirty-four minutes in my simulation.

**[Your turn]**

> Your turn. The zip for this lesson has three scripts. The first simulates spot interruptions. Change the average time between interruptions, and the cost of a save, and find your own sweet spot.

> The second does the buying maths, and the third simulates scale to zero. Put in your own traffic. One changed number teaches more than an hour of reading.

**[Recap]**

> Recap. Pick the chip for your software, not just the spec. A commitment only pays off above forty-five percent use at fifty-five percent off. Spot is brilliant with saves every thirty or so minutes, and broken without them.

> Scale to zero cut a simulated day from twenty-four GPU hours to four, at the price of sixty second cold starts. Next lesson: containers and Kubernetes. How to package a model so it runs the same everywhere.

**[Next lesson]**

> In the next lesson: containers and Kubernetes. How to package a model so it runs the same everywhere.

> Subscribe so you don't miss it. See you in the notebook.


## Short 1: Why a 100-Hour Job Can Take 2 Million Hours on Cheap GPUs #shorts

> A hundred hour job on cheap spot GPUs can take two million hours. Here is the mistake.

> Spot machines are cheap because the provider can take them back. In my simulation, one was taken every eight hours on average, an assumption.

> A job that never saves its progress needs a hundred hours without a single interruption. The average finish time was over two million hours. Save every thirty-four minutes and it took a hundred and nine.

> Spot is only cheap if your job saves its progress.


## Short 2: When a 55% GPU Discount Costs You MORE #shorts

> A fifty-five percent discount on GPUs can cost you fifty percent more. Here is the sum.

> A commitment means you pay for the GPU even when it is idle. So the real price is the rate divided by how busy you keep it. I assume ten dollars an hour on demand.

> Commit at ninety percent busy and you pay five dollars per used hour. At thirty percent busy, fifteen dollars. Break even is forty-five percent.

> Commit only to the steady part of your load.


## Instagram Reel 1: Scale to zero cut the bill 83%

> How scale to zero cut a simulated GPU bill by eighty-three percent.

> One GPU, one simulated day. Always on, twenty-four GPU hours billed. Scale to zero with a five minute idle timeout, about four. The catch, a few users a day waited a full sixty seconds.

> Cheap on average, painful for the first user. Save this.
