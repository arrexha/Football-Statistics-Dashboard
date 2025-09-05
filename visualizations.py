import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import streamlit as st

class SoccerVisualizations:
    """
    Custom visualization functions for soccer statistics
    """
    
    def __init__(self):
        self.color_palette = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', 
            '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'
        ]
        self.team_colors = {
            'Manchester City': '#6CABDD',
            'Arsenal': '#EF0107',
            'Manchester United': '#DA020E',
            'Liverpool': '#C8102E',
            'Chelsea': '#034694',
            'Tottenham': '#132257',
            'Newcastle': '#241F20',
            'Brighton': '#0057B8'
        }
    
    def create_league_table_chart(self, df: pd.DataFrame) -> go.Figure:
        """
        Create an interactive league standings visualization
        """
        fig = go.Figure()
        
        # Add points bar chart
        fig.add_trace(go.Bar(
            x=df['Team'],
            y=df['Points'],
            name='Points',
            marker_color=self.color_palette[0],
            text=df['Points'],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Points: %{y}<br>Position: %{customdata}<extra></extra>',
            customdata=df['Position']
        ))
        
        fig.update_layout(
            title='Premier League Standings - Points Total',
            xaxis_title='Team',
            yaxis_title='Points',
            xaxis_tickangle=-45,
            height=600,
            showlegend=False,
            template='plotly_white'
        )
        
        return fig
    
    def create_goals_comparison(self, df: pd.DataFrame) -> go.Figure:
        """
        Create goals for vs goals against comparison
        """
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df['Team'],
            y=df['Goals For'],
            name='Goals For',
            marker_color='#2ECC71',
            offsetgroup=1
        ))
        
        fig.add_trace(go.Bar(
            x=df['Team'],
            y=df['Goals Against'],
            name='Goals Against',
            marker_color='#E74C3C',
            offsetgroup=2
        ))
        
        fig.update_layout(
            title='Goals For vs Goals Against by Team',
            xaxis_title='Team',
            yaxis_title='Goals',
            xaxis_tickangle=-45,
            height=600,
            barmode='group',
            template='plotly_white'
        )
        
        return fig
    
    def create_player_comparison_radar(self, df: pd.DataFrame, players: list) -> go.Figure:
        """
        Create radar chart comparing players
        """
        if len(players) == 0:
            return go.Figure()
        
        # Select metrics for radar chart
        metrics = ['Goals', 'Assists', 'Goals per 90', 'Shots per Game', 'Pass Accuracy %']
        
        fig = go.Figure()
        
        for i, player in enumerate(players):
            player_data = df[df['Player'] == player].iloc[0]
            
            # Normalize values for radar chart (0-100 scale)
            values = []
            for metric in metrics:
                if metric == 'Pass Accuracy %':
                    values.append(player_data[metric])
                elif metric == 'Goals per 90':
                    values.append(min(player_data[metric] * 50, 100))  # Scale to 0-100
                else:
                    max_val = df[metric].max()
                    values.append((player_data[metric] / max_val) * 100)
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=metrics,
                fill='toself',
                name=player,
                line_color=self.color_palette[i % len(self.color_palette)]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title='Player Comparison - Key Metrics',
            height=600
        )
        
        return fig
    
    def create_team_performance_timeline(self, team_data: dict) -> go.Figure:
        """
        Create timeline showing team performance over seasons
        """
        seasons_df = pd.DataFrame(team_data['seasons'])
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('League Position', 'Points Total', 'Goals Scored', 'Win-Draw-Loss'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"type": "bar"}]]
        )
        
        # League position (inverted y-axis for better visualization)
        fig.add_trace(
            go.Scatter(x=seasons_df['Season'], y=seasons_df['Position'],
                      mode='lines+markers', name='Position',
                      line=dict(color='#E74C3C', width=3)),
            row=1, col=1
        )
        
        # Points
        fig.add_trace(
            go.Scatter(x=seasons_df['Season'], y=seasons_df['Points'],
                      mode='lines+markers', name='Points',
                      line=dict(color='#3498DB', width=3)),
            row=1, col=2
        )
        
        # Goals
        fig.add_trace(
            go.Scatter(x=seasons_df['Season'], y=seasons_df['Goals'],
                      mode='lines+markers', name='Goals',
                      line=dict(color='#2ECC71', width=3)),
            row=2, col=1
        )
        
        # Win-Draw-Loss stacked bar
        fig.add_trace(
            go.Bar(x=seasons_df['Season'], y=seasons_df['Wins'], name='Wins',
                  marker_color='#2ECC71'),
            row=2, col=2
        )
        fig.add_trace(
            go.Bar(x=seasons_df['Season'], y=seasons_df['Draws'], name='Draws',
                  marker_color='#F39C12'),
            row=2, col=2
        )
        fig.add_trace(
            go.Bar(x=seasons_df['Season'], y=seasons_df['Losses'], name='Losses',
                  marker_color='#E74C3C'),
            row=2, col=2
        )
        
        # Update y-axis for position (invert)
        fig.update_yaxes(autorange="reversed", row=1, col=1)
        
        fig.update_layout(
            height=800,
            title_text=f"{team_data['team']} - Historical Performance",
            showlegend=True,
            template='plotly_white'
        )
        
        return fig
    
    def create_prediction_probability_chart(self, predictions: dict) -> go.Figure:
        """
        Create match prediction probability visualization
        """
        outcomes = list(predictions.keys())
        probabilities = list(predictions.values())
        
        # Create color scale based on probability
        colors = ['#E74C3C' if p < 30 else '#F39C12' if p < 60 else '#2ECC71' 
                 for p in probabilities]
        
        fig = go.Figure(go.Bar(
            x=outcomes,
            y=probabilities,
            marker_color=colors,
            text=[f'{p:.1f}%' for p in probabilities],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Probability: %{y:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title='Match Outcome Predictions',
            xaxis_title='Outcome',
            yaxis_title='Probability (%)',
            height=400,
            template='plotly_white',
            yaxis=dict(range=[0, 100])
        )
        
        return fig
    
    def create_top_scorers_chart(self, df: pd.DataFrame, top_n: int = 10) -> go.Figure:
        """
        Create top scorers visualization
        """
        top_scorers = df.nlargest(top_n, 'Goals')
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=top_scorers['Player'],
            x=top_scorers['Goals'],
            orientation='h',
            marker_color=self.color_palette[0],
            text=top_scorers['Goals'],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Goals: %{x}<br>Team: %{customdata}<extra></extra>',
            customdata=top_scorers['Team']
        ))
        
        fig.update_layout(
            title=f'Top {top_n} Goal Scorers',
            xaxis_title='Goals',
            yaxis_title='Player',
            height=500,
            template='plotly_white'
        )
        
        return fig
    
    def create_form_guide(self, team_results: list) -> go.Figure:
        """
        Create team form guide visualization
        """
        # Sample form data (W=3, D=1, L=0)
        form_values = {'W': 3, 'D': 1, 'L': 0}
        colors = {'W': '#2ECC71', 'D': '#F39C12', 'L': '#E74C3C'}
        
        results = [form_values.get(result, 0) for result in team_results]
        result_colors = [colors.get(result, '#95A5A6') for result in team_results]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=list(range(1, len(team_results) + 1)),
            y=results,
            marker_color=result_colors,
            text=team_results,
            textposition='middle',
            hovertemplate='Match %{x}<br>Result: %{text}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Recent Form Guide (Last 5 Matches)',
            xaxis_title='Match (Most Recent →)',
            yaxis_title='Points',
            height=300,
            template='plotly_white',
            showlegend=False,
            yaxis=dict(range=[0, 3.5])
        )
        
        return fig

# Create global instance
viz = SoccerVisualizations()