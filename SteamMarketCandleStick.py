import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime

df = pd.read_csv("data.csv")
url = "https://steamcommunity.com/market/priceoverview/?country=DE&currency=7&appid=730&market_hash_name=AK-47%20%7C%20Slate%20%28Field-Tested%29"

response = requests.get(url)
data = json.loads(response.text)
current_price = data["lowest_price"].replace("R$ ","").replace(",", ".")

now = datetime.now()
current_day = now.strftime("%Y-%m-%d")
current_time = now.strftime("%H")



if df[(df['date'] == current_day) & (df['time'] == current_time)].empty:
    # check if there is a previous row with a different time
    previous_row = df[(df['date'] == current_day) & (df['time'] != current_time)].tail(1)
    if not previous_row.empty:
        previous_row.loc[:,'close'] = current_price
        df.update(previous_row)
        df.to_csv("data.csv", index=False)
    # add the new row to the frame
    d2 = {'date': current_day, 'time': current_time, 'open': current_price, 'close': 0, 'high': current_price, 'low': current_price}
    df2 = pd.DataFrame(d2, index=[0])
    df = pd.concat([df, df2])
    df.to_csv("data.csv", index=False)
    
else:
    # check if the current_price is lower then the low value for the current_hour
    if float(current_price) < float(df.loc[(df['date'] == current_day) & (df['time'] == current_time)]['low']):
        df.loc[np.logical_and(df['date'] == current_day, df['time'] == current_time), 'low'] = current_price
        df.to_csv("data.csv", index=False)
    # check if the current_price is higher then the high value for the current_hour
    if float(current_price) > float(df.loc[(df['date'] == current_day) & (df['time'] == current_time)]['high']):
        df.loc[np.logical_and(df['date'] == current_day, df['time'] == current_time), 'high'] = current_price
        df.to_csv("data.csv", index=False)