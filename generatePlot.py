import plotly.graph_objects as go
import pandas as pd
import mplfinance as mpf

df = pd.read_csv('data.csv')
df['time'] = pd.to_datetime(df['time'])
df = df.drop(df.index[-1])
df.set_index('time', inplace=True)
mpf.plot(df,type='candle',style='charles', savefig='plot.png')