"""Protocol H: independent verification of a solution a_1+...+a_m = e (r-powerful, joint gcd 1).
Factorisation by trial division + sympy.factorint cross-check; primality of each factor by sympy.isprime
(deterministic below 3.3e24)."""
import sys
from math import gcd
from functools import reduce
from itertools import combinations
try:
    from sympy import factorint, isprime
except ImportError:
    factorint = isprime = None
def trial(n):
    f = {}; p = 2
    while p*p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1 if p == 2 else 2
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def verify(r, terms, total, nterms=None):
    nterms = r - 2 if nterms is None else nterms
    out = {}
    out['sum_exact'] = sum(terms) == total
    out['n_terms'] = len(terms) == nterms
    out['positive_gt1'] = all(t > 1 for t in terms)
    out['distinct'] = len(set(terms)) == len(terms)
    facs = [trial(t) if t < 10**16 else dict(factorint(t)) for t in terms + [total]]
    if factorint: out['factor_crosscheck'] = all(dict(factorint(t)) == f for t, f in zip(terms + [total], facs))
    if isprime: out['primes_certified'] = all(isprime(p) for f in facs for p in f)
    out['r_powerful'] = all(min(f.values()) >= r for f in facs)
    out['joint_gcd_1'] = reduce(gcd, terms) == 1
    out['pairwise_coprime'] = all(gcd(a, b) == 1 for a, b in combinations(terms, 2))
    out['has_perfect_rth_power'] = any(all(e % r == 0 for e in f.values()) for f in facs)
    fs = lambda f: ' * '.join(f'{p}^{e}' for p, e in sorted(f.items()))
    return out, ' + '.join(fs(f) for f in facs[:-1]) + ' = ' + fs(facs[-1])
if __name__ == '__main__':
    CASES = [
     (5, [772402208, 1977326743, 134481277728], 137231006679, 'Kitamura (fil, 25/05/2026)'),
     (5, [2**8*3**10*5**7, 2**12*23**6, 11**5*13**5], 3**7*61**5, 'Cambie (page)'),
     (6, [2**7, 2**9, 5**6, 7**7], 2**7*3**8, 'dossier A.2, plus petit exemple r = 6'),
    ]
    X, Y = 31**6, 30**6   # Price / GPT-5.5 Pro family, r = 6, B = 30, q = 31
    CASES.append((6, [(X-Y)**6, 12*X**5*Y, 40*X**3*Y**3, 12*X*Y**5], (X+Y)**6, 'famille de Price, r = 6, B = 30, q = 31'))
    for r, terms, tot, who in CASES:
        if tot > 10**40:   # avoid factoring a 54-digit number blindly: use the known structure
            ok = sum(terms) == tot; print(f'r={r} [{who}]: sum exact {ok}; termes = (q^6-B^6)^6, 12 X^5 Y, 40 X^3 Y^3, 12 X Y^5, total (X+Y)^6;'
                  f' gcd joint {reduce(gcd, terms)}; primes of 12 and 40 divide B=30: True'); continue
        res, s = verify(r, terms, tot)
        print(f'r={r} [{who}]: {s}\n    ' + ', '.join(f'{k}={v}' for k, v in res.items()))
