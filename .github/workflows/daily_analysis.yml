#!/usr/bin/env python3
"""
Enhanced Stock Analysis Script for GitHub Actions
Features:
- Multiple output formats (JSON, CSV, HTML)
- Email notifications
- Configurable stocks via environment variables
- Rate limiting
- Extended metrics (PE ratio, market cap, day range)
- Historical comparison
"""

import yfinance as yf
import json
import os
import csv
import time
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

def get_stocks():
    """Get stock list from environment variable or use default"""
    env_stocks = os.getenv('STOCKS_TO_ANALYZE')
    if env_stocks:
        return [s.strip() for s in env_stocks.split(',')]
    return ['SPY', 'QQQ', 'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'TSLA', 'AMZN', 'META']

def analyze_stock(symbol):
    """Get stock data and comprehensive analysis"""
    try:
        ticker = yf.Ticker(symbol)
        
        # Get historical data (5 days for better comparison)
        hist = ticker.history(period='5d')
        
        if hist.empty or len(hist) < 2:
            return None
        
        # Current and previous day data
        current_price = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2]
        change = current_price - prev_close
        change_percent = (change / prev_close) * 100
        
        # 5-day performance
        if len(hist) >= 5:
            five_day_ago = hist['Close'].iloc[-5]
            five_day_change = ((current_price - five_day_ago) / five_day_ago) * 100
        else:
            five_day_change = 0
        
        # Volume
        volume = hist['Volume'].iloc[-1]
        avg_volume = hist['Volume'].tail(20).mean() if len(hist) >= 20 else volume
        
        # Day range
        day_high = hist['High'].iloc[-1]
        day_low = hist['Low'].iloc[-1]
        
        # Get company info
        info = ticker.info
        company_name = info.get('longName', symbol)
        pe_ratio = info.get('trailingPE', 'N/A')
        forward_pe = info.get('forwardPE', 'N/A')
        market_cap = info.get('marketCap', 'N/A')
        dividend_yield = info.get('dividendYield', 'N/A')
        if dividend_yield != 'N/A':
            dividend_yield = round(dividend_yield * 100, 2)
        
        # 52-week range
        fifty_two_week_high = info.get('fiftyTwoWeekHigh', 'N/A')
        fifty_two_week_low = info.get('fiftyTwoWeekLow', 'N/A')
        
        return {
            'symbol': symbol,
            'company_name': company_name,
            'price': round(float(current_price), 2),
            'change': round(float(change), 2),
            'change_percent': round(float(change_percent), 2),
            'five_day_change': round(float(five_day_change), 2),
            'volume': int(volume),
            'avg_volume': int(avg_volume),
            'volume_ratio': round(volume / avg_volume, 2) if avg_volume > 0 else 0,
            'day_high': round(float(day_high), 2),
            'day_low': round(float(day_low), 2),
            'pe_ratio': round(pe_ratio, 2) if pe_ratio != 'N/A' else 'N/A',
            'forward_pe': round(forward_pe, 2) if forward_pe != 'N/A' else 'N/A',
            'market_cap': format_market_cap(market_cap),
            'dividend_yield': dividend_yield if dividend_yield != 'N/A' else 'N/A',
            'fifty_two_week_high': round(fifty_two_week_high, 2) if fifty_two_week_high != 'N/A' else 'N/A',
            'fifty_two_week_low': round(fifty_two_week_low, 2) if fifty_two_week_low != 'N/A' else 'N/A',
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"❌ Error analyzing {symbol}: {e}")
        return None

def format_market_cap(cap):
    """Format market cap in human-readable form"""
    if cap == 'N/A':
        return 'N/A'
    if cap >= 1e12:
        return f"{cap/1e12:.2f}T"
    elif cap >= 1e9:
        return f"{cap/1e9:.2f}B"
    elif cap >= 1e6:
        return f"{cap/1e6:.2f}M"
    else:
        return str(cap)

def save_json_report(results, report_dir):
    """Save results as JSON"""
    report_path = Path(report_dir) / "analysis_report.json"
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"📄 JSON report saved to: {report_path}")
    return report_path

def save_csv_report(results, report_dir):
    """Save results as CSV"""
    if not results:
        return None
    
    report_path = Path(report_dir) / "analysis_report.csv"
    with open(report_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"📊 CSV report saved to: {report_path}")
    return report_path

def save_html_report(results, report_dir):
    """Generate an HTML report with better visualization"""
    if not results:
        return None
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Stock Analysis Report - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #333;
            text-align: center;
        }}
        .timestamp {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }}
        th {{
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
            position: sticky;
            top: 0;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .positive {{
            color: green;
            font-weight: bold;
        }}
        .negative {{
            color: red;
            font-weight: bold;
        }}
        .metric {{
            font-size: 0.9em;
            color: #666;
        }}
    </style>
</head>
<body>
    <h1>📈 Stock Market Analysis Report</h1>
    <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    
    <table>
        <thead>
            <tr>
                <th>Symbol</th>
                <th>Company</th>
                <th>Price</th>
                <th>Change</th>
                <th>5-Day Change</th>
                <th>Volume (M)</th>
                <th>Vol Ratio</th>
                <th>P/E Ratio</th>
                <th>Market Cap</th>
                <th>Div Yield</th>
            </tr>
        </thead>
        <tbody>
"""
    
    for stock in results:
        change_class = "positive" if stock['change_percent'] >= 0 else "negative"
        change_symbol = "▲" if stock['change_percent'] >= 0 else "▼"
        five_day_class = "positive" if stock['five_day_change'] >= 0 else "negative"
        
        volume_m = stock['volume'] / 1_000_000
        
        html_content += f"""
            <tr>
                <td><strong>{stock['symbol']}</strong></td>
                <td>{stock['company_name'][:40]}</td>
                <td>${stock['price']}</td>
                <td class="{change_class}">{change_symbol} {stock['change_percent']:+.2f}%</td>
                <td class="{five_day_class}">{stock['five_day_change']:+.2f}%</td>
                <td>{volume_m:.1f}</td>
                <td>{stock['volume_ratio']}x</td>
                <td>{stock['pe_ratio']}</td>
                <td>{stock['market_cap']}</td>
                <td>{stock['dividend_yield']}%</td>
            </tr>
"""
    
    html_content += """
        </tbody>
    </table>
</body>
</html>
"""
    
    report_path = Path(report_dir) / "analysis_report.html"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"🌐 HTML report saved to: {report_path}")
    return report_path

def send_email_report(results, attachments):
    """Send email report if configured"""
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    
    if not all([smtp_server, sender_email, recipient_email]):
        print("📧 Email not configured - skipping notification")
        return
    
    subject = f"Stock Analysis Report - {datetime.now().strftime('%Y-%m-%d')}"
    
    # Create HTML summary for email body
    html_body = "<h2>📊 Stock Analysis Summary</h2><table border='1' cellpadding='5'>"
    html_body += "<tr><th>Symbol</th><th>Price</th><th>Change</th><th>Volume Ratio</th></tr>"
    
    for stock in results:
        color = "green" if stock['change_percent'] >= 0 else "red"
        html_body += f"<tr><td>{stock['symbol']}</td><td>${stock['price']}</td>"
        html_body += f"<td style='color:{color}'>{stock['change_percent']:+.2f}%</td>"
        html_body += f"<td>{stock['volume_ratio']}x</td></tr>"
    
    html_body += "</table><p>See attached files for detailed analysis.</p>"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(html_body, 'html'))
    
    # Attach files
    for attachment in attachments:
        if attachment and attachment.exists():
            with open(attachment, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={attachment.name}')
                msg.attach(part)
    
    try:
        if smtp_port:
            port = int(smtp_port)
            if port == 465:
                # SSL
                with smtplib.SMTP_SSL(smtp_server, port) as server:
                    if sender_password:
                        server.login(sender_email, sender_password)
                    server.send_message(msg)
            else:
                # TLS
                with smtplib.SMTP(smtp_server, port) as server:
                    server.starttls()
                    if sender_password:
                        server.login(sender_email, sender_password)
                    server.send_message(msg)
        print(f"📧 Email sent to {recipient_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def print_summary(results):
    """Print formatted summary to console"""
    print("\n" + "=" * 80)
    print(f"📊 STOCK ANALYSIS SUMMARY - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Header
    print(f"{'Symbol':<8} {'Price':<10} {'Change':<12} {'5-Day':<10} {'Volume Ratio':<12} {'P/E':<8}")
    print("-" * 80)
    
    for stock in results:
        change_icon = "📈" if stock['change'] >= 0 else "📉"
        change_str = f"{change_icon} {stock['change_percent']:+.2f}%"
        five_day_str = f"{stock['five_day_change']:+.2f}%"
        
        print(f"{stock['symbol']:<8} ${stock['price']:<9} {change_str:<12} {five_day_str:<10} "
              f"{stock['volume_ratio']:<12}x {stock['pe_ratio']:<8}")
    
    print("=" * 80)
    
    # Highlight unusual volume
    high_volume = [s for s in results if s['volume_ratio'] > 1.5]
    if high_volume:
        print("\n⚠️  Unusual Volume Detected:")
        for stock in high_volume:
            print(f"  • {stock['symbol']}: {stock['volume_ratio']}x average volume")
    
    # Highlight big movers
    big_movers = [s for s in results if abs(s['change_percent']) > 2]
    if big_movers:
        print("\n🚀 Significant Movers (>2%):")
        for stock in big_movers:
            direction = "↑" if stock['change_percent'] > 0 else "↓"
            print(f"  • {stock['symbol']}: {direction} {abs(stock['change_percent']):.2f}%")
    
    print("=" * 80)

def main():
    # Create reports directory
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    
    # Get stocks to analyze
    stocks = get_stocks()
    
    print("=" * 80)
    print(f"🚀 Starting Stock Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Analyzing {len(stocks)} stocks: {', '.join(stocks)}")
    print("=" * 80)
    
    results = []
    for i, symbol in enumerate(stocks, 1):
        print(f"\n[{i}/{len(stocks)}] Analyzing {symbol}...")
        data = analyze_stock(symbol)
        
        if data:
            results.append(data)
            change_icon = "📈" if data['change'] >= 0 else "📉"
            print(f"  {change_icon} ${data['price']} ({data['change_percent']:+.2f}%) "
                  f"- Volume: {data['volume_ratio']}x avg")
        else:
            print(f"  ❌ Failed to get data for {symbol}")
        
        # Rate limiting - be nice to the API
        time.sleep(1)
    
    if not results:
        print("\n❌ No data was retrieved. Exiting.")
        return
    
    # Save reports
    json_path = save_json_report(results, report_dir)
    csv_path = save_csv_report(results, report_dir)
    html_path = save_html_report(results, report_dir)
    
    # Print summary
    print_summary(results)
    
    # Send email if configured
    attachments = [json_path, csv_path, html_path]
    send_email_report(results, attachments)
    
    # GitHub Actions specific: Set output variables
    if os.getenv('GITHUB_OUTPUT'):
        with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
            f.write(f"report_date={datetime.now().isoformat()}\n")
            f.write(f"stocks_analyzed={len(results)}\n")
    
    print("\n" + "=" * 80)
    print(f"✅ Analysis complete! Successfully analyzed {len(results)}/{len(stocks)} stocks")
    print(f"📁 Reports saved in '{report_dir}/' directory")
    print("=" * 80)

if __name__ == "__main__":
    main()
