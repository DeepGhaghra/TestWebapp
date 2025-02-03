import logging
import os
import pandas as pd
from .utils import load_categories,load_selected_stocks

DATA_INPUT = r"E:\Python Learn\Git File\eod2\src\eod2_data\daily"

def check_all_time_high(category, percentage):
    """Check stocks below all-time high by a given percentage."""
    results = []
    stocks = load_selected_stocks(category.lower())

    for stock in stocks:
        file_path = os.path.join(DATA_INPUT, f"{stock}.csv")
        print(f"stock nmeee::::{file_path}")

        if os.path.exists(file_path):
            try:
                    df = pd.read_csv(file_path)
                    print(f"Data for {stock}:\n{df.head()}")  # Debug: Check the loaded data

                    df['Date'] = pd.to_datetime(df['Date'])
                    print(f"sssssdataaaaaaaaaa-----{df['Date']}")
                    all_time_high = df['High'].max()
                    latest_close = df.iloc[-1]['Close']

                    if all_time_high == 0:
                        difference = float('inf')  # or assign another meaningful value like 0
                        logging.warning(f"All Time High is zero for the current data. Difference set to infinity or default value.")
                    else:
                        difference = ((all_time_high - latest_close) / all_time_high) * 100

                    if difference <= percentage:
                        return {
                            "stock": stock,
                            "all_time_high": all_time_high,
                            "latest_close": latest_close,
                            "difference": round(difference, 2),
                            "date": df.iloc[-1]['Date'].strftime("%Y-%m-%d"),
                        }
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {e}")
    return results
