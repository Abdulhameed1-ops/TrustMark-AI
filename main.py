from fastapi import FastAPI
from ai import extract_data
from db import cur, conn

app = FastAPI()

@app.post("/record")
def record(text: str):
    data = extract_data(text)

    cur.execute("""
    INSERT INTO ledger (item, customer, total, paid, debt)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data["item"],
        data["customer"],
        data["total"],
        data["paid"],
        data["debt"]
    ))

    conn.commit()

    return {
        "message": f"Recorded. {data['customer']} owes {data['debt']}"
    }

@app.get("/score")
def score():
    cur.execute("SELECT COUNT(*), SUM(debt) FROM ledger")
    count, debt = cur.fetchone()

    trust = max(0, 100 - (debt or 0) // 1000)
    return {"trust_score": trust}
