import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np

# Function to show a plot
# param: a pd dataset
# return: plot
def show_num_posts(p_data):
    plt.style.use("ggplot")
    fig, ax = plt.subplots()
    ax.bar(p_data.index,p_data["Num_Posts"],color="black",alpha=.75)
    plt.title("Number of forum posts(Day)",fontsize = 18, alpha = .75)
    plt.xlabel("Date")
    plt.ylabel("Number of Posts")
    ax.xaxis.set_tick_params(reset=True)
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))
    fig.autofmt_xdate(rotation=70)
    plt.show()


# Function to show a plot
# param: a pd dataset
# return: plot
def show_high_low_plot(p_data):
    # # stock prices double fig
    # # create figure and axis objects with subplots()
    plt.style.use("ggplot")
    fig, ax = plt.subplots()
    ax.plot(p_data["High"], 'black', label='High',alpha=.75)
    ax.plot(p_data["Low"], 'red', label='Low',alpha=.75)
    plt.title("High/Low Share Price ($)", fontsize=18, alpha=.75)
    plt.xlabel("Date")
    plt.ylabel("Share Price")
    leg = ax.legend()
    ax.xaxis.set_tick_params(reset=True)
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))
    fig.autofmt_xdate(rotation=70)
    plt.show()


# Function to show a plot
# param: a pd dataset
# return: plot
def show_candlestick(p_data):
    # plotting the data
    plt.style.use("ggplot")
    mc = mpf.make_marketcolors(
        up='g', down='r',
        edge='black',
        wick={'up': 'g', 'down': 'r'})
    s = mpf.make_mpf_style(base_mpl_style="ggplot", marketcolors=mc)
    fig, ax = mpf.plot(p_data, type = 'candle',title='Candlestick chart for GME',ylabel = 'Share Price ($)',returnfig = True,style=s)
    plt.show()


# Function to show a plot
# param: a pd dataset
# return: plot
def show_dual_axis_corr(p_data):
    left_data = p_data["Num_Posts"]
    right_data = p_data["High"]
    plt.style.use("ggplot")
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Num Posts', color="red")
    ax1.plot(left_data, color="red",alpha=.75)
    ax1.tick_params(axis='y', labelcolor="red")
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Share Price ($)', color="black")  # we already handled the x-label with ax1
    ax2.plot(right_data, color="black",alpha=.75)
    ax2.tick_params(axis='y', labelcolor="black")
    plt.title("Number of Reddit Posts/Day/Share Price", fontsize=18, alpha=.75)
    ax1.xaxis.set_tick_params(reset=True)
    ax1.xaxis.set_major_locator(mdates.DayLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))
    fig.autofmt_xdate(rotation=70)
    plt.show()

# Function to show a plot
# param: a pd dataset
# return: wordcloud plot
def show_wc_sentiment(p_data):
    text = " ".join(thetitle for thetitle in p_data)  ## use of for loop in Generator Expression to concat words in title sentences
    # Create stopword list to remove some profaity etc..:
    stopwords = set(STOPWORDS)
    stopwords.update(
        ["let", "will", "got", "m", "go", "one", "u", "dont", "retards", "retard", "fuck", "fucking", "see", "app",
         "part", "back", "make", "let s", "say", "S", "$", "shit", "even", "anyone"])
    wordcloud = WordCloud(stopwords=stopwords, max_words=200).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Sentiment", fontsize=18, alpha=.75)
    plt.show()

    ## now use a pic
    # Generate a word cloud image
    mask = np.array(Image.open("GMELogo.png"))  ## use of Numpy
    wsblogocloud = WordCloud(stopwords=stopwords, mode="RGBA", max_words=100, background_color="white",
                             mask=mask).generate(text)
    ## create coloring from image
    image_colors = ImageColorGenerator(mask)
    plt.figure(figsize=[7, 7])
    plt.imshow(wsblogocloud.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")
    plt.title("Sentiment", fontsize=18, alpha=.75)
    plt.show()



def show_scatter(p_data):
    plt.style.use("ggplot")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x=p_data["Num_Posts"], y=p_data["High"],color='red',alpha=.75)
    plt.xlabel("Number of Posts")
    plt.ylabel("Share Price ($)")
    plt.title("Price/Post Correlation", fontsize=18, alpha=.75)
    plt.locator_params(axis='y', nbins=10)
    plt.locator_params(axis='x', nbins=20)
    plt.show()