import streamlit as st

st.title("🏦 Bank Statement Parser")

uploaded_file = st.file_uploader("Choose PDF file", type="pdf")

if uploaded_file:
    st.write("File uploaded!")
    
st.write("📞 Contact: +91 8777654651")