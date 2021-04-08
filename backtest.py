from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
from re import search
# Import the backtrader platform
import backtrader as bt

import pandas as pd

import yfinance as yf

# from write_to_file import *

from res import *

from read_symbols import *

log_file = "C:/Users/AGV/PycharmProjects/datad/temp/Backtest.csv"
csvrow = [None]*11
csvFilerows = [["Ticker","BUY CREATE DATE","BUY CREATE PRICE","BUY EXECUTED DATE","BUY EXECUTED PRICE","SELL CREATE DATE","SELL CREATE PRICE","SELL EXECUTED DATE","SELL EXECUTED PRICE","OPERATION PROFIT DATE","OPERATION PROFIT PRICE"]]
dbFilerows = []
# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
    )

    def log(self, txt, numprice, file_name, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        ticker = self.datas[0]._dataname
        global csvrow
        global csvFilerows
        global dbFilerows
        csvrow[0] = ticker
        if 'BUY EXECUTED' in txt:
            csvrow[3] = dt.isoformat()
            csvrow[4] = str(numprice)
        elif 'SELL EXECUTED' in txt:
            csvrow[7] = dt.isoformat()
            csvrow[8] = str(numprice)
        elif 'SELL CREATE' in txt:
            csvrow[5] = dt.isoformat()
            csvrow[6] = str(numprice)
        elif 'BUY CREATE' in txt:
            csvrow[1] = dt.isoformat()
            csvrow[2] = str(numprice)
        elif 'OPERATION PROFIT' in txt:
            csvrow[9] = dt.isoformat()
            csvrow[10] = str(numprice)
            # print(csvrow)
            csvFilerows.append(csvrow)
            dbFilerows.append(csvrow)
            write_to_file(file_name, "a", csvFilerows)
            write_to_db(csvrow)
            csvrow = [None] * 11
        elif 'Order Canceled/Margin/Rejected' in txt:
            write_to_file(file_name, "a", csvFilerows)
            write_to_db(csvrow)
            csvrow = [None] * 11
        else:
            write_to_file(file_name, "a", csvFilerows)
            write_to_db(csvrow)
            csvrow = [None] * 11

        log_txt = f'{dt.isoformat()},{txt}\n'
        #print('aaaa======>'+self.ticker)




    def __init__(self):
        #print('=====>'+str(self.ticker))
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close


        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

        # Indicators for the plotting show
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
                                            subplot=True)
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0], plot=False)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            csvline = []
            if order.isbuy():
                # self.log(
                #     'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                #     (order.executed.price,
                #      order.executed.value,
                #      order.executed.comm), file_name=log_file)

                self.log('BUY EXECUTED,%.2f' % order.executed.price,order.executed.price, file_name=log_file)

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

            else:  # Sell
                # self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                #          (order.executed.price,
                #           order.executed.value,
                #           order.executed.comm), file_name=log_file)
                self.log('SELL EXECUTED,%.2f' % order.executed.price,order.executed.price, file_name=log_file)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print(f'{self.datas[0]._dataname}: Order Canceled/Margin/Rejected')
            pass

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        # self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))
        self.log('OPERATION PROFIT,%.2f,%.2f' % (trade.pnl, trade.pnlcomm),trade.pnlcomm, file_name=log_file)

    def next(self):
        # Simply log the closing price of the series from the reference
        # Commented below as we don't want the Close lines in the logs
        # self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE,%.2f' % self.dataclose[0],self.dataclose[0], file_name=log_file)

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE,%.2f' % self.dataclose[0],self.dataclose[0], file_name=log_file)
                # print(f'{self.dataclose[0]}, {self.dataclose[1]}, {self.dataclose[2]}, {self.dataclose[3]}, {self.dataclose[4]}')

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

