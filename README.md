# Bitcoin Quantitative Research & Forecasting

An end-to-end quantitative research project exploring short-term Bitcoin price forecasting using historical market data and social media sentiment.

## Project Overview

This project investigates Bitcoin (BTC) price movements over the next one to five hours using Python-based data processing and machine learning.

The pipeline includes:

* X/Twitter data collection using Apify.
* Bitcoin historical price collection using Yahoo Finance.
* Sentiment analysis using VADER.
* Hourly sentiment aggregation.
* Historical price and sentiment alignment.
* Time-based feature engineering.
* Random Forest forecasting.
* Financial performance evaluation.
* Bitcoin news collection using Tavily.
* Data visualisation and sentiment reporting.

## Technology Stack

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* VADER Sentiment
* Apify
* Tavily
* yfinance

## Project Structure

```text
BTC_Quant_Research/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── reports/
│   ├── model_evaluation.csv
│   ├── financial_metrics.csv
│   ├── btc_forecast.csv
│   ├── sentiment_outlook.md
│   └── final_evaluation_report.md
│
├── src/
│   ├── inspect_data.py
│   ├── download_prices.py
│   ├── process_tweets.py
│   ├── merge_data.py
│   ├── train_model.py
│   ├── predict_future.py
│   ├── visualize_results.py
│   ├── fetch_news.py
│   └── create_sentiment_report.py
│
├── .env
├── .gitignore
└── README.md
```

## Methodology

### 1. Data Collection

Historical BTC-USD hourly prices were collected using Yahoo Finance. Public X/Twitter posts were collected using Apify, while recent cryptocurrency news was retrieved using Tavily.

### 2. Sentiment Analysis

VADER was used to calculate positive, negative, neutral and compound sentiment scores for collected tweets.

### 3. Feature Engineering

Price-based features included historical returns and rolling volatility. Tweet sentiment and engagement statistics were aggregated hourly.

### 4. Machine Learning

Random Forest regression models were developed for five forecasting horizons, from n+1 to n+5 hours.

A naive zero-return model was used as the baseline.

### 5. Evaluation

Models were evaluated using:

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)

A simulated trading strategy was also evaluated using:

* Sharpe Ratio
* Sortino Ratio
* Maximum Drawdown

## Key Results

The Random Forest model did not outperform the naive zero-return baseline across the five forecasting horizons.

The simulated trading strategy produced:

| Metric           |  Result |
| ---------------- | ------: |
| Sharpe Ratio     | -1.4279 |
| Sortino Ratio    | -2.2272 |
| Maximum Drawdown |  -8.52% |

These results demonstrate the importance of baseline comparisons and out-of-sample evaluation in quantitative research.

## Important Data Limitations

The collected 1,000 tweets covered approximately five hours rather than the intended 180 days.

Only four hourly sentiment observations overlapped with the historical Bitcoin price dataset.

Therefore, the available data was insufficient to establish whether social media sentiment improves predictive performance.

The results should be interpreted as an exploratory experiment rather than a production-ready forecasting system.

## Running the Project

Create and activate a Python virtual environment, then install the required dependencies.

```bash
pip install pandas numpy matplotlib seaborn scikit-learn yfinance vaderSentiment python-dotenv requests
```

Create a `.env` file in the project root and configure your Tavily API key.

Run the Python scripts from the project root in the appropriate order:

1. `python src/download_prices.py`
2. `python src/process_tweets.py`
3. `python src/merge_data.py`
4. `python src/train_model.py`
5. `python src/predict_future.py`
6. `python src/visualize_results.py`
7. `python src/fetch_news.py`
8. `python src/create_sentiment_report.py`

The tweet processing step requires the collected Apify JSON dataset in `data/raw/` with the expected filename.

## Disclaimer

This project is developed for educational and quantitative research purposes. Forecasts and simulated financial metrics are not investment advice or guarantees of future performance.
