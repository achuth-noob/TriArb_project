import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *

API_KEY = ''
API_SECRET = ''
client = Client(API_KEY, API_SECRET)
# pprint.pprint(client.get_exchange_info()).

# def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
#     try:
#         # print("sending order")
#         order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
#         print('Order placed Successfully')
#     except Exception as e:
#         print("an exception occured - {}".format(e))
#         print('error : ',quantity)
#         return False
#     return True
#
# f = order('SELL',0.0009,'BTCUSDT')
# pprint.pprint(client.get_account())