import sys; sys.path.insert(0, '/home/claude/caigen')
from cai_lib import *
from c08_diagrams import DIAGRAMS
from c08_long import LONG
from c08_notes import NOTES

L = dict(
 code='CAI-08', num=8, num_word='eight', slug='RAG_From_Documents_To_Cited_Answers',
 title='RAG, Tested', title_html='RAG,<br>tested', title_size=150,
 tagline='From documents to cited answers, with a real retrieval test.', module='Module 4 · Shipping it',
 toc=['The seven steps', 'Hybrid search and RRF', 'My retrieval test', 'Chunk size, measured', 'The fusion surprise', 'Failure points', 'Interview Q&amp;A'],
 data_label='Course project', project='ShopNest Copilot', project_desc='the AI support assistant we move to the cloud, step by step',
 prev='CAI-07', next=('CAI-09', '<b>GenAI apps: agents, MCP and reliability</b>: tools, loops, protocols, retries and sandboxes'),
 next_say='agents, tools and reliability. Loops, protocols, retries and sandboxes.',
 diagrams=DIAGRAMS, long=LONG, notes=NOTES,
 glow=dict(a='RAG', b='TESTED', icons=['magn1', '>', 'doc2']),
 thumb=dict(title='RAG,<br><span class="hl">tested</span>', size=140, sub='24 real questions', chips=('300 words: 92%', '800 words: 79%'), mini='mini_thumb'),

 short1=mk_short(1, 'RAG_Chunk_Size_300_vs_800_Words', "The right chunk size for R A G found the answer ninety-two percent of the time. The wrong one, seventy-nine.",
   ('300 WORDS', 'BEATS 800', 130, 150),
   ["I searched my own forty-five thousand word notebook with twenty-four questions I wrote. A chunk is a hit if it contains the answer. With three hundred word chunks, the answer was in the top three ninety-two percent of the time.",
    "With eight hundred word chunks, eighty-eight. With keyword search, eighty-seven and a half against seventy-nine. The vector side is a stand in, so test your own."],
   'mini_thumb', "Test chunk sizes on your own questions.", 'Do this', 'measure on<br><b>your</b> data', dict(title='RAG chunk size:<br><span class="hl">300 beats 800</span>', size=96, sub='24 questions, measured', mini='mini_thumb'),
   dict(title='RAG Chunk Size: 300 Words Beat 800 in My Test (24 Questions) #shorts',
     desc="Corpus: a 45,060-word notebook. 24 hand-written questions. Hit = the top-3 chunks contain the answer phrase.\\n• 300-word chunks: 91.7% (vector stand-in), 87.5% (BM25)\\n• 800-word chunks: 87.5% (vector stand-in), 79.2% (BM25)\\n\\nThe vector retriever is a stand-in (TF-IDF + SVD), not a neural embedding model. Small test: each question = 4.2 points.\\n\\nFull lesson: Cloud for AI Engineers, lesson 8.",
     tags='shorts, rag chunk size, retrieval augmented generation, rag evaluation, chunking strategy, llm rag tutorial, cloud for ai engineers, the code notebook',
     pinned='What chunk size do you use? 👇')),

 short2=mk_short(2, 'Hybrid_Search_Did_Not_Win', "Everyone says to use hybrid search with fusion. In my test it did not win. Here is why.",
   ('HYBRID SEARCH', 'DID NOT WIN', 100, 110),
   ["With three hundred word chunks, the vector stand in found the answer in the top three ninety-two percent of the time. Keywords, eighty-seven and a half. Fusing both, eighty-seven and a half.",
    "I counted why. Twenty-one of twenty-four questions were found by both methods, so fusion had little to add. It helps when the methods fail on different questions."],
   'mini_hybrid', "Verify hybrid search on your own data.", 'Rule', 'test before<br>you trust', dict(title='Hybrid search<br><span class="hl">did not win</span>', size=100, sub='in my test, honestly', mini='mini_hybrid'),
   dict(title="Hybrid Search Didn't Win in My RAG Test (Here's Why) #shorts",
     desc="300-word chunks, 24 questions, answer in the top 3:\\n• vector stand-in (LSA): 91.7%\\n• BM25: 87.5%\\n• hybrid (reciprocal rank fusion): 87.5%\\n\\n21 of 24 questions were found by both methods, so fusion added little. It helps when the methods fail on different questions. Small test; larger benchmarks cited in the notebook show hybrid helping.\\n\\nFull lesson: Cloud for AI Engineers, lesson 8.",
     tags='shorts, hybrid search, reciprocal rank fusion, rag evaluation, bm25 vs embeddings, rag tutorial, cloud for ai engineers, the code notebook',
     pinned='Does hybrid search help on your data? 👇')),

 reel=mk_reel('Skip_RAG_Under_200K_Tokens', ["When you can skip R A G completely.",
   "If your whole knowledge base is under about two hundred thousand tokens, roughly five hundred pages, stable, and has one owner, put all of it in the prompt and cache it. Vendors report over twice the speed and up to ninety percent lower cost."],
   "Bigger, changing or permissioned? Use R A G. Save this.", 'SKIP RAG?', ['under ~200K tokens: cache it all', 'bigger or changing: use RAG'], [3.4, 6.2], 'Rule', '~500 pages<br>and stable',
   dict(title='When to<br><span class="hl">skip RAG</span>', size=110, sub='under 200K tokens', mini='mini_long'),
   dict(title='When you can skip RAG completely',
     caption="Do you even need RAG? 📚\\n\\n🟢 Knowledge base under ~200K tokens (about 500 pages), stable, one tenant: put it ALL in the prompt and cache it. (Vendors: over 2x lower latency, up to 90% cheaper.)\\n🔴 Larger, changing, permissioned or multi-tenant: use RAG.\\n\\nSave this. Full lesson on YouTube: The Code Notebook.",
     pinned="Lesson 9 next: agents, tools and reliability 🤖 Follow so you don't miss it!")),

 upload=dict(
   title='RAG Explained With a Real Test: What Actually Works (And What Did Not)',
   hook="Lesson 8 of Cloud for AI Engineers. I tested retrieval on my own notebook with 24 hand-written questions. The right chunk size put the answer in the top 3 results 92% of the time, the wrong one 79%. And the fancy fusion did not win.",
   what="We walk through the seven steps of RAG (parse, chunk, context, embed, hybrid, rerank, generate), reciprocal rank fusion, then run a real retrieval test on 45,060 words: three chunk sizes, keyword search, a vector stand-in, and fusion. We read the failures, test a title prefix as cheap context, list the seven failure points, decide when to skip RAG, and cover permissions, untrusted text, evaluation and managed services. The corpus and questions are real; the vector retriever is a stand-in (TF-IDF + SVD) because no embedding model could be downloaded. 24 questions is a small test, and I say so.",
   bullets=['RAG as an open-book exam', 'The seven steps: parse, chunk, context, embed, hybrid, rerank, generate', 'Reciprocal rank fusion with a worked example', 'A real test: 45,060 words, 24 hand-written questions', 'Chunk size measured: 300 words 91.7% vs 800 words 87.5% (dense), 87.5% vs 79.2% (BM25)',
            'The surprise: hybrid fusion did not beat the vector stand-in', 'Why: 21 of 24 questions found by both methods', 'The two misses and error analysis', 'A title prefix as context: barely helped', 'Seven failure points and their fixes', 'RAG or one long cached prompt?', 'Permissions: the worst RAG bug', 'Managed RAG on AWS, Google Cloud, Azure and OpenAI', 'ShopNest Copilot RAG plan', 'Interview questions with answers'],
   hashtags='#rag #llm #ai #vectorsearch #aiengineering',
   tags='rag explained, rag chunk size, hybrid search, reciprocal rank fusion, rag evaluation, retrieval augmented generation tutorial, rag vs long context, contextual retrieval, bm25 vs embeddings, rag failure modes, cloud for ai engineers, the code notebook',
   pinned="The retrieval test is real text and real questions, but the vector side is a stand-in and 24 questions is small: each question is 4.2 points. 📊\\n\\nQuestion for you 👇\\nWhich surprised you more: fusion not winning, or a simple title prefix barely helping?"),
)
