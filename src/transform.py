"""Transformation et enrichissement des avis produits."""

from typing import List, Dict


def transformer(lignes: List[Dict]) -> List[Dict]:
    propres = []
    for ligne in lignes:
        try:
            note = int(ligne["note"])
            if note < 1 or note > 5:
                continue
            recommande = int(ligne["recommande"])
            prix = float(ligne["prix_paye"])
            utile = int(ligne["utile_votes"])
            if prix <= 0:
                continue
            propres.append({
                "date": ligne["date"].strip(),
                "produit_id": int(ligne["produit_id"]),
                "produit": ligne["produit"].strip(),
                "categorie": ligne["categorie"].strip(),
                "note": note,
                "recommande": recommande,
                "prix_paye": round(prix, 2),
                "utile_votes": max(0, utile),
                "positif": 1 if note >= 4 else 0,
            })
        except (ValueError, KeyError):
            continue
    return propres
