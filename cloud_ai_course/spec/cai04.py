import sys; sys.path.insert(0, '/home/claude/caigen')
from cai_lib import *
from c04_diagrams import DIAGRAMS
from c04_long import LONG
from c04_notes import NOTES

L = dict(
 code='CAI-04', num=4, num_word='four', slug='Data_And_Storage_For_AI',
 title='Data and Storage', title_html='Data &amp;<br>storage', title_size=140,
 tagline='Where AI data lives, how to read it fast, and how vectors work.', module='Module 2 · Packaging and storing',
 toc=['Object storage and egress', 'Small files vs shards', 'Checkpoints', 'Lakehouse and versions', 'Vectors, measured', 'HNSW', 'Interview Q&amp;A'],
 data_label='Course project', project='ShopNest Copilot', project_desc='the AI support assistant we move to the cloud, step by step',
 prev='CAI-03', next=('CAI-05', '<b>Training at scale</b>: where the memory goes and how to split a model'),
 next_say='training at scale. Where the memory goes, and how to split a model across GPUs.',
 diagrams=DIAGRAMS, long=LONG, notes=NOTES,
 glow=dict(a='DATA AND', b='STORAGE', icons=['cyl1', '>', 'cloud2']),
 thumb=dict(title='Data &amp;<br><span class="hl">storage</span>', size=124, sub='small files vs shards', chips=('measured', '25x slower'), mini='mini_thumb'),

 short1=mk_short(1, 'Small_Files_Are_25x_Slower', "The same eighty megabytes took twenty-five times longer to read. The only difference was the file size.",
   ('SAME DATA', '25X SLOWER', 130, 110),
   ["I made eighty megabytes three ways and read each one, after clearing the file cache. Twenty thousand tiny files took one point three four seconds. One single shard took five hundredths of a second.",
    "That was a fast local disk. A cloud object store adds a delay per request, so the gap grows. Pack your samples into shards."],
   'mini_files', "Big files, not many small files.", 'Fix', 'pack into<br><b>shards</b>', dict(title='Small files are<br><span class="hl">25x slower</span>', size=100, sub='same 80 MB, measured', mini='mini_files'),
   dict(title='Why 20,000 Small Files Read 25x Slower Than One #shorts',
     desc="Same 80 MB, three layouts, local disk, page cache dropped, best of 3:\n• 20,000 files of 4 KB: 1.34 s\n• 80 files of 1 MB: 0.08 s\n• one 80 MB shard: 0.05 s\n\nCloud object stores add a delay per request, so the gap is bigger there (model with assumed numbers).\n\nFull lesson: Cloud for AI Engineers, lesson 4.",
     tags='shorts, small files problem, data sharding, webdataset, ai training data, object storage, cloud for ai engineers, the code notebook',
     pinned='How many files is your training set made of? 👇')),

 short2=mk_short(2, 'Shrink_Vectors_4x_Keep_98_Percent', "You can shrink your vector database four times and still find ninety-eight percent of the right answers.",
   ('4X SMALLER', '98% KEPT', 130, 130),
   ["I made fifty thousand synthetic vectors of seven hundred and sixty-eight numbers each. Stored as full floats they took one hundred and fifty-four megabytes. As one byte numbers, thirty-eight.",
    "Recall at ten, the share of true neighbours found, was point nine eight five. Half size numbers found all of them. These are synthetic vectors, so treat it as a pattern."],
   'mini_vec', "Try float16 or int8 before buying more memory.", 'Try this', 'float16 or<br><b>int8</b> first', dict(title='Shrink vectors<br><span class="hl">4x</span>', size=104, sub='keep 98% recall', mini='mini_vec'),
   dict(title='Shrink Your Vector Database 4x and Keep 98% Recall #shorts',
     desc="50,000 SYNTHETIC vectors x 768 numbers (not real embeddings), recall@10 vs exact float32 search:\n• float32: 153.6 MB, 1.000\n• float16: 76.8 MB, 1.000\n• int8: 38.4 MB, 0.985\n• 1-bit (Hamming only): 4.8 MB, 0.212\n\nFull lesson: Cloud for AI Engineers, lesson 4.",
     tags='shorts, vector database, quantization, embeddings memory, pgvector halfvec, rag cost, cloud for ai engineers, the code notebook',
     pinned='Do you compress your embeddings? 👇')),

 reel=mk_reel('Egress_Costs_9000_Dollars', ["Why moving data out of the cloud costs nine thousand dollars.",
   "Storing data is cheap, but egress, the charge for data leaving, is about nine cents per gigabyte at list price. One hundred terabytes is a hundred thousand gigabytes, so nine thousand dollars."],
   "Move the job to the data, not the data to the job. Save this.", '$9,000', ['store 100 TB: cheap', 'move 100 TB out: $9,000'], [3.4, 6.2], 'Arithmetic', '<b>$0.09</b> per GB out',
   dict(title='Moving 100 TB<br><span class="hl">costs $9,000</span>', size=100, sub='the egress trap', mini='mini_egress'),
   dict(title='Moving 100 TB out of the cloud costs $9,000',
     caption="The cloud bill nobody warns you about. 💸\n\nStoring data: cheap.\nMoving it OUT (egress): about $0.09 per GB at list price.\n\n100 TB = 100,000 GB x $0.09 = $9,000.\n\nMove the job to the data, not the data to the job.\n\nArithmetic from list prices, not a quote. Save this. Full lesson on YouTube: The Code Notebook.",
     pinned="Lesson 5 next: training at scale 🧠 Follow so you don't miss it!")),

 upload=dict(
   title='Why 20,000 Small Files Read 25x Slower Than One (AI Data Storage)',
   hook="Lesson 4 of Cloud for AI Engineers. I read the same 80 MB as 20,000 small files and as one shard. The small files took 25 times longer. This lesson is about where AI data lives and how to read it fast.",
   what="We cover object storage tiers, the egress bill, why small files hurt and shards fix it, checkpoint size and stalls, the lakehouse, dataset versioning and the 7 day retention trap, then vectors: what they are, how much memory they need, how float16 and int8 shrink them with almost no loss, and how HNSW finds neighbours fast. File reads and vector tests are measured on the build machine (vectors are synthetic), the object store timing is a model with assumed numbers, and prices are list prices from October 2026.",
   bullets=['Object storage: a filing cabinet with tiers', 'Region is truth, zone is speed', 'Egress: why moving 100 TB costs about $9,000 at list price', 'Small files vs shards: measured 25x',
            'An object store model with assumed latency', 'WebDataset and Mosaic streaming', 'Checkpoint size: 14 bytes per parameter, and the stall', 'The lakehouse in four boxes', 'Dataset versioning and the 7 day default trap',
            'What a vector is and how big it is', 'Shrinking vectors: float16, int8 and binary, measured', 'HNSW: layers, M and ef, and recall vs effort', 'Choosing a vector store', 'ShopNest Copilot data plan', 'Interview questions with answers'],
   hashtags='#cloudcomputing #datastorage #vectordatabase #ai #aiengineering',
   tags='small files problem, data sharding, object storage explained, s3 egress cost, vector database memory, hnsw explained, quantization embeddings, pgvector, lakehouse, delta lake time travel, cloud for ai engineers, the code notebook',
   pinned="File reads and vector tests were measured on the build machine (synthetic vectors). The object store timing is a model with assumed numbers. 📊\n\nQuestion for you 👇\nWhich surprised you more: 25x slower for small files, or 98% recall at a quarter of the vector memory?"),
)

import interview; L['notes'] = interview.add(L['notes'], L['num'])
