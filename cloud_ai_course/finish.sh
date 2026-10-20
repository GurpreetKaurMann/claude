#!/bin/bash
# after each lesson renders: thumbnails + Code.zip + check, then commit + push the lesson folder
R=/home/user/claude; Q=/home/claude/caigen; BR=claude/wonderful-heisenberg-bttwz9
touch /home/claude/finished.txt
while true; do
  for L in $(cut -d' ' -f1 $Q/done.txt 2>/dev/null); do
    grep -qx $L /home/claude/finished.txt && continue
    N=$((10#${L#cai}))
    echo "== $L $(date +%H:%M)"
    python3 /home/claude/pack_cai.py $N < /dev/null
    cd $R
    git add -f course_output/Cloud_for_AI_Course/CAI-$(printf %02d $N)_*/
    git -c core.quotepath=off commit -q -m "Render CAI-$(printf %02d $N) lesson package

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01J6ydkGW2EgNSfNzqgFehAS" || echo "nothing to commit"
    for i in 1 2 3 4; do git push -u origin $BR < /dev/null 2>&1 | tail -1 && break || sleep $((2**i)); done
    echo $L >> /home/claude/finished.txt
  done
  [ $(wc -l < /home/claude/finished.txt) -ge 11 ] && echo ALLDONE && exit 0
  sleep 30
done
