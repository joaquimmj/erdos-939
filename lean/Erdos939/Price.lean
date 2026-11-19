/-
Construction: GPT-5.5 Pro, prompted by Liam Price
(https://www.erdosproblems.com/forum/thread/939, 24 May 2026).
Lean proof: autoformalised by Aristotle (Harmonic), linked from the same thread.
This file is that formalisation, ported from Mathlib v4.28.0 to the Mathlib version
pinned by formal-conjectures; the tuple-valued corollary at the end was dropped.
The bridge to the formal-conjectures statements is in `Erdos939/Main.lean`.
-/
import Mathlib

/-!
# Infinite r-Powerful Sums

For every integer r ≥ 6, we construct infinitely many identities in which a sum of r−2
jointly coprime r-powerful positive integers is again r-powerful.
-/

open Finset Nat BigOperators

/-- A positive integer `n` is `r`-powerful if every prime divisor `p` of `n`
    satisfies `p ^ r ∣ n`. -/
def IsPowerful (r : ℕ) (n : ℕ) : Prop :=
  ∀ p : ℕ, p.Prime → p ∣ n → p ^ r ∣ n

lemma isPowerful_pow (r : ℕ) (n : ℕ) : IsPowerful r (n ^ r) := by
  intro p pp dp; by_cases h : n = 0 <;> simp_all +decide [Nat.Prime.dvd_iff_not_coprime]
  · cases r <;> aesop
  · exact pow_dvd_pow_of_dvd (pp.dvd_of_dvd_pow (pp.dvd_iff_not_coprime.mpr dp)) _

lemma isPowerful_one (r : ℕ) : IsPowerful r 1 := by
  intro p hp hdiv; have := Nat.le_of_dvd (by decide) hdiv; interval_cases p <;> trivial

lemma isPowerful_mul {r a b : ℕ} (ha : IsPowerful r a) (hb : IsPowerful r b) :
    IsPowerful r (a * b) := by
  intro p hp h; rcases eq_or_ne a 0 <;> rcases eq_or_ne b 0 <;> simp_all +decide [ hp.dvd_mul ] ;
  rcases h with ( h | h ) <;> [ exact dvd_mul_of_dvd_left ( ha p hp h ) _; exact dvd_mul_of_dvd_right ( hb p hp h ) _ ]

lemma Int.gcd_sub_mul_eq_one {X Y : ℤ} (h : Int.gcd X Y = 1) :
    Int.gcd (X - Y) (X * Y) = 1 := by
  simp_all +decide [Int.gcd_eq_natAbs, Int.natAbs_mul, Nat.coprime_mul_iff_right]
  constructor <;> refine' Nat.coprime_of_dvd' _
  · intro k hk hk₁ hk₂; have := Nat.dvd_gcd hk₂ (show k ∣ Int.natAbs (Y) from ?_); aesop
    rw [← Int.natCast_dvd] at *; simp_all +decide [dvd_sub_right]
  · intro k hk hk₁ hk₂; have := Nat.dvd_gcd (show k ∣ Int.natAbs X from ?_) hk₂; simp_all +decide
    rw [← Int.natCast_dvd] at *; simp_all +decide [dvd_sub_left]

/-- The set of odd indices in `{1, ..., r}` excluding 3. -/
def oddIndicesNo3 (r : ℕ) : Finset ℕ :=
  ((Finset.Icc 1 r).filter (fun j => Odd j ∧ j ≠ 3))

/-- The set of all odd indices in `{0, ..., r}`. -/
def oddIndices (r : ℕ) : Finset ℕ :=
  ((Finset.range (r + 1)).filter (fun j => Odd j))

/-- The number of split terms. -/
def splitCount (r : ℕ) : ℕ := r / 2 - 2

lemma sum_range_succ_list (n : ℕ) :
    ((List.range n).map (fun i => i + 1)).sum = n * (n + 1) / 2 := by
  apply Nat.eq_div_of_mul_eq_right (by decide : 2 ≠ 0)
  induction n with
  | zero => simp
  | succ n ih =>
      rw [List.range_succ, List.map_append, List.sum_append]
      simp only [List.map_singleton, List.sum_singleton]
      rw [mul_add, ih]
      ring

lemma choose_two_ge_succ (n : ℕ) (hn : 4 ≤ n) : n + 1 ≤ n.choose 2 := by
  refine Nat.le_induction ?base ?step n hn
  · norm_num [Nat.choose]
  · intro n hn ih
    rw [show (n + 1).choose 2 = n.choose 1 + n.choose 2 by
      simpa using Nat.choose_succ_succ n 1]
    rw [Nat.choose_one_right]
    omega

lemma square_lt_two_choose_three (n : ℕ) (hn : 6 ≤ n) : n * n < 2 * n.choose 3 := by
  refine Nat.le_induction ?base ?step n hn
  · norm_num [Nat.choose]
  · intro n hn ih
    rw [show (n + 1).choose 3 = n.choose 2 + n.choose 3 by
      simpa using Nat.choose_succ_succ n 2]
    have htwo := choose_two_ge_succ n (by omega)
    nlinarith

lemma oddIndices_eq_image (r : ℕ) :
    oddIndices r = (Finset.range ((r + 1) / 2)).image (fun k => 2 * k + 1) := by
  ext j
  simp only [oddIndices, Finset.mem_filter, Finset.mem_range, Finset.mem_image]
  constructor
  · rintro ⟨hjlt, ⟨k, rfl⟩⟩
    exact ⟨k, by omega, by omega⟩
  · rintro ⟨k, hk, rfl⟩
    exact ⟨by omega, ⟨k, by ring⟩⟩

lemma oddIndices_card (r : ℕ) : (oddIndices r).card = (r + 1) / 2 := by
  rw [oddIndices_eq_image]
  rw [Finset.card_image_of_injective]
  · simp
  · intro a b h
    change 2 * a + 1 = 2 * b + 1 at h
    omega

lemma count_summands (r : ℕ) (hr : 6 ≤ r) :
    1 + (oddIndicesNo3 r).card + splitCount r = r - 2 := by
  have hthree_mem : 3 ∈ oddIndices r := by
    simp only [oddIndices, Finset.mem_filter, Finset.mem_range]
    exact ⟨by omega, by norm_num⟩
  have hno3_eq : oddIndicesNo3 r = (oddIndices r).erase 3 := by
    ext j
    simp only [oddIndicesNo3, oddIndices, Finset.mem_filter, Finset.mem_Icc,
      Finset.mem_erase, Finset.mem_range]
    constructor
    · rintro ⟨⟨hjpos, hjle⟩, hjodd, hjne⟩
      exact ⟨hjne, Nat.lt_succ_iff.mpr hjle, hjodd⟩
    · rintro ⟨hjne, hjlt, hjodd⟩
      exact ⟨⟨Odd.pos hjodd, Nat.lt_succ_iff.mp hjlt⟩, hjodd, hjne⟩
  have hcard_no3 : (oddIndicesNo3 r).card = (r + 1) / 2 - 1 := by
    rw [hno3_eq, Finset.card_erase_of_mem hthree_mem, oddIndices_card]
  unfold splitCount
  rw [hcard_no3]
  have hhalf_sum : (r + 1) / 2 + r / 2 = r := by
    rcases Nat.even_or_odd r with ⟨k, rfl⟩ | ⟨k, rfl⟩ <;> omega
  omega

lemma isPowerful_coeff_prod {r c a b B m : ℕ}
    (hb : 1 ≤ b) (hcoprime : Nat.Coprime m B)
    (hc : ∀ p : ℕ, p.Prime → p ∣ c → p ∣ B) :
    IsPowerful r (c * m ^ (r * a) * B ^ (r * b)) := by
  intro p hp
  by_cases hpc : p ∣ c
  · exact fun _ => dvd_mul_of_dvd_right (dvd_trans (pow_dvd_pow_of_dvd (hc p hp hpc) _)
      (pow_dvd_pow _ (by nlinarith))) _
  · by_cases hpm : p ∣ m
    · by_cases ha : a = 0 <;> simp_all +decide [mul_assoc, Nat.Prime.dvd_mul]
      · intro h; have := Nat.dvd_gcd hpm (hp.dvd_of_dvd_pow h); aesop
      · exact fun _ => dvd_mul_of_dvd_right (dvd_mul_of_dvd_left (dvd_trans
          (pow_dvd_pow_of_dvd hpm _) (pow_dvd_pow _
            (Nat.le_mul_of_pos_right _ (Nat.pos_of_ne_zero ha)))) _) _
    · intro h; have := hp.dvd_mul.mp h; simp_all +decide [Nat.Prime.dvd_mul]
      exact dvd_mul_of_dvd_right (dvd_trans (pow_dvd_pow_of_dvd
        (hp.dvd_of_dvd_pow (h.resolve_left (mt hp.dvd_of_dvd_pow hpm))) _)
        (pow_dvd_pow _ (show r ≤ r * b by nlinarith))) _

lemma factorization_prime_scaled_term {q c B r a b : ℕ}
    (hq : q.Prime) (hc : c ≠ 0) (hqc : ¬ q ∣ c) (hB : B ≠ 0) (hqB : ¬ q ∣ B) :
    (c * (q ^ r) ^ a * (B ^ r) ^ b).factorization q = r * a := by
  rw [Nat.factorization_mul]
  · rw [Nat.factorization_mul]
    · rw [Nat.factorization_pow, Nat.factorization_pow]
      have hcq : c.factorization q = 0 := by
        rw [Nat.factorization_eq_zero_iff]
        exact Or.inr (Or.inl hqc)
      have hBq : B.factorization q = 0 := by
        rw [Nat.factorization_eq_zero_iff]
        exact Or.inr (Or.inl hqB)
      simp [hcq, hBq, hq.factorization_self, Nat.mul_comm]
    · exact hc
    · exact pow_ne_zero _ (pow_ne_zero _ hq.ne_zero)
  · exact mul_ne_zero hc (pow_ne_zero _ (pow_ne_zero _ hq.ne_zero))
  · exact pow_ne_zero _ (pow_ne_zero _ hB)

lemma binomial_odd_identity (x y : ℤ) (n : ℕ) :
    (x + y) ^ n - (x - y) ^ n =
    2 * ∑ j ∈ (Finset.range (n + 1)).filter (fun j => Odd j),
      ↑(n.choose j) * x ^ (n - j) * y ^ j := by
  have h_expand : (x + y) ^ n = ∑ j ∈ Finset.range (n + 1),
      (Nat.choose n j : ℤ) * x ^ (n - j) * y ^ j ∧
    (x - y) ^ n = ∑ j ∈ Finset.range (n + 1),
      (Nat.choose n j : ℤ) * x ^ (n - j) * (-y) ^ j := by
    exact ⟨by rw [add_comm, add_pow]; ac_rfl, by rw [sub_eq_add_neg, add_comm, add_pow]; ac_rfl⟩
  have h_combine : (∑ j ∈ Finset.range (n + 1), Nat.choose n j * x ^ (n - j) * y ^ j) -
      (∑ j ∈ Finset.range (n + 1), Nat.choose n j * x ^ (n - j) * (-y) ^ j) =
      ∑ j ∈ Finset.filter (fun j => Odd j) (Finset.range (n + 1)),
        Nat.choose n j * x ^ (n - j) * y ^ j * 2 := by
    rw [← Finset.sum_sub_distrib, Finset.sum_filter]
    rw [← Finset.sum_congr rfl]; intros; split_ifs <;> simp_all +decide [Odd.neg_pow]; ring
  simp_all +decide [mul_comm, Finset.mul_sum _ _ _]

/-! ## The ℕ version of the binomial identity -/

/-
In ℕ, when X ≥ Y: (X+Y)^r = (X-Y)^r + 2 * ∑_{j odd} C(r,j) * X^(r-j) * Y^j
-/
lemma binomial_odd_nat (X Y : ℕ) (r : ℕ) (hXY : Y ≤ X) :
    (X + Y) ^ r = (X - Y) ^ r + 2 * ∑ j ∈ oddIndices r,
      r.choose j * X ^ (r - j) * Y ^ j := by
  have h_cast : ((X + Y) : ℤ) ^ r - ((X - Y) : ℤ) ^ r = 2 * ∑ j ∈ (Finset.range (r + 1)).filter (fun j => Odd j), (Nat.choose r j : ℤ) * X ^ (r - j) * Y ^ j := by
    convert binomial_odd_identity ( X : ℤ ) Y r using 1;
  simp_all +decide [ sub_eq_iff_eq_add, oddIndices ];
  norm_cast at h_cast;
  rw [ h_cast, add_comm ]

/-! ## Splitting the j=3 term -/

/-- The final coefficient in the paper's split of the `j = 3` term. -/
def lastCoeff (r : ℕ) : ℕ :=
  2 * r.choose 3 - ((splitCount r - 1) * splitCount r / 2)

/-- The paper's distinct coefficients `v₁, ..., v_t` splitting `2 * (r.choose 3)`. -/
def splitCoeffs (r : ℕ) : List ℕ :=
  (List.range (splitCount r - 1)).map (fun i => i + 1) ++ [lastCoeff r]

/-
The last coefficient is positive for r ≥ 6.
-/
lemma lastCoeff_pos (r : ℕ) (hr : 6 ≤ r) : 0 < lastCoeff r := by
  unfold lastCoeff
  have ht_le : splitCount r ≤ r := by
    unfold splitCount
    omega
  have htail_le_sq : (splitCount r - 1) * splitCount r / 2 ≤ r * r := by
    exact (Nat.div_le_self _ _).trans
      (Nat.mul_le_mul ((Nat.sub_le _ _).trans ht_le) ht_le)
  exact Nat.sub_pos_of_lt (htail_le_sq.trans_lt (square_lt_two_choose_three r hr))

lemma splitCount_lt_lastCoeff (r : ℕ) (hr : 6 ≤ r) :
    splitCount r < lastCoeff r := by
  unfold lastCoeff
  let t := splitCount r
  have htpos : 0 < t := by
    simp [t, splitCount]
    omega
  have ht_le : t ≤ r := by
    simp [t, splitCount]
    omega
  have htail_add_le_sq : ((t - 1) * t / 2) + t ≤ r * r := by
    have htail_le : (t - 1) * t / 2 ≤ (t - 1) * t := Nat.div_le_self _ _
    calc
      (t - 1) * t / 2 + t ≤ (t - 1) * t + t := Nat.add_le_add_right htail_le t
      _ = t * t := by
        have hsucc : t - 1 + 1 = t := Nat.sub_add_cancel htpos
        nlinarith
      _ ≤ r * r := Nat.mul_le_mul ht_le ht_le
  have hsum_lt : (t - 1) * t / 2 + t < 2 * r.choose 3 :=
    htail_add_le_sq.trans_lt (square_lt_two_choose_three r hr)
  rw [show splitCount r = t by rfl]
  rw [add_comm] at hsum_lt
  exact Nat.lt_sub_of_add_lt hsum_lt

lemma splitCoeffs_length (r : ℕ) (hr : 6 ≤ r) :
    (splitCoeffs r).length = splitCount r := by
  have htpos : 0 < splitCount r := by
    unfold splitCount
    omega
  simp [splitCoeffs]
  exact Nat.sub_add_cancel htpos

lemma splitCoeffs_sum (r : ℕ) (hr : 6 ≤ r) :
    (splitCoeffs r).sum = 2 * r.choose 3 := by
  unfold splitCoeffs lastCoeff
  rw [List.sum_append, List.sum_singleton, sum_range_succ_list]
  have htpos : 0 < splitCount r := by
    unfold splitCount
    omega
  rw [Nat.sub_add_cancel htpos]
  have hle : (splitCount r - 1) * splitCount r / 2 ≤ 2 * r.choose 3 := by
    have ht_le : splitCount r ≤ r := by
      unfold splitCount
      omega
    exact ((Nat.div_le_self _ _).trans
      (Nat.mul_le_mul ((Nat.sub_le _ _).trans ht_le) ht_le)).trans
      (le_of_lt (square_lt_two_choose_three r hr))
  rw [Nat.add_sub_of_le hle]

lemma splitCoeffs_pos (r : ℕ) (hr : 6 ≤ r) :
    ∀ c ∈ splitCoeffs r, 0 < c := by
  intro c hc
  simp [splitCoeffs] at hc
  rcases hc with ⟨i, hi, rfl⟩ | hlast
  · omega
  · simpa [hlast] using lastCoeff_pos r hr

lemma splitCoeffs_nodup (r : ℕ) (hr : 6 ≤ r) :
    (splitCoeffs r).Nodup := by
  unfold splitCoeffs
  apply List.Nodup.append
  · exact (List.nodup_range).map (by
      intro a b h
      change a + 1 = b + 1 at h
      omega)
  · simp
  · intro x hx hy
    simp at hy
    subst x
    simp at hx
    rcases hx with ⟨i, hi, hlast⟩
    have hi_le : i + 1 < lastCoeff r := by
      have hlt : i + 1 ≤ splitCount r - 1 := by omega
      have hmain := splitCount_lt_lastCoeff r hr
      omega
    omega

/-
The split sum of the j=3 term:
    (splitCount r - 1) * z + lastCoeff r * z = 2 * r.choose 3 * z
-/
lemma split_j3 (r : ℕ) (hr : 6 ≤ r) (z : ℕ) :
    ((splitCoeffs r).map (fun c => c * z)).sum = 2 * r.choose 3 * z := by
  rw [List.sum_map_mul_right]
  simpa using congrArg (fun n => n * z) (splitCoeffs_sum r hr)

/-! ## Decomposition of oddIndices -/

/-
oddIndices r = oddIndicesNo3 r ∪ {3} when r ≥ 6
-/
lemma oddIndices_decomp (r : ℕ) (hr : 6 ≤ r) :
    oddIndices r = oddIndicesNo3 r ∪ {3} := by
  ext j
  simp only [oddIndices, oddIndicesNo3, Finset.mem_filter, Finset.mem_range, Finset.mem_Icc,
    Finset.mem_union, Finset.mem_singleton]
  constructor
  · intro hj
    rcases hj with ⟨hjle_succ, hjodd⟩
    have hjle : j ≤ r := Nat.lt_succ_iff.mp hjle_succ
    by_cases h3 : j = 3
    · exact Or.inr h3
    · exact Or.inl ⟨⟨(Odd.pos hjodd), hjle⟩, hjodd, h3⟩
  · intro hj
    rcases hj with hno3 | rfl
    · exact ⟨Nat.lt_succ_iff.mpr hno3.1.2, hno3.2.1⟩
    · exact ⟨by omega, by norm_num⟩

/-
3 is not in oddIndicesNo3 r
-/
lemma three_not_in_oddIndicesNo3 (r : ℕ) : 3 ∉ oddIndicesNo3 r := by
  unfold oddIndicesNo3; aesop;

/-! ## The main decomposition lemma -/

/-
The key decomposition: for suitable m, B with r ≥ 6, the number (m^r + B^r)^r
    can be decomposed into r-2 jointly coprime r-powerful positive summands.
-/
lemma rpowerful_decomposition (r : ℕ) (hr : 6 ≤ r) (m B : ℕ)
    (hm : 0 < m) (hB : 0 < B) (hmB : Nat.Coprime m B) (hmgtB : B < m)
    (hmprime : m.Prime) (hBgt1 : 1 < B)
    (hcoeffs : ∀ j ∈ oddIndicesNo3 r, ∀ p : ℕ, p ∣ (2 * r.choose j) → p ∣ B)
    (hsplit : ∀ c ∈ splitCoeffs r, ∀ p : ℕ, p ∣ c → p ∣ B) :
    ∃ f : Fin (r - 2) → ℕ,
      (∀ i, 0 < f i) ∧
      (∀ i, IsPowerful r (f i)) ∧
      ∑ i, f i = (m ^ r + B ^ r) ^ r ∧
      (∀ p : ℕ, p.Prime → ∃ i, ¬ (p ∣ f i)) ∧
      Function.Injective f := by
  -- Set X = m^r, Y = B^r. Construct the list L of r-2 natural numbers:
  set X := m ^ r
  set Y := B ^ r
  set L : List ℕ := [(X - Y) ^ r] ++ ((oddIndicesNo3 r).sort (· ≤ ·)).map (fun j => 2 * r.choose j * X ^ (r - j) * Y ^ j) ++ (splitCoeffs r).map (fun c => c * X ^ (r - 3) * Y ^ 3);
  have hL_pos : ∀ x ∈ L, 0 < x := by
    simp +zetaDelta at *; (
    refine' ⟨ pow_pos ( Nat.sub_pos_of_lt ( Nat.pow_lt_pow_left hmgtB ( by linarith ) ) ) _, _ ⟩ ; rintro a ( ⟨ j, hj, rfl ⟩ | ⟨ c, hc, rfl ⟩ ) <;> simp_all +decide;
    · exact Nat.choose_pos ( by linarith [ Finset.mem_Icc.mp ( Finset.mem_filter.mp hj |>.1 ) ] );
    · exact splitCoeffs_pos r hr c hc)
  have hL_powerful : ∀ x ∈ L, IsPowerful r x := by
    simp +zetaDelta at *; (
    refine' ⟨ isPowerful_pow r _, _ ⟩
    intro a ha
    rcases ha with (⟨j, hj, rfl⟩ | ⟨c, hc, rfl⟩);
    · convert isPowerful_coeff_prod ( show 1 ≤ j from Nat.pos_of_ne_zero ( by rintro rfl; exact absurd ( Finset.mem_filter.mp hj |>.2.1 ) ( by norm_num ) ) ) hmB ( fun p _ hpdiv => hcoeffs j hj p hpdiv ) using 1;
      rw [ ← pow_mul, ← pow_mul ];
    · convert isPowerful_coeff_prod ( show 1 ≤ 3 by norm_num ) _ _ using 1;
      congr! 1;
      congr! 1;
      convert rfl using 1;
      convert pow_mul _ _ _ using 1;
      rotate_left;
      exacts [ B, hmB, fun p _ hpdiv => hsplit c hc p hpdiv, by ring ])
  have hL_sum : L.sum = (X + Y) ^ r := by
    -- By definition of $L$, we can expand its sum.
    have hL_sum_expand : L.sum = (X - Y) ^ r + ∑ j ∈ oddIndicesNo3 r, 2 * r.choose j * X ^ (r - j) * Y ^ j + ((splitCoeffs r).map (fun c => c * X ^ (r - 3) * Y ^ 3)).sum := by
      -- (ported: the original `grind +qlia` call no longer closes this goal)
      have h : (((oddIndicesNo3 r).sort (· ≤ ·)).map
          (fun j => 2 * r.choose j * X ^ (r - j) * Y ^ j)).sum =
          ∑ j ∈ oddIndicesNo3 r, 2 * r.choose j * X ^ (r - j) * Y ^ j := by
        rw [← Finset.sum_map_toList]
        exact ((sort_perm_toList (oddIndicesNo3 r) fun x y => x ≤ y).map _).sum_eq
      simp [L, h, add_assoc]
    generalize_proofs at *; (
    -- By binomial_odd_nat, we have (X + Y)^r = (X - Y)^r + 2 * ∑_{j ∈ oddIndices r} C(r,j) * X^(r-j) * Y^j.
    have h_binom_odd_nat : (X + Y) ^ r = (X - Y) ^ r + 2 * ∑ j ∈ oddIndices r, r.choose j * X ^ (r - j) * Y ^ j := by
      apply binomial_odd_nat; exact Nat.pow_le_pow_left hmgtB.le r;
    have hdisj : Disjoint (oddIndicesNo3 r) ({3} : Finset ℕ) := by
      rw [Finset.disjoint_singleton_right]
      exact three_not_in_oddIndicesNo3 r
    have hsum_odd :
        (∑ j ∈ oddIndices r, r.choose j * X ^ (r - j) * Y ^ j)
          = (∑ j ∈ oddIndicesNo3 r, r.choose j * X ^ (r - j) * Y ^ j)
            + r.choose 3 * X ^ (r - 3) * Y ^ 3 := by
      rw [oddIndices_decomp r hr, Finset.sum_union hdisj]
      simp
    let S₀ := ∑ j ∈ oddIndicesNo3 r, r.choose j * X ^ (r - j) * Y ^ j
    let S₁ := ∑ j ∈ oddIndicesNo3 r, 2 * r.choose j * X ^ (r - j) * Y ^ j
    let z := X ^ (r - 3) * Y ^ 3
    have hsum_scale :
        2 * S₀ = S₁ := by
      simp only [S₀, S₁]
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro j hj
      ring
    calc
      L.sum = (X - Y) ^ r + S₁ + ((splitCoeffs r).map (fun c => c * z)).sum := by
        rw [hL_sum_expand]
        simp only [S₁, z]
        congr 1
        exact congrArg List.sum (List.map_congr_left (l := splitCoeffs r) (by
          intro c hc
          ring))
      _ = (X - Y) ^ r + S₁ + 2 * r.choose 3 * z := by
        rw [split_j3 r hr z]
      _ = (X - Y) ^ r + 2 * (S₀ + r.choose 3 * z) := by
        rw [← hsum_scale]
        ring
      _ = (X + Y) ^ r := by
        rw [h_binom_odd_nat, hsum_odd]
        simp only [S₀, z]
        ring ;)
  have hL_coprime : ∀ p, Nat.Prime p → ∃ x ∈ L, ¬p ∣ x := by
    intro p hp
    by_cases hp_div_XY : p ∣ X - Y;
    · -- If p divides X - Y, then p cannot divide any other term in L.
      have hp_not_div_other : ∀ j ∈ oddIndicesNo3 r, ¬(p ∣ 2 * r.choose j * X ^ (r - j) * Y ^ j) := by
        intro j hj
        have hp_not_div_m : ¬(p ∣ m) := by
          intro hpm
          have hp_div_B : p ∣ B := by
            have hp_div_B : p ∣ B ^ r := by
              convert Nat.dvd_sub ( dvd_pow hpm ( by linarith : r ≠ 0 ) ) hp_div_XY using 1 ; rw [ Nat.sub_sub_self ( show B ^ r ≤ m ^ r from Nat.pow_le_pow_left hmgtB.le _ ) ]
            generalize_proofs at *; (
            exact hp.dvd_of_dvd_pow hp_div_B)
          generalize_proofs at *; (
          exact Nat.Prime.not_dvd_one hp ( hmB.gcd_eq_one ▸ Nat.dvd_gcd hpm hp_div_B ))
        have hp_not_div_B : ¬(p ∣ B) := by
          intro h; have := Nat.dvd_gcd ( show p ∣ m from ?_ ) h; simp_all +decide [ Nat.Coprime, Nat.Coprime.gcd_eq_one ] ;
          have hp_div_m : p ∣ m ^ r := by
            convert Nat.dvd_add hp_div_XY ( h.pow ( show r ≠ 0 by linarith ) ) using 1 ; rw [ Nat.sub_add_cancel ( show B ^ r ≤ m ^ r from Nat.pow_le_pow_left hmgtB.le _ ) ]
          generalize_proofs at *; (
          exact hp.dvd_of_dvd_pow hp_div_m)
        generalize_proofs at *; (
        simp_all +decide [ Nat.Prime.dvd_mul ];
        exact ⟨ ⟨ ⟨ fun h => hp_not_div_B <| hcoeffs j hj p <| dvd_mul_of_dvd_left h _, fun h => hp_not_div_B <| hcoeffs j hj p <| dvd_mul_of_dvd_right h _ ⟩, mt ( hp.dvd_of_dvd_pow ) <| mt ( hp.dvd_of_dvd_pow ) hp_not_div_m ⟩, mt ( hp.dvd_of_dvd_pow ) <| mt ( hp.dvd_of_dvd_pow ) hp_not_div_B ⟩)
      generalize_proofs at *; (
      have hp_not_div_other : ∃ j ∈ oddIndicesNo3 r, ¬(p ∣ 2 * r.choose j * X ^ (r - j) * Y ^ j) := by
        exact ⟨ 1, by exact Finset.mem_filter.mpr ⟨ Finset.mem_Icc.mpr ⟨ by linarith, by linarith ⟩, by decide, by decide ⟩, hp_not_div_other 1 <| by exact Finset.mem_filter.mpr ⟨ Finset.mem_Icc.mpr ⟨ by linarith, by linarith ⟩, by decide, by decide ⟩ ⟩
      generalize_proofs at *; (
      obtain ⟨ j, hj₁, hj₂ ⟩ := hp_not_div_other; use 2 * r.choose j * X ^ ( r - j ) * Y ^ j; simp_all +decide;
      exact List.mem_append_left _ ( List.mem_append_right _ ( List.mem_map.mpr ⟨ j, Finset.mem_sort ( α := ℕ ) ( · ≤ · ) |>.2 hj₁, rfl ⟩ ) ) ;));
    · exact ⟨ _, List.mem_append_left _ ( List.mem_append_left _ ( List.mem_append_left _ ( List.mem_singleton_self _ ) ) ), mt ( hp.dvd_of_dvd_pow ) hp_div_XY ⟩
  have hL_nodup : L.Nodup := by
    let firstTerm := (X - Y) ^ r
    let binomTerms : List ℕ :=
      ((oddIndicesNo3 r).sort (· ≤ ·)).map
        (fun j => 2 * r.choose j * X ^ (r - j) * Y ^ j)
    let splitTerms : List ℕ :=
      (splitCoeffs r).map (fun c => c * X ^ (r - 3) * Y ^ 3)
    have hm_not_dvd_B : ¬ m ∣ B := Nat.not_dvd_of_pos_of_lt hB hmgtB
    have hfactor_binom (j : ℕ) (hj : j ∈ oddIndicesNo3 r) :
        (2 * r.choose j * X ^ (r - j) * Y ^ j).factorization m = r * (r - j) := by
      have hcpos : 0 < 2 * r.choose j := by
        exact mul_pos two_pos
          (Nat.choose_pos (by linarith [Finset.mem_Icc.mp (Finset.mem_filter.mp hj).1]))
      have hclt : 2 * r.choose j < m := by
        exact lt_of_le_of_lt (Nat.le_of_dvd hB (hcoeffs j hj _ dvd_rfl)) hmgtB
      convert factorization_prime_scaled_term (q := m) (c := 2 * r.choose j) (B := B)
          (r := r) (a := r - j) (b := j) hmprime
          (Nat.ne_of_gt hcpos) (Nat.not_dvd_of_pos_of_lt hcpos hclt)
          (Nat.ne_of_gt hB) hm_not_dvd_B using 1
    have hfactor_split (c : ℕ) (hc : c ∈ splitCoeffs r) :
        (c * X ^ (r - 3) * Y ^ 3).factorization m = r * (r - 3) := by
      have hcpos : 0 < c := splitCoeffs_pos r hr c hc
      have hclt : c < m := by
        exact lt_of_le_of_lt (Nat.le_of_dvd hB (hsplit c hc _ dvd_rfl)) hmgtB
      convert factorization_prime_scaled_term (q := m) (c := c) (B := B)
          (r := r) (a := r - 3) (b := 3) hmprime
          (Nat.ne_of_gt hcpos) (Nat.not_dvd_of_pos_of_lt hcpos hclt)
          (Nat.ne_of_gt hB) hm_not_dvd_B using 1
    have hbinom_nodup : binomTerms.Nodup := by
      simp only [binomTerms]
      apply (Finset.sort_nodup (oddIndicesNo3 r) (· ≤ ·)).map_on
      intro j hj k hk heq
      have hjmem : j ∈ oddIndicesNo3 r := (Finset.mem_sort (α := ℕ) (· ≤ ·)).1 hj
      have hkmem : k ∈ oddIndicesNo3 r := (Finset.mem_sort (α := ℕ) (· ≤ ·)).1 hk
      have hfac := congrArg (fun n => n.factorization m) heq
      change (2 * r.choose j * X ^ (r - j) * Y ^ j).factorization m =
        (2 * r.choose k * X ^ (r - k) * Y ^ k).factorization m at hfac
      rw [hfactor_binom j hjmem, hfactor_binom k hkmem] at hfac
      have hjle : j ≤ r := (Finset.mem_Icc.mp (Finset.mem_filter.mp hjmem).1).2
      have hkle : k ≤ r := (Finset.mem_Icc.mp (Finset.mem_filter.mp hkmem).1).2
      have hsubeq : r - j = r - k := Nat.mul_left_cancel (by omega : 0 < r) hfac
      omega
    have hsplit_nodup : splitTerms.Nodup := by
      simp only [splitTerms]
      apply (splitCoeffs_nodup r hr).map_on
      intro c hc d hd heq
      have hzpos : 0 < X ^ (r - 3) * Y ^ 3 := by
        exact mul_pos (pow_pos (pow_pos hm _) _) (pow_pos (pow_pos hB _) _)
      have heq' : c * (X ^ (r - 3) * Y ^ 3) = d * (X ^ (r - 3) * Y ^ 3) := by
        simpa [mul_assoc] using heq
      exact Nat.mul_right_cancel hzpos heq'
    have hbinom_split_disjoint : binomTerms.Disjoint splitTerms := by
      intro x hx hy
      simp only [binomTerms, List.mem_map] at hx
      simp only [splitTerms, List.mem_map] at hy
      rcases hx with ⟨j, hj, rfl⟩
      rcases hy with ⟨c, hc, heq⟩
      have hjmem : j ∈ oddIndicesNo3 r := (Finset.mem_sort (α := ℕ) (· ≤ ·)).1 hj
      have hfac := congrArg (fun n => n.factorization m) heq.symm
      change (2 * r.choose j * X ^ (r - j) * Y ^ j).factorization m =
        (c * X ^ (r - 3) * Y ^ 3).factorization m at hfac
      rw [hfactor_binom j hjmem, hfactor_split c hc] at hfac
      have hjne : j ≠ 3 := (Finset.mem_filter.mp hjmem).2.2
      have hjle : j ≤ r := (Finset.mem_Icc.mp (Finset.mem_filter.mp hjmem).1).2
      have hsubeq : r - j = r - 3 := Nat.mul_left_cancel (by omega : 0 < r) hfac
      omega
    have hrest_nodup : (binomTerms ++ splitTerms).Nodup :=
      hbinom_nodup.append hsplit_nodup hbinom_split_disjoint
    have hYgt1 : 1 < Y := by
      exact lt_of_lt_of_le hBgt1 (by
        simp only [Y]
        exact Nat.le_self_pow (by omega : r ≠ 0) B)
    have hfirst_coprime_Y : Nat.Coprime firstTerm Y := by
      have hXY : Nat.Coprime X Y := by
        simp only [X, Y]
        simpa using hmB.pow r r
      have hle : Y ≤ X := by
        simp only [X, Y]
        exact Nat.pow_le_pow_left hmgtB.le r
      exact ((Nat.coprime_sub_self_left hle).2 hXY).pow_left r
    have hfirst_rest_disjoint : [firstTerm].Disjoint (binomTerms ++ splitTerms) := by
      intro x hx hy
      simp only [List.mem_singleton] at hx
      subst x
      have hYdvd : Y ∣ firstTerm := by
        rcases List.mem_append.mp hy with hbin | hsplit'
        · simp only [binomTerms, List.mem_map] at hbin
          rcases hbin with ⟨j, hj, hfirst_eq⟩
          rw [← hfirst_eq]
          have hjmem : j ∈ oddIndicesNo3 r := (Finset.mem_sort (α := ℕ) (· ≤ ·)).1 hj
          have hjpos : 0 < j := Odd.pos (Finset.mem_filter.mp hjmem).2.1
          exact dvd_mul_of_dvd_right (dvd_pow_self Y (Nat.ne_of_gt hjpos)) _
        · simp only [splitTerms, List.mem_map] at hsplit'
          rcases hsplit' with ⟨c, hc, hfirst_eq⟩
          rw [← hfirst_eq]
          exact dvd_mul_of_dvd_right (dvd_pow_self Y (by decide : 3 ≠ 0)) _
      have hYeq1 : Y = 1 := Nat.eq_one_of_dvd_coprimes hfirst_coprime_Y hYdvd dvd_rfl
      omega
    change ([firstTerm] ++ binomTerms ++ splitTerms).Nodup
    exact (List.nodup_singleton firstTerm).append hrest_nodup hfirst_rest_disjoint
  generalize_proofs at *; (
  have hL_length : L.length = r - 2 := by
    simp +zetaDelta at *; (
    rw [splitCoeffs_length r hr];
    convert count_summands r hr using 1 ; ring!)
  let f : Fin (r - 2) → ℕ := fun i => L.get ⟨i, by linarith [Fin.is_lt i]⟩
  refine' ⟨f, ?_, ?_, ?_, ?_, ?_⟩
  · intro i
    simp only [f]
    exact hL_pos _ (List.get_mem L ⟨i, by linarith [Fin.is_lt i]⟩)
  · intro i
    simp only [f]
    exact hL_powerful _ (List.get_mem L ⟨i, by linarith [Fin.is_lt i]⟩)
  · simp only [f]
    convert hL_sum using 1
    generalize_proofs at *
    refine' congr_arg _ (List.ext_get _ _) <;> simp +decide [hL_length]
  · intro p hp
    obtain ⟨x, hx₁, hx₂⟩ := hL_coprime p hp
    obtain ⟨i, hi⟩ := List.mem_iff_get.mp hx₁
    use ⟨i, by grind⟩
    aesop
  · intro i j hij
    simp only [f] at hij
    let ii : Fin L.length := ⟨i, by linarith [Fin.is_lt i]⟩
    let jj : Fin L.length := ⟨j, by linarith [Fin.is_lt j]⟩
    have hget : L.get ii = L.get jj := hij
    have hii : ii = jj := (List.Nodup.get_inj_iff hL_nodup).mp hget
    have hval : ii.val = jj.val := congrArg (fun x : Fin L.length => x.val) hii
    exact Fin.ext (by simpa [ii, jj] using hval))

/-! ## B exists for each r -/

/-- A suitable B value for each r: product of all relevant coefficients. -/
noncomputable def coeffB (r : ℕ) : ℕ :=
  (oddIndicesNo3 r).prod (fun j => 2 * r.choose j) * (splitCoeffs r).prod

lemma coeffB_pos (r : ℕ) (hr : 6 ≤ r) : 0 < coeffB r := by
  refine mul_pos (Finset.prod_pos fun j hj => ?_) ?_
  · exact mul_pos two_pos ( Nat.choose_pos ( by linarith [ Finset.mem_Icc.mp ( Finset.mem_filter.mp hj |>.1 ) ] ) )
  · exact Nat.pos_iff_ne_zero.mpr (List.prod_ne_zero (by
      intro hzero
      exact Nat.ne_of_gt (splitCoeffs_pos r hr 0 hzero) rfl))

lemma coeffB_coeffs (r : ℕ) :
    ∀ j ∈ oddIndicesNo3 r, ∀ p : ℕ, p ∣ (2 * r.choose j) → p ∣ coeffB r := by
  exact fun j hj p dp => dvd_trans dp ( dvd_mul_of_dvd_left ( Finset.dvd_prod_of_mem _ hj ) _ )

lemma coeffB_splitCoeffs (r : ℕ) :
    ∀ c ∈ splitCoeffs r, ∀ p : ℕ, p ∣ c → p ∣ coeffB r := by
  exact fun c hc p hp => dvd_trans hp (dvd_mul_of_dvd_right (List.dvd_prod hc) _)

/-! ## The main theorem -/

theorem infinite_rpowerful_sums (r : ℕ) (hr : 6 ≤ r) :
    Set.Infinite {N : ℕ | 0 < N ∧ IsPowerful r N ∧
      ∃ f : Fin (r - 2) → ℕ,
        (∀ i, 0 < f i) ∧
        (∀ i, IsPowerful r (f i)) ∧
        ∑ i, f i = N ∧
        (∀ p : ℕ, p.Prime → ∃ i, ¬(p ∣ f i)) ∧
        Function.Injective f} := by
  refine Set.infinite_iff_exists_gt.mpr ?_;
  intro M;
  -- Choose $B$ to be a multiple of all relevant coefficients.
  obtain ⟨B, hB⟩ : ∃ B : ℕ, 0 < B ∧ (∀ j ∈ oddIndicesNo3 r, ∀ p : ℕ, p ∣ (2 * r.choose j) → p ∣ B) ∧ (∀ c ∈ splitCoeffs r, ∀ p : ℕ, p ∣ c → p ∣ B) := by
    exact ⟨ coeffB r, coeffB_pos r hr, coeffB_coeffs r, coeffB_splitCoeffs r ⟩;
  have hBgt1 : 1 < B := by
    have hmem : 1 ∈ oddIndicesNo3 r := by
      exact Finset.mem_filter.mpr ⟨Finset.mem_Icc.mpr ⟨by omega, by omega⟩, by decide, by decide⟩
    have hcoef_gt1 : 1 < 2 * r.choose 1 := by
      rw [Nat.choose_one_right]
      omega
    exact lt_of_lt_of_le hcoef_gt1 (Nat.le_of_dvd hB.1 (hB.2.1 1 hmem _ dvd_rfl))
  obtain ⟨q, hqge, hqprime⟩ := Nat.exists_infinite_primes (max (B + 1) (M + 1))
  have hBltq : B < q := by
    have := le_trans (Nat.le_max_left (B + 1) (M + 1)) hqge
    omega
  have hMltq : M < q := by
    have := le_trans (Nat.le_max_right (B + 1) (M + 1)) hqge
    omega
  have hqcopB : Nat.Coprime q B := by
    exact (hqprime.coprime_iff_not_dvd).2 (Nat.not_dvd_of_pos_of_lt hB.1 hBltq)
  have hNgtM : M < (q ^ r + B ^ r) ^ r := by
    have hrne : r ≠ 0 := by omega
    have hq_le_qr : q ≤ q ^ r := Nat.le_self_pow hrne q
    have hqr_le_sum : q ^ r ≤ q ^ r + B ^ r := Nat.le_add_right _ _
    have hsum_le_pow : q ^ r + B ^ r ≤ (q ^ r + B ^ r) ^ r :=
      Nat.le_self_pow hrne (q ^ r + B ^ r)
    exact hMltq.trans_le (hq_le_qr.trans (hqr_le_sum.trans hsum_le_pow))
  refine' ⟨_, ⟨_, _, _⟩, hNgtM⟩
  · positivity
  · exact isPowerful_pow r _
  · exact rpowerful_decomposition r hr q B hqprime.pos hB.1 hqcopB hBltq hqprime hBgt1 hB.2.1 hB.2.2
