#!/usr/bin/env python3
"""
Test script for the Flask API before deployment
"""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from api.index import app
    print("✅ Flask app imported successfully")
    
    # Test import of bank parser
    from bank_parser import IndianBankStatementParser
    print("✅ Bank parser imported successfully")
    
    # Test basic functionality
    parser = IndianBankStatementParser()
    print("✅ Parser initialized successfully")
    
    print("\n🚀 Ready for deployment!")
    print("Run: python api/index.py to test locally")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install -r requirements-vercel.txt")
except Exception as e:
    print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("\n🧪 Testing Flask app...")
    try:
        app.run(debug=True, port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")