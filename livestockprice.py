from flask import Flask, render_template, request
from jugaad_data.nse import NSELive

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_data = None
    error_message = None
    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol'].strip().upper()
        if stock_symbol:
            try:
                n = NSELive()
                stock_data = n.stock_quote(stock_symbol)
                if not stock_data:
                    error_message = f"No data found for symbol: {stock_symbol}"
            except Exception as e:
                error_message = f"Error fetching data: {e}"
        else:
            error_message = "Please enter a stock symbol."
    return render_template('livestock.html', stock_data=stock_data, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
