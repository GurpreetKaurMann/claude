import sys; sys.path.insert(0, '/home/claude/caigen')
from cai_lib import *
from c03_diagrams import DIAGRAMS
from c03_long import LONG
from c03_notes import NOTES

L = dict(
 code='CAI-03', num=3, num_word='three', slug='Containers_And_Kubernetes_For_AI',
 title='Containers and Kubernetes', title_html='Containers<br>&amp; Kubernetes', title_size=120,
 tagline='Package a model so it runs the same everywhere, and place it on GPUs.', module='Module 2 · Packaging and storing',
 toc=['What a container is', 'Who owns the driver', 'Layer order, measured', 'Bake or mount', 'GPUs in Kubernetes', 'Sharing a GPU', 'Gang scheduling'],
 data_label='Course project', project='ShopNest Copilot', project_desc='the AI support assistant we move to the cloud, step by step',
 prev='CAI-02', next=('CAI-04', '<b>Data and storage</b>: where information lives, how to read it fast, and how vectors work'),
 next_say='data and storage. Where information lives, how to read it fast, and how vectors work.',
 diagrams=DIAGRAMS, long=LONG, notes=NOTES,
 glow=dict(a='CONTAINERS', b='AND K8S', icons=['boxes1', '>', 'server2']),
 thumb=dict(title='Containers<br><span class="hl">&amp; K8s</span>', size=110, sub='for AI models', chips=('layer order', '401 MB vs 1 MB'), mini='mini_thumb'),

 short1=mk_short(1, 'One_Line_Changed_401_MB_Shipped', "I changed one line of code and had to ship four hundred and one megabytes. Here is why.",
   ('1 LINE', '401 MB', 150, 130),
   ["An image is a stack of layers. Change one layer and every layer above it is made again. I built real layers, with a pretend registry.",
    "With the code on top, a one line change shipped one megabyte. With the code placed before the weights, four hundred and one."],
   'mini_layers', "Rarely changing layers first. Code last.", 'Rule', 'code on the<br><b>top layer</b>', dict(title='1 line changed,<br><span class="hl">401 MB</span> shipped', size=96, sub='layer order matters', mini='mini_layers'),
   dict(title='I Changed 1 Line of Code and Shipped 401 MB (Docker Layers) #shorts',
     desc="An image is a stack of layers. Change one layer and every layer above it is rebuilt and re-shipped.\n\nReal files and real hashes, simulated registry (Docker was not running here):\n• code on the top layer: 1 MB after a one-line change\n• code before the 400 MB weights layer: 401 MB\n\nFull lesson: Cloud for AI Engineers, lesson 3.",
     tags='shorts, docker layers, docker image size, ai deployment, container best practices, cloud for ai engineers, the code notebook',
     pinned='Where do your model weights live: in the image or mounted? 👇')),

 short2=mk_short(2, 'Three_Jobs_Sixteen_GPUs_95_Percent_Deadlock', "Three jobs on sixteen GPUs froze ninety-five percent of the time. Here is the fix.",
   ('95%', 'DEADLOCK', 170, 120),
   ["Distributed training needs every worker running at once. The default scheduler places pods one at a time, so jobs grab part of what they need and wait forever.",
    "In my simulation, three jobs on sixteen GPUs deadlocked ninety-four point eight percent of the time. A gang scheduler, all or none, never did."],
   'mini_gang', "Place all of a job's pods together, or none.", 'Fix', 'gang<br><b>scheduling</b>', dict(title='95% of the time<br><span class="hl">it froze</span>', size=96, sub='3 jobs on 16 GPUs', mini='mini_gang'),
   dict(title='Why 3 AI Jobs on 16 GPUs Froze 95% of the Time #shorts',
     desc="Distributed training needs ALL workers at once.\n\nSimulation: 16 GPUs, each job = 8 pods, 10,000 random arrival orders\n• default one-by-one scheduler, 3 jobs: 94.8% deadlock\n• gang scheduler: 0%\n\nA simulation of the idea, not of the real kube-scheduler.\n\nFull lesson: Cloud for AI Engineers, lesson 3.",
     tags='shorts, gang scheduling, kubernetes gpu, distributed training, deadlock, kueue, cloud for ai engineers, the code notebook',
     pinned='Have you ever had GPUs sit idle waiting for each other? 👇')),

 reel=mk_reel('Bake_Or_Mount_Model_Weights', ["Should you bake model weights into your Docker image, or mount them?",
   "I measured it with real bytes. Weights baked in, a new model ships four hundred megabytes again. Weights mounted, zero megabytes in the app image, and a code change ships one."],
   "Big weights get their own life. Save this.", 'MOUNT IT', ['code change: 1 MB', 'new model: 0 MB in the image'], [3.2, 6.0], 'Rule', 'weights live <b>outside</b>',
   dict(title='Bake or mount<br><span class="hl">model weights?</span>', size=96, sub='measured, not guessed', mini='mini_mount'),
   dict(title='Bake or mount model weights?',
     caption="Bake model weights into the image, or mount them? 📦\n\nReal files, simulated registry:\n🔴 baked in: a new model re-ships 400 MB\n🟢 mounted: 0 MB in the app image, a code change ships 1 MB\n\nBig weights get their own life.\n\nSave this. Full lesson on YouTube: The Code Notebook.",
     pinned="Lesson 4 next: data and storage, and how vectors work 🗄️ Follow so you don't miss it!")),

 upload=dict(
   title='Why Changing One Line Re-Uploads 401 MB (Docker for AI Models)',
   hook="Lesson 3 of Cloud for AI Engineers. I changed one line of code and shipped 1 MB or 401 MB, depending only on layer order. And three jobs on 16 GPUs deadlocked 95% of the time.",
   what="We learn what a container is, who owns the GPU driver, the host driver compatibility rule, why layer order decides what you re-ship, whether to bake or mount model weights, how Kubernetes hands out GPUs, how to share one GPU (MIG, MPS, time-slicing), why distributed training needs gang scheduling, and which tool fits which job (Kueue, Ray, Kubeflow, Slurm). The layer and scheduler results are experiments with real bytes and hashes but a simulated registry and scheduler. Docker was not running on the build machine.",
   bullets=['What a container is, in meal-kit terms', 'Who owns what: host driver, image CUDA libraries, the toolkit bridge', 'The driver compatibility rule', 'CVE-2025-23266 and why you patch the host',
            'Layers: why one line can re-ship 401 MB or 1 MB', 'Bake or mount model weights (OCI image volumes)', 'Kubernetes in one picture and how pods ask for GPUs', 'Taints, labels and the GPU Operator',
            'Sharing one GPU: MIG vs MPS vs time-slicing', 'DRA in plain words', 'Gang scheduling: 94.8% deadlock without it, 0% with it', 'Kueue, JobSet, Ray, Kubeflow and Slurm: which for what',
            'ShopNest Copilot on Kubernetes', 'Interview questions with answers'],
   hashtags='#kubernetes #docker #gpu #ai #aiengineering',
   tags='docker layers explained, docker image size, kubernetes gpu, gang scheduling, kueue, bake vs mount model weights, nvidia container toolkit, mig mps time slicing, ai deployment kubernetes, cloud for ai engineers, the code notebook',
   pinned="The layer experiment uses real bytes and hashes with a simulated registry, and the gang result is a simulation, both labelled in the video. 📊\n\nQuestion for you 👇\nWhich surprised you more: 1 MB vs 401 MB for the same change, or 95% deadlock?"),
)

import interview; L['notes'] = interview.add(L['notes'], L['num'])
