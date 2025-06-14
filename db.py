import sqlite3
from datetime import datetime

DB_NAME = 'responses.db'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS modeles_reponse (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categorie TEXT NOT NULL,
            titre_modele TEXT NOT NULL,
            texte_reponse TEXT NOT NULL,
            lien_documentation TEXT,
            date_creation TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def ajouter_modele(categorie, titre, texte, lien=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO modeles_reponse (categorie, titre_modele, texte_reponse, lien_documentation, date_creation)
        VALUES (?, ?, ?, ?, ?)
        """,
        (categorie, titre, texte, lien, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
