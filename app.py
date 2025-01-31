from flask import Flask, render_template, request
from jugaad_data.nse import stock_df

app = Flask(__name__)

def get_live_stock_price(stock_symbol):
    try:
        # Fetch live stock data using Jugaad Data
        df = stock_df(stock_symbol)
        if df is not None and not df.empty:
            latest_price = df.iloc[-1]['CLOSE']  # Get the latest closing price
            return latest_price
        else:
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    stock_price = None
    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol'].upper().strip()
        stock_price = get_live_stock_price(stock_symbol)
    return render_template('index.html', stock_price=stock_price)

if __name__ == '__main__':
    app.run(debug=True)