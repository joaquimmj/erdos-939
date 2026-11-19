"""Checkpoint/resume of search_r5_wide: a run killed mid-way and resumed gives the same result as a plain run."""
import os, shutil, signal, subprocess, sys, tempfile, time
import search_r5_wide as w
r, X, B = 5, 10**16, 200_000
ref = w.search(r, X, budget=B, workers=2)
d = tempfile.mkdtemp()
code = f"import search_r5_wide as w; w.search({r}, {X}, budget={B}, workers=2, ckpt={d!r})"
def count(name, word):
    q = os.path.join(d, name); return open(q).read().count(word) if os.path.exists(q) else 0
for name, word, n in (('segments.txt', '\n', 10), ('done.txt', 'seg ', 5)):   # kill during the segmentation, then during the search
    p = subprocess.Popen([sys.executable, '-c', code], start_new_session=True)
    while count(name, word) < n: time.sleep(0.05)
    os.killpg(p.pid, signal.SIGKILL); p.wait()
    assert count('segments.txt', 'end') == (name == 'done.txt')
    print('killed:', open(os.path.join(d, 'segments.txt')).read().count('\n'), 'segment lines,',
          open(os.path.join(d, 'done.txt')).read().count('seg ') if os.path.exists(os.path.join(d, 'done.txt')) else 0, 'done')
res = w.search(r, X, budget=B, workers=2, ckpt=d)
assert res == ref, (res, ref)
shutil.rmtree(d); print('checkpoint resume == plain run: OK', ref[1], len(ref[0]))
