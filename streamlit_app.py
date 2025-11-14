import streamlit as st
import os
import json
from datetime import datetime

st.title("🏦 Bank Statement Parser")
st.write("Upload your PDF bank statement to extract transactions")

uploaded_file = st.file_uploader("Choose PDF file", type="pdf")
password = st.text_input("PDF Password (if required)", type="password")

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")
    st.write(f"File: {uploaded_file.name}")
    
    # Basic demo response
    st.subheader("📊 Demo Results")
    st.write("Bank: Demo Bank")
    st.write("Transactions: 5")
    
    # Demo table
    import pandas as pd
    demo_data = {
        'Date': ['2024-01-01', '2024-01-02'],
        'Description': ['Sample Transaction 1', 'Sample Transaction 2'],
        'Debit': [0, 500],
        'Credit': [1000, 0],
        'Balance': [1000, 500]
    }
    df = pd.DataFrame(demo_data)
    st.dataframe(df)

st.markdown("📞 Contact: +91 8777654651")