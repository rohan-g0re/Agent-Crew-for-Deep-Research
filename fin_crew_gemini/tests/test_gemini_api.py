#!/usr/bin/env python3
"""
Standalone test script to check if Gemini API is active and responsive.
This script makes a simple API call to verify connectivity.
"""

import os
import sys
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv

def load_api_key() -> Optional[str]:
    """
    Load Gemini API key from environment variables.
    Tries multiple common environment variable names.
    """
    # Load .env file if it exists
    load_dotenv()
    
    # Try multiple common API key names
    api_key_names = [
        'GEMINI_API_KEY',
        'GOOGLE_API_KEY',
        'GOOGLE_GEMINI_API_KEY',
        'GOOGLE_AI_API_KEY'
    ]
    
    for key_name in api_key_names:
        api_key = os.getenv(key_name)
        if api_key:
            print(f"✓ Found API key in environment variable: {key_name}")
            return api_key
    
    return None

def test_gemini_api() -> bool:
    """
    Test if Gemini API is active by making a simple API call.
    
    Returns:
        bool: True if API is active and responsive, False otherwise
    """
    try:
        # Load API key
        api_key = load_api_key()
        if not api_key:
            print("❌ ERROR: No Gemini API key found in environment variables.")
            print("Please set one of the following environment variables:")
            print("- GEMINI_API_KEY")
            print("- GOOGLE_API_KEY") 
            print("- GOOGLE_GEMINI_API_KEY")
            print("- GOOGLE_AI_API_KEY")
            return False
        
        # Configure the API
        genai.configure(api_key=api_key)
        print("✓ API key configured successfully")
        
        # Create a model instance
        model = genai.GenerativeModel('gemini-pro')
        print("✓ Model instance created")
        
        # Make a simple test call
        print("🔄 Testing API connection...")
        response = model.generate_content("Hello, this is a test. Please respond with 'API is working'.")
        
        if response and response.text:
            print(f"✅ SUCCESS: Gemini API is ACTIVE!")
            print(f"📝 Response: {response.text.strip()}")
            return True
        else:
            print("❌ ERROR: API responded but with empty content")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: Failed to connect to Gemini API")
        print(f"💬 Error details: {str(e)}")
        print(f"🔧 Error type: {type(e).__name__}")
        return False

def main():
    """Main function to run the API test."""
    print("=" * 50)
    print("🤖 GEMINI API CONNECTIVITY TEST")
    print("=" * 50)
    
    # Test the API
    is_active = test_gemini_api()
    
    print("\n" + "=" * 50)
    if is_active:
        print("✅ RESULT: Gemini API is ACTIVE and working properly!")
        sys.exit(0)
    else:
        print("❌ RESULT: Gemini API is NOT working or not accessible!")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your API key is valid and not expired")
        print("2. Verify your internet connection")
        print("3. Check if you have sufficient API quota")
        print("4. Ensure the API key has proper permissions")
        sys.exit(1)

if __name__ == "__main__":
    main() 