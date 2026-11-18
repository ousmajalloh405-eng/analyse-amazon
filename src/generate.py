"""Génération de données fictives type avis / recommandations Amazon."""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

PRODUITS = [
    (1, "Écouteurs Bluetooth", "Électronique"),
    (2, "Livre Python pour débutants", "Livres"),
    (3, "Gourde inox 1L", "Maison"),
    (4, "T-shirt coton bio", "Mode"),
    (5, "Lampe de bureau LED", "Maison"),
    (6, "Clavier mécanique", "Électronique"),
    (7, "Crème solaire SPF50", "Beauté"),
    (8, "Sac à dos voyage", "Mode"),
]

NOTES = [1, 2, 3, 4, 5]


def generer_avis(n: int = 600, fichier: Path = Path("data/avis_bruts.csv")) -> None:
    fichier.parent.mkdir(parents=True, exist_ok=True)
    debut = datetime(2026, 1, 1)
    with open(fichier, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "date", "produit_id", "produit", "categorie",
            "note", "recommande", "prix_paye", "utile_votes"
        ])
        for _ in range(n):
            pid, nom, cat = random.choice(PRODUITS)
            date = debut + timedelta(days=random.randint(0, 300))
            note = random.choices(NOTES, weights=[5, 8, 12, 35, 40])[0]
            recommande = 1 if note >= 4 else (1 if random.random() < 0.2 else 0)
            prix = round(random.uniform(15, 250), 2)
            utile = random.randint(0, 50)
            writer.writerow([
                date.strftime("%Y-%m-%d"),
                pid, nom, cat, note, recommande, prix, utile,
            ])
    print(f"{n} avis générés dans {fichier}")
