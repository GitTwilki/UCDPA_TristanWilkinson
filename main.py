# IMPORT SECTION
import pandas as pd
import yfinance as yf
import dbMod  # my database module
import visMod  # my visualizations module

# VARS AND SETTINGS SECTION

# set dataframe display options
pd.options.display.max_columns = None
pd.options.display.max_rows = None

fname = "reddit_wsb.csv"    # csv filename
sname = "GME"               # stock id

st_date = "2021-01-28"  # start date of analysis
end_date = "2021-02-20" # end date of analysis

db_api = 'A'  # flag to switch between using DB(D) or yfinance API(A)

# FUNCTIONS SECTION

# Function to read from CSV and return the data
# import data to panda dataframe
# param: a filename
# return: dataframe of the csv
def load_panda_csv(p_filename):
    return pd.read_csv(p_filename)


# Function to read from DB and return the data
# calls dbdata module which connects to the database to get the data for GME
# param: None
# return: dataframe stock data in a pd dataframe indexed by Date(STOCK_DATE)
def load_from_db():
    return dbMod.df_ora_idx

# Function to get data from yfinance API
# import the stock ticker info for GME
# get the data range for Feb 2021
# param: a stock id
# return: subset of the columns we want
def call_yf_api(p_stock):
  gme_st = yf.Ticker(p_stock)
  #gme_st_dr = gme_st.history(start="2021-02-01", end="2021-02-28")
  gme_st_dr = gme_st.history(start=st_date, end=end_date)
  return gme_st_dr[['Open', 'High', 'Low', 'Close']]


# Function to format the sentiment data
# param: the data from the CSV
# return: formatted data
def format_data(p_wsb_data):
    wsb_data_sub = p_wsb_data.loc[:, ['title', 'comms_num', 'body', 'timestamp']]
    ## add a formatted date column so we can match indexes - wsb_data_formatted = datetime.datetime.strptime(when, '%Y-%m-%d').date()
    ## convert column to datetime
    wsb_data_sub['timestamp'] = pd.to_datetime(wsb_data_sub['timestamp'])
    ## add just the date column
    wsb_data_sub["DATE"] = wsb_data_sub['timestamp'].dt.date
    ## set the new column as the index
    wsb_data_inx = wsb_data_sub.set_index("DATE").sort_index()
    # subset only date range of data
    # startdate = pd.to_datetime("2021-01-28").date()  ## Dates for our analysis
    # enddate = pd.to_datetime("2021-02-20").date()
    startdate = pd.to_datetime(st_date).date()
    enddate = pd.to_datetime(end_date).date()
    #return the formatted data
    return wsb_data_inx.loc[startdate:enddate]


# Function to aggregate the sentiment data
# param: formatted data
# return: aggregated data
def aggregate_data(p_wsb_data_final,p_stock_data):
    # pandas series of the aggregate counts
    wsb_agg_data = p_wsb_data_final.groupby(wsb_data_final.index)['title'].count()
    # convert series to DF to merge with stock prices
    wsb_agg_data_df = pd.DataFrame(wsb_agg_data)
    wsb_agg_data_df.rename(columns={'title': 'Num_Posts'}, inplace=True)
    ## merge the post count data with stock price join on the index (date in both cases YYYY-MM-DD)
    mergedDF = pd.merge(wsb_agg_data_df, p_stock_data, how='outer', left_index=True, right_index=True)
    ## fill the blank weekend market data with last close values
    mergedDF['Close'] = mergedDF['Close'].ffill()
    return mergedDF.bfill(axis=1)


# PROG MAIN SECTION

# load the CSV of wallstreet bets reddit data
wsb_data = load_panda_csv(fname)

# load the stock data either from database or api
if db_api == 'A':
    # load the stock data from yfinance API
    stock_data = call_yf_api(sname)
elif db_api == 'D':
    # load the data from the DB
    stock_data = load_from_db()

# call the format data function
wsb_data_final = format_data(wsb_data)

# call the aggregate_data function to merge and agg data
mergedDF = aggregate_data(wsb_data_final,stock_data)

# Final Datasets for Visualization
# mergedDF for dual Axis and Num posts line chart
# stock_data for high/low chart , candlestick
# wsb_data_final for wordcloud sentiment

# VISUALIZATION'S SECTION

# Num posts line chart
visMod.show_num_posts(mergedDF)

visMod.show_high_low_plot(stock_data)

visMod.show_candlestick(stock_data)

visMod.show_dual_axis_corr(mergedDF)

visMod.show_wc_sentiment(wsb_data_final.title)