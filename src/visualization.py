import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ------------------------------
# Define base directories
# ------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

# Ensure results folder exists
os.makedirs(RESULTS_DIR, exist_ok=True)

# ------------------------------
# 1. Load CSVs
# ------------------------------
df_trends = pd.read_csv(os.path.join(DATA_DIR, "ev_vs_petrol_india_timeseries.csv"), parse_dates=['date'])
df_states = pd.read_csv(os.path.join(DATA_DIR, "ev_vs_petrol_india_regions.csv"))
df_yoy = pd.read_csv(os.path.join(DATA_DIR, "ev_vs_petrol_yoy.csv"))

# Clean column names for consistency
df_trends.columns = df_trends.columns.str.strip().str.lower().str.replace(" ", "_")
df_states.columns = df_states.columns.str.strip().str.lower().str.replace(" ", "_")
df_yoy.columns = df_yoy.columns.str.strip().str.lower().str.replace(" ", "_")

# ------------------------------
# 2. Monthly Trends Line Chart
# ------------------------------
plt.figure(figsize=(12,6))
plt.plot(df_trends['date'], df_trends['electric_cars'], label='Electric Cars', color='green', linewidth=2, marker="o")
plt.plot(df_trends['date'], df_trends['petrol_cars'], label='Petrol Cars', color='red', linewidth=2, marker="o")
plt.title('Electric vs Petrol Cars - Trend (India)', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Cars', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "ev_vs_petrol_trends.png"))
print(" Saved:", os.path.join(RESULTS_DIR, "ev_vs_petrol_trends.png"))
plt.close()

# ------------------------------
# 3. Top States by EV Interest Bar Chart
# ------------------------------
top_states = df_states.sort_values(by='electric_cars', ascending=False).head(10)
plt.figure(figsize=(10,6))
plt.bar(top_states['geoname'], top_states['electric_cars'], color='green')
plt.title('Top 10 States by EV Adoption', fontsize=16)
plt.xlabel('State', fontsize=12)
plt.ylabel('EV Count', fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "top_states_ev.png"))
print(" Saved:", os.path.join(RESULTS_DIR, "top_states_ev.png"))
plt.close()

# ------------------------------
# 4. Year-over-Year Growth
# ------------------------------
plt.figure(figsize=(10,6))
width = 0.35
x = df_yoy['year']
plt.bar(x - width/2, df_yoy['ev_yoy_pct'], width, label='EV YoY %', color='green')
plt.bar(x + width/2, df_yoy['petrol_yoy_pct'], width, label='Petrol YoY %', color='red')
plt.title('Year-over-Year Growth % - EV vs Petrol', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('YoY % Change', fontsize=12)
plt.xticks(x)
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "ev_vs_petrol_yoy.png"))
print(" Saved:", os.path.join(RESULTS_DIR, "ev_vs_petrol_yoy.png"))
plt.close()


"""
visualization.py
----------------
Purpose:
This script generates **static visualizations (PNG charts)** using Matplotlib. 
It complements the interactive Streamlit dashboard by creating images that can be 
embedded into README.md, LinkedIn posts, or presentations.

Charts Generated:
1. EV vs Petrol trends over time (line chart)
2. Top 10 states by EV adoption (bar chart)
3. Year-over-Year growth comparison (bar chart)

Why:
- Streamlit is great for live dashboards, but static PNGs are needed for reports, 
  resumes, and GitHub READMEs.
- This demonstrates ability to create **publication-ready static charts**, 
  making the project portfolio-friendly and professional.
"""
