import sys; sys.path.insert(0, '/home/claude/caigen')
from cai_lib import *
from c05_diagrams import DIAGRAMS
from c05_long import LONG
from c05_notes import NOTES

L = dict(
 code='CAI-05', num=5, num_word='five', slug='Training_At_Scale',
 title='Training at Scale', title_html='Training<br>at scale', title_size=140,
 tagline='Where the memory goes, and how to split a model across GPUs.', module='Module 3 · Training and serving',
 toc=['The 16-byte ledger', 'Sharding', 'Recompute', 'GPU-hours', 'Splitting a model', 'The bubble', 'LoRA'],
 data_label='Course project', project='ShopNest Copilot', project_desc='the AI support assistant we move to the cloud, step by step',
 prev='CAI-04', next=('CAI-06', '<b>Inference and serving</b>: how to make a trained model answer fast'),
 next_say='inference and serving. How to make a trained model answer fast.',
 diagrams=DIAGRAMS, long=LONG, notes=NOTES,
 glow=dict(a='TRAINING', b='AT SCALE', icons=['nn1', '>', 'chip2']),
 thumb=dict(title='Training<br><span class="hl">at scale</span>', size=124, sub='the 16-byte rule', chips=('140 GB', '1,120 GB'), mini='mini_thumb'),

 short1=mk_short(1, 'Training_A_70B_Model_Needs_1120_GB', "A seventy billion parameter model is a hundred and forty gigabytes. Training it needs eleven hundred and twenty.",
   ('140 GB', '1,120 GB', 170, 150),
   ["Training keeps four things in memory. Weights, gradients, and the optimiser, which stores a full precision copy plus two running averages. In the usual recipe that is two plus two plus twelve, sixteen bytes per parameter.",
    "I measured it on a real small model and got sixteen point zero. Sixteen times seventy billion is eleven hundred and twenty gigabytes."],
   'mini_ledger', "Weights are only an eighth of the training bill.", 'Rule', '<b>16 bytes</b><br>per parameter', dict(title='140 GB model.<br><span class="hl">1,120 GB</span> to train', size=92, sub='the 16-byte rule', mini='mini_ledger'),
   dict(title='Why Training a 70B Model Needs 1,120 GB (Not 140) #shorts',
     desc="Training memory per parameter (mixed precision with Adam): 2 (weights) + 2 (gradients) + 12 (fp32 master + Adam m + Adam v) = 16 bytes.\n\nMeasured on a real 33.6M-parameter model: 16.0 bytes per parameter.\n70B x 16 = 1,120 GB (arithmetic).\n\nFull lesson: Cloud for AI Engineers, lesson 5.",
     tags='shorts, training memory, how much gpu memory to train, adam optimizer memory, zero fsdp, llm training, cloud for ai engineers, the code notebook',
     pinned='Did you know weights are only 1/8 of the training memory? 👇')),

 short2=mk_short(2, 'LoRA_Trains_1_Percent', "Fine tuning a model by training less than one percent of it. I measured the memory it saves.",
   ('TRAIN 1%', '100X LESS', 140, 130),
   ["LoRA freezes the whole model and trains two small matrices beside each layer. On my small model, rank eight trained point nine seven percent of the parameters.",
    "The optimiser memory fell from two hundred and sixty-nine megabytes to two point six. About a hundred times less. That is why fine tuning fits on one card."],
   'mini_lora', "Most teams should fine tune with LoRA, not pretrain.", 'Rule', 'train a<br><b>sliver</b>', dict(title='Train 1%.<br><span class="hl">Save 100x</span>', size=100, sub='LoRA, measured', mini='mini_lora'),
   dict(title='LoRA Trains Under 1% of a Model: 100x Less Memory #shorts',
     desc="MEASURED on a small 33.6M-parameter model (PyTorch, CPU):\n• full training: Adam state 268.6 MB\n• LoRA rank 8: trains 0.97% of parameters, Adam state 2.6 MB\n• LoRA rank 16: 1.91%, 5.2 MB\n\nFull lesson: Cloud for AI Engineers, lesson 5.",
     tags='shorts, lora explained, fine tuning memory, qlora, parameter efficient fine tuning, llm fine tuning, cloud for ai engineers, the code notebook',
     pinned='Have you fine-tuned with LoRA yet? 👇')),

 reel=mk_reel('The_Pipeline_Bubble', ["Why forty-three percent of your GPUs can sit idle in a pipeline.",
   "I simulated a four stage pipeline with four micro batches. Six of every fourteen slots were idle, forty-two point nine percent. With eight stages and a hundred and twenty-eight micro batches, five percent."],
   "Keep the pipeline full. Save this.", '43% IDLE', ['4 stages, 4 batches: 43% idle', '8 stages, 128 batches: 5% idle'], [3.2, 6.2], 'Rule', 'more micro-batches,<br><b>less bubble</b>',
   dict(title='43% of GPUs<br><span class="hl">sit idle</span>', size=104, sub='the pipeline bubble', mini='mini_bubble'),
   dict(title='Why 43% of your GPUs sit idle in a pipeline',
     caption="The pipeline bubble, simulated. 🫧\n\nBubble = (p-1) / (m+p-1)\n🔴 4 stages, 4 micro-batches: 42.9% idle\n🟠 8 stages, 32 micro-batches: 17.9%\n🟢 8 stages, 128 micro-batches: 5.2%\n\nKeep the pipeline full.\n\nSave this. Full lesson on YouTube: The Code Notebook.",
     pinned="Lesson 6 next: inference and serving, how to make a trained model answer fast ⚡ Follow so you don't miss it!")),

 upload=dict(
   title='Why Training a 70B Model Needs 1,120 GB (The 16-Byte Rule)',
   hook="Lesson 5 of Cloud for AI Engineers. A 70B model is 140 GB of weights, but training it needs 1,120 GB. This lesson explains the 16-byte rule, how to share the memory across GPUs, and what training really costs.",
   what="We build the training memory ledger (weights, gradients, optimiser state, activations), measure it on a real small model, see how ZeRO and FSDP shard it, measure what recomputation saves, count GPU-hours with the 6ND rule, compare the four ways to split a model, simulate the pipeline bubble, price the network, and measure why LoRA needs 100 times less optimiser memory. Measured on a CPU with a small model; large-model numbers are arithmetic and simulation, labelled on screen.",
   bullets=['What training is: guess, blame, nudge', 'The 16-byte ledger: 2 + 2 + 12', 'Measured: 16.0 bytes per parameter on a real model', 'ZeRO and FSDP: 1,120 GB to 17.5 GB per GPU', 'Activations and recomputation: measured 0.54x memory for about 1.2x time',
            'The 6ND rule: 7B on 2T tokens is about 59,000 GPU-hours', 'MFU, honestly', 'Data, tensor, pipeline and expert parallel', 'The pipeline bubble: 42.9% idle, simulated', 'Mapping splits to the hardware',
            'NCCL and the silent 2 to 5x slowdown', 'Failures: one every 3.1 hours', 'LoRA: 0.97% trained, 100x less optimiser memory, measured', 'ShopNest Copilot: fine-tune, do not pretrain', 'Interview questions with answers'],
   hashtags='#machinelearning #llm #gpu #ai #aiengineering',
   tags='how much gpu memory to train llm, 16 bytes per parameter, adam optimizer memory, zero fsdp explained, gradient checkpointing, lora memory, pipeline parallelism bubble, tensor parallelism, 6nd flops, training cost, cloud for ai engineers, the code notebook',
   pinned="The ledger and LoRA numbers were measured on a small real model on a CPU. Big-model numbers are arithmetic from the notebook's formulas, and the bubble is a simulation. 📊\n\nQuestion for you 👇\nWhich surprised you more: weights being only 1/8 of the training bill, or LoRA needing 100x less optimiser memory?"),
)
