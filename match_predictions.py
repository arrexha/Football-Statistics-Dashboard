import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

def show():
    """Display the Match Predictions page"""
    st.title("🔮 Match Predictions")
    st.markdown("### AI-powered Match Outcome Predictions")
    
    # Sample upcoming matches
    today = datetime.now()
    sample_matches = {
        'Date': [today + timedelta(days=i) for i in range(1, 11)],
        'Home_Team': [
            'Manchester City', 'Arsenal', 'Liverpool', 'Chelsea', 'Manchester United',
            'Tottenham', 'Newcastle', 'Brighton', 'Aston Villa', 'West Ham'
        ],
        'Away_Team': [
            'Liverpool', 'Chelsea', 'Manchester United', 'Tottenham', 'Newcastle',
            'Brighton', 'Aston Villa', 'West Ham', 'Crystal Palace', 'Fulham'
        ],
        'Home_Win_Prob': [65, 58, 72, 45, 55, 62, 48, 60, 52, 46],
        'Draw_Prob': [20, 25, 18, 30, 25, 22, 28, 22, 26, 29],
        'Away_Win_Prob': [15, 17, 10, 25, 20, 16, 24, 18, 22, 25],
        'Predicted_Score_Home': [2, 1, 3, 1, 2, 2, 1, 2, 1, 1],
        'Predicted_Score_Away': [1, 1, 0, 1, 1, 1, 1, 0, 1, 1]
    }
    
    df_matches = pd.DataFrame(sample_matches)
    df_matches['Date_Str'] = df_matches['Date'].dt.strftime('%Y-%m-%d')
    df_matches['Match'] = df_matches['Home_Team'] + ' vs ' + df_matches['Away_Team']
    df_matches['Predicted_Score'] = df_matches['Predicted_Score_Home'].astype(str) + '-' + df_matches['Predicted_Score_Away'].astype(str)
    
    # Filters
    st.sidebar.header("Prediction Filters")
    
    # Date range filter
    min_date = df_matches['Date'].min().date()
    max_date = df_matches['Date'].max().date()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Team filter
    all_teams = list(set(df_matches['Home_Team'].tolist() + df_matches['Away_Team'].tolist()))
    selected_teams = st.sidebar.multiselect("Select Teams", all_teams, default=all_teams[:5])
    
    # Filter data
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_matches = df_matches[
            (df_matches['Date'].dt.date >= start_date) & 
            (df_matches['Date'].dt.date <= end_date)
        ]
    else:
        filtered_matches = df_matches
    
    if selected_teams:
        filtered_matches = filtered_matches[
            filtered_matches['Home_Team'].isin(selected_teams) | 
            filtered_matches['Away_Team'].isin(selected_teams)
        ]
    
    # Overview metrics
    st.subheader("📊 Prediction Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Matches", len(filtered_matches))
    with col2:
        avg_home_prob = filtered_matches['Home_Win_Prob'].mean()
        st.metric("Avg Home Win %", f"{avg_home_prob:.1f}%")
    with col3:
        high_confidence = len(filtered_matches[filtered_matches['Home_Win_Prob'] > 60])
        st.metric("High Confidence Predictions", high_confidence)
    with col4:
        total_goals = filtered_matches['Predicted_Score_Home'].sum() + filtered_matches['Predicted_Score_Away'].sum()
        st.metric("Predicted Total Goals", total_goals)
    
    # Upcoming matches table
    st.subheader("🗓️ Upcoming Matches")
    
    # Create a display dataframe
    display_df = filtered_matches[[
        'Date_Str', 'Home_Team', 'Away_Team', 'Predicted_Score',
        'Home_Win_Prob', 'Draw_Prob', 'Away_Win_Prob'
    ]].copy()
    
    display_df.columns = ['Date', 'Home', 'Away', 'Predicted Score', 'Home Win %', 'Draw %', 'Away Win %']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Match selector for detailed analysis
    st.subheader("🔍 Detailed Match Analysis")
    selected_match = st.selectbox(
        "Select a match for detailed analysis:",
        filtered_matches['Match'].tolist()
    )
    
    if selected_match:
        match_data = filtered_matches[filtered_matches['Match'] == selected_match].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### {match_data['Home_Team']} vs {match_data['Away_Team']}")
            st.markdown(f"**Date:** {match_data['Date_Str']}")
            st.markdown(f"**Predicted Score:** {match_data['Predicted_Score']}")
            
            # Probability chart
            probs = [match_data['Home_Win_Prob'], match_data['Draw_Prob'], match_data['Away_Win_Prob']]
            labels = ['Home Win', 'Draw', 'Away Win']
            colors = ['#2E8B57', '#FFD700', '#DC143C']
            
            fig_prob = px.pie(
                values=probs,
                names=labels,
                title="Win Probabilities",
                color_discrete_sequence=colors
            )
            st.plotly_chart(fig_prob, use_container_width=True)
        
        with col2:
            # Team form simulation (in real app, this would be actual data)
            st.markdown("#### Recent Form")
            
            home_form = np.random.choice(['W', 'D', 'L'], size=5, p=[0.6, 0.25, 0.15])
            away_form = np.random.choice(['W', 'D', 'L'], size=5, p=[0.4, 0.3, 0.3])
            
            st.markdown(f"**{match_data['Home_Team']}:** {' '.join(home_form)}")
            st.markdown(f"**{match_data['Away_Team']}:** {' '.join(away_form)}")
            
            # Key stats comparison
            st.markdown("#### Key Statistics")
            stats_data = {
                'Metric': ['Goals/Game', 'Goals Conceded/Game', 'Win Rate %', 'Form Points'],
                match_data['Home_Team']: [2.1, 0.8, 65, 13],
                match_data['Away_Team']: [1.7, 1.2, 45, 7]
            }
            
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, hide_index=True, use_container_width=True)
    
    # Prediction confidence analysis
    st.subheader("🎯 Prediction Confidence Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Confidence distribution
        confidence_bins = ['Low (40-55%)', 'Medium (55-70%)', 'High (70%+)']
        confidence_counts = [
            len(filtered_matches[(filtered_matches['Home_Win_Prob'] >= 40) & (filtered_matches['Home_Win_Prob'] < 55)]),
            len(filtered_matches[(filtered_matches['Home_Win_Prob'] >= 55) & (filtered_matches['Home_Win_Prob'] < 70)]),
            len(filtered_matches[filtered_matches['Home_Win_Prob'] >= 70])
        ]
        
        fig_conf = px.bar(
            x=confidence_bins,
            y=confidence_counts,
            title="Prediction Confidence Distribution",
            labels={'x': 'Confidence Level', 'y': 'Number of Matches'}
        )
        st.plotly_chart(fig_conf, use_container_width=True)
    
    with col2:
        # Goals prediction distribution
        goals_data = filtered_matches['Predicted_Score_Home'] + filtered_matches['Predicted_Score_Away']
        
        fig_goals = px.histogram(
            x=goals_data,
            nbins=6,
            title="Predicted Total Goals Distribution",
            labels={'x': 'Total Goals', 'y': 'Number of Matches'}
        )
        st.plotly_chart(fig_goals, use_container_width=True)
    
    # Model performance metrics (simulated)
    st.subheader("🤖 Model Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Accuracy", "72.5%", "↗️ 2.1%")
    with col2:
        st.metric("Precision", "68.9%", "↗️ 1.8%")
    with col3:
        st.metric("Recall", "71.2%", "↗️ 0.9%")
    with col4:
        st.metric("F1 Score", "70.0%", "↗️ 1.3%")
    
    # Feature importance
    st.subheader("🎲 Prediction Factors")
    
    features = ['Recent Form', 'Head-to-Head', 'Home Advantage', 'Player Injuries', 'Goal Difference', 'League Position']
    importance = [25, 20, 18, 15, 12, 10]
    
    fig_features = px.bar(
        x=features,
        y=importance,
        title="Model Feature Importance",
        labels={'x': 'Features', 'y': 'Importance (%)'}
    )
    fig_features.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig_features, use_container_width=True)
    
    # Disclaimer
    st.info("⚠️ These predictions are for demonstration purposes only and should not be used for actual betting or gambling.")