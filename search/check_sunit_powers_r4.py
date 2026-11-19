"""r = 4 with one term a perfect square or cube of ANY size and support: filter the complete lists of von Känel &
Matschke (sums-of-units-equations/*.txt: all (x, y), x >= y, x, y supported on S, gcd(x, y) square-free,
x + y a square, resp. a cube). A coprime r = 4 solution a + b = c whose two other terms are supported on S and
whose remaining term is a square (resp. cube) appears there as (b, a) if that term is c, or as (c, -b) if it is a
(or b). So: keep pairs with |x|, |y| and x + y > 0 all 4-powerful and gcd 1.
Usage: python3 check_sunit_powers_r4.py sumsOfUnitsBeing*.txt"""
import sys, re
from math import gcd
from check_sunit_r4 import min_exponent

def check(path):
    declared = None; pairs = []; sets = 0
    for line in open(path):
        if line.startswith('#'):
            m = re.search(r'contains (\d+) pairs', line); sets += line.startswith('# S = ')
            if m: declared = int(m.group(1))
            continue
        m = re.match(r'\((-?\d+),(-?\d+)\)', line.strip())
        if m: pairs.append(tuple(map(int, m.groups())))
    power = 2 if 'Square' in path else 3
    hits = {2: [], 3: [], 4: []}
    for x, y in pairs:
        s = x + y; assert x >= y, (x, y)
        if s > 0: root = round(s ** (1 / power)); assert any((root + d) ** power == s for d in (-1, 0, 1)), (x, y)
        if s <= 0 or y == 0 or gcd(x, y) != 1: continue
        k = min(map(min_exponent, (abs(x), abs(y), s)))
        for r in hits:
            if k >= r: hits[r].append((x, y, s))
    n = len(pairs); d = len(set(pairs))
    assert declared in (n, d), ('pair count differs from the file header', declared, n, d)
    print(f'{path.split("/")[-1]}: {n} lines, {d} distinct pairs (header {declared}), {max(sets, 1)} set(s) S, '
          f'largest |x| = {max(abs(x) for x, _ in pairs)}')
    for r in hits: print(f'  x, |y|, x+y all {r}-powerful, gcd 1: {len(hits[r])}', *hits[r][:5])
    return hits

if __name__ == '__main__':
    for p in sys.argv[1:]: check(p)
