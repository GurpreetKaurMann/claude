NOTES = [
 # ---- page 1
 [('h2', '1', 'The cloud, for AI'),
  ('def', 'The cloud = <b>renting computers by the hour</b>. For AI the computers that matter are GPUs: too costly to buy, '
          'hard to get, so you rent the right ones for the time you need them.'),
  ('diagram', 'workers', 62, 1000, 300),
  ('list', 'arrow', ['A <b>CPU</b> has a few strong workers, good at many different jobs',
                     'A <b>GPU</b> has thousands of simple workers doing the same sum at once',
                     'AI is mostly one job: multiplying huge tables of numbers, so it fits a GPU perfectly']),
  ('sticky', '', 'The rule of this course', 'A number I <b>measured</b> is marked measured. A number from a vendor is marked as theirs and dated '
             '(here: 14 Oct 2026). Arithmetic with an assumed model shape is labelled too.')],

 # ---- page 2
 [('h2', '2', 'The four numbers'),
  ('diagram', 'four', 62, 1000, 270),
  ('table', ['Number', 'What it tells you', 'Lesson'], [
    ['1 · memory size', 'what fits on one GPU', '<b>this one</b>'],
    ['2 · memory speed (bandwidth)', 'how fast a chat model can talk', '<b>this one</b>'],
    ['3 · compute (flops)', 'how fast it handles prompts and training', '1, 5'],
    ['4 · connection', 'how far one model can spread', '1, 5']]),
  ('def', 'Decision order: <b>fit → speed → compute → connect</b>. If it does not fit, nothing else matters.')],

 # ---- page 3
 [('h2', '3', 'Parameters and weights'),
  ('def', 'A model is a giant list of numbers. Each number is a <b>parameter</b> (a weight). A 70B model has 70,000,000,000 of them. '
          'Training finds good values. <b>Inference</b> loads them all into memory and does arithmetic with them.'),
  ('h2', '4', 'Weights in gigabytes'),
  ('def', '<b>weights = parameters × bytes per parameter</b>'),
  ('table', ['Model', 'BF16 (2 B)', 'FP8 (1 B)', 'FP4 (½ B)'], [
    ['8B', '16 GB', '8 GB', '4 GB'],
    ['70B', '<b>140 GB</b>', '<b>70 GB</b>', '35 GB'],
    ['405B', '810 GB', '405 GB', '202 GB']]),
  ('p', '<span class="small">Arithmetic, decimal gigabytes. Script: <code>l01_fit_math.py</code>.</span>')],

 # ---- page 4
 [('h2', '5', 'Precision: bytes per number'),
  ('def', 'Each number is stored at a <b>precision</b>. Think of writing a price: £2.49 or rounded to £2. Rounding takes less space and loses a little detail.'),
  ('table', ['Format', 'Bytes per number', 'Effect'], [
    ['BF16', '2', 'the common default'],
    ['FP8', '1', 'half the memory of BF16'],
    ['FP4', '½', 'a quarter of BF16, on newer chips']]),
  ('sticky', 'yellow', 'Remember', 'Halve the bytes and you halve the memory. Newer chips can also <b>do the arithmetic</b> in the smaller formats.'),
  ('h2', '6', 'GPU memory sizes'),
  ('diagram', 'fitbars', 58, 1000, 270),
  ('p', '<span class="small">GPU memory: vendor specifications as of 14 Oct 2026, not measured here. Three tiers: 80 · about 141 to 192 · 288 GB.</span>')],

 # ---- page 5
 [('h2', '7', 'Does 70B fit?'),
  ('list', 'check', ['70B in <b>FP8 = 70 GB</b>: fits an 80 GB H100, only just, with no room for anything else',
                     '70B in <b>BF16 = 140 GB</b>: does not fit an H100; borderline on an H200 (141 GB)',
                     'Fixes: two cards, a bigger card, or a smaller format']),
  ('sticky', 'pink', 'Watch out', 'Weights fitting is <b>not enough</b>. The next page shows what the weights alone leave out.')],

 # ---- page 6
 [('h2', '8', 'The KV cache: a notepad per chat'),
  ('def', 'To write a reply the model keeps notes for the conversation so far: the <b>KV cache</b> (keys and values). '
          'Every token of every open chat adds to it, and it must stay in GPU memory while the chat is open.'),
  ('diagram', 'kvper', 58, 1000, 290),
  ('def', '<b>KV bytes per token = 2 × layers × KV heads × head size × bytes per number</b>'),
  ('p', '<span class="small">Assumed 70B-class shape: 80 layers, 8 KV heads, head size 128. Typical, not any one model. '
        'Assumed 8B-class shape: 32 layers, 8 KV heads, 128.</span>')],

 # ---- page 7
 [('h2', '9', 'Notes per chat'),
  ('table', ['Config (assumed)', 'Bytes / token', '8,192-token chat', '32 chats'], [
    ['70B-class, BF16 notes', '327,680', '2.68 GB', '85.9 GB'],
    ['70B-class, FP8 notes', '163,840', '1.34 GB', '<b>42.9 GB</b>'],
    ['8B-class, BF16 notes', '131,072', '1.07 GB', '34.4 GB'],
    ['8B-class, FP8 notes', '65,536', '0.54 GB', '17.2 GB']]),
  ('p', '<span class="small">Arithmetic, <code>l01_fit_math.py</code>. A pattern, not a benchmark.</span>'),
  ('h2', '10', 'The fit rule'),
  ('def', '<b>weights + KV cache for every open chat + 20 to 40% headroom</b> (activations, graph captures, fragmentation).'),
  ('sticky', 'green', 'Remember', 'The question is never just <i>does the model fit</i>. It is <i>do the model and its chats fit</i>.')],

 # ---- page 8
 [('h2', '11', 'Worked example: 70B, 32 chats'),
  ('diagram', 'kv_stack', 60, 1000, 280),
  ('table', ['GPU', 'Memory', 'Needed 187 GB'], [
    ['H100', '80 GB', 'no (234%)'],
    ['H200', '141 GB', 'no (133%)'],
    ['B200', '192 GB', '<b>yes (97%)</b>'],
    ['B300', '288 GB', '<b>yes (65%)</b>']]),
  ('p', '<span class="small">70 GB FP8 weights + 85.9 GB BF16 notes (32 chats × 8,192 tokens) = 155.9 GB, × 1.2 headroom = 187 GB.</span>'),
  ('h3', 'Ways to shrink the notes'),
  ('list', 'arrow', ['Store notes in FP8: 85.9 GB becomes 42.9 GB (arithmetic above)',
                     'Share notes across heads (already counted: 8 KV heads)',
                     'Hand notes out in small pages so no chat wastes space <span class="small">(taught, not measured here · lesson 6)</span>'])],

 # ---- page 9
 [('h2', '12', 'Number two: memory speed'),
  ('def', 'A chef who must walk to the fridge for every dish: the <b>walk</b> sets the pace, not the hands. '
          'To make <b>one</b> new token the GPU reads <b>all</b> the weights once. The speed of that read is <b>bandwidth</b>.'),
  ('def', '<b>time per token ≥ weight bytes ÷ memory bandwidth</b> &nbsp;<span class="small">a floor, not a promise</span>'),
  ('h3', 'Measured on my CPU: one token = matrix × vector'),
  ('diagram', 'sizes', 54, 1000, 270),
  ('p', '<span class="small">One core, float32, best of 7, whole run repeated: same story. A CPU, not a GPU. Script: <code>l01_memory_bound.py</code>.</span>'),
  ('sticky', 'yellow', 'The surprise', '4x the bytes took <b>8.4x</b> the time (9.1x on the second run). The small tables sat in the chip\'s fast cache. '
             'The big one came from main memory, about half the speed. GPUs fix this with HBM next to the chip.')],

 # ---- page 10
 [('h2', '13', 'The same law on GPUs'),
  ('diagram', 'bwcalc', 58, 1000, 300),
  ('table', ['GPU', 'Bandwidth', 'Floor per token', 'Max tokens/s'], [
    ['H100', '3.4 TB/s', '20.6 ms', '49'],
    ['H200', '4.8 TB/s', '14.6 ms', '69'],
    ['B200', '8.0 TB/s', '8.8 ms', '114']]),
  ('p', '<span class="small">70B in FP8 (70 GB), one chat at a time. Arithmetic from vendor bandwidth, not measured. Next generation is quoted near 22 TB/s, limited availability.</span>'),
  ('sticky', '', 'H200 vs H100', 'Same arithmetic power, more and faster memory. For chat that alone is a better buy.')],

 # ---- page 11
 [('h2', '14', 'Number three: compute'),
  ('def', '<b>Compute</b> = how many multiplications and additions per second (flops). It matters when there is a lot of arithmetic per byte read.'),
  ('table', ['Job', 'Arithmetic per byte', 'Limited by'], [
    ['reading a long prompt', 'high', 'compute'],
    ['training', 'high', 'compute'],
    ['writing a reply, one token at a time', 'low', 'memory speed']]),
  ('h2', '15', 'Batching: serve many at once'),
  ('diagram', 'batch', 54, 1000, 270),
  ('p', '<span class="small">Measured, 4096×4096 matrix. Second run: 388, 988, 2,860, 3,967 tokens/s. 256 at once = about 24x the time per step for 256x the tokens.</span>'),
  ('sticky', 'green', 'Linked limits', 'Every chat adds notes to memory. <b>Size</b> limits how many chats. <b>Speed</b> limits how fast each step runs.')],

 # ---- page 12
 [('h2', '16', 'Number four: connection'),
  ('diagram', 'islands', 58, 1000, 300),
  ('list', 'arrow', ['Inside one server (8 GPUs on a vendor link): about 450 GB/s per GPU on H100',
                     'Between servers, over the network: about 50 GB/s per GPU, roughly <b>9x slower</b>',
                     '405B in FP8 = 405 GB of weights = 8 × H100 (640 GB) in one server']),
  ('p', '<span class="small">Vendor figures, Oct 2026. Split a model across GPUs <b>inside</b> the fast island, not across the network.</span>'),
  ('h2', '17', 'Words to keep'),
  ('table', ['Word', 'Meaning'], [
    ['Precision', 'how many bytes each number takes'],
    ['KV cache', 'the notes kept for each open chat'],
    ['Bandwidth', 'how fast memory can be read'],
    ['HBM', 'high bandwidth memory, built next to the chip']])],

 # ---- page 13
 [('h2', '18', 'ShopNest Copilot: the sum'),
  ('table', ['Item', 'Size'], [
    ['weights, 8B in FP8', '8 GB'],
    ['32 chats × 8,192 tokens, FP8 notes (assumed 8B-class shape)', '17.2 GB'],
    ['20% headroom on top', 'total ≈ <b>30 GB</b>']]),
  ('p', 'That fits a single mid-size GPU. Lesson 2 shows which one to rent and what it costs.'),
  ('h2', '19', 'Interview corner'),
  ('qa', [('How do you size a GPU for a model?',
           'Weights (parameters × bytes per parameter) plus the KV cache for every open chat plus 20 to 40% headroom.'),
          ('Why can a model fit the GPU and still fail in production?',
           'The KV cache grows with every token of every open chat. 70B in FP8 is 70 GB, but 32 chats of 8,192 tokens add 86 GB of notes (BF16).'),
          ('Why does chat speed depend on memory speed?',
           'Each new token reads all the weights once, so time per token is at least weight bytes ÷ bandwidth. Batching shares that read across users.'),
          ('When does the connection between GPUs matter?',
           'When one model must be split across GPUs. Keep the split inside one fast server, not across the network, which is about 9x slower per GPU.')])],

 # ---- page 14
 [('h2', '20', 'Your turn'),
  ('card', '<b>l01_fit_math.py</b>: change the model size, precision and number of chats and see which GPUs fit.<br><br>'
           '<b>l01_memory_bound.py</b>: run on your own computer and compare your numbers with mine.'),
  ('revise', ['4 numbers: <b>size, speed, compute, connect</b>',
              'weights = parameters × bytes (70B FP8 = <b>70 GB</b>)',
              'KV cache: <b>327,680</b> bytes per token (assumed 70B-class)',
              '32 chats × 8,192 tokens = <b>85.9 GB</b> of notes (BF16)'],
             ['time per token ≥ <b>weight bytes ÷ bandwidth</b>',
              'CPU test: 4x the bytes took <b>8.4x</b> the time',
              'batching: 1 → 256 at once = about <b>10x</b> tokens/s',
              'inside the island ~450 GB/s · across it ~50 (H100)']),
  ('next', 'CAI-02', '<b>Renting compute</b>: which chip, what it costs, spot and autoscaling')],
]
