#!/bin/bash
# copy sources into the repo, commit the lesson zips + sources, push. usage: sync_repo.sh "message"
set -e
R=/home/user/claude; cd $R
mkdir -p cloud_ai_course/lab/results cloud_ai_course/spec cloud_ai_course/thumbs
cp /home/claude/cailab/*.py /home/claude/cailab/FINDINGS_L*.md cloud_ai_course/lab/ 2>/dev/null || true
cp /home/claude/cailab/results/*.txt cloud_ai_course/lab/results/ 2>/dev/null || true
cp /home/claude/caigen/{cai*.py,c0*.py,c1*.py,cai_lib.py,lib.py,theme.py,check.py,run.py,still.py,keys.py,lint.py,gaicovers.py,queue2.sh} cloud_ai_course/spec/ 2>/dev/null || true
cp /home/claude/caithumb/{gen.py,gen2.py,cailessons.py,face_new.jpg} cloud_ai_course/thumbs/
cp /home/claude/pack_cai.py /home/claude/sync_repo.sh cloud_ai_course/
git add -A cloud_ai_course course_output/Cloud_for_AI_Course/*.zip .gitignore
git -c core.quotepath=off commit -q -m "$1

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01JNmCcH6t2ofB4C91EEJCuZ" || echo "nothing to commit"
for i in 1 2 3 4; do git push -u origin claude/magical-tesla-b41twa 2>&1 | tail -1 && break || sleep $((2**i)); done
