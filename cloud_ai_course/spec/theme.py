import os
COURSE = dict(name='Cloud for AI', say='cloud for A I engineers', notebook='Cloud Notebook',
              project='ShopNest Copilot', project_desc='the AI support assistant we move to the cloud, step by step')
THEMES = {
 # A: Indigo on dot-grid paper
 'indigo': dict(p='#4338ca', soft='#e0e7ff', tint='#eef0fb', tint2='#e6e9f8', grid='67,56,202', paper='#fdfcf9', style='dots'),
 # B: Terracotta on lined engineering pad
 'terracotta': dict(acc='#d69e2e', acc_dark='#b7791f', p='#b4532a', soft='#fde6d8', tint='#fbf1ea', tint2='#f7e7dc', grid='180,83,42', paper='#fffcf7', style='lines'),
 # C: Plum on square graph paper
 'plum': dict(p='#86198f', soft='#f5e1f7', tint='#f8eff9', tint2='#f2e4f4', grid='134,25,143', paper='#fdfbfd', style='graph'),
 # E: Pine on square graph paper (Low-Level Design course)
 'pine': dict(acc='#ea580c', acc_dark='#9a3412', p='#0f766e', soft='#cce9e5', tint='#eefaf8', tint2='#ddf2ee',
              grid='15,118,110', paper='#fbfdfc', style='graph'),
 # F: Cobalt on lined engineering pad (Senior Java Interview course)
 'cobalt': dict(acc='#f59e0b', acc_dark='#b45309', p='#1d4ed8', soft='#d7e3ff', tint='#eef3ff', tint2='#dfe8ff',
                grid='29,78,216', paper='#fcfdff', style='lines'),
 # G: Orchid on square graph paper (Generative AI course)
 'orchid': dict(acc='#0891b2', acc_dark='#155e75', p='#a21caf', soft='#f5d0fe', tint='#fdf4ff', tint2='#fae8ff',
                grid='162,28,175', paper='#fffdff', style='graph'),
 # H: Rose on dot-grid paper (Cloud for AI Engineers course)
 'rose': dict(acc='#0e7490', acc_dark='#155e75', p='#be123c', soft='#ffe0e6', tint='#fff1f3', tint2='#ffe4e9',
              grid='190,18,60', paper='#fffdfd', style='dots'),
 # D: Violet on dot-grid lab paper (Data Science course)
 'violet': dict(acc='#db2777', acc_dark='#9d174d', p='#4f46e5', soft='#e3e0fd', tint='#f1f0fc', tint2='#e7e5fb',
                grid='79,70,229', paper='#fdfcfa', style='dots'),
}
T = THEMES[os.environ.get('GAI_THEME', 'rose')]
g = T['grid']
if T['style'] == 'dots':
    page_bg = f"background-image:radial-gradient(rgba({g},.28) 1.1px,transparent 1.3px);background-size:5mm 5mm"
    stage_bg = f"background-image:radial-gradient(rgba({g},.30) 2.4px,transparent 2.8px);background-size:48px 48px"
elif T['style'] == 'lines':
    page_bg = f"background-image:linear-gradient(rgba({g},.16) 1px,transparent 1px);background-size:100% 7mm"
    stage_bg = f"background-image:linear-gradient(rgba({g},.16) 2px,transparent 2px);background-size:100% 64px"
else:
    page_bg = (f"background-image:linear-gradient(rgba({g},.16) 1px,transparent 1px),linear-gradient(90deg,rgba({g},.16) 1px,transparent 1px),"
               f"linear-gradient(rgba({g},.07) 1px,transparent 1px),linear-gradient(90deg,rgba({g},.07) 1px,transparent 1px);background-size:25mm 25mm,25mm 25mm,5mm 5mm,5mm 5mm")
    stage_bg = (f"background-image:linear-gradient(rgba({g},.15) 1.5px,transparent 1.5px),linear-gradient(90deg,rgba({g},.15) 1.5px,transparent 1.5px);background-size:48px 48px")
p, soft = T['p'], T['soft']
THEME = dict(
 notes_css=f":root{{--teal:{p};--teal-soft:{soft};--paper:{T['paper']}}} .page{{{page_bg}!important;background-color:var(--paper)!important}} ",
 stage_css=f":root{{--teal:{p};--tealSoft:{soft};--acc:{T.get('acc','#e07a5f')};--paper:{T['paper']}}} #stage{{{stage_bg}!important}} ",
 cover_css=f":root{{--teal:{p};--sage:{soft};--sky:{T['tint2']}}} .skybg{{background:{T['tint']}}} .sagebg{{background:{T['tint']}}} .cream{{background:#faf8f3}} ",
 js=f"window.addEventListener('DOMContentLoaded',()=>{{}});if(typeof C!=='undefined'){{C.teal='{p}';C.tealSoft='{soft}';}}",
)

# ---- new layout (System Design course): side rail, bottom brand bar, marker headings ----
NAVY, ACC = '#1e2440', T.get('acc', '#e07a5f')
THEME['notes_css'] += (
 f".page{{padding-left:21mm!important}} .page::before{{left:0!important;width:8mm;border:none!important;background:{p}}}"
 f".page::after{{content:'CLOUD NOTEBOOK';position:absolute;left:4mm;top:50%;transform:translate(-50%,-50%) rotate(-90deg);"
 f"font-family:Caveat;font-weight:700;font-size:16px;letter-spacing:4px;color:#fff;white-space:nowrap}}"
 f".hdr{{left:21mm!important;color:{NAVY}}} .ftr{{left:21mm!important}} .sticker{{transform:none;border-radius:999px;padding:0 12px;background:{p}}}"
 f"h2{{color:{NAVY}!important;border-bottom:2.5px dashed {ACC}!important}} h2 .num{{background:{p};color:#fff;border-color:{p}!important;border-radius:6px!important}}"
 f"h1{{color:{p}!important}} .subtitle{{color:{ACC}!important}}")
THEME['stage_css'] += (
 f"#stage.h::before{{left:0!important;width:22px;border:none!important;background:{p}}}"
 f"#stage.h .brand{{top:auto!important;bottom:22px;left:70px!important;right:50px}} #stage.h .scene{{padding:60px 90px 120px 110px!important}}"
 f".sticker{{transform:none!important;border-radius:999px!important;box-shadow:none!important;background:{p}!important}}"
 f"h2{{color:{NAVY}!important;border-bottom:none!important;background:linear-gradient(transparent 60%,{soft} 60%,{soft} 92%,transparent 92%);padding:0 12px!important}}"
 f"#cap span{{box-shadow:0 0 0 12px #fff, 6px 8px 0 12px {p}!important}} #cap b{{color:{p}!important}}")
