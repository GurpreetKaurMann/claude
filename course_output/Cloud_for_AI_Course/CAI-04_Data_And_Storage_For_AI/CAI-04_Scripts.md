# CAI-04 · Data and Storage: Scripts

**Lesson 4 of 12 · Module 2 · Packaging and storing**

Voice: AI narrator (Kokoro `af_heart`). Final lesson video length: 16:16.

## Long video narration

**[80 megabytes, 25 times slower]**

> I read the same eighty megabytes two ways. As one file, it took five hundredths of a second. As twenty thousand small files, it took one point three seconds. Twenty-five times slower, on a plain local disk.

> On a cloud object store, where every request has a delay, the same mistake would be hundreds of times worse. This lesson is about where AI data lives, how to read it fast, and how vectors are stored and searched.

**[Intro]**

> Welcome to lesson four of the cloud for A I engineers course, on The Code Notebook.

> The handwritten notes and the code for this lesson are linked in the description.

**[Where we are]**

> So far we have rented chips and packed containers. But a GPU with nothing to read is just an expensive heater. Lesson four is about feeding it. Where does data live, how do you read it fast, how do you save a checkpoint, and how do vectors work?

> I mix measurements and models here. The file reads and the vector tests are real measurements on my machine, with synthetic vectors. The cloud object store timing is a model with assumed numbers, and I say so on screen.

**[Object storage]**

> Start with the main place AI data lives, object storage. Services like S three, Google Cloud Storage and Azure Blob. Think of a giant filing cabinet where every file has a name, and you can store almost unlimited amounts, very cheaply, with great durability.

> The catch is how you reach in. You ask for a whole file by name. You do not edit the middle of it. That one fact shapes everything else in this lesson.

**[Region is truth, zone is speed]**

> Cloud storage comes in tiers. The standard tier is regional. Your data is copied across several buildings, so it survives a fire. That is the truth, the copy you must never lose.

> Fast tiers, such as S three Express or Google's Rapid buckets, live in a single zone, right next to your GPUs. They are much quicker, but one building only.

> And archive tiers are cheap for data you almost never read. The rule is region equals truth, zone equals speed. Never keep your only copy in the fast tier.

**[What lives where]**

> So what goes where? Datasets, shards, final checkpoints and model weights belong in the regional standard tier. That is about two point three cents per gigabyte per month at the S three list price.

> Hot shards, scratch space and the most recent checkpoints can sit in the fast zonal tier, as long as a regional copy exists. Old checkpoints and raw data you rarely touch go to cooler or archive tiers.

**[Egress is the real bill]**

> Here is the surprise on cloud bills. Storing data is cheap. Moving it out is not. That charge is called egress. At list prices, the big clouds charge around nine to twelve cents per gigabyte to send data to the internet.

> Moving data between regions or between zones also costs. So before you chase cheap GPUs in another cloud, budget the cost of moving your data there. One neocloud, Cloudflare R two, charges nothing for egress, which is why people use it to serve data to many clouds.

**[An egress sum]**

> Let us do the sum. One hundred terabytes is one hundred thousand gigabytes. At the nine cent list price that is nine thousand dollars. Volume tiers bring it down somewhat, but the order of magnitude is thousands of dollars.

> That is why you should design so data stays near the compute. It is cheaper to move the job to the data than the data to the job. This is arithmetic from list prices, not a quote.

**[Small files]**

> Now back to my opening mistake. Object stores are brilliant at big sequential reads and terrible at many tiny ones. Every request has a fixed delay before any data arrives. Fetch ten thousand tiny files and you pay that delay ten thousand times.

> This is the number one beginner mistake with training data. Millions of small image or text files, read one by one. The cure is called sharding.

**[My file experiment]**

> The experiment is simple. I made eighty megabytes of random data three ways. Twenty thousand files of four kilobytes. Eighty files of one megabyte. And a single eighty megabyte file, which I call a shard.

> I dropped the operating system's file cache before every read, so I measured the disk and not memory. Best of three tries. This part is a real measurement on my machine's local disk.

**[Measured: small files]**

> Twenty thousand small files took one point three four seconds, about sixty megabytes per second. Eighty one megabyte files took point oh eight. The single shard took point oh five, about fifteen hundred megabytes per second.

> That is twenty-five times slower for the tiny files, reading exactly the same data. And this is a fast local disk. Cloud storage has far more delay per request.

**[The object store model]**

> Now a model of a cloud object store. I assume twenty milliseconds per request, and a hundred megabytes per second per stream. Those are my assumptions, and real services vary.

> Twenty thousand small files would take four hundred seconds. Eighty files, two point four seconds. One shard, point eight. The delay, not the data, dominates.

**[Shards]**

> So pack your samples into shards. A shard is a big file, from about a hundred megabytes to a gigabyte, holding many samples one after another. Each training worker holds one shard at a time, plus a small shuffle buffer.

> Two popular formats. WebDataset uses plain tar files, one sample being a few files with the same name. Mosaic's streaming format reads shards from any cloud, can resume in the middle of an epoch, and gives the same sample order whatever number of GPUs you use.

**[Text is rarely the bottleneck]**

> A reassuring fact. Plain text training is rarely limited by storage. Fifteen trillion tokens, stored as two byte ids, is about thirty terabytes, read roughly once per pass. That is manageable.

> Storage gets stressed by pictures and video, by small random reads you cannot re shard, and by checkpoint bursts. Profile first, and only buy fast storage when the GPUs are really waiting.

**[Fast file systems]**

> When you do need speed, the standard answer is a parallel file system, usually Lustre, offered as a managed service on every big cloud. Neoclouds use products like WEKA and VAST. They look like an ordinary disk to your code.

> There is a pricing trick. You buy bandwidth by buying capacity. Small data and a hungry job means paying for empty terabytes. The pattern is: the bucket is the master, the fast file system is a temporary copy for this job, torn down after the run.

**[Checkpoint size]**

> Checkpoints are the other big storage event. A full training checkpoint stores more than the weights. In the common setup it is fourteen bytes per parameter. Two for the weights, four for a full precision copy, and four each for the optimiser's two memories.

> So a seventy billion parameter model has a checkpoint close to one terabyte. A four hundred and five billion model, about five point seven. That is arithmetic from the notebook's formula.

**[The stall]**

> If training waits for the write, the GPUs idle. A terabyte written at ten gigabytes per second is about a hundred seconds. At a hundred gigabytes per second, ten. These speeds are my assumptions.

> The big models are worse. The fix is asynchronous saving. Copy the state to memory or local disk, let training continue, and drain it to the bucket in the background.

**[The lakehouse]**

> Now structured data, like tables of customers, tickets and logs. The modern pattern is called a lakehouse. Files in a columnar format called Parquet, sitting in object storage.

> On top, a table format such as Delta or Iceberg adds transactions and snapshots. On top of that, a catalog holds names, permissions and lineage. Any query engine can read it. Engines come and go, the tables stay.

**[Versioning data]**

> If you cannot reproduce last month's training data, you cannot reproduce last month's model. Version your data at three levels. Files, with tools like DVC or Hugging Face. Whole lakes, with branches, using lakeFS. And tables, using snapshots.

> Pin every training run to a version. In the table world, that means a snapshot number you can query later.

**[The retention trap]**

> A trap with Delta tables. Time travel needs the old files. By default, the clean up job deletes files older than seven days. So last month's training snapshot is already gone.

> Set the retention to at least as long as you want to look back, ninety days is common. This is a documented default, not something I measured.

**[Reproducibility and quality]**

> A reproducible training run records four things. The data snapshot, the code commit, the tokenizer and preprocessing version, and the embedding model version. Put them in your model registry.

> And before data is written into training sets or search indexes, check it. Schema, nulls, duplicates, personal data, and overlap with your evaluation set. Bad data costs more the later you find it.

**[What a vector is]**

> Now vectors. An embedding model turns text, or an image, into a list of numbers, called a vector. Similar meanings land close together. To search, you embed the question and find the nearest vectors.

> The simplest search compares the question to every stored vector. That is exact, but it slows down as the collection grows. Real systems use an approximate method, trading a little accuracy for a lot of speed.

**[How big are vectors?]**

> How much memory do vectors need? Bytes per vector equals the dimensions times the bytes per number. A model with seven hundred and sixty-eight dimensions in the standard format uses three thousand and seventy-two bytes per vector.

> Fifty thousand of them is about a hundred and fifty-four megabytes. Ten million is over thirty gigabytes. Memory is the main cost of vector search, so compression matters.

**[My compression experiment]**

> I tested compression. Fifty thousand synthetic vectors of seven hundred and sixty-eight numbers each. They are random clusters, not real embeddings, so treat the results as a pattern. Exact search on the full copy is the truth.

> Then I stored them as half size numbers, as one byte numbers, and as single bits. And I measured recall at ten, meaning how many of the true top ten each version still found.

**[Compression, measured]**

> Half size numbers, float sixteen, found every true neighbour. Recall one point zero, at half the memory. One byte numbers found ninety-eight and a half percent at a quarter of the memory.

> Single bits shrank it thirty-two times, but on their own found only twenty-one percent. After rescoring the best hundred candidates with the full numbers, recall came back to seventy-four percent.

> So bits are a first filter, not an answer. The notebook warns they work worse under about four hundred dimensions, and better as dimensions grow.

**[Finding neighbours fast]**

> Now the speed side. The most popular approximate method is HNSW. It builds a layered graph. Imagine a map with motorways at the top, main roads in the middle, and every street at the bottom.

> A search starts at the top, hops to whichever node is closest to your question, and drops a layer when it gets stuck.

> Finally it looks around its neighbours on the bottom layer. It never visits most of the data.

**[HNSW knobs and memory]**

> Two knobs matter. M is how many links, or friends, each node keeps. More friends means more memory. And ef is how hard you look, when building and when searching. Looking harder is slower but finds more.

> Memory is about N times four dimensions plus eight M bytes. For my test that formula said a hundred and sixty megabytes, and the real index file was a hundred and sixty-one. Close enough to plan with.

**[HNSW, measured]**

> Here is recall against effort. At effort ten, recall was fifty-six percent. At fifty, ninety-six, in point two milliseconds per query. At a hundred, ninety-nine point eight percent.

> Exact search took one point two one milliseconds for the same questions. So at ninety-six percent recall, the graph was about six times faster, and the gap grows as the collection grows.

**[Other index families]**

> HNSW lives in memory. For bigger collections, other designs exist. IVF with compression clusters the data and squeezes each vector. DiskANN keeps the graph on fast disks. And object tiered systems keep vectors in cheap storage, with search taking around a hundred milliseconds.

> No family wins everywhere. Memory is fast and costly. Disk and object storage are slower and cheap. You choose by how many vectors you have and how quickly users need an answer.

**[Choosing a vector store]**

> Which product should you pick? Start with what you already run. If you have Postgres, the pgvector extension handles millions of vectors, and it stores half size numbers, which my test showed lose nothing. Object backed stores such as S three Vectors suit huge, cheap, slower collections.

> Dedicated databases suit heavy, low latency workloads. And all of them work better with keyword search added, which is a topic for lesson eight.

**[ShopNest Copilot]**

> For ShopNest Copilot. Raw tickets and evaluation sets live in regional object storage, packed in shards. The nightly evaluation job reads shards, not thousands of tiny files. Checkpoints are saved asynchronously.

> The support articles, a few hundred thousand chunks, go in pgvector as half size vectors with an HNSW index. And we record the embedding model version, so we can rebuild the index at any time.

**[Four words to keep]**

> Four words to carry forward. Shard: a big file packed with many samples. Egress: the charge for data leaving a cloud.

> Recall: the share of true nearest neighbours a search returns. And quantisation: storing numbers with fewer bits to save memory.

**[Interview corner]**

> Interview corner. Asked why not store training data as millions of small files, say: every object store request has a fixed delay, so small reads are dominated by delay. Pack samples into shards of a hundred megabytes to a gigabyte. In my test, small files read twenty-five times slower.

> Asked how to cut vector memory, say: store half size or one byte numbers. In my test, one byte numbers kept recall at ninety-eight and a half percent at a quarter of the memory, but plain bits dropped to twenty-one.

**[Your turn]**

> Your turn. The zip for this lesson has three scripts. The first compares reading small files and shards on your own disk. The second compares vector formats and the graph index. The third is the checkpoint and egress arithmetic.

> Change the vector dimensions, or the number of files, and see what moves. One changed number teaches more than an hour of reading.

**[Recap]**

> Recap. Region is truth, zone is speed, and egress is the real bill. Small files are slow, so pack shards. Twenty thousand files read twenty-five times slower than one. A checkpoint is fourteen bytes per parameter. Version your data, and mind the seven day default.

> Half size or one byte vectors keep nearly all recall at a half or a quarter of the memory. A graph index found ninety-six percent of true neighbours, six times faster than exact search. Next lesson: training at scale. Where the memory goes, and how to split a model.

**[Next lesson]**

> In the next lesson: training at scale. Where the memory goes, and how to split a model across GPUs.

> Subscribe so you don't miss it. See you in the notebook.


## Short 1: Why 20,000 Small Files Read 25x Slower Than One #shorts

> The same eighty megabytes took twenty-five times longer to read. The only difference was the file size.

> I made eighty megabytes three ways and read each one, after clearing the file cache. Twenty thousand tiny files took one point three four seconds. One single shard took five hundredths of a second.

> That was a fast local disk. A cloud object store adds a delay per request, so the gap grows. Pack your samples into shards.

> Big files, not many small files.


## Short 2: Shrink Your Vector Database 4x and Keep 98% Recall #shorts

> You can shrink your vector database four times and still find ninety-eight percent of the right answers.

> I made fifty thousand synthetic vectors of seven hundred and sixty-eight numbers each. Stored as full floats they took one hundred and fifty-four megabytes. As one byte numbers, thirty-eight.

> Recall at ten, the share of true neighbours found, was point nine eight five. Half size numbers found all of them. These are synthetic vectors, so treat it as a pattern.

> Try float16 or int8 before buying more memory.


## Instagram Reel 1: Moving 100 TB out of the cloud costs $9,000

> Why moving data out of the cloud costs nine thousand dollars.

> Storing data is cheap, but egress, the charge for data leaving, is about nine cents per gigabyte at list price. One hundred terabytes is a hundred thousand gigabytes, so nine thousand dollars.

> Move the job to the data, not the data to the job. Save this.
