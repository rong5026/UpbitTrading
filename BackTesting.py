
import pyupbit
import time
import pandas as pd
import talib
import numpy as np

cnt = 15000#받아올 데이터 수
coinlist = pyupbit.get_tickers(fiat="KRW")
#["KRW-AXS","KRW-FLOW","KRW-SAND","KRW-XRP","KRW-DOGE","KRW-ETC","KRW-ETH","KRW-BTC", "KRW-XLM","KRW-SNT","KRW-MLK","KRW-WAVES"]
setTime = "minute5"

# 0 1 2 3 4 5 6 7

# def market_unit(price):
#     if price >= 2000000:
#         tick_size = 1000
#     elif price >= 1000000:
#         tick_size = 500
#     elif price >= 500000:
#         tick_size = 100
#     elif price >= 100000:
#         tick_size = 50
#     elif price >= 10000:
#         tick_size = 10
#     elif price >= 1000:
#         tick_size = 5
#     elif price >= 100:
#         tick_size = 1
#     elif price >= 10:
#         tick_size = 0.1
#     else:
#         tick_size = 0.01
#     return tick_size
#

for j in range(len(coinlist)):
    date = None
    dfs = []

    for i in range(cnt // 200 + 1):

        if i < cnt // 200:

            df = pyupbit.get_ohlcv(coinlist[j], to=date, interval=setTime)
            date = df.index[0]
        elif cnt % 200 != 0:
            df = pyupbit.get_ohlcv(coinlist[j], to=date, interval=setTime, count=cnt % 200)
        else:
            break

        dfs.append(df)
        time.sleep(0.1)


    # df가 DataFrame형식으로 저장되어있음
    df = pd.concat(dfs).sort_index()

    # RSI값 저장
    rsi14 = talib.RSI(df['close'], 14)
    df['rsi'] = rsi14

    #볼린저밴드 저장
    #upper, middle, lower = talib.BBANDS(df['close'], timeperiod=10, nbdevup=0.5, nbdevdn=0.5)
    upper, middle, lower = talib.BBANDS(df['close'], 20, 2)
    df['upper'] = upper
    df['middle'] = middle
    df['lower'] = lower


    buyprice = 0.0
    myasset = 10000
    buy = False

    # 총 손익

    per = 1

    count = 0  # 거래횟수
    wincount = 0  # 이득인거래수

    target_buyRSI = 30
    target_sellRSI = 70

    for i, row in df.iterrows():

        if row['rsi'] != None and row['low'] <= row['lower'] and buy == False:
            buy = True
            count += 1
            buyprice =(row['low'])
            myasset = 0.9995 * myasset
            # print("나는 이가격에 샀다 : ",buyprice)


        elif row['rsi'] != None and  buy == True and (row['high'] >buyprice*1.02 or
                                                      row['low']<buyprice*0.982 or
                                                      row['high']>row['upper'] ):



            if row['high'] >= buyprice * 1.02 or row['high'] >= row['upper']:



                sellprice = (row['high'])

            else:
                sellprice = (row['low'])




            myasset = myasset * (1 + (sellprice - buyprice) / buyprice)
            myasset -= myasset * 0.0005
            buy = False
            per = per * (1 + (sellprice - buyprice) / buyprice - 0.001)
            if sellprice - buyprice > 0:
                wincount += 1
            # print("나는 이가격에 팔았다 : ", row['open'])

    print("----------------------------------------------┐")
    print("거래 코인 : ", coinlist[j], " 거래분봉 : ", setTime)
    print("퍼센트 : ", per)
    print("내 자산 : ", myasset)
    print("거래 수 :", count)
    print("이득 :", wincount, " 손해:", count - wincount)
    print("----------------------------------------------┘")


    #df.to_excel(coinlist[j]+".xlsx")



