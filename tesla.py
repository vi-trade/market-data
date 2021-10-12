# import datetime
import ib_insync 
import sqlite3
# from ib_insync import *

ib = ib_insync.IB()
print("---------------------------")
try:
    ib.connect('127.0.0.1', 7497, clientId=1)
except Exception as e:
    print('ОШИБКА: Не удалось подключиться к Trader Workstation.')
    exit(1)

contract = ib_insync.Stock('TSLA', 'SMART', 'USD')

dt = ''
barsList = []
# while True:
for i in range(1):
    bars = ib.reqHistoricalData(
        contract,
        endDateTime=dt,
        durationStr='60 S',
        barSizeSetting='1 secs',
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1)
    if not bars:
        break
    barsList.append(bars)
    dt = bars[0].date
    print(dt)

allBars = [b for bars in reversed(barsList) for b in bars]
# allBars = sum(reversed(barsList),[])
df = ib_insync.util.df(allBars)

print(df)

# save to CSV file
df.to_csv(contract.symbol + '.csv', index=False)

# save to sqlite3 database
con = sqlite3.connect("market-data.sqlite")
df['bar_size']='1 secs'
df.set_index(["date","bar_size"], inplace=True)
print(df.head())
df.to_sql(contract.symbol,con, if_exists="replace" )
con.close()

# save to pickle file
# df.to_pickle(contract.symbol)

