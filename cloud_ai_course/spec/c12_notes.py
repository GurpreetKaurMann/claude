from cai_lib import notes_regroup
from c12_notes_src import NOTES as N
# pairs of light pages share one page (was one source page per notes page: 17 pages, many half empty)
G = [[1], [2, 3], [4, 5], [6], [7], [8, 9], [10, 11], [12, 13], [14, 15], [16], [17]]
NOTES = notes_regroup(N, [[(i, None) for i in g] for g in G])
