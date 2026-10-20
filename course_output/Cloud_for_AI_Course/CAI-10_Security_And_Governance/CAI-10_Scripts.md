# CAI-10 · Security and Governance: Scripts

**Lesson 10 of 12 · Module 5 · Safe, cheap, and your career**

Voice: AI narrator (Kokoro `af_heart`). Final lesson video length: 17:51.

## Long video narration

**[The filter blocked three of twelve]**

> I wrote twelve prompt injection attacks and a keyword filter to stop them. The filter stopped three. With nothing in place, all twelve stole the private record. And with a simple design change, the model was fooled all twelve times, but nothing left the building.

> That is the lesson of this security chapter. Filters are bypassable. Architecture holds. We will also test permissions, personal data and data leaks between customers. Every result comes from a toy you can run yourself.

**[Intro]**

> Welcome to lesson ten of the cloud for A I engineers course, on The Code Notebook.

> The handwritten notes and the code for this lesson are linked in the description.

**[Where we are]**

> We have built, trained, served and shipped an A I system. Now someone will try to break it, or just make an honest mistake that leaks data. Security for A I has one surprise. Most of the damage in real incidents came from the system around the model, not the model itself.

> Honest labels. The injection test uses a deliberately gullible scripted stand in, and fake data. The permission checker is my simplified version of cloud policy rules. The personal data test uses thirty made up strings. None of it is a benchmark of a real product.

**[Who secures what]**

> Start with who is responsible. The cloud provider secures the buildings, the machines, the model hosting, and promises not to train on your A P I data. You secure everything about how you use it. Who may call the model, what data goes in, what the answers are used for.

> There are five locks. Identity, network, encryption, logging, and application authorisation. A mnemonic is, I need every lock, always. The provider hands you the first four. The fifth, you build yourself.

**[The request gap]**

> Here is the gap that catches teams out. Identity and access management decides who may call the model. A private network decides which pipe the call travels. A guardrail looks for attacks in the text.

> But nothing asks the real question. May this user send this prompt, see this document, or fire this tool? That check is application authorisation, it sits in your code, and most of the incidents in this lesson come from missing it.

**[Identity]**

> Identity first. Your service needs to prove who it is to the cloud. The best way is keyless. On Kubernetes, the cluster hands each pod a short lived token, which the cloud exchanges for short lived cloud credentials. Nothing long lived exists to leak.

> All three big clouds work this way, with different names. Pod Identity on A W S, Workload Identity on Google and Azure. Prefer it over keys in files, every time.

**[Least privilege: a test]**

> Least privilege means giving a role only the permissions it needs. I wrote a small policy checker with simplified rules. Anything is denied unless allowed, an explicit deny always wins, and stars match anything. This is my teaching version, not the real cloud engine.

> I tested two roles with twelve requests. The narrow role is the notebook's example, allowed to invoke one family of models in one region. The broad role allows everything under the model service, on every resource. An organisation rule also blocks calls outside two approved European regions.

**[Least privilege, measured]**

> The narrow role was allowed two of the twelve requests. Both were ordinary model calls. The broad role was allowed nine.

> Those extra seven included creating a guardrail, starting a fine tuning job, deleting a custom model and changing the logging configuration. A role that only needed to call a model could switch off its own audit trail. The organisation rule still blocked the other regions for both.

**[Network and perimeters]**

> Network next. Use private endpoints so calls to the model service never cross the public internet. And turn public access off. If you add a private path but leave the public one on, the private path is only optional.

> A stronger control is a perimeter. Google's service controls draw a boundary around the A I service, so even valid credentials cannot copy data or models out of it. It is an anti exfiltration control.

**[Secrets and keys]**

> Secrets. Keys for outside model providers and database passwords belong in a secrets manager. Never in an environment file, never in an image, and never in a prompt, because a model can repeat what is in its context.

> Use customer managed encryption keys for training data, custom models, vector stores and logs. They let you revoke access yourself, and they leave an audit trail.

**[Two kinds of logs]**

> Logs come in two kinds, and people mix them up. The audit log records who called which A P I and when. It does not contain the prompts. A separate invocation log records prompts and answers, and it is off by default.

> Both edges are sharp. With no logs, you have no audit trail, and some regulations require one. With logs on, you have created a new store full of personal data and secrets. Encrypt it, restrict access, and set a retention period.

**[Data use and retention]**

> What happens to your data? All three big clouds commit, by contract, not to train their foundation models on your A P I data. That part is settled. The open questions are retention and residency, and they differ feature by feature.

> Some features keep prompts for a while to detect abuse. Zero data retention exists, but you usually must opt in or get approval, and some features rule it out. Residency has traps too, such as endpoints that route requests across regions. Read the provider's page before you promise a customer EU only.

**[Personal data: a test]**

> Personal data, called P I I. Redact it at four places. Before embedding documents, because it is hard to find and delete inside vectors. On the prompt. On the output. And before logging.

> How good is a simple pattern based redactor? I wrote thirty test strings, with made up people. Emails, phone numbers in several formats, card numbers with a checksum test, names, addresses and ID numbers. Then I measured how many personal items it found.

**[PII, measured]**

> Patterns did fairly well on things with a fixed shape. Emails, eighty-three percent. Phone numbers, eighty-six. Card numbers, eighty. They missed formats like at example dot com, and spoken numbers.

> On names, addresses and ID numbers they found nothing, zero. Overall, fifty-eight percent. It also raised false alarms on two of four harmless strings. Real systems add trained recognisers, such as Presidio, Comprehend and Sensitive Data Protection, which I did not test.

**[Confidential computing]**

> A word on confidential computing. It protects data while it is being processed, by running inside encrypted hardware that even the cloud operator cannot read. Azure and Google offer H one hundred machines with it.

> It has limits. It is weak against physical attacks, and multi GPU support was limited when the notebook was written. And it does nothing about prompt injection or application leaks. It is a complement to the other locks, not a replacement.

**[The OWASP list]**

> There is a standard checklist, the O W A S P top ten for language model applications. Prompt injection is number one. Then sensitive information disclosure, supply chain, data and model poisoning, improper output handling, excessive agency, system prompt leakage, vector and embedding weaknesses, misinformation, and unbounded consumption.

> Notice how many of these are about the system, not the model. Output handling, agency, vectors, consumption. That matches what the notebook says about real incidents. Architecture beats model tuning.

**[Two kinds of injection]**

> Prompt injection comes in two kinds. Direct is the user typing something like, ignore your instructions. The attacker is the user, and the harm is a bypassed policy in their own session.

> Indirect is far more dangerous. The instruction is hidden in something the model reads. A web page, an email, a P D F, a search result, a calendar invite, a tool's output. The attacker is not the user. The user is the victim.

**[How data leaves]**

> How does stolen data actually leave? One well known path is a markdown image. The injected text tells the model to write an image link, with the secret inside the web address. The chat window loads the image automatically, and the secret goes to the attacker. No click needed.

> Other paths. A link the user is nudged to click. And any tool that talks outward, such as email, a web fetch, or posting to a ticket. A real case in twenty twenty-five, called EchoLeak, used a hidden instruction in an email to make an assistant leak data with no clicks.

**[The lethal trifecta]**

> A way to think about it. An agent that has all three of these can be tricked into stealing. Untrusted content it reads. Private data it can access. And a way to act outwards, such as email, links or images.

> Meta proposed the rule of two. Until injection can be reliably detected, give an agent at most two of three. Untrusted input, sensitive data, and the power to change things or communicate. If it needs all three, a human approves. Pick two.

**[My injection experiment]**

> Let me test it. A support assistant answers a customer using their private record and a help article. An attacker has poisoned the article. I wrote twelve attacks, in different wording. Some are blunt. Some are polite. Some use spacing, number swaps, or French.

> The model is a stand in that obeys any instruction it finds, the worst case. Real models resist some attacks, but injection is unsolved, so we design as if they do not. Three setups. Nothing. A keyword filter. And an allowlist on what can leave.

**[Nothing in place]**

> With nothing in place, the stand in was fooled twelve times out of twelve, and the private record left the system twelve times. Either by email, or inside an image address.

> That is the baseline. If your assistant can read untrusted text, see private data and reach the outside world, assume it will leak.

**[The keyword filter]**

> Setup B added a keyword filter that blocks phrases like, ignore previous instructions. It stopped three attacks. Nine got through, and the record left nine times.

> Which ones? A polite request to send the order history. An administrator claiming authority. A note for quality assurance. The two image attacks. And the versions with spaces between letters, a zero for an o, French, and a plain instruction with no trigger words at all. You cannot list every way to say it.

**[Design beats filters]**

> Setup C changed no wording rules. The model was just as gullible, and was fooled twelve times. But outbound email could only go to the customer's own address, and images only loaded from our own domain.

> The record left the system zero times. The model was fooled and it did not matter. That is the principle. Break any link in the chain, and the leak stops. Filters guess about words. An allowlist controls the door.

**[Defence in depth]**

> So how do you defend? Use filters and classifiers as one cheap layer, never the only one. Give the model least privilege tools. Put approvals before anything irreversible. Restrict outbound email, links and images. Run code in sandboxes.

> And test attacks yourself. Open source tools such as garak and PyRIT run attack suites against your system, and a catalogue called Mitre Atlas maps the tactics. Treat any single defence as bypassable.

**[Leaks between customers]**

> The next leak needs no attacker at all. In lesson eight we said to filter by who is asking. Here is the test. Five thousand synthetic documents across five customers, with similar text. A user from customer two asks two hundred questions, and we ask for the top five results.

> Three designs. No filter. Filter after the search, which drops other customers' documents from the top five. And filter inside the search, so only that customer's documents are ever searched.

**[Tenant leak, measured]**

> With no filter, eight hundred and thirty-three of the thousand results shown belonged to someone else. Eighty-three percent.

> Filtering after the search leaked nothing, but returned only point eight three documents per question, because most of the top five belonged to other customers. Filtering inside the search leaked nothing and returned all five. The filter belongs inside the search.

**[Excessive agency]**

> Agents add more risks. Excessive agency means a model given more tools, permissions or freedom than the job needs. Give an agent a delete tool it never uses, and one injected sentence can use it.

> A newer list covers agents specifically. Goal hijacking, tool misuse, identity abuse, poisoned memory, rogue agents. The common fix is the same. Minimal, scoped tools, short lived credentials, human approval for irreversible steps, and a sandbox.

**[Supply chain]**

> Supply chain risks. Many model files are stored in a format called pickle, which can run code when loaded. Downloading a model can mean running a stranger's program. Prefer the safer tensor format, pin versions, and check signatures.

> The same goes for packages, M C P servers, plugins and prompts from outside. In twenty twenty-five, researchers found models on a public hub with booby trapped files that slipped past scanners. Treat third party models and tools like third party code.

**[Denial of wallet]**

> One more risk is about money. Unbounded consumption, also called denial of wallet. An attacker, or a bug, can make your assistant burn tokens, with endless loops or huge inputs, until the bill is the attack.

> Cap everything. Tokens per request, requests per user, steps per agent run, and a budget alarm per team. Lesson five showed how fast loops cost, so a cap is a safety feature.

**[Governance basics]**

> Governance. Rules about A I are arriving. In the European Union, the A I Act's obligations for general purpose models and its transparency rules became live in August twenty twenty-six, while rules for high risk systems were pushed later, to December twenty twenty-seven and August twenty twenty-eight. Deferred, not cancelled.

> In health care, whether the B A A covers your A I feature is decided feature by feature. And two habits help everywhere. Keep an inventory of every A I system, and keep logs. They are your evidence. This is not legal advice.

**[ShopNest Copilot]**

> For ShopNest Copilot. Pods use keyless identity and a role that can only invoke the one approved model in the approved regions. Keys live in a secrets manager. Private endpoints, public access off. Prompt logs encrypted, with tight access and a short retention.

> The retrieval search filters by customer inside the query. Retrieved text is data, not commands. The assistant may email only the customer's own address, and show images only from our own domain. And the refund tool needs human approval, as in lesson nine.

**[Four words to keep]**

> Four words to carry forward. Least privilege: only the permissions needed. Prompt injection: instructions hidden in text the model reads.

> Egress allowlist: a short list of places data may go. And tenant filter: a rule, inside the search, so one customer never sees another's data.

**[Interview corner]**

> Interview corner. Asked how you defend against prompt injection, say: assume it cannot be fully filtered, so limit the damage. Least privilege tools, egress allowlists, human approval for risky actions. In my test a keyword filter stopped three of twelve attacks, while an egress allowlist left zero leaks.

> Asked how you stop one customer seeing another's data in a R A G system, say: store access metadata on every chunk and filter inside the search. In my test, with no filter, eighty-three percent of results belonged to someone else.

**[Your turn]**

> Your turn. The zip for this lesson has four scripts. The injection experiment, the tenant leak test, the policy checker and the personal data test. Add a fourth setup to the injection test, with an approval step, and see what changes.

> Then write attacks of your own that beat my filter. One changed number teaches more than an hour of reading.

**[Recap]**

> Recap. Five locks, and you build the last, application authorisation. A broad role allowed nine of twelve requests, including deleting models, against two for a narrow one. Pattern based redaction found fifty-eight percent of personal data, and zero names.

> A keyword filter stopped three of twelve injections. An egress allowlist left zero leaks, even though the model was fooled every time. Filter inside the search, or eighty-three percent of results can be someone else's. Next lesson: cost and Fin Ops.

**[Next lesson]**

> In the next lesson: cost and fin ops. GPU use, token costs, and the break even sum.

> Subscribe so you don't miss it. See you in the notebook.


## Short 1: My Prompt Injection Filter Stopped 3 of 12 Attacks (What Worked) #shorts

> I wrote a filter to stop prompt injection. It stopped three of twelve attacks. Here is what worked instead.

> In my toy test the model is deliberately gullible and obeys any instruction it reads. With nothing in place, all twelve attacks leaked the private record. A keyword filter stopped three.

> The fix was not better words. It was an allowlist on what can leave. The model was still fooled twelve times, but zero records left. Control the door.

> Filters guess about words. Allowlists control the door.


## Short 2: RAG Without a Permission Filter: 83% of Results Were Someone Else's #shorts

> Without a permission filter in my RAG search, eighty-three percent of the results belonged to someone else.

> I built five thousand synthetic documents across five customers, and a user from customer two asked two hundred questions. With no filter, eight hundred and thirty-three of a thousand results were another customer's.

> Filtering after the search leaked nothing but returned under one document per question. Filtering inside the search returned all five and leaked none.

> Put the permission filter inside the search.


## Instagram Reel 1: A broad cloud role can delete your models and switch off logging

> Why a broad cloud role is dangerous for an A I app.

> I checked twelve requests against two roles with a small policy checker. The narrow role, one model family in one region, was allowed two. The broad role, everything under the model service, was allowed nine, including deleting a model and changing the logging.

> Give it only what it needs. Save this.
