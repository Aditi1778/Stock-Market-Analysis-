import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

def get_stock_data(ticker, timeframe):
    """Fetch stock data using yfinance and return as list of dicts.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL').
        timeframe (str): Timeframe ('1D', '5D', '1M', '3M', '1Y', '5Y', 'YTD', 'Max').
    
    Returns:
        tuple: (list of dicts with stock data, error message or None).
    """
    print(f"DEBUG: Fetching data for ticker: {ticker}, timeframe: {timeframe}")
    timeframes = {'1D': 1, '5D': 5, '1M': 30, '3M': 90, '1Y': 365, '5Y': 1825, 'Max': 10000}
    
    end_date = datetime.now()
    
    if timeframe == 'YTD':
        start_date = datetime(end_date.year, 1, 1)
        days = (end_date - start_date).days
    elif timeframe in timeframes:
        days = timeframes[timeframe]
        start_date = end_date - timedelta(days=days)
    else:
        return None, f"Invalid timeframe: {timeframe}"
    
    try:
        stock = yf.Ticker(ticker)
        # Use period="max" for Max timeframe to fetch all available data
        if timeframe == 'Max':
            df = stock.history(period="max")
        else:
            df = stock.history(start=start_date, end=end_date)
        if df.empty:
            raise ValueError(f"No data found for ticker {ticker}.")
        
        # Convert to list of dicts
        stock_data = []
        for date, row in df.iterrows():
            stock_data.append({
                'date': date,
                'close': float(row['Close']),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'volume': float(row['Volume'])
            })
        stock_data.sort(key=lambda x: x['date'])  # Ensure chronological order
        print(f"DEBUG: Fetched {len(stock_data)} data points")
        return stock_data, None
    except Exception as e:
        print(f"DEBUG: Error in get_stock_data: {str(e)}")
        return None, f"Error fetching data: {str(e)}"

def calculate_technical_indicators(data):
    """Calculate 20-day SMA and RSI using list of dicts.
    
    Args:
        data (list): List of dicts with stock data.
    
    Returns:
        tuple: (updated data, current SMA, current RSI).
    """
    if not data:
        return data, None, None
    
    # Calculate 20-day SMA
    closes = [d['close'] for d in data]
    sma20 = []
    for i in range(len(closes)):
        if i >= 19:
            sma20.append(sum(closes[i-19:i+1]) / 20)
        else:
            sma20.append(None)
    
    # Calculate RSI (14-day)
    rsi = []
    for i in range(len(closes)):
        if i >= 14:
            deltas = [closes[j] - closes[j-1] for j in range(i-13, i+1)]
            gains = [d if d > 0 else 0 for d in deltas]
            losses = [-d if d < 0 else 0 for d in deltas]
            avg_gain = sum(gains) / 14
            avg_loss = sum(losses) / 14
            rs = avg_gain / avg_loss if avg_loss != 0 else float('inf')
            rsi_value = 100 - (100 / (1 + rs)) if rs != float('inf') else 100
            rsi.append(rsi_value)
        else:
            rsi.append(None)
    
    # Add indicators to data
    for i, d in enumerate(data):
        d['sma20'] = sma20[i]
        d['rsi'] = rsi[i]
    
    return data, sma20[-1] if sma20[-1] is not None else None, rsi[-1] if rsi[-1] is not None else None

def analyze_stock(ticker, timeframe):
    """Analyze stock data and provide trading strategies.
    
    Args:
        ticker (str): Stock ticker symbol.
        timeframe (str): Timeframe ('1D', '5D', '1M', '3M', '1Y', '5Y', 'YTD', 'Max').
    
    Returns:
        tuple: (summary text, stock data, error message or None).
    """
    print(f"DEBUG: Entering analyze_stock with ticker: {ticker}, timeframe: {timeframe}")
    valid_timeframes = ['1D', '5D', '1M', '3M', '1Y', '5Y', 'YTD', 'Max']
    if not ticker or not isinstance(ticker, str) or not ticker.strip() or timeframe not in valid_timeframes:
        error_msg = f"Invalid input: Please provide a valid ticker and timeframe ({', '.join(valid_timeframes)})."
        print(f"DEBUG: Returning error: {error_msg}")
        return None, None, error_msg
    
    data, error = get_stock_data(ticker, timeframe)
    if error or not data:
        error_msg = error or "No data available."
        print(f"DEBUG: Returning error: {error_msg}")
        return None, None, error_msg
    
    data, current_sma20, current_rsi = calculate_technical_indicators(data)
    current_price = data[-1]['close']
    closes = [d['close'] for d in data]
    highest_peak = max(closes)
    lowest_peak = min(closes)
    highest_peak_date = next(d['date'].strftime('%Y-%m-%d') for d in data if d['close'] == highest_peak)
    lowest_peak_date = next(d['date'].strftime('%Y-%m-%d') for d in data if d['close'] == lowest_peak)
    price_change_pct = ((current_price - lowest_peak) / lowest_peak) * 100 if len(data) > 1 else 0
    
    # Calculate volatility
    returns = [(closes[i] - closes[i-1]) / closes[i-1] for i in range(1, len(closes))] if len(closes) > 1 else []
    volatility = np.std(returns) * np.sqrt(252) * 100 if returns else 0
    
    # Analysis
    trend = ("bullish" if current_sma20 and current_price > current_sma20 else
             "bearish" if current_sma20 and current_price < current_sma20 else
             "neutral")
    
    if timeframe == '1D' and len(data) < 14:
        sma_status = "SMA not available (insufficient data)."
        rsi_status = "RSI not available (insufficient data)."
    else:
        sma_status = f"20-day SMA: {f'${current_sma20:.2f}' if current_sma20 else 'N/A'}, indicating a {trend} trend."
        rsi_status = f"RSI (14-Day): {f'{current_rsi:.2f}' if current_rsi else 'N/A'}"
    
    long_term_strategy = (
        "Long-term analysis not applicable for 1-day timeframe."
        if timeframe == '1D'
        else f"""
For a {timeframe} horizon, {ticker.upper()}'s outlook depends on fundamentals.
Current price: ${current_price:.2f}, high: ${highest_peak:.2f} on {highest_peak_date}, low: ${lowest_peak:.2f} on {lowest_peak_date}.
{sma_status}
Accumulate on pullbacks to ${current_price * 0.9:.2f} if above long-term averages.
Monitor macro factors like interest rates.
"""
    )
    
    short_term_strategy = (
        f"Short-term ({timeframe}): Limited data for strategy; monitor intraday price at ${current_price:.2f}."
        if timeframe == '1D'
        else f"""
Short-term ({timeframe}), {ticker.upper()} shows a {trend} trend with {rsi_status.lower()}.
{'Overbought (caution).' if current_rsi and current_rsi > 70 else 'Oversold (opportunity).' if current_rsi and current_rsi < 30 else 'Neutral momentum.'}
Target entries near ${current_price * 0.95:.2f}, stop-loss at ${lowest_peak:.2f}.
Breakout above ${highest_peak:.2f} may signal a rally to ${current_price * 1.1:.2f}.
"""
    )
    
    long_term_risk = (
        "Risk analysis not applicable for 1-day timeframe."
        if timeframe == '1D'
        else f"""
Long-term risk for {ticker.upper()} is {'low to moderate' if timeframe in ['5Y', 'Max'] else 'moderate'}.
Volatility: {volatility:.2f}% ({'stable' if volatility < 20 else 'moderate' if volatility < 40 else 'high'}).
Risks: macro shifts, earnings misses. Diversify to mitigate.
"""
    )
    
    short_term_risk = (
        f"Short-term risk: High due to limited data; use tight stop-loss at ${current_price * 0.95:.2f}."
        if timeframe == '1D'
        else f"""
Short-term risk is {'high' if price_change_pct > 20 or volatility > 40 else 'moderate'} (volatility: {volatility:.2f}%).
{'Overbought RSI risks pullback.' if current_rsi and current_rsi > 70 else 'Oversold RSI may reverse.' if current_rsi and current_rsi < 30 else ''}
Monitor news, use stop-loss.
"""
    )
    
    recommendation = (
        f"Monitor {ticker.upper()} closely; insufficient data for robust recommendation."
        if timeframe == '1D'
        else f"""
{'Sell or take profits' if price_change_pct > 20 and (not current_rsi or current_rsi > 70) else 'Buy or accumulate'} {ticker.upper()}.
{'Caution near highs.' if price_change_pct > 20 else 'Bullish near supports.'}
Align with portfolio goals.
"""
    )
    
    summary = f"""
Stock Analysis for {ticker.upper()} ({timeframe})
Current Price: ${current_price:.2f}
Highest Peak: ${highest_peak:.2f} on {highest_peak_date}
Lowest Peak: ${lowest_peak:.2f} on {lowest_peak_date}
{sma_status}
{rsi_status}
Long-term Strategy:
{long_term_strategy}
Short-term Strategy:
{short_term_strategy}
Long-term Risk Analysis:
{long_term_risk}
Short-term Risk Analysis:
{short_term_risk}
Recommendation:
{recommendation}
"""
    print(f"DEBUG: analyze_stock returning summary (len: {len(summary)}), data: {bool(data)}, error: None")
    return summary, data, None

def plot_stock_data(data, ticker, timeframe):
    """Generate multiple plots: price with SMA, volume, RSI, and price range.
    
    Args:
        data (list): List of dicts with stock data.
        ticker (str): Stock ticker symbol.
        timeframe (str): Timeframe.
    
    Returns:
        matplotlib.figure.Figure: Figure with subplots.
    """
    fig = plt.figure(figsize=(15, 12))
    
    # Price and SMA Plot
    ax1 = plt.subplot(4, 1, 1)
    dates = [d['date'] for d in data]
    closes = [d['close'] for d in data]
    sma20 = [d['sma20'] for d in data]
    ax1.plot(dates, closes, label=f'{ticker} Closing Price', color='blue')
    if any(s is not None for s in sma20):
        ax1.plot(dates, sma20, label='20-Day SMA', color='orange', linestyle='--')
    ax1.set_title(f'{ticker.upper()} Stock Price Analysis ({timeframe})')
    ax1.set_ylabel('Price (USD)')
    ax1.grid(True)
    ax1.legend()
    ax1.tick_params(axis='x', rotation=45)
    
    # Volume Plot
    ax2 = plt.subplot(4, 1, 2)
    volumes = [d['volume'] for d in data]
    ax2.bar(dates, volumes, color='gray', alpha=0.5)
    ax2.set_title('Trading Volume')
    ax2.set_ylabel('Volume')
    ax2.grid(True)
    ax2.tick_params(axis='x', rotation=45)
    
    # RSI Plot
    ax3 = plt.subplot(4, 1, 3)
    rsi = [d['rsi'] for d in data]
    ax3.plot(dates, rsi, label='RSI (14-Day)', color='purple')
    ax3.axhline(70, color='red', linestyle='--', alpha=0.5, label='Overbought (70)')
    ax3.axhline(30, color='green', linestyle='--', alpha=0.5, label='Oversold (30)')
    ax3.set_title('Relative Strength Index (RSI)')
    ax3.set_ylabel('RSI')
    ax3.grid(True)
    ax3.legend()
    ax3.tick_params(axis='x', rotation=45)
    
    # Price Range Plot
    ax4 = plt.subplot(4, 1, 4)
    highs = [d['high'] for d in data]
    lows = [d['low'] for d in data]
    opens = [d['open'] for d in data]
    for i, (date, high, low, open_, close) in enumerate(zip(dates, highs, lows, opens, closes)):
        color = 'green' if close >= open_ else 'red'
        ax4.plot([date, date], [low, high], color='black', lw=1)  # High-low range
        ax4.plot([date, date], [open_, close], color=color, lw=3)  # Open-close body
    ax4.set_title('Daily Price Range')
    ax4.set_ylabel('Price (USD)')
    ax4.grid(True)
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    return fig

def plot_pie_chart(data, ticker, timeframe):
    """Generate a pie chart for price movement categories.
    
    Args:
        data (list): List of dicts with stock data.
        ticker (str): Stock ticker symbol.
        timeframe (str): Timeframe.
    
    Returns:
        matplotlib.figure.Figure: Pie chart figure.
    """
    if not data:
        return None
    
    above_sma = sum(1 for d in data if d['sma20'] is not None and d['close'] > d['sma20'])
    below_sma = sum(1 for d in data if d['sma20'] is not None and d['close'] <= d['sma20'])
    overbought = sum(1 for d in data if d['rsi'] is not None and d['rsi'] > 70)
    oversold = sum(1 for d in data if d['rsi'] is not None and d['rsi'] < 30)
    neutral_rsi = sum(1 for d in data if d['rsi'] is not None and 30 <= d['rsi'] <= 70)
    
    labels = ['Above SMA', 'Below SMA', 'Overbought (RSI > 70)', 'Oversold (RSI < 30)', 'Neutral RSI']
    sizes = [above_sma, below_sma, overbought, oversold, neutral_rsi]
    colors = ['#66b3ff', '#ff9999', '#ff66b3', '#66ff99', '#ffd700']
    sizes = [s for s in sizes if s > 0]  # Remove zero counts
    labels = [l for l, s in zip(labels, [above_sma, below_sma, overbought, oversold, neutral_rsi]) if s > 0]
    
    if not sizes:
        print("DEBUG: No data for pie chart categories")
        return None
    
    fig = plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title(f'{ticker.upper()} Price Movement Categories ({timeframe})')
    plt.axis('equal')
    return fig

def main():
    """Run stock analysis from command line."""
    print("Stock Analysis System")
    ticker = input("Enter stock ticker (e.g., AAPL): ").strip().upper()
    timeframe = input("Enter timeframe (1D, 5D, 1M, 3M, 1Y, 5Y, YTD, Max): ").strip().upper()
    
    if not ticker:
        print("Error: Please enter a valid stock ticker.")
        return
    valid_timeframes = ['1D', '5D', '1M', '3M', '1Y', '5Y', 'YTD', 'Max']
    if timeframe not in valid_timeframes:
        print(f"Error: Invalid timeframe. Choose from {', '.join(valid_timeframes)}.")
        return
    
    try:
        summary, data, error = analyze_stock(ticker, timeframe)
        if error:
            print(f"Error: {error}")
            return
        if not data:
            print("Error: No data returned from analysis.")
            return
        
        print(summary)
        
        # Display main plots
        fig = plot_stock_data(data, ticker, timeframe)
        plt.show()
        print("DEBUG: Main plots displayed successfully")
        
        # Display pie chart
        pie_fig = plot_pie_chart(data, ticker, timeframe)
        if pie_fig:
            plt.show()
            print("DEBUG: Pie chart displayed successfully")
        else:
            print("DEBUG: Pie chart not displayed due to insufficient data")
            
    except Exception as e:
        print(f"Error: Analysis failed due to an unexpected issue: {str(e)}")

if __name__ == "__main__":
    main()