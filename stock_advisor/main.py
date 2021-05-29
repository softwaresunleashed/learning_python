# -*- coding: utf-8 -*-
"""


@author: Softwares Unleashed
"""

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from functools import partial

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt
import time
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

import sys

# project specific includes
from utils import *






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


########################
# Communication - Email
########################
def sendemail(stock, message):
    user = "stockadvisor.noreply@gmail.com"
    password = "9211hacker"
    to = ["stockadvisor.noreply@gmail.com"]
    subject = "Stock Alert!"
    message = message
    path = ROOT_PATH_CHART
    file = path + str(stock) + '.png'

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.starttls()

    gmail.login(user, password)
    gmail.set_debuglevel(1)

    header = MIMEMultipart()
    header['Subject'] = subject
    header['From'] = user
    header['To'] = ', '.join(to)

    message = MIMEText(message, 'plain')
    header.attach(message)

    if (os.path.isfile(file)):
        attch = MIMEBase('application', 'octet-stream')
        attch.set_payload(open(file, 'rb').read())
        encode_base64(attch)
        attch.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        header.attach(attch)

    gmail.sendmail(user, to, header.as_string())
    gmail.quit()
    print('OK!')


#####################
# URLs to get Tickers
#####################
def Get_India_Tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_companies_listed_on_the_National_Stock_Exchange_of_India'
    tickers = pd.read_html(url, flavor='html5lib')
    tickers_list = []

    try:
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


# Create a Model to handle the calculator's operation
def evaluateExpression(expression):
    """Evaluate an expression."""
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG

    return result


ERROR_MSG = 'ERROR'


# Create a Controller class to connect the GUI and the model
class PyCalcCtrl:
    """PyCalc's Controller."""

    def __init__(self, model, view):
        """Controller initializer."""
        self._evaluate = model
        self._view = view
        # Connect signals and slots
        self._connectSignals()

    def _calculateResult(self):
        """Evaluate expressions."""
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, sub_exp):
        """Build expression."""
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()

        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        """Connect signals and slots."""
        for btnText, btn in self._view.buttons.items():
            if btnText not in {'=', 'C'}:
                btn.clicked.connect(partial(self._buildExpression, btnText))

        self._view.buttons['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)


# Create a subclass of QMainWindow to setup the calculator's GUI
class StockAdvisorUi(QMainWindow):
    """Stock Advisor's View (GUI)."""

    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('Stock Advisor')
        # self.setFixedSize(300, 300)
        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Create the display and the buttons
        self._createSearchPanel()
        self._createButtons()

    def _createSearchPanel(self):
        """Create the display."""

        # Create a container
        self.vbox = QVBoxLayout()

        # Search Label widget
        self.lbl_search = QLabel()
        self.lbl_search.setText('Search Scrip :')
        self.lbl_search.setAlignment(Qt.AlignCenter)

        # Search Edit Box widget
        self.display = QLineEdit()
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignLeft)
        self.display.setReadOnly(False)

        # Add the widgets to the Box layout
        self.vbox.addWidget(self.lbl_search)
        self.vbox.addWidget(self.display)
        self.vbox.addStretch()
        self.generalLayout.addLayout(self.vbox)

    def _createButtons(self):
        """Create the buttons."""

        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        buttons = {'Search': (0, 0),
                   'Clear': (0, 1),
                   'A': (1, 0),
                   'B': (1, 1),
                   'C': (2, 0),
                   'D': (2, 1),
                   'E': (3, 0),
                   'F': (3, 1),
                   }
        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(40, 40)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])

        # Search Button
        self.searchBtn = QPushButton('Search')
        buttonsLayout.addWidget(self.searchBtn)

        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        """Set display's text."""
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        """Get display's text."""
        return self.display.text()

    def clearDisplay(self):
        """Clear the display."""
        self.setDisplayText('')


# UI function
def create_application_ui():
    # Create an instance of QApplication
    stockAdvisorApp = QApplication(sys.argv)

    # Show the Stock Advisor's GUI
    view = StockAdvisorUi()
    view.show()

    # Create instances of the model and the controller
    model = evaluateExpression
    PyCalcCtrl(model=model, view=view)

    # Execute the calculator's main loop
    sys.exit(stockAdvisorApp.exec_())


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
