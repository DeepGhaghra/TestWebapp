from asyncio.log import logger
import glob
import os
import pandas as pd

from strategies.utils import load_selected_stocks
from .candle_patterns import detect_bullish_patterns, detect_bearish_patterns

DATA_INPUT = r"E:\Python Learn\Git File\eod2\src\eod2_data\daily"

def run_bullish_ground_floor_strategy(date, category):
    try:
        user_date = pd.to_datetime(date, format='%d-%m-%Y')
        selected_stocks = load_selected_stocks(category.lower())
        files = glob.glob(os.path.join(DATA_INPUT, "*.csv"))

        selected_files = [file for file in files if os.path.basename(file).split(".")[0].upper() in selected_stocks]

        if not selected_files:
            logger.info("no file found to execute bullish reversal please check")
            return

        alert_list = []
        for file in selected_files:
            symbol = os.path.basename(file).split(".")[0].upper()
            df = pd.read_csv(file)
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

            # Filter data for the selected date
            df_filtered = df[df['Date'].dt.date == user_date.date()]
            if len(df_filtered) < 3:
                df_filtered = df[df['Date'] <= user_date].tail(3)

            # Detect bullish patterns
            bullish_patterns = detect_bullish_patterns(df_filtered)
            if bullish_patterns:
                alert_list.append(symbol)
                logger.info(f"Alert generated for symbol: {symbol}")
            
        logger.info(f"Completed Bullish Reversal Strategy execution. Alerts: {alert_list}")
        return alert_list

    except Exception as e:
        logger.error(f"Error executing Bullish Ground Floor strategy: {e}")
        return []

def run_bearish_ground_floor_strategy(date, category):
    try:
        user_date = pd.to_datetime(date, format='%d-%m-%Y')
        selected_stocks = load_selected_stocks(category.lower())
        files = glob.glob(os.path.join(DATA_INPUT, "*.csv"))

        selected_files = [file for file in files if os.path.basename(file).split(".")[0].upper() in selected_stocks]
        if not selected_files:
            logger.info("no file found to execute bearish reversal please check")
            return

        alert_list = []
        for file in selected_files:
            symbol = os.path.basename(file).split(".")[0].upper()
            df = pd.read_csv(file)
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

            # Filter data for the selected date
            df_filtered = df[df['Date'].dt.date == user_date.date()]
            if len(df_filtered) < 3:
                df_filtered = df[df['Date'] <= user_date].tail(3)

            # Detect bearish patterns
            bearish_patterns = detect_bearish_patterns(df_filtered)
            if bearish_patterns:
                alert_list.append(symbol)
                logger.info(f"Alert generated for symbol: {symbol}")

        logger.info(f"Completed Bearish Reversal strategy execution. Alerts: {alert_list}")
        return alert_list
    except Exception as e:
        logger.error(f"Error executing Bearish Ground Floor strategy: {e}")
        return False
