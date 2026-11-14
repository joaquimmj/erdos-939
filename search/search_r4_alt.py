"""Independent re-check of search_r4.py: a+b=c, a<=b, r-powerful, gcd(a,b)=1, c <= X < 2^63.
Other direction: for each c, every b in [c/2, c) is tried and a = c-b is looked up (search_r4 loops on a and
looks a+b up). Used only to confirm a result by a second execution path."""
import sys, time, os, numpy as np
from math import gcd
from multiprocessing import Pool
from rpow import rpowerful
def _init(r, X):
    global L, P, N
    L = rpowerful(r, X); P = np.array(L, dtype=np.int64); N = len(P)
def _work(job):
    k0, step = job; sols = []
    for k in range(k0, N, step):
        c = L[k]; j0 = int(np.searchsorted(P, (c + 1) // 2))      # b >= c/2
        a = P[k] - P[j0:k]
        i = np.searchsorted(P, a); i[i >= N] = N - 1
        for h in np.nonzero(P[i] == a)[0]:
            x, y = int(a[h]), L[j0 + int(h)]
            if gcd(x, y) == 1: sols.append((x, y, c))
    return sols
def search(r, X, workers=None):
    assert X < 2**63
    W = workers or max(1, (os.cpu_count() or 2) - 4)
    with Pool(W, _init, (r, X)) as pool:
        return sorted(s for part in pool.map(_work, [(i, W) for i in range(W)]) for s in part)
if __name__ == '__main__':
    r = int(sys.argv[1]); X = int(float(sys.argv[2])); t = time.time(); sols = search(r, X)
    print(f'r={r} X={X} (alt) coprime solutions (including a=1): {len(sols)}; time={time.time()-t:.0f}s')
    for s in sols[:200]: print(*s)
