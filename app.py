import streamlit as st
from ai import extract_transaction
import sqlite3
from score import calculate_score
from db import init_db

# Initialize DB
init_db()

st.title("📊 Market Trust AI (Web App Version)")

# Input
user = st.text_input("Enter your name:")
text = st.text_area("Type or speak your transaction here")

if st.button("Record Transaction"):
    if not user or not text:
        st.error("Please enter your name and transaction text")
    else:
        try:
            tx = extract_transaction(text)

            # Save to DB
            conn = sqlite3.connect("ledger.db")
            c = conn.cursor()
            c.execute("""
            INSERT INTO transactions (user, customer, item, total, paid, debt)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user,
                tx["customer"],
                tx["item"],
                tx["total"],
                tx["paid"],
                tx["debt"]
            ))
            conn.commit()
            conn.close()

            st.success(f"Recorded ✅ {tx['customer']} owes {tx['debt']} Naira")

            # Show trust score
            trust = calculate_score(user)
            st.metric("Trust Score", trust)

        except Exception as e:
            st.error(f"Error: {e}")

# View ledger (optional)
if st.checkbox("Show my transactions"):
    conn = sqlite3.connect("ledger.db")
    c = conn.cursor()
    c.execute("SELECT customer, item, total, paid, debt, created_at FROM transactions WHERE user=?", (user,))
    rows = c.fetchall()
    conn.close()

    if rows:
        st.table(rows)
    else:
        st.info("No transactions yet")
