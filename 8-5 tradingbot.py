# 코인리스트에서 볼린저값을 구해 현재값이 lower보다 낮으면 마켓가로 매수
# upper값보다 크면 마켓가로 매도
# 문제점 : 원하는 매수가에 매수를 못함, 240원에 사서 매도조건이 만족되어 240원에 팔수도잇음
# - 수수료만 내야함

#추가 - > 현재가를 호가창에서 팔고하자하는 가격을 현재가, 그리고 매도할때는 사고하자는 가격을
#현재가로 지정

#추가 -> 조건식에서 매수잔량과 매도잔량이 0이상있을때 매수,매도주문

#7-27 추가 -> 호가창에서 물량이 사고자하거나 팔고자하는 만큼 남아있는지 확인 후 매수,매도

#8-05 추가 -> 매수주문이 들어가는 즉시 목표가격에 지정가주문을 걸고 만약 팔아야하는 시점이 오면 지정가 주문이 채결이 안되어있다면 취소하고 판매
import pyupbit
import time
import talib

import datetime
import pprint
import datetime

access_key = "bRRqsFuM83Gy3xV3gaFP6cJbDFvkKxL5uIE10lUh"
secret_key = "0LWSzW60DFFB7o3bB8wDuvHvVUgZznkRdsX8JgFv"

ticker = "KRW-XEM"
coinlist =["KRW-ADA","KRW-XEM","KRW-SC","KRW-MLK","KRW-UPP","KRW-BORA"]
buy = False

upbit = pyupbit.Upbit(access_key, secret_key)

def getsize(coinlist):
    current = pyupbit.get_current_price(coinlist)

    if current >=2000000:
        return 1000
    elif current>=1000000:
        return 500
    elif current>=500000:
        return 100
    elif current>=100000:
        return 50
    elif current>=10000:
        return 10
    elif current>=1000:
        return 5
    elif current>=100:
        return 1
    elif current>=10:
        return 0.1
    else:
        return 0.01
def findTicker(coinlist):
    krw = upbit.get_balance("KRW")
    while True:

        for i in range(len(coinlist)):
            df = pyupbit.get_ohlcv(coinlist[i], interval="minute5")

            upper, middle, lower = talib.BBANDS(df['close'], 20, 2)
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
    print("Coin Name :", ticker)
    print("Coin Price : ", buy_price)
    print("Coin balance :", float(balance[0][1]['balance']))

print()


target_per = 1.01
target_sellper = 0.982

while True:
    krw = upbit.get_balance("KRW")  # 잔고A
    try:
        if buy == False:

            ticker = findTicker(coinlist)

            buy_result = upbit.buy_market_order(ticker, krw * 0.9995)  # B
            print("Coin Founded!")
            print()

            time.sleep(1)
            balance = upbit.get_balances(ticker)  # A
            buy_price = float(balance[0][1]['avg_buy_price'])

            print("@@@ Buy Order @@@")
            pprint.pprint(buy_result)
            print("Coin Name : ", ticker, "Buy Price : ", buy_price)
            buy = True

            size = getsize(ticker)
            price = (int(buy_price*target_per)/size) *size

            if price < buy_price*target_per:
                price +=size

            sell = upbit.sell_limit_order(coinlist, price, (krw * 0.9995)/price)   # limitorder . price , count

            print("@@@ LIMIT SEll ORDER @@@")
            print("Coin Name : ",ticker, "Limit Sell Price :",price )
            print("uuid :",sell[0]['uuid'])


        else:
            df = pyupbit.get_ohlcv(ticker, interval="minute5")  # B
            upper, middle, lower = talib.BBANDS(df['close'], 20, 2)
            df['upper'] = upper
            Df = df.iloc[-1]

            orderbook = pyupbit.get_orderbook(tickers=ticker)

            current_bidprice = orderbook[0]['orderbook_units'][0]['bid_price']

            if upbit.get_balance("KRW") >= 5000:
                buy = False
                print("Limit Order Complete!!")
                print()

            elif (current_bidprice <= (buy_price * target_sellper) or
                  current_bidprice >= Df['upper']) and buy == True and orderbook[0]['orderbook_units'][0]['bid_size'] >= upbit.get_balance(ticker):

                #limi order cancel
                print("Limit Order Cancel!!!")
                limit = upbit.get_order(ticker)
                if limit:
                    upbit.cancel_order(limit[0]['uuid'])
                    time.sleep(0.05)
                # A
                sell_result = upbit.sell_market_order(ticker, upbit.get_balance(ticker))
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

