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
| idem, second algorithme indépendant (search_r5_seg.py) | e <= 1e16 | 2 solutions, les mêmes : le résultat à 1e16 est confirmé par deux méthodes | calcul exact, deux exécutions indépendantes | results/r5_1e16_seg.txt |
| idem, second algorithme | **e <= 9e18** | **2 solutions, les deux déjà connues** (N = 72736 nombres 5-puissants, 172 segments, 2744 s sur 5 processus) | calcul exact, une seule exécution à cette borne | results/r5_9e18.txt |
| idem, troisième programme au-delà de 64 bits (search_r5_wide.py) | **e <= 1e20** | **2 solutions, les deux déjà connues** (N = 122594 nombres 5-puissants, 487 segments ; contrôles de couverture passés) | calcul exact, une seule exécution à cette borne ; recouvre et confirme le résultat à 9e18 | results/r5_1e20.txt |
| r = 4, a+b = c, pgcd(a,b) = 1 | c <= 1e14 | aucune solution (même avec a = 1) | calcul exact | results/r4_1e14.txt |
| idem | c <= 9e18 | **aucune solution, même avec a = 1** (N = 436945 nombres 4-puissants, 1570 s sur 8 processus) | calcul exact, confirmé (ligne suivante) | results/r4_9e18.txt |
| idem, second chemin de calcul (search_r4_alt.py) | c <= 9e18 | aucune solution : résultat confirmé | calcul exact, deux exécutions indépendantes | results/r4_9e18_alt.txt |
| r = 3 (contrôle) | c <= 1e10 | 1 solution (Nitaj) | calcul exact | results/r3_1e10.txt |

Portée : « exhaustif » veut dire que tous les nombres r-puissants <= borne sont énumérés (générateur comparé à la
factorisation naïve sur de petites bornes) et que toutes les sommes sont testées en entiers 64 bits exacts.
Le code n’a pas encore été relu par des pairs.

## Vérification des solutions connues (protocole H)
results/verification_known.txt : somme exacte, factorisations par division par essais, par sympy **et** par PARI/GP
(concordantes), primalité des facteurs prouvée par sympy et par PARI (isprime), pgcd global 1.

## O3 (infinité pour r = 5)
Rien de prouvé sur la question elle-même. Résultats négatifs partiels sur les identités polynomiales « à la Price » à quatre
termes : notes/o3_identities.md. Au plus un terme peut être un monôme (preuve à la main) ; le cas « un monôme et trois termes à une
racine » est exclu par un calcul exact (33963 bases de Gröbner) ; aucune identité sur 138 configurations de racines testées.
Restent ouverts dans ce cadre : un monôme avec au moins quatre facteurs non libres, et quatre termes non monomiaux.

Second mécanisme exploré (identités au-dessus d'une équation de Fermat généralisée, même note) : aucune identité à quatre termes
pour les signatures qui ont une infinité de solutions. Seul sous-produit : la famille restreinte (U+V)² = U² + 2UV + V², cherchée
exhaustivement pour U, V <= 4,5e18 (donc e jusqu'à environ 2·10^37) : **aucune solution** (results/r5_square_family_4.5e18.txt). notes/o3_r5.md : pourquoi l'identité de Price s'arrête à r = 6, une tentative de regroupement
(impasse), pistes non explorées.

## Suite du 18/11/2026 : S-unités (r = 4), support premier (r = 5), Lean

### r = 4 : aucune solution à petits premiers, sans borne de taille
`search/check_sunit_r4.py` filtre les listes **complètes** de von Känel et Matschke (arXiv:1605.06079, données sur
github.com/bmatschke/solving-classical-diophantine-equations) des a + b = c premiers entre eux :
- tous les premiers de abc <= 53 (1 663 449 triplets) : **aucun** triplet où a, b, c sont tous 4-puissants (a = 1 admis) ;
- rad(abc) <= 10^7 (432 408 triplets) : **aucun** non plus.
Aucun triplet 3-puissant dans ces listes (celui de Nitaj contient 73, 271, 919) ; 562 et 1068 triplets 2-puissants (contrôle).
Sortie : `results/r4_sunit.txt`. Le nombre de triplets lus est comparé à l'en-tête de chaque fichier.
C'est une méthode sans rapport avec `rpow.py` ni avec les recherches par taille. Le plus grand c de la liste « premiers <= 53 »
vaut 7 058 844 079 092 540 383 < 9e18 : cette liste est donc aussi un contrôle indépendant de `r4_9e18.txt` sur ces supports.
Réserve : la complétude des listes repose sur l'article et le code de leurs auteurs ; je ne l'ai pas revérifiée.

### r = 5 : la recherche « par support » ne dépasse pas vraiment 1e20
`search_r5_wide.py` accepte un ensemble de premiers (4e argument) ; `test_support.py` : Kitamura est retrouvée avec
{2,3,7,13,17}, Cambie avec {2,3,5,11,13,23,61}, rien avec un ensemble plus petit.
Mais les nombres 5-puissants à petits premiers sont trop denses pour une rencontre au milieu à grande taille : avec les
8 plus petits premiers il y en a 1,4 million sous 1e30 et 10 millions sous 1e37 (2,9 et 28 millions avec 12 premiers), soit
1e12 à 1e15 paires. L'hypothèse du plan (« bien au-delà de 1e20 ») ne tient pas avec cet algorithme.
Fait : premiers <= 37, e <= 1e22 : seule la solution de Kitamura (152 136 nombres, 757 segments, 2 103 s sur 4 processus ; une exécution) (`results/r5_primes37_1e22.txt`).
Aller plus loin demande un autre algorithme (réduction de réseaux sur les exposants, comme pour les S-unités à 3 termes).

### Lean
Les quatre énoncés résolus de formal-conjectures (`infinite_of_six_le`, `finite`, `seven`, `eight`) sont prouvés dans un repo
séparé `erdos939-lean` (formalisation d'Aristotle portée en Lean v4.33.1, plus un pont vers `Erdos939Sums`). Non poussé.

### Seconde exécution r = 5 jusqu'à 1e20 et second générateur (19/11/2026)
`search/rpow2.py` : second générateur écrit à part (premiers par division, construction premier par premier, racine par
dichotomie). Mêmes listes que `rpow.py` pour r = 5 à 1e20 et 9e18, r = 4 à 9e18, r = 3 à 1e10, et les deux concordent avec la
définition sur de petites bornes (`results/generators_agree.txt`).
`search/run_gen2.py 5 1e20` : la recherche complète refaite avec ce générateur : **les 2 mêmes solutions**
(`results/r5_1e20_gen2.txt`, 1 408 s sur 4 processus). L'algorithme de recherche est le même que pour `r5_1e20.txt`.

### r = 5 jusqu'à 1e21 (19/11/2026)
`search_r5_wide.py 5 1e21 4` : recherche complète, N = 201 284 nombres 5-puissants, 1 313 segments, 4 664 s :
**toujours les 2 seules solutions** (Kitamura, Cambie), donc aucune autre avec e ≤ 10^21 (`results/r5_1e21.txt`).
Une seule exécution, un seul générateur (`rpow.py`) à cette borne.

### Piste C (abc@home)
Non faite : le serveur de Leiden (pub.math.leidenuniv.nl) répondait 503.

## Non fait
- Recentrage des objectifs sur r = 5 : pas encore validé par Joaquim.
