# Erdős #939 — recherche de sommes de nombres r-puissants

Problème : pour r >= 4, la somme de r − 2 nombres r-puissants premiers entre eux (pgcd global 1) peut-elle
être r-puissante ? État et résultats : `REPORT.md`. Journal : `LOG.md`. Notes : `notes/`.

## Contenu
- `search/rpow.py` : énumération exacte des nombres r-puissants <= X.
- `search/search_r5.py` : a + b + c = e, exhaustif, pgcd(a, b, c) = 1, sans hypothèse sur les pgcd deux à deux.
- `search/search_r4.py` : a + b = c, exhaustif, pgcd(a, b) = 1.
- `search/test_search.py` : générateur et recherche comparés à la force brute.
- `search/verify.py` : vérification indépendante d'une solution (somme, factorisations, pgcd).
- `results/` : sorties brutes des calculs. `notes/raw/` : copies des pages web lues.

## Rejouer
Python 3.9+ avec `numpy` (et `sympy` pour le contrôle croisé de `verify.py`). Bornes X < 2^63.
```bash
cd search
python3 test_search.py
python3 search_r5.py 5 1e14     # ~1 min
python3 search_r5.py 5 1e16     # ~3 Go de RAM
python3 search_r4.py 4 9e18
python3 verify.py
```
