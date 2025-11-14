# src/bandhan_parser.py
import re
import pdfplumber
from .models import Transaction
from datetime import datetime

class BandhanTransactionParser:
    def parse_transactions(self, pdf_path, password=None):
        all_transactions = []
        
        with pdfplumber.open(pdf_path, password=password) as pdf:
            print(f"Processing {len(pdf.pages)} pages for Bandhan Bank")
            
            for page_num, page in enumerate(pdf.pages):
                print(f"Processing page {page_num + 1}")
                tables = page.extract_tables()
                
                for table in tables:
                    if table and self._is_transaction_table(table):
                        transactions = self._extract_transactions_from_table(table)
                        all_transactions.extend(transactions)
                        print(f"Extracted {len(transactions)} transactions from page {page_num + 1}")
        
        print(f"Total Bandhan Bank transactions extracted: {len(all_transactions)}")
        return all_transactions
    
    def _is_transaction_table(self, table):
        if not table or len(table) < 1:
            return False
        
        first_row = table[0]
        if not first_row or len(first_row) < 6:
            return False
        
        # Check if first row is header
        clean_headers = [str(cell).strip().lower() if cell else '' for cell in first_row]
        key_headers = ['transaction date', 'value date', 'description', 'amount', 'dr / cr', 'balance']
        header_matches = sum(1 for key in key_headers if any(key in cell for cell in clean_headers))
        
        if header_matches >= 4:
            return True
        
        # Check if first row is transaction data (continuation page)
        date_str = str(first_row[0]).strip()
        if re.search(r'[A-Za-z]+\d{1,2},\s*\d{4}', date_str):
            return True
        
        return False
    
    def _extract_transactions_from_table(self, table):
        transactions = []
        
        # Check if first row is header or data
        first_row = table[0]
        clean_first = [str(cell).strip().lower() if cell else '' for cell in first_row]
        is_header = any('transaction date' in cell or 'value date' in cell for cell in clean_first)
        
        start_idx = 1 if is_header else 0
        
        for row in table[start_idx:]:
            if not row or not any(row):
                continue
            
            transaction = self._parse_table_row(row)
            if transaction:
                transactions.append(transaction)
        
        return transactions
    
    def _parse_table_row(self, row):
        try:
            while len(row) < 6:
                row.append('')
            
            cells = [str(cell).strip() if cell else '' for cell in row]
            
            transaction_date = cells[0].replace('\n', ' ')
            value_date = cells[1].replace('\n', ' ')
            description = cells[2].replace('\n', ' ')
            amount_str = cells[3].replace('\n', '')
            dr_cr = cells[4].replace('\n', '')
            balance_str = cells[5].replace('\n', '')
            
            # Parse date (format: "June30, 2025")
            date_match = re.search(r'([A-Za-z]+)(\d{1,2}),\s*(\d{4})', transaction_date)
            if not date_match:
                return None
            
            date = self._parse_date(date_match.group(0))
            if not date:
                return None
            
            amount = self._parse_amount(amount_str)
            balance = self._parse_amount(balance_str)
            
            if balance is None:
                return None
            
            # Determine debit/credit
            debit = amount if dr_cr.strip().upper() == 'DR' else 0
            credit = amount if dr_cr.strip().upper() == 'CR' else 0
            
            return Transaction(
                date=date,
                description=description,
                debit=debit if debit else 0,
                credit=credit if credit else 0,
                balance=balance,
                bank_name='BANDHAN'
            )
            
        except Exception as e:
            return None
    
    def _parse_date(self, date_str):
        try:
            # Parse "June30, 2025" format
            dt = datetime.strptime(date_str, '%B%d, %Y')
            return dt.strftime('%Y-%m-%d')
        except:
            return None
    
    def _parse_amount(self, amount_str):
        if not amount_str or str(amount_str).strip() in ['', '-']:
            return 0.0
        
        try:
            # Extract amount using regex (INR followed by digits, commas, and decimal)
            match = re.search(r'INR([\d,]*\.?\d+)', str(amount_str))
            if match:
                clean_str = match.group(1).replace(',', '')
                return float(clean_str)
            return 0.0
        except:
            return 0.0
