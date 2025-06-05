# Stock-Analyzer

A command-line Python application for stock market analysis, providing detailed technical analysis, trading recommendations, and real-time visualizations using yfinance for stock data retrieval.

## Overview

Stock-Analyzer fetches historical stock data for user-specified tickers and timeframes, computes technical indicators (20-day SMA, 14-day RSI, volatility), and generates comprehensive summaries with long-term and short-term strategies, risk assessments, and buy/sell recommendations. The application includes rich visualizations, such as price, volume, RSI, price range plots, and a pie chart for price movement categories, to aid decision-making.

## Features

- User Inputs: Accepts stock ticker (e.g., AAPL) and timeframe (1D, 5D, 1M, 3M, 1Y, 5Y, YTD, Max).
- Technical Analysis:
  - 20-day Simple Moving Average (SMA) for trend identification.
  - 14-day Relative Strength Index (RSI) for momentum assessment.
  - Volatility calculation for risk evaluation.
- Trading Insights:
  - Long-term and short-term strategies with entry/exit points.
  - Risk assessments based on volatility and RSI signals.
  - Buy/sell recommendations tailored to price trends.
- Visualizations:
  - Price and SMA line plot.
  - Volume bar chart.
  - RSI plot with overbought/oversold thresholds.
  - Daily price range (candlestick-like) plot.
  - Pie chart summarizing price movement categories (above/below SMA, RSI conditions).
- Data Source: Uses yfinance for reliable, rate-limit-free stock data, avoiding API key issues (e.g., compared to Alpha Vantage).
- Robustness: Handles errors gracefully with debug logging and supports minimal data cases (e.g., 1D timeframe).

## Prerequisites

- Python 3.8+
- Required libraries:
  - yfinance
  - numpy
  - matplotlib

## Installation

1. Clone the Repository:
   ```bash
   git clone https://github.com/Aditi1778/Stock-Market-Analysis.git
   cd Stock-Analyzer
