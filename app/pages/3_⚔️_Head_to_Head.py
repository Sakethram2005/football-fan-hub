"""
Head-to-Head Analysis - Historical Matchup Analysis
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import plotly.graph_objects as go
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.data_preprocessing import load_and_preprocess_data

# Page config
st.set_page_config(
    page_title="Head-to-Head Analysis",
    page_icon="⚔️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .h2h-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    .team-stat {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .match-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load and cache the dataset"""
    try:
        df = load_and_preprocess_data()
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def get_h2h_matches(df, team1, team2):
    """Get all matches between two teams"""
    matches = df[
        ((df['home_team'] == team1) & (df['away_team'] == team2)) |
        ((df['home_team'] == team2) & (df['away_team'] == team1))
    ].copy()
    
    return matches.sort_values('date', ascending=False)

def calculate_h2h_stats(matches, team1, team2):
    """Calculate head-to-head statistics"""
    
    if len(matches) == 0:
        return None
    
    # Team 1 perspective
    team1_home = matches[matches['home_team'] == team1]
    team1_away = matches[matches['away_team'] == team1]
    
    # Wins for team1
    team1_home_wins = len(team1_home[team1_home['home_score'] > team1_home['away_score']])
    team1_away_wins = len(team1_away[team1_away['away_score'] > team1_away['home_score']])
    team1_wins = team1_home_wins + team1_away_wins
    
    # Wins for team2
    team2_home_wins = len(team1_away[team1_away['home_score'] > team1_away['away_score']])
    team2_away_wins = len(team1_home[team1_home['away_score'] > team1_home['home_score']])
    team2_wins = team2_home_wins + team2_away_wins
    
    # Draws
    team1_home_draws = len(team1_home[team1_home['home_score'] == team1_home['away_score']])
    team1_away_draws = len(team1_away[team1_away['away_score'] == team1_away['home_score']])
    draws = team1_home_draws + team1_away_draws
    
    # Goals
    team1_goals = (team1_home['home_score'].sum() + team1_away['away_score'].sum())
    team2_goals = (team1_home['away_score'].sum() + team1_away['home_score'].sum())
    
    # Recent form (last 5 matches)
    recent_matches = matches.head(5)
    recent_form = []
    for _, match in recent_matches.iterrows():
        if match['home_team'] == team1:
            if match['home_score'] > match['away_score']:
                recent_form.append('W')
            elif match['home_score'] < match['away_score']:
                recent_form.append('L')
            else:
                recent_form.append('D')
        else:
            if match['away_score'] > match['home_score']:
                recent_form.append('W')
            elif match['away_score'] < match['home_score']:
                recent_form.append('L')
            else:
                recent_form.append('D')
    
    # Biggest wins
    team1_biggest_win = 0
    team2_biggest_win = 0
    
    for _, match in matches.iterrows():
        if match['home_team'] == team1:
            diff = match['home_score'] - match['away_score']
            if diff > team1_biggest_win:
                team1_biggest_win = diff
        else:
            diff = match['away_score'] - match['home_score']
            if diff > team1_biggest_win:
                team1_biggest_win = diff
    
    for _, match in matches.iterrows():
        if match['home_team'] == team2:
            diff = match['home_score'] - match['away_score']
            if diff > team2_biggest_win:
                team2_biggest_win = diff
        else:
            diff = match['away_score'] - match['home_score']
            if diff > team2_biggest_win:
                team2_biggest_win = diff
    
    return {
        'total_matches': len(matches),
        'team1_wins': team1_wins,
        'team2_wins': team2_wins,
        'draws': draws,
        'team1_goals': int(team1_goals),
        'team2_goals': int(team2_goals),
        'recent_form': recent_form,
        'team1_biggest_win': int(team1_biggest_win),
        'team2_biggest_win': int(team2_biggest_win),
        'first_meeting': matches.iloc[-1]['date'],
        'last_meeting': matches.iloc[0]['date']
    }

def main():
    st.title("⚔️ Head-to-Head Analysis")
    st.markdown("### Historical Matchup Analysis Between Teams")
    
    # Load data
    df = load_data()
    
    if df is None:
        st.error("Failed to load data. Please check the dataset.")
        return
    
    # Get available teams
    teams = sorted(set(df['home_team'].unique()) | set(df['away_team'].unique()))
    
    st.markdown("---")
    
    # Team selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏠 Team 1")
        team1 = st.selectbox(
            "Select first team",
            teams,
            index=teams.index("Brazil") if "Brazil" in teams else 0,
            key="team1"
        )
    
    with col2:
        st.markdown("### ✈️ Team 2")
        team2 = st.selectbox(
            "Select second team",
            teams,
            index=teams.index("Argentina") if "Argentina" in teams else 1,
            key="team2"
        )
    
    if st.button("⚔️ Analyze Head-to-Head", type="primary", use_container_width=True):
        if team1 == team2:
            st.error("⚠️ Please select two different teams!")
        else:
            with st.spinner(f"Analyzing {team1} vs {team2} history..."):
                # Get matches
                matches = get_h2h_matches(df, team1, team2)
                
                if len(matches) == 0:
                    st.warning(f"No matches found between {team1} and {team2} in the dataset.")
                else:
                    # Calculate statistics
                    stats = calculate_h2h_stats(matches, team1, team2)
                    
                    st.markdown("---")
                    st.markdown(f"## ⚔️ {team1} vs {team2}")
                    
                    # Overall record card
                    st.markdown(f"""
                    <div class="h2h-card">
                        <h2>Overall Head-to-Head Record</h2>
                        <h3>{stats['total_matches']} Matches Played</h3>
                        <p>First Meeting: {stats['first_meeting'].strftime('%Y-%m-%d')} | 
                           Last Meeting: {stats['last_meeting'].strftime('%Y-%m-%d')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Win/Draw/Loss statistics
                    st.markdown("### 📊 Match Results")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="team-stat">
                            <h2 style="color: #2ca02c;">{stats['team1_wins']}</h2>
                            <p><strong>{team1} Wins</strong></p>
                            <p>{stats['team1_wins']/stats['total_matches']*100:.1f}%</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="team-stat">
                            <h2 style="color: #ff7f0e;">{stats['draws']}</h2>
                            <p><strong>Draws</strong></p>
                            <p>{stats['draws']/stats['total_matches']*100:.1f}%</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"""
                        <div class="team-stat">
                            <h2 style="color: #d62728;">{stats['team2_wins']}</h2>
                            <p><strong>{team2} Wins</strong></p>
                            <p>{stats['team2_wins']/stats['total_matches']*100:.1f}%</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Visual representation
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Pie chart
                        fig = go.Figure(data=[go.Pie(
                            labels=[f'{team1} Wins', 'Draws', f'{team2} Wins'],
                            values=[stats['team1_wins'], stats['draws'], stats['team2_wins']],
                            marker_colors=['#2ca02c', '#ff7f0e', '#d62728'],
                            hole=0.4
                        )])
                        
                        fig.update_layout(
                            title="Match Results Distribution",
                            height=400
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Goals comparison
                        fig = go.Figure(data=[
                            go.Bar(
                                x=[team1, team2],
                                y=[stats['team1_goals'], stats['team2_goals']],
                                marker_color=['#1f77b4', '#ff7f0e'],
                                text=[stats['team1_goals'], stats['team2_goals']],
                                textposition='auto'
                            )
                        ])
                        
                        fig.update_layout(
                            title="Total Goals Scored",
                            yaxis_title="Goals",
                            height=400,
                            showlegend=False
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Additional statistics
                    st.markdown("### 📈 Additional Statistics")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(f"{team1} Goals", stats['team1_goals'])
                        st.metric(f"{team1} Biggest Win", f"+{stats['team1_biggest_win']}")
                    
                    with col2:
                        avg_goals = (stats['team1_goals'] + stats['team2_goals']) / stats['total_matches']
                        st.metric("Avg Goals/Match", f"{avg_goals:.2f}")
                        st.metric("Total Matches", stats['total_matches'])
                    
                    with col3:
                        st.metric(f"{team2} Goals", stats['team2_goals'])
                        st.metric(f"{team2} Biggest Win", f"+{stats['team2_biggest_win']}")
                    
                    # Recent form
                    st.markdown(f"### 📅 Recent Form ({team1} perspective)")
                    
                    form_colors = {'W': '🟢', 'D': '🟡', 'L': '🔴'}
                    form_string = ' '.join([form_colors[result] for result in stats['recent_form']])
                    
                    st.markdown(f"**Last {len(stats['recent_form'])} matches:** {form_string}")
                    st.caption("🟢 Win | 🟡 Draw | 🔴 Loss")
                    
                    # Match history
                    st.markdown("### 📜 Complete Match History")
                    
                    # Prepare match history dataframe
                    match_history = []
                    for _, match in matches.iterrows():
                        if match['home_team'] == team1:
                            result = '🟢 W' if match['home_score'] > match['away_score'] else '🔴 L' if match['home_score'] < match['away_score'] else '🟡 D'
                            score = f"{int(match['home_score'])} - {int(match['away_score'])}"
                        else:
                            result = '🟢 W' if match['away_score'] > match['home_score'] else '🔴 L' if match['away_score'] < match['home_score'] else '🟡 D'
                            score = f"{int(match['away_score'])} - {int(match['home_score'])}"
                        
                        match_history.append({
                            'Date': match['date'].strftime('%Y-%m-%d'),
                            'Home': match['home_team'],
                            'Score': score,
                            'Away': match['away_team'],
                            'Result': result,
                            'Tournament': match['tournament'],
                            'Venue': f"{match['city']}, {match['country']}"
                        })
                    
                    history_df = pd.DataFrame(match_history)
                    
                    # Display with pagination
                    st.dataframe(history_df, use_container_width=True, hide_index=True)
                    
                    # Timeline visualization
                    st.markdown("### 📈 Results Timeline")
                    
                    # Prepare timeline data
                    timeline_data = []
                    for _, match in matches.iterrows():
                        if match['home_team'] == team1:
                            if match['home_score'] > match['away_score']:
                                result = 1  # Win
                            elif match['home_score'] < match['away_score']:
                                result = -1  # Loss
                            else:
                                result = 0  # Draw
                        else:
                            if match['away_score'] > match['home_score']:
                                result = 1  # Win
                            elif match['away_score'] < match['home_score']:
                                result = -1  # Loss
                            else:
                                result = 0  # Draw
                        
                        timeline_data.append({
                            'date': match['date'],
                            'result': result
                        })
                    
                    timeline_df = pd.DataFrame(timeline_data).sort_values('date')
                    
                    fig = go.Figure()
                    
                    colors = ['#2ca02c' if r == 1 else '#d62728' if r == -1 else '#ff7f0e' 
                             for r in timeline_df['result']]
                    
                    fig.add_trace(go.Scatter(
                        x=timeline_df['date'],
                        y=timeline_df['result'],
                        mode='markers+lines',
                        marker=dict(size=10, color=colors),
                        line=dict(color='gray', width=1),
                        name='Results'
                    ))
                    
                    fig.update_layout(
                        title=f"{team1} vs {team2} - Results Over Time",
                        xaxis_title="Date",
                        yaxis_title="Result",
                        yaxis=dict(
                            tickmode='array',
                            tickvals=[-1, 0, 1],
                            ticktext=['Loss', 'Draw', 'Win']
                        ),
                        height=400,
                        hovermode='x unified'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Download report
                    st.markdown("---")
                    
                    report = f"""
HEAD-TO-HEAD ANALYSIS REPORT
{team1} vs {team2}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

OVERALL RECORD
Total Matches: {stats['total_matches']}
First Meeting: {stats['first_meeting'].strftime('%Y-%m-%d')}
Last Meeting: {stats['last_meeting'].strftime('%Y-%m-%d')}

RESULTS
{team1} Wins: {stats['team1_wins']} ({stats['team1_wins']/stats['total_matches']*100:.1f}%)
Draws: {stats['draws']} ({stats['draws']/stats['total_matches']*100:.1f}%)
{team2} Wins: {stats['team2_wins']} ({stats['team2_wins']/stats['total_matches']*100:.1f}%)

GOALS
{team1}: {stats['team1_goals']} goals
{team2}: {stats['team2_goals']} goals
Average per match: {(stats['team1_goals'] + stats['team2_goals'])/stats['total_matches']:.2f}

BIGGEST WINS
{team1}: +{stats['team1_biggest_win']} goals
{team2}: +{stats['team2_biggest_win']} goals

RECENT FORM ({team1} perspective)
{' '.join(stats['recent_form'])}

---
World Cup Fan Intelligence Hub
Powered by IBM watsonx.ai
"""
                    
                    st.download_button(
                        label="📥 Download H2H Report",
                        data=report,
                        file_name=f"h2h_{team1}_vs_{team2}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
    
    # Information
    st.markdown("---")
    st.markdown("### ℹ️ About Head-to-Head Analysis")
    
    with st.expander("What does this analysis show?"):
        st.markdown("""
        Our head-to-head analysis provides:
        
        **Match Results:**
        - Complete win/draw/loss record
        - Percentage breakdown
        - Visual distribution
        
        **Goal Statistics:**
        - Total goals scored by each team
        - Average goals per match
        - Biggest winning margins
        
        **Historical Context:**
        - First and last meeting dates
        - Complete match history with scores
        - Tournament information
        - Venue details
        
        **Trends:**
        - Recent form (last 5 matches)
        - Results timeline visualization
        - Performance patterns over time
        
        This analysis uses the complete dataset of international matches to provide 
        comprehensive insights into the historical rivalry between any two teams.
        """)

if __name__ == "__main__":
    main()

# Made with Bob
