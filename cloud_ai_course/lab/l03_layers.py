"""Lesson 3 lab A: REAL bytes and hashes, SIMULATED registry. Layer order decides what you re-ship.

A container image is a stack of layers. A layer's identity = hash(parent layer identity + its content), so changing
one layer changes every layer above it. We build real random files (stand-ins: OS 50 MB, CUDA libs 100 MB, Python
deps 60 MB, model weights 400 MB, app code 1 MB), hash them for real, and keep a pretend registry of layer ids already
pushed. We push v1, change ONE line of app code, push v2, and count the bytes that must be shipped again.
No Docker daemon was available on the build machine, so Docker itself is not run. Run: python3 l03_layers.py
"""
import hashlib, os, time
MB = 1024 * 1024
rng = __import__('numpy').random.default_rng(1)
blob = lambda mb: rng.integers(0, 256, mb * MB, dtype='uint8').tobytes()
content = {'os': blob(50), 'cuda': blob(100), 'deps': blob(60), 'weights': blob(400), 'code': blob(1)}

def build(order, c):
    parent, layers = '', []
    for name in order:
        parent = hashlib.sha256(parent.encode() + hashlib.sha256(c[name]).digest()).hexdigest()
        layers.append((name, parent, len(c[name])))
    return layers

def push(layers, registry):
    shipped = 0
    for name, lid, size in layers:
        if lid not in registry: registry.add(lid); shipped += size
    return shipped / MB

ORD_A = ['os', 'cuda', 'deps', 'weights', 'code']       # code last (the usual advice)
ORD_B = ['os', 'cuda', 'deps', 'code', 'weights']       # weights after the code
ORD_C = ['os', 'cuda', 'deps', 'code']                  # weights NOT in the image (mounted)
changed = dict(content); changed['code'] = blob(1)      # edit one line of app code
newweights = dict(content); newweights['weights'] = blob(400)   # a new model version

print(f'{"image layout":34} {"first push":>11} {"change code":>12} {"new weights":>12}')
for label, order in [('A: weights baked in, code last', ORD_A), ('B: weights baked in, code BEFORE weights', ORD_B), ('C: weights mounted, not in the image', ORD_C)]:
    reg = set(); first = push(build(order, content), reg)
    r1 = set(reg); code = push(build(order, changed), r1)
    r2 = set(reg); wt = push(build(order, newweights), r2)
    print(f'{label:34} {first:9.0f} MB {code:10.0f} MB {wt:10.0f} MB')
print('(C: a new weights version ships as its own 400 MB artifact, the app image is untouched)')

t = time.perf_counter(); h = hashlib.sha256(content['weights']).hexdigest(); dt = time.perf_counter() - t
print(f'\nreal work: hashing the 400 MB weights layer took {dt:.2f} s on this machine ({400/dt:.0f} MB/s)')
