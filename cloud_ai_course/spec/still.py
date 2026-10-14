"""Final-state stills of every scene, WITHOUT text-to-speech (fast).
usage: python3 still.py gai03 [long,short1,...]   -> contact sheets in /tmp/claude-0/still/
Each scene is shown as it looks at its END (everything revealed). Verticals include a sample caption."""
import sys, os, json, asyncio
sys.path.insert(0, '/home/claude/caigen'); import lib
from playwright.async_api import async_playwright
from PIL import Image
OUT = '/tmp/claude-0/still'; os.makedirs(OUT, exist_ok=True)
KINDS = ['long', 'short1', 'short2', 'reel']
async def main(code, kinds):
    L = lib.load(f'/home/claude/caigen/{code}.py')
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for kind in kinds:
            h = kind == 'long'
            sc = lib.long_scenes(L) if h else lib.vertical_scenes(L, kind)
            W, H = (1920, 1080) if h else (1080, 1920)
            pg = await b.new_page(viewport={'width': W, 'height': H})
            p = f'/home/claude/video/gen/still_{code}_{kind}.html'
            open(p, 'w').write(lib.page_html(L, sc, 'h' if h else 'v')); await pg.goto('file://' + p)
            await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
            TL = dict(seg={}, scenes=[], caps=[])
            for i, s in enumerate(sc):
                TL['scenes'].append([s['id'], i*100, i*100+100])
                for j in range(len(s['say'])): TL['seg'][f"{s['id']}.{j}"] = i*100
                if not h:
                    words = s['say'][-1].split(); TL['caps'].append([i*100, i*100+100, ' '.join(words[:6])])
            await pg.evaluate(f'window.T={json.dumps(TL)}'); await pg.evaluate('initEngine()'); await pg.evaluate('window.vfit && window.vfit()')
            shots = []
            for i, s in enumerate(sc):
                await pg.evaluate(f'render({i*100+99})'); f = f'{OUT}/_{code}_{kind}_{i:02d}.png'
                await pg.screenshot(path=f); shots.append((s['id'], f))
            await pg.close()
            cols, tw, th = (3, 640, 360) if h else (4, 324, 576)
            per = cols * (3 if h else 2)
            for n in range(0, len(shots), per):
                grp = shots[n:n+per]; rows = (len(grp)+cols-1)//cols
                sheet = Image.new('RGB', (cols*tw, rows*th), 'white')
                for k, (sid, f) in enumerate(grp): sheet.paste(Image.open(f).convert('RGB').resize((tw, th)), ((k % cols)*tw, (k//cols)*th))
                o = f'{OUT}/{code}_{kind}_{n//per+1}.png'; sheet.save(o); print(o, [x[0] for x in grp])
            for _, f in shots: os.remove(f)
        await b.close()
code = sys.argv[1]; kinds = sys.argv[2].split(',') if len(sys.argv) > 2 else KINDS
asyncio.run(main(code, kinds))
