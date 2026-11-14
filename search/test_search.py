"""Unit tests: generator vs naive factorisation; search vs naive triple loop."""
from rpow import rpowerful, is_rpowerful_naive
from search_r5 import search
from math import gcd
for r, X in ((2, 20000), (3, 200000), (5, 3_000_000)):
    assert rpowerful(r, X) == [n for n in range(1, X+1) if is_rpowerful_naive(n, r)], (r, X)
print('generator == naive: OK')
def naive(r, X):
    L = rpowerful(r, X); S = set(L); out = []
    for i, a in enumerate(L):
        for j in range(i, len(L)):
            b = L[j]
            for k in range(j, len(L)):
                c = L[k]; e = a+b+c
                if e > X: break
                if e in S and gcd(gcd(a, b), c) == 1: out.append((a, b, c, e))
    return sorted(out, key=lambda t: (t[3], t))
for r, X in ((2, 3000), (3, 300000), (4, 10**8), (5, 3*10**11)):
    s1 = search(r, X)[0]; s2 = naive(r, X); assert s1 == s2, (r, X, len(s1), len(s2))
    print(f'search == naive for r={r}, X={X}: {len(s1)} solutions OK')
