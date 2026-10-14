import sys; sys.path.insert(0, '/home/claude/caigen')
from frag import *
from gailab import CODE, OUT

LONG = [
 dict(id='s0', chap='80 megabytes, 25 times slower', say=[
   "I read the same eighty megabytes two ways. As one file, it took five hundredths of a second. As twenty thousand small files, it took one point three seconds. Twenty-five times slower, on a plain local disk.",
   "On a cloud object store, where every request has a delay, the same mistake would be hundreds of times worse. This lesson is about where AI data lives, how to read it fast, and how vectors are stored and searched."],
  html=[H2('Same 80 MB, 25 times slower', 0),
        DEF('one shard: <b>0.05 s</b> · 20,000 small files: <b>1.34 s</b> (measured)', 0, 0.5, style='margin-top:24px;font-size:48px'),
        MARK('on a cloud object store it is far worse (model, assumed delay)', 1, 0.6)]),

 dict(id='s1', chap='Where we are', say=[
   "So far we have rented chips and packed containers. But a GPU with nothing to read is just an expensive heater. Lesson four is about feeding it. Where does data live, how do you read it fast, how do you save a checkpoint, and how do vectors work?",
   "I mix measurements and models here. The file reads and the vector tests are real measurements on my machine, with synthetic vectors. The cloud object store timing is a model with assumed numbers, and I say so on screen."],
  html=[H2('Feeding the GPUs', 0),
        GRID([('where data lives', 0, 0.3), ('read it fast', 0, 0.7), ('save checkpoints', 0, 1.1), ('vectors', 0, 1.5)], cols=4, h=150, fs=34),
        STICKY('Honest label', 'file reads and vector tests: <b>measured</b> · cloud timing: <b>model</b>', 1, 0.5, style='margin-top:26px;font-size:38px')]),

 dict(id='s2', chap='Object storage', say=[
   "Start with the main place AI data lives, object storage. Services like S three, Google Cloud Storage and Azure Blob. Think of a giant filing cabinet where every file has a name, and you can store almost unlimited amounts, very cheaply, with great durability.",
   "The catch is how you reach in. You ask for a whole file by name. You do not edit the middle of it. That one fact shapes everything else in this lesson."],
  html=[H2('Object storage: a giant filing cabinet', 0),
        LIST([('every file has a name', 0, 0.4), ('almost unlimited, cheap, very durable', 0, 1.0), ('you fetch whole files, not edit the middle', 1, 0.4)], kind='ar', style='margin-top:26px;font-size:46px'),
        SUB('S3 · Google Cloud Storage · Azure Blob', 1, 1.0, style='margin-top:14px')]),

 dict(id='s3', chap='Region is truth, zone is speed', say=[
   "Cloud storage comes in tiers. The standard tier is regional. Your data is copied across several buildings, so it survives a fire. That is the truth, the copy you must never lose.",
   "Fast tiers, such as S three Express or Google's Rapid buckets, live in a single zone, right next to your GPUs. They are much quicker, but one building only.",
   "And archive tiers are cheap for data you almost never read. The rule is region equals truth, zone equals speed. Never keep your only copy in the fast tier."],
  html=[H2('Three kinds of tier', 0), SVG('c3', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c3', 'tiers', 1000, 290, 1)]),

 dict(id='s4', chap='What lives where', say=[
   "So what goes where? Datasets, shards, final checkpoints and model weights belong in the regional standard tier. That is about two point three cents per gigabyte per month at the S three list price.",
   "Hot shards, scratch space and the most recent checkpoints can sit in the fast zonal tier, as long as a regional copy exists. Old checkpoints and raw data you rarely touch go to cooler or archive tiers."],
  html=[H2('What goes in which tier', 0),
        TABLE(['Tier', 'Put here'], [(['regional standard', 'datasets, final checkpoints, weights'], 0, 0.4), (['one-zone fast', 'hot shards, scratch, recent checkpoints'], 0, 1.0), (['cool / archive', 'old checkpoints, raw crawls'], 1, 0.4)], style='margin-top:24px;font-size:40px'),
        SUB('S3 Standard list price: about $0.023 per GB-month (notebook, Oct 2026)', 1, 1.0, style='margin-top:14px')]),

 dict(id='s5', chap='Egress is the real bill', say=[
   "Here is the surprise on cloud bills. Storing data is cheap. Moving it out is not. That charge is called egress. At list prices, the big clouds charge around nine to twelve cents per gigabyte to send data to the internet.",
   "Moving data between regions or between zones also costs. So before you chase cheap GPUs in another cloud, budget the cost of moving your data there. One neocloud, Cloudflare R two, charges nothing for egress, which is why people use it to serve data to many clouds."],
  html=[H2('Storing is cheap. Moving is not.', 0),
        DEF('<b>egress</b> = the charge for data leaving a cloud', 0, 0.4, style='margin-top:24px;font-size:48px'),
        LIST([('big clouds: roughly $0.09 to $0.12 per GB (list)', 0, 1.0), ('cross-zone and cross-region also cost', 1, 0.3), ('budget it before chasing cheap GPUs elsewhere', 1, 0.9)], kind='ar', style='margin-top:20px;font-size:40px')]),

 dict(id='s6', chap='An egress sum', say=[
   "Let us do the sum. One hundred terabytes is one hundred thousand gigabytes. At the nine cent list price that is nine thousand dollars. Volume tiers bring it down somewhat, but the order of magnitude is thousands of dollars.",
   "That is why you should design so data stays near the compute. It is cheaper to move the job to the data than the data to the job. This is arithmetic from list prices, not a quote."],
  html=[H2('The egress sum', 0),
        OUT(['  1 TB out =   1,000 GB × $0.09 = $90', ' 10 TB out =  10,000 GB × $0.09 = $900', '100 TB out = 100,000 GB × $0.09 = $9,000'], 0, 0.4, size=32, label='arithmetic, list price', style='margin-top:24px'),
        MARK('move the job to the data, not the data to the job', 1, 0.6)]),

 dict(id='s7', chap='Small files', say=[
   "Now back to my opening mistake. Object stores are brilliant at big sequential reads and terrible at many tiny ones. Every request has a fixed delay before any data arrives. Fetch ten thousand tiny files and you pay that delay ten thousand times.",
   "This is the number one beginner mistake with training data. Millions of small image or text files, read one by one. The cure is called sharding."],
  html=[H2('Many tiny reads: the beginner mistake', 0),
        ROW(COL(CARD('<b>big sequential reads</b><br>object stores love them', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>many tiny reads</b><br>pay the delay every time', 0, 0.9, style='font-size:38px'), width='48%'), style='margin-top:28px'),
        STICKY('The cure', '<b>sharding</b>', 1, 0.6, style='margin-top:26px;font-size:50px')]),

 dict(id='s8', chap='My file experiment', say=[
   "The experiment is simple. I made eighty megabytes of random data three ways. Twenty thousand files of four kilobytes. Eighty files of one megabyte. And a single eighty megabyte file, which I call a shard.",
   "I dropped the operating system's file cache before every read, so I measured the disk and not memory. Best of three tries. This part is a real measurement on my machine's local disk."],
  html=[H2('The file experiment', 0),
        OUT(['20,000 files × 4 KB', '80 files × 1 MB', '1 file × 80 MB   (a shard)', 'same 80 MB, cache dropped, best of 3'], 0, 0.4, size=32, label='measured setup', style='margin-top:22px'),
        SUB('real local disk · not a cloud service', 1, 0.6, style='margin-top:14px')]),

 dict(id='s9', chap='Measured: small files', say=[
   "Twenty thousand small files took one point three four seconds, about sixty megabytes per second. Eighty one megabyte files took point oh eight. The single shard took point oh five, about fifteen hundred megabytes per second.",
   "That is twenty-five times slower for the tiny files, reading exactly the same data. And this is a fast local disk. Cloud storage has far more delay per request."],
  html=[H2('Reading 80 MB from local disk', 0), SVG('c9', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c9', 'files', 1000, 260, 1)]),

 dict(id='s10', chap='The object store model', say=[
   "Now a model of a cloud object store. I assume twenty milliseconds per request, and a hundred megabytes per second per stream. Those are my assumptions, and real services vary.",
   "Twenty thousand small files would take four hundred seconds. Eighty files, two point four seconds. One shard, point eight. The delay, not the data, dominates."],
  html=[H2('A model of an object store', 0), SVG('c10', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c10', 'objmodel', 1000, 260, 1)]),

 dict(id='s11', chap='Shards', say=[
   "So pack your samples into shards. A shard is a big file, from about a hundred megabytes to a gigabyte, holding many samples one after another. Each training worker holds one shard at a time, plus a small shuffle buffer.",
   "Two popular formats. WebDataset uses plain tar files, one sample being a few files with the same name. Mosaic's streaming format reads shards from any cloud, can resume in the middle of an epoch, and gives the same sample order whatever number of GPUs you use."],
  html=[H2('Pack samples into shards', 0),
        DEF('a shard = <b>100 MB to 1 GB</b> of samples, read in order', 0, 0.4, style='margin-top:24px;font-size:48px'),
        LIST([('WebDataset: plain tar files', 1, 0.3), ('Mosaic streaming: resumable, same order on any GPU count', 1, 0.9)], kind='ar', style='margin-top:20px;font-size:42px')]),

 dict(id='s12', chap='Text is rarely the bottleneck', say=[
   "A reassuring fact. Plain text training is rarely limited by storage. Fifteen trillion tokens, stored as two byte ids, is about thirty terabytes, read roughly once per pass. That is manageable.",
   "Storage gets stressed by pictures and video, by small random reads you cannot re shard, and by checkpoint bursts. Profile first, and only buy fast storage when the GPUs are really waiting."],
  html=[H2('When storage actually hurts', 0),
        OUT(['15T tokens × 2 bytes = 30 TB, read about once per pass'], 0, 0.4, size=34, label='arithmetic', style='margin-top:24px'),
        LIST([('pictures and video', 1, 0.3), ('small random reads you cannot re-shard', 1, 0.8), ('checkpoint bursts', 1, 1.3)], kind='ar', style='margin-top:18px;font-size:40px')]),

 dict(id='s13', chap='Fast file systems', say=[
   "When you do need speed, the standard answer is a parallel file system, usually Lustre, offered as a managed service on every big cloud. Neoclouds use products like WEKA and VAST. They look like an ordinary disk to your code.",
   "There is a pricing trick. You buy bandwidth by buying capacity. Small data and a hungry job means paying for empty terabytes. The pattern is: the bucket is the master, the fast file system is a temporary copy for this job, torn down after the run."],
  html=[H2('A fast file system, only when needed', 0),
        LIST([('Lustre: managed on all three big clouds', 0, 0.4), ('WEKA, VAST: common at neoclouds', 0, 1.0), ('you buy speed by buying capacity', 1, 0.3), ('bucket = master, fast file system = a job-sized copy', 1, 0.9)], kind='ar', style='margin-top:24px;font-size:42px')]),

 dict(id='s14', chap='Checkpoint size', say=[
   "Checkpoints are the other big storage event. A full training checkpoint stores more than the weights. In the common setup it is fourteen bytes per parameter. Two for the weights, four for a full precision copy, and four each for the optimiser's two memories.",
   "So a seventy billion parameter model has a checkpoint close to one terabyte. A four hundred and five billion model, about five point seven. That is arithmetic from the notebook's formula."],
  html=[H2('Checkpoint size', 0),
        DEF('14 bytes per parameter = 2 + 4 + 4 + 4', 0, 0.4, style='margin-top:24px;font-size:52px'),
        TABLE(['Model', 'Checkpoint'], [(['70B', '0.98 TB'], 1, 0.3), (['405B', '5.67 TB'], 1, 0.9)], style='margin-top:20px;font-size:44px')]),

 dict(id='s15', chap='The stall', say=[
   "If training waits for the write, the GPUs idle. A terabyte written at ten gigabytes per second is about a hundred seconds. At a hundred gigabytes per second, ten. These speeds are my assumptions.",
   "The big models are worse. The fix is asynchronous saving. Copy the state to memory or local disk, let training continue, and drain it to the bucket in the background."],
  html=[H2('How long the GPUs wait', 0), SVG('c15', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c15', 'ckpt', 1000, 310, 1)]),

 dict(id='s16', chap='The lakehouse', say=[
   "Now structured data, like tables of customers, tickets and logs. The modern pattern is called a lakehouse. Files in a columnar format called Parquet, sitting in object storage.",
   "On top, a table format such as Delta or Iceberg adds transactions and snapshots. On top of that, a catalog holds names, permissions and lineage. Any query engine can read it. Engines come and go, the tables stay."],
  html=[H2('The lakehouse in four boxes', 0), SVG('c16', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c16', 'lake', 1000, 290, 1)]),

 dict(id='s17', chap='Versioning data', say=[
   "If you cannot reproduce last month's training data, you cannot reproduce last month's model. Version your data at three levels. Files, with tools like DVC or Hugging Face. Whole lakes, with branches, using lakeFS. And tables, using snapshots.",
   "Pin every training run to a version. In the table world, that means a snapshot number you can query later."],
  html=[H2('Version your data', 0), SVG('c17', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c17', 'versions', 1000, 290, 1)]),

 dict(id='s18', chap='The retention trap', say=[
   "A trap with Delta tables. Time travel needs the old files. By default, the clean up job deletes files older than seven days. So last month's training snapshot is already gone.",
   "Set the retention to at least as long as you want to look back, ninety days is common. This is a documented default, not something I measured."],
  html=[H2('Time travel has a default expiry', 0),
        OUT(['deleted files kept:  7 days (default)', 'log kept:            30 days (default)', 'set both to 90 days to look back a quarter'], 0, 0.4, size=32, label='Delta defaults (notebook)', style='margin-top:22px'),
        MARK('last month\'s training set is already gone', 1, 0.6)]),

 dict(id='s19', chap='Reproducibility and quality', say=[
   "A reproducible training run records four things. The data snapshot, the code commit, the tokenizer and preprocessing version, and the embedding model version. Put them in your model registry.",
   "And before data is written into training sets or search indexes, check it. Schema, nulls, duplicates, personal data, and overlap with your evaluation set. Bad data costs more the later you find it."],
  html=[H2('Reproduce it, and check it first', 0),
        LIST([('data snapshot id', 0, 0.3), ('code commit', 0, 0.7), ('tokenizer + preprocessing version', 0, 1.1), ('embedding model version', 0, 1.5)], kind='ar', style='margin-top:22px;font-size:42px'),
        SUB('check first: schema, nulls, duplicates, personal data, eval overlap', 1, 0.6, style='margin-top:14px')]),

 dict(id='s20', chap='What a vector is', say=[
   "Now vectors. An embedding model turns text, or an image, into a list of numbers, called a vector. Similar meanings land close together. To search, you embed the question and find the nearest vectors.",
   "The simplest search compares the question to every stored vector. That is exact, but it slows down as the collection grows. Real systems use an approximate method, trading a little accuracy for a lot of speed."],
  html=[H2('A vector: meaning as numbers', 0),
        DEF('similar meaning = <b>close</b> numbers · search = find the nearest', 0, 0.4, style='margin-top:24px;font-size:48px'),
        ROW(COL(CARD('<b>exact</b><br>compare with all, slow at scale', 1, 0.3, style='font-size:38px'), width='48%'),
            COL(CARD('<b>approximate</b><br>a little accuracy for big speed', 1, 0.9, style='font-size:38px'), width='48%'), style='margin-top:22px')]),

 dict(id='s21', chap='How big are vectors?', say=[
   "How much memory do vectors need? Bytes per vector equals the dimensions times the bytes per number. A model with seven hundred and sixty-eight dimensions in the standard format uses three thousand and seventy-two bytes per vector.",
   "Fifty thousand of them is about a hundred and fifty-four megabytes. Ten million is over thirty gigabytes. Memory is the main cost of vector search, so compression matters."],
  html=[H2('Bytes per vector', 0),
        DEF('bytes = dimensions × bytes per number', 0, 0.4, style='margin-top:24px;font-size:50px'),
        OUT(['768 dims × 4 bytes = 3,072 bytes', '50,000 vectors = 153.6 MB', '10,000,000 vectors ≈ 30.7 GB'], 1, 0.4, size=32, label='arithmetic', style='margin-top:20px')]),

 dict(id='s22', chap='My compression experiment', say=[
   "I tested compression. Fifty thousand synthetic vectors of seven hundred and sixty-eight numbers each. They are random clusters, not real embeddings, so treat the results as a pattern. Exact search on the full copy is the truth.",
   "Then I stored them as half size numbers, as one byte numbers, and as single bits. And I measured recall at ten, meaning how many of the true top ten each version still found."],
  html=[H2('Compression test', 0),
        OUT(['50,000 vectors × 768 numbers (synthetic)', '300 queries · truth = exact float32 search', 'recall@10 = share of the true top 10 found'], 0, 0.4, size=32, label='measured setup', style='margin-top:22px'),
        SUB('synthetic clusters, not real embeddings', 1, 0.6, style='margin-top:14px')]),

 dict(id='s23', chap='Compression, measured', say=[
   "Half size numbers, float sixteen, found every true neighbour. Recall one point zero, at half the memory. One byte numbers found ninety-eight and a half percent at a quarter of the memory.",
   "Single bits shrank it thirty-two times, but on their own found only twenty-one percent. After rescoring the best hundred candidates with the full numbers, recall came back to seventy-four percent.",
   "So bits are a first filter, not an answer. The notebook warns they work worse under about four hundred dimensions, and better as dimensions grow."],
  html=[H2('Smaller vectors, recall measured', 0), SVG('c23', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c23', 'formats', 1000, 290, 1)]),

 dict(id='s24', chap='Finding neighbours fast', say=[
   "Now the speed side. The most popular approximate method is HNSW. It builds a layered graph. Imagine a map with motorways at the top, main roads in the middle, and every street at the bottom.",
   "A search starts at the top, hops to whichever node is closest to your question, and drops a layer when it gets stuck.",
   "Finally it looks around its neighbours on the bottom layer. It never visits most of the data."],
  html=[H2('HNSW: motorways, roads, streets', 0), SVG('c24', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c24', 'hnsw', 1000, 300, 1)]),

 dict(id='s25', chap='HNSW knobs and memory', say=[
   "Two knobs matter. M is how many links, or friends, each node keeps. More friends means more memory. And ef is how hard you look, when building and when searching. Looking harder is slower but finds more.",
   "Memory is about N times four dimensions plus eight M bytes. For my test that formula said a hundred and sixty megabytes, and the real index file was a hundred and sixty-one. Close enough to plan with."],
  html=[H2('HNSW: two knobs and a memory formula', 0),
        LIST([('M = friends per node (more = more RAM)', 0, 0.4), ('ef = how hard you look (more = slower)', 0, 1.0)], kind='ar', style='margin-top:24px;font-size:44px'),
        OUT(['N × (4d + 8M) = 50,000 × (3,072 + 128) = 160 MB', 'real index file: 161 MB'], 1, 0.4, size=32, label='formula vs measured', style='margin-top:18px')]),

 dict(id='s26', chap='HNSW, measured', say=[
   "Here is recall against effort. At effort ten, recall was fifty-six percent. At fifty, ninety-six, in point two milliseconds per query. At a hundred, ninety-nine point eight percent.",
   "Exact search took one point two one milliseconds for the same questions. So at ninety-six percent recall, the graph was about six times faster, and the gap grows as the collection grows."],
  html=[H2('Recall against effort', 0), SVG('c26', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c26', 'hnsw_ef', 1000, 300, 1)]),

 dict(id='s27', chap='Other index families', say=[
   "HNSW lives in memory. For bigger collections, other designs exist. IVF with compression clusters the data and squeezes each vector. DiskANN keeps the graph on fast disks. And object tiered systems keep vectors in cheap storage, with search taking around a hundred milliseconds.",
   "No family wins everywhere. Memory is fast and costly. Disk and object storage are slower and cheap. You choose by how many vectors you have and how quickly users need an answer."],
  html=[H2('Beyond memory', 0),
        TABLE(['Family', 'Lives in', 'Good at'], [(['HNSW', 'RAM', 'low latency, high recall'], 0, 0.4), (['IVF + compression', 'RAM, squeezed', 'small memory, fast build'], 0, 1.0), (['DiskANN', 'SSD + RAM', 'billions per machine'], 1, 0.3), (['object-tiered', 'cheap storage', 'cheapest, about 100 ms'], 1, 0.9)], style='margin-top:22px;font-size:36px')]),

 dict(id='s28', chap='Choosing a vector store', say=[
   "Which product should you pick? Start with what you already run. If you have Postgres, the pgvector extension handles millions of vectors, and it stores half size numbers, which my test showed lose nothing. Object backed stores such as S three Vectors suit huge, cheap, slower collections.",
   "Dedicated databases suit heavy, low latency workloads. And all of them work better with keyword search added, which is a topic for lesson eight."],
  html=[H2('Pick what you already run', 0),
        TABLE(['Situation', 'Start with'], [(['already on Postgres, millions of vectors', 'pgvector, half-size numbers'], 0, 0.4), (['huge and cheap, slower is fine', 'object-backed (S3 Vectors)'], 0, 1.0), (['heavy, low-latency search', 'a dedicated vector database'], 1, 0.3)], style='margin-top:24px;font-size:40px')]),

 dict(id='s29', chap='ShopNest Copilot', say=[
   "For ShopNest Copilot. Raw tickets and evaluation sets live in regional object storage, packed in shards. The nightly evaluation job reads shards, not thousands of tiny files. Checkpoints are saved asynchronously.",
   "The support articles, a few hundred thousand chunks, go in pgvector as half size vectors with an HNSW index. And we record the embedding model version, so we can rebuild the index at any time."],
  html=[H2('ShopNest Copilot: data plan', 0),
        TABLE(['Data', 'Where'], [(['tickets, eval sets', 'regional object storage, in shards'], 0, 0.4), (['checkpoints', 'async save, regional copy'], 0, 1.0), (['support-article vectors', 'pgvector, halfvec, HNSW'], 1, 0.3), (['index', 'rebuildable: record the model version'], 1, 0.9)], style='margin-top:22px;font-size:38px')]),

 dict(id='s30', chap='Four words to keep', say=[
   "Four words to carry forward. Shard: a big file packed with many samples. Egress: the charge for data leaving a cloud.",
   "Recall: the share of true nearest neighbours a search returns. And quantisation: storing numbers with fewer bits to save memory."],
  html=[H2('Four words to keep', 0),
        GRID([('<b>shard</b>', 0, 0.3), ('<b>egress</b>', 0, 0.9), ('<b>recall</b>', 1, 0.3), ('<b>quantisation</b>', 1, 0.9)], cols=2, h=140, fs=48, style='margin-top:30px')]),

 dict(id='s31', chap='Interview corner', say=[
   "Interview corner. Asked why not store training data as millions of small files, say: every object store request has a fixed delay, so small reads are dominated by delay. Pack samples into shards of a hundred megabytes to a gigabyte. In my test, small files read twenty-five times slower.",
   "Asked how to cut vector memory, say: store half size or one byte numbers. In my test, one byte numbers kept recall at ninety-eight and a half percent at a quarter of the memory, but plain bits dropped to twenty-one."],
  html=[H2('Interview corner', 0),
        Q('Why not millions of small files?', 'Each request has a fixed delay. Shards of 100 MB to 1 GB: small files read 25x slower.', 0, 0.4),
        Q('How do you cut vector memory?', 'float16 or int8: 0.985 recall at a quarter. Plain bits: 0.21.', 1, 0.4)]),

 dict(id='s32', chap='Your turn', say=[
   "Your turn. The zip for this lesson has three scripts. The first compares reading small files and shards on your own disk. The second compares vector formats and the graph index. The third is the checkpoint and egress arithmetic.",
   "Change the vector dimensions, or the number of files, and see what moves. One changed number teaches more than an hour of reading."],
  html=[H2('Your turn', 0),
        CARD('<b>l04_small_files.py</b>: small files against a shard, on your disk.<br><b>l04_vectors.py</b>: vector formats and the graph index.<br><b>l04_checkpoint_math.py</b>: checkpoint size, stall and egress.', 0, 0.4, style='margin-top:22px;font-size:36px'),
        SUB('one changed number teaches more than an hour of reading', 1, 0.8, style='margin-top:16px')]),

 dict(id='s33', chap='Recap', say=[
   "Recap. Region is truth, zone is speed, and egress is the real bill. Small files are slow, so pack shards. Twenty thousand files read twenty-five times slower than one. A checkpoint is fourteen bytes per parameter. Version your data, and mind the seven day default.",
   "Half size or one byte vectors keep nearly all recall at a half or a quarter of the memory. A graph index found ninety-six percent of true neighbours, six times faster than exact search. Next lesson: training at scale. Where the memory goes, and how to split a model."],
  html=[H2('Recap', 0),
        GRID([('region = truth · egress = bill', 0, 0.3), ('shards, not small files: 25x', 0, 0.9), ('checkpoint = 14 B / param', 0, 1.5),
              ('version data · 7-day default', 1, 0.3), ('int8: 0.985 recall, ¼ memory', 1, 0.9), ('HNSW: 96% recall, 6x faster', 1, 1.5)], cols=3, h=150, fs=30)]),
]
