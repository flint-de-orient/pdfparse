# src/axis_parser.py
import re
import pdfplumber
from .models import Transaction

class AxisTransactionParser:
    def __init__(self):
        self.expected_headers = [
            'S.No', 'Transaction Date', 'Value Date', 'Particulars', 
            'Amount (INR)', 'Debit/Credit', 'Balance(INR)', 'Cheque Number', 'Branch Name(SOL)'
        ]
    
    def parse_transactions(self, pdf_path):
        all_transactions = []
        
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Processing {len(pdf.pages)} pages")
            
            for page_num, page in enumerate(pdf.pages):
                print(f"Processing page {page_num + 1}")
                tables = page.extract_tables()
                
                for table_idx, table in enumerate(tables):
                    if table and self._is_transaction_table(table):
                        print(f"Found transaction table on page {page_num + 1}, table {table_idx + 1}")
                        transactions = self._extract_transactions_from_table(table)
                        all_transactions.extend(transactions)
                        print(f"Extracted {len(transactions)} transactions from this table")
        
        print(f"Total transactions extracted: {len(all_transactions)}")
        return all_transactions
    
    def _is_transaction_table(self, table):
        if not table or len(table) < 2:
            return False
        
        # Check if first row contains expected headers
        header_row = table[0]
        if not header_row:
            return False
        
        # Clean and normalize headers
        clean_headers = [str(cell).strip() if cell else '' for cell in header_row]
        
        # Check for key headers that identify transaction table
        key_headers = ['S.No', 'Transaction Date', 'Particulars', 'Amount', 'Debit/Credit', 'Balance']
        matches = 0
        
        for key_header in key_headers:
            for cell in clean_headers:
                if key_header.lower() in cell.lower():
                    matches += 1
                    break
        
        return matches >= 4  # At least 4 key headers should match
    
    def _extract_transactions_from_table(self, table):
        transactions = []
        
        if not table or len(table) < 2:
            return transactions
        
        # Skip header row
        for row_idx, row in enumerate(table[1:], 1):
            if not row or not any(row):  # Skip empty rows
                continue
            
            transaction = self._parse_table_row(row, row_idx)
            if transaction:
                transactions.append(transaction)
        
        return transactions
    
    def _parse_table_row(self, row, row_idx):
        try:
            # Ensure row has enough columns
            while len(row) < 9:
                row.append('')
            
            # Clean cell values
            cells = [str(cell).strip() if cell else '' for cell in row]
            
            # Extract data based on column positions
            sno = cells[0]
            transaction_date = cells[1]
            value_date = cells[2]
            particulars = cells[3]
            amount_str = cells[4]
            debit_credit = cells[5]
            balance_str = cells[6]
            cheque_number = cells[7]
            branch_name = cells[8]
            
            # Validate S.No (should be numeric)
            try:
                int(sno)
            except:
                return None  # Skip non-transaction rows
            
            # Validate date format
            if not re.match(r'\d{2}/\d{2}/\d{4}', transaction_date):
                return None
            
            # Parse amounts
            amount = self._parse_amount(amount_str)
            balance = self._parse_amount(balance_str)
            
            if amount is None or balance is None:
                return None
            
            # Determine debit/credit
            debit = amount if debit_credit.upper() == 'DR' else 0
            credit = amount if debit_credit.upper() == 'CR' else 0
            
            return Transaction(
                date=transaction_date,
                description=particulars,
                debit=debit,
                credit=credit,
                balance=balance,
                bank_name='AXIS'
            )
            
        except Exception as e:
            print(f"Error parsing row {row_idx}: {row}, Error: {e}")
            return None
    
    def _parse_amount(self, amount_str):
        if not amount_str:
            return 0.0
        
        try:
            # Remove commas and convert to float
            clean_amount = amount_str.replace(',', '').replace('₹', '').strip()
            return float(clean_amount)
        except:
            return None