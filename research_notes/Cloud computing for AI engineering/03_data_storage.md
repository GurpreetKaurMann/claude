# Data and Storage for AI Engineering in the Cloud (state as of October 2026)

How to read these notes: research was done on 2026-10-14. All web page fetches (aws.amazon.com, docs.aws.amazon.com, infoq.com, qdrant.tech, etc.) were blocked by the session's egress-proxy policy (HTTP 403 on CONNECT). So every "Cited Finding" below comes from search-engine result summaries of the linked pages, not from reading the full pages. The shared web-search budget also ran out partway through (after ~29 searches). Topics searched late or not at all (Azure AI Search, MongoDB Atlas, Weaviate, LanceDB, turbopuffer, feature-store internals, Kinesis/Pub/Sub/Flink, PII tooling) depend more on background knowledge.
Tags used:
- **[BG]**: background knowledge from before this session. It was NOT re-verified here. The canonical URL is given but was not re-fetched. Verify before quoting.
- **[3P]**: a third-party or aggregator source.
- **[Vendor]**: a vendor's own benchmark or claim.
- Dates in brackets such as "[2020]" or "[2024]" mark older items.

---

## 1. Object storage for AI (S3, S3 Express One Zone, GCS, Azure Blob) and training data loading

### Takeaway
Regional object storage (S3 Standard, GCS regional, Azure Blob) is the durable source of truth for nearly all AI data. It is strongly consistent, scales by parallelism (requests per prefix and many connections), and is cheap per GB. Egress and request charges, not storage, usually decide cost. For accelerator-adjacent speed, every hyperscaler now sells a zonal, low-latency object tier: S3 Express One Zone (prices cut up to 85% in April 2025) and GCS Rapid Bucket/Rapid Storage (sub-ms, up to 15 TB/s, 20M QPS), plus zonal read caches. Training data should be sharded into ~100 MB–1 GB sequential objects (WebDataset tar, Mosaic MDS) and streamed. Do not random-read millions of small files.

### Cited Findings
**Consistency and request scaling (S3)**
- S3 has had strong read-after-write consistency for all PUTs/overwrites/deletes, with strongly consistent LIST, automatically and at no extra cost since December 2020 [2020] — [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2020/12/amazon-s3-now-delivers-strong-read-after-write-consistency-automatically-for-all-applications); [InfoQ](https://www.infoq.com/news/2020/12/aws-s3-strong-consistency/)
- Baseline request rates: "at least 3,500 PUT/COPY/POST/DELETE or 5,500 GET/HEAD requests per second per partitioned prefix". Scaling comes from spreading keys across prefixes; there is no limit on the number of prefixes — [AWS performance best practices](https://aws.amazon.com:443/articles/1904); [AWS re:Post knowledge center](https://repost.aws/knowledge-center/s3-object-key-naming-pattern)
- Auto-partitioning after a load spike can take ~30–60 min. Until it completes, clients get HTTP 503 "Slow Down" responses, so you need retry with exponential backoff — [AWS re:Post thread](https://repost.aws/ja/questions/QUJ-OgPd_8QxKygfdagbs4zA/how-to-benchmark-io-throughput-storage-capacity-and-latency-per-s3-storage-class) [3P, community answer]; [AWS knowledge center](https://repost.aws/knowledge-center/s3-object-key-naming-pattern)
- S3 conditional writes: `If-None-Match: *` (put-if-absent, August 2024) and `If-Match` with an ETag (compare-and-swap, November 2024). Together they give linearizable single-key operations. These are the basis for lock-free table-format commits and "object store as database" designs [2024] — [3P skills page](https://mcpservers.org/agent-skills/triggerdotdev/staff-engineering-skills-object-store-as-database); [3P blog](https://mohakchugh.is-a.dev/blog/s3-conditional-writes-distributed-coordination)

**S3 Express One Zone (single-AZ "directory buckets")**
- Price cut effective April 10, 2025: storage −31%, PUT −55%, GET −85%. Per-GB upload/retrieval charges −60%, and these now apply to all bytes rather than only the part of a request above 512 KB — [AWS What's New, Apr 2025](https://aws.amazon.com/about-aws/whats-new/2025/04/amazon-s3-express-one-zone-reduces-storage-request-prices/); [AWS News Blog](https://aws.amazon.com/es/blogs/aws/up-to-85-price-reductions-for-amazon-s3-express-one-zone/)
- Scale: up to 2 million GET TPS and 200,000 PUT TPS per directory bucket — [AWS News Blog](https://aws.amazon.com/es/blogs/aws/up-to-85-price-reductions-for-amazon-s3-express-one-zone/)
- Launched November 2023, marketed as single-digit-ms latency and "up to 10x faster than S3 Standard". It stores data in one AZ, so you lose multi-AZ durability. Co-locate it with compute [2023] — [Blocks & Files](https://blocksandfiles.com/2023/11/29/aws-s3-express-one-zone/); [The New Stack](https://thenewstack.io/amazon-s3-express-one-zone-introduces-near-real-time-object-storage/)
- AWS claims Spark on EMR runs up to 31% faster with S3 Express One Zone [Vendor] — [AWS Storage Blog](https://aws.amazon.com/blogs/storage/run-spark-31-faster-and-optimize-compute-costs-with-amazon-s3-express-one-zone-on-amazon-emr/)

**Google Cloud Storage**
- **Rapid Bucket / Rapid Storage (zonal):** launched at Next '25 claiming "<1 ms random read and write latency, 20x faster data access, 6 TB/s throughput". Current docs say sub-ms latency, up to 15 TB/s aggregate throughput and up to 20M QPS. It supports stateful, streaming object appends, which suit checkpoints and logs. Google recommends it for training, checkpointing and model serving — [InfoQ May 2025](https://www.infoq.com/news/2025/05/google-cloud-rapid-storage); [GCS Rapid docs](https://docs.cloud.google.com/storage/docs/rapid/high-performance-storage); [Google Cloud blog](https://cloud.google.com/blog/products/storage-data-transfer/high-performance-storage-innovations-for-ai-hpc/)
- **Anywhere Cache (renamed "Rapid Cache" in some doc versions):** a managed, SSD-backed zonal read cache in front of existing regional, dual-region or multi-region buckets, with no API changes. Launch claims: up to 2.5 TB/s and 70% lower latency [Vendor]. Google advises a pre-read ("warm") of the dataset before epoch 1 — [Google Cloud blog](https://cloud.google.com/blog/products/storage-data-transfer/high-performance-storage-innovations-for-ai-hpc/); [GCS AI zones doc](https://docs.cloud.google.com/storage/docs/ai-zones)
- Google's reference pattern: a regional bucket is the durable source of truth, and a zonal "performance layer" acts as high-speed cache or scratch next to the GPUs/TPUs — [GCS AI zones doc](https://docs.cloud.google.com/storage/docs/ai-zones)
- Cloud Storage FUSE mounts buckets as file systems. In one customer anecdote, moving from Lustre to GCS FUSE gave 50% lower training cost and 14% shorter training time (single example from a talk) — [GCP architecture guide: optimize AI/ML with Cloud Storage FUSE](https://docs.cloud.google.com/architecture/optimize-ai-ml-workloads-cloud-storage-fuse?authuser=1); [Tech Field Day](https://techfieldday.com/video/google-cloud-storage-for-ai-ml-workloads)

**Egress and data-transfer costs (2026)**
- Entry internet-egress list rates: AWS ~$0.09/GB, Azure ~$0.087/GB, GCP Premium tier ~$0.12/GB. Cloudflare R2 charges $0/GB egress. AWS standard tiers drop to ~$0.05/GB at volume — [eCorpIT 2026 comparison](https://ecorpit.com/cloud-egress-fees-ai-inference-bill-comparison-2026/) [3P]; [stmicro blog](https://www.stmicro.net/blog/cloud-egress-fees-hidden-costs-2026/) [3P]
- All three hyperscalers waive egress only when a customer is leaving the platform. Google has done so since January 2024. AWS's exit window was reportedly extended to 90 days on 30 Sept 2025 (previously 60) and is handled through support and credits. Routine serving egress stays fully billable — [The Register, Sept 2025](https://www.theregister.com/2025/09/10/big_clouds_scramble_over_eu/); [cloudmagazin Aug 2026](https://www.cloudmagazin.com/2026/08/02/cloud-egress-free-tiers-exit-waiver-stille-kosten/) [3P]; [wz-it](https://wz-it.com/en/blog/cloud-exit-strategy-smes/) [3P]
- The EU Data Act bans switching charges outright. Sources conflict on the date: 12 January 2027 per [sota.io](https://sota.io/blog/eu-data-act-2025-cloud-switching-rights-developer-guide) [3P], versus 12 September 2027 in another [3P] summary. (My [BG] reading of Art. 29 is 12 January 2027, with cost-based reduced charges allowed until then. Verify against the regulation text.)

**Training data loading formats**
- **MosaicML StreamingDataset:** a PyTorch-compatible dataset that streams shards from AWS, GCS, Azure, OCI, Databricks and any S3-compatible store (Cloudflare R2, CoreWeave, Backblaze B2). Its native shard format is **MDS**, and it also reads CSV/TSV/JSONL. It is designed for multi-node distributed training and any modality (text, image, video, multimodal) — [PyPI mosaicml-streaming](https://pypi.org/project/mosaicml-streaming); [Databricks blog](https://www.databricks.com/en/blog/mosaicml-streamingdataset)
- **WebDataset:** a convention, not a database. Samples are stored as groups of sibling files sharing a basename (e.g., `000123.jpg`, `000123.txt`, `000123.json`) inside POSIX `.tar` shards, and readers iterate the tar sequentially — [ZeroEntropy explainer](https://zeroentropy.dev/concepts/streaming-datasets/) [3P]
- Why shards: sequential reads of ~100 MB chunks reach ~80% of object-store bandwidth, while random 1 KB reads reach ~1%. Typical shards are 100 MB–1 GB, and each worker holds ~1 shard plus a shuffle buffer in memory — [ZeroEntropy explainer](https://zeroentropy.dev/concepts/streaming-datasets/) [3P]
- [BG] StreamingDataset's distinguishing features are deterministic sample order regardless of GPU/node count ("elastic determinism"), fast mid-epoch resumption, and a local disk cache with shard eviction. These make it a common choice for resumable LLM pretraining on preemptible capacity — [Databricks/MosaicML blog](https://www.databricks.com/en/blog/mosaicml-streamingdataset)

**Other [BG] facts (not re-verified)**
- S3 Standard list price is ~$0.023/GB-month (us-east-1, first 50 TB). Colder classes are S3 Standard-IA, One Zone-IA, Glacier Instant/Flexible/Deep Archive and Intelligent-Tiering. GCS has Standard/Nearline/Coldline/Archive with 30/90/365-day minimum durations. Azure Blob has Hot/Cool/Cold/Archive plus Premium block blobs, and ADLS Gen2 adds a hierarchical namespace — [S3 pricing](https://aws.amazon.com/s3/pricing/); [GCS storage classes](https://cloud.google.com/storage/docs/storage-classes); [Azure access tiers](https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview)
- AWS loaders and connectors: Mountpoint for Amazon S3 (FUSE client, GA 2023) and the Amazon S3 Connector for PyTorch (2023; map/iterable datasets plus checkpoint save/load straight to S3) — [Mountpoint GitHub](https://github.com/awslabs/mountpoint-s3); [S3 Connector for PyTorch](https://github.com/awslabs/s3-connector-for-pytorch)

### Inferences
- **Decision rule, data path:** keep the canonical copy in regional object storage, and pre-tokenize or shard it into 100 MB–1 GB objects. Then stream it (Mosaic MDS for resumable, deterministic multi-node LLM training, or WebDataset for simple tar-based multimodal pipelines). Only add a zonal tier (S3 Express One Zone, GCS Rapid/Anywhere Cache) or a parallel file system when profiling shows the GPU waiting on input, or when checkpoint stalls are material.
- **Text LLM pretraining is rarely I/O-bound.** At 2 bytes per token (uint16 ids), 15T tokens ≈ 30 TB, read about once per epoch. Multimodal and video, small-file random access, and checkpoint bursts are what stress storage.
- **Egress math:** moving a 100 TB dataset out of AWS to the internet at tiered ~$0.09→$0.07/GB costs ~$8k–9k. Cross-cloud GPU "follow the capacity" strategies should budget this, or use zero-egress stores (R2) or provider exit waivers. Cross-AZ and cross-region replication charges also apply inside one cloud.
- Single-AZ tiers (S3 Express One Zone, GCS Rapid zonal buckets) should hold re-creatable data (caches, scratch, recent checkpoints that are also copied to regional storage), never the only copy.

### Gaps
- Absolute post-April-2025 S3 Express One Zone prices ($/GB-month, $/1k requests) could not be fetched. Only percentage cuts were confirmed. My [BG] recollection is ~$0.11/GB-month storage, not verified.
- Azure Blob AI-specific throughput figures (scaled or premium accounts, per-account egress limits as of 2026) were not searched (budget exhausted).
- I found no head-to-head 2025–2026 benchmark of WebDataset vs MDS vs Ray Data vs Hugging Face streaming on resumption and throughput.
- The exact EU Data Act zero-switching-charge date has conflicting secondary sources.

---

## 2. High-performance file systems for training and checkpoints

### Takeaway
Managed Lustre is now the standard "fast POSIX tier" on all three hyperscalers:
- **AWS:** FSx for Lustre, now with an Intelligent-Tiering storage class and EFA/GPUDirect Storage at up to 1,200 Gbps per client.
- **GCP:** Managed Lustre, GA June 30, 2025, with 125–1,000 MB/s per TiB tiers. It appears to be displacing DAOS-based Parallelstore.
- **Azure:** Managed Lustre, with 40–500 MB/s per TiB tiers.
WEKA, VAST and DDN fill the same role on GPU clouds and in marketplaces. You need a parallel file system when many GPUs need high aggregate bandwidth to POSIX files, small-file or random metadata-heavy access, or fast synchronous checkpoint writes. Otherwise object storage plus streaming is cheaper.

### Cited Findings
**AWS FSx for Lustre**
- Intelligent-Tiering file systems: throughput is provisioned per file system (not per TiB) in 4,000 MBps increments up to 2,000,000 MBps (2 TB/s). Each OSS delivers 4,000 MBps and holds up to 512 TiB. Metadata IOPS options are 6,000 or 12,000 — [FSx Lustre docs: throughput capacity](https://docs.aws.amazon.com/fsx/latest/LustreGuide/managing-throughput-capacity.html); [FSx Lustre performance](https://docs.aws.amazon.com/fsx/latest/LustreGuide/performance.html)
- Max per-client throughput is 100 Gbps over ENA or ENA Express, 700 Gbps with EFA, and 1,200 Gbps with EFA plus NVIDIA GPUDirect Storage (GDS), first shown on P5 instances. AWS recommends EFA for file systems above 10 GBps — [FSx Lustre performance](https://docs.aws.amazon.com/fsx/latest/LustreGuide/performance.html); [AWS News Blog launch](https://aws.amazon.com/blogs/aws/amazon-fsx-for-lustre-unlocks-full-network-bandwidth-and-gpu-performance/)
- [BG] SSD deployment types: Persistent-2 at 125/250/500/1,000 MB/s per TiB, plus Scratch-2 (~200 MB/s per TiB, no replication). FSx Lustre links to S3 through Data Repository Associations, which lazy-load objects on first access and can export changes back — [FSx Lustre deployment options](https://docs.aws.eu/fsx/latest/LustreGuide/using-fsx-lustre.html)

**Google Cloud**
- Managed Lustre went GA June 30, 2025, with four fixed tiers (1,000 / 500 / 250 / 125 MBps per TiB). The 1,000 tier targets AI/ML training and 125 targets large-capacity parallel access. Throughput scales linearly with provisioned capacity. A "Dynamic" tier (~25 MBps per TiB, lower cost) adapts to access patterns and has a separate quota — [Managed Lustre performance tiers](https://docs.cloud.google.com/managed-lustre/docs/performance-tiers); [release notes](https://docs.cloud.google.com/managed-lustre/docs/release-notes)
- Capacity ranges from 9,000 GiB to ~80.1 PiB, with throughput up to 10 TBps. Doc versions disagree: some localized pages show 1.5 TBps, and the maximum capacity for the 125 tier appears as 8, 11.7 or 19.5 PiB depending on page version — [Managed Lustre overview](https://docs.cloud.google.com/managed-lustre?authuser=0); [performance tiers](https://docs.cloud.google.com/managed-lustre/docs/performance-tiers)
- Parallelstore is DAOS-based scratch storage that Google once said gives up to 6x the read throughput of competing Lustre scratch services [Vendor]. Access requires allowlisting via sales. A Google partner says a phase-out in favor of Managed Lustre "has been announced or is foreseeable", but I found no official deprecation notice — [innFactory](https://innfactory.de/en/cloud/gcp/products/parallelstore/) [3P]; [Parallelstore page](https://cloud.google.com/parallelstore?hl=ja)

**Azure**
- Azure Managed Lustre (AMLFS) has durable SSD tiers of 40, 125, 250 and 500 MB/s per TiB. A pricing page dated 2026-09-17 lists these four. The MLPerf Storage v3.0 results doc also shows a "20" tier label and capacity increments of 96/48/16/8/4 TiB by tier, each increment giving ~2,000 MB/s. The 500 tier's minimum cluster is 4 TiB — [Azure pricing (azure.cn)](https://www.azure.cn/en-us/pricing/details/managed-lustre/index.html); [AMLFS MLPerf Storage v3.0 results](https://docs.azure.cn/en-us/azure-managed-lustre/mlperf-storage-v3-results); [Azure update: 40 and 500 MB/s/TiB tiers](https://azure.microsoft.com/en-us/updates/generally-available-40mbstib-and-500mbstib-performance-tiers-for-azure-managed-lustre)
- Azure first announced Managed Lustre for HPC and AI in 2023 [2023] — [Azure blog](https://azure.microsoft.com/en-us/blog/announcing-azure-managed-lustre-for-your-hpc-and-ai-workloads/)

**Third-party parallel or AI file systems**
- [BG] **WEKA** (WekaFS/NeuralMesh) and **VAST Data** (multiprotocol NFS/S3 "AI OS") are sold in AWS/GCP/Azure/OCI marketplaces and are the default storage at many GPU neoclouds (CoreWeave, Lambda and others). **DDN** EXAScaler (Lustre) is the technology partner behind Google Cloud Managed Lustre, and DDN Infinia is its object platform. None of this was re-verified this session — [WEKA](https://www.weka.io/); [VAST](https://www.vastdata.com/); [DDN](https://www.ddn.com/)

### Inferences
- **When you need a parallel file system:**
  1. Many small files or random reads that you cannot or will not re-shard (e.g., raw image or audio corpora, legacy code that needs POSIX).
  2. Very high aggregate read bandwidth from hundreds to thousands of GPUs, e.g., multimodal or video training.
  3. Fast synchronous checkpointing.
  4. HPC-style scratch shared across nodes.
  Otherwise, object storage plus sharded streaming plus an optional zonal cache is cheaper and simpler.
- **Checkpoint sizing math:** a full training checkpoint (bf16 weights plus fp32 master weights plus Adam m and v) is ~14–16 bytes per parameter. A 70B model is ≈1–1.1 TB, and a 405B model ≈6 TB. At 100 GB/s aggregate write, a 1 TB checkpoint takes ~10 s. At 10 GB/s it takes ~100 s of potential GPU idle time. This is why asynchronous or sharded checkpointing (write to local NVMe or host memory, then drain to Lustre or object storage) is the norm, and why Lustre tier choice is driven by checkpoint bandwidth.
- **Tier sizing:** with Lustre "MB/s per TiB" pricing, bandwidth needs often force buying more capacity than the data needs. A 1 PB-ish dataset is cheapest on a low tier. A 50 TB working set that needs 50 GB/s needs the 1,000 MB/s/TiB tier (50 TiB × 1 GB/s/TiB). Intelligent-Tiering on FSx decouples throughput from capacity.
- Pair Lustre with object storage: S3 or GCS holds the master copy, and Lustre is a hydrated cache for the active job (lazy load plus export), torn down after the run.

### Gaps
- No 2025–2026 primary data was collected on WEKA, VAST or DDN performance, pricing or cloud availability (search budget exhausted). These are [BG] only.
- Google Cloud Filestore (NFS) tiers and limits were not researched. [BG] Filestore is the managed NFS option for shared home directories and small-scale training, not high-bandwidth training.
- FSx Lustre Persistent-2 tier numbers and current $/GB pricing were not re-verified.
- MLPerf Storage v2/v3 comparative rankings across vendors were not collected.

---

## 3. Lakehouses and warehouses (Databricks, Snowflake, BigQuery, Iceberg) and their role in AI pipelines

### Takeaway
By 2026 the open table formats have largely converged. Iceberg v3 (deletion vectors, VARIANT, row lineage) is supported across Databricks Unity Catalog (DBR 18 LTS+), Snowflake (v3 GA reportedly May 2026) and AWS S3 Tables. Catalogs (Unity Catalog, Apache Polaris/Snowflake Open Catalog, AWS Glue/S3 Tables, BigLake) are the governance battleground. Each platform now bundles AI primitives next to the data:
- **Databricks:** Mosaic AI Vector Search, Lakebase (managed Postgres), Tecton-based real-time features.
- **Snowflake:** Cortex AISQL, Cortex Search.
- **BigQuery:** VECTOR_SEARCH with IVF/ScaNN-based TreeAH indexes, plus AI.EMBED/AI.GENERATE linked to Vertex AI.
In AI pipelines the lakehouse is the system of record for curated training data, features, evaluation sets, logs and traces, and it is the batch source for RAG indexes.

### Cited Findings
**Apache Iceberg v3 and table-format convergence**
- Iceberg v3 adds:
  - **Deletion vectors:** Roaring bitmaps of deleted row positions per data file, replacing v2 positional delete files. One vendor claims up to 10x faster DML.
  - **Row lineage:** `_row_id` and `_last_updated_sequence_number` fields, which enable change data capture.
  - **VARIANT:** a semi-structured type with shredding and filter pushdown.
  Upgrading by setting `'format-version'='3'` is one-way — [Google Open Source Blog, Aug 2025](https://opensource.googleblog.com/2025/08/whats-new-in-iceberg-v3.html?m=0); [Dremio](https://dremio.com/blog/apache-iceberg-v3); [Starburst](https://www.starburst.io/blog/iceberg-v3/); [AWS S3 Iceberg v3 doc](https://docs.aws.amazon.com/AmazonS3/latest/userguide/working-with-apache-iceberg-v3.md)
- AWS notes that upgrading an S3 Tables table to v3 does not backfill historical row-lineage records — [AWS S3 docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/working-with-apache-iceberg-v3.md)
- Databricks says the v3 features are consistent across Delta Lake, Parquet and Spark, so Delta and Iceberg can interoperate without rewriting data or delete files. Unity Catalog supports Iceberg v3 on managed Iceberg tables and on Delta tables with Iceberg reads (UniForm), and needs Databricks Runtime 18 LTS or later — [Databricks blog](https://www.databricks.com/en/blog/iceberg-v3-moving-ecosystem-towards-unification); [Azure Databricks Iceberg v3 docs](https://learn.microsoft.com/en-us/azure/databricks/iceberg/iceberg-v3)
- Iceberg v3 is reported GA on Snowflake on May 7, 2026 [3P, verify] — [Atlan](https://atlan.com/know/snowflake/apache-iceberg-v3/)
- MinIO AIStor Tables offers native Iceberg v3 on on-prem object storage — [MinIO blog](https://www.min.io/blog/aistor-tables-native-iceberg-v3-for-on-premises-object-storage)

**Catalogs**
- Snowflake launched Polaris Catalog (an Iceberg REST catalog) as open source in 2024 and later merged it with Project Nessie [2024]. Snowflake Open Catalog is the managed version: any engine speaking the Iceberg REST API can read and write, with centralized access control — [CIO Dive](https://ciodive.com/news/snowflake-summit-data-cloud-polaris-catalog-open-source-ai/718145); [Dremio](https://www.dremio.com/?p=21675); [Snowflake lakehouse page](https://snowflake.com/en/data-cloud/snowflake-for-data-lakehouse)
- Apache Polaris reportedly graduated to an Apache top-level project in February 2026. Snowflake Summit 2026 reportedly centered on Iceberg v3 GA and a Polaris-powered governance layer [3P] — [The State of Apache Iceberg Catalogs, June 2026](https://amdatalakehouse.substack.com/p/the-state-of-apache-iceberg-catalogs)

**Databricks**
- **Lakebase:** a fully managed Postgres (built on Neon technology, compute and storage separated) for AI apps and agents. Launched in Public Preview on June 11, 2025 and later GA (InfoQ, Feb 2026). It integrates with feature management and model serving — [Databricks press release](https://www.databricks.com/company/newsroom/press-releases/databricks-launches-lakebase-new-class-operational-database-ai-apps); [Lakebase docs](https://docs.databricks.com/aws/oltp); [InfoQ Feb 2026](https://infoq.com/news/2026/02/databricks-lakebase-postgresql/)
- Databricks agreed to acquire Tecton (August 2025) for real-time feature serving to AI agents and Agent Bricks (see Q6) — [Perficient](https://blogs.perficient.com/2025/09/26/databricks-acquires-tecton/)
- Delta time travel needs both a log entry and the data files for a version:
  - `delta.deletedFileRetentionDuration` defaults to **7 days** and governs what VACUUM removes. To keep 30 days, set it to `'30 days'`.
  - `delta.logRetentionDuration` defaults to **30 days**.
  - To time-travel N days back reliably, set both to at least N days.
  Reports say DBR 18 hard-blocks time travel past the file-retention window and requires log retention ≥ file retention [3P/community, verify] — [Databricks VACUUM docs](https://docs.databricks.com/aws/sql/language-manual/delta-vacuum); [Databricks community](https://community.databricks.com/t5/warehousing-analytics/dela-table-and-history/m-p/137263); [Substack](https://mbvyn.substack.com/p/understanding-databricks-time-travel)
- [BG] Background facts (not re-verified):
  - Databricks acquired Tabular (the Iceberg founders) in June 2024.
  - Unity Catalog was open-sourced in June 2024.
  - Mosaic AI Vector Search syncs from Delta tables (Delta Sync indexes).
  - Delta UniForm exposes Delta tables as Iceberg.
  - [Unity Catalog OSS](https://github.com/unitycatalog/unitycatalog)

**Snowflake**
- Cortex AISQL was announced June 3, 2025 (public preview then): AI functions inside SQL across text, images and documents, e.g., `AI_FILTER`, `AI_CLASSIFY`, `AI_AGG`. Snowflake Intelligence was "public preview soon" and Cortex Agents "GA soon" as of mid-2025 [2025 status, may be outdated] — [Snowflake press release](https://snowflake.com/en/news/press-releases/snowflake-introduces-cortex-aisql-and-snowconvert-ai-analytics-rebuilt-for-the-ai-era); [Snowflake blog](https://snowflake.com/en/blog/agentic-ai-ready-enterprise-data); [Coefficient overview](https://coefficient.io/?p=44299) [3P]
- A 2024 Snowflake post listed Cortex AI over Iceberg tables as a supported feature [2024] — [Snowflake blog](https://snowflake.com/blog/innovation-for-simplified-data-foundation)

**BigQuery**
- BigQuery has two vector index types:
  - **IVF:** k-means partitions, preferred for small query batches.
  - **TreeAH:** built on Google's ScaNN, preferred for large batches of hundreds or more queries. It works by sharding, clustering (`leaf_node_embedding_count`), product quantization, asymmetric-hashing scoring, then exact re-ranking.
  Indexes are used by `VECTOR_SEARCH` and `AI.SEARCH`. Embeddings can be generated in SQL with `AI.EMBED` against Vertex models (e.g., `text-embedding-005`) through a connection. DDL is `CREATE VECTOR INDEX ... OPTIONS(index_type='IVF' | 'TREE_AH')` — [BigQuery vector index docs](https://docs.cloud.google.com/bigquery/docs/vector-index)

### Inferences
- **Role in AI pipelines:** the lakehouse holds the curated, governed, versioned (time-travel) training and eval corpora, feature tables and LLM traces. Vector indexes and online feature stores are derived, rebuildable serving projections of lakehouse tables. Design for rebuild from source, not for the index as system of record.
- **Choice rule:** pick the warehouse or lakehouse you already run.
  - Databricks: Spark and ML-heavy teams, a Unity Catalog estate, and you want training, vector search, features and serving in one platform.
  - Snowflake: SQL-centric analytics teams adding LLM functions and Cortex Search over governed data.
  - BigQuery: GCP shops that want serverless SQL plus Vertex models. TreeAH makes BigQuery good for batch similarity jobs (dedup, clustering, batch RAG eval), but it is not a low-latency online vector store.
- Iceberg v3 plus REST catalogs make "one copy of data, many engines" realistic. The remaining lock-in is the catalog and governance layer, not the file format.

### Gaps
- No primary 2026 confirmation of Snowflake Cortex Search, Cortex AISQL or Snowflake Intelligence GA status (search budget exhausted).
- Delta Lake 4.x release details were not found.
- AWS S3 Tables pricing and limits, and SageMaker Lakehouse/Unified Studio, were not researched.
- BigQuery vector-index limits (max dims, rows, latency) were not retrieved; snippets were truncated.

---

## 4. Vector databases and search: ANN index internals, metrics, products, hybrid search, reranking, choosing

### Takeaway
ANN search trades recall for speed and memory:
- **HNSW (graph, in-RAM):** the default for low-latency high recall.
- **IVF (clustering) + PQ/SQ/binary quantization:** cuts memory.
- **DiskANN/Vamana and StreamingDiskANN, Elasticsearch DiskBBQ, Milvus tiered storage, S3 Vectors:** move most of the index to SSD or object storage.
Products in 2025–2026 have split into four groups:
1. **Object-storage-backed, cheap and cold:** S3 Vectors GA Dec 2025 (2B vectors/index, ~100 ms warm), Milvus/Zilliz tiered, Pinecone serverless.
2. **Dedicated or provisioned hot serving:** Pinecone Dedicated Read Nodes (GA Apr 2026), OpenSearch.
3. **"Vector in your existing DB":** pgvector/pgvectorscale, MongoDB, Elastic, BigQuery.
4. **Search platforms with built-in hybrid and reranking:** Vertex AI Vector Search 2.0 (GA Mar 2026), Azure AI Search, Elastic.
Hybrid BM25+vector with RRF fusion, then a cross-encoder reranker, is the standard RAG retrieval stack.

### Cited Findings
**ANN algorithms**
- **DiskANN/Vamana** (Subramanya et al., NeurIPS 2019): indexes and serves a billion points (100s of dims) on one workstation with 64 GB RAM at >95% 1-recall@1 and <5 ms latency. The Vamana graph has a smaller diameter than HNSW and NSG, which minimizes sequential SSD reads. The graph and full vectors stay on SSD, with PQ-compressed vectors in RAM. It matches or beats HNSW and NSG in memory, and serves 5–10x more points per node than graph methods like HNSW in the high-recall regime — [DiskANN paper PDF](https://www.cs.utexas.edu/~rak/papers/neurips19-diskann.pdf); [Microsoft Research](https://www.microsoft.com/en-us/research/publication/diskann/); [Zilliz explainer](https://zilliz.com/blog/diskann-a-disk-based-anns-solution-with-high-recall-and-high-qps-on-billion-scale-dataset)
- **ScaNN** uses anisotropic vector quantization, which weights the quantization error that matters for inner-product ranking. It underlies BigQuery TreeAH, Vertex AI Vector Search and AlloyDB ScaNN — [Google dev forum](https://discuss.google.dev/t/billion-scale-vector-search-in-gcp-the-mathematics-of-scann-hnsw-and-anisotropic-quantization/390848) [secondary]; [BigQuery docs](https://docs.cloud.google.com/bigquery/docs/vector-index); [BG] primary paper: [Guo et al., ICML 2020, arXiv:1908.10396](https://arxiv.org/abs/1908.10396)
- [BG] **HNSW** (Malkov & Yashunin, 2016/2018) is a multi-layer proximity graph searched greedily from sparse top layers down to the dense bottom layer. Key parameters are `M` (links per node), `efConstruction` (build beam) and `efSearch` (query beam; higher means more recall and more latency). Memory is roughly `4·d + 8·M` bytes per vector for float32 plus the graph. Deletes and updates cause graph degradation and need rebuilds or compaction — [arXiv:1603.09320](https://arxiv.org/abs/1603.09320); [hnswlib](https://github.com/nmslib/hnswlib)
- [BG] **IVF** partitions vectors with k-means into `nlist` cells and probes `nprobe` cells per query. It is commonly combined with **PQ** (Jégou et al., 2011): split the vector into m sub-vectors, quantize each to 256 centroids (1 byte), then compute distances with lookup tables (ADC). Example: 768-d float32 (3,072 B) becomes 96 B with m=96, a 32x reduction — [PQ paper (IEEE TPAMI 2011)](https://ieeexplore.ieee.org/document/5432202); [Faiss wiki](https://github.com/facebookresearch/faiss/wiki)
- [BG] **Distance metrics:** L2 (Euclidean), inner product (dot) and cosine. For L2-normalized vectors, cosine = dot product, and L2 ranking is equivalent (‖a−b‖² = 2 − 2a·b). Use the metric the embedding model was trained with, usually cosine or dot. Hamming distance applies to binary vectors.

**Amazon S3 Vectors**
- GA December 2, 2025:
  - Up to 2 billion vectors per index (40x the preview's 50M) and up to 10,000 indexes per vector bucket (≈20 trillion vectors per bucket).
  - Top-k up to 100 results per query, and up to 50 metadata keys per vector.
  - 14 regions, up from 5 in preview.
  - Pricing dimensions: PUT (logical GB uploaded), storage (logical GB) and queries.
  — [AWS What's New (es)](https://aws.amazon.com/es/about-aws/whats-new/2025/12/amazon-s3-vectors-generally-available/); [AWS News Blog](https://aws.amazon.com/blogs/aws/amazon-s3-vectors-now-generally-available-with-increased-scale-and-performance); [InfoQ Jan 2026](https://www.infoq.com/news/2026/01/aws-s3-vectors-ga); [HPCwire](https://www.hpcwire.com/bigdatawire/this-just-in/amazon-s3-vectors-now-generally-available-with-increased-scale-and-performance/)
- Performance and positioning:
  - Infrequent queries run "sub-second", and warm queries reach ~100 ms. A third party reports 100–300 ms on multi-million-vector indexes.
  - AWS claims up to 90% lower cost to upload, store and query vs alternatives [Vendor].
  - It is natively integrated with Bedrock Knowledge Bases.
  - AWS positions OpenSearch as the high-QPS, low-latency tier, with S3 Vectors for long-term or infrequent access, and documents a tiered pattern (S3 Vectors as storage, OpenSearch as hot tier).
  — [S3 Vectors feature page](https://aws.amazon.com/s3/features/vectors); [Classmethod](https://dev.classmethod.jp/en/articles/amazon-s3-vectors-ai-ready-storage/) [3P]
- Preview-era doc pages (e.g., "50 million vectors per index") are outdated — [S3 Vectors limitations (fr)](https://docs.aws.amazon.com/fr_fr/AmazonS3/latest/userguide/s3-vectors-limitations.html)

**Pinecone**
- Dedicated Read Nodes (DRN) went into public preview around December 2025 and GA on April 15, 2026. They provide resource isolation, guaranteed warm data and fixed hourly pricing for large or steady workloads, with a vendor claim of "up to 97% lower costs". Index fullness metrics for DRN were added August 21, 2026 — [Pinecone newsroom (ZoomInfo DRN)](https://pinecone.io/newsroom/zoominfo-pinecone-drn/); [futurecio](https://futurecio.tech/pinecone-unveils-dedicated-read-nodes); [Pinecone release notes 2026](https://docs.pinecone.io/marketplace-release-notes/2026.md); [PricingSaaS diff](https://pricingsaas.com/companies/pinecone/diffs/2025Q4) [3P]
- The "Dedicated" plan was renamed "Bring your own cloud" (BYOC) around January 2026: managed Pinecone in the customer's cloud with a zero-access operating model. One July 2026 review says it is in preview on AWS [3P] — [Pinecone pricing](https://www.pinecone.io/pricing/md/); [Dupple review](https://dupple.com/reviews/pinecone) [3P]
- [BG] Pinecone serverless (GA 2024) separates storage (object storage) from compute, with usage-based read units, write units and storage pricing.

**Postgres: pgvector and pgvectorscale**
- pgvector 0.8.x added iterative index scans. Without them, HNSW plus a selective `WHERE` filter can return fewer rows than `LIMIT`. Set `hnsw.iterative_scan = relaxed_order` (or `strict_order`) and tune `hnsw.max_scan_tuples`. Newer builds 0.8.2 and 0.8.5 exist. Guidance is to use `halfvec` (fp16) by default, at ~4–6 KB of HNSW index per 1536-d halfvec at m=16. `binary_quantize` gives ~32x memory reduction with rerank — [Timescale pg-aiguide pgvector skill](https://tessl.io/registry/skills/github/timescale/pg-aiguide/pgvector-semantic-search) [3P mirror]; [PGXN](https://pgxn.org/dist/vector)
  - Conflict: the [3P] guide says halfvec and binary_quantize need 0.8.0. My [BG] knowledge is that halfvec, bit/`binary_quantize` and sparsevec arrived in 0.7.0 (Apr 2024) and iterative scans in 0.8.0 (late 2024). Check the [pgvector CHANGELOG](https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md).
- [BG] pgvector HNSW and IVFFlat index limits: `vector` up to 2,000 dims, `halfvec` up to 4,000, `bit` up to 64,000, `sparsevec` up to 1,000 non-zeros. This is why 3072-d models (OpenAI text-embedding-3-large, Gemini embedding) are usually indexed as halfvec or truncated with Matryoshka — [pgvector README](https://github.com/pgvector/pgvector)
- pgvectorscale (Timescale/TigerData) adds a StreamingDiskANN index (disk-resident, DiskANN-inspired) plus Statistical Binary Quantization. Its 2024 vendor benchmark used 50M Cohere embeddings at 99% recall and reported 28x lower p95 latency and 16x higher QPS than Pinecone's storage-optimized s1 pod, at 75% lower cost self-hosted on EC2. One write-up reports 471 QPS at p95 28 ms vs Pinecone 784 ms [Vendor, 2024; Pinecone pod types since superseded by serverless] — [TigerData blog](https://www.tigerdata.com/blog/pgvector-is-now-as-fast-as-pinecone-at-75-less-cost); [Timescale pgvector vs Pinecone](https://www.timescale.com/blog/pgvector-vs-pinecone); [SoftwareSeni](https://www.softwareseni.com/pgvector-pgvectorscale-and-the-postgres-vector-search-stack-explained/) [3P]
- An independent-ish re-run at 50M × 1536-d and 99% recall got Postgres+pgvectorscale 471 QPS vs Qdrant 41 QPS, "with an asterisk big enough to change your architecture decision" (details paywalled) — [Towards AI (Medium)](https://pub.towardsai.net/i-benchmarked-pgvector-vs-qdrant-vs-pinecone-on-50m-vectors-postgres-crushed-the-dedicated-dbs-by-20aa6dcdf132) [3P]

**Milvus / Zilliz**
- Milvus 2.6 (June 12, 2025): hot/cold tiered storage (partners include MinIO, Pure, NetApp, Cohesity), int8 compression, direct writes to object storage instead of through Kafka (simpler WAL), geolocation types with spatial index, TIMESTAMPTZ, entity-level TTL, decay reranker and add-column schema changes — [BigDATAwire](https://www.bigdatawire.com/this-just-in/zilliz-releases-milvus-2-6-with-tiered-storage-and-int8-compression-to-cut-vector-search-costs); [Zilliz news](https://zilliz.com/news/milvus-2-6-built-for-scale-designed-to-reduce-costs); [Zilliz event](https://zilliz.com/event/milvus-2-6-deep-dive-faster-search-lower-cost-smarter-scaling)
- Milvus 2.6.x went GA on Zilliz Cloud (January 2026 report) with three-layer tiered storage, claiming up to 87% lower storage cost and up to 100x faster metadata filtering [Vendor] — [madri+d](https://ecosystem.madrimasd.org/news/feed/zilliz-launches-milvus-2-6-x-on-cloud-platform-cutting-storage-costs-by-87-1)

**Qdrant (Rust, open source)**
- 1.16: tiered multitenancy (small tenants share shards, large tenants are promoted to dedicated shards), ACORN filtered-search for multi-filter, low-selectivity queries, inline HNSW storage for disk-based search, conditional updates and `text_any` full-text — [Qdrant blog 1.16](https://qdrant.tech/blog/qdrant-1.16.x/index.md)
- 1.17 [3P summary]: Weighted RRF for hybrid ranking, relevance feedback, audit logs and RocksDB removal (gridstore). 1.18 [3P]: in-place vector schema updates and "TurboQuant" quantization. A 1.19 exists per the .NET client changelog — [skills.sh summary](https://skills.sh/itechmeat/llm-code/qdrant) [3P]; [blog](https://mohamedarbinsibi.onrender.com/posts/qdrant-118) [3P]; [qdrant-dotnet releases](https://github.com/qdrant/qdrant-dotnet/releases)

**Elastic / OpenSearch**
- Elasticsearch 9.2 (announced Oct 30, 2025) introduced **DiskBBQ**: BBQ-compressed vectors clustered into partitions read selectively from disk. It is a lower-RAM alternative to HNSW that performs well up to ~95% recall. For ≥99% recall use `bbq_hnsw`. BBQ is less accurate on <384-dim vectors, and `auto_calibrate` picks quantization and oversampling — [Elastic BBQ docs](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/bbq); [Business Wire](https://www.businesswire.com/news/home/20251030805965/en/Elastic-Introduces-New-Vector-Storage-Format-DiskBBQ-for-More-Efficient-Vector-Search); [SD Times](https://sdtimes.com/data/elastic-adds-new-vector-search-algorithm-that-cuts-down-on-memory-requirements-improves-speed/)
- OpenSearch: AWS positions the OpenSearch Service and Serverless vector engine as the hot, high-QPS tier over S3 Vectors — [S3 Vectors page](https://aws.amazon.com/s3/features/vectors)

**Google: Vertex AI Vector Search 2.0**
- GA announced March 5, 2026. Changes from v1:
  - "Collections" unify data and vectors, replacing the index-centric model.
  - Auto-embeddings.
  - Hybrid search with vector, full-text and built-in semantic re-ranking in one parallel query.
  - PSC, PGA and VPC-SC support.
  — [Vertex AI release notes](https://docs.cloud.google.com/vertex-ai/docs/release-notes); [Google dev forum intro](https://discuss.google.dev/t/introducing-vertex-ai-vector-search-2-0-from-zero-to-billion-scale/317931); [VS 2.0 overview](https://docs.cloud.google.com/vertex-ai/docs/vector-search-2/overview?hl=pt-br)

**Benchmarks**
- VectorDBBench (by Zilliz) is an open-source benchmark and cost-comparison tool with clients for Milvus, Qdrant, Pinecone, pgvector and others. I found no authoritative 2026 leaderboard. 2026 blog "benchmarks" disagree and use their own methods (one reports Qdrant leading latency and QPS at 1M and 10M vectors, Milvus ahead on hybrid) — [PyPI vectordb-bench](https://pypi.org/project/vectordb-bench/); [Ailog 2026](https://app.ailog.fr/en/blog/guides/vector-database-benchmark-2026) [3P]
- [BG] ANN-Benchmarks (Aumüller et al.) gives recall-vs-QPS curves for algorithms (HNSW, ScaNN, Faiss-IVF, DiskANN, etc.) on standard datasets (SIFT, GloVe, etc.), measuring libraries rather than managed services — [ann-benchmarks.com](https://ann-benchmarks.com)

**Hybrid search and reranking**
- Vertex Vector Search 2.0 natively fuses vector, full-text and semantic reranking. Qdrant 1.17 adds Weighted RRF. Milvus 2.6 adds a decay reranker — sources above.
- [BG] Reciprocal Rank Fusion (Cormack, Clarke & Büttcher, SIGIR 2009) scores each document as `score(d) = Σ_r 1/(k + rank_r(d))` with k ≈ 60. It is score-scale-free, so it fuses BM25 and cosine lists without normalization. It is implemented in Elasticsearch/OpenSearch, Azure AI Search, Weaviate, Qdrant and Milvus — [RRF paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- [BG] Typical pipeline: BM25 top-k plus vector top-k (e.g., 50–200 each), then RRF, then a cross-encoder reranker (Cohere Rerank, Voyage rerank, Jina, bge-reranker, Vertex or Azure semantic ranker) down to the top 5–20 for the LLM context. Rerankers add ~tens to hundreds of ms and per-query cost, but usually give the biggest precision gain per dollar.

### Inferences
- **Decision rules for choosing a vector store (2026):**
  1. **≤ ~10–50M vectors, already on Postgres, need transactional joins or filters:** pgvector (HNSW, halfvec, iterative scans), plus pgvectorscale or managed equivalents (AlloyDB ScaNN, Lakebase) as you grow.
  2. **Billions of vectors, low QPS, cost-dominated (archives, long-tail tenants, agent memory):** S3 Vectors, optionally fronted by OpenSearch for hot data. Expect ~100 ms+ latency and top-k ≤ 100.
  3. **Spiky or unpredictable RAG traffic, no ops team:** Pinecone serverless (or Zilliz Serverless, Qdrant Cloud). For steady high QPS, move to provisioned capacity (Pinecone DRN, dedicated clusters).
  4. **Self-hosted at large scale, need GPU indexing or many index types:** Milvus. Rust, filter-heavy and multi-tenant SaaS: Qdrant.
  5. **Need strong lexical search, analytics and filters already in Elastic or OpenSearch:** stay there (BBQ/DiskBBQ, RRF).
  6. **Data lives in the lakehouse or warehouse:** Databricks Vector Search, BigQuery VECTOR_SEARCH (batch) or Snowflake Cortex Search, which avoids sync pipelines.
  7. **Enterprise RAG on a single cloud with built-in hybrid and reranking:** Vertex AI Vector Search 2.0 or Azure AI Search.
- Filtered search is the most common production failure mode (fewer results than k, recall collapse with selective filters). Prefer engines with filter-aware traversal (pgvector iterative scans, Qdrant ACORN or payload indexes, Milvus/Elastic pre-filtering) and test with real filter selectivity.
- Vendor benchmarks (pgvectorscale vs Pinecone 2024, Pinecone DRN "97%", Zilliz "87%", AWS "90%") are not comparable with each other. Run VectorDBBench or your own recall@k-vs-p99-vs-$ test at your dims, filter selectivity and update rate.

### Gaps
- **Not researched (search budget exhausted):** Azure AI Search (2026 tiers, vector limits, agentic retrieval), MongoDB Atlas Vector Search (2026 features, Voyage AI integration, quantization), Weaviate (1.3x features, compression), LanceDB (Lance format, funding, multimodal lakehouse), turbopuffer, OpenSearch GPU-accelerated indexing and disk-mode details, Databricks Mosaic AI Vector Search limits, Cohere and Voyage reranker 2026 versions.
- S3 Vectors absolute pricing ($/GB storage, $/GB PUT, $/query), supported dims (my [BG] recollection is 1–4,096) and metrics (cosine, Euclidean) were not confirmed.
- Whether Milvus 2.6 ships RaBitQ (IVF_RABITQ) was not confirmed.
- No neutral 2026 VectorDBBench leaderboard was found.

---

## 5. Embeddings: dimensions, storage cost math, quantization (binary/int8), Matryoshka

### Takeaway
Raw float32 storage is `4 × d` bytes per vector: 6 KB for 1536-d and 12 KB for 3072-d. Memory-resident indexes multiply this by roughly 1.1–1.5x. int8 cuts storage 4x with ~2 points average quality loss. Binary cuts it 32x with ~6.5 points loss, recoverable by rescoring with full-precision vectors. Matryoshka (MRL) truncation cuts dimensions 2–6x with small loss. Combining them (truncate, then quantize, then rescore) yields 10–100x memory savings.

### Cited Findings
- int8 gives ~4x storage reduction and binary ~32x vs float32. Combining int8 with 256-d Matryoshka truncation gives 256 B per vector vs 2 KB for plain int8 at 2048-d — [MongoDB/Voyage docs: dimensions and quantization](https://www.mongodb.com/docs/voyageai/tutorials/dimensions-and-quantization/); [ZeroEntropy](https://www.zeroentropy.dev/concepts/embedding-quantization/) [3P]
- A neutral benchmark found average retrieval-quality deltas vs float of **binary −6.50** and **int8 −1.95** (micro-averaged across tasks) — [HAKARI-Bench, arXiv 2606.22778 (June 2026)](https://arxiv.org/pdf/2606.22778)
- Binary-first then rescore: Hamming-rank about a million candidates quickly, then re-score the top ~1,000 with float32 vectors — [Mixpeek guide](https://www.mixpeek.com/guides/embedding-quantization-compression) [Vendor]
- Voyage claims a 1024-d binary voyage-code-3 embedding nearly matches 2048-d float32 quality (code retrieval only) [Vendor] — [MongoDB blog on voyage-code-3](https://mongodb.com/company/blog/voyage-code-3-more-accurate-code-retrieval-lower-dimensional-quantized-embeddings); [W&B report](https://wandb.ai/byyoung3/ml-news/reports/Voyage-Code-3-Smarter-More-Efficient-Code-Retrieval-with-Nested-Embeddings---VmlldzoxMDkzNDg1NQ)
- Matryoshka truncation cost depends on the ratio to native dims. 512-d is a 50% cut of a 1024-d model but a 67% cut of a 768-d model, so compare ratios, not absolute sizes — [Towards Data Science: quantization vs Matryoshka for 80% cost reduction](https://v2.towardsdatascience.com/649627-2) [3P]
- Elastic notes BBQ (binary-style) loses more accuracy on <384-dim vectors — [Elastic BBQ docs](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/bbq)
- pgvector binary quantization (~32x) should be paired with re-ranking. halfvec halves storage with negligible loss — [pgvector skill guide](https://tessl.io/registry/skills/github/timescale/pg-aiguide/pgvector-semantic-search) [3P]
- [BG] Matryoshka Representation Learning (Kusupati et al., NeurIPS 2022) trains nested prefixes (e.g., 64/128/…/full) to each be usable embeddings. It is supported by OpenAI text-embedding-3 (`dimensions` parameter; 1536-d small, 3072-d large, Jan 2024), Gemini embedding (3072-d default; 1536/768 recommended truncations), Cohere Embed v4 (256–1536, with int8/binary output) and Voyage 3.x/4 (256–2048 with int8/binary) — [MRL arXiv:2205.13147](https://arxiv.org/abs/2205.13147); [OpenAI embeddings guide](https://platform.openai.com/docs/guides/embeddings)

### Inferences
**Storage math, raw vectors only (bytes = d × bytes/dim):**

| d | float32 | fp16/halfvec | int8 | binary |
|---|---|---|---|---|
| 768 | 3,072 B | 1,536 B | 768 B | 96 B |
| 1024 | 4,096 B | 2,048 B | 1,024 B | 128 B |
| 1536 | 6,144 B | 3,072 B | 1,536 B | 192 B |
| 3072 | 12,288 B | 6,144 B | 3,072 B | 384 B |

- 10M × 1536-d float32 ≈ 61 GB; int8 ≈ 15 GB; binary ≈ 1.9 GB. 100M × 1024-d float32 ≈ 410 GB; binary ≈ 13 GB. 1B × 768-d float32 ≈ 3.1 TB.
- HNSW adds roughly 8·M bytes per vector for layer-0 links (M=16 → ~128 B) plus upper layers and ids. For small d the graph can exceed the quantized vector size, so binary plus HNSW does not reach a full 32x saving.
- **Cost intuition:** RAM on cloud VMs costs dollars per GB-month, while object storage costs ~$0.02 per GB-month (S3 Standard [BG]). That is ~100x+ cheaper, which is the whole economic case for S3 Vectors, DiskANN-style and tiered designs. A 61 GB float32 index is fine in RAM. A 3 TB one pushes you to quantization plus disk or object-backed indexes.
- **Practical recipe:**
  1. Pick a model with MRL.
  2. Store full-precision vectors cheaply (object storage or a lakehouse column).
  3. Index a truncated plus int8 or binary version in RAM.
  4. Oversample (e.g., 3–10x k) and rescore with full-precision vectors, then rerank with a cross-encoder.
  5. Validate recall@k on your own data.
  Changing the embedding model requires a full re-embed and re-index, so keep source text and chunk metadata in the lakehouse.

### Gaps
- 2026 versions and native dimensions of the main embedding models (OpenAI, Gemini, Cohere, Voyage, open-weight models like Qwen3-Embedding) were not verified this session. Values above are [BG].
- No neutral study combining MRL truncation with binary quantization across MTEB-style tasks in 2026 was retrieved (HAKARI-Bench may contain it; the full text was not readable).

---

## 6. Feature stores (Feast, Tecton, Databricks, SageMaker, Vertex): online vs offline, point-in-time correctness

### Takeaway
A feature store keeps one feature definition and materializes it in two stores:
- **Offline store:** a warehouse or lakehouse holding full history, used for training sets built with point-in-time-correct "as-of" joins.
- **Online store:** low-latency key-value storage holding the latest value per entity, used at inference in ~single-digit ms.
The big 2025 event was Databricks acquiring Tecton (August 2025) to power real-time features for agents, alongside Lakebase (managed Postgres) as an online and operational store. Point-in-time correctness means joining each training label only with feature values whose timestamps are ≤ the label's event time. It prevents label leakage and train/serve skew.

### Cited Findings
- Databricks agreed to acquire Tecton (announced August 2025; Databricks was an existing investor). The deal is framed around real-time data serving for AI agents and Agent Bricks, and Tecton's online serving is cited at <10 ms latency. One outlet cites $900M, unconfirmed elsewhere — [Perficient](https://blogs.perficient.com/2025/09/26/databricks-acquires-tecton/); [IT Daily](https://itdaily.com/news/business/databricks-acquires-tecton-to-improve-real-time-data-delivery-for-ai-agents); [MIT Sloan ME](https://www.mitsloanme.com/article/databricks-to-buy-enterprise-feature-store-tecton/); [Dealroom ($900M)](https://ai-startups.dealroom.co/news/feed/databricks-acquires-tecton-for-900m) [unverified figure]
- Tecton's core use cases are fraud detection, risk scoring and personalization — [MIT Sloan ME](https://www.mitsloanme.com/article/databricks-to-buy-enterprise-feature-store-tecton/)
- Databricks Lakebase (Postgres, Neon-based) integrates with feature management and model serving — [Lakebase docs](https://docs.databricks.com/aws/oltp)
- [BG] **Feast** (open source, Apache-2.0): pluggable offline stores (BigQuery, Snowflake, Redshift, Spark, files) and online stores (Redis, DynamoDB, Bigtable, Postgres, etc.). `get_historical_features()` performs point-in-time joins using entity timestamps and feature TTLs. `materialize` / `materialize-incremental` push the latest values to the online store, and `get_online_features()` reads at inference — [Feast docs](https://docs.feast.dev/)
- [BG] **SageMaker Feature Store:** feature groups with an online store (low-latency; standard or in-memory tier) and an offline store in S3 (Glue catalog; Iceberg table format option). Time-travel queries go through Athena — [SageMaker Feature Store docs](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html)
- [BG] **Vertex AI Feature Store** (re-architected 2023–2024): BigQuery tables or views are the offline source of truth, and online serving runs on Bigtable-based or "Optimized" online stores. It supports embeddings for vector retrieval. The legacy Feature Store is deprecated — [Vertex AI Feature Store docs](https://cloud.google.com/vertex-ai/docs/featurestore/latest/overview)
- [BG] **Databricks Feature Engineering in Unity Catalog:** any UC Delta table with a primary key can be a feature table. Time-series feature tables use a `timestamp_keys` lookup for point-in-time joins in `create_training_set`. Online serving uses online tables or Lakebase-backed stores — [Databricks feature engineering docs](https://docs.databricks.com/aws/machine-learning/feature-store/)

### Inferences
- **Point-in-time join, concrete form:** for each (entity_id, label_timestamp) row, choose the latest feature row with `feature_ts ≤ label_timestamp` (and optionally `≥ label_timestamp − TTL`). This is an as-of join (`ASOF JOIN` in DuckDB, Snowflake and ClickHouse; window plus filter in Spark). A naive join on entity_id leaks future information.
- **Decision rule:**
  - Already on Databricks: use UC feature tables, plus Tecton-derived real-time capabilities as they ship.
  - GCP/BigQuery shop: Vertex Feature Store (BigQuery offline).
  - AWS/SageMaker shop: SageMaker Feature Store.
  - Multi-cloud or open source: Feast on your warehouse plus Redis or DynamoDB.
  - Streaming or real-time aggregations (fraud, sliding windows): you need a streaming engine (Flink, Spark Structured Streaming, Tecton) writing to the online store (see Q8).
- In LLM and agent systems, "features" increasingly means user, session and context facts injected into prompts or tools, served from the same online stores (Postgres/Lakebase, Redis, DynamoDB) with the same freshness and point-in-time concerns for offline evaluation.

### Gaps
- No 2026 primary source was obtained on post-acquisition Tecton product status (e.g., whether Tecton is now a Databricks-native feature) or on Feast's 2026 release level. Search budget exhausted.
- SageMaker and Vertex Feature Store 2026 changes were not verified.

---

## 7. Dataset versioning and lineage (DVC, lakeFS, Delta time travel, Hugging Face datasets) and data quality checks

### Takeaway
There are three layers of data versioning:
1. **File or repo-level:** DVC (git-like pointers to objects in S3/GCS) and Hugging Face Hub datasets (git-based, Xet storage). Suits small-to-mid ML datasets and reproducibility.
2. **Data-lake-level branching:** lakeFS, which provides zero-copy branches and commits over object storage and now also stewards DVC after acquiring it in November 2025.
3. **Table-level:** Delta, Iceberg and Hudi snapshots and time travel, with default 7-day file and 30-day log retention on Delta.
Lineage comes from catalogs (Unity Catalog, Polaris/Open Catalog, Dataplex, Purview) and OpenLineage. Quality comes from expectation frameworks run as pipeline gates.

### Cited Findings
- lakeFS (Treeverse) acquired the DVC open-source project from Iterative.ai, announced November 18, 2025. DVC remains a separate open-source tool (dvc.org) aimed at data scientists with smaller datasets, while lakeFS focuses on enterprise-scale data version control. lakeFS raised $20M in July 2025 — [lakeFS blog](https://lakefs.io/blog/lakefs-acquires-dvc/); [DVC FAQ](https://dvc.org/blog/dvc-joins-lakefs-your-questions-answered/); [Techleap](https://finder.techleap.nl/news/feed/lakefs-acquires-dvc-raises-20m)
- Delta time travel retention: `delta.deletedFileRetentionDuration` (default 7 days, governs VACUUM) and `delta.logRetentionDuration` (default 30 days). Both must cover the desired lookback — [Databricks VACUUM docs](https://docs.databricks.com/aws/sql/language-manual/delta-vacuum); [Substack](https://mbvyn.substack.com/p/understanding-databricks-time-travel) [3P]
- Iceberg v3 row lineage (`_row_id`, `_last_updated_sequence_number`) gives row-level change tracking for CDC and incremental pipelines. No historical backfill happens on upgrade — [Google OSS blog](https://opensource.googleblog.com/2025/08/whats-new-in-iceberg-v3.html?m=0); [AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/working-with-apache-iceberg-v3.md)
- [BG] Hugging Face Hub datasets are git repos with large files in Xet storage (HF acquired XetHub in 2024 and migrated from Git LFS to Xet chunk-level dedup in 2025). The `datasets` library supports `streaming=True` and `revision=` for pinned versions, and Parquet auto-conversion enables the Dataset Viewer and SQL — [HF Datasets docs](https://huggingface.co/docs/datasets); [HF Xet docs](https://huggingface.co/docs/hub/storage-backends)
- [BG] Data-quality tooling: Great Expectations / GX Core (expectations suites), AWS Deequ / PyDeequ (Spark, used by Glue Data Quality), Soda, dbt tests, and Databricks Lakeflow Declarative Pipelines (formerly DLT) "expectations" (warn, drop or fail). OpenLineage/Marquez provides lineage events — [Great Expectations](https://greatexpectations.io/); [Deequ](https://github.com/awslabs/deequ); [OpenLineage](https://openlineage.io/)

### Inferences
- **Decision rule:**
  - Notebook or project-scale datasets (GBs to low TBs) with git-centric workflows: DVC or the HF Hub.
  - Data lakes where many jobs write to object storage and you need branch, test and merge plus atomic rollback: lakeFS.
  - Tabular or feature data in a lakehouse: rely on Delta or Iceberg snapshots. Pin training runs to a table version or snapshot id (`VERSION AS OF` / `TIMESTAMP AS OF`), and set retention long enough for audit and reproducibility (default 7 days is too short for ML reproducibility).
- **Reproducibility minimum:** for every model, record the dataset snapshot id or commit, code commit, tokenizer and preprocessing version, and embedding model version. Store these in the model registry (MLflow or UC models) or lineage system.
- **Data quality gates for AI:** schema checks, null and duplicate rates, PII detection, near-duplicate and contamination checks against eval sets, label distribution drift, and freshness SLAs for RAG sources. Fail the pipeline before materializing to training sets, feature stores or vector indexes.

### Gaps
- 2026 state of DVC under lakeFS (releases, roadmap) and lakeFS feature specifics (e.g., Iceberg REST catalog support) were not retrieved.
- HF Hub Xet migration details and storage limits for 2026 were not verified.
- No 2026 survey comparing data-quality frameworks was found.

---

## 8. Streaming ingestion (Kafka/Confluent, Kinesis, Pub/Sub, Flink) for real-time features and RAG index freshness

### Takeaway
Streaming is the path from operational change to fresh features and fresh RAG indexes. The pattern runs:
1. A change event (CDC via Debezium or DMS, or app events) goes to a log (Kafka/Confluent, MSK, Kinesis, Pub/Sub, Event Hubs).
2. A stream processor (Flink, Spark Structured Streaming) computes aggregates or chunks and embeds documents.
3. Results are upserted to the online feature store or vector DB, and also landed in Iceberg or Delta for offline and training use.
The biggest 2025–2026 industry event is IBM's ~$11B acquisition of Confluent (announced December 2025, reportedly closed March 2026).

### Cited Findings
- IBM agreed to acquire Confluent for $31 per share in cash, about $11B enterprise value (one filing summary says $11.5B). It was announced December 8, 2025, with closing expected by mid-2026 subject to shareholder and regulatory approval. Holders of ~62% of voting power signed support agreements. One source reports the deal closed March 17, 2026 (not corroborated) — [MarketScreener](https://www.marketscreener.com/news/international-business-machines-corporation-entered-into-a-definitive-agreement-to-acquire-confluent-ce7d51d2d988f220); [Bloomberg via scour](https://scour.ing/@emschwartz/p/https://www.bloomberg.com/news/articles/2025-12-08/ibm-close-to-buying-confluent-in-11-billion-deal-wsj-says); [Pulse 2.0](https://pulse2.com/ibm-buying-confluent-in-11-billion-deal/); [Let's Data Science (close date)](https://letsdatascience.com/news/ibm-acquires-confluent-for-11-billion-17ed712a) [single source]
- Milvus 2.6 removed Kafka from its write path in favor of writing directly to object storage (MinIO quote), part of a broader "object-storage-native WAL" trend — [BigDATAwire](https://www.bigdatawire.com/this-just-in/zilliz-releases-milvus-2-6-with-tiered-storage-and-int8-compression-to-cut-vector-search-costs); [Arpit Bhayani notes on S3 stateless WAL](https://arpitbhayani.me/notes/how-s3-enables-stateless-write-ahead-logs-despite-latency-trade-offs) [3P]
- GCS Rapid supports streaming appendable objects, useful for logs and streaming checkpoint writes — [GCS Rapid docs](https://docs.cloud.google.com/storage/docs/rapid/high-performance-storage)
- [BG] Kafka 4.0 (March 2025) removed ZooKeeper entirely (KRaft only) and added the new consumer-group rebalance protocol (KIP-848) and early access to "queues for Kafka" (KIP-932). Confluent **Tableflow** materializes Kafka topics as Iceberg or Delta tables in object storage. Confluent Cloud offers managed Flink — [Apache Kafka 4.0 release](https://kafka.apache.org/blog); [Confluent Tableflow docs](https://docs.confluent.io/cloud/current/topics/tableflow/overview.html)
- [BG] AWS options: Kinesis Data Streams (shards: 1 MB/s or 1,000 records/s in, 2 MB/s out per shard; on-demand mode), Amazon MSK (provisioned, Serverless, and Express brokers since Nov 2024), Amazon Managed Service for Apache Flink, and Firehose (delivers to S3, Redshift, OpenSearch, and Iceberg tables) — [Kinesis quotas](https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html); [MSK Express brokers](https://aws.amazon.com/msk/)
- [BG] GCP options: Pub/Sub (global, at-least-once with exactly-once delivery option; BigQuery and Cloud Storage subscriptions write directly without Dataflow) and Dataflow (Apache Beam) / Managed Service for Apache Kafka (GA 2024–2025). Azure: Event Hubs (Kafka-compatible endpoint) and Stream Analytics / Fabric Real-Time Intelligence — [Pub/Sub BigQuery subscriptions](https://cloud.google.com/pubsub/docs/bigquery); [Event Hubs for Kafka](https://learn.microsoft.com/azure/event-hubs/azure-event-hubs-kafka-overview)

### Inferences
- **RAG index freshness pattern:**
  1. Capture document changes with CDC or events, keyed by doc_id plus version.
  2. In the stream processor: chunk, then embed (batch micro-batches to the embedding API, with rate limiting and retry), then upsert chunks keyed by `doc_id#chunk_n`, deleting stale chunks of the previous version.
  3. Also append to an Iceberg or Delta "chunks" table, which serves as rebuild source and audit.
  Freshness SLOs are typically seconds to minutes. Use full nightly or weekly rebuilds to repair drift and handle embedding-model upgrades.
- **Real-time features:** windowed aggregations (count of transactions in the last 5 min) belong in Flink or Spark streaming with event-time semantics and watermarks, written to the online store and logged offline with the same definitions. This avoids train/serve skew.
- **Choice rule:**
  - Already on a cloud and want minimal ops: Kinesis (AWS) / Pub/Sub (GCP) / Event Hubs (Azure).
  - Need the Kafka ecosystem (Connect, Debezium, multi-cloud, Tableflow to Iceberg): Confluent Cloud or MSK / Google Managed Kafka.
  - Complex stateful logic: Flink.
  - Watch IBM-Confluent integration for roadmap and pricing changes (inference; no source on post-close changes).

### Gaps
- None of the Kinesis, Pub/Sub, Flink or Tableflow 2026 facts were verified this session (search budget exhausted). All are [BG].
- The IBM-Confluent close date has only one source.
- No sourced measurements of end-to-end RAG freshness latency in production systems were found.

---

## 9. Data governance basics: PII handling and data residency

### Takeaway
For AI data, governance means:
- Discovering and classifying PII before it enters training sets, feature stores or vector indexes. Embeddings and chunk text are personal data if the source was.
- Enforcing fine-grained access (row and column masking, ABAC) in the catalog.
- Supporting deletion ("right to be forgotten") across derived copies: snapshots, indexes, fine-tuned models.
- Pinning data to regions for residency or sovereignty.
The regulatory backdrop in 2026 includes the EU Data Act (applies from Sept 2025; switching charges to zero by 2027), plus hyperscaler exit-egress waivers.

### Cited Findings
- EU Data Act cloud-switching rules: providers were forced to change data-transfer and switching terms ("big clouds scramble"). Switching charges are to be abolished (dates conflict across 3P sources: 12 Jan 2027 vs 12 Sept 2027). The waiver covers leaving, not routine serving egress — [The Register, Sept 2025](https://www.theregister.com/2025/09/10/big_clouds_scramble_over_eu/); [sota.io](https://sota.io/blog/eu-data-act-2025-cloud-switching-rights-developer-guide) [3P]; [cloudmagazin](https://www.cloudmagazin.com/2026/08/02/cloud-egress-free-tiers-exit-waiver-stille-kosten/) [3P]
- Microsoft waived Azure egress fees for customers leaving Azure — [Computerwoche](https://www.computerwoche.de/article/2833087/microsoft-erlaesst-azure-kunden-egress-kosten.html)
- AWS documentation exists for the AWS European Sovereign Cloud (docs.aws.eu domain, including FSx for Lustre pages), showing a separate EU sovereign partition — [FSx Lustre docs on docs.aws.eu](https://docs.aws.eu/fsx/latest/LustreGuide/using-fsx-lustre.html)
- Vertex AI Vector Search 2.0 supports VPC Service Controls, Private Service Connect and Private Google Access for data exfiltration controls — [Vertex AI release notes](https://docs.cloud.google.com/vertex-ai/docs/release-notes)
- Pinecone BYOC uses a "zero-access operating model" (vector data stays in the customer's cloud account), a residency and sovereignty option for managed vector DBs — [Pinecone pricing](https://www.pinecone.io/pricing/md/)
- [BG] PII discovery and classification services:
  - Amazon Macie (S3).
  - Google Sensitive Data Protection (formerly Cloud DLP; inspection plus de-identification such as masking, tokenization and format-preserving encryption).
  - Microsoft Purview (classification, sensitivity labels, DLP).
  - Databricks Unity Catalog (tags, row filters, column masks, ABAC, data classification).
  - Snowflake (tag-based masking policies, row access policies, auto-classification).
  - Bedrock Guardrails / Azure AI Content Safety / Vertex for PII filtering at inference.
  — [Amazon Macie](https://aws.amazon.com/macie/); [Google SDP](https://cloud.google.com/sensitive-data-protection/docs); [Microsoft Purview](https://learn.microsoft.com/purview/)
- [BG] Residency mechanisms: region-pinned buckets and indexes, org policies (GCP resource location constraint, Azure Policy allowed locations, AWS SCPs denying regions), Microsoft EU Data Boundary, Google Sovereign Cloud / Assured Workloads, the AWS European Sovereign Cloud (Brandenburg, launch planned for late 2025, verify status), and customer-managed keys (KMS/CMEK/HSM) — [AWS European Sovereign Cloud](https://aws.eu/); [Google Assured Workloads](https://cloud.google.com/assured-workloads/docs)

### Inferences
- **PII pipeline for AI:**
  1. Classify at ingestion with Macie, SDP or Purview scans and catalog tags.
  2. Redact or tokenize before chunking and embedding, or before inclusion in training corpora.
  3. Keep a mapping table only in a restricted zone if re-identification is needed.
  4. Propagate tags through lineage so vector indexes and feature tables inherit sensitivity.
  5. Enforce filters at retrieval (per-user ACL metadata filters in the vector DB). Otherwise, RAG can leak documents users are not entitled to.
- **Deletion requests are hard in AI stacks.** You must delete from:
  - source tables (then VACUUM or expire snapshots after the retention window: 7 days default on Delta, configurable),
  - vector indexes (by doc_id), and feature stores,
  - backups,
  - and possibly fine-tuned weights, which is practically infeasible. Hence "don't train on raw PII" is the safest rule.
  Time travel and long retention help reproducibility (Q7) but conflict with erasure obligations, so set retention deliberately.
- Residency applies to derived data too. Embeddings, caches (Anywhere Cache, Lustre), logs and LLM prompts and traces sent to model APIs in other regions can each break residency. Check where managed embedding and reranking endpoints process data.

### Gaps
- No primary 2026 sources were gathered on Macie, Sensitive Data Protection or Purview capabilities, Unity Catalog ABAC GA status, the AWS European Sovereign Cloud launch status, or EU AI Act data-governance obligations (Art. 10, training-data requirements), because the search budget was exhausted. All of these are [BG] and need verification.
- The exact EU Data Act zero-switching-charge date is unresolved (conflicting secondary sources).
