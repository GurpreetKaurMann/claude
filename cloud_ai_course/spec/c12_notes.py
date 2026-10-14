from cai_lib import notes_regroup
from c12_notes_src import NOTES as N
NOTES = notes_regroup(N, [[(i, None)] for i in range(1, len(N) + 1)])
