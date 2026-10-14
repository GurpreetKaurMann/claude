"""Regroups the pages of c01_notes_src into 11 fuller pages and renumbers the headings."""
from c01_notes_src import NOTES as N
P = lambda i: N[i - 1]
_pages = [P(1),
          P(2) + P(4)[-3:],
          P(3) + P(4)[:4],
          P(5) + P(6),
          P(7) + P(8)[:2],
          P(8)[2:] + P(9)[:3],
          P(9)[3:] + P(10),
          P(11), P(12), P(13), P(14)]
NOTES = []; _n = 0
for pg in _pages:
    out = []
    for b in pg:
        if b[0] == 'h2':
            _n += 1; b = ('h2', str(_n)) + tuple(b[2:])
        out.append(b)
    NOTES.append(out)
