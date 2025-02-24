import sqlite3
from models.offer import Offer

DB_FILE = "offers.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            link TEXT NOT NULL,
            source TEXT NOT NULL
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM offers")
    if cursor.fetchone()[0] == 0:
        initial_offers = [
            ("Часы", 3000, "url3", "Manual"),
            ("Телефон", 10000, "url2", "Manual"),
            ("Кроссовки", 5000, "url1", "Manual"),
            ("Планшет", 4000, "url4", "Manual")
        ]
        cursor.executemany("INSERT INTO offers (name, price, link, source) VALUES (?, ?, ?, ?)", initial_offers)
    conn.commit()
    conn.close()

def load_offers():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, link, source FROM offers")  # Добавляем id в запрос
    offers = [Offer(row[1], row[2], row[3], row[4], id=row[0]) for row in cursor.fetchall()]
    conn.close()
    return offers

def save_offer(offer):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO offers (name, price, link, source) VALUES (?, ?, ?, ?)",
                   (offer.name, offer.price, offer.link, offer.source))
    conn.commit()
    conn.close()

def delete_offer(offer_id):
    """Удаляет предложение из базы по id."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM offers WHERE id = ?", (offer_id,))
    conn.commit()
    conn.close()

init_db()