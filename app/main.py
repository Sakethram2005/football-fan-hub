"""
World Cup Fan Intelligence Hub - Main Streamlit Application
IBM SkillsBuild AI Builders Challenge - June 2026
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Page configuration
st.set_page_config(
    page_title="World Cup Fan Intelligence Hub",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #145a8c;
    }
    </style>
""", unsafe_allow_html=True)

# Main page content
def main():
    # Header
    st.markdown('<div class="main-header">⚽ World Cup Fan Intelligence Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Match Predictions & Football Analytics</div>', unsafe_allow_html=True)
    
    # IBM Badge
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("🏆 **IBM SkillsBuild AI Builders Challenge - June 2026**\n\n"
                "Powered by IBM watsonx.ai (Llama 3.3 70B) & RandomForest ML")
    
    st.markdown("---")
    
    # Introduction
    st.markdown("""
    ### Welcome to the Future of Football Analytics! 🌍
    
    This AI-powered platform combines **machine learning predictions** with **IBM watsonx.ai explanations** 
    to give you instant insights into any World Cup matchup.
    
    **Built with:**
    - 🤖 **IBM watsonx.ai** - Llama 3.3 70B model for plain-English explanations
    - 📊 **RandomForest ML** - Trained on 49,329 international matches (1872-2026)
    - 🎯 **13 Advanced Features** - Team form, goal difference, H2H records, and more
    """)
    
    st.markdown("---")
    
    # Features overview
    st.markdown("### 🎯 Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔮 Match Predictor</h3>
            <p>Get AI-powered predictions for any World Cup matchup with confidence scores and detailed explanations.</p>
            <ul>
                <li>RandomForest ML model (55% accuracy)</li>
                <li>13 engineered features</li>
                <li>IBM watsonx.ai explanations</li>
                <li>Win/Draw/Loss probabilities</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Team Statistics</h3>
            <p>Comprehensive analytics for any national team with interactive visualizations.</p>
            <ul>
                <li>Overall win/draw/loss record</li>
                <li>Goals scored & conceded</li>
                <li>Home vs Away performance</li>
                <li>Tournament history</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>⚔️ Head-to-Head</h3>
            <p>Deep dive into historical matchups between any two teams.</p>
            <ul>
                <li>Complete match history</li>
                <li>Win/loss records</li>
                <li>Goal statistics</li>
                <li>Recent form trends</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Dataset info
    st.markdown("### 📚 Dataset Information")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>49,329</h2>
            <p>Total Matches</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>154 Years</h2>
            <p>1872 - 2026</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>200+</h2>
            <p>National Teams</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2>55%</h2>
            <p>Model Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # How to use
    st.markdown("### 🚀 How to Use")
    
    st.markdown("""
    1. **Navigate** using the sidebar to choose a feature
    2. **Select teams** from the dropdown menus
    3. **Get predictions** with AI-powered explanations
    4. **Explore statistics** and historical data
    5. **Compare teams** head-to-head
    
    👈 **Start by selecting a page from the sidebar!**
    """)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p><strong>World Cup Fan Intelligence Hub</strong></p>
        <p>Built for IBM SkillsBuild AI Builders Challenge - June 2026</p>
        <p>Powered by IBM watsonx.ai | RandomForest ML | Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

# Made with Bob
