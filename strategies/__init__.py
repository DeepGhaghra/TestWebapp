# strategies/__init__.py

# Import functions from individual modules to make them accessible directly from the strategies package
from .abc_strategy import process_file_long, process_file_short
from .ground_floor_strategy import run_bullish_ground_floor_strategy, run_bearish_ground_floor_strategy
from .utils import load_categories, load_selected_stocks, get_processed_symbols, get_latest_modified_csv
from .candle_patterns import is_bullish_candle, is_bearish_candle, detect_bullish_patterns, detect_bearish_patterns

# Optional: Define what gets imported when using `from strategies import *`
__all__ = [
    'process_file_long', 'process_file_short',
    'run_bullish_ground_floor_strategy', 'run_bearish_ground_floor_strategy',
    'load_categories', 'load_selected_stocks', 'get_processed_symbols', 'get_latest_modified_csv',
    'is_bullish_candle', 'is_bearish_candle', 'detect_bullish_patterns', 'detect_bearish_patterns'
]