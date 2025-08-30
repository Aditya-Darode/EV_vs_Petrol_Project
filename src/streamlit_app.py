import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px
from prophet import Prophet

# ------------------------------
# Define base directories
# ------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ---------- Helper: clean column names ----------
def clean_columns(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

# ---------- Load Data ----------
df_timeseries = clean_columns(pd.read_csv(os.path.join(DATA_DIR, "ev_vs_petrol_india_timeseries.csv")))
df_regions = clean_columns(pd.read_csv(os.path.join(DATA_DIR, "ev_vs_petrol_india_regions.csv")))
df_yoy = clean_columns(pd.read_csv(os.path.join(DATA_DIR, "ev_vs_petrol_yoy.csv")))

# ------------------------------
# Streamlit App Config
# ------------------------------
st.set_page_config(page_title="EV vs Petrol Cars Dashboard", layout="wide")
st.title("🚗⚡⛽ EV vs Petrol Cars in India – Interactive Dashboard")

# ========================
# KPI Cards
# ========================
col1, col2, col3 = st.columns(3)

total_ev = df_timeseries["electric_cars"].sum()
total_petrol = df_timeseries["petrol_cars"].sum()
latest_share = round((df_yoy["total_ev"].iloc[-1] /
                     (df_yoy["total_ev"].iloc[-1] + df_yoy["total_petrol"].iloc[-1])) * 100, 2)

col1.metric("⚡ Total EVs", f"{total_ev:,}")
col2.metric("⛽ Total Petrol Cars", f"{total_petrol:,}")
col3.metric("📊 Latest EV Share (%)", f"{latest_share}%")

# ========================
# Sidebar Filters
# ========================
st.sidebar.header("🔎 Filters")

df_timeseries["date"] = pd.to_datetime(df_timeseries["date"])
df_timeseries["year"] = df_timeseries["date"].dt.year

date_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df_timeseries["year"].min()),
    max_value=int(df_timeseries["year"].max()),
    value=(int(df_timeseries["year"].min()), int(df_timeseries["year"].max()))
)

selected_region = st.sidebar.selectbox(
    "Select Region",
    options=["All"] + sorted(df_regions["geoname"].unique().tolist())
)

metrics = st.sidebar.multiselect(
    "Select Metrics to Display",
    ["electric_cars", "petrol_cars"],
    default=["electric_cars", "petrol_cars"]
)

# Filter timeseries
df_filtered = df_timeseries[(df_timeseries["year"] >= date_range[0]) & (df_timeseries["year"] <= date_range[1])]

# ========================
# Chart 1: Timeseries Trend
# ========================
st.subheader("📈 EV vs Petrol Adoption Over Time")
fig1, ax1 = plt.subplots(figsize=(10, 5))
colors = {"electric_cars": "green", "petrol_cars": "red"}
df_filtered.plot(kind="line", x="date", y=metrics, ax=ax1, marker="o", color=[colors[m] for m in metrics])
ax1.set_ylabel("Number of Cars")
ax1.set_title("EV vs Petrol Cars Over Time")
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig1)

# ========================
# Chart 2: Regional Adoption
# ========================
st.subheader("🌍 Regional EV vs Petrol Adoption")

df_regions["ev_share"] = (df_regions["electric_cars"] /
                          (df_regions["electric_cars"] + df_regions["petrol_cars"])) * 100

# 🔹 Apply filter only if a specific state is chosen
if selected_region != "All":
    df_regions_filtered = df_regions[df_regions["geoname"] == selected_region]
else:
    df_regions_filtered = df_regions

# Plot using filtered data
fig2, ax2 = plt.subplots(figsize=(12, 6))
df_regions_filtered.sort_values("ev_share", ascending=False).plot(
    kind="bar", x="geoname", y="ev_share", ax=ax2, color="green", legend=False
)
ax2.set_ylabel("EV Share %")
ax2.set_title("EV Share % by State")
plt.xticks(rotation=90, ha="center")
plt.tight_layout()
st.pyplot(fig2)

# Show filtered table
st.dataframe(df_regions_filtered[["geoname", "electric_cars", "petrol_cars", "ev_share"]]
             .sort_values("ev_share", ascending=False))



# ========================
# Chart 3: Year-over-Year Growth
# ========================
st.subheader("📉 Year-over-Year Growth (%)")
fig3, ax3 = plt.subplots(figsize=(8, 5))
df_yoy.plot(kind="bar", x="year", y=["ev_yoy_pct", "petrol_yoy_pct"], ax=ax3, color=["green", "red"])
ax3.set_ylabel("Growth %")
ax3.set_title("YoY Growth: EV vs Petrol")
plt.xticks(rotation=0)
plt.tight_layout()
st.pyplot(fig3)

# ========================
# Chart 4: EV Share of Total
# ========================
st.subheader("⚡ EV Share of Total Cars (%)")
df_yoy["ev_share_pct"] = (df_yoy["total_ev"] / (df_yoy["total_ev"] + df_yoy["total_petrol"])) * 100
st.line_chart(df_yoy.set_index("year")["ev_share_pct"])

# ========================
# Chart 5: Forecast EV Growth (Prophet)
# ========================
st.subheader("🔮 Forecasting EV Adoption till 2030")

df_forecast = df_timeseries.groupby("year")["electric_cars"].sum().reset_index()
df_forecast = df_forecast.rename(columns={"year": "ds", "electric_cars": "y"})
df_forecast["ds"] = pd.to_datetime(df_forecast["ds"], format="%Y")  # Prophet requires datetime

model = Prophet()
model.fit(df_forecast)

future = model.make_future_dataframe(periods=6, freq="Y")  # predict 6 more years
forecast = model.predict(future)

fig_forecast = px.line(forecast, x="ds", y="yhat", title="EV Adoption Forecast")
st.plotly_chart(fig_forecast, use_container_width=True)

# ========================
# Extra Insights
# ========================
st.subheader("💡 Key Insights")
years = df_forecast["ds"].nunique()
cagr = ((df_forecast["y"].iloc[-1] / df_forecast["y"].iloc[0]) ** (1/years) - 1) * 100

st.write(f"- CAGR (EV): {cagr:.2f}%")
st.write(f"- Top State by EV Share: {df_regions.loc[df_regions['ev_share'].idxmax(), 'geoname']}")
st.write(f"- EV expected to reach ~{int(forecast['yhat'].iloc[-1]):,} units by 2030")

#streamlit run src/streamlit_app.py
