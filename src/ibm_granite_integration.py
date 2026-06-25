"""
IBM Granite AI Integration Module

This module integrates IBM Granite AI for generating plain-English explanations
of football match predictions and statistics.
"""

import os
from typing import Dict, Any, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraniteExplainer:
    """
    Handles IBM Granite AI integration for generating natural language explanations
    """
    
    def __init__(self, api_key: Optional[str] = None, project_id: Optional[str] = None):
        """
        Initialize the Granite AI explainer
        
        Args:
            api_key: IBM Cloud API key (optional, will use env var if not provided)
            project_id: IBM watsonx.ai project ID (optional, will use env var if not provided)
        """
        self.api_key = api_key or os.getenv("IBM_CLOUD_API_KEY")
        self.project_id = project_id or os.getenv("IBM_WATSONX_PROJECT_ID")
        
        self.model = None
        self.is_initialized = False
        
        # Try to initialize the model
        self._initialize_model()
    
    def _initialize_model(self):
        """
        Initialize the IBM Granite model
        """
        if not self.api_key or not self.project_id:
            logger.warning("IBM credentials not found. Using fallback mode.")
            logger.warning("Set IBM_CLOUD_API_KEY and IBM_WATSONX_PROJECT_ID environment variables.")
            self.is_initialized = False
            return
        
        try:
            from ibm_watsonx_ai import Credentials
            from ibm_watsonx_ai.foundation_models import Model
            from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
            
            # Set up credentials
            credentials = Credentials(
                url="https://us-south.ml.cloud.ibm.com",
                api_key=self.api_key
            )
            
            # Initialize model
            self.model = Model(
                model_id="ibm/granite-13b-chat-v2",
                credentials=credentials,
                project_id=self.project_id,
                params={
                    GenParams.MAX_NEW_TOKENS: 200,
                    GenParams.TEMPERATURE: 0.7,
                    GenParams.TOP_P: 0.9,
                    GenParams.REPETITION_PENALTY: 1.1
                }
            )
            
            self.is_initialized = True
            logger.info("IBM Granite model initialized successfully")
            
        except ImportError:
            logger.error("ibm-watsonx-ai package not installed. Install with: pip install ibm-watsonx-ai")
            self.is_initialized = False
        except Exception as e:
            logger.error(f"Error initializing IBM Granite model: {e}")
            self.is_initialized = False
    
    def explain_prediction(self, prediction_data: Dict[str, Any]) -> str:
        """
        Generate a plain-English explanation of a match prediction
        
        Args:
            prediction_data: Dictionary containing:
                - home_team: str
                - away_team: str
                - prediction: str (e.g., "Home Win", "Draw", "Away Win")
                - confidence: float (0-100)
                - probabilities: dict with home_win, draw, away_win percentages
                - features: dict with team statistics
        
        Returns:
            Plain-English explanation string
        """
        if not self.is_initialized:
            return self._fallback_explanation(prediction_data)
        
        try:
            prompt = self._build_prediction_prompt(prediction_data)
            response = self.model.generate_text(prompt=prompt)
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return self._fallback_explanation(prediction_data)
    
    def explain_team_stats(self, team_name: str, stats: Dict[str, Any]) -> str:
        """
        Generate a plain-English explanation of team statistics
        
        Args:
            team_name: Name of the team
            stats: Dictionary with team statistics
        
        Returns:
            Plain-English explanation string
        """
        if not self.is_initialized:
            return self._fallback_team_stats(team_name, stats)
        
        try:
            prompt = self._build_stats_prompt(team_name, stats)
            response = self.model.generate_text(prompt=prompt)
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating stats explanation: {e}")
            return self._fallback_team_stats(team_name, stats)
    
    def explain_head_to_head(self, team1: str, team2: str, h2h_data: Dict[str, Any]) -> str:
        """
        Generate a plain-English explanation of head-to-head history
        
        Args:
            team1: First team name
            team2: Second team name
            h2h_data: Dictionary with head-to-head statistics
        
        Returns:
            Plain-English explanation string
        """
        if not self.is_initialized:
            return self._fallback_h2h(team1, team2, h2h_data)
        
        try:
            prompt = self._build_h2h_prompt(team1, team2, h2h_data)
            response = self.model.generate_text(prompt=prompt)
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating H2H explanation: {e}")
            return self._fallback_h2h(team1, team2, h2h_data)
    
    def _build_prediction_prompt(self, data: Dict[str, Any]) -> str:
        """Build prompt for match prediction explanation"""
        
        home_team = data.get('home_team', 'Home Team')
        away_team = data.get('away_team', 'Away Team')
        prediction = data.get('prediction', 'Unknown')
        confidence = data.get('confidence', 0)
        features = data.get('features', {})
        
        prompt = f"""You are a knowledgeable football analyst explaining match predictions to casual fans. 
Use simple language and focus on the key factors.

Match: {home_team} vs {away_team}
Prediction: {prediction}
Confidence: {confidence:.1f}%

Key Statistics:
- {home_team} recent form: {features.get('home_form', 0):.1%} win rate
- {away_team} recent form: {features.get('away_form', 0):.1%} win rate
- {home_team} goal difference: {features.get('home_goal_diff', 0):.2f} per match
- {away_team} goal difference: {features.get('away_goal_diff', 0):.2f} per match
- Head-to-head record: {features.get('h2h_record', 0.5):.1%} in favor of {home_team}

Task: Explain in 2-3 sentences why this prediction makes sense. Make it engaging and easy to understand for someone who doesn't follow football closely."""
        
        return prompt
    
    def _build_stats_prompt(self, team_name: str, stats: Dict[str, Any]) -> str:
        """Build prompt for team statistics explanation"""
        
        prompt = f"""You are a football analyst explaining team performance to casual fans.

Team: {team_name}

Statistics:
- Total matches: {stats.get('total_matches', 0)}
- Win rate: {stats.get('win_rate', 0):.1%}
- Goals per match: {stats.get('goals_per_match', 0):.2f}
- Recent form (last 10): {stats.get('recent_form', 0):.1%}

Task: Provide a 2-3 sentence summary of this team's performance. Highlight their strengths or weaknesses."""
        
        return prompt
    
    def _build_h2h_prompt(self, team1: str, team2: str, h2h_data: Dict[str, Any]) -> str:
        """Build prompt for head-to-head explanation"""
        
        prompt = f"""You are a football analyst explaining the rivalry between two teams.

Teams: {team1} vs {team2}

Head-to-Head Record:
- Total matches: {h2h_data.get('total_matches', 0)}
- {team1} wins: {h2h_data.get('team1_wins', 0)}
- {team2} wins: {h2h_data.get('team2_wins', 0)}
- Draws: {h2h_data.get('draws', 0)}
- Average goals per match: {h2h_data.get('avg_goals', 0):.2f}

Task: Describe this rivalry in 2-3 sentences. Make it interesting and highlight any patterns."""
        
        return prompt
    
    def _fallback_explanation(self, data: Dict[str, Any]) -> str:
        """Fallback explanation when IBM Granite is not available"""
        
        home_team = data.get('home_team', 'Home Team')
        away_team = data.get('away_team', 'Away Team')
        prediction = data.get('prediction', 'Unknown')
        confidence = data.get('confidence', 0)
        features = data.get('features', {})
        
        home_form = features.get('home_form', 0) * 100
        away_form = features.get('away_form', 0) * 100
        
        if prediction == "Home Win":
            return f"{home_team} is predicted to win with {confidence:.0f}% confidence. Their recent form ({home_form:.0f}% win rate) is stronger than {away_team}'s ({away_form:.0f}%), giving them a clear advantage in this matchup."
        elif prediction == "Away Win":
            return f"{away_team} is predicted to win with {confidence:.0f}% confidence. Despite playing away, their superior recent form ({away_form:.0f}% win rate) compared to {home_team} ({home_form:.0f}%) makes them favorites."
        else:
            return f"This match is predicted to end in a draw with {confidence:.0f}% confidence. Both teams have similar recent form ({home_team}: {home_form:.0f}%, {away_team}: {away_form:.0f}%), suggesting an evenly matched contest."
    
    def _fallback_team_stats(self, team_name: str, stats: Dict[str, Any]) -> str:
        """Fallback team stats explanation"""
        
        win_rate = stats.get('win_rate', 0) * 100
        goals = stats.get('goals_per_match', 0)
        
        if win_rate > 60:
            performance = "excellent"
        elif win_rate > 45:
            performance = "solid"
        else:
            performance = "struggling"
        
        return f"{team_name} has shown {performance} form with a {win_rate:.0f}% win rate. They average {goals:.1f} goals per match, demonstrating their {'attacking prowess' if goals > 2 else 'defensive approach'}."
    
    def _fallback_h2h(self, team1: str, team2: str, h2h_data: Dict[str, Any]) -> str:
        """Fallback head-to-head explanation"""
        
        total = h2h_data.get('total_matches', 0)
        team1_wins = h2h_data.get('team1_wins', 0)
        team2_wins = h2h_data.get('team2_wins', 0)
        
        if team1_wins > team2_wins:
            dominant = team1
            wins = team1_wins
        elif team2_wins > team1_wins:
            dominant = team2
            wins = team2_wins
        else:
            return f"{team1} and {team2} have a balanced rivalry with {total} matches played. Neither team has a clear historical advantage."
        
        return f"In their {total} previous encounters, {dominant} has dominated with {wins} victories. This historical advantage could play a psychological role in future matchups."


def test_granite_integration():
    """
    Test the IBM Granite integration with sample data
    """
    print("="*70)
    print("TESTING IBM GRANITE INTEGRATION")
    print("="*70)
    
    # Initialize explainer
    explainer = GraniteExplainer()
    
    print(f"\nInitialization Status: {'[OK] Success' if explainer.is_initialized else '[FALLBACK] Using Fallback Mode'}")
    
    # Test prediction explanation
    print("\n" + "-"*70)
    print("TEST 1: Match Prediction Explanation")
    print("-"*70)
    
    sample_prediction = {
        'home_team': 'Brazil',
        'away_team': 'Argentina',
        'prediction': 'Home Win',
        'confidence': 72.5,
        'probabilities': {
            'home_win': 72.5,
            'draw': 18.3,
            'away_win': 9.2
        },
        'features': {
            'home_form': 0.80,
            'away_form': 0.65,
            'home_goal_diff': 1.8,
            'away_goal_diff': 1.2,
            'h2h_record': 0.55
        }
    }
    
    explanation = explainer.explain_prediction(sample_prediction)
    print(f"\nExplanation:\n{explanation}")
    
    # Test team stats explanation
    print("\n" + "-"*70)
    print("TEST 2: Team Statistics Explanation")
    print("-"*70)
    
    sample_stats = {
        'total_matches': 150,
        'win_rate': 0.68,
        'goals_per_match': 2.3,
        'recent_form': 0.75
    }
    
    stats_explanation = explainer.explain_team_stats('Germany', sample_stats)
    print(f"\nExplanation:\n{stats_explanation}")
    
    # Test H2H explanation
    print("\n" + "-"*70)
    print("TEST 3: Head-to-Head Explanation")
    print("-"*70)
    
    sample_h2h = {
        'total_matches': 25,
        'team1_wins': 12,
        'team2_wins': 8,
        'draws': 5,
        'avg_goals': 2.8
    }
    
    h2h_explanation = explainer.explain_head_to_head('France', 'England', sample_h2h)
    print(f"\nExplanation:\n{h2h_explanation}")
    
    print("\n" + "="*70)
    print("[OK] IBM Granite integration test complete!")
    print("="*70)


if __name__ == "__main__":
    test_granite_integration()

# Made with Bob
