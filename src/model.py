import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import OneHotEncoder

PROCESSED_PATH = Path("data/processed/processed_c19.csv")
OUT_PATH = Path("data/processed/preds_c19.csv")

def model(holdout_days: int = 30):
    df = pd.read_csv(PROCESSED_PATH)

    # select modelling cols
    df["Date"] = pd.to_datetime(df["Date"])

    model_df = df[[
        "Date",
        "TargetNext_NewConfirmed",
        "Lag1_NewConfirmed",
        "Lag7_NewConfirmed",
        "DayOfWeek"
    ]].dropna().copy()

    # train test split - hold out last N days for test
    cutoff = model_df["Date"].max() - pd.Timedelta(days=holdout_days)

    train_df = model_df[model_df["Date"] <= cutoff].copy()
    test_df = model_df[model_df["Date"] > cutoff].copy()

    # features and target
    X_train_df = train_df[["Lag1_NewConfirmed", "Lag7_NewConfirmed", "DayOfWeek"]]
    y_train_series = train_df["TargetNext_NewConfirmed"]

    X_test_df = test_df[["Lag1_NewConfirmed", "Lag7_NewConfirmed", "DayOfWeek"]]
    y_test_series = test_df["TargetNext_NewConfirmed"]

    # produce baseline metrics as benchmark
    yhat_naive = test_df["Lag1_NewConfirmed"]

    mae_naive = mean_absolute_error(y_test_series, yhat_naive)
    rmse_naive = np.sqrt(mean_squared_error(y_test_series, yhat_naive))


    # encoding
    Xnum_train = train_df[["Lag1_NewConfirmed", "Lag7_NewConfirmed"]].values
    y_train = y_train_series.values

    Xnum_test = test_df[["Lag1_NewConfirmed", "Lag7_NewConfirmed"]].values
    y_test = y_test_series.values

    ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

    Xohe_train = ohe.fit_transform(train_df[["DayOfWeek"]])
    Xohe_test = ohe.transform(test_df[["DayOfWeek"]])

    # Combine numeric + ohe features
    X_train = np.hstack([Xnum_train, Xohe_train])
    X_test = np.hstack([Xnum_test, Xohe_test])

    # fit model
    lr = LinearRegression()
    lr.fit(X_train, y_train)

    yhat_model = lr.predict(X_test)

    mae_model = mean_absolute_error(y_test, yhat_model)
    rmse_model = np.sqrt(mean_squared_error(y_test, yhat_model))

    # Save predictions
    preds = pd.DataFrame({
        "Date": test_df["Date"],
        "y_true": y_test,
        "yhat_naive": yhat_naive.values,
        "yhat_model": yhat_model,
    })

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    preds.to_csv(OUT_PATH, index=False)

    print("Saved:", OUT_PATH.as_posix())
    print("MAE naive:", round(mae_naive, 2), "| RMSE naive:", round(rmse_naive, 2))
    print("MAE model:", round(mae_model, 2), "| RMSE model:", round(rmse_model, 2))

    return OUT_PATH


if __name__ == "__main__":
    model()