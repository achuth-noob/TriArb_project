import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import numpy as np
import math
import BKeys
import time

client = Client(BKeys.API_KEY, BKeys.API_SECRET)

def floor_rounding(x,y,max_rounding=8):
    x = round(x,max_rounding)
    qty = x - round(x % y, max_rounding)
    z = int(round((math.log(y, 10) * (-1)), 0))
    qty = round(qty, z)
    return qty

def method_performance(method,*args):
    t1 = time.perf_counter()
    method(*args)
    t2 = time.perf_counter()-t1
    print(f'Elapsed Time to execute the function is {t2*1000}ms')


# print(floor_rounding(0.000156,0.0001,max_rounding=6))

# print('BTCUSDT'.split('USDT')[0])

# ALT_flushconvert_BNB()


