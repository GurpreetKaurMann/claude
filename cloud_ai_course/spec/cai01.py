import sys; sys.path.insert(0, '/home/claude/caigen')
from frag import *
from gailab import CODE, OUT
from c01_diagrams import DIAGRAMS
from c01_long import LONG
from c01_notes import NOTES


def vs(id, say, html, svgs=()): return dict(id=id, say=say, html=html, svgs=list(svgs))


L = dict(
 code='CAI-01', num=1, num_word='one', slug='Will_Your_Model_Fit_On_A_GPU',
 title='Will Your Model Fit?', title_html='Will your<br>model fit?', title_size=130,
 tagline='GPUs in plain English: memory size, memory speed, compute and connection.', module='Module 1 · Compute',
 toc=['The four numbers', 'Weights in gigabytes', 'Precision', 'The KV cache', 'Memory speed, measured', 'Batching', 'Interview Q&amp;A'],
 data_label='Course project', project='ShopNest Copilot', project_desc='the AI support assistant we move to the cloud, step by step',
 prev='—', next=('CAI-02', '<b>Renting compute</b>: which chip, what it costs, spot and autoscaling'),
 next_say='renting compute. Which chip, what it really costs, and how spot machines and autoscaling save money.',
 diagrams=DIAGRAMS, long=LONG, notes=NOTES,
 glow=dict(a='WILL IT FIT', b='ON A GPU', icons=['chip1', '>', 'gauge2']),
 thumb=dict(title='Will your<br>model <span class="hl">fit?</span>', size=124, sub='the 70B model that fits, then fails',
            chips=('70 GB weights', '187 GB needed'), mini='mini_thumb'),

 short1=dict(slug='The_Model_Fits_The_Chats_Do_Not', scenes=[
   vs('a', ["A seventy billion parameter model fits on one H one hundred. Then it fails. Here is why."],
      ['<div class="center" style="padding-top:60px">' + BIG('it fits.', 0, size=150, color='var(--teal)') + BIG('then it fails', 0, 0.6, size=110, color='var(--acc)') + '</div>']),
   vs('b', ["In the smaller format the weights are seventy gigabytes. The card has eighty. Fine.",
            "But every open chat keeps notes in memory. Thirty-two chats of eight thousand tokens add eighty-six gigabytes. The total needed is one hundred and eighty-seven. That is arithmetic with an assumed model shape."],
      [SVG('v1b', 960, 330, 'margin-top:40px')], [('v1b', 'mini_fit', 760, 260, 1.15)]),
   vs('c', ["So never ask if the model fits. Ask if the model and its chats fit."],
      ['<div class="center" style="padding-top:60px">', STICKY('Ask this', 'model <b>and chats</b><br>fit?', 0, style='font-size:76px'), '</div>'])],
   cover=dict(label='Cloud for AI · Short', title='The model fits.<br>The <span class="hl">chats</span> don\'t', size=96, sub='70 GB vs 187 GB', sub_off=470, card_off=590, mini='mini_fit'),
   upload=dict(title="A 70B Model Fits Your GPU, Then Fails (Here's Why) #shorts",
     desc="70B parameters in FP8 = 70 GB of weights. One H100 has 80 GB. It fits... until people start chatting.\n\nEvery open chat keeps a KV cache in GPU memory:\n• 32 chats × 8,192 tokens = 85.9 GB of notes\n• plus 20% headroom = 187 GB needed\n\nArithmetic with an assumed model shape (80 layers, 8 KV heads, head size 128). GPU memory from vendor specs, Oct 2026.\n\nFull lesson: Cloud for AI Engineers, lesson 1.",
     tags='shorts, gpu memory, kv cache, llm serving, will my model fit, h100, cloud for ai engineers, the code notebook',
     pinned='Did you know the chat notes can use more memory than the model? 👇')),

 short2=dict(slug='4x_The_Data_8x_The_Time', scenes=[
   vs('a', ["Four times the data took eight times longer. I measured it."],
      ['<div class="center" style="padding-top:60px">' + BIG('4x the data', 0, size=130, color='var(--teal)') + BIG('8x the time', 0, 0.6, size=130, color='var(--acc)') + '</div>']),
   vs('b', ["On my C P U, a sixty-seven megabyte table took two point four milliseconds to multiply by one vector. A two hundred and sixty-eight megabyte table took twenty.",
            "The small one fit in the chip's fast cache. The big one came from slower main memory. Chat models read all their weights for every word, so memory speed sets the pace."],
      [SVG('v2b', 960, 330, 'margin-top:40px')], [('v2b', 'mini_mem', 760, 260, 1.15)]),
   vs('c', ["Faster memory helps more than a faster chip. That is what H B M is for."],
      ['<div class="center" style="padding-top:60px">', STICKY('Remember', 'chat speed =<br><b>memory speed</b>', 0, style='font-size:76px'), '</div>'])],
   cover=dict(label='Cloud for AI · Short', title='4x the data,<br><span class="hl">8x</span> the time', size=104, sub='measured, not quoted', sub_off=430, card_off=560, mini='mini_mem'),
   upload=dict(title='Why AI Chips Need Special Memory (I Measured It) #shorts',
     desc="One token of a chat model = reading ALL the weights once, so memory speed sets the pace.\n\nMeasured on a CPU, one core, matrix × vector:\n• 67 MB table: 2.43 ms\n• 268 MB table: 20.35 ms\n\n4x the bytes, 8.4x the time. The small table fit in the CPU cache.\n\nThis is a CPU, not a GPU. The law is the same: time ≥ weight bytes ÷ bandwidth.\n\nFull lesson: Cloud for AI Engineers, lesson 1.",
     tags='shorts, memory bandwidth, hbm, gpu memory, llm inference, why gpus need fast memory, cloud for ai engineers, the code notebook',
     pinned='Would you rather have a faster GPU or faster memory for chat? 👇')),

 reel=dict(slug='Why_Batching_Makes_AI_Cheap', speed=1.08, scenes=[
   vs('a', ["Why serving many people at once makes A I cheap.",
            "I tested one token at a time on my C P U, then two hundred and fifty-six at once. One at a time, about three hundred and ninety tokens a second. Two hundred and fifty-six, about four thousand."],
      ['<div class="center">' + BIG('1 vs 256', 0, size=130, color='var(--acc)') + '</div>',
       '<div style="font-size:48px;margin-top:50px">',
       LIST([('1 at a time: ~390 tokens/s', 1, 3.4), ('256 at once: ~4,000 tokens/s', 1, 6.4)], kind='ar'), '</div>']),
   vs('b', ["About ten times the output, because reading the weights once served everyone. Save this."],
      ['<div class="center" style="padding-top:80px">', STICKY('Measured', '<b>~10x</b> tokens/s', 0, style='font-size:96px'), '</div>'])],
   cover=dict(label='Save this for later', title='Why batching<br>makes AI<br><span class="hl">cheap</span>', size=100, sub='1 at a time vs 256', sub_off=470, card_off=590, mini='mini_batch'),
   upload=dict(title='Why batching makes AI cheap',
     caption="Why serving many people at once makes AI cheaper. 💸\n\nI measured it on a CPU (one core):\n1️⃣ one token at a time: about 390 tokens/s\n2️⃣5️⃣6️⃣ at once: about 4,000 tokens/s\n\nAbout 10x the output. Each step took about 24x longer, but the weights were read once for everyone.\n\nThat's batching, and it's why chat APIs can be priced so low.\n\nSave this. Full lesson on YouTube: The Code Notebook.",
     pinned="Lesson 2 next: which GPU to rent, what it costs, and how spot machines cut the bill 💸 Follow so you don't miss it!")),

 upload=dict(
   title='Why Your AI Model Fits on the GPU, Then Crashes (The 187 GB Trap)',
   hook="Lesson 1 of Cloud for AI Engineers. A 70 billion parameter model fits on one H100. Then 32 people start chatting and you need 187 GB. This lesson explains why, and gives you the sum.",
   what="We learn the four numbers on every GPU spec sheet (memory size, memory speed, compute, connection), turn parameters into gigabytes, meet the KV cache, and measure why chat speed is set by memory speed. Chip specs are vendor figures from October 2026, the sums are labelled arithmetic, and the CPU tests are measured by me.",
   bullets=['The four numbers on every GPU spec sheet',
            'Weights in gigabytes: parameters × bytes per number',
            'Precision: BF16, FP8 and FP4 in plain English',
            'GPU memory tiers: 80, about 141 to 192, 288 GB',
            'The KV cache: why 32 chats need 86 GB of notes',
            'The fit rule: weights + chats + headroom',
            'Measured: 4x the bytes took 8.4x the time on my CPU',
            'Same law on H100, H200 and B200 (arithmetic from specs)',
            'Batching: about 10x the tokens per second, measured',
            'Why the connection between GPUs matters for big models',
            'ShopNest Copilot: sizing our own assistant',
            'Interview questions with answers'],
   hashtags='#cloudcomputing #gpu #ai #llm #aiengineering',
   tags='will my model fit on a gpu, gpu memory explained, kv cache explained, llm memory, h100 vs h200, how much gpu memory do I need, hbm memory bandwidth, batching llm, cloud for ai engineers, ai infrastructure for beginners, the code notebook',
   pinned="Every measured number in this lesson came from code that ran on a CPU, and every GPU figure is labelled as a vendor number from Oct 2026. 📊\n\nQuestion for you 👇\nWhich surprised you more: the chats needing more memory than the model, or 4x the data taking 8x the time?"),
)
