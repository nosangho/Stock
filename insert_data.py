import pyupbit
import pandas as pd
import time
import talib

import yfinance as yf
from datetime import date
from database import CRUD
from get_data import GetData



def insert_chartdata(tickers):

    # data 생성
    data = GetData(tickers)
    # df = data.history_data('2020-03-01', '2021-03-01')
    df = data.oneday_data()
    
    # DB형식에 맞게 data 수정
    dfc = df.copy()
    dfc.drop('Adj Close', axis=1, inplace=True)
    dfc.rename(columns={'Date':'yyyymmdd', 'Open':'opend', 'High':'high', 'Low':'low', 'Close':'closed', 'Volume':'volume'}, inplace=True)
    cols = [col for col in dfc.columns.values]
    columns = ','.join(str(e) for e in cols)

    # DB객체 생성
    db = CRUD()

    # Dataframe 한줄씩 돌면서 데이터 입력
    for i, row in dfc.iterrows():
        yyyymmdd = f"'{row['yyyymmdd']}'"
        ticker = f"'{row['ticker']}'"
        open = round(row['opend'],2)
        high = round(row['high'],2)
        low = round(row['low'],2)
        close = round(row['closed'],2)
        volume = round(row['volume'],2)
        y_close = round(row['y_close'],2)
        atr = round(row['atr'],2)
        y_atr = round(row['y_atr'],2)
        macd = round(row['macd'],2)
        macdsignal = round(row['macdsignal'],2)
        macdhist = round(row['macdhist'], 2)
        y_macd = round(row['y_macd'], 2)
        y_macdsignal = round(row['y_macdsignal'],2)
        y_macdhist = round(row['y_macdhist'], 2)
        ma5 = round(row['ma5'], 2)
        ma20 = round(row['ma20'], 2)
        data = [yyyymmdd, open, high, low, close, volume, ticker, y_close, atr,\
                y_atr, macd, macdsignal, macdhist, y_macd, y_macdsignal, y_macdhist,\
                ma5, ma20]
        data_str = ','.join(str(e) for e in data)

        # DB에 데이터 입력
        db.insertDB('public', 'chart', columns, data_str)


if __name__ == "__main__":
    tickers = ['AAPL', 'NVDA', 'ASML', 'U', 'ABNB' 'DDOG', 'QQQ']
    insert_chartdata(tickers)