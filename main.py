### Main Functionality
from reddit import RedditScraper
from analyse import sentiment_analysis

if __name__ == "__main__":

    list_subreddit_news = ["Bitcoin", "CryptoCurrency", "btc",
                           "CryptoCurrencies", "BitcoinDiscussion", "Ethereum"
                           ]
    list_subreddit_trade = ["CryptoMarkets", "BitcoinMarkets", "bitcointrading",
                            "CryptoCurrencyTrading", "Ethtrader"]

    # list_subreddit_news = []
    # list_subreddit_trade = []
    start_date = '01-01-24 00:00:00'

    # scraper = RedditScraper()
    # scraper.scrape_subreddits(list_subreddit_news, list_subreddit_trade, start_date)
    # count = scraper.count_number_post_comment(list_subreddit_news, list_subreddit_trade)
    # print(count)

    sentiment_analysis(list_subreddit_news, list_subreddit_trade)
