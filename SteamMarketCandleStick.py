import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime
import time

df = pd.read_csv("data.csv")
url = "https://steamcommunity.com/market/priceoverview/?country=DE&currency=7&appid=730&market_hash_name=AK-47%20%7C%20Slate%20%28Field-Tested%29"
high = 123456.1
low = 0.1

while True:
    response = requests.get(url)
    data = json.loads(response.text)
    current_price = data["lowest_price"].replace("R$ ","").replace(",", ".")
    
    now = datetime.now()
    current_day = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")
    
    if current_time[-2:] == "00":
        d2 = {'date': current_day, 'time': current_time, 'open': current_price, 'close': 0, 'high': current_price, 'low': current_price}
        df2 = pd.DataFrame(d2, index=[0])
        df = pd.concat([df, df2])
        df.to_csv("data.csv", index=False)
        
        current_hour = current_time
        high = current_price
        low = current_price
    
    if current_time[-2:] == "59":
        df.loc[np.logical_and(df['date'] == current_day, df['time'] == current_hour), 'close'] = current_price
        df.to_csv("data.csv", index=False)
    
    if float(current_price) < float(low):
        df.loc[np.logical_and(df['date'] == current_day, df['time'] == current_hour), 'low'] = current_price
        low = current_price
    
    if float(current_price) > float(high):
        df.loc[np.logical_and(df['date'] == current_day, df['time'] == current_hour), 'high'] = current_price
        high = current_price


