import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show():
    """Display the Player Statistics page"""
    st.title("👤 Player Statistics")
    st.markdown("### Comprehensive Player Performance Analytics")
    
    # Sample data for demonstration
    sample_players = {
        'Player': ['Lionel Messi', 'Cristiano Ronaldo', 'Kylian Mbappé', 'Erling Haaland', 'Neymar Jr'],
        'Goals': [30, 28, 35, 42, 25],
        'Assists': [15, 8, 12, 10, 18],
        'Matches': [35, 32, 38, 40, 30],
        'Team': ['PSG', 'Al Nassr', 'PSG', 'Man City', 'Al Hilal']
    }
    
    df_players = pd.DataFrame(sample_players)
    
    # Sidebar filters
    st.sidebar.header("Player Filters")
    selected_team = st.sidebar.selectbox("Select Team", ["All"] + list(df_players['Team'].unique()))
    
    # Filter data based on selection
    if selected_team != "All":
        filtered_df = df_players[df_players['Team'] == selected_team]
    else:
        filtered_df = df_players
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Players", len(filtered_df))
    with col2:
        st.metric("Total Goals", filtered_df['Goals'].sum())
    with col3:
        st.metric("Total Assists", filtered_df['Assists'].sum())
    with col4:
        st.metric("Avg Goals/Match", f"{filtered_df['Goals'].sum() / filtered_df['Matches'].sum():.2f}")
    
    # Player statistics table
    st.subheader("📊 Player Performance Table")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚽ Goals vs Assists")
        fig_scatter = px.scatter(
            filtered_df, 
            x='Goals', 
            y='Assists', 
            hover_name='Player',
            color='Team',
            size='Matches',
            title="Player Goals vs Assists"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        st.subheader("🏆 Top Scorers")
        fig_bar = px.bar(
            filtered_df.sort_values('Goals', ascending=False),
            x='Player',
            y='Goals',
            color='Team',
            title="Goals by Player"
        )
        fig_bar.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Additional statistics
    st.subheader("📈 Detailed Statistics")
    
    # Calculate additional metrics
    filtered_df['Goals_per_Match'] = filtered_df['Goals'] / filtered_df['Matches']
    filtered_df['Assists_per_Match'] = filtered_df['Assists'] / filtered_df['Matches']
    filtered_df['Goal_Involvement'] = filtered_df['Goals'] + filtered_df['Assists']
    
    # Display enhanced table
    display_cols = ['Player', 'Team', 'Goals', 'Assists', 'Goal_Involvement', 'Goals_per_Match', 'Assists_per_Match']
    st.dataframe(
        filtered_df[display_cols].round(2),
        use_container_width=True
    )
    
    # Performance radar chart for selected player
    st.subheader("🎯 Player Performance Radar")
    selected_player = st.selectbox("Select Player for Radar Chart", filtered_df['Player'].tolist())
    
    if selected_player:
        player_data = filtered_df[filtered_df['Player'] == selected_player].iloc[0]
        
        # Normalize data for radar chart (0-100 scale)
        categories = ['Goals', 'Assists', 'Matches', 'Goals_per_Match', 'Assists_per_Match']
        values = [
            (player_data['Goals'] / filtered_df['Goals'].max()) * 100,
            (player_data['Assists'] / filtered_df['Assists'].max()) * 100,
            (player_data['Matches'] / filtered_df['Matches'].max()) * 100,
            (player_data['Goals_per_Match'] / filtered_df['Goals_per_Match'].max()) * 100,
            (player_data['Assists_per_Match'] / filtered_df['Assists_per_Match'].max()) * 100
        ]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=selected_player
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title=f"Performance Radar: {selected_player}"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)