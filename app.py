from flask import Flask, jsonify, render_template, request
from jugaad_data.nse import stock_df
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

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
    return render_template('index.html')

@app.route('/get-categories')
def get_categories():
    import json
    try:
        with open('static/all_stock_lists.json', 'r') as f:
            data = json.load(f)
            formatted_data = {key.capitalize(): value for key, value in data.items()}
        return jsonify(formatted_data)
    except Exception as e:
        return jsonify({"error": f"Unable to load categories: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)