"""r = 4 via S-unit equations: filter a complete list of coprime a+b=c (von Känel & Matschke,
github.com/bmatschke/solving-classical-diophantine-equations, s-unit-equation/*.txt) for triples
whose three terms are all k-powerful, k = 2, 3, 4. Independent of rpow.py and of the size-ordered searches.
Usage: python3 check_sunit_r4.py solutions_*.txt"""
import sys, re
from math import gcd

def min_exponent(n):
    """smallest exponent in the factorisation of n > 1 (trial division; inputs are smooth), 99 for n = 1"""
    m, p = 99, 2
    while n > 1:
        if p * p > n: return min(m, 1)
        e = 0
        while n % p == 0: n //= p; e += 1
        if e: m = min(m, e)
        p += 1
    return m
assert [min_exponent(n) for n in (1, 2, 16, 48, 2**5 * 3**4, 7**4 * 11**6)] == [99, 1, 4, 1, 4, 4]

def check(path):
    declared = None; n = 0; hits = {2: [], 3: [], 4: []}; cmax = 0
    for line in open(path):
        if line.startswith('#'):
            m = re.search(r'contains (\d+) triples', line)
            if m: declared = int(m.group(1))
            continue
        m = re.match(r'\d+: (\d+) \+ (\d+) = (\d+)', line)
        if not m: continue
        a, b, c = map(int, m.groups()); n += 1; cmax = max(cmax, c)
        assert a + b == c and 0 < a <= b and gcd(a, b) == 1, line
        k = min(map(min_exponent, (a, b, c)))
        for r in hits:
            if k >= r: hits[r].append((a, b, c))
    assert declared == n, ('triple count differs from the file header', declared, n)
    print(f'{path.split("/")[-1]}: {n} triples (matches header), largest c = {cmax}')
    for r in hits: print(f'  all three {r}-powerful (1 allowed): {len(hits[r])}', *hits[r][:6])
    return hits

if __name__ == '__main__':
    for p in sys.argv[1:]: check(p)
