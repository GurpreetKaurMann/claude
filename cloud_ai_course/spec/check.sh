#!/bin/bash
# usage: check.sh MS-06  -> builds notes/cover contact sheets
C=$1; D=$(ls -d /mnt/user-data/outputs/Low_Level_Design_Course/${C}_*/ | head -1)
mkdir -p /tmp/claude-0/pv; rm -f /tmp/claude-0/pv/n-*
pdftoppm -r 45 -png $D/*Notes.pdf /tmp/claude-0/pv/n
python3 - <<PY
from PIL import Image;import glob
fs=sorted(glob.glob('/tmp/claude-0/pv/n-*.png'));ims=[Image.open(f) for f in fs];w,h=ims[0].size
s=Image.new('RGB',(w*3,h*2),'white')
for i,im in enumerate(ims): s.paste(im,((i%3)*w,(i//3)*h))
s.save('/tmp/claude-0/pv/notes_$C.png')
D='$D'
a=Image.open(D+'/${C}_Thumbnail.png').resize((640,360));
c=[Image.open(D+'/'+n).resize((270,480)) for n in ['${C}_Short1_Cover.png','${C}_Short2_Cover.png','${C}_Reel_Cover_Instagram.png']]
s=Image.new('RGB',(640+810,480),'white');s.paste(a,(0,0))
for i,im in enumerate(c): s.paste(im,(640+i*270,0))
s.save('/tmp/claude-0/pv/covers_$C.png')
PY
