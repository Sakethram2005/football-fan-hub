"""
Team Statistics Dashboard - Comprehensive Team Analytics
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.data_preprocessing import load_and_preprocess_data

# Page config
st.set_page_config(
    page_title="Team Statistics",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
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

def calculate_team_stats(df, team_name):
    """Calculate comprehensive statistics for a team"""
    
    # Filter matches involving the team
    home_matches = df[df['home_team'] == team_name].copy()
    away_matches = df[df['away_team'] == team_name].copy()
    
    # Overall statistics
    total_matches = len(home_matches) + len(away_matches)
    
    # Home statistics
    home_wins = len(home_matches[home_matches['home_score'] > home_matches['away_score']])
    home_draws = len(home_matches[home_matches['home_score'] == home_matches['away_score']])
    home_losses = len(home_matches[home_matches['home_score'] < home_matches['away_score']])
    home_goals_scored = home_matches['home_score'].sum()
    home_goals_conceded = home_matches['away_score'].sum()
    
    # Away statistics
    away_wins = len(away_matches[away_matches['away_score'] > away_matches['home_score']])
    away_draws = len(away_matches[away_matches['away_score'] == away_matches['home_score']])
    away_losses = len(away_matches[away_matches['away_score'] < away_matches['home_score']])
    away_goals_scored = away_matches['away_score'].sum()
    away_goals_conceded = away_matches['home_score'].sum()
    
    # Overall totals
    total_wins = home_wins + away_wins
    total_draws = home_draws + away_draws
    total_losses = home_losses + away_losses
    total_goals_scored = home_goals_scored + away_goals_scored
    total_goals_conceded = home_goals_conceded + away_goals_conceded
    
    # Win percentage
    win_percentage = (total_wins / total_matches * 100) if total_matches > 0 else 0
    
    # Goal difference
    goal_difference = total_goals_scored - total_goals_conceded
    
    # Average goals per match
    avg_goals_scored = total_goals_scored / total_matches if total_matches > 0 else 0
    avg_goals_conceded = total_goals_conceded / total_matches if total_matches > 0 else 0
    
    # Recent form (last 10 matches)
    all_matches = pd.concat([
        home_matches.assign(team_score=home_matches['home_score'], 
                           opponent_score=home_matches['away_score'],
                           opponent=home_matches['away_team'],
                           venue='Home'),
        away_matches.assign(team_score=away_matches['away_score'], 
                           opponent_score=away_matches['home_score'],
                           opponent=away_matches['home_team'],
                           venue='Away')
    ]).sort_values('date', ascending=False)
    
    recent_matches = all_matches.head(10)
    
    # Tournament statistics
    tournament_stats = all_matches.groupby('tournament').size().sort_values(ascending=False)
    
    return {
        'total_matches': total_matches,
        'wins': total_wins,
        'draws': total_draws,
        'losses': total_losses,
        'win_percentage': win_percentage,
        'goals_scored': int(total_goals_scored),
        'goals_conceded': int(total_goals_conceded),
        'goal_difference': int(goal_difference),
        'avg_goals_scored': avg_goals_scored,
        'avg_goals_conceded': avg_goals_conceded,
        'home_record': {'wins': home_wins, 'draws': home_draws, 'losses': home_losses},
        'away_record': {'wins': away_wins, 'draws': away_draws, 'losses': away_losses},
        'recent_matches': recent_matches,
        'tournament_stats': tournament_stats,
        'all_matches': all_matches
    }

def main():
    st.title("📊 Team Statistics Dashboard")
    st.markdown("### Comprehensive Analytics for National Teams")
    
    # Load data
    df = load_data()
    
    if df is None:
        st.error("Failed to load data. Please check the dataset.")
        return
    
    # Get available teams
    teams = sorted(set(df['home_team'].unique()) | set(df['away_team'].unique()))
    
    st.markdown("---")
    
    # Team selection
    selected_team = st.selectbox(
        "🏆 Select a National Team",
        teams,
        index=teams.index("Brazil") if "Brazil" in teams else 0
    )
    
    if st.button("📈 Analyze Team", type="primary", use_container_width=True):
        with st.spinner(f"Analyzing {selected_team} statistics..."):
            stats = calculate_team_stats(df, selected_team)
            
            st.markdown("---")
            st.markdown(f"## 🏆 {selected_team} - Complete Statistics")
            
            # Key metrics
            st.markdown("### 📈 Key Performance Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{stats['total_matches']}</div>
                    <div class="stat-label">Total Matches</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{stats['win_percentage']:.1f}%</div>
                    <div class="stat-label">Win Rate</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{stats['goal_difference']:+d}</div>
                    <div class="stat-label">Goal Difference</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{stats['avg_goals_scored']:.2f}</div>
                    <div class="stat-label">Goals/Match</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Win/Draw/Loss record
            st.markdown("### 🎯 Overall Record")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart for W/D/L
                fig = go.Figure(data=[go.Pie(
                    labels=['Wins', 'Draws', 'Losses'],
                    values=[stats['wins'], stats['draws'], stats['losses']],
                    marker_colors=['#2ca02c', '#ff7f0e', '#d62728'],
                    hole=0.4
                )])
                
                fig.update_layout(
                    title=f"{selected_team} - Match Results Distribution",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Bar chart for goals
                fig = go.Figure(data=[
                    go.Bar(name='Goals Scored', x=['Total'], y=[stats['goals_scored']], marker_color='#2ca02c'),
                    go.Bar(name='Goals Conceded', x=['Total'], y=[stats['goals_conceded']], marker_color='#d62728')
                ])
                
                fig.update_layout(
                    title=f"{selected_team} - Goals Statistics",
                    yaxis_title="Goals",
                    height=400,
                    barmode='group'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Home vs Away performance
            st.markdown("### 🏠 Home vs ✈️ Away Performance")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏠 Home Record")
                home = stats['home_record']
                st.metric("Wins", home['wins'])
                st.metric("Draws", home['draws'])
                st.metric("Losses", home['losses'])
                home_total = home['wins'] + home['draws'] + home['losses']
                home_win_pct = (home['wins'] / home_total * 100) if home_total > 0 else 0
                st.metric("Win Rate", f"{home_win_pct:.1f}%")
            
            with col2:
                st.markdown("#### ✈️ Away Record")
                away = stats['away_record']
                st.metric("Wins", away['wins'])
                st.metric("Draws", away['draws'])
                st.metric("Losses", away['losses'])
                away_total = away['wins'] + away['draws'] + away['losses']
                away_win_pct = (away['wins'] / away_total * 100) if away_total > 0 else 0
                st.metric("Win Rate", f"{away_win_pct:.1f}%")
            
            # Recent form
            st.markdown("### 📅 Recent Form (Last 10 Matches)")
            
            recent = stats['recent_matches'].head(10)
            
            if len(recent) > 0:
                # Create form display
                form_data = []
                for _, match in recent.iterrows():
                    if match['team_score'] > match['opponent_score']:
                        result = 'W'
                        color = '🟢'
                    elif match['team_score'] < match['opponent_score']:
                        result = 'L'
                        color = '🔴'
                    else:
                        result = 'D'
                        color = '🟡'
                    
                    form_data.append({
                        'Date': match['date'].strftime('%Y-%m-%d'),
                        'Opponent': match['opponent'],
                        'Venue': match['venue'],
                        'Score': f"{int(match['team_score'])} - {int(match['opponent_score'])}",
                        'Result': f"{color} {result}",
                        'Tournament': match['tournament']
                    })
                
                form_df = pd.DataFrame(form_data)
                st.dataframe(form_df, use_container_width=True, hide_index=True)
                
                # Form string
                form_string = ''.join([
                    '🟢' if row['team_score'] > row['opponent_score'] 
                    else '🔴' if row['team_score'] < row['opponent_score'] 
                    else '🟡' 
                    for _, row in recent.iterrows()
                ])
                
                st.markdown(f"**Current Form:** {form_string}")
            
            # Tournament participation
            st.markdown("### 🏆 Tournament Participation")
            
            tournament_stats = stats['tournament_stats'].head(10)
            
            if len(tournament_stats) > 0:
                fig = go.Figure(data=[
                    go.Bar(
                        x=tournament_stats.values,
                        y=tournament_stats.index,
                        orientation='h',
                        marker_color='#1f77b4'
                    )
                ])
                
                fig.update_layout(
                    title=f"{selected_team} - Top Tournaments by Matches Played",
                    xaxis_title="Number of Matches",
                    yaxis_title="Tournament",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Performance over time
            st.markdown("### 📈 Performance Trends Over Time")
            
            all_matches = stats['all_matches'].copy()
            all_matches['year'] = pd.to_datetime(all_matches['date']).dt.year
            
            # Calculate yearly win rate
            yearly_stats = []
            for year in sorted(all_matches['year'].unique()):
                year_matches = all_matches[all_matches['year'] == year]
                wins = len(year_matches[year_matches['team_score'] > year_matches['opponent_score']])
                total = len(year_matches)
                win_rate = (wins / total * 100) if total > 0 else 0
                yearly_stats.append({'Year': year, 'Win Rate': win_rate, 'Matches': total})
            
            yearly_df = pd.DataFrame(yearly_stats)
            
            if len(yearly_df) > 0:
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=yearly_df['Year'],
                    y=yearly_df['Win Rate'],
                    mode='lines+markers',
                    name='Win Rate',
                    line=dict(color='#1f77b4', width=2),
                    marker=dict(size=8)
                ))
                
                fig.update_layout(
                    title=f"{selected_team} - Win Rate Trend Over Time",
                    xaxis_title="Year",
                    yaxis_title="Win Rate (%)",
                    height=400,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Download statistics
            st.markdown("---")
            
            # Create downloadable report
            report = f"""
TEAM STATISTICS REPORT - {selected_team}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

OVERALL RECORD
Total Matches: {stats['total_matches']}
Wins: {stats['wins']}
Draws: {stats['draws']}
Losses: {stats['losses']}
Win Rate: {stats['win_percentage']:.1f}%

GOALS
Goals Scored: {stats['goals_scored']}
Goals Conceded: {stats['goals_conceded']}
Goal Difference: {stats['goal_difference']:+d}
Average Goals Scored: {stats['avg_goals_scored']:.2f}
Average Goals Conceded: {stats['avg_goals_conceded']:.2f}

HOME RECORD
Wins: {stats['home_record']['wins']}
Draws: {stats['home_record']['draws']}
Losses: {stats['home_record']['losses']}

AWAY RECORD
Wins: {stats['away_record']['wins']}
Draws: {stats['away_record']['draws']}
Losses: {stats['away_record']['losses']}

---
World Cup Fan Intelligence Hub
Powered by IBM watsonx.ai
"""
            
            st.download_button(
                label="📥 Download Statistics Report",
                data=report,
                file_name=f"team_stats_{selected_team}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    # Information
    st.markdown("---")
    st.markdown("### ℹ️ About Team Statistics")
    
    with st.expander("What statistics are included?"):
        st.markdown("""
        Our comprehensive team statistics include:
        
        **Overall Performance:**
        - Total matches played
        - Win/Draw/Loss record
        - Win percentage
        - Goal statistics (scored, conceded, difference)
        
        **Home vs Away:**
        - Separate records for home and away matches
        - Win rates for each venue type
        
        **Recent Form:**
        - Last 10 matches with results
        - Visual form indicator
        
        **Tournament History:**
        - Participation in major tournaments
        - Match counts by tournament
        
        **Trends Over Time:**
        - Yearly win rate trends
        - Performance evolution
        
        All statistics are calculated from the complete dataset of 49,329 international matches 
        from 1872 to 2026.
        """)

if __name__ == "__main__":
    main()

# Made with Bob
