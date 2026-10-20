import sys; sys.path.insert(0, '/home/claude/caigen')
from cai_lib import *
from c06_diagrams import DIAGRAMS
from c06_long import LONG
from c06_notes import NOTES

L = dict(
 code='CAI-06', num=6, num_word='six', slug='Inference_And_Serving',
 title='Inference and Serving', title_html='Inference<br>&amp; serving', title_size=130,
 tagline='How to make a trained model answer fast, and cheaply.', module='Module 3 · Training and serving',
 toc=['Prefill and decode', 'The KV cache, measured', 'Cache size', 'Continuous batching', 'Quantisation', 'Speculative decoding', 'Interview Q&amp;A'],
 data_label='Course project', project='ShopNest Copilot', project_desc='the AI support assistant we move to the cloud, step by step',
 prev='CAI-05', next=('CAI-07', '<b>MLOps and LLMOps</b>: how to ship all of this safely, again and again'),
 next_say='M L Ops. How to ship all of this safely, again and again.',
 diagrams=DIAGRAMS, long=LONG, notes=NOTES,
 glow=dict(a='INFERENCE', b='AND SERVING', icons=['chat1', '>', 'gauge2']),
 thumb=dict(title='Inference<br><span class="hl">&amp; serving</span>', size=110, sub='12x from one trick', chips=('KV cache', '4.25 s to 0.35 s'), mini='mini_thumb'),

 short1=mk_short(1, 'The_KV_Cache_Made_It_12x_Faster', "I made a model write sixty-four words twelve times faster with one trick. Here it is.",
   ('12X FASTER', 'ONE TRICK', 130, 120),
   ["I built a small transformer by hand and timed it. Without a cache, every new word re runs the whole sequence from scratch. Sixty-four words took four point two five seconds.",
    "With a K V cache, which stores earlier keys and values, it took point three five. Twelve point one times faster. The model and the answer were identical."],
   'mini_cache', "Store earlier work. Compute only the new word.", 'Trick', 'the <b>KV cache</b>', dict(title='12x faster,<br><span class="hl">one trick</span>', size=100, sub='the KV cache, measured', mini='mini_cache'),
   dict(title='This One Trick Made My LLM 12x Faster (KV Cache) #shorts',
     desc="Small transformer written by hand in PyTorch (random weights, one CPU thread). 64 new tokens after a 256-token prompt:\n• without a KV cache: 4.25 s (15 tokens/s)\n• with a KV cache: 0.35 s (182 tokens/s)\n\n12.1x faster. Measured speed, not answer quality.\n\nFull lesson: Cloud for AI Engineers, lesson 6.",
     tags='shorts, kv cache explained, llm inference speed, how llms generate text, transformer inference, cloud for ai engineers, the code notebook',
     pinned='Did you know every word is generated one at a time? 👇')),

 short2=mk_short(2, 'Continuous_Batching_3_7x_Throughput', "The same GPU can serve three point seven times more words. The only change is when a batch refills.",
   ('3.7X', 'THE OUTPUT', 170, 120),
   ["Static batching takes thirty-two requests and waits for the slowest. Continuous batching refills a slot the moment a request finishes. I simulated two thousand requests with random lengths.",
    "Static gave three hundred and thirty-five tokens a second. Continuous, twelve hundred and forty-three. The step time and slot count are my assumptions."],
   'mini_cbatch', "Never let a slot wait for the slowest request.", 'Rule', 'refill a slot<br><b>immediately</b>', dict(title='3.7x the output,<br><span class="hl">same GPU</span>', size=96, sub='continuous batching, simulated', mini='mini_cbatch'),
   dict(title='Continuous Batching: 3.7x More Output From the Same GPU #shorts',
     desc="Simulation: 2,000 requests, 32 slots, 25 ms per step (assumed), mean answer 119 tokens:\n• static batching: 335 tokens/s, mean finish 366 s\n• continuous batching: 1,243 tokens/s, mean finish 95 s\n\nA simulation with assumed numbers.\n\nFull lesson: Cloud for AI Engineers, lesson 6.",
     tags='shorts, continuous batching, llm serving, vllm, llm throughput, inference optimization, cloud for ai engineers, the code notebook',
     pinned='Do you serve with vLLM or something else? 👇')),

 reel=mk_reel('Plain_4_Bit_Rounding_Breaks_Models', ["Why plain four bit rounding can break a model.",
   "I rounded a synthetic weight matrix with a few outlier channels. Eight bits, with a scale per group of sixty-four, moved the output by one point four percent. Plain four bit rounding with one scale, fifty-one percent."],
   "Smaller scale groups help. Real methods do better. Save this.", '51% ERROR', ['int8 in groups: 1.4% error', 'plain int4: 51% error'], [3.4, 6.2], 'Test it', 'smaller groups,<br><b>less error</b>',
   dict(title='Plain 4-bit<br><span class="hl">breaks models</span>', size=100, sub='51% vs 1.4% error', mini='mini_quant'),
   dict(title='Why plain 4-bit rounding breaks a model',
     caption="Quantisation, measured on a synthetic matrix with outliers. 🔢\n\n🟢 int8, groups of 64: 1.4% output error\n🟠 int4, groups of 64: 19%\n🔴 int4, one scale for the whole matrix: 51%\n\nPlain rounding is not enough at 4 bits. Real methods (AWQ, GPTQ) do better, I did not test them here.\n\nSave this. Full lesson on YouTube: The Code Notebook.",
     pinned="Lesson 7 next: MLOps and LLMOps, shipping it safely 🚀 Follow so you don't miss it!")),

 upload=dict(
   title='Why Your LLM Is Slow: 12x Faster From One Trick (KV Cache, Batching, Quantization)',
   hook="Lesson 6 of Cloud for AI Engineers. A small model wrote 64 words in 4.25 s without a KV cache and 0.35 s with one: 12 times faster. This lesson covers the four tricks behind fast, cheap model serving.",
   what="We split an answer into prefill and decode, learn the four latency clocks, measure prefill and decode and the KV cache on a small real transformer, check the cache-size formula, plan cache capacity for a 70B model, simulate static versus continuous batching, explain chunked prefill and disaggregation, compare serving engines, test how rounding weights to 8 and 4 bits changes error, and simulate speculative decoding. Speed tests use random weights on a CPU, batching and speculation are simulations with assumed numbers, and the rounding test uses synthetic weights.",
   bullets=['Prefill versus decode: read the question, then speak', 'TTFT, inter-token latency, throughput and goodput', 'Measured: prefill 22.6 ms for 64 tokens, 266.6 ms for 1,024', 'A decode token costs about 19 prefill tokens (measured)', 'The KV cache: 12.1x faster, and the formula checked exactly',
            'KV cache size for a 70B model and how many chats fit', 'PagedAttention and prefix caching', 'Continuous batching: 3.7x throughput (simulation)', 'Chunked prefill and disaggregation', 'vLLM, SGLang, TensorRT-LLM and when to pick each',
            'Quantisation measured: int8 groups 1.4% error, plain int4 51%', 'Speculative decoding: the formula, simulated and checked', 'Managed API or self-host', 'ShopNest Copilot serving plan', 'Interview questions with answers'],
   hashtags='#llm #inference #vllm #ai #aiengineering',
   tags='kv cache explained, llm inference optimization, continuous batching, vllm tutorial, prefill vs decode, ttft, quantization llm, speculative decoding, how to serve llm, llm latency, cloud for ai engineers, the code notebook',
   pinned="Speed tests use a small random-weight model on a CPU (timing, not quality). Batching and speculation are simulations with assumed numbers. 📊\n\nQuestion for you 👇\nWhich surprised you more: a 12x speed-up from caching, or plain 4-bit rounding giving 51% error?"),
)

import interview; L['notes'] = interview.add(L['notes'], L['num'])
