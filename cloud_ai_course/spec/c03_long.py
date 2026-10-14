import sys; sys.path.insert(0, '/home/claude/caigen')
from frag import *
from gailab import CODE, OUT

LONG = [
 dict(id='s0', chap='One line of code, 401 megabytes', say=[
   "I changed one line of code and had to ship four hundred and one megabytes again. Same change, different image layout, and only one megabyte. And when I submitted three jobs to sixteen GPUs, ninety-five percent of the time the cluster froze.",
   "Both problems are mistakes beginners make with containers and Kubernetes. Both have simple fixes. By the end of this lesson, you will know them and be able to prove them yourself."],
  html=[H2('One line changed, 401 MB shipped', 0),
        DEF('good layers: <b>1 MB</b> · bad layers: <b>401 MB</b> · 3 jobs on 16 GPUs: <b>94.8%</b> deadlock', 0, 0.5, style='margin-top:24px;font-size:46px'),
        MARK('real bytes · simulated registry and scheduler', 1, 0.6)]),

 dict(id='s1', chap='Where we are', say=[
   "In lesson two we chose chips and learned to pay for them. Now we need to run something on them. That means packing your model service into a container, and telling a cluster how to place it.",
   "This lesson has two halves. First, containers. Then Kubernetes, and the tools around it. Docker was not running on my build machine, so I label my experiments honestly: real bytes and real hashes, with a simulated registry and a simulated scheduler."],
  html=[H2('Two halves', 0),
        GRID([('containers', 0, 0.3), ('Kubernetes and friends', 0, 0.9)], cols=2, h=170, fs=46),
        STICKY('Honest label', 'real bytes, real hashes · <b>simulated</b> registry and scheduler', 1, 0.5, style='margin-top:26px;font-size:38px')]),

 dict(id='s2', chap='What a container is', say=[
   "What is a container? Think of a meal kit. The box has the recipe and every ingredient, so the dish tastes the same in any kitchen.",
   "A container holds your code, your libraries and your settings, packed together. It runs the same on your laptop, on a colleague's machine and in the cloud. The packed version is called an image, and a running copy is called a container."],
  html=[H2('A container is a meal kit', 0),
        ROW(COL(CARD('<b>image</b><br>the packed box', 0, 0.4, style='font-size:42px'), width='48%'),
            COL(CARD('<b>container</b><br>one running copy', 1, 0.3, style='font-size:42px'), width='48%'), style='margin-top:30px'),
        SUB('same box, same dish, any kitchen', 1, 1.0, style='margin-top:16px')]),

 dict(id='s3', chap='The GPU problem', say=[
   "AI adds one wrinkle. A container shares the operating system kernel of the machine it runs on. The GPU's driver is deeply tied to that kernel. So the driver cannot be packed in the box.",
   "The split is this. The host machine owns the GPU driver. Your image owns the CUDA libraries your code calls.",
   "And a piece of software called the N V I D I A Container Toolkit is the bridge. At the moment the container starts, it connects the GPU and the host's driver files into the box."],
  html=[H2('Who owns what', 0), SVG('c3', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c3', 'owners', 1000, 290, 1)]),

 dict(id='s4', chap='Inside the box', say=[
   "So what goes in your image? The CUDA runtime libraries, such as cuBLAS and N C C L. If you use PyTorch, its pip package already bundles them. The compiler, called nvcc, is only needed while building, never at runtime.",
   "That suggests a trick called a multi stage build. Build with the heavy tools in one stage. Copy only the result into a clean, small runtime image with no compiler inside."],
  html=[H2('What goes in the image', 0),
        LIST([('CUDA runtime libraries (cuBLAS, NCCL)', 0, 0.4), ('PyTorch wheels already bundle them', 0, 1.0), ('the compiler, nvcc: build time only', 0, 1.6)], kind='ar', style='margin-top:24px;font-size:42px'),
        STICKY('Trick', 'multi-stage build: heavy tools stay <b>out</b> of the final image', 1, 0.6, style='margin-top:22px;font-size:38px')]),

 dict(id='s5', chap='The compatibility rule', say=[
   "There is one rule to remember. The host driver must be new enough for the CUDA version in your image. The commonly quoted minimums are driver five twenty-five for CUDA twelve, and five eighty for CUDA thirteen.",
   "Check the official N V I D I A compatibility page for the exact numbers. If a container starts and says no CUDA device is found, the first suspect is an old driver on the host, not your code."],
  html=[H2('Host driver must be new enough', 0),
        DEF('host driver <b>≥</b> minimum for the image\'s CUDA major version', 0, 0.4, style='margin-top:24px;font-size:50px'),
        TABLE(['Image CUDA', 'Often-quoted minimum driver'], [(['12.x', 'R525 and newer'], 1, 0.3), (['13.x', 'R580 and newer'], 1, 0.9)], style='margin-top:20px;font-size:40px'),
        SUB('check NVIDIA\'s CUDA Compatibility page · not measured here', 1, 1.5, style='margin-top:12px')]),

 dict(id='s6', chap='Patch the host', say=[
   "A security note. In twenty twenty-five, a critical flaw nicknamed NVIDIAScape let a malicious image escape its container through the toolkit. It was fixed in toolkit version one point seventeen point eight.",
   "The lesson is that on a shared cluster, you run images you did not build. Rebuilding your own images does not help. You must patch the host. Keep the toolkit and the GPU operator up to date."],
  html=[H2('Patch the host, not the image', 0),
        DEF('CVE-2025-23266: container escape via the toolkit hook · fixed in toolkit <b>1.17.8</b>', 0, 0.4, style='margin-top:24px;font-size:44px'),
        STICKY('Lesson', 'shared clusters run images you did not build: <b>patch the host</b>', 1, 0.5, style='margin-top:26px;font-size:42px')]),

 dict(id='s7', chap='Layers', say=[
   "Now to the experiment. An image is a stack of layers, like bricks. A layer's identity depends on its contents and on every layer beneath it.",
   "So if you change one brick, that brick and every brick above it must be made again, and shipped again. Here is a typical AI image. Operating system, CUDA libraries, Python packages, model weights, and finally your code.",
   "Where you put the heavy weights in that stack turns out to matter a lot."],
  html=[H2('An image is a stack of layers', 0), SVG('c7', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c7', 'layers', 1000, 260, 1)]),

 dict(id='s8', chap='My layers experiment', say=[
   "I built the layers from real files. Fifty megabytes for the operating system, one hundred for CUDA, sixty for Python packages, four hundred for model weights, one for code. I hashed them for real, the way a registry identifies layers.",
   "Then I pushed the image to a pretend registry, changed one line of code, and pushed again. I counted the bytes that had to ship a second time. Docker itself was not running, so the registry is a simulation."],
  html=[H2('Real bytes, pretend registry', 0),
        OUT(['OS 50 MB · CUDA 100 MB · deps 60 MB', 'weights 400 MB · code 1 MB', 'push v1 · change ONE line of code · push v2'], 0, 0.4, size=32, label='experiment', style='margin-top:24px'),
        SUB('layer id = hash(parent id + content) · registry simulated', 1, 0.6, style='margin-top:14px')]),

 dict(id='s9', chap='Layer order, measured', say=[
   "Layout A puts the code last, on top of the weights. Changing the code ships one megabyte.",
   "Layout B puts the code before the weights, so the weights layer sits above it. One line of code now ships four hundred and one megabytes.",
   "And layout C keeps the weights out of the image altogether. Also one megabyte. Same code change, a four hundred times difference."],
  html=[H2('A one-line code change', 0), SVG('c9', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c9', 'ship_code', 1000, 270, 1)]),

 dict(id='s10', chap='The layer rules', say=[
   "So the rules follow. Put what changes rarely first, and what changes often last. Operating system, then CUDA, then Python packages, then your code.",
   "Pin your base image by its digest, not by a tag, so a rebuild next month gives the same image. Commit your lock file. Use cache mounts for package downloads so builds are fast."],
  html=[H2('Four layer rules', 0),
        LIST([('rarely changing first, code last', 0, 0.4), ('multi-stage: no compiler in the final image', 0, 1.0), ('pin base images by digest, not tag', 1, 0.4), ('commit the lock file', 1, 1.0)], kind='ar', style='margin-top:26px;font-size:44px')]),

 dict(id='s10b', chap='A Dockerfile sketch', say=[
   "Here is the whole idea as a sketch of a build file. The first stage is the heavy build stage with the compiler. Copy the lock file and install packages first. That layer stays cached until the lock file changes.",
   "Only then copy your source code. The final stage starts from a clean runtime image, copies the finished app across, and sets the start command. Verify the exact image tags before you use this, because they change."],
  html=[H2('Layers in a build file', 0),
        CODE(['FROM nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04 AS build', 'COPY pyproject.toml uv.lock ./', 'RUN uv sync --frozen --no-install-project', 'COPY src/ src/',
              'FROM nvidia/cuda:12.8.1-cudnn-runtime-ubuntu24.04', 'COPY --from=build /app /app', 'ENTRYPOINT ["python", "-m", "src.serve"]'], 0, 0.3, step=0.9, size=26, hl=False, lang='sh', style='margin-top:18px'),
        SUB('a sketch: verify image tags before use', 1, 1.0, style='margin-top:12px')]),

 dict(id='s11', chap='Bake or mount the weights?', say=[
   "Now the big question for AI. Do you bake the model weights into the image, or mount them at runtime?",
   "Baking is simple and gives you one tidy artifact. It is fine for small models, up to a gigabyte or two. For big models it is painful, because every new model version is a huge new layer and pulls become slow.",
   "Mounting keeps the app image small and lets you update the model without rebuilding anything."],
  html=[H2('Bake or mount?', 0),
        ROW(COL(CARD('<b>bake in</b><br>small models, under 1 to 2 GB<br>one tidy artifact', 1, 0.4, style='font-size:36px'), width='48%'),
            COL(CARD('<b>mount at runtime</b><br>big models<br>update without rebuilding', 2, 0.4, style='font-size:36px'), width='48%'), style='margin-top:28px')]),

 dict(id='s12', chap='When the model changes', say=[
   "I measured that too. Baked in, a new model version ships four hundred and one megabytes with layout A, and four hundred with layout B.",
   "Mounted, the app image does not change at all. The weights ship separately as their own artifact, and the app is untouched.",
   "So big weights get their own life. They change on one schedule, your code on another."],
  html=[H2('When the model changes', 0), SVG('c12', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c12', 'ship_weights', 1000, 270, 1)]),

 dict(id='s13', chap='How to mount weights', say=[
   "How do you mount a big model? Kubernetes now supports an image volume, where the weights are their own artifact in a registry, mounted read only into the pod. That became generally available in Kubernetes one point thirty-six.",
   "Other options are a fast local disk cache on the machine, a shared network drive, or object storage through a storage driver. Pin the weights by digest, just like your images."],
  html=[H2('Ways to mount weights', 0),
        LIST([('image volume: weights as their own artifact (K8s 1.36)', 0, 0.4), ('local NVMe cache on the node', 1, 0.3), ('shared network drive', 1, 0.8), ('object storage via a storage driver', 1, 1.3)], kind='ar', style='margin-top:24px;font-size:40px'),
        SUB('vendor and Kubernetes release facts, Oct 2026', 1, 1.8, style='margin-top:12px')]),

 dict(id='s14', chap='Kubernetes in one picture', say=[
   "Now Kubernetes. It is a system that runs containers across many machines. You describe what you want, and it makes it happen. A cluster is the whole group of machines. A node is one machine.",
   "A pod is one or more containers running together. The scheduler is the head chef. It looks at each order, a pod, and decides which node should cook it."],
  html=[H2('Kubernetes in one picture', 0), SVG('c14', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c14', 'k8s', 1000, 290, 1)]),

 dict(id='s15', chap='GPUs in Kubernetes', say=[
   "How does Kubernetes know about GPUs? A small helper program on each GPU node, called a device plugin, announces them. The announcement is a resource called N V I D I A dot com slash gpu.",
   "A pod asks for whole numbers. One GPU, two GPUs, never half. And for GPUs, the request and the limit must be equal. That is the classic, safest way to give a pod a whole GPU."],
  html=[H2('Asking for a GPU', 0),
        OUT(['resources:', '  limits:', '    nvidia.com/gpu: 1'], 0, 0.4, size=36, label='the pod asks', style='margin-top:24px'),
        LIST([('whole numbers only, no halves', 1, 0.3), ('request = limit', 1, 0.9)], kind='ar', style='margin-top:20px;font-size:42px')]),

 dict(id='s16', chap='Keeping GPUs for GPU jobs', say=[
   "GPU machines are expensive, so keep ordinary pods off them. Put a taint on the GPU nodes. A taint is a do not enter sign, and only pods that carry the matching toleration may land there.",
   "Also use labels. A tool called GPU Feature Discovery labels each node with its GPU model and memory, so a pod can ask for an H one hundred specifically."],
  html=[H2('Taints keep the wrong pods away', 0),
        ROW(COL(CARD('<b>taint on GPU nodes</b><br>a do-not-enter sign', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>labels</b><br>GPU model and memory', 1, 0.3, style='font-size:38px'), width='48%'), style='margin-top:28px'),
        SUB('a pod with no GPU request on a GPU node can still see every GPU', 1, 1.0, style='margin-top:14px')]),

 dict(id='s17', chap='The GPU Operator', say=[
   "Setting up each node by hand is tedious. NVIDIA's GPU Operator installs the whole node stack as one package. The driver, the container toolkit, the device plugin, the labelling tool, and monitoring.",
   "The version names follow year and month. The latest in October twenty twenty-six is twenty-six point seven point one. If your cloud image already ships drivers, you turn off the operator's driver install."],
  html=[H2('The GPU Operator: one package', 0),
        LIST([('driver + container toolkit', 0, 0.4), ('device plugin + feature discovery', 0, 0.9), ('monitoring (DCGM exporter)', 0, 1.4), ('latest: 26.7.1 (23 Sep 2026)', 1, 0.4)], kind='ar', style='margin-top:24px;font-size:42px')]),

 dict(id='s18', chap='Sharing one GPU', say=[
   "A whole GPU is wasteful for a small model. There are three ways to share one. MIG cuts a GPU into walled rooms, each with its own memory and compute.",
   "MPS gives clients desks in the same room. They get a share of memory, but no walls.",
   "Time slicing just takes turns on one chair. No memory isolation and no fair share. Only walls stop a crash in the next room."],
  html=[H2('Sharing one GPU', 0), SVG('c18', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c18', 'sharing', 1000, 290, 1)]),

 dict(id='s19', chap='Which sharing to use', say=[
   "So which to pick? MIG for several teams or customers sharing hardware, because it isolates them. It works only on certain chips, in fixed sizes.",
   "MPS for small, cooperating inference jobs. Time slicing mostly for notebooks and development. If one tenant must never hurt another, only the walls will do."],
  html=[H2('Which sharing for what', 0),
        TABLE(['Method', 'Use for'], [(['MIG', 'several tenants, real isolation'], 0, 0.4), (['MPS', 'small cooperative inference'], 1, 0.3), (['time-slicing', 'notebooks and dev only'], 1, 0.9)], style='margin-top:26px;font-size:42px')]),

 dict(id='s19b', chap='Sharing, in numbers', say=[
   "Two numbers make the sharing options concrete. With time slicing, a machine with eight GPUs set to ten replicas advertises eighty GPUs to Kubernetes, but they are still eight physical chips taking turns.",
   "With MPS, each client gets the memory divided by the number of clients. Eighty gigabytes shared by four clients is twenty gigabytes each. Sharing is a trade, not free capacity."],
  html=[H2('Sharing, in numbers', 0),
        OUT(['time-slicing: 8 GPUs × 10 replicas = 80 advertised', '(still 8 physical chips, taking turns)'], 0, 0.4, size=32, label='from the notebook', style='margin-top:22px'),
        OUT(['MPS: 80 GB ÷ 4 clients = 20 GB each'], 1, 0.3, size=34, label='from the notebook', style='margin-top:18px')]),

 dict(id='s20', chap='The future: DRA', say=[
   "There is a newer way to ask for devices, called dynamic resource allocation. Instead of counting opaque integers, a pod makes a claim, a bit like a storage claim, and a driver offers matching devices. It has been generally available since Kubernetes one point thirty-four.",
   "In practice, production use today is mostly for the multi node link on the biggest racks. For ordinary whole GPU training pods, the device plugin is still the safe choice. I mention DRA so the word is not new to you."],
  html=[H2('DRA: a claim for devices', 0),
        DEF('like a storage claim, but for <b>devices</b> · GA since Kubernetes 1.34', 0, 0.4, style='margin-top:24px;font-size:46px'),
        MARK('whole-GPU training today: the device plugin is still safe', 1, 0.6)]),

 dict(id='s21', chap='Why gang scheduling', say=[
   "Now the second horror story. Distributed training needs all of its workers running, or nobody makes progress. But the default scheduler places pods one at a time.",
   "So job A grabs three of its four machines. Job B grabs the fourth. Both sit idle, holding expensive GPUs, waiting for pods that can never be placed. This is a partial placement deadlock. The fix is gang scheduling: place all of a job's pods, or none."],
  html=[H2('Partial placement deadlock', 0),
        ROW(COL(CARD('<b>job A</b><br>holds 3 of 4 GPUs', 0, 0.4, style='font-size:42px'), width='48%'),
            COL(CARD('<b>job B</b><br>holds the other GPU', 0, 0.9, style='font-size:42px'), width='48%'), style='margin-top:28px'),
        STICKY('The fix', 'gang scheduling: <b>all or none</b>', 1, 0.6, style='margin-top:26px;font-size:46px')]),

 dict(id='s22', chap='My gang experiment', say=[
   "I simulated it. A cluster of sixteen GPUs. Each job needs eight pods, one GPU each, all at once. I shuffled the order the pods arrive, ten thousand times.",
   "The default scheduler places pods one by one. The gang scheduler places a job only when all eight GPUs are free. I counted how often the cluster ended up deadlocked. This is a simulation of the idea, not of a real Kubernetes scheduler."],
  html=[H2('The gang simulation', 0),
        OUT(['16 GPUs · each job = 8 pods × 1 GPU', '10,000 random arrival orders', 'deadlock = full, nothing complete, nothing moves'], 0, 0.4, size=32, label='simulation setup', style='margin-top:24px'),
        SUB('a simulation of the idea, not of real kube-scheduler', 1, 0.6, style='margin-top:14px')]),

 dict(id='s23', chap='Deadlock, measured', say=[
   "Two jobs fit, so no deadlock at all. Submit three jobs, and the default scheduler deadlocked ninety-four point eight percent of the time.",
   "Four jobs, always. Six jobs, always.",
   "The gang scheduler never deadlocked once. Jobs wait their turn, and every job that starts finishes."],
  html=[H2('Deadlocked, out of 10,000', 0), SVG('c23', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c23', 'gang', 1000, 320, 1)]),

 dict(id='s24', chap='Queues and gangs in practice', say=[
   "In real clusters you use a queue tool. Kueue decides when a job may start, and enforces quotas between teams. The scheduler still decides where each pod goes.",
   "For the job itself you use helpers like JobSet or Ray. Other schedulers such as Volcano or KAI also do gang placement.",
   "Kubernetes is adding native gang scheduling too, but in version one point thirty-seven it is still beta and off by default. Do not build production on alpha features, because the APIs change."],
  html=[H2('Queue first, place second', 0), SVG('c24', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c24', 'tools', 1000, 290, 1)]),

 dict(id='s25', chap='Ray, Kubeflow, Slurm', say=[
   "Which orchestrator for which job? Ray suits Python teams with mixed pipelines. Data prep, training, reinforcement learning and serving, all in one Python program.",
   "Kubeflow Trainer runs training jobs on Kubernetes the standard way. And KServe has grown into a serving layer for large models."],
  html=[H2('Which tool for which job', 0),
        TABLE(['Tool', 'Good for'], [(['Ray', 'Python-native mixed pipelines'], 0, 0.4), (['Kubeflow Trainer', 'training jobs on Kubernetes'], 1, 0.3), (['KServe', 'serving large models'], 1, 0.9)], style='margin-top:26px;font-size:42px')]),

 dict(id='s26', chap='Slurm', say=[
   "And there is an older tool that big labs still love, called Slurm. It is a batch scheduler built for supercomputers. Huge pretraining runs often use it, and in late twenty twenty-five NVIDIA bought the company behind it.",
   "You do not have to pick one world. Hybrids run Slurm on top of Kubernetes. If you are fine tuning or serving, you will probably never need Slurm. If you join a pretraining team, you will."],
  html=[H2('Slurm: the supercomputer scheduler', 0),
        LIST([('big pretraining runs still love it', 0, 0.4), ('hybrids run Slurm on Kubernetes', 0, 1.0), ('fine-tuning and serving: you probably skip it', 1, 0.4)], kind='ar', style='margin-top:26px;font-size:44px')]),

 dict(id='s27', chap='Failures are normal', say=[
   "At large scale, machines fail. Plan for it. Run health checks on the GPUs, so a sick machine is removed before it spoils a job. Restart the whole gang together when one worker dies.",
   "And save checkpoints, exactly like our spot lesson. Containers and Kubernetes make restarts easy, but only checkpoints make them cheap."],
  html=[H2('Plan for failure', 0),
        LIST([('health-check the GPUs', 0, 0.4), ('restart the whole gang together', 0, 1.0), ('checkpoints make restarts cheap', 1, 0.4)], kind='ar', style='margin-top:26px;font-size:46px')]),

 dict(id='s28', chap='A small gotcha', say=[
   "One small gotcha that costs people hours. The data loading workers in PyTorch use shared memory. The default is tiny. Give the pod a bigger shared memory volume, sixteen gigabytes is a common choice, or training will crash with a confusing error.",
   "It is a good example of what AI containers need. The defaults are made for web apps, not for training."],
  html=[H2('Give the data loader room', 0),
        OUT(['volumes:', '- name: dshm', '  emptyDir: {medium: Memory, sizeLimit: 16Gi}'], 0, 0.4, size=32, label='shared memory for DataLoader', style='margin-top:24px'),
        MARK('defaults are made for web apps, not training', 1, 0.5)]),

 dict(id='s29', chap='ShopNest Copilot', say=[
   "For ShopNest Copilot, the plan is simple. One small image with the serving code, built in two stages, code on the top layer. The model weights mounted as their own artifact, pinned by digest.",
   "The pod asks for one whole GPU, tolerates the GPU taint, and runs behind a queue. The nightly evaluation job becomes a gang job on the spot machines from lesson two."],
  html=[H2('ShopNest Copilot on Kubernetes', 0),
        TABLE(['Piece', 'Plan'], [(['image', 'two stages, code on the top layer'], 0, 0.4), (['weights', 'mounted, pinned by digest'], 0, 1.0), (['pod', '1 GPU, GPU taint toleration'], 1, 0.3), (['nightly eval', 'gang job on spot'], 1, 0.9)], style='margin-top:22px;font-size:40px')]),

 dict(id='s30', chap='Four words to keep', say=[
   "Four words to carry forward. Layer: one brick of an image. Mount: attach files at runtime instead of packing them.",
   "Taint: a sign that keeps the wrong pods off a machine. And gang scheduling: place all of a job's pods together, or none."],
  html=[H2('Four words to keep', 0),
        GRID([('<b>layer</b>', 0, 0.3), ('<b>mount</b>', 0, 0.9), ('<b>taint</b>', 1, 0.3), ('<b>gang scheduling</b>', 1, 0.9)], cols=2, h=140, fs=46, style='margin-top:30px')]),

 dict(id='s31', chap='Interview corner', say=[
   "Interview corner. Asked how to speed up image builds and pushes, say: put rarely changing layers first and code last, use multi stage builds, and keep big model weights out of the image. In my experiment that turned a four hundred and one megabyte re push into one.",
   "Asked why distributed training jobs need gang scheduling, say: they need all workers at once, so placing pods one by one can deadlock. In my simulation, three jobs on sixteen GPUs deadlocked ninety-five percent of the time."],
  html=[H2('Interview corner', 0),
        Q('How do you speed up image pushes?', 'Rare layers first, code last, multi-stage, weights out of the image: 401 MB became 1 MB.', 0, 0.4),
        Q('Why gang scheduling?', 'Jobs need all workers at once. One by one can deadlock: 94.8% in my simulation.', 1, 0.4)]),

 dict(id='s32', chap='Your turn', say=[
   "Your turn. The zip for this lesson has three scripts. The first measures layer shipping. Change the layer sizes and order, and see what a code change costs.",
   "The second simulates gang scheduling. Change the cluster size and the job size. The third checks driver and CUDA compatibility. One changed number teaches more than an hour of reading."],
  html=[H2('Your turn', 0),
        CARD('<b>l03_layers.py</b>: change layer sizes and order.<br><b>l03_gang.py</b>: change cluster and job size.<br><b>l03_compat.py</b>: check a driver against a CUDA version.', 0, 0.4, style='margin-top:22px;font-size:38px'),
        SUB('one changed number teaches more than an hour of reading', 1, 0.8, style='margin-top:16px')]),

 dict(id='s33', chap='Recap', say=[
   "Recap. The host owns the driver, the image owns the CUDA libraries, and the toolkit connects them. Layer order decides what you re ship, and big weights belong outside the image. Layout B shipped four hundred and one megabytes for one line.",
   "Kubernetes hands out whole GPUs, taints protect them, and gang scheduling stops deadlock. Next lesson: data and storage. Where information lives, how to read it fast, and how vectors work."],
  html=[H2('Recap', 0),
        GRID([('host: driver · image: CUDA libs', 0, 0.3), ('layer order: 401 MB vs 1 MB', 0, 0.9), ('weights stay outside', 0, 1.5),
              ('whole GPUs + taints', 1, 0.3), ('gang: 94.8% → 0%', 1, 0.9), ('queue first, place second', 1, 1.5)], cols=3, h=150, fs=32)]),
]
