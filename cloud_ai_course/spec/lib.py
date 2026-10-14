import os, sys, json, asyncio, importlib.util, re, shutil, subprocess, html as H
sys.path.insert(0, '/home/claude/video/engine')
import build as B          # engine/build.py (TTS + timeline + render)
import soundfile as sf

VID = '/home/claude/video'
NOTES_DIR = '/home/claude/build'
OUT_ROOT = '/home/user/claude/course_output/Cloud_for_AI_Course'
from theme import THEME, COURSE
VOICE = 'af_heart'

def _esc_code(t):
    """escape raw < > inside code (keeps existing &lt; entities)"""
    return t.replace('<', '&lt;').replace('>', '&gt;')
def _esc_pre(h):
    return re.sub(r'(<pre class="code"[^>]*>)(.*?)(</pre>)', lambda m: '<div>' + m.group(1) + _esc_code(m.group(2)) + m.group(3) + '</div>', h, flags=re.S)

def say_fix(t):
    rep = [('ShopNest', 'Shop Nest'), ('gRPC', 'G R P C'), ('QLoRA', 'Q Lora'), ('LLMs', 'L L Ms'), ('LLM', 'L L M'), ('LoRA', 'Lora'), ('MCP', 'M C P'), ('BM25', 'B M 25'), ('HNSW', 'H N S W'), ('top-k', 'top k'), ('top-p', 'top p'), ('GPUs', 'G P Us'), ('GPU', 'G P U'), ('CPU', 'C P U'), ('KV', 'K V'), ('PII', 'P I I'), ('ReAct', 'react'), ('GGUF', 'G G U F'), ('RRF', 'R R F'), ('IVF', 'I V F'), ('TTFT', 'T T F T'), ('p95', 'P 95'), ('p50', 'P 50'), ('kNN', 'K N N'), ('k-NN', 'K N N'), ('A2A', 'A to A'), ('SDK', 'S D K'), ('OWASP', 'oh wasp'), ('RPC', 'R P C'), ('BPE', 'B P E'), ('DevOps', 'dev ops'), ('DDD', 'D D D'),
           ('JSON', 'Jason'), ('Protobuf', 'proto buff'), ('HTTP/2', 'HTTP 2'), ('HTTP/1.1', 'HTTP 1 point 1'),
           ('e.g.', 'for example'), ('i.e.', 'that is'), ('SQL', 'sequel'), ('UI', 'U I'), ('CRUD', 'crud')]
    for a, b in rep: t = t.replace(a, b)
    t = re.sub(r'(\d)\s?ms\b', r'\1 milliseconds', t)
    return t

def load(path):
    spec = importlib.util.spec_from_file_location('L', path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m.L

def outdir(L):
    d = f'{OUT_ROOT}/{L["code"]}_{L["slug"]}'
    os.makedirs(d, exist_ok=True); return d

def diag_js(L):
    clamp = ("function CL(d,mx){if(mx<0)return d;var w=Object.assign({},d);"
             "w.at=function(a,dl,du){var m=String(a).match(/^(.*)\\.(\\d+)$/);"
             "if(m&&+m[2]>mx)a=m[1]+'.'+mx;d.at(a,dl,du);return w;};return w;}\n")
    return clamp + '\n'.join(f'function DG_{k}(d,S){{{v}}}' for k, v in L['diagrams'].items())

# ------------------------------------------------------------------ NOTES
def _nb(b, L):
    t = b[0]
    if t == 'h2': return f'<h2><span class="num">{b[1]}</span>{b[2]}</h2>'
    if t == 'h3': return f'<h3>{b[1]}</h3>'
    if t == 'p': return f'<p>{b[1]}</p>'
    if t == 'def': return f'<div class="def">{b[1]}</div>'
    if t == 'list':
        style, items = b[1], b[2]
        if style == 'ol': return '<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'
        return f'<ul class="{style}">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
    if t == 'cols': return '<div class="cols">' + ''.join('<div>' + ''.join(_nb(x, L) for x in c) + '</div>' for c in b[1:]) + '</div>'
    if t == 'sticky':
        color, tag, html = b[1], b[2], b[3]
        return f'<div class="sticky {color}"><span class="tag">{tag}</span>{html}</div>'
    if t == 'card':
        style = b[2] if len(b) > 2 else ''
        return f'<div class="card" style="{style}">{b[1]}</div>'
    if t == 'table':
        hd, rows = b[1], b[2]
        return '<table class="hand"><tr>' + ''.join(f'<th>{h}</th>' for h in hd) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>'
    if t == 'diagram':
        name, hmm, vw, vh = b[1], b[2], b[3], b[4]
        sid = f'nd_{name}_{abs(hash(str(b)))%10000}'
        L['_nd'].append((sid, name, vw, vh))
        return f'<svg class="dia" id="{sid}" style="height:{hmm}mm"></svg>'
    if t == 'code': return f'<div><span class="code">{_esc_code(b[1])}</span></div>'
    if t == 'jcode':
        import gailab as _ll
        return f'<div><span class="code">{_ll.jhl(_esc_code(b[1]))}</span></div>'
    if t in ('pycode', 'yamlcode', 'shcode'):
        import gailab as _ll
        fn = {'pycode': _ll.phl, 'yamlcode': _ll.shl, 'shcode': _ll.shl}[t]
        return f'<div><span class="code">{fn(_esc_code(b[1]))}</span></div>'
    if t == 'ask':
        # an interview question with the answer to say out loud, and the trap under it
        q, a, trap = b[1], b[2], (b[3] if len(b) > 3 else '')
        tr = f'<div class="small" style="margin-top:6px"><b style="color:var(--orange)">Trap →</b> {trap}</div>' if trap else ''
        return (f'<div class="card" style="border-left:6px solid var(--teal);padding-left:16px">'
                f'<div style="font-family:Caveat;font-size:1.25em;color:var(--teal)">\u201c{q}\u201d</div>'
                f'<div style="margin-top:4px">{a}</div>{tr}</div>')
    if t == 'qa': return ''.join(f'<div class="qa"><div class="q">{q}</div><div class="a">{a}</div></div>' for q, a in b[1])
    if t == 'revise':
        l, r = b[1], b[2]
        ul = lambda xs: '<ul class="arrow small">' + ''.join(f'<li>{x}</li>' for x in xs) + '</ul>'
        return f'<div class="card" style="border-color:var(--orange);border-width:2.5px"><h3 style="margin-top:0">⚡ Revise in 60 seconds</h3><div class="cols">{ul(l)}{ul(r)}</div></div>'
    if t == 'next':
        return f'<div class="sticky green"><span class="tag">{("Course complete" if b[1]=="🎉" else "Next lesson → " + b[1])}</span>{b[2]}<br><span class="small">Watch on YouTube: <b>@TheCodeNotebook</b> · Notes: <b>thecodenotebook.com</b></span></div>'
    if t == 'raw': return b[1]
    raise ValueError(t)

def build_notes(L):
    L['_nd'] = []
    pages = []
    n = len(L['notes'])
    for i, blocks in enumerate(L['notes']):
        body = ''
        if i == 0:
            toc = ' &nbsp; '.join(f'{c} {s}' for c, s in zip('①②③④⑤⑥⑦⑧⑨', L['toc']))
            body += (f'<h1>{L["title"]}</h1><div class="subtitle">Lesson {L["num"]} of 12 · {L["tagline"]}</div>'
                     f'<div class="card small"><b class="teal">In this lesson →</b> {toc}'
                     f'<br><b class="blue">{L.get("data_label", "Module dataset")}:</b> '
                     f'<span class="hl">{L.get("project", COURSE["project"])}</span>, {L.get("project_desc", COURSE["project_desc"])}.</div>')
        body += ''.join(_nb(b, L) for b in blocks)
        right = L['module'] if i == 0 else L['title']
        pages.append(f'''<section class="page"><div class="hdr"><span><span class="sticker">{L["code"]}</span> &nbsp;{COURSE['notebook']}</span><span>{right}</span></div>
{body}<div class="ftr"><span>thecodenotebook.com</span><span>{L["code"]} · page {i+1}</span></div></section>''')
    calls = '\n'.join(f"DG_{name}(D('{sid}',{vw},{vh},0.75),'x');" for sid, name, vw, vh in L['_nd'])
    html = f'''<!doctype html><html><head><meta charset="utf-8"><title>{L["code"]} {L["title"]} · Notes</title>
<link rel="stylesheet" href="notebook.css"><script src="node_modules/roughjs/bundled/rough.js"></script>
<script src="../video/engine/engine.js"></script><script>{THEME["js"]}</script>
<style>{THEME["notes_css"]}.dia text{{font-family:Kalam}} .code{{display:inline-block;white-space:pre;font-size:14px;line-height:1.4;background:#1f2937;color:#e5e7eb;border-radius:8px;padding:8px 14px}}</style></head><body>
{''.join(pages)}
<script>{diag_js(L)}
{calls}</script></body></html>'''
    src = f'{NOTES_DIR}/{L["code"]}.html'
    open(src, 'w').write(html)
    pdf = f'{outdir(L)}/{L["code"]}_{L["slug"]}_Notes.pdf'
    asyncio.run(_pdf(src, pdf))
    return pdf

def build_revision(L):
    """A dense, night-before-the-interview PDF: the answers and the numbers only."""
    L['_nd'] = []
    pages = []
    for i, blocks in enumerate(L['revision']):
        body = ''
        if i == 0:
            body += (f'<h1>{L["title"]}</h1>'
                     f'<div class="subtitle">Revision pack · Session {L["num"]} of 5 · everything measured</div>')
        body += ''.join(_nb(b, L) for b in blocks)
        pages.append(f'''<section class="page rv"><div class="hdr"><span><span class="sticker">{L["code"]}</span> &nbsp;Revision pack</span><span>{L["title"]}</span></div>
{body}<div class="ftr"><span>thecodenotebook.com</span><span>{L["code"]} revision · page {i+1}</span></div></section>''')
    calls = '\n'.join(f"DG_{name}(D('{sid}',{vw},{vh},0.75),'x');" for sid, name, vw, vh in L['_nd'])
    dense = (".rv{font-size:13.5px;line-height:1.38} .rv h2{font-size:23px;margin:10px 0 6px}"
             ".rv h3{font-size:17px;margin:8px 0 3px} .rv .card{padding:8px 12px;margin:6px 0}"
             ".rv ul,.rv ol{margin:4px 0 4px 18px} .rv li{margin:2px 0} .rv p{margin:4px 0}"
             ".rv table.hand{font-size:12.5px} .rv table.hand td,.rv table.hand th{padding:3px 7px}"
             ".rv .sticky{padding:8px 12px;margin:6px 0} .rv .def{padding:7px 12px;margin:5px 0}"
             ".rv .code{font-size:12.5px;line-height:1.32;padding:6px 11px}"
             ".rv .qa{margin:4px 0} .rv .cols{gap:14px}")
    html = f'''<!doctype html><html><head><meta charset="utf-8"><title>{L["code"]} {L["title"]} · Revision pack</title>
<link rel="stylesheet" href="notebook.css"><script src="node_modules/roughjs/bundled/rough.js"></script>
<script src="../video/engine/engine.js"></script><script>{THEME["js"]}</script>
<style>{THEME["notes_css"]}.dia text{{font-family:Kalam}} .code{{display:inline-block;white-space:pre;font-size:14px;line-height:1.4;background:#1f2937;color:#e5e7eb;border-radius:8px;padding:8px 14px}}{dense}</style></head><body>
{''.join(pages)}
<script>{diag_js(L)}
{calls}</script></body></html>'''
    src = f'{NOTES_DIR}/{L["code"]}_rev.html'
    open(src, 'w').write(html)
    pdf = f'{outdir(L)}/{L["code"]}_{L["slug"]}_Revision_Pack.pdf'
    asyncio.run(_pdf(src, pdf))
    return pdf

async def _pdf(src, out):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 900, 'height': 1200})
        await pg.goto('file://' + src); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
        ov = await pg.evaluate('''[...document.querySelectorAll('.page')].map((p,i)=>{
          const f=p.querySelector('.ftr').getBoundingClientRect(); let m=0;
          p.querySelectorAll(':scope > *:not(.ftr):not(.hdr)').forEach(e=>{m=Math.max(m,e.getBoundingClientRect().bottom)});
          return Math.round(f.top-m)})''')
        print('  notes free space per page (px):', ov)
        if min(ov) < 0: print('  !!! OVERFLOW on a notes page')
        await pg.pdf(path=out, format='A4', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
        await b.close()

# ------------------------------------------------------------------ VIDEO HTML
LONG_CSS = '''
@font-face{font-family:P;src:url(../engine/fonts/poppins-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:P;src:url(../engine/fonts/poppins-latin-600-normal.woff2);font-weight:600}

#stage.h .def,#stage.h .card,#stage.h .q,#stage.h .gridc{width:fit-content;max-width:100%}
#stage.h .outp,#stage.h .codep{width:max-content;max-width:none}
#stage.h h2{white-space:nowrap}
#stage.h .rule{height:auto!important;min-height:112px;min-width:400px}
#stage.h .def,#stage.h .card,#stage.h .q .aa,#stage.h .q .qq,#stage.h .sub,#stage.h .rule,#stage.h td,#stage.h .sticky,#stage.h .li{text-wrap:balance}
#stage.h table.vt{width:auto}
#stage.h .scene{padding-bottom:0!important}

#stage.v #cap{font-size:86px;line-height:1.18;bottom:300px;left:40px;right:40px}
.tab{border:4px solid var(--teal);border-radius:16px;padding:16px 26px;background:#fff;font-size:42px}
.rule{border:4px solid var(--teal);border-radius:18px;background:#fff;padding:22px 26px;font-size:46px;display:flex;gap:24px;align-items:center;line-height:1.25}
.rule .n{flex:none;width:76px;height:76px;border-radius:50%;background:var(--teal);color:#fff;font-family:Caveat;font-weight:700;font-size:56px;text-align:center;line-height:74px}
.q{border:4px solid var(--blue);border-radius:18px;background:#fff;padding:14px 32px;margin:0 0 20px;font-size:48px}
.q .qq{font-weight:700;color:var(--blue)} .q .qq::before{content:"Q. ";font-family:Caveat;color:var(--orange);font-size:1.3em}
.q .aa{font-size:40px}
.qs .q{padding:12px 28px;margin:0 0 16px;font-size:42px;line-height:1.2} .qs .q .aa{font-size:35px;line-height:1.22} .qs .q .qq .n{color:#6b7280;font-weight:400}
table.vt{border-collapse:collapse;width:100%;background:#fff;font-size:40px;line-height:1.3}
table.vt th{font-family:Caveat;font-size:54px;color:#fff;background:var(--teal);padding:6px 20px;text-align:left}
table.vt th:nth-child(2){background:var(--blue)}
table.vt td{border:3px solid rgba(15,118,110,.4);padding:10px 20px;vertical-align:top}
table.vt td:first-child{font-weight:700;color:var(--teal)}
'''

def _avatar_block(size, line2, seg_attr):
    return (f'<div{seg_attr} data-fx="pop" style="margin-top:60px;display:flex;align-items:center;gap:30px;justify-content:center">'
            f'<img src="../engine/avatar.png" style="width:{size}px;height:{size}px"><div style="text-align:left">'
            f'<div style="font-family:Caveat;font-weight:700;font-size:76px;color:var(--blue);line-height:1">The Code Notebook</div>'
            f'<div style="font-size:44px;color:var(--red);font-weight:700">{line2}</div></div></div>')

VFIT_JS = r'''(function(){
  let TOP=190, BOT=1340, LX=60, RX=1020, MAX=2.2;
  function ink(s){
    let t=1e9,b=-1e9,l=1e9,r=-1e9, got=false;
    s.querySelectorAll('*').forEach(e=>{
      const tag=e.tagName.toLowerCase();
      if(tag==='svg'){
        // map the drawing's real bbox through getScreenCTM: this honours the
        // viewBox + preserveAspectRatio letterboxing, which naive
        // rect.width/viewBox.width does NOT (it over-reported ink by ~1.8x).
        let bb, m; try{ bb=e.getBBox(); m=e.getScreenCTM(); }catch(_){ return; }
        if(!bb || !bb.width || !m) return;
        const P=(x,y)=>({x:m.a*x+m.c*y+m.e, y:m.b*x+m.d*y+m.f});
        const pts=[P(bb.x,bb.y),P(bb.x+bb.width,bb.y),P(bb.x,bb.y+bb.height),P(bb.x+bb.width,bb.y+bb.height)];
        pts.forEach(p=>{t=Math.min(t,p.y);b=Math.max(b,p.y);l=Math.min(l,p.x);r=Math.max(r,p.x);});
        got=true; return;
      }
      if(e.closest('svg')) return;                       // svg internals handled above
      if(e.children.length && tag!=='img') return;       // containers are full-width: skip
      let q;
      if(tag!=='img' && e.firstChild){                    // measure the TEXT, not the block box
        const rg=document.createRange(); rg.selectNodeContents(e); q=rg.getBoundingClientRect();
        const box=e.getBoundingClientRect();              // keep borders/background of chips & cards
        const cs=getComputedStyle(e);
        if(cs.borderWidth!=='0px'||cs.backgroundColor!=='rgba(0, 0, 0, 0)'||cs.boxShadow!=='none'){
          q={top:Math.min(q.top,box.top),bottom:Math.max(q.bottom,box.bottom),
             left:(cs.display==='inline'||cs.display==='inline-block')?Math.min(q.left,box.left):q.left,
             right:(cs.display==='inline'||cs.display==='inline-block')?Math.max(q.right,box.right):q.right,
             width:1,height:1};
        }
      } else { q=e.getBoundingClientRect(); }
      if(q && (q.right-q.left)>0 && (q.bottom-q.top)>0){ t=Math.min(t,q.top);b=Math.max(b,q.bottom);l=Math.min(l,q.left);r=Math.max(r,q.right);got=true; }
    });
    return got?{t,b,l,r}:null;
  }
  // ---- long (horizontal) video: scale each slide's content to fill the frame ----
  function inkH(s){
    let t=1e9,b=-1e9,l=1e9,r=-1e9, got=false;
    const add=q=>{ if(q && q.width>0 && q.height>0){ t=Math.min(t,q.top);b=Math.max(b,q.bottom);l=Math.min(l,q.left);r=Math.max(r,q.right);got=true; } };
    s.querySelectorAll('*').forEach(e=>{
      const tag=e.tagName.toLowerCase();
      if(tag==='svg'){
        let bb, m; try{ bb=e.getBBox(); m=e.getScreenCTM(); }catch(_){ return; }
        if(!bb || !bb.width || !m) return;
        const P=(x,y)=>({x:m.a*x+m.c*y+m.e, y:m.b*x+m.d*y+m.f});
        [P(bb.x,bb.y),P(bb.x+bb.width,bb.y),P(bb.x,bb.y+bb.height),P(bb.x+bb.width,bb.y+bb.height)].forEach(p=>{
          t=Math.min(t,p.y);b=Math.max(b,p.y);l=Math.min(l,p.x);r=Math.max(r,p.x);}); got=true; return;
      }
      if(e.closest('svg')) return;
      if(tag==='img'){ add(e.getBoundingClientRect()); return; }
      const cs=getComputedStyle(e);
      if(parseFloat(cs.borderTopWidth)>0||parseFloat(cs.borderLeftWidth)>0||cs.backgroundColor!=='rgba(0, 0, 0, 0)'||cs.boxShadow!=='none'||cs.backgroundImage!=='none')
        add(e.getBoundingClientRect());                    // a visible box: its whole rectangle counts
      e.childNodes.forEach(n=>{ if(n.nodeType===3 && n.textContent.trim()){ const rg=document.createRange(); rg.selectNode(n); add(rg.getBoundingClientRect()); } });
    });
    return got?{t,b,l,r}:null;
  }
  window.hfit=function(){
    // Try a narrower layout width W/s and scale by s, largest s first: text re-wraps, so wide
    // text-heavy slides grow taller instead of staying small. Falls back to a plain shrink.
    const TOP=44, BOT=968, LX=92, RX=1856, AW=RX-LX, AH=BOT-TOP;
    document.querySelectorAll('.scene').forEach(s=>{
      const prev=s.style.display; s.style.display='block'; s.style.transform='none';
      let best=null;
      for(let z=1.6; z>=0.999; z-=0.05){
        s.style.right='auto'; s.style.width=(1920/z)+'px';
        const k=inkH(s); if(!k) break;
        if((k.r-k.l)*z<=AW && (k.b-k.t)*z<=AH){ best={k,z}; break; }
      }
      if(!best){ s.style.width='1920px'; const k=inkH(s); if(!k){ s.style.display=prev; return; }
        best={k, z:Math.max(0.6, Math.min(AW/(k.r-k.l), AH/(k.b-k.t)))}; }
      const k=best.k, z=best.z, cx=(k.l+k.r)/2, cy=(k.t+k.b)/2;
      s.style.transformOrigin=cx+'px '+cy+'px';
      s.style.transform='translate('+(((LX+RX)/2)-cx)+'px,'+(((TOP+BOT)/2)-cy)+'px) scale('+z+')';
      s.dataset.hfit=z.toFixed(2);
      s.style.display=prev;
    });
  };
  window.vfit=function(){
    const st=document.getElementById('stage');
    if(!st) return;
    if(st.classList.contains('h')) return window.hfit();
    if(!st.classList.contains('v')) return;
    document.querySelectorAll('.scene').forEach(s=>{
      const prev=s.style.display; s.style.display='block'; s.style.transform='none';
      const k=ink(s);
      if(!k){ s.style.display=prev; return; }
      const w=k.r-k.l, h=k.b-k.t;
      const sc=Math.max(1, Math.min((RX-LX)/w, (BOT-TOP)/h, MAX));
      const cx=(k.l+k.r)/2, cy=(k.t+k.b)/2;
      s.style.transformOrigin=cx+'px '+cy+'px';
      s.style.transform='translate('+(((LX+RX)/2)-cx)+'px,'+(((TOP+BOT)/2)-cy)+'px) scale('+sc+')';
      s.dataset.vfit=sc.toFixed(2);
      s.style.display=prev;
    });
  };
})();
'''

def page_html(L, scenes, orient, brand_right='The Code Notebook'):
    secs, calls = [], []
    for sc in scenes:
        sid = sc['id']
        body = _esc_pre(''.join(sc['html'])).replace('§', sid)
        secs.append(f'<section class="scene" id="{sid}">{body}</section>')
        _mx = len(sc['say']) - 1
        for (svgid, name, w, h, s) in sc.get('svgs', []):
            calls.append(f"DG_{name}(CL(D('{svgid}',{w},{h},{s}),{_mx}),'{sid}');")
    cap = '<div id="cap"></div>' if orient == 'v' else ''
    lab = COURSE['name'] + ' Course' if orient == 'h' else COURSE['name']
    return f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../engine/stage.css">
<script src="../engine/rough.js"></script><script src="../engine/engine.js"></script><style>{LONG_CSS}{THEME["stage_css"]}</style><script>{THEME["js"]}</script></head><body>
<div id="stage" class="{orient}"><div class="brand"><span><span class="sticker">{L["code"]}</span>{lab}</span><span class="ch"><img src="../engine/avatar.png">{brand_right}</span></div>{cap}
{''.join(secs)}</div>
<script>{VFIT_JS}</script>
<script>{diag_js(L)}
{chr(10).join(calls)}</script></body></html>'''

def title_scene(L):
    return dict(id='st', chap='Intro', say=[
        f"Welcome to lesson {L['num_word']} of the {COURSE['say']} course, on The Code Notebook.",
        "The handwritten notes and the code for this lesson are linked in the description."],
        html=[f'''<div class="row" style="align-items:center;gap:70px;padding-top:60px">
    <div data-at="§.0" data-fx="pop" style="flex:none;text-align:center">
      <img src="../engine/avatar.png" style="width:440px;height:440px;display:block">
      <div style="font-family:Caveat;font-weight:700;font-size:60px;color:var(--blue);margin-top:6px">The Code Notebook</div>
      <div class="gray" style="font-size:34px">Gurpreet · @TheCodeNotebook</div></div>
    <div class="col">
      <div data-at="§.0" data-d="0.3"><span class="sticker" style="font-size:60px">Lesson {L["num"]} of 12</span></div>
      <h1 data-at="§.0" data-d="0.6" style="font-size:{L.get("title_size",130)}px;margin-top:24px">{L["title_html"]}</h1>
      <div class="sub" data-at="§.0" data-d="1.0" style="font-size:54px">{COURSE['name']} · {L["module"]}</div>
      <div class="card" data-at="§.1" style="display:inline-block;margin-top:40px;font-size:42px">Free handwritten notes → <b class="blue">thecodenotebook.com</b></div>
    </div></div>'''])

def end_scene(L):
    nc, nt = L['next']
    return dict(id='se', chap='Next lesson', hold=14.0, say=[
        (L['next_say'] if L.get('final') else f"In the next lesson: {L['next_say']}"),
        "Subscribe so you don't miss it. See you in the notebook."],
        html=[f'''<div style="width:880px;padding-top:30px">
    <div class="sticky green" data-at="§.0" data-rot="-2"><span class="tag">{'Course complete 🎉' if L.get('final') else f'Next → Lesson {int(nc.split("-")[1])}'}</span>{nt}</div>
    <div class="row" data-at="§.1" style="margin-top:60px;align-items:center;gap:36px">
      <img src="../engine/avatar.png" style="width:280px;height:280px;flex:none">
      <div><div style="font-family:Caveat;font-weight:700;font-size:100px;color:var(--red);line-height:1">Subscribe!</div>
        <div style="font-family:Caveat;font-weight:700;font-size:60px;color:var(--blue)">The Code Notebook</div>
        <div class="gray" style="font-size:36px">@TheCodeNotebook</div></div></div>
    <div class="sub" data-at="§.1" data-d="1.5" style="margin-top:30px">See you in the notebook ✏</div></div>'''])

def long_scenes(L):
    sc = list(L['long'])
    return [sc[0], title_scene(L)] + sc[1:] + [end_scene(L)]

def vertical_scenes(L, key):
    V = L[key]
    scenes = [dict(s) for s in V['scenes']]
    last = scenes[-1]
    nseg = len(last['say']) - 1
    line2 = 'Follow @thecodenotebookyt' if key.startswith('reel') else 'Subscribe for the full course'
    last['html'] = list(last['html']) + [_avatar_block(210, line2, f' data-at="§.{nseg}"')]
    return scenes

async def _render_run(V, TL, total, mp4, wav):
    await B.render(V, TL, total, mp4, wav)

def build_video(L, kind):
    """kind: long | short1 | short2 | short3 | reel"""
    if kind == 'long':
        scenes, orient = long_scenes(L), 'h'
        name = f'{L["code"]}_Lesson_{L["slug"]}'
        extra = dict(speed=1.0, gap=0.35, scene_gap=0.9, captions=False)
    else:
        scenes, orient = vertical_scenes(L, kind), 'v'
        V0 = L[kind]
        name = f'{L["code"]}_{"Reel1" if kind=="reel" else kind.capitalize()}_{V0["slug"]}'
        extra = dict(speed=V0.get('speed', 1.05), gap=0.25, scene_gap=0.4, captions=True)
    brand = '@thecodenotebookyt' if kind.startswith('reel') else 'The Code Notebook'
    html_path = f'{VID}/gen/{L["code"]}_{kind}.html'
    open(html_path, 'w').write(page_html(L, scenes, orient, brand))
    V = dict(name=name, html=html_path, orient=orient, voice=VOICE, say=say_fix,
             hold={s['id']: s.get('hold', 0) for s in scenes},
             scenes=[(s['id'], s['say']) for s in scenes], **extra)
    TL, wav, srt, total = B.build_timeline(V)
    os.makedirs(f'{VID}/out', exist_ok=True)
    wav_path = f'{VID}/out/{name}.wav'; sf.write(wav_path, wav, B.SR)
    raw = f'{VID}/out/{name}.mp4'
    print(f'  {name}: {total:.1f}s')
    asyncio.run(B.render(V, TL, total, raw, wav_path))
    od = outdir(L)
    final = f'{od}/{name}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11',
                    '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', final], check=True)
    if kind == 'long':
        with open(f'{od}/{L["code"]}_Lesson_English_Subtitles.srt', 'w') as f:
            for i, (s, e, tx) in enumerate(srt, 1): f.write(f'{i}\n{B.fmt(s)} --> {B.fmt(e)}\n{tx}\n\n')
    chapters = []
    for s in scenes:
        sid = s['id']; st = [x for x in TL['scenes'] if x[0] == sid][0][1]
        if s.get('chap'): chapters.append((0 if not chapters else st, s['chap']))
    json.dump(dict(total=total, chapters=chapters), open(f'{VID}/out/{name}.meta.json', 'w'))
    return dict(name=name, total=total, chapters=chapters, scenes=scenes)

def preview(L, kind, times=None):
    """render a few still frames for checking layout (at scene ends if times None)"""
    if kind == 'long': scenes, orient = long_scenes(L), 'h'
    else: scenes, orient = vertical_scenes(L, kind), 'v'
    html_path = f'{VID}/gen/{L["code"]}_{kind}.html'
    open(html_path, 'w').write(page_html(L, scenes, orient))
    V = dict(name=f'pv_{L["code"]}_{kind}', html=html_path, orient=orient, voice=VOICE, say=say_fix,
             hold={s['id']: s.get('hold', 0) for s in scenes}, scenes=[(s['id'], s['say']) for s in scenes],
             captions=(orient == 'v'), gap=0.3, scene_gap=0.6)
    TL, wav, srt, total = B.build_timeline(V)
    ts = times or [round(e - 0.3, 2) for _, s, e in TL['scenes']]
    asyncio.run(B.render(V, TL, total, None, None, preview=ts))
    return [f'{VID}/preview_{V["name"]}_{t}.png' for t in ts]

# ------------------------------------------------------------------ COVERS
COVER_CSS = open(f'{VID}/ms01/thumbs4.html').read().split('<style>')[1].split('</style>')[0]

def build_covers(L):
    T = L['thumb']
    right = '''<div class="blob" style="right:90px;top:140px;width:720px;height:720px;background:var(--sky)"></div>
  <img class="a face" src="../engine/avatar.png" style="right:215px;top:230px;width:470px;height:470px">
  <div class="a" style="right:0;width:900px;top:735px;text-align:center"><span class="nametag" style="font-size:40px">Gurpreet</span></div>
  <div class="a" style="right:70px;bottom:40px;font-family:P;font-weight:700;font-size:36px;color:#64748b">The Code Notebook</div>'''
    thumb = f'''<div class="cv H skybg dots" id="thumb">{right}
  <div class="a label" style="left:90px;top:90px;font-size:40px">{COURSE['name']} · Lesson {L["num"]:02d}</div>
  <div class="a h" style="left:84px;top:165px;font-size:{T.get("size",128)}px">{T["title"]}</div>
  <div class="a" style="left:92px;top:{T.get("sub_top",450)}px;font-size:50px;font-weight:600;color:var(--ink);line-height:1.3">{T["sub"]}</div>
  <div class="a" style="left:90px;top:{T.get("chip_top",620)}px;display:flex;gap:18px">
    <span class="hchip" style="font-size:40px;color:var(--teal);border-color:var(--teal)">{T["chips"][0]}</span>
    <span class="hchip" style="font-size:40px;color:var(--coral);border-color:var(--coral)">{T["chips"][1]}</span></div>
  <div class="a card" style="left:90px;top:730px;width:760px;height:260px"><svg id="m_thumb" width="760" height="260" style="left:0;top:0"></svg></div>
</div>'''
    vcovers = []
    for key, bg in [('short1', 'cream'), ('short2', 'skybg'), ('short3', 'cream'), ('reel', 'sagebg')]:
        C = L[key]['cover']
        top = 330 if key == 'reel' else 250   # reel: keep key content inside centre 1080x1350
        vcovers.append(f'''<div class="cv V {bg} dots" id="c_{key}">
  <div class="blob" style="left:190px;top:{top+830}px;width:700px;height:700px;background:{'#fff' if key=='reel' else 'var(--sky)' if bg=='skybg' else 'var(--sage)'};opacity:.9"></div>
  <div class="a label" style="left:0;right:0;top:{top}px;text-align:center;font-size:36px">{C["label"]}</div>
  <div class="a h" style="left:40px;right:40px;top:{top+80}px;text-align:center;font-size:{C.get("size",130)}px">{C["title"]}</div>
  <div class="a" style="left:0;right:0;top:{top+C.get("sub_off",500)}px;text-align:center;font-size:48px;font-weight:600;color:var(--ink);line-height:1.3">{C["sub"]}</div>
  <div class="a card" style="left:140px;top:{top+C.get("card_off",650)}px;width:800px;height:280px"><svg id="m_{key}" width="800" height="280" style="left:0;top:0"></svg></div>
  <img class="a face" src="../engine/avatar.png" style="left:400px;top:{top+C.get("card_off",650)+320}px;width:280px;height:280px">
  <div class="a" style="left:0;right:0;top:{top+C.get("card_off",650)+620}px;text-align:center"><span class="nametag" style="font-size:36px">Gurpreet</span></div>
  <div class="a" style="left:0;right:0;top:{top+C.get("card_off",650)+700}px;text-align:center;font-family:P;font-weight:800;color:var(--navy);font-size:46px">{'@thecodenotebookyt' if key=='reel' else 'The Code Notebook'}</div>
</div>''')
    minis = '\n'.join(f"DG_{m}(D('{sid}',760,260,1),'x');" for sid, m in
                      [('m_thumb', T['mini']), ('m_short1', L['short1']['cover']['mini']), ('m_short2', L['short2']['cover']['mini']), ('m_reel', L['reel']['cover']['mini'])])
    html = f'''<!doctype html><html><head><meta charset="utf-8"><script src="../engine/rough.js"></script><script src="../engine/engine.js"></script>
<style>{COVER_CSS}{THEME["cover_css"]}</style><script>{THEME["js"]}</script></head><body>{thumb}{''.join(vcovers)}
<script>const N='#1f2a44',TT='#2f7f79',SG='#d6ebe7',CO='#d9775b',SK='#dbe7f5';{diag_js(L)}
{minis}</script></body></html>'''
    p = f'{VID}/ms01/gen_{L["code"]}_covers.html'   # same folder depth as thumbs4 for relative paths
    open(p, 'w').write(html)
    od = outdir(L)
    outs = [('thumb', f'{L["code"]}_Thumbnail.png', (1280, 720)), ('c_short1', f'{L["code"]}_Short1_Cover.png', None),
            ('c_short2', f'{L["code"]}_Short2_Cover.png', None), ('c_reel', f'{L["code"]}_Reel_Cover_Instagram.png', None)]
    asyncio.run(_shots(p, [(i, f'{od}/{n}', r) for i, n, r in outs]))
    return [f'{od}/{n}' for _, n, _ in outs]

async def _shots(src, items):
    from playwright.async_api import async_playwright
    from PIL import Image
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1920, 'height': 1080})
        await pg.goto('file://' + src); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
        for i, out, r in items:
            tmp = out + '.tmp.png'
            await pg.locator('#' + i).screenshot(path=tmp)
            im = Image.open(tmp).convert('RGB')
            if r: im = im.resize(r, Image.LANCZOS)
            im.save(out); os.remove(tmp)
        await b.close()

# ------------------------------------------------------------------ DOCS
def fmt_t(s):
    s = int(round(s)); return f'{s//60}:{s%60:02d}'

def write_docs(L, metas):
    od = outdir(L); U = L['upload']
    long = metas['long']
    chap = '\n'.join(f'{fmt_t(t)} {c}' for t, c in long['chapters'])
    # ---- scripts
    s = [f'# {L["code"]} · {L["title"]}: Scripts\n', f'**Lesson {L["num"]} of 12 · {L["module"]}**\n',
         f'Voice: AI narrator (Kokoro `{VOICE}`). Final lesson video length: {fmt_t(long["total"])}.\n', '## Long video narration\n']
    for sc in long['scenes']:
        s.append(f'**[{sc.get("chap") or sc["id"]}]**\n')
        s += [f'> {x}\n' for x in sc['say']]
    for key, lab in [('short1', 'Short 1'), ('short2', 'Short 2'), ('reel', 'Instagram Reel 1')]:
        s.append(f'\n## {lab}: {L[key]["upload"]["title"]}\n')
        for sc in L[key]['scenes']: s += [f'> {x}\n' for x in sc['say']]
    open(f'{od}/{L["code"]}_Scripts.md', 'w').write('\n'.join(s))
    # ---- upload copy
    desc = f'''{U["hook"]}
{U["what"]}
{"" if L["prev"]=="—" else "⏮️ Previous lesson: <" + L["prev"] + " link>" + chr(10)}
In this lesson:
{chr(10).join("✅ " + b for b in U["bullets"])}

⏱️ Chapters
{chap}

{(H.unescape(re.sub("<[^>]+>", "", L["next"][1]))) if L.get("final") else ("Next lesson → " + L["next"][0] + ": " + H.unescape(re.sub("<[^>]+>", "", L["next"][1])))}

🌐 Website: https://thecodenotebook.com/
📸 Instagram: https://www.instagram.com/thecodenotebookyt/

{U["hashtags"]}'''
    out = [f'# {L["code"]} Upload Copy\n', '## 1. Lesson video (YouTube)\n', f'**Title:** {U["title"]}\n',
           '**Description:**\n```\n' + desc + '\n```\n', '**Tags:**\n```\n' + U['tags'] + '\n```\n',
           '**Pinned comment:**\n```\n' + U['pinned'] + '\n```\n', f'**Thumbnail:** {L["code"]}_Thumbnail.png\n', '---\n']
    for i, key in enumerate(['short1', 'short2'], 2):
        S = L[key]['upload']
        out += [f'## {i}. Short {i-1} (YouTube Shorts)\n', f'**Title:** {S["title"]}\n', '**Description:**\n```\n' + S['desc'] + '\n```\n',
                '**Tags:**\n```\n' + S['tags'] + '\n```\n', '**Pinned comment:**\n```\n' + S['pinned'] + '\n```\n',
                f'**Cover:** {L["code"]}_Short{i-1}_Cover.png\n', '---\n']
    for j, key in enumerate(['reel'], 1):
        R = L[key]['upload']
        out += [f'## {3+j}. Instagram Reel {j}\n', '**Caption:**\n```\n' + R['caption'] + '\n```\n', '**First comment (pin it):**\n```\n' + R['pinned'] + '\n```\n',
                f'**Cover:** {L["code"]}_Reel{j}_Cover_Instagram.png\n', '---\n']
    if os.path.exists(f'{od}/{L["code"]}_Code.zip'):
        out += ['## 5. Code for this lesson\n', f'`{L["code"]}_Code.zip` — upload it to the lesson page on thecodenotebook.com and link it in the description.\n']
    p = f'{od}/{L["code"]}_Upload_Copy.md'
    open(p, 'w').write('\n'.join(out))
    return p


# System Design course: new cover layouts
import gaicovers as _sdc
build_covers = _sdc.build_covers
