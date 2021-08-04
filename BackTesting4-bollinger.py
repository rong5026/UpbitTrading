# 볼린저밴드의 하단값에 닿으면 매수, 2프로 수익을 내거나 볼린저배드 상단에 닿거나, -1.8프로 손실이나면 매도하는 백태스팅
# 2021-08-02 17:00 추가 - while문을 돌려 target_per의 값을 바꾸며 가장 결과가 좋은 값을 찾아냄
# 2021- 08-03 16:00 추가 - 볼린저의 값에 따라 백테스팅 2~3 까지 범위로 테스트

import pprint

import pyupbit
import time
import pandas as pd
import talib
import numpy as np
from pandas import  DataFrame
import matplotlib.pyplot as plt


cnt = 9000#받아올 데이터 수
coinlist =["KRW-DOGE"]

setTime = "minute5"

bollinger_num = 2

maxper =0
result_bollinger = 2

while bollinger_num <=3.1:
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
            time.sleep(0.05)

        # df가 DataFrame형식으로 저장되어있음
        df = pd.concat(dfs).sort_index()

        # RSI값 저장
        rsi14 = talib.RSI(df['close'], 14)
        df['rsi'] = rsi14

        # 볼린저밴드 저장
        # upper, middle, lower = talib.BBANDS(df['close'], timeperiod=10, nbdevup=0.5, nbdevdn=0.5)
        upper, middle, lower = talib.BBANDS(df['close'], 20, bollinger_num)
        df['upper'] = upper
        df['middle'] = middle
        df['lower'] = lower

        buyprice = 0.0
        myasset = 10000
        buy = False

        # 총 손익
        asset = []

        per = 1

        count = 0  # 거래횟수
        wincount = 0  # 이득인거래수

        target_per = 1.02
        target_sellper = 0.982
        target_buyRSI = 20
        target_sellRSI = 70

        for i, row in df.iterrows():

            if row['rsi'] != None and row['low'] <= row['lower'] and buy == False:
                buy = True
                count += 1
                buyprice = (int)(row['lower'] * 10) / 10.0
                myasset = 0.9995 * myasset


            elif row['rsi'] != None and buy == True and (row['high'] >= buyprice * target_per or
                                                         row['low'] <= buyprice * target_sellper or
                                                         row['high'] >= row['upper']):

                if row['low'] <= buyprice * target_sellper:

                    sellprice = buyprice * target_sellper

                elif row['high'] >= row['upper']:
                    sellprice = (int)(row['upper'] * 10) / 10.0

                else:
                    sellprice = buyprice * target_per

                myasset = myasset * (1 + (sellprice - buyprice) / buyprice)
                myasset -= myasset * 0.0005

                asset.append(myasset)

                buy = False
                per = per * (1 + (sellprice - buyprice) / buyprice - 0.001)
                if sellprice - buyprice > 0:
                    wincount += 1



        print("----------------------------------------------┐")
        print("num :", bollinger_num)
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

        df.to_excel(coinlist[j] + ".xlsx")



        #8/3 추가

        if maxper < per:
            maxper = per
            result_bollinger = bollinger_num

        bollinger_num+=0.2


print("가장 best 볼린저값: ",result_bollinger, "그 결과 퍼센트:",maxper )


