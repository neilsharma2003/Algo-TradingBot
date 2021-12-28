import alpaca_trade_api as tradeapi
import pandas as pd
import threading
import datetime
import time
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import operator

api_key = pd.read_csv('alpaca_keys.csv')['Secret Key'][0]
api_secret = pd.read_csv('alpaca_keys.csv')['Secret Key'][1]
base_url = 'https://paper-api.alpaca.markets'

# instantiate REST API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# obtain account information
account = api.get_account()

def submit_my_order(symbol, qty, side, order_type, time_in_force):
    api.submit_order(symbol, qty, side, order_type, time_in_force)

def remove_duplicates(ticker):
    return list(set(ticker))

now = datetime.datetime.now()

year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
current_date = year + "-" + month + "-" + day
year_before = str(int(year) - 1) + "-" + month + "-" + day

trading_strategy = int(input("Type 1 for a safe, equally weighted buy and hold portfolio, and 2 for a riskier day trade strategy: "))
if trading_strategy == 1:
    listoftickers = []
    while True:
        ticker = input("Insert VALID USD tickers and type 'STOP' to terminate input ")
        if ticker == 'stop' or ticker == 'STOP' or ticker == 'Stop':
            break
        else:
            listoftickers.append(ticker)
    listoftickers = remove_duplicates(listoftickers)
    filtered_list = []
    for ticker in listoftickers:
        info = yf.Ticker(ticker).info
        if info.get('regularMarketPrice') == None:
            continue
        if info.get('currency')!= 'USD':
            continue
        if info.get ('market') != ('us_market'):
            continue
        else:
            filtered_list.append(ticker)
    
    ticker_list_based_on_1yr_pct_change = {"Ticker":[], "1 Year Percent Change":[]}
    
    for ticker in filtered_list:
        ticker_list_based_on_1yr_pct_change["Ticker"].append(ticker)
        ticker_list_based_on_1yr_pct_change["1 Year Percent Change"].append(pd.DataFrame(100*yf.Ticker(ticker).history(start = year_before, end = current_date)['Close'].pct_change()).describe()['Close'][1])

    ticker_list_based_on_1yr_pct_change = dict(zip(ticker_list_based_on_1yr_pct_change['Ticker'], ticker_list_based_on_1yr_pct_change['1 Year Percent Change']))
    sorted_ticker_list_based_on_1yr_pct_change = sorted(ticker_list_based_on_1yr_pct_change.items(), key=operator.itemgetter(1))
    sorted_dict = dict(sorted_ticker_list_based_on_1yr_pct_change[::-1]) 
    
    sorted_dict_no_neg = dict((ticker, pct_change) for ticker, pct_change in sorted_dict.items() if pct_change >= 0) 
    
    if len(filtered_list) > 20:
        sorted_dict_final = dict(list(sorted_dict_no_neg.items())[:20])
    else:
        pass
    
    portfolio_value = float(input("Insert the total amount of money (USD) you wish to invest. Please remember large orders can take time to fill and can result in more or less money spent."))
    
    allocated_funds_per_ticker = portfolio_value / len(sorted_dict_final) # equally weighted portfolio
    quantity = []
    for i in list(sorted_dict_final.keys()):
        quantity.append(allocated_funds_per_ticker / yf.download(tickers = i, period = '1d', interval = '1m')['Close'][-1])
    
    for i in range(len(sorted_dict_final)):
        submit_my_order(list(sorted_dict_final.keys())[i], quantity[i], 'buy', 'market', 'gtc')
        
if trading_strategy == 2:
    ticker = input("Insert 1 VALID USD ticker to day trade: ")
    quantity = input("Insert quantity of said ticker: ")
    flag = True
    while True:
        data = yf.download(tickers = ticker, period='1d', interval='1m')
        pct_change = pd.DataFrame(data['Close'].pct_change() * 100)
        pct_change.columns = ['Percentage Change in Price']
        if flag:
            if 0.05 < pct_change['Percentage Change in Price'][-1] <= 0.2:
                submit_my_order(ticker, quantity, 'buy', 'market', 'gtc')
                print(ticker + " bought at $ " + str(si.get_live_price(ticker)))
                flag = False
        try: var = api.get_position(ticker)
        except: var = "No position"   
        
        if var != "No position":
            if pct_change['Percentage Change in Price'][-1] < -0.1 or pct_change['Percentage Change in Price'][-1] > 0.21:
                submit_my_order(ticker, quantity, 'sell', 'market', 'gtc')
                print(ticker + " sold at $ " + str(si.get_live_price(ticker)))
                print("Please refer to Alpaca dashboard for accurate buy and sell prices")
                break
                
            if -0.05 < pct_change['Percentage Change in Price'][-1] < 0:
                submit_my_order(ticker, quantity, 'sell', 'market', 'gtc')
                print(ticker + " sold at $ " + str(si.get_live_price(ticker)))
                break
        time.sleep(1) 
