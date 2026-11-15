"""search_r5_wide (key/low split, beyond 64 bits) vs search_r5 (reference), with forced shifts so that the
carry, borrow and key-collision paths are exercised on small bounds."""
from search_r5 import search as ref
from search_r5_wide import search as wide
if __name__ == '__main__':
    for r, X, budget, sh in ((2, 3000, 500, 4), (2, 3000, 800, 0), (3, 300000, 2000, 5), (4, 10**8, 20000, 7), (5, 3*10**11, 50000, 4), (5, 10**13, 10**6, 9)):
        s1 = ref(r, X)[0]; s2 = wide(r, X, budget=budget, workers=3, sh=sh)[0]
        assert s1 == s2, (r, X, sh, len(s1), len(s2))
        print(f'wide == ref for r={r}, X={X}, shift={sh}: {len(s1)} solutions OK')
