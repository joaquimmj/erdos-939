"""Second generator of the r-powerful numbers <= X, written apart from rpow.py (no shared code):
primes by trial division, numbers built prime by prime (no recursion), integer root by bisection.
Run it to compare both generators at the bounds used by the searches."""
def rpowerful2(r, X):
    lo, hi = 1, 1 << (X.bit_length() // r + 1)              # largest b with b**r <= X
    while hi - lo > 1:
        m = (lo + hi) // 2
        lo, hi = (m, hi) if m**r <= X else (lo, m)
    ps = [p for p in range(2, lo + 1) if all(p % q for q in range(2, int(p**.5) + 1))]
    out = [1]
    for p in ps:                                             # multiply every number built so far by p^k, k >= r
        new = []
        for n in out:
            m = n * p**r
            while m <= X: new.append(m); m *= p
        out += new
    return sorted(out)
if __name__ == '__main__':
    import sys, hashlib
    from rpow import rpowerful, is_rpowerful_naive
    for r, X in ((2, 3000), (3, 10**5), (5, 10**6)):         # both against the definition
        ref = [n for n in range(1, X + 1) if is_rpowerful_naive(n, r)]
        assert rpowerful2(r, X) == ref == rpowerful(r, X), (r, X)
    for r, X in ((5, 10**20), (4, 9 * 10**18), (5, 9 * 10**18), (3, 10**10)):
        a, b = rpowerful(r, X), rpowerful2(r, X)
        assert a == b, (r, X, len(a), len(b))
        print(f'r={r} X={X}: {len(a)} numbers, both generators agree, sha256={hashlib.sha256(repr(a).encode()).hexdigest()[:16]}')
