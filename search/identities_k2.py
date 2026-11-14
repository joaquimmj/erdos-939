"""Case K = 2 of the identity search, over the algebraic closure, all degrees d <= D.

Relation  c1 t^a (t-1)^e1 + c2 t^b (t-rho)^e2 + c3 t^m + c4 t^n = 0,  e1, e2 >= 5,  rho not in {0, 1}:
two terms carry one non-free root each, the other two are monomials (rho = 1 is impossible: 1 would be a
root of multiplicity >= 5 of a binomial). For k outside {m, n} the coefficient of t^k must vanish:
    C(e1,k-a) (-1)^(e1-k+a) c1 + c2 C(e2,k-b) (-rho)^(e2-k+b) = 0.
So {m, n} contains the symmetric difference of the supports [a,a+e1], [b,b+e2], and on the remaining common
indices q_k * x^k is constant, with x = -rho and q_k = C(e1,k-a)(-1)^(e1-k+a) / C(e2,k-b).
We enumerate every (a,e1,b,e2,{m,n}) and test whether some complex x works (numerically, tolerance 1e-9)."""
import sys, cmath, itertools
from math import comb
from fractions import Fraction as Fr
D = int(sys.argv[1]) if len(sys.argv) > 1 else 16
hits = 0; cases = 0
for e1 in range(5, D+1):
  for e2 in range(5, D+1):
    for a in range(D - e1 + 1):
      for b in range(D - e2 + 1):
        S1 = set(range(a, a+e1+1)); S2 = set(range(b, b+e2+1)); sd = S1 ^ S2
        if len(sd) > 2: continue
        for E in itertools.combinations(range(D+1), 2):
            if not sd <= set(E): continue
            ks = sorted((S1 & S2) - set(E)); cases += 1
            q = {k: Fr(comb(e1, k-a) * (-1)**(e1-k+a), comb(e2, k-b)) for k in ks}
            k0, k1 = ks[0], ks[1]; R = complex(q[k0] / q[k1]); dl = k1 - k0
            for j in range(dl):                                   # x^dl = q_k0/q_k1
                x = abs(R)**(1/dl) * cmath.exp(1j*(cmath.phase(R) + 2*cmath.pi*j)/dl)
                if abs(x + 1) < 1e-9: continue                    # rho = 1 excluded
                if all(abs(complex(q[k]) * x**(k-k0) - complex(q[k0])) < 1e-9 * abs(complex(q[k0])) for k in ks):
                    hits += 1; print('SOLUTION', (a, e1, b, e2, E), 'rho =', -x)
print(f'K=2, d <= {D}: {cases} patterns tested, {hits} solutions')
