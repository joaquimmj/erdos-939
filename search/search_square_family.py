"""A restricted family of r = 5 solutions reaching far beyond the exhaustive bound.

(U + V)^2 = U^2 + 2UV + V^2. If gcd(U, V) = 1, V is odd and 5-powerful, U = 2^k * m with k >= 4 and m odd and
5-powerful, and W = U + V is 3-powerful, then a = U^2, b = 2UV, c = V^2 are 5-powerful, e = W^2 is 6-powerful,
gcd(a, b, c) = 1 and a + b + c = e. (This is the only 4-term relation found between monomials X^a Y^b Z^c,
Z = X + Y, with thresholds on the exponents: see identities_gfermat.py.)
We search every such pair with U, V <= B (B < 2^62), i.e. solutions with e up to about 4 B^2.
usage: search_square_family.py B [workers]"""
import sys, time, os, numpy as np
from math import gcd
from multiprocessing import Pool
from rpow import rpowerful

def build(B, tmp, rp=5, rw=3):
    P5 = rpowerful(rp, B); odd = [n for n in P5 if n % 2]
    even = sorted(m << k for m in odd for k in range(4, B.bit_length()) if (m << k) <= B)
    C3 = np.array(rpowerful(rw, 2*B), dtype=np.int64)
    np.save(os.path.join(tmp, 'c3.npy'), C3); np.save(os.path.join(tmp, 'odd.npy'), np.array(odd, dtype=np.int64))
    np.save(os.path.join(tmp, 'even.npy'), np.array(even, dtype=np.int64))
    return len(odd), len(even), len(C3)

def _init(tmp):
    global C3, ODD, EVEN
    C3 = np.load(os.path.join(tmp, 'c3.npy'), mmap_mode='r'); ODD = np.load(os.path.join(tmp, 'odd.npy')); EVEN = np.load(os.path.join(tmp, 'even.npy'))

def _work(job):
    k0, step = job; out = []
    for k in range(k0, len(EVEN), step):
        s = ODD + EVEN[k]
        i = np.searchsorted(C3, s); i[i >= len(C3)] = len(C3) - 1
        for h in np.nonzero(C3[i] == s)[0]:
            u, v = int(EVEN[k]), int(ODD[h])
            if gcd(u, v) == 1 and v > 1: out.append((u, v))
    return out

def search(B, workers=3, tmp=None, rp=5, rw=3):   # rp, rw only changed by the tests
    assert B < 2**62
    tmp = tmp or os.environ.get('TMPDIR', '.'); sizes = build(B, tmp, rp, rw)
    with Pool(workers, _init, (tmp,)) as pool:
        pairs = sorted(p for part in pool.map(_work, [(i, workers) for i in range(workers)]) for p in part)
    return pairs, sizes

if __name__ == '__main__':
    B = int(float(sys.argv[1])); t = time.time()
    pairs, sizes = search(B, int(sys.argv[2]) if len(sys.argv) > 2 else 3)
    print(f'B={B} odd 5-powerful={sizes[0]} even side={sizes[1]} 3-powerful<=2B={sizes[2]} pairs (U,V): {len(pairs)} time={time.time()-t:.0f}s')
    for u, v in pairs:
        a, b, c, e = u*u, 2*u*v, v*v, (u+v)**2
        print(f'U={u} V={v}  ->  {a} + {b} + {c} = {e}')
