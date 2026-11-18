# Analyse des recommandations produits Amazon

> Pipeline ETL d’analyse d’avis clients (notes, recommandations, catégories) + visualisation.

**Statut** : 🟢 Réalisé  
**Catégorie** : ⚙️ Création de pipelines ETL  
**Portfolio** : [Profil GitHub](https://github.com/ousmajalloh405-eng)

---

## 1. Problème métier

Comprendre quels produits sont les mieux notés, quelles catégories sont le plus recommandées, et la distribution des notes clients (style avis Amazon).

## 2. Architecture

```
generate.py → avis_bruts.csv
      │
      ▼
 extract.py → transform.py → load.py → amazon.db
                                      │
                                      ├── Indicateurs (console)
                                      └── visualize.py → charts/*.png
```

## 3. Technologies

- Python 3
- Bibliothèque standard (`csv`, `sqlite3`)
- SQLite
- matplotlib (graphiques)

## 4. Installation et exécution

```bash
git clone https://github.com/ousmajalloh405-eng/analyse-amazon.git
cd analyse-amazon
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

Graphiques générés dans `charts/` :
- `note_moyenne_produit.png`
- `taux_recommandation_categorie.png`
- `distribution_notes.png`

## 5. Indicateurs

- Note moyenne globale et par produit
- Taux de recommandation global et par catégorie
- Distribution des notes (1 à 5)

## 6. Compétences pour le CV

Pipeline ETL Python d’analyse d’avis produits (notes, recommandations), stockage SQLite et visualisation matplotlib.

---

*Projet réalisé dans le cadre de la formation Data — Sonatel Academy.*
