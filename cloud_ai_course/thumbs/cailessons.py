# lines: (text, colour key)  w=white c=cyan r=red   ·   icon: glyph name from gen.G, or 'chip'
L = {
 1: dict(lines=[('YOUR MODEL FITS', 'w'), ('THEN CRASHES', 'c'), ('THE HIDDEN MEMORY COST:', 'w'), ('187 GB', 'r')], icon='chip'),
}

# vertical covers: Shorts and the Instagram Reel (Reel key content stays inside the centre 1080x1350)
V = {
 1: [dict(id='s1', file='Short1_Cover', tag='SHORT', icon='chip', lines=[('IT FITS.', 'w'), ('THEN IT', 'c'), ('FAILS', 'r')], sub='70 GB MODEL, 187 GB NEEDED'),
     dict(id='s2', file='Short2_Cover', tag='SHORT', icon='gauge', lines=[('4X THE DATA', 'w'), ('8X THE TIME', 'c')], sub='WHY AI NEEDS FAST MEMORY'),
     dict(id='r1', file='Reel1_Cover_Instagram', tag='SAVE THIS', icon='layers', lines=[('1 VS 256', 'w'), ('AT ONCE', 'c'), ('10X', 'r')], sub='WHY BATCHING MAKES AI CHEAP')],
}
