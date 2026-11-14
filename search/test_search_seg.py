"""search_r5_seg (segmented, parallel) vs search_r5 (pair-sum table), small budgets to force many segments."""
from search_r5 import search as ref
from search_r5_seg import search as seg
if __name__ == '__main__':
    for r, X, budget in ((2, 3000, 500), (3, 300000, 2000), (4, 10**8, 20000), (5, 3*10**11, 50000), (5, 10**13, 10**6)):
        s1 = ref(r, X)[0]; s2 = seg(r, X, budget=budget, workers=3)[0]
        assert s1 == s2, (r, X, len(s1), len(s2))
        print(f'seg == ref for r={r}, X={X}: {len(s1)} solutions OK')
