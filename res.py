import psycopg2
from datetime import date, datetime
from io import *
import csv
import numpy

DB_CONN = 'LOC'    # LOC or AMZ

API_KEY = "c864a2ce0b62316cac5c00e9f8c780b8"


def get_connection(source):
    if source == 'LOC':
        conn = psycopg2.connect("dbname=sociadb user=postgres password=manager")
    elif source == 'AMZ':
        conn = psycopg2.connect(
            database="sociadb",
            user="sociausr",
            password="socia2021#",
            host="sociadb.cpfgxpxus3sj.us-east-2.rds.amazonaws.com",
            port='5432'
        )
    else:
        conn = psycopg2.connect("dbname=sociadb user=postgres password=manager")

    return conn


def exec_sql(stmt, symbol, period_type, statement_name):
    curr_date = str(date.today())
    conn = None
    ret_val = []
    try:
        conn = get_connection(DB_CONN)

        cur = conn.cursor()
        cur.execute(stmt)
        ret_val = cur.fetchall()
        cur.close()
        conn.commit()

    except Exception as error:
        err_str = f'[=== Symbol: {symbol} Period: {period_type} Statement: {statement_name} / Insert Error: {error} ===]\n'
        # print(err_str)
        f = open("D:/temp/" + curr_date + "_LoadLog.log", 'a')
        f.write(err_str)
        f.close()
        pass

    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')

    return ret_val


def exec_dml(stmt, symbol):
    curr_date = str(date.today())
    conn = None
    try:
        conn = get_connection(DB_CONN)

        cur = conn.cursor()
        cur.execute(stmt)
        cur.close()
        conn.commit()

    # except (Exception, psycopg2.DatabaseError) as error:
    #     print(error)
    #     # print(stmt)

    except Exception as error:
        err_str = f'[=== Symbol: {symbol} ===]\n'
        # print(err_str)
        f = open("D:/temp/" + curr_date + "_LoadLog.log", 'a')
        f.write(err_str)
        f.close()
        pass

    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')


def write_to_file(file_name, mode, data):
    with open(file_name, 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(data)
    # f = open(file_name, mode)
    # f.writelines(data)
    # f.close()


def write_to_db(data):
    stmt = f"insert into funda.back_test (symbol, buy_create_date, buy_create_price, buy_executed_date, " \
           f"buy_executed_price, sell_create_date, sell_create_price, sell_executed_date, sell_executed_price, " \
           f"operation_profit_date, operation_profit_gross, operation_profit_net) " \
           f" VALUES (" \
           f"'{data[0]}', '{data[1]}', {data[2]}, '{data[3]}', {data[4]}, '{data[5]}', {data[6]}, " \
           f"'{data[7]}', {data[8]}, '{data[9]}', {data[10]}, {data[10]} )"
    # print(stmt)
    exec_dml(stmt, data[0])

