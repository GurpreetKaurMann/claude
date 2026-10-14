import sys, asyncio, base64
from playwright.async_api import async_playwright
D = '/home/claude/caithumb'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()

# feather-style glyphs, 24x24 viewBox, stroked
G = {
 'check': '<polyline points="20 6 9 17 4 12"/>',
 'bolt': '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
 'cube': '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>',
 'x': '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
 'lock': '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
 'search': '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
 'mail': '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
 'db': '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',
 'up': '<line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/>',
 'right': '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
 'server': '<rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/>',
 'star': '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
 'globe': '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
 'pin': '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
 'layers': '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
 'doc': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
 'key': '<circle cx="7.5" cy="15.5" r="5.5"/><path d="M11.4 11.6 21 2m-4 4 3 3m-6-0 2 2"/>',
 'table': '<rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="12" y1="3" x2="12" y2="21"/>',
 'tree': '<rect x="9" y="2" width="6" height="5" rx="1"/><rect x="2" y="17" width="6" height="5" rx="1"/><rect x="16" y="17" width="6" height="5" rx="1"/><path d="M12 7v5M5 17v-5h14v5"/>',
 'copy': '<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
 'chart': '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>',
 'bell': '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>',
 'chat': '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
 'link': '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
 'list': '<line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/>',
 'play': '<circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/>',
 'cloud': '<path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/>',
 'award': '<circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>',
 'filter': '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>',
 'hash': '<line x1="4" y1="9" x2="20" y2="9"/><line x1="4" y1="15" x2="20" y2="15"/><line x1="10" y1="3" x2="8" y2="21"/><line x1="16" y1="3" x2="14" y2="21"/>',
 'cycle': '<polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>',
 'pulse': '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
 'ticket': '<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>',
 'clip': '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/><polyline points="8 13 11 16 16 11"/>',
 'nav': '<polygon points="3 11 22 2 13 21 11 13 3 11"/>',
 'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
 'shieldok': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="8.5 12 11 14.5 15.5 9.5"/>',
 'chip': '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/>',
 'gauge': '<path d="M3.3 17a10 10 0 1 1 17.4 0"/><line x1="12" y1="13" x2="16.5" y2="8.5"/><circle cx="12" cy="13" r="1.4"/>',
 'scale': '<line x1="12" y1="3" x2="12" y2="21"/><line x1="5" y1="7" x2="19" y2="7"/><path d="M5 7l-3 7a3 3 0 0 0 6 0z"/><path d="M19 7l-3 7a3 3 0 0 0 6 0z"/><line x1="8" y1="21" x2="16" y2="21"/>',
 'code': '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
 'nodes': '<circle cx="12" cy="4.5" r="2.5"/><circle cx="4.5" cy="18.5" r="2.5"/><circle cx="19.5" cy="18.5" r="2.5"/><line x1="10.8" y1="6.7" x2="5.7" y2="16.3"/><line x1="13.2" y1="6.7" x2="18.3" y2="16.3"/><line x1="7" y1="18.5" x2="17" y2="18.5"/>',
 'calc': '<rect x="4" y="2" width="16" height="20" rx="2"/><rect x="7" y="5" width="10" height="4" rx="1"/><line x1="8" y1="13" x2="8.01" y2="13"/><line x1="12" y1="13" x2="12.01" y2="13"/><line x1="16" y1="13" x2="16.01" y2="13"/><line x1="8" y1="17" x2="8.01" y2="17"/><line x1="12" y1="17" x2="12.01" y2="17"/><line x1="16" y1="17" x2="16.01" y2="17"/>',
 'clock': '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
 'mic': '<path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/>',
}
def glyph(name, size, col, sw=2.4):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{col}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{G[name]}</svg>')

# card colour themes: (bg, border, ink, tile)
TH = [('#DDF3F8', '#BDE5EE', '#0E7490', '#C5E8F0'),
      ('#FBF1D3', '#F1DFA8', '#B98A0E', '#F6E3A6'),
      ('#FDE2E6', '#F8C4CC', '#BE123C', '#F8CBD3'),
      ('#E6EAF2', '#CFD6E6', '#1E3A8A', '#D4DBEE')]

def hero(kind):
    if kind == 'cyl':
        return '''<svg width="170" height="210" viewBox="0 0 170 210"><defs>
<linearGradient id="hc" x1="0" x2="1"><stop offset="0" stop-color="#6E2457"/><stop offset=".45" stop-color="#9A4A80"/><stop offset="1" stop-color="#5A1846"/></linearGradient>
<linearGradient id="ht" x1="0" x2="1"><stop offset="0" stop-color="#9C5A87"/><stop offset="1" stop-color="#B57AA2"/></linearGradient></defs>
<ellipse cx="85" cy="196" rx="74" ry="12" fill="#000" opacity=".12"/>
<path d="M10 34 V170 A75 22 0 0 0 160 170 V34 Z" fill="url(#hc)"/>
<path d="M10 80 A75 22 0 0 0 160 80" fill="none" stroke="#F4E6EF" stroke-width="5"/>
<path d="M10 126 A75 22 0 0 0 160 126" fill="none" stroke="#F4E6EF" stroke-width="5"/>
<ellipse cx="85" cy="34" rx="75" ry="22" fill="url(#ht)"/></svg>'''
    return (f'<div class="htile">{glyph(kind, 96, "#fff", 2.1)}</div>')

def card(i, label, icon, h):
    bg, bd, ink, tile = TH[i % 4]
    ts = min(h - 22, 66)
    return (f'<div class="card" style="height:{h}px;background:{bg};border-color:{bd}">'
            f'<div class="lab" style="color:{ink}">{label}</div><div class="dots" style="border-color:{ink}"></div>'
            f'<div class="tile" style="width:{ts}px;height:{ts}px;background:{tile}">{glyph(icon, ts*.56, ink, 2.6)}</div></div>')

CSS = '''
@font-face{font-family:A;src:url(anton-latin-400-normal.woff2)}
@font-face{font-family:P;src:url(poppins-latin-800-normal.woff2);font-weight:800}
@font-face{font-family:P;src:url(poppins-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:P;src:url(poppins-latin-600-normal.woff2);font-weight:600}
*{margin:0;box-sizing:border-box} body{background:#ccc}
.t{position:relative;width:1280px;height:720px;overflow:hidden;background:#F3F2EF;font-family:P}
.grid{position:absolute;inset:0;background-image:linear-gradient(#E1DFDA 1.5px,transparent 1.5px),linear-gradient(90deg,#E1DFDA 1.5px,transparent 1.5px);
 background-size:118px 118px;background-position:20px 30px;
 -webkit-mask-image:radial-gradient(ellipse 62% 58% at 38% 42%,transparent 55%,#000 100%)}
.blob{position:absolute;border-radius:50%}
.pill{position:absolute;left:38px;top:92px;height:66px;padding:0 30px;border-radius:16px;background:#9F1239;color:#fff;
 display:flex;align-items:center;font-weight:700;font-size:34px;letter-spacing:2.5px;white-space:nowrap;box-shadow:0 6px 16px rgba(159,18,57,.25)}
.ln{position:absolute;left:40px;font-family:A;color:#1A0B12;white-space:nowrap;line-height:1;letter-spacing:.5px;
 text-shadow:0 3px 0 rgba(255,255,255,.9)}
.sub{position:absolute;left:40px;font-family:A;color:#0E7490;white-space:nowrap;line-height:1;letter-spacing:.5px}
.rule{position:absolute;left:42px;height:4px;background:#9F1239;border-radius:2px}
.rule:after{content:"";position:absolute;right:-7px;top:-5px;width:14px;height:14px;border-radius:50%;background:#9F1239}
.wire{position:absolute;inset:0;pointer-events:none}
.hero{position:absolute;left:810px;display:flex;align-items:center;justify-content:center;width:170px}
.htile{width:160px;height:160px;border-radius:38px;background:linear-gradient(145deg,#F43F5E,#9F1239);display:flex;align-items:center;justify-content:center;
 box-shadow:0 18px 30px rgba(159,18,57,.30), inset 0 -10px 0 rgba(0,0,0,.12), inset 0 6px 0 rgba(255,255,255,.12)}
.cards{position:absolute;left:992px;top:112px;width:270px;display:flex;flex-direction:column;gap:14px}
.card{border:2px solid;border-radius:18px;display:flex;align-items:center;padding:0 11px 0 16px;gap:10px;box-shadow:0 6px 16px rgba(0,0,0,.06)}
.lab{font-family:A;font-size:30px;line-height:1;white-space:nowrap;letter-spacing:.5px}
.dots{flex:1;border-top:3.5px dotted;min-width:14px;opacity:.75}
.tile{border-radius:14px;display:flex;align-items:center;justify-content:center;flex:none}
.brand{position:absolute;top:586px;height:46px;padding:0 24px;border-radius:23px;background:#9F1239;color:#fff;font-weight:700;font-size:26px;
 display:flex;align-items:center;transform:translateX(-50%)}
.face{position:absolute;left:1036px;top:470px;width:236px;height:236px;border-radius:50%;border:8px solid #fff;overflow:hidden;
 background:#7CD4EE;box-shadow:0 12px 30px rgba(0,0,0,.22)}
.face img{position:absolute;left:-2%;top:3%;width:104%}
'''

def thumb(num, d):
    n = len(d['cards']); h = (364 - 14*(n-1)) / n
    html = f'<div class="t" id="t{num}"><div class="grid"></div>'
    html += '<div class="blob" style="width:300px;height:300px;left:745px;top:-140px;background:#FBC4CF;opacity:.85"></div>'
    html += '<div class="blob" style="width:420px;height:420px;left:-120px;top:520px;background:#A5E3F0;opacity:.6"></div>'
    html += '<div class="blob" style="width:90px;height:90px;left:850px;top:568px;background:#F6B04A;opacity:.85"></div>'
    html += f'<div class="pill">CLOUD FOR AI&nbsp;&nbsp;·&nbsp;&nbsp;LESSON {num}</div>'
    html += f'<div class="ln" data-fit>{d["l1"]}</div><div class="ln" data-fit>{d["l2"]}</div>'
    html += f'<div class="rule"></div><div class="sub">{d["sub"]}</div>'
    html += '<svg class="wire" width="1280" height="720"></svg>'
    html += f'<div class="hero">{hero(d["hero"])}</div>'
    html += '<div class="cards">' + ''.join(card(i, l, ic, h) for i, (l, ic) in enumerate(d['cards'])) + '</div>'
    html += f'<div class="face"><img src="data:image/png;base64,{b64(D + "/face_cut.png")}"></div>'
    html += '<div class="brand" style="left:560px">The Code Notebook</div>'
    return html + '</div>'

LAYOUT = '''
for (const t of document.querySelectorAll('.t')) {
  const r0 = t.getBoundingClientRect();
  const R = e => { const r = e.getBoundingClientRect(); return {x:r.left-r0.left, y:r.top-r0.top, w:r.width, h:r.height}; };
  const W = 745, l = [...t.querySelectorAll('[data-fit]')];
  let fs = 122;
  for (const e of l) { e.style.fontSize = '100px'; fs = Math.min(fs, 100 * W / e.getBoundingClientRect().width); }
  l.forEach(e => e.style.fontSize = fs + 'px');
  const s = t.querySelector('.sub'); s.style.fontSize = '100px';
  const sfs = Math.min(86, 100 * W / s.getBoundingClientRect().width); s.style.fontSize = sfs + 'px';
  // Anton: cap height ~ .735em, top bearing ~ .13em inside a line-height:1 box
  const cap = .735, tb = .135, g1 = .15 * fs, gr = 22;
  const H = 2*cap*fs + g1 + gr + 4 + gr + cap*sfs;
  let y = 182 + (330 - H) / 2;
  l[0].style.top = (y - tb*fs) + 'px'; y += cap*fs + g1;
  l[1].style.top = (y - tb*fs) + 'px'; y += cap*fs + gr;
  const rule = t.querySelector('.rule'); rule.style.top = y + 'px';
  const tw = Math.max(...l.map(e => e.getBoundingClientRect().width), s.getBoundingClientRect().width);
  rule.style.width = Math.min(tw, 745) + 'px'; y += 4 + gr;
  s.style.top = (y - tb*sfs) + 'px';
  // card labels: one size per thumbnail, the largest that fits every card
  let f = 30;
  const cs = [...t.querySelectorAll('.card')];
  const fits = () => cs.every(c => c.querySelector('.lab').getBoundingClientRect().width <= 270 - 27 - 34 - c.querySelector('.tile').getBoundingClientRect().width);
  while (!fits() && f > 16) { f -= 1; cs.forEach(c => c.querySelector('.lab').style.fontSize = f + 'px'); }
  // hero vertical centre = centre of cards block
  const cards = R(t.querySelector('.cards')), hero = t.querySelector('.hero'), hb = R(hero);
  const hy = cards.y + cards.h/2 - hb.h/2 + 10; hero.style.top = hy + 'px';
  const H2 = R(hero.firstElementChild), cx = 810 + 85;
  const pill = R(t.querySelector('.pill'));
  const col = '#9F1239';
  let svg = '';
  const py = pill.y + pill.h/2, px = pill.x + pill.w + 16;
  svg += `<circle cx="${px}" cy="${py}" r="7" fill="${col}"/>`;
  svg += `<path d="M${px} ${py} H${cx-14} Q${cx} ${py} ${cx} ${py+14} V${H2.y-14}" fill="none" stroke="${col}" stroke-width="3.5"/>`;
  svg += `<path d="M${cx-9} ${H2.y-22} L${cx} ${H2.y-8} L${cx+9} ${H2.y-22}" fill="none" stroke="${col}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>`;
  const bx = 966, sx = H2.x + H2.w - 6, sy = H2.y + H2.h*.42;
  for (const c of t.querySelectorAll('.card')) {
    const cr = R(c), cy = cr.y + cr.h/2;
    svg += `<path d="M${sx} ${sy} H${bx-12} Q${bx} ${sy} ${bx} ${sy + Math.sign(cy-sy)*12} V${cy - Math.sign(cy-sy)*12} Q${bx} ${cy} ${bx+12} ${cy} H${cr.x-8}" fill="none" stroke="${col}" stroke-width="3.5"/>`;
    svg += `<path d="M${cr.x-17} ${cy-8} L${cr.x-6} ${cy} L${cr.x-17} ${cy+8}" fill="none" stroke="${col}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>`;
  }
  t.querySelector('.wire').innerHTML = svg;
}
'''

async def main(L, nums, outdir):
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
    html += ''.join(thumb(n, L[n]) for n in nums) + '</body></html>'
    open(f'{D}/t.html', 'w').write(html)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); pg = await b.new_page(viewport={'width': 1280, 'height': 720})
        await pg.goto(f'file://{D}/t.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
        await pg.evaluate(LAYOUT)
        for n in nums: await pg.locator(f'#t{n}').screenshot(path=f'{outdir}/CAI-{n:02d}_Thumbnail.png')
        await b.close()

if __name__ == '__main__':
    from cailessons import L
    nums = [int(x) for x in sys.argv[2:]] or sorted(L)
    asyncio.run(main(L, nums, sys.argv[1]))
