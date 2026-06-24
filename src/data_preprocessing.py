"""
Data Preprocessing Module

This module handles cleaning and preprocessing of the international football results dataset.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """
    Handles data cleaning and preprocessing for football match data
    """
    
    def __init__(self, data_path: str):
        """
        Initialize the preprocessor
        
        Args:
            data_path: Path to the raw CSV file
        """
        self.data_path = Path(data_path)
        self.df = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load the raw dataset
        
        Returns:
            DataFrame with raw data
        """
        logger.info(f"Loading data from {self.data_path}")
        
        try:
            self.df = pd.read_csv(self.data_path)
            logger.info(f"Loaded {len(self.df)} records")
            logger.info(f"Columns: {list(self.df.columns)}")
            return self.df
        except FileNotFoundError:
            logger.error(f"File not found: {self.data_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean the dataset by handling missing values and standardizing formats
        
        Returns:
            Cleaned DataFrame
        """
        logger.info("Starting data cleaning...")
        
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        initial_rows = len(self.df)
        
        # Remove rows with missing scores
        self.df = self.df.dropna(subset=['home_score', 'away_score'])
        logger.info(f"Removed {initial_rows - len(self.df)} rows with missing scores")
        
        # Convert date to datetime
        self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
        
        # Remove rows with invalid dates
        before_date_clean = len(self.df)
        self.df = self.df.dropna(subset=['date'])
        logger.info(f"Removed {before_date_clean - len(self.df)} rows with invalid dates")
        
        # Standardize team names (strip whitespace, title case)
        self.df['home_team'] = self.df['home_team'].str.strip().str.title()
        self.df['away_team'] = self.df['away_team'].str.strip().str.title()
        
        # Standardize tournament names
        self.df['tournament'] = self.df['tournament'].str.strip()
        
        # Convert scores to integers
        self.df['home_score'] = self.df['home_score'].astype(int)
        self.df['away_score'] = self.df['away_score'].astype(int)
        
        # Handle neutral venue (convert to boolean)
        if 'neutral' in self.df.columns:
            self.df['neutral'] = self.df['neutral'].fillna(False).astype(bool)
        else:
            self.df['neutral'] = False
        
        # Sort by date
        self.df = self.df.sort_values('date').reset_index(drop=True)
        
        logger.info(f"Data cleaning complete. Final dataset: {len(self.df)} rows")
        
        return self.df
    
    def filter_world_cup_matches(self) -> pd.DataFrame:
        """
        Filter dataset to include only World Cup matches
        
        Returns:
            DataFrame with World Cup matches only
        """
        logger.info("Filtering World Cup matches...")
        
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Filter for World Cup tournaments
        world_cup_keywords = ['World Cup', 'FIFA World Cup', 'WC']
        mask = self.df['tournament'].str.contains('|'.join(world_cup_keywords), case=False, na=False)
        
        wc_df = self.df[mask].copy()
        logger.info(f"Found {len(wc_df)} World Cup matches")
        
        return wc_df
    
    def get_data_summary(self) -> dict:
        """
        Get summary statistics of the dataset
        
        Returns:
            Dictionary with summary statistics
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        summary = {
            'total_matches': len(self.df),
            'date_range': {
                'start': self.df['date'].min().strftime('%Y-%m-%d'),
                'end': self.df['date'].max().strftime('%Y-%m-%d')
            },
            'unique_teams': len(set(self.df['home_team'].unique()) | set(self.df['away_team'].unique())),
            'unique_tournaments': self.df['tournament'].nunique(),
            'total_goals': int(self.df['home_score'].sum() + self.df['away_score'].sum()),
            'avg_goals_per_match': float((self.df['home_score'] + self.df['away_score']).mean()),
            'missing_values': self.df.isnull().sum().to_dict()
        }
        
        return summary
    
    def save_processed_data(self, output_path: str):
        """
        Save the processed dataset
        
        Args:
            output_path: Path to save the processed CSV
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.df.to_csv(output_path, index=False)
        logger.info(f"Saved processed data to {output_path}")
        logger.info(f"File size: {output_path.stat().st_size / (1024*1024):.2f} MB")


def main():
    """
    Main function to run data preprocessing
    """
    # Paths
    raw_data_path = "data/raw/international_results.csv"
    processed_data_path = "data/processed/international_results_cleaned.csv"
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor(raw_data_path)
    
    # Load and clean data
    preprocessor.load_data()
    preprocessor.clean_data()
    
    # Get summary
    summary = preprocessor.get_data_summary()
    print("\n" + "="*60)
    print("DATASET SUMMARY")
    print("="*60)
    print(f"Total Matches: {summary['total_matches']:,}")
    print(f"Date Range: {summary['date_range']['start']} to {summary['date_range']['end']}")
    print(f"Unique Teams: {summary['unique_teams']}")
    print(f"Unique Tournaments: {summary['unique_tournaments']}")
    print(f"Total Goals: {summary['total_goals']:,}")
    print(f"Avg Goals/Match: {summary['avg_goals_per_match']:.2f}")
    print("="*60)
    
    # Save processed data
    preprocessor.save_processed_data(processed_data_path)
    
    # Filter and save World Cup matches
    wc_df = preprocessor.filter_world_cup_matches()
    wc_output_path = "data/processed/world_cup_matches.csv"
    wc_df.to_csv(wc_output_path, index=False)
    logger.info(f"Saved World Cup matches to {wc_output_path}")
    
    print(f"\n[OK] Data preprocessing complete!")
    print(f"     - Cleaned data: {processed_data_path}")
    print(f"     - World Cup data: {wc_output_path}")


if __name__ == "__main__":
    main()

# Made with Bob
