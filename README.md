# Erdős #939 — sommes de nombres r-puissants

Problème (erdosproblems.com/939) : pour r >= 4, la somme de r − 2 nombres r-puissants premiers entre eux
(pgcd global 1) peut-elle être r-puissante ? Y a-t-il une infinité de telles sommes ?

**Le problème reste ouvert pour r = 4 et r = 5 ; ce dépôt ne le résout pas.** Il contient des recherches
exhaustives bornées, la vérification des solutions connues et des résultats négatifs partiels sur les familles
polynomiales. Rien n'est publié. Travail préparé avec l'aide d'une IA (Claude), pas encore relu par un humain.

## Où lire quoi
- `REPORT.md` : résultats et niveau de certitude de chacun. `LOG.md` : journal.
- `notes/phase0.md` : état du problème (page, fil de discussion, formalisation Lean), pages brutes dans `notes/raw/`.
- `notes/o3_r5.md` : pourquoi la construction de Price s'arrête à r = 6.
- `notes/o3_identities.md` : recherche d'une identité à quatre termes pour r = 5 (résultats négatifs partiels).

## Code (`search/`)
| Fichier | Rôle |
|---|---|
| `rpow.py` | énumération exacte des nombres r-puissants <= X |
| `search_r5.py` | a + b + c = e, exhaustif, pgcd(a, b, c) = 1, par table des sommes de paires |
| `search_r5_seg.py` | même énoncé, second algorithme indépendant (segments de valeurs, mémoire bornée, parallèle) |
| `search_r5_wide.py` | même énoncé au-delà de 64 bits (clé + bits bas), utilisé jusqu'à 1e20 |
| `search_square_family.py`, `identities_gfermat.py` | famille restreinte (U+V)² et identités au-dessus d'une équation de Fermat généralisée |
| `search_r4.py` | a + b = c, exhaustif, pgcd(a, b) = 1, parallèle |
| `test_search.py`, `test_search_r4.py`, `test_search_seg.py` | comparaison à la force brute et des deux algorithmes entre eux |
| `verify.py` | vérification indépendante d'une solution (somme, factorisations par trois méthodes, pgcd) |
| `identities.py`, `identities_k2.py`, `identities_k3.py`, `identities_batch.sh` | recherche d'identités polynomiales à quatre termes |

## Rejouer
Python 3.9+ avec `numpy` et `sympy` ; PARI/GP (`gp`) en option pour `verify.py`. Bornes X < 2^63.
```bash
cd search
python3 test_search.py && python3 test_search_r4.py && python3 test_search_seg.py
python3 search_r5_seg.py 5 1e16     # ~5 min, ~2 Go de RAM
python3 search_r5_seg.py 5 9e18     # ~1 h sur 5 processus, ~5 Go de RAM
python3 search_r5_wide.py 5 1e20 6  # ~2 h 40 sur 6 processus (machine éveillée), ~8 Go de RAM
python3 search_r4.py 4 9e18         # ~30 min sur 8 processus
python3 verify.py
python3 identities.py 12 5 1 -1     # identités de degré <= 12, seuil 5, racines 1 et -1
```
Les sorties brutes sont dans `results/`.
