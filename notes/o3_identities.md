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
- s = 3 : un terme non monomial serait combinaison de trois monômes, avec une racine non nulle de multiplicité
  >= 5 : contredit le lemme A.
- s = 2 : T1 + T2 = −(α t^m + β t^n). Une racine commune à T1 et T2 serait racine de multiplicité >= 5 du binôme :
  exclu par le lemme A. Les ensembles de racines A de T1 et B de T2 sont donc disjoints. Appliquer
  (θ − m)(θ − n) : on obtient W1 + W2 = 0 avec W_i = t^(a_i) ∏ (t − ρ)^(e_iρ − 2) · Q_i, deg Q_1 <= 2|A|,
  deg Q_2 <= 2|B|, et W_i ≠ 0 (sinon T_i serait un binôme, lemme A). Chaque racine de A, de multiplicité >= 3
  dans W1, doit diviser Q_2 : 3|A| <= 2|B|. De même 3|B| <= 2|A|. Donc |A| = |B| = 0 : contradiction.

Conséquence : dans toute identité de ce type, au plus un des quatre termes est un monôme. En particulier
l'identité de Price ((X+Y)^5 − (X−Y)^5 = trois monômes) ne peut pas être « réparée » en gardant deux monômes.

## Proposition 2 : s = 1 et K = 3 est impossible (preuve assistée par ordinateur, exacte)
Forme : c1 t^(a1) (t − 1)^(e1) + c2 t^(a2) (t − ρ)^(e2) + c3 t^(a3) (t − σ)^(e3) = α t^m.
- Les trois racines sont distinctes : si T1 et T2 partageaient ρ, alors (θ − m)T3 = t^(a3)(t − σ)^(e3 − 1)·(degré <= 1)
  s'annulerait en ρ à l'ordre >= 4.
- min a_i = 0 (sinon α = 0).
- Borne de degré : (θ − m) donne U1 + U2 + U3 = 0 avec U_i = c_i t^(a_i) (t − ρ_i)^(e_i − 1) Q_i, deg Q_i <= 1.
  Le pgcd g des U_i est de degré <= 2 (au plus le facteur t et un ρ_i, car deux ρ dans g annuleraient un Q_k),
  et U1U2U3/g³ a au plus 7 racines distinctes. Mason–Stothers donne deg(U_i/g) <= 6, donc a_i + e_i <= 9.
- Calcul (`search/identities_k3.py`) : pour chaque motif (a_i, e_i) avec a_i + e_i <= 10, chaque position de la
  racine 1 et chaque m, base de Gröbner sur Q des mineurs 3×3, saturée par ρσ(ρ−1)(σ−1)(ρ−σ). Base = {1} signifie
  aucune solution complexe. Résultat : **33963 systèmes, tous exclus** (base {1}), aucun cas dégénéré
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
