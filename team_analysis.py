import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_fetcher import data_fetcher
import numpy as np

# Simple analytics functions
def calculate_form_points(recent_form):
    """Calculate points from recent form"""
    return sum([3 if x == 'W' else 1 if x == 'D' else 0 for x in recent_form])

def calculate_team_momentum(recent_form):
    """Calculate team momentum"""
    points = [3 if x == 'W' else 1 if x == 'D' else 0 for x in recent_form]
    trend = np.polyfit(range(len(points)), points, 1)[0]
    return ("Positive" if trend > 0 else "Negative", abs(trend))

def generate_season_projection(current_points, games_left):
    """Generate season projection"""
    ppg = current_points / (38 - games_left) if games_left < 38 else 2.0
    projected_points = int(current_points + (ppg * games_left))
    return {
        'projected_points': projected_points,
        'confidence': f"{min(95, max(60, int(ppg * 30)))}%",
        'current_ppg': f"{ppg:.2f}"
    }

def create_form_guide(recent_form):
    """Create form guide chart"""
    form_data = {'Match': range(1, len(recent_form) + 1), 'Result': recent_form}
    colors = ['green' if x == 'W' else 'yellow' if x == 'D' else 'red' for x in recent_form]
    fig = px.bar(x=form_data['Match'], y=[1]*len(recent_form), color=colors, title="Recent Form")
    return fig

def create_team_performance_timeline(historical_data):
    """Create performance timeline"""
    seasons = [s['Season'] for s in historical_data['seasons']]
    points = [s['Points'] for s in historical_data['seasons']]
    fig = px.line(x=seasons, y=points, title="Historical Performance", markers=True)
    return fig

def show():
    """Display the Team Analysis page"""
    
    st.header("🏆 Team Analysis")
    st.markdown("In-depth team performance metrics and comparative analysis")
    
    # Fetch team data
    with st.spinner("Loading team data..."):
        team_df = data_fetcher.fetch_team_stats()
        league_df = data_fetcher.fetch_league_standings()
    
    if team_df.empty:
        st.error("No team data available")
        return
    
    # Team selection for detailed analysis
    st.sidebar.subheader("Team Selection")
    available_teams = team_df['Team'].tolist()
    selected_team = st.sidebar.selectbox("Select team for detailed analysis", available_teams)
    
    # Main dashboard
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⚖️ Comparison", "📈 Historical", "🎯 Performance"])
    
    with tab1:
        st.subheader("Team Performance Overview")
        
        # Key metrics for selected team
        team_data = team_df[team_df['Team'] == selected_team].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("League Position", f"#{team_data['League Position']}")
        with col2:
            st.metric("Points", team_data['Points'])
        with col3:
            st.metric("Goals Scored", team_data['Goals Scored'])
        with col4:
            st.metric("Goals Conceded", team_data['Goals Conceded'])
        
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            goal_diff = team_data['Goals Scored'] - team_data['Goals Conceded']
            st.metric("Goal Difference", goal_diff)
        with col6:
            st.metric("Clean Sheets", team_data['Clean Sheets'])
        with col7:
            st.metric("Possession %", f"{team_data['Possession %']:.1f}%")
        with col8:
            st.metric("Pass Accuracy %", f"{team_data['Pass Accuracy %']:.1f}%")
        
        # Team performance charts
        st.markdown("---")
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Goals comparison chart
            fig_goals = go.Figure()
            fig_goals.add_trace(go.Bar(
                name='Goals Scored',
                x=['Goals'],
                y=[team_data['Goals Scored']],
                marker_color='#2ECC71'
            ))
            fig_goals.add_trace(go.Bar(
                name='Goals Conceded',
                x=['Goals'],
                y=[team_data['Goals Conceded']],
                marker_color='#E74C3C'
            ))
            fig_goals.update_layout(
                title=f'{selected_team} - Goals Analysis',
                barmode='group',
                height=400
            )
            st.plotly_chart(fig_goals, use_container_width=True)
        
        with col_chart2:
            # Performance metrics radar
            metrics = ['Possession %', 'Pass Accuracy %', 'Shots per Game', 'Tackles per Game']
            values = [
                team_data['Possession %'],
                team_data['Pass Accuracy %'],
                (team_data['Shots per Game'] / 20) * 100,  # Normalize to 0-100
                (team_data['Tackles per Game'] / 25) * 100  # Normalize to 0-100
            ]
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=metrics,
                fill='toself',
                name=selected_team,
                line_color='#3498DB'
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                title=f'{selected_team} - Performance Metrics',
                height=400
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        
        # Recent form simulation
        st.markdown("---")
        st.subheader("📊 Recent Form")
        
        # Simulate recent form (in real app, this would come from API)
        import random
        random.seed(hash(selected_team) % 1000)  # Consistent results for each team
        recent_form = random.choices(['W', 'D', 'L'], weights=[0.4, 0.3, 0.3], k=5)
        
        form_points = calculate_form_points(recent_form)
        momentum_dir, momentum_strength = calculate_team_momentum(recent_form * 2)  # Extend for momentum calc
        
        form_col1, form_col2, form_col3 = st.columns(3)
        with form_col1:
            st.metric("Form Points", f"{form_points}/15")
        with form_col2:
            st.metric("Momentum", f"{momentum_dir}")
        with form_col3:
            st.metric("Strength", momentum_strength)
        
        # Form visualization
        st.plotly_chart(
            create_form_guide(recent_form),
            use_container_width=True
        )
    
    with tab2:
        st.subheader("Team Comparison")
        
        # Select teams for comparison
        comparison_teams = st.multiselect(
            "Select teams to compare (max 4)",
            available_teams,
            default=[selected_team],
            max_selections=4
        )
        
        if len(comparison_teams) >= 2:
            comparison_df = team_df[team_df['Team'].isin(comparison_teams)]
            
            # Comparison metrics
            st.markdown("#### Key Metrics Comparison")
            comparison_metrics = ['Points', 'Goals Scored', 'Goals Conceded', 'Clean Sheets']
            
            for metric in comparison_metrics:
                fig = px.bar(
                    comparison_df,
                    x='Team',
                    y=metric,
                    title=f'{metric} Comparison',
                    color='Team',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed comparison table
            st.markdown("#### Detailed Statistics")
            display_comparison = comparison_df.set_index('Team')
            st.dataframe(display_comparison, use_container_width=True)
            
            # Head-to-head insights
            st.markdown("#### 🧠 Comparison Insights")
            best_attack = comparison_df.loc[comparison_df['Goals Scored'].idxmax(), 'Team']
            best_defense = comparison_df.loc[comparison_df['Goals Conceded'].idxmin(), 'Team']
            highest_possession = comparison_df.loc[comparison_df['Possession %'].idxmax(), 'Team']
            
            insight_col1, insight_col2, insight_col3 = st.columns(3)
            with insight_col1:
                st.success(f"🥅 **Best Attack:** {best_attack}")
            with insight_col2:
                st.info(f"🛡️ **Best Defense:** {best_defense}")
            with insight_col3:
                st.warning(f"⚽ **Most Possession:** {highest_possession}")
    
    with tab3:
        st.subheader("Historical Performance")
        
        # Fetch historical data
        if selected_team:
            historical_data = data_fetcher.fetch_historical_data(selected_team)
        
        if historical_data:
            # Historical performance chart
            st.plotly_chart(
                create_team_performance_timeline(historical_data),
                use_container_width=True
            )
            
            # Season projection
            st.markdown("---")
            st.subheader("📊 Season Projection")
            
            current_points = team_data['Points']
            # Estimate games played (in real app, this would be actual data)
            estimated_games = min(38, max(10, current_points // 2))  # Rough estimate
            
            projection = generate_season_projection(current_points, estimated_games)
            
            proj_col1, proj_col2, proj_col3, proj_col4 = st.columns(4)
            with proj_col1:
                st.metric("Current Points", current_points)
            with proj_col2:
                st.metric("Projected Final", f"{projection['projected_points']}")
            with proj_col3:
                st.metric("Confidence", projection['confidence'])
            with proj_col4:
                st.metric("Points per Game", f"{projection['current_ppg']}")
        else:
            st.info("Historical data not available for this team")
    
    with tab4:
        st.subheader("Performance Analysis")
        
        # Advanced metrics
        st.markdown("#### 🔍 Advanced Metrics")
        
        # Calculate advanced stats
        goals_per_game = team_data['Goals Scored'] / 38  # Assuming 38 games
        goals_against_per_game = team_data['Goals Conceded'] / 38
        clean_sheet_percentage = (team_data['Clean Sheets'] / 38) * 100
        
        adv_col1, adv_col2, adv_col3 = st.columns(3)
        with adv_col1:
            st.metric("Goals per Game", f"{goals_per_game:.2f}")
        with adv_col2:
            st.metric("Goals Against per Game", f"{goals_against_per_game:.2f}")
        with adv_col3:
            st.metric("Clean Sheet %", f"{clean_sheet_percentage:.1f}%")
        
        # Performance categories
        st.markdown("---")
        st.markdown("#### 📈 Performance Categories")
        
        performance_data = {
            'Category': ['Attack', 'Defense', 'Midfield', 'Overall'],
            'Rating': [
                min(100, (team_data['Goals Scored'] / 100) * 100),  # Attack rating
                min(100, max(0, 100 - (team_data['Goals Conceded'] / 80) * 100)),  # Defense rating  
                team_data['Pass Accuracy %'],  # Midfield rating
                (team_data['Points'] / 114) * 100  # Overall rating (assuming max 114 points)
            ]
        }
        
        performance_df = pd.DataFrame(performance_data)
        
        fig_performance = px.bar(
            performance_df,
            x='Category',
            y='Rating',
            title=f'{selected_team} - Performance Ratings',
            color='Rating',
            color_continuous_scale='RdYlGn',
            text='Rating'
        )
        fig_performance.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_performance.update_layout(height=400, yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig_performance, use_container_width=True)
        
        # Strengths and weaknesses
        st.markdown("---")
        st.markdown("#### 💪 Strengths & Weaknesses")
        
        # Calculate relative performance vs league average
        league_avg_goals = team_df['Goals Scored'].mean()
        league_avg_conceded = team_df['Goals Conceded'].mean()
        league_avg_possession = team_df['Possession %'].mean()
        
        strengths = []
        weaknesses = []
        
        if team_data['Goals Scored'] > league_avg_goals * 1.1:
            strengths.append("Strong attacking play")
        elif team_data['Goals Scored'] < league_avg_goals * 0.9:
            weaknesses.append("Lacks attacking threat")
        
        if team_data['Goals Conceded'] < league_avg_conceded * 0.9:
            strengths.append("Solid defensive structure")
        elif team_data['Goals Conceded'] > league_avg_conceded * 1.1:
            weaknesses.append("Defensive vulnerabilities")
        
        if team_data['Possession %'] > league_avg_possession * 1.05:
            strengths.append("Excellent ball control")
        elif team_data['Possession %'] < league_avg_possession * 0.95:
            weaknesses.append("Struggles to keep possession")
        
        strength_col, weakness_col = st.columns(2)
        
        with strength_col:
            st.success("**Strengths:**")
            for strength in strengths:
                st.write(f"✅ {strength}")
            if not strengths:
                st.write("• Average performance across metrics")
        
        with weakness_col:
            st.error("**Areas for Improvement:**")
            for weakness in weaknesses:
                st.write(f"❌ {weakness}")
            if not weaknesses:
                st.write("• No significant weaknesses identified")