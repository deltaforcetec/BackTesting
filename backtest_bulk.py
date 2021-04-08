from backtest import *
import datetime


file_path = log_file
fm_date = datetime.datetime(2020, 1, 1)
to_date = datetime.datetime(2021, 3, 1)

# symbols = ['UBER', 'GE']
# symbols = ['TSLA', 'UBER']
symbols = read_csv()
# log_file = "C:/Users/AGV/PycharmProjects/datad/temp/Backtest.csv"
if __name__ == '__main__':
    for symbol in symbols:
        file_name = f'{file_path}{symbol}.csv'
        print(f"************** Symbol: {symbol} **************")

        # Create a cerebro entity
        cerebro = bt.Cerebro()

        #obj.ticker = symbol
        # Add a strategy
        cerebro.addstrategy(TestStrategy)

        # Datas are in a subfolder of the samples. Need to find where the script is
        # because it could have been called from anywhere
        # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        # datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')
        datapath = file_name

        # Create a Data Feed
        data = bt.feeds.YahooFinanceData(
            dataname=symbol,
            # Do not pass values before this date
            fromdate=fm_date,
            # Do not pass values before this date
            todate=to_date,
            # Do not pass values after this date
            reverse=False)

        # print('----')
        # print(data)
        # print('----')
        # Add the Data Feed to Cerebro
        cerebro.adddata(data)

        # Set our desired cash start
        cerebro.broker.setcash(1000.0)

        # Add a FixedSize sizer according to the stake
        cerebro.addsizer(bt.sizers.FixedSize, stake=10)

        # Set the commission
        cerebro.broker.setcommission(commission=0.0)

        # Print out the starting conditions
        val = 'Starting Portfolio Value: %.2f' % cerebro.broker.getvalue()
        print(val)
        # write_to_file("C:/Users/baps/PycharmProjects/datad/UBER.csv", "a", val)

        # Run over everything
        # cerebro.addwriter(bt.WriterFile, out=sys.stdout, csv=True)
        # cerebro.addwriter(bt.WriterFile, out=file_name, csv=True)

        resultdata = cerebro.run(ticker=symbol)
        orderData = resultdata[0]._orders;
        #for order in orderData:
            #if order.status in [order.Completed]:
                #if order.isbuy():
                    #write_to_file(log_file,"a",'BUY EXECUTED,%.2f' % order.executed.price)
                #else:
                    #write_to_file(log_file,"a", 'sell EXECUTED,%.2f' % order.executed.price)
            #elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                #print('Order Canceled/Margin/Rejected')
        # Print out the final result
        # print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        val = 'Final Portfolio Value: %.2f' % cerebro.broker.getvalue()

        print(val)
        #write_to_file("C:/Users/baps/PycharmProjects/datad/UBER.csv", "a", val)

        # write into CSV

        print('FIle Wrote')
