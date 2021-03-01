import pandas as pd
import yfinance as yf
import matplotlib as plt


#import data to panda dataframe
fname = "reddit_wsb.csv"

def load_panda_csv(v_filename):
  return pd.read_csv(v_filename)





#import the stock ticker info for GME
gme_st = yf.Ticker("GME")
# get the data range for Feb 2021
gme_st_dr = gme_st.history(start="2021-02-01", end="2021-02-28")



#subset the stock prices only of the ticker
#gme_st_dr_sp = gme_st_dr.loc[:,'Date','Open','High']



wsb_data = load_panda_csv(fname)
## add a formatted date column so we can match indexes - wsb_data_formatted = datetime.datetime.strptime(when, '%Y-%m-%d').date()

# Display first 5 rows of newly added csv file
print(wsb_data.head(5))
print(wsb_data.shape)

print(gme_st_dr.head())
