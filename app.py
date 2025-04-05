from flask import Flask, render_template, jsonify
import yfinance as yf
import pandas as pd
import time

app = Flask(__name__)

def get_nifty50_stocks():
    return [
        "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "HINDUNILVR.NS",
        "SBIN.NS", "BAJFINANCE.NS", "BHARTIARTL.NS", "KOTAKBANK.NS", "HDFC.NS", "ITC.NS",
        "LT.NS", "ASIANPAINT.NS", "AXISBANK.NS", "MARUTI.NS", "TITAN.NS", "ULTRACEMCO.NS",
        "WIPRO.NS", "SUNPHARMA.NS", "INDUSINDBK.NS", "ONGC.NS", "NTPC.NS", "POWERGRID.NS",
        "TATASTEEL.NS", "NESTLEIND.NS", "TECHM.NS", "JSWSTEEL.NS", "HCLTECH.NS",
        "COALINDIA.NS", "ADANIPORTS.NS"
    ]

def fetch_stock_data(stock):
    try:
        ticker = yf.Ticker(stock)
        data = ticker.history(period='14d')
        
        if data.empty or 'Close' not in data.columns:
            stock_alt = stock.replace(".NS", ".BO")
            ticker = yf.Ticker(stock_alt)
            data = ticker.history(period='14d')
            
            if data.empty or 'Close' not in data.columns:
                return None
        
        return {
            'symbol': stock.replace(".NS", ""),
            'lastPrice': round(data['Close'].iloc[-1], 2),
            'dayHigh': round(data['High'].iloc[-1], 2),
            'dayLow': round(data['Low'].iloc[-1], 2),
            'prevClose': round(data['Close'].iloc[-2], 2) if len(data) > 1 else None,
            'change': round(data['Close'].iloc[-1] - data['Open'].iloc[-1], 2),
            'pChange': round(((data['Close'].iloc[-1] - data['Open'].iloc[-1]) / data['Open'].iloc[-1]) * 100, 2),
            'SMA_5': round(data['Close'].rolling(window=5).mean().iloc[-1], 2) if len(data) >= 5 else None,
            'SMA_10': round(data['Close'].rolling(window=10).mean().iloc[-1], 2) if len(data) >= 10 else None
        }
    except Exception as e:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stocks', methods=['GET'])
def get_stock_data():
    stocks = get_nifty50_stocks()
    data = []
    
    for stock in stocks:
        stock_data = fetch_stock_data(stock)
        if stock_data:
            data.append(stock_data)
        time.sleep(2)
    
    df = pd.DataFrame(data)
    if df.empty:
        return jsonify({"error": "No stock data available. Check API or internet connection."}), 500
    
    live_prices = df[['symbol', 'lastPrice', 'change', 'pChange']].to_dict(orient='records')
    trending_stocks_df = df[df['SMA_5'] > df['SMA_10']]
    trending_stocks = trending_stocks_df[['symbol', 'lastPrice', 'SMA_5', 'SMA_10']].to_dict(orient='records')
    
    return jsonify({
        "livePrices": live_prices,
        "trendingStocks": trending_stocks
    })

if __name__ == '__main__':
    app.run(debug=True)
