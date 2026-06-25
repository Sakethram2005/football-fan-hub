"""
Feature Engineering Module

This module creates features from raw match data for ML model training.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureEngineer:
    """
    Creates features from historical match data for prediction
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with match data
        
        Args:
            df: DataFrame with match results
        """
        self.df = df.copy()
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.sort_values('date').reset_index(drop=True)
        
    def calculate_team_form(self, team: str, date: pd.Timestamp, window: int = 5) -> float:
        """
        Calculate team's recent form (win rate in last N matches)
        
        Args:
            team: Team name
            date: Current date
            window: Number of recent matches to consider
            
        Returns:
            Win rate (0.0 to 1.0)
        """
        # Get recent matches before this date
        recent = self.df[
            ((self.df['home_team'] == team) | (self.df['away_team'] == team)) &
            (self.df['date'] < date)
        ].tail(window)
        
        if len(recent) == 0:
            return 0.5  # Default for new teams
        
        # Count wins
        wins = 0
        for _, match in recent.iterrows():
            if match['home_team'] == team:
                if match['home_score'] > match['away_score']:
                    wins += 1
            else:  # away team
                if match['away_score'] > match['home_score']:
                    wins += 1
        
        return wins / len(recent)
    
    def calculate_goal_difference(self, team: str, date: pd.Timestamp, window: int = 10) -> float:
        """
        Calculate average goal difference per match
        
        Args:
            team: Team name
            date: Current date
            window: Number of recent matches
            
        Returns:
            Average goal difference per match
        """
        recent = self.df[
            ((self.df['home_team'] == team) | (self.df['away_team'] == team)) &
            (self.df['date'] < date)
        ].tail(window)
        
        if len(recent) == 0:
            return 0.0
        
        goal_diff = 0
        for _, match in recent.iterrows():
            if match['home_team'] == team:
                goal_diff += (match['home_score'] - match['away_score'])
            else:
                goal_diff += (match['away_score'] - match['home_score'])
        
        return goal_diff / len(recent)
    
    def calculate_h2h_record(self, team1: str, team2: str, date: pd.Timestamp) -> float:
        """
        Calculate head-to-head win rate for team1 against team2
        
        Args:
            team1: First team
            team2: Second team
            date: Current date
            
        Returns:
            Win rate for team1 (0.0 to 1.0)
        """
        h2h = self.df[
            (((self.df['home_team'] == team1) & (self.df['away_team'] == team2)) |
             ((self.df['home_team'] == team2) & (self.df['away_team'] == team1))) &
            (self.df['date'] < date)
        ]
        
        if len(h2h) == 0:
            return 0.5  # No history
        
        team1_wins = 0
        for _, match in h2h.iterrows():
            if match['home_team'] == team1:
                if match['home_score'] > match['away_score']:
                    team1_wins += 1
            else:
                if match['away_score'] > match['home_score']:
                    team1_wins += 1
        
        return team1_wins / len(h2h)
    
    def calculate_home_advantage(self, team: str, date: pd.Timestamp) -> float:
        """
        Calculate team's home win rate
        
        Args:
            team: Team name
            date: Current date
            
        Returns:
            Home win rate
        """
        home_matches = self.df[
            (self.df['home_team'] == team) &
            (self.df['date'] < date) &
            (self.df['neutral'] == False)
        ]
        
        if len(home_matches) == 0:
            return 0.5
        
        home_wins = sum(home_matches['home_score'] > home_matches['away_score'])
        return home_wins / len(home_matches)
    
    def calculate_goals_scored_rate(self, team: str, date: pd.Timestamp, window: int = 10) -> float:
        """
        Calculate average goals scored per match
        
        Args:
            team: Team name
            date: Current date
            window: Number of recent matches
            
        Returns:
            Average goals scored
        """
        recent = self.df[
            ((self.df['home_team'] == team) | (self.df['away_team'] == team)) &
            (self.df['date'] < date)
        ].tail(window)
        
        if len(recent) == 0:
            return 1.5  # Default average
        
        goals = 0
        for _, match in recent.iterrows():
            if match['home_team'] == team:
                goals += match['home_score']
            else:
                goals += match['away_score']
        
        return goals / len(recent)
    
    def calculate_goals_conceded_rate(self, team: str, date: pd.Timestamp, window: int = 10) -> float:
        """
        Calculate average goals conceded per match
        
        Args:
            team: Team name
            date: Current date
            window: Number of recent matches
            
        Returns:
            Average goals conceded
        """
        recent = self.df[
            ((self.df['home_team'] == team) | (self.df['away_team'] == team)) &
            (self.df['date'] < date)
        ].tail(window)
        
        if len(recent) == 0:
            return 1.5  # Default average
        
        goals = 0
        for _, match in recent.iterrows():
            if match['home_team'] == team:
                goals += match['away_score']
            else:
                goals += match['home_score']
        
        return goals / len(recent)
    
    def create_features_for_match(self, home_team: str, away_team: str, 
                                   date: pd.Timestamp, is_neutral: bool = False) -> Dict:
        """
        Create all features for a single match
        
        Args:
            home_team: Home team name
            away_team: Away team name
            date: Match date
            is_neutral: Whether it's a neutral venue
            
        Returns:
            Dictionary of features
        """
        features = {
            # Team form (last 5 matches)
            'home_form': self.calculate_team_form(home_team, date, window=5),
            'away_form': self.calculate_team_form(away_team, date, window=5),
            
            # Goal difference (last 10 matches)
            'home_goal_diff': self.calculate_goal_difference(home_team, date, window=10),
            'away_goal_diff': self.calculate_goal_difference(away_team, date, window=10),
            
            # Head-to-head
            'h2h_record': self.calculate_h2h_record(home_team, away_team, date),
            
            # Home advantage
            'home_advantage': self.calculate_home_advantage(home_team, date) if not is_neutral else 0.5,
            
            # Goals scored/conceded rates
            'home_goals_scored': self.calculate_goals_scored_rate(home_team, date),
            'away_goals_scored': self.calculate_goals_scored_rate(away_team, date),
            'home_goals_conceded': self.calculate_goals_conceded_rate(home_team, date),
            'away_goals_conceded': self.calculate_goals_conceded_rate(away_team, date),
            
            # Match context
            'is_neutral': 1 if is_neutral else 0,
            'year': date.year,
            'month': date.month,
        }
        
        return features
    
    def create_training_dataset(self, min_date: str = '1990-01-01') -> Tuple[pd.DataFrame, pd.Series]:
        """
        Create full training dataset with features and labels
        
        Args:
            min_date: Minimum date to include
            
        Returns:
            Tuple of (features DataFrame, labels Series)
        """
        logger.info("Creating training dataset...")
        
        # Filter by date
        df_filtered = self.df[self.df['date'] >= min_date].copy()
        logger.info(f"Using {len(df_filtered)} matches from {min_date} onward")
        
        features_list = []
        labels_list = []
        
        for idx, match in df_filtered.iterrows():
            if idx % 1000 == 0:
                logger.info(f"Processing match {idx}/{len(df_filtered)}")
            
            # Create features
            features = self.create_features_for_match(
                match['home_team'],
                match['away_team'],
                match['date'],
                match['neutral']
            )
            
            # Create label (0=away win, 1=draw, 2=home win)
            if match['home_score'] > match['away_score']:
                label = 2  # Home win
            elif match['home_score'] < match['away_score']:
                label = 0  # Away win
            else:
                label = 1  # Draw
            
            features_list.append(features)
            labels_list.append(label)
        
        X = pd.DataFrame(features_list)
        y = pd.Series(labels_list, name='outcome')
        
        logger.info(f"Created dataset with {len(X)} samples and {len(X.columns)} features")
        logger.info(f"Label distribution:\n{y.value_counts()}")
        
        return X, y


def main():
    """
    Test feature engineering
    """
    print("="*70)
    print("FEATURE ENGINEERING TEST")
    print("="*70)
    
    # Load data
    print("\nLoading data...")
    df = pd.read_csv('data/processed/matches_filtered.csv', parse_dates=['date'])
    print(f"Loaded {len(df)} matches")
    
    # Initialize feature engineer
    engineer = FeatureEngineer(df)
    
    # Create training dataset
    X, y = engineer.create_training_dataset(min_date='2000-01-01')
    
    # Display sample
    print("\n" + "-"*70)
    print("SAMPLE FEATURES:")
    print("-"*70)
    print(X.head())
    
    print("\n" + "-"*70)
    print("FEATURE STATISTICS:")
    print("-"*70)
    print(X.describe())
    
    # Save
    output_path = 'data/processed/training_features.csv'
    X.to_csv(output_path, index=False)
    y.to_csv('data/processed/training_labels.csv', index=False)
    
    print(f"\n[OK] Features saved to {output_path}")
    print(f"[OK] Labels saved to data/processed/training_labels.csv")


if __name__ == "__main__":
    main()

# Made with Bob
