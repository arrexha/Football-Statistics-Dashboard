import streamlit as st
import sys
import os

# Add the pages directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page imports
from pages import player_stats, team_analysis, league_standings, match_predictions

# Configure page
st.set_page_config(
    page_title="Soccer Statistics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title("⚽ Soccer Statistics Dashboard")
st.markdown("### Professional Soccer Analytics Platform")

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("---")

# Page selection
pages = {
    "🏠 Home": "home",
    "👤 Player Statistics": "player_stats",
    "🏆 Team Analysis": "team_analysis", 
    "📊 League Standings": "league_standings",
    "🔮 Match Predictions": "match_predictions"
}

selected_page = st.sidebar.selectbox("Select a page:", list(pages.keys()))

# Handle case where selected_page might be None
if selected_page is None:
    selected_page = "🏠 Home"

# Home page content
if pages[selected_page] == "home":
    st.markdown("## Welcome to the Soccer Statistics Dashboard!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Players", "1,247", "↗️ 15")
    
    with col2:
        st.metric("Active Teams", "89", "↗️ 3")
        
    with col3:
        st.metric("Matches Analyzed", "2,156", "↗️ 42")
    
    st.markdown("---")
    
    st.markdown("""
    ### 🚀 Features:
    - **Player Statistics**: Comprehensive player performance analytics
    - **Team Analysis**: In-depth team performance metrics and comparisons
    - **League Standings**: Real-time league tables and rankings
    - **Match Predictions**: AI-powered match outcome predictions
    
    ### 📈 Analytics Capabilities:
    - Performance tracking and trends
    - Interactive visualizations
    - Statistical comparisons
    - Predictive modeling
    
    **Select a page from the sidebar to get started!**
    """)

# Route to appropriate page
elif pages[selected_page] == "player_stats":
    player_stats.show()
elif pages[selected_page] == "team_analysis":
    team_analysis.show()
elif pages[selected_page] == "league_standings":
    league_standings.show()
elif pages[selected_page] == "match_predictions":
    match_predictions.show()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using Streamlit")