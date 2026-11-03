# Bitcoin Quantitative Research and Forecasting

## Final Evaluation Report

### 1. Project Overview

This project develops a Python-based quantitative research pipeline to analyse Bitcoin (BTC) using historical market prices and public sentiment from X (Twitter).

The objective is to investigate whether time-based price and sentiment features can help predict Bitcoin price movements over the next one to five hours.

The project also incorporates recent cryptocurrency news for market context and generates visualisations, forecasts and financial performance metrics.

### 2. Technology Stack

* Python
* Pandas and NumPy
* Matplotlib and Seaborn
* Scikit-learn
* Yahoo Finance (historical BTC price data)
* Apify (X/Twitter data collection)
* VADER Sentiment Analysis
* Tavily (news collection)

### 3. Data Collection

**Historical price data:**

* Asset: Bitcoin (BTC-USD)
* Source: Yahoo Finance
* Interval: 1 hour
* Historical coverage: Approximately 60 days
* Observations: 1,432 hourly records

**Social media data:**

* Source: X/Twitter through Apify
* Tweets collected: 1,000
* Language: English
* Features: Tweet text, timestamps, likes, reposts, replies, views and author follower counts.

**News data:**

* Source: Tavily
* Articles collected: 10
* Purpose: Understanding recent market developments and contextualising sentiment.

### 4. Data Processing and Feature Engineering

Tweets were cleaned by removing duplicate records and filtering for English-language content.

VADER was used to calculate:

* Positive sentiment
* Negative sentiment
* Neutral sentiment
* Compound sentiment score

Tweets were grouped into hourly intervals to calculate average sentiment, tweet volume and engagement statistics.

Historical Bitcoin prices were merged with hourly sentiment observations using timestamps.

Price-derived features included:

* 1-hour returns
* 2-hour returns
* 3-hour returns
* 6-hour returns
* 12-hour returns
* 24-hour returns
* 6-hour volatility
* 24-hour volatility

The prediction targets were future hourly returns for horizons n+1 through n+5.

### 5. Model Development

A Random Forest Regressor was implemented separately for each prediction horizon.

The model used:

* 100 decision trees
* Maximum tree depth of 5
* Random state of 42

A chronological 80:20 training-test split was used, with a five-observation gap to reduce overlap between training targets and test observations.

A naive zero-return prediction was used as the baseline.

### 6. Model Evaluation

| Horizon | Random Forest MAE | Random Forest RMSE | Baseline MAE | Baseline RMSE |
| ------- | ----------------: | -----------------: | -----------: | ------------: |
| n+1     |          0.002338 |           0.003516 |     0.002323 |      0.003477 |
| n+2     |          0.003268 |           0.004991 |     0.003238 |      0.004918 |
| n+3     |          0.004030 |           0.006193 |     0.003961 |      0.005979 |
| n+4     |          0.004702 |           0.007087 |     0.004671 |      0.006929 |
| n+5     |          0.005332 |           0.007873 |     0.005232 |      0.007759 |

**Interpretation:**

The Random Forest model did not outperform the naive baseline for any of the five forecasting horizons.

Prediction errors generally increased as the forecasting horizon increased.

This indicates that the implemented model did not demonstrate an improvement over the simple baseline on the available test data.

### 7. Financial Performance

A simple long/short trading strategy was simulated using the one-hour model predictions.

Assumptions:

* Positive prediction: Long position.
* Negative prediction: Short position.
* Transaction cost: 0.05% per unit change in position.

| Metric           |  Result |
| ---------------- | ------: |
| Sharpe Ratio     | -1.4279 |
| Sortino Ratio    | -2.2272 |
| Maximum Drawdown |  -8.52% |

**Interpretation:**

The negative Sharpe and Sortino ratios indicate poor risk-adjusted performance during the test period.

The maximum drawdown of approximately 8.52% represents the largest peak-to-trough decline in the simulated strategy's equity curve.

These are historical simulation results, not live trading performance. Annualised ratios are particularly unstable because the evaluation period is short.

### 8. Future Price Forecasts

The latest available Bitcoin closing price used as the reference was $77,525.

| Horizon | Predicted Price (USD) |
| ------- | --------------------: |
| n+0     |             77,525.00 |
| n+1     |             77,506.77 |
| n+2     |             77,492.88 |
| n+3     |             77,477.83 |
| n+4     |             77,474.96 |
| n+5     |             77,478.17 |

The model produced slightly negative predicted returns across the five forecast horizons, followed by a small recovery at n+5.

These forecasts are experimental and should not be interpreted as reliable market predictions.

### 9. Sentiment and News Analysis

The project incorporated VADER-based sentiment analysis of collected X/Twitter posts and recent Bitcoin news retrieved through Tavily.

The collected news highlighted market uncertainty, security concerns, liquidations and institutional Bitcoin activity.

However, the collected 1,000 tweets covered approximately five hours rather than the intended 180 days.

Furthermore, only four hourly sentiment observations overlapped with the historical Bitcoin price dataset.

Consequently, the available data was insufficient to establish whether social sentiment improves forecasting performance. Sentiment findings are exploratory rather than statistically conclusive.

### 10. Limitations

1. The collected social media sample had limited temporal coverage.
2. Only four hourly sentiment observations overlapped with historical price data.
3. The Random Forest model did not outperform the naive baseline.
4. Cryptocurrency markets are highly volatile and influenced by external factors.
5. Financial metrics were calculated using a simplified simulated trading strategy.
6. The short evaluation period limits the reliability of annualised financial metrics.
7. The model has not been tested in a live trading environment.

### 11. Future Improvements

* Collect X/Twitter data across the complete intended historical period.
* Improve hourly alignment between sentiment and market data.
* Investigate additional sentiment aggregation and engagement-weighting methods.
* Conduct more extensive walk-forward validation.
* Compare additional forecasting algorithms.
* Evaluate whether sentiment features provide measurable improvements over price-only models.
* Introduce reinforcement learning only after establishing a reliable supervised forecasting baseline.
* Improve transaction-cost and risk-management modelling.

### 12. Conclusion

This project demonstrates an end-to-end quantitative research workflow involving social media data collection, sentiment analysis, historical market data processing, feature engineering, machine learning, financial evaluation and forecasting.

Although the implemented Random Forest model did not outperform the naive baseline, the experiment highlights the challenges of short-term cryptocurrency forecasting and the importance of rigorous out-of-sample evaluation.

The project also identifies an important data limitation: insufficient historical overlap between social sentiment and market prices. Addressing this limitation is essential before drawing conclusions about the predictive value of social media sentiment.
