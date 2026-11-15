"""Four-term identities over a generalised Fermat triple (new mechanism for r = 5, to be explored).

Idea: let X + Y = Z where X = A x^p, Y = B y^q, Z = C z^s is a generalised Fermat equation with infinitely
many coprime solutions (1/p + 1/q + 1/s > 1, e.g. x^2 + y^3 = z^5). A monomial X^a Y^b Z^c is then 5-powerful
as soon as each exponent is 0 or at least the threshold ceil(5/p), ceil(5/q), ceil(5/s). Here we list the
minimal linear relations between FOUR such monomials of the same degree d with no common factor.
usage: identities_gfermat.py dmax  ta tb tc      (thresholds on the exponents of X, Y, Z)"""
import sys, itertools, random
from math import comb
import numpy as np
from sympy import Matrix

def four_term(T, dim, seed=1):
    """T: list of (label, integer vector of length dim). Minimal 4-term relations, exact."""
    n = len(T); p = 2147483647; rng = random.Random(seed)
    proj = [[rng.randrange(p) for _ in range(dim)] for _ in range(4)]
    W = np.array([[sum(c*x for c, x in zip(pr, v)) % p for pr in proj] for _, v in T], dtype=np.int64)
    idx = np.arange(n); out = []
    def m2(u, v, r, s): return (W[u, r]*W[v, s] - W[u, s]*W[v, r]) % p
    for i in range(n):
        for j in range(i+1, n):
            k = idx[j+1:]
            if len(k) < 2: continue
            Ka, Lb = np.triu_indices(len(k), 1); kk, ll = k[Ka], k[Lb]
            det = np.zeros(len(kk), dtype=np.int64)
            for (r, s), (r2, s2), sg in (((0,1),(2,3),1), ((0,2),(1,3),-1), ((0,3),(1,2),1), ((1,2),(0,3),1), ((1,3),(0,2),-1), ((2,3),(0,1),1)):
                det = (det + sg * int(m2(i, j, r, s)) * m2(kk, ll, r2, s2)) % p
            for h in np.nonzero(det == 0)[0]:
                q = (i, j, int(kk[h]), int(ll[h]))
                ns = Matrix([T[u][1] for u in q]).T.nullspace()
                if len(ns) == 1 and all(x != 0 for x in ns[0]):
                    den = 1
                    for x in ns[0]: den = den * x.q // __import__('math').gcd(den, x.q)
                    out.append(([T[u][0] for u in q], [int(x * den) for x in ns[0]]))
    return out

def monomials(d, ta, tb, tc):
    T = []
    for a in range(d+1):
        for c in range(d+1-a):
            b = d - a - c
            if (a and a < ta) or (b and b < tb) or (c and c < tc): continue
            T.append(((a, b, c), [comb(c, k-a) if a <= k <= a+c else 0 for k in range(d+1)]))   # t^a (t+1)^c
    return T

if __name__ == '__main__':
    dmax, ta, tb, tc = map(int, sys.argv[1:5])
    for d in range(2, dmax+1):
        T = monomials(d, ta, tb, tc); rel = four_term(T, d+1)
        rel = [(l, c) for l, c in rel if min(x[0] for x in l) == 0 and min(x[1] for x in l) == 0 and min(x[2] for x in l) == 0]
        print(f'd={d} thresholds=({ta},{tb},{tc}) monomials={len(T)} coprime 4-term relations: {len(rel)}', flush=True)
        for l, c in rel[:12]:
            print('    ' + '  '.join(f'{co:+d}·X^{a}Y^{b}Z^{cc}' for (a, b, cc), co in zip(l, c)) + ' = 0')
