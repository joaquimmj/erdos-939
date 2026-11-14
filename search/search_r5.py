"""Exhaustive search: a+b+c = e, a<=b<=c, all four r-powerful, e <= X, gcd(a,b,c)=1. No other restriction.
Method: sorted table of pair sums a+b (a<=b); for each c, look up e-c for all e > c. X must be < 2^63."""
import sys, time, numpy as np
from math import gcd
from rpow import rpowerful
def search(r, X, include_one=True, log=None):
    assert X < 2**63
    L = rpowerful(r, X)
    if not include_one: L = L[1:]
    P = np.array(L, dtype=np.uint64); N = len(P)
    # pair sums a+b with a<=b and a+b <= X
    chunks = []
    for i in range(N):
        s = P[i:] + P[i]; chunks.append(s[s <= np.uint64(X)])
    S2 = np.sort(np.concatenate(chunks)); del chunks
    if log: print(f'N={N}, pair sums={len(S2)}', file=log, flush=True)
    sols = set(); t0 = time.time()
    for ci in range(N):
        c = L[ci]
        if log and ci % 2000 == 0: print(f'c {ci}/{N} {time.time()-t0:.0f}s sols={len(sols)}', file=log, flush=True)
        rem = P[ci+1:] - P[ci]                      # e - c for e > c
        if len(rem) == 0: continue
        k = np.searchsorted(S2, rem); k[k >= len(S2)] = len(S2) - 1
        for h in np.nonzero(S2[k] == rem)[0]:
            s = int(rem[h]); e = L[ci+1+int(h)]
            # recover all (a,b) with a+b=s, a<=b<=c (vectorised: the Python loop over L was the bottleneck)
            A = P[:np.searchsorted(P, s // 2, 'right')]; B = np.uint64(s) - A
            j = np.searchsorted(P, B); j[j >= N] = N - 1
            for m in np.nonzero((P[j] == B) & (B <= P[ci]))[0]:
                a, b = L[int(m)], s - L[int(m)]
                if gcd(gcd(a, b), c) == 1: sols.add((a, b, c, e))
    return sorted(sols, key=lambda t: (t[3], t)), N
if __name__ == '__main__':
    r = int(sys.argv[1]); X = int(float(sys.argv[2])); t = time.time()
    sols, N = search(r, X, log=sys.stdout)
    print(f'r={r} X={X} N={N} solutions={len(sols)} time={time.time()-t:.0f}s')
    for s in sols: print(*s)
