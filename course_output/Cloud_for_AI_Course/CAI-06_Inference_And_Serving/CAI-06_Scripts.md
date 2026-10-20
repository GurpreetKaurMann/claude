# CAI-06 · Inference and Serving: Scripts

**Lesson 6 of 12 · Module 3 · Training and serving**

Voice: AI narrator (Kokoro `af_heart`). Final lesson video length: 16:57.

## Long video narration

**[Twelve times faster from one trick]**

> I made a small language model write sixty-four words two ways. Without one trick, it took four point two five seconds. With it, point three five. Twelve times faster, same model, same answer.

> That trick is the K V cache from lesson one, and it is only the first of four in this lesson. We will also measure continuous batching, compression, and speculative decoding. By the end you will know how a trained model is served fast.

**[Intro]**

> Welcome to lesson six of the cloud for A I engineers course, on The Code Notebook.

> The handwritten notes and the code for this lesson are linked in the description.

**[Where we are]**

> Lesson five trained a model. Now we use it, which the field calls inference or serving. For most companies, this is where the money goes every day, so it is worth getting right.

> As always, I label what I measure. The prefill and cache tests run a real, small transformer with random weights on one CPU thread. They measure speed, not quality. The batching and speculation results are simulations, and the compression test uses synthetic weights.

**[Two phases]**

> Every answer has two phases. Imagine being handed a long question and asked to reply out loud. First you read the whole question at once. That is prefill. All the words are processed together, which suits a GPU's thousands of workers. It is compute bound.

> Then you speak the reply one word at a time. That is decode. Each word needs the one before it, so it cannot be done in parallel, and each step re reads the model from memory. It is memory bound, as we saw in lesson one.

> Start fast is prefill. Talk fast is decode. They need different fixes.

**[The four clocks]**

> So we measure speed with several clocks. T T F T, time to first token, is the wait before the first word appears. It is queue time plus prefill.

> T P O T, or I T L, is the gap between words after that. It decides whether the stream feels smooth. Throughput is tokens per second across all users.

> And goodput is the number of requests per second that meet both targets at once. Size your fleet by goodput. Raw throughput can always be bought with worse waits.

**[A latency sum]**

> A simple sum ties them together. Total time is about the first token wait plus the number of remaining tokens times the gap between them. A five hundred token answer with a twenty millisecond gap spends ten seconds just writing.

> That is why people stream tokens to the screen as they appear. The user starts reading after the first token wait, not after the last token.

**[Why decode is slow]**

> Why is decode the slow part? Each new word re reads every weight and the whole cache from memory, but does very little arithmetic with them. The chip waits on memory.

> On an H one hundred, a decode step at batch one uses about one percent of the chip's arithmetic. More flops would not help. Faster memory, fewer bytes, or sharing each read across more users would.

**[My measurement setup]**

> Let me measure it. I wrote a small transformer by hand in PyTorch. Six layers, three hundred and eighty-four wide, about seventeen million parameters, with random weights. Random weights are fine, because I am timing, not judging answers.

> One CPU thread, full precision, best of several tries. A CPU is not a GPU, but the shape of the result, prefill is parallel and decode is not, is the same.

**[Prefill, measured]**

> First, prefill. A sixty-four token prompt took twenty-two point six milliseconds. Two hundred and fifty-six tokens took sixty-two point eight. A thousand and twenty-four took two hundred and sixty-seven.

> Per token, that is about a quarter of a millisecond. Longer prompts cost more in total, so time to first token grows with prompt length.

**[Prefill against decode]**

> Now compare the two phases. Prefill processed about four thousand tokens a second. Decode, one token per step even with a cache, managed about a hundred and eighty-two.

> A decode token costs roughly nineteen times a prefill token. Same model, same machine. Prefill is parallel, decode waits in line.

**[The cache idea]**

> Now the cache. When the model writes word number three hundred, it needs the keys and values of all the earlier words. Without a cache, it recomputes all of them from scratch at every single step.

> With a cache, the earlier keys and values are stored, so each step computes only the new word. It is the waiter with a notepad from lesson one. I tested both on the same task.

**[The cache, measured]**

> With the cache, sixty-four tokens took point three five seconds, about a hundred and eighty-two tokens a second. Without it, four point two five seconds, fifteen tokens a second.

> Twelve point one times slower. And the gap would grow with longer answers, because the no cache version re does more work each step.

**[The formula, checked]**

> The cache is not free. It uses memory. Does the formula from lesson one hold? Two times layers times heads times head size times bytes. For my model, that is two times six times six times sixty-four times four, eighteen thousand, four hundred and thirty-two bytes per token.

> I added up the real tensors after a two hundred and fifty-six token prompt. Four point seven million bytes, which divides to exactly eighteen thousand, four hundred and thirty-two per token. The formula is right.

**[Cache size for big models]**

> For a big model the cache is serious. Take a seventy billion class model with eighty layers, eight cache heads, and heads a hundred and twenty-eight wide. That is about three hundred and twenty kilobytes per token. An eight thousand token chat holds about two and a half gigabytes.

> If the model kept a separate cache head for every attention head, as the oldest designs did, that would be eight times bigger, twenty gigabytes. Sharing cache heads between groups, called grouped query attention, is why modern models use eight.

> A compressed design from DeepSeek, and smaller number formats, cut it further. These sizes come from the notebook's table, as arithmetic.

**[How many chats fit?]**

> Capacity planning follows. Two eighty gigabyte GPUs holding a seventy billion model in eight bit format use about seventy gigabytes for weights. That leaves roughly seventy to eighty for the cache.

> At three hundred and twenty kilobytes per token, that is around thirty chats of eight thousand tokens. Storing the cache in eight bit format doubles it. That is the first lever to pull before you buy more GPUs.

**[Paging and prefixes]**

> Two more cache tricks. Old servers reserved one long block of memory per request, even though most of it stayed empty. PagedAttention, from vLLM, hands out small blocks on demand, like pages in an operating system. Waste drops to under one block per chat.

> And prefix caching. If many requests start with the same system prompt, they share the same keys and values, so that part of prefill is skipped. Put shared content first, byte for byte identical, and your first token wait falls.

**[Batching: the setup]**

> Now batching, the biggest lever for cost. There are two ways to run a batch. Static batching takes thirty-two requests, runs them together, and waits until the slowest one finishes before taking the next thirty-two. Short answers sit finished but waiting.

> Continuous batching re forms the batch after every step. When one request finishes, a waiting one takes its slot straight away. I simulated both. Two thousand requests, thirty-two slots, a twenty-five millisecond step, which is my assumption, and random answer lengths averaging about a hundred and twenty tokens.

**[Throughput, simulated]**

> Static batching delivered three hundred and thirty-five tokens a second. Continuous batching, twelve hundred and forty-three.

> Three point seven times the output from the same GPU, because no slot sat idle waiting for a long answer to end.

**[Latency, simulated]**

> It improves waiting time too. With static batching, the average request finished after three hundred and sixty-six seconds. With continuous batching, ninety-five.

> Short requests no longer wait behind the longest one in their batch. That is why every modern serving engine uses continuous batching.

**[Chunked prefill]**

> One flaw remains. A long prompt's prefill is a big chunk of arithmetic that can hog a whole step. Every other user's reply freezes until it finishes, a stall that can last seconds.

> The fix is chunked prefill. Give each step a budget of tokens. Fill it with the ongoing decodes first, then add a slice of the long prompt. The gaps between words stay smooth, at the price of a slightly longer first token wait for that long prompt.

**[Splitting the phases]**

> Big deployments go one step further. Disaggregation. Run prefill on one pool of GPUs and decode on another. Prefill machines are chosen for arithmetic. Decode machines for memory speed and capacity.

> The cache must travel between them over a fast link. It pays off for long prompts, strict smoothness targets and big mixture of experts models. It does not pay on a few GPUs, where chunked prefill is enough.

**[Which engine?]**

> Which software serves the model? vLLM is the default. It supports the widest range of models and chips and speaks the OpenAI style interface. SGLang is strong when requests share prefixes, as in agents. TensorRT LLM squeezes the last few percent on NVIDIA only.

> Dynamo and llm d add multi machine routing on top. Hugging Face's old server, T G I, is in maintenance mode, and its own advice is to move to vLLM or SGLang. For a laptop, Ollama.

**[A vLLM command]**

> Here is what a real launch looks like, as a sketch. Serve a model, split across two GPUs, store weights in eight bit, and the cache in eight bit too. Cap the context, and tell it how much memory it may claim.

> The last flag, the batched token budget, is the chunked prefill knob. Higher gives more throughput, lower gives smoother gaps. Check the flags against your version, because they change often.

**[Compression]**

> Now compression, called quantisation. Decode time is proportional to the bytes you read, so storing weights in eight bits roughly halves the time per word when memory bound, and four bits roughly quarters it. It also leaves more room for the cache.

> Common formats. Eight bit float is the near lossless default on newer chips. Four bit integer methods store weights only, so the maths stays sixteen bit. The newest four bit float format on Blackwell does true four bit maths.

**[My quantisation test]**

> I tested what plain rounding does. A thousand by thousand weight matrix with a few outlier columns twenty times larger, because large models do have a few such channels. The matrix is synthetic, my own assumption.

> I rounded it to eight and four bits, three ways. One scale for the whole matrix, one per row, and one per group of sixty-four weights. Then I multiplied by random inputs and measured how far the output moved.

**[Quantisation, measured]**

> Eight bits with one scale for the whole matrix moved the output by eight point four percent. One scale per row, four point two. One scale per group of sixty-four, one point four.

> Four bits with a single scale was a disaster, fifty-one percent. Even groups of sixty-four left nineteen percent. Plain four bit rounding is not good enough. Real methods such as A W Q and G P T Q are cleverer, and I did not test them here.

**[Speculative decoding]**

> A last trick. Decode leaves arithmetic idle, so use it. A small cheap draft model guesses the next few words. The big model checks all the guesses in one pass, keeps the correct run, and adds one more. The final text is exactly what the big model would have written.

> The speed up depends on how often guesses are accepted. If each guess is accepted with probability alpha, the expected words per big model pass is one minus alpha to the power of gamma plus one, over one minus alpha. Gamma is the number of guesses.

**[Speculation, simulated]**

> I simulated two hundred thousand passes and the formula matched. With alpha point seven and five guesses, the big model gets about two point nine five words per pass. Assuming the draft costs five percent of a big step, that is a two point three five times speed up.

> At alpha point five five, one point seven three times. At point nine, three point seven five. Everything depends on how predictable your text is.

**[A reality check]**

> A reality check from the notebook. In practice, speculative decoding gives about two to three times on a small model, and only when the batch is small. At large batch sizes decode is already near the compute limit, so the benefit fades.

> One test of an eight billion model got one point eight times on code, and no gain at all on chat. If the acceptance rate falls below about fifty-five percent, it is a net loss. Measure it on your own traffic.

**[Faster attention]**

> One more building block. Attention is the part that gets slow with long inputs. Flash attention rewrites it so the huge table of scores is never stored in memory. The newest version, built for Blackwell chips, reports up to about sixteen hundred teraflops on a B two hundred.

> You rarely write this yourself. Serving engines switch it on for you. What matters is knowing it is why long contexts are affordable at all.

**[API or self-host?]**

> Should you run all this yourself? Managed A P Is bundle it. They offer on demand, batch jobs at about half price, priority tiers, and prompt caching where repeated input costs around a tenth.

> Self hosting wins only at high, steady use, because an idle GPU still costs money. Lesson eleven does the break even sum properly. For now remember that the tricks in this lesson are what the providers use to price so low.

**[ShopNest Copilot]**

> For ShopNest Copilot. Serve an eight billion model with vLLM. Eight bit weights and cache, prefix caching on because every request starts with the same store instructions, and continuous batching with chunked prefill.

> Then measure first token wait and the gap between words under our real traffic, and add speculation only if the acceptance rate is good. Measure, then decide.

**[Four words to keep]**

> Four words to carry forward. T T F T: the wait for the first word. K V cache: stored keys and values so earlier words are not recomputed.

> Continuous batching: refill a slot the moment a request finishes. And quantisation: fewer bits per number, for less memory and faster decode.

**[Interview corner]**

> Interview corner. Asked why decode is slower than prefill, say: prefill processes all prompt tokens in parallel and is compute bound, decode makes one token per step and is memory bound. In my test, a decode token cost about nineteen prefill tokens.

> Asked how to raise throughput, say: continuous batching, a quantised cache, and prefix caching. In my simulation, continuous batching gave three point seven times the tokens per second of static batching.

**[Your turn]**

> Your turn. The zip for this lesson has four scripts. The first measures prefill, decode and the cache on your own machine. The others simulate batching and speculation, and test compression.

> Change the answer length or the number of slots and watch the numbers move. One changed number teaches more than an hour of reading.

**[Recap]**

> Recap. Answers have two phases, prefill which is parallel and decode which waits on memory. The K V cache made my small model twelve times faster, and its size matches the formula. Continuous batching gave three point seven times the throughput in simulation.

> Plain four bit rounding broke a matrix, eight bit per group was fine, and speculation helps most when guesses are predictable. Next lesson: M L Ops. How to ship all of this safely, again and again.

**[Next lesson]**

> In the next lesson: M L Ops. How to ship all of this safely, again and again.

> Subscribe so you don't miss it. See you in the notebook.


## Short 1: This One Trick Made My LLM 12x Faster (KV Cache) #shorts

> I made a model write sixty-four words twelve times faster with one trick. Here it is.

> I built a small transformer by hand and timed it. Without a cache, every new word re runs the whole sequence from scratch. Sixty-four words took four point two five seconds.

> With a K V cache, which stores earlier keys and values, it took point three five. Twelve point one times faster. The model and the answer were identical.

> Store earlier work. Compute only the new word.


## Short 2: Continuous Batching: 3.7x More Output From the Same GPU #shorts

> The same GPU can serve three point seven times more words. The only change is when a batch refills.

> Static batching takes thirty-two requests and waits for the slowest. Continuous batching refills a slot the moment a request finishes. I simulated two thousand requests with random lengths.

> Static gave three hundred and thirty-five tokens a second. Continuous, twelve hundred and forty-three. The step time and slot count are my assumptions.

> Never let a slot wait for the slowest request.


## Instagram Reel 1: Why plain 4-bit rounding breaks a model

> Why plain four bit rounding can break a model.

> I rounded a synthetic weight matrix with a few outlier channels. Eight bits, with a scale per group of sixty-four, moved the output by one point four percent. Plain four bit rounding with one scale, fifty-one percent.

> Smaller scale groups help. Real methods do better. Save this.
