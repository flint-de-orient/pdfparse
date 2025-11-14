import streamlit as st
import pandas as pd

st.title("🏦 Bank Statement Parser")
st.write("Upload your PDF bank statement to extract transactions")

uploaded_file = st.file_uploader("Choose PDF file", type="pdf")
password = st.text_input("PDF Password (if required)", type="password")

if uploaded_file is not None:
    try:
        st.success("PDF uploaded successfully!")
        st.write(f"File: {uploaded_file.name}")
        
        # Demo response without file processing
        st.subheader("📊 Demo Results")
        st.write("Bank: Demo Bank")
        st.write("Transactions: 5")
        
        # Demo table
        demo_data = {
            'Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'Description': ['Sample Transaction 1', 'Sample Transaction 2', 'Sample Transaction 3'],
            'Debit': [0, 500, 0],
            'Credit': [1000, 0, 200],
            'Balance': [1000, 500, 700]
        }
        df = pd.DataFrame(demo_data)
        st.dataframe(df)
        
        # Download button
        st.download_button(
            label="Download JSON",
            data='{"demo": "data"}',
            file_name="demo.json",
            mime="application/json"
        )
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.markdown("📞 Contact: +91 8777654651")