# O3, r = 5 : existe-t-il une identité « à la Price » à quatre termes ?

Statut : **résultats négatifs partiels.** Ce qui suit n'exclut PAS une infinité de solutions pour r = 5 ; cela
exclut seulement certaines façons d'en fabriquer une famille polynomiale. Rien ici n'a été relu par un humain.

## Cadre
La famille de Price (r >= 6) vient d'une relation linéaire entre des termes de la forme
c · X^a · Y^b · ∏ G(X, Y)^e, avec G ∈ {X + Y, X − Y} et tous les e >= r. En posant X = x^r, Y = y^r, chaque
monôme X^a Y^b est une puissance r-ième, chaque G^e est r-puissant puisque e >= r, et les nombres premiers de c
sont absorbés en les faisant diviser x ou y. Pour r = 5 il faut une telle relation à **quatre** termes.

En t = X/Y, on cherche donc T1 + T2 + T3 + T4 = 0 avec
T_i = c_i · t^(a_i) · ∏_ρ (t − ρ)^(e_iρ), où chaque e_iρ vaut 0 ou est >= 5 (ρ ≠ 0 : « racine non libre »),
sans racine commune aux quatre termes (0 et l'infini compris) et sans sous-somme nulle.
Notations : s = nombre de termes qui sont de purs monômes ; K = nombre total de couples (terme, racine non libre).
θ désigne l'opérateur t·d/dt ; (θ − m) annule t^m et abaisse de 1 au plus la multiplicité de chaque racine non nulle.

## Lemme A (classique)
Un polynôme à s monômes non nuls n'a pas de racine non nulle de multiplicité >= s.
(Récurrence sur s : diviser par le monôme de plus bas degré puis dériver.)

## Proposition 1 : s >= 2 est impossible (preuve à la main, tous degrés)
- s = 4 : quatre monômes sans sous-somme nulle ont tous le même exposant, donc une racine commune (0 ou l'infini).
- s = 3 : un terme non monomial serait combinaison de trois monômes, avec une racine non nulle de multiplicité
  >= 5 : contredit le lemme A.
- s = 2 : T1 + T2 = −(α t^m + β t^n), avec m ≠ n (si m = n, on est ramené à s = 3 pour un seul monôme : même argument avec (θ − m)). Une racine commune à T1 et T2 serait racine de multiplicité >= 5 du binôme :
  exclu par le lemme A. Les ensembles de racines A de T1 et B de T2 sont donc disjoints. Appliquer
  (θ − m)(θ − n) : on obtient W1 + W2 = 0 avec W_i = t^(a_i) ∏ (t − ρ)^(e_iρ − 2) · Q_i, deg Q_1 <= 2|A|,
  deg Q_2 <= 2|B|, et W_i ≠ 0 (sinon T_i serait un binôme, lemme A). Chaque racine de A, de multiplicité >= 3
  dans W1, doit diviser Q_2 : 3|A| <= 2|B|. De même 3|B| <= 2|A|. Donc |A| = |B| = 0 : contradiction.

Conséquence : dans toute identité de ce type, au plus un des quatre termes est un monôme. En particulier
l'identité de Price ((X+Y)^5 − (X−Y)^5 = trois monômes) ne peut pas être « réparée » en gardant deux monômes.

## Proposition 2 : s = 1 et K = 3 est impossible (preuve assistée par ordinateur, exacte)
Forme : c1 t^(a1) (t − 1)^(e1) + c2 t^(a2) (t − ρ)^(e2) + c3 t^(a3) (t − σ)^(e3) = α t^m.
- Les trois racines sont distinctes. Une racine commune aux trois termes annulerait α t^m. Si T1 et T2 seulement partageaient ρ,
  alors (θ − m)T3 = t^(a3)(t − σ)^(e3 − 1)·(degré <= 1), qui est non nul (T3 n'est pas un monôme), s'annulerait en ρ à l'ordre >= 4.
- min a_i = 0 : sans racine commune, min(a_1, a_2, a_3, m) = 0 ; si tous les a_i étaient > 0 on aurait m = 0 et α = 0 en évaluant en t = 0.
- Borne de degré : (θ − m) donne U1 + U2 + U3 = 0 avec U_i = c_i t^(a_i) (t − ρ_i)^(e_i − 1) Q_i, deg Q_i <= 1.
  Le pgcd g des U_i est de degré <= 2 : il vaut 1, t, (t − ρ_i), t(t − ρ_i) ou (t − τ) pour une racine τ commune aux trois Q_i
  (deux ρ dans g annuleraient un Q_k ; et t | g force m = 0, donc la racine des Q_i concernés est 0, ce qui exclut τ),
  et U1U2U3/g³ a au plus 7 racines distinctes. Mason–Stothers donne deg(U_i/g) <= 6, donc a_i + e_i <= 9.
- Calcul (`search/identities_k3.py`) : pour chaque motif (a_i, e_i) avec a_i + e_i <= 10, chaque position de la
  racine 1 et chaque m, base de Gröbner sur Q des mineurs 3×3, saturée par ρσ(ρ−1)(σ−1)(ρ−σ). Base = {1} signifie
  aucune solution complexe (un sous-ensemble de mineurs suffit pour exclure : moins d'équations, plus de solutions).
  Ce résultat repose sur `sympy.groebner` seul, sans second système de calcul formel. Résultat : **33963 systèmes, tous exclus** (base {1}), aucun cas dégénéré
  (`results/identities_k3_part0.txt`, `results/identities_k3_part1.txt`).

## Recherches numériques sur des ensembles de racines fixés (s et K quelconques)
`search/identities.py` énumère tous les termes de degré <= d pour un ensemble fini de facteurs (racines
rationnelles ou facteurs quadratiques irréductibles) et liste toutes les relations minimales à quatre termes sans
racine commune ; les candidats sont trouvés par projection aléatoire modulo p (aucune relation n'est manquée),
puis confirmés exactement. L'outil retrouve bien (t+1)^3 − (t−1)^3 = 6t^2 + 2 quand on abaisse le seuil à 3.
Pour r = 5 (seuil 5), sur le lot de `search/identities_batch.sh` (degrés 10 à 14) : 138 configurations (2 à 4 racines parmi ±1, ±2, ±3, ±4, 5, ±1/2, ±1/3, ±3/2, ±2/3, et les facteurs t²+1, t²±t+1, t²±2, t²±3, t²−t−1), **aucune relation**.
Sortie brute : `results/identities_r5.txt`. `search/identities_k2.py` recoupe par un calcul indépendant le cas
s = 2, K = 2 jusqu'au degré 16 (déjà couvert par la proposition 1) : 0 solution sur 15294 motifs.

## Ce qui reste ouvert dans ce cadre
- s = 1 avec K >= 4 (par exemple un terme portant deux racines non libres).
- s = 0 (quatre termes non monomiaux, K >= 4), qui contient l'équation de type Fermat P^5 + Q^5 + R^5 = S^5 en
  polynômes. La borne de type Mason pour quatre termes n'exclut rien ici : elle ne devient contraignante que pour
  des exposants > 12.
- Les racines non rationnelles en dehors des facteurs quadratiques testés.
- Et surtout : une famille infinie pourrait venir d'un tout autre mécanisme (courbes de genre 0 ou 1, F.3.4 du
  dossier). Ce cadre ne le voit pas.

## Second mécanisme exploré : identités au-dessus d'une équation de Fermat généralisée
Idée : remplacer les variables libres X = x^5, Y = y^5 par un triplet X + Y = Z où X = A·x^p, Y = B·y^q,
Z = C·z^s parcourt les solutions d'une équation de Fermat généralisée qui en a une infinité
(1/p + 1/q + 1/s > 1, par exemple x² + y³ = z⁵). Un monôme X^a Y^b Z^c est alors 5-puissant dès que chaque
exposant est nul ou au moins égal au seuil ⌈5/p⌉, ⌈5/q⌉, ⌈5/s⌉. Il suffirait d'une relation linéaire entre
quatre tels monômes de même degré.

`search/identities_gfermat.py` liste toutes ces relations (minimales, sans facteur commun). Résultat jusqu'au
degré 13 : **aucune** pour les seuils (3,2,1), (3,2,2), (3,3,1), (3,3,2), (2,2,2), (2,2,1), (3,1,1), c'est-à-dire
pour toutes les signatures sphériques ou euclidiennes. Le théorème de Brownawell–Masser borne le degré par 3(|S| − 2) = 3
pour S = {0, −1, ∞}, donc le degré 13 couvre tout ce cadre avec marge (borne citée, non redémontrée ici).
La seule relation trouvée est pour les seuils (2,1,1) : X² + 2YZ = Y² + Z² avec X = Z − Y, soit
(U + V)² = U² + 2UV + V². Elle correspond à une signature hyperbolique : elle ne donne pas de famille infinie
connue, mais une **famille restreinte** de solutions de r = 5 :

> si U, V > 0, pgcd(U, V) = 1, V impair 5-puissant, U = 2^k·m avec k >= 4 et m impair 5-puissant, et W = U + V
> 3-puissant, alors U² + 2UV + V² = W² est une solution (pgcd global 1).

`search/search_square_family.py` cherche toutes ces paires avec V > 1 jusqu'à une borne B sur U et V ; la recherche est donc
exhaustive pour e <= B², très au-delà de la borne exhaustive générale. Le cas V = 1 (terme c = 1) est contrôlé à part : aucun U. Résultat : pour B = 4,5e18 (14343 valeurs de V, 56111 de U, 9380370 nombres 3-puissants <= 2B),
**aucune paire** (`results/r5_square_family_4.5e18.txt`). Il n'y a donc aucune solution de cette forme avec e <= 2·10^37 environ.
Heuristique : environ B^(2/5) paires, probabilité B^(−2/3) que W soit 3-puissant, soit B^(−4/15) par échelle :
un nombre fini de solutions attendu, cohérent avec la conjecture abc (qualité 15/11 > 1).

Variante cubique écartée : (X+Y)³ = (X−Y)³ + 6X²Y + 2Y³ demande X 3-puissant, Y 5-puissant (à cause du terme
6X²Y) et X ± Y tous deux 2-puissants : environ B^(−7/15) par échelle, encore plus rare. Non cherchée.

Leçon : dans toutes ces constructions, le terme croisé force les variables à être 5-puissantes, et la
condition restante est de type abc. Aucune ne donne de famille infinie.

## Cas s = 0, K = 4 : fermé (20/11/2026, preuve assistée par ordinateur)
Quatre termes portant chacun exactement une racine non libre : T_i = λ_i t^(a_i) (t − ρ_i)^(e_i), de degré homogène d,
b_i = d − a_i − e_i, e_i >= 5, 0 et l'infini libres.
- **Borne de degré (wronskien).** Trois des termes sont toujours linéairement indépendants : une relation à trois termes
  forcerait, par Mason–Stothers, les trois à partager leur racine non libre, et le quatrième serait alors dans leur
  span de dimension 2, ce qui donne une relation à trois termes interdite. W = W(T_i, T_j, T_k) est le même, au signe près, pour tout
  choix de trois termes, de degré homogène 3d − 6, et en chaque point P on peut choisir les trois termes pour exclure un terme
  qui ne s'annule pas en P : ord_P W >= Σ_i max(0, μ_iP − 2). En sommant, et puisque Σ_i (a_i + e_i + b_i) = 4d :
  **d <= 2 + Σ min(a_i, 2) + Σ min(b_i, 2) <= 14.** (La même borne vaut pour s = 1, K = 4.)
- **Calcul** (`search/identities_k4.py`, Singular via passagemath) : pour chaque motif (a_i, e_i) admis par la borne et
  chaque façon dont les termes partagent leurs racines (les 14 partitions des quatre termes en au moins deux blocs), idéal des
  d + 1 équations en (ρ_2, ρ_3, ρ_4, λ_2, λ_3, λ_4), ρ_1 = 1, saturé par les racines non nulles, deux à deux distinctes,
  et λ_2 λ_3 λ_4. 881 468 systèmes (`results/k4/`). Calibrage : avec le seuil 2 au lieu de 5, le programme trouve bien des relations.
- **Résultat.** 44 systèmes non exclus. 43 sont triviaux : deux termes identiques (même motif, même racine) qui
  s'annulent (λ_2 = −1, λ_3 = −λ_4), donc une sous-somme nulle. Le dernier est une vraie identité, en degré 6 :

      5√5 · Y [(X + Y)^5 + (X − Y)^5] = X [(X + √5 Y)^5 − (X − √5 Y)^5]   (les deux valent 10√5 (X^5 Y + 10 X^3 Y^3 + 5 X Y^5))

  Elle n'est pas définie sur Q, et aucun changement de variable (même sur Q(√5), en échangeant les rôles des racines
  libres) ne la rend rationnelle : les quatre racines non libres 1, −1, √5, −√5 ont un birapport irrationnel, alors que
  des racines rationnelles auraient un birapport rationnel, et le birapport est invariant par homographie.
- **Conséquence : aucune identité de Price à quatre termes avec s = 0 et K = 4 n'existe sur Q pour r = 5.**

## Cas s = 1, K = 4 : fermé (20/11/2026, preuve assistée par ordinateur)
Un monôme, un terme à deux racines non libres et deux termes à une racine (seule répartition possible de K = 4 sur trois
termes non monomiaux). Trois des termes sont indépendants (une relation à trois termes demanderait, par Mason–Stothers,
que les trois partagent toutes leurs racines non libres, impossible ici), donc la même borne du wronskien vaut :
d <= 2 + Σ min(a_i, 2) + Σ min(b_i, 2) <= 14, et d >= 10 puisque le terme à deux racines a un degré >= 10.
`search/identities_k4s1.py` : tous les motifs admis, toutes les coïncidences de racines entre termes, saturation comme
ci-dessus. **1 128 014 systèmes, aucun non exclu** (`results/k4s1/`). Calibrage : au seuil 2, le même code trouve une
famille de solutions de dimension 1 (degré 4).
**Conséquence : aucune identité de Price à quatre termes avec K <= 4 n'existe pour r = 5, même sur C, à part l'identité
en √5 ci-dessus (s = 0), qui n'est pas rationnelle.** Avec les propositions 1 et 2, tous les cas K <= 4 sont traités.
Reste ouvert : K >= 5 (la borne devient d <= 2K − 6 + Σ min(a_i, 2) + Σ min(b_i, 2)), et les mécanismes hors de ce cadre.
