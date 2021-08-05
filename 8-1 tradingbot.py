import pyupbit
import time
import talib

import datetime
import pprint
import datetime

access_key = "bRRqsFuM83Gy3xV3gaFP6cJbDFvkKxL5uIE10lUh"
secret_key = "0LWSzW60DFFB7o3bB8wDuvHvVUgZznkRdsX8JgFv"

ticker = "KRW-XEM"
coinlist = ["KRW-XEM", "KRW-SC", "KRW-MLK", "KRW-UPP", "KRW-BORA"]
buy = False

upbit = pyupbit.Upbit(access_key, secret_key)


def findTicker(coinlist):
    krw = upbit.get_balance("KRW")
    while True:

        for i in range(len(coinlist)):
            df = pyupbit.get_ohlcv(coinlist[i], interval="minute5")

            upper, middle, lower = talib.BBANDS(df['close'], 20, 2)
            df['upper'] = upper
            df['middle'] = middle
            df['lower'] = lower
            Df = df.iloc[-1]

            orderbook = pyupbit.get_orderbook(tickers=coinlist[i])

            current_price = orderbook[0]['orderbook_units'][0]['ask_price']

            if current_price < Df['lower'] and orderbook[0]['orderbook_units'][0]['ask_size'] >= krw / current_price:
                return coinlist[i]

            time.sleep(0.05)


now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d %H:%M:%S')
print("Trading STart!!!")
print("Time :", nowDate)

if upbit.get_balance("KRW") > 1:
    buy = False
    print("Trading Situation : ", buy)
    pprint.pprint(upbit.get_balances())
else:
    buy = True
    balance = upbit.get_balances(ticker)
    buy_price = float(balance[0][1]['avg_buy_price'])
    ticker = "KRW-" + balance[0][1]['currency']
    print("Trading Situation : ", buy)
    print("COin Name :", ticker)
    print("Coin Price : ", buy_price)
    print("Coin balance :", float(balance[0][1]['balance']))

print()

while True:
    krw = upbit.get_balance("KRW")  # 잔고A
    try:
        if buy == False:

            ticker = findTicker(coinlist)

            buy_result = upbit.buy_market_order(ticker, krw * 0.9995)  # B
            print("Coin Founded!")
            print()

            print("Seding Buy Order")
            time.sleep(1)
            balance = upbit.get_balances(ticker)  # A
            buy_price = float(balance[0][1]['avg_buy_price'])

            print("@@@ Buy Order @@@")
            pprint.pprint(buy_result)
            print("Coin Name : ", ticker, "Buy Price : ", buy_price)
            buy = True

        else:
            df = pyupbit.get_ohlcv(ticker, interval="minute5")  # B
            upper, middle, lower = talib.BBANDS(df['close'], 20, 2)
            df['upper'] = upper
            Df = df.iloc[-1]

            orderbook = pyupbit.get_orderbook(tickers=ticker)

            current_bidprice = orderbook[0]['orderbook_units'][0]['bid_price']

            if (current_bidprice <= (buy_price * 0.982) or
                current_bidprice >= (buy_price * 1.02) or
                current_bidprice >= Df['upper']) and buy == True and orderbook[0]['orderbook_units'][0][
                'bid_size'] >= upbit.get_balance(ticker):
                sell_result = upbit.sell_market_order(ticker, upbit.get_balance(ticker))
                # A
                print("@@@ Sell Order @@@")
                print("Present Price :", current_bidprice, "Bollinger Upper :", Df['upper'])
                time.sleep(0.01)
                pprint.pprint(sell_result)

                time.sleep(0.5)
                buy = False
                print("My Balance : ", upbit.get_balance("KRW"))
                # A
        time.sleep(0.05)

    except Exception as e:
        print(e)
        print("Error Occurred")
        time.sleep(1)

