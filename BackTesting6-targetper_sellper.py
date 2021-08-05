

# 목표 퍼센트와 손절 퍼센트에 따라 1분봉 데이터를 통해 테스트
import pprint

import pyupbit
import time
import pandas as pd
import talib
import numpy as np
from pandas import  DataFrame
import matplotlib.pyplot as plt


cnt = 9000#받아올 데이터 수
coinlist =["KRW-DOGE","KRW-XRP","KRW-ADA","KRW-AXS","KRW-XEM","KRW-SC","KRW-MLK","KRW-UPP","KRW-BORA"]
result ={}

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

def tradeStart(coinlist,df,target_per,target_sellper,target_buyRSI,target_sellRSI):

    count = 0
    buyprice = 0.0
    buy = False

    # 총 손익
    per = 1

    count = 0  # 거래횟수
    wincount = 0  # 이득인거래수
    size = getsize(coinlist)

    for i, row in df.iterrows():

        # 볼린저하단에 닿으면 매수
        if row['rsi'] != None and row['low'] <= row['lower'] and buy == False:
            buy = True
            count += 1
            buyprice = (int(row['lower'] / size)) * size

        #구매를 했으며 볼린저 상단에 닿거나, target_sellper 보다 가격이 낮아지거나, target_per 만큼 상승했다면 매도주문
        elif row['rsi'] != None and buy == True and (row['high'] >= buyprice * target_per or
                                                     row['low'] <= buyprice * target_sellper or
                                                     row['high'] >= row['upper']):
            # 판매가격을 설정
            if row['low'] <= buyprice * target_sellper:

                sellprice = (int(buyprice * target_sellper / size)) * size  # 8/5 수정

            elif row['high'] >= buyprice * target_per:

                if buyprice * target_per % size == 0:
                    sellprice = (int(buyprice * target_per / size)) * size  # 8/5 수정
                else:
                    sellprice = (int(buyprice * target_per / size)) * size + size

            else:
                sellprice = (int(row['upper'] / size)) * size  # 8/5 수정


            buy = False
            per = per * (1 + (sellprice - buyprice) / buyprice - 0.001)
            if sellprice - buyprice > 0:
                wincount += 1

            #print("Num:", count, "산가격 : ", buyprice, "판가격 : ", sellprice, "퍼센트",sellprice/buyprice)

    print("----------------------------------------------┐")
    print("거래 코인 : ", coinlist,"target_per:",target_per, "target_sellper:",target_sellper)
    print("퍼센트 : ", per)
    print("거래 수 :", count)
    print("이득 :", wincount, " 손해:", count - wincount)
    print("----------------------------------------------┘")

    return per


for j in range(len(coinlist)):

    # 원하는 날짜만큼 데이터를 불러옴
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


    target_buyRSI = 30
    target_sellRSI = 70

    best_target_per=0
    best_target_sellper=0
    best_per = 0

    Target_per = [k / 1000.0 for k in range(1010, 1052, 2)]
    Target_sellper = [k / 1000.0 for k in range(960, 992, 2)]

    for target_per in Target_per:
        for target_sellper in Target_sellper:
            per = tradeStart(coinlist[j], df, target_per, target_sellper, target_buyRSI, target_sellRSI)

            if per > best_per:
                best_target_sellper = target_sellper
                best_target_per = target_per
                best_per = per

    print("코인이름",coinlist[j])
    print("가장 좋은 목표가 :",best_target_per)
    print("가장 좋은 판매목표:",best_target_sellper)
    print("결과 :",best_per)
    result[coinlist[j]] = [best_target_per,best_target_sellper,best_per]



for i in coinlist:
    print(result[i])
    #df.to_excel(coinlist[j]+".xlsx")





