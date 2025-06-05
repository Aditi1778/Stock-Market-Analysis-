# Stock-Market-Analysis 


Stock-Analyzer
A command-line Python application for stock market analysis, providing detailed technical analysis, trading recommendations, and real-time visualizations using yfinance for stock data retrieval.
Overview
Stock-Analyzer fetches historical stock data for user-specified tickers and timeframes, computes technical indicators (20-day SMA, 14-day RSI, volatility), and generates comprehensive summaries with long-term and short-term strategies, risk assessments, and buy/sell recommendations. The application includes rich visualizations, such as price, volume, RSI, price range plots, and a pie chart for price movement categories, to aid decision-making.
Features

User Inputs: Accepts stock ticker (e.g., AAPL) and timeframe (1D, 5D, 1M, 3M, 1Y, 5Y, YTD, Max).
Technical Analysis:
20-day Simple Moving Average (SMA) for trend identification.
14-day Relative Strength Index (RSI) for momentum assessment.
Volatility calculation for risk evaluation.


Trading Insights:
Long-term and short-term strategies with entry/exit points.
Risk assessments based on volatility and RSI signals.
Buy/sell recommendations tailored to price trends.


Visualizations:
Price and SMA line plot.
Volume bar chart.
RSI plot with overbought/oversold thresholds.
Daily price range (candlestick-like) plot.
Pie chart summarizing price movement categories (above/below SMA, RSI conditions).


Data Source: Uses yfinance for reliable, rate-limit-free stock data, avoiding API key issues (e.g., compared to Alpha Vantage).
Robustness: Handles errors gracefully with debug logging and supports minimal data cases (e.g., 1D timeframe).

Prerequisites

Python 3.8+
Required libraries:
yfinance
numpy
matplotlib



Installation

Clone the Repository:
git clone https://github.com/your-username/Stock-Analyzer.git
cd Stock-Analyzer


Set Up a Virtual Environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install yfinance numpy matplotlib



Usage

Run the Application:
python stock_analyzer.py


Provide Inputs:

Enter a stock ticker (e.g., AAPL for Apple Inc.).
Select a timeframe (1D, 5D, 1M, 3M, 1Y, 5Y, YTD, Max).


View Outputs:

Console: Detailed analysis summary, including:
Current price, highest/lowest peaks.
SMA, RSI, and volatility metrics.
Long-term and short-term strategies and risks.
Buy/sell recommendation.


Visualizations:
First window: Four subplots (price/SMA, volume, RSI, price range).
Second window: Pie chart of price movement categories (if sufficient data).





Example
Stock Analysis System
Enter stock ticker (e.g., AAPL): AAPL
Enter timeframe (1D, 5D, 1M, 3M, 1Y, 5Y, YTD, Max): 1M
DEBUG: Fetching data for ticker: AAPL, timeframe: 1M
DEBUG: Fetched 22 data points
[Analysis summary printed]
[Matplotlib windows display plots]

Project Structure
Stock-Analyzer/
├── stock_analyzer.py  # Main script with analysis and visualization logic
├── README.md          # Project documentation
└── venv/              # Virtual environment (not tracked)

Notes

1D Timeframe: Limited data may result in no SMA/RSI calculations or pie chart. Analysis is simplified to focus on intraday price.
YTD: Dynamically fetches data from January 1 of the current year (e.g., Jan 1, 2025, as of June 5, 2025).
Max: Retrieves all available historical data for the ticker (e.g., since 1980 for AAPL).
Troubleshooting:
Ensure internet connectivity for yfinance.
If plots don’t display, add the following to stock_analyzer.py:import matplotlib
matplotlib.use('TkAgg')


Update dependencies: pip install --upgrade yfinance numpy matplotlib.


Comparison with Alpha Vantage: Evaluated Alpha Vantage API but chose yfinance due to no rate limits and simpler setup, avoiding issues like 5 calls/minute restrictions.

Future Enhancements

Integrate additional technical indicators (e.g., MACD, Bollinger Bands).
Support intraday data for 1D timeframe.
Explore financial LLMs (e.g., FinGPT) for advanced trading insights.
Develop a web-based UI (e.g., Streamlit) for broader accessibility.
Export analysis to PDF or CSV for reporting.

Contributing
Contributions are welcome! Please:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m 'Add your feature').
Push to the branch (git push origin feature/your-feature).
Open a pull request.



Built with yfinance for stock data and matplotlib for visualizations.
Inspired by the need for accessible, rate-limit-free stock analysis tools.
Developed as part of a stock market analysis project, with iterative improvements based on user feedback.

