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
    p_data.plot(y='Num_Posts', linestyle='dashed')
    plt.title("Number of Reddit Posts/Day")
    plt.xlabel("Date")
    plt.ylabel("Number of Posts")
    plt.legend(loc='upper right', fontsize=10, title="Legend")
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=5)
    plt.show()


# Function to show a plot
# param: a pd dataset
# return: plot
def show_high_low_plot(p_data):
    # # stock prices double fig
    # # create figure and axis objects with subplots()
    fig, ax = plt.subplots()
    ax.plot(p_data["High"], '-b', label='High')
    ax.plot(p_data["Low"], '--r', label='Low')
    # ax.axis('equal')
    leg = ax.legend()
    plt.show()


# Function to show a plot
# param: a pd dataset
# return: plot
def show_candlestick(p_data):
    #mpf.plot(p_data,type='candle',mav=(3,6,9))
    mpf.plot(p_data,type='candle')


# Function to show a plot
# param: a pd dataset
# return: plot
def show_dual_axis_corr(p_data):
    left_data = p_data["Num_Posts"]
    right_data = p_data["High"]
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Num Posts', color=color)
    ax1.plot(left_data, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('Share Price', color=color)  # we already handled the x-label with ax1
    ax2.plot(right_data, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.title("Number of Reddit Posts/Day/Share Price")
    ax1.xaxis.set_tick_params(reset=True)
    ax1.xaxis.set_major_locator(mdates.DayLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))
    fig.autofmt_xdate(rotation=90)
    plt.show()

# Function to show a plot
# param: a pd dataset
# return: wordcloud plot
def show_wc_sentiment(p_data):
    text = " ".join(thetitle for thetitle in p_data)
    # Create stopword list:
    stopwords = set(STOPWORDS)
    stopwords.update(
        ["let", "will", "got", "m", "go", "one", "u", "dont", "retards", "retard", "fuck", "fucking", "see", "app",
         "part", "back", "make", "let s", "say", "S", "$", "shit", "even", "anyone"])
    wordcloud = WordCloud(stopwords=stopwords, max_words=200).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    ## now try with a pic
    # Generate a word cloud image
    mask = np.array(Image.open("GMELogo.png"))

    wsblogocloud = WordCloud(stopwords=stopwords, mode="RGBA", max_words=100, background_color="white",
                             mask=mask).generate(text)
    ## create coloring from image
    image_colors = ImageColorGenerator(mask)

    plt.figure(figsize=[7, 7])
    plt.imshow(wsblogocloud.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")
    plt.show()



