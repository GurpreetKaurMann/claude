# CAI-08 Upload Copy

## 1. Lesson video (YouTube)

**Title:** RAG Explained With a Real Test: What Actually Works (And What Did Not)

**Description:**
```
Lesson 8 of Cloud for AI Engineers. I tested retrieval on my own notebook with 24 hand-written questions. The right chunk size put the answer in the top 3 results 92% of the time, the wrong one 79%. And the fancy fusion did not win.
We walk through the seven steps of RAG (parse, chunk, context, embed, hybrid, rerank, generate), reciprocal rank fusion, then run a real retrieval test on 45,060 words: three chunk sizes, keyword search, a vector stand-in, and fusion. We read the failures, test a title prefix as cheap context, list the seven failure points, decide when to skip RAG, and cover permissions, untrusted text, evaluation and managed services. The corpus and questions are real; the vector retriever is a stand-in (TF-IDF + SVD) because no embedding model could be downloaded. 24 questions is a small test, and I say so.
⏮️ Previous lesson: <CAI-07 link>

In this lesson:
✅ RAG as an open-book exam
✅ The seven steps: parse, chunk, context, embed, hybrid, rerank, generate
✅ Reciprocal rank fusion with a worked example
✅ A real test: 45,060 words, 24 hand-written questions
✅ Chunk size measured: 300 words 91.7% vs 800 words 87.5% (dense), 87.5% vs 79.2% (BM25)
✅ The surprise: hybrid fusion did not beat the vector stand-in
✅ Why: 21 of 24 questions found by both methods
✅ The two misses and error analysis
✅ A title prefix as context: barely helped
✅ Seven failure points and their fixes
✅ RAG or one long cached prompt?
✅ Permissions: the worst RAG bug
✅ Managed RAG on AWS, Google Cloud, Azure and OpenAI
✅ ShopNest Copilot RAG plan
✅ Interview questions with answers

⏱️ Chapters
0:00 RAG, honestly tested
0:32 Intro
0:42 Where we are
1:13 Why RAG exists
1:41 The seven steps
2:09 Parse
2:37 Chunk
3:05 Embed
3:32 Smaller vectors
4:01 Hybrid search
4:24 Fusing the lists
4:54 Rewrite the question
5:23 Keeping the index fresh
5:51 Rerank
6:19 Answer with citations
6:45 My test setup
7:19 Chunk size, measured
7:41 Why the middle wins
8:05 The fusion surprise
8:26 Why fusion did not help
8:53 The two misses
9:23 A small test, honestly
9:54 Does context help?
10:28 What I did not test
10:56 Seven ways it fails
11:22 Do you need RAG at all?
11:52 Permissions
12:19 Retrieved text is untrusted
12:42 Evaluating RAG
13:05 Beyond plain RAG
13:35 Managed services
14:11 ShopNest Copilot
14:39 Four words to keep
14:57 Interview corner
15:32 Your turn
15:54 Recap
16:27 Next lesson

Next lesson → CAI-09: GenAI apps: agents, MCP and reliability: tools, loops, protocols, retries and sandboxes

🌐 Website: https://thecodenotebook.com/
📸 Instagram: https://www.instagram.com/thecodenotebookyt/

#rag #llm #ai #vectorsearch #aiengineering
```

**Tags:**
```
rag explained, rag chunk size, hybrid search, reciprocal rank fusion, rag evaluation, retrieval augmented generation tutorial, rag vs long context, contextual retrieval, bm25 vs embeddings, rag failure modes, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
The retrieval test is real text and real questions, but the vector side is a stand-in and 24 questions is small: each question is 4.2 points. 📊\n\nQuestion for you 👇\nWhich surprised you more: fusion not winning, or a simple title prefix barely helping?
```

**Thumbnail:** CAI-08_Thumbnail.png

---

## 2. Short 1 (YouTube Shorts)

**Title:** RAG Chunk Size: 300 Words Beat 800 in My Test (24 Questions) #shorts

**Description:**
```
Corpus: a 45,060-word notebook. 24 hand-written questions. Hit = the top-3 chunks contain the answer phrase.\n• 300-word chunks: 91.7% (vector stand-in), 87.5% (BM25)\n• 800-word chunks: 87.5% (vector stand-in), 79.2% (BM25)\n\nThe vector retriever is a stand-in (TF-IDF + SVD), not a neural embedding model. Small test: each question = 4.2 points.\n\nFull lesson: Cloud for AI Engineers, lesson 8.
```

**Tags:**
```
shorts, rag chunk size, retrieval augmented generation, rag evaluation, chunking strategy, llm rag tutorial, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
What chunk size do you use? 👇
```

**Cover:** CAI-08_Short1_Cover.png

---

## 3. Short 2 (YouTube Shorts)

**Title:** Hybrid Search Didn't Win in My RAG Test (Here's Why) #shorts

**Description:**
```
300-word chunks, 24 questions, answer in the top 3:\n• vector stand-in (LSA): 91.7%\n• BM25: 87.5%\n• hybrid (reciprocal rank fusion): 87.5%\n\n21 of 24 questions were found by both methods, so fusion added little. It helps when the methods fail on different questions. Small test; larger benchmarks cited in the notebook show hybrid helping.\n\nFull lesson: Cloud for AI Engineers, lesson 8.
```

**Tags:**
```
shorts, hybrid search, reciprocal rank fusion, rag evaluation, bm25 vs embeddings, rag tutorial, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Does hybrid search help on your data? 👇
```

**Cover:** CAI-08_Short2_Cover.png

---

## 4. Instagram Reel 1

**Caption:**
```
Do you even need RAG? 📚\n\n🟢 Knowledge base under ~200K tokens (about 500 pages), stable, one tenant: put it ALL in the prompt and cache it. (Vendors: over 2x lower latency, up to 90% cheaper.)\n🔴 Larger, changing, permissioned or multi-tenant: use RAG.\n\nSave this. Full lesson on YouTube: The Code Notebook.
```

**First comment (pin it):**
```
Lesson 9 next: agents, tools and reliability 🤖 Follow so you don't miss it!
```

**Cover:** CAI-08_Reel1_Cover_Instagram.png

---
