import Erdos939.Price
import FormalConjectures.ErdosProblems.«939»

/-!
# Erdős Problem 939: the solved variants

Proofs of the four `research solved` statements left as `sorry` in
`FormalConjectures/ErdosProblems/939.lean`, with the exact definition `Erdos939Sums`
of formal-conjectures. The mathematics is Price's construction (`Erdos939/Price.lean`);
this file only translates between the two sets of definitions.
-/

open Erdos939

namespace Erdos939Proofs

theorem full_of_isPowerful {r n : ℕ} (h : IsPowerful r n) : r.Full n :=
  fun p hp => h p (Nat.prime_of_mem_primeFactors hp) (Nat.dvd_of_mem_primeFactors hp)

/-- Statement of `Erdos939.erdos_939.variants.infinite_of_six_le`. -/
theorem infinite_of_six_le : ∀ r ≥ 6, (Erdos939Sums r).Infinite := by
  intro r hr
  refine Set.Infinite.of_image (fun S : Finset ℕ => ∑ s ∈ S, s)
    ((infinite_rpowerful_sums r hr).mono ?_)
  rintro N ⟨-, hN, f, hpos, hpow, hsum, hcop, hinj⟩
  have hS : ∑ s ∈ Finset.univ.image f, s = N := by
    rw [Finset.sum_image fun _ _ _ _ h => hinj h]; exact hsum
  refine ⟨Finset.univ.image f, ⟨?_, ?_, ?_, ?_⟩, hS⟩
  · simp [Finset.card_image_of_injective _ hinj]
  · by_contra hg
    obtain ⟨p, hp, hpd⟩ := Nat.exists_prime_and_dvd hg
    obtain ⟨i, hi⟩ := hcop p hp
    exact hi (hpd.trans (Finset.gcd_dvd (f := id) (Finset.mem_image_of_mem f (Finset.mem_univ i))))
  · rw [hS]; exact full_of_isPowerful hN
  · intro s hs
    obtain ⟨i, -, rfl⟩ := Finset.mem_image.mp hs
    exact ⟨hpos i, full_of_isPowerful (hpow i)⟩

/-- Statement of `Erdos939.erdos_939.variants.finite`. -/
theorem finite : ¬ ∀ r ≥ 4, (Erdos939Sums r).Finite :=
  fun h => infinite_of_six_le 6 le_rfl (h 6 (by norm_num))

/-- Statement of `Erdos939.erdos_939.variants.seven`. -/
theorem seven : (Erdos939Sums 7).Nonempty := (infinite_of_six_le 7 (by norm_num)).nonempty

/-- Statement of `Erdos939.erdos_939.variants.eight`. -/
theorem eight : (Erdos939Sums 8).Nonempty := (infinite_of_six_le 8 (by norm_num)).nonempty

-- The statements proved here are syntactically those of formal-conjectures.
example : type_of% infinite_of_six_le = type_of% erdos_939.variants.infinite_of_six_le := rfl
example : type_of% finite = type_of% erdos_939.variants.finite := rfl
example : type_of% seven = type_of% erdos_939.variants.seven := rfl
example : type_of% eight = type_of% erdos_939.variants.eight := rfl

end Erdos939Proofs

#print axioms Erdos939Proofs.infinite_of_six_le
