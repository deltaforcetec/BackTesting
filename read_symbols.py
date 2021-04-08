import csv


def read_csv():
    path_name = 'D:/OneDrive/My Common Computer Backup/Akshay Work/SociaEdge/Python Backtesting/'
    file_name = path_name + 'stock_screener_nyse-nasdaq.csv'

    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        symbols = []
        for row in csv_reader:
            if line_count > 0 and line_count < 200:
                symbols.append(row[0])
                # print(f'{row[0]}')
            line_count += 1

        # print(symbols)
        # print(f'Processed {line_count} lines.')

    return symbols


# symbols = read_csv()
# print(f'Symbols: {symbols}')
