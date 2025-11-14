from flask import Flask, request, jsonify, render_template_string
import os
import sys
import tempfile
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from bank_parser import IndianBankStatementParser
except ImportError:
    # Fallback for deployment
    class IndianBankStatementParser:
        def parse_statement(self, pdf_path, password=None):
            return {
                'bank_name': 'Demo Bank',
                'total_transactions': 0,
                'transactions': [],
                'metadata': {'account_number': 'Demo', 'parsed_at': datetime.now().isoformat()}
            }

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🏦 Bank Statement Parser</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0; }
        .upload-area { border: 2px dashed #ccc; padding: 40px; text-align: center; border-radius: 10px; }
        .upload-area:hover { border-color: #007bff; }
        input[type="file"] { margin: 10px 0; }
        input[type="password"] { width: 200px; padding: 5px; margin: 10px 0; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { background: white; padding: 20px; border-radius: 10px; margin: 20px 0; }
        .transaction { border-bottom: 1px solid #eee; padding: 10px 0; }
        .error { color: red; background: #ffe6e6; padding: 10px; border-radius: 5px; }
        .success { color: green; background: #e6ffe6; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🏦 Bank Statement Parser</h1>
    <p>Upload your bank PDF statement to extract transactions. Supports SBI, Axis Bank, Yes Bank, Indian Overseas Bank, Bandhan Bank, HSBC, Union Bank, Indian Bank, Federal Bank, Jammu & Kashmir Bank, IDBI Bank, Bank of Baroda, HDFC Bank, Punjab National Bank, Central Bank of India, Karnataka Bank, Kotak Mahindra Bank, Canara Bank, and IndusInd Bank.</p>
    
    <div class="container">
        <form id="uploadForm" enctype="multipart/form-data">
            <div class="upload-area">
                <h3>📄 Upload PDF Statement</h3>
                <input type="file" name="pdf" accept=".pdf" required>
                <br>
                <input type="password" name="password" placeholder="PDF Password (if required)">
                <br>
                <button type="submit">Parse Statement</button>
            </div>
        </form>
    </div>
    
    <div id="result"></div>
    
    <script>
        document.getElementById('uploadForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const resultDiv = document.getElementById('result');
            
            resultDiv.innerHTML = '<div class="container">⏳ Processing PDF...</div>';
            
            try {
                const response = await fetch('/api/parse', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.error) {
                    resultDiv.innerHTML = `<div class="error">❌ Error: ${data.error}</div>`;
                } else {
                    let html = `
                        <div class="result">
                            <div class="success">✅ Successfully parsed ${data.total_transactions} transactions from ${data.bank_name} Bank</div>
                            <h3>📋 Statement Info</h3>
                            <p><strong>Bank:</strong> ${data.bank_name}</p>
                            <p><strong>Total Transactions:</strong> ${data.total_transactions}</p>
                            <p><strong>Account Number:</strong> ${data.metadata.account_number}</p>
                            
                            <h3>💳 Transactions</h3>
                    `;
                    
                    data.transactions.forEach(tx => {
                        html += `
                            <div class="transaction">
                                <strong>${tx.date}</strong> - ${tx.description}<br>
                                Debit: ₹${tx.debit.toFixed(2)} | Credit: ₹${tx.credit.toFixed(2)} | Balance: ₹${tx.balance.toFixed(2)}
                            </div>
                        `;
                    });
                    
                    html += `
                            <br>
                            <button onclick="downloadJSON()">📥 Download JSON</button>
                        </div>
                    `;
                    
                    resultDiv.innerHTML = html;
                    window.parsedData = data;
                }
            } catch (error) {
                resultDiv.innerHTML = `<div class="error">❌ Error: ${error.message}</div>`;
            }
        });
        
        function downloadJSON() {
            const dataStr = JSON.stringify(window.parsedData, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'parsed_statement.json';
            link.click();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/parse', methods=['POST'])
def parse_pdf():
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'No PDF file uploaded'}), 400
        
        pdf_file = request.files['pdf']
        password = request.form.get('password', '')
        
        if pdf_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            pdf_file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            parser = IndianBankStatementParser()
            
            # Auto-detect IDBI password from filename
            pdf_password = password if password else None
            if not pdf_password and 'IDBI_' in pdf_file.filename:
                pdf_password = pdf_file.filename.split('_')[-1].replace('.PDF', '').replace('.pdf', '')
            
            result = parser.parse_statement(temp_path, password=pdf_password)
            return jsonify(result)
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel handler
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == '__main__':
    app.run(debug=True)