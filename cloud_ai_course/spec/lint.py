"""Layout lint on final-state slides: content off-frame or in the brand/caption zone, and text overflowing its box."""
import sys, json, asyncio
sys.path.insert(0, '/home/claude/caigen'); import lib
from playwright.async_api import async_playwright
KINDS = ['long', 'short1', 'short2', 'reel']
JS = r'''([W,H,v])=>{const out=[];const lim=v?1560:1010;
 const bad=(q)=>q.width>0&&q.height>0&&(q.left<-4||q.right>W+4||q.top<-4||q.bottom>lim);
 document.querySelectorAll('.scene').forEach(s=>{ if(getComputedStyle(s).display==='none')return;
  s.querySelectorAll('*').forEach(e=>{const tag=e.tagName.toLowerCase();
   if(tag==='svg'){let bb,m;try{bb=e.getBBox();m=e.getScreenCTM()}catch(_){return}
     if(!bb||!bb.width||!m)return; const xs=[bb.x,bb.x+bb.width].map(x=>m.a*x+m.e), ys=[bb.y,bb.y+bb.height].map(y=>m.d*y+m.f);
     const q={left:Math.min(...xs),right:Math.max(...xs),top:Math.min(...ys),bottom:Math.max(...ys),width:1,height:1};
     if(bad(q))out.push(s.id+': diagram ink at '+[q.left,q.top,q.right,q.bottom].map(Math.round).join(','));return;}
   if(e.closest('svg'))return;
   const cs=getComputedStyle(e);
   if(parseFloat(cs.borderTopWidth)>0||cs.backgroundColor!=='rgba(0, 0, 0, 0)'){const r=e.getBoundingClientRect(); if(bad(r))out.push(s.id+': box at '+[r.left,r.top,r.right,r.bottom].map(Math.round).join(',')+' "'+e.textContent.trim().slice(0,40)+'"');}
   e.childNodes.forEach(n=>{if(n.nodeType===3&&n.textContent.trim()){const rg=document.createRange();rg.selectNode(n);const r=rg.getBoundingClientRect();
     if(bad(r))out.push(s.id+': text at '+[r.left,r.top,r.right,r.bottom].map(Math.round).join(',')+' "'+n.textContent.trim().slice(0,40)+'"');
     const p=e.closest('.card,.def,.q,.rule,.sticky,.outp,.codep,td'); if(p){const pr=p.getBoundingClientRect(); if(r.right>pr.right+6||r.bottom>pr.bottom+6)out.push(s.id+': text spills out of its box "'+n.textContent.trim().slice(0,40)+'"');}}});
  });});return out}'''
async def main(code):
    L = lib.load(f'/home/claude/caigen/{code}.py'); n = 0
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for kind in KINDS:
            h = kind == 'long'; sc = lib.long_scenes(L) if h else lib.vertical_scenes(L, kind)
            W, H = (1920, 1080) if h else (1080, 1920)
            pg = await b.new_page(viewport={'width': W, 'height': H})
            p = f'/home/claude/video/gen/lint_{code}_{kind}.html'; open(p, 'w').write(lib.page_html(L, sc, 'h' if h else 'v'))
            await pg.goto('file://' + p); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            TL = dict(seg={}, scenes=[], caps=[])
            for i, s in enumerate(sc):
                TL['scenes'].append([s['id'], i*100, i*100+100])
                for j in range(len(s['say'])): TL['seg'][f"{s['id']}.{j}"] = i*100
            await pg.evaluate(f'window.T={json.dumps(TL)}'); await pg.evaluate('initEngine()'); await pg.evaluate('window.vfit && window.vfit()')
            seen = set()
            for i, s in enumerate(sc):
                await pg.evaluate(f'render({i*100+99})')
                for msg in await pg.evaluate(JS, [W, H, not h]):
                    k = msg.split(' at ')[0]
                    if k in seen: continue
                    seen.add(k); print(code, kind, msg); n += 1
            await pg.close()
        await b.close()
    print(code, 'lint issues:', n)
asyncio.run(main(sys.argv[1]))
