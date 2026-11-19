# erdos939-lean

Lean 4 proofs of the four solved-but-unproved variants of
[Erdős problem 939](https://www.erdosproblems.com/939) in
[formal-conjectures](https://github.com/google-deepmind/formal-conjectures)
(`FormalConjectures/ErdosProblems/939.lean`), stated with its own definition `Erdos939Sums`:

| formal-conjectures statement | proof here (`Erdos939/Main.lean`) |
|---|---|
| `erdos_939.variants.infinite_of_six_le` : `∀ r ≥ 6, (Erdos939Sums r).Infinite` | `Erdos939Proofs.infinite_of_six_le` |
| `erdos_939.variants.finite` : `¬ ∀ r ≥ 4, (Erdos939Sums r).Finite` | `Erdos939Proofs.finite` |
| `erdos_939.variants.seven` : `(Erdos939Sums 7).Nonempty` | `Erdos939Proofs.seven` |
| `erdos_939.variants.eight` : `(Erdos939Sums 8).Nonempty` | `Erdos939Proofs.eight` |

`Main.lean` checks by `rfl` that each proved statement is the formal-conjectures one.
No `sorry`; axioms: `propext`, `Classical.choice`, `Quot.sound`.
This is a formalisation of a known argument, not new mathematics. The main question
of problem 939 (`r = 4`, and finiteness for `r = 5`) stays open.

## Credit

- Construction: GPT-5.5 Pro, prompted by Liam Price
  ([forum thread](https://www.erdosproblems.com/forum/thread/939), 24 May 2026).
- First Lean formalisation: Aristotle (Harmonic), linked from that thread, with its own
  definitions (tuples `Fin (r - 2) → ℕ`). `Erdos939/Price.lean` is that file, ported from
  Mathlib v4.28.0 (one proof step replaced).
- `Erdos939/Main.lean`: bridge to the formal-conjectures definitions
  (distinct summands as a `Finset`, positivity, global gcd 1).

## Build

formal-conjectures is pinned by commit in `lakefile.toml` (Lean v4.33.1).

```bash
lake exe cache get
```

```bash
lake build
```

`formal-conjectures-pr.patch` is the draft change for formal-conjectures (adds
`@[formal_proof using lean4 at ...]`); its linter requires a Palomar registry URL, left
as `PALOMAR-TODO`.
