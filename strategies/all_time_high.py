import logging
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from .utils import load_selected_stocks

DATA_INPUT = r"E:\Python Learn\Git File\eod2\src\eod2_data\daily"

def process_stock_file(stock, percentage, results):
    """Process the stock file for checking the all-time high."""
    file_path = os.path.join(DATA_INPUT, f"{stock}.csv")
    
    if not os.path.exists(file_path):
        return  # Skip if the file doesn't exist
    
    try:
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Ensure 'High' and 'Close' columns are numeric
        df['High'] = pd.to_numeric(df['High'], errors='coerce')
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

        # Drop rows with NaN values in 'High' or 'Close' columns
        df = df.dropna(subset=['High', 'Close'])
        
        if df.empty:
            logging.warning(f"No valid data in file {file_path} after cleaning.")
            return
        
        all_time_high = df['High'].max()
        latest_close = df.iloc[-1]['Close']
        
        if all_time_high == 0:
            difference = float('inf')  # or assign another meaningful value like 0
            logging.warning(f"All Time High is zero for {stock}. Difference set to infinity or default value.")
        else:
            difference = ((all_time_high - latest_close) / all_time_high) * 100
        
        # Ensure both difference and percentage are numeric before comparison
        if isinstance(difference, (int, float)) and isinstance(percentage, (int, float)):
            if difference <= percentage:
                results.append(stock)
        else:
            logging.error(f"Type mismatch: difference={difference}, percentage={percentage}. Both must be numeric.")
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")

def check_all_time_high(category, percentage):
    """Check stocks below all-time high by a given percentage."""
    results = []
    stocks = load_selected_stocks(category.lower())
    
    try:
        percentage = float(percentage)
    except (ValueError, TypeError) as e:
        logging.error(f"Invalid percentage value: {percentage}. It must be a numeric type.")
        return results
    
    # Use ThreadPoolExecutor to parallelize the file processing
    with ThreadPoolExecutor() as executor:
        # Dispatch tasks to the thread pool
        futures = [executor.submit(process_stock_file, stock, percentage, results) for stock in stocks]
        
        # Wait for all threads to complete
        for future in futures:
            future.result()  # Blocks until the task is done

    return results
