# CAI-05 · Training at Scale: Scripts

**Lesson 5 of 12 · Module 3 · Training and serving**

Voice: AI narrator (Kokoro `af_heart`). Final lesson video length: 16:40.

## Long video narration

**[The 1,120 gigabyte surprise]**

> A seventy billion parameter model is a hundred and forty gigabytes of weights. So training it should need a hundred and forty gigabytes, right? Wrong. Training needs one thousand, one hundred and twenty gigabytes, eight times more.

> No single GPU holds that. So how do people train big models at all? This lesson answers it. Where the memory goes, how to split it, what it costs, and what breaks along the way.

**[Intro]**

> Welcome to lesson five of the cloud for A I engineers course, on The Code Notebook.

> The handwritten notes and the code for this lesson are linked in the description.

**[Where we are]**

> In the earlier lessons we rented chips, packed containers and fed them data. Now we train. This is the most expensive thing in A I, so it pays to understand it.

> Plan for the lesson. The memory ledger, how to share it across GPUs, how to save memory by recomputing, how many GPU hours a run needs, the ways to split a model, the network, and what goes wrong. Some of it is measured on a small model on my CPU. The rest is arithmetic and simulation, labelled.

**[What training is]**

> First, what is training? Think of a teacher marking homework. The model makes a guess. That is the forward pass. We measure how wrong it was. That number is called the loss.

> Then comes the backward pass. We work out which numbers inside the model were most to blame. Those blame scores are called gradients. And finally the optimiser nudges every weight a little, in the direction that reduces the error. Repeat billions of times.

**[Four things in memory]**

> During training, four things sit in memory. The weights themselves. The gradients, one per weight. The optimiser's memory, and I will explain that next. And activations, the in between results saved during the forward pass so the backward pass can use them.

> The first three scale with the number of parameters. Activations scale with how many tokens are in flight. Together they are why training needs so much more than just storing the model.

**[The 16-byte ledger]**

> Here is the ledger for the standard recipe. Weights in the half size format, two bytes. Gradients, two bytes. Then the optimiser. Most use Adam, which keeps two numbers per weight, a running average of the gradient, and of its square, four bytes each.

> Adam also keeps a full precision master copy of the weights, four bytes, because tiny nudges vanish in half precision. Two plus two plus twelve is sixteen bytes per parameter.

> The weights, the part you thought about, are only a eighth of the bill.

**[Measured on a real model]**

> Let me check that on a real model. I built a small network with thirty-three and a half million parameters, ran one training step with Adam, and added up the bytes of every tensor.

> On a CPU everything is full precision, so weights are four bytes, gradients four, and Adam's two memories eight. Total, sixteen point zero bytes per parameter, exactly. Different recipe, same total.

**[Scaling up]**

> Now scale it. Sixteen bytes times seven billion parameters is a hundred and twelve gigabytes. Seventy billion, eleven hundred and twenty. Four hundred and five billion, nearly six and a half terabytes.

> An eighty gigabyte H one hundred cannot hold even the seven billion model's training state. Before activations, before anything else. So we share it.

**[Sharding the state]**

> The trick is called sharding, with names ZeRO and F S D P. Instead of every GPU keeping everything, each GPU keeps a slice. The first stage shards only the optimiser memory. The next also shards the gradients.

> The last stage shards the weights too. For a seventy billion model on sixty-four GPUs, the per GPU share falls from eleven hundred and twenty gigabytes, to two ninety-three, to a hundred and fifty-five, and finally to seventeen and a half.

> That last number fits an eighty gigabyte card. The earlier stages still do not.

**[Why stage three]**

> Why do the first two stages not work for seventy billion? They still keep a full copy of the half size weights on every GPU. That is a hundred and forty gigabytes before anything else.

> Only the full sharding stage, called ZeRO three or F S D P, splits the weights as well. The price is more network traffic, about one and a half times a plain data parallel run, because the weights must be gathered when needed.

**[Activations]**

> Now the fourth thing, activations. During the forward pass, every layer's in between results are saved, because the backward pass needs them. They grow with the number of tokens, and with attention, they can grow with the square of the sequence length.

> That is why long context training is so hungry. The notebook's worked example for a seventy billion class model at eight thousand tokens is about one point nine terabytes of activations if you keep everything, against about twenty-three gigabytes with recomputation and tensor parallel. A technique called flash attention avoids storing the biggest piece, and the standard trick for the rest is recomputation.

**[Recomputation]**

> Recomputation, also called gradient checkpointing, is a trade. Keep only each block's input. When the backward pass needs the inside of a block, run that block's forward pass again.

> You spend extra compute to save memory. I measured it. Twelve blocks, two thousand tokens, on one CPU thread. Each setting ran in its own process, so I could read its peak memory. The machine was shared, so timings are noisy.

**[Recompute, measured]**

> Keeping everything, the activations took seven hundred and ninety-three megabytes. With recomputation, four hundred and twenty-six. About half.

> The step time rose from five point six seconds to six point nine. A little under a quarter more.

> Half the activation memory for a fifth to a quarter more time. The notebook's rule of thumb is up to a third more compute, so mine is in range.

**[Counting compute]**

> Now compute. A good rule: training a model needs about six times the parameters times the training tokens in floating point operations. Two for the forward pass, four for the backward, per parameter per token.

> Those operations run on GPUs at a fraction of their peak speed. The fraction is called M F U, model flops utilisation. Well tuned dense runs on H one hundreds reach roughly thirty-five to forty-five percent.

**[A worked example]**

> Let us do a worked example. A seven billion model trained on two trillion tokens. Six times seven billion times two trillion is eight point four times ten to the twenty-two operations.

> An H one hundred peaks near nine hundred and eighty-nine trillion operations a second. At forty percent M F U, that is about four hundred. Divide, and the run needs about fifty-nine thousand GPU hours. On a thousand and twenty-four GPUs, two point four days.

> At an assumed two dollars per GPU hour, about a hundred and eighteen thousand dollars. Real prices vary a lot.

**[MFU honesty]**

> One warning about M F U. It depends on which peak you divide by. Run in a smaller number format and the chip's peak doubles, so the same run looks half as efficient. Compare M F U only between runs that use the same number format.

> Also quote M F U, not H F U. The second counts recomputed work, so recomputation makes it look better while the useful work is the same. As a reverse check, DeepSeek reported about two point eight million GPU hours for its large model, which works out to roughly a third of the chip's peak.

**[How many tokens?]**

> How many tokens should you train on? A famous study called Chinchilla suggested about twenty tokens per parameter for the best use of a fixed compute budget.

> But today's models train far longer on purpose. Llama three's biggest model saw about thirty-eight tokens per parameter, and a seven billion model on two trillion tokens sees nearly three hundred. A smaller, longer trained model is cheaper to run afterwards.

**[Four ways to split]**

> Sharding the state is one way to share the work. There are four main ways to split a training job. Data parallel, where every GPU runs the same model on different data. Tensor parallel, where the matrices inside each layer are cut up.

> Pipeline parallel, where layers are split into stages, like an assembly line. And expert parallel, for models made of many experts. Big runs combine three or four at once.

> Each one cuts a different thing, so each one sends different traffic over the network.

**[Tensor parallel]**

> Tensor parallel is the chattiest. Every layer, forward and backward, the GPUs must combine their partial results, and the next step waits for it. That traffic sits on the critical path.

> So tensor parallel belongs only on the fastest link, the vendor link inside one server. That is why an eight GPU server usually caps tensor parallel at eight.

**[Pipeline parallel]**

> Pipeline parallel splits the layers into stages, one stage per GPU, like an assembly line. It only sends the boundary results between stages, so it copes with the slower network between servers.

> The cost is the bubble. At the start the later stages wait for work, and at the end the early stages sit idle. To measure it, I simulated the schedule and counted the idle slots.

**[The bubble, drawn]**

> Here is a four stage pipeline with four micro batches. Blue is a forward step, orange is a backward step.

> Gray is a GPU doing nothing. Six of every fourteen slots, forty-two point nine percent idle, and it matches the formula exactly. The bubble is stages minus one, over micro batches plus stages minus one.

**[Shrinking the bubble]**

> More stages make it worse. Eight stages with eight micro batches wastes forty-seven percent. Give the pipeline more micro batches, thirty-two, and it drops to eighteen percent. A hundred and twenty-eight, five percent.

> A trick called interleaving gives each GPU several smaller chunks and cuts the bubble to roughly a quarter again. The lesson is simple. Keep the pipeline full.

**[Mapping to the hardware]**

> So where does each split go? The rule is that the more often a group talks, the faster the link it needs. Tensor parallel goes inside one server on the vendor link. Pipeline goes across servers. Data parallel, which overlaps with compute, goes outermost.

> Llama three's biggest model was reported as tensor parallel eight inside each server, pipeline sixteen, and data parallel up to a hundred and twenty-eight. A memory trick: tiny cats eat pizza daily, for tensor, context, expert, pipeline, data.

**[The network cost]**

> Now the network, in numbers. Gradients for a seven billion model in half precision are fourteen gigabytes. A ring all reduce sends about twice that per GPU, twenty-eight gigabytes.

> At fifty gigabytes per second between servers, that is point five six seconds per step if nothing overlaps. On the vendor link at four hundred and fifty, point oh six. A seventy billion model over the slow link is five point six seconds per step. This is arithmetic from vendor bandwidths.

**[The silent slowdown]**

> A nasty gotcha. The library that does these group communications is called N C C L. If the right network plugin or settings are missing, it quietly falls back to a slower route. Nothing crashes. Your job is just two to five times slower.

> The habit to build is to turn on N C C L debug logging on every new cluster, and read which transport it picked. Ten seconds of reading can save a month of wasted GPUs.

**[Number formats]**

> Number formats again. B F sixteen is the default for training. Eight bit floats are now proven in production, DeepSeek trained a very large model with them. And the newest four bit format matched eight bit quality on a twelve billion model over ten trillion tokens in one report.

> Smaller formats mean less memory and faster maths on chips that support them. But each needs careful recipes, so adopt them one step at a time.

**[Failures are routine]**

> At scale, things break all the time. Llama three's training run reported four hundred and nineteen unexpected interruptions in fifty-four days. That is one every three point one hours.

> Plan for it. Save checkpoints on a schedule, like lesson two's square root rule. Save them asynchronously like lesson four. And restart automatically from the latest one.

**[Fine-tuning]**

> Most teams never pretrain. They fine tune an existing model. And the cheap way is called LoRA. Freeze the whole model and train two small matrices next to each layer instead.

> I measured it on my small model. With rank eight, LoRA trained under one percent of the parameters, and the optimiser's memory shrank from two hundred and sixty-nine megabytes to two point six. A hundred times less.

**[The usual order]**

> The usual fine tuning order has three steps. First, supervised fine tuning on examples of good answers. Then preference training, such as D P O, where the model learns which of two answers people prefer. Then, for some tasks, reinforcement learning against a checker.

> A variant called Q LoRA also stores the frozen weights in four bits, so a big model fits on one card. I am describing these. They are not measured in this lesson.

**[Tools to know]**

> A quick map of the tools. PyTorch's own stack, with torchrun to launch, F S D P two to shard, and torchtitan as a reference. NVIDIA's Megatron for thousand GPU runs and mixture of experts. JAX with MaxText on TPUs. And Hugging Face Trainer with DeepSpeed for one machine to a few, and for fine tuning.

> For most people reading this, the last one is the right start.

**[ShopNest Copilot]**

> For ShopNest Copilot, we will not pretrain. We will fine tune an eight billion model to answer in our store's style. Full fine tuning would need about a hundred and twenty-eight gigabytes of training state. Sixteen bytes times eight billion.

> LoRA keeps the frozen weights at sixteen gigabytes in the half size format, plus a few megabytes of adapters, and it fits one card. That is our plan.

**[Four words to keep]**

> Four words to carry forward. Optimiser state: the memory the optimiser keeps for each weight. Sharding: giving each GPU a slice instead of a copy.

> Recompute: trading extra compute for less memory. And bubble: the idle time at the start and end of a pipeline.

**[Interview corner]**

> Interview corner. Asked how much memory training needs per parameter, say: about sixteen bytes with Adam in mixed precision. Two for weights, two for gradients, twelve for the master copy and Adam's two memories. I measured sixteen point zero on a real model.

> Asked how to fit a big model, say: shard the state with ZeRO three or F S D P, recompute activations, and split with tensor parallel inside a server and pipeline across servers.

**[Your turn]**

> Your turn. The zip for this lesson has four scripts. The memory ledger and LoRA test, the recomputation test, the pipeline bubble simulator, and the GPU hours calculator.

> Change the model size or the number of micro batches and see what moves. One changed number teaches more than an hour of reading.

**[Recap]**

> Recap. Training needs sixteen bytes per parameter, not two, so a seventy billion model needs eleven hundred and twenty gigabytes. Sharding gets it down to seventeen and a half per GPU on sixty-four. Recompute halves activation memory for about a fifth more time.

> A seven billion run on two trillion tokens is about fifty-nine thousand GPU hours. Keep the chattiest split on the fastest link. LoRA trains under one percent. Next lesson: inference and serving. How to make a trained model answer fast.

**[Next lesson]**

> In the next lesson: inference and serving. How to make a trained model answer fast.

> Subscribe so you don't miss it. See you in the notebook.


## Short 1: Why Training a 70B Model Needs 1,120 GB (Not 140) #shorts

> A seventy billion parameter model is a hundred and forty gigabytes. Training it needs eleven hundred and twenty.

> Training keeps four things in memory. Weights, gradients, and the optimiser, which stores a full precision copy plus two running averages. In the usual recipe that is two plus two plus twelve, sixteen bytes per parameter.

> I measured it on a real small model and got sixteen point zero. Sixteen times seventy billion is eleven hundred and twenty gigabytes.

> Weights are only an eighth of the training bill.


## Short 2: LoRA Trains Under 1% of a Model: 100x Less Memory #shorts

> Fine tuning a model by training less than one percent of it. I measured the memory it saves.

> LoRA freezes the whole model and trains two small matrices beside each layer. On my small model, rank eight trained point nine seven percent of the parameters.

> The optimiser memory fell from two hundred and sixty-nine megabytes to two point six. About a hundred times less. That is why fine tuning fits on one card.

> Most teams should fine tune with LoRA, not pretrain.


## Instagram Reel 1: Why 43% of your GPUs sit idle in a pipeline

> Why forty-three percent of your GPUs can sit idle in a pipeline.

> I simulated a four stage pipeline with four micro batches. Six of every fourteen slots were idle, forty-two point nine percent. With eight stages and a hundred and twenty-eight micro batches, five percent.

> Keep the pipeline full. Save this.
