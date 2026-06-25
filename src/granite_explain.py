"""
IBM Granite Connection Test

Tests the IBM Granite AI connection with the updated WML-associated project.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_granite_connection():
    """
    Test IBM Granite AI connection with real credentials
    """
    print("="*70)
    print("IBM GRANITE CONNECTION TEST")
    print("="*70)
    
    # Get credentials from environment
    api_key = os.getenv("WATSONX_API_KEY") or os.getenv("IBM_CLOUD_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID") or os.getenv("IBM_WATSONX_PROJECT_ID")
    url = os.getenv("WATSONX_URL", "https://eu-de.ml.cloud.ibm.com")
    
    print(f"\nConfiguration:")
    print(f"  API Key: {'*' * 20}{api_key[-10:] if api_key else 'NOT SET'}")
    print(f"  Project ID: {project_id}")
    print(f"  URL: {url}")
    
    if not api_key or not project_id:
        print("\n[ERROR] Missing credentials!")
        print("Please set WATSONX_API_KEY and WATSONX_PROJECT_ID in .env file")
        return False
    
    try:
        print("\n" + "-"*70)
        print("Initializing IBM watsonx.ai client...")
        print("-"*70)
        
        from ibm_watsonx_ai import Credentials
        from ibm_watsonx_ai.foundation_models import ModelInference
        from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
        
        # Set up credentials
        credentials = Credentials(
            url=url,
            api_key=api_key
        )
        
        print("[OK] Credentials configured")
        
        # Initialize model with available model
        model_id = "meta-llama/llama-3-3-70b-instruct"
        print(f"\nInitializing model: {model_id}")
        
        model = ModelInference(
            model_id=model_id,
            credentials=credentials,
            project_id=project_id,
            params={
                GenParams.MAX_NEW_TOKENS: 150,
                GenParams.TEMPERATURE: 0.7,
                GenParams.TOP_P: 0.9
            }
        )
        
        print("[OK] Model initialized successfully")
        
        # Test prompt
        print("\n" + "-"*70)
        print("Testing with sample prompt...")
        print("-"*70)
        
        prompt = """Explain in 3 sentences why Brazil would be favored against Argentina in a World Cup match, given Brazil has a 63% win rate and Argentina has 58%."""
        
        print(f"\nPrompt:\n{prompt}")
        print("\nGenerating response...")
        
        # Generate response
        response = model.generate_text(prompt=prompt)
        
        print("\n" + "="*70)
        print("GRANITE AI RESPONSE:")
        print("="*70)
        print(response)
        print("="*70)
        
        print("\n[OK] IBM Granite connected successfully!")
        return True
        
    except ImportError as e:
        print(f"\n[ERROR] Import error: {e}")
        print("Make sure ibm-watsonx-ai is installed: pip install ibm-watsonx-ai")
        return False
        
    except Exception as e:
        print(f"\n[ERROR] Connection failed!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        
        # Print detailed error if available
        if hasattr(e, 'response'):
            print(f"\nHTTP Status: {e.response.status_code if hasattr(e.response, 'status_code') else 'N/A'}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text[:500]}")
        
        return False


if __name__ == "__main__":
    success = test_granite_connection()
    exit(0 if success else 1)

# Made with Bob
