from cai_lib import notes_regroup
from c09_notes_src import NOTES as N
NOTES = notes_regroup(N, [[(1, None)], [(2, None), (3, None)]] + [[(i, None)] for i in range(4, len(N) + 1)])
