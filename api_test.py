import datetime
import time

import pandas as pd
import pandas.io.sql as pd_sql
import win32com
import win32com.client

import database as db

# 객체 생성
instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")
inCpStockCode = win32com.client.Dispatch("CpUtil.CpStockCode")

kospiList = instCpCodeMgr.GetStockListByMarket(1)
kosdacList = instCpCodeMgr.GetStockListByMarket(2)
codeList = kospiList + kosdacList

testList = codeList[310:320]

print(len(kosdacList))

def marketEye(codeList):
    date = datetime.date.today()
    stock_list = []

    for code in codeList:
        instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")
        instMarketEye.SetInputValue(1, code)
        instMarketEye.SetInputValue(0, (4, 67, 77, 89, 100, 110))

        instMarketEye.BlockRequest()

        stock_dict= {}
        stock_dict['date'] = date
        stock_dict['code'] = code
        stock_dict['name'] = inCpStockCode.CodeToName(code)
        stock_dict['price'] = round(instMarketEye.GetDataValue(0, 0), 2)
        stock_dict['per'] = round(instMarketEye.GetDataValue(1, 0), 2)
        stock_dict['roe'] = round(instMarketEye.GetDataValue(2, 0), 2)
        stock_dict['bps'] = round(instMarketEye.GetDataValue(3, 0), 2)
        stock_dict['profit'] = round(instMarketEye.GetDataValue(4, 0), 2)
        stock_dict['debt'] = round(instMarketEye.GetDataValue(5, 0), 2)
        try:
            stock_dict['pbr'] = round(stock_dict['price'] / stock_dict['bps'], 2)
        except ZeroDivisionError:
            stock_dict['pbr'] = 0

        stock_list.append(stock_dict)
        # time.sleep(1)
        print(code)
        print('{} complite'.format(inCpStockCode.CodeToName(code)))
        print(stock_dict['price'])
        print('-------------')

    return stock_list


result = marketEye(codeList)

df = pd.DataFrame(result, columns=['date', 'code', 'name', 'price', 'per', 'roe', 'bps', 'profit', 'debt', 'pbr'])
print(df)
db = db.Database()
engine = db.return_engine()
# engine = db.create_engine('postgresql://postgres:8121438n@nosangho.asuscomm.com:5432/stock')
pd_sql.to_sql(df, 'test3', con=engine, schema='basic', if_exists='append', index=False)