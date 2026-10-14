import sys, asyncio
sys.path.insert(0,'/home/claude/caigen'); import lib
from playwright.async_api import async_playwright
async def m():
  async with async_playwright() as pw:
    b=await pw.chromium.launch(); pg=await b.new_page()
    for code in sys.argv[1:]:
      L=lib.load(f'/home/claude/caigen/{code}.py')
      for kind in ['long','short1','short2','reel']:
        sc=lib.long_scenes(L) if kind=='long' else lib.vertical_scenes(L,kind)
        have={f"{s['id']}.{i}" for s in sc for i in range(len(s['say']))}
        p='/home/claude/video/gen/dbg.html'; open(p,'w').write(lib.page_html(L,sc,'h' if kind=='long' else 'v'))
        await pg.goto('file://'+p); await pg.evaluate('window.T={seg:{},scenes:[],caps:[]}')
        ks=await pg.evaluate('initEngine()')
        miss=[k for k in ks if k not in have]
        if miss: print(code,kind,miss)
    await b.close()
asyncio.run(m())
