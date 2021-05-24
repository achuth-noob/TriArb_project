import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
from utils import *
import numpy as np
import math
import BKeys
import time

client = Client(BKeys.API_KEY, BKeys.API_SECRET)

# pprint.pprint(client.futures_exchange_info()['symbols'])

# pprint.pprint(client.futures_funding_rate())

def get_lowest_askprice(asset):
    snap = np.array(client.get_orderbook_tickers())
    for i in snap:
        if i['symbol']==asset:
            return(float(i['askPrice']))
        
def get_highest_bidprice(asset):
    snap = np.array(client.get_orderbook_tickers())
    for i in snap:
        if i['symbol'] == asset:
            return (float(i['bidPrice']))
        
print(get_highest_bidprice('BNBUSDT'))

# method_performance(get_lowest_askprice,'BNBUSDT')