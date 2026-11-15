"""search_square_family vs a naive loop; and with threshold relaxed, the naive loop must find something."""
from math import gcd
from rpow import rpowerful, is_rpowerful_naive
from search_square_family import search
if __name__ == '__main__':
    B = 10**9
    pairs, _ = search(B, 2)
    P5 = rpowerful(5, B); odd = [n for n in P5 if n % 2 and n > 1]
    even = [m << k for m in [n for n in P5 if n % 2] for k in range(4, 40) if (m << k) <= B]
    naive = sorted((u, v) for u in even for v in odd if gcd(u, v) == 1 and is_rpowerful_naive(u+v, 3))
    assert pairs == naive, (len(pairs), len(naive)); print(f'square family == naive for B={B}: {len(naive)} pairs OK')
    for u, v in pairs:
        for n in (u*u, 2*u*v, v*v, (u+v)**2): assert is_rpowerful_naive(n, 5)
    print('every reported solution is 5-powerful (naive factorisation): OK')
    B = 10**5                                   # relaxed levels (2, 2): the hit path must agree with a naive loop
    pairs, _ = search(B, 2, rp=2, rw=2)
    P = rpowerful(2, B); odd = [n for n in P if n % 2 and n > 1]
    even = [m << k for m in [n for n in P if n % 2] for k in range(4, 40) if (m << k) <= B]
    naive = sorted((u, v) for u in even for v in odd if gcd(u, v) == 1 and is_rpowerful_naive(u+v, 2))
    assert pairs == naive and len(naive) > 0, (len(pairs), len(naive)); print(f'relaxed (2,2) family == naive for B={B}: {len(naive)} pairs OK')
