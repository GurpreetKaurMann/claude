import sys; sys.path.insert(0, '/home/claude/caigen')
from frag import *
from gailab import CODE, OUT

LONG = [
 dict(id='s0', chap='The model fits. The chats do not.', say=[
   "I tried to plan a seventy billion parameter model on one H one hundred. The weights are seventy gigabytes. The card has eighty. It fits, with room to spare.",
   "Then I added thirty-two people chatting at once, and the memory needed jumped to one hundred and eighty-seven gigabytes. Not even close. In this lesson you will learn why, and you will be able to do this sum yourself."],
  html=[H2('The model fits. The chats do not.', 0),
        DEF('weights <b>70 GB</b> · one H100 <b>80 GB</b> · 32 chats added: <b>187 GB</b> needed', 0, 0.5, style='margin-top:24px;font-size:48px'),
        MARK('the part nobody warns you about', 1, 0.6)]),

 dict(id='s1', chap='What this course is', say=[
   "This is a twelve lesson course on the cloud side of A I engineering. We start with the chips you rent. Then containers, data, training, serving, shipping, security, and cost. The last lesson is a learning path for you.",
   "One project runs through it: ShopNest Copilot, an A I support assistant for an online store, which we move to the cloud step by step. And one rule runs through it. A number I measured is marked as measured. A number from a vendor is marked as theirs, and dated."],
  html=[H2('Twelve lessons, one project', 0),
        GRID([('chips', 0, 0.3), ('containers', 0, 0.7), ('data', 0, 1.1), ('training &amp; serving', 0, 1.5), ('shipping &amp; security', 0, 1.9), ('cost', 0, 2.3)], cols=3, h=130, fs=40),
        STICKY('The rule', '<b>measured</b> by me, or <b>from vendors</b> and dated', 1, 0.8, style='margin-top:22px;font-size:40px')]),

 dict(id='s2', chap='What the cloud is', say=[
   "First, what does the cloud mean here? It means renting someone else's computers by the hour. For A I that means renting graphics cards, called GPUs, which cost too much to buy and are hard to get.",
   "Think of a restaurant that rents a kitchen instead of building one. You pay for the time you use. The skill is knowing which equipment to rent, and that starts with understanding what a GPU actually does."],
  html=[H2('The cloud = renting computers by the hour', 0),
        ROW(COL(CARD('<b>buy</b><br>huge cost, long wait', 0, 0.4, style='font-size:42px'), width='48%'),
            COL(CARD('<b>rent</b><br>pay per hour, start now', 1, 0.3, style='font-size:42px'), width='48%'), style='margin-top:30px'),
        SUB('like a restaurant renting a kitchen', 1, 1.0, style='margin-top:20px')]),

 dict(id='s3', chap='CPU versus GPU', say=[
   "Your laptop has a C P U. It has a few strong workers, and each one is good at many different jobs.",
   "A GPU has thousands of simple workers. Each can only do basic arithmetic, but all of them do it at the same moment.",
   "Running an A I model is mostly one job, multiplying huge tables of numbers. That job splits perfectly across thousands of simple workers. That is the whole reason A I runs on GPUs."],
  html=[H2('Few strong workers, or thousands of simple ones', 0), SVG('c3', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c3', 'workers', 1000, 300, 1)]),

 dict(id='s4', chap='The four numbers', say=[
   "A GPU spec sheet is a wall of numbers, but only four of them decide almost everything. One, memory size, which tells you what fits. Two, memory speed, which tells you how fast a chat model can talk.",
   "Three, compute, which tells you how fast it can think through a big job. And four, the connection between GPUs, which tells you how far you can spread one model. We take them one at a time."],
  html=[H2('Four numbers decide almost everything', 0), SVG('c4', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c4', 'four', 1000, 270, 1)]),

 dict(id='s5', chap='Parameters and weights', say=[
   "Number one, memory size. To use it we need to know what goes into that memory first. A model is a giant list of numbers. Each number is called a parameter, or a weight. A seventy billion parameter model has seventy billion of them.",
   "Training is the process of finding good values for those numbers. Using the model, called inference, means loading all of them into memory and doing arithmetic with them. So the first question is always: how much room do the numbers take?"],
  html=[H2('A model is a giant list of numbers', 0),
        DEF('<b>parameter</b> = one number inside the model<br>70B model = <b>70,000,000,000</b> numbers', 0, 0.5, style='margin-top:24px;font-size:48px'),
        LIST([('training finds good values', 1, 0.3), ('inference loads them all into memory', 1, 0.9)], kind='ar', style='margin-top:20px;font-size:42px')]),

 dict(id='s6', chap='Weights in gigabytes', say=[
   "Here is the sum, and it is just multiplication. Memory for the weights equals the number of parameters times the bytes each number takes. In the most common format, each number takes two bytes.",
   "So an eight billion model needs sixteen gigabytes. Seventy billion needs one hundred and forty. Four hundred and five billion needs eight hundred and ten. This is arithmetic, and you can check it with a calculator."],
  html=[H2('weights = parameters × bytes each', 0),
        TABLE(['Model', 'BF16 (2 bytes)', 'FP8 (1 byte)'], [
          (['8B', '16 GB', '8 GB'], 0, 0.4),
          (['70B', '<b>140 GB</b>', '<b>70 GB</b>'], 1, 0.3),
          (['405B', '810 GB', '405 GB'], 1, 1.1)], style='margin-top:26px;font-size:44px')]),

 dict(id='s7', chap='Precision', say=[
   "Why two bytes? Because each number is stored with a certain precision. Think of writing a price. You can write two pounds, forty-nine pence, or round to two pounds. Rounding takes less space and loses a little detail.",
   "The common formats are called B F sixteen, F P eight and F P four. They use two bytes, one byte, and half a byte per number. Halving the bytes halves the memory. Newer chips can do arithmetic in the smaller formats too."],
  html=[H2('Precision: how many bytes per number', 0),
        GRID([('BF16<br>2 bytes', 1, 0.3), ('FP8<br>1 byte', 1, 0.8), ('FP4<br>½ byte', 1, 1.3)], cols=3, h=190, fs=46),
        SUB('like rounding a price: smaller, a little less detail', 0, 0.4, style='margin-top:20px')]),

 dict(id='s8', chap='Does it fit?', say=[
   "Now line the weights up against real GPU memory. These sizes come from vendor specifications, as of October twenty twenty-six. An H one hundred has eighty gigabytes. An H two hundred has one hundred and forty-one. A B two hundred has one hundred and ninety-two. A B three hundred has two hundred and eighty-eight.",
   "Seventy billion in F P eight is seventy gigabytes. It fits on an H one hundred, but only just.",
   "Seventy billion in B F sixteen is one hundred and forty. That does not fit an H one hundred at all. You would need two cards, or a bigger one."],
  html=[H2('Weights against GPU memory', 0), SVG('c8', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c8', 'fitbars', 1000, 290, 1)]),

 dict(id='s9', chap='Three memory tiers', say=[
   "A useful way to remember the chips is three memory tiers. Around eighty gigabytes is the older workhorse. Between one hundred and forty and one hundred and ninety-two is the middle tier. And two hundred and eighty-eight gigabytes is the newest tier.",
   "Across these generations, memory per card has gone from eighty to two hundred and eighty-eight gigabytes. That matters more than it sounds, because memory decides whether your model needs one card or several."],
  html=[H2('Three tiers to remember', 0),
        GRID([('<b>80 GB</b><br>H100', 0, 0.3), ('<b>141 to 192 GB</b><br>H200, B200', 0, 0.9), ('<b>288 GB</b><br>B300', 0, 1.5)], cols=3, h=200, fs=40),
        SUB('from vendor specs, Oct 2026', 1, 0.5, style='margin-top:20px')]),

 dict(id='s10', chap='The KV cache', say=[
   "But weights are only half the story, and this is the part that surprised me. When a model writes a reply, it does not re-read the whole conversation from scratch for every new word. It keeps notes.",
   "Think of a waiter with a notepad for each table. The notepad is the K V cache. Every token in every conversation adds a line to it, and the notes must stay in GPU memory while the chat is open."],
  html=[H2('The KV cache: a notepad per chat', 0),
        DEF('<b>KV cache</b> = the notes the model keeps for each open conversation', 0, 0.4, style='margin-top:24px;font-size:48px'),
        LIST([('one line added per token', 1, 0.3), ('lives in GPU memory', 1, 0.9), ('every open chat has its own', 1, 1.5)], kind='ar', style='margin-top:20px;font-size:44px')]),

 dict(id='s11', chap='How big is one token of notes?', say=[
   "How big are those notes? Here is the recipe. Two, because we keep a key and a value. Times the number of layers in the model. Times the number of K V heads.",
   "Times how many numbers each head holds. Times the bytes per number.",
   "For a seventy billion class model, and I am assuming a typical shape of eighty layers, eight heads and one hundred and twenty-eight numbers, that is three hundred and twenty-seven thousand, six hundred and eighty bytes. For every single token."],
  html=[H2('Notes per token', 0), SVG('c11', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c11', 'kvper', 1000, 290, 1)]),

 dict(id='s12', chap='Adding it up', say=[
   "Now go back to the opening. Start with the weights in F P eight. Seventy gigabytes.",
   "Now add thirty-two chats, each with eight thousand one hundred and ninety-two tokens of history. At three hundred and twenty-seven thousand bytes a token, that is eighty-six gigabytes of notes. More than the weights themselves.",
   "Add twenty percent headroom for everything else, and the total is one hundred and eighty-seven gigabytes.",
   "An H one hundred fails. An H two hundred fails. A B two hundred just fits. A B three hundred fits with room to spare."],
  html=[H2('Weights plus chats plus headroom', 0), SVG('c12', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c12', 'kv_stack', 1000, 280, 1)]),

 dict(id='s13', chap='The numbers per chat', say=[
   "Let me show the per chat numbers. One chat of eight thousand tokens costs two point six eight gigabytes of notes in the common format, or one point three four in the smaller one.",
   "Thirty-two chats cost eighty-five point nine, or forty-two point nine. Remember these are arithmetic with an assumed model shape. They are not a benchmark, but they show the pattern clearly."],
  html=[H2('Notes per chat (70B-class)', 0),
        OUT(['1 chat, 8,192 tokens:   2.68 GB (BF16)   1.34 GB (FP8)',
             '32 chats:              85.9 GB (BF16)  42.9 GB (FP8)'], 0, 0.4, size=30, label='arithmetic, assumed config', style='margin-top:24px'),
        MARK('a pattern, not a benchmark', 1, 0.6)]),

 dict(id='s14', chap='The fit rule', say=[
   "So the rule for fitting a model is three parts, not one. The weights, plus the notes for every chat you want open at once, plus headroom. Leave twenty to forty percent for the working space, the fragmentation, and the extra buffers the software needs.",
   "If you remember only one thing from this lesson, remember that the question is never just, does the model fit. It is, do the model and its conversations fit."],
  html=[H2('The fit rule', 0),
        DEF('weights <b>+</b> notes for every open chat <b>+</b> 20 to 40% headroom', 0, 0.4, style='margin-top:26px;font-size:50px'),
        STICKY('Remember', 'does the model <b>and its chats</b> fit?', 1, 0.6, style='margin-top:26px;font-size:46px')]),

 dict(id='s15', chap='Shrinking the notes', say=[
   "You can shrink the notes. Store them in the smaller one byte format and the eighty-six gigabytes becomes forty-three, which my sum showed. Modern models also share notes between attention heads, which is why I used only eight.",
   "And serving software can hand out notes in small pages, so no chat wastes space. I am teaching those last two as concepts here. They are not measured in this lesson. Lesson six goes deeper."],
  html=[H2('Ways to shrink the notes', 0),
        LIST([('smaller format: 85.9 → 42.9 GB (arithmetic)', 0, 0.4), ('share notes across heads', 0, 1.2), ('hand out in pages, waste nothing', 1, 0.4)], kind='ar', style='margin-top:24px;font-size:44px'),
        SUB('last two: taught, not measured here · more in lesson 6', 1, 1.2, style='margin-top:16px')]),

 dict(id='s16', chap='Number two: memory speed', say=[
   "Number two, memory speed. Imagine a chef who must walk to the fridge for every dish. It does not matter how fast their hands are. The walking sets the pace.",
   "Writing a chat reply works like this. For every single word, the GPU must fetch the model's weights from its memory. The speed of that walk, measured in gigabytes or terabytes per second, is called bandwidth."],
  html=[H2('Memory speed: the walk to the fridge', 0),
        ROW(COL(CARD('<b>fast hands</b><br>compute', 0, 0.4, style='font-size:42px'), width='48%'),
            COL(CARD('<b>the walk</b><br>memory bandwidth', 1, 0.3, style='font-size:42px'), width='48%'), style='margin-top:30px'),
        SUB('the walk sets the pace', 1, 1.0, style='margin-top:20px')]),

 dict(id='s17', chap='One word, all the weights', say=[
   "Here is the rule that follows. To make one new token, the GPU reads all the weights once. So the fastest it can possibly go is the weight size divided by the memory speed.",
   "That is a floor on time, not a promise. Real systems are slower. But it explains something odd: giving a chat model more arithmetic power barely helps. Giving it faster memory helps a lot."],
  html=[H2('The speed limit of a chat model', 0),
        DEF('time per token <b>≥</b> weight bytes ÷ memory speed', 0, 0.4, style='margin-top:26px;font-size:52px'),
        MARK('memory speed matters most', 1, 0.5)]),

 dict(id='s18', chap='Let me measure it', say=[
   "Let me test that on a machine I have. This is my C P U, not a GPU, so the speeds are far lower. But the law is the same. I multiply a table of numbers by one vector. That is exactly one token's worth of work.",
   "I measure the time for four table sizes. One core, plain float numbers, best of seven tries. The machine is shared, so I ran the whole thing twice, and the results agreed."],
  html=[H2('My test: one token on a CPU', 0),
        CARD('multiply a table of numbers by <b>one</b> vector<br>= the work for <b>one token</b>', 0, 0.4, style='margin-top:24px;font-size:44px'),
        SUB('one core · float32 · best of 7 · run twice · a CPU, not a GPU', 1, 0.5, style='margin-top:20px')]),

 dict(id='s19', chap='Measured: size and time', say=[
   "A four megabyte table takes point one five milliseconds. Seventeen megabytes takes point six two. Sixty-seven megabytes takes two point four three.",
   "Then two hundred and sixty-eight megabytes takes twenty point three five milliseconds.",
   "Four times the bytes took eight point four times the time. That surprised me. The small tables fit inside the chip's fast cache. The big one had to come from main memory, which was about twice as slow. That is exactly the problem GPUs solve with very fast memory right next to the chip."],
  html=[H2('Measured on my CPU', 0), SVG('c19', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c19', 'sizes', 1000, 270, 1)]),

 dict(id='s20', chap='Same law, on a GPU', say=[
   "Now use the same law on real GPUs, with the vendors' memory speeds. Seventy gigabytes of weights, read once for each token. On an H one hundred, at three point four terabytes per second, the floor is twenty point six milliseconds. About forty-nine tokens per second at most.",
   "An H two hundred, at four point eight terabytes per second, gives fourteen point six milliseconds. A B two hundred, at eight, gives eight point eight.",
   "Same weights, same arithmetic. The only change is the speed of the walk. And remember, this is arithmetic from specifications, a floor and not a benchmark."],
  html=[H2('Same law, bigger numbers', 0), SVG('c20', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c20', 'bwcalc', 1000, 300, 1)]),

 dict(id='s21', chap='The bandwidth ladder', say=[
   "Memory speed has roughly doubled every generation. About three point four terabytes per second on the H one hundred, four point eight on the H two hundred, eight on the Blackwell chips, and around twenty-two promised for the next generation, which is still in limited availability.",
   "Notice the H two hundred. It has the same arithmetic as the H one hundred, only more and faster memory. For chat, that alone makes it a better buy."],
  html=[H2('Memory speed, generation by generation', 0),
        GRID([('<b>3.4</b><br>H100', 0, 0.3), ('<b>4.8</b><br>H200', 0, 0.8), ('<b>8</b><br>B200', 0, 1.3)], cols=3, h=190, fs=44),
        SUB('TB/s · next generation: about 22, limited access · vendor figures, Oct 2026', 1, 0.5, style='margin-top:20px')]),

 dict(id='s22', chap='Number three: compute', say=[
   "Number three, compute. That is the speed of the cooks' hands, counted in flops, which is simply multiplications and additions per second. Compute matters when there is a lot of arithmetic for each byte read.",
   "Reading your long prompt is that kind of job, because all the words are processed together. Training is too. A chat reply, one word at a time, is the opposite. So the same chip can be limited by different numbers, depending on the job."],
  html=[H2('Compute: the speed of the cooks', 0),
        ROW(COL(CARD('<b>lots of arithmetic per byte</b><br>reading a long prompt, training', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>little arithmetic per byte</b><br>writing a reply, one word at a time', 1, 0.3, style='font-size:38px'), width='48%'), style='margin-top:30px'),
        SUB('same chip, different limit', 1, 1.2, style='margin-top:18px')]),

 dict(id='s23', chap='Batching', say=[
   "So how do providers make chat affordable? By serving many people at once. If the GPU is walking to the fridge anyway, it can carry orders for many tables on the same trip.",
   "I measured this. One token at a time on my C P U gave about three hundred and ninety tokens per second. Sixty-four at a time gave about three thousand.",
   "Two hundred and fifty-six at a time gave about four thousand. That is roughly ten times more tokens per second, while each step took about twenty-four times longer. Reading the weights once served everyone."],
  html=[H2('Serve many at once', 0), SVG('c23', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c23', 'batch', 1000, 310, 1)]),

 dict(id='s24', chap='What limits batching', say=[
   "Why not batch a thousand people then? Because every person needs their notepad. Each extra chat adds notes to memory, which is the thing we just calculated.",
   "Which means memory size and memory speed are linked. Memory size limits how many chats you can serve at once. Memory speed limits how fast each step runs. A good serving setup balances both."],
  html=[H2('Batching hits the memory wall', 0),
        LIST([('each chat needs its own notes', 0, 0.4), ('more chats = more memory', 0, 1.0)], kind='ar', style='margin-top:24px;font-size:46px'),
        STICKY('Linked', 'size limits <b>how many</b> chats · speed limits <b>how fast</b>', 1, 0.5, style='margin-top:24px;font-size:42px')]),

 dict(id='s25', chap='Number four: connection', say=[
   "Number four, the connection between GPUs. A server often holds eight GPUs, joined by a very fast link made by the vendor. Think of eight cooks in one kitchen, passing ingredients by hand.",
   "Another server is a second kitchen. To pass something between kitchens, you use the building's network.",
   "For an H one hundred, about four hundred and fifty gigabytes per second per GPU inside the kitchen. About fifty between kitchens. Roughly nine times slower, vendor figures. That gap shapes everything about big models."],
  html=[H2('Cooks in one kitchen, or two', 0), SVG('c25', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c25', 'islands', 1000, 300, 1)]),

 dict(id='s26', chap='When one GPU is not enough', say=[
   "When does the connection matter? When one model does not fit one card. A four hundred and five billion model in F P eight needs about four hundred and five gigabytes of weights alone. That is eight H one hundreds, which hold six hundred and forty together.",
   "The model is split across the eight cards, and they must swap results all the time. That works well inside one server and badly across the network. So the bigger the model, the more the fast connection matters."],
  html=[H2('Splitting a model across GPUs', 0),
        OUT(['405B in FP8:   405 GB of weights', '8 × H100:        640 GB in one server'], 0, 0.4, size=32, label='arithmetic + vendor spec', style='margin-top:24px'),
        STICKY('Rule', 'split inside the <b>fast island</b>, not across the network', 1, 0.6, style='margin-top:24px;font-size:42px')]),

 dict(id='s27', chap='How to choose', say=[
   "Put the four numbers into an order. First, does it fit, weights plus chats plus headroom. If not, nothing else matters.",
   "Second, memory speed, for chat. Third, compute, for training and long prompts. And fourth, the connection, if you need more than one server. Fit, speed, compute, connect."],
  html=[H2('Fit, speed, compute, connect', 0), SVG('c27', 1400, 380, 'margin:14px auto 0')],
  svgs=[('c27', 'decide', 1000, 270, 1)]),

 dict(id='s28', chap='ShopNest Copilot', say=[
   "Let us do this for our project, ShopNest Copilot. Say we choose an eight billion parameter model in the smaller format. The weights are eight gigabytes.",
   "Say we want thirty-two chats open at once, with eight thousand tokens each, using the smaller notes. That is seventeen point two gigabytes. Add the weights, add twenty percent, and the total is about thirty gigabytes. That fits one mid-size GPU. Lesson two shows which one to rent."],
  html=[H2('ShopNest Copilot: the sum', 0),
        OUT(['weights (8B, FP8):      8 GB', '32 chats, FP8 notes:   17.2 GB', 'plus 20% headroom:      ≈ 30 GB'], 1, 0.4, size=32, label='arithmetic, assumed 8B-class config', style='margin-top:24px'),
        MARK('fits one mid-size GPU', 1, 1.2)]),

 dict(id='s29', chap='Four words to keep', say=[
   "Four words to carry forward. Precision: how many bytes each number takes. K V cache: the notes kept for each open chat. Bandwidth: how fast memory can be read.",
   "And H B M, high bandwidth memory, the very fast memory built right next to the chip. You will hear all four in every lesson from here on."],
  html=[H2('Four words to keep', 0),
        GRID([('<b>precision</b>', 0, 0.3), ('<b>KV cache</b>', 0, 0.9), ('<b>bandwidth</b>', 0, 1.5), ('<b>HBM</b>', 1, 0.3)], cols=2, h=140, fs=48, style='margin-top:30px')]),

 dict(id='s30', chap='Interview corner', say=[
   "Interview corner. Asked how to size a GPU for a model, say: the weights, which is parameters times bytes per parameter, plus the notes for every open chat, plus twenty to forty percent headroom.",
   "Asked why chat speed depends on memory speed, say: each new token reads all the weights once, so the time per token is at least the weight size divided by memory bandwidth. Batching is how that read is shared across many users."],
  html=[H2('Interview corner', 0),
        Q('How do you size a GPU?', 'Weights + KV cache for every open chat + 20 to 40% headroom.', 0, 0.4),
        Q('Why is chat speed set by memory?', 'Each token reads all weights once: time ≥ bytes ÷ bandwidth.', 1, 0.4)]),

 dict(id='s31', chap='Your turn', say=[
   "Your turn. The zip for this lesson has two scripts. The first one is the fit calculator. Change the model size, the precision and the number of chats, and see which GPUs survive.",
   "The second is the memory test. Run it on your own computer and compare your numbers with mine. One changed number teaches more than an hour of reading."],
  html=[H2('Your turn', 0),
        CARD('<b>l01_fit_math.py</b>: change the model, precision and chats, see which GPUs fit.<br>'
             '<b>l01_memory_bound.py</b>: run it on your machine and compare with mine.', 0, 0.4, style='margin-top:24px;font-size:40px'),
        SUB('one changed number teaches more than an hour of reading', 1, 0.8, style='margin-top:16px')]),

 dict(id='s32', chap='Recap', say=[
   "Recap. A GPU has four numbers that matter: memory size, memory speed, compute and connection. Weights are parameters times bytes. The notes for each chat can be bigger than the weights. Seventy billion in F P eight needed one hundred and eighty-seven gigabytes for thirty-two chats.",
   "Chat speed is set by memory speed, and batching shares each read. On my C P U, two hundred and fifty-six at once gave about ten times the tokens per second. Next lesson: which chip to rent, what it costs, and how spot and autoscaling save money."],
  html=[H2('Recap', 0),
        GRID([('4 numbers matter', 0, 0.3), ('weights = params × bytes', 0, 0.9), ('chats can outweigh weights', 0, 1.5),
              ('time ≥ bytes ÷ speed', 1, 0.3), ('batching ≈ 10x tokens/s', 1, 0.9), ('fit, speed, compute, connect', 1, 1.5)], cols=3, h=150, fs=34)]),
]
