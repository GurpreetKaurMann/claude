"""Lesson 4 lab C: ARITHMETIC. How big is a training checkpoint, and how long does saving it stall the GPUs?

Full checkpoint = bf16 weights 2 B + fp32 master weights 4 B + Adam m 4 B + Adam v 4 B = 14 bytes per parameter (notebook, Oct 2026).
Stall = size / write bandwidth (if you wait for the write). The write speeds are ASSUMED round numbers.
Also: egress cost = GB moved x $/GB, using the ~$0.09 per GB AWS list price quoted in the notebook (volume tiers are lower).
Run: python3 l04_checkpoint_math.py
"""
print('== checkpoint size = 14 bytes x parameters')
for name, p in [('8B', 8e9), ('70B', 70e9), ('405B', 405e9)]:
    print(f'{name:5} {p*14/1e12:6.2f} TB')
print('\n== stall seconds if training waits for the write (size / bandwidth, ASSUMED speeds)')
print(f'{"model":6} {"size TB":>8} {"10 GB/s":>9} {"100 GB/s":>9}')
for name, p in [('70B', 70e9), ('405B', 405e9)]:
    s = p * 14 / 1e9
    print(f'{name:6} {s/1e3:8.2f} {s/10:8.0f}s {s/100:8.0f}s')
print('\n== dataset read once: tokens x bytes per token (uint16 ids = 2 bytes, vocab <= 65,536)')
print(f'15T tokens x 2 B = {15e12*2/1e12:.0f} TB')
print('\n== egress at the ~$0.09 per GB list price')
for tb in [1, 10, 100]:
    print(f'{tb:4d} TB out = {tb*1000:7,d} GB x $0.09 = ${tb*1000*0.09:9,.0f}')
