import pandas as pd
from pathlib import Path

URL = "https://raw.githubusercontent.com/datasets/covid-19/refs/heads/main/data/worldwide-aggregate.csv"
OUT_PATH = Path("data/raw/raw_c19.csv")

EXPECTED_COLS = {"Date", "Confirmed", "Recovered", "Deaths", "Increase rate"}

def extract():
    df = pd.read_csv(URL)

    # check for expected columns
    assert EXPECTED_COLS.issubset(df.columns), f"Missing cols: {EXPECTED_COLS - set(df.columns)}"

    # parse dates
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # fix the null value in increase rate col
    df["Increase rate"] = df["Increase rate"].fillna(0)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print("Saved: ", OUT_PATH.as_posix())
    return OUT_PATH

if __name__ == "__main__":
    extract()