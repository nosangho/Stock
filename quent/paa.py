# 필요 라이브러리 import
import pandas_datareader as pdr
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import math
import quantstats as qs

# pandas 설정 및 메타데이터 세팅
pd.options.display.float_format = '{:.4f}'.format
pd.set_option('display.max_columns', None)

start_day = datetime(2008,1,1) # 시작일
end_day = datetime(2021,4,30) # 종료일

# RU : Risky Universe
# CU : Cash Universe
# BU : Benchmark Universe
RU = ['SPY','VEA','EEM','AGG'] 
CU = ['LQD','SHY','IEF']
BU = ['^GSPC','^IXIC','^KS11','^KQ11'] # S&P500 지수, 나스닥 지수, 코스피 지수, 코스닥 지수

# 데이터 추출 함수
def get_price_data(RU, CU, BU):
    df_RCU = pd.DataFrame(columns=RU+CU)
    df_BU = pd.DataFrame(columns=BU)
    
    for ticker in RU + CU:
        df_RCU[ticker] = pdr.get_data_yahoo(ticker, start_day - timedelta(days=365), end_day)['Adj Close']  
    
    for ticker in BU:
        df_BU[ticker] = pdr.get_data_yahoo(ticker, start_day - timedelta(days=365), end_day)['Adj Close']  
     
    return df_RCU, df_BU

# 모멘텀 지수 계산 함수
def get_momentum(x):
    temp_list = [0 for i in range(len(x.index))]
    momentum = pd.Series(temp_list, index=x.index)

    try:
        before1 = df_RCU[x.name-timedelta(days=35):x.name-timedelta(days=30)].iloc[-1][RU+CU]
        before3 = df_RCU[x.name-timedelta(days=95):x.name-timedelta(days=90)].iloc[-1][RU+CU]        
        before6 = df_RCU[x.name-timedelta(days=185):x.name-timedelta(days=180)].iloc[-1][RU+CU]        
        before12 = df_RCU[x.name-timedelta(days=370):x.name-timedelta(days=365)].iloc[-1][RU+CU]

        momentum = 12 * (x / before1 - 1) + 4 * (x / before3 - 1) + 2 * (x / before6 - 1) + (x / before12 - 1)
    except Exception as e:
        #print("Error : ", str(e))
        pass
    
    return momentum

# VAA 전략 기준에 맞춰 자산 선택
def select_asset(x):
    asset = pd.Series([0,0], index=['ASSET','PRICE'])
    
    # 공격 자산이 모두 0이상이면, 공격 자산 중 최고 모멘텀 자산 선정
    if x['SPY_M'] > 0 and x['VEA_M'] > 0 and x['EEM_M'] > 0 and x['AGG_M'] > 0:
        max_momentum = max(x['SPY_M'],x['VEA_M'],x['EEM_M'],x['AGG_M'])     
    
    # 공격 자산 중 하나라도 0이하라면, 방어 자산 중 최고 모멘텀 자산 선정
    else :
        max_momentum = max(x['LQD_M'],x['SHY_M'],x['IEF_M'])
    
    asset['ASSET'] = x[x == max_momentum].index[0][:3]
    asset['PRICE'] = x[asset['ASSET']]   
     
    return asset

# 각 자산 군의 데이터 추출
df_RCU, df_BU = get_price_data(RU, CU, BU)

# 각 자산별 모멘텀 지수 계산
mom_col_list = [col+'_M' for col in df_RCU[RU+CU].columns]
df_RCU[mom_col_list] = df_RCU[RU+CU].apply(lambda x: get_momentum(x), axis=1)

# 백테스트할 기간 데이터 추출
df_RCU = df_RCU[start_day:end_day]

# 매월 말일 데이터만 추출(리밸런싱에 사용)
df_RCU = df_RCU.resample(rule='M').last()

# 매월 선택할 자산과 가격
df_RCU[['ASSET','PRICE']] = df_RCU.apply(lambda x: select_asset(x), axis=1)

# 각 자산별 수익률 계산
profit_col_list = [col+'_P' for col in df_RCU[RU+CU].columns]
df_RCU[profit_col_list] = df_RCU[RU+CU].pct_change()

# 매월 수익률 & 누적 수익률 계산
df_RCU['PROFIT'] = 0
df_RCU['PROFIT_ACC'] = 0
df_RCU['LOG_PROFIT'] = 0
df_RCU['LOG_PROFIT_ACC'] = 0

for i in range(len(df_RCU)):
    profit = 0
    log_profit = 0
        
    if i != 0:
        profit = df_RCU[df_RCU.iloc[i-1]['ASSET'] + '_P'].iloc[i]
        log_profit = math.log(profit+1)
    
    df_RCU.loc[df_RCU.index[i], 'PROFIT'] = profit
    df_RCU.loc[df_RCU.index[i], 'PROFIT_ACC'] = (1+df_RCU.loc[df_RCU.index[i-1], 'PROFIT_ACC'])*(1+profit)-1
    df_RCU.loc[df_RCU.index[i], 'LOG_PROFIT'] = log_profit
    df_RCU.loc[df_RCU.index[i], 'LOG_PROFIT_ACC'] = df_RCU.loc[df_RCU.index[i-1], 'LOG_PROFIT_ACC'] + log_profit
    
# 백분율을 %로 표기    
df_RCU[['PROFIT', 'PROFIT_ACC', 'LOG_PROFIT','LOG_PROFIT_ACC']] = df_RCU[['PROFIT', 'PROFIT_ACC', 'LOG_PROFIT','LOG_PROFIT_ACC']] * 100
df_RCU[profit_col_list] = df_RCU[profit_col_list] * 100

# QuantStats의 기본 리포트
qs.reports.basic(df_RCU['PROFIT']/100)