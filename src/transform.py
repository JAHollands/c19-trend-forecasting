from pathlib import Path
import pandas as pd 

RAW_PATH = Path("data/raw/raw_c19.csv")
OUT_PATH = Path("data/processed/processed_c19.csv")


def transform():
    df = pd.read_csv(RAW_PATH)

    # daily values from cumulative totals
    df["NewConfirmed"] = df["Confirmed"].diff().fillna(0).clip(lower=0)
    df["NewDeaths"] = df["Deaths"].diff().fillna(0).clip(lower=0)

    # weekly seasonality features
    df["Date"] = pd.to_datetime(df["Date"])
    df["DayOfWeek"] = df["Date"].dt.dayofweek
    df["Lag7_NewConfirmed"] = df["NewConfirmed"].shift(7).fillna(0)

    # modelling frame (next-day prediction)
    df["Lag1_NewConfirmed"] = df["NewConfirmed"].shift(1).fillna(0)
    df["TargetNext_NewConfirmed"] = df["NewConfirmed"].shift(-1)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print("Saved:", OUT_PATH.as_posix())
    return OUT_PATH


if __name__ == "__main__":
    transform()
