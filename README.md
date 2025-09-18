# ⚽ Football Statistics Dashboard

A comprehensive, interactive web application for analyzing soccer statistics and predictions, built with Streamlit and Plotly. This professional analytics platform provides real-time insights into player performance, team analytics, league standings, and AI-powered match predictions.

![Soccer Dashboard](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)
![Machine Learning](https://img.shields.io/badge/ML-Predictions-green?style=for-the-badge)

## 🌟 Features

### 🏠 **Dashboard Overview**
- Real-time statistics summary with live metrics
- Key performance indicators (KPIs)
- Interactive navigation with responsive design
- Multi-league support (Premier League, La Liga, and more)

### 👤 **Player Statistics**
- **Individual Performance Metrics**
  - Goals, assists, and advanced statistics
  - Expected Goals (xG) and Expected Assists (xA)
  - Heat maps and position analysis
  - Injury and fitness tracking
- **Comparative Analysis**
  - Player vs player radar charts
  - Position-based comparisons
  - Season-over-season performance
- **Visualizations**
  - Top scorers and assist leaders
  - Performance trends over time
  - Shot maps and passing networks

### 🏆 **Team Analysis**
- **Performance Metrics**
  - Comprehensive team statistics
  - Tactical formation analysis
  - Home vs Away performance splits
  - Head-to-head records
- **Historical Data**
  - Multi-season performance trends
  - Transfer market impact analysis
  - Manager performance correlation
- **Advanced Analytics**
  - Team form guide (last 5-10 matches)
  - Strength of schedule analysis
  - Goal difference progression

### 📊 **League Standings**
- **Real-time Tables**
  - Live league standings with automatic updates
  - Alternative tables (home/away, last 6 matches)
  - Relegation and European qualification zones
- **Interactive Visualizations**
  - Goals for/against scatter plots
  - Points progression over season
  - Form table vs actual table comparison

### 🔮 **Match Predictions**
- **AI-Powered Predictions**
  - Machine learning models for match outcomes
  - Probability distributions for scorelines
  - Over/Under goals predictions
  - Both teams to score analysis
- **Prediction Accuracy**
  - Model performance tracking
  - Historical prediction success rates
  - Confidence intervals and uncertainty quantification

### 📈 **Advanced Analytics**
- **Statistical Models**
  - Expected Goals (xG) models
  - Player valuation algorithms
  - Team strength ratings
  - Injury impact analysis
- **Market Intelligence**
  - Transfer value predictions
  - Contract expiry tracking
  - Performance vs salary analysis

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning)

### Quick Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/arrexha/soccer-statistics-dashboard.git
   cd soccer-statistics-dashboard
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the dashboard**
   - Local: `http://localhost:8501`
   - Network: `http://[your-ip]:8501`

### Docker Installation

```bash
# Build the image
docker build -t soccer-dashboard .

# Run the container
docker run -p 8501:8501 soccer-dashboard
```

## 📦 Dependencies

```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
requests>=2.31.0
numpy>=1.24.0
scikit-learn>=1.3.0
scipy>=1.11.0
beautifulsoup4>=4.12.0
selenium>=4.15.0
python-dotenv>=1.0.0
```

## 📁 Project Structure

```
soccer-statistics-dashboard/
├── 📄 app.py                    # Main Streamlit application
├── 🔧 data_fetcher.py          # Data retrieval and API integration
├── 📊 visualizations.py        # Custom plotting and chart functions
├── 🤖 ml_models.py             # Machine learning prediction models
├── ⚙️ config.py                # Configuration and settings
├── 📋 requirements.txt         # Project dependencies
├── 🐳 Dockerfile              # Docker configuration
├── 📖 README.md               # Project documentation
├── 📁 data/                   # Data storage directory
│   ├── raw/                   # Raw data files
│   ├── processed/             # Cleaned data
│   └── models/                # Trained ML models
├── 📁 pages/                  # Streamlit pages
│   ├── __init__.py
│   ├── 👤 player_stats.py     # Player statistics page
│   ├── 🏆 team_analysis.py    # Team analysis page
│   ├── 📊 league_standings.py # League standings page
│   ├── 🔮 match_predictions.py # Match predictions page
│   └── ⚙️ settings.py         # Settings and configuration page
├── 📁 utils/                  # Utility functions
│   ├── __init__.py
│   ├── data_processing.py     # Data cleaning and preprocessing
│   ├── api_helpers.py         # API interaction helpers
│   └── constants.py           # Constants and configurations
└── 📁 tests/                  # Test files
    ├── test_data_fetcher.py
    ├── test_visualizations.py
    └── test_ml_models.py
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# API Keys
FOOTBALL_DATA_API_KEY=your_football_data_api_key
RAPID_API_KEY=your_rapid_api_key
SPORTS_DB_API_KEY=your_sports_db_api_key

# Database Configuration
DATABASE_URL=your_database_url
REDIS_URL=your_redis_url

# Application Settings
DEBUG=False
CACHE_TTL=300
MAX_RETRIES=3
```

### API Integration

The dashboard supports multiple data sources:

- **Football-Data.org API** - Comprehensive European league data
- **RapidAPI Football** - Real-time match data and statistics
- **TheSportsDB API** - Historical data and media content
- **Custom scrapers** - Additional data sources

### Supported Leagues

- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League
- 🇪🇸 La Liga
- 🇩🇪 Bundesliga
- 🇮🇹 Serie A
- 🇫🇷 Ligue 1
- 🇪🇺 UEFA Champions League
- 🇪🇺 UEFA Europa League

## 📈 Key Metrics Tracked

### Player Metrics
| Category | Metrics |
|----------|---------|
| **Scoring** | Goals, Assists, xG, xA, Shot Conversion Rate |
| **Passing** | Pass Completion %, Key Passes, Through Balls |
| **Defending** | Tackles, Interceptions, Clearances, Blocks |
| **Physical** | Distance Covered, Sprints, Duels Won |
| **Goalkeeping** | Saves, Clean Sheets, Save Percentage, Distribution |

### Team Metrics
| Category | Metrics |
|----------|---------|
| **Performance** | Points, Goal Difference, Form Rating |
| **Style** | Possession %, Pass Accuracy, Pressing Intensity |
| **Efficiency** | Goals per Shot, xG Difference, Set Piece Success |
| **Defensive** | Clean Sheets, Goals Conceded, Defensive Actions |

## 🎨 Visualizations

### Interactive Charts
- **📊 Bar Charts**: League standings, top scorers, team comparisons
- **🎯 Radar Charts**: Player attribute comparisons, team style analysis
- **📈 Line Charts**: Performance trends, form guides, season progression
- **🗺️ Heat Maps**: Player positioning, shot maps, pass networks
- **📋 Tables**: Sortable statistics, league tables, head-to-head records
- **🎲 Probability Charts**: Match predictions, outcome distributions

### Advanced Visualizations
- **Network Graphs**: Player passing networks, team connectivity
- **Scatter Plots**: Performance correlations, efficiency analysis
- **Box Plots**: Statistical distributions, performance variability
- **Geographical Maps**: Player origins, transfer flows

## 🤖 Machine Learning Models

### Prediction Models
- **Match Outcome Prediction**: Random Forest + Gradient Boosting
- **Goal Prediction**: Poisson Regression with team strength
- **Player Performance**: LSTM for time series forecasting
- **Transfer Value**: Multiple regression with market factors

### Model Performance
- **Match Predictions**: ~65% accuracy
- **Over/Under Goals**: ~58% accuracy
- **Both Teams Score**: ~62% accuracy

## 🚀 Deployment Options

### Streamlit Cloud
1. Push code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy with automatic updates

### Heroku Deployment
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port \$PORT --server.enableCORS false" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### AWS/Azure/GCP
- Use container services (ECS, Container Instances, Cloud Run)
- Set up load balancing for high traffic
- Configure auto-scaling policies

### Docker Compose
```yaml
version: '3.8'
services:
  soccer-dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      - FOOTBALL_DATA_API_KEY=${FOOTBALL_DATA_API_KEY}
    volumes:
      - ./data:/app/data
```

## 🔒 Security & Privacy

- API keys stored securely in environment variables
- Rate limiting implemented for API calls
- User data privacy compliance (GDPR)
- Secure data transmission (HTTPS)

## 📊 Performance Optimization

- **Caching**: Redis for API responses, Streamlit cache for computations
- **Lazy Loading**: Load data on-demand to reduce initial load time
- **Data Compression**: Optimize data storage and transfer
- **CDN Integration**: Serve static assets efficiently

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### Development Workflow
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes and add tests
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Create Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include unit tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Roadmap

### Short-term (1-3 months)
- [ ] Real-time live match tracking
- [ ] Mobile app development
- [ ] Advanced ML model improvements
- [ ] Multi-language support

### Medium-term (3-6 months)
- [ ] Fantasy football integration
- [ ] Social features and community
- [ ] Custom alert system
- [ ] API for third-party access

### Long-term (6+ months)
- [ ] AI-powered tactical analysis
- [ ] Video analysis integration
- [ ] Blockchain-based fan tokens
- [ ] VR/AR match experiences

## 🐛 Known Issues & Limitations

- **Rate Limits**: Some APIs have request limitations
- **Data Delays**: Real-time data may have 1-2 minute delays
- **Mobile**: Some visualizations need mobile optimization
- **Performance**: Large datasets may cause slower loading

## 📞 Support & Contact

- **GitHub Issues**: [Create an issue](https://github.com/arrexha/Soccer-Dashboard/issues/new)
- **Email**: arrexha529@gmail.com
- **Twitter**: [@ArRexha00](https://twitter.com/ArRexha00)

## 🏆 Acknowledgments

- **Data Providers**: Football-Data.org, RapidAPI, TheSportsDB
- **Frameworks**: Streamlit, Plotly, Pandas, Scikit-learn
- **Community**: Open-source contributors and soccer analytics community
- **Inspiration**: Football analytics pioneers and data science community

## 📈 Statistics

![GitHub stars](https://img.shields.io/github/stars/arrexha/soccer-statistics-dashboard?style=social)
![GitHub forks](https://img.shields.io/github/forks/arrexha/soccer-statistics-dashboard?style=social)
![GitHub issues](https://img.shields.io/github/issues/arrexha/soccer-statistics-dashboard)
![GitHub license](https://img.shields.io/github/license/arrexha/soccer-statistics-dashboard)

---

**Built with ❤️ and ⚽ by [Ar Rexha](https://github.com/arrexha)**

*Professional Soccer Analytics • Machine Learning Predictions • Real-time Data*

⭐ **Star this repository if you found it helpful!**

[![GitHub](https://img.shields.io/badge/GitHub-arrexha-blue?style=flat&logo=github)](https://github.com/arrexha)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-orange?style=flat&logo=web)](https://github.com/arrexha/Portfolio-Website)
