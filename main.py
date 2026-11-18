"""Pipeline d'analyse des recommandations produits (style Amazon)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from generate import generer_avis
from extract import extraire
from transform import transformer
from load import initialiser_base, charger
from visualize import generer_graphiques


CSV_PATH = Path(__file__).parent / "data" / "avis_bruts.csv"
DB_PATH = Path(__file__).parent / "data" / "amazon.db"
CHARTS_DIR = Path(__file__).parent / "charts"


def afficher_indicateurs(conn):
    print("\n=== Indicateurs recommandations ===")

    row = conn.execute("""
        SELECT ROUND(AVG(note), 2),
               ROUND(100.0 * SUM(recommande) / COUNT(*), 1),
               COUNT(*)
        FROM avis
    """).fetchone()
    print(f"Note moyenne globale : {row[0]} / 5")
    print(f"Taux de recommandation : {row[1]} %")
    print(f"Nombre d'avis : {row[2]}")

    print("\nTop produits (note moyenne) :")
    for r in conn.execute("""
        SELECT produit, ROUND(AVG(note), 2) AS moy, COUNT(*) AS n
        FROM avis
        GROUP BY produit
        ORDER BY moy DESC
        LIMIT 5
    """):
        print(f"  {r[0]:30} note {r[1]} ({r[2]} avis)")

    print("\nTaux de recommandation par catégorie :")
    for r in conn.execute("""
        SELECT categorie,
               ROUND(100.0 * SUM(recommande) / COUNT(*), 1) AS taux
        FROM avis
        GROUP BY categorie
        ORDER BY taux DESC
    """):
        print(f"  {r[0]:15} {r[1]} %")


def main():
    print("=== Analyse recommandations produits Amazon ===\n")

    generer_avis(600, CSV_PATH)

    brut = extraire(CSV_PATH)
    print(f"Avis extraits : {len(brut)}")

    propres = transformer(brut)
    print(f"Après nettoyage : {len(propres)}")

    conn = initialiser_base(DB_PATH)
    nb = charger(conn, propres)
    print(f"Chargés dans {DB_PATH} : {nb}")

    afficher_indicateurs(conn)

    print("\n=== Visualisation ===")
    charts = generer_graphiques(conn, CHARTS_DIR)
    if charts:
        print(f"{len(charts)} graphiques générés dans {CHARTS_DIR}/")

    conn.close()
    print("\nPipeline terminé.")


if __name__ == "__main__":
    main()
