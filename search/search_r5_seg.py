"""Exhaustive search, second algorithm: a+b+c = e, a<=b<=c, all four r-powerful, e <= X < 2^63, gcd(a,b,c)=1.

Same statement as search_r5.py, independent method with bounded memory: the value range [0, X] is cut into
segments [lo, hi). In each segment we list every pair sum a+b (a<=b) and every difference e-c (c<e) lying in
it, sort the sums, and look every difference up. Each solution has a+b = e-c in exactly one segment, so the
union over segments is exhaustive. Everything is vectorised; segments run in worker processes."""
import sys, time, os, numpy as np
from multiprocessing import Pool
from rpow import rpowerful

def _init(r, X):
    global P, Pu, N
    P = np.array(rpowerful(r, X), dtype=np.int64); Pu = P.astype(np.uint64); N = len(P)

def _ranges(lo, hi):
    """index ranges: sums P[i]+P[j] in [lo,hi) with j>=i ; differences P[e]-P[c] in [lo,hi) with e>c"""
    idx = np.arange(N)
    j0 = np.maximum(np.searchsorted(P, lo - P), idx); j1 = np.searchsorted(P, hi - P)
    e0 = np.maximum(np.searchsorted(Pu, Pu + np.uint64(lo)), idx + 1); e1 = np.searchsorted(Pu, Pu + np.uint64(hi))
    return j0, np.maximum(j1 - j0, 0), e0, np.maximum(e1 - e0, 0)

def _expand(start, cnt):
    """all (i, k) with start[i] <= k < start[i]+cnt[i]"""
    M = int(cnt.sum()); first = np.repeat(np.arange(len(cnt)), cnt)
    off = np.cumsum(cnt) - cnt
    return first, np.arange(M) - np.repeat(off, cnt) + np.repeat(start, cnt)

def _count(lo, hi):
    _, cs, _, cd = _ranges(lo, hi); return int(cs.sum()) + int(cd.sum())

def _segment(seg):
    lo, hi = seg
    j0, cs, e0, cd = _ranges(lo, hi)
    i, j = _expand(j0, cs); sv = P[i] + P[j]
    o = np.argsort(sv, kind='stable'); sv = sv[o]; i = i[o]; j = j[o]
    c, e = _expand(e0, cd); dv = P[e] - P[c]
    L = np.searchsorted(sv, dv, 'left'); R = np.searchsorted(sv, dv, 'right')
    hit = np.nonzero(R > L)[0]
    d, t = _expand(L[hit], R[hit] - L[hit])            # d indexes hit, t indexes the sorted sums
    a, b, cc, ee = P[i[t]], P[j[t]], P[c[hit[d]]], P[e[hit[d]]]
    ok = (b <= cc) & (np.gcd(np.gcd(a, b), cc) == 1)
    return [tuple(int(v) for v in s) for s in zip(a[ok], b[ok], cc[ok], ee[ok])], len(sv) + len(dv)

def segments(X, budget):
    """cut [0, X+1) so that each segment holds at most `budget` sums + differences"""
    out = []; lo = 0
    while lo <= X:
        if _count(lo, X + 1) <= budget: out.append((lo, X + 1)); break
        a, b = lo + 1, X + 1                           # largest hi with count(lo, hi) <= budget
        while b - a > 1:
            m = (a + b) // 2
            if _count(lo, m) <= budget: a = m
            else: b = m
        assert _count(lo, a) <= budget, 'a single value exceeds the budget'
        out.append((lo, a)); lo = a
    return out

def search(r, X, budget=30_000_000, workers=None, log=None):
    assert X < 2**63
    _init(r, X); segs = segments(X, budget); t0 = time.time()
    if log: print(f'N={N}, segments={len(segs)}', file=log, flush=True)
    sols = set(); total = 0
    with Pool(workers or max(1, (os.cpu_count() or 2) // 2), _init, (r, X)) as pool:
        for k, (part, m) in enumerate(pool.imap_unordered(_segment, segs)):
            sols.update(part); total += m
            if log and (k + 1) % 10 == 0: print(f'segments {k+1}/{len(segs)} {time.time()-t0:.0f}s sols={len(sols)}', file=log, flush=True)
    assert total == N*(N+1)//2 - _pairs_over(X) + N*(N-1)//2, 'segments do not cover every pair exactly once'
    return sorted(sols, key=lambda s: (s[3], s)), N

def _pairs_over(X):
    """number of pairs i<=j with P[i]+P[j] > X (those are in no segment)"""
    return int((N - np.maximum(np.searchsorted(P, X + 1 - P), np.arange(N))).clip(0).sum())

if __name__ == '__main__':
    r = int(sys.argv[1]); X = int(float(sys.argv[2])); t = time.time()
    sols, n = search(r, X, log=sys.stdout)
    print(f'r={r} X={X} N={n} solutions={len(sols)} time={time.time()-t:.0f}s')
    for s in sols: print(*s)
