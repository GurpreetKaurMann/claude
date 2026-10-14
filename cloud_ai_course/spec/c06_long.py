import sys; sys.path.insert(0, '/home/claude/caigen')
from frag import *
from gailab import CODE, OUT

LONG = [
 dict(id='s0', chap='Twelve times faster from one trick', say=[
   "I made a small language model write sixty-four words two ways. Without one trick, it took four point two five seconds. With it, point three five. Twelve times faster, same model, same answer.",
   "That trick is the K V cache from lesson one, and it is only the first of four in this lesson. We will also measure continuous batching, compression, and speculative decoding. By the end you will know how a trained model is served fast."],
  html=[H2('Same model. Twelve times faster.', 0),
        DEF('without a cache: <b>4.25 s</b> · with a KV cache: <b>0.35 s</b> (measured)', 0, 0.5, style='margin-top:24px;font-size:48px'),
        MARK('plus continuous batching, compression and speculation', 1, 0.6)]),

 dict(id='s1', chap='Where we are', say=[
   "Lesson five trained a model. Now we use it, which the field calls inference or serving. For most companies, this is where the money goes every day, so it is worth getting right.",
   "As always, I label what I measure. The prefill and cache tests run a real, small transformer with random weights on one CPU thread. They measure speed, not quality. The batching and speculation results are simulations, and the compression test uses synthetic weights."],
  html=[H2('Serving: where the daily money goes', 0),
        GRID([('measured: prefill, decode, cache', 0, 0.3), ('simulated: batching, speculation', 0, 0.8), ('synthetic: compression', 1, 0.3)], cols=3, h=170, fs=34),
        SUB('speed tests use random weights: speed, not quality', 1, 0.8, style='margin-top:20px')]),

 dict(id='s2', chap='Two phases', say=[
   "Every answer has two phases. Imagine being handed a long question and asked to reply out loud. First you read the whole question at once. That is prefill. All the words are processed together, which suits a GPU's thousands of workers. It is compute bound.",
   "Then you speak the reply one word at a time. That is decode. Each word needs the one before it, so it cannot be done in parallel, and each step re reads the model from memory. It is memory bound, as we saw in lesson one.",
   "Start fast is prefill. Talk fast is decode. They need different fixes."],
  html=[H2('Read the question, then speak', 0), SVG('c2', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c2', 'phases', 1000, 290, 1)]),

 dict(id='s3', chap='The four clocks', say=[
   "So we measure speed with several clocks. T T F T, time to first token, is the wait before the first word appears. It is queue time plus prefill.",
   "T P O T, or I T L, is the gap between words after that. It decides whether the stream feels smooth. Throughput is tokens per second across all users.",
   "And goodput is the number of requests per second that meet both targets at once. Size your fleet by goodput. Raw throughput can always be bought with worse waits."],
  html=[H2('The clocks', 0), SVG('c3', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c3', 'metrics', 1000, 290, 1)]),

 dict(id='s4', chap='A latency sum', say=[
   "A simple sum ties them together. Total time is about the first token wait plus the number of remaining tokens times the gap between them. A five hundred token answer with a twenty millisecond gap spends ten seconds just writing.",
   "That is why people stream tokens to the screen as they appear. The user starts reading after the first token wait, not after the last token."],
  html=[H2('How long is an answer?', 0),
        DEF('total ≈ TTFT + (tokens − 1) × gap', 0, 0.4, style='margin-top:24px;font-size:54px'),
        OUT(['500 tokens × 20 ms gap = about 10 s of writing'], 1, 0.4, size=34, label='arithmetic', style='margin-top:22px'),
        MARK('stream the tokens', 1, 1.0)]),

 dict(id='s5', chap='Why decode is slow', say=[
   "Why is decode the slow part? Each new word re reads every weight and the whole cache from memory, but does very little arithmetic with them. The chip waits on memory.",
   "On an H one hundred, a decode step at batch one uses about one percent of the chip's arithmetic. More flops would not help. Faster memory, fewer bytes, or sharing each read across more users would."],
  html=[H2('Decode waits on memory', 0),
        LIST([('every step re-reads weights + cache', 0, 0.4), ('almost no arithmetic per byte', 0, 1.0), ('H100, batch 1: about 1% of peak maths (notebook)', 1, 0.4)], kind='ar', style='margin-top:26px;font-size:44px'),
        STICKY('Three fixes', 'fewer bytes · faster memory · share each read', 1, 0.9, style='margin-top:22px;font-size:40px')]),

 dict(id='s6', chap='My measurement setup', say=[
   "Let me measure it. I wrote a small transformer by hand in PyTorch. Six layers, three hundred and eighty-four wide, about seventeen million parameters, with random weights. Random weights are fine, because I am timing, not judging answers.",
   "One CPU thread, full precision, best of several tries. A CPU is not a GPU, but the shape of the result, prefill is parallel and decode is not, is the same."],
  html=[H2('A small transformer, by hand', 0),
        OUT(['6 layers · 384 wide · 6 heads', '16.8 million parameters (random weights)', 'one CPU thread · float32 · best of several'], 0, 0.4, size=32, label='measured setup', style='margin-top:22px'),
        SUB('timing, not quality · a CPU shows the same shape', 1, 0.6, style='margin-top:14px')]),

 dict(id='s7', chap='Prefill, measured', say=[
   "First, prefill. A sixty-four token prompt took twenty-two point six milliseconds. Two hundred and fifty-six tokens took sixty-two point eight. A thousand and twenty-four took two hundred and sixty-seven.",
   "Per token, that is about a quarter of a millisecond. Longer prompts cost more in total, so time to first token grows with prompt length."],
  html=[H2('Prefill: the wait for the first word', 0), SVG('c7', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c7', 'prefill_ms', 1000, 260, 1)]),

 dict(id='s8', chap='Prefill against decode', say=[
   "Now compare the two phases. Prefill processed about four thousand tokens a second. Decode, one token per step even with a cache, managed about a hundred and eighty-two.",
   "A decode token costs roughly nineteen times a prefill token. Same model, same machine. Prefill is parallel, decode waits in line."],
  html=[H2('Reading is fast. Writing is slow.', 0), SVG('c8', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c8', 'speed', 1000, 270, 1)]),

 dict(id='s9', chap='The cache idea', say=[
   "Now the cache. When the model writes word number three hundred, it needs the keys and values of all the earlier words. Without a cache, it recomputes all of them from scratch at every single step.",
   "With a cache, the earlier keys and values are stored, so each step computes only the new word. It is the waiter with a notepad from lesson one. I tested both on the same task."],
  html=[H2('Cache the earlier work', 0),
        ROW(COL(CARD('<b>no cache</b><br>re-run the whole sequence<br>every step', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>KV cache</b><br>store earlier keys and values<br>compute only the new word', 1, 0.3, style='font-size:38px'), width='48%'), style='margin-top:28px'),
        SUB('task: 64 new tokens after a 256-token prompt', 1, 1.0, style='margin-top:16px')]),

 dict(id='s10', chap='The cache, measured', say=[
   "With the cache, sixty-four tokens took point three five seconds, about a hundred and eighty-two tokens a second. Without it, four point two five seconds, fifteen tokens a second.",
   "Twelve point one times slower. And the gap would grow with longer answers, because the no cache version re does more work each step."],
  html=[H2('64 tokens, with and without', 0), SVG('c10', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c10', 'cache_cmp', 1000, 270, 1)]),

 dict(id='s11', chap='The formula, checked', say=[
   "The cache is not free. It uses memory. Does the formula from lesson one hold? Two times layers times heads times head size times bytes. For my model, that is two times six times six times sixty-four times four, eighteen thousand, four hundred and thirty-two bytes per token.",
   "I added up the real tensors after a two hundred and fifty-six token prompt. Four point seven million bytes, which divides to exactly eighteen thousand, four hundred and thirty-two per token. The formula is right."],
  html=[H2('The cache formula, checked', 0),
        OUT(['formula: 2 × 6 × 6 × 64 × 4 = 18,432 bytes per token', 'real tensors: 4,718,592 bytes ÷ 256 tokens = 18,432'], 0, 0.4, size=30, label='measured', style='margin-top:24px'),
        MARK('the formula is right', 1, 0.6)]),

 dict(id='s12', chap='Cache size for big models', say=[
   "For a big model the cache is serious. Take a seventy billion class model with eighty layers, eight cache heads, and heads a hundred and twenty-eight wide. That is about three hundred and twenty kilobytes per token. An eight thousand token chat holds about two and a half gigabytes.",
   "If the model kept a separate cache head for every attention head, as the oldest designs did, that would be eight times bigger, twenty gigabytes. Sharing cache heads between groups, called grouped query attention, is why modern models use eight.",
   "A compressed design from DeepSeek, and smaller number formats, cut it further. These sizes come from the notebook's table, as arithmetic."],
  html=[H2('KV memory for one 8K-token chat', 0), SVG('c12', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c12', 'kvsize', 1000, 300, 1)]),

 dict(id='s13', chap='How many chats fit?', say=[
   "Capacity planning follows. Two eighty gigabyte GPUs holding a seventy billion model in eight bit format use about seventy gigabytes for weights. That leaves roughly seventy to eighty for the cache.",
   "At three hundred and twenty kilobytes per token, that is around thirty chats of eight thousand tokens. Storing the cache in eight bit format doubles it. That is the first lever to pull before you buy more GPUs."],
  html=[H2('How many chats fit?', 0),
        OUT(['2 × 80 GB GPUs, 70B in FP8: weights ≈ 70 GB', 'left for cache ≈ 70 to 80 GB', '320 KiB per token → about 30 chats of 8K tokens'], 0, 0.4, size=30, label='notebook, derived', style='margin-top:22px'),
        STICKY('First lever', 'FP8 cache = <b>2x</b> the chats', 1, 0.6, style='margin-top:22px;font-size:44px')]),

 dict(id='s14', chap='Paging and prefixes', say=[
   "Two more cache tricks. Old servers reserved one long block of memory per request, even though most of it stayed empty. PagedAttention, from vLLM, hands out small blocks on demand, like pages in an operating system. Waste drops to under one block per chat.",
   "And prefix caching. If many requests start with the same system prompt, they share the same keys and values, so that part of prefill is skipped. Put shared content first, byte for byte identical, and your first token wait falls."],
  html=[H2('Pages and shared prefixes', 0),
        ROW(COL(CARD('<b>paged cache</b><br>small blocks on demand<br>waste under one block per chat', 0, 0.4, style='font-size:36px'), width='48%'),
            COL(CARD('<b>prefix caching</b><br>same start = reuse its cache<br>shared content first', 1, 0.3, style='font-size:36px'), width='48%'), style='margin-top:28px')]),

 dict(id='s15', chap='Batching: the setup', say=[
   "Now batching, the biggest lever for cost. There are two ways to run a batch. Static batching takes thirty-two requests, runs them together, and waits until the slowest one finishes before taking the next thirty-two. Short answers sit finished but waiting.",
   "Continuous batching re forms the batch after every step. When one request finishes, a waiting one takes its slot straight away. I simulated both. Two thousand requests, thirty-two slots, a twenty-five millisecond step, which is my assumption, and random answer lengths averaging about a hundred and twenty tokens."],
  html=[H2('Static or continuous batching?', 0),
        ROW(COL(CARD('<b>static</b><br>wait for the slowest<br>then start the next batch', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>continuous</b><br>refill a slot the moment<br>a request finishes', 1, 0.3, style='font-size:38px'), width='48%'), style='margin-top:28px'),
        SUB('simulation: 2,000 requests · 32 slots · 25 ms step (assumed)', 1, 1.0, style='margin-top:16px')]),

 dict(id='s16', chap='Throughput, simulated', say=[
   "Static batching delivered three hundred and thirty-five tokens a second. Continuous batching, twelve hundred and forty-three.",
   "Three point seven times the output from the same GPU, because no slot sat idle waiting for a long answer to end."],
  html=[H2('Same GPU, 3.7 times the output', 0), SVG('c16', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c16', 'batchsim', 1000, 270, 1)]),

 dict(id='s17', chap='Latency, simulated', say=[
   "It improves waiting time too. With static batching, the average request finished after three hundred and sixty-six seconds. With continuous batching, ninety-five.",
   "Short requests no longer wait behind the longest one in their batch. That is why every modern serving engine uses continuous batching."],
  html=[H2('And requests finish sooner', 0), SVG('c17', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c17', 'finish', 1000, 270, 1)]),

 dict(id='s18', chap='Chunked prefill', say=[
   "One flaw remains. A long prompt's prefill is a big chunk of arithmetic that can hog a whole step. Every other user's reply freezes until it finishes, a stall that can last seconds.",
   "The fix is chunked prefill. Give each step a budget of tokens. Fill it with the ongoing decodes first, then add a slice of the long prompt. The gaps between words stay smooth, at the price of a slightly longer first token wait for that long prompt."],
  html=[H2('Chunked prefill', 0),
        LIST([('a long prefill can freeze everyone else', 0, 0.4), ('give each step a token budget', 1, 0.3), ('decodes first, then a slice of the prompt', 1, 0.8), ('smooth gaps, slightly later first token for the long prompt', 1, 1.3)], kind='ar', style='margin-top:24px;font-size:40px')]),

 dict(id='s19', chap='Splitting the phases', say=[
   "Big deployments go one step further. Disaggregation. Run prefill on one pool of GPUs and decode on another. Prefill machines are chosen for arithmetic. Decode machines for memory speed and capacity.",
   "The cache must travel between them over a fast link. It pays off for long prompts, strict smoothness targets and big mixture of experts models. It does not pay on a few GPUs, where chunked prefill is enough."],
  html=[H2('Disaggregation: two pools', 0), SVG('c19', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c19', 'disagg', 1000, 290, 1)]),

 dict(id='s20', chap='Which engine?', say=[
   "Which software serves the model? vLLM is the default. It supports the widest range of models and chips and speaks the OpenAI style interface. SGLang is strong when requests share prefixes, as in agents. TensorRT LLM squeezes the last few percent on NVIDIA only.",
   "Dynamo and llm d add multi machine routing on top. Hugging Face's old server, T G I, is in maintenance mode, and its own advice is to move to vLLM or SGLang. For a laptop, Ollama."],
  html=[H2('Which serving engine?', 0),
        TABLE(['Engine', 'Pick when'], [(['vLLM', 'the default'], 0, 0.4), (['SGLang', 'shared prefixes, agents'], 0, 0.9), (['TensorRT-LLM', 'all-NVIDIA, last few percent'], 1, 0.3), (['Ollama / llama.cpp', 'laptop and edge'], 1, 0.8)], style='margin-top:24px;font-size:42px'),
        SUB('status as of Oct 2026 (notebook) · TGI: maintenance mode', 1, 1.4, style='margin-top:14px')]),

 dict(id='s21', chap='A vLLM command', say=[
   "Here is what a real launch looks like, as a sketch. Serve a model, split across two GPUs, store weights in eight bit, and the cache in eight bit too. Cap the context, and tell it how much memory it may claim.",
   "The last flag, the batched token budget, is the chunked prefill knob. Higher gives more throughput, lower gives smoother gaps. Check the flags against your version, because they change often."],
  html=[H2('A serving command (sketch)', 0),
        CODE(['vllm serve MODEL_NAME \\', '  --tensor-parallel-size 2 \\', '  --quantization fp8 \\', '  --kv-cache-dtype fp8 \\', '  --max-model-len 32768 \\', '  --gpu-memory-utilization 0.90 \\', '  --max-num-batched-tokens 8192'], 0, 0.3, step=0.8, size=28, hl=False, lang='sh', style='margin-top:16px'),
        SUB('a sketch from the notebook: verify flags for your version', 1, 1.0, style='margin-top:12px')]),

 dict(id='s22', chap='Compression', say=[
   "Now compression, called quantisation. Decode time is proportional to the bytes you read, so storing weights in eight bits roughly halves the time per word when memory bound, and four bits roughly quarters it. It also leaves more room for the cache.",
   "Common formats. Eight bit float is the near lossless default on newer chips. Four bit integer methods store weights only, so the maths stays sixteen bit. The newest four bit float format on Blackwell does true four bit maths."],
  html=[H2('Fewer bits, faster decode', 0),
        LIST([('decode time ∝ bytes read', 0, 0.4), ('8-bit ≈ 2x faster, 4-bit ≈ 4x, when memory-bound', 0, 1.0), ('FP8: the near-lossless default', 1, 0.3), ('4-bit: weights only, or true 4-bit on Blackwell', 1, 0.8)], kind='ar', style='margin-top:24px;font-size:42px')]),

 dict(id='s23', chap='My quantisation test', say=[
   "I tested what plain rounding does. A thousand by thousand weight matrix with a few outlier columns twenty times larger, because large models do have a few such channels. The matrix is synthetic, my own assumption.",
   "I rounded it to eight and four bits, three ways. One scale for the whole matrix, one per row, and one per group of sixty-four weights. Then I multiplied by random inputs and measured how far the output moved."],
  html=[H2('Rounding weights, measured', 0),
        OUT(['1,024 × 1,024 weights, 8 outlier columns ×20 (synthetic)', 'round to int8 / int4 with 3 scale choices', 'error = how far the output moves'], 0, 0.4, size=30, label='measured setup', style='margin-top:22px'),
        SUB('plain rounding, no clever tricks', 1, 0.6, style='margin-top:14px')]),

 dict(id='s24', chap='Quantisation, measured', say=[
   "Eight bits with one scale for the whole matrix moved the output by eight point four percent. One scale per row, four point two. One scale per group of sixty-four, one point four.",
   "Four bits with a single scale was a disaster, fifty-one percent. Even groups of sixty-four left nineteen percent. Plain four bit rounding is not good enough. Real methods such as A W Q and G P T Q are cleverer, and I did not test them here."],
  html=[H2('Output error by format', 0), SVG('c24', 1400, 420, 'margin:10px auto 0')],
  svgs=[('c24', 'quanterr', 1000, 320, 1)]),

 dict(id='s25', chap='Speculative decoding', say=[
   "A last trick. Decode leaves arithmetic idle, so use it. A small cheap draft model guesses the next few words. The big model checks all the guesses in one pass, keeps the correct run, and adds one more. The final text is exactly what the big model would have written.",
   "The speed up depends on how often guesses are accepted. If each guess is accepted with probability alpha, the expected words per big model pass is one minus alpha to the power of gamma plus one, over one minus alpha. Gamma is the number of guesses."],
  html=[H2('Guess cheaply, check once', 0),
        DEF('words per big pass ≈ (1 − α<sup>γ+1</sup>) ÷ (1 − α)', 0, 0.4, style='margin-top:24px;font-size:48px'),
        LIST([('α = how often a guess is accepted', 1, 0.3), ('γ = how many guesses per pass', 1, 0.8), ('the text is exactly the big model\'s', 1, 1.3)], kind='ar', style='margin-top:20px;font-size:40px')]),

 dict(id='s26', chap='Speculation, simulated', say=[
   "I simulated two hundred thousand passes and the formula matched. With alpha point seven and five guesses, the big model gets about two point nine five words per pass. Assuming the draft costs five percent of a big step, that is a two point three five times speed up.",
   "At alpha point five five, one point seven three times. At point nine, three point seven five. Everything depends on how predictable your text is."],
  html=[H2('Speed up by acceptance rate', 0), SVG('c26', 1400, 420, 'margin:10px auto 0')],
  svgs=[('c26', 'specbars', 1000, 320, 1)]),

 dict(id='s27', chap='A reality check', say=[
   "A reality check from the notebook. In practice, speculative decoding gives about two to three times on a small model, and only when the batch is small. At large batch sizes decode is already near the compute limit, so the benefit fades.",
   "One test of an eight billion model got one point eight times on code, and no gain at all on chat. If the acceptance rate falls below about fifty-five percent, it is a net loss. Measure it on your own traffic."],
  html=[H2('Speculation: measure on your traffic', 0),
        LIST([('about 2 to 3x on small models, small batches', 0, 0.4), ('fades at large batch sizes', 0, 1.0), ('one 8B test: 1.8x on code, 1.0x on chat', 1, 0.4), ('acceptance below ~55%: a net loss', 1, 1.0)], kind='ar', style='margin-top:24px;font-size:42px')]),

 dict(id='s28', chap='Faster attention', say=[
   "One more building block. Attention is the part that gets slow with long inputs. Flash attention rewrites it so the huge table of scores is never stored in memory. The newest version, built for Blackwell chips, reports up to about sixteen hundred teraflops on a B two hundred.",
   "You rarely write this yourself. Serving engines switch it on for you. What matters is knowing it is why long contexts are affordable at all."],
  html=[H2('FlashAttention: never store the big table', 0),
        DEF('rewrites attention so the score table is never kept in memory', 0, 0.4, style='margin-top:24px;font-size:46px'),
        MARK('on by default in the engines · you rarely write it', 1, 0.5)]),

 dict(id='s29', chap='API or self-host?', say=[
   "Should you run all this yourself? Managed A P Is bundle it. They offer on demand, batch jobs at about half price, priority tiers, and prompt caching where repeated input costs around a tenth.",
   "Self hosting wins only at high, steady use, because an idle GPU still costs money. Lesson eleven does the break even sum properly. For now remember that the tricks in this lesson are what the providers use to price so low."],
  html=[H2('Managed API or self-host?', 0),
        LIST([('on-demand, batch (~50% off), priority tiers', 0, 0.4), ('prompt caching: repeated input about 10%', 0, 1.0), ('self-host only at high, steady use', 1, 0.4), ('break-even sum: lesson 11', 1, 1.0)], kind='ar', style='margin-top:24px;font-size:42px'),
        SUB('notebook, Oct 2026', 1, 1.5, style='margin-top:14px')]),

 dict(id='s30', chap='ShopNest Copilot', say=[
   "For ShopNest Copilot. Serve an eight billion model with vLLM. Eight bit weights and cache, prefix caching on because every request starts with the same store instructions, and continuous batching with chunked prefill.",
   "Then measure first token wait and the gap between words under our real traffic, and add speculation only if the acceptance rate is good. Measure, then decide."],
  html=[H2('ShopNest Copilot: serving plan', 0),
        TABLE(['Piece', 'Choice'], [(['engine', 'vLLM, 8B model'], 0, 0.4), (['bytes', 'FP8 weights + FP8 cache'], 0, 0.9), (['reuse', 'prefix caching (same store instructions)'], 1, 0.3), (['batching', 'continuous + chunked prefill'], 1, 0.8), (['speculation', 'only if acceptance is good'], 1, 1.3)], style='margin-top:22px;font-size:38px')]),

 dict(id='s31', chap='Four words to keep', say=[
   "Four words to carry forward. T T F T: the wait for the first word. K V cache: stored keys and values so earlier words are not recomputed.",
   "Continuous batching: refill a slot the moment a request finishes. And quantisation: fewer bits per number, for less memory and faster decode."],
  html=[H2('Four words to keep', 0),
        GRID([('<b>TTFT</b>', 0, 0.3), ('<b>KV cache</b>', 0, 0.9), ('<b>continuous batching</b>', 1, 0.3), ('<b>quantisation</b>', 1, 0.9)], cols=2, h=140, fs=44, style='margin-top:30px')]),

 dict(id='s32', chap='Interview corner', say=[
   "Interview corner. Asked why decode is slower than prefill, say: prefill processes all prompt tokens in parallel and is compute bound, decode makes one token per step and is memory bound. In my test, a decode token cost about nineteen prefill tokens.",
   "Asked how to raise throughput, say: continuous batching, a quantised cache, and prefix caching. In my simulation, continuous batching gave three point seven times the tokens per second of static batching."],
  html=[H2('Interview corner', 0),
        Q('Why is decode slower than prefill?', 'Prefill is parallel and compute-bound. Decode is one token per step and memory-bound. About 19x per token in my test.', 0, 0.4),
        Q('How do you raise throughput?', 'Continuous batching, a quantised KV cache, prefix caching. Continuous batching gave 3.7x in my simulation.', 1, 0.4)]),

 dict(id='s33', chap='Your turn', say=[
   "Your turn. The zip for this lesson has four scripts. The first measures prefill, decode and the cache on your own machine. The others simulate batching and speculation, and test compression.",
   "Change the answer length or the number of slots and watch the numbers move. One changed number teaches more than an hour of reading."],
  html=[H2('Your turn', 0),
        CARD('<b>l06_decode_kv.py</b>: prefill, decode and the cache.<br><b>l06_batching_sim.py</b>: static vs continuous.<br><b>l06_quant_error.py</b>: rounding error.<br><b>l06_spec_decode.py</b>: speculation.', 0, 0.4, style='margin-top:22px;font-size:34px'),
        SUB('one changed number teaches more than an hour of reading', 1, 0.8, style='margin-top:16px')]),

 dict(id='s34', chap='Recap', say=[
   "Recap. Answers have two phases, prefill which is parallel and decode which waits on memory. The K V cache made my small model twelve times faster, and its size matches the formula. Continuous batching gave three point seven times the throughput in simulation.",
   "Plain four bit rounding broke a matrix, eight bit per group was fine, and speculation helps most when guesses are predictable. Next lesson: M L Ops. How to ship all of this safely, again and again."],
  html=[H2('Recap', 0),
        GRID([('prefill parallel · decode waits', 0, 0.3), ('KV cache: 12x faster', 0, 0.9), ('continuous batching: 3.7x', 0, 1.5),
              ('plain int4: 51% error', 1, 0.3), ('int8 groups: 1.4%', 1, 0.9), ('speculation: 2 to 3x, if predictable', 1, 1.5)], cols=3, h=150, fs=30)]),
]
