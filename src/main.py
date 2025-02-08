from reddit import RedditScraper
from analyse import sentiment_analysis
from graph import process_and_plot_boxplots
from word_counter import process_subreddit_files, create_word_cloud

if __name__ == "__main__":

    list_subreddit_news = ["Bitcoin", "CryptoCurrency", "btc",
                           "CryptoCurrencies", "BitcoinDiscussion", "Ethereum"
                          ]
    list_subreddit_trade = ["CryptoMarkets", "BitcoinMarkets", "bitcointrading",
                            "CryptoCurrencyTrading", "Ethtrader"]

    start_date = '01-01-24 00:00:00'

    scraper = RedditScraper()
    scraper.scrape_subreddits(list_subreddit_news, list_subreddit_trade, start_date)
    # count = scraper.count_number_post_comment(list_subreddit_news, list_subreddit_trade)
    # print(count)

    sentiment_analysis(list_subreddit_news, list_subreddit_trade)

    news_output_directory = 'file/analyse_news_charts/'
    process_and_plot_boxplots('file/analyse_news/', news_output_directory, 'news', whis=2.0)

    trade_output_directory = 'file/analyse_trade_charts/'
    process_and_plot_boxplots('file/analyse_trade/', trade_output_directory, 'trade',
                              whis=2.0)

    word_freq_news, word_freq_trade = process_subreddit_files(list_subreddit_news, list_subreddit_trade)

    # Store word cloud for news
    print("Saving word cloud for news...")
    create_word_cloud(word_freq_news, "Top Words in News Subreddits", "../file/analyse_news_charts/news_wordcloud.png")

    # Store word cloud for trade
    print("Saving word cloud for trade...")
    create_word_cloud(word_freq_trade, "Top Words in Trade Subreddits",
                      "../file/analyse_trade_charts/trade_wordcloud.png")
