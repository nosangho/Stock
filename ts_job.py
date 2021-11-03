from get_data import GetData
import telegram
import json
import schedule
import time

def ts_checker():
    """ 티커별 TS 구해서 텔레그램으로 송출 """

    # ticker 목록 가져오기
    with open('./tickers.json', 'r') as fin:
        params = json.load(fin)
        tickers = params['tickers']

    data = GetData(tickers)
    df = data.oneday_data()

    text = ">>> today's trailing stop <<<\n"
    for i in range(len(df)):
        ticker = df['ticker'][i]
        ts = round(df['ts'][i], 2)

        text = text + f'\nTicker : {ticker}\nTS : {ts}\n\n'

    bot = telegram.Bot(token = '2036874422:AAF8hY2FPqInzbzvteXHYSTRfFq41VFILfY')
    chat_id = '319142645'
    bot.send_message(chat_id=chat_id, text=text)

# main
if __name__ == "__main__":
    print('+++++++++ TS Checker +++++++++')
    print('')
    schedule.every().day.at("17:00").do(ts_checker)

    while True:
        schedule.run_pending()
        time.sleep(1)