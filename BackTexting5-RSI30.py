# 볼린저밴드의 하단값에 닿으면 매수, 2프로 수익을 내거나 볼린저배드 상단에 닿거나, -1.8프로 손실이나면 매도하는 백태스팅

# 2021-08-02 수정할점 : 산가격과 판가격이 볼린저값으로 들어가서 14.1111123 이렇게 되는거 고침
import pprint

import pyupbit
import time
import pandas as pd
import talib
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt

cnt = 9000  # 받아올 데이터 수
coinlist = "KRW-XRP"

setTime = "minute5"

date = None
dfs = []

for i in range(cnt // 200 + 1):

    if i < cnt // 200:

        df = pyupbit.get_ohlcv(coinlist, to=date, interval=setTime)
        date = df.index[0]
    elif cnt % 200 != 0:
        df = pyupbit.get_ohlcv(coinlist, to=date, interval=setTime, count=cnt % 200)
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
upper, middle, lower = talib.BBANDS(df['close'], 20, 2)
df['upper'] = upper
df['middle'] = middle
df['lower'] = lower



RSI_under30 = False

while True:
    buyprice = 0.0
    myasset = 10000
    buy = False

    # 총 손익

    day = []
    per = 1

    count = 0  # 거래횟수
    wincount = 0  # 이득인거래수

    target_per = 1.02
    target_sellper = 0.96
    target_buyRSI = 30
    target_sellRSI = 70

    for i, row in df.iterrows():


        if row['rsi'] != None and row['rsi'] <=30 and buy ==False and  RSI_under30 == False:
            RSI_under30 = True

        elif row['rsi'] != None and buy == False and (  row['rsi'] >  target_buyRSI  and RSI_under30 ==True ):
            buy = True
            count += 1
            buyprice = (int)(row['close'] * 10) / 10.0
            myasset = 0.9995 * myasset


        elif row['rsi'] != None and buy == True and ( row['low'] <= buyprice * target_sellper or row['rsi']>target_sellRSI):
            if row['low'] <= buyprice * target_sellper:

                sellprice = buyprice * target_sellper

            elif row['rsi']>target_sellRSI:
                sellprice = row['high']

            # elif row['high'] >= row['upper']:
            #     sellprice = (int)(row['upper'] * 10) / 10.0


            myasset = myasset * (1 + (sellprice - buyprice) / buyprice)
            myasset -= myasset * 0.0005



            buy = False
            RSI_under30 = False
            per = per * (1 + (sellprice - buyprice) / buyprice - 0.001)
            if sellprice - buyprice > 0:
                wincount += 1

            # print("Num:", count, "산가격 : ", buyprice, "판가격 : ", sellprice)

    print("----------------------------------------------┐")
    print("거래 코인 : ", coinlist, " 거래분봉 : ", setTime)
    print("퍼센트 : ", per)
    print("내 자산 : ", myasset)
    print("거래 수 :", count)
    print("이득 :", wincount, " 손해:", count - wincount)
    print("----------------------------------------------┘")



    # df.to_excel(coinlist+".xlsx")
    break


