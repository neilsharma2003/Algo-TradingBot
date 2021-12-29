# Algo-TradingBot
Trading bot written in Python and uses Alpaca trading API, yfinance and other libraries included in the import section of the code. 

**Setup**

Given the imports in the code, you must pip install alpaca-trade-api, pandas, yfinance, numpy and matplotlib if you have not already. The base URL is set to execute trades through Alpaca's paper trading. It is recommended you test this code with your desired inputs before proceeding to live trading with actual money. All trades will be executed in USD. 

When you create an Alpaca trading account, you must generate your unique API key and secret key and paste them (in that specific order) replacing the text in the given CSV file (alpaca_keys.csv). 

If you run api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
and account = api.get_account()  without error, the setup is now complete (assuming the previous steps have been done correctly). 

**Explanation of The Code**

After the imports and the REST API/account info initialization, an order function is created that executes buy/sell trades. An additional function that removes duplicate tickers (in a list) is created and is called later into the code. 

At this point, the user has two options:
  1) Momentum trading portfolio (meant to be held for 1 year or more) that accepts ticker inputs from the user, removes false, non-USD tickers, and tickers     
     whose 1 year percentage return is negative. Credits to Jenny Zhang for the the loop that forms a filtered list. Then, the program will rank 1 year     
     percentage returns (via sorting), and choose the top 20 stocks or the keep the list of tickers intact if it is less than 20.
     
     The program then will ask the user for the amount of money they wish to invest, allocates the money to each ticker, and determines the quantity for
     each ticker. Finally, the order function is called to execute buys on each ticker at their according quantity. 
     
  2) Day trading strategy that searches for an increase in the price and sells at a small profit. More specifically, the program will purchase the inputted  
     ticker (at said quantity) when the price begins to increase and sells once the price declines. If the price does not increase, there is a pseudo-stop-loss   
     order that sells the ticker. The goal of this strategy is to reduce losses and to withdraw from a position if there is high price volatility. 
 
 It is well noting that stock prices printed in the code have delays and you should keep an eye on your Alpaca dashboard to get the most up-to-date stock information as well as withdrawing from trades if necessary. 
