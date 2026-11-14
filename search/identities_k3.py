"""Case K = 3, type (i): three terms carrying one non-free root each, fourth term a monomial:
    c1 t^a1 (t-1)^e1 + c2 t^a2 (t-rho)^e2 + c3 t^a3 (t-sigma)^e3 = alpha t^m,   e_i >= 5.
rho, sigma are rational, distinct, not in {0, 1} (see notes/o3_identities.md), min(a_i) = 0, and Mason-Stothers
applied after (t d/dt - m) bounds a_i + e_i <= 10. For each pattern the 3 coefficient vectors, with row m
removed, must have rank <= 2: all 3x3 minors vanish. We compute a Groebner basis of the minors, saturated
by rho*sigma*(rho-1)*(sigma-1)*(rho-sigma), exactly over Q; basis {1} means no solution over the complex numbers.
usage: identities_k3.py [part nparts]"""
import sys, itertools
from math import comb
from sympy import symbols, Matrix, groebner, expand, Poly
x, y, z = symbols('x y z')
def vec(a, e, root, d): return [comb(e, k-a) * (-root)**(e-(k-a)) if a <= k <= a+e else 0 for k in range(d+1)]
opts = [(a, e) for e in range(5, 11) for a in range(0, 11-e)]
pats = [p for p in itertools.combinations_with_replacement(opts, 3) if min(a for a, _ in p) == 0]
part, nparts = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, 1)
bad = 0; n = 0
for pi, pat in enumerate(pats):
    if pi % nparts != part: continue
    # the root 1 may sit on any of the three terms: try each rotation of the roots
    for roots in set(itertools.permutations((1, x, y))):
        if roots.index(x) > roots.index(y): continue                  # x <-> y symmetry
        d = max(a+e for a, e in pat)
        V = [vec(a, e, r, d) for (a, e), r in zip(pat, roots)]
        for m in range(d+1):
            rows = [k for k in range(d+1) if k != m]
            M = Matrix([[V[i][k] for i in range(3)] for k in rows])
            nz = [k for k in range(len(rows)) if any(M[k, i] != 0 for i in range(3))]
            minors = set()
            for tr in itertools.combinations(nz[:7] + nz[-3:], 3):
                mm = expand(M.extract(list(tr), [0, 1, 2]).det())
                if mm != 0: minors.add(mm)
            n += 1
            if not minors: bad += 1; print('DEGENERATE', pat, roots, m, flush=True); continue
            G = groebner(list(minors) + [1 - z*x*y*(x-1)*(y-1)*(x-y)], z, x, y, order='lex')
            if G.exprs != [1]:
                bad += 1; print('CANDIDATE', pat, roots, 'm =', m, G.exprs, flush=True)
print(f'part {part}/{nparts}: {n} systems, {bad} not excluded', flush=True)
