import glob
import json
import logging
import os
from datetime import datetime
import pandas as pd
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from SMA_BB_Extract import calculate_bollinger_bands
from strategies import (
    process_file_long, process_file_short,
    run_bullish_ground_floor_strategy, run_bearish_ground_floor_strategy,
    load_categories, load_selected_stocks, get_processed_symbols, get_latest_modified_csv,
    is_bullish_candle, is_bearish_candle, detect_bullish_patterns, detect_bearish_patterns
)

# Constants
DATA_INPUT = r"E:\Python Learn\Git File\eod2\src\eod2_data\daily"
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
STOCK_CATEGORIES_FILE = os.path.join(DATA_DIR, 'all_stock_lists.json')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')
LOG_FILE = "logfile.log"
thr_range = 3/100


# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['ENV'] = 'development'

# Function to read categories from JSON
@app.route('/get-categories')
def get_categories():
    try:
        with open(STOCK_CATEGORIES_FILE, 'r') as f:
            data = json.load(f)
            formatted_data = {key.capitalize(): value for key, value in data.items()}
        logger.info("Loaded stock categories successfully.")
        return jsonify(formatted_data)
    except Exception as e:
        logger.error(f"Error loading categories: {str(e)}")
        return jsonify({"error": f"Unable to load categories: {str(e)}"})
    
# ABC Long strategy function
def abc_long_strategy(date, category):
    try:
        logger.info(f"Executing ABC Long strategy for date: {date}, category: {category}")
        
        user_date = pd.to_datetime(date, format='%d-%m-%Y')
        selected_stocks = load_selected_stocks(category.lower())
        processed_symbols = get_processed_symbols(OUTPUT_DIR)
        files = glob.glob(os.path.join(DATA_INPUT, "*.csv"))

        selected_files = [file for file in files if os.path.basename(file).split(".")[0].upper() in selected_stocks]
        if not selected_files:
            # Return a message to the user that no matching files were found
            result_message = "No matching files found for the selected stocks."
            return render_template('result.html', result_message=result_message)
        # Process each stock
        alert_list = []
        for file in selected_files:
            symbol = os.path.basename(file).split(".")[0].upper()
            if symbol in processed_symbols:
                logger.info(f"Skipping already processed symbol: {symbol}")
                continue
            try:
                if process_file_long(file, user_date):
                    alert_list.append(symbol)
                    logger.info(f"Alert generated for symbol: {symbol}")
            except Exception as e:
                logger.error(f"Error processing file {file}: {e}")

        logger.info(f"Completed strategy execution. Alerts: {alert_list}")
        return alert_list

    except Exception as e:
        logger.error(f"Error in ABC Long strategy: {e}")
        return []
def abc_short_strategy(date, category):
    try:
        logger.info(f"Executing ABC Short strategy for date: {date}, category: {category}")
        
        user_date = pd.to_datetime(date, format='%d-%m-%Y')
        selected_stocks = load_selected_stocks(category.lower())
        processed_symbols = get_processed_symbols(OUTPUT_DIR)
        files = glob.glob(os.path.join(DATA_INPUT, "*.csv"))

        selected_files = [file for file in files if os.path.basename(file).split(".")[0].upper() in selected_stocks]
        if not selected_files:
            # Return a message to the user that no matching files were found
            result_message = "No matching files found for the selected stocks."
            return render_template('result.html', result_message=result_message)
        # Process each stock
        alert_list = []
        for file in selected_files:
            symbol = os.path.basename(file).split(".")[0].upper()
            if symbol in processed_symbols:
                logger.info(f"Skipping already processed symbol: {symbol}")
                continue
            try:
                if process_file_short(file, user_date):
                    alert_list.append(symbol)
                    logger.info(f"Alert generated for symbol: {symbol}")
            except Exception as e:
                logger.error(f"Error processing file {file}: {e}")

        logger.info(f"Completed strategy execution. Alerts: {alert_list}")
        return alert_list

    except Exception as e:
        logger.error(f"Error in ABC Short strategy: {e}")
        return []
def generate_tradingview_chart_link(stock_symbol: str) -> str:
    base_url = "https://www.tradingview.com/chart/?symbol=NSE%3A"
    return f"{base_url}{stock_symbol.upper()}"
# Home page with form
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        categories = get_categories()
        return render_template('index.html', categories=categories)
    except Exception as e:
        logger.error(f"Error loading index page: {e}")
        return "Error loading page."

# Process form data and display results
@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        # Get form data
        date = request.form['date']
        category = request.form['category']
        strategy = request.form['strategy']
     
        logger.info(f"Form data received: date={date}, category={category}, strategy={strategy}")

        # Validate date format
        try:
            formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')
        except ValueError:
            logger.warning("Invalid date format received.")
            return "Invalid date format. Please use DD-MM-YYYY."

        # Run the selected strategy
        try:
            if strategy == "abc_long":
                alert_list = abc_long_strategy(formatted_date, category)
                links = [generate_tradingview_chart_link(stock) for stock in alert_list]

                result_message = f"Total alerts generated : {len(alert_list)}"
                result_data = [{"date": formatted_date, "symbol": symbol, "strategy": "ABC Long", "link":link} for symbol ,link in zip(alert_list, links)]
            elif strategy == "abc_short":
                alert_list = abc_short_strategy(formatted_date, category)
                links = [generate_tradingview_chart_link(stock) for stock in alert_list]

                result_message = f"Total alerts generated : {len(alert_list)}"
                result_data = [{"date": formatted_date, "symbol": symbol, "strategy": "ABC Short", "link":link} for symbol ,link in zip(alert_list, links)]
            elif strategy == "bullish_floor":
                alert_list = run_bullish_ground_floor_strategy(formatted_date,category)
                links = [generate_tradingview_chart_link(stock) for stock in alert_list]

                result_message = f"Total alerts generated : {len(alert_list)}"
                result_data = [{"date": formatted_date, "symbol": symbol, "strategy": "Bullish Reversal", "link":link} for symbol ,link in zip(alert_list, links)]
            elif strategy == "bearish_floor":
                alert_list = run_bearish_ground_floor_strategy(formatted_date,category)
                links = [generate_tradingview_chart_link(stock) for stock in alert_list]

                result_message = f"Total alerts generated : {len(alert_list)}"
                result_data = [{"date": formatted_date, "symbol": symbol, "strategy": "Bearish Reversal", "link":link} for symbol ,link in zip(alert_list, links)]
            elif strategy == "alltimehigh":
                result_message = f"All Time High Range strategy executed for {category} on {formatted_date}."
            else:
                result_message = "Invalid strategy selected."
                result_data = []
            logger.info(f"Result message: {result_message}")
            # Render result page with output
            return render_template('result.html', result_message=result_message,result_data=result_data)
        except Exception as e:
            logger.error(f"Error during strategy execution: {e}")
            return "An error occurred while processing your request. Please try again."

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, threaded=False)
