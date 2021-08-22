# -*- coding: utf-8 -*-
"""

@author: Softwares Unleashed
"""

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt
import time

import sys

# project specific includes
from utils.utils import *
from utils.communication import *


#########################
# Stock Related Functions
#########################
def Chart(stock, start, interval):
    ticker = yf.Ticker(stock)
    now = dt.datetime.now()
    path = ROOT_PATH_CHART
    stock_historical = ticker.history(start=start, end=now, interval=interval)
    adj_close_px = stock_historical['Close']
    stock_historical['21'] = adj_close_px.rolling(window=21).mean()
    stock_historical['55'] = adj_close_px.rolling(window=55).mean()
    stock_historical['150'] = adj_close_px.rolling(window=150).mean()
    stock_historical[['Close', '21', '55', '150']].plot()
    ''' Save chart to PNG file '''
    plt.savefig(path + str(stock) + '.png')
    ''' Add title to chart '''
    plt.title(str(stock))


def TradingStrategyRSI(stock, start, interval):
    df = yf.download(stock, start=start, interval=interval, threads=False)
    df['MA9'] = df['Adj Close'].rolling(window=9).mean()
    df['MA14'] = df['Adj Close'].rolling(window=14).mean()

    df["MA9"].fillna(0, inplace=True)
    df["MA14"].fillna(0, inplace=True)

    # Check which all rows have MA9 > MA14
    # and mark them as "Buy"
    ma9_gt_ma14_rows = (df['MA9'] > df['MA14'])
    df.loc[ma9_gt_ma14_rows, 'Signal'] = 'Buy'

    ma9_lt_ma14_rows = (df['MA9'] < df['MA14'])
    df.loc[ma9_lt_ma14_rows, 'Signal'] = 'Sell'

    # Fill all rows with "na" with "Wait and See"
    # in the column "Signal"
    df['Signal'].fillna('Wait and see', inplace=True)
    return df


def TradingStrategy(stock, start, interval):
    df = yf.download(stock, start=start, interval=interval, threads=False)
    df['MA21'] = df['Adj Close'].rolling(window=21).mean()
    df['MA55'] = df['Adj Close'].rolling(window=55).mean()
    df['MA150'] = df['Adj Close'].rolling(window=150).mean()
    df["MA21"].fillna(0, inplace=True)
    df["MA55"].fillna(0, inplace=True)
    df["MA150"].fillna(0, inplace=True)
    df.loc[
        (df['MA21'] > df['MA55']) & (df['MA55'] > df['MA150']) & (df['Adj Close'] > df['MA21']), 'Signal'] = 'Buy'
    df.loc[(df['Adj Close'] < df['MA21']), 'Signal'] = 'Sell'
    df['Signal'].fillna('Wait and see', inplace=True)
    return df


# Main function
def main():
    # Scrip Advisor Code begins here.
    j = 0
    dayCondition = True
    while dayCondition:
        pd.options.mode.chained_assignment = None

        # Call Appropriate URL function (India / SP500)
        # tickers = Get_SP500_Tickers()
        tickers = Get_India_Tickers()

        # Set the Start Date to start analysis
        start = "2021-02-01"
        interval = "1h"

        # Add working directory
        AddDirectory()

        # Start from first scrip in list and iterate till end.
        i = 0
        condition = True
        while condition:
            try:
                # Select Stock + NSE / BSE exchange
                tickers.clear()
                tickers.append('SBIN')
                tickers.append('PVR')

                # Original Code - Extract for all tickers passed
                stock = tickers[i] + '.NS'
                print(stock)

                # Sudhanshu's RSI_14 calculation code
                signal = TradingStrategyRSI(stock, start, interval)['Signal']
                # Original Code
                # signal = TradingStrategy(stock, start, interval)['Signal']
                if (signal[len(signal) - 1]) != (signal[len(signal) - 2]):
                    if (signal[len(signal) - 1] == 'Buy') & (signal[len(signal) - 2] == 'Sell'):
                        Chart(stock, start, interval)
                        message = "TestBot-price above average, recommendation buy: " + str(stock)
                        sendemail(stock, message)
                    elif (signal[len(signal) - 1] == 'Sell') & (signal[len(signal) - 2] == 'Buy'):
                        Chart(stock, start, interval)
                        message = "TestBot-price below average, recommendation close position: " + str(stock)
                        sendemail(stock, message)

                # Move to next ticker in list
                i = i + 1
                if i == len(tickers):
                    condition = False
                time.sleep(SLEEP_INTERIM_SEC)
            except Exception as e:
                print('ERROR', e)
                i = i + 1  # Move to next scrip
                pass

        # Remove working directory
        RemoveDirectory()

        print('-------------Finish------------')

        # Number of times to reevaluate results
        j = j + 1
        if j == NUM_OF_REEVALS:
            dayCondition = False
        time.sleep(SLEEP_REEVAL_SECS)


if __name__ == '__main__':
    # create_application_ui()
    main()
