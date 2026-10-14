"""New cover/thumbnail layouts for the System Design course."""
import os, asyncio
import lib
from theme import THEME, COURSE, T

FONTS = '''@font-face{font-family:P;src:url(../engine/fonts/poppins-latin-500-normal.woff2);font-weight:500}
@font-face{font-family:P;src:url(../engine/fonts/poppins-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:P;src:url(../engine/fonts/poppins-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:P;src:url(../engine/fonts/poppins-latin-800-normal.woff2);font-weight:800}
@font-face{font-family:Caveat;src:url(../engine/fonts/caveat-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:Kalam;src:url(../engine/fonts/kalam-latin-700-normal.woff2);font-weight:700}'''

def css():
    p, soft, tint = T['p'], T['soft'], T['tint']
    return FONTS + f'''
:root{{--p:{p};--soft:{soft};--tint:{tint};--navy:#1e2440;--slate:#475569;--acc:{T.get('acc','#e07a5f')};--accdark:{T.get('acc_dark','#e07a5f')}}}
body{{margin:0;background:#999;font-family:P}}
.cv{{position:relative;overflow:hidden;margin:0 0 40px;background:#f7f7fb}}
.H{{width:1920px;height:1080px}}.V{{width:1080px;height:1920px}}
.a{{position:absolute}}
.dots::before{{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(30,36,64,.10) 2px,transparent 2.4px);background-size:40px 40px}}
.bp{{background-color:var(--tint);background-image:linear-gradient(rgba(255,255,255,.9) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.9) 2px,transparent 2px),
   linear-gradient(rgba(255,255,255,.55) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.55) 1px,transparent 1px);
   background-size:160px 160px,160px 160px,32px 32px,32px 32px}}
.pill{{display:inline-block;font-family:P;font-weight:700;letter-spacing:5px;text-transform:uppercase;border-radius:999px;padding:10px 30px}}
.pill.f{{background:var(--p);color:#fff}} .pill.o{{border:3px solid var(--p);color:var(--p);background:#fff}}
.h{{font-family:P;font-weight:800;color:var(--navy);line-height:1.02;letter-spacing:-3px}}
.h .hl{{background:none;color:var(--p);position:relative;white-space:nowrap}}
.h .hl::after{{content:"";position:absolute;left:0;right:0;bottom:-.06em;height:.16em;border-radius:99px;background:var(--acc);opacity:.85}}
.sub{{font-family:P;font-weight:600;color:var(--slate);line-height:1.3}}
.board{{background:#fff;border-radius:22px;box-shadow:0 22px 50px rgba(30,36,64,.16);border:3px solid rgba(30,36,64,.06)}}
.tape{{position:absolute;width:150px;height:44px;background:var(--acc);opacity:.35;border-radius:4px}}
.face{{border-radius:50%;box-shadow:0 0 0 8px #fff,0 0 0 12px var(--p),0 16px 30px rgba(30,36,64,.25)}}
.who .n{{font-family:P;font-weight:800;color:var(--navy)}} .who .s{{font-family:P;font-weight:600;color:var(--slate)}}
.chip{{font-family:Kalam;font-weight:700;border:4px solid var(--p);color:var(--p);border-radius:14px;padding:2px 20px;background:#fff}}
.chip.c{{border-color:var(--acc);color:var(--accdark)}}
.num{{font-family:P;font-weight:800;color:transparent;-webkit-text-stroke:5px var(--p);opacity:.9;letter-spacing:-6px}}
'''

def _mini(sid, w, h):
    return f'<svg id="{sid}" width="{w}" height="{h}" style="position:absolute;left:0;top:0"></svg>'

def thumb_x(L):
    T_ = L['thumb']
    return f'''<div class="cv H dots" id="thumb">
  <div class="a" style="left:90px;top:80px;display:flex;gap:16px"><span class="pill f" style="font-size:34px">{COURSE['name']}</span><span class="pill o" style="font-size:34px">Lesson {L["num"]:02d}</span></div>
  <div class="a" style="left:84px;top:185px;width:980px;display:flex;flex-direction:column;gap:34px">
    <div class="h" style="font-size:{T_.get("size",128)}px">{T_["title"]}</div>
    <div class="sub" style="margin-left:8px;font-size:48px">{T_["sub"]}</div>
    <div style="margin-left:6px;display:flex;gap:18px"><span class="chip" style="font-size:40px">{T_["chips"][0]}</span><span class="chip c" style="font-size:40px">{T_["chips"][1]}</span></div></div>
  <div class="a who" style="left:90px;top:820px;display:flex;align-items:center;gap:32px">
    <img class="face" src="../engine/avatar.png" style="width:170px;height:170px">
    <div><div class="n" style="font-size:48px">Gurpreet</div><div class="s" style="font-size:36px">The Code Notebook</div></div></div>
  <div class="a board" style="left:1060px;top:250px;width:790px;height:470px;transform:rotate(2deg)">
    <div class="tape" style="left:-30px;top:-14px;transform:rotate(-30deg)"></div><div class="tape" style="right:-30px;top:-14px;transform:rotate(30deg)"></div>
    <div class="a" style="left:15px;top:40px;width:760px;height:390px">{_mini('m_thumb', 760, 390)}</div></div>
</div>'''

def thumb_y(L):
    T_ = L['thumb']
    title = T_["title"].replace('<br>', ' ')
    return f'''<div class="cv H" id="thumb">
  <div class="a bp" style="left:0;top:0;width:1920px;height:640px"></div>
  <div class="a num" style="left:70px;top:40px;font-size:300px;line-height:1">{L["num"]:02d}</div>
  <div class="a board" style="left:560px;top:70px;width:1020px;height:470px;transform:rotate(-1.5deg)">
    <div class="a" style="left:40px;top:40px;width:940px;height:390px">{_mini('m_thumb', 940, 390)}</div></div>
  <div class="a" style="left:90px;top:700px"><span class="pill f" style="font-size:30px">{COURSE['name']} · Lesson {L["num"]:02d}</span></div>
  <div class="a h fit" data-w="1300" style="left:84px;top:775px;font-size:112px;white-space:nowrap">{title}</div>
  <div class="a sub" style="left:92px;top:930px;width:1300px;font-size:44px">{T_["sub"].replace('<br>', ' ')}</div>
  <img class="a face" src="../engine/avatar.png" style="right:110px;top:560px;width:280px;height:280px">
  <div class="a who" style="right:40px;width:420px;top:870px;text-align:center"><div class="n" style="font-size:44px">Gurpreet</div><div class="s" style="font-size:32px">The Code Notebook</div></div>
</div>'''

def vcover_x(L, key):
    C = L[key]['cover']
    top = 300 if key.startswith('reel') else 220
    handle = '@thecodenotebookyt' if key.startswith('reel') else 'The Code Notebook'
    return f'''<div class="cv V dots" id="c_{key}">
  <div class="a" style="left:0;right:0;top:{top}px;text-align:center"><span class="pill f" style="font-size:32px">{C["label"]}</span></div>
  <div class="a h" style="left:50px;right:50px;top:{top+110}px;text-align:center;font-size:{C.get("size",130)}px">{C["title"]}</div>
  <div class="a sub" style="left:0;right:0;top:{top+C.get("sub_off",500)+10}px;text-align:center;font-size:46px">{C["sub"]}</div>
  <div class="a board" style="left:110px;top:{top+C.get("card_off",650)+20}px;width:860px;height:330px;transform:rotate(-1.5deg)">
    <div class="tape" style="left:-24px;top:-12px;transform:rotate(-28deg)"></div><div class="tape" style="right:-24px;top:-12px;transform:rotate(28deg)"></div>
    <div class="a" style="left:30px;top:25px;width:800px;height:280px">{_mini('m_'+key, 800, 280)}</div></div>
  <div class="a who" style="left:0;right:0;top:{top+C.get("card_off",650)+420}px;display:flex;justify-content:center;align-items:center;gap:30px">
    <img class="face" src="../engine/avatar.png" style="width:190px;height:190px">
    <div><div class="n" style="font-size:48px">Gurpreet</div><div class="s" style="font-size:36px">{handle}</div></div></div>
</div>'''

def vcover_y(L, key):
    C = L[key]['cover']
    top = 300 if key.startswith('reel') else 220
    handle = '@thecodenotebookyt' if key.startswith('reel') else 'The Code Notebook'
    return f'''<div class="cv V" id="c_{key}">
  <div class="a bp" style="left:0;top:0;width:1080px;height:{top+C.get("card_off",650)+420}px"></div>
  <div class="a" style="left:0;right:0;top:{top}px;text-align:center"><span class="pill f" style="font-size:32px">{C["label"]}</span></div>
  <div class="a h" style="left:50px;right:50px;top:{top+110}px;text-align:center;font-size:{C.get("size",130)}px">{C["title"]}</div>
  <div class="a sub" style="left:0;right:0;top:{top+C.get("sub_off",500)+10}px;text-align:center;font-size:46px">{C["sub"]}</div>
  <div class="a board" style="left:110px;top:{top+C.get("card_off",650)+20}px;width:860px;height:330px">
    <div class="a" style="left:30px;top:25px;width:800px;height:280px">{_mini('m_'+key, 800, 280)}</div></div>
  <img class="a face" src="../engine/avatar.png" style="left:420px;top:{top+C.get("card_off",650)+400}px;width:240px;height:240px">
  <div class="a who" style="left:0;right:0;top:{top+C.get("card_off",650)+670}px;text-align:center"><div class="n" style="font-size:46px">Gurpreet</div><div class="s" style="font-size:34px">{handle}</div></div>
</div>'''

VK = ['short1', 'short2', 'reel']
NAME = dict(short1='Short1_Cover', short2='Short2_Cover', reel='Reel1_Cover_Instagram')
def build_covers(L, layout=None):
    layout = layout or os.environ.get('LLD_LAYOUT', 'x')
    th = thumb_x if layout == 'x' else thumb_y
    vc = vcover_x if layout == 'x' else vcover_y
    body = th(L) + ''.join(vc(L, k) for k in VK)
    minis = '\n'.join(f"DG_{m}(D('{sid}',760,260,1),'x');" for sid, m in [('m_thumb', L['thumb']['mini'])] + [('m_'+k, L[k]['cover']['mini']) for k in VK])
    html = f'''<!doctype html><html><head><meta charset="utf-8"><script src="../engine/rough.js"></script><script src="../engine/engine.js"></script>
<script>{THEME["js"]}</script><style>{css()}</style></head><body>{body}
<script>{lib.diag_js(L)}
{minis}
document.fonts.ready.then(()=>document.querySelectorAll('.fit').forEach(e=>{{let f=parseFloat(e.style.fontSize);while(e.scrollWidth>+e.dataset.w&&f>40){{f-=2;e.style.fontSize=f+'px';}}}}));</script></body></html>'''
    p = f'{lib.VID}/ms01/gen_{L["code"]}_covers.html'
    open(p, 'w').write(html)
    od = lib.outdir(L)
    outs = [('thumb', f'{L["code"]}_Thumbnail.png', (1280, 720))] + [('c_'+k, f'{L["code"]}_{NAME[k]}.png', None) for k in VK]
    asyncio.run(lib._shots(p, [(i, f'{od}/{n}', r) for i, n, r in outs]))
    return [f'{od}/{n}' for _, n, _ in outs]
