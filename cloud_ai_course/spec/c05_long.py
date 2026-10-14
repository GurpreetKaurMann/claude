import sys; sys.path.insert(0, '/home/claude/caigen')
from frag import *
from gailab import CODE, OUT

LONG = [
 dict(id='s0', chap='The 1,120 gigabyte surprise', say=[
   "A seventy billion parameter model is a hundred and forty gigabytes of weights. So training it should need a hundred and forty gigabytes, right? Wrong. Training needs one thousand, one hundred and twenty gigabytes, eight times more.",
   "No single GPU holds that. So how do people train big models at all? This lesson answers it. Where the memory goes, how to split it, what it costs, and what breaks along the way."],
  html=[H2('Weights: 140 GB. Training: 1,120 GB.', 0),
        DEF('70B model · weights <b>140 GB</b> · training state <b>1,120 GB</b> · one H100 <b>80 GB</b>', 0, 0.5, style='margin-top:24px;font-size:46px'),
        MARK('the 16-byte rule explains it', 1, 0.6)]),

 dict(id='s1', chap='Where we are', say=[
   "In the earlier lessons we rented chips, packed containers and fed them data. Now we train. This is the most expensive thing in A I, so it pays to understand it.",
   "Plan for the lesson. The memory ledger, how to share it across GPUs, how to save memory by recomputing, how many GPU hours a run needs, the ways to split a model, the network, and what goes wrong. Some of it is measured on a small model on my CPU. The rest is arithmetic and simulation, labelled."],
  html=[H2('The plan', 0),
        GRID([('memory ledger', 0, 0.3), ('sharing it', 0, 0.7), ('recompute', 0, 1.1), ('GPU-hours', 1, 0.3), ('splitting', 1, 0.7), ('network + failures', 1, 1.1)], cols=3, h=140, fs=36),
        SUB('measured on a small model · the rest is arithmetic and simulation', 1, 1.6, style='margin-top:18px')]),

 dict(id='s2', chap='What training is', say=[
   "First, what is training? Think of a teacher marking homework. The model makes a guess. That is the forward pass. We measure how wrong it was. That number is called the loss.",
   "Then comes the backward pass. We work out which numbers inside the model were most to blame. Those blame scores are called gradients. And finally the optimiser nudges every weight a little, in the direction that reduces the error. Repeat billions of times."],
  html=[H2('Training: guess, blame, nudge', 0),
        LIST([('forward: the model guesses', 0, 0.3), ('loss: how wrong was it?', 0, 0.8), ('backward: who is to blame? (gradients)', 1, 0.3), ('optimiser: nudge every weight', 1, 0.9)], kind='ar', numbered=True, style='margin-top:26px;font-size:44px')]),

 dict(id='s3', chap='Four things in memory', say=[
   "During training, four things sit in memory. The weights themselves. The gradients, one per weight. The optimiser's memory, and I will explain that next. And activations, the in between results saved during the forward pass so the backward pass can use them.",
   "The first three scale with the number of parameters. Activations scale with how many tokens are in flight. Together they are why training needs so much more than just storing the model."],
  html=[H2('Four things in memory', 0),
        GRID([('<b>weights</b><br>the model', 0, 0.3), ('<b>gradients</b><br>one per weight', 0, 0.7), ('<b>optimiser state</b><br>its memory', 1, 0.2), ('<b>activations</b><br>saved mid-results', 1, 0.6)], cols=2, h=170, fs=42, style='margin-top:24px')]),

 dict(id='s4', chap='The 16-byte ledger', say=[
   "Here is the ledger for the standard recipe. Weights in the half size format, two bytes. Gradients, two bytes. Then the optimiser. Most use Adam, which keeps two numbers per weight, a running average of the gradient, and of its square, four bytes each.",
   "Adam also keeps a full precision master copy of the weights, four bytes, because tiny nudges vanish in half precision. Two plus two plus twelve is sixteen bytes per parameter.",
   "The weights, the part you thought about, are only a eighth of the bill."],
  html=[H2('The 16-byte ledger', 0), SVG('c4', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c4', 'ledger', 1000, 290, 1)]),

 dict(id='s5', chap='Measured on a real model', say=[
   "Let me check that on a real model. I built a small network with thirty-three and a half million parameters, ran one training step with Adam, and added up the bytes of every tensor.",
   "On a CPU everything is full precision, so weights are four bytes, gradients four, and Adam's two memories eight. Total, sixteen point zero bytes per parameter, exactly. Different recipe, same total."],
  html=[H2('Measured: one real training step', 0), SVG('c5', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c5', 'ledger_measured', 1000, 270, 1)]),

 dict(id='s6', chap='Scaling up', say=[
   "Now scale it. Sixteen bytes times seven billion parameters is a hundred and twelve gigabytes. Seventy billion, eleven hundred and twenty. Four hundred and five billion, nearly six and a half terabytes.",
   "An eighty gigabyte H one hundred cannot hold even the seven billion model's training state. Before activations, before anything else. So we share it."],
  html=[H2('Training state at 16 bytes per parameter', 0), SVG('c6', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c6', 'bigstate', 1000, 280, 1)]),

 dict(id='s7', chap='Sharding the state', say=[
   "The trick is called sharding, with names ZeRO and F S D P. Instead of every GPU keeping everything, each GPU keeps a slice. The first stage shards only the optimiser memory. The next also shards the gradients.",
   "The last stage shards the weights too. For a seventy billion model on sixty-four GPUs, the per GPU share falls from eleven hundred and twenty gigabytes, to two ninety-three, to a hundred and fifty-five, and finally to seventeen and a half.",
   "That last number fits an eighty gigabyte card. The earlier stages still do not."],
  html=[H2('Share the state across GPUs', 0), SVG('c7', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c7', 'zero', 1000, 300, 1)]),

 dict(id='s8', chap='Why stage three', say=[
   "Why do the first two stages not work for seventy billion? They still keep a full copy of the half size weights on every GPU. That is a hundred and forty gigabytes before anything else.",
   "Only the full sharding stage, called ZeRO three or F S D P, splits the weights as well. The price is more network traffic, about one and a half times a plain data parallel run, because the weights must be gathered when needed."],
  html=[H2('Only full sharding fits 70B', 0),
        ROW(COL(CARD('<b>ZeRO-1 and 2</b><br>still keep all bf16 weights<br>140 GB on every GPU', 0, 0.4, style='font-size:36px'), width='48%'),
            COL(CARD('<b>ZeRO-3 / FSDP</b><br>shards the weights too<br>~1.5x the network traffic', 1, 0.3, style='font-size:36px'), width='48%'), style='margin-top:28px')]),

 dict(id='s9', chap='Activations', say=[
   "Now the fourth thing, activations. During the forward pass, every layer's in between results are saved, because the backward pass needs them. They grow with the number of tokens, and with attention, they can grow with the square of the sequence length.",
   "That is why long context training is so hungry. The notebook's worked example for a seventy billion class model at eight thousand tokens is about one point nine terabytes of activations if you keep everything, against about twenty-three gigabytes with recomputation and tensor parallel. A technique called flash attention avoids storing the biggest piece, and the standard trick for the rest is recomputation."],
  html=[H2('Activations: saved mid-results', 0),
        LIST([('grow with tokens in flight', 0, 0.4), ('attention can grow with length squared', 0, 1.0), ('FlashAttention avoids the biggest piece', 1, 0.3), ('the standard trick: recompute', 1, 0.9)], kind='ar', style='margin-top:26px;font-size:44px')]),

 dict(id='s10', chap='Recomputation', say=[
   "Recomputation, also called gradient checkpointing, is a trade. Keep only each block's input. When the backward pass needs the inside of a block, run that block's forward pass again.",
   "You spend extra compute to save memory. I measured it. Twelve blocks, two thousand tokens, on one CPU thread. Each setting ran in its own process, so I could read its peak memory. The machine was shared, so timings are noisy."],
  html=[H2('Trade compute for memory', 0),
        ROW(COL(CARD('<b>normal</b><br>keep every in-between result', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>recompute</b><br>keep block inputs, re-run the rest', 0, 0.9, style='font-size:38px'), width='48%'), style='margin-top:28px'),
        SUB('12 blocks · 2,048 tokens · one CPU thread · separate processes', 1, 0.6, style='margin-top:14px')]),

 dict(id='s11', chap='Recompute, measured', say=[
   "Keeping everything, the activations took seven hundred and ninety-three megabytes. With recomputation, four hundred and twenty-six. About half.",
   "The step time rose from five point six seconds to six point nine. A little under a quarter more.",
   "Half the activation memory for a fifth to a quarter more time. The notebook's rule of thumb is up to a third more compute, so mine is in range."],
  html=[H2('Recompute, measured', 0), SVG('c11', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c11', 'rc_result', 1000, 290, 1)]),

 dict(id='s12', chap='Counting compute', say=[
   "Now compute. A good rule: training a model needs about six times the parameters times the training tokens in floating point operations. Two for the forward pass, four for the backward, per parameter per token.",
   "Those operations run on GPUs at a fraction of their peak speed. The fraction is called M F U, model flops utilisation. Well tuned dense runs on H one hundreds reach roughly thirty-five to forty-five percent."],
  html=[H2('The 6ND rule', 0),
        DEF('training FLOPs ≈ <b>6 × N × D</b><br>N = parameters · D = training tokens', 0, 0.4, style='margin-top:24px;font-size:50px'),
        MARK('MFU: the share of peak speed you really get, about 35 to 45%', 1, 0.5)]),

 dict(id='s13', chap='A worked example', say=[
   "Let us do a worked example. A seven billion model trained on two trillion tokens. Six times seven billion times two trillion is eight point four times ten to the twenty-two operations.",
   "An H one hundred peaks near nine hundred and eighty-nine trillion operations a second. At forty percent M F U, that is about four hundred. Divide, and the run needs about fifty-nine thousand GPU hours. On a thousand and twenty-four GPUs, two point four days.",
   "At an assumed two dollars per GPU hour, about a hundred and eighteen thousand dollars. Real prices vary a lot."],
  html=[H2('7B on 2T tokens', 0), SVG('c13', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c13', 'gpuhours', 1000, 290, 1)]),

 dict(id='s14', chap='MFU honesty', say=[
   "One warning about M F U. It depends on which peak you divide by. Run in a smaller number format and the chip's peak doubles, so the same run looks half as efficient. Compare M F U only between runs that use the same number format.",
   "Also quote M F U, not H F U. The second counts recomputed work, so recomputation makes it look better while the useful work is the same. As a reverse check, DeepSeek reported about two point eight million GPU hours for its large model, which works out to roughly a third of the chip's peak."],
  html=[H2('Quote MFU, and name the peak', 0),
        LIST([('different number format = different peak', 0, 0.4), ('compare MFU only like with like', 0, 1.0), ('MFU counts needed work · HFU counts recompute too', 1, 0.4)], kind='ar', style='margin-top:26px;font-size:44px')]),

 dict(id='s15', chap='How many tokens?', say=[
   "How many tokens should you train on? A famous study called Chinchilla suggested about twenty tokens per parameter for the best use of a fixed compute budget.",
   "But today's models train far longer on purpose. Llama three's biggest model saw about thirty-eight tokens per parameter, and a seven billion model on two trillion tokens sees nearly three hundred. A smaller, longer trained model is cheaper to run afterwards."],
  html=[H2('How many tokens?', 0),
        TABLE(['Model', 'Tokens per parameter'], [(['Chinchilla-optimal', '≈ 20'], 0, 0.4), (['Llama 3 405B (reported)', '≈ 38'], 1, 0.3), (['7B on 2T tokens', '≈ 286'], 1, 0.9)], style='margin-top:26px;font-size:44px'),
        SUB('smaller + longer trained = cheaper to run later', 1, 1.5, style='margin-top:14px')]),

 dict(id='s16', chap='Four ways to split', say=[
   "Sharding the state is one way to share the work. There are four main ways to split a training job. Data parallel, where every GPU runs the same model on different data. Tensor parallel, where the matrices inside each layer are cut up.",
   "Pipeline parallel, where layers are split into stages, like an assembly line. And expert parallel, for models made of many experts. Big runs combine three or four at once.",
   "Each one cuts a different thing, so each one sends different traffic over the network."],
  html=[H2('Four ways to split a model', 0), SVG('c16', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c16', 'split4', 1000, 290, 1)]),

 dict(id='s17', chap='Tensor parallel', say=[
   "Tensor parallel is the chattiest. Every layer, forward and backward, the GPUs must combine their partial results, and the next step waits for it. That traffic sits on the critical path.",
   "So tensor parallel belongs only on the fastest link, the vendor link inside one server. That is why an eight GPU server usually caps tensor parallel at eight."],
  html=[H2('Tensor parallel: the chatty one', 0),
        DEF('cut the matrices inside each layer · <b>every layer</b> the GPUs must meet', 0, 0.4, style='margin-top:24px;font-size:46px'),
        STICKY('Rule', 'only on the <b>fastest link</b>: inside one server', 1, 0.5, style='margin-top:26px;font-size:44px')]),

 dict(id='s18', chap='Pipeline parallel', say=[
   "Pipeline parallel splits the layers into stages, one stage per GPU, like an assembly line. It only sends the boundary results between stages, so it copes with the slower network between servers.",
   "The cost is the bubble. At the start the later stages wait for work, and at the end the early stages sit idle. To measure it, I simulated the schedule and counted the idle slots."],
  html=[H2('Pipeline parallel: an assembly line', 0),
        ROW(COL(CARD('<b>good</b><br>sends only boundary results<br>copes with the slower network', 0, 0.4, style='font-size:36px'), width='48%'),
            COL(CARD('<b>cost</b><br>the bubble: GPUs idle at start and end', 1, 0.3, style='font-size:36px'), width='48%'), style='margin-top:28px')]),

 dict(id='s19', chap='The bubble, drawn', say=[
   "Here is a four stage pipeline with four micro batches. Blue is a forward step, orange is a backward step.",
   "Gray is a GPU doing nothing. Six of every fourteen slots, forty-two point nine percent idle, and it matches the formula exactly. The bubble is stages minus one, over micro batches plus stages minus one."],
  html=[H2('A pipeline, slot by slot', 0), SVG('c19', 1400, 420, 'margin:10px auto 0')],
  svgs=[('c19', 'bubble', 1000, 295, 1)]),

 dict(id='s20', chap='Shrinking the bubble', say=[
   "More stages make it worse. Eight stages with eight micro batches wastes forty-seven percent. Give the pipeline more micro batches, thirty-two, and it drops to eighteen percent. A hundred and twenty-eight, five percent.",
   "A trick called interleaving gives each GPU several smaller chunks and cuts the bubble to roughly a quarter again. The lesson is simple. Keep the pipeline full."],
  html=[H2('Keep the pipeline full', 0), SVG('c20', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c20', 'bubble_tbl', 1000, 300, 1)]),

 dict(id='s21', chap='Mapping to the hardware', say=[
   "So where does each split go? The rule is that the more often a group talks, the faster the link it needs. Tensor parallel goes inside one server on the vendor link. Pipeline goes across servers. Data parallel, which overlaps with compute, goes outermost.",
   "Llama three's biggest model was reported as tensor parallel eight inside each server, pipeline sixteen, and data parallel up to a hundred and twenty-eight. A memory trick: tiny cats eat pizza daily, for tensor, context, expert, pipeline, data."],
  html=[H2('The chattiest group sits closest', 0), SVG('c21', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c21', 'mapping', 1000, 290, 1)]),

 dict(id='s22', chap='The network cost', say=[
   "Now the network, in numbers. Gradients for a seven billion model in half precision are fourteen gigabytes. A ring all reduce sends about twice that per GPU, twenty-eight gigabytes.",
   "At fifty gigabytes per second between servers, that is point five six seconds per step if nothing overlaps. On the vendor link at four hundred and fifty, point oh six. A seventy billion model over the slow link is five point six seconds per step. This is arithmetic from vendor bandwidths."],
  html=[H2('Syncing gradients', 0), SVG('c22', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c22', 'netcost', 1000, 270, 1)]),

 dict(id='s23', chap='The silent slowdown', say=[
   "A nasty gotcha. The library that does these group communications is called N C C L. If the right network plugin or settings are missing, it quietly falls back to a slower route. Nothing crashes. Your job is just two to five times slower.",
   "The habit to build is to turn on N C C L debug logging on every new cluster, and read which transport it picked. Ten seconds of reading can save a month of wasted GPUs."],
  html=[H2('NCCL can quietly pick the slow route', 0),
        OUT(['export NCCL_DEBUG=INFO', '# read which transport it chose'], 0, 0.4, size=36, label='the habit', style='margin-top:24px'),
        MARK('missing plugin = a silent 2 to 5 times slowdown', 1, 0.5)]),

 dict(id='s24', chap='Number formats', say=[
   "Number formats again. B F sixteen is the default for training. Eight bit floats are now proven in production, DeepSeek trained a very large model with them. And the newest four bit format matched eight bit quality on a twelve billion model over ten trillion tokens in one report.",
   "Smaller formats mean less memory and faster maths on chips that support them. But each needs careful recipes, so adopt them one step at a time."],
  html=[H2('Number formats for training', 0),
        TABLE(['Format', 'Status (notebook, Oct 2026)'], [(['BF16', 'the default'], 0, 0.4), (['FP8', 'proven in production (DeepSeek-V3)'], 0, 1.0), (['NVFP4', 'matched FP8 on a 12B model, 10T tokens (one report)'], 1, 0.3)], style='margin-top:24px;font-size:38px')]),

 dict(id='s25', chap='Failures are routine', say=[
   "At scale, things break all the time. Llama three's training run reported four hundred and nineteen unexpected interruptions in fifty-four days. That is one every three point one hours.",
   "Plan for it. Save checkpoints on a schedule, like lesson two's square root rule. Save them asynchronously like lesson four. And restart automatically from the latest one."],
  html=[H2('Something breaks every 3 hours', 0),
        OUT(['419 interruptions in 54 days', '54 × 24 ÷ 419 = one every 3.1 hours'], 0, 0.4, size=34, label='Llama 3 (reported) + arithmetic', style='margin-top:24px'),
        LIST([('checkpoint on a schedule', 1, 0.3), ('save asynchronously', 1, 0.8), ('restart automatically', 1, 1.3)], kind='ar', style='margin-top:18px;font-size:42px')]),

 dict(id='s26', chap='Fine-tuning', say=[
   "Most teams never pretrain. They fine tune an existing model. And the cheap way is called LoRA. Freeze the whole model and train two small matrices next to each layer instead.",
   "I measured it on my small model. With rank eight, LoRA trained under one percent of the parameters, and the optimiser's memory shrank from two hundred and sixty-nine megabytes to two point six. A hundred times less."],
  html=[H2('LoRA: train a sliver', 0), SVG('c26', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c26', 'lora', 1000, 290, 1)]),

 dict(id='s27', chap='The usual order', say=[
   "The usual fine tuning order has three steps. First, supervised fine tuning on examples of good answers. Then preference training, such as D P O, where the model learns which of two answers people prefer. Then, for some tasks, reinforcement learning against a checker.",
   "A variant called Q LoRA also stores the frozen weights in four bits, so a big model fits on one card. I am describing these. They are not measured in this lesson."],
  html=[H2('Fine-tuning, in order', 0),
        LIST([('SFT: learn from good answers', 0, 0.4), ('DPO: learn which answer people prefer', 0, 0.9), ('RL: learn against a checker', 0, 1.4), ('QLoRA: frozen weights in 4 bits', 1, 0.4)], kind='ar', numbered=True, style='margin-top:24px;font-size:42px'),
        SUB('described, not measured here', 1, 1.0, style='margin-top:14px')]),

 dict(id='s28', chap='Tools to know', say=[
   "A quick map of the tools. PyTorch's own stack, with torchrun to launch, F S D P two to shard, and torchtitan as a reference. NVIDIA's Megatron for thousand GPU runs and mixture of experts. JAX with MaxText on TPUs. And Hugging Face Trainer with DeepSpeed for one machine to a few, and for fine tuning.",
   "For most people reading this, the last one is the right start."],
  html=[H2('Which training tool?', 0),
        TABLE(['Situation', 'Start with'], [(['custom PyTorch model', 'FSDP2, torchtitan'], 0, 0.4), (['1,000+ NVIDIA GPUs', 'Megatron Core'], 0, 1.0), (['TPUs', 'JAX + MaxText'], 1, 0.3), (['small scale, fine-tuning', 'HF Trainer'], 1, 0.9)], style='margin-top:22px;font-size:38px')]),

 dict(id='s29', chap='ShopNest Copilot', say=[
   "For ShopNest Copilot, we will not pretrain. We will fine tune an eight billion model to answer in our store's style. Full fine tuning would need about a hundred and twenty-eight gigabytes of training state. Sixteen bytes times eight billion.",
   "LoRA keeps the frozen weights at sixteen gigabytes in the half size format, plus a few megabytes of adapters, and it fits one card. That is our plan."],
  html=[H2('ShopNest Copilot: fine-tune, don\'t pretrain', 0),
        OUT(['full fine-tune: 8B × 16 bytes = 128 GB', 'LoRA: 8B × 2 bytes = 16 GB frozen + small adapters'], 0, 0.4, size=32, label='arithmetic', style='margin-top:24px'),
        MARK('fits one card', 1, 0.6)]),

 dict(id='s30', chap='Four words to keep', say=[
   "Four words to carry forward. Optimiser state: the memory the optimiser keeps for each weight. Sharding: giving each GPU a slice instead of a copy.",
   "Recompute: trading extra compute for less memory. And bubble: the idle time at the start and end of a pipeline."],
  html=[H2('Four words to keep', 0),
        GRID([('<b>optimiser state</b>', 0, 0.3), ('<b>sharding</b>', 0, 0.9), ('<b>recompute</b>', 1, 0.3), ('<b>bubble</b>', 1, 0.9)], cols=2, h=140, fs=44, style='margin-top:30px')]),

 dict(id='s31', chap='Interview corner', say=[
   "Interview corner. Asked how much memory training needs per parameter, say: about sixteen bytes with Adam in mixed precision. Two for weights, two for gradients, twelve for the master copy and Adam's two memories. I measured sixteen point zero on a real model.",
   "Asked how to fit a big model, say: shard the state with ZeRO three or F S D P, recompute activations, and split with tensor parallel inside a server and pipeline across servers."],
  html=[H2('Interview corner', 0),
        Q('How much memory does training need per parameter?', 'About 16 bytes with Adam: 2 + 2 + 12. I measured 16.0 on a real model.', 0, 0.4),
        Q('How do you fit a model that is too big?', 'Shard (ZeRO-3 / FSDP), recompute activations, TP inside a server, PP across servers.', 1, 0.4)]),

 dict(id='s32', chap='Your turn', say=[
   "Your turn. The zip for this lesson has four scripts. The memory ledger and LoRA test, the recomputation test, the pipeline bubble simulator, and the GPU hours calculator.",
   "Change the model size or the number of micro batches and see what moves. One changed number teaches more than an hour of reading."],
  html=[H2('Your turn', 0),
        CARD('<b>l05_memory_ledger.py</b>: ledger, ZeRO and LoRA.<br><b>l05_recompute.py</b>: memory vs time.<br><b>l05_bubble_sim.py</b>: pipeline idle time.<br><b>l05_flops_math.py</b>: GPU-hours and network.', 0, 0.4, style='margin-top:22px;font-size:34px'),
        SUB('one changed number teaches more than an hour of reading', 1, 0.8, style='margin-top:16px')]),

 dict(id='s33', chap='Recap', say=[
   "Recap. Training needs sixteen bytes per parameter, not two, so a seventy billion model needs eleven hundred and twenty gigabytes. Sharding gets it down to seventeen and a half per GPU on sixty-four. Recompute halves activation memory for about a fifth more time.",
   "A seven billion run on two trillion tokens is about fifty-nine thousand GPU hours. Keep the chattiest split on the fastest link. LoRA trains under one percent. Next lesson: inference and serving. How to make a trained model answer fast."],
  html=[H2('Recap', 0),
        GRID([('16 bytes per parameter', 0, 0.3), ('shard: 1,120 → 17.5 GB', 0, 0.9), ('recompute: ½ memory, +20% time', 0, 1.5),
              ('7B on 2T: 59K GPU-hours', 1, 0.3), ('chattiest split, fastest link', 1, 0.9), ('LoRA: under 1% trained', 1, 1.5)], cols=3, h=150, fs=30)]),
]
