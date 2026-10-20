# CAI-03 · Containers and Kubernetes: Scripts

**Lesson 3 of 12 · Module 2 · Packaging and storing**

Voice: AI narrator (Kokoro `af_heart`). Final lesson video length: 16:20.

## Long video narration

**[One line of code, 401 megabytes]**

> I changed one line of code and had to ship four hundred and one megabytes again. Same change, different image layout, and only one megabyte. And when I submitted three jobs to sixteen GPUs, ninety-five percent of the time the cluster froze.

> Both problems are mistakes beginners make with containers and Kubernetes. Both have simple fixes. By the end of this lesson, you will know them and be able to prove them yourself.

**[Intro]**

> Welcome to lesson three of the cloud for A I engineers course, on The Code Notebook.

> The handwritten notes and the code for this lesson are linked in the description.

**[Where we are]**

> In lesson two we chose chips and learned to pay for them. Now we need to run something on them. That means packing your model service into a container, and telling a cluster how to place it.

> This lesson has two halves. First, containers. Then Kubernetes, and the tools around it. Docker was not running on my build machine, so I label my experiments honestly: real bytes and real hashes, with a simulated registry and a simulated scheduler.

**[What a container is]**

> What is a container? Think of a meal kit. The box has the recipe and every ingredient, so the dish tastes the same in any kitchen.

> A container holds your code, your libraries and your settings, packed together. It runs the same on your laptop, on a colleague's machine and in the cloud. The packed version is called an image, and a running copy is called a container.

**[The GPU problem]**

> AI adds one wrinkle. A container shares the operating system kernel of the machine it runs on. The GPU's driver is deeply tied to that kernel. So the driver cannot be packed in the box.

> The split is this. The host machine owns the GPU driver. Your image owns the CUDA libraries your code calls.

> And a piece of software called the N V I D I A Container Toolkit is the bridge. At the moment the container starts, it connects the GPU and the host's driver files into the box.

**[Inside the box]**

> So what goes in your image? The CUDA runtime libraries, such as cuBLAS and N C C L. If you use PyTorch, its pip package already bundles them. The compiler, called nvcc, is only needed while building, never at runtime.

> That suggests a trick called a multi stage build. Build with the heavy tools in one stage. Copy only the result into a clean, small runtime image with no compiler inside.

**[The compatibility rule]**

> There is one rule to remember. The host driver must be new enough for the CUDA version in your image. The commonly quoted minimums are driver five twenty-five for CUDA twelve, and five eighty for CUDA thirteen.

> Check the official N V I D I A compatibility page for the exact numbers. If a container starts and says no CUDA device is found, the first suspect is an old driver on the host, not your code.

**[Patch the host]**

> A security note. In twenty twenty-five, a critical flaw nicknamed NVIDIAScape let a malicious image escape its container through the toolkit. It was fixed in toolkit version one point seventeen point eight.

> The lesson is that on a shared cluster, you run images you did not build. Rebuilding your own images does not help. You must patch the host. Keep the toolkit and the GPU operator up to date.

**[Layers]**

> Now to the experiment. An image is a stack of layers, like bricks. A layer's identity depends on its contents and on every layer beneath it.

> So if you change one brick, that brick and every brick above it must be made again, and shipped again. Here is a typical AI image. Operating system, CUDA libraries, Python packages, model weights, and finally your code.

> Where you put the heavy weights in that stack turns out to matter a lot.

**[My layers experiment]**

> I built the layers from real files. Fifty megabytes for the operating system, one hundred for CUDA, sixty for Python packages, four hundred for model weights, one for code. I hashed them for real, the way a registry identifies layers.

> Then I pushed the image to a pretend registry, changed one line of code, and pushed again. I counted the bytes that had to ship a second time. Docker itself was not running, so the registry is a simulation.

**[Layer order, measured]**

> Layout A puts the code last, on top of the weights. Changing the code ships one megabyte.

> Layout B puts the code before the weights, so the weights layer sits above it. One line of code now ships four hundred and one megabytes.

> And layout C keeps the weights out of the image altogether. Also one megabyte. Same code change, a four hundred times difference.

**[The layer rules]**

> So the rules follow. Put what changes rarely first, and what changes often last. Operating system, then CUDA, then Python packages, then your code.

> Pin your base image by its digest, not by a tag, so a rebuild next month gives the same image. Commit your lock file. Use cache mounts for package downloads so builds are fast.

**[A Dockerfile sketch]**

> Here is the whole idea as a sketch of a build file. The first stage is the heavy build stage with the compiler. Copy the lock file and install packages first. That layer stays cached until the lock file changes.

> Only then copy your source code. The final stage starts from a clean runtime image, copies the finished app across, and sets the start command. Verify the exact image tags before you use this, because they change.

**[Bake or mount the weights?]**

> Now the big question for AI. Do you bake the model weights into the image, or mount them at runtime?

> Baking is simple and gives you one tidy artifact. It is fine for small models, up to a gigabyte or two. For big models it is painful, because every new model version is a huge new layer and pulls become slow.

> Mounting keeps the app image small and lets you update the model without rebuilding anything.

**[When the model changes]**

> I measured that too. Baked in, a new model version ships four hundred and one megabytes with layout A, and four hundred with layout B.

> Mounted, the app image does not change at all. The weights ship separately as their own artifact, and the app is untouched.

> So big weights get their own life. They change on one schedule, your code on another.

**[How to mount weights]**

> How do you mount a big model? Kubernetes now supports an image volume, where the weights are their own artifact in a registry, mounted read only into the pod. That became generally available in Kubernetes one point thirty-six.

> Other options are a fast local disk cache on the machine, a shared network drive, or object storage through a storage driver. Pin the weights by digest, just like your images.

**[Kubernetes in one picture]**

> Now Kubernetes. It is a system that runs containers across many machines. You describe what you want, and it makes it happen. A cluster is the whole group of machines. A node is one machine.

> A pod is one or more containers running together. The scheduler is the head chef. It looks at each order, a pod, and decides which node should cook it.

**[GPUs in Kubernetes]**

> How does Kubernetes know about GPUs? A small helper program on each GPU node, called a device plugin, announces them. The announcement is a resource called N V I D I A dot com slash gpu.

> A pod asks for whole numbers. One GPU, two GPUs, never half. And for GPUs, the request and the limit must be equal. That is the classic, safest way to give a pod a whole GPU.

**[Keeping GPUs for GPU jobs]**

> GPU machines are expensive, so keep ordinary pods off them. Put a taint on the GPU nodes. A taint is a do not enter sign, and only pods that carry the matching toleration may land there.

> Also use labels. A tool called GPU Feature Discovery labels each node with its GPU model and memory, so a pod can ask for an H one hundred specifically.

**[The GPU Operator]**

> Setting up each node by hand is tedious. NVIDIA's GPU Operator installs the whole node stack as one package. The driver, the container toolkit, the device plugin, the labelling tool, and monitoring.

> The version names follow year and month. The latest in October twenty twenty-six is twenty-six point seven point one. If your cloud image already ships drivers, you turn off the operator's driver install.

**[Sharing one GPU]**

> A whole GPU is wasteful for a small model. There are three ways to share one. MIG cuts a GPU into walled rooms, each with its own memory and compute.

> MPS gives clients desks in the same room. They get a share of memory, but no walls.

> Time slicing just takes turns on one chair. No memory isolation and no fair share. Only walls stop a crash in the next room.

**[Which sharing to use]**

> So which to pick? MIG for several teams or customers sharing hardware, because it isolates them. It works only on certain chips, in fixed sizes.

> MPS for small, cooperating inference jobs. Time slicing mostly for notebooks and development. If one tenant must never hurt another, only the walls will do.

**[Sharing, in numbers]**

> Two numbers make the sharing options concrete. With time slicing, a machine with eight GPUs set to ten replicas advertises eighty GPUs to Kubernetes, but they are still eight physical chips taking turns.

> With MPS, each client gets the memory divided by the number of clients. Eighty gigabytes shared by four clients is twenty gigabytes each. Sharing is a trade, not free capacity.

**[The future: DRA]**

> There is a newer way to ask for devices, called dynamic resource allocation. Instead of counting opaque integers, a pod makes a claim, a bit like a storage claim, and a driver offers matching devices. It has been generally available since Kubernetes one point thirty-four.

> In practice, production use today is mostly for the multi node link on the biggest racks. For ordinary whole GPU training pods, the device plugin is still the safe choice. I mention DRA so the word is not new to you.

**[Why gang scheduling]**

> Now the second horror story. Distributed training needs all of its workers running, or nobody makes progress. But the default scheduler places pods one at a time.

> So job A grabs three of its four machines. Job B grabs the fourth. Both sit idle, holding expensive GPUs, waiting for pods that can never be placed. This is a partial placement deadlock. The fix is gang scheduling: place all of a job's pods, or none.

**[My gang experiment]**

> I simulated it. A cluster of sixteen GPUs. Each job needs eight pods, one GPU each, all at once. I shuffled the order the pods arrive, ten thousand times.

> The default scheduler places pods one by one. The gang scheduler places a job only when all eight GPUs are free. I counted how often the cluster ended up deadlocked. This is a simulation of the idea, not of a real Kubernetes scheduler.

**[Deadlock, measured]**

> Two jobs fit, so no deadlock at all. Submit three jobs, and the default scheduler deadlocked ninety-four point eight percent of the time.

> Four jobs, always. Six jobs, always.

> The gang scheduler never deadlocked once. Jobs wait their turn, and every job that starts finishes.

**[Queues and gangs in practice]**

> In real clusters you use a queue tool. Kueue decides when a job may start, and enforces quotas between teams. The scheduler still decides where each pod goes.

> For the job itself you use helpers like JobSet or Ray. Other schedulers such as Volcano or KAI also do gang placement.

> Kubernetes is adding native gang scheduling too, but in version one point thirty-seven it is still beta and off by default. Do not build production on alpha features, because the APIs change.

**[Ray, Kubeflow, Slurm]**

> Which orchestrator for which job? Ray suits Python teams with mixed pipelines. Data prep, training, reinforcement learning and serving, all in one Python program.

> Kubeflow Trainer runs training jobs on Kubernetes the standard way. And KServe has grown into a serving layer for large models.

**[Slurm]**

> And there is an older tool that big labs still love, called Slurm. It is a batch scheduler built for supercomputers. Huge pretraining runs often use it, and in late twenty twenty-five NVIDIA bought the company behind it.

> You do not have to pick one world. Hybrids run Slurm on top of Kubernetes. If you are fine tuning or serving, you will probably never need Slurm. If you join a pretraining team, you will.

**[Failures are normal]**

> At large scale, machines fail. Plan for it. Run health checks on the GPUs, so a sick machine is removed before it spoils a job. Restart the whole gang together when one worker dies.

> And save checkpoints, exactly like our spot lesson. Containers and Kubernetes make restarts easy, but only checkpoints make them cheap.

**[A small gotcha]**

> One small gotcha that costs people hours. The data loading workers in PyTorch use shared memory. The default is tiny. Give the pod a bigger shared memory volume, sixteen gigabytes is a common choice, or training will crash with a confusing error.

> It is a good example of what AI containers need. The defaults are made for web apps, not for training.

**[ShopNest Copilot]**

> For ShopNest Copilot, the plan is simple. One small image with the serving code, built in two stages, code on the top layer. The model weights mounted as their own artifact, pinned by digest.

> The pod asks for one whole GPU, tolerates the GPU taint, and runs behind a queue. The nightly evaluation job becomes a gang job on the spot machines from lesson two.

**[Four words to keep]**

> Four words to carry forward. Layer: one brick of an image. Mount: attach files at runtime instead of packing them.

> Taint: a sign that keeps the wrong pods off a machine. And gang scheduling: place all of a job's pods together, or none.

**[Interview corner]**

> Interview corner. Asked how to speed up image builds and pushes, say: put rarely changing layers first and code last, use multi stage builds, and keep big model weights out of the image. In my experiment that turned a four hundred and one megabyte re push into one.

> Asked why distributed training jobs need gang scheduling, say: they need all workers at once, so placing pods one by one can deadlock. In my simulation, three jobs on sixteen GPUs deadlocked ninety-five percent of the time.

**[Your turn]**

> Your turn. The zip for this lesson has three scripts. The first measures layer shipping. Change the layer sizes and order, and see what a code change costs.

> The second simulates gang scheduling. Change the cluster size and the job size. The third checks driver and CUDA compatibility. One changed number teaches more than an hour of reading.

**[Recap]**

> Recap. The host owns the driver, the image owns the CUDA libraries, and the toolkit connects them. Layer order decides what you re ship, and big weights belong outside the image. Layout B shipped four hundred and one megabytes for one line.

> Kubernetes hands out whole GPUs, taints protect them, and gang scheduling stops deadlock. Next lesson: data and storage. Where information lives, how to read it fast, and how vectors work.

**[Next lesson]**

> In the next lesson: data and storage. Where information lives, how to read it fast, and how vectors work.

> Subscribe so you don't miss it. See you in the notebook.


## Short 1: I Changed 1 Line of Code and Shipped 401 MB (Docker Layers) #shorts

> I changed one line of code and had to ship four hundred and one megabytes. Here is why.

> An image is a stack of layers. Change one layer and every layer above it is made again. I built real layers, with a pretend registry.

> With the code on top, a one line change shipped one megabyte. With the code placed before the weights, four hundred and one.

> Rarely changing layers first. Code last.


## Short 2: Why 3 AI Jobs on 16 GPUs Froze 95% of the Time #shorts

> Three jobs on sixteen GPUs froze ninety-five percent of the time. Here is the fix.

> Distributed training needs every worker running at once. The default scheduler places pods one at a time, so jobs grab part of what they need and wait forever.

> In my simulation, three jobs on sixteen GPUs deadlocked ninety-four point eight percent of the time. A gang scheduler, all or none, never did.

> Place all of a job's pods together, or none.


## Instagram Reel 1: Bake or mount model weights?

> Should you bake model weights into your Docker image, or mount them?

> I measured it with real bytes. Weights baked in, a new model ships four hundred megabytes again. Weights mounted, zero megabytes in the app image, and a code change ships one.

> Big weights get their own life. Save this.
