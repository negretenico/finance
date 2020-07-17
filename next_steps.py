import bs4 as bs
import datetime as dt
import os
import pandas as pd
from pandas_datareader import data as pdr
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import requests
import yfinance as yf

class DataAcquisition:
    def __init__(self):
        yf.pdr_override()
        style.use('ggplot')

    def save_sp500_tickers(self):
        resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text.replace('.', '-')
            ticker = ticker[:-1]
            tickers.append(ticker)
        with open("sp500tickers.pickle", "wb") as f:
            pickle.dump(tickers, f)
        return tickers

    def get_data_from_yahoo(self,reload_sp500=False):
        if reload_sp500:
            tickers = save_sp500_tickers()
        else:
            with open("sp500tickers.pickle", "rb") as f:
                tickers = pickle.load(f)
        if not os.path.exists('stock_dfs'):
            os.makedirs('stock_dfs')
        start = dt.datetime(2019, 6, 8)
        end = dt.datetime.now()
        for ticker in tickers:
            if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
                df = pdr.get_data_yahoo(ticker, start, end)
                df.reset_index(inplace=True)
                df.set_index("Date", inplace=True)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            else:
                print('Already have {}'.format(ticker))

    def combine_data(self):
        with open('sp500tickers.pickle','rb') as f:
            tickers = pickle.load(f)
        main_df = pd.DataFrame()

        for count,ticker in enumerate(tickers):
            df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
            df.set_index('Date', inplace = True)
            df.rename(columns= {'Adj Close' : ticker}, inplace = True)
            df.drop(['Open','High','Low','Close','Volume'],1,inplace = True)
            if main_df.empty:
                main_df = df
            else:
                main_df  = main_df.join(df, how = 'outer')
        main_df.to_csv('sp500_joined_closes.csv')


    def visualize_data(self):
        df = pd.read_csv('sp500_joined_closes.csv')
        df_corr = df.corr()
        data = df_corr.values
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

        heat_map = ax.pcolor(data,cmap = plt.cm.RdYlGn)

        fig.colorbar(heat_map)

        ax.set_xticks(np.arange(data.shape[1])+.05, minor= False)
        ax.set_yticks(np.arange(data.shape[0])+.05, minor= False)

        ax.invert_yaxis()

        ax.xaxis.tick_top()

        column_labels = df_corr.columns
        row_labels = df_corr.index

        ax.set_xticklabels(column_labels)
        ax.set_yticklabels(row_labels)

        plt.xticks(rotation = 90)

        heat_map.set_clim(-1,1)
        plt.tight_layout()

        fig.savefig('plot.png')
        plt.show()



