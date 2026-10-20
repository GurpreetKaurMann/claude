#!/bin/bash
# render worker: each line "sjiNN [kinds]" (default kinds = long,short1,short2,short3,reel,docs)
cd /home/claude/caigen
while true; do
  LINE=$(head -1 queue.txt 2>/dev/null)
  if [ -z "$LINE" ]; then sleep 20; continue; fi
  L=$(echo $LINE | cut -d' ' -f1); K=$(echo $LINE | cut -s -d' ' -f2); K=${K:-notes,long,short1,short2,reel,docs}
  python3 run.py $L $K > b_$L.log 2>&1
  echo "$L $K $(date +%H:%M)" >> done.txt
  sed -i '1d' queue.txt
done
