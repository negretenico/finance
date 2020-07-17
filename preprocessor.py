import numpy as np
import pandas as pd
import pickle
import sys
from collections import Counter
from sklearn import svm, neighbors
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier, RandomForestClassifier


class Preprocessor:
    def __init__(self,threshold):
        self.threshold = threshold
    def process_data_for_labels(self,ticker):
        #we must use 8 instead of 7 to make srue we iterate over 7 days
        df = pd.read_csv('sp500_joined_closes.csv',index_col = 0)
        tickers = df.columns.values.tolist()
        df.fillna(0,inplace = True)

        for i in range(1,self.threshold):
            df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker])/ df[ticker]

        df.fillna(0,inplace = True)
        return tickers, df

    def buy_sell_hold(self, *args):
        cols = [c for c in args]
        requirement = .028
        returnVal = 0
        BUY = 1
        SELL = -1
        for col in cols:
            if col > requirement:
                returnVal =  BUY
                break
            if col < -requirement:
                returnVal = SELL
                break
        return returnVal

    def extract_featureSets(self,ticker):
        tickers, df = self.process_data_for_labels(ticker)

        df['{}_target'.format(ticker)] = list(map(self.buy_sell_hold,*[df['{}_{}d'.format(ticker, i)] for i in range(1,self.threshold, 1)]))
        vals = df['{}_target'.format(ticker)].values.tolist()
        str_vals = [str(i) for i in vals]
        df.fillna(0, inplace = True)

        df = df.replace([np.inf,-np.inf], np.nan)

        df.dropna(inplace = True)

        df_vals = df[[ticker for ticker in tickers]].pct_change()

        df_vals = df_vals.replace([np.inf,-np.inf],0)
        df_vals.fillna(0,inplace = True)

        features = df_vals.values
        labels = df['{}_target'.format(ticker)].values
        return features, labels, df

    def do_ml(self,ticker):
        features,labels,df = self.extract_featureSets(ticker)

        features_train,features_test,labels_train, labels_test = train_test_split(features,labels,test_size = 0.25)

        clf = VotingClassifier([('lsvc', svm.LinearSVC()),('knn',neighbors.KNeighborsClassifier()),('rfor', RandomForestClassifier())])
        clf.fit(features_train,labels_train)

        confidence = clf.score(features_test,labels_test)
        prediction = clf.predict(features_test)
        print("Predicted Spread", Counter(prediction))
        print(confidence)
        return confidence