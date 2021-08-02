import pyupbit
import time
import pandas as pd
import talib
import requests
import datetime
import pprint




access_key = "bRRqsFuM83Gy3xV3gaFP6cJbDFvkKxL5uIE10lUh"
secret_key = "0LWSzW60DFFB7o3bB8wDuvHvVUgZznkRdsX8JgFv"

ticker = "KRW-XRP"
buy = False

upbit = pyupbit.Upbit(access_key, secret_key)

print("매매 시작!!!")



if upbit.get_balance("KRW") > 1:
    buy = False
    print("매매 상황 : ", buy, "현재가 :", pyupbit.get_current_price(ticker))
else:
    buy = True
    balance = upbit.get_balances(ticker)
    buy_price = float(balance[0][1]['avg_buy_price'])
    print("매매 상황 : ", buy , "Name :",ticker, "Coin Price : ",buy_price, "Coin balance :",float(balance[0][1]['balance']) )



while True:

    try:
        df = pyupbit.get_ohlcv(ticker,interval="minute5")

        current_price = pyupbit.get_current_price(ticker)

        upper, middle, lower = talib.BBANDS(df['close'], 20, 2)
        df['upper'] = upper
        df['middle'] = middle
        df['lower'] = lower

        Df = df.iloc[-1]
        krw = upbit.get_balance("KRW")

        if current_price <= Df['lower'] and buy == False:

            buy = True


            buy_result = upbit.buy_market_order(ticker, krw * 0.9995)

            balance = upbit.get_balances(ticker)
            buy_price = float(balance[0][1]['avg_buy_price'])

            print("현재가격 : ", current_price)
            print("@@@매수@@@")
            pprint.pprint(buy_result)
            print("코인이름 : ", ticker, "구매가격 : ", buy_price)

        elif (current_price <= (buy_price *0.982) or
              current_price >= (buy_price*1.02) or
              current_price >= Df['upper']) and buy == True:

            sell_result = upbit.sell_market_order(ticker,upbit.get_balance(ticker))

            print("@@@매도@@@")
            pprint.pprint(sell_result)

            buy = False
            print("나의 잔고 : ",upbit.get_balance("KRW"))



        time.sleep(0.2)

    except Exception as e:
        print(e)

        time.sleep(1)










