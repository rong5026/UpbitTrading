# 코인리스트에서 볼린저값을 구해 현재값이 lower보다 낮으면 마켓가로 매수
# upper값보다 크면 마켓가로 매도
# 문제점 : 원하는 매수가에 매수를 못함, 240원에 사서 매도조건이 만족되어 240원에 팔수도잇음
# - 수수료만 내야함

#추가 - > 현재가를 호가창에서 팔고하자하는 가격을 현재가, 그리고 매도할때는 사고하자는 가격을
#현재가로 지정

#추가 -> 조건식에서 매수잔량과 매도잔량이 있을때 매수,매도주문

import pyupbit
import time
import pandas as pd
import talib
import requests
import datetime
import pprint

import datetime




access_key = "bRRqsFuM83Gy3xV3gaFP6cJbDFvkKxL5uIE10lUh"
secret_key = "0LWSzW60DFFB7o3bB8wDuvHvVUgZznkRdsX8JgFv"

ticker = "KRW-XEM"
coinlist = ["KRW-XEM","KRW-SC","KRW-META","KRW-CVC","KRW-BORA","KRW-AXS","KRW-STRK"]
buy = False
hong = [0 for i in range(len(coinlist))]
upbit = pyupbit.Upbit(access_key, secret_key)

def findTicker(coinlist):
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

            #print("##코인이름##: ",coinlist[i],"볼린저값:",Df['lower'])
            if current_price <=Df['lower'] and orderbook[0]['orderbook_units'][0]['ask_size'] > 0 :
                return coinlist[i]

            time.sleep(0.05)

now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d %H:%M:%S')
print("매매 시작!!!")
print("현재시간 :",nowDate)


if upbit.get_balance("KRW") > 1:
    buy = False
    print("매매 상황 : ", buy)
    pprint.pprint(upbit.get_balances())
else:
    buy = True
    balance = upbit.get_balances(ticker)
    buy_price = float(balance[0][1]['avg_buy_price'])
    ticker = "KRW-"+balance[0][1]['currency']
    print("매매 상황 : ", buy)
    print("Name :",ticker)
    print("Coin Price : ",buy_price)
    print("Coin balance :",float(balance[0][1]['balance'] ))


print()

while True:
    krw = upbit.get_balance("KRW")  # 잔고A
    try:
        if buy == False:

            ticker = findTicker(coinlist)

            buy_result = upbit.buy_market_order(ticker, krw * 0.9995)  # B
            print("코인포착!")
            print()


            print("매수주문 보냄")
            time.sleep(1)
            balance = upbit.get_balances(ticker) #A
            buy_price = float(balance[0][1]['avg_buy_price'])

            print("@@@매수@@@")
            pprint.pprint(buy_result)
            print("코인이름 : ", ticker, "구매가격 : ", buy_price)
            buy = True

        else:

            orderbook = pyupbit.get_orderbook(tickers=ticker)

            current_bidprice = orderbook[0]['orderbook_units'][0]['bid_price']

            df = pyupbit.get_ohlcv(ticker, interval="minute5") #B

            upper, middle, lower = talib.BBANDS(df['close'], 20, 2)
            df['upper'] = upper


            Df = df.iloc[-1]

            if (current_bidprice <= (buy_price * 0.982) or
                current_bidprice >= (buy_price * 1.02) or
                current_bidprice >= Df['upper']) and buy == True and orderbook[0]['orderbook_units'][0]['bid_size']>0 :

                sell_result = upbit.sell_market_order(ticker, upbit.get_balance(ticker))
                # A
                print("@@@매도@@@")
                print("현재가 :",current_bidprice, "볼린저Upper :",Df['upper'])
                time.sleep(0.01)
                pprint.pprint(sell_result)


                buy = False
                print("나의 잔고 : ", upbit.get_balance("KRW"))
                #A
        time.sleep(0.1)

    except Exception as e:
        print(e)
        print("오류발생")
        time.sleep(1)



