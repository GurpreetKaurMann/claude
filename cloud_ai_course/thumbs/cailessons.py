# lines: (text, colour key)  w=white c=cyan r=red   ·   icon: glyph name from gen.G, or 'chip'
L = {
 1: dict(lines=[('YOUR MODEL FITS', 'w'), ('THEN CRASHES', 'c'), ('THE HIDDEN MEMORY COST:', 'w'), ('187 GB', 'r')], icon='chip'),
 2: dict(lines=[('CHEAP GPUS', 'w'), ('COST MORE', 'c'), ('ONE MISTAKE MAKES', 'w'), ('IT NEVER ENDS', 'r')], icon='clock'),
 3: dict(lines=[('ONE LINE CHANGED', 'w'), ('401 MB SHIPPED', 'c'), ('THE DOCKER MISTAKE:', 'w'), ('LAYER ORDER', 'r')], icon='cube'),
 4: dict(lines=[('SMALL FILES ARE', 'w'), ('25X SLOWER', 'c'), ('THE AI DATA MISTAKE:', 'w'), ('SHARD IT', 'r')], icon='db'),
 5: dict(lines=[('70B MODEL: 140 GB', 'w'), ('TRAINING NEEDS', 'c'), ('THE 16-BYTE RULE:', 'w'), ('1,120 GB', 'r')], icon='chip'),
}

# vertical covers: Shorts and the Instagram Reel (Reel key content stays inside the centre 1080x1350)
V = {
 1: [dict(id='s1', file='Short1_Cover', tag='SHORT', icon='chip', lines=[('IT FITS.', 'w'), ('THEN IT', 'c'), ('FAILS', 'r')], sub='70 GB MODEL, 187 GB NEEDED'),
     dict(id='s2', file='Short2_Cover', tag='SHORT', icon='gauge', lines=[('4X THE DATA', 'w'), ('8X THE TIME', 'c')], sub='WHY AI NEEDS FAST MEMORY'),
     dict(id='r1', file='Reel1_Cover_Instagram', tag='SAVE THIS', icon='layers', lines=[('1 VS 256', 'w'), ('AT ONCE', 'c'), ('10X', 'r')], sub='WHY BATCHING MAKES AI CHEAP')],
 2: [dict(id='s1', file='Short1_Cover', tag='SHORT', icon='clock', lines=[('100-HOUR JOB', 'w'), ('2 MILLION', 'c'), ('HOURS', 'r')], sub='THE SPOT GPU MISTAKE'),
     dict(id='s2', file='Short2_Cover', tag='SHORT', icon='scale', lines=[('55% OFF', 'w'), ('CAN COST', 'c'), ('MORE', 'r')], sub='THE COMMITMENT TRAP'),
     dict(id='r1', file='Reel1_Cover_Instagram', tag='SAVE THIS', icon='bolt', lines=[('24 TO 4', 'w'), ('GPU-HOURS', 'c'), ('A DAY', 'r')], sub='SCALE TO ZERO')],
 3: [dict(id='s1', file='Short1_Cover', tag='SHORT', icon='layers', lines=[('1 LINE', 'w'), ('401 MB', 'c'), ('SHIPPED', 'r')], sub='DOCKER LAYER ORDER'),
     dict(id='s2', file='Short2_Cover', tag='SHORT', icon='nodes', lines=[('3 JOBS', 'w'), ('95%', 'c'), ('FROZE', 'r')], sub='16 GPUS, NO GANG SCHEDULING'),
     dict(id='r1', file='Reel1_Cover_Instagram', tag='SAVE THIS', icon='cube', lines=[('BAKE OR', 'w'), ('MOUNT', 'c'), ('WEIGHTS?', 'r')], sub='MEASURED, NOT GUESSED')],
 4: [dict(id='s1', file='Short1_Cover', tag='SHORT', icon='db', lines=[('SAME DATA', 'w'), ('25X', 'c'), ('SLOWER', 'r')], sub='SMALL FILES VS SHARDS'),
     dict(id='s2', file='Short2_Cover', tag='SHORT', icon='layers', lines=[('SHRINK', 'w'), ('VECTORS 4X', 'c'), ('KEEP 98%', 'r')], sub='FLOAT16 AND INT8'),
     dict(id='r1', file='Reel1_Cover_Instagram', tag='SAVE THIS', icon='cloud', lines=[('MOVING', 'w'), ('100 TB', 'c'), ('$9,000', 'r')], sub='THE EGRESS TRAP')],
 5: [dict(id='s1', file='Short1_Cover', tag='SHORT', icon='chip', lines=[('140 GB', 'w'), ('MODEL', 'c'), ('1,120 GB', 'r')], sub='TO TRAIN IT'),
     dict(id='s2', file='Short2_Cover', tag='SHORT', icon='bolt', lines=[('TRAIN', 'w'), ('1%', 'c'), ('SAVE 100X', 'r')], sub='LORA, MEASURED'),
     dict(id='r1', file='Reel1_Cover_Instagram', tag='SAVE THIS', icon='pulse', lines=[('43%', 'w'), ('OF GPUS', 'c'), ('SIT IDLE', 'r')], sub='THE PIPELINE BUBBLE')],
}
