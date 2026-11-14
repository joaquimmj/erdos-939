"""Search for 4-term polynomial identities that would give infinitely many solutions for r = 5 (Price's method).

Price's identity for r >= 6 is a linear relation between terms of the shape  c * X^a * Y^b * prod G(X,Y)^e  with
G in {X+Y, X-Y} and every e >= r: setting X = x^r, Y = y^r makes each monomial X^a Y^b an r-th power, each G^e is
r-powerful because e >= r, and the primes of c are absorbed by taking them as divisors of x or y.
For r = 5 one needs such a relation with only FOUR terms. We enumerate, in t = X/Y, all terms
    t^a * prod_{rho in R} (t - rho)^e_rho,   e_rho = 0 or >= 5,   a + sum e_rho <= d,
for a finite set R of rational roots, and list every minimal linear relation between four of them having no
common root (0 and infinity included). Candidates are found by a random projection mod p (dependent vectors
stay dependent, so nothing is missed), then confirmed exactly over Q.
usage: identities.py d emin rho1 rho2 ...     (rho as p/q, or an irreducible factor as its coefficients c0,c1,c2; emin = 5 for the real question)"""
import sys, itertools, random
from fractions import Fraction as Fr
import numpy as np
from sympy import Matrix

def polymul(p, q):
    out = [0]*(len(p)+len(q)-1)
    for i, x in enumerate(p):
        for j, y in enumerate(q): out[i+j] += x*y
    return out

def terms(d, R, emin=5):
    lin = {rho: rho if isinstance(rho, tuple) else [-rho.numerator, rho.denominator] for rho in R}   # q*t - p, or a factor given by its coefficients
    out = []
    for es in itertools.product(*[[0] + list(range(emin, d+1))]*len(R)):
        if sum(es) > d: continue
        base = [1]
        for rho, e in zip(R, es):
            for _ in range(e): base = polymul(base, list(lin[rho]))
        if len(base) > d + 1: continue
        for a in range(d - len(base) + 2):
            v = [0]*a + base; out.append(((a, es), v + [0]*(d + 1 - len(v))))
    return out

def relations(d, R, emin=5, seed=1):
    T = terms(d, R, emin); n = len(T); p = 2147483647; rng = random.Random(seed)
    proj = [[rng.randrange(p) for _ in range(d+1)] for _ in range(4)]
    W = np.array([[sum(c*x for c, x in zip(pr, v)) % p for pr in proj] for _, v in T], dtype=np.int64)
    found = []
    idx = np.arange(n)
    for i in range(n):
        for j in range(i+1, n):
            # 2x2 minors of (i, j) on every pair of the 4 coordinates, Laplace expansion against (k, l), k<l
            k = idx[j+1:]
            if len(k) < 2: continue
            K, Lx = np.triu_indices(len(k), 1); kk, ll = k[K], k[Lx]
            def m2(u, v, r, s): return (W[u, r]*W[v, s] - W[u, s]*W[v, r]) % p
            det = np.zeros(len(kk), dtype=np.int64)
            for (r, s), (r2, s2), sg in (((0,1),(2,3),1), ((0,2),(1,3),-1), ((0,3),(1,2),1), ((1,2),(0,3),1), ((1,3),(0,2),-1), ((2,3),(0,1),1)):
                det = (det + sg * int(m2(i, j, r, s)) * m2(kk, ll, r2, s2)) % p
            for h in np.nonzero(det == 0)[0]:
                found.append((i, j, int(kk[h]), int(ll[h])))
    out = []
    for q in found:
        M = Matrix([T[i][1] for i in q]).T
        ns = M.nullspace()
        if len(ns) != 1 or any(x == 0 for x in ns[0]): continue        # exact, minimal (all four terms used)
        labels = [T[i][0] for i in q]
        if min(a for a, _ in labels) > 0: continue                       # common root t = 0
        if any(min(es[r] for _, es in labels) > 0 for r in range(len(R))): continue    # common root rho
        if max(len([x for x in T[i][1]]) - list(reversed(T[i][1])).index(next(x for x in reversed(T[i][1]) if x)) for i in q) < d + 1: continue           # common root at infinity (seen at smaller d)
        out.append((labels, [Fr(int(x.p), int(x.q)) for x in ns[0]]))
    return out, n

if __name__ == '__main__':
    d = int(sys.argv[1]); emin = int(sys.argv[2]); R = [tuple(int(x) for x in s.split(',')) if ',' in s else Fr(s) for s in sys.argv[3:]]
    rel, n = relations(d, R, emin)
    print(f'd={d} roots={[str(r) for r in R]} terms={n} minimal coprime 4-term relations: {len(rel)}')
    for labels, co in rel:
        print('   ', ' ; '.join(f'({c}) t^{a}' + ''.join(f'(t-{rho})^{e}' for rho, e in zip(R, es) if e) for (a, es), c in zip(labels, co)))
