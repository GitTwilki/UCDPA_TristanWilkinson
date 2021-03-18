# Module to connect to database to get the Stock data
import pandas as pd
import cx_Oracle  # Oracle lib
import config  # my config details for the db connection

connection = None

try:
    # get connection details
    connection = cx_Oracle.connect(
        config.username,
        config.password,
        config.dsn,
        encoding=config.encoding)

    query = "select STOCK_DATE,OPEN,HIGH,LOW,CLOSE from stock_data where stock_date between to_date('2021-01-28', 'YYYY-MM-DD') and to_date('2021-02-20', 'YYYY-MM-DD') order by stock_date"
    df_ora = pd.read_sql(query, con=connection)
    #rename the headings to allow merge with main datasets
    df_ora.rename(columns={'STOCK_DATE': 'Date','OPEN':'Open','HIGH':'High','LOW':'Low','CLOSE':'Close'}, inplace=True)
    df_ora_idx = df_ora.set_index("Date").sort_index()

except cx_Oracle.Error as error:
    print(error)
finally:
    # close the connection
    if connection:
        connection.close()

