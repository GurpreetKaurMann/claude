import sys; sys.path.insert(0, '/home/claude/caigen')
from cai_lib import *
from c12_diagrams import DIAGRAMS
from c12_long import LONG
from c12_notes import NOTES

L = dict(
 code='CAI-12', num=12, num_word='twelve', slug='Your_Learning_Path', final=True,
 title='Your Learning Path', title_html='Your learning<br>path', title_size=120,
 tagline='From zero to cloud AI engineer, in 16 weeks.', module='Module 5 · Safe, cheap, and your career',
 toc=['Six stops', 'Projects and done-when checks', 'Time and money', 'The forgotten GPU', 'Certificates in 2026', 'What employers ask', 'The claims ledger'],
 data_label='Course project', project='ShopNest Copilot', project_desc='the AI support assistant we moved to the cloud, step by step',
 prev='CAI-11', next=('🎉', '<b>Thank you for learning with me.</b> Go and build your first project this week.'),
 next_say='That was the last lesson of the course. Thank you for learning with me. Now go and build your first project.',
 diagrams=DIAGRAMS, long=LONG, notes=NOTES,
 glow=dict(a='ZERO TO CLOUD', b='AI ENGINEER', icons=['trophy1', '>', 'check2']),
 thumb=dict(title='16-week<br><span class="hl">roadmap</span>', size=120, sub='zero to cloud AI engineer', chips=('160 hours', '$150-250'), mini='mini_thumb'),

 short1=mk_short(1, 'One_Forgotten_GPU_Costs_More_Than_The_Whole_Path', "One forgotten G P U can cost more than learning the entire cloud A I path. Here is the sum.",
   ('$365-876', 'ONE FORGOTTEN GPU', 100, 100),
   ["A G P U node left up for a month is seven hundred thirty hours at fifty cents to a dollar twenty. That is three hundred sixty-five to eight hundred seventy-six dollars, estimated.",
    "The whole sixteen week learning path adds up to at most about a hundred fifty-five dollars in project estimates. So after every lab, destroy, then list your clusters and expect nothing."],
   'mini_forgot', "Destroy it, then check the list.", 'Rule', 'teardown<br>after <b>every</b> lab', dict(title='One GPU left on<br><span class="hl">costs $876</span>', size=96, sub='more than the whole path', mini='mini_forgot'),
   dict(title='One Forgotten GPU Costs More Than the Whole Cloud AI Path #shorts',
     desc="Arithmetic on the notebook's estimates (Oct 2026):\\n• one L4 node left up a month: 730 h x $0.50-1.20 = $365 to $876\\n• sum of the six stops' project estimates: $32 to $155 before credits\\n• habit: terraform destroy, then list clusters and expect nothing; check billing every Friday\\n\\nFull lesson: Cloud for AI Engineers, lesson 12.",
     tags='shorts, cloud cost, gpu cost, ai engineer roadmap, finops, terraform destroy, learn cloud ai, cloud for ai engineers, the code notebook',
     pinned='Have you ever left a GPU running by accident? 👇')),

 short2=mk_short(2, 'The_6_Stop_Cloud_AI_Roadmap_In_16_Weeks', "Zero to cloud A I engineer in sixteen weeks. Six stops, in a specific order, and the order has a reason.",
   ('16 WEEKS', '6 STOPS', 130, 150),
   ["Cloud basics, containers, serving, retrieval with evaluations, MLOps, then distributed training. Each stop uses the one before, and the rarest, most expensive one goes last.",
    "Frugal Coders Spend Really Modest Dollars. About ten hours a week, a hundred and sixty hours. Every stop ends with a project and a done when check."],
   'mini_thumb', "Order matters. Cheapest first.", 'Mnemonic', 'F · C · S · R · M · D', dict(title='6 stops.<br><span class="hl">16 weeks.</span>', size=110, sub='cloud AI engineer roadmap', mini='mini_thumb'),
   dict(title='The 16-Week Cloud AI Engineer Roadmap (6 Stops, Frugal Coders) #shorts',
     desc="The notebook's learning path (Oct 2026), order is my own synthesis:\\n• F Fundamentals, C Containers, S Serving, R RAG + evals, M MLOps, D Distributed\\n• about 10 h/week for 16 weeks = 160 hours (my assumption)\\n• each stop ends with a project and a 'done when' check\\n• notebook estimate: $150-250 out of pocket if you tear everything down\\n\\nFull lesson: Cloud for AI Engineers, lesson 12.",
     tags='shorts, ai engineer roadmap, cloud ai roadmap, learn cloud, mlops roadmap, kubernetes, vllm, cloud for ai engineers, the code notebook',
     pinned='Which stop are you on? 👇')),

 reel=mk_reel('3_AI_Certs_Were_Retired_In_2026', ["Three popular cloud A I certificates were retired in twenty twenty-six.",
   "The A W S Machine Learning Specialty in March. The Azure A I Engineer exam in June. And the Azure Data Scientist exam in June. Who went mad, M L S, A I one oh two, D P one hundred. Check the exam code before you book. Projects beat badges anyway."],
   "Check the code first. Save this.", 'RETIRED', ['MLS-C01 · AI-102 · DP-100', 'check the exam code first'], [3.0, 5.6], 'Rule', 'check the<br><b>exam code</b>',
   dict(title='3 AI certs<br><span class="hl">were retired</span>', size=100, sub='check the code first', mini='mini_cert'),
   dict(title='3 popular cloud AI certs were retired in 2026 (check before you book)',
     caption="Before you book an exam 📜\\n\\nRetired in 2026 (notebook list, Oct 2026):\\n❌ AWS ML Specialty MLS-C01 (last exam Mar 31)\\n❌ Azure AI Engineer AI-102 (Jun 30)\\n❌ Azure Data Scientist DP-100 (Jun 1)\\n\\nWho went MAD. Always check the exam code on the official page first, and remember: projects beat badges. Save this. Full roadmap on YouTube: The Code Notebook.",
     pinned="That was the last lesson of Cloud for AI Engineers 🎉 Follow for the next course!")),

 upload=dict(
   title='The 16-Week Cloud AI Engineer Roadmap (Under $250 If You Avoid This Mistake)',
   hook="Lesson 12 of Cloud for AI Engineers, the finale. The notebook's six-stop path from zero to cloud AI engineer takes about 16 weeks at 10 hours a week and an estimated $150-250 out of pocket, if you tear everything down. One forgotten GPU for a month costs $365-876.",
   what="We cover the six stops (fundamentals, containers and Kubernetes, serving, RAG and agents with evals, MLOps, distributed training) and why that order, a project and a 'done when' check for every stop, the timeline (160 hours), the cost (sum of project estimates, credits, free GPU notebooks), the forgotten-GPU mistake and the teardown habit, cheap GPUs by stop, the 2026 certificate churn (MLS-C01, AI-102 and DP-100 retired) and which cert fits which stop, books and courses, what employers ask for (a 43,480-posting sample), and a claims ledger that checks 32 headline numbers from lessons 1-11 against their saved results. Prices, exam codes and posting figures are dated notebook estimates and the stage order is my own synthesis.",
   bullets=['Six stops: F-C-S-R-M-D (Frugal Coders Spend Really Modest Dollars)', 'Why run RAG and agents alongside stops 2-3', 'A project and a done-when check for every stop', '16 weeks, 160 hours: change the hours in the script', 'What it costs: $150-250 notebook estimate, credits and free GPUs',
            'The forgotten GPU: $365-876 a month, and the teardown habit', 'Cheap GPUs by stop', 'Certificates retired in 2026 and which to take', 'Books and courses: a minimal stack', 'What employers ask for: Python 62%, cloud 55%, foundation models 51%',
            'Name projects in the posting\'s words', 'The claims ledger: 32 of 32 headline numbers found in their saved results', 'ShopNest Copilot: the whole plan', 'Your first week', 'Interview questions with answers'],
   hashtags='#cloudcomputing #aiengineer #roadmap #mlops #learntocode',
   tags='ai engineer roadmap, cloud ai roadmap, how to become an ai engineer, mlops roadmap, aws ai certification 2026, kubernetes for ai, gpu cost, terraform destroy, cloud for ai engineers, the code notebook',
   pinned="Prices, exam codes and posting figures are dated notebook estimates (Oct 2026), and the stage order is my own synthesis. 🎓\\n\\nQuestion for you 👇\\nWhich stop are you starting at, and what project will you build first?"),
)

import interview; L['notes'] = interview.add(L['notes'], L['num'])
