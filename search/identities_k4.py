"""Open case s = 0, K = 4 of notes/o3_identities.md: four terms, each carrying exactly one non-free root,
    T1 + l2 T2 + l3 T3 + l4 T4 = 0,   T_i = t^a_i (t - rho_i)^e_i  (homogeneous degree d, b_i = d - a_i - e_i),
with e_i >= R (R = 5 for r = 5), 0 and infinity free (any multiplicity), no common root (min a = min b = 0).
Scaling t fixes rho_1 = 1. Terms may share a non-free root (all set partitions of the terms except one block). Wronskian bound (notes): d <= 2 + sum min(a_i, 2) + sum min(b_i, 2), hence d <= 14.
A relation over Q with these exponents gives an infinite family for r = 5 (X = x^5, Y = y^5).
For each pattern: ideal of the d+1 coefficient equations in (rho2, rho3, rho4, l2, l3, l4), saturated by
the distinct roots, their differences and l2 l3 l4 (Singular via passagemath). Ideal = (1): no solution over C.
usage: identities_k4.py R dmax part nparts   (calibration: R = 2 must report candidates)"""
import sys, itertools, time
from sage.all import QQ, PolynomialRing, binomial
R_, dmax, part, nparts = (int(a) for a in sys.argv[1:5])
P = PolynomialRing(QQ, 'r2,r3,r4,l2,l3,l4,w'); r2, r3, r4, l2, l3, l4, w = P.gens()
lam = (P(1), l2, l3, l4)
# root assignments: set partitions of the 4 terms (terms in one block share their non-free root), never one block;
# the block of term 0 gets the root 1 (scaling), the others r2, r3, r4 in order; saturate by distinctness of blocks.
def partitions(s):
    if not s: yield []; return
    for p in partitions(s[1:]):
        for i in range(len(p)): yield p[:i] + [[s[0]] + p[i]] + p[i+1:]
        yield [[s[0]]] + p
ASSIGN = []
for blocks in partitions([0, 1, 2, 3]):
    if len(blocks) == 1: continue
    blocks.sort(key=min); vals = [P(1), r2, r3, r4][:len(blocks)]
    rho = [None]*4
    for b, v in zip(blocks, vals):
        for i in b: rho[i] = v
    sat = l2*l3*l4
    for i in range(len(vals)):
        sat *= vals[i] if i else 1
        for j in range(i): sat *= vals[i] - vals[j]
    ASSIGN.append((tuple(rho), sat, len(blocks)))
def coeffs(a, e, rho, d): return [binomial(e, k-a) * (-rho)**(e-(k-a)) if a <= k <= a+e else 0 for k in range(d+1)]
n = cand = 0; t0 = time.time()
for d in range(R_, dmax+1):
    opts = [(a, d-a-b) for a in range(d-R_+1) for b in range(d-R_-a+1) if d-a-b >= R_]
    for idx, pat in enumerate(itertools.combinations_with_replacement(opts, 4)):
        if (idx + d) % nparts != part: continue
        A = [a for a, e in pat]; B = [d-a-e for a, e in pat]
        if min(A) or min(B) or d > 2 + sum(min(a, 2) for a in A) + sum(min(b, 2) for b in B): continue
        for roots, sat, nb in ASSIGN:
            V = [coeffs(a, e, rho, d) for (a, e), rho in zip(pat, roots)]
            eqs = [sum(lam[i] * V[i][k] for i in range(4)) for k in range(d+1)]
            I = P.ideal([q for q in eqs if q != 0] + [1 - w*sat]); n += 1
            if not I.is_one():
                cand += 1; print('CANDIDATE d=%d' % d, pat, roots, I.elimination_ideal([w]).gens()[:4], flush=True)
    print(f'R={R_} d={d} part {part}/{nparts}: {n} systems so far, {cand} not excluded, {time.time()-t0:.0f}s', flush=True)
