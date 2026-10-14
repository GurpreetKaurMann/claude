# CAI-01 · Will Your Model Fit?: Scripts

**Lesson 1 of 12 · Module 1 · Compute**

Voice: AI narrator (Kokoro `af_heart`). Final lesson video length: 16:15.

## Long video narration

**[The model fits. The chats do not.]**

> I tried to plan a seventy billion parameter model on one H one hundred. The weights are seventy gigabytes. The card has eighty. It fits, with room to spare.

> Then I added thirty-two people chatting at once, and the memory needed jumped to one hundred and eighty-seven gigabytes. Not even close. In this lesson you will learn why, and you will be able to do this sum yourself.

**[Intro]**

> Welcome to lesson one of the cloud for A I engineers course, on The Code Notebook.

> The handwritten notes and the code for this lesson are linked in the description.

**[What this course is]**

> This is a twelve lesson course on the cloud side of A I engineering. We start with the chips you rent. Then containers, data, training, serving, shipping, security, and cost. The last lesson is a learning path for you.

> One project runs through it: ShopNest Copilot, an A I support assistant for an online store, which we move to the cloud step by step. And one rule runs through it. A number I measured is marked as measured. A number from a vendor is marked as theirs, and dated.

**[What the cloud is]**

> First, what does the cloud mean here? It means renting someone else's computers by the hour. For A I that means renting graphics cards, called GPUs, which cost too much to buy and are hard to get.

> Think of a restaurant that rents a kitchen instead of building one. You pay for the time you use. The skill is knowing which equipment to rent, and that starts with understanding what a GPU actually does.

**[CPU versus GPU]**

> Your laptop has a C P U. It has a few strong workers, and each one is good at many different jobs.

> A GPU has thousands of simple workers. Each can only do basic arithmetic, but all of them do it at the same moment.

> Running an A I model is mostly one job, multiplying huge tables of numbers. That job splits perfectly across thousands of simple workers. That is the whole reason A I runs on GPUs.

**[The four numbers]**

> A GPU spec sheet is a wall of numbers, but only four of them decide almost everything. One, memory size, which tells you what fits. Two, memory speed, which tells you how fast a chat model can talk.

> Three, compute, which tells you how fast it can think through a big job. And four, the connection between GPUs, which tells you how far you can spread one model. We take them one at a time.

**[Parameters and weights]**

> Number one, memory size. To use it we need to know what goes into that memory first. A model is a giant list of numbers. Each number is called a parameter, or a weight. A seventy billion parameter model has seventy billion of them.

> Training is the process of finding good values for those numbers. Using the model, called inference, means loading all of them into memory and doing arithmetic with them. So the first question is always: how much room do the numbers take?

**[Weights in gigabytes]**

> Here is the sum, and it is just multiplication. Memory for the weights equals the number of parameters times the bytes each number takes. In the most common format, each number takes two bytes.

> So an eight billion model needs sixteen gigabytes. Seventy billion needs one hundred and forty. Four hundred and five billion needs eight hundred and ten. This is arithmetic, and you can check it with a calculator.

**[Precision]**

> Why two bytes? Because each number is stored with a certain precision. Think of writing a price. You can write two pounds, forty-nine pence, or round to two pounds. Rounding takes less space and loses a little detail.

> The common formats are called B F sixteen, F P eight and F P four. They use two bytes, one byte, and half a byte per number. Halving the bytes halves the memory. Newer chips can do arithmetic in the smaller formats too.

**[Does it fit?]**

> Now line the weights up against real GPU memory. These sizes come from vendor specifications, as of October twenty twenty-six. An H one hundred has eighty gigabytes. An H two hundred has one hundred and forty-one. A B two hundred has one hundred and ninety-two. A B three hundred has two hundred and eighty-eight.

> Seventy billion in F P eight is seventy gigabytes. It fits on an H one hundred, but only just.

> Seventy billion in B F sixteen is one hundred and forty. That does not fit an H one hundred at all. You would need two cards, or a bigger one.

**[Three memory tiers]**

> A useful way to remember the chips is three memory tiers. Around eighty gigabytes is the older workhorse. Between one hundred and forty and one hundred and ninety-two is the middle tier. And two hundred and eighty-eight gigabytes is the newest tier.

> Across these generations, memory per card has gone from eighty to two hundred and eighty-eight gigabytes. That matters more than it sounds, because memory decides whether your model needs one card or several.

**[The KV cache]**

> But weights are only half the story, and this is the part that surprised me. When a model writes a reply, it does not re-read the whole conversation from scratch for every new word. It keeps notes.

> Think of a waiter with a notepad for each table. The notepad is the K V cache. Every token in every conversation adds a line to it, and the notes must stay in GPU memory while the chat is open.

**[How big is one token of notes?]**

> How big are those notes? Here is the recipe. Two, because we keep a key and a value. Times the number of layers in the model. Times the number of K V heads.

> Times how many numbers each head holds. Times the bytes per number.

> For a seventy billion class model, and I am assuming a typical shape of eighty layers, eight heads and one hundred and twenty-eight numbers, that is three hundred and twenty-seven thousand, six hundred and eighty bytes. For every single token.

**[Adding it up]**

> Now go back to the opening. Start with the weights in F P eight. Seventy gigabytes.

> Now add thirty-two chats, each with eight thousand one hundred and ninety-two tokens of history. At three hundred and twenty-seven thousand bytes a token, that is eighty-six gigabytes of notes. More than the weights themselves.

> Add twenty percent headroom for everything else, and the total is one hundred and eighty-seven gigabytes.

> An H one hundred fails. An H two hundred fails. A B two hundred just fits. A B three hundred fits with room to spare.

**[The numbers per chat]**

> Let me show the per chat numbers. One chat of eight thousand tokens costs two point six eight gigabytes of notes in the common format, or one point three four in the smaller one.

> Thirty-two chats cost eighty-five point nine, or forty-two point nine. Remember these are arithmetic with an assumed model shape. They are not a benchmark, but they show the pattern clearly.

**[The fit rule]**

> So the rule for fitting a model is three parts, not one. The weights, plus the notes for every chat you want open at once, plus headroom. Leave twenty to forty percent for the working space, the fragmentation, and the extra buffers the software needs.

> If you remember only one thing from this lesson, remember that the question is never just, does the model fit. It is, do the model and its conversations fit.

**[Shrinking the notes]**

> You can shrink the notes. Store them in the smaller one byte format and the eighty-six gigabytes becomes forty-three, which my sum showed. Modern models also share notes between attention heads, which is why I used only eight.

> And serving software can hand out notes in small pages, so no chat wastes space. I am teaching those last two as concepts here. They are not measured in this lesson. Lesson six goes deeper.

**[Number two: memory speed]**

> Number two, memory speed. Imagine a chef who must walk to the fridge for every dish. It does not matter how fast their hands are. The walking sets the pace.

> Writing a chat reply works like this. For every single word, the GPU must fetch the model's weights from its memory. The speed of that walk, measured in gigabytes or terabytes per second, is called bandwidth.

**[One word, all the weights]**

> Here is the rule that follows. To make one new token, the GPU reads all the weights once. So the fastest it can possibly go is the weight size divided by the memory speed.

> That is a floor on time, not a promise. Real systems are slower. But it explains something odd: giving a chat model more arithmetic power barely helps. Giving it faster memory helps a lot.

**[Let me measure it]**

> Let me test that on a machine I have. This is my C P U, not a GPU, so the speeds are far lower. But the law is the same. I multiply a table of numbers by one vector. That is exactly one token's worth of work.

> I measure the time for four table sizes. One core, plain float numbers, best of seven tries. The machine is shared, so I ran the whole thing twice, and the results agreed.

**[Measured: size and time]**

> A four megabyte table takes point one five milliseconds. Seventeen megabytes takes point six two. Sixty-seven megabytes takes two point four three.

> Then two hundred and sixty-eight megabytes takes twenty point three five milliseconds.

> Four times the bytes took eight point four times the time. That surprised me. The small tables fit inside the chip's fast cache. The big one had to come from main memory, which was about twice as slow. That is exactly the problem GPUs solve with very fast memory right next to the chip.

**[Same law, on a GPU]**

> Now use the same law on real GPUs, with the vendors' memory speeds. Seventy gigabytes of weights, read once for each token. On an H one hundred, at three point four terabytes per second, the floor is twenty point six milliseconds. About forty-nine tokens per second at most.

> An H two hundred, at four point eight terabytes per second, gives fourteen point six milliseconds. A B two hundred, at eight, gives eight point eight.

> Same weights, same arithmetic. The only change is the speed of the walk. And remember, this is arithmetic from specifications, a floor and not a benchmark.

**[The bandwidth ladder]**

> Memory speed has roughly doubled every generation. About three point four terabytes per second on the H one hundred, four point eight on the H two hundred, eight on the Blackwell chips, and around twenty-two promised for the next generation, which is still in limited availability.

> Notice the H two hundred. It has the same arithmetic as the H one hundred, only more and faster memory. For chat, that alone makes it a better buy.

**[Number three: compute]**

> Number three, compute. That is the speed of the cooks' hands, counted in flops, which is simply multiplications and additions per second. Compute matters when there is a lot of arithmetic for each byte read.

> Reading your long prompt is that kind of job, because all the words are processed together. Training is too. A chat reply, one word at a time, is the opposite. So the same chip can be limited by different numbers, depending on the job.

**[Batching]**

> So how do providers make chat affordable? By serving many people at once. If the GPU is walking to the fridge anyway, it can carry orders for many tables on the same trip.

> I measured this. One token at a time on my C P U gave about three hundred and ninety tokens per second. Sixty-four at a time gave about three thousand.

> Two hundred and fifty-six at a time gave about four thousand. That is roughly ten times more tokens per second, while each step took about twenty-four times longer. Reading the weights once served everyone.

**[What limits batching]**

> Why not batch a thousand people then? Because every person needs their notepad. Each extra chat adds notes to memory, which is the thing we just calculated.

> Which means memory size and memory speed are linked. Memory size limits how many chats you can serve at once. Memory speed limits how fast each step runs. A good serving setup balances both.

**[Number four: connection]**

> Number four, the connection between GPUs. A server often holds eight GPUs, joined by a very fast link made by the vendor. Think of eight cooks in one kitchen, passing ingredients by hand.

> Another server is a second kitchen. To pass something between kitchens, you use the building's network.

> For an H one hundred, about four hundred and fifty gigabytes per second per GPU inside the kitchen. About fifty between kitchens. Roughly nine times slower, vendor figures. That gap shapes everything about big models.

**[When one GPU is not enough]**

> When does the connection matter? When one model does not fit one card. A four hundred and five billion model in F P eight needs about four hundred and five gigabytes of weights alone. That is eight H one hundreds, which hold six hundred and forty together.

> The model is split across the eight cards, and they must swap results all the time. That works well inside one server and badly across the network. So the bigger the model, the more the fast connection matters.

**[How to choose]**

> Put the four numbers into an order. First, does it fit, weights plus chats plus headroom. If not, nothing else matters.

> Second, memory speed, for chat. Third, compute, for training and long prompts. And fourth, the connection, if you need more than one server. Fit, speed, compute, connect.

**[ShopNest Copilot]**

> Let us do this for our project, ShopNest Copilot. Say we choose an eight billion parameter model in the smaller format. The weights are eight gigabytes.

> Say we want thirty-two chats open at once, with eight thousand tokens each, using the smaller notes. That is seventeen point two gigabytes. Add the weights, add twenty percent, and the total is about thirty gigabytes. That fits one mid-size GPU. Lesson two shows which one to rent.

**[Four words to keep]**

> Four words to carry forward. Precision: how many bytes each number takes. K V cache: the notes kept for each open chat. Bandwidth: how fast memory can be read.

> And H B M, high bandwidth memory, the very fast memory built right next to the chip. You will hear all four in every lesson from here on.

**[Interview corner]**

> Interview corner. Asked how to size a GPU for a model, say: the weights, which is parameters times bytes per parameter, plus the notes for every open chat, plus twenty to forty percent headroom.

> Asked why chat speed depends on memory speed, say: each new token reads all the weights once, so the time per token is at least the weight size divided by memory bandwidth. Batching is how that read is shared across many users.

**[Your turn]**

> Your turn. The zip for this lesson has two scripts. The first one is the fit calculator. Change the model size, the precision and the number of chats, and see which GPUs survive.

> The second is the memory test. Run it on your own computer and compare your numbers with mine. One changed number teaches more than an hour of reading.

**[Recap]**

> Recap. A GPU has four numbers that matter: memory size, memory speed, compute and connection. Weights are parameters times bytes. The notes for each chat can be bigger than the weights. Seventy billion in F P eight needed one hundred and eighty-seven gigabytes for thirty-two chats.

> Chat speed is set by memory speed, and batching shares each read. On my C P U, two hundred and fifty-six at once gave about ten times the tokens per second. Next lesson: which chip to rent, what it costs, and how spot and autoscaling save money.

**[Next lesson]**

> In the next lesson: renting compute. Which chip, what it really costs, and how spot machines and autoscaling save money.

> Subscribe so you don't miss it. See you in the notebook.


## Short 1: A 70B Model Fits Your GPU, Then Fails (Here's Why) #shorts

> A seventy billion parameter model fits on one H one hundred. Then it fails. Here is why.

> In the smaller format the weights are seventy gigabytes. The card has eighty. Fine.

> But every open chat keeps notes in memory. Thirty-two chats of eight thousand tokens add eighty-six gigabytes. The total needed is one hundred and eighty-seven. That is arithmetic with an assumed model shape.

> So never ask if the model fits. Ask if the model and its chats fit.


## Short 2: Why AI Chips Need Special Memory (I Measured It) #shorts

> Four times the data took eight times longer. I measured it.

> On my C P U, a sixty-seven megabyte table took two point four milliseconds to multiply by one vector. A two hundred and sixty-eight megabyte table took twenty.

> The small one fit in the chip's fast cache. The big one came from slower main memory. Chat models read all their weights for every word, so memory speed sets the pace.

> Faster memory helps more than a faster chip. That is what H B M is for.


## Instagram Reel 1: Why batching makes AI cheap

> Why serving many people at once makes A I cheap.

> I tested one token at a time on my C P U, then two hundred and fifty-six at once. One at a time, about three hundred and ninety tokens a second. Two hundred and fifty-six, about four thousand.

> About ten times the output, because reading the weights once served everyone. Save this.
