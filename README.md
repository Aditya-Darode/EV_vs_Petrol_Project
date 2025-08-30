#  EV vs Petrol Cars in India – Data Analytics Project

## Project Overview
This project analyzes **Electric Vehicles (EVs) vs Petrol Cars adoption trends in India (2019–2025)** using real-world **Google Trends data**.  
It demonstrates end-to-end **data collection → processing → visualization → forecasting**, making it a portfolio-ready analytics project.  

Key highlights:
-  Trend analysis of EV vs Petrol search interest (time-series)
-  State-wise adoption share
-  Year-over-Year (YoY) growth patterns
-  Forecast of EV adoption till 2030 (using Prophet)
-  Interactive dashboard for exploration (Streamlit)

---

##  Live Demo
 [Streamlit Dashboard](https://evvspetrolproject-mjmgczbno7fdstqqewud96.streamlit.app)

---

##  Project Structure
```bash
EV_vs_Petrol_Project/
│
├── data/               # Raw and processed CSV files
│   ├─ ev_vs_petrol_india_timeseries.csv
│   ├─ ev_vs_petrol_india_regions.csv
│   └─ ev_vs_petrol_yoy.csv
│
├── results/            # Generated PNG visualizations
│   ├─ ev_vs_petrol_trends.png
│   ├─ ev_vs_petrol_yoy.png
│   └─ top_states_ev.png
│
├── src/                # Python scripts
│   ├─ extract_data.py        # Collects Google Trends data (Pytrends)
│   ├─ visualization.py       # Generates static charts (Matplotlib)
│   └─ streamlit_app.py       # Interactive dashboard (Streamlit)
│
├── queries.sql         # BigQuery SQL for YoY and aggregated analysis
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation


