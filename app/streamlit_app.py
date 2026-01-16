from pathlib import Path
import sys

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

PROCESSED_PATH = Path("data/processed/processed_c19.csv")
PREDS_PATH = Path("data/processed/preds_c19.csv")

# Function to load required data
def load_data():
    df_processed = pd.read_csv(PROCESSED_PATH)
    df_preds = pd.read_csv(PREDS_PATH)

    df_processed = df_processed.sort_values("Date")
    df_preds = df_preds.sort_values("Date")

    return df_processed, df_preds

# Function to compute metrics
def metrics(df_preds_slice: pd.DataFrame):
    mae_bl = (df_preds_slice["y_true"] - df_preds_slice["yhat_naive"]).abs().mean()
    mae_model = (df_preds_slice["y_true"] - df_preds_slice["yhat_model"]).abs().mean()

    rmse_bl = np.sqrt(((df_preds_slice["y_true"] - df_preds_slice["yhat_naive"]) ** 2).mean())
    rmse_model = np.sqrt(((df_preds_slice["y_true"] - df_preds_slice["yhat_model"]) ** 2).mean())

    return mae_bl, rmse_bl, mae_model, rmse_model

# Streamlit app configuration
st.set_page_config(page_title="C19 Trend Forecasting", layout="wide")
st.title("C19 Trend Forecasting Dashboard")
st.caption("C19 Pipeline")

# Load data
df_processed, df_preds = load_data()

# Sidebar controls
st.sidebar.header("Filters")

df_preds["Date"] = pd.to_datetime(df_preds["Date"], errors="coerce")

min_date = df_preds["Date"].dt.date.min()
max_date = df_preds["Date"].dt.date.max()

date_range = st.sidebar.date_input(
    "Holdout date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

mask = (df_preds["Date"].dt.date >= start_date) & (df_preds["Date"].dt.date <= end_date)
df_preds_slice = df_preds.loc[mask].copy()

# Metrics
mae_b, rmse_b, mae_m, rmse_m = metrics(df_preds_slice)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Baseline MAE", f"{mae_b:,.0f}")
col2.metric("Baseline RMSE", f"{rmse_b:,.0f}")
col3.metric("Model MAE", f"{mae_m:,.0f}")
col4.metric("Model RMSE", f"{rmse_m:,.0f}")

st.divider()

# Actual vs predictions
st.subheader("Actual vs Predictions")

fig = plt.figure(figsize=(12, 5))
plt.plot(df_preds_slice["Date"], df_preds_slice["y_true"], label="Actual")
plt.plot(df_preds_slice["Date"], df_preds_slice["yhat_naive"], label="Baseline (Lag1)")
plt.plot(df_preds_slice["Date"], df_preds_slice["yhat_model"], label="Linear Regression")
plt.xlabel("Date")
plt.ylabel("Next day cases")
plt.legend()
plt.tight_layout()
st.pyplot(fig)

# Weekly seasonality from processed dataset
st.subheader("Weekly Seasonality (Average NewConfirmed by Day of Week)")

dow_map = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
dow_avg = (
    df_processed.groupby("DayOfWeek")["NewConfirmed"]
    .mean()
    .reindex(range(7))
)

fig2 = plt.figure(figsize=(8, 4))
plt.bar([dow_map[i] for i in dow_avg.index], dow_avg.values)
plt.xlabel("Day of Week")
plt.ylabel("Avg cases")
plt.tight_layout()
st.pyplot(fig2)

st.divider()

st.subheader("Summary")
st.write(
    f"""
- The linear regression model reduces error compared with the baseline.
- On the selected date range, baseline MAE is **{mae_b:,.0f}** vs model MAE **{mae_m:,.0f}**.
- This suggests weekly seasonality and recent momentum add useful signal beyond “tomorrow equals today”.
"""
)