# CAI-10 Upload Copy

## 1. Lesson video (YouTube)

**Title:** Prompt Injection Explained: Why My Filter Failed and the Design That Worked (Tested)

**Description:**
```
Lesson 10 of Cloud for AI Engineers. I wrote 12 prompt injection attacks and a keyword filter. It stopped 3. With nothing in place all 12 stole the record. With an egress allowlist the model was fooled 12 times and nothing left.
We cover the five locks (identity, network, encryption, logging, application authorisation), the request gap, keyless identity, a least-privilege policy test (narrow role 2 of 12, broad role 9 of 12), private endpoints and perimeters, secrets, the two kinds of logs, data use and retention, PII redaction measured (58% overall, 0% of names), confidential computing, the OWASP LLM top 10, direct and indirect injection, how data leaves, the lethal trifecta and the Rule of Two, a 12-attack injection experiment, cross-customer leaks in RAG (83% without a filter), excessive agency, supply chain, denial of wallet and governance basics. The injection test uses a deliberately gullible scripted stand-in model, the data is synthetic, and the policy checker is a simplified teaching version.
⏮️ Previous lesson: <CAI-09 link>

In this lesson:
✅ Who secures what, and the five locks
✅ The request gap: nobody checks THIS user for THIS document
✅ Keyless identity
✅ Least privilege tested: broad role 9 of 12 allowed, narrow role 2
✅ Private endpoints, perimeters, secrets and encryption keys
✅ Two kinds of logs, and why a prompt log is a PII database
✅ PII redaction measured: 58% overall, 0% of names
✅ The OWASP top 10 for LLM apps
✅ Direct vs indirect prompt injection and how data leaves
✅ The lethal trifecta and the Rule of Two
✅ The experiment: nothing 12/12 leaked, filter 9/12, egress allowlist 0/12
✅ RAG tenant leak: 83% of results not yours without a filter
✅ Excessive agency, supply chain and denial of wallet
✅ Governance basics (not legal advice)
✅ ShopNest Copilot security plan
✅ Interview questions with answers

⏱️ Chapters
0:00 The filter blocked three of twelve
0:32 Intro
0:42 Where we are
1:19 Who secures what
1:50 The request gap
2:18 Identity
2:46 Least privilege: a test
3:25 Least privilege, measured
3:51 Network and perimeters
4:19 Secrets and keys
4:45 Two kinds of logs
5:14 Data use and retention
5:50 Personal data: a test
6:21 PII, measured
6:53 Confidential computing
7:23 The OWASP list
7:59 Two kinds of injection
8:28 How data leaves
9:04 The lethal trifecta
9:34 My injection experiment
10:08 Nothing in place
10:28 The keyword filter
10:59 Design beats filters
11:26 Defence in depth
11:57 Leaks between customers
12:29 Tenant leak, measured
12:53 Excessive agency
13:25 Supply chain
13:58 Denial of wallet
14:25 Governance basics
15:01 ShopNest Copilot
15:37 Four words to keep
15:56 Interview corner
16:31 Your turn
16:53 Recap
17:27 Next lesson

Next lesson → CAI-11: Cost and FinOps: GPU utilisation, token economics and the break-even sum

🌐 Website: https://thecodenotebook.com/
📸 Instagram: https://www.instagram.com/thecodenotebookyt/

#aisecurity #promptinjection #llm #cloudsecurity #aiengineering
```

**Tags:**
```
prompt injection explained, llm security, egress allowlist, lethal trifecta, rule of two, owasp llm top 10, rag permissions, least privilege iam, pii redaction, ai agent security, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
The injection test uses a deliberately gullible stand-in model with synthetic data, the policy checker is a simplified teaching version, and the PII test uses 30 made-up strings. 📊\n\nQuestion for you 👇\nWhich surprised you more: a filter stopping only 3 of 12, or 83% of RAG results belonging to someone else?
```

**Thumbnail:** CAI-10_Thumbnail.png

---

## 2. Short 1 (YouTube Shorts)

**Title:** My Prompt Injection Filter Stopped 3 of 12 Attacks (What Worked) #shorts

**Description:**
```
Toy test: a deliberately gullible stand-in model (not a real LLM), 12 attack variants written by me, some to dodge the filter.\n• nothing in place: record left 12 of 12\n• keyword filter: 9 of 12 left (it stopped 3)\n• egress allowlist (email only to the customer, images only from our domain): the model was fooled 12 of 12, 0 left\n\nFull lesson: Cloud for AI Engineers, lesson 10.
```

**Tags:**
```
shorts, prompt injection, llm security, egress allowlist, indirect prompt injection, ai agent security, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Do you rely on a filter or on design? 👇
```

**Cover:** CAI-10_Short1_Cover.png

---

## 3. Short 2 (YouTube Shorts)

**Title:** RAG Without a Permission Filter: 83% of Results Were Someone Else's #shorts

**Description:**
```
5,000 synthetic documents, 5 customers, a customer-2 user asks 200 questions (top 5):\n• no filter: 833 of 1,000 results were another customer's\n• filter after search: 0 leaked, but only 0.83 documents returned per question\n• filter inside the search: 0 leaked, 5.00 documents returned\n\nFull lesson: Cloud for AI Engineers, lesson 10.
```

**Tags:**
```
shorts, rag security, multi-tenant rag, data leak, access control, vector database permissions, cloud for ai engineers, the code notebook
```

**Pinned comment:**
```
Is your RAG filter inside the search or after it? 👇
```

**Cover:** CAI-10_Short2_Cover.png

---

## 4. Instagram Reel 1

**Caption:**
```
Least privilege, tested. 🔐\n\n12 requests, checked with a simplified policy checker (my teaching version, not the real cloud engine):\n🟢 narrow role (one model family, one region): 2 allowed\n🔴 broad role (everything under the model service): 9 allowed, including deleting a custom model and changing the logging configuration\n\nGive it only what it needs. Save this. Full lesson on YouTube: The Code Notebook.
```

**First comment (pin it):**
```
Lesson 11 next: cost and FinOps 💸 Follow so you don't miss it!
```

**Cover:** CAI-10_Reel1_Cover_Instagram.png

---
