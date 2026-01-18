import sqlite3

conn = sqlite3.connect("trust.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS ledger (
    id INTEGER PRIMARY KEY,
    item TEXT,
    customer TEXT,
    total INTEGER,
    paid INTEGER,
    debt INTEGER
)
""")

conn.commit()
