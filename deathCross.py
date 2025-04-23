import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
import argparse

# CONFIGURATION
NTFY_TOPIC = "BTC_death_cross"  # Replace with your topic name
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"
ADVANCE_NOTICE_DAYS = 3
SYMBOL = "BTC-USD"

def send_notification(title, message, tags):
    requests.post(NTFY_URL,
    data=message,
    headers={
        "Title": title,
        "Tags": tags
    })

def get_moving_averages(end_date=None, days=300):
    if end_date is None:
        end = datetime.today()
    else:
        end = pd.to_datetime(end_date) + timedelta(days=1)
    start = end - timedelta(days=300)
    df = yf.download(SYMBOL, start=start, end=end)
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()
    return df

def check_for_death_cross(df):
    df = df.dropna().copy()
    df['Cross'] = df['MA50'] <= df['MA200']
    #print(df['Cross'])
    df['PrevCross'] = df['Cross'].shift(1)
    if df['Cross'].iloc[-1] and not df['PrevCross'].iloc[-1]:
        send_notification("Bitcoin Death Cross", f"A Death Cross has occurred today!", "bell")
        return

    if not df['PrevCross'].iloc[-1]:
        # Calculate slope (rate of change per day)
        ma50_slope = (df['MA50'].iloc[-2] - df['MA50'].iloc[-1])
        ma200_slope = (df['MA200'].iloc[-1] - df['MA200'].iloc[-2])

        ma50_pred = df['MA50'].iloc[-1]
        ma200_pred = df['MA200'].iloc[-1]

        for day in range(1, ADVANCE_NOTICE_DAYS + 1):
            ma50_pred -= ma50_slope
            ma200_pred += ma200_slope

            if ma50_pred < ma200_pred:
                send_notification("Bitcoin Death Cross Warning",
                                f"A Death Cross is predicted in {day} day(s).",
                                "warning")
                break


def backtest_for_date(test_date):
    print(f"\n🔍 Backtesting for: {test_date}")
    df = get_moving_averages(end_date=test_date, days=300)
    check_for_death_cross(df)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', help="Backtest as if script ran on this date (YYYY-MM-DD)")
    args = parser.parse_args()

    if args.date:
        backtest_for_date(args.date)
    else:
        df = get_moving_averages()
        check_for_death_cross(df)

if __name__ == "__main__":
    main()