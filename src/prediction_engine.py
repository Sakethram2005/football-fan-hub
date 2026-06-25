"""
Prediction Engine

Combines ML model predictions with IBM Granite AI explanations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
import logging
from pathlib import Path

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.feature_engineering import FeatureEngineer
from src.model_training import MatchPredictor
from src.ibm_granite_integration import GraniteExplainer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FootballPredictionEngine:
    """
    Complete prediction engine with ML model and AI explanations
    """
    
    def __init__(self, data_path: str = 'data/processed/matches_filtered.csv'):
        """
        Initialize the prediction engine
        
        Args:
            data_path: Path to historical match data
        """
        logger.info("Initializing Football Prediction Engine...")
        
        # Load historical data
        self.df = pd.read_csv(data_path, parse_dates=['date'])
        logger.info(f"Loaded {len(self.df)} historical matches")
        
        # Initialize components
        self.feature_engineer = FeatureEngineer(self.df)
        self.predictor = MatchPredictor()
        self.explainer = GraniteExplainer()
        
        # Load trained model
        try:
            self.predictor.load()
            logger.info("Loaded trained model successfully")
        except Exception as e:
            logger.warning(f"Could not load model: {e}")
            logger.warning("Model needs to be trained first")
    
    def predict_match(self, home_team: str, away_team: str, 
                     match_date: str = None, is_neutral: bool = False) -> Dict[str, Any]:
        """
        Predict match outcome with AI explanation
        
        Args:
            home_team: Home team name
            away_team: Away team name
            match_date: Match date (YYYY-MM-DD), defaults to today
            is_neutral: Whether it's a neutral venue
            
        Returns:
            Dictionary with prediction, probabilities, and explanation
        """
        # Parse date
        if match_date is None:
            match_date = pd.Timestamp.now()
        else:
            match_date = pd.to_datetime(match_date)
        
        logger.info(f"\nPredicting: {home_team} vs {away_team} on {match_date.date()}")
        
        # Create features
        features = self.feature_engineer.create_features_for_match(
            home_team, away_team, match_date, is_neutral
        )
        
        # Convert to DataFrame
        X = pd.DataFrame([features])
        
        # Get prediction
        prediction_label = self.predictor.predict(X)[0]
        probabilities = self.predictor.predict_proba(X)[0]
        
        # Map label to outcome
        outcome_map = {0: 'Away Win', 1: 'Draw', 2: 'Home Win'}
        predicted_outcome = outcome_map[prediction_label]
        confidence = probabilities[prediction_label] * 100
        
        # Prepare result
        result = {
            'home_team': home_team,
            'away_team': away_team,
            'match_date': match_date.strftime('%Y-%m-%d'),
            'prediction': predicted_outcome,
            'confidence': float(confidence),
            'probabilities': {
                'home_win': float(probabilities[2] * 100),
                'draw': float(probabilities[1] * 100),
                'away_win': float(probabilities[0] * 100)
            },
            'features': features
        }
        
        # Generate AI explanation
        try:
            explanation = self.explainer.explain_prediction(result)
            result['explanation'] = explanation
        except Exception as e:
            logger.warning(f"Could not generate AI explanation: {e}")
            result['explanation'] = self._fallback_explanation(result)
        
        return result
    
    def _fallback_explanation(self, result: Dict[str, Any]) -> str:
        """Generate fallback explanation if AI fails"""
        home = result['home_team']
        away = result['away_team']
        pred = result['prediction']
        conf = result['confidence']
        features = result['features']
        
        home_form = features['home_form'] * 100
        away_form = features['away_form'] * 100
        
        if pred == "Home Win":
            return f"{home} is predicted to win with {conf:.0f}% confidence. Their recent form ({home_form:.0f}% win rate) is stronger than {away}'s ({away_form:.0f}%), giving them a clear advantage."
        elif pred == "Away Win":
            return f"{away} is predicted to win with {conf:.0f}% confidence. Despite playing away, their superior form ({away_form:.0f}% vs {home_form:.0f}%) makes them favorites."
        else:
            return f"This match is predicted to end in a draw with {conf:.0f}% confidence. Both teams have similar form ({home}: {home_form:.0f}%, {away}: {away_form:.0f}%)."
    
    def get_team_list(self) -> list:
        """
        Get list of all teams in the dataset
        
        Returns:
            Sorted list of team names
        """
        teams = set(self.df['home_team'].unique()) | set(self.df['away_team'].unique())
        return sorted(list(teams))


def main():
    """
    Test the prediction engine
    """
    print("="*70)
    print("FOOTBALL PREDICTION ENGINE TEST")
    print("="*70)
    
    # Initialize engine
    engine = FootballPredictionEngine()
    
    # Test predictions
    test_matches = [
        ('Brazil', 'Argentina', '2026-07-01', False),
        ('Germany', 'France', '2026-07-05', True),
        ('England', 'Spain', '2026-07-10', False),
    ]
    
    for home, away, date, neutral in test_matches:
        print("\n" + "="*70)
        result = engine.predict_match(home, away, date, neutral)
        
        print(f"\nMatch: {result['home_team']} vs {result['away_team']}")
        print(f"Date: {result['match_date']}")
        print(f"Venue: {'Neutral' if neutral else 'Home'}")
        print(f"\nPrediction: {result['prediction']}")
        print(f"Confidence: {result['confidence']:.1f}%")
        print(f"\nProbabilities:")
        print(f"  {result['home_team']} Win: {result['probabilities']['home_win']:.1f}%")
        print(f"  Draw: {result['probabilities']['draw']:.1f}%")
        print(f"  {result['away_team']} Win: {result['probabilities']['away_win']:.1f}%")
        print(f"\nExplanation:")
        print(f"{result['explanation']}")
    
    print("\n" + "="*70)
    print("[OK] Prediction engine test complete!")
    print("="*70)


if __name__ == "__main__":
    main()

# Made with Bob
