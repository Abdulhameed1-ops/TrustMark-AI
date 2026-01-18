import sqlite3

def get_db():
    conn = sqlite3.connect("ledger.db", check_same_thread=False)
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        customer TEXT,
        item TEXT,
        total INTEGER,
        paid INTEGER,
        debt INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
