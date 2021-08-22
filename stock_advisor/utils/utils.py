import pandas as pd

# Project specific imports
from config.config import *



def AddDirectory():
    import os
    path = ROOT_PATH
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)


def RemoveDirectory():
    import shutil
    path = ROOT_PATH

    try:
        shutil.rmtree(path)
    except OSError:
        print("Deletion of the directory %s failed" % path)
    else:
        print("Successfully deleted the directory %s" % path)


#####################
# URLs to get Tickers
#####################
def Get_India_Tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_companies_listed_on_the_National_Stock_Exchange_of_India'

    try:
        # Read page and extract Indian companies
        tickers = pd.read_html(url, flavor='html5lib')
        tickers_list = []

        # Try iterating through all the scrip tables
        # Ignore the ones that don't have Symbol column
        for ticker_element in tickers:
            tickers_list.extend(ticker_element.Symbol.to_list())
    except Exception as e:
        print('ERROR', e)
        pass

    # Remove
    #   NSE from the list and also
    #   \u00A0 (Non-breaking space - Unicode char)
    tickers_list = [s.replace("NSE:\u00A0", "") for s in tickers_list]

    return tickers_list


def Get_SP500_Tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tickers = pd.read_html(url, flavor='html5lib')[0]
    tickers = tickers.Symbol.to_list()
    tickers = [i.replace('.', '-') for i in tickers]
    return tickers
