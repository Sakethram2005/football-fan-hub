# ⚽ World Cup Fan Intelligence Hub

**IBM SkillsBuild AI Builders Challenge - June 2026**  
*Theme: "AI Inside the Match"*

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![IBM watsonx.ai](https://img.shields.io/badge/IBM%20watsonx.ai-0F62FE?style=for-the-badge&logo=IBM&logoColor=white)](https://www.ibm.com/watsonx)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

An AI-powered web application that gives every football fan instant match predictions, plain-English explanations, team statistics, and head-to-head history for any World Cup matchup.

![World Cup Fan Intelligence Hub](https://img.shields.io/badge/Status-Complete-success?style=for-the-badge)

---

## 🎯 The Problem

Football fans worldwide struggle to:
- **Predict match outcomes** without access to advanced analytics
- **Understand the reasoning** behind predictions in technical jargon
- **Access comprehensive statistics** for national teams
- **Compare historical performance** between teams

Traditional sports analytics platforms are either too complex for casual fans or lack AI-powered explanations that make predictions understandable.

---

## 💡 Our Solution

**World Cup Fan Intelligence Hub** democratizes football analytics by combining:

1. **🤖 Machine Learning Predictions** - RandomForest model trained on 49,329 international matches (1872-2026)
2. **🧠 AI-Powered Explanations** - IBM watsonx.ai (Llama 3.3 70B) generates plain-English explanations
3. **📊 Interactive Dashboards** - Beautiful visualizations for team statistics and trends
4. **⚔️ Head-to-Head Analysis** - Complete historical matchup data between any two teams

### Key Features

#### 🔮 Match Predictor
- Predict outcomes for any World Cup matchup
- Get win/draw/loss probabilities with confidence scores
- Receive AI-generated explanations in plain English
- View key features influencing the prediction

#### 📊 Team Statistics Dashboard
- Comprehensive analytics for 336+ national teams
- Overall win/draw/loss records and goal statistics
- Home vs Away performance comparison
- Recent form analysis (last 10 matches)
- Tournament participation history
- Performance trends over time

#### ⚔️ Head-to-Head Analysis
- Complete match history between any two teams
- Win/loss records and goal statistics
- Recent form trends
- Biggest wins and historical context
- Interactive timeline visualization

---

## 🏆 Why This Matters

### For Football Fans
- **Accessibility**: Complex analytics made simple through AI explanations
- **Engagement**: Interactive tools to explore team performance
- **Education**: Learn what factors influence match outcomes
- **Entertainment**: Data-driven insights enhance match viewing experience

### For the Sport
- **Data Democratization**: Advanced analytics accessible to everyone
- **Fan Experience**: Deeper engagement with the beautiful game
- **Historical Preservation**: 154 years of football history at your fingertips
- **Predictive Insights**: Understanding team dynamics and performance patterns

### Technical Innovation
- **IBM watsonx.ai Integration**: Leveraging cutting-edge LLMs for explanations
- **Hybrid AI Approach**: Combining ML predictions with generative AI
- **Real-world Dataset**: 49,329 matches spanning 154 years
- **Production-Ready**: Scalable architecture with caching and optimization

---

## 🛠️ Technical Architecture

### Technology Stack

**Frontend & UI**
- **Streamlit** - Interactive web application framework
- **Plotly** - Interactive data visualizations
- **Custom CSS** - Enhanced UI/UX design

**Machine Learning**
- **scikit-learn** - RandomForest classifier
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computations
- **Feature Engineering** - 13 custom features from historical data

**AI & NLP**
- **IBM watsonx.ai** - Llama 3.3 70B model for explanations
- **IBM Watson Machine Learning** - Model deployment and inference

**Data Processing**
- **Python 3.14** - Core programming language
- **pandas** - Data preprocessing and cleaning
- **datetime** - Temporal feature engineering

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web App                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Match      │  │    Team      │  │  Head-to-    │     │
│  │  Predictor   │  │  Statistics  │  │    Head      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Prediction Engine (Python)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Feature Engineering → ML Model → AI Explanation     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Dataset    │    │ RandomForest │    │ IBM watsonx  │
│  49,329      │    │    Model     │    │   Llama 3.3  │
│  Matches     │    │  (55% acc)   │    │   70B Model  │
└──────────────┘    └──────────────┘    └──────────────┘
```

### Machine Learning Pipeline

1. **Data Preprocessing**
   - Load 49,329 international matches (1872-2026)
   - Clean and standardize team names
   - Handle missing values and invalid dates
   - Filter matches from 1990 onwards for training

2. **Feature Engineering** (13 Features)
   - `home_form`: Last 5 matches performance (home team)
   - `away_form`: Last 5 matches performance (away team)
   - `home_goal_diff`: Recent goal difference trend
   - `away_goal_diff`: Recent goal difference trend
   - `h2h_record`: Historical head-to-head record
   - `home_advantage`: Home venue advantage factor
   - `home_goals_scored_rate`: Average goals scored per match
   - `away_goals_scored_rate`: Average goals scored per match
   - `home_goals_conceded_rate`: Average goals conceded per match
   - `away_goals_conceded_rate`: Average goals conceded per match
   - `is_neutral`: Neutral venue indicator
   - `year`: Temporal feature
   - `month`: Temporal feature

3. **Model Training**
   - Algorithm: RandomForest Classifier
   - Training Data: 25,268 matches (80%)
   - Test Data: 6,318 matches (20%)
   - Hyperparameters:
     - n_estimators: 200
     - max_depth: 20
     - min_samples_split: 5
     - min_samples_leaf: 2
   - Performance: 55% accuracy (3-class problem)

4. **AI Explanation Generation**
   - Model: IBM watsonx.ai Llama 3.3 70B
   - Input: Prediction result + feature values
   - Output: Plain-English explanation
   - Temperature: 0.7 for balanced creativity

---

## 📊 Dataset

**Source**: International Football Results (1872-2026)  
**Size**: 49,329 matches  
**Coverage**: 336 national teams  
**Time Span**: 154 years (1872-2026)

### Dataset Columns
- `date`: Match date
- `home_team`: Home team name
- `away_team`: Away team name
- `home_score`: Goals scored by home team
- `away_score`: Goals scored by away team
- `tournament`: Tournament/competition name
- `city`: Match city
- `country`: Match country
- `neutral`: Neutral venue indicator

### Data Quality
- **Completeness**: 99.85% (72 matches with missing scores removed)
- **Validity**: 100% valid dates
- **Standardization**: Team names normalized to title case
- **Temporal Coverage**: Continuous from 1872 to 2026

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip package manager
- IBM Cloud account (for watsonx.ai)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/football-fan-hub.git
cd football-fan-hub
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up IBM watsonx.ai credentials**

Create a `.env` file in the project root:
```env
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://eu-de.ml.cloud.ibm.com
```

See `docs/ibm_setup_guide.md` for detailed setup instructions.

4. **Download the dataset**
```bash
python scripts/download_dataset.py
```

5. **Train the model** (optional - pre-trained model included)
```bash
python src/model_training.py
```

### Running the Application

```bash
streamlit run app/main.py
```

The application will open in your default browser at `http://localhost:8501`

### Running Tests

```bash
python tests/test_streamlit_app.py
```

---

## 📁 Project Structure

```
football-fan-hub/
├── app/
│   ├── main.py                          # Main Streamlit application
│   ├── pages/
│   │   ├── 1_🔮_Match_Predictor.py     # Match prediction page
│   │   ├── 2_📊_Team_Statistics.py     # Team statistics page
│   │   └── 3_⚔️_Head_to_Head.py        # Head-to-head analysis page
│   └── __init__.py
├── src/
│   ├── data_preprocessing.py            # Data cleaning and preprocessing
│   ├── feature_engineering.py           # Feature creation for ML
│   ├── model_training.py                # RandomForest model training
│   ├── prediction_engine.py             # Complete prediction system
│   ├── ibm_granite_integration.py       # IBM watsonx.ai integration
│   └── granite_explain.py               # AI explanation generation
├── data/
│   ├── raw/                             # Raw dataset
│   └── processed/                       # Cleaned dataset
├── models/
│   ├── match_predictor.pkl              # Trained RandomForest model
│   ├── feature_scaler.pkl               # Feature scaler
│   └── model_metrics.json               # Model performance metrics
├── tests/
│   └── test_streamlit_app.py            # Application tests
├── scripts/
│   ├── download_dataset.py              # Dataset download script
│   └── create_sample_dataset.py         # Sample data generator
├── docs/
│   └── ibm_setup_guide.md               # IBM watsonx.ai setup guide
├── .streamlit/
│   └── config.toml                      # Streamlit configuration
├── requirements.txt                      # Python dependencies
├── .env.example                         # Environment variables template
├── .gitignore                           # Git ignore rules
├── LICENSE                              # MIT License
├── README.md                            # This file
└── project-plan.md                      # Detailed project plan
```

---

## 🎯 Model Performance

### RandomForest Classifier Metrics

**Overall Accuracy**: 55.0%  
**Cross-Validation Score**: 55.35% (±1.2%)

**Class-wise Performance**:
| Outcome | Precision | Recall | F1-Score | Support |
|---------|-----------|--------|----------|---------|
| Home Win | 0.58 | 0.60 | 0.59 | 2,847 |
| Draw | 0.48 | 0.44 | 0.46 | 1,523 |
| Away Win | 0.57 | 0.59 | 0.58 | 1,948 |

**Feature Importance** (Top 5):
1. `h2h_record`: 11.8%
2. `home_advantage`: 11.0%
3. `home_goal_diff`: 10.2%
4. `away_goal_diff`: 9.8%
5. `home_form`: 9.5%

### Why 55% Accuracy is Good

Football is inherently unpredictable due to:
- Player injuries and form
- Weather conditions
- Tactical decisions
- Referee decisions
- Random events (luck)

Our 55% accuracy significantly outperforms:
- Random guessing: 33.3% (3 outcomes)
- Baseline (always predict home win): 45%
- Many professional tipsters: 50-52%

---

## 🎥 Demo Video

**Duration**: 3 minutes  
**Content**:
1. Problem statement and solution overview (30s)
2. Match Predictor demonstration (60s)
3. Team Statistics dashboard (45s)
4. Head-to-Head analysis (45s)

[Link to demo video will be added]

---

## 🤝 IBM Technologies Used

### IBM watsonx.ai
- **Model**: Llama 3.3 70B Instruct
- **Purpose**: Generate plain-English explanations for predictions
- **Region**: EU (Frankfurt)
- **API**: Watson Machine Learning v1

### IBM Watson Machine Learning
- **Service**: Model deployment and inference
- **Features**: Real-time predictions, model versioning
- **Integration**: Python SDK (ibm-watsonx-ai)

### Why IBM watsonx.ai?

1. **State-of-the-art LLM**: Llama 3.3 70B provides high-quality explanations
2. **Enterprise-grade**: Reliable, scalable, and secure
3. **Easy Integration**: Python SDK with excellent documentation
4. **Cost-effective**: Pay-per-use pricing model
5. **EU Data Residency**: Data stays in Europe for GDPR compliance

---

## 📈 Future Enhancements

### Short-term (Next 3 months)
- [ ] Add player-level statistics
- [ ] Implement real-time match tracking
- [ ] Add more visualization options
- [ ] Support for club football predictions
- [ ] Mobile-responsive design improvements

### Medium-term (6 months)
- [ ] Multi-language support
- [ ] User accounts and saved predictions
- [ ] Social sharing features
- [ ] API for third-party integrations
- [ ] Advanced filtering and search

### Long-term (1 year)
- [ ] Live match commentary with AI
- [ ] Fantasy football integration
- [ ] Betting odds comparison
- [ ] Mobile app (iOS/Android)
- [ ] Community features and forums

---

## 🐛 Known Issues

1. **Unicode Display**: Some emojis may not display correctly in Windows console
2. **Model Loading Time**: Initial load takes 5-10 seconds (cached afterwards)
3. **API Rate Limits**: IBM watsonx.ai has rate limits for free tier
4. **Large Dataset**: Full dataset is 15MB (may take time to load)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Thammandra Saketh Ram**  
IBM SkillsBuild AI Builders Challenge - June 2026

- GitHub: [@Sakethram2005](https://github.com/Sakethram2005)
- LinkedIn: [](https://www.linkedin.com/in/thammandra-saketh-ram-7b1590321/).
- Email: saketh123.indus@gmail.com

---

## 🙏 Acknowledgments

- **IBM SkillsBuild** for organizing the AI Builders Challenge
- **IBM watsonx.ai** for providing access to Llama 3.3 70B
- **Kaggle** for the international football results dataset
- **Streamlit** for the amazing web framework
- **scikit-learn** for machine learning tools
- **Plotly** for interactive visualizations

---

## 📚 References

1. [IBM watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
2. [Streamlit Documentation](https://docs.streamlit.io/)
3. [scikit-learn Documentation](https://scikit-learn.org/stable/)
4. [International Football Results Dataset](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017)
5. [RandomForest Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)

---

## 📞 Support

For questions or issues:
1. Check the [documentation](docs/)
2. Search [existing issues](https://github.com/yourusername/football-fan-hub/issues)
3. Create a [new issue](https://github.com/yourusername/football-fan-hub/issues/new)
4. Contact the author

---

<div align="center">

**⚽ Made with ❤️ for football fans worldwide**

*Powered by IBM watsonx.ai | Built with Streamlit | Trained on 154 years of football history*

</div>
