"""Exhaustive search beyond 64 bits: a+b+c = e, a<=b<=c, all four r-powerful, e <= X, gcd(a,b,c)=1.

Same statement and same segment idea as search_r5_seg.py, but every number n is split as
    n = key * 2^SH + low,   0 <= low < 2^SH,   key < 2^62,
so that X may exceed 2^63. Sums a+b and differences e-c are computed on (key, low) with explicit carry / borrow,
matched on the key by sorting, then filtered on the low part. Every reported solution is re-checked with exact
Python integers. Coprimality: a bitmask of the primes <= 61 dividing each number removes most common factors
in bulk; the survivors get an exact gcd.
Checks of exhaustiveness: every difference is counted in exactly one segment, and the number of sums counted
equals the exact number of pairs whose sum has an admissible key (both asserted)."""
import sys, time, os, bisect, numpy as np
from math import gcd
from multiprocessing import Pool
from rpow import rpowerful, primes_upto

SMALL = primes_upto(61)

def _init(r, X, sh, primes=None):
    global L, K, LO, MASK, N, SH, M
    L = rpowerful(r, X, primes); N = len(L); SH = sh; M = (1 << sh) - 1
    K = np.array([n >> sh for n in L], dtype=np.int64); LO = np.array([n & M for n in L], dtype=np.int64)
    MASK = np.array([sum(1 << t for t, p in enumerate(SMALL) if n % p == 0) for n in L], dtype=np.int64)
    assert int(K[-1]) < 2**62 - 2

def _expand(start, cnt):
    Mx = int(cnt.sum()); first = np.repeat(np.arange(len(cnt)), cnt); off = np.cumsum(cnt) - cnt
    return first, np.arange(Mx) - np.repeat(off, cnt) + np.repeat(start, cnt)

def _ranges(lo, hi):
    """candidate index ranges. sums: K[i]+K[j] in [lo-1, hi), j>=i. differences: K[e]-K[c] in [lo, hi+1), e>c."""
    idx = np.arange(N)
    j0 = np.maximum(np.searchsorted(K, lo - 1 - K), idx); j1 = np.searchsorted(K, hi - K)
    e0 = np.maximum(np.searchsorted(K, K + lo), idx + 1); e1 = np.searchsorted(K, K + hi + 1)
    return j0, np.maximum(j1 - j0, 0), e0, np.maximum(e1 - e0, 0)

def _count(lo, hi):
    _, cs, _, cd = _ranges(lo, hi); return int(cs.sum()) + int(cd.sum())

def _segment(seg):
    lo, hi = seg
    j0, cs, e0, cd = _ranges(lo, hi)
    i, j = _expand(j0, cs); t = LO[i] + LO[j]; sk = K[i] + K[j] + (t >> SH); sl = t & M
    keep = (sk >= lo) & (sk < hi); i, j, sk, sl = i[keep], j[keep], sk[keep], sl[keep]
    o = np.argsort(sk, kind='stable'); sk, sl, i, j = sk[o], sl[o], i[o], j[o]
    c, e = _expand(e0, cd); t = LO[e] - LO[c]; dk = K[e] - K[c] - (t < 0); dl = t & M
    keep = (dk >= lo) & (dk < hi); c, e, dk, dl = c[keep], e[keep], dk[keep], dl[keep]
    Lf = np.searchsorted(sk, dk, 'left'); Rt = np.searchsorted(sk, dk, 'right')
    hit = np.nonzero(Rt > Lf)[0]
    d, s = _expand(Lf[hit], Rt[hit] - Lf[hit]); d = hit[d]
    ok = (sl[s] == dl[d]) & (j[s] <= c[d]) & ((MASK[i[s]] & MASK[j[s]] & MASK[c[d]]) == 0)
    out = []
    for ia, ib, ic, ie in zip(i[s][ok].tolist(), j[s][ok].tolist(), c[d][ok].tolist(), e[d][ok].tolist()):
        a, b, cc, ee = L[ia], L[ib], L[ic], L[ie]
        assert a + b + cc == ee and a <= b <= cc, 'key/low arithmetic disagrees with exact integers'
        if gcd(gcd(a, b), cc) == 1: out.append((a, b, cc, ee))
    return out, len(sk), len(dk)

def segments(KX, budget):
    out = []; lo = 0
    while lo <= KX:
        if _count(lo, KX + 1) <= budget: out.append((lo, KX + 1)); break
        a, b = lo + 1, KX + 1
        while b - a > 1:
            m = (a + b) // 2
            if _count(lo, m) <= budget: a = m
            else: b = m
        out.append((lo, a)); lo = a
    return out

def search(r, X, budget=30_000_000, workers=None, sh=None, log=None, primes=None):
    if sh is None: sh = max(0, X.bit_length() - 61)
    _init(r, X, sh, primes); KX = X >> sh; segs = segments(KX, budget); t0 = time.time()
    if log: print(f'N={N}, shift={sh}, segments={len(segs)}', file=log, flush=True)
    sols = set(); ns = nd = 0
    with Pool(workers or max(1, (os.cpu_count() or 2) // 2), _init, (r, X, sh, primes)) as pool:
        for k, (part, a, b) in enumerate(pool.imap_unordered(_segment, segs)):
            sols.update(part); ns += a; nd += b
            if log and (k + 1) % 10 == 0: print(f'segments {k+1}/{len(segs)} {time.time()-t0:.0f}s sols={len(sols)}', file=log, flush=True)
    lim = (KX + 1) << sh                                    # sums with an admissible key are those < lim
    exp_s = sum(max(0, bisect.bisect_left(L, lim - L[q]) - q) for q in range(N))
    assert nd == N*(N-1)//2 and ns == exp_s, ('coverage', nd, N*(N-1)//2, ns, exp_s)
    return sorted((s for s in sols if s[3] <= X), key=lambda s: (s[3], s)), N

if __name__ == '__main__':
    r = int(sys.argv[1]); X = int(float(sys.argv[2])); t = time.time()
    ps = [int(p) for p in sys.argv[4].split(',')] if len(sys.argv) > 4 else None   # optional support, e.g. 2,3,7,13,17
    sols, n = search(r, X, workers=int(sys.argv[3]) if len(sys.argv) > 3 else None, log=sys.stdout, primes=ps)
    print(f'r={r} X={X} primes={ps or "all"} N={n} solutions={len(sols)} time={time.time()-t:.0f}s')
    for s in sols: print(*s)
