# 볼린저밴드의 하단값에 닿으면 매수, 2프로 수익을 내거나 볼린저배드 상단에 닿거나, -1.8프로 손실이나면 매도하는 백태스팅
import pprint

import pyupbit
import time
import pandas as pd
import talib
import numpy as np
from pandas import  DataFrame
import matplotlib.pyplot as plt


cnt = 9000#받아올 데이터 수
coinlist =["KRW-MLK","KRW-BORA","KRW-XEM","KRW-SC","KRW-BCHA","KRW-ETH","KRW-MED","KRW-BTC","KRW-LSK","KRW-ETC","KRW-REP","KRW-XRP","KRW-FLOW","KRW-DOGE","KRW-STRK","KRW-SXP","KRW-DOT","KRW-UPP","KRW-ANKR","KRW-ELF","KRW-SAND","KRW-BTT"]

setTime = "minute5"

# 이전 데이터를 엑셀파일에 저장하는 방법2
# dfs=[]
# df = pyupbit.get_ohlcv("KRW-XRP",interval="minute5")
# dfs.append(df)
#
# for i in range(10):
#     df= pyupbit.get_ohlcv("KRW-XRP",interval="minute5",to=df.index[0])
#     dfs.append(df)
#     time.sleep(0.1)
#
# df= pd.concat(dfs).sort_index()

print(len(coinlist))
for j in range(len(coinlist)):

    # df = pyupbit.get_ohlcv(coinlist[j],interval=setTime, count=00)
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
        time.sleep(0.05)




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
    asset = []
    day=[]
    per = 1

    count = 0  # 거래횟수
    wincount = 0  # 이득인거래수

    target_per = 1.1
    target_buyRSI = 20
    target_sellRSI = 70

    for i, row in df.iterrows():

        if row['rsi'] != None and row['rsi'] <= target_buyRSI and buy == False:
            buy = True
            count += 1
            buyprice =row['lower']
            myasset = 0.9995 * myasset
            # print("나는 이가격에 샀다 : ",buyprice)


        elif row['rsi'] != None and  buy == True and row['high'] >= buyprice*target_per:


            sellprice = buyprice*target_per



            myasset = myasset * (1 + (sellprice - buyprice) / buyprice)
            myasset -= myasset * 0.0005

            asset.append(myasset)
            day.append(str(row.name))

            buy = False
            per = per * (1 + (sellprice - buyprice) / buyprice - 0.001)
            if sellprice - buyprice > 0:
                wincount += 1
            # print("나는 이가격에 팔았다 : ", row['open'])

    print("----------------------------------------------┐")
    print("num :",j+1)
    print("거래 코인 : ", coinlist[j], " 거래분봉 : ", setTime)
    print("퍼센트 : ", per)
    print("내 자산 : ", myasset)
    print("거래 수 :", count)
    print("이득 :", wincount, " 손해:", count - wincount)
    print("----------------------------------------------┘")


    # x_values = asset
    #
    # plt.plot(x_values)
    # plt.show()

    #df.to_excel(coinlist[j]+".xlsx")





