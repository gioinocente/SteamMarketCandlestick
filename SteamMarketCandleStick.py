import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime
import mplfinance as mpf

df = pd.read_csv("data.csv")
url = "https://steamcommunity.com/market/priceoverview/?country=DE&currency=7&appid=730&market_hash_name=AK-47%20%7C%20Slate%20%28Field-Tested%29"

response = requests.get(url)
data = json.loads(response.text)
current_price = data["lowest_price"].replace("R$ ","").replace(",", ".")

now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H:00:00")



df.drop_duplicates(subset=['time'], keep='first', inplace=True)
if df[(df['time'] == current_time)].empty:
    # check if there is a previous row with a different time
    previous_row = df[(df['time'] != current_time)].tail(1)
    if not previous_row.empty:
        previous_row.loc[:,'close'] = current_price
        if float(current_price) < float(previous_row['low'].values[0]):
            previous_row.loc[:, 'low'] = current_price
        if float(current_price) > float(previous_row['high'].values[0]):
            previous_row.loc[:, 'high'] = current_price
        df.update(previous_row)
        df.to_csv("data.csv", index=False)
    # add the new row to the frame
    d2 = {'time': current_time, 'open': current_price, 'close': 0, 'high': current_price, 'low': current_price}
    df2 = pd.DataFrame(d2, index=[0])
    df = pd.concat([df, df2])
    df.to_csv("data.csv", index=False)
    
else:
    # check if the current_price is lower then the low value for the current_hour
    if float(current_price) < float(df.loc[df['time'] == current_time]['low']):
        df.loc[df['time'] == current_time, 'low'] = current_price
        df.to_csv("data.csv", index=False)
    # check if the current_price is higher then the high value for the current_hour
    if float(current_price) > float(df.loc[df['time'] == current_time]['high']):
        df.loc[df['time'] == current_time, 'high'] = current_price
        df.to_csv("data.csv", index=False)
df.loc[df.index[-1], "close"] = float(current_price)

df['time'] = pd.to_datetime(df['time'])
df['close'] = pd.to_numeric(df['close'])
df['open'] = pd.to_numeric(df['open'])
df['high'] = pd.to_numeric(df['high'])
df['low'] = pd.to_numeric(df['low'])
df.set_index('time', inplace=True)
df = df.tail(144)
mpf.plot(df,type='candle',style='charles', savefig='plot.png')

