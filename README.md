# c19-trend-forecasting (module 14 assessment)

This repo demonstrates an end to end time series pipeline for the module 14 assessment:
- Extract c19 time series dataset
- Build a small feature layer
- Train a basic model and evaluate against a baseline
- Visualise results in a Streamlit dashboard

Hosted Streamlit app: https://c19-trend-forecasting-mod14.streamlit.app/

## How to run this locally on windows:

### 1. Clone the repo locally
- Clone from github to local file storage

### 2. Run 'run.ps1'
- Creates a virtual environment in .venv if one does not already exist
- Installs the required packages from requirements.txt file in the repo
- Runs the pipeline
- Generates file outputs in both raw and processed folders locally (updated data if available)

## Project report

### Design
This solution is designed to be a simple, sequential pipeline with four distinct layers.

1. Extract:
- Downloads the data from the source
- Performs some validation and small transformations
- Saves the data locally

2. Transform:
- Builds features for time series forecasting
- Converts cumulative totals into daily values, then producing some lag and seasonality featutres to support next day predictions 
- Saves the processed dataset locally

Feature details:
- `NewConfirmed`: daily new cases derived from differences in cumulative confirmed totals
- `DayOfWeek`: simple weekly seasonality signal
- `Lag1_NewConfirmed`: yesterday’s daily new cases
- `Lag7_NewConfirmed`: value from 7 days ago to capture weekly pattern
- `TargetNext_NewConfirmed`: next day target value for supervised learning

3. Model:
- Trains and evaluates two different models on a holdout set of data (last 30 days)
    - Baseline: yesterdays value = todays value
    - Linear regression: uses lag features and one hot encoded days of the week
- Evaluation metrics:
    - MAE (average error)
    - RMSE (average error but higher penalty for larger misses)
- Outputs predictons for the holdout period and saves locally

4. Visualisation:
- Loads the processed dataset and predictions
- Visualises:
    - trend
    - weekly seasonality
    - actuals vs predicted values
- Displays baseline vs model metrics for comparison

Orchestration:
- `pipeline.py` runs each python module in the required order
- `run.ps1` builds the required environment and runs the pipeline

### Challenges

#### Environment consistency and dependencies:
The main challenge was ensuring the pipeline would run reliably from a fresh starting point on a Windows machine regardless of what had already been installed. I encountered this problem as I developed this across multiple devices with the repo cloned locally. This was solved by developing the `run.ps1` script which creates a virtual environment and installs dependencies from `requirements.txt` before running the pipeline. This made the project reproducible and removed reliance on existing local environments.

#### Time series behaviour
The dataset has large regime shifts which limits how well a simple model can generalise and is why a strong baseline comparison is useful.

#### Weekly reporting effects
The data shows clear weekly seasonality, likely influenced by reporting behaviour. Including a simple `DayOfWeek` feature helped the model capture part of that pattern.

### Insights and findings
- The covid-19 series changes significantly over time, with distinct spikes or waves of increased reporting. This makes the task difficult for simple models because the underlying process is not consistent/ stable.
- There is clear weekly seasonality, suggesting consistent reporting across the week.
- The linear regression model improved on the baseline approach during the holdout period:
  - Baseline MAE was approximately 387k cases per day vs around 294k for the linear regression model (about a 24% improvement).
  - Baseline RMSE was approximately 467k vs around 346k for the model (about a 26% improvement).
- This suggests that even a basic feature set (recent lag + weekly seasonality) can capture useful signal beyond our baseline naive tomorrow = today forecast.
- Limitations:
  - The model is intentionally simple due to time constraints.
  - Further work could include additional lags, rolling averages, alternative horizons, or intoroduction of more specialised time series forecasting methods.