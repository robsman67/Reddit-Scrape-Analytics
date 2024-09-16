import nltk
from nltk.corpus import stopwords
from collections import Counter
import string

STOP_WORDS = set(stopwords.words('english'))

def clean_text(text):
    words = text.lower().split()
    # Remove punctuation and stopwords and digits
    words = [word.strip(string.punctuation) for word in words
             if word.lower() not in STOP_WORDS and not word.isdigit()]
    return words


def extract_words(file_path):
    all_words = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            current_text = []

            for line in lines:
                line = line.strip()
                if line.startswith("Title:"):
                    # If we have accumulated text, process it
                    if current_text:
                        text_content = ' '.join(current_text)
                        all_words.extend(clean_text(text_content))

                    # Reset for the next post
                    current_text = [line]

                else:
                    current_text.append(line)

            # Process the last accumulated post
            if current_text:
                text_content = ' '.join(current_text)
                all_words.extend(clean_text(text_content))

    except FileNotFoundError:
        print(f"File not found: {file_path}")

    return all_words


#100 more used words
def get_top_words(words_list, top_n=100):
    word_count = Counter(words_list)
    return word_count.most_common(top_n)


def process_subreddit_files(news_subreddits, trade_subreddits):
    all_words_news = []
    all_words_trade = []

    # Process news subreddits
    for subreddit in news_subreddits:
        file_path = f'file/news/{subreddit}'
        try:
            words = extract_words(file_path)
            all_words_news.extend(words)
        except FileNotFoundError:
            print(f"File not found: {file_path}")

    # Process trade subreddits
    for subreddit in trade_subreddits:
        file_path = f'file/trade/{subreddit}'
        try:
            words = extract_words(file_path)
            all_words_trade.extend(words)
        except FileNotFoundError:
            print(f"File not found: {file_path}")

    return (get_top_words(all_words_news), get_top_words(all_words_trade))



# Example usage
list_subreddit_news = ["Bitcoin", "CryptoCurrency", "btc",
                       "CryptoCurrencies", "BitcoinDiscussion", "Ethereum"]

list_subreddit_trade = ["CryptoMarkets", "BitcoinMarkets", "bitcointrading",
                        "CryptoCurrencyTrading", "Ethtrader"]

top_words_news, top_words_trade = process_subreddit_files(
    list_subreddit_news, list_subreddit_trade
)

print("Top words in news:")
for word, count in top_words_news:
    print(f"{word}: {count}")

print("\nTop words in trade:")
for word, count in top_words_trade:
    print(f"{word}: {count}")

