import pprint

import pyupbit
import time
import talib
import datetime



# 잔고조회 밑 매수

access_key = "bRRqsFuM83Gy3xV3gaFP6cJbDFvkKxL5uIE10lUh"
secret_key = "0LWSzW60DFFB7o3bB8wDuvHvVUgZznkRdsX8JgFv"
#ask 매도 bid 매수


upbit = pyupbit.Upbit(access_key,secret_key)

krw = 9940.924

orderbook = pyupbit.get_orderbook(tickers="KRW-SC")

current_price = orderbook[0]['orderbook_units'][0]['ask_price']

cnt = krw/current_price
print(current_price)
print(krw)
print(cnt)

pprint.pprint(upbit.get_balance("KRW-SC"))
# #CoinList의 볼린저밴드값과 RSI값 프린트
# coinlist = ["KRW-XRP","KRW-AXS","KRW-ADA"]
#
#
# def hong(coinlist):
#
#     while True:
#
#         for i in range(len(coinlist)):
#
#             if coinlist[i]=="KRW-AXS":
#
#                 return coinlist[i]
#
#
# m = hong(coinlist)
#
# print(m)

# while True:
#
#     for i in range(len(coinlist)):
#         df = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute5")
#
#         upper, middle, lower = talib.BBANDS(df['close'], 20, 2)
#         df['upper'] = upper
#         df['middle'] = middle
#         df['lower'] = lower
#
#         # RSI값 저장
#         rsi14 = talib.RSI(df['close'], 14)
#         df['rsi'] = rsi14
#
#         Df = df.iloc[-1]
#
#         print("코인명: ", coinlist[i])
#         print("현재시간: ", datetime.datetime.now())
#         print("Bollinger Bands :",Df['upper'],Df['middle'],Df['lower'] )
#         print("RSI :",Df['rsi'])
#         print()
#
#         df.to_excel("btc.xlsx")
#     break
#
#






#
# for i in range(len(b)):
#     df = pyupbit.get_ohlcv(b[i],interval="minute5")
#     upper, middle, lower = talib.BBANDS(df['close'], 20, 2)
#     df['upper'] = upper
#     df['middle'] = middle
#     df['lower'] = lower
#
#     current_price = pyupbit.get_current_price(b[i])
#
#     Df = df.iloc[-1]
#     if current_price <=Df['lower']:
#         print(b[i])
#     #time.sleep(0.1)



# buy = upbit.get_balances(ticker)
#
# pprint.pprint(buy)
#
# print()
# print()
# pprint.pprint(buy[0])
#
# print()
# print()
# pprint.pprint( float(buy[0][1]['avg_buy_price']))
#
# print(upbit.get_balance("KRW"))
# pprint.pprint( float(buy[0][0]['balance']))
#
# a = upbit.get_order(ticker,state='done')
#
# pprint.pprint(a)



# sell_result = upbit.sell_market_order(ticker,upbit.get_balance(ticker))
# print(sell_result)
#
# buy_price= upbit.get_avg_buy_price(ticker)
#
# print(buy_price)

# if sell_result['error']:
#
#     print(sell_result['error'])
# else:
#     print("실패")



# while True:
#     df = pyupbit.get_ohlcv(ticker, interval="minute5")
#
#     current_price = pyupbit.get_current_price(ticker)
#     upper, middle, lower = talib.BBANDS(df['close'], 20, 2)
#     df['upper'] = upper
#     df['middle'] = middle
#     df['lower'] = lower
#
#     Df = df.iloc[-1]
#     print(Df['upper'])
#
#
#
#     time.sleep(2)

# ret = upbit.get_order("KRW-XRP",state='done')
#
# pprint.pprint(ret)
#
# print(upbit.get_avg_buy_price("KRW-BTC"))
#
# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# if ret[1]['side'] == 'ask':
#     pprint.pprint(float(ret[1]['price']))
#
# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# print(ret[0]['created_at'])
# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# print(upbit.get_avg_buy_price("KRW-XRP"))



# balances = upbit.get_balances()
# pprint.pprint(balances[0])
# print("-----------------------")
#
# pprint.pprint(balances)
#
# print(float(balances[0]['balance']))# KRW 얼마 있는지
# print("-----------------------")
#
# #pprint.pprint(upbit.get_balance("XRP")) # 보유수량
#
# buy_price = upbit.buy_market_order("XRP", 100000)
#
# pprint.pprint(buy_price)
# #
