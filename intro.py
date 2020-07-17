import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import mplfinance  as mpf
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

start = dt.datetime(2000,1,1)
end = dt.datetime(2020,6,30)

df = web.DataReader('TSLA','yahoo',start,end)

#resappling we do this to go up
#think like when we have data in seconds but we need data in days

df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volumn = df['Volume'].resample('10D').sum()

print(df_ohlc.head())


# df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)




# df.plot()
# plt.show()

mpf.plot(df_ohlc, type = 'candle',style = 'charles')

axis1 = plt.subplot2grid((6,1),(0,0),rowspan =5, colspan = 1)
axis2 = plt.subplot2grid((6,1),(5,0),rowspan =1, colspan = 1, sharex = axis1)


# axis1.plot(df.index, df['Adj Close'])
#
# axis2.plot(df.index, df['100ma'])
#
# axis2.plot(df.index,df['Volume'])
#
# plt.show()