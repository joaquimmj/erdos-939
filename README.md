# erdos-939: sums of r-powerful numbers

A number is **r-powerful** if every prime that divides it divides it at least r times (for example 2⁵ · 3⁶ is
5-powerful). [Erdős problem #939](https://www.erdosproblems.com/939) asks, for r ≥ 4: can a sum of r − 2 coprime
r-powerful numbers be r-powerful, and can this happen infinitely often?

The answer to the second question is known to be yes for every r ≥ 6, by a construction of Price. **r = 4 and r = 5 are
open**: for r = 5 only two solutions are known (found by Kitamura and Cambie), and for r = 4 none.

**This repository does not solve the problem.** It pushes exhaustive searches much further, checks the known
solutions independently, and rules out some families of polynomial identities.

## Results

| Search | Bound | Result |
| r = 5: a + b + c = e, gcd(a, b, c) = 1 | e ≤ **10²²** | only the two known solutions (two runs and two generators up to 10²⁰, one run beyond) |
| r = 5: a + b + c = e, gcd(a, b, c) = 1 | e ≤ **10²⁰** | only the two known solutions |
| r = 4: a + b = c, gcd(a, b) = 1 | c ≤ **9·10¹⁸** | no solution, even with a = 1 |
| r = 4, all primes of abc ≤ 53, or rad(abc) ≤ 10⁷ | **no size bound** | no solution (filter of the complete S-unit lists of von Känel–Matschke) |
| r = 4 (even r = 3): two terms supported on S, third a square or a cube; S = {2,3,5,7,11}, {2,3,5,p ≤ 31}, {2,3,p ≤ 100}, {2,p ≤ 250} | **no size bound**, any support for the third term | no solution (complete sums-of-units lists of von Känel–Matschke) |
| r = 5, all primes ≤ 37 | e ≤ 10²² | only Kitamura's solution (one run) |
| r = 5, restricted family (U + V)² = U² + 2UV + V² | U, V ≤ 4.5·10¹⁸ (e up to about 2·10³⁷) | no solution |
| r = 3 (control) | c ≤ 10¹⁰ | finds Nitaj's solution |

"Exhaustive" means that every r-powerful number up to the bound is listed and every sum is tested in exact
integer arithmetic. Each search is tested against brute force on small bounds, and the main results are confirmed
by two or three independent programs:
- for r = 5, the result up to 10¹⁶ is reproduced by two algorithms, and the run up to 10²⁰ uses a third program
  that goes beyond 64-bit integers;
- for r = 4, the result up to 9·10¹⁸ is reproduced by a second computation path.

The two known r = 5 solutions are checked independently: exact sum, factorisations by three methods (trial division,
sympy and PARI/GP), proven primality of the factors and global gcd 1.

**Polynomial identities.** Price's construction for r ≥ 6 is a polynomial identity. For r = 5 we searched for a
similar identity with four terms and found partial negative results: at most one term can be a monomial (proved by
hand), the case of one monomial and three one-root terms is excluded by exact computation (33,963 Gröbner bases),
and none of 138 tested root configurations gives an identity. Details in `notes/o3_identities.md`, and why Price's
identity stops at r = 6 in `notes/o3_r5.md`.

## Lean

`lean/` proves, in Lean 4 with Mathlib, the four `research solved` statements of formal-conjectures for this
problem (`Erdos939Sums r` is infinite for every r ≥ 6, and the `finite`, `seven`, `eight` variants), against their
exact definitions. The construction is Price's (found with GPT-5.5 Pro); the formalisation is Aristotle's, ported to
Lean v4.33.1. Build: `cd lean && lake exe cache get && lake build`. See `lean/README.md`.

## Layout

| Path | Role |
|---|---|
| `search/rpow.py` | exact enumeration of r-powerful numbers up to X |
| `search/search_r5.py` | a + b + c = e, exhaustive, using a table of pairwise sums |
| `search/search_r5_seg.py` | same statement, independent second algorithm (value segments, bounded memory, parallel) |
| `search/search_r5_wide.py` | same statement beyond 64 bits, used up to 10²⁰ |
| `search/search_r4.py` | a + b = c, exhaustive, parallel |
| `search/search_square_family.py`, `search/identities_gfermat.py` | the (U + V)² family and identities above a generalised Fermat equation |
| `search/identities*.py`, `search/identities_batch.sh` | search for four-term polynomial identities |
| `search/verify.py` | independent check of a solution |
| `search/test_*.py` | comparisons with brute force and between the algorithms |
| `results/` | raw outputs |
| `notes/` | state of the problem, notes on identities, raw copies of the pages read |

`REPORT.md` (results and how certain each one is) and `LOG.md` (work log) are in French.

## Reproduce

Python 3.9+ with `numpy` and `sympy`; PARI/GP (`gp`) is optional, for `verify.py`.

```bash
cd search
python3 test_search.py && python3 test_search_r4.py && python3 test_search_seg.py
python3 search_r5_seg.py 5 1e16     # ~5 min, ~2 GB of RAM
python3 search_r5_seg.py 5 9e18     # ~1 h on 5 processes, ~5 GB of RAM
python3 search_r5_wide.py 5 1e20 6  # ~2 h 40 on 6 processes, ~8 GB of RAM
python3 search_r4.py 4 9e18         # ~30 min on 8 processes
python3 verify.py
python3 identities.py 12 5 1 -1     # identities of degree <= 12
```

Joaquim Manji-Jung, Paris.
