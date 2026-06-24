"""
Prepare Real Dataset

This script loads the real international football results dataset,
analyzes it, filters matches from 1990 onwards, and saves the filtered data.
"""

import pandas as pd
from pathlib import Path

def prepare_data():
    """
    Load, analyze, and prepare the real dataset
    """
    print("="*70)
    print("LOADING REAL INTERNATIONAL FOOTBALL RESULTS DATASET")
    print("="*70)
    
    # Load the real dataset
    input_path = "data/results.csv"
    print(f"\nLoading data from: {input_path}")
    
    df = pd.read_csv(input_path, parse_dates=['date'])
    
    # Print shape
    print(f"\nDataset Shape: {df.shape}")
    print(f"  Rows: {df.shape[0]:,}")
    print(f"  Columns: {df.shape[1]}")
    
    # Print columns
    print(f"\nColumns: {list(df.columns)}")
    
    # Print date range
    print(f"\nDate Range:")
    print(f"  Earliest match: {df['date'].min().strftime('%Y-%m-%d')}")
    print(f"  Latest match: {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"  Span: {(df['date'].max() - df['date'].min()).days / 365.25:.1f} years")
    
    # Count unique teams
    unique_home = set(df['home_team'].unique())
    unique_away = set(df['away_team'].unique())
    all_teams = unique_home | unique_away
    print(f"\nUnique Teams: {len(all_teams)}")
    
    # Missing values report
    print(f"\nMissing Values Report:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("  No missing values found!")
    else:
        for col in missing[missing > 0].index:
            print(f"  {col}: {missing[col]} ({missing[col]/len(df)*100:.2f}%)")
    
    # Filter matches from 1990-01-01 onward
    print(f"\n{'='*70}")
    print("FILTERING MATCHES FROM 1990-01-01 ONWARD")
    print("="*70)
    
    cutoff_date = pd.Timestamp('1990-01-01')
    df_filtered = df[df['date'] >= cutoff_date].copy()
    
    print(f"\nOriginal matches: {len(df):,}")
    print(f"Matches after 1990-01-01: {len(df_filtered):,}")
    print(f"Matches removed: {len(df) - len(df_filtered):,}")
    print(f"Percentage retained: {len(df_filtered)/len(df)*100:.1f}%")
    
    # Additional statistics on filtered data
    print(f"\nFiltered Dataset Statistics:")
    print(f"  Date range: {df_filtered['date'].min().strftime('%Y-%m-%d')} to {df_filtered['date'].max().strftime('%Y-%m-%d')}")
    print(f"  Unique teams: {len(set(df_filtered['home_team'].unique()) | set(df_filtered['away_team'].unique()))}")
    print(f"  Unique tournaments: {df_filtered['tournament'].nunique()}")
    print(f"  Total goals: {df_filtered['home_score'].sum() + df_filtered['away_score'].sum():,}")
    print(f"  Average goals per match: {(df_filtered['home_score'] + df_filtered['away_score']).mean():.2f}")
    
    # Save filtered data
    output_path = "data/processed/matches_filtered.csv"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df_filtered.to_csv(output_path, index=False)
    
    print(f"\n{'='*70}")
    print(f"SAVED FILTERED DATA")
    print("="*70)
    print(f"Output file: {output_path}")
    print(f"File size: {Path(output_path).stat().st_size / (1024*1024):.2f} MB")
    print(f"\n[OK] Data preparation complete!")
    
    return df_filtered


if __name__ == "__main__":
    prepare_data()

# Made with Bob
