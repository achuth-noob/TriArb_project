import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
from utils import *
import numpy as np
import math
import BKeys
import time

client = Client(BKeys.API_KEY, BKeys.API_SECRET)

def get_lowest_askprice(asset):
    snap = np.array(client.get_orderbook_tickers())
    for i in snap:
        if i['symbol']==asset:
            return(float(i['bidPrice']))

method_performance(get_lowest_askprice,'BNBUSDT')