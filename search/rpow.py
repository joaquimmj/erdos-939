"""All r-powerful numbers <= X (every prime exponent >= r), 1 included. Exact integers."""
def primes_upto(b):
    s = bytearray([1])*(b+1); s[0:2] = b"\x00\x00"
    for i in range(2, int(b**.5)+1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(b+1) if s[i]]
def iroot(n, k):
    x = int(round(n ** (1.0/k)))
    while x**k > n: x -= 1
    while (x+1)**k <= n: x += 1
    return x
def rpowerful(r, X):
    ps = primes_upto(iroot(X, r) + 1); out = []
    def rec(i, n):
        out.append(n)
        for j in range(i, len(ps)):
            p = ps[j]; m = n * p**r
            if m > X: break
            while m <= X:
                rec(j+1, m); m *= p
    rec(0, 1)
    return sorted(out)
def is_rpowerful_naive(n, r):
    p = 2
    while p*p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0: n //= p; e += 1
            if e < r: return False
        p += 1
    return n == 1
