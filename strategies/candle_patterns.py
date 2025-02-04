import logging
logger = logging.getLogger(__name__)

def is_bullish_candle(row):
    try:
        row=row.copy()
        row['Close'] = round(float(row['Close']), 2)
        row['Open'] = round(float(row['Open']), 2)
        row['High'] = round(float(row['High']), 2)
        row['Low'] = round(float(row['Low']), 2)
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid data in row: {row} - Error: {e}")
        return False
    body = abs(row['Close'] - row['Open'])
    lower_wick = row['Open'] - row['Low'] if row['Close'] > row['Open'] else row['Close'] - row['Low']
    upper_wick = row['High'] - row['Close'] if row['Close'] > row['Open'] else row['High'] - row['Open']
    total_range = row['High'] - row['Low']

    if row['Close'] > row['Open']:
        return True
    if (lower_wick > 2 * body) and (upper_wick < body):
        return True
    if body <= (0.1 * total_range) and upper_wick > body and lower_wick > body:
        return True
    return False

def is_bearish_candle(row):
    try:
        row=row.copy()
        row['Close'] = round(float(row['Close']), 2)
        row['Open'] = round(float(row['Open']), 2)
        row['High'] = round(float(row['High']), 2)
        row['Low'] = round(float(row['Low']), 2)
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid data in row: {row} - Error: {e}")
        return False
    body = abs(row['Close'] - row['Open'])
    lower_wick = row['Open'] - row['Low'] if row['Close'] > row['Open'] else row['Close'] - row['Low']
    upper_wick = row['High'] - row['Close'] if row['Close'] > row['Open'] else row['High'] - row['Open']
    total_range = row['High'] - row['Low']
    if row['Close'] < row['Open']:
        return True
    if body <= (0.1 * total_range) and upper_wick > 2 * body and lower_wick < body:
        return True
    if (upper_wick > 2 * body) and (lower_wick < body):
        return True
    if body <= (0.1 * total_range) and upper_wick > body and lower_wick > body:
        return True
            
    return False

def detect_bullish_patterns(df):
    """Detects bullish patterns in the dataframe."""
    patterns = []

    if len(df) < 3:
        logger.warning("Not enough data to detect patterns.")
        return patterns

    for i in range(2, len(df)):
        condition1 = (
            df.iloc[i-2]['Close'] < df.iloc[i-2]['Open'] and  # First red candle
            df.iloc[i-1]['Close'] < df.iloc[i-1]['Open'] and  # Second red candle
            df.iloc[i]['Close'] > df.iloc[i]['Open'] and      # Third green candle
            df.iloc[i]['Low'] >= df.iloc[i-1]['Low'] and      # Green low >= last red low
            df.iloc[i]['Close'] > df.iloc[i-1]['High']        # Green close > last red high
        )

        condition2 = (
            df.iloc[i-2]['Close'] < df.iloc[i-2]['Open'] and  # First red candle
            df.iloc[i-1]['Close'] < df.iloc[i-1]['Open'] and  # Second red candle
            df.iloc[i]['Close'] > df.iloc[i]['Open'] and      # Third green candle
            abs(df.iloc[i]['Open'] - df.iloc[i-1]['High']) <= 0.01 * df.iloc[i-1]['High'] and  # Green open near red high
            df.iloc[i]['Low'] >= df.iloc[i-1]['Low']          # Green low not breaching red low
        )

        condition3 = (
            df.iloc[i-2]['Close'] < df.iloc[i-2]['Open'] and  # First red candle
            df.iloc[i-1]['Close'] < df.iloc[i-1]['Open'] and  # Second red candle
            df.iloc[i]['Close'] > df.iloc[i]['Open'] and      # Third green candle
            df.iloc[i]['Open'] > df.iloc[i-1]['High'] and     # Green gap up
            df.iloc[i]['Low'] > df.iloc[i-1]['High']          # Green low > last red high
        )

        if condition1 or condition2 or condition3:
            patterns.append(i)
            #logger.info(f"Bullish Reversal pattern detected on {df['Date'].iloc[i]} ")

    return patterns

def detect_bearish_patterns(df):
    """Detects bullish patterns in the dataframe."""
    patterns = []

    if len(df) < 3:
        logger.warning("Not enough data to detect patterns.")
        return patterns

    for i in range(2, len(df)):
        # Condition 1: Two consecutive green candles followed by a red candle
        # Accessing rows by position using .iloc
      
        condition4 = (
            df.iloc[i-2]['Close'] > df.iloc[i-2]['Open'] and  # First green candle
            df.iloc[i-1]['Close'] > df.iloc[i-1]['Open'] and  # Second green candle
            df.iloc[i]['Close'] < df.iloc[i]['Open'] and      # Third red candle
            df.iloc[i]['High'] <= df.iloc[i-1]['High'] *1.01 and    # Red high <= previous green high
            df.iloc[i]['Close'] < df.iloc[i-1]['Open']         # Red close < previous green low
        )

        condition5 = (
            df.iloc[i-2]['Close'] > df.iloc[i-2]['Open'] and  # First green candle
            df.iloc[i-1]['Close'] > df.iloc[i-1]['Open'] and  # Second green candle
            df.iloc[i]['Close'] < df.iloc[i]['Open'] and      # Third red candle
            abs(df.iloc[i]['Open'] - df.iloc[i-1]['Low']) <= 0.01 * df.iloc[i-1]['Low'] and  # Red open near green low
            df.iloc[i]['High'] <= df.iloc[i-1]['High']        # Red high not breaching green high
        )

        condition6 = (
            df.iloc[i-2]['Close'] > df.iloc[i-2]['Open'] and  # First green candle
            df.iloc[i-1]['Close'] > df.iloc[i-1]['Open'] and  # Second green candle
            df.iloc[i]['Close'] < df.iloc[i]['Open'] and      # Third red candle
            df.iloc[i]['Open'] < df.iloc[i-1]['Low'] and      # Red gap down
            df.iloc[i]['High'] < df.iloc[i-1]['Low']          # Red high < last green low
        )

        if condition4 or condition5 or condition6:
            patterns.append(i)
            #logger.info(f"Bullish Reversal pattern detected on {df['Date'].iloc[i]} ")

    return patterns
