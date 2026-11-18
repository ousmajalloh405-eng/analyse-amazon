"""Visualisation des recommandations produits (matplotlib)."""

from pathlib import Path
import sqlite3


def generer_graphiques(conn: sqlite3.Connection, output_dir: Path) -> list:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib non installé. Exécutez: pip install matplotlib")
        return []

    output_dir.mkdir(parents=True, exist_ok=True)
    fichiers = []

    rows = conn.execute("""
        SELECT produit, ROUND(AVG(note), 2) AS moy, COUNT(*) AS n
        FROM avis
        GROUP BY produit
        ORDER BY moy DESC
    """).fetchall()
    if rows:
        labels = [r[0][:22] for r in rows]
        notes = [r[1] for r in rows]
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.barh(labels, notes, color="#ff9900", edgecolor="white")
        ax.set_xlim(0, 5.2)
        ax.set_title("Note moyenne par produit", fontsize=14, fontweight="bold")
        ax.set_xlabel("Note moyenne (1–5)")
        for bar, n in zip(bars, notes):
            ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                    f"{n}", va="center", fontsize=9)
        fig.tight_layout()
        path = output_dir / "note_moyenne_produit.png"
        fig.savefig(path, dpi=120)
        plt.close(fig)
        fichiers.append(path)
        print(f"  Graphique : {path.name}")

    rows = conn.execute("""
        SELECT categorie,
               ROUND(100.0 * SUM(recommande) / COUNT(*), 1) AS taux
        FROM avis
        GROUP BY categorie
        ORDER BY taux DESC
    """).fetchall()
    if rows:
        cats = [r[0] for r in rows]
        taux = [r[1] for r in rows]
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(cats, taux, color="#146eb4", edgecolor="white")
        ax.set_title("Taux de recommandation par catégorie (%)", fontsize=14, fontweight="bold")
        ax.set_ylabel("% d'avis qui recommandent")
        ax.set_ylim(0, 100)
        ax.tick_params(axis="x", rotation=20)
        for bar, t in zip(bars, taux):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                    f"{t}%", ha="center", fontsize=9)
        fig.tight_layout()
        path = output_dir / "taux_recommandation_categorie.png"
        fig.savefig(path, dpi=120)
        plt.close(fig)
        fichiers.append(path)
        print(f"  Graphique : {path.name}")

    rows = conn.execute("""
        SELECT note, COUNT(*) FROM avis GROUP BY note ORDER BY note
    """).fetchall()
    if rows:
        notes = [r[0] for r in rows]
        counts = [r[1] for r in rows]
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(notes, counts, color="#232f3e", edgecolor="white")
        ax.set_title("Distribution des notes", fontsize=14, fontweight="bold")
        ax.set_xlabel("Note")
        ax.set_ylabel("Nombre d'avis")
        ax.set_xticks(notes)
        fig.tight_layout()
        path = output_dir / "distribution_notes.png"
        fig.savefig(path, dpi=120)
        plt.close(fig)
        fichiers.append(path)
        print(f"  Graphique : {path.name}")

    return fichiers
