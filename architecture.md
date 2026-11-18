# Architecture — Analyse Amazon

## Flux

```
generate.py → CSV (avis)
     │
     ▼
extract.py → transform.py (note, positif, nettoyage)
     │
     ▼
  load.py → amazon.db
     │
     ├── Indicateurs
     └── visualize.py → charts/*.png
```

## Table `avis`

- date, produit_id, produit, categorie
- note (1–5), recommande (0/1)
- prix_paye, utile_votes, positif
