import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
from utils import *
import numpy as np
import math
import BKeys
import time

client = Client(BKeys.API_KEY, BKeys.API_SECRET)

def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        # print("sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        print('error : ',quantity)
        return False
    return True

def ALT_flushconvert_USDT(side='SELL'):
    x = client.get_account()
    min_trade_qty = {}
    for k in client.get_exchange_info()['symbols']:
        for i in k['filters']:
            if i['filterType'] == 'LOT_SIZE':
                min_trade_qty[k['symbol']] = float(i['minQty'])
    for k in x['balances']:
        base_asset = k['asset']
        tgt_asset = 'USDT'
        pair = base_asset+tgt_asset
        base_qty = float(k['free'])
        if base_qty==0:
            continue
        else:
            try:
                bid_price = 1
                if min_trade_qty[pair] == 1:
                    tgt_qty = base_qty - base_qty % 1
                    print('Symbol Ask = ', bid_price)
                else:
                    x = base_qty
                    y = min_trade_qty[pair]
                    tgt_qty = floor_rounding(x, y, max_rounding=8)
                    print('Symbol Ask = ', bid_price)
                f = order(side, tgt_qty, pair)
            except:
                continue