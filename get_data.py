import pyupbit
import pandas as pd
import time
import talib

import yfinance as yf
from datetime import date
from database import CRUD


class GetData(object):
    def __init__(self, tickers:list):
        """
        셍상지 힘수

        객체생성시 ticker를 list형태로 받기
        """
        self._tickers = tickers

    def history_data(self, start:str, end:str):
        """
        정해진 기간 데이터 수집

        보조지표까지 추가하여 리턴 : DataFrame

        start : 시작 날짜
        end : 마지막 날짜
        """
        dfs = []
        for ticker in self._tickers:
            df = yf.download(ticker, start=start, end=end)
            df['ticker'] = ticker
            dfs.append(df)
        
        df = pd.concat(dfs).sort_index()
        df.index = df.index.strftime("%Y-%m-%d")
        df.reset_index(inplace=True)

        self.add_indicator(df)

        return df
        
    def oneday_data(self):
        """
        하루 데이터 업데이트

        보조지표까지 추가하여 리턴 : DataFrame
        """
        dfs = []
        for ticker in self._tickers:
            df = yf.download(ticker, period='2mo')
            df['ticker'] = ticker
            self.add_indicator(df)
            dfs.append(df)
        
        df = pd.concat(dfs).sort_index()
        df.index = df.index.strftime("%Y-%m-%d")
        ticker_cnt = len(self._tickers)
        df = df.iloc[-ticker_cnt:,:]
        df.reset_index(inplace=True)

        return df

    def add_indicator(self, df):
        """
        보조 지표 추가하여 차트 데이터 리턴 

        atr : ATR
        y_atr : 어제기준 ATR
        macd : MACD
        y_macd : 어제기준 MACD
        ma5 : 5일 이동평균선
        ma20 : 20일 이동평균선
        """
        df['y_close'] = df['Close'].shift(1)
        df['atr'] = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
        df['y_atr'] = df['atr'].shift(1)
        df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        df['y_macd'], df['y_macdsignal'], df['y_macdhist'] = talib.MACD(df['y_close'], fastperiod=12, slowperiod=26, signalperiod=9)
        df['ma5'] = talib.MA(df['Close'], timeperiod=5, matype=0)
        df['ma20'] = talib.MA(df['Close'], timeperiod=20, matype=0)
        
        return df