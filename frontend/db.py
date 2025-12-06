import sqlite3
from datetime import datetime

DB_FILE = "fakty.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS fakty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fakt TEXT NOT NULL,
            zrodlo TEXT,
            waga REAL,
            data TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def add_fakt(fakt, zrodlo, waga):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO fakty (fakt, zrodlo, waga, data) VALUES (?, ?, ?, ?)",
        (fakt, zrodlo, float(waga), datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()


def get_all_fakty():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, fakt, zrodlo, waga, data FROM fakty")
    rows = c.fetchall()
    conn.close()
    return rows


def update_waga(fakt_id, new_waga):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE fakty SET waga=? WHERE id=?", (float(new_waga), fakt_id))
    conn.commit()
    conn.close()


def delete_fakt(fakt_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM fakty WHERE id=?", (fakt_id,))
    conn.commit()
    conn.close()
