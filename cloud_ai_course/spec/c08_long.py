import sys; sys.path.insert(0, '/home/claude/caigen')
from frag import *
from gailab import CODE, OUT

LONG = [
 dict(id='s0', chap='RAG, honestly tested', say=[
   "I tested retrieval on my own notes. Forty-five thousand words, twenty-four questions I wrote myself, and three ways to search. With the right chunk size, the answer sat in the top three results ninety-two percent of the time. With the wrong one, seventy-nine.",
   "And the fancy fusion method that every guide recommends did not win in my test. This lesson explains how R A G works, and shows what a real test actually says, including the parts that did not go to plan."],
  html=[H2('RAG, tested on 24 real questions', 0),
        DEF('right chunk size: answer in the top 3 <b>92%</b> · wrong size: <b>79%</b> · fancy fusion: <b>did not win</b>', 0, 0.5, style='margin-top:24px;font-size:44px'),
        MARK('real corpus, hand-written questions, stand-in embeddings', 1, 0.6)]),

 dict(id='s1', chap='Where we are', say=[
   "We now have the cloud pieces. Chips, containers, data, training, serving and shipping. From here we build the applications on top, starting with the most common one, retrieval augmented generation, called R A G.",
   "A note on honesty before we start. The search test uses the text of my own notebook, and questions I wrote by hand. The vector side uses a stand in, because no embedding model could be downloaded on my machine. I will label it every time."],
  html=[H2('The most common AI app', 0),
        GRID([('chips', 0, 0.3), ('containers', 0, 0.5), ('data', 0, 0.7), ('training', 0, 0.9), ('serving', 0, 1.1), ('RAG', 0, 1.3)], cols=6, h=120, fs=26),
        STICKY('Honest label', 'real text, my own 24 questions · vectors are a <b>stand-in</b>', 1, 0.5, style='margin-top:26px;font-size:38px')]),

 dict(id='s2', chap='Why RAG exists', say=[
   "Why does R A G exist? A language model only knows what was in its training data. It does not know your company's documents, today's prices, or last week's policy. And if you ask anyway, it may confidently invent an answer.",
   "R A G fixes this like an open book exam. When a question arrives, you first look up the relevant pages, and put them in the prompt. The model then answers from those pages, ideally quoting them."],
  html=[H2('An open-book exam for the model', 0),
        ROW(COL(CARD('<b>without RAG</b><br>answers from memory<br>may invent', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>with RAG</b><br>look up pages first<br>answer from them', 1, 0.3, style='font-size:38px'), width='48%'), style='margin-top:28px')]),

 dict(id='s3', chap='The seven steps', say=[
   "A real R A G pipeline has seven steps. Parse the files. Chunk them into pieces. Add context to each piece. Embed the pieces as vectors.",
   "Then, at question time, search with both keywords and vectors. Rerank the results so the best come first.",
   "And finally generate an answer with citations. The mnemonic is pretty cats can eat hot red grapes, for parse, chunk, context, embed, hybrid, rerank, generate."],
  html=[H2('Seven steps from files to answer', 0), SVG('c3', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c3', 'pipeline', 1000, 290, 1)]),

 dict(id='s4', chap='Parse', say=[
   "Step one, parse. Turn files into clean text. This is where many projects quietly go wrong. A table flattened into a line of words can turn a column of prices into nonsense, and your answers will quote the wrong number with total confidence.",
   "Use a parser that understands layout, and keep metadata with every chunk. The source, the date, the tenant and who may read it. You will need that metadata for filters later."],
  html=[H2('1 · Parse: keep the layout', 0),
        LIST([('layout-aware parsing: tables stay tables', 0, 0.4), ('flattened tables = wrong numbers, quoted confidently', 0, 1.0), ('keep metadata: source, date, tenant, who may read it', 1, 0.4)], kind='ar', style='margin-top:26px;font-size:44px')]),

 dict(id='s5', chap='Chunk', say=[
   "Step two, chunk. A whole document is too big to search well, so cut it into pieces. The rule of thumb is three hundred to eight hundred tokens, with some overlap so a sentence is not cut in half.",
   "Common ways: fixed windows, splitting at paragraphs and sentences, splitting where the topic changes, or keeping small child chunks but returning their larger parent. I tested window size myself, so let us see what the numbers say."],
  html=[H2('2 · Chunk: how big?', 0),
        DEF('rule of thumb: <b>300 to 800 tokens</b>, with overlap', 0, 0.4, style='margin-top:24px;font-size:50px'),
        LIST([('fixed windows or paragraph splits', 1, 0.3), ('split where the topic changes', 1, 0.8), ('small child chunk, big parent returned', 1, 1.3)], kind='ar', style='margin-top:14px;font-size:38px')]),

 dict(id='s6', chap='Embed', say=[
   "Step four, embed. An embedding model turns each chunk into a vector, so similar meanings sit close together. You embed the chunks once, offline. At question time you embed the question and find the nearest chunks.",
   "Cache embeddings by the hash of the text, so unchanged chunks are never paid for twice. And always record which embedding model made them. Mixing two models in one index quietly ruins search."],
  html=[H2('4 · Embed once, search often', 0),
        LIST([('chunks embedded once, offline', 0, 0.4), ('question embedded at query time', 0, 1.0), ('cache by hash of the text', 1, 0.3), ('record the embedding model version', 1, 0.9)], kind='ar', style='margin-top:26px;font-size:46px')]),

 dict(id='s6b', chap='Smaller vectors', say=[
   "A tip that connects to lesson four. Vectors cost memory, so shrink them. Some embedding models are trained so that you can simply cut off the end of each vector and keep working, losing a little quality gracefully. They are called Matryoshka vectors, after the nested Russian dolls.",
   "Combine that with half size or one byte numbers, and a large index can fit in a fraction of the memory. Always check recall on your own questions after shrinking anything."],
  html=[H2('Matryoshka: nested vectors', 0),
        LIST([('cut the end off each vector, keep searching', 0, 0.4), ('quality falls gracefully, memory falls a lot', 0, 1.0), ('combine with float16 or int8 (lesson 4)', 1, 0.3), ('re-check recall on your own questions', 1, 0.9)], kind='ar', style='margin-top:24px;font-size:42px')]),

 dict(id='s7', chap='Hybrid search', say=[
   "Step five, hybrid search. Vectors are good at meaning. A question phrased differently from the document still finds it. But vectors are weak at exact things, like an error code, a product number or a name.",
   "Keyword search, called B M twenty-five, is the opposite. Exact terms win, paraphrases lose. So run both, and merge the two lists."],
  html=[H2('5 · Hybrid: two kinds of search', 0),
        ROW(COL(CARD('<b>vectors</b><br>good at meaning<br>weak at error codes, names', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>BM25 keywords</b><br>good at exact terms<br>weak at paraphrases', 1, 0.3, style='font-size:38px'), width='48%'), style='margin-top:28px')]),

 dict(id='s8', chap='Fusing the lists', say=[
   "How do you merge two lists whose scores mean different things? The popular answer is reciprocal rank fusion. Ignore the scores and use only the ranks. Each list gives a document one over sixty plus its rank.",
   "A document that is first in the vector list and third in the keyword list scores one over sixty-one plus one over sixty-three, about point oh three two three. A document found by only one list scores about point oh one six. Found by both wins."],
  html=[H2('Reciprocal rank fusion', 0),
        DEF('score = Σ 1 ÷ (60 + rank)  · ranks only, no score scaling', 0, 0.4, style='margin-top:24px;font-size:48px'),
        OUT(['#1 vector + #3 keyword: 1/61 + 1/63 = 0.0323', '#2 vector only:          1/62       = 0.0161'], 1, 0.4, size=32, label='arithmetic', style='margin-top:20px'),
        MARK('found by both wins', 1, 1.2)]),

 dict(id='s9', chap='Rewrite the question', say=[
   "A small trick before searching. Users write short, vague questions, so rewrite them. One method asks the model to write a hypothetical answer and searches with that, because answer shaped text is closer to answer documents.",
   "Another splits a complex question into several smaller ones, searches for each in parallel, and merges. It costs one extra model call, so it adds a little latency. Use it when questions are genuinely multi part."],
  html=[H2('Rewrite the question first', 0),
        LIST([('hypothetical answer, then search with it (HyDE)', 0, 0.4), ('split a big question into smaller ones', 1, 0.3), ('costs one extra model call', 1, 0.9)], kind='ar', style='margin-top:26px;font-size:46px')]),

 dict(id='s9b', chap='Keeping the index fresh', say=[
   "Documents change, and a stale index gives stale answers. Connect the index to your storage, so a changed file is parsed and embedded again, and a deleted file's chunks are removed. Hash each chunk's text, so you only pay to embed what actually changed.",
   "Also store the date with each chunk, and decide what should win when two versions disagree. A search that returns last year's policy next to this year's is worse than no search."],
  html=[H2('Keep the index fresh', 0),
        LIST([('changed file: re-parse and re-embed', 0, 0.4), ('deleted file: remove its chunks', 0, 0.9), ('hash chunk text: pay only for changes', 0, 1.4), ('store dates: new beats old', 1, 0.4)], kind='ar', style='margin-top:24px;font-size:44px')]),

 dict(id='s10', chap='Rerank', say=[
   "Step six, rerank. Retrieve a generous number, say a hundred and fifty, then use a slower, smarter model that reads the question and each candidate together, and keep the best twenty. Managed rerankers exist on every big cloud.",
   "Tune the final number. Twenty beat ten and five in the notebook's reading. But stuffing too many passages backfires, because models notice the start and end of a long prompt more than the middle."],
  html=[H2('6 · Rerank: retrieve wide, keep few', 0),
        DEF('top <b>150</b> → cross-encoder rerank → keep <b>20</b>', 0, 0.4, style='margin-top:24px;font-size:52px'),
        MARK('too much context distracts: models skim the middle', 1, 0.5)]),

 dict(id='s11', chap='Answer with citations', say=[
   "Step seven, generate. Give each chunk an I D. Tell the model to answer only from the sources, to cite the I Ds, and to say not found if the answer is absent. That last instruction matters. Without it, the model fills gaps with guesses.",
   "Some model providers offer a citations feature that returns the exact quoted spans. Either way, users should be able to click from an answer to its source."],
  html=[H2('7 · Answer, and cite', 0),
        OUT(['Answer ONLY from the sources below.', 'Cite the source IDs, like [3].', 'If the answer is not there, say "not found".'], 0, 0.4, size=34, label='the rule in the prompt', style='margin-top:24px'),
        MARK('users can click from answer to source', 1, 0.5)]),

 dict(id='s12', chap='My test setup', say=[
   "Now my test. The corpus is the text of this course's notebook, about forty-five thousand words. I wrote twenty-four questions, such as, how long does S three take to auto partition after a load spike, and for each, the exact phrase that answers it.",
   "A chunk counts as a hit if it contains that phrase. Hit at three means the answer is somewhere in the top three chunks. I compared keyword search, a stand in for vectors built from word statistics, and the fusion of both. The stand in is not a neural embedding model."],
  html=[H2('The test', 0),
        OUT(['corpus: 45,060 words (this course\'s notebook)', '24 hand-written questions + answer phrases', 'hit@3 = answer phrase is in the top 3 chunks', 'BM25 · dense stand-in (LSA) · hybrid (RRF)'], 0, 0.4, size=30, label='measured setup', style='margin-top:22px'),
        SUB('the dense retriever is a stand-in: no embedding model could be downloaded', 1, 0.6, style='margin-top:14px')]),

 dict(id='s13', chap='Chunk size, measured', say=[
   "First, chunk size. With hundred word chunks, keyword search found the answer in the top three eighty-three percent of the time. With three hundred words, eighty-seven and a half. With eight hundred, seventy-nine.",
   "The vector stand in followed the same shape. Eighty-three, ninety-two, eighty-eight. Three hundred words was best for both."],
  html=[H2('Chunk size, measured', 0), SVG('c13', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c13', 'chunk_hit3', 1000, 300, 1)]),

 dict(id='s14', chap='Why the middle wins', say=[
   "Why does the middle win? Chunks that are too small lose their surroundings. A line like k equals sixty means little without the sentence around it.",
   "Chunks that are too big dilute the match, because one long chunk holds many topics and ranks well for none of them. That agrees with the three to eight hundred token rule. The exact best size depends on your documents, so test it."],
  html=[H2('Too small, too big', 0),
        ROW(COL(CARD('<b>too small</b><br>loses its surroundings<br>"k = 60" means little alone', 0, 0.4, style='font-size:36px'), width='48%'),
            COL(CARD('<b>too big</b><br>many topics in one chunk<br>ranks well for none', 1, 0.3, style='font-size:36px'), width='48%'), style='margin-top:28px'),
        STICKY('Test it', 'the best size depends on <b>your</b> documents', 1, 0.8, style='margin-top:22px;font-size:38px')]),

 dict(id='s15', chap='The fusion surprise', say=[
   "Now the surprise. With three hundred word chunks, keyword search got eighty-seven and a half percent. The vector stand in, ninety-one point seven. And the fusion of both, eighty-seven and a half.",
   "I expected the fusion to win. It did not.",
   "It matched keyword search and trailed the vector stand in. Honest result, from a small test."],
  html=[H2('The fancy fusion did not win', 0), SVG('c15', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c15', 'methods300', 1000, 290, 1)]),

 dict(id='s16', chap='Why fusion did not help', say=[
   "Why? I counted who found what. Twenty-one of the twenty-four questions were found by both methods. Nothing was found only by keywords. One was found only by the vectors. And two were missed by both.",
   "Fusion helps when the two methods fail on different questions. On my corpus, the two mostly agree, so there is little for fusion to add. Your documents may differ. Codes and names favour keywords."],
  html=[H2('Who found what?', 0), SVG('c16', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c16', 'overlap', 1000, 290, 1)]),

 dict(id='s17', chap='The two misses', say=[
   "The two questions both missed are instructive. How much notice does A W S give for a spot instance. And what value of k does reciprocal rank fusion use.",
   "The first is about spot instances, a word that appears in many chunks across the notebook, so dozens of chunks compete. The second has an answer made of symbols, k equals sixty, which my keyword tokenizer throws away. Reading failures like this is called error analysis, and it tells you what to fix next."],
  html=[H2('Reading the failures', 0),
        LIST([('"spot notice on AWS": the word spot is everywhere', 0, 0.4), ('"k = 60": the answer is symbols, thrown away', 1, 0.3), ('read failures: it tells you what to fix', 1, 0.9)], kind='ar', style='margin-top:26px;font-size:44px'),
        STICKY('Error analysis', 'always <b>read</b> the misses', 1, 1.2, style='margin-top:22px;font-size:42px')]),

 dict(id='s18', chap='A small test, honestly', say=[
   "A caution about my own test. Twenty-four questions is small. Each question is worth four point two percentage points, so differences of one question are noise. I trust the pattern, three hundred words beating eight hundred, more than any single gap.",
   "The point is not that fusion is bad. The notebook cites larger benchmarks where hybrid search helps. The point is to build an eval set of your own, because it takes an afternoon and tells you what really works on your documents."],
  html=[H2('Twenty-four questions is small', 0),
        LIST([('each question = 4.2 points', 0, 0.4), ('one-question gaps are noise', 0, 1.0), ('trust patterns, not single gaps', 0, 1.5), ('build your own eval set: one afternoon', 1, 0.4)], kind='ar', style='margin-top:24px;font-size:44px')]),

 dict(id='s19', chap='Does context help?', say=[
   "Next, an idea called contextual retrieval. Before indexing, ask a model to write one or two sentences placing each chunk in its document, and prepend them. The original study reported that this, with reranking, cut failed retrievals by sixty-seven percent.",
   "I tried the cheapest possible version. I just prepended the topic title to each hundred word chunk. Keyword search did not change. The vector stand in went from eighty-three to eighty-seven and a half, one question. A title is very weak context."],
  html=[H2('Prepending context to chunks', 0), SVG('c19', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c19', 'ctx', 1000, 290, 1)]),

 dict(id='s20', chap='What I did not test', say=[
   "I could not run the real method, which uses a language model to write each chunk's context. So I cannot confirm sixty-seven percent. That figure comes from the original study, described in the notebook. What I can say is that a plain title is not enough.",
   "The real method is affordable, about one dollar per million document tokens, once, using prompt caching. If your search quality matters, it is among the first things worth trying."],
  html=[H2('The real method: not tested here', 0),
        LIST([('real method: an LLM writes each chunk\'s context', 0, 0.4), ('reported: 67% fewer failed retrievals (with reranking)', 0, 1.0), ('cost about $1 per million document tokens, once', 1, 0.4)], kind='ar', style='margin-top:26px;font-size:42px'),
        SUB('from the original study, via the notebook: not reproduced', 1, 1.0, style='margin-top:14px')]),

 dict(id='s21', chap='Seven ways it fails', say=[
   "Researchers listed seven ways R A G systems fail. Missing content, so the answer is not in the data. The right document is not ranked high enough. It was found but dropped before the prompt.",
   "It is in the prompt but the model ignores it. The format is wrong. The answer is too vague. Or it is incomplete. Each failure has a different fix, and only an eval set tells you which one you have."],
  html=[H2('Seven failure points', 0),
        TABLE(['Failure', 'Usual fix'], [(['content missing', 'allow "I don\'t know"'], 0, 0.4), (['right doc ranked low', 'hybrid, context, rewriting'], 0, 0.9), (['found but dropped', 'rerank, tune k'], 1, 0.3), (['in prompt, ignored', 'fewer, better-ordered chunks'], 1, 0.8)], style='margin-top:20px;font-size:36px')]),

 dict(id='s22', chap='Do you need RAG at all?', say=[
   "Do you even need R A G? If your whole knowledge base is under about two hundred thousand tokens, roughly five hundred pages, and it rarely changes, and has one owner, you can put all of it in the prompt and cache it.",
   "Caching can give more than twice the speed and up to ninety percent lower cost, according to vendors. If it is larger, changing, permissioned, or shared by many tenants, use R A G. Cost per question grows with context, and models miss things in the middle."],
  html=[H2('RAG or one long prompt?', 0), SVG('c22', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c22', 'longctx', 1000, 290, 1)]),

 dict(id='s23', chap='Permissions', say=[
   "Permissions deserve their own warning. If your documents have different owners, every chunk carries a list of who may read it, and the search must filter by the asking user. Retrieving first and filtering afterwards is not good enough.",
   "A missing filter means one customer's data appears in another customer's answer. That is the most serious R A G bug there is, and it is caused by metadata, not by the model."],
  html=[H2('Filter by who is asking', 0),
        LIST([('every chunk carries who may read it', 0, 0.4), ('filter inside the search, not afterwards', 0, 1.0), ('a missing filter leaks data between users', 1, 0.4)], kind='ar', style='margin-top:26px;font-size:46px'),
        STICKY('Worst RAG bug', 'a missing <b>tenant filter</b>', 1, 0.9, style='margin-top:22px;font-size:42px')]),

 dict(id='s24', chap='Retrieved text is untrusted', say=[
   "One more warning, which lesson ten covers in full. Text you retrieve is not your instructions. A document can contain sentences written to hijack the model. Treat retrieved text as data, never as commands.",
   "For now, remember to keep the instruction part of the prompt separate from the retrieved part, and never let retrieved text grant the model new powers."],
  html=[H2('Retrieved text is data, not commands', 0),
        ROW(COL(CARD('<b>your instructions</b><br>trusted', 0, 0.4, style='font-size:42px'), width='48%'),
            COL(CARD('<b>retrieved text</b><br>untrusted data', 0, 0.9, style='font-size:42px'), width='48%'), style='margin-top:28px'),
        SUB('indirect prompt injection: lesson 10', 1, 0.6, style='margin-top:16px')]),

 dict(id='s25', chap='Evaluating RAG', say=[
   "How do you know a change helped? Keep a labelled set of questions, with the source passage that answers each. Measure whether the right passage is retrieved, called recall at k, separately from whether the final answer is right.",
   "Track both on every release. Retrieval failures and answer failures need different fixes, and mixing them makes debugging a guessing game."],
  html=[H2('Measure retrieval and answers apart', 0),
        LIST([('labelled questions + the passage that answers each', 0, 0.4), ('retrieval: was the right passage found? (recall@k)', 0, 1.0), ('answer: is the final text right?', 1, 0.3), ('track both on every release', 1, 0.8)], kind='ar', style='margin-top:24px;font-size:42px')]),

 dict(id='s26', chap='Beyond plain RAG', say=[
   "Two advanced ideas to know by name. Graph R A G builds a graph of entities from your documents and answers big picture questions like, what are the main themes. It beats plain R A G on those. For pinpoint facts, hybrid search with reranking is enough.",
   "Agentic R A G lets the model plan searches, pick sources and iterate. Better for multi step questions, but more calls and more cost. Both are extras. Get the basics measured first."],
  html=[H2('Two advanced ideas', 0),
        ROW(COL(CARD('<b>GraphRAG</b><br>entity graph<br>big-picture questions', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>agentic RAG</b><br>the model plans searches<br>more calls, more cost', 1, 0.3, style='font-size:38px'), width='48%'), style='margin-top:28px'),
        SUB('extras: measure the basics first', 1, 0.8, style='margin-top:14px')]),

 dict(id='s27', chap='Managed services', say=[
   "Every big cloud sells managed R A G. Amazon Bedrock Knowledge Bases, Google's R A G Engine, Azure A I Search with Foundry I Q, and OpenAI's file search. They handle ingestion, chunking, embedding, storage, retrieval and grounded answers, and all offer a retrieve only call.",
   "Pick by where your data and your identity already live. SharePoint and Entra point to Azure. S three points to Bedrock. Google storage and BigQuery point to Google. Minimal operations points to OpenAI, though your data leaves your cloud."],
  html=[H2('Managed RAG on each cloud', 0),
        TABLE(['Your data lives in', 'Look at'], [(['SharePoint / Microsoft 365', 'Azure AI Search + Foundry IQ'], 0, 0.4), (['Amazon S3', 'Bedrock Knowledge Bases'], 0, 0.9), (['Google storage, BigQuery', 'Vertex AI RAG Engine'], 1, 0.3), (['minimal operations', 'OpenAI file search (data leaves your cloud)'], 1, 0.9)], style='margin-top:22px;font-size:38px')]),

 dict(id='s28', chap='ShopNest Copilot', say=[
   "For ShopNest Copilot. Parse the help articles and policies, chunk at about three hundred words with overlap, store the source and access level with each chunk, and embed once with a recorded model version.",
   "Search with keywords and vectors, rerank, answer with citations and a not found rule, and filter by customer. Then build a forty question eval set from real tickets, and measure recall before touching anything fancy."],
  html=[H2('ShopNest Copilot: RAG plan', 0),
        TABLE(['Step', 'Plan'], [(['chunk', '~300 words, overlap, metadata'], 0, 0.4), (['index', 'embed once, record the model version'], 0, 0.9), (['search', 'keywords + vectors, rerank'], 1, 0.3), (['answer', 'cite sources, "not found" rule, filter by customer'], 1, 0.8), (['test', '40 real questions, recall@k per release'], 1, 1.3)], style='margin-top:22px;font-size:36px')]),

 dict(id='s29', chap='Four words to keep', say=[
   "Four words to carry forward. Chunk: a piece of a document, sized for search. Hybrid search: keywords and vectors together.",
   "Rerank: sorting the shortlist with a smarter model. And hit at k: the share of questions whose answer appears in the top k results."],
  html=[H2('Four words to keep', 0),
        GRID([('<b>chunk</b>', 0, 0.3), ('<b>hybrid search</b>', 0, 0.9), ('<b>rerank</b>', 1, 0.3), ('<b>hit@k</b>', 1, 0.9)], cols=2, h=140, fs=46, style='margin-top:30px')]),

 dict(id='s30', chap='Interview corner', say=[
   "Interview corner. Asked how you choose chunk size, say: start around three hundred to eight hundred tokens with overlap, then measure on your own questions. In my test, three hundred words found the answer in the top three ninety-two percent of the time, against seventy-nine for eight hundred.",
   "Asked why hybrid search, say: vectors catch paraphrases and keywords catch exact terms, merged by reciprocal rank fusion. But verify on your data. In my test, fusion did not beat the vector stand in, because the two methods failed on the same questions."],
  html=[H2('Interview corner', 0),
        Q('How do you choose chunk size?', '300 to 800 tokens with overlap, then measure. Mine: 300 words 92% vs 800 words 79%.', 0, 0.4),
        Q('Why hybrid search?', 'Vectors: paraphrase. Keywords: exact terms. Fuse by RRF, but verify: it did not win in my test.', 1, 0.4)]),

 dict(id='s31', chap='Your turn', say=[
   "Your turn. The zip for this lesson has two scripts and the notebook text. Run the evaluation. Then replace my questions with your own, from your own documents, and see which chunk size wins for you.",
   "Add a question whose answer is an error code, and watch which method finds it. One changed question teaches more than an hour of reading."],
  html=[H2('Your turn', 0),
        CARD('<b>l08_rag_eval.py</b>: chunk sizes and three retrievers.<br><b>l08_context_prefix.py</b>: does a title prefix help?<br><b>data/notebook_text.txt</b>: the corpus. Swap in your own.', 0, 0.4, style='margin-top:22px;font-size:36px'),
        SUB('one changed question teaches more than an hour of reading', 1, 0.8, style='margin-top:16px')]),

 dict(id='s32', chap='Recap', say=[
   "Recap. R A G is an open book exam in seven steps, parse, chunk, context, embed, hybrid, rerank, generate. On my test, three hundred word chunks found the answer in the top three ninety-two percent of the time, and eight hundred, seventy-nine.",
   "Fusion did not win, because both methods failed on the same questions, and a title prefix barely helped. Filter by user, treat retrieved text as data, and build your own eval set. Next lesson: agents, tools and reliability."],
  html=[H2('Recap', 0),
        GRID([('7 steps, open-book exam', 0, 0.3), ('300 words: 92% in top 3', 0, 0.9), ('800 words: 79%', 0, 1.5),
              ('fusion: did not win', 1, 0.3), ('title prefix: barely helped', 1, 0.9), ('filter by user · build your eval', 1, 1.5)], cols=3, h=150, fs=30)]),
]
