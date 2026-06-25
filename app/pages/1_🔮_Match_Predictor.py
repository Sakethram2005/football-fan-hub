"""
Match Predictor Page - AI-Powered Match Outcome Predictions
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.prediction_engine import FootballPredictionEngine

# Page config
st.set_page_config(
    page_title="Match Predictor",
    page_icon="🔮",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    .prediction-result {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .confidence-score {
        font-size: 1.5rem;
        margin: 0.5rem 0;
    }
    .explanation-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .feature-importance {
        background-color: #fff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'prediction_engine' not in st.session_state:
    st.session_state.prediction_engine = None
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None

# Load prediction engine
@st.cache_resource
def load_prediction_engine():
    """Load the prediction engine (cached)"""
    try:
        engine = FootballPredictionEngine()
        return engine
    except Exception as e:
        st.error(f"Error loading prediction engine: {str(e)}")
        return None

# Main page
def main():
    st.title("🔮 Match Outcome Predictor")
    st.markdown("### AI-Powered Predictions with IBM watsonx.ai Explanations")
    
    # Load engine
    if st.session_state.prediction_engine is None:
        with st.spinner("Loading prediction engine..."):
            st.session_state.prediction_engine = load_prediction_engine()
    
    engine = st.session_state.prediction_engine
    
    if engine is None:
        st.error("Failed to load prediction engine. Please check the setup.")
        return
    
    # Get available teams
    teams = sorted(engine.feature_engineer.df['home_team'].unique().tolist())
    
    st.markdown("---")
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏠 Home Team")
        home_team = st.selectbox(
            "Select home team",
            teams,
            index=teams.index("Brazil") if "Brazil" in teams else 0,
            key="home_team"
        )
    
    with col2:
        st.markdown("### ✈️ Away Team")
        away_team = st.selectbox(
            "Select away team",
            teams,
            index=teams.index("Argentina") if "Argentina" in teams else 1,
            key="away_team"
        )
    
    # Additional options
    col1, col2 = st.columns(2)
    
    with col1:
        match_date = st.date_input(
            "Match Date",
            value=datetime.now(),
            help="Date of the match (affects temporal features)"
        )
    
    with col2:
        is_neutral = st.checkbox(
            "Neutral Venue",
            value=False,
            help="Check if match is at a neutral venue (e.g., World Cup)"
        )
    
    st.markdown("---")
    
    # Predict button
    if st.button("🎯 Predict Match Outcome", type="primary", use_container_width=True):
        if home_team == away_team:
            st.error("⚠️ Please select different teams for home and away!")
        else:
            with st.spinner("🤖 Analyzing match data and generating prediction..."):
                try:
                    # Get prediction
                    result = engine.predict_match(
                        home_team=home_team,
                        away_team=away_team,
                        match_date=match_date.strftime("%Y-%m-%d"),
                        is_neutral=is_neutral
                    )
                    st.session_state.prediction_result = result
                    
                except Exception as e:
                    st.error(f"Error making prediction: {str(e)}")
                    st.exception(e)
    
    # Display results
    if st.session_state.prediction_result:
        result = st.session_state.prediction_result
        
        st.markdown("---")
        st.markdown("## 📊 Prediction Results")
        
        # Main prediction card
        prediction_emoji = {
            "Home Win": "🏠",
            "Draw": "🤝",
            "Away Win": "✈️"
        }
        
        st.markdown(f"""
        <div class="prediction-card">
            <h2>{prediction_emoji.get(result['prediction'], '⚽')} Predicted Outcome</h2>
            <div class="prediction-result">{result['prediction']}</div>
            <div class="confidence-score">Confidence: {result['confidence']:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Probability distribution
        st.markdown("### 📈 Win Probability Distribution")
        
        probabilities = result['probabilities']
        
        # Create probability chart
        fig = go.Figure(data=[
            go.Bar(
                x=['Home Win', 'Draw', 'Away Win'],
                y=[probabilities['home_win'], probabilities['draw'], probabilities['away_win']],
                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'],
                text=[f"{probabilities['home_win']:.1f}%", 
                      f"{probabilities['draw']:.1f}%", 
                      f"{probabilities['away_win']:.1f}%"],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title=f"{home_team} vs {away_team} - Outcome Probabilities",
            xaxis_title="Outcome",
            yaxis_title="Probability (%)",
            yaxis_range=[0, 100],
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # AI Explanation
        st.markdown("### 🤖 AI-Powered Explanation")
        st.markdown("**Powered by IBM watsonx.ai (Llama 3.3 70B)**")
        
        if result.get('explanation'):
            st.markdown(f"""
            <div class="explanation-box">
                {result['explanation']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("AI explanation not available for this prediction.")
        
        # Feature values
        st.markdown("### 🔍 Key Features Used in Prediction")
        
        features = result.get('features', {})
        
        if features:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Home Team Form", f"{features.get('home_form', 0):.2f}")
                st.metric("Home Goal Difference", f"{features.get('home_goal_diff', 0):.2f}")
                st.metric("Home Goals/Match", f"{features.get('home_goals_scored_rate', 0):.2f}")
            
            with col2:
                st.metric("Away Team Form", f"{features.get('away_form', 0):.2f}")
                st.metric("Away Goal Difference", f"{features.get('away_goal_diff', 0):.2f}")
                st.metric("Away Goals/Match", f"{features.get('away_goals_scored_rate', 0):.2f}")
            
            with col3:
                st.metric("Head-to-Head Record", f"{features.get('h2h_record', 0):.2f}")
                st.metric("Home Advantage", f"{features.get('home_advantage', 0):.2f}")
                st.metric("Neutral Venue", "Yes" if features.get('is_neutral', 0) == 1 else "No")
        
        # Download results
        st.markdown("---")
        
        # Create downloadable report
        report = f"""
MATCH PREDICTION REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

MATCH DETAILS
Home Team: {home_team}
Away Team: {away_team}
Date: {match_date}
Neutral Venue: {"Yes" if is_neutral else "No"}

PREDICTION
Outcome: {result['prediction']}
Confidence: {result['confidence']:.1f}%

PROBABILITIES
Home Win: {probabilities['home_win']:.1f}%
Draw: {probabilities['draw']:.1f}%
Away Win: {probabilities['away_win']:.1f}%

AI EXPLANATION
{result.get('explanation', 'Not available')}

---
Powered by IBM watsonx.ai & RandomForest ML
World Cup Fan Intelligence Hub
"""
        
        st.download_button(
            label="📥 Download Prediction Report",
            data=report,
            file_name=f"prediction_{home_team}_vs_{away_team}_{match_date}.txt",
            mime="text/plain"
        )
    
    # Information section
    st.markdown("---")
    st.markdown("### ℹ️ About the Prediction Model")
    
    with st.expander("How does the prediction work?"):
        st.markdown("""
        Our prediction system combines **machine learning** with **AI explanations**:
        
        **1. Feature Engineering (13 Features)**
        - Team form (last 5 matches)
        - Goal difference trends
        - Head-to-head historical record
        - Home advantage factor
        - Goals scored/conceded rates
        - Temporal features (year, month)
        
        **2. RandomForest ML Model**
        - Trained on 25,268 matches (1990-2026)
        - 200 decision trees
        - 55% accuracy on test set
        - Balanced for 3-class prediction (Win/Draw/Loss)
        
        **3. IBM watsonx.ai Explanations**
        - Llama 3.3 70B model
        - Plain-English explanations
        - Context-aware analysis
        - Real-time generation
        
        **Note:** Football is inherently unpredictable! Our model provides data-driven insights 
        but cannot account for all factors (injuries, weather, tactics, etc.).
        """)
    
    with st.expander("Model Performance Metrics"):
        st.markdown("""
        **Overall Accuracy:** 55.0%
        
        **Class-wise Performance:**
        - Home Win: Precision 0.58, Recall 0.60
        - Draw: Precision 0.48, Recall 0.44
        - Away Win: Precision 0.57, Recall 0.59
        
        **Cross-Validation:** 55.35% (±1.2%)
        
        **Training Data:** 25,268 matches from 1990-2026
        **Test Data:** 6,318 matches (20% holdout)
        """)

if __name__ == "__main__":
    main()

# Made with Bob
