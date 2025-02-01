from asyncio.log import logger
import glob
import os
import pandas as pd

from strategies.utils import load_selected_stocks
from .candle_patterns import detect_bullish_patterns, detect_bearish_patterns

DATA_INPUT = r"E:\Python Learn\Git File\eod2\src\eod2_data\daily"

def run_bullish_ground_floor_strategy(update, context, date, category, processing_message):
    try:
        user_date = pd.to_datetime(date, format='%d-%m-%Y')
        selected_stocks = load_selected_stocks(category)
        files = glob.glob(os.path.join(DATA_INPUT, "*.csv"))

        selected_files = [file for file in files if os.path.basename(file).split(".")[0].upper() in selected_stocks]

        ''' if not selected_files:
            await processing_message.edit_text("No matching files found for the selected stocks.")
            return'''

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

        final_message = f"✅ Bullish Ground Floor strategy executed for <b>{category.upper()}</b> and <b>{user_date.strftime('%d-%m-%Y')}</b>. \nTotal alerts generated: <b>{len(alert_list)}</b>.\n"
        if alert_list:
            final_message += "\nHere are the scanned alerts:\n"
            final_message += "\n".join([f"• {symbol}" for symbol in alert_list])
        
    except Exception as e:
        logger.error(f"Error executing Bullish Ground Floor strategy: {e}")
        return False

def run_bearish_ground_floor_strategy(update, context, date, category, processing_message):
    try:
        user_date = pd.to_datetime(date, format='%d-%m-%Y')
        selected_stocks = load_selected_stocks(category)
        files = glob.glob(os.path.join(DATA_INPUT, "*.csv"))

        selected_files = [file for file in files if os.path.basename(file).split(".")[0].upper() in selected_stocks]

        '''if not selected_files:
            await processing_message.edit_text("No matching files found for the selected stocks.")
            return'''

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

        final_message = f"✅ Bearish High Floor strategy executed for <b>{category.upper()}</b> and <b>{user_date.strftime('%d-%m-%Y')}</b>. \nTotal alerts generated: <b>{len(alert_list)}</b>.\n"
        if alert_list:
            final_message += "\nHere are the scanned alerts:\n"
            final_message += "\n".join([f"• {symbol}" for symbol in alert_list])

    except Exception as e:
        logger.error(f"Error executing Bearish Ground Floor strategy: {e}")
        return False
