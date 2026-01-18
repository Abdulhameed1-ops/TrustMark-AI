import sqlite3

def calculate_score(user):
    conn = sqlite3.connect("ledger.db")
    c = conn.cursor()

    c.execute("SELECT total, paid FROM transactions WHERE user=?", (user,))
    rows = c.fetchall()
    conn.close()

    if not rows:
        return 0

    total = sum(r[0] for r in rows)
    paid = sum(r[1] for r in rows)
    tx_count = len(rows)
    payment_ratio = paid / total if total else 0

    score = (
        payment_ratio * 40 +
        min(tx_count / 50, 1) * 20 +
        payment_ratio * 25 +
        15
    )
    return round(score, 2)
