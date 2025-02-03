import json
import os
import glob
from datetime import datetime
import random
import logging

logger = logging.getLogger(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__),'..', 'data')
STOCK_CATEGORIES_FILE = os.path.join(DATA_DIR, 'all_stock_lists.json')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..','output')

def load_categories():
    try:
        with open(STOCK_CATEGORIES_FILE, "r") as file:
            data = json.load(file)
        categories = list(data.keys())
        if not categories:
            logger.error("No categories found in the JSON file.")
        return categories
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading categories: {str(e)}")
        return []

def load_selected_stocks(category: str):
    try:
        with open(STOCK_CATEGORIES_FILE, "r") as f:
            all_stock_lists = json.load(f)
        return all_stock_lists.get(category, [])
    except Exception as e:
        logger.error(f"Error loading selected stocks: {e}")
        return []

def get_processed_symbols(procesfolder):
    processed_files = glob.glob(os.path.join(procesfolder, "*.csv"))
    processed_symbols = {os.path.basename(file).split(".")[0].upper() for file in processed_files}
    return processed_symbols

def get_latest_modified_csv(directory):
    """Get the latest modified CSV file from the given directory."""
    csv_files = glob.glob(os.path.join(directory, "*.csv"))
    if not csv_files:
        return None, None
    
    # Pick a random CSV file and get its modified date
    selected_file = random.choice(csv_files)
    modified_date = datetime.fromtimestamp(os.path.getmtime(selected_file)).strftime("%d-%m-%Y")
    return modified_date

def generate_tradingview_chart_link(stock_symbol: str) -> str:
    base_url = "https://www.tradingview.com/chart/?symbol=NSE%3A"
    return f"{base_url}{stock_symbol.upper()}"