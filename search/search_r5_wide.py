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

def _append(f, line):
    f.write(line + '\n'); f.flush(); os.fsync(f.fileno())

def segments(KX, budget, path=None):
    """path: checkpoint file, one 'lo hi' line per segment found, then 'end'; an interrupted run resumes from it."""
    out = []
    if path and os.path.exists(path):
        rows = open(path).read().split('\n')
        rows = rows[:-1]                                     # drop the possibly torn last line (no newline yet)
        if rows and rows[-1] == 'end': return [tuple(map(int, l.split())) for l in rows[:-1]]
        out = [tuple(map(int, l.split())) for l in rows]
        with open(path, 'w') as f: f.write(''.join(f'{a} {b}\n' for a, b in out))
    f = open(path, 'a') if path else None
    lo = out[-1][1] if out else 0
    while lo <= KX:
        if _count(lo, KX + 1) <= budget: out.append((lo, KX + 1)); f and _append(f, f'{lo} {KX + 1}'); break
        a, b = lo + 1, KX + 1
        while b - a > 1:
            m = (a + b) // 2
            if _count(lo, m) <= budget: a = m
            else: b = m
        out.append((lo, a)); f and _append(f, f'{lo} {a}'); lo = a
    if f: _append(f, 'end'); f.close()
    return out

def _segment_k(ks):
    k, seg = ks; part, a, b = _segment(seg); return k, part, a, b

def search(r, X, budget=30_000_000, workers=None, sh=None, log=None, primes=None, ckpt=None):
    """ckpt: directory for checkpoints (segments.txt, done.txt); rerunning with the same arguments resumes."""
    if sh is None: sh = max(0, X.bit_length() - 61)
    if ckpt:
        os.makedirs(ckpt, exist_ok=True); tag = f'r={r} X={X} sh={sh} budget={budget} primes={primes}'
        tp = os.path.join(ckpt, 'params.txt')
        if os.path.exists(tp): assert open(tp).read() == tag, ('checkpoint of another run', ckpt)
        else: open(tp, 'w').write(tag)
    _init(r, X, sh, primes); KX = X >> sh
    segs = segments(KX, budget, ckpt and os.path.join(ckpt, 'segments.txt')); t0 = time.time()
    if log: print(f'N={N}, shift={sh}, segments={len(segs)}', file=log, flush=True)
    sols = set(); ns = nd = 0; done = set(); f = None
    if ckpt:                                                 # done.txt: 'sol a b c e' lines, then 'seg k ns nd' per segment
        dp = os.path.join(ckpt, 'done.txt')
        if os.path.exists(dp):
            txt = open(dp).read(); txt = txt[:txt.rfind('\n') + 1]   # drop a torn last line
            open(dp, 'w').write(txt)
            for l in txt.split('\n')[:-1]:
                w = l.split()
                if w[0] == 'seg': done.add(int(w[1])); ns += int(w[2]); nd += int(w[3])
                else: sols.add(tuple(map(int, w[1:])))
            if log: print(f'resumed: {len(done)} segments already done, sols={len(sols)}', file=log, flush=True)
        f = open(dp, 'a')
    todo = [(k, sg) for k, sg in enumerate(segs) if k not in done]
    with Pool(workers or max(1, (os.cpu_count() or 2) // 2), _init, (r, X, sh, primes)) as pool:
        for n, (k, part, a, b) in enumerate(pool.imap_unordered(_segment_k, todo), len(done)):
            sols.update(part); ns += a; nd += b
            if f:                                            # solutions before the 'seg' line, so a torn write loses only the segment
                f.write(''.join('sol ' + ' '.join(map(str, s)) + '\n' for s in part)); _append(f, f'seg {k} {a} {b}')
            if log and (n + 1) % 10 == 0: print(f'segments {n+1}/{len(segs)} {time.time()-t0:.0f}s sols={len(sols)}', file=log, flush=True)
    if f: f.close()
    lim = (KX + 1) << sh                                    # sums with an admissible key are those < lim
    exp_s = sum(max(0, bisect.bisect_left(L, lim - L[q]) - q) for q in range(N))
    assert nd == N*(N-1)//2 and ns == exp_s, ('coverage', nd, N*(N-1)//2, ns, exp_s)
    return sorted((s for s in sols if s[3] <= X), key=lambda s: (s[3], s)), N

if __name__ == '__main__':
    r = int(sys.argv[1]); X = int(float(sys.argv[2])); t = time.time()
    ps = [int(p) for p in sys.argv[4].split(',')] if len(sys.argv) > 4 else None   # optional support, e.g. 2,3,7,13,17
    ck = os.environ.get('CKPT')                                                  # checkpoint directory, optional
    sols, n = search(r, X, workers=int(sys.argv[3]) if len(sys.argv) > 3 else None, log=sys.stdout, primes=ps, ckpt=ck)
    print(f'r={r} X={X} primes={ps or "all"} N={n} solutions={len(sols)} time={time.time()-t:.0f}s')
    for s in sols: print(*s)
