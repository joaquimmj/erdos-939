"""search_r5_wide with the second generator (rpow2.py) in place of rpow.py: python3 run_gen2.py 5 1e20 [workers]"""
import os, sys, time, search_r5_wide as w
from rpow2 import rpowerful2
w.rpowerful = lambda r, X, primes=None: rpowerful2(r, X)     # workers are forked, they inherit the patch
if __name__ == '__main__':
    r = int(sys.argv[1]); X = int(float(sys.argv[2])); t = time.time()
    sols, n = w.search(r, X, workers=int(sys.argv[3]) if len(sys.argv) > 3 else None, log=sys.stdout, ckpt=os.environ.get('CKPT'))   # CKPT: optional checkpoint directory
    print(f'r={r} X={X} generator=rpow2 N={n} solutions={len(sols)} time={time.time()-t:.0f}s')
    for s in sols: print(*s)
