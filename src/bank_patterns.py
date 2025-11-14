# src/bank_patterns.py
BANK_SIGNATURES = {
    'AXIS': {
        'keywords': ['statement of axis bank', 'axis bank'],
        'account_pattern': r'Account No[.:]?\s*(\d+)',
        'opening_balance_pattern': r'Opening Balance:\s*INR\s*([\d,]+\.?\d{0,2})',
        'typical_headers': ['S.No', 'Transaction Date', 'Value Date', 'Particulars', 'Amount', 'Debit/Credit', 'Balance']
    },
    'IDBI': {
        'keywords': ['idbi bank', 'idbi', 'ibkl'],
        'account_pattern': r'\d{16}',
        'typical_headers': ['Date', 'Particulars', 'Chq. no', 'Withdrawals', 'Deposits', 'Balance']
    },
    'IOB': {
        'keywords': ['indian overseas bank', 'iob'],
        'account_pattern': r'Account No[.:]?\s*(\d+)',
        'typical_headers': ['Date', 'Value Date', 'Particulars', 'Ref No', 'Cheque No', 'Transaction Type', 'Debit', 'Credit', 'Balance']
    },
    'INDIAN': {
        'keywords': ['indian bank', 'idib'],
        'account_pattern': r'\d{10}',
        'typical_headers': ['Post Date', 'Value Date', 'Details', 'Chq.No.', 'Debit', 'Credit', 'Balance']
    },
    'SBI': {
        'keywords': ['sbi', 'sbin', 'state bank of india'],
        'account_pattern': r'\d{11,17}',
        'typical_headers': ['Txn Date', 'Value Date', 'Description', 'Ref No./Cheque No.', 'Branch Code', 'Debit', 'Credit', 'Balance']
    },
    'JK': {
        'keywords': ['jammu and kashmir bank', 'jaka'],
        'account_pattern': r'\d{16}',
        'typical_headers': []
    },
    'FEDERAL': {
        'keywords': ['federal bank', 'fdrl'],
        'account_pattern': r'\d{14}',
        'typical_headers': ['Date', 'Value Date', 'Particulars', 'Tran Type', 'Tran ID', 'Withdrawals', 'Deposits', 'Balance']
    },
    'INDIAN': {
        'keywords': ['indian bank', 'idib'],
        'account_pattern': r'\d{10}',
        'typical_headers': ['Post Date', 'Value Date', 'Details', 'Chq.No.', 'Debit', 'Credit', 'Balance']
    },
    'UNION': {
        'keywords': ['union bank', 'ubin'],
        'account_pattern': r'\d{15}',
        'typical_headers': ['S.No', 'Date', 'Transaction Id', 'Remarks', 'Amount(Rs.)', 'Balance(Rs.)']
    },
    'HSBC': {
        'keywords': ['hsbc', 'ifsc code: hsbc'],
        'account_pattern': r'\d{3}-\d{6}-\d{3}',
        'typical_headers': ['Date Transaction Details', 'Deposits', 'Withdrawals', 'Balance']
    },
    'BANDHAN': {
        'keywords': ['bandhan bank', 'bandhan', 'bdbl', 'ifsc bdbl'],
        'account_pattern': r'Account Number\s*(\d+)',
        'typical_headers': ['Transaction Date', 'Value Date', 'Description', 'Amount', 'Dr / Cr', 'Balance']
    },
    'YES': {
        'keywords': ['branch name: yes bank ltd', 'yes bank'],
        'account_pattern': r'Account No[.:]?\s*(\d+)',
        'typical_headers': ['Transaction Date', 'Value Date', 'Description', 'Reference Number', 'Withdrawals', 'Deposits', 'Running Balance']
    },
    'BOB': {
        'keywords': ['bank of baroda', 'barb'],
        'account_pattern': r'\d{14}',
        'typical_headers': ['Serial No', 'Transaction Date', 'Value Date', 'Description', 'Cheque Number', 'Debit', 'Credit', 'Balance']
    },
    'HDFC': {
        'keywords': ['hdfc bank', 'hdfc'],
        'account_pattern': r'\d{14}',
        'typical_headers': ['Date', 'Narration', 'Chq./Ref.No.', 'Value Dt', 'Withdrawal Amt.', 'Deposit Amt.', 'Closing Balance']
    },
    'PNB': {
        'keywords': ['punjab national bank', 'punb'],
        'account_pattern': r'\d{16}',
        'typical_headers': ['Date', 'Instrument ID', 'Amount', 'Type', 'Balance', 'Remarks']
    },
    'CBI': {
        'keywords': ['central bank of india', 'cbin'],
        'account_pattern': r'\d{16}',
        'typical_headers': ['Post Date', 'Value Date', 'Branch Code', 'Cheque Number', 'Account Description', 'Debit', 'Credit', 'Balance']
    },
    'KARNATAKA': {
        'keywords': ['karnataka bank ltd', 'karb'],
        'account_pattern': r'\d{16}',
        'typical_headers': ['Date', 'Particulars', 'Withdrawals', 'Deposits', 'Balance']
    },
    'KOTAK': {
        'keywords': ['kotak mahindra bank', 'kotak', 'kkbk'],
        'account_pattern': r'\d{10}',
        'typical_headers': ['Date', 'Narration', 'Chq/Ref No.', 'Withdrawal(Dr)', 'Deposit(Cr)', 'Balance']
    },
    'CANARA': {
        'keywords': ['canara bank', 'cnrb'],
        'account_pattern': r'\d{10}',
        'typical_headers': ['Date', 'Particulars', 'Deposits', 'Withdrawals', 'Balance']
    },
    'INDUSIND': {
        'keywords': ['indusind bank', 'indb'],
        'account_pattern': r'\d{12}',
        'typical_headers': ['Date', 'Particulars', 'Chq No/Ref No', 'Withdrawal', 'Deposit', 'Balance']
    }
}

class BankIdentifier:
    def identify_bank(self, text):
        text_lower = text.lower()
        
        # Identify by IFSC code only
        if 'indb0' in text_lower:
            return 'INDUSIND'
        if 'cnrb0' in text_lower:
            return 'CANARA'
        if 'kkbk0' in text_lower:
            return 'KOTAK'
        if 'karb0' in text_lower:
            return 'KARNATAKA'
        if 'cbin0' in text_lower:
            return 'CBI'
        if 'punb0' in text_lower:
            return 'PNB'
        if 'barb0' in text_lower:
            return 'BOB'
        if 'ibkl0' in text_lower:
            return 'IDBI'
        if 'jaka0' in text_lower:
            return 'JK'
        if 'fdrl0' in text_lower:
            return 'FEDERAL'
        if 'idib0' in text_lower:
            return 'INDIAN'
        if 'ubin0' in text_lower:
            return 'UNION'
        if 'hsbc0' in text_lower:
            return 'HSBC'
        if 'bdbl0' in text_lower:
            return 'BANDHAN'
        if 'yesb0' in text_lower:
            return 'YES'
        if 'ioba0' in text_lower:
            return 'IOB'
        if 'sbin0' in text_lower:
            return 'SBI'
        if 'hdfc0' in text_lower:
            return 'HDFC'
        
        return "UNKNOWN"
    
    def _check_headers(self, text, headers):
        found_headers = 0
        for header in headers:
            if header.lower() in text.lower():
                found_headers += 1
        return found_headers >= 3