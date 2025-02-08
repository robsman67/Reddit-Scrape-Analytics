from nltk.corpus import stopwords
from collections import Counter
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

STOP_WORDS = set(stopwords.words('english'))


def clean_text(text, remove_chars=None):
    if remove_chars is None:
        remove_chars = []

    # Create a translation table to remove specific characters
    remove_chars_table = str.maketrans('', '', ''.join(remove_chars))

    # Lowercase the text, remove specific characters, split into words
    words = text.lower().translate(remove_chars_table).split()
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
                        all_words.extend(clean_text(text_content, remove_chars=[':']))

                    # Reset for the next post
                    current_text = [line]

                else:
                    current_text.append(line)

            # Process the last accumulated post
            if current_text:
                text_content = ' '.join(current_text)
                all_words.extend(clean_text(text_content, remove_chars=[':']))

    except FileNotFoundError:
        print(f"File not found: {file_path}")

    return all_words


def get_top_words(words_list, top_n=50):
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

    return (Counter(all_words_news), Counter(all_words_trade))


def create_word_cloud(word_freq, title, output_path):
    # Convert Counter object to a dictionary for wordcloud generation
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(word_freq))

    # Save the word cloud as an image
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the figure to the specified path
    plt.savefig(output_path, format='png')
    plt.close()
