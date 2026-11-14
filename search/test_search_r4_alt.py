"""search_r4_alt vs search_r4 on small bounds (trivial a = 1 solutions included)."""
from search_r4 import search as s1
from search_r4_alt import search as s2
if __name__ == '__main__':
    for r, X in ((2, 20000), (3, 10**7), (3, 10**10), (4, 10**12)):
        a = s1(r, X, 3)[0]; b = s2(r, X, 3); assert a == b, (r, X, len(a), len(b))
        print(f'r4_alt == r4 for r={r}, X={X}: {len(a)} solutions OK')
