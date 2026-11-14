"""Exhaustive search for a+b=c, a<=b, all r-powerful, c <= X (< 2^63), gcd(a,b)=1 (then pairwise coprime).
Trivial solutions with a = 1 are reported separately (1 is vacuously r-powerful).
The loop over a is split over worker processes (stride W); each worker rebuilds the table itself."""
import sys, time, os, numpy as np
from math import gcd
from multiprocessing import Pool
from rpow import rpowerful
def _init(r, X):
    global L, P, N, XX
    L = rpowerful(r, X); P = np.array(L, dtype=np.uint64); N = len(P); XX = np.uint64(X)
def _work(job):
    i0, step = job; sols = []
    for i in range(i0, N, step):
        s = P[i:] + P[i]; s = s[s <= XX]      # no uint64 overflow: 2X < 2^64
        if len(s) == 0: break
        k = np.searchsorted(P, s); k[k >= N] = N - 1
        for h in np.nonzero(P[k] == s)[0]:
            a, b = L[i], L[i+int(h)]
            if gcd(a, b) == 1: sols.append((a, b, a+b))
    return sols
def search(r, X, workers=None):
    assert X < 2**63
    W = workers or max(1, (os.cpu_count() or 2) - 2)
    with Pool(W, _init, (r, X)) as pool:
        sols = sorted(s for part in pool.map(_work, [(i, W) for i in range(W)]) for s in part)
    return sols, len(rpowerful(r, X))
if __name__ == '__main__':
    r = int(sys.argv[1]); X = int(float(sys.argv[2])); t = time.time()
    sols, N = search(r, X)
    print(f'r={r} X={X} N={N} coprime solutions (including a=1): {len(sols)}; with a>1: {sum(1 for s in sols if s[0] > 1)}; time={time.time()-t:.0f}s')
    for s in sols[:200]: print(*s)
