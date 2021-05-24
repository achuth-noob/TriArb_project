import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import numpy as np
import math
import BKeys
import time

client = Client(BKeys.API_KEY, BKeys.API_SECRET)

min_trade_qty = {}
for k in client.get_exchange_info()['symbols']:
    for i in k['filters']:
        if i['filterType'] == 'LOT_SIZE':
            min_trade_qty[k['symbol']] = float(i['minQty'])