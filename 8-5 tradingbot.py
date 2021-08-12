# 코인리스트에서 볼린저값을 구해 현재값이 lower보다 낮으면 마켓가로 매수
# upper값보다 크면 마켓가로 매도
# 문제점 : 원하는 매수가에 매수를 못함, 240원에 사서 매도조건이 만족되어 240원에 팔수도잇음
# - 수수료만 내야함

#추가 - > 현재가를 호가창에서 팔고하자하는 가격을 현재가, 그리고 매도할때는 사고하자는 가격을
#현재가로 지정

#추가 -> 조건식에서 매수잔량과 매도잔량이 0이상있을때 매수,매도주문

#7-27 추가 -> 호가창에서 물량이 사고자하거나 팔고자하는 만큼 남아있는지 확인 후 매수,매도

#8-05 추가 -> 매수주문이 들어가는 즉시 목표가격에 지정가주문을 걸고 만약 팔아야하는 시점이 오면 지정가 주문이 채결이 안되어있다면 취소하고 판매

#8-07 추가 -> 매도를 했다면 coin_rebuy에 매도된 가격을 넣고 다음 주문에서 매도한가격보다 낮을때만 매수하도록 변경

#8-12 추가 -> 텔레그렘 봇을 이용하여 거래 내용을 텔레그램으로 정보 받기
import pyupbit
import time
import talib

import datetime
import pprint
import datetime
import telegram

access_key = "bRRqsFuM83Gy3xV3gaFP6cJbDFvkKxL5uIE10lUh"
secret_key = "0LWSzW60DFFB7o3bB8wDuvHvVUgZznkRdsX8JgFv"

ticker = "KRW-XEM"
coinlist =["KRW-ADA","KRW-XEM","KRW-SC","KRW-MLK","KRW-UPP","KRW-BORA"]

coin_rebuy = [0 for i in range(len(coinlist))] # 매도한 후 매도가격보다 낮으면 다시 매수가능
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
            if coin_rebuy[i] ==0 or coin_rebuy[i] > current_price:  #8/8 오류수정

                if current_price < Df['lower'] and orderbook[0]['orderbook_units'][0]['ask_size'] >= krw / current_price:
                    return coinlist[i]
            #print(coinlist[i])
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

telegram_token = "1933596461:AAHAMmGniaCtEUUSdgKYrWnrlsFpXz8-nHo"
telegram_chat_id = 1665697222
bot = telegram.Bot(token = telegram_token)


while True:
    krw = upbit.get_balance("KRW")  # 잔고A
    try:
        if buy == False:

            ticker = findTicker(coinlist)

            buy_result = upbit.buy_market_order(ticker, upbit.get_balance("KRW") * 0.9995)  # B

            bot.sendMessage(chat_id=telegram_chat_id, text="[Buy_Result]")
            bot.sendMessage(chat_id=telegram_chat_id, text=buy_result)

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
            price = int((buy_price*target_per)/size) *size  # 8/7 오류 수정

            if price < buy_price*target_per:
                price +=size


            sell = upbit.sell_limit_order(ticker, price, upbit.get_balance(ticker))   # limitorder . price , count , 8/8 오류 수정
            bot.sendMessage(chat_id=telegram_chat_id, text="[Limit_Sell]")
            bot.sendMessage(chat_id=telegram_chat_id, text=sell)
            coin_rebuy = [0 for i in range(len(coinlist))] # 8/7 추가 coin_rebuy리스트 초기화
            time.sleep(1)

            print("@@@ LIMIT SEll ORDER @@@")
            print("Coin Name : ", ticker)
            print("Limit Sell Price :",price )
            pprint.pprint(sell)
            print("-----------------------------------")


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
                time.sleep(0.5)
                for i in range(len(coinlist)):
                    if coinlist[i] == ticker:
                        m=upbit.get_order(ticker, state="done")[0]['uuid']
                        coin_rebuy[i] = float(upbit.get_order(m)['trades'][0]['price'])

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
                bot.sendMessage(chat_id=telegram_chat_id, text="[Sell_Result]")
                bot.sendMessage(chat_id=telegram_chat_id, text=sell_result)

                pprint.pprint(sell_result)

                time.sleep(1)
                buy = False
                print("My Balance : ", upbit.get_balance("KRW"))
                # A

                for i in range(len(coinlist)):
                    if coinlist[i]==ticker:
                        m = upbit.get_order(ticker, state="done")[0]['uuid']
                        coin_rebuy[i] = float(upbit.get_order(m)['trades'][0]['price']) # 8/7 추가



        time.sleep(0.05)

    except Exception as e:
        print(e)
        print("Error Occurred")
        time.sleep(1)

