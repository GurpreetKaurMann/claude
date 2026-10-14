import sys; sys.path.insert(0, '/home/claude/caigen')
from cai_lib import *
from c10_diagrams import DIAGRAMS
from c10_long import LONG
from c10_notes import NOTES

L = dict(
 code='CAI-10', num=10, num_word='ten', slug='Security_And_Governance',
 title='Security and Governance', title_html='Security &amp;<br>governance', title_size=120,
 tagline='Why the filter failed, and the design that held.', module='Module 5 · Safe, cheap, and your career',
 toc=['Five locks', 'Least privilege, tested', 'Personal data', 'Prompt injection', 'The injection experiment', 'Leaks between customers', 'Governance basics'],
 data_label='Course project', project='ShopNest Copilot', project_desc='the AI support assistant we move to the cloud, step by step',
 prev='CAI-09', next=('CAI-11', '<b>Cost and FinOps</b>: GPU utilisation, token economics and the break-even sum'),
 next_say='cost and fin ops. GPU use, token costs, and the break even sum.',
 diagrams=DIAGRAMS, long=LONG, notes=NOTES,
 glow=dict(a='SECURITY', b='AND GOVERNANCE', icons=['shield1', '>', 'check2']),
 thumb=dict(title='Security &amp;<br><span class="hl">governance</span>', size=110, sub='filter 3 of 12', chips=('filter: 3 of 12', 'design: 0 leaks'), mini='mini_thumb'),

 short1=mk_short(1, 'My_Prompt_Injection_Filter_Stopped_3_Of_12', "I wrote a filter to stop prompt injection. It stopped three of twelve attacks. Here is what worked instead.",
   ('FILTER: 3 OF 12', 'DESIGN: 0 LEAKS', 100, 100),
   ["In my toy test the model is deliberately gullible and obeys any instruction it reads. With nothing in place, all twelve attacks leaked the private record. A keyword filter stopped three.",
    "The fix was not better words. It was an allowlist on what can leave. The model was still fooled twelve times, but zero records left. Control the door."],
   'mini_inject', "Filters guess about words. Allowlists control the door.", 'Rule', 'limit what can<br><b>leave</b>', dict(title='Filter: 3 of 12.<br><span class="hl">Design: 0 leaks</span>', size=88, sub='prompt injection, tested', mini='mini_inject'),
   dict(title='My Prompt Injection Filter Stopped 3 of 12 Attacks (What Worked) #shorts',
     desc="Toy test: a deliberately gullible stand-in model (not a real LLM), 12 attack variants written by me, some to dodge the filter.\\n• nothing in place: record left 12 of 12\\n• keyword filter: 9 of 12 left (it stopped 3)\\n• egress allowlist (email only to the customer, images only from our domain): the model was fooled 12 of 12, 0 left\\n\\nFull lesson: Cloud for AI Engineers, lesson 10.",
     tags='shorts, prompt injection, llm security, egress allowlist, indirect prompt injection, ai agent security, cloud for ai engineers, the code notebook',
     pinned='Do you rely on a filter or on design? 👇')),

 short2=mk_short(2, 'No_Tenant_Filter_83_Percent_Leak', "Without a permission filter in my RAG search, eighty-three percent of the results belonged to someone else.",
   ('83%', 'NOT YOURS', 170, 120),
   ["I built five thousand synthetic documents across five customers, and a user from customer two asked two hundred questions. With no filter, eight hundred and thirty-three of a thousand results were another customer's.",
    "Filtering after the search leaked nothing but returned under one document per question. Filtering inside the search returned all five and leaked none."],
   'mini_tenant', "Put the permission filter inside the search.", 'Rule', 'filter <b>inside</b><br>the search', dict(title='83% of results<br><span class="hl">not yours</span>', size=96, sub='RAG without a tenant filter', mini='mini_tenant'),
   dict(title='RAG Without a Permission Filter: 83% of Results Were Someone Else\'s #shorts',
     desc="5,000 synthetic documents, 5 customers, a customer-2 user asks 200 questions (top 5):\\n• no filter: 833 of 1,000 results were another customer's\\n• filter after search: 0 leaked, but only 0.83 documents returned per question\\n• filter inside the search: 0 leaked, 5.00 documents returned\\n\\nFull lesson: Cloud for AI Engineers, lesson 10.",
     tags='shorts, rag security, multi-tenant rag, data leak, access control, vector database permissions, cloud for ai engineers, the code notebook',
     pinned='Is your RAG filter inside the search or after it? 👇')),

 reel=mk_reel('A_Broad_IAM_Role_Can_Delete_Your_Models', ["Why a broad cloud role is dangerous for an A I app.",
   "I checked twelve requests against two roles with a small policy checker. The narrow role, one model family in one region, was allowed two. The broad role, everything under the model service, was allowed nine, including deleting a model and changing the logging."],
   "Give it only what it needs. Save this.", '9 VS 2', ['broad role: 9 of 12 allowed', 'narrow role: 2 of 12'], [3.2, 5.8], 'Rule', 'only what it<br><b>needs</b>',
   dict(title='A broad role<br><span class="hl">can delete models</span>', size=100, sub='9 of 12 vs 2 of 12', mini='mini_iam'),
   dict(title='A broad cloud role can delete your models and switch off logging',
     caption="Least privilege, tested. 🔐\\n\\n12 requests, checked with a simplified policy checker (my teaching version, not the real cloud engine):\\n🟢 narrow role (one model family, one region): 2 allowed\\n🔴 broad role (everything under the model service): 9 allowed, including deleting a custom model and changing the logging configuration\\n\\nGive it only what it needs. Save this. Full lesson on YouTube: The Code Notebook.",
     pinned="Lesson 11 next: cost and FinOps 💸 Follow so you don't miss it!")),

 upload=dict(
   title='Prompt Injection Explained: Why My Filter Failed and the Design That Worked (Tested)',
   hook="Lesson 10 of Cloud for AI Engineers. I wrote 12 prompt injection attacks and a keyword filter. It stopped 3. With nothing in place all 12 stole the record. With an egress allowlist the model was fooled 12 times and nothing left.",
   what="We cover the five locks (identity, network, encryption, logging, application authorisation), the request gap, keyless identity, a least-privilege policy test (narrow role 2 of 12, broad role 9 of 12), private endpoints and perimeters, secrets, the two kinds of logs, data use and retention, PII redaction measured (58% overall, 0% of names), confidential computing, the OWASP LLM top 10, direct and indirect injection, how data leaves, the lethal trifecta and the Rule of Two, a 12-attack injection experiment, cross-customer leaks in RAG (83% without a filter), excessive agency, supply chain, denial of wallet and governance basics. The injection test uses a deliberately gullible scripted stand-in model, the data is synthetic, and the policy checker is a simplified teaching version.",
   bullets=['Who secures what, and the five locks', 'The request gap: nobody checks THIS user for THIS document', 'Keyless identity', 'Least privilege tested: broad role 9 of 12 allowed, narrow role 2', 'Private endpoints, perimeters, secrets and encryption keys',
            'Two kinds of logs, and why a prompt log is a PII database', 'PII redaction measured: 58% overall, 0% of names', 'The OWASP top 10 for LLM apps', 'Direct vs indirect prompt injection and how data leaves', 'The lethal trifecta and the Rule of Two',
            'The experiment: nothing 12/12 leaked, filter 9/12, egress allowlist 0/12', 'RAG tenant leak: 83% of results not yours without a filter', 'Excessive agency, supply chain and denial of wallet', 'Governance basics (not legal advice)', 'ShopNest Copilot security plan', 'Interview questions with answers'],
   hashtags='#aisecurity #promptinjection #llm #cloudsecurity #aiengineering',
   tags='prompt injection explained, llm security, egress allowlist, lethal trifecta, rule of two, owasp llm top 10, rag permissions, least privilege iam, pii redaction, ai agent security, cloud for ai engineers, the code notebook',
   pinned="The injection test uses a deliberately gullible stand-in model with synthetic data, the policy checker is a simplified teaching version, and the PII test uses 30 made-up strings. 📊\\n\\nQuestion for you 👇\\nWhich surprised you more: a filter stopping only 3 of 12, or 83% of RAG results belonging to someone else?"),
)
