import dart_fss as dart
import pandas as pd
import win32com.client

# DART API setting
api_key = 'ebef76b6fa887498f9588ceb2cea36512d042f87'
dart.set_api_key(api_key=api_key)

# 크레온 객체 생성
instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")

# 주식 codeList 반환
kospiList = instCpCodeMgr.GetStockListByMarket(1)
kosdacList = instCpCodeMgr.GetStockListByMarket(2)
codeList = kospiList + kosdacList
testList = codeList[310:320]

for code in testList:
    fs = dart.fs.extract(corp_code=code, bgn_de='20160101')
    df_fs = fs['bs']
    df_ci = fs['cis']
    df_cf = fs['cf']

corp