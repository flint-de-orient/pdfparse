from flask import Flask, request, jsonify, render_template_string
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h1>🏦 Bank Statement Parser</h1>
    <p>Upload your PDF bank statement to extract transactions.</p>
    <form action="/parse" method="post" enctype="multipart/form-data">
        <input type="file" name="pdf" accept=".pdf" required><br><br>
        <input type="password" name="password" placeholder="PDF Password (optional)"><br><br>
        <button type="submit">Parse Statement</button>
    </form>
    '''

@app.route('/parse', methods=['POST'])
def parse():
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'No PDF uploaded'}), 400
        
        pdf_file = request.files['pdf']
        if pdf_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Basic response for now
        return jsonify({
            'status': 'success',
            'message': f'Received PDF: {pdf_file.filename}',
            'bank_name': 'Demo Bank',
            'total_transactions': 5,
            'transactions': [
                {'date': '2024-01-01', 'description': 'Sample Transaction', 'debit': 0, 'credit': 1000, 'balance': 1000}
            ]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)