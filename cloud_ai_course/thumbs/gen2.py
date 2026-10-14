"""Dark 'glow' thumbnails for Cloud for AI Engineers. usage: python3 gen2.py OUTDIR [lesson numbers]"""
import sys, asyncio, base64
from playwright.async_api import async_playwright
from gen import G, glyph
D = '/home/claude/caithumb'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
COL = dict(w='#FFFFFF', c='#1FE6F2', r='#FF4747')
GLOW = dict(w='rgba(255,255,255,.25)', c='rgba(31,230,242,.55)', r='rgba(255,71,71,.5)')

CHIP = '''<svg width="360" height="360" viewBox="0 0 360 360" fill="none" stroke="#2E8BFF" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">
<defs><filter id="g" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9"/></filter></defs>
<g id="c"><rect x="80" y="80" width="200" height="200" rx="26"/><rect x="118" y="118" width="124" height="124" rx="14"/><rect x="150" y="150" width="60" height="60" rx="8" fill="#2E8BFF" fill-opacity=".55"/>
<path d="M120 80V40M160 80V30M200 80V30M240 80V40M120 280V320M160 280V330M200 280V330M240 280V320M80 120H40M80 160H30M80 200H30M80 240H40M280 120H320M280 160H330M280 200H330M280 240H320"/></g>
<use href="#c" filter="url(#g)" opacity=".9"/></svg>'''

def icon(name):
    if name == 'chip': return CHIP
    return f'<div style="filter:drop-shadow(0 0 18px #2E8BFF)">{glyph(name, 300, "#2E8BFF", 1.6)}</div>'

CSS = '''
@font-face{font-family:A;src:url(anton-latin-400-normal.woff2)}
@font-face{font-family:P;src:url(poppins-latin-800-normal.woff2);font-weight:800}
@font-face{font-family:P;src:url(poppins-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:P;src:url(poppins-latin-600-normal.woff2);font-weight:600}
*{margin:0;box-sizing:border-box} body{background:#000}
.t{position:relative;width:1280px;height:720px;overflow:hidden;font-family:P;
 background:radial-gradient(ellipse 60% 70% at 78% 34%,#0f4fb8 0%,#0a2f7a 34%,#071d4c 62%,#040f2a 100%)}
.t:after{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,transparent 55%,rgba(0,0,0,.45) 100%)}
.ln{position:absolute;left:46px;font-family:A;white-space:nowrap;line-height:1;letter-spacing:.5px;z-index:3}
.icon{position:absolute;left:905px;top:62px;transform:rotate(14deg);z-index:2}
.foot{position:absolute;left:48px;top:641px;font-weight:600;font-size:29px;letter-spacing:2.5px;color:#C9D6EE;z-index:3;white-space:nowrap}
.foot b{color:#1FE6F2;font-weight:800}
.face{position:absolute;left:998px;top:430px;width:214px;height:214px;border-radius:50%;border:7px solid #fff;overflow:hidden;z-index:4;
 background:#E6F3FF;box-shadow:0 0 0 5px #1FA9F2,0 0 34px 8px rgba(31,169,242,.7)}
.face img{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;object-position:52% 28%;transform:scale(1.6);transform-origin:53% 40%}
.brand{position:absolute;left:1105px;top:628px;transform:translateX(-50%);height:50px;padding:0 26px;border-radius:25px;background:#05143a;
 border:3px solid #1FA9F2;color:#fff;font-weight:800;font-size:25px;letter-spacing:.5px;display:flex;align-items:center;z-index:5;white-space:nowrap;
 box-shadow:0 0 22px rgba(31,169,242,.65)}
'''

def thumb(num, d):
    h = f'<div class="t" id="t{num}"><div class="icon">{icon(d["icon"])}</div>'
    for text, k in d['lines']:
        h += (f'<div class="ln" data-fit style="color:{COL[k]};text-shadow:0 7px 0 rgba(0,0,0,.38),0 0 34px {GLOW[k]}">{text}</div>')
    h += f'<div class="foot">CLOUD FOR AI ENGINEERS &nbsp;<b>LESSON {num}</b></div>'
    h += f'<div class="face"><img src="data:image/jpeg;base64,{b64(D + "/face_new.jpg")}"></div><div class="brand">THE CODE NOTEBOOK</div></div>'
    return h

# target widths per line index, then stack; shrink everything if the block would be too tall
LAYOUT = '''
for (const t of document.querySelectorAll('.t')) {
  const ls = [...t.querySelectorAll('[data-fit]')];
  const W = [880, 880, 820, 640], cap = .735, tb = .135;
  const fs = ls.map((e, i) => { e.style.fontSize = '100px'; return 100 * (W[i] || 800) / e.getBoundingClientRect().width; });
  const gap = 20; let H = fs.reduce((a, f) => a + cap * f, 0) + gap * (ls.length - 1);
  const k = Math.min(1, 565 / H);
  let y = 40 + (565 - H * k) / 2;
  ls.forEach((e, i) => { const f = fs[i] * k; e.style.fontSize = f + 'px'; e.style.top = (y - tb * f) + 'px'; y += cap * f + gap * k; });
}
'''

VCSS = CSS + '''
.v{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:P;
 background:radial-gradient(ellipse 80% 45% at 50% 22%,#0f4fb8 0%,#0a2f7a 36%,#071d4c 66%,#040f2a 100%)}
.v:after{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,transparent 55%,rgba(0,0,0,.45) 100%)}
.v .vic{position:absolute;left:50%;top:335px;transform:translateX(-50%) rotate(10deg) scale(.78);z-index:2;width:360px;height:360px;display:flex;justify-content:center}
.v .ln{left:50%;right:auto;transform:translateX(-50%)}
.v .sub{position:absolute;left:0;right:0;top:1200px;text-align:center;font-weight:800;font-size:44px;letter-spacing:1.5px;color:#fff;z-index:3;padding:0 60px}
.v .face{left:415px;top:1290px;width:250px;height:250px}
.v .brand{left:540px;top:1520px;font-size:30px;height:58px;border-radius:29px;padding:0 32px}
.v .foot{left:0;right:0;top:1598px;text-align:center;font-size:30px}
.v .tag{position:absolute;left:50%;top:296px;transform:translateX(-50%);z-index:5;padding:8px 30px;border-radius:30px;background:#FF4747;color:#fff;font-weight:800;font-size:32px;letter-spacing:3px}
'''

def vthumb(n, d):
    h = f'<div class="v" id="v{n}_{d["id"]}"><div class="tag">{d["tag"]}</div><div class="vic">{icon(d["icon"])}</div>'
    for text, k in d['lines']:
        h += f'<div class="ln" data-fit style="color:{COL[k]};text-shadow:0 8px 0 rgba(0,0,0,.38),0 0 40px {GLOW[k]}">{text}</div>'
    h += f'<div class="sub">{d["sub"]}</div>'
    h += f'<div class="face"><img src="data:image/jpeg;base64,{b64(D + "/face_new.jpg")}"></div><div class="brand">THE CODE NOTEBOOK</div>'
    h += f'<div class="foot">CLOUD FOR AI ENGINEERS &nbsp;<b>LESSON {n}</b></div></div>'
    return h

VLAYOUT = '''
for (const t of document.querySelectorAll('.v')) {
  const ls = [...t.querySelectorAll('[data-fit]')]; const cap = .86, tb = .135, W = 940;
  const fs = ls.map(e => { e.style.fontSize = '100px'; return Math.min(260, 100 * W / e.getBoundingClientRect().width); });
  const gap = 18; let H = fs.reduce((a, f) => a + cap * f, 0) + gap * (ls.length - 1);
  const k = Math.min(1, 500 / H); let y = 680 + (500 - H * k) / 2;
  ls.forEach((e, i) => { const f = fs[i] * k; e.style.fontSize = f + 'px'; e.style.top = (y - tb * f) + 'px'; y += cap * f + gap * k; });
}
'''

async def vmain(V, outdir):
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{VCSS}</style></head><body>' + ''.join(vthumb(n, d) for n, d in V) + '</body></html>'
    open(f'{D}/v2.html', 'w').write(html)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto(f'file://{D}/v2.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
        await pg.evaluate(VLAYOUT)
        for n, d in V: await pg.locator(f'#v{n}_{d["id"]}').screenshot(path=f'{outdir}/CAI-{n:02d}_{d["file"]}.png')
        await b.close()

async def main(L, nums, outdir):
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>' + ''.join(thumb(n, L[n]) for n in nums) + '</body></html>'
    open(f'{D}/t2.html', 'w').write(html)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); pg = await b.new_page(viewport={'width': 1280, 'height': 720})
        await pg.goto(f'file://{D}/t2.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
        await pg.evaluate(LAYOUT)
        for n in nums: await pg.locator(f'#t{n}').screenshot(path=f'{outdir}/CAI-{n:02d}_Thumbnail.png')
        await b.close()

if __name__ == '__main__':
    from cailessons import L, V
    asyncio.run(main(L, [int(x) for x in sys.argv[2:]] or sorted(L), sys.argv[1]))
    asyncio.run(vmain([(n, d) for n, ds in V.items() for d in ds if (not sys.argv[2:] or str(n) in sys.argv[2:])], sys.argv[1]))
