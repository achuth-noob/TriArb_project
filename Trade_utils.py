import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
from Exchange_utils import *
from Binance_cache import *
from utils import *
import numpy as np
import math
import time

def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        print('error : ',quantity)
        return False
    return True

def force_market_order(side, tgt_qty, pair):
    try:
        client.create_order(symbol=pair, side=side, type=ORDER_TYPE_MARKET, quantity=tgt_qty)
        print('-------------------Order Placed Successfully------------------')
        return
    except Exception as e:
        print('Exception hit')
        mtgt_qty = tgt_qty - min_trade_qty[pair]
        print('Min Trade Qty: ',min_trade_qty[pair])
        if mtgt_qty<0:
            return
        print(mtgt_qty)
        force_market_order(side,mtgt_qty,pair)
    return True

def ALT_flushconvert_USDT(side='SELL'):
    x = client.get_account()
    for k in x['balances']:
        base_asset = k['asset']
        tgt_asset = 'USDT'
        pair = base_asset+tgt_asset
        base_qty = float(k['free'])
        if base_qty==0:
            continue
        else:
            try:
                bid_price = get_highest_bidprice(pair)
                if min_trade_qty[pair] == 1:
                    tgt_qty = base_qty - base_qty % 1
                    print('Symbol Bid = ', bid_price)
                else:
                    x = base_qty
                    y = min_trade_qty[pair]
                    tgt_qty = floor_rounding(x, y, max_rounding=8)
                    print('Symbol Bid = ', bid_price)
                f = order(side, tgt_qty, pair)
            except:
                continue

# ALT_flushconvert_USDT()
# pprint.pprint(client.get_account()['balances'])
# force_market_order('SELL',0.00810000,'BNTUSDT')
# pprint.pprint(client.get_asset_balance('BNT'))