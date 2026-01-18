import streamlit as st
import requests

st.title("📊 Market Trust AI")

text = st.text_input("Say or type your transaction")

if st.button("Record"):
    r = requests.post(
        "http://127.0.0.1:8000/record",
        params={"text": text}
    )
    st.success(r.json()["message"])

if st.button("Check Trust Score"):
    r = requests.get("http://127.0.0.1:8000/score")
    st.metric("Trust Score", r.json()["trust_score"])
