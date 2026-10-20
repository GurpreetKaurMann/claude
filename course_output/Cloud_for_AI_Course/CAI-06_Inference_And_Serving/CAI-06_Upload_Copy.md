# CAI-06 Upload Copy

## 1. Lesson video (YouTube)

**Title:** Why Your LLM Is Slow: 12x Faster From One Trick (KV Cache, Batching, Quantization)

**Description:**
```
Lesson 6 of Cloud for AI Engineers. A small model wrote 64 words in 4.25 s without a KV cache and 0.35 s with one: 12 times faster. This lesson covers the four tricks behind fast, cheap model serving.
We split an answer into prefill and decode, learn the four latency clocks, measure prefill and decode and the KV cache on a small real transformer, check the cache-size formula, plan cache capacity for a 70B model, simulate static versus continuous batching, explain chunked prefill and disaggregation, compare serving engines, test how rounding weights to 8 and 4 bits changes error, and simulate speculative decoding. Speed tests use random weights on a CPU, batching and speculation are simulations with assumed numbers, and the rounding test uses synthetic weights.
⏮️ Previous lesson: <CAI-05 link>

In this lesson:
✅ Prefill versus decode: read the question, then speak
✅ TTFT, inter-token latency, throughput and goodput
✅ Measured: prefill 22.6 ms for 64 tokens, 266.6 ms for 1,024
✅ A decode token costs about 19 prefill tokens (measured)
✅ The KV cache: 12.1x faster, and the formula checked exactly
✅ KV cache size for a 70B model and how many chats fit
✅ PagedAttention and prefix caching
✅ Continuous batching: 3.7x throughput (simulation)
✅ Chunked prefill and disaggregation
✅ vLLM, SGLang, TensorRT-LLM and when to pick each
✅ Quantisation measured: int8 groups 1.4% error, plain int4 51%
✅ Speculative decoding: the formula, simulated and checked
✅ Managed API or self-host
✅ ShopNest Copilot serving plan
✅ Interview questions with answers

⏱️ Chapters
0:00 Twelve times faster from one trick
0:29 Intro
0:39 Where we are
1:08 Two phases
1:45 The four clocks
2:17 A latency sum
2:41 Why decode is slow
3:05 My measurement setup
3:33 Prefill, measured
3:57 Prefill against decode
4:18 The cache idea
4:42 The cache, measured
5:03 The formula, checked
5:35 Cache size for big models
6:17 How many chats fit?
6:44 Paging and prefixes
7:17 Batching: the setup
7:54 Throughput, simulated
8:10 Latency, simulated
8:30 Chunked prefill
8:59 Splitting the phases
9:27 Which engine?
10:04 A vLLM command
10:30 Compression
11:01 My quantisation test
11:29 Quantisation, measured
11:58 Speculative decoding
12:33 Speculation, simulated
13:01 A reality check
13:30 Faster attention
13:57 API or self-host?
14:25 ShopNest Copilot
14:50 Four words to keep
15:11 Interview corner
15:42 Your turn
16:03 Recap
16:34 Next lesson

Next lesson → CAI-07: MLOps and LLMOps: how to ship all of this safely, again and again

🌐 Website: https://thecodenotebook.com/
📸 Instagram: https://www.instagram.com/thecodenotebookyt/

#llm #inference #vllm #ai #aiengineering
```

**Tags:**
```
kv cache explained, llm inference optimization, continuous batching, vllm tutorial, prefill vs decode, ttft, quantization llm, speculative decoding, how to serve llm, llm latency, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Speed tests use a small random-weight model on a CPU (timing, not quality). Batching and speculation are simulations with assumed numbers. 📊

Question for you 👇
Which surprised you more: a 12x speed-up from caching, or plain 4-bit rounding giving 51% error?
```

**Thumbnail:** CAI-06_Thumbnail.png

---

## 2. Short 1 (YouTube Shorts)

**Title:** This One Trick Made My LLM 12x Faster (KV Cache) #shorts

**Description:**
```
Small transformer written by hand in PyTorch (random weights, one CPU thread). 64 new tokens after a 256-token prompt:
• without a KV cache: 4.25 s (15 tokens/s)
• with a KV cache: 0.35 s (182 tokens/s)

12.1x faster. Measured speed, not answer quality.

Full lesson: Cloud for AI Engineers, lesson 6.
```

**Tags:**
```
shorts, kv cache explained, llm inference speed, how llms generate text, transformer inference, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Did you know every word is generated one at a time? 👇
```

**Cover:** CAI-06_Short1_Cover.png

---

## 3. Short 2 (YouTube Shorts)

**Title:** Continuous Batching: 3.7x More Output From the Same GPU #shorts

**Description:**
```
Simulation: 2,000 requests, 32 slots, 25 ms per step (assumed), mean answer 119 tokens:
• static batching: 335 tokens/s, mean finish 366 s
• continuous batching: 1,243 tokens/s, mean finish 95 s

A simulation with assumed numbers.

Full lesson: Cloud for AI Engineers, lesson 6.
```

**Tags:**
```
shorts, continuous batching, llm serving, vllm, llm throughput, inference optimization, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Do you serve with vLLM or something else? 👇
```

**Cover:** CAI-06_Short2_Cover.png

---

## 4. Instagram Reel 1

**Caption:**
```
Quantisation, measured on a synthetic matrix with outliers. 🔢

🟢 int8, groups of 64: 1.4% output error
🟠 int4, groups of 64: 19%
🔴 int4, one scale for the whole matrix: 51%

Plain rounding is not enough at 4 bits. Real methods (AWQ, GPTQ) do better, I did not test them here.

Save this. Full lesson on YouTube: The Code Notebook.
```

**First comment (pin it):**
```
Lesson 7 next: MLOps and LLMOps, shipping it safely 🚀 Follow so you don't miss it!
```

**Cover:** CAI-06_Reel1_Cover_Instagram.png

---
