# Erdős #939 — Phase 0, vérification en direct (14/11/2026)

Sources lues en entier : erdosproblems.com/939 et son fil (9 commentaires), /940, /941, /364 ;
`FormalConjectures/ErdosProblems/939.lean` et son historique git. Copies brutes dans `notes/raw/`.
Non lu : conjectures.io (hôte bloqué depuis la session).

## Page (dernière modification : 28 mai 2026), statut « open »
- Question 3 : résolue (Nitaj [Ni95] ; Cohn [Co98] ; Walsh [Wa24] = arXiv:2404.03970, courbes elliptiques).
- Exemples : Cambie pour r = 5 (3^7·61^5 = 2^8·3^10·5^7 + 2^12·23^6 + 11^5·13^5), r = 7, r = 8 (5 termes) ;
  Kitamura pour r = 5 (commentaire).
- « GPT-5.5 Pro (prompted by Price) has given a simple construction in the comments that shows for r >= 6
  there are infinitely many r-powerful numbers which are the sum of (r-2) (in fact ⌈r/2⌉+1) many coprime
  r-powerful numbers. »
- **« The ability to post new comments has been suspended. »** Aucun commentaire ne peut être déposé.

## Fil
- Kitamura, 25/05/2026 : 2^5·17^6 + 7^11 + 2^5·3^6·7^8 = 3^7·13^7, soit
  772402208 + 1977326743 + 134481277728 = 137231006679. « the three summands have joint gcd 1. They are not
  pairwise coprime ». Il demande confirmation de l'interprétation de « coprime ».
- Cambie, 26/05/2026 : « Correct. » Puis : pour r = 4, recherche exhaustive, aucune solution avec
  max(a,b) <= 10^14. Pour r = 5 : si d < 10^16, la solution est l'une des deux connues, **ou bien**
  gcd(a,b), gcd(b,c), gcd(a,c) > 1 avec gcd(a,b,c) = 1 (cas non couvert par sa recherche).
  « For r=5, I even do not dare to guess if there is a finite or infinite number of solutions. »
- Price, 24/05/2026 : construction pour r >= 6 via (X+Y)^r = (X−Y)^r + Σ_{j impair} 2·C(r,j)·X^{r−j}·Y^j,
  X = q^r, Y = B^r ; formalisée en Lean par Aristotle (lien dans le fil).
- Alfaiz / Cambie / Dogmachine, 13/10/2025 : Walsh ; la conjecture n (abc à plusieurs termes) ne suffit pas,
  à première vue, pour la finitude (référence [HKS25]).

## Conclusions
1. **Interprétation : pgcd global = 1**, confirmée par l'échange Kitamura–Cambie et par le Lean
   (« their greatest common divisor is 1 »). Conforme à A.2 du dossier.
2. L'exemple à 137231006679 du dossier est bien celui de Kitamura.
3. Question 2 : réglée (infinité) pour tout r >= 6 ; **ouverte pour r = 5** ; r = 4 sans exemple.
4. Petits exemples r = 6 du dossier : absents du fil, mais sans enjeu depuis la famille infinie.
5. Lean : positivité corrigée (commit 23e0351, 09/09/2026), finitude reformulée et r >= 6 ajouté
   (8fff9a7, 11/09/2026). Restent des `sorry` : `infinite_of_six_le`, `seven`, `eight`.
6. Problèmes liés : #940 (sommes d'au plus r nombres r-puissants, densité), #941 (résolu, Heath-Brown),
   #364 (trois puissants consécutifs), #1107 (r+1 termes). Rien de directement réutilisable pour r = 5.

## Objectifs après Phase 0
- O1 : réduit à r = 5 (recherche réellement exhaustive, sans hypothèse sur les pgcd deux à deux).
- O2 : retiré (déjà corrigé). Variante possible : prouver les `sorry`.
- O3 : seul cas ouvert avec exemples : r = 5.
- O4, O5 : inchangés ; Cambie a déjà 10^14 pour r = 4.
