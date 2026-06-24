"""
Download International Football Results Dataset

This script downloads the international football results dataset from Kaggle.
You'll need to have kaggle API credentials configured.

Setup:
1. Install kaggle: pip install kaggle
2. Get API credentials from https://www.kaggle.com/account
3. Place kaggle.json in ~/.kaggle/ (Linux/Mac) or C:\\Users\\<username>\\.kaggle\\ (Windows)
4. Run this script: python scripts/download_dataset.py
"""

import os
import sys
from pathlib import Path

def download_dataset():
    """Download the international football results dataset"""
    
    # Add project root to path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    data_dir = project_root / "data" / "raw"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("International Football Results Dataset Downloader")
    print("=" * 60)
    
    # Check if dataset already exists
    csv_file = data_dir / "international_results.csv"
    if csv_file.exists():
        print(f"\n✓ Dataset already exists at: {csv_file}")
        print(f"  File size: {csv_file.stat().st_size / (1024*1024):.2f} MB")
        
        response = input("\nDo you want to re-download? (y/n): ")
        if response.lower() != 'y':
            print("Skipping download.")
            return
    
    print("\nAttempting to download dataset...")
    print("Note: This requires Kaggle API credentials")
    
    try:
        import kaggle
        
        # Download from Kaggle
        # Dataset: martj42/international-football-results-from-1872-to-2017
        print("\nDownloading from Kaggle...")
        kaggle.api.dataset_download_files(
            'martj42/international-football-results-from-1872-to-2017',
            path=str(data_dir),
            unzip=True
        )
        
        print(f"\n✓ Dataset downloaded successfully to: {data_dir}")
        
        # Verify the file
        if csv_file.exists():
            print(f"✓ File verified: {csv_file}")
            print(f"  File size: {csv_file.stat().st_size / (1024*1024):.2f} MB")
        else:
            print("⚠ Warning: Expected file not found after download")
            
    except ImportError:
        print("\n✗ Error: kaggle package not installed")
        print("  Install it with: pip install kaggle")
        print("\nAlternative: Manual Download")
        print("1. Visit: https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017")
        print("2. Download the dataset")
        print(f"3. Extract and place 'results.csv' in: {data_dir}")
        print(f"4. Rename it to: international_results.csv")
        
    except Exception as e:
        print(f"\n✗ Error downloading dataset: {e}")
        print("\nAlternative: Manual Download")
        print("1. Visit: https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017")
        print("2. Download the dataset")
        print(f"3. Extract and place 'results.csv' in: {data_dir}")
        print(f"4. Rename it to: international_results.csv")

if __name__ == "__main__":
    download_dataset()

# Made with Bob
