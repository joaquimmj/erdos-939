"""Open case s = 1, K = 4 of notes/o3_identities.md: one monomial and three terms carrying 4 non-free roots (2, 1, 1):
    t^a1 + l2 t^a2 (t - 1)^e (t - s)^f + l3 t^a3 (t - u)^g + l4 t^a4 (t - v)^h = 0   (homogeneous degree d),
exponents at non-free roots >= R, 0 and infinity free, min a = min b = 0. Same Wronskian bound as identities_k4.py:
d <= 2 + sum min(a_i, 2) + sum min(b_i, 2) <= 14. Roots of different terms may coincide (all cases), s != 1.
Ideal = (1) after saturation (distinct roots, nonzero roots, l2 l3 l4): no solution over C.
usage: identities_k4s1.py R dmax part nparts"""
import sys, itertools, time
from sage.all import QQ, PolynomialRing, binomial
R_, dmax, part, nparts = (int(a) for a in sys.argv[1:5])
P = PolynomialRing(QQ, 's,u,v,l2,l3,l4,w'); s_, u_, v_, l2, l3, l4, w = P.gens(); tt = PolynomialRing(P, 't').gen()
# roots u (term 3) and v (term 4) may equal 1, s, or each other: enumerate the identifications
ASSIGN = []
for U in ('1', 's', 'u'):
    for V in ('1', 's', 'u', 'v'):
        if V == 'u' and U != 'u': continue                       # v = u only if u is new
        val = {'1': P(1), 's': s_, 'u': u_, 'v': v_}
        new = [s_] + ([u_] if U == 'u' else []) + ([v_] if V == 'v' else [])
        pts = [P(1)] + new; sat = l2*l3*l4
        for i in range(1, len(pts)):
            sat *= pts[i]
            for j in range(i): sat *= pts[i] - pts[j]
        ASSIGN.append((val[U], val[V], sat, U+V))
n = cand = 0; t0 = time.time()
for d in range(2*R_, dmax+1):
    T2 = [(a, e, f) for e in range(R_, d+1) for f in range(e, d+1) for a in range(d-e-f+1)]   # f >= e: the root 1 sits on e (scaling, and 1 <-> s symmetry swaps e, f)
    T1 = [(a,) for a in range(d+1)]
    T3 = [(a, g) for g in range(R_, d+1) for a in range(d-g+1)]
    for idx, (m, t2, t3, t4) in enumerate((m, t2, t3, t4) for m in T1 for t2 in T2 for t3 in T3 for t4 in T3):
        if (idx + d) % nparts != part: continue
        A = [m[0], t2[0], t3[0], t4[0]]; B = [d - m[0], d - sum(t2), d - sum(t3), d - sum(t4)]
        if min(A) or min(B) or d > 2 + sum(min(a, 2) for a in A) + sum(min(b, 2) for b in B): continue
        for U, V, sat, tag in ASSIGN:
            if tag[0] == tag[1] and t3 > t4: continue             # identical roots: order the two one-root terms
            if tag == 'uv' and t3 > t4: continue                  # u <-> v symmetry
            F = tt**m[0] + l2*tt**t2[0]*(tt-1)**t2[1]*(tt-s_)**t2[2] + l3*tt**t3[0]*(tt-U)**t3[1] + l4*tt**t4[0]*(tt-V)**t4[1]
            I = P.ideal([c for c in F.list() if c != 0] + [1 - w*sat]); n += 1
            if not I.is_one():
                cand += 1; print('CANDIDATE d=%d' % d, m, t2, t3, t4, tag, I.elimination_ideal([w]).gens()[:4], flush=True)
    print(f'R={R_} d={d} part {part}/{nparts}: {n} systems so far, {cand} not excluded, {time.time()-t0:.0f}s', flush=True)
