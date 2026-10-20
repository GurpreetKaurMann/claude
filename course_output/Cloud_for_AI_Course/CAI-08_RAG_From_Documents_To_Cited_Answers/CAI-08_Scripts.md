# CAI-08 · RAG, Tested: Scripts

**Lesson 8 of 12 · Module 4 · Shipping it**

Voice: AI narrator (Kokoro `af_heart`). Final lesson video length: 16:52.

## Long video narration

**[RAG, honestly tested]**

> I tested retrieval on my own notes. Forty-five thousand words, twenty-four questions I wrote myself, and three ways to search. With the right chunk size, the answer sat in the top three results ninety-two percent of the time. With the wrong one, seventy-nine.

> And the fancy fusion method that every guide recommends did not win in my test. This lesson explains how R A G works, and shows what a real test actually says, including the parts that did not go to plan.

**[Intro]**

> Welcome to lesson eight of the cloud for A I engineers course, on The Code Notebook.

> The handwritten notes and the code for this lesson are linked in the description.

**[Where we are]**

> We now have the cloud pieces. Chips, containers, data, training, serving and shipping. From here we build the applications on top, starting with the most common one, retrieval augmented generation, called R A G.

> A note on honesty before we start. The search test uses the text of my own notebook, and questions I wrote by hand. The vector side uses a stand in, because no embedding model could be downloaded on my machine. I will label it every time.

**[Why RAG exists]**

> Why does R A G exist? A language model only knows what was in its training data. It does not know your company's documents, today's prices, or last week's policy. And if you ask anyway, it may confidently invent an answer.

> R A G fixes this like an open book exam. When a question arrives, you first look up the relevant pages, and put them in the prompt. The model then answers from those pages, ideally quoting them.

**[The seven steps]**

> A real R A G pipeline has seven steps. Parse the files. Chunk them into pieces. Add context to each piece. Embed the pieces as vectors.

> Then, at question time, search with both keywords and vectors. Rerank the results so the best come first.

> And finally generate an answer with citations. The mnemonic is pretty cats can eat hot red grapes, for parse, chunk, context, embed, hybrid, rerank, generate.

**[Parse]**

> Step one, parse. Turn files into clean text. This is where many projects quietly go wrong. A table flattened into a line of words can turn a column of prices into nonsense, and your answers will quote the wrong number with total confidence.

> Use a parser that understands layout, and keep metadata with every chunk. The source, the date, the tenant and who may read it. You will need that metadata for filters later.

**[Chunk]**

> Step two, chunk. A whole document is too big to search well, so cut it into pieces. The rule of thumb is three hundred to eight hundred tokens, with some overlap so a sentence is not cut in half.

> Common ways: fixed windows, splitting at paragraphs and sentences, splitting where the topic changes, or keeping small child chunks but returning their larger parent. I tested window size myself, so let us see what the numbers say.

**[Embed]**

> Step four, embed. An embedding model turns each chunk into a vector, so similar meanings sit close together. You embed the chunks once, offline. At question time you embed the question and find the nearest chunks.

> Cache embeddings by the hash of the text, so unchanged chunks are never paid for twice. And always record which embedding model made them. Mixing two models in one index quietly ruins search.

**[Smaller vectors]**

> A tip that connects to lesson four. Vectors cost memory, so shrink them. Some embedding models are trained so that you can simply cut off the end of each vector and keep working, losing a little quality gracefully. They are called Matryoshka vectors, after the nested Russian dolls.

> Combine that with half size or one byte numbers, and a large index can fit in a fraction of the memory. Always check recall on your own questions after shrinking anything.

**[Hybrid search]**

> Step five, hybrid search. Vectors are good at meaning. A question phrased differently from the document still finds it. But vectors are weak at exact things, like an error code, a product number or a name.

> Keyword search, called B M twenty-five, is the opposite. Exact terms win, paraphrases lose. So run both, and merge the two lists.

**[Fusing the lists]**

> How do you merge two lists whose scores mean different things? The popular answer is reciprocal rank fusion. Ignore the scores and use only the ranks. Each list gives a document one over sixty plus its rank.

> A document that is first in the vector list and third in the keyword list scores one over sixty-one plus one over sixty-three, about point oh three two three. A document found by only one list scores about point oh one six. Found by both wins.

**[Rewrite the question]**

> A small trick before searching. Users write short, vague questions, so rewrite them. One method asks the model to write a hypothetical answer and searches with that, because answer shaped text is closer to answer documents.

> Another splits a complex question into several smaller ones, searches for each in parallel, and merges. It costs one extra model call, so it adds a little latency. Use it when questions are genuinely multi part.

**[Keeping the index fresh]**

> Documents change, and a stale index gives stale answers. Connect the index to your storage, so a changed file is parsed and embedded again, and a deleted file's chunks are removed. Hash each chunk's text, so you only pay to embed what actually changed.

> Also store the date with each chunk, and decide what should win when two versions disagree. A search that returns last year's policy next to this year's is worse than no search.

**[Rerank]**

> Step six, rerank. Retrieve a generous number, say a hundred and fifty, then use a slower, smarter model that reads the question and each candidate together, and keep the best twenty. Managed rerankers exist on every big cloud.

> Tune the final number. Twenty beat ten and five in the notebook's reading. But stuffing too many passages backfires, because models notice the start and end of a long prompt more than the middle.

**[Answer with citations]**

> Step seven, generate. Give each chunk an I D. Tell the model to answer only from the sources, to cite the I Ds, and to say not found if the answer is absent. That last instruction matters. Without it, the model fills gaps with guesses.

> Some model providers offer a citations feature that returns the exact quoted spans. Either way, users should be able to click from an answer to its source.

**[My test setup]**

> Now my test. The corpus is the text of this course's notebook, about forty-five thousand words. I wrote twenty-four questions, such as, how long does S three take to auto partition after a load spike, and for each, the exact phrase that answers it.

> A chunk counts as a hit if it contains that phrase. Hit at three means the answer is somewhere in the top three chunks. I compared keyword search, a stand in for vectors built from word statistics, and the fusion of both. The stand in is not a neural embedding model.

**[Chunk size, measured]**

> First, chunk size. With hundred word chunks, keyword search found the answer in the top three eighty-three percent of the time. With three hundred words, eighty-seven and a half. With eight hundred, seventy-nine.

> The vector stand in followed the same shape. Eighty-three, ninety-two, eighty-eight. Three hundred words was best for both.

**[Why the middle wins]**

> Why does the middle win? Chunks that are too small lose their surroundings. A line like k equals sixty means little without the sentence around it.

> Chunks that are too big dilute the match, because one long chunk holds many topics and ranks well for none of them. That agrees with the three to eight hundred token rule. The exact best size depends on your documents, so test it.

**[The fusion surprise]**

> Now the surprise. With three hundred word chunks, keyword search got eighty-seven and a half percent. The vector stand in, ninety-one point seven. And the fusion of both, eighty-seven and a half.

> I expected the fusion to win. It did not.

> It matched keyword search and trailed the vector stand in. Honest result, from a small test.

**[Why fusion did not help]**

> Why? I counted who found what. Twenty-one of the twenty-four questions were found by both methods. Nothing was found only by keywords. One was found only by the vectors. And two were missed by both.

> Fusion helps when the two methods fail on different questions. On my corpus, the two mostly agree, so there is little for fusion to add. Your documents may differ. Codes and names favour keywords.

**[The two misses]**

> The two questions both missed are instructive. How much notice does A W S give for a spot instance. And what value of k does reciprocal rank fusion use.

> The first is about spot instances, a word that appears in many chunks across the notebook, so dozens of chunks compete. The second has an answer made of symbols, k equals sixty, which my keyword tokenizer throws away. Reading failures like this is called error analysis, and it tells you what to fix next.

**[A small test, honestly]**

> A caution about my own test. Twenty-four questions is small. Each question is worth four point two percentage points, so differences of one question are noise. I trust the pattern, three hundred words beating eight hundred, more than any single gap.

> The point is not that fusion is bad. The notebook cites larger benchmarks where hybrid search helps. The point is to build an eval set of your own, because it takes an afternoon and tells you what really works on your documents.

**[Does context help?]**

> Next, an idea called contextual retrieval. Before indexing, ask a model to write one or two sentences placing each chunk in its document, and prepend them. The original study reported that this, with reranking, cut failed retrievals by sixty-seven percent.

> I tried the cheapest possible version. I just prepended the topic title to each hundred word chunk. Keyword search did not change. The vector stand in went from eighty-three to eighty-seven and a half, one question. A title is very weak context.

**[What I did not test]**

> I could not run the real method, which uses a language model to write each chunk's context. So I cannot confirm sixty-seven percent. That figure comes from the original study, described in the notebook. What I can say is that a plain title is not enough.

> The real method is affordable, about one dollar per million document tokens, once, using prompt caching. If your search quality matters, it is among the first things worth trying.

**[Seven ways it fails]**

> Researchers listed seven ways R A G systems fail. Missing content, so the answer is not in the data. The right document is not ranked high enough. It was found but dropped before the prompt.

> It is in the prompt but the model ignores it. The format is wrong. The answer is too vague. Or it is incomplete. Each failure has a different fix, and only an eval set tells you which one you have.

**[Do you need RAG at all?]**

> Do you even need R A G? If your whole knowledge base is under about two hundred thousand tokens, roughly five hundred pages, and it rarely changes, and has one owner, you can put all of it in the prompt and cache it.

> Caching can give more than twice the speed and up to ninety percent lower cost, according to vendors. If it is larger, changing, permissioned, or shared by many tenants, use R A G. Cost per question grows with context, and models miss things in the middle.

**[Permissions]**

> Permissions deserve their own warning. If your documents have different owners, every chunk carries a list of who may read it, and the search must filter by the asking user. Retrieving first and filtering afterwards is not good enough.

> A missing filter means one customer's data appears in another customer's answer. That is the most serious R A G bug there is, and it is caused by metadata, not by the model.

**[Retrieved text is untrusted]**

> One more warning, which lesson ten covers in full. Text you retrieve is not your instructions. A document can contain sentences written to hijack the model. Treat retrieved text as data, never as commands.

> For now, remember to keep the instruction part of the prompt separate from the retrieved part, and never let retrieved text grant the model new powers.

**[Evaluating RAG]**

> How do you know a change helped? Keep a labelled set of questions, with the source passage that answers each. Measure whether the right passage is retrieved, called recall at k, separately from whether the final answer is right.

> Track both on every release. Retrieval failures and answer failures need different fixes, and mixing them makes debugging a guessing game.

**[Beyond plain RAG]**

> Two advanced ideas to know by name. Graph R A G builds a graph of entities from your documents and answers big picture questions like, what are the main themes. It beats plain R A G on those. For pinpoint facts, hybrid search with reranking is enough.

> Agentic R A G lets the model plan searches, pick sources and iterate. Better for multi step questions, but more calls and more cost. Both are extras. Get the basics measured first.

**[Managed services]**

> Every big cloud sells managed R A G. Amazon Bedrock Knowledge Bases, Google's R A G Engine, Azure A I Search with Foundry I Q, and OpenAI's file search. They handle ingestion, chunking, embedding, storage, retrieval and grounded answers, and all offer a retrieve only call.

> Pick by where your data and your identity already live. SharePoint and Entra point to Azure. S three points to Bedrock. Google storage and BigQuery point to Google. Minimal operations points to OpenAI, though your data leaves your cloud.

**[ShopNest Copilot]**

> For ShopNest Copilot. Parse the help articles and policies, chunk at about three hundred words with overlap, store the source and access level with each chunk, and embed once with a recorded model version.

> Search with keywords and vectors, rerank, answer with citations and a not found rule, and filter by customer. Then build a forty question eval set from real tickets, and measure recall before touching anything fancy.

**[Four words to keep]**

> Four words to carry forward. Chunk: a piece of a document, sized for search. Hybrid search: keywords and vectors together.

> Rerank: sorting the shortlist with a smarter model. And hit at k: the share of questions whose answer appears in the top k results.

**[Interview corner]**

> Interview corner. Asked how you choose chunk size, say: start around three hundred to eight hundred tokens with overlap, then measure on your own questions. In my test, three hundred words found the answer in the top three ninety-two percent of the time, against seventy-nine for eight hundred.

> Asked why hybrid search, say: vectors catch paraphrases and keywords catch exact terms, merged by reciprocal rank fusion. But verify on your data. In my test, fusion did not beat the vector stand in, because the two methods failed on the same questions.

**[Your turn]**

> Your turn. The zip for this lesson has two scripts and the notebook text. Run the evaluation. Then replace my questions with your own, from your own documents, and see which chunk size wins for you.

> Add a question whose answer is an error code, and watch which method finds it. One changed question teaches more than an hour of reading.

**[Recap]**

> Recap. R A G is an open book exam in seven steps, parse, chunk, context, embed, hybrid, rerank, generate. On my test, three hundred word chunks found the answer in the top three ninety-two percent of the time, and eight hundred, seventy-nine.

> Fusion did not win, because both methods failed on the same questions, and a title prefix barely helped. Filter by user, treat retrieved text as data, and build your own eval set. Next lesson: agents, tools and reliability.

**[Next lesson]**

> In the next lesson: agents, tools and reliability. Loops, protocols, retries and sandboxes.

> Subscribe so you don't miss it. See you in the notebook.


## Short 1: RAG Chunk Size: 300 Words Beat 800 in My Test (24 Questions) #shorts

> The right chunk size for R A G found the answer ninety-two percent of the time. The wrong one, seventy-nine.

> I searched my own forty-five thousand word notebook with twenty-four questions I wrote. A chunk is a hit if it contains the answer. With three hundred word chunks, the answer was in the top three ninety-two percent of the time.

> With eight hundred word chunks, eighty-eight. With keyword search, eighty-seven and a half against seventy-nine. The vector side is a stand in, so test your own.

> Test chunk sizes on your own questions.


## Short 2: Hybrid Search Didn't Win in My RAG Test (Here's Why) #shorts

> Everyone says to use hybrid search with fusion. In my test it did not win. Here is why.

> With three hundred word chunks, the vector stand in found the answer in the top three ninety-two percent of the time. Keywords, eighty-seven and a half. Fusing both, eighty-seven and a half.

> I counted why. Twenty-one of twenty-four questions were found by both methods, so fusion had little to add. It helps when the methods fail on different questions.

> Verify hybrid search on your own data.


## Instagram Reel 1: When you can skip RAG completely

> When you can skip R A G completely.

> If your whole knowledge base is under about two hundred thousand tokens, roughly five hundred pages, stable, and has one owner, put all of it in the prompt and cache it. Vendors report over twice the speed and up to ninety percent lower cost.

> Bigger, changing or permissioned? Use R A G. Save this.
