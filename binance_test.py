import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
from utils import *
import BKeys
import math

print('---------------------Process Initiated--------------------')

client = Client(BKeys.API_KEY, BKeys.API_SECRET)
symbols = []
usdt_symbols = []
snap = client.get_orderbook_tickers()

min_trade_qty = {}

# print(snap)
usdt_wallet = client.get_asset_balance('USDT')
# pprint.pprint(client.get_account())
tmp = {}
for i in snap:
    tmp[i['symbol']]=i
# print(tmp)

for i in snap:
    symbols.append(i['symbol'])
    if 'USDT' in i['symbol'] and ('UP' not in i['symbol'] and 'DOWN' not in i['symbol']
    and 'BULL' not in i['symbol'] and 'BEAR' not in i['symbol']):
        usdt_symbols.append(i['symbol'])

for k in client.get_exchange_info()['symbols']:
    for i in k['filters']:
        if i['filterType']=='LOT_SIZE':
            min_trade_qty[k['symbol']] = float(i['minQty'])

# print(min_trade_qty)

def is_suffix(s,symbol):
    return True if symbol[-len(s):]==s else False



def handle_steps(side='BUY',bidask_price=1,min_trade_qty=0.000001,step=0,
                 target_asset='BTC',base_asset='USDT',pair='BTCUSDT'):
    base_qty = float(client.get_asset_balance(base_asset)['free'])
    print('Step {}:Converting {} to {}'.format(step,base_asset,target_asset))
    print("Available {}: ".format(base_asset), base_qty)
    if side == "BUY":
        # bidask_price = lowest ask price
        if min_trade_qty == 1:
            tgt_qty = int(math.floor(float(base_qty/bidask_price)*0.95))
            print('Symbol Ask = ', bidask_price)
        else:
            x = float(base_qty/bidask_price)*0.95
            y = min_trade_qty
            tgt_qty = utils.floor_rounding(x,y,max_rounding=8)
            print('Symbol Ask = ', bidask_price)
    else:
        # Sell testcase
        # bidask_price = bid_price
        if min_trade_qty == 1:
            tgt_qty = base_qty - base_qty%1
            print('Symbol Ask = ', bidask_price)
        else:
            x = base_qty
            y = min_trade_qty
            tgt_qty = utils.floor_rounding(x,y,max_rounding=8)
            print('Symbol Ask = ', bidask_price)
    f = order(side, tgt_qty, pair)
    print('Conversion Successful' if f==True else 'Conversion Failed')
    print()

try:
    while True:
        snap = client.get_orderbook_tickers()
        # print(snap)
        tmp = {}
        for i in snap:
            tmp[i['symbol']] = i
        # print(tmp)
        # print('Data processed')
        for i in range(len(usdt_symbols)):
            for j in range(len(symbols)):
                if 'USDT' in symbols[j]:
                    continue
                try:
                    first_usdt_ask = float(tmp[usdt_symbols[i]]['askPrice'])
                    s = usdt_symbols[i][:-len('USDT')]
                    if is_suffix(s,symbols[j]):
                        symbol_ask = float(tmp[symbols[j]]['askPrice'])
                        # print('1   ------>   ',first_usdt_ask)
                        # print('2   ------>   ',symbol_bid)
                        p = symbols[j][:-len(s)]
                        second_usdt_bid = float(tmp[p+'USDT']['bidPrice'])
                        # print('3   ------>   ',second_usdt_bid)
                        profit = ((((1/first_usdt_ask)/symbol_ask)*second_usdt_bid)-1)*100
                        profit = profit
                        # print(profit)
                        # print(usdt_symbols[i], '->', symbols[j], '->', p + 'USDT')
                        # print('q1 = ',q1,'q2 = ',q2,'q3 = ',q3)

                        if profit>0.1:

                            # Step 1
                            handle_steps(side='BUY', bidask_price=first_usdt_ask,min_trade_qty=0.000001,step=1,
                                         target_asset=usdt_symbols[i].split('USDT')[0],
                                         base_asset='USDT',pair=usdt_symbols[i])

                            # Step 2
                            handle_steps(side='BUY',bidask_price=symbol_ask,min_trade_qty=min_trade_qty[symbols[j]],step=2,
                                         target_asset=symbols[j].split(s)[0],
                                         base_asset=s,pair=symbols[j])

                            # Step 3
                            handle_steps(side='SELL',min_trade_qty=min_trade_qty[p+'USDT'],
                                         step=3,target_asset='USDT',
                                         base_asset=p,pair=p+'USDT')




                            print(usdt_symbols[i],'->',symbols[j],'->',p+'USDT','profit =',profit)
                            tmp1 = float(client.get_asset_balance('USDT')['free'])
                            print('Available USDT: ', tmp1, usdt_symbols[i])
                            print()
                            print()
                            print()
                    else:
                        # print('pofit problem')
                        continue
                        # symbol_bid = tmp[j]['bidPrice']
                        # p = j[:-len(s)]
                        # second_usdt_bid = tmp[p+'USDT']['askPrice']

                except:
                    # print('Missed an opportunity for {}'.format(i))
                    continue
            break
        # print('Cycle finished')
except KeyboardInterrupt:
    print("Press Ctrl+C to terminate while statement")
    pass

# TRADE_SYMBOL = 'ETHUSDT'
# info = client.get_symbol_info('ETHUSDT')
# # TRADE_QUANTITY = info['filters'][2]['minQty']
# TRADE_QUANTITY = 0.005
# def place_order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
#     try:
#         print("sending order")
#         order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
#         print(order)
#     except Exception as e:
#         print("an exception occured - {}".format(e))
#         return False
#     return True
#
#
# def on_open(ws):
#     print('opened connection')
#
# def on_close(ws):
#     print('closed connection')
#
# def on_message(ws, message):
#     flag = place_order(side=SIDE_BUY, quantity=TRADE_QUANTITY, symbol=TRADE_SYMBOL)
#     if flag:
#         print('Order placed')
#     else:
#         print('failed')

# ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
# ws.run_forever()
