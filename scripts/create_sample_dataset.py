"""
Create Sample Dataset for Testing

This script creates a sample international football results dataset
for testing purposes when the full dataset is not available.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def create_sample_dataset(num_matches=1000, output_path="data/raw/international_results.csv"):
    """
    Create a sample dataset with realistic football match data
    
    Args:
        num_matches: Number of matches to generate
        output_path: Path to save the CSV file
    """
    
    # Sample teams (major football nations)
    teams = [
        'Brazil', 'Argentina', 'Germany', 'France', 'Spain', 'Italy',
        'England', 'Netherlands', 'Portugal', 'Belgium', 'Uruguay',
        'Croatia', 'Mexico', 'Colombia', 'Chile', 'Switzerland',
        'Denmark', 'Sweden', 'Poland', 'Austria', 'Japan', 'South Korea',
        'United States', 'Australia', 'Nigeria', 'Senegal', 'Morocco',
        'Egypt', 'Ghana', 'Cameroon', 'Iran', 'Saudi Arabia'
    ]
    
    # Sample tournaments
    tournaments = [
        'FIFA World Cup', 'FIFA World Cup qualification', 
        'Friendly', 'Copa América', 'UEFA Euro',
        'African Cup of Nations', 'Gold Cup',
        'Confederations Cup'
    ]
    
    # Sample cities and countries
    cities = [
        'London', 'Paris', 'Berlin', 'Madrid', 'Rome', 'Moscow',
        'Rio de Janeiro', 'Buenos Aires', 'Mexico City', 'Tokyo',
        'Seoul', 'Sydney', 'New York', 'Los Angeles', 'Dubai'
    ]
    
    countries = [
        'England', 'France', 'Germany', 'Spain', 'Italy', 'Russia',
        'Brazil', 'Argentina', 'Mexico', 'Japan', 'South Korea',
        'Australia', 'United States', 'UAE', 'Qatar'
    ]
    
    # Generate random matches
    matches = []
    start_date = datetime(2000, 1, 1)
    
    for i in range(num_matches):
        # Random date between 2000 and 2026
        days_offset = random.randint(0, 9500)
        match_date = start_date + timedelta(days=days_offset)
        
        # Random teams (ensure home != away)
        home_team = random.choice(teams)
        away_team = random.choice([t for t in teams if t != home_team])
        
        # Generate realistic scores (most matches have 0-4 goals per team)
        home_score = np.random.poisson(1.5)  # Average 1.5 goals
        away_score = np.random.poisson(1.2)  # Slightly lower for away team
        
        # Ensure scores are reasonable (0-7)
        home_score = min(home_score, 7)
        away_score = min(away_score, 7)
        
        # Random tournament (higher chance for World Cup)
        tournament_weights = [0.15, 0.25, 0.30, 0.10, 0.10, 0.05, 0.03, 0.02]
        tournament = random.choices(tournaments, weights=tournament_weights)[0]
        
        # Random location
        city = random.choice(cities)
        country = random.choice(countries)
        
        # Neutral venue (more likely for World Cup)
        neutral = tournament == 'FIFA World Cup' or random.random() < 0.3
        
        match = {
            'date': match_date.strftime('%Y-%m-%d'),
            'home_team': home_team,
            'away_team': away_team,
            'home_score': home_score,
            'away_score': away_score,
            'tournament': tournament,
            'city': city,
            'country': country,
            'neutral': neutral
        }
        
        matches.append(match)
    
    # Create DataFrame
    df = pd.DataFrame(matches)
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    print(f"[OK] Created sample dataset with {num_matches} matches")
    print(f"     Saved to: {output_path}")
    print(f"\nDataset Summary:")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Unique teams: {len(set(df['home_team'].unique()) | set(df['away_team'].unique()))}")
    print(f"  World Cup matches: {len(df[df['tournament'] == 'FIFA World Cup'])}")
    print(f"  Total goals: {df['home_score'].sum() + df['away_score'].sum()}")
    print(f"  Avg goals/match: {(df['home_score'] + df['away_score']).mean():.2f}")
    
    return df


if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Ensure data directory exists
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    
    # Get number of matches from command line or use default
    num_matches = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    
    # Create sample dataset
    create_sample_dataset(num_matches)

# Made with Bob
