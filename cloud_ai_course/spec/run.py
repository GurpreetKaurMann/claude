import sys, json, os
sys.path.insert(0, '/home/claude/caigen')
import lib
code = sys.argv[1]; steps = sys.argv[2].split(',')
L = lib.load(f'/home/claude/caigen/{code}.py')
if 'notes' in steps: print(lib.build_notes(L))
if 'covers' in steps:
    print(lib.build_covers(L))
    import gaithumb; print(gaithumb.build(L))
if 'preview' in steps:
    for k in sys.argv[3].split(','): print(lib.preview(L, k))
metas = {}
for k in ['long', 'short1', 'short2', 'reel']:
    if k in steps:
        m = lib.build_video(L, k)
        json.dump(dict(total=m['total'], chapters=m['chapters']), open(f'/home/claude/video/out/{L["code"]}_{k}.meta.json', 'w'))
if 'docs' in steps:
    m = json.load(open(f'/home/claude/video/out/{L["code"]}_long.meta.json'))
    m['scenes'] = lib.long_scenes(L)
    print(lib.write_docs(L, {'long': m}))
