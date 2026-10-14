"""Fast spec checks (no video, no speech). usage: python3 check.py cai03"""
import sys, re, json
sys.path.insert(0, '/home/claude/caigen'); import lib
ICONS = set('ab bars bell bits boxes chat check chip cloud clusters curve cyl doc funnel gauge gear globe grid layers leaf magn nn pin pipe play queue ring scatter server shield sig table ticket tile tree trophy wheel'.split())
code = sys.argv[1]; L = lib.load(f'/home/claude/caigen/{code}.py'); bad = []
for k in ['code','num','num_word','slug','title','title_html','tagline','module','toc','prev','next','next_say','diagrams','long','notes','glow','thumb','short1','short2','reel','upload']:
    if k not in L: bad.append(f'missing L[{k!r}]')
sc = lib.long_scenes(L); w = sum(len(x.split()) for s in sc for x in s['say'])
print(f'long: {len(sc)} scenes, {w} words, about {w/158 + len(sc)*0.9/60:.1f} min')
if not 2500 <= w <= 3000: bad.append(f'long narration is {w} words; target 2,550-2,950')
ids = [s['id'] for s in sc]
if len(set(ids)) != len(ids): bad.append('duplicate scene ids')
for s in sc:
    if not s.get('chap'): bad.append(f'scene {s["id"]} has no chap')
    for x in s['say']:
        if len(x.split()) > 75: bad.append(f'scene {s["id"]}: a say segment has {len(x.split())} words (keep under ~70)')
for kind in ['long','short1','short2','reel']:
    scs = sc if kind == 'long' else lib.vertical_scenes(L, kind)
    if kind != 'long':
        ww = sum(len(x.split()) for s in scs for x in s['say']); print(f'{kind}: {ww} words, about {ww/158*60/1.05:.0f} s')
        if not 50 <= ww <= 95: bad.append(f'{kind}: {ww} words; target 55-90')
        for key in ['slug','scenes','cover','upload']:
            if key not in L[kind]: bad.append(f'{kind} missing {key}')
        U = L[kind].get('upload', {})
        need = ['title','caption','pinned'] if kind.startswith('reel') else ['title','desc','tags','pinned']
        for key in need:
            if key not in U: bad.append(f'{kind}.upload missing {key}')
        if L[kind]['cover'].get('mini') not in L['diagrams']: bad.append(f'{kind}.cover.mini not in DIAGRAMS')
    for s in scs:
        html = ''.join(s['html']); refs = {int(m) for m in re.findall(r'data-at="§\.(\d+)"', html)}
        over = sorted(refs - set(range(len(s['say']))))
        if over: bad.append(f'{kind} scene {s["id"]}: data-at refers to segment {over} but say has {len(s["say"])} segments')
        for (svgid, name, *_r) in s.get('svgs', []):
            if name not in L['diagrams']: bad.append(f'{kind} scene {s["id"]}: diagram {name} not defined')
            if f'id="{svgid}"' not in html: bad.append(f'{kind} scene {s["id"]}: no SVG element with id {svgid}')
            js = L['diagrams'].get(name, ''); segs = {int(m) for m in re.findall(r"S\+'\.(\d+)'", js)}
            o2 = sorted(segs - set(range(len(s['say']))))
            if o2 and kind == 'long': bad.append(f'{kind} scene {s["id"]}: diagram {name} uses segment {o2} but say has {len(s["say"])}')
for it in L['glow']['icons']:
    if it == '>': continue
    n = it.partition(':')[0]; n = n[:-1] if n.endswith('s') else n
    if n[:-1] not in ICONS or n[-1] not in '12': bad.append(f'glow icon {it!r} invalid')
if L['thumb'].get('mini') not in L['diagrams']: bad.append('thumb.mini not in DIAGRAMS')
txt = open(f'/home/claude/caigen/{code}.py').read()
for ch, why in [('—', 'em dash'), ('–', 'en dash in narration is fine in tables only')]:
    n = sum(x.count(ch) for s in sc for x in s['say'])
    if n and ch == '—': bad.append(f'{n} em dashes in narration: rewrite as separate sentences')
print('OK' if not bad else 'PROBLEMS:\n - ' + '\n - '.join(bad))
