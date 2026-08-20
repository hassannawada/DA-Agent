📊 Universal.DA — AI-Powered Data Analytics Platform
Universal.DA is an all-in-one, AI-powered data analytics workspace built with Streamlit. It takes raw data — from a file, a database, or an API — and turns it into cleaned data, statistical insights, visualizations, AI-generated business recommendations, sales forecasts, and downloadable professional reports.
---
✨ Features
📥 Data Ingestion
Upload CSV or Excel files
Connect directly to a MySQL database
Fetch data from any REST API / JSON endpoint
🧬 Data Profiling & Validation
Automatic column type detection (Identifier, Monetary, Date, Category, Name, etc.)
Null percentage and unique value analysis per column
Flags columns with significant missing data
🧹 Data Cleaning
One-click duplicate row removal
Automatic missing value imputation (mean for numeric, mode for categorical)
Automatic date column detection and conversion
IQR-based outlier detection with the ability to inspect and remove outliers per column
📈 Statistics & Correlations
Full descriptive statistics (mean, std, min, max, quartiles)
Correlation matrix with heatmap styling
📊 Dynamic Visualizations
Auto-suggested chart type based on data structure
Bar, Line, Scatter, Pie, Histogram, and Box Plot support
Fully interactive Plotly charts
🤖 AI Business Insights
Powered by Google Gemini
Uses a multi-step "thinking" prompt (business problem → statistical approach → insights) to reduce hallucinations
Generates trends, anomalies, recommendations, and a business conclusion — without sending raw data to the AI (only statistical summaries, for cost efficiency and privacy)
🔮 Sales Forecasting
30-day sales forecast using Scikit-Learn Linear Regression
Automatic detection of date and sales columns
Interactive historical + forecast chart with trend direction
📑 Final Report Generator
One-click HTML report with full analysis, charts, and AI insights
One-click PDF report generation via ReportLab
Both reports are fully downloadable
---
🛠️ Tech Stack
Category	Tools
Frontend / App Framework	Streamlit
Data Handling	Pandas, NumPy
Visualization	Plotly
Machine Learning	Scikit-Learn
AI	Google Gemini (`google-genai`)
Database	SQLAlchemy, MySQL Connector
Reporting	ReportLab (PDF), custom HTML templating
Environment Config	python-dotenv
---
📁 Project Structure
```
Universal.DA/
│
├── app.py                     # Main entry point (routing + UI shell)
├── config.py                  # Page setup, theming, session state
├── requirements.txt
├── .env                       # API keys (not committed to GitHub)
├── .gitignore
│
├── utils/
│   ├── data_loading.py        # File / Database / API ingestion
│   ├── data_profiling.py      # Data profiling + outlier detection
│   └── report_generator.py    # HTML + PDF report generation
│
└── tabs/
    ├── tab_preview.py
    ├── tab_profile.py
    ├── tab_cleaning.py
    ├── tab_stats.py
    ├── tab_correlations.py
    ├── tab_visualizations.py
    ├── tab_ai_insights.py
    ├── tab_forecasting.py
    └── tab_final_report.py
```
---
🚀 Getting Started
1. Clone the repository
```bash
git clone https://github.com/your-username/universal-da.git
cd universal-da
```
2. Create a virtual environment
```bash
python -m venv analyst_env
analyst_env\Scripts\activate      # Windows
source analyst_env/bin/activate   # macOS/Linux
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Add your Gemini API key
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
```
Get a free key at aistudio.google.com/apikey
5. Run the app
```bash
streamlit run app.py
```
---
🔐 Environment Variables
Variable	Description
`GEMINI_API_KEY`	Google Gemini API key used for AI-powered business insights
---
📌 Notes
Only statistical summaries (not raw data) are sent to the AI, keeping the workflow cost-efficient and privacy-conscious.
Outlier detection uses the IQR (Interquartile Range) method.
Forecasting requires at least one recognizable date column and one sales/revenue column.
---
📄 License
This project is open for personal and educational use.
---
🙌 Built With
Streamlit • Pandas • Plotly • Scikit-Learn • Google Gemini • ReportLab
