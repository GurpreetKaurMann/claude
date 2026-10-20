import sys; sys.path.insert(0, '/home/claude/caigen')
from cai_lib import *
from c02_diagrams import DIAGRAMS
from c02_long import LONG
from c02_notes import NOTES

L = dict(
 code='CAI-02', num=2, num_word='two', slug='Renting_Compute_Chips_Prices_Spot',
 title='Renting Compute', title_html='Renting<br>compute', title_size=140,
 tagline='Which chip, how to pay, and how to stop the meter.', module='Module 1 · Compute',
 toc=['Four chip families', 'Reading the names', 'The buying ladder', 'The commitment trap', 'Spot and checkpoints', 'Price per petaflop', 'Scale to zero'],
 data_label='Course project', project='ShopNest Copilot', project_desc='the AI support assistant we move to the cloud, step by step',
 prev='CAI-01', next=('CAI-03', '<b>Containers and Kubernetes for AI</b>: package a model so it runs the same everywhere'),
 next_say='containers and Kubernetes. How to package a model so it runs the same everywhere.',
 diagrams=DIAGRAMS, long=LONG, notes=NOTES,
 glow=dict(a='RENTING', b='COMPUTE', icons=['chip1', '>', 'gauge2']),
 thumb=dict(title='Renting<br><span class="hl">compute</span>', size=124, sub='chips, prices and spot', chips=('spot simulation', 'save every 34 min'), mini='mini_thumb'),

 short1=mk_short(1, 'Cheap_GPUs_Can_Take_2_Million_Hours', "A hundred hour job on cheap spot GPUs can take two million hours. Here is the mistake.",
   ('100 HOURS', '2 MILLION', 140, 120),
   ["Spot machines are cheap because the provider can take them back. In my simulation, one was taken every eight hours on average, an assumption.",
    "A job that never saves its progress needs a hundred hours without a single interruption. The average finish time was over two million hours. Save every thirty-four minutes and it took a hundred and nine."],
   'mini_thumb', "Spot is only cheap if your job saves its progress.", 'Rule', 'spot needs<br><b>checkpoints</b>', dict(title='Cheap GPUs<br><span class="hl">never finish</span>', size=100, sub='one missing habit', mini='mini_thumb'),
   dict(title='Why a 100-Hour Job Can Take 2 Million Hours on Cheap GPUs #shorts',
     desc="Spot GPUs are cheap because the provider can take them back.\n\nSimulation (assumed: interrupted every 8 h on average, 100 h job):\n• never save: 2,203,564 hours\n• save every 34 min: about 109 hours\n\nThis is a simulation with assumed rates, not real machines.\n\nFull lesson: Cloud for AI Engineers, lesson 2.",
     tags='shorts, spot instances, gpu cost, checkpointing, ai training cost, cloud for ai engineers, the code notebook',
     pinned='Do you checkpoint your training runs? 👇')),

 short2=mk_short(2, 'A_55_Percent_Discount_Can_Cost_More', "A fifty-five percent discount on GPUs can cost you fifty percent more. Here is the sum.",
   ('55% OFF', 'COSTS MORE', 140, 110),
   ["A commitment means you pay for the GPU even when it is idle. So the real price is the rate divided by how busy you keep it. I assume ten dollars an hour on demand.",
    "Commit at ninety percent busy and you pay five dollars per used hour. At thirty percent busy, fifteen dollars. Break even is forty-five percent."],
   'mini_commit', "Commit only to the steady part of your load.", 'Rule', 'busy &gt; <b>45%</b><br>or don\'t commit', dict(title='55% off can<br><span class="hl">cost more</span>', size=100, sub='the commitment trap', mini='mini_commit'),
   dict(title='When a 55% GPU Discount Costs You MORE #shorts',
     desc="A commitment is a promise to pay, busy or idle.\n\nReal price = rate ÷ how busy you keep it.\nAssumed on-demand: $10/hr, commit: 55% off ($4.50)\n• 90% busy: $5.00 per used hour\n• 45% busy: $10.00\n• 30% busy: $15.00\n• 10% busy: $45.00\n\nArithmetic with assumed prices.\n\nFull lesson: Cloud for AI Engineers, lesson 2.",
     tags='shorts, gpu commitment, reserved instances, cloud cost, ai infrastructure, finops, cloud for ai engineers, the code notebook',
     pinned='What percent busy is your GPU, really? 👇')),

 reel=mk_reel('Scale_To_Zero_Cuts_GPU_Bills', ["How scale to zero cut a simulated GPU bill by eighty-three percent.",
   "One GPU, one simulated day. Always on, twenty-four GPU hours billed. Scale to zero with a five minute idle timeout, about four. The catch, a few users a day waited a full sixty seconds."],
   "Cheap on average, painful for the first user. Save this.", '24 → 4', ['always on: 24 GPU-hours', 'scale to zero: ~4 GPU-hours'], [3.2, 6.2], 'Simulation', '<b>-83%</b> GPU-hours',
   dict(title='Scale to zero<br><span class="hl">cut the bill</span>', size=100, sub='24 to 4 GPU-hours a day', mini='mini_zero'),
   dict(title='Scale to zero cut the bill 83%',
     caption="Scale to zero, simulated. 🔌\n\nOne GPU, one bursty day (assumed traffic):\n🔴 always on: 24 GPU-hours\n🟢 scale to zero: about 4 GPU-hours\n\n83% fewer hours billed.\nThe catch: about 4 cold starts a day, each user waits a full 60 s (assumed cold start).\n\nSave this. Full lesson on YouTube: The Code Notebook.",
     pinned="Lesson 3 next: containers and Kubernetes for AI 📦 Follow so you don't miss it!")),

 upload=dict(
   title='Why Cheap Spot GPUs End Up Costing MORE (The Checkpoint Mistake)',
   hook="Lesson 2 of Cloud for AI Engineers. I simulated a 100 hour job on cheap spot GPUs. With no saves it needs over two million hours. Save too often and it costs more than on-demand.",
   what="We pick a chip (NVIDIA, AMD, Google TPU, AWS Trainium), learn to read machine names, climb the buying ladder from on-demand to spot, find the commitment trap, simulate spot interruptions, work out the best save interval, compare price per petaflop and simulate scale to zero. Chip facts and prices are vendor figures dated October 2026, the sums are labelled arithmetic, and the spot and scale to zero results are simulations with assumed rates.",
   bullets=['Four chip families and what each is for', 'Which NVIDIA, AMD, TPU and Trainium chips you can really rent in October 2026', 'How to read machine names on AWS, Google Cloud and Azure',
            'Big clouds versus neoclouds', 'The buying ladder: on-demand, queued, commitment, spot', 'The commitment trap: real price = rate ÷ how busy you are',
            'Spot simulation: no saves needs 2,203,564 hours for a 100 hour job', 'The best save interval: about 34 minutes, and why 30 seconds costs more than on-demand',
            'Price per petaflop-hour for TPU and B200', 'Autoscaling with KEDA and Karpenter', 'Scale to zero: 24 to 4.04 GPU-hours a day, and the 60 second cold start',
            'ShopNest Copilot: three workloads, three rungs', 'Interview questions with answers'],
   hashtags='#cloudcomputing #gpu #ai #spotinstances #aiengineering',
   tags='spot instances explained, gpu cost, how to rent gpus, checkpointing, reserved instances vs spot, scale to zero, ai infrastructure cost, tpu vs gpu, trainium, h100 price, cloud for ai engineers, the code notebook',
   pinned="Every spot and scale to zero number here comes from a simulation with assumed rates, and every price is a vendor figure from Oct 2026. 📊\n\nQuestion for you 👇\nWhich surprised you more: a job that never finishes without saves, or saving too often costing more than on-demand?"),
)

import interview; L['notes'] = interview.add(L['notes'], L['num'])
