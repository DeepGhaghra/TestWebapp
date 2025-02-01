from asyncio.log import logger
import os
import glob
import pandas as pd
from SMA_BB_Extract import calculate_bollinger_bands
from .candle_patterns import is_bullish_candle, is_bearish_candle

thr_range = 3/100
DATA_DIR = os.path.join(os.path.dirname(__file__),'..', 'data')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')

def process_file_long(file_path, user_date):
    try:
        symbol = os.path.basename(file_path).split(".")[0]
        output_bb = os.path.join(OUTPUT_DIR, f"{symbol}_BB.csv")

        if os.path.exists(output_bb):
            df = pd.read_csv(output_bb, usecols=['Date'])
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            max_date = df['Date'].max()
            if user_date > max_date:
                calculate_bollinger_bands(file_path, output_bb)
        else:
            calculate_bollinger_bands(file_path, output_bb)

        df = pd.read_csv(output_bb)
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', '50_SMA', 'Lower_Band']
        if not all(col in df.columns for col in required_columns):
            return False

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        last_day_data = df[df['Date'] == user_date]

        if last_day_data.empty:
            return False

        last_day_data = last_day_data.copy()  # Ensure it's a new DataFrame
        last_day_data['Lower_Band_Threshold'] = thr_range * last_day_data['Lower_Band']
        last_day_data['SMA_Threshold'] = thr_range * last_day_data['50_SMA']

        df['Bullish_Candle'] = df.apply(is_bullish_candle, axis=1)
        df['SMA_Rising'] = df['50_SMA'].diff() > 0

        last_day_data['Signal'] = (
            (last_day_data['Open'] >= last_day_data['Lower_Band'] - last_day_data['Lower_Band_Threshold']) &
            (last_day_data['Open'] <= last_day_data['Lower_Band'] + last_day_data['Lower_Band_Threshold']) &
            (last_day_data['Open'] >= last_day_data['50_SMA'] - last_day_data['SMA_Threshold']) &
            (last_day_data['Open'] <= last_day_data['50_SMA'] + last_day_data['SMA_Threshold']) &
            (df['Bullish_Candle']) &
            (df['SMA_Rising'])
        )
        return not last_day_data[last_day_data['Signal']].empty
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        return False

def process_file_short(file_path, user_date):
    try:
        symbol = os.path.basename(file_path).split(".")[0]
        output_bb = os.path.join(OUTPUT_DIR, f"{symbol}_BB.csv")

        if os.path.exists(output_bb):
            df = pd.read_csv(output_bb, usecols=['Date'])
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            max_date = df['Date'].max()
            if user_date > max_date:
                calculate_bollinger_bands(file_path, output_bb)
        else:
            calculate_bollinger_bands(file_path, output_bb)

        df = pd.read_csv(output_bb)
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', '50_SMA', 'Upper_Band']
        if not all(col in df.columns for col in required_columns):
            return False

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        last_day_data = df[df['Date'] == user_date]

        if last_day_data.empty:
            return False

        last_day_data = last_day_data.copy()  # Ensure it's a new DataFrame
        last_day_data['Upper_Band_Threshold'] = thr_range * last_day_data['Upper_Band']
        last_day_data['SMA_Threshold'] = thr_range * last_day_data['50_SMA']

        df['Bearish_Candle'] = df.apply(is_bearish_candle, axis=1)
        df['SMA_Falling'] = df['50_SMA'].diff() < 0

        last_day_data['Signal'] = (
            (last_day_data['Open'] >= last_day_data['Upper_Band'] - last_day_data['Upper_Band_Threshold']) &
            (last_day_data['Open'] <= last_day_data['Upper_Band'] + last_day_data['Upper_Band_Threshold']) &
            (last_day_data['Open'] >= last_day_data['50_SMA'] - last_day_data['SMA_Threshold']) &
            (last_day_data['Open'] <= last_day_data['50_SMA'] + last_day_data['SMA_Threshold']) &
            (df['Bearish_Candle']) &
            (df['SMA_Falling'])
        )
        return not last_day_data[last_day_data['Signal']].empty
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        return False