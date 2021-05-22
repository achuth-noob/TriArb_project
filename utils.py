import math

def floor_rounding(x,y,max_rounding=8):
    x = round(x,max_rounding)
    qty = x - round(x % y, max_rounding)
    z = int(round((math.log(y, 10) * (-1)), 0))
    qty = round(qty, z)
    return qty

# def ALT_flushconvert_BNB():

# print(floor_rounding(0.000156,0.0001,max_rounding=6))

# print('BTCUSDT'.split('USDT')[0])