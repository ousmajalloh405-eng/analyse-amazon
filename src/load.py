"""Chargement des avis dans SQLite."""

import sqlite3
from pathlib import Path
from typing import List, Dict


def initialiser_base(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS avis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            produit_id INTEGER,
            produit TEXT,
            categorie TEXT,
            note INTEGER,
            recommande INTEGER,
            prix_paye REAL,
            utile_votes INTEGER,
            positif INTEGER
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_produit ON avis(produit_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_categorie ON avis(categorie)")
    conn.commit()
    return conn


def charger(conn: sqlite3.Connection, data: List[Dict]) -> int:
    conn.execute("DELETE FROM avis")
    for a in data:
        conn.execute(
            """INSERT INTO avis
               (date, produit_id, produit, categorie, note, recommande,
                prix_paye, utile_votes, positif)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                a["date"], a["produit_id"], a["produit"], a["categorie"],
                a["note"], a["recommande"], a["prix_paye"],
                a["utile_votes"], a["positif"],
            ),
        )
    conn.commit()
    return len(data)
