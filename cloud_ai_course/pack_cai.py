"""usage: python3 pack_cai.py N  -> makes thumbnails + covers + Code.zip + the final lesson zip, and reports anything missing."""
import sys, os, glob, zipfile, subprocess, shutil
n = int(sys.argv[1]); root = '/home/user/claude/course_output/Cloud_for_AI_Course'
folder = glob.glob(f'{root}/CAI-{n:02d}_*/')[0].rstrip('/'); code = f'CAI-{n:02d}'
subprocess.run([sys.executable, '/home/claude/caithumb/gen2.py', folder, str(n)], cwd='/home/claude/caithumb', check=True, capture_output=True)
lab = '/home/claude/cailab'
with zipfile.ZipFile(f'{folder}/{code}_Code.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for f in sorted(glob.glob(f'{lab}/l{n:02d}_*.py')): z.write(f, os.path.basename(f))
    for f in sorted(glob.glob(f'{lab}/results/l{n:02d}_*.txt')): z.write(f, 'results/' + os.path.basename(f))
    if os.path.exists(f'{lab}/FINDINGS_L{n}.md'): z.write(f'{lab}/FINDINGS_L{n}.md', f'FINDINGS_L{n}.md')
need = ['_Lesson_', '_Short1_', '_Short2_', '_Reel1_', '_Notes.pdf', '_Scripts.md', '_Upload_Copy.md', '_Subtitles.srt', '_Thumbnail.png', '_Short1_Cover.png', '_Short2_Cover.png', '_Reel1_Cover_Instagram.png', '_Code.zip']
names = os.listdir(folder)
missing = [k for k in need if not any(k in x for x in names)]
for f in glob.glob(f'{folder}/*.mp4'):
    if os.path.getsize(f) < 100000: missing.append('tiny mp4 ' + f)
out = f'{folder}.zip'
if os.path.exists(out): os.remove(out)
with zipfile.ZipFile(out, 'w', zipfile.ZIP_STORED) as z:
    for f in sorted(os.listdir(folder)): z.write(f'{folder}/{f}', f'{os.path.basename(folder)}/{f}')
print('missing:', missing or 'none'); print(out, round(os.path.getsize(out) / 1e6, 1), 'MB'); print(len(names), 'files')
