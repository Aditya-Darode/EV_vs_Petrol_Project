import pandas as pd
from pytrends.request import TrendReq

# Connect to Google Trends
pytrends = TrendReq(hl='en-US', tz=330)

# Define search keywords
kw_list = ["Electric Cars", "Petrol Cars"]

# Build payload
pytrends.build_payload(kw_list, timeframe='2019-01-01 2025-08-29', geo='IN', gprop='')

# Interest over time
df_trends = pytrends.interest_over_time()
df_trends.to_csv("ev_vs_petrol_india_timeseries.csv")
print("Time-series CSV generated:", df_trends.head())

# Interest by region (state-wise)
region = pytrends.interest_by_region(resolution="REGION", inc_low_vol=True)
region.to_csv("ev_vs_petrol_india_regions.csv")
print("Region-wise CSV generated:", region.head())



"""
extract_data.py
---------------
Purpose:
This script is responsible for the **data collection phase** of the project. 
We use the PyTrends library (an unofficial Google Trends API) to programmatically 
fetch search interest data for keywords "Electric Cars" and "Petrol Cars" in India.

Why we are using this file:
- To automate the collection of real-world data instead of using pre-existing datasets.
- It ensures the project demonstrates **end-to-end capability**: from raw data extraction → analysis → visualization.
- The script generates two key CSV files that act as the foundation for the entire analysis:
    1. ev_vs_petrol_india_timeseries.csv → search interest over time (monthly/weekly trends)
    2. ev_vs_petrol_india_regions.csv → search interest broken down by Indian states/regions
- By including this file, we show recruiters that the dataset was not “taken from somewhere”, 
  but rather programmatically collected from Google Trends using Python.

In short:
This file proves you can **source your own data programmatically**, 
which is a critical skill for real-world data analysts and engineers.
"""

