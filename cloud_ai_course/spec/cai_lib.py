"""Helpers shared by the Cloud for AI lessons: diagram JS builders, Short / Reel builders, notes helpers."""
import sys; sys.path.insert(0, '/home/claude/caigen')
from frag import *

CK = dict(teal='C.teal', orange='C.orange', red='C.red', blue='C.blue', gray='C.gray', green='C.green')
SOFT = dict(teal='C.tealSoft', orange='C.orangeSoft', red='C.redSoft', blue='C.blueSoft', gray="'#f3f4f6'", green="'#dcfce7'")
TXT = dict(teal='C.teal', orange="'#92400e'", red='C.red', blue='C.blue', gray="'#4b5563'", green='C.green')


def bars(rows, segs, vmax, head=None, x0=250, wmax=560, y0=44, dy=56, bh=40, note=None, line=None):
    """Horizontal bar chart. rows: (label, value, colour key, value text). segs: segment index per row.
    head: (left title, right title). note: (text, seg, colour key). line: (value, text, seg, colour key) vertical marker."""
    js = []
    if head:
        js.append(f"d.at(S+'.{segs[0]}',0).text(20,24,'{head[0]}',{{size:20,bold:false,color:'#6b7280',anchor:'start'}});")
        js.append(f"d.at(S+'.{segs[0]}',0).text({x0},24,'{head[1]}',{{size:20,bold:false,color:'#6b7280',anchor:'start'}});")
    for i, (lab, v, c, txt) in enumerate(rows):
        y = y0 + i * dy; w = max(v / vmax * wmax, 6); sg = segs[i]; dl = 0.15 + (i % 2) * 0.35
        js.append(f"d.at(S+'.{sg}',{dl}).text(20,{y+bh-6},'{lab}',{{size:26,color:C.ink,anchor:'start'}});")
        js.append(f"d.at(S+'.{sg}',{dl+0.15}).box({x0},{y},{w:.0f},{bh},null,{{stroke:{CK[c]},fill:{SOFT[c]},fillStyle:'solid'}});")
        tx = x0 + w + 14
        if line and x0 + w < x0 + line[0] / vmax * wmax and tx < x0 + line[0] / vmax * wmax + 90:
            tx = x0 + line[0] / vmax * wmax + 16          # keep the value clear of the marker line
        js.append(f"d.at(S+'.{sg}',{dl+0.3}).text({tx:.0f},{y+bh-6},'{txt}',{{size:25,color:{TXT[c]},anchor:'start'}});")
    ymax = y0 + len(rows) * dy
    if line:
        v, t, sg, c = line; lx = x0 + v / vmax * wmax
        js.append(f"d.at(S+'.{sg}',0.2).line({lx:.0f},{y0-12},{lx:.0f},{ymax},{{sw:4,stroke:{CK[c]},dash:true}});")
        js.append(f"d.at(S+'.{sg}',0.4).text({lx+8:.0f},{ymax+22},'{t}',{{size:24,color:{CK[c]},anchor:'start',font:'Caveat'}});")
    if note:
        t, sg, c = note
        js.append(f"d.at(S+'.{sg}',0.2).text(500,{ymax+(52 if line else 28)},'{t}',{{size:26,color:{CK[c]},font:'Caveat'}});")
    return '\n ' + '\n '.join(js) + '\n'


def boxes(items, segs, y=50, h=190, note=None, arrows=False, size=28):
    """A row of boxes. items: (title, subtitle, colour key). segs: segment index per item. Up to 4-5 items."""
    n = len(items); gap = 20; w = (1000 - 28 - gap * (n - 1)) / n; js = []
    for i, (t, sub, c) in enumerate(items):
        x = 14 + i * (w + gap); sg = segs[i]; dl = 0.1 + (i % 2) * 0.4
        js.append(f"d.at(S+'.{sg}',{dl}).box({x:.0f},{y},{w:.0f},{h},null,{{stroke:{CK[c]},fill:'#fff',fillStyle:'solid'}});")
        js.append(f"d.at(S+'.{sg}',{dl+0.15}).text({x+w/2:.0f},{y+h*0.42:.0f},'{t}',{{size:{size},color:{CK[c]}}});")
        js.append(f"d.at(S+'.{sg}',{dl+0.3}).text({x+w/2:.0f},{y+h*0.74:.0f},'{sub}',{{size:21,color:'#4b5563',bold:false}});")
        if arrows and i < n - 1:
            js.append(f"d.at(S+'.{sg}',{dl+0.5}).arrow({x+w+2:.0f},{y+h/2:.0f},{x+w+gap-2:.0f},{y+h/2:.0f},{{sw:3}});")
    if note:
        t, sg, c = note
        js.append(f"d.at(S+'.{sg}',0.3).text(500,{y+h+42},'{t}',{{size:27,color:{CK[c]},font:'Caveat'}});")
    return '\n ' + '\n '.join(js) + '\n'


def mini2(l1, v1, c1, l2, v2, c2, foot, fs=36, vs=52):
    """Static two-row mini diagram (760x260) for covers: two label/value rows and a footer line."""
    col = dict(red='#dc2626', green='#0f766e', amber='#b45309', grey='#6b7280', navy='#1e2440', rose='#be123c')
    return (f"\n d.text(40,75,'{l1}',{{size:{fs},color:'#6b7280',font:'P',anchor:'start'}}); d.text(720,75,'{v1}',{{size:{vs},color:'{col[c1]}',font:'P',anchor:'end'}});\n"
            f" d.text(40,160,'{l2}',{{size:{fs},color:'#6b7280',font:'P',anchor:'start'}}); d.text(720,160,'{v2}',{{size:{vs},color:'{col[c2]}',font:'P',anchor:'end'}});\n"
            f" d.text(380,238,'{foot}',{{size:34,color:'#be123c',font:'P'}});\n")


def vs(id, say, html, svgs=()): return dict(id=id, say=say, html=html, svgs=list(svgs))


def _big2(a, b, sa=150, sb=110):
    return ('<div class="center" style="padding-top:60px">' + BIG(a, 0, size=sa, color='var(--teal)') + BIG(b, 0, 0.6, size=sb, color='var(--acc)') + '</div>')


def mk_short(n, slug, hook, big, b_say, mini, c_say, c_tag, c_text, cover, upload, c_size=80):
    """A Short: a (hook with two BIG lines), b (proof with mini diagram), c (takeaway sticky)."""
    return dict(slug=slug, scenes=[
        vs('a', [hook], [_big2(big[0], big[1], *(big[2:4] if len(big) > 2 else (150, 110)))]),
        vs('b', b_say, [SVG(f'v{n}b', 960, 330, 'margin-top:40px')], [(f'v{n}b', mini, 760, 260, 1.15)]),
        vs('c', [c_say], ['<div class="center" style="padding-top:60px">', STICKY(c_tag, c_text, 0, style=f'font-size:{c_size}px'), '</div>'])],
        cover={**dict(label='Cloud for AI · Short', mini=mini, sub_off=430, card_off=560), **cover}, upload=upload)


def mk_reel(slug, say_a, say_b, big, items, times, sticky_tag, sticky_text, cover, upload):
    return dict(slug=slug, speed=1.08, scenes=[
        vs('a', say_a, ['<div class="center">' + BIG(big, 0, size=120, color='var(--acc)') + '</div>', '<div style="font-size:46px;margin-top:50px">',
                         LIST([(t, 1, tm) for t, tm in zip(items, times)], kind='ar'), '</div>']),
        vs('b', [say_b], ['<div class="center" style="padding-top:80px">', STICKY(sticky_tag, sticky_text, 0, style='font-size:92px'), '</div>'])],
        cover={**dict(label='Save this for later', sub_off=470, card_off=590), **cover}, upload=upload)


def notes_regroup(N, groups):
    """groups: list of lists of (page_index, slice or None). Returns renumbered NOTES."""
    pages = []
    for g in groups:
        pg = []
        for idx, sl in g:
            pg += N[idx - 1][sl] if sl else N[idx - 1]
        pages.append(pg)
    out, n = [], 0
    for pg in pages:
        o = []
        for b in pg:
            if b[0] == 'h2':
                n += 1; b = ('h2', str(n)) + tuple(b[2:])
            o.append(b)
        out.append(o)
    return out
