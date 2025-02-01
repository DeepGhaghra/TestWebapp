import pandas as pd

# Load CSV file
def calculate_bollinger_bands(input_csv, output_csv):
    # Read the CSV file
    df = pd.read_csv(input_csv)

    # Ensure the required columns are present
    required_columns = ['Open', 'High', 'Low', 'Close']
    if not all(column in df.columns for column in required_columns):
        raise ValueError(f"Input CSV must contain the following columns: {', '.join(required_columns)}")

    # Calculate 50-day Simple Moving Average (SMA)
    df['50_SMA'] = df['Close'].rolling(window=50).mean()

    df['20_SMA'] = df['Close'].rolling(window=20).mean()

    # Calculate the rolling standard deviation
    rolling_std = df['Close'].rolling(window=20).std()

    # Calculate Upper and Lower Bollinger Bands
    df['Upper_Band'] = df['20_SMA'] + (2 * rolling_std)
    df['Lower_Band'] = df['20_SMA'] - (2 * rolling_std)

    # Save the resulting DataFrame to a new CSV file
    select_column = df[['Date','Open','High','Low','Close','50_SMA','Lower_Band','Upper_Band']]
    select_column.to_csv(output_csv, index=False)
    print(f"Bollinger Bands and 50 SMA calculated and saved to {output_csv}")

# Example usage
# symbol = input("Enter the stock symbol (e.g. HCLTECH): ").strip()
# input_csv = r'E:\Python Learn\Git File\eod2\src\eod2_data\daily\{symbol}.csv'  # Replace with your input CSV file path //input("Enter the path of the input CSV file: ").strip()
# output_csv = '{symbol}_BB_Temp.csv'  # Replace with your desired output CSV file path
# calculate_bollinger_bands(input_csv, output_csv)
