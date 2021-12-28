# Algo-TradingBot
Trading bot coded in Python and uses Alpaca trading API, yfinance and other libraries included in the import section of the code. 

**Setup**
Given the imports in the code, you must pip install alpaca-trade-api, pandas, yfinance, numpy and matplotlib if you have not already. The base URL is set to execute trades through Alpaca's paper trading. It is recommended you test this code with your desired inputs before proceeding to live trading with actual money. All trades will be executed in USD. 

When you create an Alpaca trading account, you must generate your unique API key and secret key and paste them (in that specific order) replacing the text in the given CSV file (alpaca_keys.csv). 
If you run 

'''
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
account = api.get_account()
'''
without error, the setup is now complete (assuming the previous steps have been done). 
