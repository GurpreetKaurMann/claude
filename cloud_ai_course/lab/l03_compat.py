"""Lesson 3 lab C: a RULE CHECK from the notebook (not a measurement). Will an image's CUDA version run on this host driver?

Rule (often-quoted minimums, Oct 2026): CUDA 12.x needs driver R525+, CUDA 13.x needs R580+.
Always confirm with NVIDIA's CUDA Compatibility guide. Run: python3 l03_compat.py [host_driver_major image_cuda_major]
"""
import sys
MIN = {12: 525, 13: 580}
def ok(driver, cuda_major): return driver >= MIN[cuda_major]
if len(sys.argv) == 3:
    d, c = int(sys.argv[1]), int(sys.argv[2]); print(f'host R{d}, image CUDA {c}.x ->', 'runs' if ok(d, c) else f'NO: needs R{MIN[c]}+')
else:
    print(f'{"host driver":>12} {"CUDA 12.x":>10} {"CUDA 13.x":>10}')
    for d in [515, 525, 535, 550, 570, 580, 595]:
        print(f'{"R"+str(d):>12} {"runs" if ok(d,12) else "NO":>10} {"runs" if ok(d,13) else "NO":>10}')
