import jugaad_data as jd
import yfinance as yf
from jugaad_data.nse import NSELive

n = NSELive()
nifty_data = n.live_index('NIFTY 50')
print(nifty_data['name'], nifty_data['timestamp'], nifty_data['data'][0]['lastPrice'])