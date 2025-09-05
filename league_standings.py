import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show():
    """Display the League Standings page"""
    st.title("📊 League Standings")
    st.markdown("### Real-time League Tables and Rankings")
    
    # Sample league data
    sample_standings = {
        'Position': list(range(1, 21)),
        'Team': [
            'Manchester City', 'Arsenal', 'Manchester United', 'Newcastle United', 
            'Liverpool', 'Brighton', 'Aston Villa', 'Tottenham', 'Brentford', 
            'Fulham', 'Crystal Palace', 'Chelsea', 'Wolves', 'West Ham',
            'Leeds United', 'Everton', 'Nottingham Forest', 'Leicester City',
            'Bournemouth', 'Southampton'
        ],
        'Played': [38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38],
        'Won': [28, 26, 23, 19, 19, 18, 18, 18, 15, 16, 11, 12, 13, 14, 11, 13, 9, 11, 11, 12],
        'Drawn': [5, 6, 6, 14, 10, 8, 7, 6, 14, 7, 12, 11, 6, 7, 10, 6, 11, 7, 9, 6],
        'Lost': [5, 6, 9, 5, 9, 12, 13, 14, 9, 15, 15, 15, 19, 17, 17, 19, 18, 20, 18, 20],
        'Goals_For': [89, 88, 58, 68, 75, 72, 61, 66, 58, 55, 40, 38, 31, 42, 48, 34, 38, 51, 37, 36],
        'Goals_Against': [31, 43, 43, 33, 28, 53, 61, 40, 46, 53, 49, 47, 58, 58, 78, 57, 68, 68, 71, 73],
        'Goal_Difference': [58, 45, 15, 35, 47, 19, 0, 26, 12, 2, -9, -9, -27, -16, -30, -23, -30, -17, -34, -37],
        'Points': [89, 84, 75, 71, 67, 62, 61, 60, 59, 55, 45, 44, 45, 49, 43, 45, 38, 40, 42, 42]
    }
    
    df_standings = pd.DataFrame(sample_standings)
    
    # League selection
    leagues = ["Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1"]
    selected_league = st.selectbox("Select League", leagues)
    
    st.subheader(f"🏆 {selected_league} Table")
    
    # Create a styled dataframe
    def style_table(row):
        if row['Position'] <= 4:  # Champions League
            return ['background-color: #d4edda'] * len(row)
        elif row['Position'] <= 6:  # Europa League
            return ['background-color: #fff3cd'] * len(row)
        elif row['Position'] >= 18:  # Relegation
            return ['background-color: #f8d7da'] * len(row)
        else:
            return [''] * len(row)
    
    # Display table with colors
    st.dataframe(
        df_standings.style.apply(style_table, axis=1),
        use_container_width=True,
        hide_index=True
    )
    
    # Legend
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🟢 **Champions League** (Top 4)")
    with col2:
        st.markdown("🟡 **Europa League** (5th-6th)")
    with col3:
        st.markdown("🔴 **Relegation** (Bottom 3)")
    
    # Statistics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Goals", df_standings['Goals_For'].sum())
    with col2:
        st.metric("Average Goals/Game", f"{df_standings['Goals_For'].sum() / (df_standings['Played'].sum() / 2):.1f}")
    with col3:
        st.metric("Highest Scorer", f"{df_standings.loc[df_standings['Goals_For'].idxmax(), 'Team']}")
    with col4:
        st.metric("Best Defense", f"{df_standings.loc[df_standings['Goals_Against'].idxmin(), 'Team']}")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Points Distribution")
        fig_points = px.bar(
            df_standings.head(10), 
            x='Team', 
            y='Points',
            color='Points',
            title="Top 10 Teams by Points"
        )
        fig_points.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_points, use_container_width=True)
    
    with col2:
        st.subheader("⚖️ Goal Difference")
        fig_gd = px.bar(
            df_standings.head(10),
            x='Team',
            y='Goal_Difference',
            color='Goal_Difference',
            color_continuous_scale='RdYlGn',
            title="Goal Difference (Top 10)"
        )
        fig_gd.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_gd, use_container_width=True)
    
    # Form table
    st.subheader("📊 Detailed Statistics")
    
    # Calculate additional metrics
    df_standings['Win_Rate'] = (df_standings['Won'] / df_standings['Played'] * 100).round(1)
    df_standings['Points_Per_Game'] = (df_standings['Points'] / df_standings['Played']).round(2)
    
    # Advanced stats table
    advanced_stats = df_standings[['Position', 'Team', 'Points', 'Win_Rate', 'Points_Per_Game', 'Goal_Difference']].head(10)
    st.dataframe(advanced_stats, use_container_width=True, hide_index=True)
    
    # Position changes simulation
    st.subheader("📈 Position Trends")
    st.info("This would show position changes over the season in a real implementation")
    
    # Create a sample trend chart
    import numpy as np
    
    weeks = list(range(1, 39))
    top_teams = df_standings.head(6)['Team'].tolist()
    
    fig_trends = go.Figure()
    
    for i, team in enumerate(top_teams):
        # Simulate position changes (in real app, this would be historical data)
        positions = np.random.randint(1, 10, size=38)
        positions = np.sort(positions)[::-1] if i < 3 else np.sort(positions)
        
        fig_trends.add_trace(go.Scatter(
            x=weeks,
            y=positions,
            mode='lines+markers',
            name=team,
            line=dict(width=2)
        ))
    
    fig_trends.update_layout(
        title="League Position Over Season (Simulated)",
        xaxis_title="Week",
        yaxis_title="Position",
        yaxis=dict(autorange="reversed", dtick=1),
        height=400
    )
    
    st.plotly_chart(fig_trends, use_container_width=True)