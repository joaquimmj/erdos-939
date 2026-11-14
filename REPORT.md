# REPORT — Erdős #939 (14/11/2026)

Rien n'est publié ni soumis. Aucun résultat nouveau sur la question ouverte : ce rapport ne contient que des
vérifications et des recherches exhaustives bornées.

## État du problème (Phase 0, détail dans notes/phase0.md)
- « coprime » = pgcd global 1 (échange Kitamura–Cambie du fil ; docstring Lean).
- Question 2 (infinité) : réglée pour tout r >= 6 (construction de Price / GPT-5.5 Pro, 24/05/2026).
  **r = 5 : ouvert**, deux solutions connues. **r = 4 : aucun exemple connu.**
- Lean (`formal-conjectures`, 939.lean) : énoncé corrigé en septembre 2026 ; restent des `sorry`.
- Les commentaires d'erdosproblems.com sont suspendus.
- conjectures.io (lu le 14/11 au soir, copie dans notes/raw/) : une « preuve » Lean approuvée le 06/08/2026 puis
  retirée, car l'énoncé formel d'alors omettait la positivité (r = 4 satisfait par {0, 1}). Cohérent avec la
  correction de septembre ; rien de nouveau sur le problème lui-même.

## Recherches exhaustives (search/, testées contre la force brute)
| Recherche | Borne | Résultat | Niveau de certitude | Fichier |
|---|---|---|---|---|
| r = 5, a+b+c = e, pgcd(a,b,c) = 1, sans hypothèse deux à deux | e <= 1e14 | 2 solutions (Kitamura, Cambie) | calcul exact, rejoué en local | results/r5_1e14.txt |
| idem | e <= 1e16 | **2 solutions, les deux déjà connues** (N = 16266 nombres 5-puissants, 124315057 sommes de paires, 1513 s) | calcul exact, une seule exécution | results/r5_1e16.txt |
| r = 4, a+b = c, pgcd(a,b) = 1 | c <= 1e14 | aucune solution (même avec a = 1) | calcul exact | results/r4_1e14.txt |
| idem | c <= 9e18 | **aucune solution, même avec a = 1** (N = 436945 nombres 4-puissants, 1570 s sur 8 processus) | calcul exact, une seule exécution | results/r4_9e18.txt |
| r = 3 (contrôle) | c <= 1e10 | 1 solution (Nitaj) | calcul exact | results/r3_1e10.txt |

Portée : « exhaustif » veut dire que tous les nombres r-puissants <= borne sont énumérés (générateur comparé à la
factorisation naïve sur de petites bornes) et que toutes les sommes sont testées en entiers 64 bits exacts.
Le code n'a été relu par personne d'autre que des IA.

## Vérification des solutions connues (protocole H)
results/verification_known.txt : somme exacte, factorisations par division par essais, par sympy **et** par PARI/GP
(concordantes), primalité des facteurs prouvée par sympy et par PARI (isprime), pgcd global 1.

## O3 (infinité pour r = 5)
Rien de prouvé. notes/o3_r5.md : pourquoi l'identité de Price s'arrête à r = 6, une tentative de regroupement
(impasse), pistes non explorées.

## Non fait
- Recentrage des objectifs sur r = 5 : pas encore validé par Joaquim.
- `sorry` Lean (`infinite_of_six_le`, `seven`, `eight`) : non abordés.
- Aucune seconde exécution indépendante des recherches à 1e16 et 9e18.
