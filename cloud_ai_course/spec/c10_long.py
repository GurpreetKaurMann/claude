import sys; sys.path.insert(0, '/home/claude/caigen')
from frag import *
from gailab import CODE, OUT

LONG = [
 dict(id='s0', chap='The filter blocked three of twelve', say=[
   "I wrote twelve prompt injection attacks and a keyword filter to stop them. The filter stopped three. With nothing in place, all twelve stole the private record. And with a simple design change, the model was fooled all twelve times, but nothing left the building.",
   "That is the lesson of this security chapter. Filters are bypassable. Architecture holds. We will also test permissions, personal data and data leaks between customers. Every result comes from a toy you can run yourself."],
  html=[H2('Filter: 3 of 12 stopped. Design: 0 leaks.', 0),
        DEF('no protection: <b>12/12</b> left · keyword filter: <b>9/12</b> left · egress allowlist: <b>0/12</b> left', 0, 0.5, style='margin-top:24px;font-size:44px'),
        MARK('a gullible stand-in model, synthetic data', 1, 0.6)]),

 dict(id='s1', chap='Where we are', say=[
   "We have built, trained, served and shipped an A I system. Now someone will try to break it, or just make an honest mistake that leaks data. Security for A I has one surprise. Most of the damage in real incidents came from the system around the model, not the model itself.",
   "Honest labels. The injection test uses a deliberately gullible scripted stand in, and fake data. The permission checker is my simplified version of cloud policy rules. The personal data test uses thirty made up strings. None of it is a benchmark of a real product."],
  html=[H2('Security for AI systems', 0),
        GRID([('who may call it', 0, 0.3), ('what leaks', 0, 0.7), ('who gets hijacked', 0, 1.1)], cols=3, h=150, fs=36),
        STICKY('Honest label', 'gullible stand-in model · synthetic data · simplified policy checker', 1, 0.5, style='margin-top:26px;font-size:36px')]),

 dict(id='s2', chap='Who secures what', say=[
   "Start with who is responsible. The cloud provider secures the buildings, the machines, the model hosting, and promises not to train on your A P I data. You secure everything about how you use it. Who may call the model, what data goes in, what the answers are used for.",
   "There are five locks. Identity, network, encryption, logging, and application authorisation. A mnemonic is, I need every lock, always. The provider hands you the first four. The fifth, you build yourself."],
  html=[H2('Five locks', 0), SVG('c2', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c2', 'locks', 1000, 290, 1)]),

 dict(id='s3', chap='The request gap', say=[
   "Here is the gap that catches teams out. Identity and access management decides who may call the model. A private network decides which pipe the call travels. A guardrail looks for attacks in the text.",
   "But nothing asks the real question. May this user send this prompt, see this document, or fire this tool? That check is application authorisation, it sits in your code, and most of the incidents in this lesson come from missing it."],
  html=[H2('The request gap', 0),
        LIST([('IAM: who may call the model', 0, 0.4), ('private link: which pipe', 0, 0.9), ('guardrail: is this text an attack?', 0, 1.4), ('nobody asks: may THIS user see THIS document?', 1, 0.4)], kind='ar', style='margin-top:24px;font-size:44px'),
        STICKY('Yours to build', 'application authorisation', 1, 0.9, style='margin-top:22px;font-size:44px')]),

 dict(id='s4', chap='Identity', say=[
   "Identity first. Your service needs to prove who it is to the cloud. The best way is keyless. On Kubernetes, the cluster hands each pod a short lived token, which the cloud exchanges for short lived cloud credentials. Nothing long lived exists to leak.",
   "All three big clouds work this way, with different names. Pod Identity on A W S, Workload Identity on Google and Azure. Prefer it over keys in files, every time."],
  html=[H2('Keyless identity', 0),
        LIST([('the cluster gives each pod a short-lived token', 0, 0.4), ('the cloud swaps it for short-lived credentials', 0, 1.0), ('nothing long-lived exists to leak', 1, 0.3), ('AWS Pod Identity · Google and Azure Workload Identity', 1, 0.9)], kind='ar', style='margin-top:24px;font-size:44px')]),

 dict(id='s5', chap='Least privilege: a test', say=[
   "Least privilege means giving a role only the permissions it needs. I wrote a small policy checker with simplified rules. Anything is denied unless allowed, an explicit deny always wins, and stars match anything. This is my teaching version, not the real cloud engine.",
   "I tested two roles with twelve requests. The narrow role is the notebook's example, allowed to invoke one family of models in one region. The broad role allows everything under the model service, on every resource. An organisation rule also blocks calls outside two approved European regions."],
  html=[H2('Narrow role against broad role', 0),
        OUT(['narrow: invoke ONE model family, ONE region', 'broad:  bedrock:*  on  *', 'org rule: no calls outside two EU regions', '12 requests, from invoking a model to deleting one'], 0, 0.4, size=30, label='setup', style='margin-top:22px'),
        SUB('a simplified checker I wrote, not the real cloud engine', 1, 0.6, style='margin-top:14px')]),

 dict(id='s6', chap='Least privilege, measured', say=[
   "The narrow role was allowed two of the twelve requests. Both were ordinary model calls. The broad role was allowed nine.",
   "Those extra seven included creating a guardrail, starting a fine tuning job, deleting a custom model and changing the logging configuration. A role that only needed to call a model could switch off its own audit trail. The organisation rule still blocked the other regions for both."],
  html=[H2('Allowed out of 12 requests', 0), SVG('c6', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c6', 'iam', 1000, 270, 1)]),

 dict(id='s7', chap='Network and perimeters', say=[
   "Network next. Use private endpoints so calls to the model service never cross the public internet. And turn public access off. If you add a private path but leave the public one on, the private path is only optional.",
   "A stronger control is a perimeter. Google's service controls draw a boundary around the A I service, so even valid credentials cannot copy data or models out of it. It is an anti exfiltration control."],
  html=[H2('Private paths, closed public doors', 0),
        LIST([('private endpoints: no public internet', 0, 0.4), ('turn public access OFF, or the private path is optional', 0, 1.0), ('a perimeter: valid credentials cannot copy data out', 1, 0.4)], kind='ar', style='margin-top:26px;font-size:46px')]),

 dict(id='s8', chap='Secrets and keys', say=[
   "Secrets. Keys for outside model providers and database passwords belong in a secrets manager. Never in an environment file, never in an image, and never in a prompt, because a model can repeat what is in its context.",
   "Use customer managed encryption keys for training data, custom models, vector stores and logs. They let you revoke access yourself, and they leave an audit trail."],
  html=[H2('Secrets stay out of everything', 0),
        LIST([('secrets manager, not .env files or images', 0, 0.4), ('never in a prompt: models can repeat it', 0, 1.0), ('your own encryption keys for data and logs', 1, 0.4)], kind='ar', style='margin-top:26px;font-size:46px')]),

 dict(id='s9', chap='Two kinds of logs', say=[
   "Logs come in two kinds, and people mix them up. The audit log records who called which A P I and when. It does not contain the prompts. A separate invocation log records prompts and answers, and it is off by default.",
   "Both edges are sharp. With no logs, you have no audit trail, and some regulations require one. With logs on, you have created a new store full of personal data and secrets. Encrypt it, restrict access, and set a retention period."],
  html=[H2('Two logs, two risks', 0),
        ROW(COL(CARD('<b>audit log</b><br>who called what, when<br>no prompts', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>prompt log</b><br>prompts + answers<br>off by default', 0, 0.9, style='font-size:38px'), width='48%'), style='margin-top:28px'),
        STICKY('Careful', 'a prompt log is a <b>PII database</b>', 1, 0.6, style='margin-top:24px;font-size:44px')]),

 dict(id='s10', chap='Data use and retention', say=[
   "What happens to your data? All three big clouds commit, by contract, not to train their foundation models on your A P I data. That part is settled. The open questions are retention and residency, and they differ feature by feature.",
   "Some features keep prompts for a while to detect abuse. Zero data retention exists, but you usually must opt in or get approval, and some features rule it out. Residency has traps too, such as endpoints that route requests across regions. Read the provider's page before you promise a customer EU only."],
  html=[H2('Settled and not settled', 0),
        ROW(COL(CARD('<b>settled</b><br>no training on your API data<br>(by contract)', 0, 0.4, style='font-size:36px'), width='48%'),
            COL(CARD('<b>open, per feature</b><br>retention · residency<br>zero data retention', 1, 0.3, style='font-size:36px'), width='48%'), style='margin-top:28px'),
        SUB('read the provider page before promising "EU only"', 1, 1.0, style='margin-top:14px')]),

 dict(id='s11', chap='Personal data: a test', say=[
   "Personal data, called P I I. Redact it at four places. Before embedding documents, because it is hard to find and delete inside vectors. On the prompt. On the output. And before logging.",
   "How good is a simple pattern based redactor? I wrote thirty test strings, with made up people. Emails, phone numbers in several formats, card numbers with a checksum test, names, addresses and ID numbers. Then I measured how many personal items it found."],
  html=[H2('Redact PII at four places', 0),
        LIST([('before embedding documents', 0, 0.4), ('on the prompt and the output', 0, 0.9), ('before logging', 0, 1.4)], kind='ar', style='margin-top:22px;font-size:44px'),
        SUB('test: 30 made-up strings · emails, phones, cards (checksum), names, addresses, IDs', 1, 0.6, style='margin-top:16px')]),

 dict(id='s12', chap='PII, measured', say=[
   "Patterns did fairly well on things with a fixed shape. Emails, eighty-three percent. Phone numbers, eighty-six. Card numbers, eighty. They missed formats like at example dot com, and spoken numbers.",
   "On names, addresses and ID numbers they found nothing, zero. Overall, fifty-eight percent. It also raised false alarms on two of four harmless strings. Real systems add trained recognisers, such as Presidio, Comprehend and Sensitive Data Protection, which I did not test."],
  html=[H2('What patterns can find', 0), SVG('c12', 1400, 420, 'margin:10px auto 0')],
  svgs=[('c12', 'pii', 1000, 320, 1)]),

 dict(id='s13', chap='Confidential computing', say=[
   "A word on confidential computing. It protects data while it is being processed, by running inside encrypted hardware that even the cloud operator cannot read. Azure and Google offer H one hundred machines with it.",
   "It has limits. It is weak against physical attacks, and multi GPU support was limited when the notebook was written. And it does nothing about prompt injection or application leaks. It is a complement to the other locks, not a replacement."],
  html=[H2('Confidential computing', 0),
        LIST([('hides data in use from the cloud operator', 0, 0.4), ('H100 confidential VMs on Azure and Google', 0, 1.0), ('limits: physical attacks, multi-GPU', 1, 0.3), ('does nothing about prompt injection', 1, 0.8)], kind='ar', style='margin-top:24px;font-size:44px'),
        SUB('a complement to the other locks, not a replacement', 1, 1.4, style='margin-top:14px')]),

 dict(id='s14', chap='The OWASP list', say=[
   "There is a standard checklist, the O W A S P top ten for language model applications. Prompt injection is number one. Then sensitive information disclosure, supply chain, data and model poisoning, improper output handling, excessive agency, system prompt leakage, vector and embedding weaknesses, misinformation, and unbounded consumption.",
   "Notice how many of these are about the system, not the model. Output handling, agency, vectors, consumption. That matches what the notebook says about real incidents. Architecture beats model tuning."],
  html=[H2('OWASP top 10 for LLM apps (2025)', 0),
        TABLE(['#', 'Risk'], [(['01', 'prompt injection'], 0, 0.4), (['02', 'sensitive information disclosure'], 0, 0.7), (['05', 'improper output handling'], 0, 1.0), (['06', 'excessive agency'], 1, 0.3), (['08', 'vector and embedding weaknesses'], 1, 0.6), (['10', 'unbounded consumption'], 1, 0.9)], style='margin-top:20px;font-size:36px'),
        SUB('a selection of the ten · notebook, Oct 2026', 1, 1.4, style='margin-top:10px')]),

 dict(id='s15', chap='Two kinds of injection', say=[
   "Prompt injection comes in two kinds. Direct is the user typing something like, ignore your instructions. The attacker is the user, and the harm is a bypassed policy in their own session.",
   "Indirect is far more dangerous. The instruction is hidden in something the model reads. A web page, an email, a P D F, a search result, a calendar invite, a tool's output. The attacker is not the user. The user is the victim."],
  html=[H2('Direct and indirect injection', 0),
        ROW(COL(CARD('<b>direct</b><br>the user types it<br>attacker = user', 0, 0.4, style='font-size:38px'), width='48%'),
            COL(CARD('<b>indirect</b><br>hidden in content the model reads<br>the user is the victim', 1, 0.3, style='font-size:38px'), width='48%'), style='margin-top:28px')]),

 dict(id='s16', chap='How data leaves', say=[
   "How does stolen data actually leave? One well known path is a markdown image. The injected text tells the model to write an image link, with the secret inside the web address. The chat window loads the image automatically, and the secret goes to the attacker. No click needed.",
   "Other paths. A link the user is nudged to click. And any tool that talks outward, such as email, a web fetch, or posting to a ticket. A real case in twenty twenty-five, called EchoLeak, used a hidden instruction in an email to make an assistant leak data with no clicks."],
  html=[H2('How data leaves', 0),
        LIST([('markdown image: secret hidden in the web address', 0, 0.4), ('the chat loads it automatically: no click', 0, 1.0), ('links, email, web fetch, ticket comments', 1, 0.3), ('real case: EchoLeak (2025), zero clicks', 1, 0.8)], kind='ar', style='margin-top:24px;font-size:42px')]),

 dict(id='s17', chap='The lethal trifecta', say=[
   "A way to think about it. An agent that has all three of these can be tricked into stealing. Untrusted content it reads. Private data it can access. And a way to act outwards, such as email, links or images.",
   "Meta proposed the rule of two. Until injection can be reliably detected, give an agent at most two of three. Untrusted input, sensitive data, and the power to change things or communicate. If it needs all three, a human approves. Pick two."],
  html=[H2('The lethal trifecta', 0), SVG('c17', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c17', 'trifecta', 1000, 290, 1)]),

 dict(id='s18', chap='My injection experiment', say=[
   "Let me test it. A support assistant answers a customer using their private record and a help article. An attacker has poisoned the article. I wrote twelve attacks, in different wording. Some are blunt. Some are polite. Some use spacing, number swaps, or French.",
   "The model is a stand in that obeys any instruction it finds, the worst case. Real models resist some attacks, but injection is unsolved, so we design as if they do not. Three setups. Nothing. A keyword filter. And an allowlist on what can leave."],
  html=[H2('Twelve attacks, three setups', 0),
        OUT(['A  nothing in place', 'B  keyword filter on retrieved text', 'C  egress allowlist: email only to the customer, images only from our own domain'], 0, 0.4, size=30, label='setups', style='margin-top:22px'),
        SUB('worst-case stand-in model · my own wording, some written to dodge the filter', 1, 0.6, style='margin-top:14px')]),

 dict(id='s19', chap='Nothing in place', say=[
   "With nothing in place, the stand in was fooled twelve times out of twelve, and the private record left the system twelve times. Either by email, or inside an image address.",
   "That is the baseline. If your assistant can read untrusted text, see private data and reach the outside world, assume it will leak."],
  html=[H2('Setup A: nothing in place', 0), SVG('c19', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c19', 'path', 1000, 290, 1)]),

 dict(id='s20', chap='The keyword filter', say=[
   "Setup B added a keyword filter that blocks phrases like, ignore previous instructions. It stopped three attacks. Nine got through, and the record left nine times.",
   "Which ones? A polite request to send the order history. An administrator claiming authority. A note for quality assurance. The two image attacks. And the versions with spaces between letters, a zero for an o, French, and a plain instruction with no trigger words at all. You cannot list every way to say it."],
  html=[H2('Setup B: a keyword filter', 0),
        OUT(['stopped:  3 of 12', 'got through:  9 of 12', '  polite request · fake admin · "for QA"', '  image attacks · "i g n o r e" · "Ign0re" · French'], 0, 0.4, size=30, label='measured', style='margin-top:22px'),
        MARK('you cannot list every way to say it', 1, 0.6)]),

 dict(id='s21', chap='Design beats filters', say=[
   "Setup C changed no wording rules. The model was just as gullible, and was fooled twelve times. But outbound email could only go to the customer's own address, and images only loaded from our own domain.",
   "The record left the system zero times. The model was fooled and it did not matter. That is the principle. Break any link in the chain, and the leak stops. Filters guess about words. An allowlist controls the door."],
  html=[H2('Setup C: control the door', 0), SVG('c21', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c21', 'inject', 1000, 290, 1)]),

 dict(id='s22', chap='Defence in depth', say=[
   "So how do you defend? Use filters and classifiers as one cheap layer, never the only one. Give the model least privilege tools. Put approvals before anything irreversible. Restrict outbound email, links and images. Run code in sandboxes.",
   "And test attacks yourself. Open source tools such as garak and PyRIT run attack suites against your system, and a catalogue called Mitre Atlas maps the tactics. Treat any single defence as bypassable."],
  html=[H2('Layers, not a single filter', 0),
        LIST([('filters: one cheap layer, never the only one', 0, 0.4), ('least-privilege tools and approvals', 0, 0.9), ('egress allowlists, sandboxes', 0, 1.4), ('attack your own system: garak, PyRIT, MITRE ATLAS', 1, 0.4)], kind='ar', style='margin-top:24px;font-size:44px')]),

 dict(id='s23', chap='Leaks between customers', say=[
   "The next leak needs no attacker at all. In lesson eight we said to filter by who is asking. Here is the test. Five thousand synthetic documents across five customers, with similar text. A user from customer two asks two hundred questions, and we ask for the top five results.",
   "Three designs. No filter. Filter after the search, which drops other customers' documents from the top five. And filter inside the search, so only that customer's documents are ever searched."],
  html=[H2('Three ways to filter', 0),
        OUT(['5,000 synthetic documents · 5 customers', 'a customer-2 user asks 200 questions · top 5 wanted', 'no filter · filter AFTER search · filter IN search'], 0, 0.4, size=30, label='measured setup', style='margin-top:22px'),
        SUB('synthetic data, real search', 1, 0.6, style='margin-top:14px')]),

 dict(id='s24', chap='Tenant leak, measured', say=[
   "With no filter, eight hundred and thirty-three of the thousand results shown belonged to someone else. Eighty-three percent.",
   "Filtering after the search leaked nothing, but returned only point eight three documents per question, because most of the top five belonged to other customers. Filtering inside the search leaked nothing and returned all five. The filter belongs inside the search."],
  html=[H2('Other customers\' documents shown', 0), SVG('c24', 1400, 400, 'margin:14px auto 0')],
  svgs=[('c24', 'tenant', 1000, 290, 1)]),

 dict(id='s25', chap='Excessive agency', say=[
   "Agents add more risks. Excessive agency means a model given more tools, permissions or freedom than the job needs. Give an agent a delete tool it never uses, and one injected sentence can use it.",
   "A newer list covers agents specifically. Goal hijacking, tool misuse, identity abuse, poisoned memory, rogue agents. The common fix is the same. Minimal, scoped tools, short lived credentials, human approval for irreversible steps, and a sandbox."],
  html=[H2('Excessive agency', 0),
        LIST([('a tool the agent never needs = a tool an attacker can use', 0, 0.4), ('minimal, scoped tools', 1, 0.3), ('short-lived credentials', 1, 0.7), ('human approval for irreversible steps', 1, 1.1)], kind='ar', style='margin-top:26px;font-size:44px')]),

 dict(id='s26', chap='Supply chain', say=[
   "Supply chain risks. Many model files are stored in a format called pickle, which can run code when loaded. Downloading a model can mean running a stranger's program. Prefer the safer tensor format, pin versions, and check signatures.",
   "The same goes for packages, M C P servers, plugins and prompts from outside. In twenty twenty-five, researchers found models on a public hub with booby trapped files that slipped past scanners. Treat third party models and tools like third party code."],
  html=[H2('Models are code', 0),
        LIST([('pickle model files can run code when loaded', 0, 0.4), ('prefer safetensors · pin versions · check signatures', 0, 1.0), ('same for packages, MCP servers, plugins', 1, 0.3), ('treat third-party models like third-party code', 1, 0.8)], kind='ar', style='margin-top:24px;font-size:44px')]),

 dict(id='s27', chap='Denial of wallet', say=[
   "One more risk is about money. Unbounded consumption, also called denial of wallet. An attacker, or a bug, can make your assistant burn tokens, with endless loops or huge inputs, until the bill is the attack.",
   "Cap everything. Tokens per request, requests per user, steps per agent run, and a budget alarm per team. Lesson five showed how fast loops cost, so a cap is a safety feature."],
  html=[H2('Denial of wallet', 0),
        LIST([('tokens per request', 0, 0.4), ('requests per user', 0, 0.8), ('steps per agent run', 0, 1.2), ('a budget alarm per team', 1, 0.4)], kind='ok', style='margin-top:26px;font-size:46px'),
        SUB('the bill can be the attack', 1, 0.9, style='margin-top:14px')]),

 dict(id='s28', chap='Governance basics', say=[
   "Governance. Rules about A I are arriving. In the European Union, the A I Act's obligations for general purpose models and its transparency rules became live in August twenty twenty-six, while rules for high risk systems were pushed later, to December twenty twenty-seven and August twenty twenty-eight. Deferred, not cancelled.",
   "In health care, whether the B A A covers your A I feature is decided feature by feature. And two habits help everywhere. Keep an inventory of every A I system, and keep logs. They are your evidence. This is not legal advice."],
  html=[H2('Governance basics', 0),
        TABLE(['Item', 'Note (notebook, Oct 2026)'], [(['EU AI Act', 'general-purpose rules + transparency live Aug 2026'], 0, 0.4), (['high-risk systems', 'pushed to Dec 2027 and Aug 2028'], 0, 0.9), (['HIPAA / BAA', 'check each feature'], 1, 0.3), (['always', 'an AI inventory + logs = your evidence'], 1, 0.8)], style='margin-top:12px;font-size:34px'),
        SUB('not legal advice', 1, 1.4, style='margin-top:6px')]),

 dict(id='s29', chap='ShopNest Copilot', say=[
   "For ShopNest Copilot. Pods use keyless identity and a role that can only invoke the one approved model in the approved regions. Keys live in a secrets manager. Private endpoints, public access off. Prompt logs encrypted, with tight access and a short retention.",
   "The retrieval search filters by customer inside the query. Retrieved text is data, not commands. The assistant may email only the customer's own address, and show images only from our own domain. And the refund tool needs human approval, as in lesson nine."],
  html=[H2('ShopNest Copilot: security plan', 0),
        TABLE(['Lock', 'Plan'], [(['identity', 'keyless; one role, one approved model'], 0, 0.4), (['network, keys, logs', 'private endpoints, secrets manager, encrypted logs'], 0, 0.9), (['data', 'tenant filter inside the search'], 1, 0.3), (['agency', 'egress allowlist, refund approval'], 1, 0.8)], style='margin-top:12px;font-size:32px')]),

 dict(id='s30', chap='Four words to keep', say=[
   "Four words to carry forward. Least privilege: only the permissions needed. Prompt injection: instructions hidden in text the model reads.",
   "Egress allowlist: a short list of places data may go. And tenant filter: a rule, inside the search, so one customer never sees another's data."],
  html=[H2('Four words to keep', 0),
        GRID([('<b>least privilege</b>', 0, 0.3), ('<b>prompt injection</b>', 0, 0.9), ('<b>egress allowlist</b>', 1, 0.3), ('<b>tenant filter</b>', 1, 0.9)], cols=2, h=140, fs=42, style='margin-top:30px')]),

 dict(id='s31', chap='Interview corner', say=[
   "Interview corner. Asked how you defend against prompt injection, say: assume it cannot be fully filtered, so limit the damage. Least privilege tools, egress allowlists, human approval for risky actions. In my test a keyword filter stopped three of twelve attacks, while an egress allowlist left zero leaks.",
   "Asked how you stop one customer seeing another's data in a R A G system, say: store access metadata on every chunk and filter inside the search. In my test, with no filter, eighty-three percent of results belonged to someone else."],
  html=[H2('Interview corner', 0),
        Q('How do you defend against prompt injection?', 'Assume it gets through. Filter: 3 of 12. Allowlist: 0 leaks.', 0, 0.4),
        Q('Stopping cross-customer leaks in RAG?', 'Filter INSIDE the search. No filter: 83% not yours.', 1, 0.4)]),

 dict(id='s32', chap='Your turn', say=[
   "Your turn. The zip for this lesson has four scripts. The injection experiment, the tenant leak test, the policy checker and the personal data test. Add a fourth setup to the injection test, with an approval step, and see what changes.",
   "Then write attacks of your own that beat my filter. One changed number teaches more than an hour of reading."],
  html=[H2('Your turn', 0),
        CARD('<b>l10_injection_toy.py</b>: add your own attacks and setups.<br><b>l10_tenant_leak.py</b> · <b>l10_iam_check.py</b> · <b>l10_pii_redact.py</b>', 0, 0.4, style='margin-top:22px;font-size:36px'),
        SUB('one changed number teaches more than an hour of reading', 1, 0.8, style='margin-top:16px')]),

 dict(id='s33', chap='Recap', say=[
   "Recap. Five locks, and you build the last, application authorisation. A broad role allowed nine of twelve requests, including deleting models, against two for a narrow one. Pattern based redaction found fifty-eight percent of personal data, and zero names.",
   "A keyword filter stopped three of twelve injections. An egress allowlist left zero leaks, even though the model was fooled every time. Filter inside the search, or eighty-three percent of results can be someone else's. Next lesson: cost and Fin Ops."],
  html=[H2('Recap', 0),
        GRID([('5 locks · you build the 5th', 0, 0.3), ('broad role: 9 of 12 allowed', 0, 0.9), ('PII patterns: 58%, names 0%', 0, 1.5),
              ('filter: 3 of 12 stopped', 1, 0.3), ('allowlist: 0 leaks', 1, 0.9), ('tenant filter inside search', 1, 1.5)], cols=3, h=150, fs=30)]),
]
