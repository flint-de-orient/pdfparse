import streamlit as st
import os
import json
from datetime import datetime
from src.bank_parser import IndianBankStatementParser
from src.tally_export import generate_tally_xml
from src.models import Transaction

# Page config
st.set_page_config(
    page_title="Bank Statement Parser",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.upload-section {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 2rem;
    border-radius: 15px;
    border: 2px dashed #667eea;
    margin: 1rem 0;
}
.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    border-left: 4px solid #667eea;
}
.success-box {
    background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin: 1rem 0;
}
.bank-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 10px;
    margin: 1rem 0;
}
.bank-item {
    background: linear-gradient(45deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
    padding: 0.5rem;
    border-radius: 8px;
    text-align: center;
    font-size: 0.9rem;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🏦 Smart Bank Statement Parser</h1>
    <p>AI-Powered Transaction Extraction for Indian Banks</p>
</div>
""", unsafe_allow_html=True)

# Supported banks in sidebar
with st.sidebar:
    st.markdown("### 🏛️ Supported Banks")
    banks = [
        "State Bank of India", "Axis Bank", "Yes Bank", "Indian Overseas Bank",
        "Bandhan Bank", "HSBC", "Union Bank", "Indian Bank", "Federal Bank",
        "Jammu & Kashmir Bank", "IDBI Bank", "Bank of Baroda", "HDFC Bank",
        "Punjab National Bank", "Central Bank of India", "Karnataka Bank",
        "Kotak Mahindra Bank", "Canara Bank", "IndusInd Bank"
    ]
    
    for bank in banks:
        st.markdown(f"✅ {bank}")
    
    st.markdown("---")
    st.markdown("### 🚀 Features")
    st.markdown("• PDF Password Support")
    st.markdown("• Auto Bank Detection")
    st.markdown("• JSON Export")
    st.markdown("• Tally XML Export")
    st.markdown("• Transaction Summary")

# Upload section
st.markdown("""
<div class="upload-section">
    <h3 style="text-align: center; color: #667eea;">📄 Upload Your Bank Statement</h3>
    <p style="text-align: center;">Drag and drop your PDF file or click to browse</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    uploaded_file = st.file_uploader(
        "Choose PDF file", 
        type="pdf",
        help="Select your bank statement PDF file"
    )
with col2:
    password = st.text_input(
        "🔐 PDF Password", 
        type="password", 
        help="Leave blank if not password-protected",
        placeholder="Enter password if required"
    )

if uploaded_file is not None:
    # Save uploaded file temporarily
    temp_path = "temp_statement.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())
    
    try:
        with st.spinner("Parsing statement..."):
            parser = IndianBankStatementParser()
            
            # Show debug info
            with st.expander("🔍 Debug Information", expanded=False):
                st.write("Processing PDF...")
            
            # Auto-detect IDBI password from filename
            pdf_password = password if password else None
            if not pdf_password and 'IDBI_' in uploaded_file.name:
                pdf_password = uploaded_file.name.split('_')[-1].replace('.PDF', '').replace('.pdf', '')
            
            result = parser.parse_statement(temp_path, password=pdf_password)
        
        # Display results
        st.markdown(f"""
        <div class="success-box">
            <h3>✅ Parsing Complete!</h3>
            <p>Successfully extracted <strong>{result['total_transactions']}</strong> transactions from <strong>{result['bank_name']} Bank</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show metadata with colorful cards
        st.markdown("### 📊 Statement Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>🏦 Bank</h4>
                <h3 style="color: #667eea;">{}</h3>
            </div>
            """.format(result['bank_name']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>📊 Transactions</h4>
                <h3 style="color: #28a745;">{}</h3>
            </div>
            """.format(result['total_transactions']), unsafe_allow_html=True)
        
        with col3:
            account_num = result['metadata'].get('account_number', 'N/A')
            st.markdown("""
            <div class="metric-card">
                <h4>🔢 Account</h4>
                <h3 style="color: #fd7e14;">{}</h3>
            </div>
            """.format(account_num), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h4>📅 Parsed</h4>
                <h3 style="color: #6f42c1;">Today</h3>
            </div>
            """, unsafe_allow_html=True)
        
        # Show transactions in table format
        st.subheader("💳 Transactions")
        if result['transactions']:
            import pandas as pd
            
            # Convert to DataFrame for table display
            df_data = []
            for tx in result['transactions']:
                # Extract reference number if it exists in description
                desc_parts = tx['description'].split(' | Ref: ')
                description = desc_parts[0]
                reference = desc_parts[1] if len(desc_parts) > 1 else '-'
                
                df_data.append({
                    'Date': tx['date'],
                    'Description': description,
                    'Reference': reference,
                    'Debit (₹)': f"{tx['debit']:,.2f}" if tx['debit'] > 0 else "-",
                    'Credit (₹)': f"{tx['credit']:,.2f}" if tx['credit'] > 0 else "-",
                    'Balance (₹)': f"{tx['balance']:,.2f}"
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # Summary statistics with gradient cards
            st.markdown("### 💰 Financial Summary")
            col1, col2, col3 = st.columns(3)
            
            total_debits = sum(tx['debit'] for tx in result['transactions'])
            total_credits = sum(tx['credit'] for tx in result['transactions'])
            net_change = total_credits - total_debits
            
            with col1:
                st.markdown("""
                <div style="background: linear-gradient(45deg, #ff6b6b, #ee5a52); padding: 1.5rem; border-radius: 15px; color: white; text-align: center;">
                    <h4>💸 Total Debits</h4>
                    <h2>₹{:,.2f}</h2>
                </div>
                """.format(total_debits), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background: linear-gradient(45deg, #51cf66, #40c057); padding: 1.5rem; border-radius: 15px; color: white; text-align: center;">
                    <h4>💰 Total Credits</h4>
                    <h2>₹{:,.2f}</h2>
                </div>
                """.format(total_credits), unsafe_allow_html=True)
            
            with col3:
                color = "#51cf66" if net_change >= 0 else "#ff6b6b"
                st.markdown("""
                <div style="background: linear-gradient(45deg, {}, {}); padding: 1.5rem; border-radius: 15px; color: white; text-align: center;">
                    <h4>📈 Net Change</h4>
                    <h2>₹{:,.2f}</h2>
                </div>
                """.format(color, color, net_change), unsafe_allow_html=True)
            
            # Opening and Closing Balance with modern cards
            st.markdown("### 🏦 Account Balance")
            col1, col2 = st.columns(2)
            
            if result['transactions']:
                opening_balance = result['transactions'][0]['balance'] - result['transactions'][0]['credit'] + result['transactions'][0]['debit']
                closing_balance = result['transactions'][-1]['balance']
                
                with col1:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white; text-align: center;">
                        <h4>🏁 Opening Balance</h4>
                        <h2>₹{:,.2f}</h2>
                    </div>
                    """.format(opening_balance), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 15px; color: white; text-align: center;">
                        <h4>🎯 Closing Balance</h4>
                        <h2>₹{:,.2f}</h2>
                    </div>
                    """.format(closing_balance), unsafe_allow_html=True)
        else:
            st.warning("No transactions found. Please check if the PDF format is supported.")
        
        # Download section with modern styling
        st.markdown("""
        <div style="background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); padding: 1rem; border-radius: 10px; margin: 2rem 0;">
            <h3 style="color: white; text-align: center;">📥 Export Your Data</h3>
        </div>
        """)
        col1, col2 = st.columns(2)
        
        with col1:
            json_str = json.dumps(result, indent=2)
            st.download_button(
                label="📄 Download JSON",
                data=json_str,
                file_name=f"parsed_{uploaded_file.name}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            # Tally XML Export
            with st.expander("📤 Export to Tally XML"):
                bank_ledger_name = st.text_input(
                    "Bank Ledger Name (as in Tally)",
                    help="Enter the exact ledger name as saved in Tally",
                    key=f"ledger_{uploaded_file.name}"
                )
                
                # Pre-populate dates with first and last transaction dates
                # Try all date formats from different banks
                def parse_date(date_str):
                    formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%d %b %Y', '%d-%b-%Y', '%d/%b/%Y', '%B%d%Y', '%B%d,%Y', '%B%d, %Y']
                    for fmt in formats:
                        try:
                            return datetime.strptime(date_str, fmt).date()
                        except ValueError:
                            continue
                    raise ValueError(f"Unable to parse date: {date_str}")
                
                if not result['transactions']:
                    st.warning("No transactions available for Tally export")
                else:
                    first_date = parse_date(result['transactions'][0]['date'])
                    last_date = parse_date(result['transactions'][-1]['date'])
                    
                    # Ensure from_date is earlier than to_date
                    min_date = min(first_date, last_date)
                    max_date = max(first_date, last_date)
                    
                    col_date1, col_date2 = st.columns(2)
                    with col_date1:
                        from_date = st.date_input("From Date", value=min_date)
                    with col_date2:
                        to_date = st.date_input("To Date", value=max_date)
                    
                    if bank_ledger_name:
                        # Filter transactions by date range
                        filtered_txns = []
                        for tx in result['transactions']:
                            # Convert transaction date string to date object for comparison
                            tx_date = parse_date(tx['date'])
                            if from_date <= tx_date <= to_date:
                                filtered_txns.append(Transaction(
                                    date=tx_date,
                                    description=tx['description'],
                                    debit=tx['debit'],
                                    credit=tx['credit'],
                                    balance=tx['balance'],
                                    bank_name=tx['bank_name']
                                ))
                        
                        if filtered_txns:
                            xml_content = generate_tally_xml(filtered_txns, bank_ledger_name)
                            st.download_button(
                                label=f"📊 Download Tally XML ({len(filtered_txns)} transactions)",
                                data=xml_content,
                                file_name=f"tally_{bank_ledger_name}_{from_date}_{to_date}.xml",
                                mime="application/xml",
                                use_container_width=True
                            )
                        else:
                            st.warning("No transactions found in selected date range")
                    else:
                        st.info("Enter Bank Ledger Name to enable Tally XML export")
        
    except Exception as e:
        st.error(f"❌ Error parsing statement: {str(e)}")
        import traceback
        with st.expander("🐛 Error Details"):
            st.code(traceback.format_exc())
    
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)