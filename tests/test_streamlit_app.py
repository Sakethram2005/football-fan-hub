"""
Test script for Streamlit application
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("[OK] Streamlit imported")
    except ImportError as e:
        print(f"[ERROR] Failed to import streamlit: {e}")
        return False
    
    try:
        import pandas as pd
        print("[OK] Pandas imported")
    except ImportError as e:
        print(f"[ERROR] Failed to import pandas: {e}")
        return False
    
    try:
        import plotly.graph_objects as go
        print("[OK] Plotly imported")
    except ImportError as e:
        print(f"[ERROR] Failed to import plotly: {e}")
        return False
    
    try:
        from src.prediction_engine import FootballPredictionEngine
        print("[OK] Prediction engine imported")
    except ImportError as e:
        print(f"[ERROR] Failed to import prediction engine: {e}")
        return False
    
    try:
        from src.data_preprocessing import load_and_preprocess_data
        print("[OK] Data preprocessing imported")
    except ImportError as e:
        print(f"[ERROR] Failed to import data preprocessing: {e}")
        return False
    
    return True

def test_data_loading():
    """Test that data can be loaded"""
    print("\nTesting data loading...")
    
    try:
        from src.data_preprocessing import load_and_preprocess_data
        df = load_and_preprocess_data()
        print(f"[OK] Data loaded: {len(df)} matches")
        print(f"[OK] Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"[OK] Unique teams: {len(set(df['home_team'].unique()) | set(df['away_team'].unique()))}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")
        return False

def test_prediction_engine():
    """Test that prediction engine can be initialized"""
    print("\nTesting prediction engine...")
    
    try:
        from src.prediction_engine import FootballPredictionEngine
        engine = FootballPredictionEngine()
        print("[OK] Prediction engine initialized")
        
        # Test a simple prediction
        result = engine.predict_match("Brazil", "Argentina", "2026-06-30", False)
        print(f"[OK] Prediction made: {result['prediction']} ({result['confidence']:.1f}%)")
        
        return True
    except Exception as e:
        print(f"[ERROR] Failed to initialize prediction engine: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_files():
    """Test that model files exist"""
    print("\nTesting model files...")
    
    model_files = [
        "models/match_predictor.pkl",
        "models/feature_scaler.pkl",
        "models/model_metrics.json"
    ]
    
    all_exist = True
    for file_path in model_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size / (1024 * 1024)
            print(f"[OK] {file_path} exists ({size:.2f} MB)")
        else:
            print(f"[ERROR] {file_path} not found")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("="*60)
    print("STREAMLIT APPLICATION TEST SUITE")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("Model Files", test_model_files),
        ("Data Loading", test_data_loading),
        ("Prediction Engine", test_prediction_engine)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n[ERROR] Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("="*60)
    print(f"SUMMARY: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n✓ All tests passed! Application is ready to run.")
        print("\nTo start the application, run:")
        print("  streamlit run app/main.py")
        return True
    else:
        print("\n✗ Some tests failed. Please fix the issues before running the application.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

# Made with Bob
