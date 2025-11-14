# Vercel Deployment Guide

## 🚀 Deploy to Vercel

This project has been configured for deployment on Vercel. Follow these steps:

### Prerequisites
- GitHub account
- Vercel account (free)
- Git installed

### Step 1: Push to GitHub
```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit for Vercel deployment"

# Add GitHub remote (replace with your repository URL)
git remote add origin https://github.com/yourusername/pdfparse.git

# Push to GitHub
git push -u origin main
```

### Step 2: Deploy on Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "New Project"
4. Import your GitHub repository
5. Vercel will automatically detect the configuration
6. Click "Deploy"

### Step 3: Configuration
The project includes:
- `vercel.json` - Vercel configuration
- `api/index.py` - Flask API endpoint
- `requirements-vercel.txt` - Python dependencies
- `.vercelignore` - Files to exclude from deployment

### Features
- ✅ Web interface for PDF upload
- ✅ Support for 19+ Indian banks
- ✅ JSON export of transactions
- ✅ Password-protected PDF support
- ✅ Auto-detection of IDBI passwords

### Supported Banks
- State Bank of India (SBI)
- Axis Bank
- Yes Bank
- Indian Overseas Bank
- Bandhan Bank
- HSBC
- Union Bank
- Indian Bank
- Federal Bank
- Jammu & Kashmir Bank
- IDBI Bank
- Bank of Baroda
- HDFC Bank
- Punjab National Bank
- Central Bank of India
- Karnataka Bank
- Kotak Mahindra Bank
- Canara Bank
- IndusInd Bank

### Usage
1. Visit your deployed URL
2. Upload a bank statement PDF
3. Enter password if required
4. View parsed transactions
5. Download JSON results

### Local Testing
```bash
# Install dependencies
pip install -r requirements-vercel.txt

# Run Flask app
python api/index.py
```

### Troubleshooting
- Ensure all dependencies are in `requirements-vercel.txt`
- Check Vercel function logs for errors
- Verify PDF file size is under Vercel limits (4.5MB)
- Test locally before deploying