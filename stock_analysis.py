#!/usr/bin/env python3
"""
Simple Stock Analysis Script for GitHub Actions
"""

import yfinance as yf
import json
import os
from datetime import datetime

def analyze_stock(symbol):
    """Get stock data and simple analysis"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period='2d')
        
        if hist.empty:
            return None
        
        # Get current price
        current_price = hist['Close'].iloc[-1]
        
        # Get previous day's close
        if len(hist) > 1:
            prev_close = hist['Close'].iloc[-2]
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100
        else:
            change = 0
            change_percent = 0
        
        # Get volume
        volume = hist['Volume'].iloc[-1]
        
        return {
            'symbol': symbol,
            'price': round(float(current_price), 2),
            'change': round(float(change), 2),
            'change_percent': round(float(change_percent), 2),
            'volume': int(volume),
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error analyzing {symbol}: {e}")
        return None

def main():
    # Stocks to analyze
    stocks = ['SPY', 'QQQ', 'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'TSLA', 'AMZN', 'META']
    
    print("=" * 60)
    print(f"📊 STOCK ANALYSIS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = []
    for symbol in stocks:
        print(f"\nAnalyzing {symbol}...")
        data = analyze_stock(symbol)
        if data:
            results.append(data)
            change_icon = "📈" if data['change'] >= 0 else "📉"
            print(f"  {change_icon} ${data['price']} ({data['change_percent']:+.2f}%)")
            print(f"  Volume: {data['volume']:,}")
    
    # Save results
    os.makedirs("reports", exist_ok=True)
    report_path = "reports/analysis_report.json"
    
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 60)
    print(f"✅ Analysis complete! {len(results)} stocks analyzed")
    print(f"📁 Report saved to: {report_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
