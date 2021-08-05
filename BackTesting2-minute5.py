# 볼린저밴드의 하단값에 닿으면 매수, 2프로 수익을 내거나 볼린저배드 상단에 닿거나, -1.8프로 손실이나면 매도하는 백태스팅

# 2021-08-02 수정할점 : 산가격과 판가격이 볼린저값으로 들어가서 14.1111123 이렇게 되는거 고침

# 2021-08-03 수정할점 : 산가격과 판가격이 코인상관없이 소수점1자리까지 나타내는거 고쳐야함

# 2021-08-04 : 산가격과 판가격을 소수점자리의 코인과 1의자리코인 등 구분, 살때는 내림해서 사고, 팔때는 단위가격만큼 반올림해서 팜 , 팔때 순서를 -1.8 손해 - 2프로 수익 - 볼린저 밴드순
import pprint

import pyupbit
import time
import pandas as pd
import talib
import numpy as np
from pandas import  DataFrame
import matplotlib.pyplot as plt



cnt = 9000#받아올 데이터 수
coinlist =["KRW-XEM","KRW-SC","KRW-MLK","KRW-UPP","KRW-BORA"]

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


print(len(coinlist))
for j in range(len(coinlist)):

    size = getsize(coinlist[j])
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
    per = 1

    count = 0  # 거래횟수
    wincount = 0  # 이득인거래수

    target_per = 1.03
    target_sellper = 0.98
    target_buyRSI = 20
    target_sellRSI = 70

    for i, row in df.iterrows():

        if row['rsi'] != None and row['low'] <= row['lower'] and buy == False:
            buy = True
            count += 1


            buyprice =  (int(row['lower']/size))*size
            myasset = 0.9995 * myasset


        elif row['rsi'] != None and buy == True and (row['high'] >= buyprice * target_per or
                                                     row['low'] <= buyprice * target_sellper or
                                                     row['high'] >= row['upper']):

            if  row['low'] <= buyprice * target_sellper:

                sellprice =  (int(buyprice * target_sellper / size)) * size  # 8/5 수정

            elif row['high'] >= buyprice * target_per:

                sellprice = (int(buyprice * target_per / size)) * size  # 8/5 수정


            else:
                sellprice = (int(row['upper'] / size)) * size + size  # 8/5 수정


            myasset = myasset * (1 + (sellprice - buyprice) / buyprice)
            myasset -= myasset * 0.0005

            asset.append(myasset)

            buy = False
            per = per * (1 + (sellprice - buyprice) / buyprice - 0.001)
            if sellprice - buyprice > 0:
                wincount += 1

            #print("Num:", count, "산가격 : ", buyprice, "판가격 : ", sellprice, "퍼센트",sellprice/buyprice)


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





