import streamlit as st
from app import analyze_stock, plot_stock_data

st.set_page_config(page_title="Stock Analysis System", layout="wide")

def main():
    st.title("Stock Analysis System")
    st.write("Enter a stock ticker and select a timeframe to view trading strategies and a price chart.")

    # Input section
    col1, col2 = st.columns([1, 1])
    with col1:
        ticker = st.text_input("Stock Ticker", placeholder="e.g., AAPL", value="AAPL").strip().upper()
    with col2:
        timeframe = st.selectbox("Timeframe", options=["1D", "5D", "1M", "3M", "1Y", "5Y", "YTD", "Max"], index=0)

    if st.button("Analyze"):
        with st.spinner("Analyzing..."):
            print(f"DEBUG: Analyzing ticker: {ticker}, timeframe: {timeframe}")
            
            # Validate inputs
            if not ticker:
                st.error("Please enter a valid stock ticker.")
                print(f"DEBUG: Invalid ticker: {ticker}")
                return
            if timeframe not in ["1D", "5D", "1M", "3M", "1Y", "5Y", "YTD", "Max"]:
                st.error("Please select a valid timeframe.")
                print(f"DEBUG: Invalid timeframe: {timeframe}")
                return
            
            # Run analysis
            try:
                summary, data, error = analyze_stock(ticker, timeframe)
                print(f"DEBUG: analyze_stock result - summary: {summary is not None}, data: {data is not None}, error: {error}")
                
                if error:
                    st.error(f"Error: {error}")
                    print(f"DEBUG: Error from analyze_stock: {error}")
                    return
                if not data:
                    st.error("Error: No data returned from analysis.")
                    print(f"DEBUG: No data returned")
                    return
                
                # Display results
                st.subheader("Analysis Results")
                st.text_area("Summary", summary, height=400)
                
                # Generate and display chart
                chart = plot_stock_data(data, ticker, timeframe)
                st.pyplot(chart)
                print(f"DEBUG: Chart displayed successfully")
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                print(f"DEBUG: Exception in analysis: {str(e)}")

if __name__ == "__main__":
    main()