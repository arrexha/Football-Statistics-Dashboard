import pandas as pd
import streamlit as st
from typing import Optional, Dict

class SoccerDataFetcher:
    def __init__(self):
        pass
    
    def fetch_league_standings(self, league_id: str = "39") -> pd.DataFrame:
        """Fetch current league standings"""
        sample_data = {
            'Position': range(1, 21),
            'Team': [
                'Manchester City', 'Arsenal', 'Manchester United', 'Newcastle',
                'Liverpool', 'Brighton', 'Aston Villa', 'Tottenham',
                'Brentford', 'Fulham', 'Crystal Palace', 'Chelsea',
                'Wolves', 'West Ham', 'Leeds United', 'Everton',
                'Nottingham Forest', 'Leicester City', 'Bournemouth', 'Southampton'
            ],
            'Played': [38] * 20,
            'Won': [28, 26, 23, 19, 19, 18, 18, 17, 15, 15, 11, 12, 13, 14, 11, 13, 9, 9, 11, 12],
            'Points': [89, 84, 75, 74, 67, 62, 61, 59, 59, 52, 45, 45, 45, 49, 42, 45, 38, 34, 42, 42]
        }
        return pd.DataFrame(sample_data)
    
    def fetch_team_stats(self, team_name: Optional[str] = None) -> pd.DataFrame:
        """Fetch team statistics"""
        sample_teams = {
            'Team': ['Manchester City', 'Arsenal', 'Manchester United', 'Newcastle',
                    'Liverpool', 'Brighton', 'Aston Villa', 'Tottenham'],
            'League Position': [1, 2, 3, 4, 5, 6, 7, 8],
            'Points': [89, 84, 75, 74, 67, 62, 61, 59],
            'Goals Scored': [89, 88, 58, 68, 75, 72, 61, 66],
            'Goals Conceded': [31, 43, 43, 33, 28, 53, 51, 40],
            'Clean Sheets': [17, 14, 13, 19, 21, 8, 9, 12],
            'Possession %': [67.2, 59.8, 56.4, 52.1, 61.7, 58.9, 54.2, 55.8],
            'Pass Accuracy %': [90.1, 86.7, 83.2, 81.9, 87.4, 84.6, 82.1, 83.7]
        }
        df = pd.DataFrame(sample_teams)
        if team_name:
            df = df[df['Team'].str.contains(team_name, case=False, na=False)]
        return df
    
    def fetch_historical_data(self, team: str, seasons: int = 5) -> Dict:
        """Fetch historical performance data"""
        seasons_data = []
        for i in range(seasons):
            season = f"202{3-i}/2{4-i}"
            seasons_data.append({
                'Season': season,
                'Position': 3 + i,
                'Points': 75 - (i * 5),
                'Goals': 68 - (i * 3),
                'Wins': 22 - i,
                'Draws': 8 + i,
                'Losses': 8 + i
            })
        return {
            'team': team,
            'seasons': seasons_data,
            'trend': 'improving' if seasons_data[0]['Points'] > seasons_data[-1]['Points'] else 'declining'
        }

data_fetcher = SoccerDataFetcher()