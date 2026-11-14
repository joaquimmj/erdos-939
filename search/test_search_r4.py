"""search_r4 (parallel) vs naive pair loop, trivial a = 1 solutions included. Separate file: worker processes re-import the main module."""
from math import gcd
from rpow import rpowerful
from search_r4 import search as search2
if __name__ == '__main__':
    for r, X in ((2, 20000), (3, 10**7)):
        L = rpowerful(r, X); S = set(L)
        nv = sorted((a, b, a+b) for i, a in enumerate(L) for b in L[i:] if a+b in S and gcd(a, b) == 1)
        assert search2(r, X, 3)[0] == nv, (r, X)
        print(f'search_r4 == naive for r={r}, X={X}: {len(nv)} solutions OK')
